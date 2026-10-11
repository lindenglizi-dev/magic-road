#!/usr/bin/env python3
"""Attribute baseline/min_run1 crop and score changes on the fixed local targets.

This is a bounded, mechanical diagnostic.  It verifies the frozen receipts, uses
the existing class-blind one-to-one IoU>=0.5 matcher, recomputes every stored
candidate score from the lossless packaged frame, and never promotes visual
inspection to a human label.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from local_paired_diagnostic import PACKAGE, PROJECT, candidates, digest, iou, match, read_json
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi
from run_local_scene_pilot import MODEL_DIR, load_models, make_hog324, quantization_contract, score_roi


BASE = PROJECT / "evaluation/local_scene_pilots"
CONFIRMED = BASE / "intersection_2415171_confirmed_20260930"
STAGE = BASE / "intersection_2415171_stage_diagnostic_v1"
GRID = BASE / "intersection_2415171_fourgrid_v2"
MINRUN = BASE / "intersection_2415171_diagnostic_summary_v2"
DEFAULT_OUTPUT = BASE / "intersection_2415171_crop_change_v2"
IOU_THRESHOLD = 0.5
SCORE_KEYS = (
    "hog64_feature_sha256", "hog64_score", "hog64_prediction",
    "hog324_feature_sha256", "hog324_float_score", "hog324_float_prediction",
    "hog324_q_score_integer", "hog324_q_score_normalized", "hog324_q_prediction",
)
PRIORITY_KEYS = {(360, "p01"), (690, "p02"), (1050, "p02"),
                 (300, "p01"), (450, "p01")}


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verified(directory: Path) -> dict[str, Any]:
    receipt = read_json(directory / "receipt.json")
    hashes = receipt.get("artifact_hashes")
    if not isinstance(hashes, dict):
        raise ValueError(f"missing artifact hashes: {directory}")
    for name, expected in hashes.items():
        path = (directory / name).resolve()
        if not path.is_relative_to(directory.resolve()) or digest(path) != expected:
            raise ValueError(f"artifact mismatch: {path}")
    return receipt


def candidate_geometry(box: list[int]) -> dict[str, Any]:
    width = box[2] - box[0] + 1
    height = box[3] - box[1] + 1
    return {"width": width, "height": height, "aspect_w_over_h": width / height}


def source_from_analysis(box: list[int]) -> list[int]:
    return [box[0] * 5, box[1] * 5, min(1279, box[2] * 5 + 4),
            min(719, box[3] * 5 + 4)]


def stored_baseline_score(row: dict[str, str]) -> dict[str, str]:
    return {key: row[key] for key in SCORE_KEYS}


def shape_relation(a: list[int], b: list[int]) -> str:
    if a == b:
        return "same_box"
    if b[0] <= a[0] and b[1] <= a[1] and b[2] >= a[2] and b[3] >= a[3]:
        return "minrun_box_contains_baseline_box"
    if a[0] <= b[0] and a[1] <= b[1] and a[2] >= b[2] and a[3] >= b[3]:
        return "baseline_box_contains_minrun_box"
    if iou(a, b) > 0:
        return "overlapping_changed_boxes"
    return "disjoint_changed_boxes"


def summarize_candidate(candidate: dict[str, Any] | None, target_box: list[int]) -> dict[str, Any] | None:
    if candidate is None:
        return None
    source_box = candidate["source_box"]
    analysis_box = candidate["analysis_box"]
    return {
        "candidate_id": candidate["candidate_id"],
        "rank": candidate["rank"],
        "component_label": candidate["component_label"],
        "component_area": candidate["component_area"],
        "analysis_box": analysis_box,
        "source_box": source_box,
        "iou_with_gt": iou(target_box, source_box),
        "analysis_geometry": candidate_geometry(analysis_box),
        "source_geometry": candidate_geometry(source_box),
        "component_pixel_set_sha256": candidate.get("component_pixel_set_sha256"),
        "roi_pixel_sha256": candidate["roi_pixel_sha256"],
        "score": candidate["score"],
    }


def best_non_hit(target_box: list[int], pool: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not pool:
        return None
    rank, candidate = max(enumerate(pool), key=lambda item: (iou(target_box, item[1]["source_box"]), -item[0]))
    value = iou(target_box, candidate["source_box"])
    if value >= IOU_THRESHOLD:
        raise AssertionError("non-hit best candidate unexpectedly reaches the match threshold")
    return {
        "candidate_id": candidate["candidate_id"], "rank": rank + 1,
        "source_box": candidate["source_box"], "analysis_box": candidate["analysis_box"],
        "best_iou": value, "is_iou05_match": False,
        "excluded_from_match_metrics": True,
        "note": "Diagnostic nearest candidate only; not substituted for the missing one-to-one match.",
    }


def lost_attribution(target_box: list[int], clean_components: list[dict[str, Any]]) -> dict[str, Any]:
    """Locate an unmatched min_run1 target within clean_all then area16/top4."""
    if not clean_components:
        return {"reason": "clean_all_empty", "clean_all_best": None,
                "area16_iou05_candidates": [], "boundary": "Mechanical stage attribution."}
    clean_rank, clean_best = max(
        enumerate(clean_components, 1), key=lambda item: (iou(target_box, item[1]["source_box"]), -item[0]))
    clean_best_iou = iou(target_box, clean_best["source_box"])
    area16 = [component for component in clean_components if component["area"] >= 16]
    eligible = []
    for rank, component in enumerate(area16, 1):
        value = iou(target_box, component["source_box"])
        if value >= IOU_THRESHOLD:
            eligible.append({"area16_pool_rank": rank, "clean_all_rank": clean_components.index(component) + 1,
                             "component_label": component["label"], "component_area": component["area"],
                             "source_box": component["source_box"], "iou_with_gt": value,
                             "selected_by_area_top4": rank <= 4})
    if clean_best_iou < IOU_THRESHOLD:
        reason = "clean_all_component_geometry_below_iou05_before_area16_top4"
    elif eligible and min(row["area16_pool_rank"] for row in eligible) > 4:
        reason = "area_top4_selection_loss"
    else:
        reason = "one_to_one_or_other_selection_loss"
    return {
        "reason": reason,
        "clean_all_best": {"clean_all_rank": clean_rank, "component_label": clean_best["label"],
                           "component_area": clean_best["area"], "source_box": clean_best["source_box"],
                           "iou_with_gt": clean_best_iou},
        "area16_pool_size": len(area16), "area16_iou05_candidates": eligible,
        "boundary": "Stage/rank facts only; no visual merge/split or class inference.",
    }


def make_candidate_pools(stage_frames: list[dict[str, Any]], minrun_frames: list[dict[str, Any]],
                         package_frames: dict[int, dict[str, Any]], parameters: dict[str, Any],
                         hog: cv2.HOGDescriptor, quant: dict[str, Any]) -> tuple[
                             dict[int, list[dict[str, Any]]], dict[int, list[dict[str, Any]]]]:
    frozen, _ = candidates()
    stage_by_frame = {row["frame_index"]: row for row in stage_frames}
    minrun_by_frame = {row["frame_index"]: row for row in minrun_frames}
    baseline: dict[int, list[dict[str, Any]]] = {}
    minrun: dict[int, list[dict[str, Any]]] = {}
    for frame_index in sorted(package_frames):
        image = cv2.imread(str(PACKAGE / package_frames[frame_index]["path"]), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"cannot read packaged frame {frame_index}")
        gray = fpga_analysis_frame(image)
        stage_components = stage_by_frame[frame_index]["stages"]["top4"]["components"]
        component_by_key = {(int(c["label"]), tuple(c["analysis_box"])): c for c in stage_components}
        baseline[frame_index] = []
        for rank, row in enumerate(frozen[frame_index], 1):
            analysis_box = json.loads(row["selected_analysis_box"])
            source_box = json.loads(row["selected_source_box"])
            x0, y0, x1, y1 = analysis_box
            roi = fpga_resize_roi(gray[y0:y1 + 1, x0:x1 + 1])
            roi_hash = hashlib.sha256(roi.tobytes()).hexdigest()
            score = score_roi(roi, parameters, hog, quant)
            if roi_hash != row["roi_pixel_sha256"] or score != stored_baseline_score(row):
                raise ValueError(f"baseline stored crop/score mismatch: f{frame_index} rank{rank}")
            key = (int(row["component_label"]), tuple(analysis_box))
            if key not in component_by_key:
                raise ValueError(f"baseline component missing from stage receipt: f{frame_index} {key}")
            component = component_by_key[key]
            if component["source_box"] != source_box:
                raise ValueError("baseline source box disagrees with stage receipt")
            baseline[frame_index].append({
                "candidate_id": row["candidate_id"], "rank": rank,
                "component_label": int(row["component_label"]),
                "component_area": int(row["component_area"]),
                "component_pixel_set_sha256": component["pixel_set_sha256"],
                "analysis_box": analysis_box, "source_box": source_box,
                "roi_pixel_sha256": roi_hash, "roi": roi, "score": score,
            })
        saved = minrun_by_frame[frame_index]
        minrun[frame_index] = []
        for rank, row in enumerate(saved["candidates"], 1):
            analysis_box = list(row["analysis_box"])
            source_box = list(row["source_box"])
            x0, y0, x1, y1 = analysis_box
            roi = fpga_resize_roi(gray[y0:y1 + 1, x0:x1 + 1])
            roi_hash = hashlib.sha256(roi.tobytes()).hexdigest()
            score = score_roi(roi, parameters, hog, quant)
            if score != row["score"]:
                raise ValueError(f"min_run1 stored score mismatch: f{frame_index} rank{rank}")
            candidate_id = f"min_run1:f{frame_index:06d}:rank{rank}:cc{int(row['label'])}"
            minrun[frame_index].append({
                "candidate_id": candidate_id, "rank": rank,
                "component_label": int(row["label"]), "component_area": int(row["area"]),
                "component_pixel_set_sha256": row["pixel_set_sha256"],
                "analysis_box": analysis_box, "source_box": source_box,
                "roi_pixel_sha256": roi_hash, "roi": roi, "score": score,
            })
    return baseline, minrun


def render_target(output: Path, index: int, record: dict[str, Any], frame_path: Path,
                  baseline_candidate: dict[str, Any] | None,
                  minrun_candidate: dict[str, Any] | None) -> str:
    frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError(frame_path)
    colors = {"gt": (0, 190, 0), "baseline": (255, 0, 0), "minrun": (0, 140, 255)}
    cv2.rectangle(frame, tuple(record["gt_box"][:2]), tuple(record["gt_box"][2:]), colors["gt"], 3)
    if baseline_candidate is not None:
        cv2.rectangle(frame, tuple(baseline_candidate["source_box"][:2]),
                      tuple(baseline_candidate["source_box"][2:]), colors["baseline"], 3)
    if minrun_candidate is not None:
        cv2.rectangle(frame, tuple(minrun_candidate["source_box"][:2]),
                      tuple(minrun_candidate["source_box"][2:]), colors["minrun"], 3)
    context = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
    canvas = np.full((500, 1000, 3), 248, np.uint8)
    canvas[70:430, 20:660] = context
    title = (f"f{record['frame_index']:06d} {record['track_id']} {record['label']} | "
             f"{record['coverage_outcome']} | {record.get('prediction_transition') or 'n/a'}")
    cv2.putText(canvas, title, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, .65, (20, 20, 20), 2, cv2.LINE_AA)
    cv2.putText(canvas, "GT green | baseline blue | min_run1 orange", (20, 56),
                cv2.FONT_HERSHEY_SIMPLEX, .52, (30, 30, 30), 1, cv2.LINE_AA)
    roi_paths: dict[str, str | None] = {}
    for col, (name, candidate, color) in enumerate((
            ("baseline", baseline_candidate, colors["baseline"]),
            ("minrun", minrun_candidate, colors["minrun"]))):
        x = 690 + col * 150
        cv2.putText(canvas, "baseline" if name == "baseline" else "min_run1", (x, 88),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, color, 2, cv2.LINE_AA)
        if candidate is None:
            cv2.rectangle(canvas, (x, 105), (x + 127, 232), (185, 185, 185), 2)
            cv2.putText(canvas, "missing", (x + 22, 174), cv2.FONT_HERSHEY_SIMPLEX,
                        .55, (80, 80, 80), 2, cv2.LINE_AA)
            roi_paths[name] = None
        else:
            view = cv2.resize(candidate["roi"], (128, 128), interpolation=cv2.INTER_NEAREST)
            canvas[105:233, x:x + 128] = cv2.cvtColor(view, cv2.COLOR_GRAY2BGR)
            roi_name = f"t{index:03d}_f{record['frame_index']:06d}_{record['track_id']}_{name}_roi32.png"
            roi_path = output / "rois" / roi_name
            if not cv2.imwrite(str(roi_path), candidate["roi"]):
                raise OSError(roi_path)
            roi_paths[name] = f"rois/{roi_name}"
            score = candidate["score"]
            cv2.putText(canvas, f"rank {candidate['rank']} {score['hog324_q_prediction']}", (x, 258),
                        cv2.FONT_HERSHEY_SIMPLEX, .42, (35, 35, 35), 1, cv2.LINE_AA)
            cv2.putText(canvas, f"q={score['hog324_q_score_integer']}", (x, 278),
                        cv2.FONT_HERSHEY_SIMPLEX, .38, (35, 35, 35), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Nearest non-hit stays unmatched.", (685, 315),
                cv2.FONT_HERSHEY_SIMPLEX, .38, (50, 50, 50), 1, cv2.LINE_AA)
    cv2.putText(canvas, "It is excluded from metrics.", (685, 338),
                cv2.FONT_HERSHEY_SIMPLEX, .38, (50, 50, 50), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Panels add no human label.", (685, 361),
                cv2.FONT_HERSHEY_SIMPLEX, .38, (50, 50, 50), 1, cv2.LINE_AA)
    name = f"t{index:03d}_f{record['frame_index']:06d}_{record['track_id']}.png"
    path = output / "grids" / name
    if not cv2.imwrite(str(path), canvas):
        raise OSError(path)
    record["grid_path"] = f"grids/{name}"
    record["baseline_roi_path"] = roi_paths["baseline"]
    record["minrun_roi_path"] = roi_paths["minrun"]
    return str(path)


def contact_sheets(output: Path, grid_paths: list[str], per_sheet: int = 4) -> list[str]:
    paths = []
    for page, start in enumerate(range(0, len(grid_paths), per_sheet), 1):
        items = [cv2.imread(path, cv2.IMREAD_COLOR) for path in grid_paths[start:start + per_sheet]]
        if any(item is None for item in items):
            raise ValueError("cannot reload target grid")
        sheet = np.full((len(items) * 500, 1000, 3), 255, np.uint8)
        for row, item in enumerate(items):
            sheet[row * 500:(row + 1) * 500] = item
        name = f"crop_change_contact_{page:02d}.jpg"
        path = output / name
        if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 94]):
            raise OSError(path)
        paths.append(name)
    return paths


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = ["frame_index", "track_id", "label", "coverage_outcome", "prediction_transition",
              "end_to_end_correct_delta", "same_analysis_box", "shape_relation", "lost_reason",
              "baseline_candidate_id", "baseline_rank", "baseline_iou", "baseline_q_prediction",
              "baseline_q_score_integer", "minrun_candidate_id", "minrun_rank", "minrun_iou",
              "minrun_q_prediction", "minrun_q_score_integer", "change_reasons", "grid_path"]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for record in records:
            a, b = record["baseline_match"], record["minrun_match"]
            writer.writerow({
                "frame_index": record["frame_index"], "track_id": record["track_id"],
                "label": record["label"], "coverage_outcome": record["coverage_outcome"],
                "prediction_transition": record.get("prediction_transition"),
                "end_to_end_correct_delta": record["end_to_end_correct_delta"],
                "same_analysis_box": record.get("same_analysis_box"),
                "shape_relation": record.get("shape_relation"),
                "lost_reason": (record.get("lost_attribution") or {}).get("reason"),
                "baseline_candidate_id": a["candidate_id"] if a else None,
                "baseline_rank": a["rank"] if a else None, "baseline_iou": a["iou_with_gt"] if a else None,
                "baseline_q_prediction": a["score"]["hog324_q_prediction"] if a else None,
                "baseline_q_score_integer": a["score"]["hog324_q_score_integer"] if a else None,
                "minrun_candidate_id": b["candidate_id"] if b else None,
                "minrun_rank": b["rank"] if b else None, "minrun_iou": b["iou_with_gt"] if b else None,
                "minrun_q_prediction": b["score"]["hog324_q_prediction"] if b else None,
                "minrun_q_score_integer": b["score"]["hog324_q_score_integer"] if b else None,
                "change_reasons": ";".join(record["change_reasons"]),
                "grid_path": record.get("grid_path"),
            })


def html_report(output: Path, summary: dict[str, Any], changed: list[dict[str, Any]]) -> None:
    rows = []
    for record in changed:
        a, b = record["baseline_match"], record["minrun_match"]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in (
            record["frame_index"], record["track_id"], record["label"], record["coverage_outcome"],
            record.get("prediction_transition"), record["end_to_end_correct_delta"],
            a["rank"] if a else "missing", a["score"]["hog324_q_score_integer"] if a else "missing",
            b["rank"] if b else "missing", b["score"]["hog324_q_score_integer"] if b else "missing",
            ", ".join(record["change_reasons"]))) +
            f'<td><a href="{html.escape(record["grid_path"])}">panel</a></td></tr>')
    page = f"""<!doctype html><meta charset="utf-8"><title>crop change attribution</title>
