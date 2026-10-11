#!/usr/bin/env python3
"""Evaluate a fixed-budget small-component branch beside the deployed top-4.

The preprocessing path is the deployed Python reference through the post-cleanup,
post-min-run mask.  The main branch remains area-ranked top-4 with area >= 16.
An experimental branch ranks only smaller remaining components, expands their
boxes to a configurable minimum size, and applies NMS against both the main boxes
and previously accepted small boxes.  This is Python diagnostic evidence, not an
RTL implementation or an acceptance result.  Optional final-four policies compare
fixed 3+1 and 2+2 quotas with an RTL-friendly unified eight-to-four arbitration.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference


SCORERS = ("contrast_fill", "area", "peak_difference")
MAX_FIXED_BUDGET = 8
FINAL4_STRATEGIES = ("main3_small1", "main2_small2", "internal8_to4")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_development_inputs(video: Path, annotations: Path, clip_id: str,
                                catalog_path: Path) -> dict[str, object]:
    """Fail closed unless the inputs are a cataloged train/val VIRAT clip."""
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    matches = [entry for entry in catalog.get("clips", [])
               if entry.get("clip_id") == clip_id]
    if len(matches) != 1:
        raise ValueError("clip must appear exactly once in the development catalog")
    clip = matches[0]
    if clip.get("split") not in {"train", "val"}:
        raise ValueError("only cataloged train/val clips are allowed; holdout/blind is forbidden")
    if digest(video) != clip.get("video_sha256"):
        raise ValueError("video hash does not match the cataloged development clip")
    canonical_annotations = catalog_path.parent / "annotations.csv"
    if not canonical_annotations.is_file():
        raise ValueError("canonical development annotations are missing")
    if digest(annotations) != digest(canonical_annotations):
        raise ValueError("annotations hash does not match the development catalog export")
    return clip


def validate_budget(main_slots: int, total_budget: int) -> None:
    if main_slots < 1 or total_budget < main_slots or total_budget > MAX_FIXED_BUDGET:
        raise ValueError(f"candidate budget must satisfy 1 <= main_slots <= total_budget <= {MAX_FIXED_BUDGET}")


def inclusive_iou(left: tuple[int, int, int, int],
                  right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = max(0, left[2] - left[0] + 1) * max(0, left[3] - left[1] + 1)
    right_area = max(0, right[2] - right[0] + 1) * max(0, right[3] - right[1] + 1)
    union = left_area + right_area - intersection
    return intersection / union if union else 0.0


@dataclass(frozen=True)
class Component:
    label: int
    area: int
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    fill_ratio: float
    mean_difference: float
    peak_difference: int

    @property
    def box(self) -> tuple[int, int, int, int]:
        return self.xmin, self.ymin, self.xmax, self.ymax


def extract_components(mask: np.ndarray, difference: np.ndarray) -> list[Component]:
    """Return all 8-connected post-min-run components with interpretable stats."""
    if mask.shape != difference.shape:
        raise ValueError("mask and difference shapes differ")
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (mask != 0).astype(np.uint8), connectivity=8)
    found = []
    for label in range(1, count):
        x, y, width, height, area = (int(value) for value in stats[label])
        pixels = difference[labels == label]
        found.append(Component(
            label=label, area=area, xmin=x, ymin=y,
            xmax=x + width - 1, ymax=y + height - 1,
            fill_ratio=area / (width * height),
            mean_difference=float(pixels.mean()),
            peak_difference=int(pixels.max()),
        ))
    return found


def expand_minimum_box(box: tuple[int, int, int, int], minimum_width: int,
                       minimum_height: int, image_width: int,
                       image_height: int) -> tuple[int, int, int, int]:
    """Center-expand an inclusive box, shifting at image edges without shrinking."""
    if minimum_width < 1 or minimum_height < 1:
        raise ValueError("minimum box dimensions must be positive")
    x0, y0, x1, y1 = box
    target_width = min(image_width, max(x1 - x0 + 1, minimum_width))
    target_height = min(image_height, max(y1 - y0 + 1, minimum_height))
    center_x, center_y = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    new_x0 = max(0, min(int(math.floor(center_x - (target_width - 1) / 2.0)),
                        image_width - target_width))
    new_y0 = max(0, min(int(math.floor(center_y - (target_height - 1) / 2.0)),
                        image_height - target_height))
    return (new_x0, new_y0, new_x0 + target_width - 1,
            new_y0 + target_height - 1)


def expand_top_anchored_box(box: tuple[int, int, int, int], minimum_width: int,
                            minimum_height: int, top_margin: int,
                            image_width: int,
                            image_height: int) -> tuple[int, int, int, int]:
    """Expand inclusively, keeping the raw component near the new box top."""
    if minimum_width < 1 or minimum_height < 1 or top_margin < 0:
        raise ValueError("invalid top-anchored box parameters")
    x0, y0, x1, y1 = box
    target_width = min(image_width, max(x1 - x0 + 1, minimum_width))
    target_height = min(image_height, max(y1 - y0 + 1, minimum_height))
    center_x = (x0 + x1) / 2.0
    new_x0 = max(0, min(int(math.floor(center_x - (target_width - 1) / 2.0)),
                        image_width - target_width))
    new_y0 = max(0, min(y0 - top_margin, image_height - target_height))
    expanded = (new_x0, new_y0, new_x0 + target_width - 1,
                new_y0 + target_height - 1)
    if not (expanded[0] <= x0 <= x1 <= expanded[2] and
            expanded[1] <= y0 <= y1 <= expanded[3]):
        raise AssertionError("top-anchored expansion must contain the raw component")
    return expanded


def expand_small_component_box(
        component: Component, small_box_mode: str, minimum_width: int,
        minimum_height: int, perspective_y_threshold: int,
        perspective_width: int, perspective_height: int,
        perspective_top_margin: int, image_width: int,
        image_height: int) -> tuple[int, int, int, int]:
    """Apply the selected small-box policy before NMS."""
    if small_box_mode == "square":
        return expand_minimum_box(component.box, minimum_width, minimum_height,
                                  image_width, image_height)
    if small_box_mode != "perspective":
        raise ValueError(f"unknown small-box mode: {small_box_mode}")
    center_y = (component.ymin + component.ymax) / 2.0
    if center_y < perspective_y_threshold:
        return expand_minimum_box(component.box, minimum_width, minimum_height,
                                  image_width, image_height)
    return expand_top_anchored_box(
        component.box, perspective_width, perspective_height,
        perspective_top_margin, image_width, image_height)


def component_score(component: Component, scorer: str, threshold: int,
                    main_min_area: int) -> float:
    if scorer == "area":
        return float(component.area)
    if scorer == "peak_difference":
        return float(component.peak_difference)
    if scorer == "contrast_fill":
        contrast = max(0.0, component.mean_difference - threshold) / max(1, 255 - threshold)
        area_fraction = min(1.0, component.area / main_min_area)
        return 0.60 * contrast + 0.25 * component.fill_ratio + 0.15 * area_fraction
    raise ValueError(f"unknown scorer: {scorer}")


def select_fixed_budget(components_found: list[Component], scorer: str,
                        threshold: int, main_slots: int, total_budget: int,
                        main_min_area: int, small_min_area: int,
                        small_max_area: int, minimum_width: int,
                        minimum_height: int, nms_iou: float,
                        image_width: int, image_height: int,
                        small_box_mode: str = "square",
                        perspective_y_threshold: int = 110,
                        perspective_width: int = 6,
                        perspective_height: int = 16,
                        perspective_top_margin: int = 2,
                        small_scan_limit: int | None = None) -> list[dict[str, object]]:
    """Keep the deployed main selection and fill remaining slots from small CCs."""
    validate_budget(main_slots, total_budget)
    main_components = sorted(
        (item for item in components_found if item.area >= main_min_area),
        key=lambda item: (-item.area, item.label))[:main_slots]
    selected = [{"component": item, "branch": "main_area_topk",
                 "selection_score": float(item.area), "raw_box": item.box,
                 "selected_box": item.box} for item in main_components]
    # The branch allocation is fixed: unused main slots do not silently enlarge
    # the experimental branch and change its workload.
    small_slots = max(0, total_budget - main_slots)
    if small_slots == 0:
        return selected
    eligible = [item for item in components_found
                if small_min_area <= item.area <= small_max_area]
    ranked = sorted(
        eligible,
        key=lambda item: (-component_score(item, scorer, threshold, main_min_area),
                          -item.area, item.label))
    if small_scan_limit is not None:
        if small_scan_limit < small_slots:
            raise ValueError("small scan limit cannot be smaller than its output quota")
        ranked = ranked[:small_scan_limit]
    occupied = [item["selected_box"] for item in selected]
    for component in ranked:
        # Expansion precedes NMS.  A rejected component does not consume a slot;
        # ranking continues so later non-conflicting components can refill it.
        expanded = expand_small_component_box(
            component, small_box_mode, minimum_width, minimum_height,
            perspective_y_threshold, perspective_width, perspective_height,
            perspective_top_margin, image_width, image_height)
        if any(inclusive_iou(expanded, box) > nms_iou for box in occupied):
            continue
        selected.append({
            "component": component,
            "branch": "small_component_experimental",
            "selection_score": component_score(component, scorer, threshold,
                                                main_min_area),
            "raw_box": component.box,
            "selected_box": expanded,
        })
        occupied.append(expanded)
        if sum(item["branch"] == "small_component_experimental"
               for item in selected) >= small_slots:
            break
    if len(selected) > total_budget or len(selected) > MAX_FIXED_BUDGET:
        raise AssertionError("candidate selection exceeded its hard budget")
    return selected


def internal8_arbitration_key(entry: dict[str, object]) -> tuple[int, int, int]:
    """Integer-only final comparator key, ascending means higher priority."""
    component = entry["component"]
    return (-component.peak_difference, -component.area, component.label)


def build_internal8_pool(
        components_found: list[Component], threshold: int,
        main_min_area: int, small_min_area: int, small_max_area: int,
        minimum_width: int, minimum_height: int, image_width: int,
        image_height: int, small_box_mode: str,
        perspective_y_threshold: int, perspective_width: int,
        perspective_height: int,
        perspective_top_margin: int) -> list[dict[str, object]]:
    """Build four area-main plus four peak-small entries without pre-arbitration NMS."""
    main = sorted((item for item in components_found if item.area >= main_min_area),
                  key=lambda item: (-item.area, item.label))[:4]
    small = sorted(
        (item for item in components_found
         if small_min_area <= item.area <= small_max_area),
        key=lambda item: (-component_score(item, "peak_difference", threshold,
                                           main_min_area),
                          -item.area, item.label))[:4]
    pool = [{"component": item, "branch": "main_area_topk",
             "selection_score": float(item.area), "raw_box": item.box,
             "selected_box": item.box} for item in main]
    for item in small:
        expanded = expand_small_component_box(
            item, small_box_mode, minimum_width, minimum_height,
            perspective_y_threshold, perspective_width, perspective_height,
            perspective_top_margin, image_width, image_height)
        pool.append({"component": item, "branch": "small_component_experimental",
                     "selection_score": float(item.peak_difference),
                     "raw_box": item.box, "selected_box": expanded})
    if len(pool) > 8:
        raise AssertionError("internal pool exceeded eight candidates")
    return pool


def select_final4_strategy(
        components_found: list[Component], strategy: str, threshold: int,
        main_min_area: int, small_min_area: int, small_max_area: int,
        minimum_width: int, minimum_height: int, nms_iou: float,
        image_width: int, image_height: int, small_box_mode: str,
        perspective_y_threshold: int, perspective_width: int,
        perspective_height: int,
        perspective_top_margin: int) -> list[dict[str, object]]:
    """Select one of three final-four policies using peak-difference small ranking."""
    if strategy == "main3_small1":
        return select_fixed_budget(
            components_found, "peak_difference", threshold, 3, 4,
            main_min_area, small_min_area, small_max_area,
            minimum_width, minimum_height, nms_iou, image_width, image_height,
            small_box_mode, perspective_y_threshold, perspective_width,
            perspective_height, perspective_top_margin, small_scan_limit=4)
    if strategy == "main2_small2":
        return select_fixed_budget(
            components_found, "peak_difference", threshold, 2, 4,
            main_min_area, small_min_area, small_max_area,
            minimum_width, minimum_height, nms_iou, image_width, image_height,
            small_box_mode, perspective_y_threshold, perspective_width,
            perspective_height, perspective_top_margin, small_scan_limit=4)
    if strategy != "internal8_to4":
        raise ValueError(f"unknown final-four strategy: {strategy}")
    internal = build_internal8_pool(
        components_found, threshold, main_min_area, small_min_area, small_max_area,
        minimum_width, minimum_height, image_width, image_height, small_box_mode,
        perspective_y_threshold, perspective_width, perspective_height,
        perspective_top_margin)
    ranked = sorted(internal, key=internal8_arbitration_key)
    result = []
    for arbitration_rank, entry in enumerate(ranked):
        if any(inclusive_iou(entry["selected_box"], accepted["selected_box"]) > nms_iou
               for accepted in result):
            continue
        result.append({**entry, "final_arbitration_rank": arbitration_rank})
        if len(result) == 4:
            break
    if len(result) > 4:
        raise AssertionError("final-four arbitration exceeded four outputs")
    return result


def source_box(box: tuple[int, int, int, int], stride: int,
               source_width: int = 1280, source_height: int = 720) -> tuple[int, int, int, int]:
    return (box[0] * stride, box[1] * stride,
            min((box[2] + 1) * stride - 1, source_width - 1),
            min((box[3] + 1) * stride - 1, source_height - 1))


def load_annotations(path: Path, clip_id: str, start_frame: int, frame_count: int,
                     labels: set[str]) -> dict[int, list[dict[str, object]]]:
    if "blind" in str(path).lower():
        raise ValueError("blind-reserve annotations are forbidden for this diagnostic")
    selected: dict[int, list[dict[str, object]]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for csv_line, row in enumerate(csv.DictReader(handle), start=2):
            frame_index = int(row["frame_index"])
            if (row["clip_id"] == clip_id and row["label"] in labels and
                    start_frame <= frame_index < start_frame + frame_count):
                selected[frame_index].append({**row, "_csv_line": csv_line})
    return selected


def summarize_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {}
    for label in ["all", *sorted({str(row["label"]) for row in rows})]:
        subset = rows if label == "all" else [row for row in rows if row["label"] == label]
        count = len(subset)
        baseline = sum(bool(row["covered_by_baseline_main4"]) for row in subset)
        main = sum(bool(row["covered_by_main"]) for row in subset)
        combined = sum(bool(row["covered_by_combined"]) for row in subset)
        incremental = sum(bool(row["covered_by_small_incremental"]) for row in subset)
        summary[label] = {
            "annotation_rows": count,
            "covered_by_baseline_main4_rows": baseline,
            "covered_by_main_rows": main,
            "covered_by_combined_rows": combined,
            "incremental_rows_from_small_branch": incremental,
            "baseline_main4_coverage_rate": baseline / count if count else None,
            "main_coverage_rate": main / count if count else None,
            "combined_coverage_rate": combined / count if count else None,
        }
    return summary


def summarize_iou_thresholds(rows: list[dict[str, object]],
                             thresholds: tuple[float, ...] = (0.1, 0.25, 0.5)
                             ) -> list[dict[str, object]]:
    """Re-score stored exact IoUs without rerunning candidate selection."""
    summaries = []
    for threshold in thresholds:
        for label in ("all", "ped", "ped_analysis_h_le_6", "vehicle"):
            if label == "all":
                subset = rows
            elif label == "ped_analysis_h_le_6":
                subset = [row for row in rows if row["label"] == "ped" and
                          int(row["annotation_analysis_height"]) <= 6]
            else:
                subset = [row for row in rows if row["label"] == label]
            baseline = sum(float(row["baseline_main4_max_iou"]) >= threshold
                           for row in subset)
            main = sum(float(row["main_max_iou"]) >= threshold for row in subset)
            combined = sum(float(row["combined_max_iou"]) >= threshold for row in subset)
            summaries.append({
                "iou_threshold": threshold, "label": label,
                "annotation_rows": len(subset),
                "baseline_main4_covered_rows": baseline,
                "main_covered_rows": main,
                "combined_covered_rows": combined,
                "added_vs_baseline_rows": sum(
                    float(row["combined_max_iou"]) >= threshold and
                    float(row["baseline_main4_max_iou"]) < threshold
                    for row in subset),
                "lost_vs_baseline_rows": sum(
                    float(row["combined_max_iou"]) < threshold and
                    float(row["baseline_main4_max_iou"]) >= threshold
                    for row in subset),
                "incremental_rows": combined - main,
                "baseline_main4_coverage_rate": (
                    baseline / len(subset) if subset else None),
                "main_coverage_rate": main / len(subset) if subset else None,
                "combined_coverage_rate": combined / len(subset) if subset else None,
            })
    return summaries


def run(args: argparse.Namespace) -> dict[str, object]:
    if "blind" in str(args.video).lower():
        raise ValueError("blind-reserve video is forbidden for this diagnostic")
    validate_budget(args.main_slots, args.total_budget)
    if (args.start_frame < 0 or args.frames < 1 or args.small_min_area < 1 or
            args.small_max_area < args.small_min_area or
            args.small_max_area >= args.main_min_area or
            args.minimum_width < 1 or args.minimum_height < 1 or
            args.perspective_y_threshold < 0 or args.perspective_width < 1 or
            args.perspective_height < 1 or args.perspective_top_margin < 0 or
            not 0 <= args.nms_iou <= 1 or not 0 <= args.match_iou <= 1):
        raise ValueError("invalid interval, budget, component area, or IoU parameters")
    development_clip = validate_development_inputs(
        args.video, args.annotations, args.clip_id, args.catalog)
    final_strategies = args.final4_strategy or ["existing_budget"]
    comparison_mode = final_strategies != ["existing_budget"]
    if len(set(final_strategies)) != len(final_strategies):
        raise ValueError("duplicate final-four strategy")
    if comparison_mode and args.scorer and set(args.scorer) != {"peak_difference"}:
        raise ValueError("final-four strategies require scorer=peak_difference")
    scorers = ["peak_difference"] if comparison_mode else (args.scorer or list(SCORERS))
    if len(set(scorers)) != len(scorers):
        raise ValueError("duplicate scorer")
    labels = set(args.label or ("ped", "vehicle"))
    annotations = load_annotations(args.annotations, args.clip_id, args.start_frame,
                                   args.frames, labels)
    chain = CandidateChainReference(
        learn_frames=args.learn_frames, threshold=args.threshold,
        min_neighbors=args.min_neighbors, min_area=args.main_min_area,
        update_enable=True, freeze_foreground=True, min_run=args.min_run,
        top_k=args.main_slots, sample_stride=args.sample_stride)

    result_keys = [(scorer, strategy) for scorer in scorers
                   for strategy in final_strategies]
    candidates_by_key: dict[tuple[str, str], list[dict[str, object]]] = {
        key: [] for key in result_keys}
    coverage_by_key: dict[tuple[str, str], list[dict[str, object]]] = {
        key: [] for key in result_keys}
    raw_main_pool_count: Counter[tuple[str, str]] = Counter()
    raw_main_retained_count: Counter[tuple[str, str]] = Counter()
    raw_main_rank_possible: Counter[tuple[str, str, int]] = Counter()
    raw_main_rank_retained: Counter[tuple[str, str, int]] = Counter()
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {args.video}")
    source_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    processed_total = 0
    processed_window = 0
    try:
        for frame_index in range(args.start_frame + args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            processed_total += 1
            result = chain.process_bgr(frame, frame_index)
            if frame_index < args.start_frame:
                continue
            processed_window += 1
            found = extract_components(result["run_filtered_mask"], result["difference"])
            baseline_main4 = sorted(
                (item for item in found if item.area >= args.main_min_area),
                key=lambda item: (-item.area, item.label))[:4]
            baseline_rank = {item.label: rank for rank, item in enumerate(baseline_main4)}
            baseline_source_boxes = [
                source_box(item.box, args.sample_stride, source_width, source_height)
                for item in baseline_main4]
            for scorer in scorers:
              for strategy in final_strategies:
                key = (scorer, strategy)
                raw_main_pool_count[key] += len(baseline_main4)
                for rank in range(len(baseline_main4)):
                    raw_main_rank_possible[(scorer, strategy, rank)] += 1
                if strategy == "existing_budget":
                    selected = select_fixed_budget(
                        found, scorer, args.threshold, args.main_slots, args.total_budget,
                        args.main_min_area, args.small_min_area, args.small_max_area,
                        args.minimum_width, args.minimum_height, args.nms_iou,
                        chain.analysis_shape[1], chain.analysis_shape[0],
                        args.small_box_mode, args.perspective_y_threshold,
                        args.perspective_width, args.perspective_height,
                        args.perspective_top_margin)
                else:
                    selected = select_final4_strategy(
                        found, strategy, args.threshold, args.main_min_area,
                        args.small_min_area, args.small_max_area,
                        args.minimum_width, args.minimum_height, args.nms_iou,
                        chain.analysis_shape[1], chain.analysis_shape[0],
                        args.small_box_mode, args.perspective_y_threshold,
                        args.perspective_width, args.perspective_height,
                        args.perspective_top_margin)
                serialized = []
                for slot, entry in enumerate(selected):
                    component = entry["component"]
                    retained_rank = baseline_rank.get(component.label)
                    if retained_rank is not None:
                        raw_main_retained_count[key] += 1
                        raw_main_rank_retained[(scorer, strategy, retained_rank)] += 1
                    selected_source_box = source_box(
                        entry["selected_box"], args.sample_stride,
                        source_width, source_height)
                    prefix = f"{strategy}:" if comparison_mode else ""
                    candidate_id = f"{prefix}{scorer}:f{frame_index:06d}:slot{slot}"
                    record = {
                        "scorer": scorer, "frame_index": frame_index,
                        "candidate_id": candidate_id, "slot": slot,
                        "branch": entry["branch"], "component_label": component.label,
                        "component_area": component.area,
                        "component_fill_ratio": component.fill_ratio,
                        "component_mean_difference": component.mean_difference,
                        "component_peak_difference": component.peak_difference,
                        "selection_score": entry["selection_score"],
                        "baseline_main4_rank": retained_rank if retained_rank is not None else "",
                        "raw_analysis_box": list(entry["raw_box"]),
                        "selected_analysis_box": list(entry["selected_box"]),
                        "selected_source_box": list(selected_source_box),
                    }
                    if comparison_mode:
                        record["final_strategy"] = strategy
                        record["final_arbitration_rank"] = entry.get(
                            "final_arbitration_rank", slot)
                    candidates_by_key[key].append(record)
                    serialized.append(record)
                main_records = [row for row in serialized
                                if row["branch"] == "main_area_topk"]
                small_records = [row for row in serialized
                                 if row["branch"] == "small_component_experimental"]
                for annotation in annotations.get(frame_index, []):
                    annotation_box = tuple(int(annotation[key]) for key in
                                           ("xmin", "ymin", "xmax", "ymax"))
                    baseline_max_iou = max(
                        (inclusive_iou(box, annotation_box)
                         for box in baseline_source_boxes), default=0.0)
                    main_matches = [(inclusive_iou(tuple(row["selected_source_box"]),
                                                   annotation_box), row)
                                    for row in main_records]
                    small_matches = [(inclusive_iou(tuple(row["selected_source_box"]),
                                                    annotation_box), row)
                                     for row in small_records]
                    best_main = max(main_matches, key=lambda item: item[0], default=(0.0, None))
                    best_small = max(small_matches, key=lambda item: item[0], default=(0.0, None))
                    best = max((best_main, best_small), key=lambda item: item[0])
                    main_covered = best_main[0] >= args.match_iou
                    combined_covered = best[0] >= args.match_iou
                    coverage_record = {
                        "scorer": scorer,
                        "annotation_csv_line": annotation["_csv_line"],
                        "clip_id": args.clip_id, "frame_index": frame_index,
                        "label": annotation["label"],
                        "object_id": annotation["object_id"],
                        "annotation_box": list(annotation_box),
                        "annotation_analysis_height": (
                            int(annotation["ymax"]) // args.sample_stride -
                            int(annotation["ymin"]) // args.sample_stride + 1),
                        "baseline_main4_max_iou": baseline_max_iou,
                        "covered_by_baseline_main4": baseline_max_iou >= args.match_iou,
                        "main_max_iou": best_main[0],
                        "small_max_iou": best_small[0],
                        "combined_max_iou": best[0],
                        "covered_by_main": main_covered,
                        "covered_by_combined": combined_covered,
                        "covered_by_small_incremental": combined_covered and not main_covered,
                        "matched_candidate_id": (
                            best[1]["candidate_id"] if combined_covered and best[1] else ""),
                        "matched_branch": (
                            best[1]["branch"] if combined_covered and best[1] else ""),
                    }
                    if comparison_mode:
                        coverage_record["final_strategy"] = strategy
                    coverage_by_key[key].append(coverage_record)
    finally:
        capture.release()

    if processed_window != args.frames:
        raise ValueError(f"decoded only {processed_window}/{args.frames} scoring frames")
    args.output.mkdir(parents=True, exist_ok=True)
    candidate_fields = [
        "scorer", "frame_index", "candidate_id", "slot", "branch",
        "component_label", "component_area", "component_fill_ratio",
        "component_mean_difference", "component_peak_difference", "selection_score",
        "baseline_main4_rank",
        "raw_analysis_box", "selected_analysis_box", "selected_source_box"]
    if comparison_mode:
        candidate_fields[1:1] = ["final_strategy", "final_arbitration_rank"]
    with (args.output / "candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, candidate_fields)
        writer.writeheader()
        for key in result_keys:
            writer.writerows(candidates_by_key[key])
    coverage_fields = [
        "scorer", "annotation_csv_line", "clip_id", "frame_index", "label",
        "object_id", "annotation_box", "main_max_iou", "small_max_iou",
        "annotation_analysis_height", "baseline_main4_max_iou",
        "covered_by_baseline_main4",
        "combined_max_iou", "covered_by_main", "covered_by_combined",
        "covered_by_small_incremental", "matched_candidate_id", "matched_branch"]
    if comparison_mode:
        coverage_fields.insert(1, "final_strategy")
    with (args.output / "annotation_row_coverage.csv").open(
            "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, coverage_fields)
        writer.writeheader()
        for key in result_keys:
            writer.writerows(coverage_by_key[key])

    parameters = {
        "sample_stride": args.sample_stride, "learn_frames": args.learn_frames,
        "threshold": args.threshold, "min_neighbors": args.min_neighbors,
        "min_run": args.min_run, "main_min_area": args.main_min_area,
        "main_slots": args.main_slots, "total_budget": args.total_budget,
        "small_min_area": args.small_min_area, "small_max_area": args.small_max_area,
        "minimum_small_box": [args.minimum_width, args.minimum_height],
        "small_box_mode": args.small_box_mode,
        "perspective_y_threshold": args.perspective_y_threshold,
        "perspective_minimum_box": [args.perspective_width,
                                    args.perspective_height],
        "perspective_top_margin": args.perspective_top_margin,
        "fixed_small_slot_count": args.total_budget - args.main_slots,
        "nms_iou": args.nms_iou, "annotation_match_iou": args.match_iou,
        "scorers": scorers,
        "final_output_strategies": final_strategies,
        "effective_final_output_budget": 4 if comparison_mode else args.total_budget,
        "internal_pool_budget": 8 if comparison_mode else None,
        "bounded_small_pool_budget": 4 if comparison_mode else None,
    }
    results = []
    for scorer, strategy in result_keys:
        candidate_rows = candidates_by_key[(scorer, strategy)]
        branch_counts = Counter(str(row["branch"]) for row in candidate_rows)
        per_frame_counts = Counter(int(row["frame_index"]) for row in candidate_rows)
        scored_frames = range(args.start_frame, args.start_frame + args.frames)
        effective_budget = 4 if strategy != "existing_budget" else args.total_budget
        result_summary = {
            "scorer": scorer,
            "candidate_count": len(candidate_rows),
            "candidate_count_by_branch": dict(sorted(branch_counts.items())),
            "frames_at_total_budget": sum(
                count == effective_budget for count in per_frame_counts.values()),
            "minimum_candidates_per_frame": min(
                (per_frame_counts.get(frame, 0) for frame in scored_frames), default=0),
            "maximum_candidates_per_frame": max(
                (per_frame_counts.get(frame, 0) for frame in scored_frames), default=0),
            "annotation_coverage": summarize_rows(coverage_by_key[(scorer, strategy)]),
            "annotation_coverage_iou_sweep": summarize_iou_thresholds(
                coverage_by_key[(scorer, strategy)]),
        }
        if comparison_mode:
            result_summary["final_strategy"] = strategy
            result_summary["final_empty_slots"] = sum(
                4 - per_frame_counts.get(frame, 0) for frame in scored_frames)
            result_summary["raw_main_top4_retained_count"] = raw_main_retained_count[
                (scorer, strategy)]
            result_summary["raw_main_top4_possible_count"] = raw_main_pool_count[
                (scorer, strategy)]
            result_summary["raw_main_top4_retention_rate"] = (
                raw_main_retained_count[(scorer, strategy)] /
                raw_main_pool_count[(scorer, strategy)]
                if raw_main_pool_count[(scorer, strategy)] else None)
            result_summary["raw_main_top4_retention_by_rank"] = [
                {
                    "rank": rank,
                    "retained": raw_main_rank_retained[(scorer, strategy, rank)],
                    "possible": raw_main_rank_possible[(scorer, strategy, rank)],
                    "rate": (
                        raw_main_rank_retained[(scorer, strategy, rank)] /
                        raw_main_rank_possible[(scorer, strategy, rank)]
                        if raw_main_rank_possible[(scorer, strategy, rank)] else None),
                }
                for rank in range(4)
            ]
        results.append(result_summary)
    reference_path = Path(__file__).with_name("candidate_chain_reference.py")
    report = {
        "status": "python_fixed_budget_post_cleanup_diagnostic_not_rtl_or_acceptance_evidence",
        "clip_id": args.clip_id,
        "scored_frame_interval_inclusive": [args.start_frame,
                                             args.start_frame + args.frames - 1],
        "warmup_contract": "decode and process causally from source frame 0; score only requested interval",
        "processed_frames_including_warmup": processed_total,
        "processed_scoring_frames": processed_window,
        "annotation_labels": sorted(labels),
        "parameters": parameters,
        "hashes": {
            "source_video_sha256": digest(args.video),
            "annotations_csv_sha256": digest(args.annotations),
            "script_sha256": digest(Path(__file__)),
            "candidate_chain_reference_sha256": digest(reference_path),
            "candidates_csv_sha256": digest(args.output / "candidates.csv"),
            "annotation_row_coverage_csv_sha256": digest(
                args.output / "annotation_row_coverage.csv"),
            "development_catalog_sha256": digest(args.catalog),
        },
        "inputs": {"source_video": str(args.video.resolve()),
                   "annotations_csv": str(args.annotations.resolve()),
                   "development_catalog": str(args.catalog.resolve()),
                   "catalog_split": development_clip["split"]},
        "scoring_contract": {
            "contrast_fill": (
                "0.60*normalized(mean_difference-threshold) + "
                "0.25*component_fill_ratio + 0.15*min(area/main_min_area,1)"),
            "area": "component foreground-pixel area; deterministic label tie-break",
            "peak_difference": "component maximum absolute gray/background difference",
            "tie_break": "higher score, then larger area, then lower component label",
        },
        "final_output_contracts": {
            "existing_budget": (
                "Backward-compatible configurable main_slots plus "
                "total_budget-main_slots small slots; output is not reduced to four."),
            "main3_small1": (
                "Area-ranked main top3 plus one peak-difference-ranked small candidate. "
                "The internal small pool is capped at peak top4. Small expansion precedes "
                "NMS; rejected candidates are refilled only from that bounded pool."),
            "main2_small2": (
                "Area-ranked main top2 plus two peak-difference-ranked small candidates. "
                "The internal small pool is capped at peak top4. Small expansion precedes "
                "NMS; rejected candidates are refilled only from that bounded pool."),
            "internal8_to4": (
                "Build an internal pool of area top4 main boxes and peak-difference top4 "
                "expanded small boxes without pre-NMS. Sort the unified pool by integer "
                "key (-peak_difference,-area,+component_label), then greedily accept in "
                "that order when IoU<=nms_iou against every accepted box, continuing "
                "after rejection until four outputs or pool exhaustion. A high-peak "
                "small box can therefore replace a conflicting main box. This requires "
                "only fixed-width comparators, a four-entry accepted set and IoU logic."),
        },
        "selection_contract": (
            "Main branch exactly keeps area>=main_min_area components sorted by "
            "(-area,label), capped at main_slots. The experimental branch only considers "
            "small_min_area<=area<=small_max_area. In square mode it center-expands to "
            "minimum_small_box. In perspective mode, components whose center_y reaches "
            "perspective_y_threshold use a top-anchored perspective_minimum_box; components "
            "above the threshold retain square expansion. Expansion occurs before NMS; "
            "after a conflict the rank scan continues to refill the fixed small slots. "
            "NMS rejects IoU>nms_iou against main and accepted small boxes. "
            "Its fixed slot allocation is total_budget-main_slots; unused main slots are "
            "not reassigned, so the per-frame count may be below the total budget."),
        "coordinate_contract": (
            "All analysis boxes are inclusive. Source extent is "
            "[stride*xmin,stride*ymin,stride*(xmax+1)-1,stride*(ymax+1)-1], clipped."),
        "results": results,
        "boundary": (
            "Only the main area-top4 branch represents current selection behavior. The "
            "small branch, box expansion and NMS are Python proposals. VIRAT annotations "
            "are not exhaustive background truth, so candidate count is processing load, "
            "not a false-positive count. No blind-reserve input is accepted."),
    }
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def self_test() -> None:
    mask = np.zeros((20, 24), np.uint8)
    difference = np.zeros_like(mask)
    # Four main components and two small components, one near a main box for NMS.
    rectangles = [
        (1, 1, 4, 4, 30), (8, 1, 11, 4, 35), (15, 1, 18, 4, 40),
        (1, 10, 4, 13, 45), (10, 10, 11, 11, 80), (20, 10, 21, 10, 120)]
    for x0, y0, x1, y1, value in rectangles:
        mask[y0:y1 + 1, x0:x1 + 1] = 1
        difference[y0:y1 + 1, x0:x1 + 1] = value
    found = extract_components(mask, difference)
    selected = select_fixed_budget(found, "contrast_fill", 20, 4, 6, 16, 2, 15,
                                   4, 4, 0.3, 24, 20)
    explicit_square = select_fixed_budget(
        found, "contrast_fill", 20, 4, 6, 16, 2, 15,
        4, 4, 0.3, 24, 20, small_box_mode="square")
    assert [(row["component"].label, row["selected_box"]) for row in selected] == [
        (row["component"].label, row["selected_box"]) for row in explicit_square]
    assert len([row for row in selected if row["branch"] == "main_area_topk"]) == 4
    assert len([row for row in selected
                if row["branch"] == "small_component_experimental"]) == 2
    assert all((row["selected_box"][2] - row["selected_box"][0] + 1 >= 4 and
                row["selected_box"][3] - row["selected_box"][1] + 1 >= 4)
               for row in selected if row["branch"] == "small_component_experimental")
    upper = Component(100, 2, 40, 108, 41, 109, 1.0, 60.0, 80)
    lower = Component(101, 2, 40, 110, 41, 111, 1.0, 60.0, 80)
    upper_box = expand_small_component_box(
        upper, "perspective", 4, 4, 110, 6, 16, 2, 256, 144)
    lower_box = expand_small_component_box(
        lower, "perspective", 4, 4, 110, 6, 16, 2, 256, 144)
    assert upper_box == expand_minimum_box(upper.box, 4, 4, 256, 144)
    assert lower_box == (38, 108, 43, 123)
    assert lower_box[0] <= lower.xmin <= lower.xmax <= lower_box[2]
    assert lower_box[1] <= lower.ymin <= lower.ymax <= lower_box[3]

    def synthetic(label: int, area: int, box: tuple[int, int, int, int],
                  peak: int) -> Component:
        return Component(label, area, *box, 1.0, float(peak), peak)

    refill_components = [
        synthetic(1, 16, (0, 0, 3, 3), 20),
        synthetic(2, 16, (12, 0, 15, 3), 20),
        synthetic(3, 16, (24, 0, 27, 3), 20),
        synthetic(4, 16, (36, 0, 39, 3), 20),
        synthetic(5, 2, (1, 1, 2, 1), 200),  # rejected against main label 1
        synthetic(6, 2, (2, 20, 3, 20), 190),
        synthetic(7, 2, (14, 20, 15, 20), 180),
        synthetic(8, 2, (26, 20, 27, 20), 170),
        synthetic(9, 2, (38, 20, 39, 20), 160),
    ]
    refilled = select_fixed_budget(
        refill_components, "peak_difference", 20, 4, 8, 16, 2, 15,
        4, 4, 0.3, 64, 32)
    small_labels = [row["component"].label for row in refilled
                    if row["branch"] == "small_component_experimental"]
    assert small_labels == [6, 7, 8, 9]
    assert len(refilled) == 8
    bounded = select_fixed_budget(
        refill_components, "peak_difference", 20, 4, 8, 16, 2, 15,
        4, 4, 0.3, 64, 32, small_scan_limit=4)
    assert [row["component"].label for row in bounded
            if row["branch"] == "small_component_experimental"] == [6, 7, 8]
    main3 = select_final4_strategy(
        refill_components, "main3_small1", 20, 16, 2, 15, 4, 4, 0.3,
        64, 32, "square", 110, 6, 16, 2)
    main2 = select_final4_strategy(
        refill_components, "main2_small2", 20, 16, 2, 15, 4, 4, 0.3,
        64, 32, "square", 110, 6, 16, 2)
    assert Counter(row["branch"] for row in main3) == {
        "main_area_topk": 3, "small_component_experimental": 1}
    assert Counter(row["branch"] for row in main2) == {
        "main_area_topk": 2, "small_component_experimental": 2}

    unified_components = [
        synthetic(1, 16, (0, 0, 3, 3), 190),
        synthetic(2, 16, (12, 0, 15, 3), 180),
        synthetic(3, 16, (24, 0, 27, 3), 170),
        synthetic(4, 16, (36, 0, 39, 3), 160),
        synthetic(5, 2, (1, 1, 2, 1), 200),  # wins, then suppresses main 1
        synthetic(6, 2, (50, 20, 51, 20), 100),
    ]
    internal4 = select_final4_strategy(
        unified_components, "internal8_to4", 20, 16, 2, 15, 4, 4, 0.3,
        64, 32, "square", 110, 6, 16, 2)
    assert len(internal4) == 4
    assert [row["component"].label for row in internal4] == [5, 2, 3, 4]
    assert all(inclusive_iou(left["selected_box"], right["selected_box"]) <= 0.3
               for index, left in enumerate(internal4)
               for right in internal4[index + 1:])
    assert source_box((1, 2, 3, 4), 5) == (5, 10, 19, 24)
    assert inclusive_iou((0, 0, 1, 1), (0, 0, 1, 1)) == 1.0
    validate_budget(4, 8)
    try:
        validate_budget(4, 9)
    except ValueError as exc:
        assert "<= 8" in str(exc)
    else:
        raise AssertionError("budget above eight was accepted")
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "blind_annotations.csv"
        path.write_text("clip_id,frame_index,label\n", encoding="utf-8")
        try:
            load_annotations(path, "clip", 0, 1, {"ped"})
        except ValueError as exc:
            assert "blind-reserve" in str(exc)
        else:
            raise AssertionError("blind-reserve guard did not trigger")
    print("PASS: perspective, three final4 strategies, NMS refill, <=8 budget and blind guard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--clip-id")
    parser.add_argument("--start-frame", type=int)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--catalog", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/catalog.json"))
    parser.add_argument("--label", action="append", choices=("ped", "vehicle"))
    parser.add_argument("--scorer", action="append", choices=SCORERS)
    parser.add_argument("--final4-strategy", action="append",
                        choices=FINAL4_STRATEGIES,
                        help=("repeat to compare final-four policies; when present, "
                              "peak_difference is the only allowed scorer"))
    parser.add_argument("--sample-stride", type=int, default=5)
    parser.add_argument("--learn-frames", type=int, default=4)
    parser.add_argument("--threshold", type=int, default=20)
    parser.add_argument("--min-neighbors", type=int, default=3)
    parser.add_argument("--min-run", type=int, default=2)
    parser.add_argument("--main-min-area", type=int, default=16)
    parser.add_argument("--main-slots", type=int, default=4)
    parser.add_argument("--total-budget", type=int, default=8)
    parser.add_argument("--small-min-area", type=int, default=2)
    parser.add_argument("--small-max-area", type=int, default=15)
    parser.add_argument("--minimum-width", type=int, default=4)
    parser.add_argument("--minimum-height", type=int, default=4)
    parser.add_argument("--small-box-mode", choices=("square", "perspective"),
                        default="square")
    parser.add_argument("--perspective-y-threshold", type=int, default=110)
    parser.add_argument("--perspective-width", type=int, default=6)
    parser.add_argument("--perspective-height", type=int, default=16)
    parser.add_argument("--perspective-top-margin", type=int, default=2)
    parser.add_argument("--nms-iou", type=float, default=0.3)
    parser.add_argument("--match-iou", type=float, default=0.1)
    parser.add_argument("--self-test", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    required = ("video", "annotations", "clip_id", "start_frame", "frames", "output")
    missing = [name for name in required if getattr(args, name) is None]
    if missing:
        parser.error("required unless --self-test: " + ", ".join("--" + name.replace("_", "-")
                                                                  for name in missing))
    report = run(args)
    print(json.dumps({"status": report["status"],
                      "processed_scoring_frames": report["processed_scoring_frames"],
                      "results": report["results"],
                      "output": str(args.output.resolve())},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
