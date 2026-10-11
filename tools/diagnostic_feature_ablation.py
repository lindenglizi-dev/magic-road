#!/usr/bin/env python3
"""Compare small feature-capacity variants without opening test or blind data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from hog_reference import direction_bin, extract_features
from road_evaluation import LABELS, audit_dataset
from train_hog_svm import rtl_gray, rtl_resize_32
from candidate_review_io import load_reviewed

VALID_LABELS = {"ped", "vehicle"}


WIDTH, HEIGHT = 256, 144


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def spatial(roi: np.ndarray, cell_x_shift: int, cell_y_shift: int) -> list[int]:
    cells_x = 32 >> cell_x_shift
    cells_y = 32 >> cell_y_shift
    features = [0] * (cells_x * cells_y * 4)
    for y in range(1, 31):
        for x in range(1, 31):
            left = int(roi[y - 1, x - 1]) + 2 * int(roi[y, x - 1]) + int(roi[y + 1, x - 1])
            right = int(roi[y - 1, x + 1]) + 2 * int(roi[y, x + 1]) + int(roi[y + 1, x + 1])
            upper = int(roi[y - 1, x - 1]) + 2 * int(roi[y - 1, x]) + int(roi[y - 1, x + 1])
            lower = int(roi[y + 1, x - 1]) + 2 * int(roi[y + 1, x]) + int(roi[y + 1, x + 1])
            gx, gy = right - left, lower - upper
            magnitude = min(abs(gx) + abs(gy), 0x7ff)
            index = ((y >> cell_y_shift) * cells_x * 4 +
                     (x >> cell_x_shift) * 4 + direction_bin(gx, gy))
            features[index] += magnitude
    return features


def geometry(width: int, height: int) -> list[int]:
    return [width, height, (256 * width) // max(1, height),
            (256 * height) // max(1, width)]


def feature(roi: np.ndarray, width: int, height: int, variant: str) -> list[int]:
    base64 = extract_features(roi.astype(int).tolist())[0]
    if variant == "rtl64":
        return base64
    if variant == "rtl64_geometry4":
        return base64 + geometry(width, height)
    if variant.startswith("spatial128_x"):
        dense = spatial(roi, 2, 3)
    elif variant.startswith("spatial128_y"):
        dense = spatial(roi, 3, 2)
    else:
        dense = spatial(roi, 2, 2)
    if variant in {"spatial128_x", "spatial128_y", "spatial256"}:
        return dense
    if variant in {"spatial128_x_geometry4", "spatial128_y_geometry4",
                   "spatial256_geometry4"}:
        return dense + geometry(width, height)
    raise ValueError(variant)


def read_frame(path: Path) -> np.ndarray:
    values = np.asarray([int(value, 16) for value in path.read_text(
        encoding="ascii").splitlines()], dtype=np.uint8)
    if values.size != WIDTH * HEIGHT:
        raise ValueError(f"bad analysis frame: {path}")
    return values.reshape(HEIGHT, WIDTH)


def metrics(truth: np.ndarray, prediction: np.ndarray) -> dict:
    return {
        "confusion_matrix": confusion_matrix(truth, prediction, labels=[0, 1]).tolist(),
        "classes": classification_report(
            truth, prediction, labels=[0, 1], target_names=["ped", "vehicle"],
            output_dict=True, zero_division=0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--val-review-set", nargs=3, action="append", required=True,
                        metavar=("FRAME_ROOT", "CANDIDATE_ROOT", "REVIEWED"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = audit_dataset(args.dataset)
    train_rows = [row for row in rows if row["split"] == "train" and
                  row["roi_source"] == "annotated" and row["label"] in VALID_LABELS]
    val_rows = [row for row in rows if row["split"] == "val" and
                row["roi_source"] == "annotated" and row["label"] in VALID_LABELS]

    def annotated_samples(selected: list[dict]) -> list[tuple[np.ndarray, int, int]]:
        result = []
        for row in selected:
            with Image.open(args.dataset / row["crop_path"]) as image:
                gray = rtl_gray(image)
            result.append((np.asarray(rtl_resize_32(gray), dtype=np.uint8),
                           int(row["xmax"]) - int(row["xmin"]) + 1,
                           int(row["ymax"]) - int(row["ymin"]) + 1))
        return result

    train_samples = annotated_samples(train_rows)
    val_samples = annotated_samples(val_rows)
    ccl_rows, ccl_samples, review_receipts = [], [], []
    frame_cache: dict[Path, np.ndarray] = {}
    for frame_root_text, candidate_root_text, reviewed_text in args.val_review_set:
        frame_root, candidate_root, reviewed = (Path(frame_root_text),
                                                Path(candidate_root_text), Path(reviewed_text))
        all_rows, set_receipt = load_reviewed(candidate_root, reviewed, "val", frame_root)
        set_rows = [row for row in all_rows if row["label"] in VALID_LABELS]
        for row in set_rows:
            frame_path = frame_root / f'frame_{int(row["replay_frame"]):04d}.hex'
            if frame_path not in frame_cache:
                frame_cache[frame_path] = read_frame(frame_path)
            gray = frame_cache[frame_path]
            x0, y0, x1, y1 = (int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
            raw = gray[y0:y1 + 1, x0:x1 + 1]
            ccl_samples.append((np.asarray(rtl_resize_32(raw), dtype=np.uint8),
                                x1 - x0 + 1, y1 - y0 + 1))
        ccl_rows.extend(set_rows)
        review_receipts.append({**set_receipt, "valid_count": len(set_rows)})

    y_train = np.asarray([LABELS[row["label"]] for row in train_rows])
    y_val = np.asarray([LABELS[row["label"]] for row in val_rows])
    y_ccl = np.asarray([LABELS[row["label"]] for row in ccl_rows])
    variants = ("rtl64", "rtl64_geometry4",
                "spatial128_x", "spatial128_x_geometry4",
                "spatial128_y", "spatial128_y_geometry4",
                "spatial256", "spatial256_geometry4")
    results = []
    for variant in variants:
        x_train = np.asarray([feature(*sample, variant) for sample in train_samples], dtype=np.int64)
        x_val = np.asarray([feature(*sample, variant) for sample in val_samples], dtype=np.int64)
        x_ccl = np.asarray([feature(*sample, variant) for sample in ccl_samples], dtype=np.int64)
        scaler = StandardScaler().fit(x_train)
        classifier = LinearSVC(C=1.0, class_weight="balanced", random_state=20260927,
                               max_iter=30000).fit(scaler.transform(x_train), y_train)
        results.append({
            "variant": variant,
            "feature_count": int(x_train.shape[1]),
            "annotated_validation": metrics(y_val, classifier.predict(scaler.transform(x_val))),
            "ccl_validation": metrics(y_ccl, classifier.predict(scaler.transform(x_ccl))),
        })
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "python_feature_capacity_diagnostic_not_rtl_or_acceptance_evidence",
        "fixed_conditions": "32x32 stretch, C=1.0, annotated train only, unchanged scene split",
        "train_count": len(train_rows), "annotated_validation_count": len(val_rows),
        "ccl_validation_count": len(ccl_rows),
        "variants": results,
        "dataset_manifest_sha256": digest(args.dataset / "manifest.csv"),
        "review_sets": review_receipts,
        "limitations": [
            "The 256-feature variants have no RTL implementation or bit-width proof.",
            "Geometry features can expose candidate-box shape but do not repair fragmented boxes.",
            (f"Validation CCL rows are {len(review_receipts)} short correlated windows from "
             f"{len({receipt['scene_id'] for receipt in review_receipts})} scene(s)."),
            "No invalid rejection, test data, or blind reserve data are used.",
        ],
    }
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "variants": [{
        "variant": item["variant"], "feature_count": item["feature_count"],
        "annotated_ped_recall": item["annotated_validation"]["classes"]["ped"]["recall"],
        "annotated_vehicle_recall": item["annotated_validation"]["classes"]["vehicle"]["recall"],
        "ccl_ped_recall": item["ccl_validation"]["classes"]["ped"]["recall"],
        "ccl_vehicle_recall": item["ccl_validation"]["classes"]["vehicle"]["recall"],
    } for item in results]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
