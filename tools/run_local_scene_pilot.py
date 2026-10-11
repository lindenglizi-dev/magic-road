#!/usr/bin/env python3
"""Run the bounded local-intersection baseline pilot on frames 120..1079.

The deployed Python candidate reference is advanced causally from frame zero.
Only baseline area-top4 candidates in the registered window are recorded and
scored with the existing hash-bound HOG64 and HOG324 diagnostic models.  No
labels, training, threshold tuning, fill-only arbitration, or RTL changes are
part of this tool.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import cv2
import numpy as np


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
TOOLS = PROJECT / "tools"
EXTERNAL = PROJECT / "external_reference_exploration"
for directory in (TOOLS, EXTERNAL):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from analyze_virat_failure_sources import GeometryTracker  # noqa: E402
from candidate_chain_reference import CandidateChainReference  # noqa: E402
from fixed_budget_candidate_prototype import Component, extract_components, source_box  # noqa: E402
from guarded_final4_arbitration import baseline_select  # noqa: E402
from opencv_hog_candidate_diagnostic import (  # noqa: E402
    extract_variant,
    load_models,
    make_hog324,
    model_score,
    quantization_contract,
    quantized_score,
)
from roi_dataset_tool import fpga_resize_roi  # noqa: E402


DEFAULT_VIDEO = Path(
    r"E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\public_data\raw\2415171-hd_1920_1080_24fps.mp4"
)
DEFAULT_OUTPUT = (
    PROJECT / "evaluation/local_scene_pilots/intersection_2415171_f120_1079_v1"
)
MODEL_DIR = PROJECT / "external_reference_exploration/results/opencv_hog_diagnostic"

EXPECTED_VIDEO_SHA256 = "5bd44aededccb88ac75febb170ae0f916b909277a0b4e8450adc4e33d440ea6b"
EXPECTED_WIDTH = 1280
EXPECTED_HEIGHT = 720
EXPECTED_FPS = 24000.0 / 1001.0
EXPECTED_FRAMES = 3765
START_FRAME = 120
END_FRAME = 1079
QA_FRAMES = (120, 600, 1079)
LEARN_FRAMES = 4
FOREGROUND_THRESHOLD = 20
MAIN_MIN_AREA = 16
SAMPLE_STRIDE = 5
REPRESENTATIVE_GAP = 30
CONTACT_SHEET_SIZE = 4
CLIP_ID = "local_intersection_2415171"
SCENE_ID = "local-intersection-fixed-camera-2415171"
FORBIDDEN = re.compile(r"(^|[/\\_.-])(blind|holdout|reserve|test)($|[/\\_.-])", re.I)

HUMAN_FIELDS = (
    "review_class", "semantic_subtype", "candidate_condition", "crop_usable",
    "reviewer", "reviewed_at", "review_note",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pixel_sha256(image: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(image, dtype=np.uint8).tobytes()).hexdigest()


def guard_path(path: Path) -> None:
    if FORBIDDEN.search(str(path.resolve()).replace("\\", "/")):
        raise ValueError(f"sealed path rejected: {path}")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]],
              fields: Sequence[str] | None = None) -> None:
    if fields is None:
        if not rows:
            raise ValueError(f"cannot infer fields for empty CSV: {path}")
        fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields), lineterminator="\n",
                                extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def box_text(box: tuple[int, int, int, int]) -> str:
    return json.dumps(list(box), separators=(",", ":"))


def height_bin(height: int) -> str:
    if height <= 0:
        raise ValueError("candidate height must be positive")
    if height <= 6:
        return "le_6"
    if height <= 15:
        return "7_15"
    if height <= 31:
        return "16_31"
    return "ge_32"


def score_roi(roi: np.ndarray, parameters: Mapping[str, Any],
              hog324: cv2.HOGDescriptor, q_contract: Mapping[str, Any]) -> dict[str, Any]:
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


class RepresentativeGate:
    def __init__(self, gap: int = REPRESENTATIVE_GAP) -> None:
        self.gap = gap
        self.last_by_track: dict[str, int] = {}

    def accept(self, track_id: str, frame_index: int) -> bool:
        last = self.last_by_track.get(track_id)
        selected = last is None or frame_index - last >= self.gap
        if selected:
            self.last_by_track[track_id] = frame_index
        return selected


def validate_inputs(video: Path, output: Path) -> dict[str, Any]:
    for path in (video, output, MODEL_DIR):
        guard_path(path)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")
    if sha256(video) != EXPECTED_VIDEO_SHA256:
        raise ValueError("local pilot video SHA256 mismatch")
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {video}")
    metadata = {
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": float(capture.get(cv2.CAP_PROP_FPS)),
        "frame_count": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "fourcc": int(capture.get(cv2.CAP_PROP_FOURCC)),
    }
    capture.release()
    if (
        metadata["width"] != EXPECTED_WIDTH
        or metadata["height"] != EXPECTED_HEIGHT
        or not math.isclose(metadata["fps"], EXPECTED_FPS, rel_tol=0.0, abs_tol=1e-9)
        or metadata["frame_count"] != EXPECTED_FRAMES
    ):
        raise ValueError(f"local pilot video metadata mismatch: {metadata}")
    metadata["codec_fourcc"] = "".join(
        chr((metadata["fourcc"] >> (8 * index)) & 255) for index in range(4)
    ).rstrip("\x00")
    metadata["sha256"] = EXPECTED_VIDEO_SHA256
    return metadata


def resize_letterbox(image: np.ndarray, target: tuple[int, int],
                     color: tuple[int, int, int] = (25, 25, 25)) -> np.ndarray:
    target_w, target_h = target
    scale = min(target_w / image.shape[1], target_h / image.shape[0])
    resized = cv2.resize(
        image,
        (max(1, round(image.shape[1] * scale)), max(1, round(image.shape[0] * scale))),
        interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_NEAREST,
    )
    canvas = np.full((target_h, target_w, 3), color, np.uint8)
    x = (target_w - resized.shape[1]) // 2
    y = (target_h - resized.shape[0]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def annotated_frame(frame: np.ndarray, entries: Sequence[Mapping[str, Any]],
                    selected_slot: int | None = None, title: str = "") -> np.ndarray:
    result = frame.copy()
    for slot, entry in enumerate(entries):
        component: Component = entry["component"]
        box = source_box(component.box, SAMPLE_STRIDE, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        color = (0, 255, 255) if selected_slot == slot else (255, 100, 0)
        thickness = 4 if selected_slot == slot else 2
        cv2.rectangle(result, box[:2], box[2:], color, thickness)
        cv2.putText(result, f"B{slot}", (box[0], max(20, box[1] - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.58, color, 2, cv2.LINE_AA)
    if title:
        cv2.rectangle(result, (0, 0), (1279, 46), (0, 0, 0), -1)
        cv2.putText(result, title, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.72,
                    (255, 255, 255), 2, cv2.LINE_AA)
    return result


def render_review_assets(output: Path, sample_id: str, frame: np.ndarray,
                         entries: Sequence[Mapping[str, Any]], slot: int,
                         roi: np.ndarray, row: Mapping[str, Any]) -> dict[str, str]:
    frame_dir = output / "review_frames"
    roi_dir = output / "review_rois_32x32"
    panel_dir = output / "review_panels"
    for directory in (frame_dir, roi_dir, panel_dir):
        directory.mkdir(exist_ok=True)
    full = annotated_frame(
        frame, entries, slot,
        f"{sample_id} frame {row['frame_index']} baseline B{slot} track {row['geometry_track_id']}",
    )
    frame_path = frame_dir / f"{sample_id}.jpg"
    roi_path = roi_dir / f"{sample_id}.png"
    panel_path = panel_dir / f"{sample_id}.jpg"
    if not cv2.imwrite(str(frame_path), full, [cv2.IMWRITE_JPEG_QUALITY, 94]):
        raise ValueError(f"cannot write review frame: {frame_path}")
    if not cv2.imwrite(str(roi_path), roi, [cv2.IMWRITE_PNG_COMPRESSION, 4]):
        raise ValueError(f"cannot write review ROI: {roi_path}")

    panel = np.full((450, 1000, 3), 238, np.uint8)
    panel[20:380, 20:660] = resize_letterbox(full, (640, 360), (20, 20, 20))
    roi_view = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    roi_view = cv2.resize(roi_view, (256, 256), interpolation=cv2.INTER_NEAREST)
    panel[55:311, 704:960] = roi_view
    cv2.rectangle(panel, (704, 55), (959, 310), (0, 0, 0), 2)
    cv2.putText(panel, "actual 32x32 ROI (8x nearest view)", (690, 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (20, 20, 20), 1, cv2.LINE_AA)
    lines = (
        f"box h={row['analysis_box_height']} bin={row['analysis_box_height_bin']}",
        f"HOG64={row['hog64_prediction']} score={row['hog64_score']}",
        f"HOG324 float/q={row['hog324_float_prediction']}/{row['hog324_q_prediction']}",
    )
    for index, text in enumerate(lines):
        cv2.putText(panel, text, (690, 342 + index * 29), cv2.FONT_HERSHEY_SIMPLEX,
                    0.48, (20, 20, 20), 1, cv2.LINE_AA)
    if not cv2.imwrite(str(panel_path), panel, [cv2.IMWRITE_JPEG_QUALITY, 93]):
        raise ValueError(f"cannot write review panel: {panel_path}")
    return {
        "review_frame_path": frame_path.relative_to(output).as_posix(),
        "review_frame_sha256": sha256(frame_path),
        "roi_32x32_path": roi_path.relative_to(output).as_posix(),
        "roi_file_sha256": sha256(roi_path),
        "review_panel_path": panel_path.relative_to(output).as_posix(),
        "review_panel_sha256": sha256(panel_path),
    }


def render_contact_sheets(output: Path, panel_paths: Sequence[Path]) -> list[dict[str, Any]]:
    contact_dir = output / "contact_sheets"
    contact_dir.mkdir(exist_ok=True)
    receipts = []
    for sheet_number, start in enumerate(range(0, len(panel_paths), CONTACT_SHEET_SIZE), 1):
        selected = panel_paths[start:start + CONTACT_SHEET_SIZE]
        canvas = np.full((980, 2040, 3), 245, np.uint8)
        for local_index, path in enumerate(selected):
            panel = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if panel is None:
                raise ValueError(f"cannot reopen review panel: {path}")
            view = resize_letterbox(panel, (1000, 450), (245, 245, 245))
            row, column = divmod(local_index, 2)
            x, y = 20 + 1010 * column, 20 + 470 * row
            canvas[y:y + 450, x:x + 1000] = view
            cv2.putText(canvas, path.stem, (x + 8, y + 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 0, 0), 1, cv2.LINE_AA)
        path = contact_dir / f"contact_sheet_{sheet_number:02d}.jpg"
        if not cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 91]):
            raise ValueError(f"cannot write contact sheet: {path}")
        receipts.append({
            "path": path.relative_to(output).as_posix(),
            "sha256": sha256(path),
            "sample_count": len(selected),
        })
    return receipts


def render_qa(output: Path, frame_index: int, frame: np.ndarray,
              entries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    qa_dir = output / "qa"
    qa_dir.mkdir(exist_ok=True)
    image = annotated_frame(
        frame, entries, None,
        f"local pilot QA frame {frame_index}: deployed baseline area-top4",
    )
    path = qa_dir / f"frame_{frame_index:06d}.jpg"
    if not cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, 94]):
        raise ValueError(f"cannot write QA frame: {path}")
    return {
        "frame_index": frame_index,
        "path": path.relative_to(output).as_posix(),
        "sha256": sha256(path),
        "candidate_count": len(entries),
    }


def qa_contact_sheet(output: Path, receipts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    canvas = np.full((2160, 1280, 3), 245, np.uint8)
    for index, receipt in enumerate(receipts):
        image = cv2.imread(str(output / str(receipt["path"])), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("cannot reopen QA frame")
        view = cv2.resize(image, (1200, 675), interpolation=cv2.INTER_AREA)
        top = 25 + 710 * index
        canvas[top:top + 675, 40:1240] = view
    path = output / "qa/contact_sheet_120_600_1079.jpg"
    if not cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 92]):
        raise ValueError("cannot write QA contact sheet")
    return {
        "path": path.relative_to(output).as_posix(),
        "sha256": sha256(path),
        "frame_indices": [int(item["frame_index"]) for item in receipts],
    }


def phase_diagnostic(previous: np.ndarray | None, current: np.ndarray,
                     window: np.ndarray) -> dict[str, Any]:
    gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (320, 180), interpolation=cv2.INTER_AREA).astype(np.float32)
    result = {
        "source_luma_mean": f"{float(gray.mean()):.9g}",
        "source_luma_std": f"{float(gray.std()):.9g}",
        "small_gray": small,
    }
    if previous is None:
        result.update({
            "global_shift_x_320": "", "global_shift_y_180": "",
            "global_shift_magnitude_320x180": "", "phase_response": "",
        })
    else:
        shift, response = cv2.phaseCorrelate(previous, small, window)
        result.update({
            "global_shift_x_320": f"{shift[0]:.9g}",
            "global_shift_y_180": f"{shift[1]:.9g}",
            "global_shift_magnitude_320x180": f"{math.hypot(*shift):.9g}",
            "phase_response": f"{response:.9g}",
        })
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    video = args.video.resolve()
    output = args.output.resolve()
    metadata = validate_inputs(video, output)
    parameters, model_report, model_receipt = load_models(MODEL_DIR)
    hog324 = make_hog324()
    q_contract = quantization_contract(parameters["opencv_hog324"])
    output.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {video}")
    chain = CandidateChainReference(
        learn_frames=LEARN_FRAMES, threshold=FOREGROUND_THRESHOLD,
        min_neighbors=3, min_area=MAIN_MIN_AREA, update_enable=True,
        freeze_foreground=True, min_run=2, top_k=4, sample_stride=SAMPLE_STRIDE,
    )
    tracker = GeometryTracker()
    gate = RepresentativeGate()
    hanning = cv2.createHanningWindow((320, 180), cv2.CV_32F)
    previous_small: np.ndarray | None = None
    previous_luma: float | None = None
    candidate_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    review_panel_paths: list[Path] = []
    qa_receipts: list[dict[str, Any]] = []
    decoded = 0
    try:
        for frame_index in range(END_FRAME + 1):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"decode stopped at frame {frame_index}")
            decoded += 1
            motion = phase_diagnostic(previous_small, frame, hanning)
            current_small = motion.pop("small_gray")
            luma_mean = float(motion["source_luma_mean"])
            luma_delta = "" if previous_luma is None else f"{luma_mean - previous_luma:.9g}"
            previous_small = current_small
            previous_luma = luma_mean

            result = chain.process_bgr(frame, frame_index)
            if result["learning"]:
                continue
            components = extract_components(result["run_filtered_mask"], result["difference"])
            baseline, _, baseline_diag = baseline_select(components)
            track_rows = tracker.update(
                frame_index, [tuple(entry["raw_box"]) for entry in baseline]
            )
            if frame_index < START_FRAME:
                continue

            frame_candidate_rows: list[dict[str, Any]] = []
            for slot, (entry, track) in enumerate(zip(baseline, track_rows)):
                component: Component = entry["component"]
                box = tuple(entry["selected_box"])
                x0, y0, x1, y1 = box
                roi = fpga_resize_roi(result["gray"][y0:y1 + 1, x0:x1 + 1])
                score = score_roi(roi, parameters, hog324, q_contract)
                source_candidate = source_box(box, SAMPLE_STRIDE, EXPECTED_WIDTH, EXPECTED_HEIGHT)
                box_height = y1 - y0 + 1
                row: dict[str, Any] = {
                    "candidate_id": (
                        f"local_baseline_main4:f{frame_index:06d}:slot{slot}:cc{component.label}"
                    ),
                    "clip_id": CLIP_ID,
                    "scene_id": SCENE_ID,
                    "frame_index": frame_index,
                    "timestamp_ms": f"{1000.0 * frame_index / EXPECTED_FPS:.6f}",
                    "strategy": "deployed_baseline_main4",
                    "slot": slot,
                    "branch": "main_area_topk",
                    "reason_code": "BASELINE_MAIN",
                    "component_label": component.label,
                    "component_area": component.area,
                    "component_fill_ratio": f"{component.fill_ratio:.9g}",
                    "component_mean_difference": f"{component.mean_difference:.9g}",
                    "component_peak_difference": component.peak_difference,
                    "analysis_box_height": box_height,
                    "analysis_box_height_bin": height_bin(box_height),
                    "raw_analysis_box": box_text(component.box),
                    "selected_analysis_box": box_text(box),
                    "selected_source_box": box_text(source_candidate),
                    "roi_pixel_sha256": pixel_sha256(roi),
                    "geometry_track_id": track["causal_track_id"],
                    "geometry_recent_3_frame_hits": track["causal_recent_3_frame_hits"],
                    "geometry_recent_5_frame_hits": track["causal_recent_5_frame_hits"],
                    "geometry_track_age_frames": track["causal_track_age_frames"],
                    "geometry_consecutive_hits": track["causal_consecutive_hits"],
                    "geometry_previous_gap_frames": track["causal_previous_gap_frames"],
                    **score,
                }
                candidate_rows.append(row)
                frame_candidate_rows.append(row)
                if gate.accept(str(track["causal_track_id"]), frame_index):
                    sample_id = f"lp{len(review_rows):05d}"
                    assets = render_review_assets(
                        output, sample_id, frame, baseline, slot, roi, row
                    )
                    review = {
                        "sample_id": sample_id,
                        **row,
                        "representative_gap_frames": REPRESENTATIVE_GAP,
                        **assets,
                        **{field: "" for field in HUMAN_FIELDS},
                    }
                    review_rows.append(review)
                    review_panel_paths.append(output / assets["review_panel_path"])

            diagnostic_rows.append({
                "frame_index": frame_index,
                "timestamp_ms": f"{1000.0 * frame_index / EXPECTED_FPS:.6f}",
                "source_luma_mean": motion["source_luma_mean"],
                "source_luma_std": motion["source_luma_std"],
                "source_luma_mean_delta": luma_delta,
                "global_shift_x_320": motion["global_shift_x_320"],
                "global_shift_y_180": motion["global_shift_y_180"],
                "global_shift_magnitude_320x180": motion["global_shift_magnitude_320x180"],
                "phase_response": motion["phase_response"],
                "foreground_pixels_raw": result["foreground_pixels_raw"],
                "foreground_pixels_clean": result["foreground_pixels_clean"],
                "foreground_pixels_after_min_run": result["foreground_pixels_after_min_run"],
                "post_run_component_count_all": len(components),
                "baseline_candidate_count": baseline_diag["final_candidates"],
                "baseline_candidate_area_sum": sum(entry["component"].area for entry in baseline),
                "baseline_candidate_area_max": max(
                    (entry["component"].area for entry in baseline), default=0
                ),
            })
            if frame_index in QA_FRAMES:
                qa_receipts.append(render_qa(output, frame_index, frame, baseline))
    finally:
        capture.release()
    if decoded != END_FRAME + 1:
        raise AssertionError("video was not decoded exactly once from frame zero through 1079")
    if len(diagnostic_rows) != END_FRAME - START_FRAME + 1:
        raise AssertionError("scoring-window diagnostics do not cover 120..1079")
    if [item["frame_index"] for item in qa_receipts] != list(QA_FRAMES):
        raise AssertionError("QA frame coverage mismatch")

    contact_receipts = render_contact_sheets(output, review_panel_paths)
    qa_contact = qa_contact_sheet(output, qa_receipts)
    candidate_path = output / "candidates.csv"
    diagnostics_path = output / "frame_diagnostics.csv"
    manifest_path = output / "review_manifest.csv"
    report_path = output / "report.json"
    receipt_path = output / "receipt.json"
    write_csv(candidate_path, candidate_rows)
    write_csv(diagnostics_path, diagnostic_rows)
    write_csv(manifest_path, review_rows)
    if manifest_path.read_bytes().startswith(b"PK"):
        raise AssertionError("review_manifest.csv is not true CSV")
    if any(row[field] for row in review_rows for field in HUMAN_FIELDS):
        raise AssertionError("human fields were not initialized blank")

    # Readback joins establish candidate/manifest identity and the 30-frame rule.
    candidate_by_id = {row["candidate_id"]: row for row in candidate_rows}
    if len(candidate_by_id) != len(candidate_rows):
        raise AssertionError("candidate_id values are not unique")
    last_rep: dict[str, int] = {}
    for review in review_rows:
        candidate = candidate_by_id.get(str(review["candidate_id"]))
        if candidate is None:
            raise AssertionError("review representative missing from candidate table")
        for field in (
            "frame_index", "slot", "component_label", "raw_analysis_box",
            "selected_analysis_box", "roi_pixel_sha256", "geometry_track_id",
        ):
            if str(review[field]) != str(candidate[field]):
                raise AssertionError(f"candidate/review identity mismatch at {field}")
        track_id = str(review["geometry_track_id"])
        frame_index = int(review["frame_index"])
        if track_id in last_rep and frame_index - last_rep[track_id] < REPRESENTATIVE_GAP:
            raise AssertionError("representative gap below 30 frames")
        last_rep[track_id] = frame_index

    height_counts = dict(sorted(Counter(
        str(row["analysis_box_height_bin"]) for row in candidate_rows
    ).items()))
    prediction_counts = {
        field: dict(sorted(Counter(str(row[field]) for row in candidate_rows).items()))
        for field in (
            "hog64_prediction", "hog324_float_prediction", "hog324_q_prediction"
        )
    }
    float_q_mismatch = sum(
        row["hog324_float_prediction"] != row["hog324_q_prediction"]
        for row in candidate_rows
    )
    frame_loads = [int(row["baseline_candidate_count"]) for row in diagnostic_rows]
    shifts = [
        float(row["global_shift_magnitude_320x180"])
        for row in diagnostic_rows if row["global_shift_magnitude_320x180"] != ""
    ]
    responses = [
        float(row["phase_response"]) for row in diagnostic_rows
        if row["phase_response"] != ""
    ]
    luma = [float(row["source_luma_mean"]) for row in diagnostic_rows]
    luma_delta = [
        abs(float(row["source_luma_mean_delta"])) for row in diagnostic_rows
        if row["source_luma_mean_delta"] != ""
    ]
    model_input_hashes = {
        key: value for key, value in model_receipt.items() if key.endswith("sha256")
    }
    dependency_paths = (
        TOOLS / "candidate_chain_reference.py",
        TOOLS / "fixed_budget_candidate_prototype.py",
        TOOLS / "guarded_final4_arbitration.py",
        TOOLS / "roi_dataset_tool.py",
        TOOLS / "hog_reference.py",
        TOOLS / "analyze_virat_failure_sources.py",
        EXTERNAL / "opencv_hog_candidate_diagnostic.py",
    )
    report = {
        "schema": "local_scene_baseline_pilot_v1",
        "scope": {
            "clip_id": CLIP_ID,
            "scene_id": SCENE_ID,
            "causal_decode_inclusive": [0, END_FRAME],
            "scoring_window_inclusive": [START_FRAME, END_FRAME],
            "scoring_frames": END_FRAME - START_FRAME + 1,
            "development_pilot_only": True,
            "human_labels_available": False,
            "training_performed": False,
            "threshold_tuning_performed": False,
            "fill_only_used": False,
            "rtl_modified": False,
        },
        "inputs": {
            "video": {"path": str(video), **metadata},
            "model_receipt": model_receipt,
            "model_input_sha256": model_input_hashes,
            "model_source_status": {
                "current_rtl64": parameters["current_rtl64"].get("status"),
                "opencv_hog324": parameters["opencv_hog324"].get("status"),
                "run_semantics": "existing parameter files hash-locked for this pilot; no retraining",
            },
            "dependency_sha256": {
                str(path.relative_to(PROJECT)).replace("\\", "/"): sha256(path)
                for path in dependency_paths
            },
            "script_sha256": sha256(SCRIPT),
        },
        "candidate_contract": {
            "strategy": "deployed baseline area-top4 only",
            "component_input": "post-3x3-cleanup and row-min-run=2, 8-connected",
            "selection": "area>=16, area descending then component label ascending, top four",
            "roi": "inclusive main analysis box, deterministic nearest-neighbor to uint8 32x32",
            "representatives": "geometry-only causal tracks; at most one representative per track per 30 frames",
            "fill_only": "terminated and excluded from primary results",
        },
        "counts": {
            "candidate_rows": len(candidate_rows),
            "review_representatives": len(review_rows),
            "geometry_tracks_with_representatives": len(last_rep),
            "candidate_height_bins": height_counts,
            "model_prediction_counts": prediction_counts,
            "hog324_float_q_prediction_mismatch": float_q_mismatch,
        },
        "candidate_load": {
            "frames": len(frame_loads),
            "mean_candidates_per_frame": sum(frame_loads) / len(frame_loads),
            "max_candidates_per_frame": max(frame_loads),
            "frames_by_candidate_count": dict(sorted(Counter(frame_loads).items())),
        },
        "jitter_exposure_diagnostic": {
            "method": "phase correlation on adjacent 320x180 grayscale frames; moving targets can bias estimates",
            "window": [START_FRAME, END_FRAME],
            "shift_median_px_at_320x180": float(np.median(shifts)),
            "shift_p95_px_at_320x180": float(np.percentile(shifts, 95)),
            "shift_max_px_at_320x180": max(shifts),
            "phase_response_median": float(np.median(responses)),
            "luma_mean_min": min(luma),
            "luma_mean_max": max(luma),
            "max_abs_adjacent_luma_mean_delta": max(luma_delta),
            "interpretation": "pilot diagnostic only; not camera calibration or stabilization proof",
        },
        "review_contract": {
            "authoritative_human_input": "review_manifest.csv",
            "human_fields_initialized_blank": list(HUMAN_FIELDS),
            "review_class_allowed": ["ped", "vehicle", "invalid", "ignore"],
            "semantic_subtype_allowed": ["", "rider_bicycle"],
            "candidate_condition_allowed": [
                "complete", "truncated", "merged", "background_fragment", "other"
            ],
            "crop_usable_allowed": ["yes", "no"],
        },
        "outputs": {
            "candidates": "candidates.csv",
            "frame_diagnostics": "frame_diagnostics.csv",
            "review_manifest": "review_manifest.csv",
            "review_frame_count": len(review_rows),
            "roi_32x32_count": len(review_rows),
            "review_panel_count": len(review_rows),
            "contact_sheets": contact_receipts,
            "qa_frames": qa_receipts,
            "qa_contact_sheet": qa_contact,
        },
        "metric_boundary": (
            "No accuracy, precision, recall, FAR, or acceptance decision is reported before "
            "human review; binary SVM margins are not probabilities."
        ),
        "limitations": [
            "This is one local fixed-camera development clip and not an independent test set.",
            "The phase-correlation diagnostic may respond to large moving vehicles as well as camera motion.",
            "The Python candidate reference does not model RTL run/label overflow or cycle timing.",
            "Existing HOG models remain development diagnostics even though their files are hash-locked for this run.",
        ],
    }
    write_json(report_path, report)

    artifact_paths = [
        candidate_path, diagnostics_path, manifest_path, report_path,
        *(output / receipt["path"] for receipt in contact_receipts),
        *(output / receipt["path"] for receipt in qa_receipts),
        output / qa_contact["path"],
    ]
    for review in review_rows:
        artifact_paths.extend((
            output / str(review["review_frame_path"]),
            output / str(review["roi_32x32_path"]),
            output / str(review["review_panel_path"]),
        ))
    artifact_hashes = {
        path.relative_to(output).as_posix(): sha256(path)
        for path in sorted(set(artifact_paths))
    }
    receipt = {
        "schema": "local_scene_baseline_pilot_receipt_v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script_sha256": sha256(SCRIPT),
        "video_sha256": EXPECTED_VIDEO_SHA256,
        "model_input_sha256": model_input_hashes,
        "artifact_hashes": artifact_hashes,
        "receipt_self_hash_included": False,
        "assertions": {
            "strict_video_hash_and_metadata_match": True,
            "decoded_once_from_frame_zero_through_1079": True,
            "statistics_only_frames_120_through_1079": True,
            "deployed_baseline_top4_only": True,
            "fill_only_excluded": True,
            "representative_gap_ge_30_per_geometry_track": True,
            "candidate_review_identity_readback": True,
            "review_manifest_true_csv": True,
            "all_human_fields_blank": True,
            "training_performed": False,
            "threshold_tuning_performed": False,
            "accuracy_or_recall_reported": False,
        },
    }
    write_json(receipt_path, receipt)
    parsed_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    for relative, expected in parsed_receipt["artifact_hashes"].items():
        if sha256(output / relative) != expected:
            raise RuntimeError(f"artifact hash readback mismatch: {relative}")
    if parsed_receipt["script_sha256"] != sha256(SCRIPT):
        raise RuntimeError("script hash readback mismatch")
    return {
        "output": str(output),
        "candidate_rows": len(candidate_rows),
        "review_rows": len(review_rows),
        "height_bins": height_counts,
        "prediction_counts": prediction_counts,
        "float_q_mismatch": float_q_mismatch,
        "receipt_sha256": sha256(receipt_path),
    }


def self_test() -> None:
    try:
        guard_path(Path("x/blind_reserve/y"))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("sealed path guard failed")
    assert [height_bin(value) for value in (1, 6, 7, 15, 16, 31, 32, 100)] == [
        "le_6", "le_6", "7_15", "7_15", "16_31", "16_31", "ge_32", "ge_32"
    ]
    gate = RepresentativeGate(30)
    assert gate.accept("t0", 420)
    assert not gate.accept("t0", 449)
    assert gate.accept("t0", 450)
    tracker = GeometryTracker()
    first = tracker.update(1, [(10, 10, 20, 20)])[0]
    second = tracker.update(2, [(10, 10, 20, 20)])[0]
    assert first["causal_track_id"] == second["causal_track_id"]
    assert second["causal_consecutive_hits"] == 2
    roi = np.arange(32 * 32, dtype=np.uint8).reshape(32, 32)
    view = resize_letterbox(cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR), (256, 256))
    assert view.shape == (256, 256, 3)
    print("SELF_TEST PASS")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    result = run(args)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
