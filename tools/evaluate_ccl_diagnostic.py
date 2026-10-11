#!/usr/bin/env python3
"""Evaluate the frozen diagnostic two-class model on reviewed RTL CCL crops."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

from train_hog_svm import image_features
from candidate_review_io import load_reviewed


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--reviewed", type=Path)
    parser.add_argument("--review-set", nargs=2, action="append",
                        metavar=("CANDIDATE_ROOT", "REVIEWED"),
                        help="Repeat to evaluate several reviewed windows together")
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence-scope", choices=("train", "validation"), default="train")
    args = parser.parse_args()
    if args.review_set:
        if args.candidate_root is not None or args.reviewed is not None:
            parser.error("use either --review-set or --candidate-root/--reviewed")
        review_sets = [(Path(root), Path(reviewed)) for root, reviewed in args.review_set]
    else:
        if args.candidate_root is None or args.reviewed is None:
            parser.error("--candidate-root and --reviewed are required without --review-set")
        review_sets = [(args.candidate_root, args.reviewed)]
    rows = []
    reviewed_set_receipts = []
    for set_index, (candidate_root, reviewed_path) in enumerate(review_sets):
        set_rows, set_receipt = load_reviewed(
            candidate_root, reviewed_path, "val" if args.evidence_scope == "validation" else "train")
        set_name = candidate_root.name or f"set_{set_index}"
        for row in set_rows:
            row["_candidate_root"] = str(candidate_root)
            row["_review_set"] = set_name
        rows.extend(set_rows)
        reviewed_set_receipts.append({"name": set_name, **set_receipt})
    if not rows or any(row["label"] not in {"ped", "vehicle", "invalid", "ignore"}
                       for row in rows):
        raise ValueError("reviewed CCL rows need explicit ped/vehicle/invalid/ignore labels")
    ignored_rows = [row for row in rows if row["label"] == "ignore"]
    rows = [row for row in rows if row["label"] != "ignore"]
    if not rows:
        raise ValueError("no metric-bearing rows remain after excluding ignore labels")
    model = json.loads(args.model.read_text(encoding="utf-8"))
    features = np.asarray([
        image_features(Path(row["_candidate_root"]) / row["roi_path"]) for row in rows],
        dtype=np.int64)
    float_scores = features @ np.asarray(model["float_folded_weights"]) + model["float_folded_bias"]
    fixed_scores = (features @ np.asarray(model["quantized_weights"], dtype=np.int64) +
                    int(model["quantized_bias"]))
    float_predictions = (float_scores >= 0).astype(int)
    fixed_predictions = (fixed_scores >= 0).astype(int)
    truth = np.asarray([0 if row["label"] == "ped" else
                        1 if row["label"] == "vehicle" else -1 for row in rows])
    valid = truth >= 0
    labels = ["ped", "vehicle"]
    records = []
    failure_count = 0
    for row, fs, qs, fp, qp in zip(rows, float_scores, fixed_scores,
                                   float_predictions, fixed_predictions):
        prediction = labels[int(qp)]
        reason = ("invalid_candidate_forced_class" if row["label"] == "invalid" else
                  "misclassified" if prediction != row["label"] else "")
        if fp != qp:
            reason = (reason + ";" if reason else "") + "float_fixed_disagreement"
        failure_count += bool(reason)
        records.append({
            "candidate_id": f'{row["_review_set"]}:{row["candidate_id"]}',
            "review_set": row["_review_set"], "source_frame": row["source_frame"],
            "label": row["label"], "prediction": prediction,
            "float_score": float(fs), "fixed_score": int(qs), "reason": reason,
            "review_basis": row["review_basis"], "roi_path": row["roi_path"],
        })
    available_labels = {row["label"] for row in rows}
    complete_coverage = {"ped", "vehicle", "invalid"}.issubset(available_labels)
    valid_report = classification_report(
        truth[valid], fixed_predictions[valid], labels=[0, 1], target_names=labels,
        output_dict=True, zero_division=0)
    coverage_reason = (
        "Acceptance criteria are not frozen, so no rejection threshold is selected."
        if complete_coverage else
        "Acceptance criteria are not frozen and the reviewed windows lack at least one required "
        "class, so no rejection threshold is selected.")
    report = {
        "status": ("diagnostic_validation_ccl_not_threshold_selection_evidence"
                   if args.evidence_scope == "validation" else
                   "diagnostic_train_scene_ccl_not_acceptance_evidence"),
        "candidate_count": len(rows),
        "ignored_candidate_count": len(ignored_rows),
        "class_counts": dict(sorted(Counter(row["label"] for row in rows).items())),
        "valid_confusion_matrix": confusion_matrix(truth[valid], fixed_predictions[valid],
                                                     labels=[0, 1]).tolist(),
        "valid_classes": valid_report,
        "invalid_false_accept_rate": 1.0 if np.any(~valid) else None,
        "invalid_forced_predictions": {
            "ped": int(np.sum((truth == -1) & (fixed_predictions == 0))),
            "vehicle": int(np.sum((truth == -1) & (fixed_predictions == 1))),
        },
        "float_fixed_class_disagreements": int(np.sum(float_predictions != fixed_predictions)),
        "failure_row_count": failure_count,
        "model_sha256": digest(args.model),
        "reviewed_sets": reviewed_set_receipts,
        "threshold_selection": {
            "selected_threshold": None,
            "criteria_status": "suggested_not_frozen",
            "complete_class_coverage": complete_coverage,
            "reason": coverage_reason,
            "fixed_score_ranges": {
                label: {
                    "minimum": int(np.min(fixed_scores[[row["label"] == label for row in rows]])),
                    "maximum": int(np.max(fixed_scores[[row["label"] == label for row in rows]])),
                    "minimum_absolute": int(np.min(np.abs(
                        fixed_scores[[row["label"] == label for row in rows]]))),
                    "maximum_absolute": int(np.max(np.abs(
                        fixed_scores[[row["label"] == label for row in rows]]))),
                }
                for label in sorted(available_labels)
            },
            "recall_upper_bound_under_abs_score_rejection": {
                "ped": float(valid_report["ped"]["recall"]),
                "vehicle": float(valid_report["vehicle"]["recall"]),
                "explanation": (
                    "Changing abs(score)<T to invalid can only reject existing class decisions; "
                    "it cannot turn a ped/vehicle misclassification into the correct class."),
            },
        },
        "note": (
            "Consecutive frames are correlated. The binary model has no rejection path, so every "
            "invalid candidate is accepted. Ignore rows are excluded from metrics. No rejection "
            "threshold is selected while criteria remain suggested."),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    fields = list(records[0])
    with (args.output / "predictions.csv").open(
            "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(records)
    with (args.output / "failures.csv").open(
            "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(row for row in records if row["reason"])
    report["predictions_sha256"] = digest(args.output / "predictions.csv")
    (args.output / "metrics.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
