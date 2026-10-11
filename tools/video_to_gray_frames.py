#!/usr/bin/env python3
"""Convert an ordinary video into per-frame 256x144 hexadecimal memories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
from roi_dataset_tool import fpga_analysis_frame
import hashlib


WIDTH = 256
HEIGHT = 144


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert video frames to the grayscale format consumed by the RTL replay testbench."
    )
    parser.add_argument("input", type=Path, help="Input MP4/AVI/MOV video")
    parser.add_argument("output", type=Path, help="New or empty output directory")
    start_group = parser.add_mutually_exclusive_group()
    start_group.add_argument("--start", type=float, default=None, help="Start time in seconds")
    start_group.add_argument("--start-frame", type=int, default=None,
                             help="Exact zero-based source frame at which to start")
    parser.add_argument("--duration", type=float, default=0.0, help="Duration in seconds; 0 means to EOF")
    parser.add_argument("--max-frames", type=int, default=0, help="Maximum exported frames; 0 means unlimited")
    parser.add_argument(
        "--target-fps",
        type=float,
        default=0.0,
        help="Approximate export FPS; 0 preserves every source frame",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.input.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise SystemExit(f"Input video not found: {source}")
    if ((args.start is not None and args.start < 0) or
            (args.start_frame is not None and args.start_frame < 0) or
            args.duration < 0 or args.max_frames < 0 or args.target_fps < 0):
        raise SystemExit("Time, FPS and frame limits must not be negative.")

    output.mkdir(parents=True, exist_ok=True)
    existing = list(output.glob("frame_*.hex"))
    if existing:
        raise SystemExit(
            f"Output already contains {len(existing)} frame files. Use a new/empty directory: {output}"
        )

    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise SystemExit(f"OpenCV cannot open: {source}")

    source_fps = float(capture.get(cv2.CAP_PROP_FPS))
    source_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    source_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if (source_width, source_height) != (1280, 720):
        capture.release()
        raise SystemExit("Use a traceable 1280x720 derivative; replay does not silently resize input.")
    if source_fps <= 0:
        raise SystemExit("Source FPS unavailable; refusing to invent timestamps.")
    requested_start_seconds = args.start if args.start is not None else 0.0
    start_index = (args.start_frame if args.start_frame is not None else
                   int(round(requested_start_seconds * source_fps)))
    if start_index >= source_frames:
        capture.release()
        raise SystemExit(f"Start frame {start_index} is outside {source_frames} source frames.")
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_index)
    actual_start_seconds = start_index / source_fps

    target_fps = args.target_fps if args.target_fps > 0 else source_fps
    target_fps = min(target_fps, source_fps)
    sample_period = 1.0 / target_fps
    end_time = actual_start_seconds + args.duration if args.duration > 0 else None
    next_sample_time = actual_start_seconds
    exported = 0
    decoded = 0
    frame_map = []

    while True:
        ok, frame = capture.read()
        if not ok:
            break
        decoded += 1
        source_index = start_index + decoded - 1
        timestamp = source_index / source_fps
        if end_time is not None and timestamp > end_time:
            break
        if timestamp + (0.5 / source_fps) < next_sample_time:
            continue

        gray = fpga_analysis_frame(frame)
        frame_path = output / f"frame_{exported:04d}.hex"
        frame_path.write_text(
            "\n".join(f"{value:02x}" for value in gray.reshape(-1)) + "\n",
            encoding="ascii",
        )
        exported += 1
        frame_map.append({"replay_frame": exported - 1, "source_frame": source_index,
                          "timestamp_ms": timestamp * 1000})
        next_sample_time += sample_period
        if args.max_frames and exported >= args.max_frames:
            break

    capture.release()
    if exported == 0:
        raise SystemExit("No frame was exported. Check --start/--duration and the source video.")

    manifest = {
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "preprocessing": "rtl_shift_gray_stride5_v1",
        "frame_map": frame_map,
        "source_width": source_width,
        "source_height": source_height,
        "source_fps": source_fps,
        "source_frame_count": source_frames,
        "analysis_width": WIDTH,
        "analysis_height": HEIGHT,
        "export_fps": target_fps,
        "requested_start_seconds": args.start,
        "requested_start_frame": args.start_frame,
        "start_frame": start_index,
        "start_seconds": actual_start_seconds,
        "requested_duration_seconds": args.duration,
        "decoded_frames": decoded,
        "frame_count": exported,
        "format": "one 8-bit grayscale pixel per hexadecimal line, row-major",
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Exported {exported} frames to {output}")
    print(f"Analysis stream: {WIDTH}x{HEIGHT} @ {target_fps:.3f} fps")


if __name__ == "__main__":
    main()
