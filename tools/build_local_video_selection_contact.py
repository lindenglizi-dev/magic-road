#!/usr/bin/env python3
"""Build a reproducible, model-blind contact sheet for direct local MP4 inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def fit(image: np.ndarray, width: int = 480, height: int = 270) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (max(1, round(image.shape[1] * scale)), max(1, round(image.shape[0] * scale))),
        interpolation=cv2.INTER_AREA,
    )
    canvas = np.zeros((height, width, 3), np.uint8)
    x = (width - resized.shape[1]) // 2
    y = (height - resized.shape[0]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    videos = sorted(args.input_dir.resolve().glob("*.mp4"))
    if len(videos) != 3:
        raise ValueError(f"expected exactly three direct MP4 files, found {len(videos)}")
    if args.output.exists() and any(path.name != ".gitkeep" for path in args.output.iterdir()):
        raise ValueError(f"output must be absent or empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)

    rows = []
    for video in videos:
        capture = cv2.VideoCapture(str(video))
        if not capture.isOpened():
            raise ValueError(f"cannot open {video}")
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        times = sorted(set((0.0, duration * .25, duration * .5, duration * .75,
                            max(0.0, duration - 1.0 / fps))))
        samples = []
        for sample_time in times:
            frame_index = min(frame_count - 1, round(sample_time * fps))
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"cannot decode {video.name} frame {frame_index}")
            samples.append((frame_index, frame))
        capture.release()

        canvas = np.full((640, 1480, 3), 242, np.uint8)
        title = f"{video.name} | {width}x{height} | {fps:.6g} fps | {frame_count} frames | {duration:.3f} s"
        cv2.putText(canvas, title, (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    .65, (10, 10, 10), 2, cv2.LINE_AA)
        sample_receipts = []
        for index, (frame_index, frame) in enumerate(samples):
            row, column = divmod(index, 3)
            x, y = 15 + column * 490, 60 + row * 290
            canvas[y:y + 270, x:x + 480] = fit(frame)
            label = f"frame {frame_index} / {frame_index / fps:.2f}s"
            cv2.putText(canvas, label, (x + 6, y + 24), cv2.FONT_HERSHEY_SIMPLEX,
                        .55, (255, 255, 255), 2, cv2.LINE_AA)
            sample_receipts.append({"frame_index": frame_index,
                                    "timestamp_seconds": frame_index / fps})
        output_image = args.output / f"{video.stem}_contact.jpg"
        if not cv2.imwrite(str(output_image), canvas, [cv2.IMWRITE_JPEG_QUALITY, 94]):
            raise ValueError(f"cannot write {output_image}")
        rows.append({
            "name": video.name,
            "bytes": video.stat().st_size,
            "sha256": sha256(video),
            "width": width,
            "height": height,
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration,
            "samples": sample_receipts,
            "contact_sheet": output_image.name,
            "contact_sheet_sha256": sha256(output_image),
        })
    report = {"schema": "local_video_model_blind_selection_v1", "videos": rows}
    (args.output / "inventory.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