<style>body{{font-family:Arial,sans-serif;max-width:1500px;margin:24px}}table{{border-collapse:collapse;font-size:13px}}th,td{{border:1px solid #bbb;padding:5px;vertical-align:top}}code{{white-space:pre-wrap}}.note{{background:#fff4cc;padding:12px}}</style>
<h1>Baseline vs min_run1 same-target crop/score attribution</h1>
<p class="note">Mechanical attribution only. Green=confirmed GT, blue=baseline match, orange=min_run1 match. “missing” stays missing; nearest non-hit candidates are never substituted into the IoU≥0.5 denominator. Box-containment names are geometry facts, not a visual claim that objects merged. Scores are margins, not probabilities.</p>
<p>Targets: {summary['targets_total']}; changed: {summary['changed_targets']}. Full machine-readable records: <a href="all_targets.json">all_targets.json</a>, <a href="changed_targets.json">changed_targets.json</a>.</p>
<pre>{html.escape(json.dumps(summary['by_class'], ensure_ascii=False, indent=2))}</pre>
<table><thead><tr><th>frame</th><th>track</th><th>class</th><th>coverage</th><th>both-match prediction transition</th><th>E2E delta</th><th>base rank</th><th>base q margin</th><th>min rank</th><th>min q margin</th><th>change reasons</th><th>image</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"""
    (output / "report.html").write_text(page, encoding="utf-8")


def self_test() -> dict[str, Any]:
    assert candidate_geometry([0, 0, 4, 9]) == {"width": 5, "height": 10, "aspect_w_over_h": .5}
    assert shape_relation([1, 1, 3, 3], [0, 0, 4, 4]) == "minrun_box_contains_baseline_box"
    assert shape_relation([0, 0, 4, 4], [1, 1, 3, 3]) == "baseline_box_contains_minrun_box"
    assert shape_relation([0, 0, 2, 2], [2, 2, 4, 4]) == "overlapping_changed_boxes"
    assert shape_relation([0, 0, 1, 1], [3, 3, 4, 4]) == "disjoint_changed_boxes"
    return {"self_test": "PASS"}


def main(output: Path) -> dict[str, Any]:
    if output.exists() and any(path.name != ".gitkeep" for path in output.rglob("*") if path.is_file()):
        raise ValueError("output already contains diagnostic artifacts; use a new version")
    for directory in (PACKAGE, STAGE, GRID, MINRUN):
        verified(directory)
    confirmation = read_json(CONFIRMED / "confirmation_receipt.json")
    annotations_path = CONFIRMED / "annotations.confirmed.json"
    if digest(annotations_path) != confirmation["derived_sha256"]:
        raise ValueError("confirmed annotation hash mismatch")
    annotations = read_json(annotations_path)
    if annotations.get("human_confirmed") is not True or annotations.get("evaluation_scope") != "moving_ped_vehicle_only":
        raise ValueError("moving-only human confirmation missing")
    stage_frames = read_json(STAGE / "frame_stages.json")
    minrun_frames = read_json(MINRUN / "min_run1_frames.json")
    fourgrid = read_json(GRID / "fourgrid_rows.json")
    package = read_json(PACKAGE / "package.json")
    package_frames = {row["frame_index"]: row for row in package["frames"]}
    if len(stage_frames) != 32 or len(minrun_frames) != 32 or len(fourgrid) != 57:
        raise ValueError("unexpected frozen diagnostic cardinality")
    targets = [dict(frame_index=frame["frame_index"], **target)
               for frame in annotations["frames"] for target in frame["targets"]]
    if len(targets) != 57 or any(t["label"] not in {"ped", "vehicle"} or t["motion"] != "moving" for t in targets):
        raise ValueError("scope is not exactly 57 moving ped/vehicle observations")
    stage_target_keys = [(row["frame_index"], t["track_id"], t["box"])
                         for row in stage_frames for t in row["targets"]]
    annotation_target_keys = [(t["frame_index"], t["track_id"], t["box"]) for t in targets]
    if stage_target_keys != annotation_target_keys:
        raise ValueError("stage targets differ from confirmed annotations")
    parameters, _, model_receipt = load_models(MODEL_DIR)
    hog = make_hog324()
    quant = quantization_contract(parameters["opencv_hog324"])
    baseline_pools, minrun_pools = make_candidate_pools(
        stage_frames, minrun_frames, package_frames, parameters, hog, quant)
    minrun_saved = {row["frame_index"]: row for row in minrun_frames}
    grid_by_key = {(row["frame_index"], row["track_id"]): row for row in fourgrid}
    all_records: list[dict[str, Any]] = []
    for ann_frame in annotations["frames"]:
        frame_index = ann_frame["frame_index"]
        frame_targets = ann_frame["targets"]
        base_pool, new_pool = baseline_pools[frame_index], minrun_pools[frame_index]
        base_links = match(frame_targets, [row["source_box"] for row in base_pool], IOU_THRESHOLD)
        new_links = match(frame_targets, [row["source_box"] for row in new_pool], IOU_THRESHOLD)
        saved_links = {row["track_id"]: row["candidate_index"] for row in minrun_saved[frame_index]["matching"]}
        actual_links = {frame_targets[index]["track_id"]: candidate for index, candidate in new_links.items()}
        if saved_links != actual_links:
            raise ValueError(f"min_run1 stored matching mismatch: f{frame_index}")
        for index, target in enumerate(frame_targets):
            key = (frame_index, target["track_id"])
            base_candidate = base_pool[base_links[index]] if index in base_links else None
            new_candidate = new_pool[new_links[index]] if index in new_links else None
            grid_row = grid_by_key[key]
            if bool(base_candidate) != bool(grid_row["matched"]):
                raise ValueError(f"baseline/fourgrid matching mismatch: {key}")
            if base_candidate and base_candidate["candidate_id"] != grid_row["candidate_id"]:
                raise ValueError(f"baseline candidate identity mismatch: {key}")
            outcome = ("both" if base_candidate is not None and new_candidate is not None else
                       "gained" if base_candidate is None and new_candidate is not None else
                       "lost" if base_candidate is not None and new_candidate is None else "neither")
            base_correct = bool(base_candidate and base_candidate["score"]["hog324_q_prediction"] == target["label"])
            new_correct = bool(new_candidate and new_candidate["score"]["hog324_q_prediction"] == target["label"])
            prediction_transition = None
            if outcome == "both":
                prediction_transition = ("correct" if base_correct else "wrong") + "_to_" + ("correct" if new_correct else "wrong")
            change_reasons = []
            same_box = None
            relation = None
            if outcome in {"gained", "lost"}:
                change_reasons.append("coverage_" + outcome)
            elif outcome == "both":
                same_box = base_candidate["analysis_box"] == new_candidate["analysis_box"]
                relation = shape_relation(base_candidate["analysis_box"], new_candidate["analysis_box"])
                if not same_box:
                    change_reasons.append("matched_box_changed")
                if base_candidate["roi_pixel_sha256"] != new_candidate["roi_pixel_sha256"]:
                    change_reasons.append("roi_pixels_changed")
                if base_candidate["score"] != new_candidate["score"]:
                    change_reasons.append("stored_score_vector_changed")
                if base_candidate["candidate_id"] != new_candidate["candidate_id"] or base_candidate["rank"] != new_candidate["rank"]:
                    change_reasons.append("candidate_id_or_rank_changed")
                if base_candidate["score"]["hog324_q_prediction"] != new_candidate["score"]["hog324_q_prediction"]:
                    change_reasons.append("hog324_q_prediction_changed")
            lost_detail = (lost_attribution(target["box"],
                           next(row for row in stage_frames if row["frame_index"] == frame_index)["stages"]["clean_all"]["components"])
                           if outcome == "lost" else None)
            record = {
                "frame_index": frame_index, "track_id": target["track_id"], "label": target["label"],
                "motion": target["motion"], "visibility": target["visibility"], "gt_box": target["box"],
                "coverage_outcome": outcome, "prediction_transition": prediction_transition,
                "baseline_end_to_end_correct": base_correct, "minrun_end_to_end_correct": new_correct,
                "end_to_end_correct_delta": int(new_correct) - int(base_correct),
                "baseline_match": summarize_candidate(base_candidate, target["box"]),
                "minrun_match": summarize_candidate(new_candidate, target["box"]),
                "same_analysis_box": same_box, "shape_relation": relation,
                "same_component_pixel_set_sha256": (
                    base_candidate["component_pixel_set_sha256"] == new_candidate["component_pixel_set_sha256"]
                    if outcome == "both" else None),
                "non_hit_best_iou": {
                    "baseline": best_non_hit(target["box"], base_pool) if base_candidate is None else None,
                    "minrun1": best_non_hit(target["box"], new_pool) if new_candidate is None else None,
                },
                "lost_attribution": lost_detail,
                "change_reasons": change_reasons,
                "changed": bool(change_reasons),
                "interpretation_boundary": "Mechanical crop/score attribution only; no visual relabeling.",
            }
            all_records.append(record)
    if len(all_records) != 57 or Counter(row["coverage_outcome"] for row in all_records).total() != 57:
        raise AssertionError("target count conservation failed")
    for row in all_records:
        for side in ("baseline_match", "minrun_match"):
            match_row = row[side]
            if match_row is not None and (not match_row["analysis_box"] or match_row["iou_with_gt"] < IOU_THRESHOLD):
                raise AssertionError("matched record has empty or sub-threshold box")
    changed = [row for row in all_records if row["changed"]]
    changed.sort(key=lambda row: (0 if (row["frame_index"], row["track_id"]) in PRIORITY_KEYS else 1,
                                  row["frame_index"], row["track_id"]))
    output.mkdir(parents=True, exist_ok=True)
    (output / "grids").mkdir(exist_ok=True)
    (output / "rois").mkdir(exist_ok=True)
    grid_paths = []
    for index, row in enumerate(changed):
        key = (row["frame_index"], row["track_id"])
        base_pool, new_pool = baseline_pools[row["frame_index"]], minrun_pools[row["frame_index"]]
        base_candidate = next((c for c in base_pool if row["baseline_match"] and c["candidate_id"] == row["baseline_match"]["candidate_id"]), None)
        new_candidate = next((c for c in new_pool if row["minrun_match"] and c["candidate_id"] == row["minrun_match"]["candidate_id"]), None)
        if (row["baseline_match"] is None) != (base_candidate is None) or (row["minrun_match"] is None) != (new_candidate is None):
            raise AssertionError(f"render candidate lookup mismatch: {key}")
        grid_paths.append(render_target(output, index, row,
                          PACKAGE / package_frames[row["frame_index"]]["path"], base_candidate, new_candidate))
    sheets = contact_sheets(output, grid_paths)
    by_class: dict[str, Any] = {}
    by_track: dict[str, Any] = {}
    for field, keys, destination in (("label", ("ped", "vehicle"), by_class),
                                     ("track_id", sorted({r["track_id"] for r in all_records}), by_track)):
        for key in keys:
            subset = [r for r in all_records if r[field] == key]
            destination[key] = {
                "targets": len(subset),
                "coverage_outcome": dict(Counter(r["coverage_outcome"] for r in subset)),
                "both_match_prediction_transition": dict(Counter(
                    r["prediction_transition"] for r in subset if r["prediction_transition"] is not None)),
                "baseline_covered": sum(r["baseline_match"] is not None for r in subset),
                "minrun_covered": sum(r["minrun_match"] is not None for r in subset),
                "baseline_end_to_end_correct": sum(r["baseline_end_to_end_correct"] for r in subset),
                "minrun_end_to_end_correct": sum(r["minrun_end_to_end_correct"] for r in subset),
                "end_to_end_correct_delta": sum(r["end_to_end_correct_delta"] for r in subset),
            }
    if by_class["ped"]["baseline_covered"] != 11 or by_class["vehicle"]["baseline_covered"] != 3:
        raise AssertionError("baseline coverage does not reproduce the frozen 11/3 counts")
    if by_class["ped"]["minrun_covered"] != 15 or by_class["vehicle"]["minrun_covered"] != 5:
        raise AssertionError("min_run1 coverage does not reproduce the frozen 15/5 counts")
    if by_class["ped"]["baseline_end_to_end_correct"] != 7 or by_class["vehicle"]["baseline_end_to_end_correct"] != 2:
        raise AssertionError("baseline correct counts do not reproduce 7/2")
    if by_class["ped"]["minrun_end_to_end_correct"] != 4 or by_class["vehicle"]["minrun_end_to_end_correct"] != 4:
        raise AssertionError("min_run1 correct counts do not reproduce 4/4")
    decisive = {label: [{"frame_index": r["frame_index"], "track_id": r["track_id"],
                         "coverage_outcome": r["coverage_outcome"],
                         "prediction_transition": r["prediction_transition"],
                         "delta": r["end_to_end_correct_delta"]}
                        for r in all_records if r["label"] == label and r["end_to_end_correct_delta"] != 0]
                for label in ("ped", "vehicle")}
    summary = {
        "schema": "local_crop_change_attribution_v1", "targets_total": 57,
        "frames": 32, "tracks": 4, "iou_threshold": IOU_THRESHOLD,
        "changed_targets": len(changed),
        "coverage_outcome_all": dict(Counter(r["coverage_outcome"] for r in all_records)),
        "both_match_prediction_transition_all": dict(Counter(
            r["prediction_transition"] for r in all_records if r["prediction_transition"] is not None)),
        "by_class": by_class, "by_track": by_track,
        "end_to_end_delta_contributors": decisive,
        "matched_to_both_geometry": {
            "same_analysis_box": sum(r["coverage_outcome"] == "both" and r["same_analysis_box"] is True for r in all_records),
            "changed_analysis_box": sum(r["coverage_outcome"] == "both" and r["same_analysis_box"] is False for r in all_records),
            "shape_relation": dict(Counter(r["shape_relation"] for r in all_records if r["coverage_outcome"] == "both")),
            "boundary": "Containment/overlap labels describe bounding-box geometry only; no unreviewed merge/split visual claim.",
        },
        "contact_sheets": sheets,
        "score_validation": "All baseline and min_run1 stored score dictionaries and ROI hashes were recomputed from hash-verified lossless package frames.",
        "matching_boundary": "Class-blind maximum-cardinality one-to-one IoU>=0.5 per method. Non-hit best-IoU rows are separate diagnostics and never enter coverage/correctness denominators.",
        "human_label_boundary": "No visual inference was promoted to a human label.",
        "models": model_receipt,
    }
    dump(output / "all_targets.json", all_records)
    dump(output / "changed_targets.json", changed)
    dump(output / "summary.json", summary)
    write_csv(output / "all_targets.csv", all_records)
    write_csv(output / "changed_targets.csv", changed)
    html_report(output, summary, changed)
    source_files = [
        annotations_path, CONFIRMED / "confirmation_receipt.json",
        STAGE / "frame_stages.json", STAGE / "receipt.json",
        GRID / "fourgrid_rows.json", GRID / "receipt.json",
        MINRUN / "min_run1_frames.json", MINRUN / "receipt.json",
        PACKAGE / "package.json", PACKAGE / "receipt.json",
        PROJECT / "evaluation/local_scene_pilots/intersection_2415171_f120_1079_v1/candidates.csv",
    ]
    artifact_hashes = {p.relative_to(output).as_posix(): digest(p)
                       for p in sorted(output.rglob("*")) if p.is_file()}
    dump(output / "receipt.json", {
        "schema": "local_crop_change_attribution_receipt_v1",
        "source_hashes": {p.relative_to(PROJECT).as_posix(): digest(p) for p in source_files},
        "script_sha256": digest(__file__), "artifact_hashes": artifact_hashes,
        "self_checks": {
            "matched_category_conservation": "PASS", "empty_matched_box": "PASS",
            "57_target_conservation": "PASS", "stored_score_recalculation": "PASS",
            "frozen_count_reproduction": "PASS",
        },
    })
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = self_test() if args.self_test else main(args.output.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
