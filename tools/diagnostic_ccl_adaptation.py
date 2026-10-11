#!/usr/bin/env python3
"""Diagnostic fit with a small, thinned set of reviewed train-scene CCL crops."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from road_evaluation import LABELS, audit_dataset, features_for
from train_hog_svm import image_features
from candidate_review_io import load_reviewed

VALID_LABELS = {"ped", "vehicle"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def thin(rows: list[dict], minimum_gap: int, maximum_per_label: int) -> list[dict]:
    selected = []
    for label in ("ped", "vehicle"):
        last = None
        for row in sorted((item for item in rows if item["label"] == label),
                          key=lambda item: (int(item["source_frame"]), item["candidate_id"])):
            frame = int(row["source_frame"])
            if last is not None and frame - last < minimum_gap:
                continue
            selected.append(row)
            last = frame
            if sum(item["label"] == label for item in selected) >= maximum_per_label:
                break
    return selected


def summarize(rows: list[dict], truth: np.ndarray, prediction: np.ndarray) -> dict:
    return {
        "sample_count": len(rows),
        "class_counts": dict(sorted(Counter(row["label"] for row in rows).items())),
        "confusion_matrix": confusion_matrix(truth, prediction, labels=[0, 1]).tolist(),
        "classes": classification_report(
            truth, prediction, labels=[0, 1], target_names=["ped", "vehicle"],
            output_dict=True, zero_division=0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--train-ccl-root", type=Path, required=True)
    parser.add_argument("--train-reviewed", type=Path, required=True)
    parser.add_argument("--val-review-set", nargs=2, action="append", required=True,
                        metavar=("CANDIDATE_ROOT", "REVIEWED"))
    parser.add_argument("--minimum-frame-gap", type=int, default=2)
    parser.add_argument("--maximum-per-label", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.minimum_frame_gap < 1 or args.maximum_per_label < 1:
        raise ValueError("thinning parameters must be positive")

    manifest_rows = audit_dataset(args.dataset)
    annotated_train = [row for row in manifest_rows if row["split"] == "train" and
                       row["roi_source"] == "annotated" and row["label"] in VALID_LABELS]
    annotated_val = [row for row in manifest_rows if row["split"] == "val" and
                     row["roi_source"] == "annotated" and row["label"] in VALID_LABELS]
    reviewed_train, train_review_receipt = load_reviewed(
        args.train_ccl_root, args.train_reviewed, "train")
    train_ccl = thin([row for row in reviewed_train if row["label"] in VALID_LABELS],
                     args.minimum_frame_gap, args.maximum_per_label)

    x_train_annotated = features_for(args.dataset, annotated_train)
    x_train_ccl = np.asarray([
        image_features(args.train_ccl_root / row["roi_path"]) for row in train_ccl],
        dtype=np.int64)
    x_train = np.concatenate((x_train_annotated, x_train_ccl), axis=0)
    y_train = np.asarray([LABELS[row["label"]] for row in annotated_train + train_ccl])

    val_ccl = []
    x_val_ccl_parts = []
    val_receipts = []
    for candidate_root_text, reviewed_text in args.val_review_set:
        candidate_root, reviewed = Path(candidate_root_text), Path(reviewed_text)
        set_rows, set_receipt = load_reviewed(candidate_root, reviewed, "val")
        metric_rows = [row for row in set_rows if row["label"] in VALID_LABELS]
        val_ccl.extend(metric_rows)
        x_val_ccl_parts.append(np.asarray([
            image_features(candidate_root / row["roi_path"]) for row in metric_rows],
            dtype=np.int64))
        val_receipts.append({**set_receipt, "valid_row_count": len(metric_rows)})
    x_val_annotated = features_for(args.dataset, annotated_val)
    x_val_ccl = np.concatenate(x_val_ccl_parts, axis=0)
    y_val_annotated = np.asarray([LABELS[row["label"]] for row in annotated_val])
    y_val_ccl = np.asarray([LABELS[row["label"]] for row in val_ccl])

    scaler = StandardScaler().fit(x_train)
    classifier = LinearSVC(C=1.0, class_weight="balanced", random_state=20260927,
                           max_iter=30000).fit(scaler.transform(x_train), y_train)
    weights = classifier.coef_[0] / scaler.scale_
    bias = float(classifier.intercept_[0] -
                 np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_))
    scale = ((1 << 11) - 1) / float(np.max(np.abs(weights)))
    qweights = np.rint(weights * scale).astype(np.int64)
    qbias = int(round(bias * scale))

    def predict(features: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        floating = (features @ weights + bias >= 0).astype(np.int64)
        fixed = (features @ qweights + qbias >= 0).astype(np.int64)
        return floating, fixed

    float_annotated, fixed_annotated = predict(x_val_annotated)
    float_ccl, fixed_ccl = predict(x_val_ccl)
    args.output.mkdir(parents=True, exist_ok=True)
    model = {
        "diagnostic_only": True, "adaptation": "annotated_plus_thinned_train_scene_ccl",
        "float_folded_weights": weights.tolist(), "float_folded_bias": bias,
        "quantized_weights": qweights.tolist(), "quantized_bias": qbias,
        "quantization_scale": scale,
    }
    model_path = args.output / "model.diagnostic.json"
    model_path.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    report = {
        "status": "pilot_ccl_adaptation_not_acceptance_evidence",
        "train_annotated_count": len(annotated_train),
        "train_ccl_selected_count": len(train_ccl),
        "train_ccl_selected_by_label": dict(sorted(Counter(
            row["label"] for row in train_ccl).items())),
        "train_ccl_frames_by_label": {
            label: [int(row["source_frame"]) for row in train_ccl if row["label"] == label]
            for label in ("ped", "vehicle")},
        "thinning": {"minimum_frame_gap": args.minimum_frame_gap,
                     "maximum_per_label": args.maximum_per_label},
        "annotated_validation": summarize(annotated_val, y_val_annotated, fixed_annotated),
        "ccl_validation": summarize(val_ccl, y_val_ccl, fixed_ccl),
        "float_fixed_class_disagreements": {
            "annotated_validation": int(np.sum(float_annotated != fixed_annotated)),
            "ccl_validation": int(np.sum(float_ccl != fixed_ccl)),
        },
        "invalid_rejection_measured": False,
        "dataset_manifest_sha256": digest(args.dataset / "manifest.csv"),
        "train_review_set": train_review_receipt,
        "validation_review_sets": val_receipts,
        "model_sha256": digest(model_path),
        "limitations": [
            "Only one short train-scene CCL sequence is available and its frames remain correlated.",
            "No invalid rows are fitted; this experiment cannot select a rejection threshold.",
            "C=1.0 and preprocessing remain fixed; this diagnoses input-domain mismatch only.",
            "No test or blind reserve data are opened.",
        ],
    }
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "train_ccl_selected_by_label": report["train_ccl_selected_by_label"],
        "annotated_recall": {label: report["annotated_validation"]["classes"][label]["recall"]
                             for label in ("ped", "vehicle")},
        "ccl_recall": {label: report["ccl_validation"]["classes"][label]["recall"]
                       for label in ("ped", "vehicle")},
        "float_fixed_class_disagreements": report["float_fixed_class_disagreements"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
