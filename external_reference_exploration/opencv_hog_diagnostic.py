#!/usr/bin/env python3
"""Sealed train/validation diagnostic for OpenCV HOG and the current RTL HOG.

This is an external-reference experiment.  It does not create RTL, tune C, or
read test/blind/holdout samples.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import cv2
import numpy as np
import PIL
from PIL import Image
import sklearn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
TOOLS_DIR = PROJECT_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from hog_reference import extract_features  # noqa: E402


LABEL_TO_ID = {"ped": 0, "vehicle": 1}
ID_TO_LABEL = {value: key for key, value in LABEL_TO_ID.items()}
ALLOWED_SPLITS = {"train", "val"}
EXPECTED_SCENE_SPLITS = {
    "train": {"virat-ground-000201", "virat-ground-000206"},
    "val": {"virat-ground-000200", "virat-ground-000203"},
}
SEED = 20260927
FORBIDDEN_TOKEN = re.compile(r"(^|[_\-.])(test|blind|holdout)($|[_\-.])", re.IGNORECASE)

HOG_COMMON = {
    "win_size": [32, 32],
    "block_size": [16, 16],
    "block_stride": [8, 8],
    "cell_size": [8, 8],
    "deriv_aperture": 1,
    "win_sigma": 4.0,
    "histogram_norm_type": "L2Hys",
    "l2_hys_threshold": 0.2,
    "gamma_correction": False,
    "nlevels": 64,
    "signed_gradient": False,
    "compute_win_stride": [0, 0],
    "compute_padding": [0, 0],
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(records: Iterable[dict[str, Any]]) -> str:
    payload = json.dumps(list(records), ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def assert_safe_path(path: Path, role: str) -> None:
    for part in path.parts:
        if FORBIDDEN_TOKEN.search(part):
            raise ValueError(f"sealed-data guard rejected {role} path component: {part}")


def read_manifest(dataset: Path, enforce_expected_scenes: bool = True) -> list[dict[str, str]]:
    assert_safe_path(dataset, "dataset")
    manifest = dataset / "manifest.csv"
    if not manifest.is_file():
        raise ValueError(f"missing manifest: {manifest}")
    with manifest.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("empty manifest")

    required = {
        "sample_id", "split", "label", "scene_id", "roi_source", "roi_path",
        "roi_sha256", "xmin", "ymin", "xmax", "ymax", "frame_index",
    }
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"manifest fields missing: {sorted(missing)}")

    seen_ids: set[str] = set()
    scene_splits: dict[str, set[str]] = {}
    for row in rows:
        split = row["split"].strip().lower()
        if split not in ALLOWED_SPLITS:
            raise ValueError(f"sealed-data guard rejected split={split!r}")
        if row["label"] not in LABEL_TO_ID:
            raise ValueError(f"only ped/vehicle are allowed, got {row['label']!r}")
        if row["roi_source"] != "annotated":
            raise ValueError(f"only annotated ROI is allowed: {row['sample_id']}")
        if row["sample_id"] in seen_ids:
            raise ValueError(f"duplicate sample_id: {row['sample_id']}")
        seen_ids.add(row["sample_id"])
        assert_safe_path(Path(row["roi_path"]), "ROI")
        scene_splits.setdefault(row["scene_id"], set()).add(split)
    leaked = {scene: splits for scene, splits in scene_splits.items() if len(splits) != 1}
    if leaked:
        raise ValueError(f"scene leakage across splits: {leaked}")
    if enforce_expected_scenes:
        actual = {
            split: {row["scene_id"] for row in rows if row["split"] == split}
            for split in sorted(ALLOWED_SPLITS)
        }
        if actual != EXPECTED_SCENE_SPLITS:
            raise ValueError(f"unexpected scene split: {actual}")
    for split in ALLOWED_SPLITS:
        for label in LABEL_TO_ID:
            if not any(row["split"] == split and row["label"] == label for row in rows):
                raise ValueError(f"missing {split}/{label} samples")
    return rows


def make_hog(nbins: int) -> cv2.HOGDescriptor:
    if nbins not in (4, 9):
        raise ValueError("this diagnostic permits only 4 or 9 HOG bins")
    return cv2.HOGDescriptor(
        (32, 32), (16, 16), (8, 8), (8, 8), nbins,
        1, 4.0, cv2.HOGDescriptor_L2Hys, 0.2, False, 64, False,
    )


def load_roi(dataset: Path, row: dict[str, str], verify_hash: bool = True) -> np.ndarray:
    path = dataset / row["roi_path"]
    if not path.is_file():
        raise ValueError(f"missing ROI: {path}")
    with Image.open(path) as image:
        if image.size != (32, 32):
            raise ValueError(f"ROI is not 32x32: {path} -> {image.size}")
        roi = np.asarray(image.convert("L"), dtype=np.uint8)
    # DatasetWriter defines roi_sha256 over the canonical uint8 pixel payload,
    # not over the PNG container bytes.  Verify the same contract here while
    # recording the file hash separately in the run receipt.
    if verify_hash and hashlib.sha256(roi.tobytes()).hexdigest() != row["roi_sha256"]:
        raise ValueError(f"ROI pixel-payload hash mismatch: {path}")
    return roi


def extract_variant(roi: np.ndarray, variant: str,
                    hogs: dict[str, cv2.HOGDescriptor]) -> np.ndarray:
    if variant == "current_rtl64":
        values, _ = extract_features(roi.astype(int).tolist())
        return np.asarray(values, dtype=np.float64)
    descriptor = hogs[variant].compute(
        np.ascontiguousarray(roi), winStride=(0, 0), padding=(0, 0)
    )
    return descriptor.reshape(-1).astype(np.float64)


def class_metrics(y_true: np.ndarray, prediction: np.ndarray,
                  decision: np.ndarray) -> dict[str, Any]:
    report = classification_report(
        y_true, prediction, labels=[0, 1], target_names=["ped", "vehicle"],
        output_dict=True, zero_division=0,
    )
    score_by_class = {}
    for class_id, label in ID_TO_LABEL.items():
        selected = decision[y_true == class_id]
        score_by_class[label] = {
            "count": int(selected.size),
            "min": float(np.min(selected)) if selected.size else None,
            "max": float(np.max(selected)) if selected.size else None,
            "mean": float(np.mean(selected)) if selected.size else None,
            "median": float(np.median(selected)) if selected.size else None,
        }
    return {
        "accuracy": float(accuracy_score(y_true, prediction)),
        "balanced_accuracy": supported_balanced_accuracy(y_true, prediction),
        "confusion_matrix_truth_rows_pred_columns_labels_ped_vehicle":
            confusion_matrix(y_true, prediction, labels=[0, 1]).tolist(),
        "per_class": {
            label: {
                "precision": float(report[label]["precision"]),
                "recall": float(report[label]["recall"]),
                "f1": float(report[label]["f1-score"]),
                "support": int(report[label]["support"]),
            }
            for label in ("ped", "vehicle")
        },
        "decision_score_by_true_class": score_by_class,
        "decision_score_semantics": "negative=ped, positive=vehicle; not a probability",
    }


def height_value(row: dict[str, str]) -> int:
    return int(row["ymax"]) - int(row["ymin"]) + 1


def supported_balanced_accuracy(y_true: np.ndarray, prediction: np.ndarray) -> float:
    """Macro recall over classes present in the stratum, without sklearn warnings."""
    matrix = confusion_matrix(y_true, prediction, labels=[0, 1])
    support = matrix.sum(axis=1)
    recalls = [matrix[index, index] / support[index]
               for index in range(2) if support[index] > 0]
    return float(np.mean(recalls))


def height_band(height: int) -> str:
    if height <= 5:
        return "h01_05"
    if height <= 10:
        return "h06_10"
    if height <= 20:
        return "h11_20"
    return "h21_plus"


def metric_flat(model: str, group_type: str, group_value: str,
                rows: list[dict[str, str]], y_true: np.ndarray,
                pred: np.ndarray) -> dict[str, Any]:
    matrix = confusion_matrix(y_true, pred, labels=[0, 1])
    report = classification_report(
        y_true, pred, labels=[0, 1], target_names=["ped", "vehicle"],
        output_dict=True, zero_division=0,
    )
    return {
        "model": model,
        "split": "val",
        "group_type": group_type,
        "group_value": group_value,
        "sample_count": len(rows),
        "ped_support": int(report["ped"]["support"]),
        "vehicle_support": int(report["vehicle"]["support"]),
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": supported_balanced_accuracy(y_true, pred),
        "ped_precision": float(report["ped"]["precision"]),
        "ped_recall": float(report["ped"]["recall"]),
        "vehicle_precision": float(report["vehicle"]["precision"]),
        "vehicle_recall": float(report["vehicle"]["recall"]),
        "cm_ped_as_ped": int(matrix[0, 0]),
        "cm_ped_as_vehicle": int(matrix[0, 1]),
        "cm_vehicle_as_ped": int(matrix[1, 0]),
        "cm_vehicle_as_vehicle": int(matrix[1, 1]),
    }


def stratified_rows(model: str, rows: list[dict[str, str]], truth: np.ndarray,
                    prediction: np.ndarray) -> list[dict[str, Any]]:
    output = [metric_flat(model, "overall", "all", rows, truth, prediction)]
    group_specs = {
        "scene": [row["scene_id"] for row in rows],
        "height": [height_band(height_value(row)) for row in rows],
        "scene_height": [f"{row['scene_id']}|{height_band(height_value(row))}" for row in rows],
    }
    for group_type, values in group_specs.items():
        for value in sorted(set(values)):
            indices = np.asarray([index for index, candidate in enumerate(values)
                                  if candidate == value], dtype=np.int64)
            selected_rows = [rows[index] for index in indices]
            output.append(metric_flat(model, group_type, value, selected_rows,
                                      truth[indices], prediction[indices]))
    return output


def signed_required_bits(max_abs: int) -> int:
    return 2 if max_abs == 0 else int(max_abs).bit_length() + 1


def fixed_point_feasibility(
    x_by_split: dict[str, np.ndarray], scaler: StandardScaler,
    classifier: LinearSVC, float_prediction: dict[str, np.ndarray],
    float_decision: dict[str, np.ndarray],
) -> dict[str, Any]:
    """Evaluate one explicit integer candidate without claiming RTL equivalence."""
    feature_fraction_bits = 12
    feature_scale = 1 << feature_fraction_bits
    feature_storage_bits = 13  # unsigned Q1.12, permits the normalized endpoint 1.0
    feature_integer_max = (1 << feature_storage_bits) - 1
    weight_bits = 16
    weight_integer_max = (1 << (weight_bits - 1)) - 1

    folded_weights = classifier.coef_[0] / scaler.scale_
    folded_bias = float(
        classifier.intercept_[0] -
        np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_)
    )
    max_abs_weight = float(np.max(np.abs(folded_weights)))
    if max_abs_weight == 0.0:
        raise ValueError("zero folded weight vector")
    weight_scale = weight_integer_max / max_abs_weight
    quant_weights = np.rint(folded_weights * weight_scale).astype(np.int64)
    quant_bias = int(round(folded_bias * feature_scale * weight_scale))
    worst_abs_bound = int(abs(quant_bias) + feature_integer_max *
                          np.sum(np.abs(quant_weights), dtype=np.int64))

    split_results: dict[str, Any] = {}
    observed_abs = 0
    for split, features in x_by_split.items():
        if float(np.min(features)) < -1e-12 or float(np.max(features)) > 1.0 + 1e-9:
            raise ValueError("OpenCV HOG values do not fit the stated unsigned [0,1] contract")
        quant_features = np.rint(features * feature_scale).astype(np.int64)
        if int(np.max(quant_features)) > feature_integer_max:
            raise ValueError("quantized feature exceeds Q1.12 storage")
        integer_scores = quant_features @ quant_weights + quant_bias
        observed_abs = max(observed_abs, int(np.max(np.abs(integer_scores))))
        quant_prediction = (integer_scores >= 0).astype(np.int64)
        normalized_score = integer_scores.astype(np.float64) / (feature_scale * weight_scale)
        delta = normalized_score - float_decision[split]
        split_results[split] = {
            "sample_count": int(features.shape[0]),
            "classification_mismatch_vs_float":
                int(np.sum(quant_prediction != float_prediction[split])),
            "max_abs_score_error": float(np.max(np.abs(delta))),
            "mean_abs_score_error": float(np.mean(np.abs(delta))),
            "integer_score_min": int(np.min(integer_scores)),
            "integer_score_max": int(np.max(integer_scores)),
        }
    return {
        "status": "diagnostic_fixed_point_candidate_not_rtl_equivalence",
        "runtime_scaler": "none; StandardScaler is algebraically folded into weights and bias",
        "feature_format": {
            "unsigned_storage_bits": feature_storage_bits,
            "fraction_bits": feature_fraction_bits,
            "scale": feature_scale,
            "rounding": "round-to-nearest-even via numpy.rint",
            "saturation": "none needed for observed [0,1] descriptor contract",
        },
        "weight_format": {
            "signed_bits": weight_bits,
            "scale": weight_scale,
            "rounding": "round-to-nearest-even via numpy.rint",
            "max_abs_integer_weight": int(np.max(np.abs(quant_weights))),
        },
        "quantized_bias": quant_bias,
        "worst_case_accumulator_abs_bound": worst_abs_bound,
        "worst_case_required_signed_accumulator_bits": signed_required_bits(worst_abs_bound),
        "observed_max_abs_accumulator": observed_abs,
        "observed_required_signed_accumulator_bits": signed_required_bits(observed_abs),
        "splits": split_results,
        "limitations": [
            "The descriptor itself is still OpenCV floating-point HOG; only its output and linear model are quantized here.",
            "No integer gradient, orientation interpolation, L2-Hys, reciprocal-square-root, rounding, or saturation implementation is defined.",
            "The worst-case accumulator bound is conservative and assumes every feature reaches the storage maximum simultaneously.",
            "These formats are feasibility evidence only and must not be presented as Python/RTL equivalence.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def self_test() -> None:
    hog4 = make_hog(4)
    hog9 = make_hog(9)
    zero = np.zeros((32, 32), dtype=np.uint8)
    assert hog4.getDescriptorSize() == 144
    assert hog9.getDescriptorSize() == 324
    assert np.array_equal(hog4.compute(zero), hog4.compute(zero))
    assert np.count_nonzero(hog4.compute(zero)) == 0

    horizontal = np.tile(np.arange(32, dtype=np.uint8) * 8, (32, 1))
    vertical = horizontal.T.copy()
    horizontal_bins = hog4.compute(horizontal).reshape(-1, 4).sum(axis=0)
    vertical_bins = hog4.compute(vertical).reshape(-1, 4).sum(axis=0)
    assert horizontal_bins[0] > 0 and horizontal_bins[3] > 0
    assert np.allclose(horizontal_bins[1:3], 0)
    assert vertical_bins[1] > 0 and vertical_bins[2] > 0
    assert np.allclose(vertical_bins[[0, 3]], 0)

    top_left = zero.copy()
    bottom_right = zero.copy()
    top_left[4:12, 4:12] = 255
    bottom_right[20:28, 20:28] = 255
    first = hog4.compute(top_left).reshape(-1)
    second = hog4.compute(bottom_right).reshape(-1)
    first_centroid = float(np.dot(np.arange(first.size), first) / np.sum(first))
    second_centroid = float(np.dot(np.arange(second.size), second) / np.sum(second))
    assert first_centroid < second_centroid

    try:
        assert_safe_path(Path("safe") / "blind_holdout", "synthetic")
    except ValueError:
        pass
    else:
        raise AssertionError("sealed path guard did not reject blind_holdout")

    with tempfile.TemporaryDirectory(prefix="opencv_hog_guard_") as temporary:
        synthetic_root = Path(temporary) / "safe_dataset"
        synthetic_root.mkdir()
        fields = [
            "sample_id", "split", "label", "scene_id", "roi_source", "roi_path",
            "roi_sha256", "xmin", "ymin", "xmax", "ymax", "frame_index",
        ]
        with (synthetic_root / "manifest.csv").open(
            "w", encoding="utf-8", newline=""
        ) as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerow({
                "sample_id": "forbidden", "split": "test", "label": "ped",
                "scene_id": "scene", "roi_source": "annotated", "roi_path": "roi.png",
                "roi_sha256": "0" * 64, "xmin": 0, "ymin": 0, "xmax": 1,
                "ymax": 1, "frame_index": 0,
            })
        try:
            read_manifest(synthetic_root, enforce_expected_scenes=False)
        except ValueError as error:
            assert "rejected split" in str(error)
        else:
            raise AssertionError("sealed manifest guard did not reject split=test")

    print(json.dumps({
        "status": "PASS",
        "checks": [
            "descriptor_dimensions_144_324",
            "deterministic_and_zero_image",
            "orientation_bin_layout_basic_property",
            "spatial_descriptor_order_basic_property",
            "sealed_path_guard",
            "sealed_manifest_split_guard",
        ],
    }, indent=2))


def run(dataset: Path, output: Path) -> None:
    dataset = dataset.resolve()
    output = output.resolve()
    assert_safe_path(output, "output")
    rows = read_manifest(dataset)
    manifest_path = dataset / "manifest.csv"
    hog_reference_path = TOOLS_DIR / "hog_reference.py"

    hogs = {
        "opencv_hog144": make_hog(4),
        "opencv_hog324": make_hog(9),
    }
    variants = ("current_rtl64", "opencv_hog144", "opencv_hog324")

    roi_cache: dict[str, np.ndarray] = {}
    verified_roi_hashes: list[dict[str, str]] = []
    for row in rows:
        roi = load_roi(dataset, row, verify_hash=True)
        roi_cache[row["sample_id"]] = roi
        verified_roi_hashes.append({
            "sample_id": row["sample_id"],
            "split": row["split"],
            "label": row["label"],
            "scene_id": row["scene_id"],
            "roi_pixel_payload_sha256": row["roi_sha256"],
            "roi_png_file_sha256": sha256_file(dataset / row["roi_path"]),
        })

    split_rows = {
        split: [row for row in rows if row["split"] == split]
        for split in ("train", "val")
    }
    y_by_split = {
        split: np.asarray([LABEL_TO_ID[row["label"]] for row in selected], dtype=np.int64)
        for split, selected in split_rows.items()
    }

    output.mkdir(parents=True, exist_ok=True)
    report_models: dict[str, Any] = {}
    predictions_csv: list[dict[str, Any]] = []
    failures_csv: list[dict[str, Any]] = []
    strata_csv: list[dict[str, Any]] = []
    ranges_csv: list[dict[str, Any]] = []
    model_parameters: dict[str, Any] = {}

    for variant in variants:
        x_by_split = {
            split: np.vstack([
                extract_variant(roi_cache[row["sample_id"]], variant, hogs)
                for row in selected
            ])
            for split, selected in split_rows.items()
        }
        scaler = StandardScaler().fit(x_by_split["train"])
        classifier = LinearSVC(
            C=1.0, class_weight="balanced", random_state=SEED, max_iter=30000,
        ).fit(scaler.transform(x_by_split["train"]), y_by_split["train"])
        if classifier.classes_.tolist() != [0, 1]:
            raise ValueError(f"unexpected class order: {classifier.classes_.tolist()}")

        prediction_by_split: dict[str, np.ndarray] = {}
        decision_by_split: dict[str, np.ndarray] = {}
        split_metrics: dict[str, Any] = {}
        for split in ("train", "val"):
            transformed = scaler.transform(x_by_split[split])
            prediction = classifier.predict(transformed)
            decision = classifier.decision_function(transformed)
            prediction_by_split[split] = prediction
            decision_by_split[split] = decision
            split_metrics[split] = class_metrics(y_by_split[split], prediction, decision)

            for index, row in enumerate(split_rows[split]):
                result = {
                    "model": variant,
                    "split": split,
                    "sample_id": row["sample_id"],
                    "scene_id": row["scene_id"],
                    "frame_index": row["frame_index"],
                    "bbox_height": height_value(row),
                    "height_band": height_band(height_value(row)),
                    "truth": row["label"],
                    "prediction": ID_TO_LABEL[int(prediction[index])],
                    "decision_score_vehicle_positive": float(decision[index]),
                    "roi_path": row["roi_path"],
                    "roi_sha256": row["roi_sha256"],
                }
                predictions_csv.append(result)
                if int(prediction[index]) != int(y_by_split[split][index]):
                    failures_csv.append(result)

        strata_csv.extend(stratified_rows(
            variant, split_rows["val"], y_by_split["val"], prediction_by_split["val"]
        ))

        dimension = int(x_by_split["train"].shape[1])
        for feature_index in range(dimension):
            ranges_csv.append({
                "model": variant,
                "feature_index": feature_index,
                "train_min": float(np.min(x_by_split["train"][:, feature_index])),
                "train_max": float(np.max(x_by_split["train"][:, feature_index])),
                "train_mean": float(np.mean(x_by_split["train"][:, feature_index])),
                "val_min": float(np.min(x_by_split["val"][:, feature_index])),
                "val_max": float(np.max(x_by_split["val"][:, feature_index])),
                "val_mean": float(np.mean(x_by_split["val"][:, feature_index])),
            })

        descriptor_stats = {
            split: {
                "global_min": float(np.min(features)),
                "global_max": float(np.max(features)),
                "global_mean": float(np.mean(features)),
                "global_std": float(np.std(features)),
                "zero_fraction": float(np.mean(features == 0)),
            }
            for split, features in x_by_split.items()
        }
        report_models[variant] = {
            "feature_dimension": dimension,
            "descriptor_stats": descriptor_stats,
            "metrics": split_metrics,
            "linear_svc": {
                "C": 1.0,
                "class_weight": "balanced",
                "loss": classifier.loss,
                "penalty": classifier.penalty,
                "dual": classifier.dual,
                "fit_intercept": classifier.fit_intercept,
                "random_state": SEED,
                "max_iter": 30000,
                "n_iter": int(classifier.n_iter_),
            },
        }
        if variant.startswith("opencv_hog"):
            report_models[variant]["fixed_point_feasibility"] = fixed_point_feasibility(
                x_by_split, scaler, classifier, prediction_by_split, decision_by_split
            )

        folded_weights = classifier.coef_[0] / scaler.scale_
        folded_bias = float(
            classifier.intercept_[0] -
            np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_)
        )
        model_parameters[variant] = {
            "status": "diagnostic_float_model_not_frozen_not_rtl",
            "class_order": ["ped", "vehicle"],
            "decision_score_positive_class": "vehicle",
            "scaler_mean": scaler.mean_.tolist(),
            "scaler_scale": scaler.scale_.tolist(),
            "linear_svc_coef_on_scaled_features": classifier.coef_[0].tolist(),
            "linear_svc_intercept_on_scaled_features": float(classifier.intercept_[0]),
            "folded_weights_on_raw_features": folded_weights.tolist(),
            "folded_bias_on_raw_features": folded_bias,
        }

    write_csv(output / "predictions.csv", predictions_csv)
    if failures_csv:
        write_csv(output / "failures.csv", failures_csv)
    else:
        (output / "failures.csv").write_text(
            "model,split,sample_id,scene_id,frame_index,bbox_height,height_band,truth,prediction,decision_score_vehicle_positive,roi_path,roi_sha256\n",
            encoding="utf-8",
        )
    write_csv(output / "stratified_metrics.csv", strata_csv)
    write_csv(output / "feature_ranges.csv", ranges_csv)
    (output / "model_parameters.json").write_text(
        json.dumps(model_parameters, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = {
        "status": "external_reference_diagnostic_train_val_only_not_acceptance_not_rtl",
        "scope": {
            "dataset": str(dataset),
            "splits_read": ["train", "val"],
            "roi_source": "annotated",
            "labels": ["ped", "vehicle"],
            "test_blind_holdout": "rejected_by_fail_closed_path_and_manifest_guards",
            "hyperparameter_tuning": False,
            "test_evaluation": False,
        },
        "sample_counts": {
            split: {
                "total": len(selected),
                "by_label": dict(sorted(Counter(row["label"] for row in selected).items())),
                "by_scene": dict(sorted(Counter(row["scene_id"] for row in selected).items())),
            }
            for split, selected in split_rows.items()
        },
        "scene_split_contract": {
            split: sorted(scenes) for split, scenes in EXPECTED_SCENE_SPLITS.items()
        },
        "preprocessing": {
            "input": "stored 32x32 uint8 grayscale roi_path from road_roi_dataset_virat",
            "additional_resize_or_color_conversion": "none beyond PIL conversion of stored L image to L",
            "classifier_preprocessing": "StandardScaler fit on train only; folded coefficients exported for analysis",
        },
        "opencv_hog_explicit_parameters": {
            "opencv_hog144": {**HOG_COMMON, "nbins": 4, "descriptor_size": 144},
            "opencv_hog324": {**HOG_COMMON, "nbins": 9, "descriptor_size": 324},
        },
        "current_rtl64_contract": {
            "implementation": str(hog_reference_path),
            "implementation_sha256": sha256_file(hog_reference_path),
            "feature_dimension": 64,
            "note": "Calls the existing bit-exact Sobel/bin/cell accumulation function; classifier remains a diagnostic float fit.",
        },
        "models": report_models,
        "inputs": {
            "manifest": str(manifest_path),
            "manifest_sha256": sha256_file(manifest_path),
            "selected_roi_count": len(verified_roi_hashes),
            "selected_roi_receipt_sha256": canonical_sha256(verified_roi_hashes),
            "manifest_roi_hash_contract": "SHA256 of canonical 32x32 uint8 grayscale pixel payload",
            "all_manifest_roi_pixel_payload_hashes_verified": True,
        },
        "implementation": {
            "script": str(SCRIPT_PATH),
            "script_sha256": sha256_file(SCRIPT_PATH),
            "python": platform.python_version(),
            "opencv": cv2.__version__,
            "scikit_learn": sklearn.__version__,
            "numpy": np.__version__,
            "pillow": PIL.__version__,
        },
        "licenses": {
            "OpenCV": {
                "license": "Apache-2.0 for OpenCV 4.x",
                "url": "https://github.com/opencv/opencv/blob/4.x/LICENSE",
            },
            "scikit-learn": {
                "license": "BSD-3-Clause",
                "url": "https://github.com/scikit-learn/scikit-learn/blob/main/COPYING",
            },
            "NumPy": {
                "license": "BSD-3-Clause",
                "url": "https://github.com/numpy/numpy/blob/main/LICENSE.txt",
            },
            "Pillow": {
                "license": "HPND",
                "url": "https://github.com/python-pillow/Pillow/blob/main/LICENSE",
            },
        },
        "artifacts": {
            "predictions": "predictions.csv",
            "failures": "failures.csv",
            "stratified_metrics": "stratified_metrics.csv",
            "feature_ranges": "feature_ranges.csv",
            "model_parameters": "model_parameters.json",
        },
        "limitations": [
            "This run uses only 429 sparsely sampled annotated VIRAT ROIs from four scenes and is not a formal model acceptance result.",
            "The validation scenes are independent of the train scenes, but both belong to one dataset family and one camera-domain family.",
            "OpenCV HOG is a floating-point external reference; its orientation interpolation and L2-Hys path are not bit-exact models of current RTL.",
            "The current_rtl64 descriptor is bit-exact, but the fitted StandardScaler/LinearSVC in this experiment is not the production quantized SVM.",
            "Very small distant pedestrians contain only a few analysis pixels; a richer descriptor cannot reconstruct missing spatial detail.",
            "No invalid-candidate rejection, CCL candidate boxes, threshold tuning, test split, blind reserve, or holdout is evaluated.",
            "Decision scores are margins and are not probabilities.",
            "No RTL, ROM, HDL parameters, or claim of Python/RTL classification equivalence is produced.",
        ],
    }
    report_path = output / "report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    artifact_hashes = {
        path.name: sha256_file(path)
        for path in sorted(output.iterdir())
        if path.is_file() and path.name != "artifact_hashes.json" and not path.name.startswith(".")
    }
    (output / "artifact_hashes.json").write_text(
        json.dumps(artifact_hashes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": report["status"],
        "output": str(output),
        "sample_counts": report["sample_counts"],
        "validation": {
            variant: report_models[variant]["metrics"]["val"]
            for variant in variants
        },
        "fixed_point_mismatches": {
            variant: report_models[variant]["fixed_point_feasibility"]["splits"]
            for variant in variants if variant.startswith("opencv_hog")
        },
    }, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        if args.dataset is not None or args.output is not None:
            parser.error("--self-test cannot be combined with --dataset/--output")
        self_test()
        return 0
    if args.dataset is None or args.output is None:
        parser.error("--dataset and --output are required for a diagnostic run")
    run(args.dataset, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
