#!/usr/bin/env python3
"""Evaluate sealed candidate ROIs with the existing 64/324-d HOG models.

This is a diagnostic only.  It never trains or modifies model parameters and
fails closed on test/blind/holdout/reserve paths and reserved VIRAT clips.
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
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import cv2
import numpy as np
from PIL import Image


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
TOOLS_DIR = PROJECT_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from candidate_review_io import load_reviewed  # noqa: E402
from hog_reference import extract_features  # noqa: E402
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi  # noqa: E402


DEFAULT_ADJUDICATED = (
    PROJECT_ROOT / "evaluation/candidate_reviews/finalized_20260927/"
    "fill_only_adjudicated.csv"
)
DEFAULT_MODEL_DIR = (
    PROJECT_ROOT / "external_reference_exploration/results/opencv_hog_diagnostic"
)
VIRAT_CATALOG = PROJECT_ROOT / "evaluation/public_data/virat_ground_v2/catalog.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "external_reference_exploration/results/"
    "opencv_hog_candidate_diagnostic"
)
VALIDATION_REVIEW_ROOTS = (
    PROJECT_ROOT / "evaluation/candidates/virat_000200_f1840_1859",
    PROJECT_ROOT / "evaluation/candidates/virat_000200_f608_627",
    PROJECT_ROOT / "evaluation/candidates/virat_000203_f600_619",
)

FORBIDDEN_PATH_TOKEN = re.compile(
    r"(^|[_\-.])(test|blind|holdout|reserve)($|[_\-.])", re.IGNORECASE
)
FORBIDDEN_CLIP_TOKEN = re.compile(r"000205|000207|010106|010108", re.IGNORECASE)
ALLOWED_SPLITS = {"train", "val"}
REVIEW_CLASS_TO_TRUTH = {
    "ped_full": "ped",
    "ped_truncated": "ped",
    "vehicle": "vehicle",
    "background_fragment": "invalid",
    "merged_target": "invalid",
    "other_ignore": "invalid",
}
TARGETS = {"ped_recall": 0.85, "vehicle_recall": 0.90,
           "invalid_acceptance": 0.10}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pixel_sha256(image: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(image, dtype=np.uint8).tobytes()).hexdigest()


def assert_safe_path(path: Path, role: str) -> None:
    for part in path.resolve().parts:
        if FORBIDDEN_PATH_TOKEN.search(part) or FORBIDDEN_CLIP_TOKEN.search(part):
            raise ValueError(f"sealed-data guard rejected {role} path component: {part}")


def assert_safe_record(row: dict[str, str], role: str) -> None:
    for field, value in row.items():
        if not value:
            continue
        key = field.lower()
        if any(token in key for token in ("path", "split", "clip", "scene", "window")):
            if FORBIDDEN_CLIP_TOKEN.search(value) or FORBIDDEN_PATH_TOKEN.search(value):
                raise ValueError(
                    f"sealed-data guard rejected {role} {field}={value!r}"
                )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    return rows


def first_value(row: dict[str, str], names: Iterable[str], role: str) -> str:
    for name in names:
        value = row.get(name, "").strip()
        if value:
            return value
    raise ValueError(f"missing {role}; accepted fields={list(names)}")


def parse_box(text: str) -> tuple[int, int, int, int]:
    values = [int(value) for value in re.findall(r"-?\d+", text)]
    if len(values) != 4:
        raise ValueError(f"inclusive box must have four integers: {text!r}")
    x0, y0, x1, y1 = values
    if not (0 <= x0 <= x1 < 256 and 0 <= y0 <= y1 < 144):
        raise ValueError(f"inclusive analysis box out of bounds: {values}")
    return x0, y0, x1, y1


def make_hog324() -> cv2.HOGDescriptor:
    return cv2.HOGDescriptor(
        (32, 32), (16, 16), (8, 8), (8, 8), 9,
        1, 4.0, cv2.HOGDescriptor_L2Hys, 0.2, False, 64, False,
    )


def extract_variant(roi: np.ndarray, variant: str,
                    hog324: cv2.HOGDescriptor) -> np.ndarray:
    if roi.shape != (32, 32) or roi.dtype != np.uint8:
        raise ValueError(f"ROI contract violation: shape={roi.shape}, dtype={roi.dtype}")
    if variant == "current_rtl64":
        values, _ = extract_features(roi.astype(int).tolist())
        return np.asarray(values, dtype=np.float64)
    if variant == "opencv_hog324":
        descriptor = hog324.compute(
            np.ascontiguousarray(roi), winStride=(0, 0), padding=(0, 0)
        )
        result = descriptor.reshape(-1).astype(np.float64)
        if result.size != 324:
            raise ValueError(f"unexpected OpenCV HOG dimension: {result.size}")
        return result
    raise ValueError(f"unknown model variant: {variant}")


def load_models(model_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    assert_safe_path(model_dir, "model directory")
    parameter_path = model_dir / "model_parameters.json"
    report_path = model_dir / "report.json"
    hashes_path = model_dir / "artifact_hashes.json"
    for path in (parameter_path, report_path, hashes_path):
        if not path.is_file():
            raise ValueError(f"missing sealed model artifact: {path}")
    hashes = json.loads(hashes_path.read_text(encoding="utf-8"))
    for name, path in (("model_parameters.json", parameter_path),
                       ("report.json", report_path)):
        actual = sha256_file(path)
        if hashes.get(name) != actual:
            raise ValueError(f"sealed model artifact hash mismatch: {name}")
    parameters = json.loads(parameter_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    for variant, dimension in (("current_rtl64", 64), ("opencv_hog324", 324)):
        entry = parameters.get(variant, {})
        if entry.get("class_order") != ["ped", "vehicle"]:
            raise ValueError(f"unexpected class order for {variant}")
        if entry.get("decision_score_positive_class") != "vehicle":
            raise ValueError(f"unexpected positive class for {variant}")
        if len(entry.get("folded_weights_on_raw_features", [])) != dimension:
            raise ValueError(f"unexpected feature dimension for {variant}")
    receipt = {
        "model_parameters": str(parameter_path),
        "model_parameters_sha256": sha256_file(parameter_path),
        "model_report": str(report_path),
        "model_report_sha256": sha256_file(report_path),
        "artifact_hashes": str(hashes_path),
        "artifact_hashes_sha256": sha256_file(hashes_path),
    }
    return parameters, report, receipt


def model_score(features: np.ndarray, model: dict[str, Any]) -> float:
    weights = np.asarray(model["folded_weights_on_raw_features"], dtype=np.float64)
    if features.shape != weights.shape:
        raise ValueError(f"feature/model dimension mismatch: {features.shape} vs {weights.shape}")
    return float(features @ weights + float(model["folded_bias_on_raw_features"]))


def quantization_contract(model: dict[str, Any]) -> dict[str, Any]:
    weights = np.asarray(model["folded_weights_on_raw_features"], dtype=np.float64)
    max_abs = float(np.max(np.abs(weights)))
    if max_abs == 0.0:
        raise ValueError("zero OpenCV HOG weight vector")
    feature_scale = 1 << 12
    weight_scale = ((1 << 15) - 1) / max_abs
    weight_q = np.rint(weights * weight_scale).astype(np.int64)
    bias_q = int(round(float(model["folded_bias_on_raw_features"]) *
                       feature_scale * weight_scale))
    if np.max(np.abs(weight_q)) > 32767:
        raise ValueError("quantized weights exceed signed 16-bit storage")
    return {
        "feature_scale": feature_scale,
        "feature_fraction_bits": 12,
        "feature_storage_bits_unsigned": 13,
        "weight_scale": weight_scale,
        "weight_storage_bits_signed": 16,
        "weight_q": weight_q,
        "bias_q": bias_q,
    }


def quantized_score(features: np.ndarray, contract: dict[str, Any]) -> tuple[int, float]:
    if float(np.min(features)) < -1e-12 or float(np.max(features)) > 1.0 + 1e-9:
        raise ValueError("OpenCV HOG feature violates unsigned [0,1] contract")
    feature_q = np.rint(features * contract["feature_scale"]).astype(np.int64)
    if np.max(feature_q) > (1 << contract["feature_storage_bits_unsigned"]) - 1:
        raise ValueError("Q1.12 feature overflow")
    score_q = int(feature_q @ contract["weight_q"] + contract["bias_q"])
    normalized = score_q / (contract["feature_scale"] * contract["weight_scale"])
    return score_q, float(normalized)


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> dict[str, Any]:
    if total == 0:
        return {"value": None, "low": None, "high": None,
                "successes": successes, "total": total}
    value = successes / total
    denominator = 1.0 + z * z / total
    centre = (value + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(value * (1 - value) / total + z * z / (4 * total * total)) / denominator
    return {"value": value, "low": max(0.0, centre - radius),
            "high": min(1.0, centre + radius), "successes": successes,
            "total": total}


def prediction_metrics(rows: list[dict[str, Any]], prediction_field: str,
                       accepted_field: str | None = None) -> dict[str, Any]:
    def accepted(row: dict[str, Any]) -> bool:
        return True if accepted_field is None else bool(row[accepted_field])

    output: dict[str, Any] = {"sample_count": len(rows)}
    for truth in ("ped", "vehicle"):
        selected = [row for row in rows if row["truth"] == truth]
        correct = sum(accepted(row) and row[prediction_field] == truth for row in selected)
        output[f"{truth}_recall"] = wilson(correct, len(selected))
    invalid = [row for row in rows if row["truth"] == "invalid"]
    invalid_accepted = sum(accepted(row) for row in invalid)
    output["invalid_acceptance"] = wilson(invalid_accepted, len(invalid))
    for label in ("ped", "vehicle"):
        predicted = [row for row in rows if accepted(row) and row[prediction_field] == label]
        correct = sum(row["truth"] == label for row in predicted)
        output[f"{label}_precision"] = wilson(correct, len(predicted))
    return output


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fields or (list(rows[0]) if rows else [])
    if not fieldnames:
        raise ValueError(f"CSV field list is empty: {path}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_virat_catalog() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    assert_safe_path(VIRAT_CATALOG, "VIRAT catalog")
    if not VIRAT_CATALOG.is_file():
        raise ValueError(f"missing VIRAT catalog: {VIRAT_CATALOG}")
    payload = json.loads(VIRAT_CATALOG.read_text(encoding="utf-8"))
    clips: dict[str, dict[str, Any]] = {}
    for item in payload.get("clips", []):
        clip_id = str(item.get("clip_id", ""))
        # Reserved records may be present in the catalog, but their paths are
        # never resolved, opened or hashed by this diagnostic.
        if FORBIDDEN_CLIP_TOKEN.search(clip_id):
            continue
        if clip_id in clips:
            raise ValueError(f"duplicate clip in VIRAT catalog: {clip_id}")
        clips[clip_id] = item
    return clips, {"path": str(VIRAT_CATALOG), "sha256": sha256_file(VIRAT_CATALOG)}


def adjudicated_records(path: Path, roi_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    assert_safe_path(path, "adjudicated CSV")
    finalized_receipt_path = path.parent / "receipt.json"
    if not finalized_receipt_path.is_file():
        raise ValueError(f"missing finalization receipt: {finalized_receipt_path}")
    finalized_receipt = json.loads(finalized_receipt_path.read_text(encoding="utf-8"))
    if finalized_receipt.get("status") != "complete_hash_verified_human_review_finalization":
        raise ValueError("finalization receipt status is not complete")
    expected_csv_hash = finalized_receipt.get("outputs", {}).get(path.name)
    if expected_csv_hash != sha256_file(path):
        raise ValueError("finalized adjudicated CSV does not match its receipt")
    rows = read_csv(path)
    if len(rows) != 54:
        raise ValueError(f"expected all 54 fill-only temporal groups, got {len(rows)}")
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    source_hashes: dict[Path, str] = {}
    captures: dict[Path, cv2.VideoCapture] = {}
    catalog, catalog_receipt = load_virat_catalog()
    roi_dir.mkdir(parents=True, exist_ok=True)
    try:
        for index, row in enumerate(rows, 2):
            assert_safe_record(row, f"adjudicated row {index}")
            if row.get("review_basis_canonical", "").strip() != "human_visual_review":
                raise ValueError(f"non-canonical review basis at line {index}")
            if not row.get("review_basis_source", "").strip():
                raise ValueError(f"missing source review basis at line {index}")
            if row.get("metric_eligible", "").strip().lower() != "yes":
                raise ValueError(f"non-eligible row in finalized fill set at line {index}")
            if row.get("audit_gap_codes", "").strip():
                raise ValueError(f"unresolved audit gap in finalized fill set at line {index}")
            if not row.get("adjudication_status", "").strip():
                raise ValueError(f"missing adjudication status at line {index}")
            group_id = first_value(row, ("group_id", "sample_id"), "group id")
            if group_id in seen:
                raise ValueError(f"duplicate adjudicated group id: {group_id}")
            seen.add(group_id)
            clip_id = first_value(row, ("clip_id",), "clip id")
            split = first_value(row, ("scene_split", "split"), "scene split").lower()
            if split not in ALLOWED_SPLITS:
                raise ValueError(f"sealed-data guard rejected split={split!r}")
            review_class = first_value(row, ("review_class", "final_review_class"),
                                       "review class")
            if review_class not in REVIEW_CLASS_TO_TRUTH:
                raise ValueError(f"unadjudicated or unknown review class: {group_id}")
            frame_index = int(first_value(row, ("middle_frame", "frame_index"),
                                          "middle frame"))
            box = parse_box(first_value(
                row,
                ("T100_selected_analysis_box", "t100_selected_analysis_box",
                 "selected_analysis_box", "analysis_box"),
                "T100 inclusive analysis box",
            ))
            catalog_row = catalog.get(clip_id)
            if catalog_row is None:
                raise ValueError(f"clip is absent from allowed VIRAT catalog entries: {clip_id}")
            if catalog_row.get("split") != split:
                raise ValueError(f"catalog split mismatch for {group_id}")
            if catalog_row.get("official_video_identity_check") != "pass_expected_size_and_sha256":
                raise ValueError(f"catalog video identity is not verified for {group_id}")
            video = Path(catalog_row["video_path"])
            assert_safe_path(video, "source video")
            if not video.is_file():
                raise ValueError(f"source video missing: {video}")
            expected_hash = first_value(row, ("source_video_sha256", "source_sha256"),
                                        "source video hash")
            if catalog_row.get("video_sha256") != expected_hash:
                raise ValueError(f"adjudicated/catalog video hash mismatch for {group_id}")
            actual_hash = source_hashes.setdefault(video, sha256_file(video))
            if actual_hash != expected_hash:
                raise ValueError(f"source video hash mismatch for {group_id}")
            capture = captures.get(video)
            if capture is None:
                capture = cv2.VideoCapture(str(video))
                if not capture.isOpened():
                    raise ValueError(f"cannot open source video: {video}")
                captures[video] = capture
            if not capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index):
                raise ValueError(f"cannot seek {clip_id} to frame {frame_index}")
            ok, frame = capture.read()
            if not ok or frame is None:
                raise ValueError(f"cannot decode {clip_id} frame {frame_index}")
            analysis = fpga_analysis_frame(frame)
            x0, y0, x1, y1 = box
            roi = fpga_resize_roi(analysis[y0:y1 + 1, x0:x1 + 1])
            roi_path = roi_dir / f"{group_id}.png"
            if roi_path.is_file():
                existing_roi = cv2.imread(str(roi_path), cv2.IMREAD_GRAYSCALE)
                if existing_roi is None or not np.array_equal(existing_roi, roi):
                    raise ValueError(
                        f"existing generated ROI does not match current contract: {roi_path}"
                    )
            elif not cv2.imwrite(str(roi_path), roi):
                raise ValueError(f"failed to write generated ROI: {roi_path}")
            scene_id = str(catalog_row.get("scene_id", ""))
            if not scene_id:
                raise ValueError(f"catalog scene id missing for {clip_id}")
            crop_usable = row.get("crop_usable", "not_available").strip() or "not_available"
            if crop_usable not in {"yes", "no", "uncertain", "not_available"}:
                raise ValueError(f"invalid crop_usable for {group_id}: {crop_usable}")
            records.append({
                "sample_id": group_id,
                "review_set": "fill_only_adjudicated",
                "scene_id": scene_id,
                "split": split,
                "source_frame": frame_index,
                "source_kind": "fill_only_middle_frame_t100",
                "review_class": review_class,
                "truth": REVIEW_CLASS_TO_TRUTH[review_class],
                "full_truncated": review_class if review_class.startswith("ped_") else "not_ped",
                "crop_usable": crop_usable,
                "occlusion": row.get("occlusion", "not_available").strip() or "not_available",
                "truncation_reason": row.get("truncation_reason", "not_available").strip() or "not_available",
                "roi_path": str(roi_path.relative_to(roi_dir.parent).as_posix()),
                "roi_pixel_sha256": pixel_sha256(roi),
                "_roi": roi,
            })
    finally:
        for capture in captures.values():
            capture.release()
    return records, {
        "path": str(path.resolve()), "sha256": sha256_file(path),
        "row_count": len(rows), "generated_roi_count": len(records),
        "source_video_hashes": {str(path): digest for path, digest in source_hashes.items()},
        "catalog": catalog_receipt,
        "finalization_receipt": {
            "path": str(finalized_receipt_path.resolve()),
            "sha256": sha256_file(finalized_receipt_path),
            "status": finalized_receipt["status"],
        },
    }


def validation_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    for candidate_root in VALIDATION_REVIEW_ROOTS:
        assert_safe_path(candidate_root, "validation candidate root")
        reviewed_path = candidate_root / "reviewed/reviewed_candidates.csv"
        rows, receipt = load_reviewed(candidate_root, reviewed_path, "val")
        provenance = json.loads((candidate_root / "provenance.json").read_text(encoding="utf-8"))
        source_path = Path(provenance["source"])
        assert_safe_path(source_path, "validation source video")
        if sha256_file(source_path) != provenance["source_sha256"]:
            raise ValueError(f"validation source video hash mismatch: {candidate_root.name}")
        receipt["source_video_hash_verified"] = True
        receipts.append(receipt)
        for row in rows:
            assert_safe_record(row, "validation reviewed row")
            if row["label"] == "ignore":
                raise ValueError("the fixed 70-candidate validation set must not contain ignore")
            roi_path = candidate_root / row["roi_path"]
            with Image.open(roi_path) as image:
                roi = np.asarray(image.convert("L"), dtype=np.uint8)
            records.append({
                "sample_id": f"{candidate_root.name}:{row['candidate_id']}",
                "review_set": candidate_root.name,
                "scene_id": receipt["scene_id"],
                "split": "val",
                "source_frame": int(row["source_frame"]),
                "source_kind": "reviewed_validation_ccl",
                "review_class": row["label"],
                "truth": row["label"],
                "full_truncated": "not_available",
                "crop_usable": "not_available",
                "occlusion": "not_available",
                "truncation_reason": "not_available",
                "roi_path": str(roi_path.resolve()),
                "roi_pixel_sha256": pixel_sha256(roi),
                "_roi": roi,
            })
    if len(records) != 70 or Counter(row["truth"] for row in records) != {
        "ped": 20, "vehicle": 32, "invalid": 18,
    }:
        raise ValueError("reviewed validation CCL set is not the sealed 70-row set")
    return records, receipts


def evaluate(records: list[dict[str, Any]], parameters: dict[str, Any]) -> tuple[
        list[dict[str, Any]], dict[str, Any]]:
    hog324 = make_hog324()
    q_contract = quantization_contract(parameters["opencv_hog324"])
    evaluated: list[dict[str, Any]] = []
    q_errors: list[float] = []
    q_mismatches = 0
    margin_condition_failures = 0
    for record in records:
        base = {key: value for key, value in record.items() if not key.startswith("_")}
        features64 = extract_variant(record["_roi"], "current_rtl64", hog324)
        score64 = model_score(features64, parameters["current_rtl64"])
        features324 = extract_variant(record["_roi"], "opencv_hog324", hog324)
        score324 = model_score(features324, parameters["opencv_hog324"])
        score_q, score_q_normalized = quantized_score(features324, q_contract)
        prediction64 = "vehicle" if score64 >= 0 else "ped"
        prediction324 = "vehicle" if score324 >= 0 else "ped"
        prediction_q = "vehicle" if score_q >= 0 else "ped"
        error = score_q_normalized - score324
        margin_safe = abs(score324) > abs(error)
        q_errors.append(abs(error))
        q_mismatches += prediction324 != prediction_q
        margin_condition_failures += not margin_safe
        evaluated.append({
            **base,
            "retrained_rtl64_reference_float_score": score64,
            "retrained_rtl64_reference_prediction": prediction64,
            "opencv_hog324_float_score": score324,
            "opencv_hog324_float_prediction": prediction324,
            "opencv_hog324_score_q": score_q,
            "opencv_hog324_score_q_normalized": score_q_normalized,
            "opencv_hog324_quantized_prediction": prediction_q,
            "opencv_hog324_float_quantized_label_mismatch": int(prediction324 != prediction_q),
            "opencv_hog324_abs_quantization_error": abs(error),
            "opencv_hog324_abs_float_margin": abs(score324),
            "opencv_hog324_margin_exceeds_own_error": int(margin_safe),
        })
    q_summary = {
        "feature_format": {
            "name": "unsigned_Q1.12", "scale": q_contract["feature_scale"],
            "rounding": "numpy.rint_round_to_nearest_even",
        },
        "weight_format": {
            "signed_bits": 16, "scale": q_contract["weight_scale"],
            "rounding": "numpy.rint_round_to_nearest_even",
        },
        "bias_q": q_contract["bias_q"],
        "sample_count": len(evaluated),
        "float_quantized_label_mismatch": int(q_mismatches),
        "max_abs_normalized_score_error": max(q_errors, default=0.0),
        "mean_abs_normalized_score_error": float(np.mean(q_errors)) if q_errors else 0.0,
        "margin_condition": "abs(float_score) > abs(quantized_normalized_score - float_score)",
        "margin_condition_not_proven_count": int(margin_condition_failures),
        "note": "The condition is a per-sample sufficient sign-stability check, not a calibrated confidence measure.",
    }
    return evaluated, q_summary


def metric_record(model: str, group_type: str, group_value: str,
                  selected: list[dict[str, Any]], prediction_field: str) -> dict[str, Any]:
    metrics = prediction_metrics(selected, prediction_field)
    output: dict[str, Any] = {
        "model": model, "group_type": group_type, "group_value": group_value,
        "sample_count": len(selected),
    }
    for name in ("ped_recall", "vehicle_recall", "invalid_acceptance",
                 "ped_precision", "vehicle_precision"):
        item = metrics[name]
        output[f"{name}_value"] = item["value"]
        output[f"{name}_low95"] = item["low"]
        output[f"{name}_high95"] = item["high"]
        output[f"{name}_numerator"] = item["successes"]
        output[f"{name}_denominator"] = item["total"]
    return output


def stratified_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    model_fields = {
        "retrained_rtl64_reference": "retrained_rtl64_reference_prediction",
        "opencv_hog324_float": "opencv_hog324_float_prediction",
        "opencv_hog324_q": "opencv_hog324_quantized_prediction",
    }
    groups = {
        "overall": ["all"],
        "scene": sorted({row["scene_id"] for row in rows}),
        "review_set": sorted({row["review_set"] for row in rows}),
        "full_truncated": sorted({row["full_truncated"] for row in rows}),
        "usable": sorted({row["crop_usable"] for row in rows}),
    }
    output: list[dict[str, Any]] = []
    for model, field in model_fields.items():
        for group_type, values in groups.items():
            for value in values:
                key = {"scene": "scene_id", "usable": "crop_usable"}.get(
                    group_type, group_type)
                selected = rows if group_type == "overall" else [
                    row for row in rows if row[key] == value
                ]
                output.append(metric_record(model, group_type, value, selected, field))
    return output


def paired_gate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    groups = {
        "descriptive_union": rows,
        "fill_only_adjudicated": [row for row in rows if row["source_kind"] == "fill_only_middle_frame_t100"],
        "reviewed_validation_ccl": [row for row in rows if row["source_kind"] == "reviewed_validation_ccl"],
    }
    for value in sorted({row["review_set"] for row in rows}):
        groups[value] = [row for row in rows if row["review_set"] == value]
    for name, selected_all in groups.items():
        selected = [row for row in selected_all if row["truth"] in {"ped", "vehicle"}]
        if not selected:
            continue
        both = current_only = opencv_only = neither = 0
        for row in selected:
            current = row["retrained_rtl64_reference_prediction"] == row["truth"]
            opencv = row["opencv_hog324_quantized_prediction"] == row["truth"]
            if current and opencv:
                both += 1
            elif current:
                current_only += 1
            elif opencv:
                opencv_only += 1
            else:
                neither += 1
        discordant = current_only + opencv_only
        two_sided = 1.0 if discordant == 0 else min(
            1.0,
            2.0 * sum(math.comb(discordant, k) for k in range(0, min(current_only, opencv_only) + 1)) /
            (2 ** discordant),
        )
        current_metrics = prediction_metrics(selected, "retrained_rtl64_reference_prediction")
        opencv_metrics = prediction_metrics(selected, "opencv_hog324_quantized_prediction")
        support = Counter(row["truth"] for row in selected)
        gate_evaluable = support["ped"] > 0 and support["vehicle"] > 0
        no_class_regression = all(
            (opencv_metrics[f"{label}_recall"]["value"] or 0.0) >=
            (current_metrics[f"{label}_recall"]["value"] or 0.0)
            for label in ("ped", "vehicle")
        )
        output.append({
            "review_set": name, "object_sample_count": len(selected),
            "both_correct": both, "current_only_correct": current_only,
            "opencv_only_correct": opencv_only, "both_wrong": neither,
            "net_correct_delta_opencv_minus_current": opencv_only - current_only,
            "exact_mcnemar_two_sided_p": two_sided,
            "exploratory_gate_definition": "net_correct_delta>=0 and no ped/vehicle recall regression",
            "ped_support": support["ped"], "vehicle_support": support["vehicle"],
            "gate_evaluable_both_classes_present": gate_evaluable,
            "exploratory_gate_pass": (
                (opencv_only >= current_only and no_class_regression)
                if gate_evaluable else None
            ),
            "acceptance_eligible": False,
            "scope_boundary": (
                "heterogeneous descriptive union" if name == "descriptive_union"
                else "small reviewed pilot"
            ),
            "invalid_candidates_excluded_reason": "raw binary models cannot reject invalid candidates",
        })
    return output


def approved_validation_pilot_gate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate the predeclared HOG324 pilot gate on validation scenes only.

    Fill-only records from train scene 000206 are useful error-analysis inputs,
    but they must not contribute to this gate.  Invalid candidates are also
    outside the paired binary-class comparison and are handled by the separate
    rejection scan.
    """
    selected = [
        row for row in rows
        if row["split"] == "val" and row["truth"] in {"ped", "vehicle"}
    ]
    scene_ids = sorted({row["scene_id"] for row in selected})
    scene_rows: list[dict[str, Any]] = []
    for scene_id in scene_ids:
        current_scene = [row for row in selected if row["scene_id"] == scene_id]
        record: dict[str, Any] = {"scene_id": scene_id}
        for truth in ("ped", "vehicle"):
            class_rows = [row for row in current_scene if row["truth"] == truth]
            current_correct = sum(
                row["retrained_rtl64_reference_prediction"] == truth
                for row in class_rows
            )
            hog_correct = sum(
                row["opencv_hog324_quantized_prediction"] == truth
                for row in class_rows
            )
            record[f"{truth}_support"] = len(class_rows)
            record[f"{truth}_rtl64_correct"] = current_correct
            record[f"{truth}_hog324q_correct"] = hog_correct
            record[f"{truth}_correct_delta"] = hog_correct - current_correct
        scene_rows.append(record)

    pooled: dict[str, Any] = {}
    recalls: dict[str, dict[str, float]] = {
        "retrained_rtl64_reference": {}, "opencv_hog324_q": {}
    }
    for truth in ("ped", "vehicle"):
        class_rows = [row for row in selected if row["truth"] == truth]
        current_correct = sum(
            row["retrained_rtl64_reference_prediction"] == truth
            for row in class_rows
        )
        hog_correct = sum(
            row["opencv_hog324_quantized_prediction"] == truth
            for row in class_rows
        )
        pooled[f"{truth}_support"] = len(class_rows)
        pooled[f"{truth}_rtl64_correct"] = current_correct
        pooled[f"{truth}_hog324q_correct"] = hog_correct
        pooled[f"{truth}_correct_delta"] = hog_correct - current_correct
        recalls["retrained_rtl64_reference"][truth] = current_correct / len(class_rows)
        recalls["opencv_hog324_q"][truth] = hog_correct / len(class_rows)

    current_ba = sum(recalls["retrained_rtl64_reference"].values()) / 2.0
    hog_ba = sum(recalls["opencv_hog324_q"].values()) / 2.0
    conditions = {
        "every_validation_scene_ped_correct_not_lower": all(
            item["ped_hog324q_correct"] >= item["ped_rtl64_correct"]
            for item in scene_rows if item["ped_support"] > 0
        ),
        "at_least_one_validation_scene_ped_correct_higher": any(
            item["ped_hog324q_correct"] > item["ped_rtl64_correct"]
            for item in scene_rows if item["ped_support"] > 0
        ),
        "pooled_ped_correct_delta_at_least_3": pooled["ped_correct_delta"] >= 3,
        "every_validation_scene_vehicle_correct_not_lower": all(
            item["vehicle_hog324q_correct"] >= item["vehicle_rtl64_correct"]
            for item in scene_rows if item["vehicle_support"] > 0
        ),
        "pooled_vehicle_correct_not_lower": pooled["vehicle_correct_delta"] >= 0,
        "pooled_balanced_accuracy_delta_at_least_0_05": hog_ba - current_ba >= 0.05,
    }
    return {
        "status": "pilot_route_gate_pass" if all(conditions.values()) else "pilot_route_gate_fail",
        "acceptance_eligible": False,
        "scope": "validation_split_only; train-scene fill rows and invalid candidates excluded",
        "scene_ids": scene_ids,
        "object_sample_count": len(selected),
        "scene_counts": scene_rows,
        "pooled": {
            **pooled,
            "rtl64_balanced_accuracy": current_ba,
            "hog324q_balanced_accuracy": hog_ba,
            "balanced_accuracy_delta": hog_ba - current_ba,
        },
        "predeclared_conditions": conditions,
        "all_conditions_pass": all(conditions.values()),
        "interpretation": "continue HOG324 data expansion and integer-reference work; do not freeze model or RTL",
    }


