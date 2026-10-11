#!/usr/bin/env python3
"""Single-decode perspective-threshold sweep for internal8-to-final4.

The deployed Python candidate chain is processed causally from source frame zero.
For every scored frame, the same post-cleanup components feed five geometry-only
variants.  Each variant builds area-top4 main plus peak-difference-top4 small
candidates, applies perspective expansion before unified greedy NMS, and emits at
most four final candidates.  This is development diagnostic evidence, not RTL or
acceptance evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference
from fixed_budget_candidate_prototype import (
    Component,
    build_internal8_pool,
    digest,
    extract_components,
    inclusive_iou,
    internal8_arbitration_key,
    source_box,
    validate_development_inputs,
)


DEFAULT_THRESHOLDS = (90, 100, 110, 120, 130)
IOU_THRESHOLDS = (0.1, 0.25, 0.5)
SOURCE_WIDTH = 1280
SOURCE_HEIGHT = 720
SAMPLE_STRIDE = 5
MAIN_MIN_AREA = 16
SMALL_MIN_AREA = 2
SMALL_MAX_AREA = 15
INTERNAL_MAIN_SLOTS = 4
INTERNAL_SMALL_SLOTS = 4
FINAL_SLOTS = 4
PERSPECTIVE_WIDTH = 6
PERSPECTIVE_HEIGHT = 16
PERSPECTIVE_TOP_MARGIN = 2
SQUARE_WIDTH = 4
SQUARE_HEIGHT = 4
NMS_IOU = 0.3


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def reject_non_development_path(path: Path) -> None:
    lowered = str(path).lower()
    if "blind" in lowered or "holdout" in lowered or "reserve" in lowered:
        raise ValueError("blind/holdout/reserve inputs are forbidden")


def ped_y_band(center_y: float) -> str:
    if center_y < 90:
        return "lt90"
    if center_y < 100:
        return "90_to_lt100"
    if center_y < 110:
        return "100_to_lt110"
    if center_y < 120:
        return "110_to_lt120"
    if center_y < 130:
        return "120_to_lt130"
    return "ge130"


def load_annotations(path: Path, clip_id: str, start_frame: int,
                     frame_count: int) -> dict[int, list[dict[str, object]]]:
    reject_non_development_path(path)
    result: dict[int, list[dict[str, object]]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for csv_line, row in enumerate(csv.DictReader(handle), start=2):
            frame = int(row["frame_index"])
            if (row["clip_id"] != clip_id or row["label"] not in {"ped", "vehicle"} or
                    not start_frame <= frame < start_frame + frame_count):
                continue
            box = tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
            center_y = (box[1] + box[3]) / (2.0 * SAMPLE_STRIDE)
            result[frame].append({
                "annotation_csv_line": csv_line,
                "frame_index": frame,
                "label": row["label"],
                "object_id": row["object_id"],
                "annotation_box": box,
                "truth_center_y_analysis": center_y,
                "truth_center_y_band": ped_y_band(center_y) if row["label"] == "ped" else "all",
            })
    return result


def select_internal8_to4(
        components: list[Component], perspective_threshold: int,
        image_width: int, image_height: int) -> tuple[list[dict[str, object]], dict[str, int]]:
    """Build the fixed internal pool and apply integer-priority greedy NMS."""
    pool = build_internal8_pool(
        components, 20, MAIN_MIN_AREA, SMALL_MIN_AREA, SMALL_MAX_AREA,
        SQUARE_WIDTH, SQUARE_HEIGHT, image_width, image_height, "perspective",
        perspective_threshold, PERSPECTIVE_WIDTH, PERSPECTIVE_HEIGHT,
        PERSPECTIVE_TOP_MARGIN)
    main_pool = [row for row in pool if row["branch"] == "main_area_topk"]
    small_pool = [row for row in pool
                  if row["branch"] == "small_component_experimental"]

    pair_counts: Counter[str] = Counter()
    for left_index, left in enumerate(pool):
        for right in pool[left_index + 1:]:
            if inclusive_iou(left["selected_box"], right["selected_box"]) > NMS_IOU:
                branches = sorted((str(left["branch"]), str(right["branch"])))
                if branches[0] == branches[1] == "main_area_topk":
                    pair_counts["main_main_pair_conflicts"] += 1
                elif branches[0] == branches[1] == "small_component_experimental":
                    pair_counts["small_small_pair_conflicts"] += 1
                else:
                    pair_counts["main_small_pair_conflicts"] += 1

    accepted: list[dict[str, object]] = []
    rejection_counts: Counter[str] = Counter()
    for arbitration_rank, entry in enumerate(sorted(pool, key=internal8_arbitration_key)):
        conflicts = [item for item in accepted
                     if inclusive_iou(entry["selected_box"], item["selected_box"]) > NMS_IOU]
        if conflicts:
            rejection_counts["nms_rejected_candidates"] += 1
            rejection_counts[f"nms_rejected_{entry['branch']}"] += 1
            continue
        accepted.append({**entry, "final_arbitration_rank": arbitration_rank})
        if len(accepted) == FINAL_SLOTS:
            break
    diagnostics = {
        "internal_pool_candidates": len(pool),
        "internal_main_candidates": len(main_pool),
        "internal_small_candidates": len(small_pool),
        "final_candidates": len(accepted),
        "final_main_candidates": sum(row["branch"] == "main_area_topk" for row in accepted),
        "final_small_candidates": sum(
            row["branch"] == "small_component_experimental" for row in accepted),
        "final_empty_slots": FINAL_SLOTS - len(accepted),
        "frames_at_final4": int(len(accepted) == FINAL_SLOTS),
        "frames_with_any_pair_conflict": int(sum(pair_counts.values()) > 0),
        "frames_with_nms_rejection": int(rejection_counts["nms_rejected_candidates"] > 0),
        **{key: pair_counts[key] for key in (
            "main_main_pair_conflicts", "main_small_pair_conflicts",
            "small_small_pair_conflicts")},
        **{key: rejection_counts[key] for key in (
            "nms_rejected_candidates", "nms_rejected_main_area_topk",
            "nms_rejected_small_component_experimental")},
    }
    return accepted, diagnostics


def add_coverage_rows(
        destination: list[dict[str, object]], annotations: list[dict[str, object]],
        threshold: int, accepted: list[dict[str, object]],
        main_pool: list[dict[str, object]], source_width: int,
        source_height: int) -> None:
    final_records = []
    for slot, entry in enumerate(accepted):
        final_records.append({
            "candidate_id": f"y{threshold}:f{annotations[0]['frame_index'] if annotations else 0:06d}:slot{slot}",
            "branch": entry["branch"],
            "box": source_box(entry["selected_box"], SAMPLE_STRIDE,
                              source_width, source_height),
        })
    main_boxes = [source_box(entry["selected_box"], SAMPLE_STRIDE,
                             source_width, source_height) for entry in main_pool]
    for annotation in annotations:
        truth_box = annotation["annotation_box"]
        matches = [(inclusive_iou(truth_box, row["box"]), row)
                   for row in final_records]
        best = max(matches, key=lambda item: item[0], default=(0.0, None))
        main_iou = max((inclusive_iou(truth_box, box) for box in main_boxes), default=0.0)
        row = {
            "perspective_y_threshold": threshold,
            "annotation_csv_line": annotation["annotation_csv_line"],
            "frame_index": annotation["frame_index"],
            "label": annotation["label"],
            "object_id": annotation["object_id"],
            "truth_center_y_analysis": annotation["truth_center_y_analysis"],
            "truth_center_y_band": annotation["truth_center_y_band"],
            "annotation_box": list(truth_box),
            "main_top4_max_iou": main_iou,
            "final_max_iou": best[0],
            "matched_candidate_id": best[1]["candidate_id"] if best[1] else "",
            "matched_branch": best[1]["branch"] if best[1] else "",
        }
        for iou_threshold in IOU_THRESHOLDS:
            suffix = str(iou_threshold).replace(".", "p")
            row[f"main_covered_iou_{suffix}"] = main_iou >= iou_threshold
            row[f"final_covered_iou_{suffix}"] = best[0] >= iou_threshold
        destination.append(row)


def aggregate_threshold_metrics(
        coverage_rows: list[dict[str, object]],
        candidate_metrics: dict[int, Counter[str]]) -> list[dict[str, object]]:
    result = []
    for threshold in sorted(candidate_metrics):
        threshold_rows = [row for row in coverage_rows
                          if row["perspective_y_threshold"] == threshold]
        scopes = [("ped", "all"), ("vehicle", "all")]
        scopes.extend(("ped", band) for band in
                      ("lt90", "90_to_lt100", "100_to_lt110", "110_to_lt120",
                       "120_to_lt130", "ge130"))
        for label, band in scopes:
            subset = [row for row in threshold_rows if row["label"] == label and
                      (band == "all" or row["truth_center_y_band"] == band)]
            metrics = candidate_metrics[threshold]
            row = {
                "perspective_y_threshold": threshold,
                "label": label,
                "truth_center_y_band": band,
                "annotation_rows": len(subset),
                "final_candidate_count": metrics["final_candidates"],
                "final_empty_slots": metrics["final_empty_slots"],
                "internal_main_count": metrics["internal_main_candidates"],
                "retained_main_count": metrics["final_main_candidates"],
                "main_top4_retention_rate": (
                    metrics["final_main_candidates"] / metrics["internal_main_candidates"]
                    if metrics["internal_main_candidates"] else None),
                "nms_rejected_candidates": metrics["nms_rejected_candidates"],
                "main_main_pair_conflicts": metrics["main_main_pair_conflicts"],
                "main_small_pair_conflicts": metrics["main_small_pair_conflicts"],
                "small_small_pair_conflicts": metrics["small_small_pair_conflicts"],
            }
            for iou_threshold in IOU_THRESHOLDS:
                suffix = str(iou_threshold).replace(".", "p")
                main = sum(bool(item[f"main_covered_iou_{suffix}"]) for item in subset)
                final = sum(bool(item[f"final_covered_iou_{suffix}"]) for item in subset)
                row[f"main_covered_iou_{suffix}"] = main
                row[f"final_covered_iou_{suffix}"] = final
                row[f"main_coverage_rate_iou_{suffix}"] = (
                    main / len(subset) if subset else None)
                row[f"final_coverage_rate_iou_{suffix}"] = (
                    final / len(subset) if subset else None)
            result.append(row)
    return result


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> dict[str, object]:
    for path in (args.video, args.annotations, args.catalog):
        reject_non_development_path(path)
    if (args.start_frame < 0 or args.frames < 1 or
            len(set(args.thresholds)) != len(args.thresholds) or
            any(value < 0 for value in args.thresholds)):
        raise ValueError("invalid frame interval or perspective thresholds")
    clip = validate_development_inputs(
        args.video, args.annotations, args.clip_id, args.catalog)
    if clip["split"] not in {"train", "val"}:
        raise ValueError("only cataloged train/val clips are allowed")
    annotations = load_annotations(
        args.annotations, args.clip_id, args.start_frame, args.frames)
    chain = CandidateChainReference(
        learn_frames=4, threshold=20, min_neighbors=3, min_area=MAIN_MIN_AREA,
        update_enable=True, freeze_foreground=True, min_run=2, top_k=4,
        sample_stride=SAMPLE_STRIDE)
    coverage_rows: list[dict[str, object]] = []
    candidate_metrics = {threshold: Counter() for threshold in args.thresholds}
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {args.video}")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (width, height) != (SOURCE_WIDTH, SOURCE_HEIGHT):
        capture.release()
        raise ValueError(f"expected 1280x720 video, got {width}x{height}")
    processed_total = 0
    processed_scored = 0
    try:
        for frame_index in range(args.start_frame + args.frames):
            ok, frame = capture.read()
            if not ok:
                break
            processed_total += 1
            chain_result = chain.process_bgr(frame, frame_index)
            if frame_index < args.start_frame:
                continue
            processed_scored += 1
            components = extract_components(
                chain_result["run_filtered_mask"], chain_result["difference"])
            for threshold in args.thresholds:
                pool = build_internal8_pool(
                    components, 20, MAIN_MIN_AREA, SMALL_MIN_AREA, SMALL_MAX_AREA,
                    SQUARE_WIDTH, SQUARE_HEIGHT, chain.analysis_shape[1],
                    chain.analysis_shape[0], "perspective", threshold,
                    PERSPECTIVE_WIDTH, PERSPECTIVE_HEIGHT,
                    PERSPECTIVE_TOP_MARGIN)
                main_pool = [row for row in pool if row["branch"] == "main_area_topk"]
                accepted, diagnostics = select_internal8_to4(
                    components, threshold, chain.analysis_shape[1],
                    chain.analysis_shape[0])
                candidate_metrics[threshold].update(diagnostics)
                add_coverage_rows(
                    coverage_rows, annotations.get(frame_index, []), threshold,
                    accepted, main_pool, width, height)
    finally:
        capture.release()
    if processed_scored != args.frames:
        raise ValueError(f"decoded only {processed_scored}/{args.frames} scoring frames")

    threshold_rows = aggregate_threshold_metrics(coverage_rows, candidate_metrics)
    args.output.mkdir(parents=True, exist_ok=True)
    coverage_path = args.output / "annotation_coverage.csv"
    metrics_path = args.output / "threshold_metrics.csv"
    write_csv(coverage_path, coverage_rows)
    write_csv(metrics_path, threshold_rows)
    script_path = Path(__file__)
    fixed_path = script_path.with_name("fixed_budget_candidate_prototype.py")
    chain_path = script_path.with_name("candidate_chain_reference.py")
    report = {
        "status": "single_decode_perspective_threshold_final4_diagnostic_not_rtl_or_acceptance_evidence",
        "clip_id": args.clip_id,
        "catalog_split": clip["split"],
        "scored_frame_interval_inclusive": [args.start_frame,
                                             args.start_frame + args.frames - 1],
        "processed_frames_including_causal_warmup": processed_total,
        "processed_scoring_frames": processed_scored,
        "perspective_y_thresholds": args.thresholds,
        "input_hashes": {
            "video_sha256": digest(args.video),
            "annotations_sha256": digest(args.annotations),
            "catalog_sha256": digest(args.catalog),
        },
        "script_hashes": {
            "sweep_script_sha256": digest(script_path),
            "fixed_budget_dependency_sha256": digest(fixed_path),
            "candidate_chain_dependency_sha256": digest(chain_path),
        },
        "output_hashes": {
            "annotation_coverage_csv_sha256": digest(coverage_path),
            "threshold_metrics_csv_sha256": digest(metrics_path),
        },
        "parameters": {
            "deployed_candidate_chain": {
                "sample_stride": SAMPLE_STRIDE, "learn_frames": 4,
                "difference_threshold": 20, "min_neighbors": 3,
                "min_run": 2, "main_min_area": MAIN_MIN_AREA,
            },
            "internal_pool": {"main_area_topk": INTERNAL_MAIN_SLOTS,
                              "small_peak_difference_topk": INTERNAL_SMALL_SLOTS,
                              "maximum_candidates": 8},
            "small_geometry": {
                "upper_square_minimum": [SQUARE_WIDTH, SQUARE_HEIGHT],
                "lower_perspective_minimum": [PERSPECTIVE_WIDTH,
                                               PERSPECTIVE_HEIGHT],
                "perspective_top_margin": PERSPECTIVE_TOP_MARGIN,
                "center_y_rule": "perspective when component center_y >= threshold",
            },
            "final_arbitration": {
                "maximum_outputs": FINAL_SLOTS,
                "sort_key": "peak_difference desc, area desc, component_label asc",
                "nms_rule": f"reject when inclusive IoU > {NMS_IOU}; continue for refill",
            },
            "coverage_iou_thresholds": list(IOU_THRESHOLDS),
            "ped_truth_center_y_bands": [
                "lt90", "90_to_lt100", "100_to_lt110", "110_to_lt120",
                "120_to_lt130", "ge130"],
        },
        "threshold_summaries": [
            {"perspective_y_threshold": threshold,
             **dict(candidate_metrics[threshold]),
             "main_top4_retention_rate": (
                 candidate_metrics[threshold]["final_main_candidates"] /
                 candidate_metrics[threshold]["internal_main_candidates"]
                 if candidate_metrics[threshold]["internal_main_candidates"] else None)}
            for threshold in sorted(candidate_metrics)],
        "contracts": {
            "causal_decode": (
                "Decode and update one deployed background model from source frame 0. "
                "Only geometry expansion and final arbitration are repeated per threshold."),
            "common_main_baseline": (
                "main_top4_max_iou uses the same raw area-top4 main boxes for every "
                "perspective threshold before final arbitration."),
            "truth_y": (
                "Pedestrian band uses canonical source-box center divided by stride five; "
                "it is a truth-box proxy, not the CCL component center used for expansion."),
            "nms_diagnostics": (
                "Pair-conflict counts cover every pair in the internal pool. Rejection "
                "counts cover the priority scan until four outputs are filled or the pool "
                "is exhausted."),
            "report_payload_sha256": (
                "SHA256 of canonical JSON before adding report_payload_sha256; CSV hashes "
                "cover the two tabular output files."),
        },
        "boundary": (
            "VIRAT annotations are not exhaustive background truth, so candidate counts "
            "and NMS conflicts are workload diagnostics rather than false-positive rates. "
            "Python 8-connectivity does not model RTL MAX_RUN/MAX_LABEL overflow or label-"
            "union timing. No blind, holdout or reserve input is accepted."),
    }
    report["report_payload_sha256"] = canonical_digest(report)
    report_path = args.output / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    return report


def self_test() -> None:
    def component(label: int, area: int, box: tuple[int, int, int, int],
                  peak: int) -> Component:
        return Component(label, area, *box, 1.0, float(peak), peak)

    components = [
        component(1, 16, (0, 0, 3, 3), 190),
        component(2, 16, (12, 0, 15, 3), 180),
        component(3, 16, (24, 0, 27, 3), 170),
        component(4, 16, (36, 0, 39, 3), 160),
        component(5, 2, (1, 1, 2, 1), 200),
        component(6, 2, (50, 20, 51, 20), 100),
    ]
    accepted, diagnostics = select_internal8_to4(components, 110, 64, 32)
    assert [row["component"].label for row in accepted] == [5, 2, 3, 4]
    assert diagnostics["final_candidates"] == 4
    assert diagnostics["final_empty_slots"] == 0
    assert diagnostics["final_main_candidates"] == 3
    assert diagnostics["nms_rejected_main_area_topk"] == 1
    rows: list[dict[str, object]] = []
    annotations = [{
        "annotation_csv_line": 2, "frame_index": 0, "label": "ped",
        "object_id": "ped-1", "annotation_box": (5, 5, 14, 14),
        "truth_center_y_analysis": 1.9, "truth_center_y_band": "lt90"}]
    pool = build_internal8_pool(
        components, 20, 16, 2, 15, 4, 4, 64, 32, "perspective", 110,
        6, 16, 2)
    add_coverage_rows(rows, annotations, 110, accepted,
                      [row for row in pool if row["branch"] == "main_area_topk"],
                      320, 160)
    metrics = aggregate_threshold_metrics(rows, {110: Counter(diagnostics)})
    assert len(rows) == 1 and rows[0]["perspective_y_threshold"] == 110
    assert any(row["label"] == "ped" and row["truth_center_y_band"] == "lt90"
               for row in metrics)
    with tempfile.TemporaryDirectory(prefix="sweep_fixture_") as temporary:
        root = Path(temporary)
        video = root / "fixture.avi"
        writer = cv2.VideoWriter(
            str(video), cv2.VideoWriter_fourcc(*"MJPG"), 5.0,
            (SOURCE_WIDTH, SOURCE_HEIGHT))
        if not writer.isOpened():
            raise RuntimeError("self-test video writer unavailable")
        for frame_index in range(6):
            frame = np.zeros((SOURCE_HEIGHT, SOURCE_WIDTH, 3), np.uint8)
            if frame_index >= 4:
                frame[100:140, 100:140] = 255
            writer.write(frame)
        writer.release()
        annotations_path = root / "annotations.csv"
        with annotations_path.open("w", encoding="utf-8", newline="") as handle:
            csv_writer = csv.DictWriter(handle, [
                "clip_id", "frame_index", "xmin", "ymin", "xmax", "ymax",
                "label", "object_id"])
            csv_writer.writeheader()
            csv_writer.writerow({
                "clip_id": "fixture", "frame_index": 4, "xmin": 100,
                "ymin": 100, "xmax": 139, "ymax": 139, "label": "ped",
                "object_id": "ped-1"})
        catalog_path = root / "catalog.json"
        catalog_path.write_text(json.dumps({"clips": [{
            "clip_id": "fixture", "split": "train",
            "video_sha256": digest(video)}]}), encoding="utf-8")
        output = root / "output"
        smoke = run(argparse.Namespace(
            video=video, annotations=annotations_path, catalog=catalog_path,
            clip_id="fixture", start_frame=0, frames=6,
            thresholds=[90, 110], output=output))
        assert smoke["processed_frames_including_causal_warmup"] == 6
        assert smoke["perspective_y_thresholds"] == [90, 110]
        for name in ("report.json", "annotation_coverage.csv", "threshold_metrics.csv"):
            assert (output / name).is_file()
        assert smoke["output_hashes"]["annotation_coverage_csv_sha256"] == digest(
            output / "annotation_coverage.csv")
    with tempfile.TemporaryDirectory(prefix="blind_holdout_") as temporary:
        try:
            reject_non_development_path(Path(temporary))
        except ValueError as exc:
            assert "forbidden" in str(exc)
        else:
            raise AssertionError("blind/holdout guard did not trigger")
    print("PASS: internal8/NMS, exact-IoU aggregation, single-decode smoke and input guard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--catalog", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/catalog.json"))
    parser.add_argument("--clip-id")
    parser.add_argument("--start-frame", type=int)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--perspective-y-threshold", type=int, action="append",
                        dest="thresholds")
    parser.add_argument("--self-test", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    required = ("video", "annotations", "clip_id", "start_frame", "frames", "output")
    missing = [name for name in required if getattr(args, name) is None]
    if missing:
        parser.error("required unless --self-test: " + ", ".join(
            "--" + name.replace("_", "-") for name in missing))
    args.thresholds = args.thresholds or list(DEFAULT_THRESHOLDS)
    report = run(args)
    print(json.dumps({
        "status": report["status"],
        "processed_frames_including_causal_warmup":
            report["processed_frames_including_causal_warmup"],
        "processed_scoring_frames": report["processed_scoring_frames"],
        "thresholds": report["perspective_y_thresholds"],
        "output": str(args.output.resolve()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
