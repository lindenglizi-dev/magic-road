#!/usr/bin/env python3
"""Evaluate causal foreground-mask retention as a Python-only candidate diagnostic."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference, components
from candidate_resolution_sweep import source_extent_box
from select_candidate_windows import inclusive_iou


DEFAULT_VARIANTS = (
    "5,20,16,4,1",
    "5,20,16,4,3",
    "5,20,16,4,5",
    "5,12,8,4,3",
    "5,12,8,8,3",
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_variant(spec: str) -> dict[str, int]:
    try:
        values = [int(value) for value in spec.split(",")]
        if len(values) == 5:
            values.extend((0, 3, 2))
        elif len(values) == 6:
            values.extend((3, 2))
        if len(values) != 8:
            raise ValueError
        (stride, threshold, min_area, top_k, temporal_frames, dilate_iterations,
         min_neighbors, min_run) = values
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"invalid variant {spec!r}; expected stride,threshold,min_area,top_k,"
            "temporal_frames[,dilate_iterations[,min_neighbors,min_run]]"
        ) from exc
    if (stride < 1 or not 0 <= threshold <= 255 or min_area < 1 or top_k < 1 or
            temporal_frames < 1 or dilate_iterations < 0 or
            not 1 <= min_neighbors <= 9 or min_run < 1):
        raise ValueError(f"invalid variant values: {spec!r}")
    return {"sample_stride": stride, "threshold": threshold,
            "min_area": min_area, "top_k": top_k,
            "temporal_frames": temporal_frames,
            "dilate_iterations": dilate_iterations,
            "min_neighbors": min_neighbors,
            "min_run": min_run}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--start-frame", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--warmup-start-frame", type=int,
                        help="process from this frame but score only --start-frame onward")
    parser.add_argument("--variant", action="append", default=None,
                        help=("stride,threshold,min_area,top_k,temporal_frames"
                              "[,dilate_iterations[,min_neighbors,min_run]]"))
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    warmup_start = (args.start_frame if args.warmup_start_frame is None else
                    args.warmup_start_frame)
    if (args.frames < 1 or args.start_frame < 0 or warmup_start < 0 or
            warmup_start > args.start_frame or not 0 <= args.iou_threshold <= 1):
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
    chain_keys = sorted({(item["sample_stride"], item["threshold"],
                          item["min_neighbors"], item["min_run"])
                         for item in specifications})
    maximum_history = {
        key: max(item["temporal_frames"] for item in specifications
                 if (item["sample_stride"], item["threshold"],
                     item["min_neighbors"], item["min_run"]) == key)
        for key in chain_keys
    }
    chains = {
        key: CandidateChainReference(sample_stride=key[0], threshold=key[1],
                                     min_neighbors=key[2], min_run=key[3])
        for key in chain_keys
    }
    histories = {key: deque(maxlen=maximum_history[key]) for key in chain_keys}
    variants = [{**item, "candidate_count": 0, "candidate_frames": 0,
                 "annotation_rows": 0, "covered_rows": 0,
                 "covered_tracks": set(), "target_rows_with_raw_pixel": 0,
                 "target_rows_with_clean_pixel": 0,
                 "target_rows_with_run_pixel": 0,
                 "target_difference_maximum": 0,
                 "target_difference_row_maximum_sum": 0}
                for item in specifications]

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open {args.video}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, warmup_start)
    processed = 0
    processed_total = 0
    try:
        for frame_index in range(warmup_start, args.start_frame + args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            processed_total += 1
            current_results = {}
            for key, chain in chains.items():
                result = chain.process_bgr(frame, frame_index)
                current_results[key] = result
                histories[key].append(result["run_filtered_mask"])
            for variant in variants:
                key = (variant["sample_stride"], variant["threshold"],
                       variant["min_neighbors"], variant["min_run"])
                selected = list(histories[key])[-variant["temporal_frames"]:]
                retained = np.bitwise_or.reduce(selected)
                if variant["dilate_iterations"]:
                    retained = cv2.dilate(
                        retained, np.ones((3, 3), np.uint8),
                        iterations=variant["dilate_iterations"])
                found = components(retained, variant["min_area"], variant["top_k"])
                if frame_index < args.start_frame:
                    continue
                variant["candidate_count"] += len(found)
                variant["candidate_frames"] += bool(found)
                boxes = [source_extent_box({"xmin": candidate.xmin,
                                            "ymin": candidate.ymin,
                                            "xmax": candidate.xmax,
                                            "ymax": candidate.ymax},
                                           variant["sample_stride"])
                         for candidate in found]
                for annotation in annotations.get(frame_index, []):
                    variant["annotation_rows"] += 1
                    stride = variant["sample_stride"]
                    height, width = current_results[key]["difference"].shape
                    x0 = max(0, min(int(annotation["xmin"]) // stride, width - 1))
                    y0 = max(0, min(int(annotation["ymin"]) // stride, height - 1))
                    x1 = max(0, min(int(annotation["xmax"]) // stride, width - 1))
                    y1 = max(0, min(int(annotation["ymax"]) // stride, height - 1))
                    slices = np.s_[y0:y1 + 1, x0:x1 + 1]
                    row_maximum = int(current_results[key]["difference"][slices].max())
                    variant["target_difference_maximum"] = max(
                        variant["target_difference_maximum"], row_maximum)
                    variant["target_difference_row_maximum_sum"] += row_maximum
                    variant["target_rows_with_raw_pixel"] += bool(
                        current_results[key]["raw_mask"][slices].any())
                    variant["target_rows_with_clean_pixel"] += bool(
                        current_results[key]["clean_mask"][slices].any())
                    variant["target_rows_with_run_pixel"] += bool(
                        current_results[key]["run_filtered_mask"][slices].any())
                    annotation_box = tuple(int(annotation[field]) for field in
                                           ("xmin", "ymin", "xmax", "ymax"))
                    if max((inclusive_iou(box, annotation_box) for box in boxes),
                           default=0.0) >= args.iou_threshold:
                        variant["covered_rows"] += 1
                        variant["covered_tracks"].add(annotation["object_id"])
            if frame_index >= args.start_frame:
                processed += 1
    finally:
        capture.release()

    results = []
    for variant in variants:
        row_count = variant["annotation_rows"]
        results.append({
            "sample_stride": variant["sample_stride"],
            "threshold": variant["threshold"],
            "min_area": variant["min_area"],
            "top_k": variant["top_k"],
            "temporal_frames": variant["temporal_frames"],
            "dilate_iterations": variant["dilate_iterations"],
            "min_neighbors": variant["min_neighbors"],
            "min_run": variant["min_run"],
            "candidate_count": variant["candidate_count"],
            "candidate_frames": variant["candidate_frames"],
            "target_annotation_row_count": row_count,
            "covered_target_annotation_rows": variant["covered_rows"],
            "target_annotation_coverage_rate": (
                variant["covered_rows"] / row_count if row_count else None),
            "covered_target_tracks": len(variant["covered_tracks"]),
            "target_rows_with_raw_pixel": variant["target_rows_with_raw_pixel"],
            "target_rows_with_clean_pixel": variant["target_rows_with_clean_pixel"],
            "target_rows_with_run_pixel": variant["target_rows_with_run_pixel"],
            "target_difference_maximum": variant["target_difference_maximum"],
            "target_difference_row_maximum_mean": (
                variant["target_difference_row_maximum_sum"] / row_count
                if row_count else None),
            "current_rtl_parameters": (
                variant["sample_stride"] == 5 and variant["threshold"] == 20 and
                variant["min_area"] == 16 and variant["top_k"] == 4 and
                variant["temporal_frames"] == 1 and
                variant["dilate_iterations"] == 0 and
                variant["min_neighbors"] == 3 and variant["min_run"] == 2),
        })
    report = {
        "status": "python_causal_temporal_mask_diagnostic_not_rtl_or_acceptance_evidence",
        "clip_id": args.clip_id,
        "target_label": args.target_label,
        "start_frame": args.start_frame,
        "warmup_start_frame": warmup_start,
        "pre_roll_frame_count": max(0, args.start_frame - warmup_start),
        "requested_frames": args.frames,
        "processed_frames": processed,
        "processed_frames_including_pre_roll": processed_total,
        "iou_threshold": args.iou_threshold,
        "video_sha256": digest(args.video),
        "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)),
        "results": results,
        "contract": (
            "Each variant causally ORs the current and preceding N-1 post-cleanup, "
            "post-min-run masks, then optionally applies 3x3 binary dilation before "
            "connected components. It uses no future frame. Retention or dilation is not "
            "present in current RTL and would require new ghosting, merge, CCL-load and "
            "timing verification. min_neighbors=3 and min_run=2 are the deployed cleanup "
            "values; weaker cleanup is a small-target diagnostic only."),
        "boundary": (
            "VIRAT tracks are not exhaustive background truth; candidate count measures "
            "load rather than false positives. This scan does not label new candidates."),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": report["status"], "processed_frames": processed,
                      "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
