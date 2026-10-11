#!/usr/bin/env python3
"""Guarded final-four arbitration sweep on four development windows.

Each source clip is decoded causally once from frame zero.  Post-cleanup
components are cached for every requested frame and reused by all guarded and
legacy-control configurations.  The guarded policy preserves the area-ranked
main structure, fills empty slots from a bounded qualified small pool, and can
replace only weak main rank three under explicit integer and IoU guards.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference
from fixed_budget_candidate_prototype import (
    Component,
    digest,
    expand_small_component_box,
    extract_components,
    inclusive_iou,
    select_final4_strategy,
    source_box,
    validate_development_inputs,
)


DEFAULT_WINDOWS = (
    "VIRAT_S_000203_03_000736_000785:600-899",
    "VIRAT_S_000200_00_000100_000171:600-899",
    "VIRAT_S_000200_00_000100_000171:1600-1899",
    "VIRAT_S_000206_07_001501_001600:600-1499",
)
T_VALUES = (90, 100, 110)
P_VALUES = (40, 64)
DELTA_VALUES = (16, 32)
AWEAK_VALUES = (32, 64)
IOU_THRESHOLDS = (0.1, 0.25, 0.5)
SAMPLE_STRIDE = 5
NMS_IOU = 0.3
MAIN_MIN_AREA = 16
SMALL_MIN_AREA = 2
SMALL_MAX_AREA = 15
SMALL_POOL_LIMIT = 4
FINAL_LIMIT = 4
TIME_BIN_FRAMES = 30
LEGACY_000206_REFERENCE = Path(
    "evaluation/python_references/final4_bounded_virat_000206_f600_1499_y100")


REASON_CODES = {
    "KEEP_MAIN": "Original area-ranked main candidate retained in its structural slot.",
    "FILL_EMPTY_SLOT": "Qualified small candidate filled an unused main output slot.",
    "REPLACE_WEAK_M3": "Qualified small candidate replaced original main rank three.",
    "DROP_WEAK_M3": "Original main rank three was removed by the single replacement.",
    "REJECT_AREA_LT4": "Small pool candidate has area below four pixels.",
    "REJECT_DENSITY_LT_QUARTER": "Four times component area is below raw bbox area.",
    "REJECT_PEAK_FLOOR": "Small component peak difference is below P.",
    "REJECT_NMS_MAIN": "Expanded small box overlaps an original main box above IoU 0.3.",
    "REJECT_NMS_SELECTED_SMALL": "Expanded small box overlaps an accepted small box above IoU 0.3.",
    "REJECT_OUTPUT_FULL_FILL_ONLY": "All four main slots are occupied and replacement is disabled.",
    "REJECT_M3_NOT_WEAK": "Main rank three area is not below Aweak.",
    "REJECT_PEAK_MARGIN": "Small peak is below main-rank-three peak plus delta.",
    "REJECT_NMS_ORIGINAL_MAIN4": "Replacement box overlaps at least one original main box.",
    "REJECT_REPLACEMENT_ALREADY_USED": "The one permitted main-rank-three replacement was used.",
    "REJECT_OUTPUT_FULL_AFTER_FILL": "Empty slots were already filled by earlier qualified small boxes.",
    "CONTROL_SELECTED_MAIN": "Legacy comparison selected this main candidate without new guards.",
    "CONTROL_SELECTED_SMALL": "Legacy comparison selected this small candidate without new guards.",
    "BASELINE_MAIN": "Unmodified area-ranked main top-four baseline output.",
}


@dataclass(frozen=True)
class Window:
    clip_id: str
    start: int
    end: int

    @property
    def window_id(self) -> str:
        return f"{self.clip_id}:{self.start}-{self.end}"


@dataclass(frozen=True)
class Config:
    config_id: str
    family: str
    perspective_threshold: int | None
    peak_floor: int | None
    delta: int | None
    weak_area: int | None
    replacement_enabled: bool
    control_strategy: str | None = None


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reject_sealed_path(path: Path) -> None:
    lowered = str(path).lower()
    if any(token in lowered for token in ("blind", "holdout", "reserve")):
        raise ValueError("blind/holdout/reserve inputs are forbidden")


def parse_window(specification: str) -> Window:
    try:
        clip_id, interval = specification.rsplit(":", 1)
        start_text, end_text = interval.split("-", 1)
        result = Window(clip_id, int(start_text), int(end_text))
    except (ValueError, TypeError) as exc:
        raise ValueError(f"invalid window specification: {specification!r}") from exc
    if not clip_id or result.start < 0 or result.end < result.start:
        raise ValueError(f"invalid window specification: {specification!r}")
    return result


def build_configs() -> list[Config]:
    configs = [Config("baseline_main4", "baseline", None, None, None, None, False)]
    for threshold in T_VALUES:
        for strategy in ("main3_small1", "main2_small2", "internal8_to4"):
            configs.append(Config(
                f"control_{strategy}_T{threshold}", "legacy_control", threshold,
                None, None, None, False, strategy))
        configs.append(Config(
            f"fill_only_T{threshold}", "guarded_fill_only", threshold,
            40, None, None, False))
        for peak_floor in P_VALUES:
            for delta in DELTA_VALUES:
                for weak_area in AWEAK_VALUES:
                    configs.append(Config(
                        f"guarded_T{threshold}_P{peak_floor}_D{delta}_A{weak_area}",
                        "guarded_replace", threshold, peak_floor, delta,
                        weak_area, True))
    if len(configs) != 37:
        raise AssertionError("expected baseline + 9 controls + 3 fill-only + 24 guarded")
    return configs


def main_pool(components: list[Component]) -> list[dict[str, object]]:
    ranked = sorted((item for item in components if item.area >= MAIN_MIN_AREA),
                    key=lambda item: (-item.area, item.label))[:4]
    return [{"component": item, "branch": "main_area_topk",
             "raw_box": item.box, "selected_box": item.box,
             "baseline_main_rank": rank, "reason_code": "KEEP_MAIN"}
            for rank, item in enumerate(ranked)]


def small_pool(components: list[Component]) -> list[dict[str, object]]:
    ranked = sorted(
        (item for item in components if SMALL_MIN_AREA <= item.area <= SMALL_MAX_AREA),
        key=lambda item: (-item.peak_difference, -item.area, item.label))[:SMALL_POOL_LIMIT]
    return [{"component": item, "small_rank": rank} for rank, item in enumerate(ranked)]


def raw_bbox_area(component: Component) -> int:
    return (component.xmax - component.xmin + 1) * (component.ymax - component.ymin + 1)


def qualification_reason(component: Component, peak_floor: int) -> str | None:
    if component.area < 4:
        return "REJECT_AREA_LT4"
    if 4 * component.area < raw_bbox_area(component):
        return "REJECT_DENSITY_LT_QUARTER"
    if component.peak_difference < peak_floor:
        return "REJECT_PEAK_FLOOR"
    return None


def expand_small(component: Component, threshold: int,
                 image_width: int, image_height: int) -> tuple[int, int, int, int]:
    return expand_small_component_box(
        component, "perspective", 4, 4, threshold, 6, 16, 2,
        image_width, image_height)


def guarded_select(components: list[Component], config: Config,
                   image_width: int, image_height: int
                   ) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    """Apply the evaluated development guarded policy and return outputs plus events."""
    if config.peak_floor is None or config.perspective_threshold is None:
        raise ValueError("guarded configuration lacks P or T")
    mains = main_pool(components)
    original_main_boxes = [row["selected_box"] for row in mains]
    outputs = [dict(row) for row in mains]
    events: list[dict[str, object]] = []
    accepted_small_boxes: list[tuple[int, int, int, int]] = []
    original_main_count = len(mains)
    replacement_used = False

    for pool_row in small_pool(components):
        component = pool_row["component"]
        event = {"component": component, "small_rank": pool_row["small_rank"],
                 "selected_box": None, "reason_code": None}
        reason = qualification_reason(component, config.peak_floor)
        if reason is not None:
            event["reason_code"] = reason
            events.append(event)
            continue
        expanded = expand_small(component, config.perspective_threshold,
                                image_width, image_height)
        event["selected_box"] = expanded

        if original_main_count < FINAL_LIMIT:
            if len(outputs) >= FINAL_LIMIT:
                event["reason_code"] = "REJECT_OUTPUT_FULL_AFTER_FILL"
            elif any(inclusive_iou(expanded, box) > NMS_IOU
                     for box in original_main_boxes):
                event["reason_code"] = "REJECT_NMS_MAIN"
            elif any(inclusive_iou(expanded, box) > NMS_IOU
                     for box in accepted_small_boxes):
                event["reason_code"] = "REJECT_NMS_SELECTED_SMALL"
            else:
                event["reason_code"] = "FILL_EMPTY_SLOT"
                accepted_small_boxes.append(expanded)
                outputs.append({"component": component,
                                "branch": "small_component_experimental",
                                "raw_box": component.box,
                                "selected_box": expanded,
                                "baseline_main_rank": None,
                                "small_rank": pool_row["small_rank"],
                                "reason_code": "FILL_EMPTY_SLOT"})
            events.append(event)
            continue

        if not config.replacement_enabled:
            event["reason_code"] = "REJECT_OUTPUT_FULL_FILL_ONLY"
        elif replacement_used:
            event["reason_code"] = "REJECT_REPLACEMENT_ALREADY_USED"
        else:
            m3 = mains[3]["component"]
            if config.weak_area is None or m3.area >= config.weak_area:
                event["reason_code"] = "REJECT_M3_NOT_WEAK"
            elif config.delta is None or component.peak_difference < m3.peak_difference + config.delta:
                event["reason_code"] = "REJECT_PEAK_MARGIN"
            elif any(inclusive_iou(expanded, box) > NMS_IOU
                     for box in original_main_boxes):
                event["reason_code"] = "REJECT_NMS_ORIGINAL_MAIN4"
            else:
                event["reason_code"] = "REPLACE_WEAK_M3"
                replacement_used = True
                outputs[3] = {"component": component,
                              "branch": "small_component_experimental",
                              "raw_box": component.box,
                              "selected_box": expanded,
                              "baseline_main_rank": None,
                              "small_rank": pool_row["small_rank"],
                              "reason_code": "REPLACE_WEAK_M3"}
                events.append({"component": m3, "small_rank": None,
                               "selected_box": m3.box,
                               "reason_code": "DROP_WEAK_M3"})
        events.append(event)

    if len(mains) == 4:
        if [row["component"].label for row in outputs[:3]] != [
                row["component"].label for row in mains[:3]]:
            raise AssertionError("protected main ranks zero through two changed")
        if sum(row["branch"] == "small_component_experimental" for row in outputs) > 1:
            raise AssertionError("more than one replacement occurred")
    if len(mains) < 4 and [row["component"].label for row in outputs[:len(mains)]] != [
            row["component"].label for row in mains]:
        raise AssertionError("main output order changed during fill")
    if len(mains) + len(small_pool(components)) > 8 or len(outputs) > 4:
        raise AssertionError("internal or final budget exceeded")
    diagnostics = {
        "internal_candidates": len(mains) + len(small_pool(components)),
        "main_candidates": len(mains),
        "small_pool_candidates": len(small_pool(components)),
        "final_candidates": len(outputs),
        "empty_slots": FINAL_LIMIT - len(outputs),
        "replacement_used": int(replacement_used),
    }
    return outputs, events, diagnostics


def baseline_select(components: list[Component]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    outputs = main_pool(components)
    for row in outputs:
        row["reason_code"] = "BASELINE_MAIN"
    return outputs, [], {
        "internal_candidates": len(outputs), "main_candidates": len(outputs),
        "small_pool_candidates": 0, "final_candidates": len(outputs),
        "empty_slots": FINAL_LIMIT - len(outputs), "replacement_used": 0}


def control_select(components: list[Component], config: Config,
                   image_width: int, image_height: int
                   ) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    if config.control_strategy is None or config.perspective_threshold is None:
        raise ValueError("legacy control configuration is incomplete")
    selected = select_final4_strategy(
        components, config.control_strategy, 20, MAIN_MIN_AREA, SMALL_MIN_AREA,
        SMALL_MAX_AREA, 4, 4, NMS_IOU, image_width, image_height,
        "perspective", config.perspective_threshold, 6, 16, 2)
    main_ranks = {row["component"].label: row["baseline_main_rank"]
                  for row in main_pool(components)}
    outputs = []
    for row in selected:
        is_main = row["branch"] == "main_area_topk"
        outputs.append({**row,
                        "baseline_main_rank": main_ranks.get(row["component"].label)
                        if is_main else None,
                        "small_rank": None,
                        "reason_code": "CONTROL_SELECTED_MAIN" if is_main
                        else "CONTROL_SELECTED_SMALL"})
    if len(main_pool(components)) + len(small_pool(components)) > 8 or len(outputs) > 4:
        raise AssertionError("legacy comparison exceeded frozen budgets")
    return outputs, [], {
        "internal_candidates": len(main_pool(components)) + len(small_pool(components)),
        "main_candidates": len(main_pool(components)),
        "small_pool_candidates": len(small_pool(components)),
        "final_candidates": len(outputs), "empty_slots": 4 - len(outputs),
        "replacement_used": 0}


def select_config(components: list[Component], config: Config,
                  image_width: int, image_height: int
                  ) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    if config.family == "baseline":
        return baseline_select(components)
    if config.family == "legacy_control":
        return control_select(components, config, image_width, image_height)
    return guarded_select(components, config, image_width, image_height)


def load_annotations(path: Path, windows: list[Window]) -> tuple[
        dict[tuple[str, int], list[dict[str, object]]], dict[str, list[dict[str, object]]]]:
    by_clip_frame: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    by_window: dict[str, list[dict[str, object]]] = defaultdict(list)
    windows_by_clip: dict[str, list[Window]] = defaultdict(list)
    for window in windows:
        windows_by_clip[window.clip_id].append(window)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for csv_line, row in enumerate(csv.DictReader(handle), start=2):
            clip_id = row["clip_id"]
            if clip_id not in windows_by_clip or row["label"] not in {"ped", "vehicle"}:
                continue
            frame = int(row["frame_index"])
            matching = [window for window in windows_by_clip[clip_id]
                        if window.start <= frame <= window.end]
            if not matching:
                continue
            annotation = {
                "annotation_key": f"{clip_id}:line{csv_line}",
                "annotation_csv_line": csv_line, "clip_id": clip_id,
                "frame_index": frame, "label": row["label"],
                "object_id": row["object_id"],
                "annotation_box": tuple(int(row[key]) for key in
                                        ("xmin", "ymin", "xmax", "ymax")),
            }
            by_clip_frame[(clip_id, frame)].append(annotation)
            for window in matching:
                by_window[window.window_id].append(annotation)
    return by_clip_frame, by_window


def cache_components(catalog_path: Path, annotations_path: Path,
                     windows: list[Window]) -> tuple[
                         dict[tuple[str, int], list[Component]],
                         dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog_entries = {row["clip_id"]: row for row in catalog.get("clips", [])}
    windows_by_clip: dict[str, list[Window]] = defaultdict(list)
    for window in windows:
        windows_by_clip[window.clip_id].append(window)
    cache: dict[tuple[str, int], list[Component]] = {}
    receipts: dict[str, dict[str, object]] = {}
    clip_meta: dict[str, dict[str, object]] = {}
    for clip_id, clip_windows in windows_by_clip.items():
        if clip_id not in catalog_entries:
            raise ValueError(f"clip absent from catalog: {clip_id}")
        entry = catalog_entries[clip_id]
        video = Path(entry["video_path"])
        reject_sealed_path(video)
        validate_development_inputs(video, annotations_path, clip_id, catalog_path)
        maximum_frame = max(window.end for window in clip_windows)
        target_frames = {frame for window in clip_windows
                         for frame in range(window.start, window.end + 1)}
        chain = CandidateChainReference(
            learn_frames=4, threshold=20, min_neighbors=3,
            min_area=MAIN_MIN_AREA, update_enable=True, freeze_foreground=True,
            min_run=2, top_k=4, sample_stride=SAMPLE_STRIDE)
        capture = cv2.VideoCapture(str(video))
        if not capture.isOpened():
            raise ValueError(f"cannot open video: {video}")
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        processed = 0
        try:
            for frame_index in range(maximum_frame + 1):
                ok, frame = capture.read()
                if not ok:
                    break
                processed += 1
                result = chain.process_bgr(frame, frame_index)
                if frame_index in target_frames:
                    cache[(clip_id, frame_index)] = extract_components(
                        result["run_filtered_mask"], result["difference"])
        finally:
            capture.release()
        if processed != maximum_frame + 1 or any(
                (clip_id, frame) not in cache for frame in target_frames):
            raise ValueError(f"incomplete causal decode for {clip_id}")
        receipts[clip_id] = {
            "path": str(video.resolve()), "sha256": digest(video),
            "catalog_split": entry["split"],
            "decoded_frames_from_zero": processed,
            "cached_scoring_frames": len(target_frames),
        }
        clip_meta[clip_id] = {"width": width, "height": height}
    return cache, receipts, clip_meta


def maximum_iou(box: tuple[int, int, int, int],
                candidates: list[dict[str, object]], width: int,
                height: int) -> tuple[float, dict[str, object] | None]:
    best = (0.0, None)
    for row in candidates:
        candidate_box = source_box(row["selected_box"], SAMPLE_STRIDE, width, height)
        overlap = inclusive_iou(box, candidate_box)
        if overlap > best[0]:
            best = (overlap, row)
    return best


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def safe_rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def coverage_counts(rows: list[dict[str, object]], threshold: float
                    ) -> dict[str, int | float | None]:
    baseline = sum(row["baseline_max_iou"] >= threshold for row in rows)
    final = sum(row["final_max_iou"] >= threshold for row in rows)
    retained = sum(row["baseline_max_iou"] >= threshold and
                   row["final_max_iou"] >= threshold for row in rows)
    added = sum(row["baseline_max_iou"] < threshold <= row["final_max_iou"]
                for row in rows)
    lost = sum(row["final_max_iou"] < threshold <= row["baseline_max_iou"]
               for row in rows)
    return {
        "annotation_rows": len(rows), "baseline_covered": baseline,
        "retained_covered": retained, "final_covered": final,
        "added_vs_baseline": added, "lost_vs_baseline": lost,
        "net_vs_baseline": added - lost,
        "baseline_coverage_rate": safe_rate(baseline, len(rows)),
        "final_coverage_rate": safe_rate(final, len(rows)),
    }


def summarize_coverage(coverage_rows: list[dict[str, object]],
                       configs: list[Config], windows: list[Window]
                       ) -> tuple[list[dict[str, object]], list[dict[str, object]],
                                  list[dict[str, object]], list[dict[str, object]]]:
    window_metrics = []
    object_metrics = []
    time_metrics = []
    by_config_window_label: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in coverage_rows:
        by_config_window_label[(row["config_id"], row["window_id"], row["label"])].append(row)
    for config in configs:
        for window in windows:
            for label in ("ped", "vehicle"):
                subset = by_config_window_label[(config.config_id, window.window_id, label)]
                for threshold in IOU_THRESHOLDS:
                    window_metrics.append({
                        "config_id": config.config_id, "family": config.family,
                        "window_id": window.window_id, "label": label,
                        "iou_threshold": threshold,
                        **coverage_counts(subset, threshold),
                    })
                by_object: dict[str, list[dict[str, object]]] = defaultdict(list)
                by_time: dict[int, list[dict[str, object]]] = defaultdict(list)
                for row in subset:
                    by_object[row["object_id"]].append(row)
                    by_time[(int(row["frame_index"]) - window.start) // TIME_BIN_FRAMES].append(row)
                for object_id, object_rows in sorted(by_object.items()):
                    for threshold in IOU_THRESHOLDS:
                        object_metrics.append({
                            "config_id": config.config_id, "window_id": window.window_id,
                            "label": label, "object_id": object_id,
                            "iou_threshold": threshold,
                            **coverage_counts(object_rows, threshold),
                        })
                for time_bin, time_rows in sorted(by_time.items()):
                    for threshold in IOU_THRESHOLDS:
                        time_metrics.append({
                            "config_id": config.config_id, "window_id": window.window_id,
                            "label": label, "time_bin": time_bin,
                            "first_frame": window.start + time_bin * TIME_BIN_FRAMES,
                            "last_frame": min(window.end, window.start +
                                              (time_bin + 1) * TIME_BIN_FRAMES - 1),
                            "iou_threshold": threshold,
                            **coverage_counts(time_rows, threshold),
                        })

    aggregate_metrics = []
    for config in configs:
        for label in ("ped", "vehicle"):
            for threshold in IOU_THRESHOLDS:
                rows = [row for row in window_metrics
                        if row["config_id"] == config.config_id and row["label"] == label and
                        row["iou_threshold"] == threshold]
                objects = [row for row in object_metrics
                           if row["config_id"] == config.config_id and row["label"] == label and
                           row["iou_threshold"] == threshold]
                times = [row for row in time_metrics
                         if row["config_id"] == config.config_id and row["label"] == label and
                         row["iou_threshold"] == threshold]
                count = sum(row["annotation_rows"] for row in rows)
                baseline = sum(row["baseline_covered"] for row in rows)
                retained = sum(row["retained_covered"] for row in rows)
                final = sum(row["final_covered"] for row in rows)
                added = sum(row["added_vs_baseline"] for row in rows)
                lost = sum(row["lost_vs_baseline"] for row in rows)
                aggregate_metrics.append({
                    "config_id": config.config_id, "family": config.family,
                    "label": label, "iou_threshold": threshold,
                    "window_count": len(rows), "annotation_rows": count,
                    "baseline_covered": baseline, "retained_covered": retained,
                    "final_covered": final,
                    "added_vs_baseline": added, "lost_vs_baseline": lost,
                    "net_vs_baseline": added - lost,
                    "micro_coverage_rate": safe_rate(final, count),
                    "window_macro_coverage_rate": (lambda valid:
                        sum(valid) / len(valid) if valid else None)([
                            row["final_coverage_rate"] for row in rows
                            if row["final_coverage_rate"] is not None]),
                    "object_macro_coverage_rate": (
                        sum(row["final_coverage_rate"] for row in objects) / len(objects)
                        if objects else None),
                    "time_bin_macro_coverage_rate": (
                        sum(row["final_coverage_rate"] for row in times) / len(times)
                        if times else None),
                })
    return window_metrics, aggregate_metrics, object_metrics, time_metrics


def add_vehicle_loss_metrics(coverage_rows: list[dict[str, object]],
                             configs: list[Config], aggregate_rows: list[dict[str, object]],
                             windows: list[Window]) -> list[dict[str, object]]:
    lookup = {(row["config_id"], row["window_id"], row["annotation_key"]): row
              for row in coverage_rows if row["label"] == "vehicle"}
    detailed = []
    for aggregate in aggregate_rows:
        if aggregate["label"] != "vehicle":
            aggregate["vehicle_old_loss_recovered"] = None
            aggregate["vehicle_old_loss_residual"] = None
            aggregate["vehicle_new_loss"] = None
            continue
        config = next(item for item in configs if item.config_id == aggregate["config_id"])
        if config.perspective_threshold is None or config.family not in {
                "guarded_fill_only", "guarded_replace"}:
            aggregate["vehicle_old_loss_recovered"] = None
            aggregate["vehicle_old_loss_residual"] = None
            aggregate["vehicle_new_loss"] = None
            continue
        old_id = f"control_internal8_to4_T{config.perspective_threshold}"
        threshold = float(aggregate["iou_threshold"])
        recovered = 0
        residual = 0
        new_loss = 0
        guarded_rows = [row for row in coverage_rows
                        if row["config_id"] == config.config_id and row["label"] == "vehicle"]
        for row in guarded_rows:
            old = lookup[(old_id, row["window_id"], row["annotation_key"])]
            baseline_covered = row["baseline_max_iou"] >= threshold
            old_covered = old["final_max_iou"] >= threshold
            guarded_covered = row["final_max_iou"] >= threshold
            recovered += baseline_covered and not old_covered and guarded_covered
            residual += baseline_covered and not old_covered and not guarded_covered
            new_loss += baseline_covered and old_covered and not guarded_covered
        aggregate["vehicle_old_loss_recovered"] = recovered
        aggregate["vehicle_old_loss_residual"] = residual
        aggregate["vehicle_new_loss"] = new_loss
        for window in windows:
            subset = [row for row in guarded_rows if row["window_id"] == window.window_id]
            old_loss = recovered_window = residual_window = new_window = 0
            for row in subset:
                old = lookup[(old_id, row["window_id"], row["annotation_key"])]
                baseline_covered = row["baseline_max_iou"] >= threshold
                old_covered = old["final_max_iou"] >= threshold
                guarded_covered = row["final_max_iou"] >= threshold
                old_loss += baseline_covered and not old_covered
                recovered_window += baseline_covered and not old_covered and guarded_covered
                residual_window += baseline_covered and not old_covered and not guarded_covered
                new_window += baseline_covered and old_covered and not guarded_covered
            detailed.append({
                "config_id": config.config_id, "family": config.family,
                "window_id": window.window_id, "legacy_config_id": old_id,
                "iou_threshold": threshold, "old_loss_rows": old_loss,
                "old_loss_recovered_rows": recovered_window,
                "old_loss_residual_rows": residual_window,
                "new_loss_rows": new_window,
                "old_loss_recovery_rate": safe_rate(recovered_window, old_loss),
            })
    return detailed


def build_loss_intervals(coverage_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Collapse frames containing one or more baseline losses into consecutive intervals."""
    result = []
    grouped: dict[tuple[str, str, str, str, float], dict[int, int]] = defaultdict(
        lambda: defaultdict(int))
    for row in coverage_rows:
        for threshold in IOU_THRESHOLDS:
            if row["final_max_iou"] < threshold <= row["baseline_max_iou"]:
                grouped[(row["config_id"], row["window_id"], row["label"],
                         row["object_id"], threshold)][
                    int(row["frame_index"])] += 1
    for (config_id, window_id, label, object_id, threshold), frame_counts in sorted(
            grouped.items()):
        frames = sorted(frame_counts)
        start = previous = frames[0]
        rows_lost = frame_counts[start]
        for frame in frames[1:]:
            if frame == previous + 1:
                previous = frame
                rows_lost += frame_counts[frame]
                continue
            result.append({"config_id": config_id, "window_id": window_id,
                           "label": label, "object_id": object_id,
                           "iou_threshold": threshold,
                           "first_frame": start, "last_frame": previous,
                           "frame_count": previous - start + 1,
                           "lost_annotation_rows": rows_lost})
            start = previous = frame
            rows_lost = frame_counts[frame]
        result.append({"config_id": config_id, "window_id": window_id,
                       "label": label, "object_id": object_id,
                       "iou_threshold": threshold,
                       "first_frame": start, "last_frame": previous,
                       "frame_count": previous - start + 1,
                       "lost_annotation_rows": rows_lost})
    return result


