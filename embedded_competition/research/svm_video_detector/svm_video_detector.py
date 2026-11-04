#!/usr/bin/env python3
"""Train a HOG+linear-SVM classifier and draw detections on road videos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


LABELS = ("ped", "vehicle")


def hog() -> cv2.HOGDescriptor:
    return cv2.HOGDescriptor(
        (32, 32), (16, 16), (8, 8), (8, 8), 9,
        1, 4.0, cv2.HOGDescriptor_L2Hys, 0.2, False, 64, False,
    )


def feature(image: np.ndarray, extractor: cv2.HOGDescriptor) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    roi = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA)
    return extractor.compute(roi).reshape(-1).astype(np.float64)


def load_split(root: Path, split: str, extractor: cv2.HOGDescriptor) -> tuple[np.ndarray, np.ndarray]:
    samples, labels = [], []
    for label_id, label in enumerate(LABELS):
        paths = sorted((root / split / label).glob("*.png"))
        if not paths:
            raise ValueError(f"no images in {root / split / label}")
        for path in paths:
            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise ValueError(f"cannot read {path}")
            samples.append(feature(image, extractor))
            labels.append(label_id)
    return np.asarray(samples), np.asarray(labels)


def train(dataset: Path, output: Path) -> dict:
    extractor = hog()
    x_train, y_train = load_split(dataset, "train", extractor)
    x_val, y_val = load_split(dataset, "val", extractor)
    scaler = StandardScaler().fit(x_train)
    classifier = LinearSVC(C=1.0, class_weight="balanced", random_state=20260927,
                           max_iter=30000).fit(scaler.transform(x_train), y_train)
    prediction = classifier.predict(scaler.transform(x_val))
    weights = classifier.coef_[0] / scaler.scale_
    bias = float(classifier.intercept_[0] - np.dot(classifier.coef_[0], scaler.mean_ / scaler.scale_))
    metrics = {
        "train_samples": int(len(y_train)),
        "validation_samples": int(len(y_val)),
        "validation_accuracy": float(accuracy_score(y_val, prediction)),
        "validation_balanced_accuracy": float(balanced_accuracy_score(y_val, prediction)),
        "confusion_matrix_truth_rows_pred_columns_ped_vehicle": confusion_matrix(y_val, prediction).tolist(),
        "note": "ROI classification only; this is not end-to-end video detection accuracy.",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "model.json").write_text(json.dumps({
        "labels": LABELS,
        "feature": "OpenCV HOG 32x32, 9 bins, 324 dimensions",
        "weights": weights.tolist(),
        "bias": bias,
    }, indent=2) + "\n", encoding="utf-8")
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def video_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]
    raw = sorted(source.glob("*_raw.mp4"))
    return raw or sorted(path for path in source.iterdir() if path.suffix.lower() in {".mp4", ".avi", ".mov", ".mkv"})


def detect_video(source: Path, destination: Path, model: dict, max_width: int) -> dict:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise ValueError(f"cannot open {source}")
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    source_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = min(1.0, max_width / source_width)
    width, height = round(source_width * scale), round(source_height * scale)
    width -= width % 2
    height -= height % 2
    destination.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(destination), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise ValueError(f"cannot create {destination}")

    extractor = hog()
    weights = np.asarray(model["weights"], dtype=np.float64)
    bias = float(model["bias"])
    if weights.shape != (324,):
        raise ValueError("model must contain 324 HOG weights")
    background = cv2.createBackgroundSubtractorMOG2(history=120, varThreshold=24, detectShadows=False)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    frames = boxes = ped = vehicle = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if scale != 1.0:
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        mask = background.apply(frame)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=2)
        candidates = []
        if frames >= 20:
            for contour in cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h >= width * height * 0.001 and w >= 18 and h >= 18:
                    candidates.append((x, y, w, h))
        for x, y, w, h in sorted(candidates, key=lambda box: box[2] * box[3], reverse=True)[:8]:
            score = float(feature(frame[y:y + h, x:x + w], extractor) @ weights + bias)
            label = "vehicle" if score >= 0 else "ped"
            color = (0, 165, 255) if label == "vehicle" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {score:+.2f}", (x, max(18, y - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
            boxes += 1
            vehicle += label == "vehicle"
            ped += label == "ped"
        writer.write(frame)
        frames += 1
    capture.release()
    writer.release()
    return {"source": str(source), "output": str(destination), "frames": frames,
            "boxes": boxes, "ped_boxes": ped, "vehicle_boxes": vehicle}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, help="folder containing train/val and ped/vehicle")
    parser.add_argument("--videos", type=Path, help="video file or folder")
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--model", type=Path)
    parser.add_argument("--max-width", type=int, default=960)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        assert feature(np.zeros((40, 60), np.uint8), hog()).shape == (324,)
        print("self-test passed")
        return 0
    model_path = args.model or args.output / "model.json"
    if args.dataset:
        print(json.dumps(train(args.dataset, args.output), indent=2))
    if args.videos:
        model = json.loads(model_path.read_text(encoding="utf-8"))
        results = [detect_video(path, args.output / f"{path.stem}_detected.mp4", model, args.max_width)
                   for path in video_files(args.videos)]
        (args.output / "video_results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(results, indent=2))
    if not args.dataset and not args.videos:
        parser.error("provide --dataset and/or --videos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
