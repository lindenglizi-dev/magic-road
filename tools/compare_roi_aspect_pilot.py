#!/usr/bin/env python3
"""Two-arm HOG324 pilot: direct stretch versus aspect-preserving letterbox.

The pilot is deliberately limited to the audited train/validation manifest.  It
reads each manifest-declared raw crop directly and never opens source video.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import cv2
import numpy as np
import PIL
from PIL import Image
import sklearn
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
LABEL_TO_ID = {"ped": 0, "vehicle": 1}
ID_TO_LABEL = {0: "ped", 1: "vehicle"}
EXPECTED_SCENES = {
    "train": {"virat-ground-000201", "virat-ground-000206"},
    "val": {"virat-ground-000200", "virat-ground-000203"},
}
EXPECTED_COUNTS = {"train": 360, "val": 69}
FORBIDDEN = re.compile(r"(^|[_\-.])(test|blind|holdout)($|[_\-.])", re.IGNORECASE)
SEED = 20260927
FILL_VALUE = 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def assert_no_sealed_token(path: Path, role: str) -> None:
    for part in path.parts:
        if FORBIDDEN.search(part):
            raise ValueError(f"sealed-data guard rejected {role} path component: {part}")


def resolve_beneath(root: Path, relative: str, role: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute():
        raise ValueError(f"{role} must be relative: {relative}")
    assert_no_sealed_token(candidate, role)
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"{role} escapes dataset root: {relative}")
    return resolved


def read_and_validate_manifest(dataset: Path) -> list[dict[str, str]]:
    """Validate every split/provenance/path declaration before opening any crop."""
    assert_no_sealed_token(dataset, "dataset")
    manifest = dataset / "manifest.csv"
    if not manifest.is_file():
        raise ValueError(f"missing manifest: {manifest}")
    with manifest.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    required = {
        "sample_id", "split", "label", "class_id", "frame_index", "xmin", "ymin",
        "xmax", "ymax", "crop_path", "roi_path", "roi_sha256", "scene_id",
        "source_sha256", "source_family", "roi_source", "reviewer",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"manifest missing fields: {sorted(required - set(rows[0] if rows else []))}")

    ids: set[str] = set()
    actual_scenes: dict[str, set[str]] = {"train": set(), "val": set()}
    counts: Counter[str] = Counter()
    for row in rows:
        split = row["split"].strip().lower()
        scene = row["scene_id"].strip()
        if split not in EXPECTED_SCENES:
            raise ValueError(f"sealed-data guard rejected split={split!r}")
        if scene not in EXPECTED_SCENES[split]:
            raise ValueError(f"scene is not allowlisted for {split}: {scene!r}")
        if row["label"] not in LABEL_TO_ID or row["class_id"] != str(LABEL_TO_ID[row["label"]]):
            raise ValueError(f"invalid label/class_id: {row['sample_id']}")
        if row["roi_source"] != "annotated" or not row["reviewer"].startswith("official_annotation:"):
            raise ValueError(f"sample is not official audited GT: {row['sample_id']}")
        if row["sample_id"] in ids:
            raise ValueError(f"duplicate sample_id: {row['sample_id']}")
        ids.add(row["sample_id"])
        counts[split] += 1
        actual_scenes[split].add(scene)
        crop_rel = Path(row["crop_path"])
        if len(crop_rel.parts) < 4 or crop_rel.parts[:3] != ("raw_crops", split, row["label"]):
            raise ValueError(f"crop path does not match split/label: {row['crop_path']}")
        roi_rel = Path(row["roi_path"])
        if len(roi_rel.parts) < 3 or roi_rel.parts[:2] != (split, row["label"]):
            raise ValueError(f"ROI path does not match split/label: {row['roi_path']}")
        resolve_beneath(dataset, row["crop_path"], "raw crop")
        resolve_beneath(dataset, row["roi_path"], "stored ROI")
        if int(row["xmin"]) > int(row["xmax"]) or int(row["ymin"]) > int(row["ymax"]):
            raise ValueError(f"invalid inclusive box: {row['sample_id']}")
    if dict(counts) != EXPECTED_COUNTS:
        raise ValueError(f"unexpected split counts: {dict(counts)}")
    if actual_scenes != EXPECTED_SCENES:
        raise ValueError(f"unexpected scene coverage: {actual_scenes}")
    return rows


def cross_split_values(rows: list[dict[str, str]], field: str) -> list[str]:
    membership: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        membership[row[field]].add(row["split"])
    return sorted(value for value, splits in membership.items() if len(splits) > 1)


def fpga_stretch_32(crop: np.ndarray) -> np.ndarray:
    """Existing Q8 pixel-centre nearest-neighbour mapping to 32x32."""
    height, width = crop.shape
    positions = np.arange(32, dtype=np.int64)
    xs = np.minimum((width * (4 + 8 * positions)) >> 8, width - 1)
    ys = np.minimum((height * (4 + 8 * positions)) >> 8, height - 1)
    return crop[np.ix_(ys, xs)]


def aspect_letterbox_32(crop: np.ndarray, fill: int = FILL_VALUE) -> tuple[np.ndarray, dict[str, int]]:
    """Fit crop in 32x32, NN sample at pixel centres, and center-pad.

    The longer side is exactly 32.  The shorter output dimension is
    round-half-up(shorter*32/longer), clamped to [1, 32].  For an output index
    i of length D, source index is floor(source_length*(2*i+1)/(2*D)).
    Odd padding puts the extra pixel on the right or bottom.
    """
    height, width = crop.shape
    if width < 1 or height < 1:
        raise ValueError("empty raw crop")
    longest = max(width, height)
    target_w = max(1, min(32, (width * 32 + longest // 2) // longest))
    target_h = max(1, min(32, (height * 32 + longest // 2) // longest))
    xs = np.minimum((width * (2 * np.arange(target_w, dtype=np.int64) + 1)) //
                    (2 * target_w), width - 1)
    ys = np.minimum((height * (2 * np.arange(target_h, dtype=np.int64) + 1)) //
                    (2 * target_h), height - 1)
    resized = crop[np.ix_(ys, xs)]
    left = (32 - target_w) // 2
    top = (32 - target_h) // 2
    output = np.full((32, 32), fill, dtype=np.uint8)
    output[top:top + target_h, left:left + target_w] = resized
    return output, {
        "target_width": target_w, "target_height": target_h,
        "pad_left": left, "pad_right": 32 - target_w - left,
        "pad_top": top, "pad_bottom": 32 - target_h - top,
    }


def make_hog324() -> cv2.HOGDescriptor:
    return cv2.HOGDescriptor(
        (32, 32), (16, 16), (8, 8), (8, 8), 9,
        1, 4.0, cv2.HOGDescriptor_L2Hys, 0.2, False, 64, False,
    )


def height(row: dict[str, str]) -> int:
    return int(row["ymax"]) - int(row["ymin"]) + 1


def height_band(value: int) -> str:
    if value <= 5:
        return "h01_05"
    if value <= 10:
        return "h06_10"
    if value <= 20:
        return "h11_20"
    return "h21_plus"


def aspect_band(row: dict[str, str]) -> str:
    width = int(row["xmax"]) - int(row["xmin"]) + 1
    ratio = width / height(row)
    if ratio < 0.5:
        return "portrait_lt_0p5"
    if ratio < 1.0:
        return "portrait_0p5_1"
    if ratio <= 2.0:
        return "landscape_1_2"
    return "landscape_gt_2"


def balanced_accuracy_present(y_true: np.ndarray, prediction: np.ndarray) -> float:
    matrix = confusion_matrix(y_true, prediction, labels=[0, 1])
    support = matrix.sum(axis=1)
    return float(np.mean([matrix[i, i] / support[i] for i in range(2) if support[i]]))


def flat_metrics(model: str, split: str, group_type: str, group_value: str,
                 y_true: np.ndarray, prediction: np.ndarray) -> dict[str, Any]:
    matrix = confusion_matrix(y_true, prediction, labels=[0, 1])
    report = classification_report(y_true, prediction, labels=[0, 1],
                                   target_names=["ped", "vehicle"],
                                   output_dict=True, zero_division=0)
    return {
        "model": model, "split": split, "group_type": group_type,
        "group_value": group_value, "sample_count": int(y_true.size),
        "accuracy": float(accuracy_score(y_true, prediction)),
        "balanced_accuracy": balanced_accuracy_present(y_true, prediction),
        "ped_support": int(report["ped"]["support"]),
        "ped_precision": float(report["ped"]["precision"]),
        "ped_recall": float(report["ped"]["recall"]),
        "vehicle_support": int(report["vehicle"]["support"]),
        "vehicle_precision": float(report["vehicle"]["precision"]),
        "vehicle_recall": float(report["vehicle"]["recall"]),
        "cm_ped_as_ped": int(matrix[0, 0]),
        "cm_ped_as_vehicle": int(matrix[0, 1]),
        "cm_vehicle_as_ped": int(matrix[1, 0]),
        "cm_vehicle_as_vehicle": int(matrix[1, 1]),
    }


def grouped_metrics(model: str, rows: list[dict[str, str]], truth: np.ndarray,
                    prediction: np.ndarray) -> list[dict[str, Any]]:
    output = [flat_metrics(model, "val", "overall", "all", truth, prediction)]
    groups = {
        "scene": [row["scene_id"] for row in rows],
        "height": [height_band(height(row)) for row in rows],
        "aspect": [aspect_band(row) for row in rows],
        "scene_height": [f"{row['scene_id']}|{height_band(height(row))}" for row in rows],
    }
    for group_type, values in groups.items():
        for value in sorted(set(values)):
            indices = np.asarray([i for i, candidate in enumerate(values) if candidate == value])
            output.append(flat_metrics(model, "val", group_type, value,
                                       truth[indices], prediction[indices]))
    return output


def signed_bits(max_abs: int) -> int:
    return 2 if max_abs == 0 else int(max_abs).bit_length() + 1


def quantize_model(features: dict[str, np.ndarray], scaler: StandardScaler,
                   classifier: LinearSVC, float_predictions: dict[str, np.ndarray],
                   float_scores: dict[str, np.ndarray], truth: dict[str, np.ndarray]) -> tuple[dict[str, Any], dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any]]:
    folded_weights = classifier.coef_[0] / scaler.scale_
    folded_bias = float(classifier.intercept_[0] -
                        np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_))
    feature_scale = 1 << 12
    weight_scale = ((1 << 15) - 1) / float(np.max(np.abs(folded_weights)))
    q_weights = np.rint(folded_weights * weight_scale).astype(np.int64)
    q_bias = int(round(folded_bias * feature_scale * weight_scale))
    q_predictions: dict[str, np.ndarray] = {}
    q_scores: dict[str, np.ndarray] = {}
    split_report: dict[str, Any] = {}
    observed = 0
    for split in ("train", "val"):
        q_features = np.rint(features[split] * feature_scale).astype(np.int64)
        integer_scores = q_features @ q_weights + q_bias
        normalized_scores = integer_scores.astype(np.float64) / (feature_scale * weight_scale)
        q_prediction = (integer_scores >= 0).astype(np.int64)
        q_predictions[split], q_scores[split] = q_prediction, integer_scores
        observed = max(observed, int(np.max(np.abs(integer_scores))))
        by_truth = {}
        for class_id, label in ID_TO_LABEL.items():
            selected = truth[split] == class_id
            by_truth[label] = {
                "support": int(np.sum(selected)),
                "classification_mismatch_vs_float": int(np.sum(
                    q_prediction[selected] != float_predictions[split][selected])),
            }
        delta = normalized_scores - float_scores[split]
        split_report[split] = {
            "classification_mismatch_vs_float": int(np.sum(q_prediction != float_predictions[split])),
            "classification_mismatch_vs_float_by_true_class": by_truth,
            "float_to_quantized_prediction_confusion_ped_vehicle": confusion_matrix(
                float_predictions[split], q_prediction, labels=[0, 1]).tolist(),
            "max_abs_score_error": float(np.max(np.abs(delta))),
            "mean_abs_score_error": float(np.mean(np.abs(delta))),
            "float_score_range": [float(np.min(float_scores[split])), float(np.max(float_scores[split]))],
            "quantized_integer_score_range": [int(np.min(integer_scores)), int(np.max(integer_scores))],
        }
    worst = int(abs(q_bias) + ((1 << 13) - 1) * np.sum(np.abs(q_weights), dtype=np.int64))
    quant_report = {
        "status": "diagnostic_descriptor_output_and_linear_model_quantization_not_rtl_equivalence",
        "feature_format": {"unsigned_bits": 13, "fraction_bits": 12, "scale": feature_scale,
                           "rounding": "numpy.rint round-to-nearest-even", "saturation": "none"},
        "weight_format": {"signed_bits": 16, "scale": weight_scale,
                          "rounding": "numpy.rint round-to-nearest-even"},
        "quantized_bias": q_bias,
        "worst_case_accumulator_abs_bound": worst,
        "worst_case_required_signed_bits": signed_bits(worst),
        "observed_max_abs_accumulator": observed,
        "observed_required_signed_bits": signed_bits(observed),
        "splits": split_report,
        "limitation": "OpenCV HOG remains floating point; this quantizes its 324 outputs and folded SVM only.",
    }
    model = {
        "class_order": ["ped", "vehicle"], "decision_positive_class": "vehicle",
        "scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist(),
        "linear_svc_coef_scaled": classifier.coef_[0].tolist(),
        "linear_svc_intercept_scaled": float(classifier.intercept_[0]),
        "folded_weights": folded_weights.tolist(), "folded_bias": folded_bias,
        "quantized_weights": q_weights.tolist(), "quantized_bias": q_bias,
        "feature_scale": feature_scale, "weight_scale": weight_scale,
    }
    return model, q_predictions, q_scores, quant_report


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    if fields is None:
        if not rows:
            raise ValueError(f"fields required for empty CSV: {path}")
        fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(dataset: Path, output: Path) -> dict[str, Any]:
    dataset, output = dataset.resolve(), output.resolve()
    assert_no_sealed_token(output, "output")
    rows = read_and_validate_manifest(dataset)

    # Provenance leakage is checked entirely from validated manifest metadata,
    # before any declared crop path is opened.
    manifest_leakage = {
        field: cross_split_values(rows, field)
        for field in ("scene_id", "source_sha256", "source_family")
    }
    if any(manifest_leakage.values()):
        raise ValueError(f"cross-split provenance leakage: {manifest_leakage}")

    crops: dict[str, np.ndarray] = {}
    prepared: dict[str, dict[str, np.ndarray]] = {"fpga_stretch": {}, "aspect_letterbox": {}}
    input_receipt: list[dict[str, Any]] = []
    raw_hash_splits: dict[str, set[str]] = defaultdict(set)
    prepared_hash_splits: dict[str, dict[str, set[str]]] = {
        name: defaultdict(set) for name in prepared
    }
    stretch_contract_mismatches: list[str] = []
    missing_crops: list[str] = []
    for row in rows:
        crop_path = resolve_beneath(dataset, row["crop_path"], "raw crop")
        if not crop_path.is_file():
            missing_crops.append(row["sample_id"])
            continue
        with Image.open(crop_path) as image:
            crop = np.asarray(image.convert("L"), dtype=np.uint8)
        expected_shape = (height(row), int(row["xmax"]) - int(row["xmin"]) + 1)
        if crop.shape != expected_shape:
            raise ValueError(f"raw crop shape mismatch {row['sample_id']}: {crop.shape} != {expected_shape}")
        crops[row["sample_id"]] = crop
        raw_hash = hashlib.sha256(crop.tobytes()).hexdigest()
        stretch = fpga_stretch_32(crop)
        letterbox, geometry = aspect_letterbox_32(crop)
        stretch_hash = hashlib.sha256(stretch.tobytes()).hexdigest()
        letterbox_hash = hashlib.sha256(letterbox.tobytes()).hexdigest()
        if stretch_hash != row["roi_sha256"]:
            stretch_contract_mismatches.append(row["sample_id"])
        prepared["fpga_stretch"][row["sample_id"]] = stretch
        prepared["aspect_letterbox"][row["sample_id"]] = letterbox
        raw_hash_splits[raw_hash].add(row["split"])
        prepared_hash_splits["fpga_stretch"][stretch_hash].add(row["split"])
        prepared_hash_splits["aspect_letterbox"][letterbox_hash].add(row["split"])
        input_receipt.append({
            "sample_id": row["sample_id"], "split": row["split"], "label": row["label"],
            "scene_id": row["scene_id"], "crop_path": row["crop_path"],
            "crop_png_sha256": sha256_file(crop_path), "raw_crop_pixel_sha256": raw_hash,
            "fpga_stretch_pixel_sha256": stretch_hash,
            "aspect_letterbox_pixel_sha256": letterbox_hash, **geometry,
        })
    if missing_crops:
        raise ValueError(f"missing raw crops ({len(missing_crops)}): {missing_crops[:20]}")
    if stretch_contract_mismatches:
        raise ValueError(f"generated stretch does not match audited ROI ({len(stretch_contract_mismatches)}): "
                         f"{stretch_contract_mismatches[:20]}")
    pixel_leakage = {
        "raw_crop_pixel_sha256": sorted(key for key, splits in raw_hash_splits.items() if len(splits) > 1),
        **{f"{name}_pixel_sha256": sorted(key for key, splits in hashes.items() if len(splits) > 1)
           for name, hashes in prepared_hash_splits.items()},
    }
    if any(pixel_leakage.values()):
        raise ValueError(f"cross-split pixel leakage: {pixel_leakage}")

    split_rows = {split: [row for row in rows if row["split"] == split]
                  for split in ("train", "val")}
    truth = {split: np.asarray([LABEL_TO_ID[row["label"]] for row in selected], dtype=np.int64)
             for split, selected in split_rows.items()}
    hog = make_hog324()
    output.mkdir(parents=True, exist_ok=False)
    predictions_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    metrics_rows: list[dict[str, Any]] = []
    range_rows: list[dict[str, Any]] = []
    models: dict[str, Any] = {}
    model_reports: dict[str, Any] = {}

    for model_name in ("fpga_stretch", "aspect_letterbox"):
        features = {
            split: np.vstack([
                hog.compute(np.ascontiguousarray(prepared[model_name][row["sample_id"]]),
                            winStride=(0, 0), padding=(0, 0)).reshape(-1).astype(np.float64)
                for row in selected
            ]) for split, selected in split_rows.items()
        }
        scaler = StandardScaler().fit(features["train"])
        classifier = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED,
                               max_iter=30000).fit(scaler.transform(features["train"]), truth["train"])
        float_predictions, float_scores = {}, {}
        for split in ("train", "val"):
            transformed = scaler.transform(features[split])
            float_predictions[split] = classifier.predict(transformed)
            float_scores[split] = classifier.decision_function(transformed)
        model, q_predictions, q_scores, quant_report = quantize_model(
            features, scaler, classifier, float_predictions, float_scores, truth)
        models[model_name] = model

        split_metrics = {}
        for split in ("train", "val"):
            split_metrics[split] = {
                "float": flat_metrics(model_name, split, "overall", "all", truth[split],
                                      float_predictions[split]),
                "quantized": flat_metrics(model_name + "_q", split, "overall", "all", truth[split],
                                          q_predictions[split]),
            }
            for index, row in enumerate(split_rows[split]):
                record = {
                    "model": model_name, "split": split, "sample_id": row["sample_id"],
                    "scene_id": row["scene_id"], "frame_index": row["frame_index"],
                    "bbox_width": int(row["xmax"]) - int(row["xmin"]) + 1,
                    "bbox_height": height(row), "height_band": height_band(height(row)),
                    "aspect_band": aspect_band(row), "truth": row["label"],
                    "float_prediction": ID_TO_LABEL[int(float_predictions[split][index])],
                    "quantized_prediction": ID_TO_LABEL[int(q_predictions[split][index])],
                    "float_score_vehicle_positive": float(float_scores[split][index]),
                    "quantized_integer_score_vehicle_positive": int(q_scores[split][index]),
                    "crop_path": row["crop_path"],
                }
                predictions_rows.append(record)
                reasons = []
                if float_predictions[split][index] != truth[split][index]:
                    reasons.append("float_misclassified")
                if q_predictions[split][index] != truth[split][index]:
                    reasons.append("quantized_misclassified")
                if q_predictions[split][index] != float_predictions[split][index]:
                    reasons.append("float_quantized_category_disagreement")
                if reasons:
                    failure_rows.append({**record, "reason": ";".join(reasons)})

        metrics_rows.extend(grouped_metrics(model_name, split_rows["val"], truth["val"],
                                            float_predictions["val"]))
        metrics_rows.extend(grouped_metrics(model_name + "_q", split_rows["val"], truth["val"],
                                            q_predictions["val"]))
        for feature_index in range(324):
            range_rows.append({
                "model": model_name, "feature_index": feature_index,
                "train_min": float(np.min(features["train"][:, feature_index])),
                "train_max": float(np.max(features["train"][:, feature_index])),
                "train_mean": float(np.mean(features["train"][:, feature_index])),
                "val_min": float(np.min(features["val"][:, feature_index])),
                "val_max": float(np.max(features["val"][:, feature_index])),
                "val_mean": float(np.mean(features["val"][:, feature_index])),
            })
        model_reports[model_name] = {
            "feature_dimension": 324,
            "linear_svc": {"C": 1.0, "class_weight": "balanced", "random_state": SEED,
                           "max_iter": 30000, "n_iter": int(classifier.n_iter_)},
            "metrics": split_metrics, "fixed_point_feasibility": quant_report,
            "descriptor_ranges": {
                split: {"min": float(np.min(values)), "max": float(np.max(values)),
                        "mean": float(np.mean(values)), "std": float(np.std(values)),
                        "zero_fraction": float(np.mean(values == 0))}
                for split, values in features.items()
            },
        }

    prediction_fields = list(predictions_rows[0])
    write_csv(output / "predictions.csv", predictions_rows, prediction_fields)
    write_csv(output / "failures.csv", failure_rows, prediction_fields + ["reason"])
    write_csv(output / "stratified_metrics.csv", metrics_rows)
    write_csv(output / "feature_ranges.csv", range_rows)
    (output / "models.json").write_text(json.dumps(models, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8")
    receipt = {
        "status": "all_inputs_verified",
        "manifest_sha256": sha256_file(dataset / "manifest.csv"),
        "selected_input_count": len(input_receipt),
        "selected_inputs_canonical_sha256": canonical_sha256(input_receipt),
        "cross_split_leakage": {**manifest_leakage, **pixel_leakage},
        "stretch_regeneration_matches_all_manifest_roi_sha256": True,
        "missing_raw_crops": [], "input_records": input_receipt,
    }
    (output / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    report = {
        "status": "python_only_roi_preprocessing_pilot_not_production_not_rtl_not_acceptance",
        "scope": {
            "dataset": str(dataset), "splits_read": ["train", "val"],
            "source_access": "manifest.csv and manifest-declared crop_path only; source_video not opened",
            "labels": "official annotation GT ped/vehicle only",
            "hyperparameter_tuning": False, "models_fit": 2,
            "test_blind_holdout": "rejected by fail-closed path and manifest guards",
        },
        "sample_counts": {
            split: {"total": len(selected),
                    "by_label": dict(sorted(Counter(row["label"] for row in selected).items())),
                    "by_scene": dict(sorted(Counter(row["scene_id"] for row in selected).items()))}
            for split, selected in split_rows.items()
        },
        "scene_split_contract": {split: sorted(scenes) for split, scenes in EXPECTED_SCENES.items()},
        "preprocessing_contracts": {
            "fpga_stretch": {
                "input": "manifest crop_path uint8 grayscale inclusive annotation crop",
                "output": "32x32 uint8", "mapping": "src=floor(length*(i+0.5)/32), capped length-1; existing Q8 DDA expression (length*(4+8*i))>>8",
                "padding": "none", "training_validation_identical": True,
            },
            "aspect_letterbox": {
                "input": "same manifest crop_path as fpga_stretch", "output": "32x32 uint8",
                "scale": "long side=32; short side=round-half-up(short*32/long), clamped [1,32]",
                "nearest_neighbor_mapping": "for output i of target length D: src=floor(source_length*(2*i+1)/(2*D)), capped source_length-1",
                "centering": "floor(left/top padding); any odd extra pad pixel goes right/bottom",
                "boundary_fill_value_uint8": FILL_VALUE, "training_validation_identical": True,
            },
            "hog324": {"win_size": [32, 32], "block_size": [16, 16],
                       "block_stride": [8, 8], "cell_size": [8, 8], "nbins": 9,
                       "signed_gradient": False, "gamma_correction": False,
                       "descriptor_size": 324},
            "classifier": "StandardScaler fit on train only then fixed LinearSVC C=1 class_weight=balanced; scaler folded in exported model",
        },
        "models": model_reports,
        "inputs": {key: value for key, value in receipt.items() if key != "input_records"},
        "implementation": {"script": str(SCRIPT_PATH), "script_sha256": sha256_file(SCRIPT_PATH),
                           "python": platform.python_version(), "opencv": cv2.__version__,
                           "numpy": np.__version__, "pillow": PIL.__version__,
                           "scikit_learn": sklearn.__version__},
        "artifacts": {"receipt": "receipt.json", "models": "models.json",
                      "predictions": "predictions.csv", "failures": "failures.csv",
                      "stratified_metrics": "stratified_metrics.csv",
                      "feature_ranges": "feature_ranges.csv"},
        "limitations": [
            "This creates a new preprocessing contract for a Python pilot and does not replace the existing ROI contract.",
            "No RTL, source video, invalid-candidate rejection, test, blind, or holdout evidence is included.",
            "Only 429 samples from four VIRAT scenes are measured; validation remains diagnostic, not acceptance evidence.",
            "OpenCV HOG is floating point and its quantized-output/SVM feasibility result is not RTL equivalence.",
        ],
    }
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8")
    hashes = {path.name: sha256_file(path) for path in sorted(output.iterdir())
              if path.is_file() and path.name != "artifact_hashes.json"}
    (output / "artifact_hashes.json").write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=PROJECT_ROOT / "road_roi_dataset_virat")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "evaluation" / "roi_aspect_pilot_v1")
    args = parser.parse_args()
    report = run(args.dataset, args.output)
    summary = {
        "status": report["status"],
        "sample_counts": report["sample_counts"],
        "validation": {
            name: {kind: metrics["accuracy"]
                   for kind, metrics in values["metrics"]["val"].items()}
            for name, values in report["models"].items()
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