def build_vehicle_zero_loss_gates(window_metrics: list[dict[str, object]]) -> list[dict[str, object]]:
    return [{"config_id": row["config_id"], "family": row["family"],
             "window_id": row["window_id"], "iou_threshold": row["iou_threshold"],
             "vehicle_lost_vs_baseline": row["lost_vs_baseline"],
             "zero_vehicle_loss_gate": "pass" if row["lost_vs_baseline"] == 0 else "fail"}
            for row in window_metrics
            if row["label"] == "vehicle" and row["iou_threshold"] in {0.25, 0.5}]


def run(args: argparse.Namespace) -> dict[str, object]:
    for path in (args.annotations, args.catalog, args.output):
        reject_sealed_path(path)
    windows = [parse_window(item) for item in args.windows]
    if len({window.window_id for window in windows}) != len(windows):
        raise ValueError("duplicate windows")
    configs = build_configs()
    if args.output_prefix and any(character in args.output_prefix for character in "\\/:"):
        raise ValueError("output prefix must be a plain filename prefix")
    legacy_reference_files = {
        name: LEGACY_000206_REFERENCE / name
        for name in ("report.json", "annotation_row_coverage.csv")
    }
    missing_legacy = [str(path) for path in legacy_reference_files.values()
                      if not path.is_file()]
    if missing_legacy:
        raise ValueError("missing frozen legacy 000206 reference: " + ", ".join(missing_legacy))
    legacy_coverage_hash = digest(legacy_reference_files["annotation_row_coverage.csv"])
    annotations_by_frame, annotations_by_window = load_annotations(args.annotations, windows)
    cache, video_receipts, clip_meta = cache_components(args.catalog, args.annotations, windows)
    coverage_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, object]] = []
    event_rows: list[dict[str, object]] = []
    reason_counter: Counter[tuple[str, str, str]] = Counter()
    selection_counter: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)

    for window in windows:
        width = int(clip_meta[window.clip_id]["width"])
        height = int(clip_meta[window.clip_id]["height"])
        for frame in range(window.start, window.end + 1):
            components = cache[(window.clip_id, frame)]
            baseline = main_pool(components)
            for config in configs:
                outputs, events, diagnostics = select_config(
                    components, config, width // SAMPLE_STRIDE,
                    height // SAMPLE_STRIDE)
                if diagnostics["internal_candidates"] > 8 or len(outputs) > 4:
                    raise AssertionError("budget invariant failed")
                counter = selection_counter[(config.config_id, window.window_id)]
                counter.update(diagnostics)
                counter["frames"] += 1
                for rank in range(4):
                    possible = any(row["baseline_main_rank"] == rank for row in baseline)
                    retained = any(row.get("baseline_main_rank") == rank for row in outputs)
                    counter[f"rank{rank}_possible"] += possible
                    counter[f"rank{rank}_retained"] += retained
                for slot, output in enumerate(outputs):
                    component = output["component"]
                    candidate_rows.append({
                        "config_id": config.config_id, "family": config.family,
                        "window_id": window.window_id, "frame_index": frame,
                        "output_slot": slot, "branch": output["branch"],
                        "component_label": component.label,
                        "component_area": component.area,
                        "component_peak_difference": component.peak_difference,
                        "baseline_main_rank": output.get("baseline_main_rank"),
                        "small_rank": output.get("small_rank"),
                        "reason_code": output["reason_code"],
                        "raw_analysis_box": list(output["raw_box"]),
                        "selected_analysis_box": list(output["selected_box"]),
                        "selected_source_box": list(source_box(
                            output["selected_box"], SAMPLE_STRIDE, width, height)),
                    })
                for event in events:
                    component = event["component"]
                    reason_counter[(config.config_id, window.window_id,
                                    event["reason_code"])] += 1
                    event_rows.append({
                        "config_id": config.config_id, "family": config.family,
                        "window_id": window.window_id, "frame_index": frame,
                        "component_label": component.label,
                        "component_area": component.area,
                        "raw_bbox_area": raw_bbox_area(component),
                        "component_peak_difference": component.peak_difference,
                        "small_rank": event.get("small_rank"),
                        "reason_code": event["reason_code"],
                        "selected_analysis_box": (list(event["selected_box"])
                                                  if event.get("selected_box") else None),
                    })
                for annotation in annotations_by_frame.get((window.clip_id, frame), []):
                    baseline_iou, _ = maximum_iou(
                        annotation["annotation_box"], baseline, width, height)
                    final_iou, matched = maximum_iou(
                        annotation["annotation_box"], outputs, width, height)
                    coverage_rows.append({
                        "config_id": config.config_id, "family": config.family,
                        "window_id": window.window_id,
                        "annotation_key": annotation["annotation_key"],
                        "annotation_csv_line": annotation["annotation_csv_line"],
                        "frame_index": frame, "label": annotation["label"],
                        "object_id": annotation["object_id"],
                        "annotation_box": list(annotation["annotation_box"]),
                        "baseline_max_iou": baseline_iou,
                        "final_max_iou": final_iou,
                        "matched_branch": matched["branch"] if matched else "",
                        "matched_component_label": (
                            matched["component"].label if matched else ""),
                    })

    window_metrics, aggregate_metrics, object_metrics, time_metrics = summarize_coverage(
        coverage_rows, configs, windows)
    vehicle_loss_metrics = add_vehicle_loss_metrics(
        coverage_rows, configs, aggregate_metrics, windows)
    for row in vehicle_loss_metrics:
        row["legacy_reference_annotation_coverage_sha256"] = legacy_coverage_hash
    legacy_561_rows = [row for row in vehicle_loss_metrics
                       if row["window_id"].startswith(
                           "VIRAT_S_000206_07_001501_001600:600-1499") and
                       row["legacy_config_id"] == "control_internal8_to4_T100" and
                       row["iou_threshold"] == 0.25]
    if not legacy_561_rows or any(row["old_loss_rows"] != 561 for row in legacy_561_rows):
        raise AssertionError("recomputed T100/IoU0.25 000206 old-loss set is not 561 rows")
    loss_intervals = build_loss_intervals(coverage_rows)
    vehicle_zero_loss_gates = build_vehicle_zero_loss_gates(window_metrics)
    selection_rows = []
    for config in configs:
        for window in windows:
            counter = selection_counter[(config.config_id, window.window_id)]
            row = {"config_id": config.config_id, "family": config.family,
                   "window_id": window.window_id, **dict(counter)}
            possible = sum(counter[f"rank{rank}_possible"] for rank in range(4))
            retained = sum(counter[f"rank{rank}_retained"] for rank in range(4))
            row["baseline_main_possible"] = possible
            row["baseline_main_retained"] = retained
            row["baseline_main_retention_rate"] = safe_rate(retained, possible)
            selection_rows.append(row)
    reason_rows = [
        {"config_id": config_id, "window_id": window_id,
         "reason_code": reason, "count": count}
        for (config_id, window_id, reason), count in sorted(reason_counter.items())]

    args.output.mkdir(parents=True, exist_ok=True)
    logical_outputs = {
        "selected_candidates.csv": candidate_rows,
        "decision_events.csv": event_rows,
        "annotation_coverage.csv": coverage_rows,
        "window_metrics.csv": window_metrics,
        "aggregate_metrics.csv": aggregate_metrics,
        "selection_metrics.csv": selection_rows,
        "reason_counts.csv": reason_rows,
        "object_metrics.csv": object_metrics,
        "time_metrics.csv": time_metrics,
        "loss_intervals.csv": loss_intervals,
        "vehicle_old_loss_metrics.csv": vehicle_loss_metrics,
        "vehicle_zero_loss_gates.csv": vehicle_zero_loss_gates,
    }
    outputs = {f"{args.output_prefix}{filename}": rows
               for filename, rows in logical_outputs.items()}
    for filename, rows in outputs.items():
        write_csv(args.output / filename, rows)
    script_path = Path(__file__)
    dependency_paths = [script_path.with_name("fixed_budget_candidate_prototype.py"),
                        script_path.with_name("candidate_chain_reference.py")]
    report = {
        "status": "guarded_final4_development_sweep_not_rtl_or_acceptance_evidence",
        "windows": [window.__dict__ | {"window_id": window.window_id}
                    for window in windows],
        "configuration_count": len(configs),
        "configurations": [config.__dict__ for config in configs],
        "contract": {
            "main_pool": "area>=16, sort area desc then component label asc, take four",
            "small_pool": (
                "area 2..15, sort peak_difference desc then area desc then label asc, "
                "take four before qualification; rejected pool entries are not replaced "
                "from outside the bounded top four"),
            "qualification": "area>=4 and 4*area>=raw_bbox_area and peak_difference>=P",
            "perspective": (
                "center_y>=T uses top-anchored minimum 6x16 with top margin two; "
                "otherwise center-expanded minimum 4x4"),
            "main_structure": (
                "Original main boxes keep order and are never NMS-filtered. Small boxes "
                "fill empty slots after NMS against all original mains and accepted smalls."),
            "replacement": (
                "Only when original main count is four: M[0:3] are protected; at most one "
                "small replaces M[3], requiring m3.area<Aweak, small.peak>=m3.peak+delta, "
                "and expanded-small IoU<=0.3 against every original main box. The first "
                "qualified peak-ranked small satisfying all guards wins."),
            "output_order": (
                "No replacement: original mains in rank order followed by accepted fill "
                "smalls in small-rank order. Replacement: M0,M1,M2,replacement-small."),
            "fill_only": "For each T, P is fixed at 40 and replacement is disabled.",
            "budgets": "internal pool <=8 and final output <=4 asserted on every frame/config",
            "reason_codes": REASON_CODES,
            "legacy_controls": (
                "baseline, main3_small1, main2_small2 and internal8_to4 use their original "
                "selection semantics; new qualification guards are not applied."),
        },
        "metric_contract": {
            "coverage_iou_thresholds": list(IOU_THRESHOLDS),
            "baseline_added_lost_net": (
                "Compared row-wise with the common unmodified area-top4 baseline."),
            "vehicle_old_loss_recovered": (
                "Baseline-covered vehicle row lost by old internal8 at the same T and "
                "covered by guarded output."),
            "vehicle_new_loss": (
                "Baseline-covered vehicle row retained by old internal8 at the same T but "
                "lost by guarded output."),
            "retained_covered": "Rows covered by both the common baseline and final output.",
            "object_aggregate": (
                "Per-object baseline/retained/final/added/lost/net counts and mean of "
                "per-object annotation-row coverage rates."),
            "time_aggregate": (
                f"Per-{TIME_BIN_FRAMES}-frame-bin baseline/retained/final/added/lost/net "
                "counts, plus consecutive loss-frame intervals."),
            "vehicle_zero_loss_gate": (
                "Pre-registered development configuration gate: pass only when per-window "
                "vehicle lost_vs_baseline is zero at IoU 0.25 and 0.5. This gate selects "
                "a development configuration; it is not final product acceptance."),
        },
        "inputs": {"catalog": str(args.catalog.resolve()),
                   "annotations": str(args.annotations.resolve()),
                   "videos": video_receipts},
        "input_hashes": {"catalog_sha256": digest(args.catalog),
                         "annotations_sha256": digest(args.annotations)},
        "script_hashes": {"guarded_tool_sha256": digest(script_path),
                          "fixed_budget_dependency_sha256": digest(dependency_paths[0]),
                          "candidate_chain_dependency_sha256": digest(dependency_paths[1])},
        "legacy_000206_reference": {
            "purpose": (
                "Provenance receipt for the previously reported T100 internal8 vehicle "
                "loss set (561 rows at IoU 0.25). Metrics are recomputed from the common "
                "control in this run; this reference is not used as a scoring input."),
            "files": {name: {"path": str(path.resolve()), "sha256": digest(path)}
                      for name, path in legacy_reference_files.items()},
        },
        "output_hashes": {filename: digest(args.output / filename)
                          for filename in outputs},
        "boundary": (
            "Development train/validation windows only. VIRAT annotation rows are "
            "temporally correlated and incomplete; candidate geometry coverage is not "
            "object recall, classifier recall or false-positive rate. Python connected "
            "components do not model RTL label/run overflow or cycle timing. No blind, "
            "holdout or reserve path is accepted."),
    }
    report["report_payload_sha256"] = canonical_digest(report)
    report_path = args.output / f"{args.output_prefix}report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["report_path"] = str(report_path.resolve())
    return report


def self_test() -> None:
    def component(label: int, area: int, box: tuple[int, int, int, int],
                  peak: int) -> Component:
        return Component(label, area, *box, area / raw_area(box), float(peak), peak)

    def raw_area(box: tuple[int, int, int, int]) -> int:
        return (box[2] - box[0] + 1) * (box[3] - box[1] + 1)

    mains = [component(1, 80, (0, 0, 9, 7), 90),
             component(2, 60, (20, 0, 29, 5), 80),
             component(3, 40, (40, 0, 49, 3), 70),
             component(4, 20, (60, 0, 64, 3), 50)]
    good = component(5, 8, (80, 20, 83, 21), 100)
    sparse = component(6, 4, (90, 20, 97, 23), 120)
    tiny = component(7, 3, (100, 20, 101, 21), 130)
    low_peak = component(8, 8, (110, 20, 113, 21), 30)
    config = Config("test", "guarded_replace", 110, 40, 16, 32, True)
    outputs, events, diagnostics = guarded_select(
        mains + [good, sparse, tiny, low_peak], config, 256, 144)
    assert [row["component"].label for row in outputs] == [1, 2, 3, 5]
    assert outputs[3]["reason_code"] == "REPLACE_WEAK_M3"
    reasons = Counter(row["reason_code"] for row in events)
    assert reasons["REJECT_AREA_LT4"] == 1
    assert reasons["REJECT_DENSITY_LT_QUARTER"] == 1
    assert reasons["REJECT_PEAK_FLOOR"] == 1
    assert reasons["DROP_WEAK_M3"] == 1
    assert diagnostics["internal_candidates"] == 8 and len(outputs) == 4

    fill_outputs, fill_events, _ = guarded_select(
        mains[:2] + [good, component(9, 8, (120, 20, 123, 21), 95)],
        Config("fill", "guarded_fill_only", 110, 40, None, None, False),
        256, 144)
    assert [row["reason_code"] for row in fill_outputs] == [
        "KEEP_MAIN", "KEEP_MAIN", "FILL_EMPTY_SLOT", "FILL_EMPTY_SLOT"]
    assert len(fill_outputs) == 4 and not any(
        row["reason_code"] == "REPLACE_WEAK_M3" for row in fill_events)
    assert len(build_configs()) == 37
    try:
        reject_sealed_path(Path("blind_reserve"))
    except ValueError:
        pass
    else:
        raise AssertionError("sealed path guard did not trigger")
    print("PASS: qualification, protected replacement, fill order, budgets and sealed-input guard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/catalog.json"))
    parser.add_argument("--annotations", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/annotations.csv"))
    parser.add_argument("--window", action="append", dest="windows")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--output-prefix", default="",
                        help="plain filename prefix, useful when output must be an existing directory")
    parser.add_argument("--self-test", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.output is None:
        parser.error("--output is required unless --self-test")
    args.windows = args.windows or list(DEFAULT_WINDOWS)
    report = run(args)
    print(json.dumps({"status": report["status"],
                      "windows": len(report["windows"]),
                      "configurations": report["configuration_count"],
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