def threshold_scan(rows: list[dict[str, Any]], scope: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    magnitudes = sorted({abs(int(row["opencv_hog324_score_q"])) for row in rows})
    # These are all integer cutoffs at which acceptance can change.  Every
    # omitted integer has exactly the same outcome as the preceding row.
    thresholds = sorted({0, *(value + 1 for value in magnitudes)})
    output: list[dict[str, Any]] = []
    feasible: list[dict[str, Any]] = []
    for threshold in thresholds:
        working = []
        for row in rows:
            copy = dict(row)
            copy["threshold_accepted"] = abs(int(row["opencv_hog324_score_q"])) >= threshold
            working.append(copy)
        metrics = prediction_metrics(
            working, "opencv_hog324_quantized_prediction", "threshold_accepted"
        )
        item: dict[str, Any] = {
            "scope": scope,
            "abs_score_q_threshold": threshold,
            "accepted_count": sum(row["threshold_accepted"] for row in working),
            "rejected_count": sum(not row["threshold_accepted"] for row in working),
        }
        for name in ("ped_recall", "vehicle_recall", "invalid_acceptance"):
            value = metrics[name]
            item[f"{name}_value"] = value["value"]
            item[f"{name}_low95"] = value["low"]
            item[f"{name}_high95"] = value["high"]
            item[f"{name}_numerator"] = value["successes"]
            item[f"{name}_denominator"] = value["total"]
        item["suggested_point_feasible"] = bool(
            item["ped_recall_value"] is not None and
            item["vehicle_recall_value"] is not None and
            item["invalid_acceptance_value"] is not None and
            item["ped_recall_value"] >= TARGETS["ped_recall"] and
            item["vehicle_recall_value"] >= TARGETS["vehicle_recall"] and
            item["invalid_acceptance_value"] <= TARGETS["invalid_acceptance"]
        )
        output.append(item)
        if item["suggested_point_feasible"]:
            feasible.append(dict(item))
    return output, feasible


def self_test() -> None:
    assert parse_box("[1, 2, 3, 4]") == (1, 2, 3, 4)
    assert wilson(0, 0)["value"] is None
    assert wilson(5, 10)["low"] < 0.5 < wilson(5, 10)["high"]
    try:
        assert_safe_path(Path("blind/sample.csv"), "synthetic")
    except ValueError:
        pass
    else:
        raise AssertionError("blind guard did not fail closed")
    try:
        assert_safe_record({"clip_id": "VIRAT_S_000205_x"}, "synthetic")
    except ValueError:
        pass
    else:
        raise AssertionError("reserved clip guard did not fail closed")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "metrics.csv"
        write_csv(path, [{"a": 1, "b": 2}])
        assert read_csv(path) == [{"a": "1", "b": "2"}]
    zero = np.zeros((32, 32), dtype=np.uint8)
    assert extract_variant(zero, "current_rtl64", make_hog324()).shape == (64,)
    assert extract_variant(zero, "opencv_hog324", make_hog324()).shape == (324,)
    gate_rows = []
    for scene_id in ("scene-a", "scene-b"):
        for index in range(4):
            gate_rows.append({
                "split": "val", "scene_id": scene_id, "truth": "ped",
                "retrained_rtl64_reference_prediction": "ped" if index == 0 else "vehicle",
                "opencv_hog324_quantized_prediction": "ped" if index < 3 else "vehicle",
            })
        gate_rows.append({
            "split": "val", "scene_id": scene_id, "truth": "vehicle",
            "retrained_rtl64_reference_prediction": "vehicle",
            "opencv_hog324_quantized_prediction": "vehicle",
        })
    # A train row must not alter the validation-only gate.
    gate_rows.append({
        "split": "train", "scene_id": "scene-train", "truth": "ped",
        "retrained_rtl64_reference_prediction": "vehicle",
        "opencv_hog324_quantized_prediction": "vehicle",
    })
    gate = approved_validation_pilot_gate(gate_rows)
    assert gate["all_conditions_pass"] is True
    assert gate["object_sample_count"] == 10
    assert gate["pooled"]["ped_correct_delta"] == 4
    print(json.dumps({"self_test": "pass"}))


def run(adjudicated: Path, model_dir: Path, output: Path,
        validation_only: bool = False) -> None:
    assert_safe_path(output, "output")
    parameters, source_report, model_receipt = load_models(model_dir)
    if validation_only:
        fill_records: list[dict[str, Any]] = []
        fill_receipt: dict[str, Any] = {
            "status": "not_read_in_validation_only_mode", "path": str(adjudicated)
        }
    else:
        fill_records, fill_receipt = adjudicated_records(
            adjudicated, output / "fill_rois"
        )
    validation, validation_receipts = validation_records()
    records = fill_records + validation
    evaluated, quantization = evaluate(records, parameters)
    metrics = stratified_metrics(evaluated)
    gates = paired_gate(evaluated)
    approved_gate = approved_validation_pilot_gate(evaluated)
    scopes = {
        "reviewed_validation_ccl": [row for row in evaluated if row["source_kind"] == "reviewed_validation_ccl"],
        "validation_union": [row for row in evaluated if row["split"] == "val"],
        "descriptive_union": evaluated,
    }
    if fill_records:
        scopes = {
            "fill_only_adjudicated": [row for row in evaluated if row["source_kind"] == "fill_only_middle_frame_t100"],
            **scopes,
        }
    scan: list[dict[str, Any]] = []
    feasible_by_scope: dict[str, list[dict[str, Any]]] = {}
    for scope, selected in scopes.items():
        scope_scan, scope_feasible = threshold_scan(selected, scope)
        scan.extend(scope_scan)
        feasible_by_scope[scope] = scope_feasible

    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "predictions.csv", evaluated)
    write_csv(output / "stratified_metrics.csv", metrics)
    write_csv(output / "paired_pilot_gate.csv", gates)
    write_csv(
        output / "approved_validation_pilot_gate.csv",
        approved_gate["scene_counts"],
    )
    write_csv(output / "threshold_scan.csv", scan)

    report = {
        "status": "candidate_diagnostic_not_acceptance_not_threshold_selection_not_rtl",
        "scope": {
            "models_loaded_without_retraining": ["retrained_rtl64_reference", "opencv_hog324"],
            "fill_roi_contract": "middle_frame -> fpga_analysis_frame gray/stride5 -> T100 inclusive crop -> fpga_resize_roi 32x32",
            "validation_ccl_contract": "three complete reviewed val candidate sets; 70 ROI pixel hashes reverified",
            "test_blind_holdout_reserve": "rejected by fail-closed path, record, split and clip guards",
            "forbidden_clips": ["000205", "000207", "010106", "010108"],
            "threshold_selection": False,
            "model_training": False,
            "validation_only_mode": validation_only,
        },
        "counts": {
            "total": len(evaluated),
            "fill_only_adjudicated": len(fill_records),
            "reviewed_validation_ccl": len(validation),
            "truth": dict(sorted(Counter(row["truth"] for row in evaluated).items())),
            "review_class": dict(sorted(Counter(row["review_class"] for row in evaluated).items())),
            "scene": dict(sorted(Counter(row["scene_id"] for row in evaluated).items())),
            "review_set": dict(sorted(Counter(row["review_set"] for row in evaluated).items())),
            "full_truncated": dict(sorted(Counter(row["full_truncated"] for row in evaluated).items())),
            "usable": dict(sorted(Counter(row["crop_usable"] for row in evaluated).items())),
        },
        "metrics_by_evidence_set": {
            scope: {
                "retrained_rtl64_reference": prediction_metrics(selected, "retrained_rtl64_reference_prediction"),
                "opencv_hog324_float": prediction_metrics(selected, "opencv_hog324_float_prediction"),
                "opencv_hog324_q": prediction_metrics(selected, "opencv_hog324_quantized_prediction"),
                "acceptance_eligible": False,
                "boundary": ("descriptive union; heterogeneous review sets" if scope == "descriptive_union"
                             else "small reviewed pilot; report separately"),
            }
            for scope, selected in scopes.items()
        },
        "opencv_hog324_quantization": quantization,
        "paired_pilot_gate": gates,
        "approved_validation_pilot_gate": approved_gate,
        "threshold_scan": {
            "semantics": "accept iff abs(score_q)>=threshold; rows contain every integer cutoff where an observed decision can change",
            "outcome_distinct_integer_threshold_count_by_scope": {
                scope: sum(row["scope"] == scope for row in scan) for scope in scopes
            },
            "suggested_targets_unfrozen": TARGETS,
            "feasible_point_count_by_scope": {
                scope: len(points) for scope, points in feasible_by_scope.items()
            },
            "feasible_points_by_scope": feasible_by_scope,
            "selected_threshold": None,
        },
        "inputs": {
            "adjudicated": fill_receipt,
            "validation_review_sets": validation_receipts,
            "model": model_receipt,
            "source_model_report_status": source_report.get("status"),
        },
        "implementation": {
            "script": str(SCRIPT_PATH), "script_sha256": sha256_file(SCRIPT_PATH),
            "opencv": cv2.__version__, "numpy": np.__version__,
        },
        "limitations": [
            "OpenCV HOG extraction remains floating point; Q1.12 quantizes only its descriptor output.",
            "The parameter key current_rtl64 is reported as retrained_rtl64_reference because it was refit in the external experiment and is not the historical 55% candidate model.",
            "The 16-bit weights and integer accumulator are feasibility arithmetic, not an RTL implementation or Python/RTL equivalence claim.",
            "VIRAT labels are not exhaustive; invalid truth comes only from explicit human adjudication, never from unmatched annotation regions.",
            "Wilson intervals describe this small reviewed pilot and are not independent-scene deployment guarantees.",
            "Scores are SVM margins, not probabilities.",
        ],
    }
    report_path = output / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    artifacts = {}
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name != "artifact_hashes.json":
            artifacts[path.relative_to(output).as_posix()] = sha256_file(path)
    (output / "artifact_hashes.json").write_text(
        json.dumps(artifacts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": report["status"], "total": len(evaluated),
        "fill": len(fill_records), "validation_ccl": len(validation),
        "float_quantized_mismatch": quantization["float_quantized_label_mismatch"],
        "feasible_threshold_points": {key: len(value) for key, value in feasible_by_scope.items()},
        "output": str(output),
    }, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--adjudicated", type=Path, default=DEFAULT_ADJUDICATED)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validation-only", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    run(args.adjudicated.resolve(), args.model_dir.resolve(), args.output.resolve(),
        validation_only=args.validation_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
