#!/usr/bin/env python3
"""Render RTL track CSV data over the converted grayscale video frames."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an MP4 preview from RTL replay results.")
    parser.add_argument("frames", type=Path, help="Directory produced by video_to_gray_frames.py")
    parser.add_argument("results", type=Path, help="Directory produced by run_video_replay.ps1")
    parser.add_argument("output", type=Path, help="Output MP4 path")
    parser.add_argument("--scale", type=int, default=5, help="Display scale; default gives 1280x720")
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    args = parse_args()
    frames_dir = args.frames.resolve()
    results_dir = args.results.resolve()
    manifest = json.loads((frames_dir / "manifest.json").read_text(encoding="utf-8"))
    frame_count = int(manifest["frame_count"])
    fps = float(manifest["export_fps"])
    scale = max(1, args.scale)
    width, height = 256, 144

    tracks_by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(results_dir / "tracks.csv"):
        tracks_by_frame[int(row["frame"])].append(row)
    events_by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(results_dir / "events.csv"):
        events_by_frame[int(row["frame"])].append(row)
    summary_by_frame = {
        int(row["frame"]): row for row in read_rows(results_dir / "frame_summary.csv")
    }

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width * scale, height * scale)
    )
    if not writer.isOpened():
        raise SystemExit(f"Cannot create output video: {output}")

    colors = {1: (0, 255, 0), 2: (255, 255, 0)}  # OpenCV BGR: green/cyan
    labels = {0: "unknown", 1: "person", 2: "vehicle"}
    for frame_index in range(frame_count):
        frame_path = frames_dir / f"frame_{frame_index:04d}.hex"
        values = np.loadtxt(frame_path, dtype=np.uint8, converters={0: lambda x: int(x, 16)})
        gray = values.reshape((height, width))
        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        image = cv2.resize(image, (width * scale, height * scale), interpolation=cv2.INTER_NEAREST)

        for track in tracks_by_frame.get(frame_index, []):
            if track["valid"] != "1" or track["visible"] != "1":
                continue
            class_code = int(track["class"])
            color = colors.get(class_code, (255, 0, 255))
            x0, y0 = int(track["xmin"]) * scale, int(track["ymin"]) * scale
            x1 = (int(track["xmax"]) + 1) * scale - 1
            y1 = (int(track["ymax"]) + 1) * scale - 1
            thickness = 3 if track["confirmed"] == "1" else 1
            cv2.rectangle(image, (x0, y0), (x1, y1), color, thickness)
            text = f"ID {track['id']} {labels.get(class_code, 'unknown')}"
            cv2.putText(image, text, (x0, max(18, y0 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

        summary = summary_by_frame.get(frame_index, {})
        status = f"frame {frame_index} objects {summary.get('object_count', '?')} error {summary.get('core_error', '?')}"
        cv2.putText(image, status, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        if events_by_frame.get(frame_index):
            cv2.putText(image, "EVENT", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
        writer.write(image)

    writer.release()
    print(f"Rendered {frame_count} frames to {output}")


if __name__ == "__main__":
    main()
