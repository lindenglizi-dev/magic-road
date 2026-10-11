#!/usr/bin/env python3
"""Trace target overlap before min-area/top-K and test box repair diagnostics."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference
from candidate_resolution_sweep import source_extent_box
from select_candidate_windows import inclusive_iou


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def expand_minimum(box: tuple[int, int, int, int], minimum_width: int,
                   minimum_height: int, width: int, height: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    current_width, current_height = x1 - x0 + 1, y1 - y0 + 1
    if current_width < minimum_width:
        extra = minimum_width - current_width
        x0 -= extra // 2
        x1 += extra - extra // 2
    if current_height < minimum_height:
        extra = minimum_height - current_height
        y0 -= extra // 2
        y1 += extra - extra // 2
    if x0 < 0:
        x1 -= x0
        x0 = 0
    if y0 < 0:
        y1 -= y0
        y0 = 0
    if x1 >= width:
        x0 -= x1 - width + 1
        x1 = width - 1
    if y1 >= height:
        y0 -= y1 - height + 1
        y1 = height - 1
    return max(0, x0), max(0, y0), x1, y1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--warmup-start-frame", type=int, default=0)
    parser.add_argument("--start-frame", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--threshold", type=int, default=20)
    parser.add_argument("--min-neighbors", type=int, default=3)
    parser.add_argument("--min-run", type=int, default=2)
    parser.add_argument("--opening-iterations", type=int, default=0)
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if (args.frames < 1 or args.warmup_start_frame < 0 or
            args.warmup_start_frame > args.start_frame or args.opening_iterations < 0):
        raise ValueError("invalid frame interval")

    annotations: dict[int, list[dict[str, str]]] = defaultdict(list)
    with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            frame_index = int(row["frame_index"])
            if (row["clip_id"] == args.clip_id and row["label"] == args.target_label and
                    args.start_frame <= frame_index < args.start_frame + args.frames):
                annotations[frame_index].append(row)

    top_ks = (4, 8, 16, 32)
    repairs = ((4, 4), (4, 8), (6, 6))
    counters = {f"raw_top_{top_k}": 0 for top_k in top_ks}
    counters.update({f"repair_{w}x{h}_top_{top_k}": 0
                     for w, h in repairs for top_k in top_ks})
    counters["raw_any_rank"] = 0
    counters.update({f"repair_{w}x{h}_any_rank": 0 for w, h in repairs})
    best_ranks, best_areas, best_ious = [], [], []

    chain = CandidateChainReference(
        threshold=args.threshold, min_neighbors=args.min_neighbors,
        min_run=args.min_run)
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open {args.video}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, args.warmup_start_frame)
    processed = 0
    try:
        for frame_index in range(args.warmup_start_frame,
                                 args.start_frame + args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            result = chain.process_bgr(frame, frame_index)
            if frame_index < args.start_frame:
                continue
            processed += 1
            mask = (result["run_filtered_mask"] != 0).astype(np.uint8)
            if args.opening_iterations:
                mask = cv2.morphologyEx(
                    mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8),
                    iterations=args.opening_iterations)
            count, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
            components = []
            for label in range(1, count):
                x, y, width, height, area = (int(value) for value in stats[label])
                components.append({"label": label, "area": area, "xmin": x, "ymin": y,
                                   "xmax": x + width - 1, "ymax": y + height - 1})
            components.sort(key=lambda item: (-item["area"], item["label"]))
            raw_boxes = [source_extent_box(item, 5) for item in components]
            repaired = {
                (w, h): [source_extent_box({
                    "xmin": fixed[0], "ymin": fixed[1],
                    "xmax": fixed[2], "ymax": fixed[3]}, 5)
                    for item in components
                    for fixed in [expand_minimum(
                        (item["xmin"], item["ymin"], item["xmax"], item["ymax"]),
                        w, h, 256, 144)]]
                for w, h in repairs
            }
            for annotation in annotations.get(frame_index, []):
                annotation_box = tuple(int(annotation[field]) for field in
                                       ("xmin", "ymin", "xmax", "ymax"))
                raw_ious = [inclusive_iou(box, annotation_box) for box in raw_boxes]
                if raw_ious:
                    best_index = int(np.argmax(raw_ious))
                    best_ranks.append(best_index + 1)
                    best_areas.append(components[best_index]["area"])
                    best_ious.append(raw_ious[best_index])
                for top_k in top_ks:
                    counters[f"raw_top_{top_k}"] += (
                        max(raw_ious[:top_k], default=0.0) >= args.iou_threshold)
                counters["raw_any_rank"] += max(raw_ious, default=0.0) >= args.iou_threshold
                for w, h in repairs:
                    repair_ious = [inclusive_iou(box, annotation_box)
                                   for box in repaired[(w, h)]]
                    for top_k in top_ks:
                        counters[f"repair_{w}x{h}_top_{top_k}"] += (
                            max(repair_ious[:top_k], default=0.0) >= args.iou_threshold)
                    counters[f"repair_{w}x{h}_any_rank"] += (
                        max(repair_ious, default=0.0) >= args.iou_threshold)
    finally:
        capture.release()

    row_count = sum(len(rows) for rows in annotations.values())
    report = {
        "status": "target_conditioned_component_miss_analysis_not_candidate_or_acceptance_evidence",
        "clip_id": args.clip_id,
        "target_label": args.target_label,
        "warmup_start_frame": args.warmup_start_frame,
        "start_frame": args.start_frame,
        "requested_frames": args.frames,
        "processed_frames": processed,
        "parameters": {"threshold": args.threshold,
                       "min_neighbors": args.min_neighbors,
                       "min_run": args.min_run,
                       "opening_iterations": args.opening_iterations,
                       "iou_threshold": args.iou_threshold},
        "target_annotation_row_count": row_count,
        "coverage_counts": counters,
        "coverage_rates": {key: value / row_count if row_count else None
                           for key, value in counters.items()},
        "best_raw_component": {
            "rank_minimum": min(best_ranks) if best_ranks else None,
            "rank_median": float(np.median(best_ranks)) if best_ranks else None,
            "rank_maximum": max(best_ranks) if best_ranks else None,
            "area_median": float(np.median(best_areas)) if best_areas else None,
            "iou_median": float(np.median(best_ious)) if best_ious else None,
        },
        "video_sha256": digest(args.video),
        "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)),
        "boundary": (
            "This target-conditioned analysis looks at every post-cleanup connected component, "
            "including components current RTL would discard. Minimum-box repair is diagnostic "
            "and changes ROI semantics; it requires complete candidate review before metrics."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
