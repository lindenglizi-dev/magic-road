#!/usr/bin/env python3
"""Four-grid ROI diagnostic for the confirmed local-intersection annotations.

This is a bounded development-scene diagnostic.  It compares dense source-gray
and stride-5 analysis-gray ROI paths for the same physical cell extent:

  A: dense source-gray GT extent       B: stride-5 analysis-gray GT extent
  C: stride-5 matched candidate extent D: dense source-gray candidate extent

Only confirmed moving pedestrian/vehicle targets are evaluated.  Detection is
class-blind maximum-cardinality one-to-one source IoU >= 0.5.  No training,
threshold selection, RTL change, or sealed-set access is performed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import cv2
import numpy as np

from local_paired_diagnostic import (
    CONTRACT,
    FRAME_IDS,
    PACKAGE,
    candidates,
    digest,
    iou,
    match,
    read_json,
    validate_annotations,
)
from roi_dataset_tool import fpga_analysis_frame, fpga_gray_bgr, fpga_resize_roi
from run_local_scene_pilot import (
    DEFAULT_OUTPUT,
    EXPECTED_VIDEO_SHA256,
    MODEL_DIR,
    guard_path,
    load_models,
    make_hog324,
    quantization_contract,
    score_roi,
)


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
DEFAULT_ANNOTATIONS = (
    PROJECT
    / "evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930"
    / "annotations.confirmed.json"
)
DEFAULT_FOURGRID_OUTPUT = (
    PROJECT
    / "evaluation/local_scene_pilots/intersection_2415171_fourgrid_v2"
)
MODEL_KEYS = (
    "hog64_prediction",
    "hog324_float_prediction",
    "hog324_q_prediction",
)
SCORE_KEYS = (
    "hog64_feature_sha256",
    "hog64_score",
    "hog64_prediction",
    "hog324_feature_sha256",
    "hog324_float_score",
    "hog324_float_prediction",
    "hog324_q_score_integer",
    "hog324_q_score_normalized",
    "hog324_q_prediction",
)
CELL_STRIDE = 5
SOURCE_WIDTH = 1280
SOURCE_HEIGHT = 720
GRID_CELL = 176
GRID_HEADER = 62
GRID_FOOTER = 44
GRID_WIDTH = 4 * GRID_CELL
GRID_HEIGHT = GRID_HEADER + GRID_CELL + GRID_FOOTER
CONTACT_ROWS = 10
CONFIRMATION_RECEIPT_NAME = "confirmation_receipt.json"
EVALUATION_SCOPE = "moving_ped_vehicle_only"
TRACK_ID = re.compile(r"^[pv][0-9]{2}$")


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def pixel_sha256(image: np.ndarray) -> str:
    return hashlib.sha256(
        np.ascontiguousarray(image, dtype=np.uint8).tobytes()
    ).hexdigest()


def analysis_box(source_box: Sequence[int]) -> list[int]:
    """Map an inclusive source box to its inclusive stride-5 cell range."""
    if len(source_box) != 4:
        raise ValueError("source box requires four coordinates")
    x0, y0, x1, y1 = (int(value) for value in source_box)
    if not (0 <= x0 <= x1 < SOURCE_WIDTH and 0 <= y0 <= y1 < SOURCE_HEIGHT):
        raise ValueError("source box is outside the 1280x720 frame")
    return [x0 // CELL_STRIDE, y0 // CELL_STRIDE,
            x1 // CELL_STRIDE, y1 // CELL_STRIDE]


def source_cell_extent(box: Sequence[int]) -> list[int]:
    """Expand an inclusive analysis box to the same inclusive source cells."""
    if len(box) != 4:
        raise ValueError("analysis box requires four coordinates")
    x0, y0, x1, y1 = (int(value) for value in box)
    if not (0 <= x0 <= x1 < SOURCE_WIDTH // CELL_STRIDE
            and 0 <= y0 <= y1 < SOURCE_HEIGHT // CELL_STRIDE):
        raise ValueError("analysis box is outside the 256x144 frame")
    return [CELL_STRIDE * x0, CELL_STRIDE * y0,
            min(SOURCE_WIDTH, CELL_STRIDE * (x1 + 1)) - 1,
            min(SOURCE_HEIGHT, CELL_STRIDE * (y1 + 1)) - 1]


def crop_inclusive(image: np.ndarray, box: Sequence[int]) -> np.ndarray:
    x0, y0, x1, y1 = (int(value) for value in box)
    return image[y0:y1 + 1, x0:x1 + 1]


def roi_pair(full_gray: np.ndarray, analysis_gray: np.ndarray,
             box: Sequence[int]) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Return dense-source and stride-5 ROIs for one analysis-cell range."""
    extent = source_cell_extent(box)
    dense = fpga_resize_roi(crop_inclusive(full_gray, extent))
    sampled = fpga_resize_roi(crop_inclusive(analysis_gray, box))
    return dense, sampled, extent


