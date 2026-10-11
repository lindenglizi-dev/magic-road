#!/usr/bin/env python3
"""Compare a few sampling resolutions before considering any RTL change.

The deployed candidate chain remains stride 5 (256x144).  Other variants are
Python diagnostics that preserve the integer grayscale/background operations
while changing the source-pixel sampling grid.  They are workload and target
coverage evidence only, not RTL-equivalence or acceptance evidence.
"""
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


DEFAULT_VARIANTS = (
    "5,20,16,4",
    "4,20,16,4",
    "4,20,25,4",
    "4,12,16,4",
    "4,12,16,8",
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_variant(spec: str) -> dict[str, int]:
    try:
        stride, threshold, min_area, top_k = (int(value) for value in spec.split(","))
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"invalid variant {spec!r}; expected stride,threshold,min_area,top_k") from exc
    if stride < 1 or not 0 <= threshold <= 255 or min_area < 1 or top_k < 1:
        raise ValueError(f"invalid variant values: {spec!r}")
    return {"sample_stride": stride, "threshold": threshold,
            "min_area": min_area, "top_k": top_k}


def source_extent_box(candidate: dict[str, object], stride: int) -> tuple[int, int, int, int]:
    """Map inclusive sampled cells to their inclusive source-pixel extent."""
    return (
        int(candidate["xmin"]) * stride,
        int(candidate["ymin"]) * stride,
        min((int(candidate["xmax"]) + 1) * stride - 1, 1279),
        min((int(candidate["ymax"]) + 1) * stride - 1, 719),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--start-frame", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--variant", action="append", default=None,
                        help="stride,threshold,min_area,top_k; may be repeated")
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.frames < 1 or args.start_frame < 0 or not 0 <= args.iou_threshold <= 1:
        raise ValueError("invalid frame interval or IoU threshold")

    annotations: dict[int, list[dict[str, str]]] = defaultdict(list)
    with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            frame_index = int(row["frame_index"])
            if (row["clip_id"] == args.clip_id and row["label"] == args.target_label and
                    args.start_frame <= frame_index < args.start_frame + args.frames):
                annotations[frame_index].append(row)

    specifications = [parse_variant(item) for item in (args.variant or DEFAULT_VARIANTS)]
    if len({tuple(item.values()) for item in specifications}) != len(specifications):
        raise ValueError("duplicate variant")
    variants = []
    for specification in specifications:
        variants.append({
            **specification,
            "chain": CandidateChainReference(
                threshold=specification["threshold"],
                min_area=specification["min_area"],
                top_k=specification["top_k"],
                sample_stride=specification["sample_stride"],
            ),
            "candidate_count": 0,
            "candidate_frames": 0,
            "annotation_rows": 0,
            "covered_annotation_rows": 0,
            "covered_tracks": set(),
            "track_rows": defaultdict(int),
            "track_covered_rows": defaultdict(int),
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
                boxes = [source_extent_box(candidate, variant["sample_stride"])
                         for candidate in candidates]
                for annotation in annotations.get(frame_index, []):
                    track = annotation["object_id"]
                    variant["annotation_rows"] += 1
                    variant["track_rows"][track] += 1
                    annotation_box = tuple(int(annotation[key]) for key in
                                           ("xmin", "ymin", "xmax", "ymax"))
                    maximum = max((inclusive_iou(box, annotation_box) for box in boxes),
                                  default=0.0)
                    if maximum >= args.iou_threshold:
                        variant["covered_annotation_rows"] += 1
                        variant["covered_tracks"].add(track)
                        variant["track_covered_rows"][track] += 1
    finally:
        capture.release()

    results = []
    for variant in variants:
        row_count = variant["annotation_rows"]
        track_coverage = {}
        for track, count in sorted(variant["track_rows"].items()):
            covered = variant["track_covered_rows"][track]
            track_coverage[track] = {
                "annotation_rows": count,
                "covered_rows": covered,
                "coverage_rate": covered / count if count else None,
            }
        results.append({
            "sample_stride": variant["sample_stride"],
            "analysis_shape": [variant["chain"].analysis_shape[1],
                               variant["chain"].analysis_shape[0]],
            "analysis_pixel_count": (variant["chain"].analysis_shape[1] *
                                     variant["chain"].analysis_shape[0]),
            "threshold": variant["threshold"],
            "min_area": variant["min_area"],
            "top_k": variant["top_k"],
            "candidate_count": variant["candidate_count"],
            "candidate_frames": variant["candidate_frames"],
            "target_annotation_row_count": row_count,
            "covered_target_annotation_rows": variant["covered_annotation_rows"],
            "target_annotation_coverage_rate": (
                variant["covered_annotation_rows"] / row_count if row_count else None),
            "covered_target_tracks": len(variant["covered_tracks"]),
            "track_coverage": track_coverage,
            "current_rtl_parameters": (
                variant["sample_stride"] == 5 and variant["threshold"] == 20 and
                variant["min_area"] == 16 and variant["top_k"] == 4),
        })
    report = {
        "status": "python_cold_start_resolution_sweep_not_continuous_or_rtl_evidence",
        "clip_id": args.clip_id,
        "target_label": args.target_label,
        "start_frame": args.start_frame,
        "requested_frames": args.frames,
        "processed_frames": processed,
        "iou_threshold": args.iou_threshold,
        "video_sha256": digest(args.video),
        "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)),
        "results": results,
        "background_initialization": (
            f"new candidate chain at start_frame={args.start_frame}; first four frames "
            "relearn the background; no pre-roll"),
        "boundary": (
            "Only stride=5, threshold=20, min_area=16, top_k=4 is current RTL. "
            "Other rows change analysis memory, CCL load and timing. VIRAT tracks are "
            "not exhaustive background truth, so candidate count is load rather than a "
            "false-positive count. Use candidate_temporal_sweep.py with "
            "--warmup-start-frame for continuous-window coverage."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": report["status"], "processed_frames": processed,
                      "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
