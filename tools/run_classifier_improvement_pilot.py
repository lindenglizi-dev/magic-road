#!/usr/bin/env python3
"""Run a fail-closed HOG324 classifier-improvement pilot.

The official train/validation ROIs are the only gold labels.  Historical CCL
candidate reviews are audited by their actual reviewer field.  Since the
current train candidate file contains annotation-assisted and Codex-generated
labels rather than verified human labels, formal augmented fits are blocked.
Two optional weak-label fits are still emitted as hypothesis-only diagnostics.

No test, blind, holdout, or reserve path is read.  No recursive public_data
search is performed.  C and all preprocessing choices are fixed in this file.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable

import cv2
import numpy as np
import sklearn
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
EXTERNAL = PROJECT / "external_reference_exploration"
if str(EXTERNAL) not in sys.path:
    sys.path.insert(0, str(EXTERNAL))

from opencv_hog_candidate_diagnostic import (  # noqa: E402
    extract_variant,
    load_models,
    make_hog324,
    model_score,
)


DATASET = PROJECT / "road_roi_dataset_virat"
MODEL_DIR = PROJECT / "external_reference_exploration/results/opencv_hog_diagnostic"
TRAIN_CANDIDATES = PROJECT / "evaluation/candidates/virat_000201_60f"
VAL_CANDIDATES = (
    ("virat_000200_f608_627", "virat-ground-000200"),
    ("virat_000200_f1840_1859", "virat-ground-000200"),
    ("virat_000203_f600_619", "virat-ground-000203"),
)
DEFAULT_OUTPUT = PROJECT / "evaluation/classifier_improvement_v1"

EXPECTED_SCENES = {
    "train": {"virat-ground-000201", "virat-ground-000206"},
    "val": {"virat-ground-000200", "virat-ground-000203"},
}
EXPECTED_GT_COUNTS = {"train": 360, "val": 69}
EXPECTED_CANDIDATE_COUNTS = {"train": 88, "val": 70}
LABELS = ("ped", "vehicle", "invalid")
SEED = 20260927
MIN_TRACK_GAP = 30
FORBIDDEN = re.compile(r"(^|[_\-.])(test|blind|holdout|reserve)($|[_\-.])", re.I)
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def guard_path(path: Path, role: str) -> None:
    for part in path.resolve().parts:
        if FORBIDDEN.search(part):
            raise ValueError(f"sealed-data guard rejected {role} path component: {part}")


def read_csv(path: Path) -> list[dict[str, str]]:
    guard_path(path, "CSV")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def pixel_hash(roi: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(roi, dtype=np.uint8).tobytes()).hexdigest()


def load_gray32(path: Path, expected_hash: str, role: str) -> np.ndarray:
    guard_path(path, role)
    if not path.is_file():
        raise ValueError(f"missing {role}: {path}")
    with Image.open(path) as image:
        if image.size != (32, 32):
            raise ValueError(f"{role} is not 32x32: {path} -> {image.size}")
        roi = np.asarray(image.convert("L"), dtype=np.uint8)
    actual = pixel_hash(roi)
    if expected_hash and actual != expected_hash:
        raise ValueError(f"{role} pixel hash mismatch: {path}")
    return roi


def reviewer_kind(reviewer: str, basis: str) -> str:
    reviewer_l = reviewer.strip().lower()
    basis_l = basis.strip().lower()
    if reviewer_l.startswith("codex_"):
        return "ai_visual_reference"
    if reviewer_l.startswith("official_annotation_") or "annotation_overlap" in basis_l:
        return "official_annotation_assisted_reference"
    if reviewer_l:
        return "unverified_reviewer"
    return "missing_reviewer"


def verify_review_receipt(root: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    reviewed = root / "reviewed/reviewed_candidates.csv"
    summary_path = root / "reviewed/review_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("candidate_count") != len(rows):
        raise ValueError(f"candidate count/receipt mismatch: {root}")
    if summary.get("reviewed_candidates_sha256") != sha256_file(reviewed):
        raise ValueError(f"reviewed candidate receipt hash mismatch: {root}")
    expected_manual = summary.get("manual_decisions_sha256")
    manual = root / "manual_decisions.json"
    if expected_manual:
        if not manual.is_file() or sha256_file(manual) != expected_manual:
            raise ValueError(f"manual decision receipt mismatch: {root}")
    expected_matches = summary.get("matches_sha256")
    matches = root / "annotation_overlap/candidate_matches.csv"
    if expected_matches:
        if not matches.is_file() or sha256_file(matches) != expected_matches:
            raise ValueError(f"annotation match receipt mismatch: {root}")
    return {
        "root": str(root),
        "reviewed_csv": str(reviewed),
        "reviewed_csv_sha256": sha256_file(reviewed),
        "summary": str(summary_path),
        "summary_sha256": sha256_file(summary_path),
        "manual_decisions_sha256": sha256_file(manual) if manual.is_file() else None,
        "annotation_matches_sha256": sha256_file(matches) if matches.is_file() else None,
    }


def load_gt() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest_path = DATASET / "manifest.csv"
    rows = read_csv(manifest_path)
    required = {"sample_id", "split", "label", "scene_id", "roi_source",
                "roi_path", "roi_sha256", "frame_index", "reviewer"}
    if required - set(rows[0]):
        raise ValueError(f"manifest missing fields: {sorted(required - set(rows[0]))}")
    if len(rows) != sum(EXPECTED_GT_COUNTS.values()):
        raise ValueError(f"expected 429 train/val GT rows, got {len(rows)}")
    records: list[dict[str, Any]] = []
    for row in rows:
        split = row["split"].strip().lower()
        if split not in EXPECTED_SCENES:
            raise ValueError(f"sealed-data guard rejected manifest split={split!r}")
        if row["scene_id"] not in EXPECTED_SCENES[split]:
            raise ValueError(f"unexpected {split} scene: {row['scene_id']}")
        if row["label"] not in ("ped", "vehicle") or row["roi_source"] != "annotated":
            raise ValueError(f"non-official GT row: {row['sample_id']}")
        if not HEX64.fullmatch(row["roi_sha256"]):
            raise ValueError(f"invalid ROI hash: {row['sample_id']}")
        roi_path = DATASET / row["roi_path"]
        roi = load_gray32(roi_path, row["roi_sha256"], "official GT ROI")
        records.append({
            "sample_id": row["sample_id"], "split": split, "truth": row["label"],
            "scene_id": row["scene_id"], "frame_index": int(row["frame_index"]),
            "source_kind": "official_gt_roi", "review_basis": "official_annotation",
            "reviewer": row["reviewer"], "reviewer_kind": "official_annotation_gold",
            "roi_path": str(roi_path), "roi_sha256": row["roi_sha256"], "roi": roi,
        })
    counts = Counter(record["split"] for record in records)
    if dict(counts) != EXPECTED_GT_COUNTS:
        raise ValueError(f"unexpected official GT split counts: {dict(counts)}")
    return records, {
        "manifest": str(manifest_path), "manifest_sha256": sha256_file(manifest_path),
        "count": len(records), "split_counts": dict(sorted(counts.items())),
        "label_counts": dict(sorted(Counter(r["truth"] for r in records).items())),
        "scene_counts": dict(sorted(Counter(r["scene_id"] for r in records).items())),
    }


def load_candidate_set(root: Path, scene_id: str, split: str,
                       set_name: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reviewed_path = root / "reviewed/reviewed_candidates.csv"
    rows = read_csv(reviewed_path)
    receipt = verify_review_receipt(root, rows)
    records: list[dict[str, Any]] = []
    for row in rows:
        truth = row.get("label", "").strip().lower()
        if truth not in LABELS:
            raise ValueError(f"unknown candidate reference label: {truth!r}")
        expected = row.get("roi_sha256", "").strip().lower()
        if not HEX64.fullmatch(expected):
            raise ValueError(f"invalid candidate ROI hash: {row.get('candidate_id')}")
        roi_path = root / row["roi_path"]
        roi = load_gray32(roi_path, expected, "candidate ROI")
        reviewer = row.get("reviewer", "").strip()
        basis = row.get("review_basis", "").strip()
        records.append({
            "sample_id": f"{set_name}:{row['candidate_id']}", "candidate_id": row["candidate_id"],
            "candidate_set": set_name, "split": split, "truth": truth,
            "scene_id": scene_id, "frame_index": int(row["source_frame"]),
            "source_kind": "ccl_candidate_reference", "review_basis": basis,
            "reviewer": reviewer, "reviewer_kind": reviewer_kind(reviewer, basis),
            "review_note": row.get("review_note", ""),
            "best_annotation_object_id": row.get("best_annotation_object_id", "").strip(),
            "best_annotation_iou": row.get("best_annotation_iou", "").strip(),
            "bbox": tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax")),
            "roi_path": str(roi_path), "roi_sha256": expected, "roi": roi,
        })
    audit = {
        **receipt, "set_name": set_name, "scene_id": scene_id, "split": split,
        "raw_count": len(records),
        "label_counts": dict(sorted(Counter(r["truth"] for r in records).items())),
        "basis_counts": dict(sorted(Counter(r["review_basis"] for r in records).items())),
        "reviewer_counts": dict(sorted(Counter(r["reviewer"] for r in records).items())),
        "reviewer_kind_counts": dict(sorted(Counter(r["reviewer_kind"] for r in records).items())),
        "verified_human_count": 0,
        "label_status": "reference_only_not_verified_human_gold",
    }
    return records, audit


def iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    intersection = max(0, x1 - x0 + 1) * max(0, y1 - y0 + 1)
    area_a = (a[2] - a[0] + 1) * (a[3] - a[1] + 1)
    area_b = (b[2] - b[0] + 1) * (b[3] - b[1] + 1)
    return intersection / (area_a + area_b - intersection) if intersection else 0.0


def assign_tracks(records: list[dict[str, Any]]) -> None:
    """Assign existing annotation IDs first, then conservative geometry tracks."""
    active: dict[str, list[dict[str, Any]]] = defaultdict(list)
    next_id: Counter[str] = Counter()
    for record in sorted(records, key=lambda item: (item["frame_index"], item["sample_id"])):
        object_id = record["best_annotation_object_id"]
        if object_id:
            record["track_key"] = f"annotation:{object_id}"
            continue
        label = record["truth"]
        candidates = [track for track in active[label]
                      if 0 <= record["frame_index"] - track["last_frame"] <= 5]
        scored = [(iou(record["bbox"], track["last_box"]), track) for track in candidates]
        score, chosen = max(scored, key=lambda pair: pair[0], default=(0.0, None))
        if chosen is None or score < 0.20:
            next_id[label] += 1
            chosen = {"key": f"geometry:{label}:{next_id[label]:02d}"}
            active[label].append(chosen)
        record["track_key"] = chosen["key"]
        chosen["last_frame"] = record["frame_index"]
        chosen["last_box"] = record["bbox"]


def thin_train_candidates(records: list[dict[str, Any]], gt_train_hashes: set[str]) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]]
]:
    assign_tracks(records)
    selected: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    last_frame: dict[tuple[str, str], int] = {}
    seen_pixels: set[str] = set()
    for record in sorted(records, key=lambda item: (item["frame_index"], item["sample_id"])):
        key = (record["truth"], record["track_key"])
        reason = "selected"
        if record["roi_sha256"] in gt_train_hashes:
            reason = "duplicate_of_official_train_gt_pixel_payload"
        elif record["roi_sha256"] in seen_pixels:
            reason = "duplicate_candidate_pixel_payload"
        elif key in last_frame and record["frame_index"] - last_frame[key] < MIN_TRACK_GAP:
            reason = f"same_track_gap_lt_{MIN_TRACK_GAP}"
        else:
            selected.append(record)
            seen_pixels.add(record["roi_sha256"])
            last_frame[key] = record["frame_index"]
        audit_rows.append({
            "sample_id": record["sample_id"], "label": record["truth"],
            "frame_index": record["frame_index"], "track_key": record["track_key"],
            "review_basis": record["review_basis"], "reviewer": record["reviewer"],
            "reviewer_kind": record["reviewer_kind"], "roi_sha256": record["roi_sha256"],
            "decision": "selected" if reason == "selected" else "excluded", "reason": reason,
        })
    return selected, audit_rows


def feature_matrix(records: list[dict[str, Any]], hog: cv2.HOGDescriptor) -> np.ndarray:
    return np.vstack([extract_variant(record["roi"], "opencv_hog324", hog)
                      for record in records])


def fit_linear(records: list[dict[str, Any]], classes: list[str],
               hog: cv2.HOGDescriptor) -> tuple[StandardScaler, LinearSVC, dict[str, Any]]:
    label_to_id = {label: index for index, label in enumerate(classes)}
    x = feature_matrix(records, hog)
    y = np.asarray([label_to_id[record["truth"]] for record in records], dtype=np.int64)
    scaler = StandardScaler().fit(x)
    classifier = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED,
                           max_iter=30000).fit(scaler.transform(x), y)
    if classifier.classes_.tolist() != list(range(len(classes))):
        raise ValueError(f"unexpected fitted classes: {classifier.classes_.tolist()}")
    payload = {
        "status": "hypothesis_only_weak_labels_not_acceptance",
        "classes": classes, "C": 1.0, "class_weight": "balanced",
        "random_state": SEED, "max_iter": 30000, "feature_count": 324,
        "train_count": len(records),
        "train_counts": dict(sorted(Counter(r["truth"] for r in records).items())),
        "scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist(),
        "coef_on_scaled_features": classifier.coef_.tolist(),
        "intercept_on_scaled_features": classifier.intercept_.tolist(),
        "n_iter": np.asarray(classifier.n_iter_).astype(int).tolist(),
    }
    payload["model_sha256"] = canonical_sha256(payload)
    return scaler, classifier, payload


def metric_block(rows: list[dict[str, Any]], predictions: list[str]) -> dict[str, Any]:
    if len(rows) != len(predictions):
        raise ValueError("metric row/prediction length mismatch")
    result: dict[str, Any] = {"raw_count": len(rows)}
    for label in ("ped", "vehicle"):
        truth_indices = [i for i, row in enumerate(rows) if row["truth"] == label]
        predicted_indices = [i for i, prediction in enumerate(predictions) if prediction == label]
        true_positive = sum(predictions[i] == label for i in truth_indices)
        result[label] = {
            "support": len(truth_indices), "predicted": len(predicted_indices),
            "correct": true_positive,
            "recall": true_positive / len(truth_indices) if truth_indices else None,
            "precision": (sum(rows[i]["truth"] == label for i in predicted_indices) /
                          len(predicted_indices)) if predicted_indices else None,
        }
    invalid_indices = [i for i, row in enumerate(rows) if row["truth"] == "invalid"]
    invalid_accepted = sum(predictions[i] != "invalid" for i in invalid_indices)
    result["invalid"] = {
        "support": len(invalid_indices), "false_accepts": invalid_accepted,
        "false_accept_rate": invalid_accepted / len(invalid_indices) if invalid_indices else None,
    }
    result["truth_counts"] = dict(sorted(Counter(r["truth"] for r in rows).items()))
    result["prediction_counts"] = dict(sorted(Counter(predictions).items()))
    return result


def evaluate_model(name: str, rows: list[dict[str, Any]], hog: cv2.HOGDescriptor,
                   predict: Callable[[np.ndarray], tuple[list[str], list[Any]]]) -> tuple[
    dict[str, Any], list[dict[str, Any]]
]:
    features = feature_matrix(rows, hog)
    predictions, scores = predict(features)
    groups: dict[str, Any] = {"overall": metric_block(rows, predictions), "by_scene": {}}
    for scene in sorted({row["scene_id"] for row in rows}):
        indices = [i for i, row in enumerate(rows) if row["scene_id"] == scene]
        groups["by_scene"][scene] = metric_block(
            [rows[i] for i in indices], [predictions[i] for i in indices]
        )
    failures: list[dict[str, Any]] = []
    for row, prediction, score in zip(rows, predictions, scores):
        failed = prediction != row["truth"]
        if failed:
            failures.append({
                "model": name, "evaluation_source": row["source_kind"],
                "scene_id": row["scene_id"], "sample_id": row["sample_id"],
                "frame_index": row["frame_index"], "truth": row["truth"],
                "prediction": prediction, "score": json.dumps(score, separators=(",", ":")),
                "review_basis": row["review_basis"], "reviewer": row["reviewer"],
                "reviewer_kind": row["reviewer_kind"], "roi_path": row["roi_path"],
                "roi_sha256": row["roi_sha256"],
            })
    return groups, failures


def binary_predictor(weights: np.ndarray, bias: float) -> Callable[[np.ndarray], tuple[list[str], list[Any]]]:
    def predict(features: np.ndarray) -> tuple[list[str], list[Any]]:
        scores = features @ weights + bias
        labels = ["vehicle" if score >= 0 else "ped" for score in scores]
        return labels, [float(score) for score in scores]
    return predict


def fitted_predictor(scaler: StandardScaler, classifier: LinearSVC,
                     classes: list[str]) -> Callable[[np.ndarray], tuple[list[str], list[Any]]]:
    def predict(features: np.ndarray) -> tuple[list[str], list[Any]]:
        transformed = scaler.transform(features)
        ids = classifier.predict(transformed)
        decision = classifier.decision_function(transformed)
        labels = [classes[int(index)] for index in ids]
        if np.asarray(decision).ndim == 1:
            scores: list[Any] = [float(value) for value in decision]
        else:
            scores = [[float(value) for value in row] for row in decision]
        return labels, scores
    return predict


def count_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    return {
        "count": len(rows),
        "by_label": dict(sorted(Counter(r["truth"] for r in rows).items())),
        "by_scene": dict(sorted(Counter(r["scene_id"] for r in rows).items())),
        "by_source": dict(sorted(Counter(r["source_kind"] for r in rows).items())),
        "by_reviewer_kind": dict(sorted(Counter(r["reviewer_kind"] for r in rows).items())),
    }


def duplicate_audit(train_gt: list[dict[str, Any]], train_raw: list[dict[str, Any]],
                    train_selected: list[dict[str, Any]], val_gt: list[dict[str, Any]],
                    val_candidates: list[dict[str, Any]]) -> dict[str, Any]:
    def hashes(rows: list[dict[str, Any]]) -> set[str]:
        return {row["roi_sha256"] for row in rows}

    val_all = hashes(val_gt) | hashes(val_candidates)
    checks = {
        "official_train_vs_official_val": hashes(train_gt) & hashes(val_gt),
        "official_train_vs_all_val": hashes(train_gt) & val_all,
        "raw_train_ccl_vs_all_val": hashes(train_raw) & val_all,
        "selected_train_ccl_vs_all_val": hashes(train_selected) & val_all,
    }
    return {
        "contract": "SHA256 of canonical 32x32 uint8 grayscale pixel payload",
        "intersections": {name: sorted(values) for name, values in checks.items()},
        "intersection_counts": {name: len(values) for name, values in checks.items()},
        "selected_training_cross_split_duplicate_free": not checks["official_train_vs_all_val"]
        and not checks["selected_train_ccl_vs_all_val"],
    }


def review_queue_rows(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered_raw = sorted(selected, key=lambda row: (row["frame_index"], row["sample_id"]))
    output = []
    for record in sorted(ordered_raw, key=lambda row: (row["truth"] != "invalid",
                                                         row["frame_index"], row["sample_id"])):
        frame = record["frame_index"]
        overlay_index = min(5, max(1, (frame - 4) // 12 + 1))
        output.append({
            "priority": "1_invalid_first" if record["truth"] == "invalid" else "2_valid",
            "sample_id": record["sample_id"], "weak_reference_label": record["truth"],
            "frame_index": frame, "track_key": record["track_key"],
            "current_reviewer": record["reviewer"], "current_review_basis": record["review_basis"],
            "roi_path": record["roi_path"],
            "frame_overlay_path": str(TRAIN_CANDIDATES / f"frame_overlay_{overlay_index:02d}.jpg"),
            "human_label": "", "human_reviewer": "", "human_reviewed_at": "",
            "human_note": "",
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-weak-label-hypothesis", action="store_true",
                        help="only audit and run frozen model A")
    args = parser.parse_args()
    output = args.output.resolve()
    guard_path(output, "output")
    if output.exists():
        raise ValueError(f"output already exists; use a new vN directory: {output}")

    gt, gt_receipt = load_gt()
    train_gt = [row for row in gt if row["split"] == "train"]
    val_gt = [row for row in gt if row["split"] == "val"]

    train_ccl, train_ccl_audit = load_candidate_set(
        TRAIN_CANDIDATES, "virat-ground-000201", "train", "virat_000201_60f"
    )
    if len(train_ccl) != EXPECTED_CANDIDATE_COUNTS["train"]:
        raise ValueError(f"expected 88 train candidates, got {len(train_ccl)}")
    val_ccl: list[dict[str, Any]] = []
    val_audits = []
    for name, scene in VAL_CANDIDATES:
        rows, audit = load_candidate_set(PROJECT / "evaluation/candidates" / name,
                                         scene, "val", name)
        val_ccl.extend(rows)
        val_audits.append(audit)
    if len(val_ccl) != EXPECTED_CANDIDATE_COUNTS["val"]:
        raise ValueError(f"expected 70 validation candidates, got {len(val_ccl)}")

    selected_ccl, thinning_rows = thin_train_candidates(
        train_ccl, {row["roi_sha256"] for row in train_gt}
    )
    duplicates = duplicate_audit(train_gt, train_ccl, selected_ccl, val_gt, val_ccl)
    if not duplicates["selected_training_cross_split_duplicate_free"]:
        raise ValueError("pixel-payload duplicate leakage crosses train/validation")

    output.mkdir(parents=True)
    write_csv(output / "train_ccl_thinning_audit.csv", thinning_rows,
              ["sample_id", "label", "frame_index", "track_key", "review_basis",
               "reviewer", "reviewer_kind", "roi_sha256", "decision", "reason"])
    queue = review_queue_rows(selected_ccl)
    write_csv(output / "train_candidate_human_review_queue.csv", queue,
              ["priority", "sample_id", "weak_reference_label", "frame_index", "track_key",
               "current_reviewer", "current_review_basis", "roi_path", "frame_overlay_path",
               "human_label", "human_reviewer", "human_reviewed_at", "human_note"])

    parameters, model_report, model_receipt = load_models(MODEL_DIR)
    baseline = parameters["opencv_hog324"]
    baseline_weights = np.asarray(baseline["folded_weights_on_raw_features"], dtype=np.float64)
    baseline_bias = float(baseline["folded_bias_on_raw_features"])
    hog = make_hog324()

    evaluation_sets = {"official_gt_val69": val_gt, "candidate_reference_val70": val_ccl}
    models: dict[str, dict[str, Any]] = {
        "A_frozen_gt_binary": {
            "status": "existing_fixed_C1_binary_reference",
            "classes": ["ped", "vehicle"],
            "model_parameters_sha256": model_receipt["model_parameters_sha256"],
            "training": "existing official GT train360 only",
        }
    }
    predictors: dict[str, Callable[[np.ndarray], tuple[list[str], list[Any]]]] = {
        "A_frozen_gt_binary": binary_predictor(baseline_weights, baseline_bias)
    }

    formal_augmented = {
        "B_gt_plus_human_ccl_binary": "blocked_no_verified_human_train_ccl_labels",
        "C_gt_plus_human_ccl_invalid_three_class": "blocked_no_verified_human_train_ccl_labels",
    }
    weak_models: dict[str, Any] = {}
    if not args.skip_weak_label_hypothesis:
        selected_valid = [row for row in selected_ccl if row["truth"] in ("ped", "vehicle")]
        selected_all = [row for row in selected_ccl if row["truth"] in LABELS]
        scaler_b, classifier_b, payload_b = fit_linear(
            train_gt + selected_valid, ["ped", "vehicle"], hog
        )
        scaler_c, classifier_c, payload_c = fit_linear(
            train_gt + selected_all, ["ped", "vehicle", "invalid"], hog
        )
        weak_models = {
            "B_weak_annotation_ai_binary": payload_b,
            "C_weak_annotation_ai_three_class": payload_c,
        }
        models.update(weak_models)
        predictors.update({
            "B_weak_annotation_ai_binary": fitted_predictor(
                scaler_b, classifier_b, ["ped", "vehicle"]
            ),
            "C_weak_annotation_ai_three_class": fitted_predictor(
                scaler_c, classifier_c, ["ped", "vehicle", "invalid"]
            ),
        })
        dump_json(output / "weak_models.json", weak_models)

    all_metrics: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    for model_name, predictor in predictors.items():
        model_metrics = {}
        for eval_name, rows in evaluation_sets.items():
            block, model_failures = evaluate_model(model_name, rows, hog, predictor)
            model_metrics[eval_name] = block
            failures.extend(model_failures)
            for group_name, group in [("overall", block["overall"]), *block["by_scene"].items()]:
                metric_rows.append({
                    "model": model_name, "evaluation_set": eval_name,
                    "group": group_name, "raw_count": group["raw_count"],
                    "ped_support": group["ped"]["support"],
                    "ped_precision": group["ped"]["precision"],
                    "ped_recall": group["ped"]["recall"],
                    "vehicle_support": group["vehicle"]["support"],
                    "vehicle_precision": group["vehicle"]["precision"],
                    "vehicle_recall": group["vehicle"]["recall"],
                    "invalid_support": group["invalid"]["support"],
                    "invalid_false_accepts": group["invalid"]["false_accepts"],
                    "invalid_false_accept_rate": group["invalid"]["false_accept_rate"],
                })
        all_metrics[model_name] = model_metrics

    metric_fields = ["model", "evaluation_set", "group", "raw_count", "ped_support",
                     "ped_precision", "ped_recall", "vehicle_support", "vehicle_precision",
                     "vehicle_recall", "invalid_support", "invalid_false_accepts",
                     "invalid_false_accept_rate"]
    write_csv(output / "metrics_by_source_scene.csv", metric_rows, metric_fields)
    failure_fields = ["model", "evaluation_source", "scene_id", "sample_id", "frame_index",
                      "truth", "prediction", "score", "review_basis", "reviewer",
                      "reviewer_kind", "roi_path", "roi_sha256"]
    write_csv(output / "failures.csv", failures, failure_fields)

    human_audit = {
        "train_candidate_conclusion": "not_verified_human_labels",
        "reason": (
            "66 train rows are official-annotation-overlap assisted; 22 are labeled by "
            "codex_visual_review_2026-09-27. No user or named human confirmation receipt exists."
        ),
        "historical_human_visual_review_field": (
            "provenance category only; contradicted by reviewer=codex_visual_review_2026-09-27"
        ),
        "train": train_ccl_audit,
        "validation": val_audits,
        "validation_label_boundary": (
            "All val70 candidate labels are reference labels, not verified human gold: "
            "6 annotation-assisted and 64 Codex visual labels."
        ),
        "formal_augmented_models": formal_augmented,
    }
    dump_json(output / "human_label_audit.json", human_audit)
    dump_json(output / "duplicate_audit.json", duplicates)
    dump_json(output / "metrics.json", all_metrics)

    report = {
        "status": "completed_with_formal_B_C_blocked_and_weak_hypothesis_isolated",
        "scope": {
            "production_rtl_changed": False,
            "feature": "OpenCV HOG324 fixed descriptor",
            "C": 1.0, "hyperparameter_tuning": False, "threshold_selection": False,
            "official_gold": "train360/val69 from scenes 000201/000206 and 000200/000203",
            "candidate_validation": "existing val70 reference labels only; not human gold",
            "new_intersection_ai60_used": False,
            "test_blind_holdout_reserve": "fail-closed path guards; not read",
            "public_data": "no recursive search and no source video read",
        },
        "decisions": {
            "A": "evaluated existing frozen binary model",
            "formal_B": formal_augmented["B_gt_plus_human_ccl_binary"],
            "formal_C": formal_augmented["C_gt_plus_human_ccl_invalid_three_class"],
            "weak_B_C": "hypothesis_only_not_acceptance" if weak_models else "skipped_by_cli",
            "required_next_step": (
                "A real person must complete train_candidate_human_review_queue.csv and a "
                "hash-bound finalization receipt before candidate labels may enter formal training."
            ),
        },
        "counts": {
            "official_gt": gt_receipt,
            "train_candidate_raw": count_summary(train_ccl),
            "train_candidate_selected_after_track_gap_and_pixel_dedup": count_summary(selected_ccl),
            "validation_candidate_raw": count_summary(val_ccl),
            "review_queue": count_summary(selected_ccl),
        },
        "label_provenance": human_audit,
        "duplicate_audit": duplicates,
        "models": models,
        "metrics": all_metrics,
        "inputs": {
            "dataset_manifest": gt_receipt,
            "baseline_model": model_receipt,
            "baseline_model_status": model_report["models"]["opencv_hog324"]["status"]
            if "status" in model_report.get("models", {}).get("opencv_hog324", {}) else
            "existing_external_reference_diagnostic",
        },
        "implementation": {
            "script": str(SCRIPT), "script_sha256": sha256_file(SCRIPT),
            "python": platform.python_version(), "opencv": cv2.__version__,
            "numpy": np.__version__, "scikit_learn": sklearn.__version__,
            "seed": SEED, "min_same_track_frame_gap": MIN_TRACK_GAP,
        },
        "artifacts": {
            "human_label_audit": "human_label_audit.json",
            "duplicate_audit": "duplicate_audit.json",
            "thinning_audit": "train_ccl_thinning_audit.csv",
            "human_review_queue": "train_candidate_human_review_queue.csv",
            "metrics": "metrics.json", "metrics_table": "metrics_by_source_scene.csv",
            "failures": "failures.csv",
            "weak_models": "weak_models.json" if weak_models else None,
        },
        "limitations": [
            "The candidate windows contain adjacent correlated frames; raw candidate counts are not independent samples.",
            "The weak B/C fits use annotation-assisted and AI-generated labels and cannot support acceptance, freezing, or human-ground-truth claims.",
            "The val70 candidate labels are also reference labels rather than verified human gold.",
            "The three-class invalid evidence is tiny after the required 30-frame track thinning and exact-pixel deduplication.",
            "OpenCV HOG324 remains a floating-point descriptor and is not an integer or RTL-equivalent HOG implementation.",
            "Decision scores are margins, not probabilities.",
        ],
    }
    report_path = output / "report.json"
    dump_json(report_path, report)
    artifacts = {
        path.name: sha256_file(path) for path in sorted(output.iterdir())
        if path.is_file() and path.name != "artifact_hashes.json"
    }
    dump_json(output / "artifact_hashes.json", artifacts)
    print(json.dumps({
        "status": report["status"], "output": str(output),
        "selected_train_ccl": count_summary(selected_ccl),
        "formal_augmented_models": formal_augmented,
        "metrics": all_metrics,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
