#!/usr/bin/env python3
"""Decode once and compare small candidate-chain parameter variants in Python."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import cv2

from candidate_chain_reference import CandidateChainReference
from select_candidate_windows import inclusive_iou


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--start-frame", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--thresholds", type=int, nargs="+", default=[12, 16, 20])
    parser.add_argument("--min-areas", type=int, nargs="+", default=[8, 16])
    parser.add_argument("--top-k", type=int, nargs="+", default=[4])
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.frames < 1 or args.start_frame < 0:
        raise ValueError("invalid frame interval")

    annotations: dict[int, list[dict]] = defaultdict(list)
    with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            frame = int(row["frame_index"])
            if (row["clip_id"] == args.clip_id and row["label"] == args.target_label and
                    args.start_frame <= frame < args.start_frame + args.frames):
                annotations[frame].append(row)

    variants = []
    for threshold in sorted(set(args.thresholds)):
        for min_area in sorted(set(args.min_areas)):
            for top_k in sorted(set(args.top_k)):
                variants.append({
                    "threshold": threshold, "min_area": min_area, "top_k": top_k,
                    "chain": CandidateChainReference(
                        threshold=threshold, min_area=min_area, top_k=top_k),
                    "candidate_count": 0, "candidate_frames": 0,
                    "annotation_rows": 0, "covered_annotation_rows": 0,
                    "covered_tracks": set(), "candidate_annotation_matches": 0,
                })

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open {args.video}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, args.start_frame)
    processed = 0
    try:
        for offset in range(args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            frame_index = args.start_frame + offset
            processed += 1
            for variant in variants:
                result = variant["chain"].process_bgr(frame, frame_index)
                candidates = result["candidates"]
                variant["candidate_count"] += len(candidates)
                variant["candidate_frames"] += bool(candidates)
                boxes = [
                    (int(candidate["xmin"]) * 5, int(candidate["ymin"]) * 5,
                     int(candidate["xmax"]) * 5 + 4, int(candidate["ymax"]) * 5 + 4)
                    for candidate in candidates]
                frame_annotations = annotations.get(frame_index, [])
                variant["annotation_rows"] += len(frame_annotations)
                for annotation in frame_annotations:
                    annotation_box = tuple(int(annotation[key]) for key in
                                           ("xmin", "ymin", "xmax", "ymax"))
                    maximum = max((inclusive_iou(box, annotation_box) for box in boxes),
                                  default=0.0)
                    if maximum >= args.iou_threshold:
                        variant["covered_annotation_rows"] += 1
                        variant["covered_tracks"].add(annotation["object_id"])
                for box in boxes:
                    if any(inclusive_iou(box, tuple(int(annotation[key]) for key in
                                                       ("xmin", "ymin", "xmax", "ymax"))) >=
                           args.iou_threshold for annotation in frame_annotations):
                        variant["candidate_annotation_matches"] += 1
    finally:
        capture.release()

    results = []
    for variant in variants:
        row_count = variant["annotation_rows"]
        results.append({
            "threshold": variant["threshold"], "min_area": variant["min_area"],
            "top_k": variant["top_k"], "candidate_count": variant["candidate_count"],
            "candidate_frames": variant["candidate_frames"],
            "target_annotation_row_count": row_count,
            "covered_target_annotation_rows": variant["covered_annotation_rows"],
            "target_annotation_coverage_rate": (
                variant["covered_annotation_rows"] / row_count if row_count else None),
            "covered_target_tracks": len(variant["covered_tracks"]),
            "candidate_target_match_count": variant["candidate_annotation_matches"],
        })
    results.sort(key=lambda item: (
        -(item["target_annotation_coverage_rate"] or 0), item["candidate_count"],
        item["threshold"], item["min_area"], item["top_k"]))
    report = {
        "status": "python_cold_start_parameter_sweep_not_continuous_or_rtl_evidence",
        "clip_id": args.clip_id, "target_label": args.target_label,
        "start_frame": args.start_frame, "requested_frames": args.frames,
        "processed_frames": processed, "iou_threshold": args.iou_threshold,
        "video_sha256": digest(args.video), "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)), "results": results,
        "background_initialization": (
            f"new candidate chain at start_frame={args.start_frame}; first four frames "
            "relearn the background; no pre-roll"),
        "boundary": (
            "VIRAT object tracks are not exhaustive background truth. Candidate counts measure "
            "load, not false positives. Only the exact deployed parameters threshold=20, "
            "min_area=16, top_k=4 correspond to current RTL. Use candidate_temporal_sweep.py "
            "with --warmup-start-frame for continuous-window coverage."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": report["status"], "processed_frames": processed,
                      "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
