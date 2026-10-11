#!/usr/bin/env python3
"""Report deployed candidate coverage by factual target-box geometry strata."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import cv2

from candidate_chain_reference import CandidateChainReference
from candidate_resolution_sweep import source_extent_box
from select_candidate_windows import inclusive_iou


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def geometry_stratum(box: tuple[int, int, int, int], frame_width: int = 1280,
                     frame_height: int = 720) -> str:
    x0, y0, x1, y1 = box
    width, height = x1 - x0 + 1, y1 - y0 + 1
    if x0 <= 0 or y0 <= 0 or x1 >= frame_width - 1 or y1 >= frame_height - 1:
        return "frame_edge_truncated"
    if height * 4 < width * 5:
        return "low_aspect_h_over_w_lt_1.25"
    if height < 40:
        return "upright_small_h_lt_40"
    if height < 80:
        return "upright_medium_h_40_79"
    return "upright_large_h_ge_80"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--warmup-start-frame", type=int, default=0)
    parser.add_argument("--start-frame", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if (args.frames < 1 or args.warmup_start_frame < 0 or
            args.warmup_start_frame > args.start_frame):
        raise ValueError("invalid frame interval")

    annotations: dict[int, list[dict[str, str]]] = defaultdict(list)
    with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            frame_index = int(row["frame_index"])
            if (row["clip_id"] == args.clip_id and row["label"] == args.target_label and
                    args.start_frame <= frame_index < args.start_frame + args.frames):
                annotations[frame_index].append(row)

    groups: dict[str, dict[str, int]] = defaultdict(lambda: {"rows": 0, "covered": 0})
    tracks: dict[str, dict[str, int]] = defaultdict(lambda: {"rows": 0, "covered": 0})
    candidate_count = 0
    candidate_frames = 0
    chain = CandidateChainReference()
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
            candidates = result["candidates"]
            candidate_count += len(candidates)
            candidate_frames += bool(candidates)
            boxes = [source_extent_box(candidate, 5) for candidate in candidates]
            for annotation in annotations.get(frame_index, []):
                target_box = tuple(int(annotation[field]) for field in
                                   ("xmin", "ymin", "xmax", "ymax"))
                covered = max((inclusive_iou(box, target_box) for box in boxes),
                              default=0.0) >= args.iou_threshold
                group = geometry_stratum(target_box)
                groups[group]["rows"] += 1
                groups[group]["covered"] += covered
                track = annotation["object_id"]
                tracks[track]["rows"] += 1
                tracks[track]["covered"] += covered
    finally:
        capture.release()

    def rates(values: dict[str, dict[str, int]]) -> dict[str, dict[str, float | int]]:
        return {key: {**item, "coverage_rate": item["covered"] / item["rows"]}
                for key, item in sorted(values.items())}

    report = {
        "status": "deployed_candidate_geometry_strata_diagnostic_not_acceptance_evidence",
        "clip_id": args.clip_id,
        "target_label": args.target_label,
        "warmup_start_frame": args.warmup_start_frame,
        "start_frame": args.start_frame,
        "requested_frames": args.frames,
        "processed_frames": processed,
        "iou_threshold": args.iou_threshold,
        "candidate_count": candidate_count,
        "candidate_frames": candidate_frames,
        "target_annotation_row_count": sum(item["rows"] for item in groups.values()),
        "geometry_strata": rates(groups),
        "tracks": rates(tracks),
        "video_sha256": digest(args.video),
        "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)),
        "boundary": (
            "Strata use only source-box geometry. low_aspect is not automatically invalid or "
            "excluded; visibility and occlusion require an explicit review policy before metrics "
            "can be filtered. Rows are correlated annotation frames, not independent objects."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
