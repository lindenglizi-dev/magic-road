#!/usr/bin/env python3
"""Sweep small-candidate box shapes without decoding video or changing selection.

This consumes a fixed-budget prototype receipt.  It keeps the selected component
IDs and per-frame budget fixed, changes only the experimental small-branch box,
and reports annotation-row coverage plus box-overlap conflicts.  It is a geometry
diagnostic, not a classifier, RTL implementation, or acceptance result.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path


VARIANTS = {
    "square4_center": (4, 4, None, None),
    "pedestrian_6x12_top1": (6, 12, 1, None),
    "pedestrian_6x16_top2": (6, 16, 2, None),
    "pedestrian_8x16_top2": (8, 16, 2, None),
    "pedestrian_8x20_top2": (8, 20, 2, None),
    "perspective_y90_6x16": (6, 16, 2, 90),
    "perspective_y100_6x16": (6, 16, 2, 100),
    "perspective_y110_6x16": (6, 16, 2, 110),
    "perspective_y120_6x16": (6, 16, 2, 120),
}
IOU_THRESHOLDS = (0.1, 0.25, 0.5)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def inclusive_iou(left: tuple[int, int, int, int],
                  right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = max(0, left[2] - left[0] + 1) * max(0, left[3] - left[1] + 1)
    right_area = max(0, right[2] - right[0] + 1) * max(0, right[3] - right[1] + 1)
    union = left_area + right_area - intersection
    return intersection / union if union else 0.0


def expand_box(raw: tuple[int, int, int, int], minimum_width: int,
               minimum_height: int, top_margin: int | None,
               image_width: int, image_height: int) -> tuple[int, int, int, int]:
    """Expand an inclusive box either about its center or below its top edge."""
    x0, y0, x1, y1 = raw
    width = min(image_width, max(x1 - x0 + 1, minimum_width))
    height = min(image_height, max(y1 - y0 + 1, minimum_height))
    center_x = (x0 + x1) / 2.0
    new_x0 = max(0, min(int(math.floor(center_x - (width - 1) / 2.0)),
                        image_width - width))
    if top_margin is None:
        center_y = (y0 + y1) / 2.0
        new_y0 = int(math.floor(center_y - (height - 1) / 2.0))
    else:
        # The small moving response is often head/torso.  Leave a small margin
        # above it and put the remaining hypothesis below, while containing raw.
        new_y0 = max(y0 - top_margin, y1 - height + 1)
    new_y0 = max(0, min(new_y0, image_height - height))
    return new_x0, new_y0, new_x0 + width - 1, new_y0 + height - 1


def source_box(box: tuple[int, int, int, int], stride: int,
               width: int, height: int) -> tuple[int, int, int, int]:
    return (box[0] * stride, box[1] * stride,
            min(width - 1, (box[2] + 1) * stride - 1),
            min(height - 1, (box[3] + 1) * stride - 1))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def rate_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    labels = ["all", *sorted({str(row["label"]) for row in rows})]
    for label in labels:
        subset = rows if label == "all" else [row for row in rows if row["label"] == label]
        entry: dict[str, object] = {"annotation_rows": len(subset)}
        for threshold in IOU_THRESHOLDS:
            key = str(threshold)
            main = sum(float(row["main_max_iou"]) >= threshold for row in subset)
            combined = sum(float(row["combined_max_iou"]) >= threshold for row in subset)
            entry[key] = {
                "main_covered": main,
                "combined_covered": combined,
                "main_rate": main / len(subset) if subset else None,
                "combined_rate": combined / len(subset) if subset else None,
            }
        result[label] = entry
    return result


def validate_development_receipt(report: dict[str, object],
                                 catalog_path: Path) -> dict[str, object]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    matches = [entry for entry in catalog.get("clips", [])
               if entry.get("clip_id") == report.get("clip_id")]
    if len(matches) != 1 or matches[0].get("split") not in {"train", "val"}:
        raise ValueError("fixed-budget receipt is not a cataloged train/val clip")
    if report["hashes"].get("source_video_sha256") != matches[0].get("video_sha256"):
        raise ValueError("fixed-budget video hash differs from development catalog")
    canonical_annotations = catalog_path.parent / "annotations.csv"
    if (not canonical_annotations.is_file() or
            report["hashes"].get("annotations_csv_sha256") != digest(canonical_annotations)):
        raise ValueError("fixed-budget annotations are not the development catalog export")
    return matches[0]


def run(candidate_dir: Path, output: Path, scorer: str,
        source_width: int, source_height: int, catalog_path: Path) -> dict[str, object]:
    if "blind" in str(candidate_dir).lower():
        raise ValueError("blind-reserve input is forbidden")
    report_path = candidate_dir / "report.json"
    candidates_path = candidate_dir / "candidates.csv"
    coverage_path = candidate_dir / "annotation_row_coverage.csv"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    development_clip = validate_development_receipt(report, catalog_path)
    if digest(candidates_path) != report["hashes"]["candidates_csv_sha256"]:
        raise ValueError("candidate CSV differs from fixed-budget receipt")
    if digest(coverage_path) != report["hashes"]["annotation_row_coverage_csv_sha256"]:
        raise ValueError("coverage CSV differs from fixed-budget receipt")
    stride = int(report["parameters"]["sample_stride"])
    analysis_width = math.ceil(source_width / stride)
    analysis_height = math.ceil(source_height / stride)
    candidate_rows = [row for row in read_csv(candidates_path) if row["scorer"] == scorer]
    annotation_rows = [row for row in read_csv(coverage_path) if row["scorer"] == scorer]
    if not candidate_rows or not annotation_rows:
        raise ValueError(f"scorer has no candidates or annotations: {scorer}")
    by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in candidate_rows:
        by_frame[int(row["frame_index"])].append(row)

    results = []
    for name, (minimum_width, minimum_height, top_margin, minimum_center_y) in VARIANTS.items():
        frame_boxes: dict[int, list[tuple[str, tuple[int, int, int, int]]]] = defaultdict(list)
        main_boxes: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
        conflict_pairs = 0
        conflict_frames = 0
        for frame_index, frame_rows in by_frame.items():
            expanded = []
            for row in frame_rows:
                selected = tuple(int(value) for value in json.loads(row["selected_analysis_box"]))
                if row["branch"] == "small_component_experimental":
                    raw = tuple(int(value) for value in json.loads(row["raw_analysis_box"]))
                    use_person_shape = (minimum_center_y is None or
                                        (raw[1] + raw[3]) / 2.0 >= minimum_center_y)
                    if use_person_shape:
                        selected = expand_box(raw, minimum_width, minimum_height, top_margin,
                                              analysis_width, analysis_height)
                    else:
                        selected = expand_box(raw, 4, 4, None,
                                              analysis_width, analysis_height)
                mapped = source_box(selected, stride, source_width, source_height)
                frame_boxes[frame_index].append((row["branch"], mapped))
                if row["branch"] == "main_area_topk":
                    main_boxes[frame_index].append(mapped)
                expanded.append(mapped)
            pairs = sum(inclusive_iou(expanded[left], expanded[right]) > 0.3
                        for left in range(len(expanded))
                        for right in range(left + 1, len(expanded)))
            conflict_pairs += pairs
            conflict_frames += pairs > 0

        scored_rows = []
        for annotation in annotation_rows:
            frame_index = int(annotation["frame_index"])
            target = tuple(int(value) for value in json.loads(annotation["annotation_box"]))
            all_iou = [inclusive_iou(box, target) for _, box in frame_boxes[frame_index]]
            main_iou = [inclusive_iou(box, target) for box in main_boxes[frame_index]]
            scored_rows.append({
                "label": annotation["label"],
                "main_max_iou": max(main_iou, default=0.0),
                "combined_max_iou": max(all_iou, default=0.0),
            })
        results.append({
            "variant": name,
            "minimum_analysis_box": [minimum_width, minimum_height],
            "top_margin_analysis_pixels": top_margin,
            "person_shape_minimum_component_center_y": minimum_center_y,
            "source_minimum_extent": [minimum_width * stride, minimum_height * stride],
            "candidate_count": len(candidate_rows),
            "overlap_pairs_iou_gt_0.3": conflict_pairs,
            "frames_with_overlap_iou_gt_0.3": conflict_frames,
            "annotation_coverage": rate_summary(scored_rows),
        })

    document = {
        "status": "offline_fixed_selection_box_geometry_diagnostic_not_acceptance_evidence",
        "candidate_dir": str(candidate_dir.resolve()),
        "clip_id": report["clip_id"],
        "scored_frame_interval_inclusive": report["scored_frame_interval_inclusive"],
        "scorer": scorer,
        "fixed_selection_contract": (
            "Candidate IDs, component ranking, branch assignment and per-frame count are read "
            "unchanged from the fixed-budget receipt; only small-branch box geometry changes."),
        "hashes": {
            "fixed_budget_report_sha256": digest(report_path),
            "candidates_csv_sha256": digest(candidates_path),
            "annotation_row_coverage_csv_sha256": digest(coverage_path),
            "script_sha256": digest(Path(__file__)),
            "development_catalog_sha256": digest(catalog_path),
        },
        "catalog_split": development_clip["split"],
        "source_geometry": {"width": source_width, "height": source_height,
                            "sample_stride": stride},
        "iou_thresholds": list(IOU_THRESHOLDS),
        "results": results,
        "boundary": (
            "Coverage counts correlated annotation-frame rows. Larger boxes can improve IoU "
            "while adding background or neighboring objects; every selected geometry still "
            "requires ROI review and classifier validation. Reported overlap is diagnostic "
            "because NMS was not rerun after offline expansion."),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return document


def self_test() -> None:
    assert expand_box((10, 10, 11, 11), 4, 4, None, 30, 30) == (9, 9, 12, 12)
    assert expand_box((10, 10, 11, 11), 6, 12, 1, 30, 30) == (8, 9, 13, 20)
    assert expand_box((0, 0, 1, 1), 6, 12, 2, 30, 30) == (0, 0, 5, 11)
    assert inclusive_iou((0, 0, 1, 1), (0, 0, 1, 1)) == 1.0
    assert source_box((1, 2, 3, 4), 5, 1280, 720) == (5, 10, 19, 24)
    print("PASS: centered/top-anchored expansion, clipping, IoU and source mapping")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scorer", default="peak_difference")
    parser.add_argument("--source-width", type=int, default=1280)
    parser.add_argument("--source-height", type=int, default=720)
    parser.add_argument("--catalog", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/catalog.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.candidate_dir is None or args.output is None:
        parser.error("--candidate-dir and --output are required unless --self-test is used")
    document = run(args.candidate_dir, args.output, args.scorer,
                   args.source_width, args.source_height, args.catalog)
    print(json.dumps({"status": document["status"], "clip_id": document["clip_id"],
                      "results": document["results"], "output": str(args.output.resolve())},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
