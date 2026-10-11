"""Manifest-audited, validation-only tuning and frozen-test road ROI evaluation."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

LABELS = {"ped": 0, "vehicle": 1, "invalid": -1}
PREPROCESSING = "rtl_shift_gray_stride5_v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")


def audit_dataset(root: Path) -> list[dict]:
    """Reject source/scene/pixel leakage and untraceable or altered ROIs."""
    root = root.resolve()
    with (root / "manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("empty manifest")
    owners: dict[tuple[str, str], str] = {}
    labels: dict[str, str] = {}
    sample_ids: set[str] = set()
    source_checks: dict[str, str] = {}
    for row in rows:
        for name in ("sample_id", "split", "label", "scene_id", "source_sha256",
                     "source_family", "source_video", "roi_source", "reviewer",
                     "roi_path", "roi_sha256", "frame_index", "xmin", "ymin", "xmax", "ymax"):
            if not row.get(name):
                raise ValueError(f"missing provenance field {name}")
        if row["sample_id"] in sample_ids:
            raise ValueError("duplicate sample_id")
        sample_ids.add(row["sample_id"])
        if row["split"] not in {"train", "val", "test"} or row["label"] not in LABELS:
            raise ValueError("invalid split/label")
        if row["roi_source"] not in {"manual", "annotated", "ccl"}:
            raise ValueError("unknown ROI source")
        if (row.get("source_width"), row.get("source_height"),
            row.get("analysis_width"), row.get("analysis_height")) != ("1280", "720", "256", "144"):
            raise ValueError("non-hardware dimensions in manifest")
        source = str(Path(row["source_video"]).resolve())
        if source not in source_checks:
            source_checks[source] = digest(Path(source))
        if source_checks[source] != row["source_sha256"]:
            raise ValueError("source video changed")
        for field in ("scene_id", "source_sha256", "source_family", "roi_sha256"):
            key = field, row[field]
            if key in owners and owners[key] != row["split"]:
                raise ValueError(f"cross-split leakage: {field}={row[field]}")
            owners[key] = row["split"]
        pixel_hash = row["roi_sha256"]
        if pixel_hash in labels and labels[pixel_hash] != row["label"]:
            raise ValueError("identical pixels have conflicting labels")
        labels[pixel_hash] = row["label"]
        path = (root / row["roi_path"]).resolve()
        if not path.is_relative_to(root):
            raise ValueError("ROI path escapes dataset")
        with Image.open(path) as image:
            if image.mode != "L" or image.size != (32, 32):
                raise ValueError("ROI must be native grayscale 32x32")
            if hashlib.sha256(np.asarray(image).tobytes()).hexdigest() != pixel_hash:
                raise ValueError(f"ROI pixels changed: {path}")
    return rows


def features_for(root: Path, rows: list[dict]) -> np.ndarray:
    from train_hog_svm import image_features
    return np.asarray([image_features(root / row["roi_path"]) for row in rows], dtype=np.int64)


def report(rows: list[dict], scores: np.ndarray) -> dict:
    valid = np.asarray([r["label"] != "invalid" for r in rows])
    truth = np.asarray([LABELS[r["label"]] for r in rows])
    predicted = (scores >= 0).astype(int)
    return {
        "count": len(rows),
        "class_counts": {name: sum(r["label"] == name for r in rows) for name in LABELS},
        "accuracy": float(np.mean(truth[valid] == predicted[valid])) if valid.any() else None,
        "classes": classification_report(truth[valid], predicted[valid], labels=[0, 1],
                     target_names=["ped", "vehicle"], output_dict=True, zero_division=0)
                     if valid.any() else None,
        "confusion_matrix": confusion_matrix(truth[valid], predicted[valid], labels=[0, 1]).tolist(),
        "invalid_forced_predictions": {name: int(np.sum((truth == -1) & (predicted == code)))
                                        for name, code in (("ped", 0), ("vehicle", 1))},
        "invalid_false_accept_rate": 1.0 if (truth == -1).any() else None,
        "note": "Binary baseline has no rejection; every invalid candidate is accepted. Scores are not probabilities.",
    }


def evaluate(root: Path, rows: list[dict], model: dict, output: Path, split: str) -> dict:
    selected = [r for r in rows if r["split"] == split]
    if not selected:
        raise ValueError(f"no {split} samples")
    x = features_for(root, selected)
    floating_scores = x @ np.asarray(model["float_folded_weights"]) + model["float_folded_bias"]
    quantized_scores = x @ np.asarray(model["quantized_weights"], dtype=np.int64) + model["quantized_bias"]
    result = {"split": split, "preprocessing": PREPROCESSING,
              "model_sha256": digest(output / "model.json"), "by_roi_source": {}}
    for kind in ("manual", "annotated", "ccl"):
        mask = np.asarray([r["roi_source"] == kind for r in selected])
        subset = [r for r in selected if r["roi_source"] == kind]
        result["by_roi_source"][kind] = {
            "float": report(subset, floating_scores[mask]),
            "quantized": report(subset, quantized_scores[mask]),
            "quantization_disagreements": int(np.sum(
                (floating_scores[mask] >= 0) != (quantized_scores[mask] >= 0))),
        } if subset else {"status": "not_measured", "count": 0}
    criteria = json.loads((output / "criteria.json").read_text(encoding="utf-8"))
    acceptance_source = criteria["acceptance_roi_source"]
    source_result = result["by_roi_source"][acceptance_source]
    checks: dict[str, object] = {}
    blockers: list[str] = []
    if source_result.get("status") == "not_measured":
        blockers.append(f"acceptance source {acceptance_source} is not measured")
    else:
        quantized_report = source_result["quantized"]
        ped_recall = quantized_report["classes"]["ped"]["recall"]
        vehicle_recall = quantized_report["classes"]["vehicle"]["recall"]
        invalid_far = quantized_report["invalid_false_accept_rate"]
        checks = {
            "ped_recall": {"actual": ped_recall, "required_min": criteria["ped_recall_min"],
                           "pass": ped_recall >= criteria["ped_recall_min"]},
            "vehicle_recall": {"actual": vehicle_recall,
                               "required_min": criteria["vehicle_recall_min"],
                               "pass": vehicle_recall >= criteria["vehicle_recall_min"]},
            "invalid_false_accept_rate": {
                "actual": invalid_far, "required_max": criteria["invalid_false_accept_max"],
                "pass": invalid_far is not None and invalid_far <= criteria["invalid_false_accept_max"]},
            "float_quantized_class_disagreements": {
                "actual": source_result["quantization_disagreements"], "required_max": 0,
                "pass": source_result["quantization_disagreements"] == 0},
        }
        blockers.extend(name for name, check in checks.items() if not check["pass"])
    checks["rtl_fixed_python_class_disagreements"] = {
        "actual": None, "required_max": criteria["rtl_python_class_disagreements_max"],
        "pass": False, "status": "not_measured_by_python_evaluation"}
    blockers.append("rtl_fixed_python_class_disagreements")
    result["acceptance"] = {
        "source": acceptance_source,
        "criteria_frozen": criteria.get("frozen") is True,
        "checks": checks,
        "model_metrics_pass": bool(checks) and all(
            check.get("pass") is True for name, check in checks.items()
            if name != "rtl_fixed_python_class_disagreements"),
        "integration_ready": False,
        "blockers": sorted(set(blockers)),
        "note": "freeze.json freezes artifacts; only this explicit criteria table reports acceptance",
    }
    fields = ["sample_id", "split", "roi_source", "scene_id", "source_video", "frame_index",
              "roi_path", "label", "float_score", "quantized_score", "prediction", "reason"]
    with (output / f"{split}_predictions.csv").open("w", encoding="utf-8-sig", newline="") as all_file, \
         (output / f"{split}_failures.csv").open("w", encoding="utf-8-sig", newline="") as failure_file:
        writers = [csv.DictWriter(file, fields) for file in (all_file, failure_file)]
        for writer in writers:
            writer.writeheader()
        for row, f, q in zip(selected, floating_scores, quantized_scores):
            predicted = "vehicle" if q >= 0 else "ped"
            reason = "invalid_candidate_forced_class" if row["label"] == "invalid" else (
                "misclassified" if predicted != row["label"] else "")
            if (f >= 0) != (q >= 0):
                reason += ";quantization_disagreement"
            record = {key: row[key] for key in fields if key in row}
            record.update(float_score=float(f), quantized_score=int(q), prediction=predicted, reason=reason)
            writers[0].writerow(record)
            if reason:
                writers[1].writerow(record)
    result["integration_status"] = "not_approved" if result["acceptance"]["blockers"] else "approved"
    write_json(output / f"{split}_metrics.json", result)
    write_json(output / "metrics.json", result)
    return result


def run(args) -> int:
    from train_hog_svm import export_rom, write_hex
    root, output = args.dataset.resolve(), args.output.resolve()
    rows = audit_dataset(root)
    dataset_hash = digest(root / "manifest.csv")
    if args.phase == "test":
        model = json.loads((output / "model.json").read_text(encoding="utf-8"))
        frozen = json.loads((output / "freeze.json").read_text(encoding="utf-8"))
        if frozen["manifest_sha256"] != dataset_hash or frozen["model_sha256"] != digest(output / "model.json"):
            raise ValueError("dataset/model changed after freeze; use a new experiment")
        for relative, expected in frozen["artifact_sha256"].items():
            if digest(output / relative) != expected:
                raise ValueError(f"frozen artifact changed: {relative}")
        if (output / "test_metrics.json").exists():
            raise ValueError("test already evaluated; do not tune against repeated test feedback")
        print(json.dumps(evaluate(root, rows, model, output, "test"), ensure_ascii=False, indent=2))
        return 0
    if output.exists() and any(output.iterdir()):
        raise ValueError("fit requires a new empty experiment directory")
    if args.criteria is None:
        raise ValueError("--criteria required before validation tuning; null values mean undecided, not pass")
    criteria = json.loads(args.criteria.read_text(encoding="utf-8"))
    if criteria.get("frozen") is not True:
        raise ValueError(
            "formal fit requires criteria.frozen=true; use a diagnostic-only fit without freeze/test")
    for key in ("ped_recall_min", "vehicle_recall_min", "invalid_false_accept_max"):
        if (key not in criteria or criteria[key] is None or
                not isinstance(criteria[key], (float, int)) or not 0 <= criteria[key] <= 1):
            raise ValueError(f"invalid criterion: {key}")
    if (not isinstance(criteria.get("rtl_python_class_disagreements_max"), int) or
            criteria["rtl_python_class_disagreements_max"] < 0):
        raise ValueError("invalid criterion: rtl_python_class_disagreements_max")
    if criteria.get("acceptance_roi_source") not in {"manual", "annotated", "ccl"}:
        raise ValueError("invalid criterion: acceptance_roi_source")
    train = [r for r in rows if r["split"] == "train" and r["roi_source"] == args.train_source and r["label"] != "invalid"]
    validation = [r for r in rows if r["split"] == "val" and r["roi_source"] == args.train_source and r["label"] != "invalid"]
    for name, subset in (("train", train), ("val", validation)):
        if {r["label"] for r in subset} != {"ped", "vehicle"}:
            raise ValueError(f"{name}/{args.train_source} needs both classes from independent scene groups")
    x_train, x_val = features_for(root, train), features_for(root, validation)
    y_train = np.asarray([LABELS[r["label"]] for r in train])
    y_val = np.asarray([LABELS[r["label"]] for r in validation])
    scaler = StandardScaler().fit(x_train)
    trials = []
    best = None
    for c in sorted(set(args.c_grid)):
        if not np.isfinite(c) or c <= 0:
            raise ValueError("C must be positive and finite")
        classifier = LinearSVC(C=c, class_weight="balanced", random_state=args.seed, max_iter=30000)
        classifier.fit(scaler.transform(x_train), y_train)
        score = float(balanced_accuracy_score(y_val, classifier.predict(scaler.transform(x_val))))
        trials.append({"C": c, "validation_balanced_accuracy": score})
        if best is None or score > best[0]:
            best = score, c, classifier
    classifier = best[2]
    weights = classifier.coef_[0] / scaler.scale_
    bias = float(classifier.intercept_[0] - np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_))
    scale = ((1 << (args.weight_bits - 1)) - 1) / float(np.max(np.abs(weights)))
    if not np.isfinite(scale):
        raise ValueError("zero/nonfinite weights")
    quant_weights = np.rint(weights * scale).astype(np.int64)
    quant_bias = int(round(bias * scale))
    bound = abs(quant_bias) + sum(abs(int(v)) for v in quant_weights) * (64 * 2040)
    if bound >= 1 << (args.accumulator_bits - 1) or bound >= 1 << 63:
        raise ValueError("accumulator/numpy integer overflow risk")
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "criteria.json", criteria)
    model = {"float_folded_weights": weights.tolist(), "float_folded_bias": bias,
             "quantized_weights": quant_weights.tolist(), "quantized_bias": quant_bias,
             "quantization_scale": scale, "weight_bits": args.weight_bits,
             "accumulator_bits": args.accumulator_bits, "worst_score_bound": bound,
             "C": best[1], "trials": trials, "train_source": args.train_source,
             "feature_order": "{cell_y,cell_x,bin}", "preprocessing": PREPROCESSING,
             "negative_class": "ped", "nonnegative_class": "vehicle", "reject_threshold": None}
    write_json(output / "model.json", model)
    export_rom(output / "hog_svm_weights.v", quant_weights, quant_bias, args.weight_bits, args.accumulator_bits)
    write_hex(output / "hog_svm_weights.hex", quant_weights, args.weight_bits)
    # Validation vector verifies the ROM/MAC without opening held-out test features.
    vector = x_val[0]
    expected = int(vector @ quant_weights + quant_bias)
    write_hex(output / "svm_test_feature.hex", vector, 18)
    write_hex(output / "svm_test_score.hex", np.asarray([expected]), args.accumulator_bits)
    write_hex(output / "svm_test_class.hex", np.asarray([2 if expected >= 0 else 1]), 2)
    artifacts = ["criteria.json", "hog_svm_weights.v", "hog_svm_weights.hex",
                 "svm_test_feature.hex", "svm_test_score.hex", "svm_test_class.hex"]
    write_json(output / "freeze.json", {"status": "artifact_freeze_only_not_acceptance",
               "manifest_sha256": dataset_hash,
               "model_sha256": digest(output / "model.json"),
               "artifact_sha256": {p: digest(output / p) for p in artifacts},
               "test_used_for_selection": False, "training_samples": len(train),
               "validation_samples": len(validation), "criteria_declared_before_tuning": True})
    print(json.dumps(evaluate(root, rows, model, output, "val"), ensure_ascii=False, indent=2))
    return 0
