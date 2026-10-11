#!/usr/bin/env python3
"""Evaluate uniform analysis-box padding before the deployed 32x32 feature path.

This is a Python-only diagnostic. Labels on valid ped/vehicle candidates remain
usable, while previously invalid crops require fresh review when padding brings a
real object into view.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from sklearn.metrics import classification_report, confusion_matrix

from hog_reference import extract_features
from train_hog_svm import rtl_resize_32
from candidate_review_io import load_reviewed


WIDTH, HEIGHT = 256, 144


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expanded_box(row: dict, padding: int) -> tuple[int, int, int, int]:
    return (max(0, int(row["xmin"]) - padding),
            max(0, int(row["ymin"]) - padding),
            min(WIDTH - 1, int(row["xmax"]) + padding),
            min(HEIGHT - 1, int(row["ymax"]) + padding))


def load_gray(path: Path) -> np.ndarray:
    values = np.asarray([int(value, 16) for value in path.read_text(
        encoding="ascii").splitlines()], dtype=np.uint8)
    if values.size != WIDTH * HEIGHT:
        raise ValueError(f"{path} has {values.size} pixels, expected {WIDTH * HEIGHT}")
    return values.reshape(HEIGHT, WIDTH)


def contact_sheet(items: list[dict], path: Path, padding: int) -> None:
    scale, tile_w, tile_h, columns = 3, 128, 132, 5
    rows = (len(items) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * tile_w, rows * tile_h), "white")
    draw = ImageDraw.Draw(canvas)
    for index, item in enumerate(items):
        x, y = (index % columns) * tile_w, (index // columns) * tile_h
        crop = Image.fromarray(item["roi"], mode="L").resize(
            (32 * scale, 32 * scale), Image.Resampling.NEAREST).convert("RGB")
        canvas.paste(crop, (x, y))
        draw.text((x, y + 98), item["candidate_id"][-18:], fill="black")
        draw.text((x, y + 111),
                  f'{item["label"]}->{item["prediction"]} q={item["fixed_score"]}',
                  fill="black")
    draw.text((4, max(0, canvas.height - 14)), f"uniform padding={padding}", fill="red")
    canvas.save(path, quality=92)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-set", nargs=3, action="append", required=True,
                        metavar=("NAME", "FRAME_ROOT", "REVIEWED"))
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--padding", type=int, nargs="+", default=[0, 2, 4, 6])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if any(value < 0 or value > 32 for value in args.padding):
        raise ValueError("padding must be in [0,32]")
    model = json.loads(args.model.read_text(encoding="utf-8"))
    float_weights = np.asarray(model["float_folded_weights"])
    float_bias = float(model["float_folded_bias"])
    fixed_weights = np.asarray(model["quantized_weights"], dtype=np.int64)
    fixed_bias = int(model["quantized_bias"])
    rows = []
    receipts = []
    frame_cache: dict[Path, np.ndarray] = {}
    for name, frame_root_text, reviewed_text in args.review_set:
        frame_root, reviewed = Path(frame_root_text), Path(reviewed_text)
        candidate_root = reviewed.resolve().parent.parent
        set_rows, set_receipt = load_reviewed(
            candidate_root, reviewed, "val", frame_root)
        for row in set_rows:
            row["_set"] = name
            row["_frame_root"] = str(frame_root)
        rows.extend(set_rows)
        receipts.append({"name": name, **set_receipt})
    args.output.mkdir(parents=True, exist_ok=True)
    padding_reports = []
    for padding in sorted(set(args.padding)):
        items = []
        for row in rows:
            frame_path = Path(row["_frame_root"]) / f'frame_{int(row["replay_frame"]):04d}.hex'
            if frame_path not in frame_cache:
                frame_cache[frame_path] = load_gray(frame_path)
            gray = frame_cache[frame_path]
            x0, y0, x1, y1 = expanded_box(row, padding)
            roi = np.asarray(rtl_resize_32(gray[y0:y1 + 1, x0:x1 + 1]), dtype=np.uint8)
            features = np.asarray(extract_features(roi.astype(int).tolist())[0], dtype=np.int64)
            float_score = float(features @ float_weights + float_bias)
            fixed_score = int(features @ fixed_weights + fixed_bias)
            items.append({
                "candidate_id": f'{row["_set"]}:{row["candidate_id"]}',
                "review_set": row["_set"], "source_frame": int(row["source_frame"]),
                "label": row["label"], "prediction": "vehicle" if fixed_score >= 0 else "ped",
                "float_prediction": "vehicle" if float_score >= 0 else "ped",
                "float_score": float_score, "fixed_score": fixed_score,
                "expanded_box": [x0, y0, x1, y1], "roi": roi,
            })
        valid = [item for item in items if item["label"] in {"ped", "vehicle"}]
        truth = np.asarray([0 if item["label"] == "ped" else 1 for item in valid])
        predictions = np.asarray([0 if item["prediction"] == "ped" else 1 for item in valid])
        class_metrics = classification_report(
            truth, predictions, labels=[0, 1], target_names=["ped", "vehicle"],
            output_dict=True, zero_division=0)
        contact_path = args.output / f"contact_padding_{padding:02d}.jpg"
        contact_sheet(items, contact_path, padding)
        csv_path = args.output / f"predictions_padding_{padding:02d}.csv"
        fields = ["candidate_id", "review_set", "source_frame", "label", "prediction",
                  "float_prediction", "float_score", "fixed_score", "expanded_box"]
        with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            for item in items:
                writer.writerow({key: item[key] for key in fields})
        padding_reports.append({
            "padding": padding,
            "valid_candidate_count": len(valid),
            "original_invalid_needs_re_review": sum(item["label"] == "invalid" for item in items),
            "class_counts": dict(sorted(Counter(item["label"] for item in valid).items())),
            "confusion_matrix": confusion_matrix(truth, predictions, labels=[0, 1]).tolist(),
            "classes": class_metrics,
            "float_fixed_class_disagreements": sum(
                item["prediction"] != item["float_prediction"] for item in items),
            "contact_sheet": contact_path.name,
            "contact_sheet_sha256": digest(contact_path),
            "predictions_sha256": digest(csv_path),
        })
    report = {
        "status": "python_padding_diagnostic_not_rtl_or_acceptance_evidence",
        "model_sha256": digest(args.model),
        "review_sets": receipts,
        "padding_results": padding_reports,
        "label_boundary": (
            "Padding changes every crop. Original invalid labels are excluded from metrics, and "
            "all padded ped/vehicle/invalid crops require fresh visual review before formal use. "
            "Reported ped/vehicle recalls are sensitivity diagnostics only."),
        "selection_boundary": (
            "Criteria remain suggested, so this report diagnoses sensitivity and does not select "
            "or freeze a padding value."),
    }
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "padding_results": [
        {"padding": item["padding"],
         "ped_recall": item["classes"]["ped"]["recall"],
         "vehicle_recall": item["classes"]["vehicle"]["recall"],
         "float_fixed_class_disagreements": item["float_fixed_class_disagreements"]}
        for item in padding_reports]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