def score_record(roi: np.ndarray, parameters: Mapping[str, Any],
                 hog: cv2.HOGDescriptor, quant: Mapping[str, Any]) -> dict[str, Any]:
    score = score_roi(roi, parameters, hog, quant)
    score["roi_pixel_sha256"] = pixel_sha256(roi)
    score["hog324_float_minus_q_normalized"] = (
        f"{float(score['hog324_float_score']) - float(score['hog324_q_score_normalized']):.12g}"
    )
    score["hog324_float_q_prediction_match"] = (
        score["hog324_float_prediction"] == score["hog324_q_prediction"]
    )
    return score


def verify_candidate(candidate: Mapping[str, str], roi: np.ndarray,
                     score: Mapping[str, Any]) -> None:
    if pixel_sha256(roi) != candidate["roi_pixel_sha256"]:
        raise ValueError(
            f"frozen candidate pixel mismatch: {candidate['candidate_id']}"
        )
    for key in SCORE_KEYS:
        if str(score[key]) != str(candidate[key]):
            raise ValueError(
                f"frozen candidate score mismatch: {candidate['candidate_id']} {key}"
            )


def prediction_correct(roi: Mapping[str, Any] | None, model: str,
                       label: str) -> bool:
    return roi is not None and roi[model] == label


def transitions(rows: Sequence[Mapping[str, Any]], left: str, right: str,
                model: str) -> dict[str, int]:
    values = [(prediction_correct(row[left], model, row["label"]),
               prediction_correct(row[right], model, row["label"]))
              for row in rows]
    return {
        "improved": sum(not a and b for a, b in values),
        "degraded": sum(a and not b for a, b in values),
        "same_correct": sum(a and b for a, b in values),
        "same_wrong": sum(not a and not b for a, b in values),
    }


