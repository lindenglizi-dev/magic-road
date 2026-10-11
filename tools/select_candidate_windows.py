#!/usr/bin/env python3
"""Rank short replay windows from a long Python candidate scan.

This is a cost-control aid: it uses already-produced Python geometry to choose a
small interval before generating gray HEX frames, VCD, or RTL simulation output.
It does not replace the later RTL replay or human semantic review.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def inclusive_iou(left: tuple[int, int, int, int],
                  right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = (left[2] - left[0] + 1) * (left[3] - left[1] + 1)
    right_area = (right[2] - right[0] + 1) * (right[3] - right[1] + 1)
    union = left_area + right_area - intersection
    return intersection / union if union else 0.0


def rank_windows(summary_path: Path, annotations_path: Path, clip_id: str,
                 target_label: str, window_length: int, threshold: float) -> dict:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    frames = {int(item["frame_index"]): item for item in summary["frames"]}
    annotations: dict[int, list[dict]] = defaultdict(list)
    with annotations_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["clip_id"] == clip_id and row["label"] == target_label:
                annotations[int(row["frame_index"])].append(row)

    per_frame = {}
    for frame_index, frame in frames.items():
        frame_hits = []
        candidate_boxes = []
        for candidate_index, candidate in enumerate(frame["candidates"]):
            candidate_box = (
                int(candidate["xmin"]) * 5, int(candidate["ymin"]) * 5,
                int(candidate["xmax"]) * 5 + 4, int(candidate["ymax"]) * 5 + 4)
            candidate_boxes.append(candidate_box)
            best = None
            for annotation in annotations.get(frame_index, []):
                annotation_box = tuple(int(annotation[key]) for key in
                                       ("xmin", "ymin", "xmax", "ymax"))
                overlap = inclusive_iou(candidate_box, annotation_box)
                if best is None or overlap > best["iou"]:
                    best = {"candidate_index": candidate_index,
                            "object_id": annotation["object_id"], "iou": overlap}
            if best is not None and best["iou"] >= threshold:
                frame_hits.append(best)
        annotation_hits = []
        for annotation in annotations.get(frame_index, []):
            annotation_box = tuple(int(annotation[key]) for key in
                                   ("xmin", "ymin", "xmax", "ymax"))
            best_iou = max((inclusive_iou(box, annotation_box) for box in candidate_boxes),
                           default=0.0)
            annotation_hits.append({"object_id": annotation["object_id"],
                                    "iou": best_iou, "covered": best_iou >= threshold})
        per_frame[frame_index] = {
            "candidate_count": len(frame["candidates"]),
            "hits": frame_hits,
            "annotation_hits": annotation_hits,
        }

    indices = sorted(frames)
    windows = []
    for start in indices:
        end = start + window_length - 1
        if end not in frames:
            continue
        entries = [per_frame[index] for index in range(start, end + 1)]
        hits = [hit for entry in entries for hit in entry["hits"]]
        hit_frames = sum(bool(entry["hits"]) for entry in entries)
        windows.append({
            "start_frame": start,
            "end_frame": end,
            "target_hit_frames": hit_frames,
            "target_hit_count": len(hits),
            "distinct_target_tracks": len({hit["object_id"] for hit in hits}),
            "candidate_count": sum(entry["candidate_count"] for entry in entries),
            "maximum_iou": max((hit["iou"] for hit in hits), default=0.0),
        })
    windows.sort(key=lambda item: (
        -item["target_hit_frames"], -item["distinct_target_tracks"],
        -item["maximum_iou"], item["candidate_count"], item["start_frame"]))
    all_annotation_hits = [hit for frame in per_frame.values()
                           for hit in frame["annotation_hits"]]
    covered_annotation_hits = [hit for hit in all_annotation_hits if hit["covered"]]
    return {
        "status": "python_geometry_window_ranking_not_rtl_evidence",
        "target_label": target_label,
        "iou_threshold": threshold,
        "window_length": window_length,
        "coordinate_mapping": "analysis inclusive bbox maps to [xmin*5,ymin*5,xmax*5+4,ymax*5+4]",
        "limitations": (
            "An isolated replay relearns its background during its first four frames, so its "
            "candidates can differ from this long-scan ranking. Human review and RTL replay remain required."),
        "target_annotation_coverage": {
            "annotation_row_count": len(all_annotation_hits),
            "covered_annotation_row_count": len(covered_annotation_hits),
            "coverage_rate": (len(covered_annotation_hits) / len(all_annotation_hits)
                              if all_annotation_hits else None),
            "distinct_tracks": len({hit["object_id"] for hit in all_annotation_hits}),
            "covered_distinct_tracks": len({hit["object_id"] for hit in covered_annotation_hits}),
        },
        "windows": windows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--window-length", type=int, default=20)
    parser.add_argument("--iou-threshold", type=float, default=.1)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.window_length < 5 or args.top < 1 or not 0 <= args.iou_threshold <= 1:
        raise ValueError("invalid window length, top count, or IoU threshold")
    report = rank_windows(args.summary, args.annotations, args.clip_id,
                          args.target_label, args.window_length, args.iou_threshold)
    report["windows"] = report["windows"][:args.top]
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
