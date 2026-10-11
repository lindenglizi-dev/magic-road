#!/usr/bin/env python3
"""Run a VIRAT-only diagnostic float/fixed SVM fit without test or freezing."""
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(rows: list[dict], predictions: np.ndarray) -> dict[str, object]:
    truth = np.asarray([LABELS[row["label"]] for row in rows])
    return {
        "sample_count": len(rows),
        "class_counts": dict(sorted(Counter(row["label"] for row in rows).items())),
        "accuracy": float(np.mean(truth == predictions)),
        "confusion_matrix": confusion_matrix(truth, predictions, labels=[0, 1]).tolist(),
        "classes": classification_report(
            truth, predictions, labels=[0, 1], target_names=["ped", "vehicle"],
            output_dict=True, zero_division=0),
    }


def grouped_recall(rows: list[dict], predictions: np.ndarray) -> dict[str, object]:
    """Expose scene and sampled-bbox scale limits without tuning the model."""
    truth = np.asarray([LABELS[row["label"]] for row in rows])

    def summarize(indices: list[int]) -> dict[str, object]:
        return {
            "count": len(indices),
            "class_counts": dict(sorted(Counter(rows[index]["label"] for index in indices).items())),
            "recall": {
                label: (float(np.mean(predictions[selected] == class_id)) if selected else None)
                for label, class_id in (("ped", 0), ("vehicle", 1))
                for selected in [[index for index in indices if truth[index] == class_id]]
            },
        }

    by_scene: dict[str, list[int]] = {}
    by_height: dict[str, list[int]] = {}
    for index, row in enumerate(rows):
        by_scene.setdefault(row["scene_id"], []).append(index)
        height = int(row["ymax"]) - int(row["ymin"]) + 1
        height_bin = ("h_le_6" if height <= 6 else "h_7_9" if height <= 9
                      else "h_10_15" if height <= 15 else "h_ge_16")
        by_height.setdefault(height_bin, []).append(index)
    return {
        "by_scene": {key: summarize(value) for key, value in sorted(by_scene.items())},
        "by_analysis_bbox_height": {
            key: summarize(value) for key, value in sorted(by_height.items())},
        "height_definition": "inclusive 256x144 analysis-box height before 32x32 resize",
    }


