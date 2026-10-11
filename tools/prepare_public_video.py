"""Prepare a traceable lossless 720p derivative of an acquired public video/sequence.

This does not download data, accept dataset agreements, infer class mappings, or
turn foreground masks into semantic labels. Annotations use explicit canonical
CSV: frame_index,xmin,ymin,xmax,ymax,label,original_label,object_id (0-based,
inclusive boxes). Output annotations retain original coordinates and classes.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
import cv2
import numpy as np


def fit_frame(frame):
    height, width = frame.shape[:2]
    scale = min(1280 / width, 720 / height)
    resized_width, resized_height = round(width * scale), round(height * scale)
    offset_x, offset_y = (1280-resized_width)//2, (720-resized_height)//2
    canvas = np.zeros((720, 1280, 3), np.uint8)
    resized = cv2.resize(frame, (resized_width, resized_height), interpolation=cv2.INTER_AREA
                        if scale < 1 else cv2.INTER_LINEAR)
    canvas[offset_y:offset_y+resized_height, offset_x:offset_x+resized_width] = resized
    return canvas, (width, height, resized_width, resized_height, offset_x, offset_y)


def map_box(box, geometry):
    width, height, rw, rh, ox, oy = geometry
    x0, y0, x1, y1 = box
    if not (0 <= x0 <= x1 < width and 0 <= y0 <= y1 < height):
        raise ValueError("annotation bbox outside original image")
    return (math.floor(x0*rw/width)+ox, math.floor(y0*rh/height)+oy,
            min(1279, math.ceil((x1+1)*rw/width)+ox-1),
            min(719, math.ceil((y1+1)*rh/height)+oy-1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--sequence-id", required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--license-url", required=True)
    timebase = parser.add_mutually_exclusive_group()
    timebase.add_argument("--fps", type=float, help="known source FPS for image sequences")
    timebase.add_argument("--index-only", action="store_true",
                          help="source cadence is unavailable; use a 1 FPS container only for frame indexing")
    parser.add_argument("--annotations", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("use a new output directory")
    args.output.mkdir(parents=True)
    capture = None
    if args.input.is_dir():
        def natural(path):
            return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]
        paths = sorted([p for p in args.input.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}], key=natural)
        source_fps = None if args.index_only else args.fps
        container_fps = 1.0 if args.index_only else args.fps
        frames = ((p, cv2.imread(str(p))) for p in paths)
    else:
        if args.fps is not None or args.index_only:
            raise ValueError("video inputs carry their own FPS; do not override the timebase")
        capture = cv2.VideoCapture(str(args.input))
        if not capture.isOpened():
            raise ValueError("cannot open video")
        source_fps = capture.get(cv2.CAP_PROP_FPS)
        container_fps = source_fps
        def decoded():
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                yield args.input, frame
        frames = decoded()
    if container_fps is None or not math.isfinite(container_fps) or container_fps <= 0:
        raise ValueError("known source FPS or explicit --index-only is required")
    output_video = args.output / f"{args.dataset_name}_{args.sequence_id}.avi"
    writer = cv2.VideoWriter(str(output_video), cv2.VideoWriter_fourcc(*"FFV1"), container_fps, (1280, 720))
    if not writer.isOpened():
        raise RuntimeError("FFV1 lossless encoder unavailable; refusing lossy fallback")
    frame_map = []
    geometry = None
    hashes = {}
    try:
        for index, (path, frame) in enumerate(frames):
            if frame is None:
                raise ValueError(f"unreadable image {path}")
            fitted, current = fit_frame(frame)
            if geometry is not None and current != geometry:
                raise ValueError("frame dimensions changed within sequence")
            geometry = current
            key = str(path.resolve())
            if key not in hashes:
                hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            frame_map.append({"frame_index": index, "source_asset": key,
                              "timestamp_ms": 1000*index/source_fps if source_fps else None})
            writer.write(fitted)
    finally:
        writer.release()
        if capture is not None:
            capture.release()
    if not frame_map:
        raise ValueError("no frames")
    if args.annotations:
        with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            frame_index = int(row["frame_index"])
            if frame_index < 0 or frame_index >= len(frame_map):
                raise ValueError("annotation frame outside sequence")
            if row["label"] not in {"ped", "vehicle", "invalid", "ignore"} or not row.get("original_label"):
                raise ValueError("explicit class mapping and original_label required")
            coordinates = [int(row[k]) for k in ("xmin", "ymin", "xmax", "ymax")]
            for k, value in zip(("xmin", "ymin", "xmax", "ymax"), map_box(coordinates, geometry)):
                row["original_"+k] = row[k]
                row[k] = value
        if rows:
            with (args.output / "annotations_720p.csv").open("w", encoding="utf-8-sig", newline="") as handle:
                csv_writer = csv.DictWriter(handle, list(rows[0]))
                csv_writer.writeheader()
                csv_writer.writerows(rows)
    receipt = {"dataset": args.dataset_name, "sequence_id": args.sequence_id, "scene_id": args.scene_id,
               "source_url": args.source_url, "license_url": args.license_url,
               "source_sha256": hashes, "output_sha256": hashlib.sha256(output_video.read_bytes()).hexdigest(),
               "fps": source_fps, "container_fps": container_fps,
               "timebase": "source_fps" if source_fps else "index_only_unknown_source_cadence",
               "frame_count": len(frame_map), "frame_map": frame_map,
               "geometry": geometry, "annotation_sha256": hashlib.sha256(args.annotations.read_bytes()).hexdigest() if args.annotations else None,
               "transform": "aspect-preserving 720p letterbox; AREA downsample / LINEAR upsample; FFV1 lossless",
               "note": "Preparation transform is not sensor ISP equivalence; downstream uses RTL gray/stride5. No temporal interpolation. Index-only clips do not support timing claims."}
    (args.output / "provenance.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_video)


if __name__ == "__main__":
    main()
