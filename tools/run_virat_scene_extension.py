#!/usr/bin/env python3
"""Build a sealed development-validation extension for VIRAT 010107.

The source video is decoded once from frame zero.  The deployed Python
background/candidate reference is warmed for about five seconds, then both the
area-top4 baseline and the existing guarded fill-only T100 policy are recorded
over three contiguous time intervals.  Review representatives are thinned to
at most one member per temporal track in any 30-source-frame span.

This tool does not train, tune a threshold, modify the historical catalog, read
sealed test/blind/holdout material, import samples, or modify RTL.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import cv2
import numpy as np


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
TOOLS = PROJECT / "tools"
EXTERNAL = PROJECT / "external_reference_exploration"
for directory in (TOOLS, EXTERNAL):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from candidate_chain_reference import CandidateChainReference  # noqa: E402
from fixed_budget_candidate_prototype import (  # noqa: E402
    Component,
    extract_components,
    inclusive_iou,
    source_box,
)
from guarded_final4_arbitration import (  # noqa: E402
    Config,
    baseline_select,
    guarded_select,
)
from opencv_hog_candidate_diagnostic import (  # noqa: E402
    extract_variant,
    load_models,
    make_hog324,
    model_score,
    quantization_contract,
    quantized_score,
)
from roi_dataset_tool import fpga_resize_roi  # noqa: E402


CLIP_ID = "VIRAT_S_010107_02_000282_000312"
SCENE_ID = "virat-ground-010107"
SPLIT = "val"
VIDEO_ITEM_ID = "56f587b88d777f753209cb94"
VIDEO_SHA512 = (
    "a65ff0da41b340ba85033e8e9423b239377151b7a133203f4328e0f697566441"
    "07b731ee5ec78377b3804ff4cd12677f4720d8d8ea421aecc7ff63955de07ecd"
)
ANNOTATION_ITEM_ID = "56f57eeb8d777f753209c28f"
ANNOTATION_SHA512 = (
    "1d045de5fc97c0f823e2fb91880f30f80929f688b6c9e8d2054cd2c90265a62"
    "f1e10114b12b572474edd43d58f988b233b60f56bba4a096341b14f2f4dd7c468"
)
VIDEO = PROJECT / "public_data/raw/virat_ground_v2/video_original" / f"{CLIP_ID}.mp4"
ANNOTATIONS = VIDEO.with_suffix(".viratdata.objects.txt")
HISTORICAL_CATALOG = PROJECT / "evaluation/public_data/virat_ground_v2/catalog.json"
ROI_CONTRACT = PROJECT / "evaluation/experiment_roi_contract_v1.json"
MODEL_DIR = PROJECT / "external_reference_exploration/results/opencv_hog_diagnostic"
DEFAULT_OUTPUT = PROJECT / "evaluation/scene_extensions/virat_010107_02_t100"

SAMPLE_STRIDE = 5
WARMUP_SECONDS = 5.0
LEARN_FRAMES = 4
FOREGROUND_THRESHOLD = 20
MAIN_MIN_AREA = 16
PERSPECTIVE_THRESHOLD = 100
PEAK_FLOOR = 40
FINAL_BUDGET = 4
REPRESENTATIVE_GAP = 30
ASSOCIATION_GAP = 5
ASSOCIATION_IOU = 0.3
ASSOCIATION_CENTER_DELTA = 3.0
ANNOTATION_TRACK_IOU = 0.1
IOU_THRESHOLDS = (0.1, 0.25, 0.5)
FORBIDDEN_TOKEN = re.compile(r"(^|[_\-.])(test|blind|holdout|reserve)($|[_\-.])", re.I)
FORBIDDEN_CLIP = re.compile(r"000205|000207|010106|010108", re.I)

DEPENDENCIES = (
    ROI_CONTRACT,
    TOOLS / "candidate_chain_reference.py",
    TOOLS / "fixed_budget_candidate_prototype.py",
    TOOLS / "guarded_final4_arbitration.py",
    TOOLS / "hog_reference.py",
    TOOLS / "roi_dataset_tool.py",
    EXTERNAL / "opencv_hog_candidate_diagnostic.py",
    EXTERNAL / "opencv_hog_diagnostic.py",
)

HUMAN_FIELDS = (
    "review_class",
    "candidate_condition",
    "crop_usable",
    "occlusion",
    "truncation_reason",
    "same_frame_new_target",
    "duplicate_of_baseline",
    "duplicate_baseline_number",
    "reviewer",
    "reviewed_at",
    "review_basis",
    "review_note",
)
CANDIDATE_CONDITIONS = (
    "complete", "truncated", "merged", "background_fragment", "other",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha512(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pixel_sha256(image: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(image, dtype=np.uint8).tobytes()).hexdigest()


def canonical_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def json_compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    if fields is None:
        if not rows:
            raise ValueError(f"cannot infer fields for empty CSV: {path}")
        fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n", extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def reject_sealed(path: Path, role: str) -> None:
    for part in path.resolve().parts:
        if FORBIDDEN_TOKEN.search(part) or FORBIDDEN_CLIP.search(part):
            raise ValueError(f"sealed-data guard rejected {role}: {part}")


def validate_inputs(output: Path) -> None:
    for role, path in (
        ("video", VIDEO), ("annotations", ANNOTATIONS),
        ("historical catalog", HISTORICAL_CATALOG), ("ROI contract", ROI_CONTRACT),
        ("model directory", MODEL_DIR), ("output", output),
    ):
        reject_sealed(path, role)
    if CLIP_ID != VIDEO.stem or FORBIDDEN_CLIP.search(CLIP_ID):
        raise ValueError("unexpected or sealed clip ID")
    for path in (VIDEO, ANNOTATIONS, HISTORICAL_CATALOG, ROI_CONTRACT, *DEPENDENCIES):
        if not path.is_file():
            raise FileNotFoundError(path)
    contract = json.loads(ROI_CONTRACT.read_text(encoding="utf-8"))
    if contract.get("contract_id") != "experiment_roi_contract_v1":
        raise ValueError("experiment ROI contract ID changed")
    pixel = contract.get("pixel_pipeline", {})
    required = {
        "analysis_sampling": "take every fifth source pixel in x and y to form 256x144",
        "crop_box": "T100_selected_analysis_box",
        "crop_coordinates": "inclusive x0,y0,x1,y1",
        "resize": "fpga_resize_roi deterministic nearest-neighbor to 32x32 uint8",
    }
    for key, expected in required.items():
        if pixel.get(key) != expected:
            raise ValueError(f"ROI contract changed at {key}")
    if SPLIT not in contract.get("input_scope", {}).get("allowed_splits", []):
        raise ValueError("validation overlay split not allowed by ROI contract")
    expected_scoring_hash = contract.get("sealed_inputs", {}).get("hog_candidate_script_sha256")
    actual_scoring_hash = sha256(EXTERNAL / "opencv_hog_candidate_diagnostic.py")
    if expected_scoring_hash != actual_scoring_hash:
        raise ValueError("candidate HOG scoring script no longer matches ROI contract")
    actual_video_sha512 = sha512(VIDEO)
    actual_annotation_sha512 = sha512(ANNOTATIONS)
    if actual_video_sha512 != VIDEO_SHA512:
        raise ValueError(
            f"official video SHA512 mismatch for item {VIDEO_ITEM_ID}: {actual_video_sha512}"
        )
    if actual_annotation_sha512 != ANNOTATION_SHA512:
        raise ValueError(
            f"official annotation SHA512 mismatch for item {ANNOTATION_ITEM_ID}: "
            f"{actual_annotation_sha512}"
        )


def intervals(frame_count: int, warmup_frames: int) -> list[tuple[str, int, int]]:
    remaining = frame_count - warmup_frames
    if remaining < 3:
        raise ValueError("not enough frames after warmup")
    base, extra = divmod(remaining, 3)
    output = []
    start = warmup_frames
    for index in range(3):
        length = base + (1 if index < extra else 0)
        end = start + length - 1
        output.append((f"interval_{index + 1}", start, end))
        start = end + 1
    if output[-1][2] != frame_count - 1:
        raise AssertionError("interval partition does not cover remaining video")
    return output


def interval_for(frame_index: int, values: list[tuple[str, int, int]]) -> str:
    for name, start, end in values:
        if start <= frame_index <= end:
            return name
    raise ValueError(f"frame outside scoring intervals: {frame_index}")


def parse_annotations(frame_count: int) -> tuple[dict[int, list[dict[str, Any]]], dict[str, Any]]:
    by_frame: dict[int, list[dict[str, Any]]] = defaultdict(list)
    type_counts: Counter[str] = Counter()
    excluded = 0
    line_count = 0
    with ANNOTATIONS.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            values = line.split()
            if len(values) != 8:
                raise ValueError(f"annotation line {line_number} does not have eight columns")
            object_id, duration, frame, x, y, width, height, raw_type = map(int, values)
            line_count += 1
            type_counts[str(raw_type)] += 1
            if frame < 0 or frame >= frame_count:
                excluded += 1
                continue
            if width <= 0 or height <= 0:
                raise ValueError(f"nonpositive annotation box at line {line_number}")
            label = {1: "ped", 2: "vehicle", 3: "vehicle"}.get(raw_type, "ignore")
            row = {
                "annotation_key": f"{CLIP_ID}:line{line_number}",
                "annotation_line": line_number,
                "object_id": object_id,
                "declared_track_duration": duration,
                "frame_index": frame,
                "box": (x, y, x + width - 1, y + height - 1),
                "raw_type": raw_type,
                "label": label,
            }
            by_frame[frame].append(row)
    return by_frame, {
        "rows": line_count,
        "valid_rows": sum(len(rows) for rows in by_frame.values()),
        "excluded_out_of_range_rows": excluded,
        "raw_type_counts": dict(sorted(type_counts.items())),
        "frame_index_contract": "zero-based; out-of-range rows excluded without shifting",
    }


def best_annotation(box: tuple[int, int, int, int], annotations: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, float | None]:
    candidates = []
    for row in annotations:
        if row["label"] not in {"ped", "vehicle"}:
            continue
        score = inclusive_iou(box, row["box"])
        candidates.append((-score, row["object_id"], row["annotation_line"], row))
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: item[:3])
    best_iou = -candidates[0][0]
    if best_iou < ANNOTATION_TRACK_IOU:
        return None, None
    return candidates[0][3], best_iou


def center(box: tuple[int, int, int, int]) -> tuple[float, float]:
    return (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0


@dataclass
class TemporalTrack:
    track_id: str
    frame_index: int
    box: tuple[int, int, int, int]


class RepresentativeSampler:
    def __init__(self) -> None:
        self._next_track = 0
        self._active: dict[str, TemporalTrack] = {}
        self._last_representative: dict[str, int] = {}

    def assign(self, frame_index: int, box: tuple[int, int, int, int],
               annotation: dict[str, Any] | None, annotation_iou: float | None,
               used_this_frame: set[str]) -> tuple[str, bool, str]:
        if annotation is not None and annotation_iou is not None:
            track_id = f"annotation_object_{annotation['object_id']}"
            basis = "annotation_object_iou_ge_0p1"
        else:
            cx, cy = center(box)
            eligible = []
            for track_id, state in self._active.items():
                if track_id in used_this_frame or frame_index - state.frame_index > ASSOCIATION_GAP:
                    continue
                old_cx, old_cy = center(state.box)
                overlap = inclusive_iou(box, state.box)
                if (overlap >= ASSOCIATION_IOU and abs(cx - old_cx) <= ASSOCIATION_CENTER_DELTA
                        and abs(cy - old_cy) <= ASSOCIATION_CENTER_DELTA):
                    eligible.append((-overlap, abs(cx - old_cx) + abs(cy - old_cy), track_id))
            if eligible:
                eligible.sort()
                track_id = eligible[0][2]
                basis = "temporal_geometry_iou_center"
            else:
                track_id = f"unmatched_track_{self._next_track:05d}"
                self._next_track += 1
                basis = "new_unmatched_temporal_track"
        used_this_frame.add(track_id)
        self._active[track_id] = TemporalTrack(track_id, frame_index, box)
        last = self._last_representative.get(track_id)
        selected = last is None or frame_index - last >= REPRESENTATIVE_GAP
        if selected:
            self._last_representative[track_id] = frame_index
        return track_id, selected, basis


def box_text(box: tuple[int, int, int, int]) -> str:
    return json_compact(list(box))


def save_image(path: Path, image: np.ndarray, params: list[int] | None = None) -> str:
    if not cv2.imwrite(str(path), image, params or []):
        raise ValueError(f"failed to write image: {path}")
    return sha256(path)


def render_review_assets(output: Path, sample_id: str, frame: np.ndarray,
                         source_candidate_box: tuple[int, int, int, int],
                         source_raw_box: tuple[int, int, int, int], roi: np.ndarray,
                         label: str,
                         baseline_boxes: list[tuple[int, int, int, int]],
                         fill_boxes: list[tuple[tuple[int, int, int, int], str]]) -> dict[str, str]:
    frames = output / "review_frames"
    rois = output / "review_rois_32x32"
    frames.mkdir(exist_ok=True)
    rois.mkdir(exist_ok=True)
    annotated = frame.copy()
    # Draw all same-frame policies.  Shared main boxes retain a blue outer
    # baseline stroke and a thin green fill-final stroke, so both are visible.
    for rank, box in enumerate(baseline_boxes):
        cv2.rectangle(annotated, box[:2], box[2:], (255, 80, 0), 4)
        cv2.putText(annotated, f"B{rank}", (box[0], max(18, box[1] - 7)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 80, 0), 2, cv2.LINE_AA)
    for rank, (box, branch) in enumerate(fill_boxes):
        color = (0, 190, 0) if branch == "main_area_topk" else (255, 0, 255)
        thickness = 1 if branch == "main_area_topk" else 3
        cv2.rectangle(annotated, box[:2], box[2:], color, thickness)
        cv2.putText(annotated, f"F{rank}", (box[2] - 24, min(710, box[3] + 18)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    # Raw component (orange) and the current selected fill output (yellow outer
    # halo) remain separately visible for crop-shape review.
    cv2.rectangle(annotated, source_raw_box[:2], source_raw_box[2:], (0, 128, 255), 1)
    sx0, sy0, sx1, sy1 = source_candidate_box
    halo = (max(0, sx0 - 4), max(0, sy0 - 4), min(1279, sx1 + 4), min(719, sy1 + 4))
    cv2.rectangle(annotated, halo[:2], halo[2:], (0, 255, 255), 3)
    cv2.putText(annotated, "SELECT", (halo[0], max(20, halo[1] - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.58, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(annotated, (0, 0), (1279, 66), (20, 20, 20), -1)
    legends = [
        ("baseline B#", (255, 80, 0)), ("fill-main F#", (0, 190, 0)),
        ("fill-small F#", (255, 0, 255)), ("selected halo", (0, 255, 255)),
        ("raw component", (0, 128, 255)),
    ]
    x = 14
    for text, color in legends:
        cv2.line(annotated, (x, 20), (x + 28, 20), color, 5)
        cv2.putText(annotated, text, (x + 34, 27), cv2.FONT_HERSHEY_SIMPLEX,
                    0.48, (245, 245, 245), 1, cv2.LINE_AA)
        x += 230
    cv2.putText(annotated, f"{sample_id} {label}", (14, 57), cv2.FONT_HERSHEY_SIMPLEX,
                0.62, (255, 255, 255), 2, cv2.LINE_AA)
    roi_preview = cv2.resize(roi, (160, 160), interpolation=cv2.INTER_NEAREST)
    roi_preview = cv2.cvtColor(roi_preview, cv2.COLOR_GRAY2BGR)
    annotated[545:705, 14:174] = roi_preview
    cv2.rectangle(annotated, (12, 543), (176, 707), (0, 255, 255), 3)
    cv2.putText(annotated, "SELECTED 32x32 ROI", (14, 535), cv2.FONT_HERSHEY_SIMPLEX,
                0.52, (0, 255, 255), 2, cv2.LINE_AA)
    frame_path = frames / f"{sample_id}.jpg"
    roi_path = rois / f"{sample_id}.png"
    frame_hash = save_image(frame_path, annotated, [cv2.IMWRITE_JPEG_QUALITY, 94])
    roi_hash = save_image(roi_path, roi)
    return {
        "review_frame_path": frame_path.relative_to(output).as_posix(),
        "review_frame_sha256": frame_hash,
        "roi_32x32_path": roi_path.relative_to(output).as_posix(),
        "roi_file_sha256": roi_hash,
        "roi_pixel_sha256": pixel_sha256(roi),
    }


def render_mapping_qa(output: Path, frame_index: int, frame: np.ndarray,
                      annotations: list[dict[str, Any]]) -> dict[str, Any]:
    qa_dir = output / "mapping_qa"
    qa_dir.mkdir(exist_ok=True)
    image = frame.copy()
    colors = {"ped": (0, 220, 0), "vehicle": (255, 100, 0), "ignore": (150, 150, 150)}
    for row in annotations:
        box = row["box"]
        color = colors[row["label"]]
        cv2.rectangle(image, box[:2], box[2:], color, 2)
        cv2.putText(image, f"id{row['object_id']} t{row['raw_type']}",
                    (box[0], max(16, box[1] - 4)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.42, color, 1, cv2.LINE_AA)
    cv2.rectangle(image, (0, 0), (1279, 52), (20, 20, 20), -1)
    cv2.putText(image, f"official VIRAT mapping QA frame {frame_index}", (14, 23),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(image, "green=type1 ped  blue=type2/3 vehicle  gray=ignored type",
                (14, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (235, 235, 235), 1, cv2.LINE_AA)
    path = qa_dir / f"frame_{frame_index:06d}_official_annotations.jpg"
    digest = save_image(path, image, [cv2.IMWRITE_JPEG_QUALITY, 94])
    return {
        "frame_index": frame_index,
        "path": path.relative_to(output).as_posix(),
        "sha256": digest,
        "annotation_count": len(annotations),
        "annotation_label_counts": dict(sorted(Counter(row["label"] for row in annotations).items())),
    }


def render_mapping_qa_contact_sheet(output: Path, receipts: list[dict[str, Any]]) -> dict[str, Any]:
    if len(receipts) != 3:
        raise ValueError("mapping QA contact sheet requires first/middle/last receipts")
    canvas = np.full((2160, 1280, 3), 245, dtype=np.uint8)
    for index, receipt in enumerate(receipts):
        image = cv2.imread(str(output / receipt["path"]), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"cannot reopen mapping QA image: {receipt['path']}")
        view = cv2.resize(image, (1200, 675), interpolation=cv2.INTER_AREA)
        top = 25 + index * 710
        canvas[top:top + 675, 40:1240] = view
    path = output / "mapping_qa/contact_sheet_first_middle_last.jpg"
    digest = save_image(path, canvas, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return {"path": path.relative_to(output).as_posix(), "sha256": digest,
            "frame_indices": [row["frame_index"] for row in receipts]}


def score_roi(roi: np.ndarray, parameters: dict[str, Any], hog324: cv2.HOGDescriptor,
              q_contract: dict[str, Any]) -> dict[str, Any]:
    f64 = extract_variant(roi, "current_rtl64", hog324)
    f324 = extract_variant(roi, "opencv_hog324", hog324)
    score64 = model_score(f64, parameters["current_rtl64"])
    score324 = model_score(f324, parameters["opencv_hog324"])
    score324_q, score324_q_normalized = quantized_score(f324, q_contract)
    return {
        "hog64_feature_sha256": hashlib.sha256(f64.astype("<f8").tobytes()).hexdigest(),
        "hog64_score": f"{score64:.12g}",
        "hog64_prediction": "vehicle" if score64 >= 0 else "ped",
        "hog324_feature_sha256": hashlib.sha256(f324.astype("<f8").tobytes()).hexdigest(),
        "hog324_float_score": f"{score324:.12g}",
        "hog324_float_prediction": "vehicle" if score324 >= 0 else "ped",
        "hog324_q_score_integer": str(score324_q),
        "hog324_q_score_normalized": f"{score324_q_normalized:.12g}",
        "hog324_q_prediction": "vehicle" if score324_q >= 0 else "ped",
    }


def output_row(frame_index: int, interval_id: str, strategy: str, slot: int,
               entry: dict[str, Any], frame_width: int, frame_height: int,
               score: dict[str, Any], roi_hash: str, annotation: dict[str, Any] | None,
               annotation_iou: float | None) -> dict[str, Any]:
    component: Component = entry["component"]
    selected_box = tuple(entry["selected_box"])
    raw_box = tuple(entry["raw_box"])
    selected_source = source_box(selected_box, SAMPLE_STRIDE, frame_width, frame_height)
    raw_source = source_box(raw_box, SAMPLE_STRIDE, frame_width, frame_height)
    return {
        "candidate_id": f"{strategy}:f{frame_index:06d}:slot{slot}:cc{component.label}",
        "clip_id": CLIP_ID,
        "scene_id": SCENE_ID,
        "split_overlay": SPLIT,
        "interval_id": interval_id,
        "frame_index": frame_index,
        "strategy": strategy,
        "slot": slot,
        "branch": entry["branch"],
        "reason_code": entry["reason_code"],
        "component_label": component.label,
        "component_area": component.area,
        "component_fill_ratio": f"{component.fill_ratio:.9g}",
        "component_mean_difference": f"{component.mean_difference:.9g}",
        "component_peak_difference": component.peak_difference,
        "baseline_main_rank": "" if entry.get("baseline_main_rank") is None else entry["baseline_main_rank"],
        "raw_analysis_box": box_text(raw_box),
        "selected_analysis_box": box_text(selected_box),
        "raw_source_box": box_text(raw_source),
        "selected_source_box": box_text(selected_source),
        "roi_pixel_sha256": roi_hash,
        "annotation_hint_object_id": "" if annotation is None else annotation["object_id"],
        "annotation_hint_label": "" if annotation is None else annotation["label"],
        "annotation_hint_iou": "" if annotation_iou is None else f"{annotation_iou:.9g}",
        **score,
    }


def coverage_rows(annotations_by_frame: dict[int, list[dict[str, Any]]],
                  candidate_boxes: dict[tuple[str, int], list[tuple[str, tuple[int, int, int, int]]]],
                  scoring_start: int) -> list[dict[str, Any]]:
    output = []
    for frame_index in sorted(frame for frame in annotations_by_frame if frame >= scoring_start):
        for annotation in annotations_by_frame[frame_index]:
            if annotation["label"] not in {"ped", "vehicle"}:
                continue
            row: dict[str, Any] = {
                "annotation_key": annotation["annotation_key"],
                "clip_id": CLIP_ID,
                "split_overlay": SPLIT,
                "frame_index": frame_index,
                "object_id": annotation["object_id"],
                "label": annotation["label"],
                "annotation_box": box_text(annotation["box"]),
            }
            for strategy in ("baseline_main4", "fill_only_T100"):
                choices = candidate_boxes.get((strategy, frame_index), [])
                ranked = sorted(
                    ((-inclusive_iou(annotation["box"], box), candidate_id)
                     for candidate_id, box in choices),
                    key=lambda item: (item[0], item[1]),
                )
                best_iou = -ranked[0][0] if ranked else 0.0
                row[f"{strategy}_best_iou"] = f"{best_iou:.9g}"
                row[f"{strategy}_best_candidate_id"] = ranked[0][1] if ranked else ""
                for threshold in IOU_THRESHOLDS:
                    suffix = str(threshold).replace(".", "p")
                    row[f"{strategy}_covered_iou_{suffix}"] = "yes" if best_iou >= threshold else "no"
            output.append(row)
    return output


def make_contact_sheets(output: Path, manifest: list[dict[str, Any]], per_page: int = 6) -> list[dict[str, Any]]:
    sheets = output / "contact_sheets"
    sheets.mkdir(exist_ok=True)
    receipts = []
    for page_index, start in enumerate(range(0, len(manifest), per_page), 1):
        page_rows = manifest[start:start + per_page]
        canvas = np.full((1500, 1600, 3), 245, dtype=np.uint8)
        for local, row in enumerate(page_rows):
            cell_x = (local % 2) * 800
            cell_y = (local // 2) * 500
            frame = cv2.imread(str(output / row["review_frame_path"]), cv2.IMREAD_COLOR)
            roi = cv2.imread(str(output / row["roi_32x32_path"]), cv2.IMREAD_GRAYSCALE)
            if frame is None or roi is None:
                raise ValueError(f"failed to reopen review asset: {row['sample_id']}")
            view = cv2.resize(frame, (760, 428), interpolation=cv2.INTER_AREA)
            canvas[cell_y + 48:cell_y + 476, cell_x + 20:cell_x + 780] = view
            enlarged = cv2.resize(roi, (128, 128), interpolation=cv2.INTER_NEAREST)
            enlarged = cv2.cvtColor(enlarged, cv2.COLOR_GRAY2BGR)
            canvas[cell_y + 340:cell_y + 468, cell_x + 640:cell_x + 768] = enlarged
            text = f"{row['sample_id']} f{row['frame_index']} {row['branch']}"
            cv2.putText(canvas, text, (cell_x + 20, cell_y + 32), cv2.FONT_HERSHEY_SIMPLEX,
                        0.62, (20, 20, 20), 2, cv2.LINE_AA)
        path = sheets / f"contact_sheet_{page_index:02d}.jpg"
        digest = save_image(path, canvas, [cv2.IMWRITE_JPEG_QUALITY, 92])
        receipts.append({"path": path.relative_to(output).as_posix(), "sha256": digest,
                         "sample_count": len(page_rows)})
    return receipts


def summarize_coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for strategy in ("baseline_main4", "fill_only_T100"):
        result[strategy] = {}
        for label in ("ped", "vehicle"):
            selected = [row for row in rows if row["label"] == label]
            result[strategy][label] = {
                "annotation_frame_rows": len(selected),
                **{
                    f"covered_iou_{str(threshold).replace('.', 'p')}": sum(
                        row[f"{strategy}_covered_iou_{str(threshold).replace('.', 'p')}"] == "yes"
                        for row in selected)
                    for threshold in IOU_THRESHOLDS
                },
            }
    return result


def finalize_artifacts_and_receipt(output: Path, receipt: dict[str, Any],
                                   mode: str) -> str:
    """Hash final artifacts, then write a non-self-referential receipt.

    Every file that can affect review is finalized before this function runs.
    artifact_hashes.json excludes itself and receipt.json; receipt.json binds
    that inventory plus the final report, manifest, overlay, and script.
    """
    required = (
        output / "split_overlay.json",
        output / "report.json",
        output / "review_manifest.csv",
    )
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(f"cannot finalize missing artifact: {path}")
    artifacts: dict[str, str] = {}
    for path in sorted(output.rglob("*")):
        relative = path.relative_to(output).as_posix()
        if path.is_file() and path.name not in {"artifact_hashes.json", "receipt.json"}:
            artifacts[relative] = sha256(path)
    artifact_path = output / "artifact_hashes.json"
    canonical_json(artifact_path, artifacts)
    receipt.update({
        "script": {"path": str(SCRIPT), "sha256": sha256(SCRIPT)},
        "split_overlay_sha256": sha256(output / "split_overlay.json"),
        "report_sha256": sha256(output / "report.json"),
        "review_manifest_sha256": sha256(output / "review_manifest.csv"),
        "artifact_hashes_sha256": sha256(artifact_path),
        "artifact_count": len(artifacts),
        "finalization": {
            "mode": mode,
            "ordering": "final artifacts -> artifact_hashes.json -> receipt.json",
            "receipt_self_hash_included": False,
        },
    })
    receipt_path = output / "receipt.json"
    canonical_json(receipt_path, receipt)
    # Independent in-process readback catches stale or incorrectly ordered
    # receipt fields before the command reports success.
    reloaded = json.loads(receipt_path.read_text(encoding="utf-8"))
    expected = {
        "split_overlay_sha256": sha256(output / "split_overlay.json"),
        "report_sha256": sha256(output / "report.json"),
        "review_manifest_sha256": sha256(output / "review_manifest.csv"),
        "artifact_hashes_sha256": sha256(artifact_path),
    }
    for key, value in expected.items():
        if reloaded.get(key) != value:
            raise AssertionError(f"receipt finalization mismatch for {key}")
    if reloaded.get("script", {}).get("sha256") != sha256(SCRIPT):
        raise AssertionError("receipt finalization mismatch for script SHA256")
    inventory = json.loads(artifact_path.read_text(encoding="utf-8"))
    for relative, expected_hash in inventory.items():
        if sha256(output / relative) != expected_hash:
            raise AssertionError(f"artifact inventory mismatch after finalization: {relative}")
    return sha256(receipt_path)


def finalize_existing(output: Path) -> dict[str, Any]:
    """Finalize existing outputs only; never open video, labels, or models."""
    output = output.resolve()
    reject_sealed(output, "existing output")
    manifest_path = output / "review_manifest.csv"
    report_path = output / "report.json"
    receipt_path = output / "receipt.json"
    for path in (manifest_path, report_path, receipt_path, output / "split_overlay.json"):
        if not path.is_file():
            raise FileNotFoundError(path)
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("review manifest has no header")
        fields = list(reader.fieldnames)
        rows = list(reader)
    if "candidate_condition" not in fields:
        if "review_class" not in fields:
            raise ValueError("review manifest lacks review_class anchor")
        fields.insert(fields.index("review_class") + 1, "candidate_condition")
        for row in rows:
            row["candidate_condition"] = ""
    if any(row.get("candidate_condition", "") for row in rows):
        raise ValueError("existing candidate_condition values must remain blank before human review")
    if any(row.get(field, "") for row in rows for field in HUMAN_FIELDS):
        raise ValueError("human review fields must remain blank during offline finalization")
    write_csv(manifest_path, rows, fields)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    review_sampling = report.setdefault("review_sampling", {})
    review_sampling["authoritative_human_input"] = "review_manifest.csv"
    review_sampling["human_fields_initialized_blank"] = list(HUMAN_FIELDS)
    review_sampling["candidate_condition_contract"] = {
        "allowed_values": list(CANDIDATE_CONDITIONS),
        "initial_value": "blank",
        "semantics": (
            "Human-visible candidate condition independent of automatic annotation hints "
            "and model scores."
        ),
    }
    report.setdefault("limitations", []).append(
        "candidate_condition is pending human review and is never inferred from annotations or model scores."
    )
    # Avoid duplicate limitation on repeated offline finalization.
    report["limitations"] = list(dict.fromkeys(report["limitations"]))
    canonical_json(report_path, report)

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["status"] = "complete_hash_bound_development_extension_human_review_pending"
    receipt.setdefault("assertions", {})["all_human_fields_blank"] = True
    receipt["assertions"]["candidate_condition_blank_pending_human_review"] = True
    receipt["boundary"] = (
        "CSV review_manifest.csv is the sole authoritative human-input artifact; "
        "candidate_condition allows complete|truncated|merged|background_fragment|other; "
        "no XLSX is generated."
    )
    receipt_hash = finalize_artifacts_and_receipt(
        output, receipt, "existing_outputs_only_no_video_annotation_or_model_access")
    return {
        "status": "existing_outputs_finalized",
        "review_rows": len(rows),
        "candidate_condition_blank": True,
        "artifact_count": json.loads((output / "receipt.json").read_text(encoding="utf-8"))["artifact_count"],
        "receipt_sha256": receipt_hash,
        "output": str(output),
    }


def run(output: Path) -> dict[str, Any]:
    output = output.resolve()
    validate_inputs(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    catalog_hash_before = sha256(HISTORICAL_CATALOG)

    capture = cv2.VideoCapture(str(VIDEO))
    if not capture.isOpened():
        raise ValueError(f"cannot open source video: {VIDEO}")
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (width, height) != (1280, 720) or frame_count <= 0 or fps <= 0:
        raise ValueError("source video metadata violates the 1280x720 positive-FPS contract")
    warmup_frames = int(round(WARMUP_SECONDS * fps))
    scoring_intervals = intervals(frame_count, warmup_frames)
    annotations_by_frame, annotation_receipt = parse_annotations(frame_count)
    parameters, model_report, model_receipt = load_models(MODEL_DIR)
    hog324 = make_hog324()
    q_contract = quantization_contract(parameters["opencv_hog324"])
    chain = CandidateChainReference(
        learn_frames=LEARN_FRAMES, threshold=FOREGROUND_THRESHOLD,
        min_neighbors=3, min_area=MAIN_MIN_AREA, update_enable=True,
        freeze_foreground=True, min_run=2, top_k=4, sample_stride=SAMPLE_STRIDE,
    )
    baseline_config = Config("baseline_main4", "baseline", None, None, None, None, False)
    fill_config = Config("fill_only_T100", "guarded_fill_only", PERSPECTIVE_THRESHOLD,
                         PEAK_FLOOR, None, None, False)
    sampler = RepresentativeSampler()
    candidate_rows: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    candidate_boxes: dict[tuple[str, int], list[tuple[str, tuple[int, int, int, int]]]] = defaultdict(list)
    reason_counts: Counter[str] = Counter()
    mapping_qa_indices = {0, frame_count // 2, frame_count - 1}
    mapping_qa_receipts: list[dict[str, Any]] = []
    processed = 0
    try:
        for frame_index in range(frame_count):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"decode stopped at frame {frame_index} of {frame_count}")
            processed += 1
            if frame_index in mapping_qa_indices:
                mapping_qa_receipts.append(render_mapping_qa(
                    output, frame_index, frame, annotations_by_frame.get(frame_index, [])))
            result = chain.process_bgr(frame, frame_index)
            if frame_index < warmup_frames:
                continue
            interval_id = interval_for(frame_index, scoring_intervals)
            components = extract_components(result["run_filtered_mask"], result["difference"])
            baseline, _, baseline_diag = baseline_select(components)
            fill, events, fill_diag = guarded_select(components, fill_config, 256, 144)
            if len(baseline) > FINAL_BUDGET or len(fill) > FINAL_BUDGET:
                raise AssertionError("final candidate budget exceeded")
            if [row["component"].label for row in fill[:len(baseline)]] != [
                    row["component"].label for row in baseline]:
                raise AssertionError("fill-only did not preserve all baseline mains in order")
            for event in events:
                reason_counts[str(event["reason_code"])] += 1
            diagnostics.append({
                "frame_index": frame_index, "interval_id": interval_id,
                "component_count": len(components),
                "foreground_pixels_after_min_run": result["foreground_pixels_after_min_run"],
                "baseline_main_count": baseline_diag["final_candidates"],
                "fill_final_count": fill_diag["final_candidates"],
                "fill_small_pool_count": fill_diag["small_pool_candidates"],
                "fill_empty_slots": fill_diag["empty_slots"],
            })
            evaluation_cache: dict[tuple[int, tuple[int, int, int, int]], tuple[np.ndarray, dict[str, Any], str]] = {}
            for entry in fill:
                component: Component = entry["component"]
                selected_box = tuple(entry["selected_box"])
                key = (component.label, selected_box)
                x0, y0, x1, y1 = selected_box
                roi = fpga_resize_roi(result["gray"][y0:y1 + 1, x0:x1 + 1])
                evaluation_cache[key] = (roi, score_roi(roi, parameters, hog324, q_contract), pixel_sha256(roi))
            rows_this_frame: dict[str, list[dict[str, Any]]] = {}
            for strategy, selected in ((baseline_config.config_id, baseline), (fill_config.config_id, fill)):
                rows_this_frame[strategy] = []
                for slot, entry in enumerate(selected):
                    component: Component = entry["component"]
                    selected_box = tuple(entry["selected_box"])
                    key = (component.label, selected_box)
                    if key not in evaluation_cache:
                        x0, y0, x1, y1 = selected_box
                        roi = fpga_resize_roi(result["gray"][y0:y1 + 1, x0:x1 + 1])
                        evaluation_cache[key] = (roi, score_roi(roi, parameters, hog324, q_contract), pixel_sha256(roi))
                    roi, score, roi_hash = evaluation_cache[key]
                    candidate_source = source_box(selected_box, SAMPLE_STRIDE, width, height)
                    annotation, annotation_iou = best_annotation(
                        candidate_source, annotations_by_frame.get(frame_index, []))
                    row = output_row(frame_index, interval_id, strategy, slot, entry,
                                     width, height, score, roi_hash, annotation, annotation_iou)
                    candidate_rows.append(row)
                    rows_this_frame[strategy].append(row)
                    candidate_boxes[(strategy, frame_index)].append((row["candidate_id"], candidate_source))
            used_tracks: set[str] = set()
            baseline_source_boxes = [
                tuple(json.loads(item["selected_source_box"]))
                for item in rows_this_frame[baseline_config.config_id]
            ]
            fill_source_boxes = [
                (tuple(json.loads(item["selected_source_box"])), item["branch"])
                for item in rows_this_frame[fill_config.config_id]
            ]
            for slot, (entry, row) in enumerate(zip(fill, rows_this_frame[fill_config.config_id])):
                annotation, annotation_iou = best_annotation(
                    tuple(json.loads(row["selected_source_box"])),
                    annotations_by_frame.get(frame_index, []))
                track_id, selected_rep, association_basis = sampler.assign(
                    frame_index, tuple(entry["selected_box"]), annotation, annotation_iou, used_tracks)
                if not selected_rep:
                    continue
                sample_id = f"vr{len(manifest):05d}"
                roi, _, _ = evaluation_cache[(entry["component"].label, tuple(entry["selected_box"]))]
                assets = render_review_assets(
                    output, sample_id, frame,
                    tuple(json.loads(row["selected_source_box"])),
                    tuple(json.loads(row["raw_source_box"])), roi,
                    f"{row['branch']} {row['reason_code']}",
                    baseline_source_boxes,
                    fill_source_boxes,
                )
                review = {
                    "sample_id": sample_id,
                    "candidate_id": row["candidate_id"],
                    "clip_id": CLIP_ID,
                    "scene_id": SCENE_ID,
                    "split_overlay": SPLIT,
                    "interval_id": interval_id,
                    "frame_index": frame_index,
                    "timestamp_ms": f"{1000.0 * frame_index / fps:.6f}",
                    "slot": slot,
                    "branch": row["branch"],
                    "reason_code": row["reason_code"],
                    "component_label": row["component_label"],
                    "component_area": row["component_area"],
                    "component_peak_difference": row["component_peak_difference"],
                    "raw_analysis_box": row["raw_analysis_box"],
                    "selected_analysis_box": row["selected_analysis_box"],
                    "selected_source_box": row["selected_source_box"],
                    "baseline_member": "yes" if row["branch"] == "main_area_topk" else "no",
                    "temporal_track_id": track_id,
                    "temporal_association_basis": association_basis,
                    "representative_gap_source_frames": REPRESENTATIVE_GAP,
                    "annotation_hint_object_id": row["annotation_hint_object_id"],
                    "annotation_hint_label": row["annotation_hint_label"],
                    "annotation_hint_iou": row["annotation_hint_iou"],
                    **assets,
                    "hog64_score": row["hog64_score"],
                    "hog64_prediction": row["hog64_prediction"],
                    "hog324_float_score": row["hog324_float_score"],
                    "hog324_float_prediction": row["hog324_float_prediction"],
                    "hog324_q_score_integer": row["hog324_q_score_integer"],
                    "hog324_q_score_normalized": row["hog324_q_score_normalized"],
                    "hog324_q_prediction": row["hog324_q_prediction"],
                    **{field: "" for field in HUMAN_FIELDS},
                }
                manifest.append(review)
    finally:
        capture.release()
    if processed != frame_count:
        raise AssertionError("source video was not decoded exactly once from frame zero")
    by_track: dict[str, list[int]] = defaultdict(list)
    for row in manifest:
        by_track[row["temporal_track_id"]].append(int(row["frame_index"]))
    for track_id, frames in by_track.items():
        frames.sort()
        if any(right - left < REPRESENTATIVE_GAP for left, right in zip(frames, frames[1:])):
            raise AssertionError(f"representative gap violated for {track_id}")
    if any(row[field] for row in manifest for field in HUMAN_FIELDS):
        raise AssertionError("human review fields must remain blank")
    for row in candidate_rows:
        hint_values = (row["annotation_hint_object_id"], row["annotation_hint_label"],
                       row["annotation_hint_iou"])
        if row["annotation_hint_iou"] == "":
            if any(hint_values):
                raise AssertionError("sub-threshold annotation hint fields must all be blank")
        elif (not row["annotation_hint_object_id"] or not row["annotation_hint_label"]
              or float(row["annotation_hint_iou"]) < ANNOTATION_TRACK_IOU):
            raise AssertionError("nonblank annotation hint violates the IoU>=0.1 contract")
    mapping_qa_receipts.sort(key=lambda row: row["frame_index"])
    if [row["frame_index"] for row in mapping_qa_receipts] != sorted(mapping_qa_indices):
        raise AssertionError("first/middle/last mapping QA frames were not all rendered")

    coverage = coverage_rows(annotations_by_frame, candidate_boxes, warmup_frames)
    contact_sheets = make_contact_sheets(output, manifest)
    mapping_qa_contact_sheet = render_mapping_qa_contact_sheet(output, mapping_qa_receipts)
    candidate_path = output / "candidates.csv"
    diagnostic_path = output / "frame_diagnostics.csv"
    coverage_path = output / "annotation_coverage.csv"
    manifest_path = output / "review_manifest.csv"
    write_csv(candidate_path, candidate_rows)
    write_csv(diagnostic_path, diagnostics)
    write_csv(coverage_path, coverage)
    write_csv(manifest_path, manifest)

    overlay = {
        "overlay_id": "virat_010107_development_validation_extension_v1",
        "status": "development_validation_extension_not_catalog_commit_not_blind",
        "clip_id": CLIP_ID,
        "scene_id": SCENE_ID,
        "split": SPLIT,
        "purpose": "new fixed-camera development validation extension",
        "historical_catalog": str(HISTORICAL_CATALOG.resolve()),
        "historical_catalog_sha256": catalog_hash_before,
        "historical_catalog_modified": False,
        "video": str(VIDEO.resolve()),
        "video_sha256": sha256(VIDEO),
        "annotations": str(ANNOTATIONS.resolve()),
        "annotations_sha256": sha256(ANNOTATIONS),
        "source_collection_url": "https://data.kitware.com/#collection/56f56db28d777f753209ba9f",
        "video_item_id": VIDEO_ITEM_ID,
        "video_item_url": f"https://data.kitware.com/api/v1/item/{VIDEO_ITEM_ID}",
        "video_download_url": f"https://data.kitware.com/api/v1/item/{VIDEO_ITEM_ID}/download",
        "video_sha512": VIDEO_SHA512,
        "annotation_item_id": ANNOTATION_ITEM_ID,
        "annotation_item_url": f"https://data.kitware.com/api/v1/item/{ANNOTATION_ITEM_ID}",
        "annotation_download_url": f"https://data.kitware.com/api/v1/item/{ANNOTATION_ITEM_ID}/download",
        "annotation_sha512": ANNOTATION_SHA512,
        "license_agreement": "VIRAT Video Dataset Usage Agreement, 1-4-11",
        "license_url": "https://viratdata.org/resources/VIRAT-Video-Data-Set-Protection-Agreement-1-4-11.pdf",
        "boundary": "Local overlay only; it does not rewrite or append the historical catalog.",
    }
    overlay_path = output / "split_overlay.json"
    canonical_json(overlay_path, overlay)
    if sha256(HISTORICAL_CATALOG) != catalog_hash_before:
        raise AssertionError("historical catalog changed during extension run")

    model_prediction_counts = {
        key: dict(sorted(Counter(row[key] for row in candidate_rows
                                 if row["strategy"] == "fill_only_T100").items()))
        for key in ("hog64_prediction", "hog324_float_prediction", "hog324_q_prediction")
    }
    report = {
        "status": "development_review_batch_ready_human_fields_blank_no_training_no_tuning",
        "clip": {
            "clip_id": CLIP_ID, "scene_id": SCENE_ID, "split_overlay": SPLIT,
            "frame_count": frame_count, "fps": fps, "width": width, "height": height,
            "decoded_once_from_frame_zero": True,
        },
        "causal_timing": {
            "background_model_learn_frames": LEARN_FRAMES,
            "warmup_frames_not_scored": warmup_frames,
            "warmup_seconds_actual": warmup_frames / fps,
            "scoring_intervals_inclusive": [
                {"interval_id": name, "start": start, "end": end, "frames": end - start + 1}
                for name, start, end in scoring_intervals
            ],
        },
        "candidate_contract": {
            "baseline": "area>=16, area-desc/label-asc top4",
            "fill_only": "baseline mains preserved; qualified peak-difference small pool fills only empty slots",
            "perspective_threshold": PERSPECTIVE_THRESHOLD,
            "peak_floor": PEAK_FLOOR,
            "main_min_area": MAIN_MIN_AREA,
            "final_budget": FINAL_BUDGET,
            "roi_contract_id": "experiment_roi_contract_v1",
            "no_replacement": True,
        },
        "counts": {
            "candidate_rows": len(candidate_rows),
            "by_strategy": dict(sorted(Counter(row["strategy"] for row in candidate_rows).items())),
            "fill_by_branch": dict(sorted(Counter(row["branch"] for row in candidate_rows
                                                        if row["strategy"] == "fill_only_T100").items())),
            "review_representatives": len(manifest),
            "review_by_interval": dict(sorted(Counter(row["interval_id"] for row in manifest).items())),
            "review_by_branch": dict(sorted(Counter(row["branch"] for row in manifest).items())),
            "unique_temporal_tracks": len(by_track),
            "fill_event_reasons": dict(sorted(reason_counts.items())),
        },
        "annotation_receipt": annotation_receipt,
        "annotation_geometry_coverage": summarize_coverage(coverage),
        "existing_model_scores": {
            "training_performed": False,
            "threshold_tuning_performed": False,
            "score_semantics": "binary SVM margin; positive means vehicle; not a probability; no invalid rejection",
            "fill_prediction_counts": model_prediction_counts,
            "hog324_float_quantized_prediction_mismatch": sum(
                row["hog324_float_prediction"] != row["hog324_q_prediction"]
                for row in candidate_rows if row["strategy"] == "fill_only_T100"
            ),
            "source_model_status": model_report.get("status"),
        },
        "review_sampling": {
            "authoritative_human_input": "review_manifest.csv",
            "human_fields_initialized_blank": list(HUMAN_FIELDS),
            "candidate_condition_contract": {
                "allowed_values": list(CANDIDATE_CONDITIONS),
                "initial_value": "blank",
                "semantics": "Human-visible candidate condition independent of automatic annotation hints and model scores.",
            },
            "rule": "annotation object track when IoU>=0.1, otherwise deterministic short temporal geometry chain; greedy representatives are at least 30 source frames apart per track",
            "representative_gap_source_frames": REPRESENTATIVE_GAP,
            "association_gap_source_frames": ASSOCIATION_GAP,
            "association_iou_min": ASSOCIATION_IOU,
            "association_center_each_axis_max_analysis_pixels": ASSOCIATION_CENTER_DELTA,
            "visual_content_used_for_selection": False,
        },
        "inputs": {
            "video": {
                "path": str(VIDEO.resolve()), "sha256": sha256(VIDEO), "sha512": sha512(VIDEO),
                "official_item_id": VIDEO_ITEM_ID,
                "official_download_url": f"https://data.kitware.com/api/v1/item/{VIDEO_ITEM_ID}/download",
                "bytes": VIDEO.stat().st_size,
            },
            "annotations": {
                "path": str(ANNOTATIONS.resolve()), "sha256": sha256(ANNOTATIONS),
                "sha512": sha512(ANNOTATIONS), "official_item_id": ANNOTATION_ITEM_ID,
                "official_download_url": f"https://data.kitware.com/api/v1/item/{ANNOTATION_ITEM_ID}/download",
                "bytes": ANNOTATIONS.stat().st_size,
            },
            "historical_catalog": {"path": str(HISTORICAL_CATALOG.resolve()), "sha256": catalog_hash_before, "modified": False},
            "experiment_roi_contract": {"path": str(ROI_CONTRACT.resolve()), "sha256": sha256(ROI_CONTRACT)},
            "models": model_receipt,
            "dependency_hashes": {str(path.relative_to(PROJECT)).replace("\\", "/"): sha256(path)
                                  for path in DEPENDENCIES},
        },
        "outputs": {
            "review_manifest": "review_manifest.csv", "candidates": "candidates.csv",
            "annotation_coverage": "annotation_coverage.csv", "frame_diagnostics": "frame_diagnostics.csv",
            "split_overlay": "split_overlay.json", "contact_sheets": contact_sheets,
            "mapping_qa": {
                "frames": mapping_qa_receipts,
                "contact_sheet": mapping_qa_contact_sheet,
                "coordinate_contract": "official VIRAT 0-based source-frame inclusive boxes rendered directly on decoded 1280x720 frames",
            },
        },
        "limitations": [
            "VIRAT object annotations are not exhaustive; annotation hints and geometry coverage are not human labels or end-to-end recall.",
            "Automatic model outputs are uncalibrated binary margins and cannot reject invalid candidates.",
            "OpenCV HOG324 extraction remains floating point; quantization covers descriptor output and the linear model only.",
            "This new scene is development validation evidence, not a sealed blind test or production acceptance result.",
            "The Python component model does not implement RTL run/label overflow or cycle timing.",
        ],
    }
    report_path = output / "report.json"
    canonical_json(report_path, report)

    receipt = {
        "status": "complete_hash_bound_development_extension_human_review_pending",
        "source_hashes": report["inputs"],
        "assertions": {
            "single_video_decode_pass": processed == frame_count,
            "catalog_unchanged": sha256(HISTORICAL_CATALOG) == catalog_hash_before,
            "official_video_sha512_match": sha512(VIDEO) == VIDEO_SHA512,
            "official_annotation_sha512_match": sha512(ANNOTATIONS) == ANNOTATION_SHA512,
            "all_human_fields_blank": True,
            "candidate_condition_blank_pending_human_review": True,
            "subthreshold_annotation_hints_blank": all(
                row["annotation_hint_iou"] == "" or float(row["annotation_hint_iou"]) >= ANNOTATION_TRACK_IOU
                for row in candidate_rows
            ),
            "mapping_qa_first_middle_last_present": len(mapping_qa_receipts) == 3,
            "representative_gap_ge_30_per_track": True,
            "final_candidate_budget_le_4": True,
            "training_performed": False,
            "threshold_tuning_performed": False,
        },
        "boundary": (
            "CSV review_manifest.csv is the sole authoritative human-input artifact; "
            "candidate_condition allows complete|truncated|merged|background_fragment|other; "
            "no XLSX is generated."
        ),
    }
    receipt_hash = finalize_artifacts_and_receipt(output, receipt, "full_generation")
    return {
        "status": report["status"], "output": str(output),
        "frames": frame_count, "warmup_frames": warmup_frames,
        "candidate_rows": len(candidate_rows), "review_representatives": len(manifest),
        "receipt_sha256": receipt_hash,
        "coverage": report["annotation_geometry_coverage"],
    }


def self_test() -> None:
    assert intervals(479, 120) == [
        ("interval_1", 120, 239), ("interval_2", 240, 359), ("interval_3", 360, 478)
    ]
    reject_sealed(Path("safe/virat_010107"), "safe")
    for unsafe in (Path("x/blind/y"), Path("x/holdout/y"), Path("x/test/y"), Path("x/010108/y")):
        try:
            reject_sealed(unsafe, "self-test")
        except ValueError:
            pass
        else:
            raise AssertionError(f"sealed guard accepted {unsafe}")
    sampler = RepresentativeSampler()
    used: set[str] = set()
    track, selected, _ = sampler.assign(10, (1, 1, 4, 4), None, 0.0, used)
    assert selected
    used = set()
    same, selected, _ = sampler.assign(15, (1, 1, 4, 4), None, 0.0, used)
    assert same == track and not selected
    for frame_index in (20, 25, 30, 35):
        used = set()
        same, selected, _ = sampler.assign(frame_index, (1, 1, 4, 4), None, 0.0, used)
        assert same == track and not selected
    used = set()
    same, selected, _ = sampler.assign(40, (1, 1, 4, 4), None, 0.0, used)
    assert same == track and selected
    components = [
        Component(1, 20, 10, 10, 14, 13, 1.0, 60.0, 80),
        Component(2, 6, 40, 115, 41, 117, 1.0, 70.0, 90),
    ]
    baseline, _, _ = baseline_select(components)
    fill, _, diag = guarded_select(
        components, Config("fill_only_T100", "guarded_fill_only", 100, 40, None, None, False),
        256, 144,
    )
    assert len(baseline) == 1 and len(fill) == 2 and diag["final_candidates"] <= 4
    assert fill[0]["component"].label == baseline[0]["component"].label
    annotations = [{"object_id": 7, "annotation_line": 1, "label": "ped",
                    "box": (100, 100, 109, 109)}]
    hint, overlap = best_annotation((0, 0, 9, 9), annotations)
    assert hint is None and overlap is None
    hint, overlap = best_annotation((100, 100, 109, 109), annotations)
    assert hint is annotations[0] and overlap == 1.0
    assert "candidate_condition" in HUMAN_FIELDS
    assert CANDIDATE_CONDITIONS == (
        "complete", "truncated", "merged", "background_fragment", "other")
    print("SELF_TEST_PASS")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--self-test", action="store_true")
    action.add_argument(
        "--finalize-existing", action="store_true",
        help="update the review CSV/report contract and rebuild hashes without reading source data",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    result = finalize_existing(args.output) if args.finalize_existing else run(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
