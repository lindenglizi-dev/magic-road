#!/usr/bin/env python3
"""Run the OpenCV Zoo YOLOX model on a video using OpenCV DNN only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


CLASSES = {0: "person", 1: "vehicle", 2: "vehicle", 3: "vehicle", 5: "vehicle", 7: "vehicle"}


def grids() -> tuple[np.ndarray, np.ndarray]:
    positions, strides = [], []
    for stride in (8, 16, 32):
        size = 640 // stride
        x, y = np.meshgrid(np.arange(size), np.arange(size))
        positions.append(np.stack((x, y), axis=2).reshape(-1, 2))
        strides.append(np.full((size * size, 1), stride))
    return np.concatenate(positions), np.concatenate(strides)


GRID, STRIDE = grids()


def infer(net: cv2.dnn.Net, frame: np.ndarray, confidence: float) -> list[tuple]:
    height, width = frame.shape[:2]
    scale = min(640 / height, 640 / width)
    resized = cv2.resize(frame, (round(width * scale), round(height * scale)))
    canvas = np.full((640, 640, 3), 114, np.float32)
    canvas[:resized.shape[0], :resized.shape[1]] = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    net.setInput(np.transpose(canvas, (2, 0, 1))[None])
    output = net.forward()[0]
    output[:, :2] = (output[:, :2] + GRID) * STRIDE
    output[:, 2:4] = np.exp(output[:, 2:4]) * STRIDE

    boxes, scores, class_ids = [], [], []
    for row in output:
        class_id = int(np.argmax(row[5:]))
        score = float(row[4] * row[5 + class_id])
        if class_id not in CLASSES or score < confidence:
            continue
        cx, cy, w, h = row[:4]
        boxes.append([float(cx - w / 2), float(cy - h / 2), float(w), float(h)])
        scores.append(score)
        class_ids.append(class_id)
    keep = cv2.dnn.NMSBoxesBatched(boxes, scores, class_ids, confidence, 0.5)
    return [(CLASSES[class_ids[i]], scores[i], *(np.asarray(boxes[i]) / scale)) for i in keep]


def process(video: Path, model: Path, output: Path, confidence: float) -> dict:
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise ValueError(f"cannot open {video}")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise ValueError(f"cannot create {output}")
    net = cv2.dnn.readNet(str(model))
    counts = {"person": 0, "vehicle": 0}
    frames = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        for label, score, x, y, w, h in infer(net, frame, confidence):
            x, y, w, h = map(round, (x, y, w, h))
            x, y = max(0, x), max(0, y)
            color = (0, 255, 0) if label == "person" else (0, 165, 255)
            cv2.rectangle(frame, (x, y), (min(width - 1, x + w), min(height - 1, y + h)), color, 2)
            cv2.putText(frame, f"{label} {score:.2f}", (x, max(18, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
            counts[label] += 1
        writer.write(frame)
        frames += 1
    capture.release()
    writer.release()
    result = {"video": str(video), "model": str(model), "output": str(output),
              "frames": frames, "confidence": confidence, "detections": counts}
    output.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--confidence", type=float, default=0.60)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert GRID.shape == (8400, 2) and STRIDE.shape == (8400, 1)
        print("self-test passed")
        return 0
    if not all((args.video, args.model, args.output)):
        parser.error("--video, --model and --output are required")
    print(json.dumps(process(args.video, args.model, args.output, args.confidence), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