def run(dataset: Path, output: Path, weight_bits: int = 12,
        accumulator_bits: int = 40, c_value: float = 1.0) -> dict[str, object]:
    rows = audit_dataset(dataset)
    selected = [row for row in rows if row["scene_id"].startswith("virat-ground-") and
                row["roi_source"] == "annotated" and row["label"] in {"ped", "vehicle"}]
    train = [row for row in selected if row["split"] == "train"]
    validation = [row for row in selected if row["split"] == "val"]
    if any({row["label"] for row in subset} != {"ped", "vehicle"}
           for subset in (train, validation)):
        raise ValueError("VIRAT train and val must each contain both classes")
    if any(row["split"] == "test" for row in selected):
        raise ValueError("diagnostic fit refuses imported test samples")
    x_train, x_val = features_for(dataset, train), features_for(dataset, validation)
    y_train = np.asarray([LABELS[row["label"]] for row in train])
    y_val = np.asarray([LABELS[row["label"]] for row in validation])
    scaler = StandardScaler().fit(x_train)
    classifier = LinearSVC(C=c_value, class_weight="balanced", random_state=20260927,
                           max_iter=30000)
    classifier.fit(scaler.transform(x_train), y_train)
    float_predictions = classifier.predict(scaler.transform(x_val))
    weights = classifier.coef_[0] / scaler.scale_
    bias = float(classifier.intercept_[0] -
                 np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_))
    scale = ((1 << (weight_bits - 1)) - 1) / float(np.max(np.abs(weights)))
    quantized_weights = np.rint(weights * scale).astype(np.int64)
    quantized_bias = int(round(bias * scale))
    float_scores = x_val @ weights + bias
    quantized_scores = x_val @ quantized_weights + quantized_bias
    quantized_predictions = (quantized_scores >= 0).astype(np.int64)
    worst_bound = abs(quantized_bias) + int(np.abs(quantized_weights).sum()) * (64 * 2040)
    accumulator_limit = (1 << (accumulator_bits - 1)) - 1
    if worst_bound > accumulator_limit:
        raise ValueError("configured accumulator may overflow")

    output.mkdir(parents=True, exist_ok=True)
    model = {
        "diagnostic_only": True,
        "C": c_value,
        "feature_count": 64,
        "weight_bits": weight_bits,
        "accumulator_bits": accumulator_bits,
        "float_folded_weights": weights.tolist(),
        "float_folded_bias": bias,
        "quantized_weights": quantized_weights.tolist(),
        "quantized_bias": quantized_bias,
        "quantization_scale": scale,
        "worst_score_bound": worst_bound,
    }
    (output / "model.diagnostic.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["sample_id", "split", "scene_id", "frame_index", "label", "roi_path",
              "float_score", "quantized_score", "float_prediction", "quantized_prediction",
              "reason"]
    prediction_rows = []
    for row, float_score, quantized_score, float_prediction, quantized_prediction in zip(
            validation, float_scores, quantized_scores, float_predictions, quantized_predictions):
        expected = LABELS[row["label"]]
        reasons = []
        if quantized_prediction != expected:
            reasons.append("quantized_misclassification")
        if float_prediction != quantized_prediction:
            reasons.append("float_quantized_class_disagreement")
        prediction_rows.append({
            **{key: row[key] for key in ("sample_id", "split", "scene_id", "frame_index",
                                         "label", "roi_path")},
            "float_score": float(float_score),
            "quantized_score": int(quantized_score),
            "float_prediction": "vehicle" if float_prediction else "ped",
            "quantized_prediction": "vehicle" if quantized_prediction else "ped",
            "reason": ";".join(reasons),
        })
    for name, filtered in (("predictions.csv", prediction_rows),
                           ("failures.csv", [row for row in prediction_rows if row["reason"]])):
        with (output / name).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(filtered)
    result = {
        "status": "pilot_only_not_acceptance_evidence",
        "test_split_used": False,
        "development_holdout_mapping_qa_viewed": True,
        "model_or_metric_frozen": False,
        "thresholds_frozen": False,
        "scene_isolation": {
            "train": sorted({row["scene_id"] for row in train}),
            "val": sorted({row["scene_id"] for row in validation}),
        },
        "source_confounded": False,
        "source_note": "fit is restricted to official VIRAT scenes containing both ped and vehicle; legacy CDnet and UA-DETRAC-mirror ROI are excluded",
        "train_count": len(train),
        "validation_count": len(validation),
        "float": metrics(validation, float_predictions),
        "quantized": metrics(validation, quantized_predictions),
        "quantized_grouped": grouped_recall(validation, quantized_predictions),
        "float_quantized_class_disagreements": int(np.sum(float_predictions != quantized_predictions)),
        "worst_score_bound": worst_bound,
        "accumulator_limit": accumulator_limit,
        "dataset_manifest_sha256": digest(dataset / "manifest.csv"),
        "model_sha256": digest(output / "model.diagnostic.json"),
        "failure_count": sum(bool(row["reason"]) for row in prediction_rows),
        "limitations": [
            "contact-sheet review is pilot-level and distant pedestrians can be only 2-6 analysis pixels wide",
            "fixed C=1.0 is used; validation tuning and acceptance-threshold decisions were not performed",
            "no invalid or CCL candidates are present, so invalid false acceptance and end-to-end recall are unmeasured",
            "split=test scenes were viewed for mapping QA but neither imported nor scored; they are not a blind final test",
            "this is Python float/fixed comparison; RTL score/feature crosscheck remains separate",
        ],
    }
    (output / "metrics.diagnostic.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.dataset.resolve(), args.output.resolve())
    print(json.dumps({key: result[key] for key in (
        "status", "train_count", "validation_count", "float", "quantized",
        "float_quantized_class_disagreements", "failure_count")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
