#!/usr/bin/env python3
"""Measure CCL/annotation overlap without turning unmatched boxes into negative labels."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analysis_box(row: dict[str, str]) -> tuple[int, int, int, int] | None:
    box = (math.ceil(int(row["xmin"]) / 5), math.ceil(int(row["ymin"]) / 5),
           int(row["xmax"]) // 5, int(row["ymax"]) // 5)
    return box if box[0] <= box[2] and box[1] <= box[3] else None


def iou(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = (left[2] - left[0] + 1) * (left[3] - left[1] + 1)
    right_area = (right[2] - right[0] + 1) * (right[3] - right[1] + 1)
    return intersection / (left_area + right_area - intersection)


def match(annotations_path: Path, candidates_path: Path, clip_id: str,
          evaluated_frames: set[int] | None = None) -> tuple[list[dict], dict]:
    with candidates_path.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    candidate_frames = {int(row["source_frame"]) for row in candidates}
    frame_scope = set(evaluated_frames) if evaluated_frames is not None else candidate_frames
    if not candidate_frames <= frame_scope:
        raise ValueError("candidate source frame is absent from the replay manifest")
    with annotations_path.open(encoding="utf-8-sig", newline="") as handle:
        source_annotations = [row for row in csv.DictReader(handle)
                              if row["clip_id"] == clip_id and
                              int(row["frame_index"]) in frame_scope]
    if not source_annotations or not candidates:
        raise ValueError("clip annotations and candidates must both be nonempty")

    annotations = []
    collapsed = 0
    by_frame: dict[int, list[dict]] = defaultdict(list)
    for row in source_annotations:
        box = analysis_box(row)
        if box is None:
            collapsed += 1
            continue
        record = {"frame": int(row["frame_index"]), "label": row["label"],
                  "object_id": row["object_id"], "box": box}
        annotations.append(record)
        by_frame[record["frame"]].append(record)

    candidate_records = []
    by_candidate_frame: dict[int, list[tuple[tuple[int, int, int, int], dict]]] = defaultdict(list)
    for row in candidates:
        frame = int(row["source_frame"])
        box = tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
        possible = by_frame.get(frame, [])
        best = max(possible, key=lambda item: iou(box, item["box"])) if possible else None
        best_iou = iou(box, best["box"]) if best else 0.0
        candidate_records.append({
            **row,
            "best_annotation_label": best["label"] if best else "",
            "best_annotation_object_id": best["object_id"] if best else "",
            "best_annotation_iou": f"{best_iou:.6f}",
            "review_hint": (f"overlap_{best['label']}" if best_iou >= .3 else
                            "unmatched_needs_human_review"),
        })
        by_candidate_frame[frame].append((box, row))

    thresholds = (0.1, 0.3, 0.5)
    coverage = {}
    for threshold in thresholds:
        counts: Counter[str] = Counter()
        totals: Counter[str] = Counter()
        for annotation in annotations:
            if annotation["label"] not in {"ped", "vehicle"}:
                continue
            totals[annotation["label"]] += 1
            best_iou = max((iou(annotation["box"], box)
                            for box, _ in by_candidate_frame.get(annotation["frame"], [])), default=0.0)
            counts[annotation["label"]] += int(best_iou >= threshold)
        coverage[str(threshold)] = {
            label: {"covered": counts[label], "total": totals[label],
                    "rate": counts[label] / totals[label] if totals[label] else None}
            for label in ("ped", "vehicle")
        }
    candidate_overlap = {
        str(threshold): sum(float(row["best_annotation_iou"]) >= threshold
                            for row in candidate_records)
        for threshold in thresholds
    }
    report = {
        "status": "diagnostic_overlap_only_not_semantic_labels",
        "clip_id": clip_id,
        "candidate_count": len(candidate_records),
        "annotation_row_count": len(annotations),
        "evaluated_source_frames": sorted(frame_scope),
        "collapsed_annotation_boxes": collapsed,
        "candidate_overlap_counts": candidate_overlap,
        "annotation_coverage_by_label": coverage,
        "annotations_sha256": digest(annotations_path),
        "candidates_sha256": digest(candidates_path),
        "box_mapping": "ceil(xmin/5),ceil(ymin/5),floor(xmax/5),floor(ymax/5), inclusive",
        "boundary": (
            "VIRAT Release 2 object tracks are not treated as exhaustive background truth. "
            "Unmatched candidates remain pending human review and are never auto-labeled invalid. "
            "Coverage is per annotation row and is not end-to-end object/track recall."),
    }
    return candidate_records, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--frame-manifest", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.frame_manifest.read_text(encoding="utf-8"))
    if manifest.get("preprocessing") != "rtl_shift_gray_stride5_v1":
        raise ValueError("unexpected replay preprocessing contract")
    evaluated_frames = {int(row["source_frame"]) for row in manifest["frame_map"]}
    rows, report = match(args.annotations, args.candidates, args.clip_id, evaluated_frames)
    report["frame_manifest_sha256"] = digest(args.frame_manifest)
    args.output.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (args.output / "candidate_matches.csv").open(
            "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(rows)
    report["candidate_matches_sha256"] = digest(args.output / "candidate_matches.csv")
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