def metrics_for(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    matched = [row for row in rows if row["matched"]]
    result: dict[str, Any] = {
        "targets": len(rows),
        "matched": len(matched),
        "coverage": len(matched) / len(rows) if rows else None,
        "models": {},
    }
    for model in MODEL_KEYS:
        all_correct = {
            cell: sum(prediction_correct(row[cell], model, row["label"])
                      for row in rows)
            for cell in ("A", "B")
        }
        matched_correct = {
            cell: sum(prediction_correct(row[cell], model, row["label"])
                      for row in matched)
            for cell in ("A", "B", "C", "D")
        }
        result["models"][model] = {
            "all_targets_AB_correct": all_correct,
            "all_targets_A_to_B": transitions(rows, "A", "B", model),
            "matched_subset_ABCD_correct": matched_correct,
            "matched_subset_A_to_B": transitions(matched, "A", "B", model),
            "matched_subset_D_to_C": transitions(matched, "D", "C", model),
            "end_to_end_recall_C": (
                matched_correct["C"] / len(rows) if rows else None
            ),
            "dense_candidate_counterfactual_recall_D": (
                matched_correct["D"] / len(rows) if rows else None
            ),
        }
    return result


def grouped_metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_class = {
        label: metrics_for([row for row in rows if row["label"] == label])
        for label in ("ped", "vehicle")
    }
    tracks: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        tracks[f"{row['label']}:{row['track_id']}"] .append(row)
    return {
        "overall": metrics_for(rows),
        "by_class": by_class,
        "by_track": {key: metrics_for(value)
                     for key, value in sorted(tracks.items())},
    }


def roi_view(roi: np.ndarray | None) -> np.ndarray:
    if roi is None:
        view = np.full((GRID_CELL, GRID_CELL, 3), 232, dtype=np.uint8)
        cv2.line(view, (18, 18), (GRID_CELL - 19, GRID_CELL - 19),
                 (120, 120, 120), 3)
        cv2.line(view, (GRID_CELL - 19, 18), (18, GRID_CELL - 19),
                 (120, 120, 120), 3)
        cv2.putText(view, "UNMATCHED", (31, GRID_CELL // 2 + 6),
                    cv2.FONT_HERSHEY_SIMPLEX, .55, (60, 60, 60), 2,
                    cv2.LINE_AA)
        return view
    return cv2.cvtColor(
        cv2.resize(roi, (GRID_CELL, GRID_CELL), interpolation=cv2.INTER_NEAREST),
        cv2.COLOR_GRAY2BGR,
    )


def short_score(record: Mapping[str, Any] | None) -> str:
    if record is None:
        return "no candidate"
    return (
        f"64:{record['hog64_prediction']} "
        f"F:{record['hog324_float_prediction']} "
        f"Q:{record['hog324_q_prediction']}"
    )


def render_grid(row: Mapping[str, Any], rois: Mapping[str, np.ndarray | None]) -> np.ndarray:
    canvas = np.full((GRID_HEIGHT, GRID_WIDTH, 3), 250, dtype=np.uint8)
    title = (
        f"f{row['frame_index']:06d} {row['label']} {row['track_id']} "
        f"IoU={row['candidate_iou']:.4f}" if row["matched"] else
        f"f{row['frame_index']:06d} {row['label']} {row['track_id']} UNMATCHED"
    )
    cv2.putText(canvas, title, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                .63, (15, 15, 15), 2, cv2.LINE_AA)
    cv2.putText(canvas, f"GT {row['original_gt_box']}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, .45, (40, 40, 40), 1, cv2.LINE_AA)
    headings = (
        "A dense GT cells", "B stride5 GT cells",
        "C stride5 candidate", "D dense candidate cells",
    )
    for index, cell in enumerate(("A", "B", "C", "D")):
        x0 = index * GRID_CELL
        canvas[GRID_HEADER:GRID_HEADER + GRID_CELL, x0:x0 + GRID_CELL] = roi_view(rois[cell])
        cv2.putText(canvas, headings[index], (x0 + 6, GRID_HEADER + 17),
                    cv2.FONT_HERSHEY_SIMPLEX, .40, (0, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(canvas, short_score(row[cell]),
                    (x0 + 5, GRID_HEADER + GRID_CELL + 19),
                    cv2.FONT_HERSHEY_SIMPLEX, .36, (25, 25, 25), 1,
                    cv2.LINE_AA)
        delta = "" if row[cell] is None else row[cell]["hog324_float_minus_q_normalized"]
        cv2.putText(canvas, f"F-Q:{delta}",
                    (x0 + 5, GRID_HEADER + GRID_CELL + 38),
                    cv2.FONT_HERSHEY_SIMPLEX, .34, (25, 25, 25), 1,
                    cv2.LINE_AA)
    return canvas


def render_contacts(output: Path, grid_paths: Sequence[Path]) -> list[dict[str, Any]]:
    contacts: list[dict[str, Any]] = []
    for start in range(0, len(grid_paths), CONTACT_ROWS):
        paths = grid_paths[start:start + CONTACT_ROWS]
        sheet = np.full((len(paths) * GRID_HEIGHT, GRID_WIDTH, 3),
                        245, dtype=np.uint8)
        for index, path in enumerate(paths):
            grid = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if grid is None or grid.shape[:2] != (GRID_HEIGHT, GRID_WIDTH):
                raise ValueError(f"cannot read rendered grid: {path}")
            y0 = index * GRID_HEIGHT
            sheet[y0:y0 + GRID_HEIGHT] = grid
        page = start // CONTACT_ROWS + 1
        path = output / f"fourgrid_contact_{page:02d}.png"
        if not cv2.imwrite(str(path), sheet):
            raise OSError(path)
        contacts.append({"path": path.name, "rows": len(paths),
                         "sha256": digest(path)})
    return contacts


def flatten_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    for row in rows:
        item = {
            "frame_index": row["frame_index"],
            "track_id": row["track_id"],
            "label": row["label"],
            "visibility": row["visibility"],
            "original_gt_box": json.dumps(row["original_gt_box"], separators=(",", ":")),
            "gt_analysis_box": json.dumps(row["gt_analysis_box"], separators=(",", ":")),
            "gt_source_cell_extent": json.dumps(row["gt_source_cell_extent"], separators=(",", ":")),
            "matched": row["matched"],
            "candidate_id": row["candidate_id"] or "",
            "candidate_iou": "" if row["candidate_iou"] is None else f"{row['candidate_iou']:.12g}",
            "candidate_analysis_box": "" if row["candidate_analysis_box"] is None else json.dumps(row["candidate_analysis_box"], separators=(",", ":")),
            "candidate_source_cell_extent": "" if row["candidate_source_cell_extent"] is None else json.dumps(row["candidate_source_cell_extent"], separators=(",", ":")),
            "grid_path": row["grid_path"],
        }
        for cell in ("A", "B", "C", "D"):
            score = row[cell]
            for key in ("roi_pixel_sha256", *SCORE_KEYS,
                        "hog324_float_minus_q_normalized",
                        "hog324_float_q_prediction_match"):
                item[f"{cell}_{key}"] = "" if score is None else score[key]
        flat.append(item)
    return flat


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError("four-grid CSV cannot be empty")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validated_package(package_dir: Path) -> tuple[dict[str, Any], str]:
    package = read_json(package_dir / "package.json")
    receipt_path = package_dir / "receipt.json"
    receipt = read_json(receipt_path)
    for name, expected in receipt["artifact_hashes"].items():
        path = (package_dir / name).resolve()
        if not path.is_relative_to(package_dir.resolve()) or digest(path) != expected:
            raise ValueError(f"package artifact mismatch: {name}")
    return package, digest(receipt_path)


def validate_confirmation_chain(annotation_path: Path,
                                annotation: Mapping[str, Any]) -> dict[str, Any]:
    """Bind the derived annotation to its fixed sidecar and unchanged source."""
    receipt_path = annotation_path.parent / CONFIRMATION_RECEIPT_NAME
    if not receipt_path.is_file():
        raise ValueError(f"fixed confirmation receipt is missing: {receipt_path}")
    confirmation = read_json(receipt_path)
    if confirmation.get("schema") != "human_confirmation_sidecar_v1":
        raise ValueError("unknown confirmation receipt schema")
    if annotation.get("confirmation_receipt") != CONFIRMATION_RECEIPT_NAME:
        raise ValueError("derived annotation does not name the fixed confirmation receipt")
    if annotation.get("evaluation_scope") != EVALUATION_SCOPE:
        raise ValueError("derived annotation evaluation_scope mismatch")
    if confirmation.get("evaluation_scope") != EVALUATION_SCOPE:
        raise ValueError("confirmation evaluation_scope mismatch")
    if confirmation.get("confirmation_method") != "explicit_user_chat_reply":
        raise ValueError("confirmation must come from an explicit user chat reply")
    if confirmation.get("derived_sha256") != digest(annotation_path):
        raise ValueError("confirmation derived SHA256 mismatch")
    if confirmation.get("original_file_unchanged") is not True:
        raise ValueError("confirmation does not assert an unchanged original")
    if confirmation.get("targets_or_boxes_modified") is not False:
        raise ValueError("confirmation permits target or box changes")

    original_value = confirmation.get("original_path")
    if not isinstance(original_value, str) or not original_value:
        raise ValueError("confirmation original_path is missing")
    relative = Path(original_value)
    if relative.is_absolute():
        raise ValueError("confirmation original_path must be project relative")
    original_path = (PROJECT / relative).resolve()
    if not original_path.is_relative_to(PROJECT.resolve()):
        raise ValueError("confirmation original_path escapes the project")
    guard_path(original_path)
    if not original_path.is_file():
        raise ValueError("confirmation original annotation is missing")
    original_hash = digest(original_path)
    if original_hash != confirmation.get("original_sha256"):
        raise ValueError("original annotation changed after confirmation")
    original = read_json(original_path)
    if original.get("human_confirmed") is not False:
        raise ValueError("confirmation source was not the unconfirmed original")
    if confirmation.get("original_human_confirmed") is not False:
        raise ValueError("confirmation receipt original state mismatch")
    if original.get("source_sha256") != EXPECTED_VIDEO_SHA256:
        raise ValueError("original annotation source hash mismatch")
    if annotation.get("source_sha256") != EXPECTED_VIDEO_SHA256:
        raise ValueError("derived annotation source hash mismatch")
    for key in ("frames", "reviewer", "reviewed_at"):
        if annotation.get(key) != original.get(key):
            raise ValueError(f"derived annotation changed original {key}")
    if confirmation.get("reviewed_at_preserved") != original.get("reviewed_at"):
        raise ValueError("confirmation reviewed_at preservation mismatch")
    normalized = dict(annotation)
    normalized.pop("evaluation_scope", None)
    normalized.pop("confirmation_receipt", None)
    normalized["human_confirmed"] = False
    if normalized != original:
        raise ValueError("derived annotation contains changes beyond confirmation metadata")

    for frame in annotation.get("frames", []):
        for target in frame.get("targets", []):
            track_id = target.get("track_id")
            label = target.get("label")
            if not isinstance(track_id, str) or TRACK_ID.fullmatch(track_id) is None:
                raise ValueError(f"track ID is outside the filename-safe whitelist: {track_id!r}")
            expected_prefix = {"ped": "p", "vehicle": "v"}.get(label)
            if expected_prefix is not None and not track_id.startswith(expected_prefix):
                raise ValueError(f"track ID/class prefix mismatch: {track_id!r} {label!r}")
    return {
        "path": receipt_path,
        "sha256": digest(receipt_path),
        "original_path": original_path,
        "original_sha256": original_hash,
    }


def evaluate(annotation_path: Path, package_dir: Path, output: Path) -> dict[str, Any]:
    for path in (annotation_path, package_dir, output):
        guard_path(path)
    if output.exists():
        raise ValueError("output must be absent; immutable reruns require a new directory")
    if not annotation_path.is_file():
        raise ValueError(
            f"confirmed annotation file is required and was not found: {annotation_path}"
        )

    package, package_receipt_hash = validated_package(package_dir)
    annotation = read_json(annotation_path)
    validate_annotations(annotation, package)
    if annotation.get("human_confirmed") is not True:
        raise ValueError("explicit confirmed annotation is required")
    confirmation_chain = validate_confirmation_chain(annotation_path, annotation)
    table, candidate_csv_hash = candidates()
    candidate_receipt = read_json(DEFAULT_OUTPUT / "receipt.json")
    parameters, _, model_receipt = load_models(MODEL_DIR)
    hog = make_hog324()
    quant = quantization_contract(parameters["opencv_hog324"])

    output.mkdir(parents=True)
    grid_dir = output / "grids"
    grid_dir.mkdir()
    rows: list[dict[str, Any]] = []
    grid_paths: list[Path] = []
    frame_summary: list[dict[str, Any]] = []

    for ann, package_frame in zip(annotation["frames"], package["frames"]):
        frame_index = int(ann["frame_index"])
        if frame_index != int(package_frame["frame_index"]):
            raise ValueError("annotation/package frame order mismatch")
        frame_path = package_dir / package_frame["path"]
        frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
        if frame is None or frame.shape[:2] != (SOURCE_HEIGHT, SOURCE_WIDTH):
            raise ValueError(f"invalid package frame: {frame_path}")
        if digest(frame_path) != package_frame["sha256"]:
            raise ValueError(f"package frame hash mismatch: {frame_path}")
        full_gray = fpga_gray_bgr(frame)
        sampled_gray = fpga_analysis_frame(frame)
        if not np.array_equal(full_gray[::CELL_STRIDE, ::CELL_STRIDE], sampled_gray):
            raise AssertionError("dense/source gray and stride-5 analysis gray diverged")

        moving = [target for target in ann["targets"]
                  if target["label"] in {"ped", "vehicle"}
                  and target["motion"] == "moving"]
        frame_candidates = table[frame_index]
        source_boxes = [json.loads(candidate["selected_source_box"])
                        for candidate in frame_candidates]
        links = match(moving, source_boxes, .5)

        verified_candidates: list[tuple[np.ndarray, dict[str, Any], list[int], list[int], np.ndarray, dict[str, Any]]] = []
        for candidate, source_box in zip(frame_candidates, source_boxes):
            cbox = json.loads(candidate["selected_analysis_box"])
            dense_roi, sampled_roi, extent = roi_pair(full_gray, sampled_gray, cbox)
            if source_box != extent:
                raise ValueError(
                    f"candidate source/cell extent mismatch: {candidate['candidate_id']}"
                )
            c_score = score_record(sampled_roi, parameters, hog, quant)
            verify_candidate(candidate, sampled_roi, c_score)
            d_score = score_record(dense_roi, parameters, hog, quant)
            verified_candidates.append(
                (sampled_roi, c_score, cbox, extent, dense_roi, d_score)
            )

        for target_index, target in enumerate(moving):
            gt_analysis = analysis_box(target["box"])
            a_roi, b_roi, gt_extent = roi_pair(full_gray, sampled_gray, gt_analysis)
            a_score = score_record(a_roi, parameters, hog, quant)
            b_score = score_record(b_roi, parameters, hog, quant)
            linked = links.get(target_index)
            if linked is None:
                c_roi = d_roi = None
                c_score = d_score = None
                candidate = None
                candidate_box = candidate_extent = None
                candidate_iou = None
            else:
                c_roi, c_score, candidate_box, candidate_extent, d_roi, d_score = verified_candidates[linked]
                candidate = frame_candidates[linked]
                candidate_iou = iou(target["box"], source_boxes[linked])
                if candidate_iou < .5:
                    raise AssertionError("matching returned an IoU below 0.5")
            row: dict[str, Any] = {
                "frame_index": frame_index,
                "track_id": target["track_id"],
                "label": target["label"],
                "motion": target["motion"],
                "visibility": target["visibility"],
                "original_gt_box": list(target["box"]),
                "gt_analysis_box": gt_analysis,
                "gt_source_cell_extent": gt_extent,
                "matched": linked is not None,
                "candidate_id": None if candidate is None else candidate["candidate_id"],
                "candidate_iou": candidate_iou,
                "candidate_analysis_box": candidate_box,
                "candidate_source_cell_extent": candidate_extent,
                "A": a_score,
                "B": b_score,
                "C": c_score,
                "D": d_score,
            }
            ordinal = len(rows)
            grid_path = grid_dir / (
                f"t{ordinal:03d}_f{frame_index:06d}_{target['label']}_{target['track_id']}.png"
            )
            grid = render_grid(row, {"A": a_roi, "B": b_roi, "C": c_roi, "D": d_roi})
            if not cv2.imwrite(str(grid_path), grid):
                raise OSError(grid_path)
            row["grid_path"] = grid_path.relative_to(output).as_posix()
            rows.append(row)
            grid_paths.append(grid_path)

        frame_summary.append({
            "frame_index": frame_index,
            "moving_targets": len(moving),
            "candidates": len(frame_candidates),
            "matched": len(links),
            "unmatched_targets": len(moving) - len(links),
        })

    if any(row["motion"] != "moving" or row["label"] not in {"ped", "vehicle"}
           for row in rows):
        raise AssertionError("non-moving or non-target annotation entered the evaluation")
    if len(rows) != 57:
        raise ValueError(f"expected 57 confirmed moving targets, found {len(rows)}")

    contacts = render_contacts(output, grid_paths)
    pair_path = output / "fourgrid_rows.json"
    csv_path = output / "fourgrid_rows.csv"
    report_path = output / "report.json"
    receipt_path = output / "receipt.json"
    dump_json(pair_path, rows)
    write_csv(csv_path, flatten_rows(rows))

    model_input_hashes = {
        key: value for key, value in model_receipt.items()
        if key.endswith("sha256")
    }
    dependencies = (
        SCRIPT,
        PROJECT / "tools/local_paired_diagnostic.py",
        PROJECT / "tools/run_local_scene_pilot.py",
        PROJECT / "tools/roi_dataset_tool.py",
    )
    report = {
        "schema": "local_intersection_fourgrid_diagnostic_v2",
        "scope": {
            "development_scene_only": True,
            "frames": FRAME_IDS,
            "annotation_filter": "moving ped/vehicle only",
            "all_visible_alias_reported": False,
            "target_instances": len(rows),
            "training_performed": False,
            "threshold_tuning_performed": False,
            "rtl_modified": False,
        },
        "four_grid_contract": {
            "A": "dense fpga_gray_bgr pixels over GT analysis-cell extent, fpga_resize_roi",
            "B": "fpga_analysis_frame stride-5 pixels over GT analysis-cell extent, fpga_resize_roi",
            "C": "frozen actual matched candidate analysis pixels, fpga_resize_roi",
            "D": "dense fpga_gray_bgr pixels over the same candidate analysis-cell extent, fpga_resize_roi",
            "source_to_analysis": "floor(coordinate/5), inclusive",
            "analysis_to_source_extent": "[5*x0,5*y0,5*(x1+1)-1,5*(y1+1)-1], clipped to frame",
            "localization": "original unexpanded GT boxes retained for class-blind matching and IoU",
            "matching": "maximum-cardinality then maximum-total-IoU one-to-one, class blind, source IoU >= 0.5",
            "unmatched": "A/B retained, C/D null, target remains in all denominators",
        },
        "metrics": grouped_metrics(rows),
        "metrics_by_visibility": {
            visibility: metrics_for(
                [row for row in rows if row["visibility"] == visibility]
            )
            for visibility in ("full", "occluded", "frame_truncated")
        },
        "capacity_relation": {
            "A_B_capacity_independent": True,
            "A_B_reason": "oracle GT ROIs are scored without candidate selection",
            "C_D_and_end_to_end_capacity_independent": False,
            "C_D_reason": "actual frozen deployed baseline area-top4 candidates are used",
        },
        "frames": frame_summary,
        "float_q_diagnostic": {
            "definition": "hog324_float_score - hog324_q_score_normalized; margins are not probabilities",
            "prediction_mismatches": {
                cell: sum(row[cell] is not None and not row[cell]["hog324_float_q_prediction_match"]
                          for row in rows)
                for cell in ("A", "B", "C", "D")
            },
        },
        "inputs": {
            "annotation": {"path": str(annotation_path), "sha256": digest(annotation_path)},
            "confirmation_receipt": {
                "path": str(confirmation_chain["path"]),
                "sha256": confirmation_chain["sha256"],
                "method": "explicit_user_chat_reply",
                "evaluation_scope": EVALUATION_SCOPE,
            },
            "original_annotation": {
                "path": str(confirmation_chain["original_path"]),
                "sha256": confirmation_chain["original_sha256"],
            },
            "package": {"path": str(package_dir), "receipt_sha256": package_receipt_hash},
            "candidate_csv_sha256": candidate_csv_hash,
            "candidate_receipt_sha256": digest(DEFAULT_OUTPUT / "receipt.json"),
            "video_sha256": EXPECTED_VIDEO_SHA256,
            "model_receipt": model_receipt,
            "model_input_sha256": model_input_hashes,
            "dependency_sha256": {
                path.relative_to(PROJECT).as_posix(): digest(path)
                for path in dependencies
            },
        },
        "outputs": {
            "rows_json": pair_path.name,
            "rows_csv": csv_path.name,
            "individual_grids": len(grid_paths),
            "contact_sheets": contacts,
        },
        "boundary": (
            "32 sampled frames and 57 correlated moving target instances from one local "
            "development clip only; GT ROI results diagnose classification after oracle "
            "localization, C end-to-end recall includes actual candidate coverage; Python "
            "results do not establish RTL timing, overflow, throughput, or independent-test performance."
        ),
    }
    dump_json(report_path, report)

    artifact_paths = [pair_path, csv_path, report_path, *grid_paths,
                      *(output / contact["path"] for contact in contacts)]
    receipt = {
        "schema": "local_intersection_fourgrid_receipt_v2",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "annotation_sha256": digest(annotation_path),
        "confirmation_receipt_sha256": confirmation_chain["sha256"],
        "confirmation_original_sha256": confirmation_chain["original_sha256"],
        "package_receipt_sha256": package_receipt_hash,
        "candidate_csv_sha256": candidate_csv_hash,
        "candidate_receipt_sha256": digest(DEFAULT_OUTPUT / "receipt.json"),
        "script_sha256": digest(SCRIPT),
        "dependency_sha256": {
            path.relative_to(PROJECT).as_posix(): digest(path)
            for path in dependencies
        },
        "model_input_sha256": model_input_hashes,
        "artifact_hashes": {
            path.relative_to(output).as_posix(): digest(path)
            for path in sorted(artifact_paths)
        },
        "receipt_self_hash_included": False,
        "assertions": {
            "human_confirmed_annotation_validated": True,
            "confirmation_receipt_chain_validated": True,
            "confirmation_method_explicit_user_chat_reply": True,
            "evaluation_scope_moving_ped_vehicle_only": True,
            "original_annotation_unchanged": True,
            "track_ids_filename_safe_whitelist": True,
            "moving_ped_vehicle_only": True,
            "target_count_57": True,
            "original_gt_retained_for_matching": True,
            "candidate_match_class_blind_iou_ge_0_5": True,
            "all_frozen_candidate_pixels_and_scores_readback_verified": True,
            "dense_gray_stride5_identity_verified_each_frame": True,
            "unmatched_targets_retained": True,
            "training_performed": False,
            "threshold_tuning_performed": False,
            "rtl_modified": False,
        },
    }
    dump_json(receipt_path, receipt)
    for relative, expected in read_json(receipt_path)["artifact_hashes"].items():
        if digest(output / relative) != expected:
            raise RuntimeError(f"artifact hash readback mismatch: {relative}")

    metrics = report["metrics"]["overall"]
    return {
        "output": str(output),
        "targets": len(rows),
        "matched": metrics["matched"],
        "coverage": metrics["coverage"],
        "contact_sheets": len(contacts),
        "receipt_sha256": digest(receipt_path),
    }


def self_test() -> dict[str, Any]:
    assert TRACK_ID.fullmatch("p01") and TRACK_ID.fullmatch("v99")
    assert TRACK_ID.fullmatch("../p01") is None
    assert TRACK_ID.fullmatch("p/01") is None
    assert analysis_box([6, 11, 14, 20]) == [1, 2, 2, 4]
    assert source_cell_extent([1, 2, 2, 4]) == [5, 10, 14, 24]
    assert source_cell_extent([255, 143, 255, 143]) == [1275, 715, 1279, 719]

    yy, xx = np.indices((SOURCE_HEIGHT, SOURCE_WIDTH), dtype=np.uint16)
    full_gray = ((3 * xx + 7 * yy) & 255).astype(np.uint8)
    sampled = full_gray[::CELL_STRIDE, ::CELL_STRIDE]
    dense_roi, sampled_roi, extent = roi_pair(full_gray, sampled, [1, 2, 2, 4])
    assert extent == [5, 10, 14, 24]
    assert dense_roi.shape == sampled_roi.shape == (32, 32)
    assert np.array_equal(
        crop_inclusive(full_gray, extent)[::CELL_STRIDE, ::CELL_STRIDE],
        crop_inclusive(sampled, [1, 2, 2, 4]),
    )

    gt = [{"box": [0, 0, 9, 9]}, {"box": [20, 20, 29, 29]}]
    links = match(gt, [[0, 0, 9, 9]], .5)
    assert links == {0: 0}
    dummy = {
        "frame_index": 0, "label": "ped", "track_id": "p0",
        "original_gt_box": [0, 0, 9, 9], "matched": False,
        "candidate_iou": None,
        "A": None, "B": None, "C": None, "D": None,
    }
    grid = render_grid(dummy, {"A": dense_roi, "B": sampled_roi,
                               "C": None, "D": None})
    assert grid.shape == (GRID_HEIGHT, GRID_WIDTH, 3)
    return {
        "self_test": "PASS",
        "coordinate_mapping": True,
        "same_cell_extent": True,
        "unmatched_CD_missing": True,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("evaluate", "self-test"))
    parser.add_argument("--annotations", type=Path, default=DEFAULT_ANNOTATIONS)
    parser.add_argument("--package", type=Path, default=PACKAGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_FOURGRID_OUTPUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = self_test() if args.mode == "self-test" else evaluate(
        args.annotations.resolve(), args.package.resolve(), args.output.resolve()
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
