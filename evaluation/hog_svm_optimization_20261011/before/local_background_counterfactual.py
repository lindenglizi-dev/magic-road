#!/usr/bin/env python3
"""Fixed MOG2 foreground counterfactual on the confirmed local development frames."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import cleanup_3x3, filter_short_runs
from local_candidate_stage_diagnostic import checked_components
from local_fourgrid_diagnostic import score_record
from local_paired_diagnostic import FRAME_IDS, digest, dump, iou, match, read_json
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi
from run_local_scene_pilot import (
    DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256, MODEL_DIR, guard_path, load_models,
    make_hog324, quantization_contract,
)


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
ANNOTATIONS = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930/annotations.confirmed.json"
CONFIRMATION = ANNOTATIONS.with_name("confirmation_receipt.json")
BASELINE = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_stage_diagnostic_v1"
SUMMARY = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_diagnostic_summary_v2"
OUTPUT = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_mog2_fixed_v1"
MODEL_SHA256 = "9b6a96aeae291d60628c7352616fade1b03cb280a8ed6c8384b6acd03c13a99a"
CONFIG = {"history": 500, "varThreshold": 16, "detectShadows": False, "learningRate": -1,
          "cleanup": "3x3 center-preserving sum>=3", "min_run": 2,
          "min_area": 16, "top_k": 4}


def verified_json(directory: Path, name: str):
    receipt = read_json(directory / "receipt.json")
    path = directory / name
    expected = receipt.get("artifact_hashes", {}).get(name)
    if expected is not None and digest(path) != expected:
        raise ValueError(f"frozen artifact changed: {path}")
    return read_json(path), digest(path), digest(directory / "receipt.json")


def matching(targets, pool, threshold):
    boxes = [row["source_box"] for row in pool]
    links = match(targets, boxes, threshold)
    return links, [{"track_id": targets[i]["track_id"], "label": targets[i]["label"],
                    "component_label": pool[j]["label"],
                    "iou": iou(targets[i]["box"], boxes[j])}
                   for i, j in links.items()]


def transition(old: bool, new: bool) -> str:
    return "gain" if new and not old else "loss" if old and not new else "same_matched" if new else "same_missed"


def draw_panel(frame, targets, top4, raw, clean, run):
    view = frame.copy()
    for target in targets:
        cv2.rectangle(view, tuple(target["box"][:2]), tuple(target["box"][2:]), (0, 255, 255), 2)
    for row in top4:
        cv2.rectangle(view, tuple(row["source_box"][:2]), tuple(row["source_box"][2:]), (255, 80, 20), 2)
    panels = [cv2.resize(view, (512, 288), interpolation=cv2.INTER_AREA)]
    for mask in (raw, clean, run):
        panels.append(cv2.resize(mask * 255, (512, 288), interpolation=cv2.INTER_NEAREST))
    return np.hstack(panels)


def summarize_target_rows(rows, pool, threshold):
    selected = [row for row in rows if row["pool"] == pool and row["iou_threshold"] == threshold]
    transitions = Counter(row["transition"] for row in selected)
    by_class = {}
    for label in ("ped", "vehicle"):
        subset = [row for row in selected if row["label"] == label]
        by_class[label] = {"targets": len(subset),
                           "baseline_matched": sum(row["baseline_matched"] for row in subset),
                           "mog2_matched": sum(row["mog2_matched"] for row in subset)}
    return {"targets": len(selected), "baseline_matched": sum(row["baseline_matched"] for row in selected),
            "mog2_matched": sum(row["mog2_matched"] for row in selected),
            "paired": dict(transitions), "by_class": by_class}


def run(output: Path):
    started = dt.datetime.now(dt.timezone.utc)
    tick = time.monotonic()
    for path in (output, DEFAULT_VIDEO, ANNOTATIONS, CONFIRMATION, BASELINE, SUMMARY, MODEL_DIR):
        guard_path(path)
    if output.exists():
        raise ValueError("output must be new")
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError("source video changed")

    annotation = read_json(ANNOTATIONS)
    confirmation = read_json(CONFIRMATION)
    if (annotation.get("human_confirmed") is not True or
            annotation.get("evaluation_scope") != "moving_ped_vehicle_only" or
            confirmation.get("derived_sha256") != digest(ANNOTATIONS)):
        raise ValueError("confirmed moving-target annotation chain changed")
    baseline_rows, baseline_hash, baseline_receipt_hash = verified_json(BASELINE, "frame_stages.json")
    _, summary_hash, summary_receipt_hash = verified_json(SUMMARY, "summary.json")
    baseline_by_frame = {row["frame_index"]: row for row in baseline_rows}
    annotations = {row["frame_index"]: row for row in annotation["frames"]}

    parameters, _, model_receipt = load_models(MODEL_DIR)
    if model_receipt.get("model_parameters_sha256") != MODEL_SHA256:
        raise ValueError("fixed model parameters changed")
    hog = make_hog324()
    quant = quantization_contract(parameters["opencv_hog324"])
    mog2 = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

    output.mkdir(parents=True)
    panel_dir = output / "failure_panels"
    panel_dir.mkdir()
    frame_rows, target_rows, panels = [], [], []
    end_to_end = Counter()
    cap = cv2.VideoCapture(str(DEFAULT_VIDEO))
    try:
        for frame_index in range(max(FRAME_IDS) + 1):
            ok, frame = cap.read()
            if not ok or frame.shape[:2] != (720, 1280):
                raise ValueError(f"decode failure at frame {frame_index}")
            gray = fpga_analysis_frame(frame)
            raw = (mog2.apply(gray, learningRate=-1) != 0).astype(np.uint8)
            clean = cleanup_3x3(raw, 3, True)
            run_mask = filter_short_runs(clean, 2)
            if frame_index not in annotations:
                continue

            targets = [target for target in annotations[frame_index]["targets"]
                       if target["motion"] == "moving" and target["label"] in ("ped", "vehicle")]
            all_components = checked_components(run_mask)
            area16 = [row for row in all_components if row["area"] >= 16]
            top4 = area16[:4]
            pools = {"all_ccl_area16": area16, "top4": top4}
            frame_matches = {}
            for pool_name, pool in pools.items():
                frame_matches[pool_name] = {}
                for threshold in (.5, .25):
                    links, pairs = matching(targets, pool, threshold)
                    frame_matches[pool_name][str(threshold)] = {"matched_total": len(links), "pairs": pairs}
                    baseline_stage = "area16_all" if pool_name == "all_ccl_area16" else "top4"
                    baseline_pairs = baseline_by_frame[frame_index]["stages"][baseline_stage]["matching"][str(threshold)]["pairs"]
                    baseline_tracks = {row["track_id"] for row in baseline_pairs}
                    mog2_tracks = {targets[index]["track_id"] for index in links}
                    for target in targets:
                        old, new = target["track_id"] in baseline_tracks, target["track_id"] in mog2_tracks
                        target_rows.append({"frame_index": frame_index, "track_id": target["track_id"],
                                            "label": target["label"], "pool": pool_name,
                                            "iou_threshold": threshold, "baseline_matched": old,
                                            "mog2_matched": new, "transition": transition(old, new)})

            primary_links, _ = matching(targets, top4, .5)
            top4_scores = []
            for row in top4:
                x0, y0, x1, y1 = row["analysis_box"]
                roi = fpga_resize_roi(gray[y0:y1 + 1, x0:x1 + 1])
                top4_scores.append({"component_label": row["label"], "analysis_box": row["analysis_box"],
                                    "source_box": row["source_box"], "method": "MOG2 area-top4 analysis-mask bbox; no inherited candidate human label",
                                    "scores": score_record(roi, parameters, hog, quant)})
            for target_index, candidate_index in primary_links.items():
                target, scored = targets[target_index], top4_scores[candidate_index]
                end_to_end["localized"] += 1
                end_to_end[f"localized_{target['label']}"] += 1
                for key in ("hog64_prediction", "hog324_float_prediction", "hog324_q_prediction"):
                    if scored["scores"][key] == target["label"]:
                        end_to_end[f"{key}_correct"] += 1
                        end_to_end[f"{key}_correct_{target['label']}"] += 1

            baseline_primary = {row["track_id"] for row in baseline_by_frame[frame_index]["stages"]["top4"]["matching"]["0.5"]["pairs"]}
            mog2_primary = {targets[index]["track_id"] for index in primary_links}
            failure = bool((baseline_primary - mog2_primary) or ({target["track_id"] for target in targets} - mog2_primary))
            if failure and len(panels) < 6:
                panel_path = panel_dir / f"f{frame_index:06d}_failure.png"
                if not cv2.imwrite(str(panel_path), draw_panel(frame, targets, top4, raw, clean, run_mask)):
                    raise OSError(panel_path)
                panels.append(panel_path)

            frame_rows.append({"frame_index": frame_index, "target_count": len(targets),
                               "foreground_pixels": {"raw": int(raw.sum()), "clean": int(clean.sum()), "run": int(run_mask.sum())},
                               "component_count_before_area": len(all_components),
                               "component_count_area16": len(area16), "top4_count": len(top4),
                               "component_count_capacity_lower_bound_exceeds32": len(all_components) > 32,
                               "matching": frame_matches, "top4_scores": top4_scores})
    finally:
        cap.release()

    if len(frame_rows) != 32 or len(target_rows) != 57 * 2 * 2:
        raise AssertionError("fixed frame or target pairing count changed")
    target_total = 57
    metrics = {pool: {str(threshold): summarize_target_rows(target_rows, pool, threshold)
                      for threshold in (.5, .25)}
               for pool in ("all_ccl_area16", "top4")}
    end_to_end.update({"targets": target_total})
    capacity_frames = [row["frame_index"] for row in frame_rows
                       if row["component_count_capacity_lower_bound_exceeds32"]]
    report = {
        "schema": "local_background_counterfactual_mog2_fixed_v1",
        "scope": {"source": "development scene 2415171 only", "decoded_interval_inclusive": [0, 1050],
                  "scored_frames": FRAME_IDS, "moving_ped_vehicle_targets": target_total,
                  "fixed_experiment_parameter_search": False, "training_performed": False,
                  "rtl_modified": False, "deployment_approved": False},
        "config": CONFIG,
        "foreground_change_only": True,
        "unchanged_downstream": "center-preserving cleanup3; min-run2; area>=16; area-top4; frozen HOG64/HOG324 models",
        "coverage": metrics,
        "end_to_end_top4_iou05": dict(end_to_end),
        "candidate_load": {"frames": len(frame_rows),
                           "component_count_before_area": {"min": min(row["component_count_before_area"] for row in frame_rows),
                                                           "max": max(row["component_count_before_area"] for row in frame_rows),
                                                           "mean": sum(row["component_count_before_area"] for row in frame_rows) / len(frame_rows)},
                           "area16_total": sum(row["component_count_area16"] for row in frame_rows),
                           "top4_total": sum(row["top4_count"] for row in frame_rows)},
        "capacity": {"production_max_label": 32, "frames_component_lower_bound_exceeds32": capacity_frames,
                     "count": len(capacity_frames),
                     "interpretation": "OpenCV CCL has no production label cap; component count is only a lower bound on temporary labels. These geometry results are not deployable RTL performance. Hardware feasibility requires RTL measurement."},
        "far": None, "precision": None,
        "missing_background_truth": "unmatched candidates are not labeled invalid",
        "failure_panels": [path.relative_to(output).as_posix() for path in panels],
        "boundaries": ["Fixed MOG2 algorithm diagnostic only; no approval to deploy MOG2 or any algorithm family.",
                       "One correlated development scene and 32 confirmed frames; no independent-test claim.",
                       "Only foreground generation changed; classifier models, thresholds and training are frozen."]}
    dump(output / "frames.json", frame_rows)
    dump(output / "target_pairs.json", target_rows)
    dump(output / "report.json", report)
    ended = dt.datetime.now(dt.timezone.utc)
    log = {"started_at": started.isoformat(), "ended_at": ended.isoformat(),
           "elapsed_seconds": time.monotonic() - tick, "decoded_interval_inclusive": [0, 1050],
           "decoded_once": True, "processed_frames": 1051, "scored_frames": 32}
    dump(output / "run_log.json", log)
    dependencies = [SCRIPT, PROJECT / "tools/candidate_chain_reference.py",
                    PROJECT / "tools/local_candidate_stage_diagnostic.py",
                    PROJECT / "tools/local_paired_diagnostic.py", PROJECT / "tools/local_fourgrid_diagnostic.py",
                    PROJECT / "tools/roi_dataset_tool.py", PROJECT / "tools/run_local_scene_pilot.py"]
    artifacts = {path.relative_to(output).as_posix(): digest(path)
                 for path in sorted(output.rglob("*")) if path.is_file()}
    receipt = {"schema": "local_background_counterfactual_receipt_v1", "source": {"path": DEFAULT_VIDEO.relative_to(PROJECT).as_posix(), "sha256": EXPECTED_VIDEO_SHA256, "actual_size": [1280, 720]},
               "config": CONFIG, "model_input_hashes": {key: value for key, value in model_receipt.items() if key.endswith("sha256")},
               "frozen_inputs": {"annotation_sha256": digest(ANNOTATIONS), "confirmation_sha256": digest(CONFIRMATION),
                                 "baseline_frame_stages_sha256": baseline_hash, "baseline_receipt_sha256": baseline_receipt_hash,
                                 "diagnostic_summary_v2_sha256": summary_hash, "diagnostic_summary_v2_receipt_sha256": summary_receipt_hash},
               "dependency_hashes": {path.relative_to(PROJECT).as_posix(): digest(path) for path in dependencies},
               "artifact_hashes": artifacts, "run_log": log,
               "assertions": {"source_decoded_once_0_through_1050": True, "fixed_parameters_no_search": True,
                              "moving_confirmed_targets_only": True, "unmatched_not_labeled_invalid": True,
                              "far_and_precision_null": True, "training_performed": False,
                              "rtl_modified": False, "deployment_approved": False}, "receipt_self_hash_included": False}
    dump(output / "receipt.json", receipt)
    return report


def self_check():
    assert transition(False, True) == "gain" and transition(True, False) == "loss"
    assert cleanup_3x3(np.ones((3, 3), np.uint8), 3, True).sum() == 9
    assert filter_short_runs(np.array([[1, 0, 1, 1]], np.uint8), 2).tolist() == [[0, 0, 1, 1]]
    assert len(checked_components(np.array([[1, 0, 1]], np.uint8))) == 2
    return {"self_check": "PASS", "config": CONFIG}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output), ensure_ascii=False, indent=2))
