#!/usr/bin/env python3
"""Run the preregistered three-fit HOG324 augmentation diagnostic once."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import cv2
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
EXTERNAL = PROJECT / "external_reference_exploration"
for directory in (PROJECT / "tools", EXTERNAL):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from local_fourgrid_diagnostic import (  # noqa: E402
    analysis_box,
    digest,
    pixel_sha256,
    roi_pair,
    validate_confirmation_chain,
    validated_package,
)
from local_paired_diagnostic import validate_annotations  # noqa: E402
from opencv_hog_candidate_diagnostic import (  # noqa: E402
    load_models,
    model_score,
    quantization_contract,
    quantized_score,
)
from opencv_hog_diagnostic import load_roi, make_hog, read_manifest  # noqa: E402
from roi_dataset_tool import fpga_analysis_frame, fpga_gray_bgr  # noqa: E402


DATASET = PROJECT / "road_roi_dataset_virat"
EXPERIMENT = PROJECT / "evaluation/hog_svm_parallel_20261011/experiment.json"
OUTPUT = PROJECT / "evaluation/hog_svm_parallel_20261011/augmentation_v1"
BASELINE = PROJECT / "external_reference_exploration/results/opencv_hog_diagnostic"
PACKAGE = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_target32_v2"
ANNOTATIONS = (
    PROJECT / "evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930"
    / "annotations.confirmed.json"
)
FOURGRID = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_fourgrid_v2"
BASELINE_PARAMETER_SHA256 = "9b6a96aeae291d60628c7352616fade1b03cb280a8ed6c8384b6acd03c13a99a"
EXPERIMENT_SHA256 = "4dffbfee4f550702f622e623daa66a9c4ec28a3062328438a42461c4c29e6963"
FOURGRID_RECEIPT_SHA256 = "7513425a415679968e6f80713efb8f6ff2ce2e6648f6dd5e4adbbe8416b1be84"
FOURGRID_ROWS_SHA256 = "fc3d0642dfcfb88d30be3632c213d9551225d2a42d01551ebd2d417f3332803d"
LABEL_TO_ID = {"ped": 0, "vehicle": 1}
ID_TO_LABEL = {value: key for key, value in LABEL_TO_ID.items()}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def augment_roi(roi: np.ndarray, mirror: bool, dx: int, dy: int) -> np.ndarray:
    """Mirror first, then integer translate with replicated 32x32 boundaries."""
    if roi.shape != (32, 32) or roi.dtype != np.uint8:
        raise ValueError("augmentation input must be 32x32 uint8")
    image = cv2.flip(roi, 1) if mirror else roi
    if dx or dy:
        image = cv2.warpAffine(
            image,
            np.asarray([[1, 0, dx], [0, 1, dy]], dtype=np.float32),
            (32, 32),
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_REPLICATE,
        )
    return np.ascontiguousarray(image, dtype=np.uint8)


def augmentation_rows(
    originals: Sequence[Mapping[str, Any]], transforms: Sequence[Sequence[Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not transforms:
        raise ValueError("fit has no registered augmentation")
    output: list[dict[str, Any]] = []
    keys: set[tuple[str, int]] = set()
    duplicate_pixels = 0
    for original in originals:
        local_hashes: dict[str, int] = {}
        weight = 1.0 / len(transforms)
        for index, (mirror, dx, dy) in enumerate(transforms):
            key = (str(original["sample_key"]), index)
            if key in keys:
                raise ValueError(f"duplicate augmentation identity: {key}")
            keys.add(key)
            roi = augment_roi(original["roi"], bool(mirror), int(dx), int(dy))
            roi_hash = pixel_sha256(roi)
            duplicate_of = local_hashes.get(roi_hash)
            duplicate_pixels += duplicate_of is not None
            local_hashes.setdefault(roi_hash, index)
            output.append({
                **{k: v for k, v in original.items() if k != "roi"},
                "augmentation_index": index,
                "mirror": bool(mirror),
                "dx": int(dx),
                "dy": int(dy),
                "sample_weight": weight,
                "roi_pixel_sha256": roi_hash,
                "duplicate_of_augmentation_index": duplicate_of,
                "roi": roi,
            })
    totals = defaultdict(float)
    class_totals = defaultdict(float)
    for row in output:
        totals[row["sample_key"]] += row["sample_weight"]
        class_totals[row["truth"]] += row["sample_weight"]
    if any(not np.isclose(value, 1.0) for value in totals.values()):
        raise AssertionError("per-original augmentation weight does not sum to one")
    expected_class_totals = Counter(row["truth"] for row in originals)
    if any(not np.isclose(class_totals[label], count)
           for label, count in expected_class_totals.items()):
        raise AssertionError("augmentation changed original class sample weight")
    return output, {
        "original_count": len(originals),
        "registered_transforms_per_original": len(transforms),
        "fit_row_count": len(output),
        "unique_root_augmentation_keys": len(keys),
        "same_original_duplicate_pixel_rows_retained": duplicate_pixels,
        "per_original_total_sample_weight_min": min(totals.values()),
        "per_original_total_sample_weight_max": max(totals.values()),
        "class_total_sample_weight": dict(sorted(class_totals.items())),
        "duplicate_policy": (
            "retain every preregistered (root,augmentation) row; equal weights still sum "
            "to one per original; duplicate pixels are explicitly marked"
        ),
    }


def hog_features(hog: cv2.HOGDescriptor, rows: Sequence[Mapping[str, Any]]) -> np.ndarray:
    features = [
        hog.compute(np.ascontiguousarray(row["roi"]), winStride=(0, 0), padding=(0, 0))
        .reshape(-1).astype(np.float64)
        for row in rows
    ]
    result = np.vstack(features)
    if result.shape != (len(rows), 324):
        raise ValueError(f"unexpected HOG324 shape: {result.shape}")
    if float(result.min()) < -1e-12 or float(result.max()) > 1.0 + 1e-9:
        raise ValueError("HOG324 descriptor is outside [0,1]")
    return result


def local_samples() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    package, package_receipt_hash = validated_package(PACKAGE)
    annotation = read_json(ANNOTATIONS)
    validate_annotations(annotation, package)
    confirmation = validate_confirmation_chain(ANNOTATIONS, annotation)

    receipt_path = FOURGRID / "receipt.json"
    if sha256(receipt_path) != FOURGRID_RECEIPT_SHA256:
        raise ValueError("frozen four-grid receipt hash changed")
    receipt = read_json(receipt_path)
    rows_path = FOURGRID / "fourgrid_rows.json"
    if sha256(rows_path) != FOURGRID_ROWS_SHA256:
        raise ValueError("frozen four-grid rows hash changed")
    if receipt.get("artifact_hashes", {}).get(rows_path.name) != sha256(rows_path):
        raise ValueError("four-grid rows do not match receipt")
    old_rows = read_json(rows_path)
    if len(old_rows) != 57:
        raise ValueError(f"expected 57 four-grid targets, got {len(old_rows)}")
    by_frame: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in old_rows:
        by_frame[int(row["frame_index"])].append(row)

    annotation_identity = {
        (int(frame["frame_index"]), target["label"], target["track_id"], target["visibility"],
         tuple(target["box"]))
        for frame in annotation["frames"]
        for target in frame["targets"]
        if target["motion"] == "moving" and target["label"] in LABEL_TO_ID
    }
    row_identity = {
        (int(row["frame_index"]), row["label"], row["track_id"], row["visibility"],
         tuple(row["original_gt_box"]))
        for row in old_rows
    }
    if row_identity != annotation_identity:
        raise ValueError("four-grid labels/targets do not match confirmed annotations")

    gt_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for frame_row in package["frames"]:
        frame_index = int(frame_row["frame_index"])
        frame_path = PACKAGE / frame_row["path"]
        if sha256(frame_path) != frame_row["sha256"]:
            raise ValueError(f"target32_v2 frame hash mismatch: {frame_path}")
        frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
        if frame is None or frame.shape[:2] != (720, 1280):
            raise ValueError(f"invalid target32_v2 PNG: {frame_path}")
        full_gray = fpga_gray_bgr(frame)
        analysis_gray = fpga_analysis_frame(frame)
        if not np.array_equal(full_gray[::5, ::5], analysis_gray):
            raise AssertionError("dense/analysis gray stride mismatch")
        for old in by_frame.get(frame_index, []):
            if analysis_box(old["original_gt_box"]) != old["gt_analysis_box"]:
                raise ValueError("stored GT analysis box changed")
            _, gt_roi, _ = roi_pair(full_gray, analysis_gray, old["gt_analysis_box"])
            if pixel_sha256(gt_roi) != old["B"]["roi_pixel_sha256"]:
                raise ValueError("rebuilt GT B ROI pixel hash differs from four-grid record")
            base = {
                "truth": old["label"],
                "scene_id": "local2415171",
                "source_family": "local2415171",
                "source_sha256": package["source_sha256"],
                "frame_index": frame_index,
                "track_id": old["track_id"],
                "visibility": old["visibility"],
                "matched": bool(old["matched"]),
            }
            gt_rows.append({
                **base,
                "sample_key": f"local:B:f{frame_index:06d}:{old['track_id']}",
                "dataset": "local_gt_B",
                "roi_pixel_sha256": pixel_sha256(gt_roi),
                "roi": gt_roi,
            })
            if old["matched"]:
                if old["C"] is None or old["candidate_analysis_box"] is None:
                    raise ValueError("matched target lacks candidate C")
                _, candidate_roi, _ = roi_pair(
                    full_gray, analysis_gray, old["candidate_analysis_box"]
                )
                if pixel_sha256(candidate_roi) != old["C"]["roi_pixel_sha256"]:
                    raise ValueError("rebuilt candidate C ROI pixel hash differs from four-grid record")
                candidate_rows.append({
                    **base,
                    "sample_key": f"local:C:f{frame_index:06d}:{old['track_id']}",
                    "dataset": "local_matched_C",
                    "roi_pixel_sha256": pixel_sha256(candidate_roi),
                    "roi": candidate_roi,
                })
    if len(gt_rows) != 57 or len(candidate_rows) != 14:
        raise ValueError(f"unexpected local counts B={len(gt_rows)} C={len(candidate_rows)}")
    return gt_rows, candidate_rows, {
        "package_receipt_sha256": package_receipt_hash,
        "annotation_sha256": sha256(ANNOTATIONS),
        "confirmation_receipt_sha256": confirmation["sha256"],
        "fourgrid_receipt_sha256": sha256(receipt_path),
        "fourgrid_rows_sha256": sha256(rows_path),
        "inputs": "target32_v2 PNG only; no grid/JPG/source-video crop",
    }


def official_samples() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = read_manifest(DATASET)
    samples = []
    for row in rows:
        roi = load_roi(DATASET, row, verify_hash=True)
        samples.append({
            "sample_key": f"official:{row['sample_id']}",
            "dataset": f"official_{row['split']}",
            "truth": row["label"],
            "scene_id": row["scene_id"],
            "source_family": row["source_family"],
            "source_sha256": row["source_sha256"],
            "frame_index": int(row["frame_index"]),
            "track_id": "",
            "visibility": "",
            "matched": True,
            "roi_pixel_sha256": row["roi_sha256"],
            "roi_path": row["roi_path"],
            "roi": roi,
        })
    train = [row for row in samples if row["dataset"] == "official_train"]
    val = [row for row in samples if row["dataset"] == "official_val"]
    if len(train) != 360 or len(val) != 69:
        raise ValueError(f"unexpected official counts train={len(train)} val={len(val)}")
    return train, val, {
        "manifest_sha256": sha256(DATASET / "manifest.csv"),
        "train_count": len(train),
        "val_count": len(val),
    }


def intersection(left: Iterable[str], right: Iterable[str]) -> list[str]:
    return sorted(set(left) & set(right))


def leakage_audit(
    train: Sequence[Mapping[str, Any]],
    val: Sequence[Mapping[str, Any]],
    local_gt: Sequence[Mapping[str, Any]],
    local_candidate: Sequence[Mapping[str, Any]],
    augmented_by_fit: Mapping[str, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    evaluations = list(val) + list(local_gt) + list(local_candidate)
    checks = {}
    for field in ("scene_id", "source_family", "source_sha256", "roi_pixel_sha256"):
        overlap = intersection((row[field] for row in train), (row[field] for row in evaluations))
        checks[f"train_evaluation_{field}_overlap"] = overlap
        if overlap:
            raise ValueError(f"train/evaluation {field} leakage: {overlap[:3]}")
    eval_hashes = {row["roi_pixel_sha256"] for row in evaluations}
    augmented_overlap = {}
    pixel_label: dict[str, set[str]] = defaultdict(set)
    for fit, rows in augmented_by_fit.items():
        overlap = sorted({row["roi_pixel_sha256"] for row in rows} & eval_hashes)
        augmented_overlap[fit] = overlap
        if overlap:
            raise ValueError(f"augmented train/evaluation pixel leakage in {fit}")
        for row in rows:
            pixel_label[row["roi_pixel_sha256"]].add(row["truth"])
    conflicts = sorted(key for key, labels in pixel_label.items() if len(labels) > 1)
    if conflicts:
        raise ValueError(f"augmented pixels have conflicting labels: {conflicts[:3]}")
    return {
        **checks,
        "augmented_train_evaluation_roi_pixel_overlap": augmented_overlap,
        "augmented_cross_class_pixel_conflicts": conflicts,
        "passed": True,
    }


def signed_bits_for_range(minimum: int, maximum: int) -> int:
    if minimum > maximum:
        raise ValueError("invalid signed range")
    bits = 1
    while minimum < -(1 << (bits - 1)) or maximum > (1 << (bits - 1)) - 1:
        bits += 1
    return bits


def quantization_ranges(contract: Mapping[str, Any]) -> dict[str, Any]:
    weights = np.asarray(contract["weight_q"], dtype=np.int64)
    bias = int(contract["bias_q"])
    bias_bits = signed_bits_for_range(bias, bias)

    def actual_weight_bound(feature_max: int) -> dict[str, Any]:
        lows = np.minimum(0, feature_max * weights)
        highs = np.maximum(0, feature_max * weights)
        prefix_low = bias + np.cumsum(lows, dtype=np.int64)
        prefix_high = bias + np.cumsum(highs, dtype=np.int64)
        minimum = min(bias, int(prefix_low.min()))
        maximum = max(bias, int(prefix_high.max()))
        return {
            "feature_q_range": [0, feature_max],
            "weight_q_source": "actual exported signed16 weights",
            "bias_q": bias,
            "all_partial_accumulator_range_including_bias": [minimum, maximum],
            "required_signed_bits": signed_bits_for_range(minimum, maximum),
        }

    def full_storage_bound(feature_max: int) -> dict[str, Any]:
        weight_min, weight_max = -(1 << 15), (1 << 15) - 1
        product_min, product_max = feature_max * weight_min, feature_max * weight_max
        bias_min, bias_max = -(1 << (bias_bits - 1)), (1 << (bias_bits - 1)) - 1
        minimum = bias_min + len(weights) * product_min
        maximum = bias_max + len(weights) * product_max
        return {
            "feature_q_range": [0, feature_max],
            "weight_q_full_storage_range": [weight_min, weight_max],
            "bias_storage_bits_signed": bias_bits,
            "bias_full_storage_range": [bias_min, bias_max],
            "single_product_full_storage_range": [product_min, product_max],
            "all_partial_accumulator_full_storage_range_including_bias": [minimum, maximum],
            "required_signed_bits": signed_bits_for_range(minimum, maximum),
        }

    return {
        "legal_hog_descriptor_bound_actual_model": actual_weight_bound(1 << 12),
        "legal_hog_descriptor_bound_full_weight_storage": full_storage_bound(1 << 12),
        "full_13bit_feature_port_and_full_weight_storage": full_storage_bound((1 << 13) - 1),
        "note": "legal HOG semantics cap feature_q at 4096; 8191 is only the 13-bit port full-storage stress bound",
    }


def transition(old_prediction: str | None, new_prediction: str | None, truth: str) -> str:
    old_correct = old_prediction == truth
    new_correct = new_prediction == truth
    if old_correct and not new_correct:
        return "lost"
    if not old_correct and new_correct:
        return "gained"
    return "same_correct" if old_correct else "same_wrong"


def grouped_metrics(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    def add(scope: str, selected: list[dict[str, Any]], groups: Sequence[str], end_to_end: bool = False) -> None:
        definitions: list[tuple[str, str, list[dict[str, Any]]]] = [("overall", "all", selected)]
        for field in groups:
            for value in sorted({str(row[field]) for row in selected if row.get(field) != ""}):
                definitions.append((field, value, [row for row in selected if str(row[field]) == value]))
        if "scene_id" in groups:
            for scene in sorted({row["scene_id"] for row in selected}):
                for label in LABEL_TO_ID:
                    definitions.append(("scene_class", f"{scene}|{label}", [
                        row for row in selected if row["scene_id"] == scene and row["truth"] == label
                    ]))
        for group_type, group_value, subset in definitions:
            if not subset:
                continue
            record: dict[str, Any] = {
                "scope": scope,
                "group_type": group_type,
                "group_value": group_value,
                "denominator": len(subset),
                "metric": "valid_ROI_classification_accuracy" if not end_to_end else "sampled_target_end_to_end_recall",
                "invalid_FAR": None,
            }
            for mode in ("float", "quantized"):
                old_field = f"baseline_{mode}_prediction"
                new_field = f"new_{mode}_prediction"
                record[f"baseline_{mode}_correct"] = sum(row.get(old_field) == row["truth"] for row in subset)
                record[f"new_{mode}_correct"] = sum(row.get(new_field) == row["truth"] for row in subset)
                record[f"new_{mode}_available_predictions"] = sum(row.get(new_field) is not None for row in subset)
                record[f"new_{mode}_accuracy_or_recall"] = record[f"new_{mode}_correct"] / len(subset)
                record[f"paired_{mode}"] = dict(Counter(
                    transition(row.get(old_field), row.get(new_field), row["truth"])
                    for row in subset
                ))
            output.append(record)

    ordinary = [dict(row) for row in rows]
    add("official_val", [row for row in ordinary if row["dataset"] == "official_val"],
        ("scene_id", "truth"))
    add("local_gt_B", [row for row in ordinary if row["dataset"] == "local_gt_B"],
        ("truth", "track_id", "visibility"))
    add("local_matched_C", [row for row in ordinary if row["dataset"] == "local_matched_C"],
        ("truth", "track_id", "visibility"))

    candidates = {
        (row["frame_index"], row["track_id"]): row
        for row in ordinary if row["dataset"] == "local_matched_C"
    }
    end_to_end = []
    for gt in (row for row in ordinary if row["dataset"] == "local_gt_B"):
        candidate = candidates.get((gt["frame_index"], gt["track_id"]))
        row = dict(gt)
        for mode in ("float", "quantized"):
            row[f"baseline_{mode}_prediction"] = None if candidate is None else candidate[f"baseline_{mode}_prediction"]
            row[f"new_{mode}_prediction"] = None if candidate is None else candidate[f"new_{mode}_prediction"]
        end_to_end.append(row)
    add("local_end_to_end_all57", end_to_end, ("truth", "track_id", "visibility"), True)
    return output


def quantization_scope_gate(
    rows: Sequence[Mapping[str, Any]], score_lsb: float
) -> dict[str, Any]:
    if not rows:
        raise ValueError("quantization gate scope is empty")
    mismatch_rows = [
        row for row in rows
        if row["new_float_prediction"] != row["new_quantized_prediction"]
    ]
    max_error = max(float(row["abs_float_quantized_error"]) for row in rows)
    margin_limit = max_error + score_lsb
    margin_violations = [
        row["sample_key"] for row in mismatch_rows
        if float(row["abs_float_margin"]) > margin_limit
    ]
    recall_losses = {}
    for label in LABEL_TO_ID:
        selected = [row for row in rows if row["truth"] == label]
        if not selected:
            continue
        float_recall = sum(row["new_float_prediction"] == label for row in selected) / len(selected)
        quant_recall = sum(row["new_quantized_prediction"] == label for row in selected) / len(selected)
        recall_losses[label] = {
            "support": len(selected),
            "float_recall": float_recall,
            "quantized_recall": quant_recall,
            "loss_percentage_points": 100.0 * max(0.0, float_recall - quant_recall),
        }
    return {
        "sample_count": len(rows),
        "float_quantized_label_mismatch": len(mismatch_rows),
        "mismatch_rate": len(mismatch_rows) / len(rows),
        "mismatch_rate_le_1_percent": len(mismatch_rows) / len(rows) <= 0.01,
        "per_class_recall": recall_losses,
        "per_class_recall_loss_le_1_percentage_point": all(
            item["loss_percentage_points"] <= 1.0 for item in recall_losses.values()
        ),
        "max_observed_abs_normalized_score_error": max_error,
        "normalized_score_lsb": score_lsb,
        "sign_flip_margin_limit_max_error_plus_lsb": margin_limit,
        "sign_flip_margin_violation_sample_keys": margin_violations,
        "sign_flip_margin_condition_passed": not margin_violations,
        "each_margin_exceeds_own_error_diagnostic": all(
            row["float_margin_exceeds_own_quantization_error"] for row in rows
        ),
    }


def fit_gate(
    metrics: Sequence[Mapping[str, Any]],
    prediction_rows: Sequence[Mapping[str, Any]],
    score_lsb: float,
) -> dict[str, Any]:
    gate_rows = [
        row for row in metrics
        if (row["scope"] == "official_val" and row["group_type"] == "scene_class")
        or (row["scope"] in {"local_gt_B", "local_matched_C"} and row["group_type"] == "truth")
    ]
    result: dict[str, Any] = {"comparisons": gate_rows}
    for mode in ("float", "quantized"):
        nondecrease = all(row[f"new_{mode}_correct"] >= row[f"baseline_{mode}_correct"] for row in gate_rows)
        ped_improved = any(
            row["group_value"].endswith("ped")
            and row[f"new_{mode}_correct"] > row[f"baseline_{mode}_correct"]
            for row in gate_rows
        )
        result[f"{mode}_per_scope_class_nondecrease"] = nondecrease
        result[f"{mode}_ped_improved_somewhere"] = ped_improved

    result["quantization_by_evaluation_scope"] = {
        dataset: quantization_scope_gate(
            [row for row in prediction_rows if row["dataset"] == dataset], score_lsb
        )
        for dataset in ("official_val", "local_gt_B", "local_matched_C")
    }
    quantization_passed = all(
        scope["mismatch_rate_le_1_percent"]
        and scope["per_class_recall_loss_le_1_percentage_point"]
        and scope["sign_flip_margin_condition_passed"]
        for scope in result["quantization_by_evaluation_scope"].values()
    )
    result["quantization_conditions_passed_all_three_scopes"] = quantization_passed
    result["passed"] = (
        result["float_per_scope_class_nondecrease"]
        and result["float_ped_improved_somewhere"]
        and result["quantized_per_scope_class_nondecrease"]
        and result["quantized_ped_improved_somewhere"]
        and quantization_passed
    )
    return result


def score_samples(
    samples: Sequence[Mapping[str, Any]],
    features: np.ndarray,
    model: Mapping[str, Any],
    baseline_model: Mapping[str, Any],
    fit_name: str,
    output: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    q = quantization_contract(model)
    baseline_q = quantization_contract(baseline_model)
    products = np.empty((len(samples), 324), dtype=np.int64)
    accumulators = np.empty((len(samples), 324), dtype=np.int64)
    predictions = []
    observed_min = int(q["bias_q"])
    observed_max = int(q["bias_q"])
    for index, (sample, feature) in enumerate(zip(samples, features)):
        float_score = model_score(feature, model)
        score_q, q_score = quantized_score(feature, q)
        baseline_float_score = model_score(feature, baseline_model)
        baseline_score_q, baseline_q_score = quantized_score(feature, baseline_q)
        feature_q = np.rint(feature * q["feature_scale"]).astype(np.int64)
        product = feature_q * q["weight_q"]
        accumulator = int(q["bias_q"]) + np.cumsum(product, dtype=np.int64)
        if int(accumulator[-1]) != score_q:
            raise AssertionError("stepwise accumulator disagrees with quantized_score")
        products[index] = product
        accumulators[index] = accumulator
        observed_min = min(observed_min, int(product.min()), int(accumulator.min()))
        observed_max = max(observed_max, int(product.max()), int(accumulator.max()))
        float_prediction = "vehicle" if float_score >= 0 else "ped"
        q_prediction = "vehicle" if score_q >= 0 else "ped"
        baseline_float_prediction = "vehicle" if baseline_float_score >= 0 else "ped"
        baseline_q_prediction = "vehicle" if baseline_score_q >= 0 else "ped"
        error = abs(float_score - q_score)
        predictions.append({
            "fit": fit_name,
            **{key: sample.get(key, "") for key in (
                "sample_key", "dataset", "truth", "scene_id", "source_family",
                "source_sha256", "frame_index", "track_id", "visibility", "matched",
                "roi_pixel_sha256", "roi_path",
            )},
            "baseline_float_score": baseline_float_score,
            "baseline_float_prediction": baseline_float_prediction,
            "baseline_quantized_score_integer": baseline_score_q,
            "baseline_quantized_score_normalized": baseline_q_score,
            "baseline_quantized_prediction": baseline_q_prediction,
            "new_float_score": float_score,
            "new_float_prediction": float_prediction,
            "new_quantized_score_integer": score_q,
            "new_quantized_score_normalized": q_score,
            "new_quantized_prediction": q_prediction,
            "float_quantized_label_mismatch": float_prediction != q_prediction,
            "abs_float_quantized_error": error,
            "abs_float_margin": abs(float_score),
            "float_margin_exceeds_own_quantization_error": abs(float_score) > error,
            "paired_float_vs_frozen_baseline": transition(
                baseline_float_prediction, float_prediction, sample["truth"]
            ),
            "paired_quantized_vs_frozen_baseline": transition(
                baseline_q_prediction, q_prediction, sample["truth"]
            ),
        })
    trace_path = output / f"quantization_trace_{fit_name}.npz"
    np.savez_compressed(
        trace_path,
        sample_keys=np.asarray([row["sample_key"] for row in predictions]),
        product_q=products,
        accumulator_after_product_q=accumulators,
    )
    ranges = quantization_ranges(q)
    ranges["observed_all_products_and_bias_first_partial_accumulators"] = {
        "minimum": observed_min,
        "maximum": observed_max,
        "required_signed_bits": signed_bits_for_range(observed_min, observed_max),
    }
    ranges["trace"] = {
        "path": trace_path.name,
        "sample_order": "sample_keys array; same order as product_q and accumulator_after_product_q",
        "product_q_shape": list(products.shape),
        "accumulator_shape": list(accumulators.shape),
        "accumulator_definition": "bias_q + cumulative sum of product_q from feature index 0",
        "sha256": sha256(trace_path),
    }
    return predictions, ranges


def fit_model(features: np.ndarray, truth: np.ndarray, weights: np.ndarray) -> tuple[dict[str, Any], dict[str, Any]]:
    scaler = StandardScaler().fit(features, sample_weight=weights)
    classifier = LinearSVC(
        C=1.0,
        class_weight="balanced",
        random_state=20260927,
        max_iter=30000,
        tol=0.0001,
        dual="auto",
    ).fit(scaler.transform(features), truth, sample_weight=weights)
    if classifier.classes_.tolist() != [0, 1]:
        raise ValueError(f"unexpected classifier class order: {classifier.classes_.tolist()}")
    folded_weights = classifier.coef_[0] / scaler.scale_
    folded_bias = float(
        classifier.intercept_[0]
        - np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_)
    )
    model = {
        "status": "augmentation_pilot_not_frozen_not_rtl",
        "class_order": ["ped", "vehicle"],
        "decision_score_positive_class": "vehicle",
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "linear_svc_coef_on_scaled_features": classifier.coef_[0].tolist(),
        "linear_svc_intercept_on_scaled_features": float(classifier.intercept_[0]),
        "folded_weights_on_raw_features": folded_weights.tolist(),
        "folded_bias_on_raw_features": folded_bias,
    }
    return model, {
        "C": 1.0,
        "class_weight": "balanced",
        "random_state": 20260927,
        "max_iter": 30000,
        "tol": 0.0001,
        "dual": "auto",
        "n_iter": int(classifier.n_iter_),
        "classes": classifier.classes_.tolist(),
    }


def reused_source_hashes() -> dict[str, str]:
    paths = (
        EXTERNAL / "opencv_hog_diagnostic.py",
        EXTERNAL / "opencv_hog_candidate_diagnostic.py",
        PROJECT / "tools/local_fourgrid_diagnostic.py",
        PROJECT / "tools/local_paired_diagnostic.py",
        PROJECT / "tools/roi_dataset_tool.py",
    )
    return {path.relative_to(PROJECT).as_posix(): sha256(path) for path in paths}


def control_reproduction(
    predictions: Sequence[Mapping[str, Any]],
    control_model: Mapping[str, Any],
    baseline_model: Mapping[str, Any],
) -> dict[str, Any]:
    selected = [row for row in predictions if row["fit"] == "control_original"]
    by_dataset = {}
    for dataset in sorted({row["dataset"] for row in selected}):
        rows = [row for row in selected if row["dataset"] == dataset]
        by_dataset[dataset] = {
            "sample_count": len(rows),
            "float_prediction_mismatch": sum(
                row["baseline_float_prediction"] != row["new_float_prediction"] for row in rows
            ),
            "quantized_prediction_mismatch": sum(
                row["baseline_quantized_prediction"] != row["new_quantized_prediction"] for row in rows
            ),
            "max_abs_float_score_delta": max(
                abs(float(row["baseline_float_score"]) - float(row["new_float_score"]))
                for row in rows
            ),
            "max_abs_quantized_normalized_score_delta": max(
                abs(float(row["baseline_quantized_score_normalized"])
                    - float(row["new_quantized_score_normalized"]))
                for row in rows
            ),
        }
    baseline_weights = np.asarray(baseline_model["folded_weights_on_raw_features"])
    control_weights = np.asarray(control_model["folded_weights_on_raw_features"])
    baseline_q = quantization_contract(baseline_model)
    control_q = quantization_contract(control_model)
    deltas = {
        "max_abs_folded_weight_delta": float(np.max(np.abs(control_weights - baseline_weights))),
        "abs_folded_bias_delta": abs(
            float(control_model["folded_bias_on_raw_features"])
            - float(baseline_model["folded_bias_on_raw_features"])
        ),
        "max_abs_quantized_weight_integer_delta": int(np.max(np.abs(
            control_q["weight_q"] - baseline_q["weight_q"]
        ))),
        "abs_quantized_bias_integer_delta": abs(int(control_q["bias_q"]) - int(baseline_q["bias_q"])),
    }
    if any(item["float_prediction_mismatch"] or item["quantized_prediction_mismatch"]
           for item in by_dataset.values()):
        raise AssertionError("control_original predictions differ from frozen baseline")
    if max(item["max_abs_float_score_delta"] for item in by_dataset.values()) > 1e-9:
        raise AssertionError("control_original float score differs beyond 1e-9")
    if deltas["max_abs_folded_weight_delta"] > 1e-9 or deltas["abs_folded_bias_delta"] > 1e-9:
        raise AssertionError("control_original folded parameters differ beyond 1e-9")
    if deltas["max_abs_quantized_weight_integer_delta"] or deltas["abs_quantized_bias_integer_delta"]:
        raise AssertionError("control_original quantized parameters differ from frozen baseline")
    return {
        "assertion": "PASS",
        "float_tolerance": 1e-9,
        "by_dataset": by_dataset,
        "parameter_deltas": deltas,
    }


def compare_prior_run(output: Path) -> dict[str, Any]:
    if output == OUTPUT.resolve():
        return {"performed": False, "reason": "this is the prior output path"}
    required = ["model_parameters.json", "predictions.csv"] + [
        f"quantization_trace_{name}.npz"
        for name in ("control_original", "horizontal_mirror", "mirror_translate2")
    ]
    if not all((OUTPUT / name).is_file() for name in required):
        raise ValueError("prior augmentation_v1 artifacts are missing")
    model_equal = read_json(output / "model_parameters.json") == read_json(OUTPUT / "model_parameters.json")
    with (output / "predictions.csv").open(encoding="utf-8", newline="") as stream:
        current_predictions = list(csv.DictReader(stream))
    with (OUTPUT / "predictions.csv").open(encoding="utf-8", newline="") as stream:
        prior_predictions = list(csv.DictReader(stream))
    prediction_equal = current_predictions == prior_predictions
    traces = {}
    for fit_name in ("control_original", "horizontal_mirror", "mirror_translate2"):
        name = f"quantization_trace_{fit_name}.npz"
        with np.load(output / name) as current, np.load(OUTPUT / name) as prior:
            keys_equal = set(current.files) == set(prior.files)
            arrays_equal = keys_equal and all(
                np.array_equal(current[key], prior[key]) for key in current.files
            )
        traces[fit_name] = {
            "array_keys_equal": keys_equal,
            "all_array_values_equal": arrays_equal,
            "current_file_sha256": sha256(output / name),
            "prior_file_sha256": sha256(OUTPUT / name),
            "container_bytes_equal": sha256(output / name) == sha256(OUTPUT / name),
        }
    if not model_equal or not prediction_equal or not all(
        item["all_array_values_equal"] for item in traces.values()
    ):
        raise AssertionError("verified replay differs from prior fit artifacts")
    return {
        "performed": True,
        "status": "PASS",
        "prior_output": str(OUTPUT),
        "prior_receipt_note": "prior run retained unchanged; its report script hash was later overwritten by summary-only finalization",
        "model_parameters_json_values_equal": model_equal,
        "prediction_csv_rows_and_values_equal": prediction_equal,
        "quantization_trace_arrays": traces,
    }


def self_test() -> dict[str, Any]:
    ramp = np.arange(32 * 32, dtype=np.uint16).reshape(32, 32).astype(np.uint8)
    mirrored = augment_roi(ramp, True, 0, 0)
    assert np.array_equal(mirrored, ramp[:, ::-1])
    shifted_right = augment_roi(ramp, False, 2, 0)
    assert np.array_equal(shifted_right[:, 0], ramp[:, 0])
    assert np.array_equal(shifted_right[:, 1], ramp[:, 0])
    assert np.array_equal(shifted_right[:, 2:], ramp[:, :-2])
    shifted_up = augment_roi(ramp, False, 0, -2)
    assert np.array_equal(shifted_up[:-2], ramp[2:])
    assert np.array_equal(shifted_up[-2], ramp[-1])
    assert np.array_equal(shifted_up[-1], ramp[-1])
    originals = [
        {"sample_key": "a", "truth": "ped", "roi": ramp},
        {"sample_key": "b", "truth": "vehicle", "roi": ramp.T.copy()},
    ]
    rows, audit = augmentation_rows(originals, [(False, 0, 0), (True, 0, 0)])
    assert len(rows) == 4 and audit["class_total_sample_weight"] == {"ped": 1.0, "vehicle": 1.0}
    metric_rows = grouped_metrics([
        {"dataset": "official_val", "truth": "ped", "scene_id": "s", "track_id": "",
         "visibility": "", "frame_index": 0, "baseline_float_prediction": "vehicle",
         "new_float_prediction": "ped", "baseline_quantized_prediction": "vehicle",
         "new_quantized_prediction": "ped"},
    ])
    scene_class = next(row for row in metric_rows if row["group_type"] == "scene_class")
    assert scene_class["new_float_correct"] == 1
    contract = {"weight_q": np.asarray([2, -3]), "bias_q": 1}
    ranges = quantization_ranges(contract)
    assert ranges["legal_hog_descriptor_bound_actual_model"]["required_signed_bits"] > 1
    near = {
        "sample_key": "near", "truth": "ped", "new_float_prediction": "ped",
        "new_quantized_prediction": "vehicle", "abs_float_quantized_error": 0.002,
        "abs_float_margin": 0.0025, "float_margin_exceeds_own_quantization_error": False,
    }
    assert quantization_scope_gate([near], 0.001)["sign_flip_margin_condition_passed"]
    far = {**near, "sample_key": "far", "abs_float_margin": 0.01}
    assert not quantization_scope_gate([far], 0.001)["sign_flip_margin_condition_passed"]
    synthetic_x = np.asarray([
        [-2.0, -1.0, 0.0], [-1.0, -2.0, 0.5], [-1.5, -0.5, -0.5],
        [1.0, 2.0, 0.0], [2.0, 1.0, -0.5], [1.5, 0.5, 0.5],
    ])
    synthetic_y = np.asarray([0, 0, 0, 1, 1, 1])
    synthetic_model, synthetic_fit = fit_model(synthetic_x, synthetic_y, np.ones(6))
    mean = np.asarray(synthetic_model["scaler_mean"])
    scale = np.asarray(synthetic_model["scaler_scale"])
    coef = np.asarray(synthetic_model["linear_svc_coef_on_scaled_features"])
    scaled_score = ((synthetic_x - mean) / scale) @ coef + synthetic_model["linear_svc_intercept_on_scaled_features"]
    folded_score = synthetic_x @ np.asarray(synthetic_model["folded_weights_on_raw_features"]) + synthetic_model["folded_bias_on_raw_features"]
    assert synthetic_fit["classes"] == [0, 1]
    assert np.allclose(scaled_score, folded_score, rtol=0.0, atol=1e-12)
    return {
        "status": "PASS",
        "checks": ["mirror", "translate_border_replicate", "sample_weight", "scene_group",
                   "quantized_ranges", "synthetic_fit_and_folded_score"],
    }


def run(output: Path) -> dict[str, Any]:
    output = output.resolve()
    if output.exists():
        raise ValueError("output must be absent; this preregistered run is immutable")
    experiment = read_json(EXPERIMENT)
    if sha256(EXPERIMENT) != EXPERIMENT_SHA256:
        raise ValueError("registered experiment hash changed")
    if experiment.get("contract_id") != "hog324_train_augmentation_pilot_v1":
        raise ValueError("unexpected experiment contract")
    if list(experiment.get("fits", [])) != [
        "control_original", "horizontal_mirror", "mirror_translate2"
    ]:
        raise ValueError("experiment fits changed")
    if sha256(BASELINE / "model_parameters.json") != BASELINE_PARAMETER_SHA256:
        raise ValueError("frozen HOG324 baseline parameter hash changed")

    baseline_parameters, _, baseline_receipt = load_models(BASELINE)
    baseline_model = baseline_parameters["opencv_hog324"]
    if baseline_model["class_order"] != ["ped", "vehicle"]:
        raise ValueError("baseline class order changed")
    train, val, official_receipt = official_samples()
    local_gt, local_candidate, local_receipt = local_samples()
    hog = make_hog(9)
    if hog.getDescriptorSize() != 324:
        raise ValueError("HOG324 descriptor contract changed")

    augmented_by_fit = {}
    augmentation_audits = {}
    for fit_name in experiment["fits"]:
        augmented, audit = augmentation_rows(train, experiment["augmentations"][fit_name])
        augmented_by_fit[fit_name] = augmented
        augmentation_audits[fit_name] = audit
    leakage = leakage_audit(train, val, local_gt, local_candidate, augmented_by_fit)

    output.mkdir(parents=True)
    evaluation_samples = list(train) + list(val) + list(local_gt) + list(local_candidate)
    evaluation_features = hog_features(hog, evaluation_samples)
    all_predictions: list[dict[str, Any]] = []
    all_metrics: dict[str, Any] = {}
    models: dict[str, Any] = {}
    quantization: dict[str, Any] = {}
    fit_reports: dict[str, Any] = {}
    augmentation_manifest: list[dict[str, Any]] = []

    for fit_name in experiment["fits"]:
        augmented = augmented_by_fit[fit_name]
        for row in augmented:
            augmentation_manifest.append({
                key: row.get(key, "") for key in (
                    "sample_key", "truth", "scene_id", "source_family", "source_sha256",
                    "augmentation_index", "mirror", "dx", "dy", "sample_weight",
                    "roi_pixel_sha256", "duplicate_of_augmentation_index",
                )
            } | {"fit": fit_name})
        fit_features = hog_features(hog, augmented)
        truth = np.asarray([LABEL_TO_ID[row["truth"]] for row in augmented], dtype=np.int64)
        weights = np.asarray([row["sample_weight"] for row in augmented], dtype=np.float64)
        model, fit_parameters = fit_model(fit_features, truth, weights)
        q_contract = quantization_contract(model)
        models[fit_name] = {
            **model,
            "quantized_weight_q_signed16": q_contract["weight_q"].tolist(),
            "quantized_bias_q": int(q_contract["bias_q"]),
            "quantization_feature_scale": int(q_contract["feature_scale"]),
            "quantization_weight_scale": float(q_contract["weight_scale"]),
        }
        predictions, q_report = score_samples(
            evaluation_samples, evaluation_features, model, baseline_model, fit_name, output
        )
        metrics = grouped_metrics(predictions)
        gate = fit_gate(
            metrics,
            predictions,
            1.0 / (q_contract["feature_scale"] * q_contract["weight_scale"]),
        )
        control_mismatch = {
            dataset: {
                "sample_count": len(selected),
                "float_prediction_mismatch": sum(
                    row["baseline_float_prediction"] != row["new_float_prediction"] for row in selected
                ),
                "quantized_prediction_mismatch": sum(
                    row["baseline_quantized_prediction"] != row["new_quantized_prediction"] for row in selected
                ),
            }
            for dataset in sorted({row["dataset"] for row in predictions})
            for selected in [[row for row in predictions if row["dataset"] == dataset]]
        }
        all_predictions.extend(predictions)
        all_metrics[fit_name] = metrics
        quantization[fit_name] = q_report
        fit_reports[fit_name] = {
            "fit_parameters": fit_parameters,
            "augmentation": augmentation_audits[fit_name],
            "pilot_gate": gate,
            "frozen_baseline_prediction_comparison": control_mismatch,
        }

    reproduction = control_reproduction(
        all_predictions, models["control_original"], baseline_model
    )

    write_csv(output / "augmentation_manifest.csv", augmentation_manifest)
    write_csv(output / "predictions.csv", all_predictions)
    failures = [row for row in all_predictions if (
        row["new_float_prediction"] != row["truth"]
        or row["new_quantized_prediction"] != row["truth"]
    )]
    write_csv(output / "failures.csv", failures)
    dump_json(output / "model_parameters.json", models)
    dump_json(output / "metrics.json", all_metrics)
    dump_json(output / "quantization.json", quantization)
    prior_comparison = compare_prior_run(output)

    report = {
        "status": "completed_three_preregistered_fits_pilot_only_not_frozen_not_rtl",
        "experiment": {
            "path": str(EXPERIMENT),
            "sha256": sha256(EXPERIMENT),
            "contract_id": experiment["contract_id"],
            "fits_run_once": experiment["fits"],
            "extra_variants_or_parameter_sweep": False,
            "fit_execution_count_for_same_registered_three_variants": 2,
            "selection_used_only_same_three_registered_variants": True,
        },
        "verified_replay_against_prior_run": prior_comparison,
        "scope": {
            "training": "360 official annotated train ROIs only",
            "evaluation": "69 official val + local B57 GT + matched C14; local end-to-end denominator remains 57",
            "metric_definition": "accuracy/recall over valid ped/vehicle ROI; no invalid samples, so invalid FAR is null",
            "local_correlation": "57 observations are four correlated tracks, not 57 independent targets",
            "local_tracks": dict(sorted(Counter(row["track_id"] for row in local_gt).items())),
            "pilot_only": True,
            "model_freeze_or_deployment_permission": False,
        },
        "inputs": {
            "official": official_receipt,
            "local": local_receipt,
            "baseline": baseline_receipt,
            "baseline_parameter_sha256_expected": BASELINE_PARAMETER_SHA256,
            "pinned_input_hashes": {
                "experiment": EXPERIMENT_SHA256,
                "baseline_model_parameters": BASELINE_PARAMETER_SHA256,
                "fourgrid_receipt": FOURGRID_RECEIPT_SHA256,
                "fourgrid_rows": FOURGRID_ROWS_SHA256,
            },
        },
        "control_original_reproduction": reproduction,
        "data_isolation": leakage,
        "fit_reports": fit_reports,
        "artifacts": {
            "augmentation_manifest": "augmentation_manifest.csv",
            "predictions": "predictions.csv",
            "failures": "failures.csv",
            "model_parameters_and_quantized_weights": "model_parameters.json",
            "grouped_metrics": "metrics.json",
            "quantization_ranges_and_trace_index": "quantization.json",
            "quantization_traces": [f"quantization_trace_{name}.npz" for name in experiment["fits"]],
        },
        "implementation": {
            "script": str(SCRIPT),
            "script_sha256": sha256(SCRIPT),
            "python": platform.python_version(),
            "opencv": cv2.__version__,
            "numpy": np.__version__,
            "scikit_learn": sklearn.__version__,
            "reused_functions": [
                "opencv_hog_diagnostic.read_manifest/load_roi/make_hog(9)",
                "opencv_hog_candidate_diagnostic.load_models/model_score/quantization_contract/quantized_score",
                "local_fourgrid_diagnostic.validated_package/validate_confirmation_chain/roi_pair",
                "local_paired_diagnostic.validate_annotations",
            ],
            "reused_source_sha256": reused_source_hashes(),
        },
        "limitations": [
            "OpenCV HOG internals remain floating point and are not integer-HOG or RTL equivalence evidence.",
            "No invalid candidates are present, so FAR and rejection performance are unmeasured.",
            "This pilot does not read test/blind/holdout data and does not authorize model freeze or deployment.",
        ],
    }
    dump_json(output / "report.json", report)
    artifacts = {
        path.name: sha256(path)
        for path in sorted(output.iterdir()) if path.is_file()
    }
    dump_json(output / "artifact_hashes.json", artifacts)
    return {
        "output": str(output),
        "fits": {
            name: {
                "pilot_gate_passed": fit_reports[name]["pilot_gate"]["passed"],
                "augmentation_rows": augmentation_audits[name]["fit_row_count"],
            }
            for name in experiment["fits"]
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "self-test"))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    result = self_test() if args.mode == "self-test" else run(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
