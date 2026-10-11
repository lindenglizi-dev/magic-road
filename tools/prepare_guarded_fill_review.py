#!/usr/bin/env python3
"""Prepare a deterministic paired human-review batch for guarded fill-only T100."""
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


CONFIGS = ("fill_only_T90", "fill_only_T100", "fill_only_T110")
THRESHOLDS = (90, 100, 110)
BASELINE_COLORS = (
    (230, 90, 30),    # M0: blue
    (40, 185, 40),    # M1: green
    (20, 145, 245),   # M2: orange
    (45, 45, 225),    # M3: red
)
REVIEW_CLASSES = (
    "ped_full", "ped_truncated", "vehicle", "merged_target",
    "background_fragment", "other_ignore")
DEFAULT_SEED = "guarded-fill-only-t100-paired-v1"
SAMPLE_STRIDE = 5
GROUP_GAP = 5
GROUP_IOU = 0.3
GROUP_CENTER_DELTA = 3.0
MAX_CHAIN_SPAN = 30
WINDOW_TARGET = 15
STABLE_TARGET = 10
SENSITIVE_TARGET = 5


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def reject_sealed(path: Path) -> None:
    if any(token in str(path).lower() for token in ("blind", "holdout", "reserve")):
        raise ValueError(f"blind/holdout/reserve path is forbidden: {path}")


def parse_box(value: str | list[int] | tuple[int, int, int, int]
              ) -> tuple[int, int, int, int]:
    parsed = json.loads(value) if isinstance(value, str) else value
    if not isinstance(parsed, (list, tuple)) or len(parsed) != 4:
        raise ValueError(f"invalid box: {value!r}")
    box = tuple(int(item) for item in parsed)
    if box[0] > box[2] or box[1] > box[3]:
        raise ValueError(f"inverted box: {box}")
    return box


def inclusive_iou(left: tuple[int, int, int, int],
                  right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = max(0, left[2] - left[0] + 1) * max(0, left[3] - left[1] + 1)
    right_area = max(0, right[2] - right[0] + 1) * max(0, right[3] - right[1] + 1)
    union = left_area + right_area - intersection
    return intersection / union if union else 0.0


def center(box: tuple[int, int, int, int]) -> tuple[float, float]:
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)


def source_box(box: tuple[int, int, int, int], width: int, height: int
               ) -> tuple[int, int, int, int]:
    return (max(0, SAMPLE_STRIDE * box[0]), max(0, SAMPLE_STRIDE * box[1]),
            min(width - 1, SAMPLE_STRIDE * (box[2] + 1) - 1),
            min(height - 1, SAMPLE_STRIDE * (box[3] + 1) - 1))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require_hash(path: Path, expected: str, label: str) -> str:
    actual = digest(path)
    if actual != expected:
        raise ValueError(f"{label} SHA256 mismatch: expected {expected}, got {actual}")
    return actual


def load_bound_inputs(report_path: Path, catalog_path: Path,
                      guarded_tool_path: Path) -> tuple[
                          dict[str, object], Path, Path, Path,
                          dict[str, dict[str, object]]]:
    for path in (report_path, catalog_path, guarded_tool_path):
        reject_sealed(path)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    root = report_path.parent
    selected_name = "guarded_final4_arbitration_selected_candidates.csv"
    events_name = "guarded_final4_arbitration_decision_events.csv"
    metrics_name = "guarded_final4_arbitration_window_metrics.csv"
    selected_path, events_path, metrics_path = (
        root / selected_name, root / events_name, root / metrics_name)
    for name, path in ((selected_name, selected_path), (events_name, events_path),
                       (metrics_name, metrics_path)):
        require_hash(path, report["output_hashes"][name], name)
    require_hash(catalog_path, report["input_hashes"]["catalog_sha256"], "catalog")
    require_hash(guarded_tool_path, report["script_hashes"]["guarded_tool_sha256"],
                 "guarded arbitration tool")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog_by_clip = {row["clip_id"]: row for row in catalog["clips"]}
    videos: dict[str, dict[str, object]] = {}
    for clip_id, receipt in report["inputs"]["videos"].items():
        if receipt["catalog_split"] not in {"train", "val"}:
            raise ValueError("only train/val development clips are allowed")
        if clip_id not in catalog_by_clip:
            raise ValueError(f"clip missing from catalog: {clip_id}")
        video = Path(receipt["path"])
        reject_sealed(video)
        actual = require_hash(video, receipt["sha256"], f"video {clip_id}")
        if catalog_by_clip[clip_id]["video_sha256"] != actual:
            raise ValueError(f"catalog video hash differs for {clip_id}")
        videos[clip_id] = {"path": video, "sha256": actual,
                           "split": receipt["catalog_split"]}
    return report, selected_path, events_path, metrics_path, videos


def check_ped_gate(metrics_path: Path) -> list[dict[str, object]]:
    rows = [row for row in load_csv(metrics_path)
            if row["config_id"] == "fill_only_T100" and row["label"] == "ped" and
            float(row["iou_threshold"]) == 0.25]
    if len(rows) != 4:
        raise ValueError("expected four fill_only_T100 ped@IoU0.25 window rows")
    result = []
    for row in rows:
        net = int(row["net_vs_baseline"])
        if net < 0:
            raise ValueError(f"ped@0.25 gate failed for {row['window_id']}: {net}")
        result.append({"window_id": row["window_id"], "net_vs_baseline": net,
                       "gate": "pass"})
    return result


def canonical_candidates(selected_rows: list[dict[str, str]],
                         event_rows: list[dict[str, str]]) -> tuple[
                             list[dict[str, object]],
                             dict[tuple[str, int], list[dict[str, str]]],
                             dict[tuple[str, int], list[dict[str, str]]]]:
    selected_configs = {row["config_id"] for row in selected_rows}
    if not set(CONFIGS).issubset(selected_configs) or "baseline_main4" not in selected_configs:
        raise ValueError("selected-candidate table lacks required baseline/fill configurations")
    baseline_by_frame: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    final_t100_by_frame: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    selected_small: dict[tuple[str, int, int], dict[int, dict[str, str]]] = defaultdict(dict)
    for row in selected_rows:
        key = (row["window_id"], int(row["frame_index"]))
        if row["config_id"] == "baseline_main4":
            baseline_by_frame[key].append(row)
        if row["config_id"] == "fill_only_T100":
            final_t100_by_frame[key].append(row)
        if row["config_id"] in CONFIGS and row["branch"] == "small_component_experimental":
            threshold = int(row["config_id"].rsplit("T", 1)[1])
            component_key = (row["window_id"], int(row["frame_index"]),
                             int(row["component_label"]))
            if threshold in selected_small[component_key]:
                raise ValueError(f"duplicate selected small candidate: {component_key}")
            selected_small[component_key][threshold] = row
    events: dict[tuple[str, int, int], dict[int, dict[str, str]]] = defaultdict(dict)
    for row in event_rows:
        if row["config_id"] not in CONFIGS:
            continue
        threshold = int(row["config_id"].rsplit("T", 1)[1])
        key = (row["window_id"], int(row["frame_index"]), int(row["component_label"]))
        if threshold in events[key]:
            raise ValueError(f"duplicate decision event: {key}, T{threshold}")
        events[key][threshold] = row
    candidates = []
    for key, threshold_rows in sorted(selected_small.items()):
        if 100 not in threshold_rows:
            continue
        if key not in events or set(events[key]) != set(THRESHOLDS):
            raise ValueError(f"missing threshold decision events for {key}")
        decisions = events[key]
        for threshold in THRESHOLDS:
            selected = threshold_rows.get(threshold)
            event = decisions[threshold]
            accepted = event["reason_code"] == "FILL_EMPTY_SLOT"
            if accepted != (selected is not None):
                raise ValueError(f"event/selected acceptance mismatch for {key}, T{threshold}")
            if accepted and parse_box(event["selected_analysis_box"]) != parse_box(
                    selected["selected_analysis_box"]):
                raise ValueError(f"event/selected box mismatch for {key}, T{threshold}")
        t100 = threshold_rows[100]
        raw_box = parse_box(t100["raw_analysis_box"])
        statuses = {}
        accepted_boxes = []
        for threshold in THRESHOLDS:
            event = decisions[threshold]
            accepted = event["reason_code"] == "FILL_EMPTY_SLOT"
            box = parse_box(event["selected_analysis_box"]) if accepted else None
            statuses[threshold] = {"accepted": accepted,
                                   "reason_code": event["reason_code"],
                                   "selected_analysis_box": box}
            if box is not None:
                accepted_boxes.append(box)
        stable = all(statuses[t]["accepted"] for t in THRESHOLDS) and len(
            set(accepted_boxes)) == 1
        candidates.append({
            "candidate_key": f"{key[0]}:f{key[1]:06d}:cc{key[2]}",
            "window_id": key[0], "frame_index": key[1],
            "component_label": key[2], "component_area": int(t100["component_area"]),
            "component_peak_difference": int(t100["component_peak_difference"]),
            "raw_analysis_box": raw_box,
            "t100_selected_analysis_box": parse_box(t100["selected_analysis_box"]),
            "center_x": center(raw_box)[0], "center_y": center(raw_box)[1],
            "threshold_status": statuses,
            "sampling_type": "stable" if stable else "threshold_sensitive",
        })
    for rows in baseline_by_frame.values():
        rows.sort(key=lambda row: int(row["output_slot"]))
    for rows in final_t100_by_frame.values():
        rows.sort(key=lambda row: int(row["output_slot"]))
    if not candidates:
        raise ValueError("no T100 accepted small candidates")
    return candidates, baseline_by_frame, final_t100_by_frame


def temporal_groups(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    """Deterministic one-pass association; semantic labels never enter the grouping."""
    groups: list[dict[str, object]] = []
    by_partition: dict[tuple[str, str], list[int]] = defaultdict(list)
    ordered = sorted(candidates, key=lambda row: (
        row["window_id"], row["sampling_type"], row["frame_index"],
        row["component_label"], row["candidate_key"]))
    for row in ordered:
        partition = (row["window_id"], row["sampling_type"])
        frame = int(row["frame_index"])
        raw_box = row["raw_analysis_box"]
        row_center = center(raw_box)
        eligible = []
        for group_index in by_partition[partition]:
            group = groups[group_index]
            gap = frame - int(group["last_frame"])
            if not 1 <= gap <= GROUP_GAP:
                continue
            if frame - int(group["first_frame"]) > MAX_CHAIN_SPAN:
                continue
            last_box = group["last_box"]
            last_center = center(last_box)
            overlap = inclusive_iou(raw_box, last_box)
            dx, dy = abs(row_center[0] - last_center[0]), abs(row_center[1] - last_center[1])
            if overlap < GROUP_IOU or dx > GROUP_CENTER_DELTA or dy > GROUP_CENTER_DELTA:
                continue
            distance = dx * dx + dy * dy
            eligible.append((-overlap, distance, int(group["last_component_label"]),
                             str(group["provisional_id"]), group_index))
        if eligible:
            chosen = min(eligible)[-1]
        else:
            chosen = len(groups)
            provisional = f"p{chosen:05d}"
            groups.append({"provisional_id": provisional, "window_id": row["window_id"],
                           "sampling_type": row["sampling_type"], "members": [],
                           "first_frame": frame})
            by_partition[partition].append(chosen)
        group = groups[chosen]
        group["members"].append(row)
        group["last_frame"] = frame
        group["last_box"] = raw_box
        group["last_component_label"] = row["component_label"]
    for index, group in enumerate(sorted(groups, key=lambda item: (
            item["window_id"], item["sampling_type"], item["first_frame"],
            item["provisional_id"]))):
        group["group_id"] = f"gf{index:04d}"
    return groups


def deterministic_order(groups: list[dict[str, object]], seed: str,
                        window_id: str, sampling_type: str) -> list[dict[str, object]]:
    return sorted(groups, key=lambda group: hashlib.sha256(
        f"{seed}|{window_id}|{sampling_type}|{group['group_id']}|"
        f"{group['members'][0]['candidate_key']}".encode("utf-8")).hexdigest())


def sample_groups(groups: list[dict[str, object]], seed: str
                  ) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    selected: list[dict[str, object]] = []
    receipts_by_window: dict[str, dict[str, object]] = {}
    windows = sorted({group["window_id"] for group in groups})
    if len(windows) != 4:
        raise ValueError(f"expected four development windows, found {len(windows)}")
    for window_id in windows:
        stable = deterministic_order(
            [g for g in groups if g["window_id"] == window_id and
             g["sampling_type"] == "stable"], seed, window_id, "stable")
        sensitive = deterministic_order(
            [g for g in groups if g["window_id"] == window_id and
             g["sampling_type"] == "threshold_sensitive"], seed, window_id,
            "threshold_sensitive")
        stable_take = min(STABLE_TARGET, len(stable))
        sensitive_take = min(SENSITIVE_TARGET, len(sensitive))
        stable_shortfall = STABLE_TARGET - stable_take
        sensitive_shortfall = SENSITIVE_TARGET - sensitive_take
        # Pre-registered transfer: first move an unavailable stratum quota to the
        # other stratum in the same window. Never choose using image content.
        sensitive_extra = min(stable_shortfall, len(sensitive) - sensitive_take)
        stable_extra = min(sensitive_shortfall, len(stable) - stable_take)
        stable_take += stable_extra
        sensitive_take += sensitive_extra
        remaining = WINDOW_TARGET - stable_take - sensitive_take
        if remaining:
            stable_more = min(remaining, len(stable) - stable_take)
            stable_take += stable_more
            remaining -= stable_more
        if remaining:
            sensitive_more = min(remaining, len(sensitive) - sensitive_take)
            sensitive_take += sensitive_more
            remaining -= sensitive_more
        chosen = stable[:stable_take] + sensitive[:sensitive_take]
        for group in chosen:
            group["quota_assignment_window"] = window_id
            group["sampling_seed"] = seed
        selected.extend(chosen)
        receipts_by_window[window_id] = {
            "window_id": window_id, "candidate_groups": len(stable) + len(sensitive),
            "stable_groups": len(stable), "sensitive_groups": len(sensitive),
            "requested_stable": STABLE_TARGET, "requested_sensitive": SENSITIVE_TARGET,
            "selected_stable": stable_take, "selected_sensitive": sensitive_take,
            "stable_quota_transferred_to_sensitive": sensitive_extra,
            "sensitive_quota_transferred_to_stable": stable_extra,
            "initial_unfilled_after_within_window_transfer": remaining,
            "cross_window_groups_received": 0,
            "cross_window_groups_donated": 0,
        }

    # Second pre-registered transfer: unused groups from any donor window are
    # assigned to deficient windows in lexical order. Selection remains a fixed
    # seed hash and never inspects pixels or labels. If all unique groups are
    # exhausted, retain and report the global shortfall instead of duplicating.
    selected_ids = {group["group_id"] for group in selected}
    surplus = [group for group in groups if group["group_id"] not in selected_ids]
    surplus.sort(key=lambda group: hashlib.sha256(
        f"{seed}|cross-window|{group['window_id']}|{group['group_id']}".encode(
            "utf-8")).hexdigest())
    for receiving_window in windows:
        receipt = receipts_by_window[receiving_window]
        deficit = int(receipt["initial_unfilled_after_within_window_transfer"])
        while deficit and surplus:
            group = surplus.pop(0)
            donor_window = str(group["window_id"])
            group["quota_assignment_window"] = receiving_window
            group["sampling_seed"] = seed
            selected.append(group)
            receipt["cross_window_groups_received"] += 1
            receipts_by_window[donor_window]["cross_window_groups_donated"] += 1
            deficit -= 1
        receipt["final_unfilled_target"] = deficit

    final_by_origin_stratum = Counter(
        (str(group["window_id"]), str(group["sampling_type"])) for group in selected)
    population_by_origin_stratum = Counter(
        (str(group["window_id"]), str(group["sampling_type"])) for group in groups)
    for group in selected:
        key = (str(group["window_id"]), str(group["sampling_type"]))
        group["inclusion_probability"] = (
            final_by_origin_stratum[key] / population_by_origin_stratum[key])
    for window_id, receipt in receipts_by_window.items():
        receipt["final_selected_from_window"] = sum(
            group["window_id"] == window_id for group in selected)
        receipt["final_quota_assignments_for_window"] = (
            int(receipt["selected_stable"]) + int(receipt["selected_sensitive"]) +
            int(receipt["cross_window_groups_received"]))
        receipt["stable_inclusion_probability"] = (
            final_by_origin_stratum[(window_id, "stable")] /
            population_by_origin_stratum[(window_id, "stable")]
            if population_by_origin_stratum[(window_id, "stable")] else None)
        receipt["sensitive_inclusion_probability"] = (
            final_by_origin_stratum[(window_id, "threshold_sensitive")] /
            population_by_origin_stratum[(window_id, "threshold_sensitive")]
            if population_by_origin_stratum[(window_id, "threshold_sensitive")] else None)
    if len(selected) != min(60, len(groups)):
        raise AssertionError("cross-window deterministic sampling count mismatch")
    return (sorted(selected, key=lambda group: (group["window_id"], group["group_id"])),
            [receipts_by_window[window_id] for window_id in windows])


def representative_members(group: dict[str, object]) -> list[tuple[str, dict[str, object]]]:
    members = group["members"]
    indices = (0, len(members) // 2, len(members) - 1)
    return [(label, members[index]) for label, index in zip(("FIRST", "MIDDLE", "LAST"), indices)]


def context_box(box: tuple[int, int, int, int], width: int, height: int,
                minimum_width: int = 420, minimum_height: int = 260,
                scale: float = 6.0) -> tuple[int, int, int, int]:
    box_width, box_height = box[2] - box[0] + 1, box[3] - box[1] + 1
    wanted_width = min(width, max(minimum_width, int(round(box_width * scale))))
    wanted_height = min(height, max(minimum_height, int(round(box_height * scale))))
    cx, cy = center(box)
    left = max(0, min(int(round(cx - wanted_width / 2)), width - wanted_width))
    top = max(0, min(int(round(cy - wanted_height / 2)), height - wanted_height))
    return left, top, left + wanted_width - 1, top + wanted_height - 1


def draw_box(image: np.ndarray, box: tuple[int, int, int, int], crop: tuple[int, int, int, int],
             color: tuple[int, int, int], text: str, thickness: int = 2) -> None:
    local = (box[0] - crop[0], box[1] - crop[1], box[2] - crop[0], box[3] - crop[1])
    cv2.rectangle(image, local[:2], local[2:], color, thickness)
    if text:
        font, scale, font_thickness = cv2.FONT_HERSHEY_SIMPLEX, .52, 1
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, scale, font_thickness)
        label_x = max(0, min(local[0], image.shape[1] - text_width - 8))
        label_bottom = local[1] - 4
        if label_bottom - text_height - baseline - 6 < 0:
            label_bottom = min(image.shape[0] - 2, local[1] + text_height + baseline + 8)
        top = max(0, label_bottom - text_height - baseline - 6)
        right = min(image.shape[1] - 1, label_x + text_width + 8)
        cv2.rectangle(image, (label_x, top), (right, label_bottom), color, -1)
        cv2.putText(image, text, (label_x + 4, label_bottom - baseline - 3), font,
                    scale, (255, 255, 255), font_thickness, cv2.LINE_AA)


def crop_and_resize(frame: np.ndarray, box: tuple[int, int, int, int],
                    size: tuple[int, int]) -> np.ndarray:
    crop = frame[box[1]:box[3] + 1, box[0]:box[2] + 1]
    if crop.size == 0:
        raise ValueError(f"empty crop for {box}")
    return cv2.resize(crop, size, interpolation=cv2.INTER_NEAREST)


def labeled_roi_tile(frame: np.ndarray,
                     box: tuple[int, int, int, int] | None,
                     size: tuple[int, int], label: str,
                     color: tuple[int, int, int], subtitle: str = "") -> np.ndarray:
    """Render one exact ROI as a self-contained, readable review tile."""
    width, height = size
    header_height, footer_height = 34, 34
    tile = np.full((height, width, 3), 242, np.uint8)
    cv2.rectangle(tile, (0, 0), (width - 1, height - 1), color, 3)
    cv2.rectangle(tile, (0, 0), (width - 1, header_height), color, -1)
    cv2.putText(tile, label, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, .68,
                (255, 255, 255), 2, cv2.LINE_AA)
    roi_height = height - header_height - footer_height
    if box is None:
        cv2.putText(tile, "REJECT / EMPTY", (12, header_height + roi_height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, .58, (40, 40, 180), 2, cv2.LINE_AA)
    else:
        roi = crop_and_resize(frame, box, (width - 8, roi_height - 4))
        tile[header_height + 2:header_height + roi_height - 2, 4:width - 4] = roi
    if subtitle:
        cv2.putText(tile, subtitle[:42], (7, height - 11), cv2.FONT_HERSHEY_SIMPLEX,
                    .39, (25, 25, 25), 1, cv2.LINE_AA)
    return tile


def draw_color_legend(canvas: np.ndarray, origin: tuple[int, int],
                      entries: list[tuple[str, tuple[int, int, int]]]) -> None:
    """Draw fixed badges so overlapping boxes never hide their identities."""
    x, y = origin
    for label, color in entries:
        cv2.rectangle(canvas, (x, y), (x + 54, y + 27), color, -1)
        cv2.putText(canvas, label, (x + 8, y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                    .52, (255, 255, 255), 2, cv2.LINE_AA)
        x += 66


def render_member(frame: np.ndarray, label: str, member: dict[str, object],
                  baseline: list[dict[str, str]], final_t100: list[dict[str, str]]) -> np.ndarray:
    height, width = frame.shape[:2]
    raw_source = source_box(member["raw_analysis_box"], width, height)
    expanded_source = source_box(member["t100_selected_analysis_box"], width, height)
    crop = context_box(expanded_source, width, height)
    raw_context = frame[crop[1]:crop[3] + 1, crop[0]:crop[2] + 1].copy()
    baseline_view, final_view = raw_context.copy(), raw_context.copy()
    for index, row in enumerate(baseline):
        draw_box(baseline_view, parse_box(row["selected_source_box"]), crop,
                 BASELINE_COLORS[index % len(BASELINE_COLORS)], "", 3)
    for row in final_t100:
        box = parse_box(row["selected_source_box"])
        if (row["branch"] == "small_component_experimental" and
                int(row["component_label"]) == member["component_label"]):
            draw_box(final_view, box, crop, (220, 0, 220), "T100 SMALL", 3)
        else:
            rank = row.get("baseline_main_rank", "")
            rank_index = int(rank) if str(rank).isdigit() else 0
            draw_box(final_view, box, crop,
                     BASELINE_COLORS[rank_index % len(BASELINE_COLORS)], "", 3)
    draw_box(final_view, raw_source, crop, (0, 220, 255), "RAW", 2)
    baseline_view = cv2.resize(baseline_view, (590, 350), interpolation=cv2.INTER_AREA)
    final_view = cv2.resize(final_view, (590, 350), interpolation=cv2.INTER_AREA)
    canvas = np.full((800, 1900, 3), 245, np.uint8)
    canvas[55:405, 10:600] = baseline_view
    canvas[55:405, 615:1205] = final_view
    cv2.putText(canvas, f"{label} frame={member['frame_index']} group candidate={member['candidate_key']}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .65, (20, 20, 20), 2, cv2.LINE_AA)
    cv2.putText(canvas, "BASELINE OVERVIEW (match colors to M0-M3 crops below)",
                (12, 431), cv2.FONT_HERSHEY_SIMPLEX, .53, (30, 30, 30), 1, cv2.LINE_AA)
    draw_color_legend(canvas, (12, 443), [
        (f"M{index}", BASELINE_COLORS[index]) for index in range(4)])
    cv2.putText(canvas, "T100 OVERVIEW (candidate=magenta, raw component=yellow)",
                (617, 431), cv2.FONT_HERSHEY_SIMPLEX, .53, (80, 20, 80), 1, cv2.LINE_AA)

    # Exact classifier-input crops for all perspective thresholds.  A reviewer no
    # longer needs to infer geometry from coordinates alone.
    threshold_x = (1220, 1445, 1670)
    threshold_colors = ((180, 100, 20), (190, 20, 190), (20, 110, 210))
    for x, threshold, color in zip(threshold_x, THRESHOLDS, threshold_colors):
        status = member["threshold_status"][threshold]
        state = "ACCEPT" if status["accepted"] else "REJECT"
        analysis_box = status["selected_analysis_box"]
        threshold_source = (source_box(analysis_box, width, height)
                            if analysis_box is not None else None)
        box_text = str(list(analysis_box)) if analysis_box is not None else "-"
        tile = labeled_roi_tile(frame, threshold_source, (215, 220),
                                f"T{threshold} {state}", color, box_text)
        canvas[55:275, x:x + 215] = tile

    raw_tile = labeled_roi_tile(frame, raw_source, (215, 185), "RAW COMPONENT",
                                (0, 170, 210), str(list(member["raw_analysis_box"])))
    canvas[295:480, 1220:1435] = raw_tile
    cv2.putText(canvas, "Compare these three ROI crops directly.", (1450, 320),
                cv2.FONT_HERSHEY_SIMPLEX, .55, (30, 30, 30), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Do not infer T90/T110 from coordinates only.", (1450, 350),
                cv2.FONT_HERSHEY_SIMPLEX, .50, (30, 30, 30), 1, cv2.LINE_AA)

    # One exact crop per baseline slot removes ambiguity when boxes overlap.
    cv2.putText(canvas, "BASELINE EXACT ROI CROPS (the content sent by each M slot)",
                (10, 505), cv2.FONT_HERSHEY_SIMPLEX, .58, (25, 25, 25), 1, cv2.LINE_AA)
    baseline_x = (10, 300, 590, 880)
    for index, x in enumerate(baseline_x):
        if index < len(baseline):
            baseline_source = parse_box(baseline[index]["selected_source_box"])
            subtitle = str(list(baseline_source))
        else:
            baseline_source, subtitle = None, "empty slot"
        tile = labeled_roi_tile(frame, baseline_source, (280, 220), f"M{index}",
                                BASELINE_COLORS[index], subtitle)
        canvas[525:745, x:x + 280] = tile

    cv2.putText(canvas,
                f"raw={list(member['raw_analysis_box'])} center=({member['center_x']:.1f},"
                f"{member['center_y']:.1f}) area={member['component_area']} "
                f"peak={member['component_peak_difference']} source={width}x{height} context={list(crop)}",
                (10, 782), cv2.FONT_HERSHEY_SIMPLEX, .46, (20, 20, 20), 1, cv2.LINE_AA)
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1] - 1, canvas.shape[0] - 1),
                  (40, 40, 40), 2)
    return canvas


def render_groups(output: Path, groups: list[dict[str, object]],
                  videos: dict[str, dict[str, object]],
                  baseline_by_frame: dict[tuple[str, int], list[dict[str, str]]],
                  final_t100_by_frame: dict[tuple[str, int], list[dict[str, str]]],
                  artifact_suffix: str = ""
                  ) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    images_dir = output / "groups"
    images_dir.mkdir(parents=True, exist_ok=True)
    captures = {}
    frame_cache: dict[tuple[str, int], np.ndarray] = {}
    image_receipts = []
    try:
        for clip_id, video in videos.items():
            capture = cv2.VideoCapture(str(video["path"]))
            if not capture.isOpened():
                raise ValueError(f"cannot open video: {video['path']}")
            captures[clip_id] = capture
        for group in groups:
            clip_id = str(group["window_id"]).split(":", 1)[0]
            panels = []
            displayed = []
            for position, member in representative_members(group):
                frame_index = int(member["frame_index"])
                key = (clip_id, frame_index)
                if key not in frame_cache:
                    capture = captures[clip_id]
                    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                    ok, frame = capture.read()
                    if not ok:
                        raise ValueError(f"cannot decode {clip_id} frame {frame_index}")
                    frame_cache[key] = frame
                panel = render_member(
                    frame_cache[key], position, member,
                    baseline_by_frame[(group["window_id"], frame_index)],
                    final_t100_by_frame[(group["window_id"], frame_index)])
                panels.append(panel)
                displayed.append({"position": position, "candidate_key": member["candidate_key"],
                                  "frame_index": frame_index})
            image = np.vstack(panels)
            filename = f"{group['group_id']}_{group['sampling_type']}{artifact_suffix}.jpg"
            path = images_dir / filename
            if not cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, 94]):
                raise OSError(f"cannot write {path}")
            image_receipts.append({"group_id": group["group_id"],
                                   "path": f"groups/{filename}", "sha256": digest(path),
                                   "width": int(image.shape[1]), "height": int(image.shape[0]),
                                   "displayed": displayed})
    finally:
        for capture in captures.values():
            capture.release()
    sheets = render_contact_sheets(output, image_receipts, artifact_suffix=artifact_suffix)
    return image_receipts, sheets


def render_contact_sheets(output: Path, images: list[dict[str, object]],
                          per_sheet: int = 2,
                          artifact_suffix: str = "") -> list[dict[str, object]]:
    result = []
    tile_width, tile_height, columns = 1200, 1560, 1
    for page, offset in enumerate(range(0, len(images), per_sheet), 1):
        subset = images[offset:offset + per_sheet]
        rows = (len(subset) + columns - 1) // columns
        sheet = np.full((rows * tile_height, columns * tile_width, 3), 245, np.uint8)
        for index, item in enumerate(subset):
            source = cv2.imread(str(output / item["path"]))
            if source is None:
                raise ValueError(f"missing review image: {item['path']}")
            preview = cv2.resize(source, (tile_width, tile_height - 45),
                                 interpolation=cv2.INTER_AREA)
            top, left = (index // columns) * tile_height, (index % columns) * tile_width
            sheet[top:top + tile_height - 45, left:left + tile_width] = preview
            cv2.putText(sheet, f"{item['group_id']}  {Path(item['path']).stem}",
                        (left + 8, top + tile_height - 14), cv2.FONT_HERSHEY_SIMPLEX,
                        .55, (20, 20, 20), 1, cv2.LINE_AA)
        path = output / f"contact_sheet_{page:02d}{artifact_suffix}.jpg"
        if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 92]):
            raise OSError(f"cannot write {path}")
        result.append({"path": path.name, "sha256": digest(path),
                       "group_count": len(subset)})
    return result


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> dict[str, object]:
    for path in (args.report, args.catalog, args.output):
        reject_sealed(path)
    script_path = Path(__file__)
    guarded_tool = script_path.with_name("guarded_final4_arbitration.py")
    report, selected_path, events_path, metrics_path, videos = load_bound_inputs(
        args.report, args.catalog, guarded_tool)
    ped_gate = check_ped_gate(metrics_path)
    selected_rows, event_rows = load_csv(selected_path), load_csv(events_path)
    candidates, baseline_by_frame, final_t100_by_frame = canonical_candidates(
        selected_rows, event_rows)
    groups = temporal_groups(candidates)
    selected_groups, sampling_receipts = sample_groups(groups, args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    image_receipts, sheets = render_groups(
        args.output, selected_groups, videos, baseline_by_frame, final_t100_by_frame,
        artifact_suffix=args.artifact_suffix)
    image_by_group = {row["group_id"]: row for row in image_receipts}
    bound_hashes = {
        "guarded_report_sha256": digest(args.report),
        "selected_candidates_sha256": digest(selected_path),
        "decision_events_sha256": digest(events_path),
        "window_metrics_sha256": digest(metrics_path),
        "catalog_sha256": digest(args.catalog),
        "review_tool_sha256": digest(script_path),
    }
    manifest = []
    groups_document = []
    for group in selected_groups:
        members = group["members"]
        representative = members[len(members) // 2]
        key = (group["window_id"], int(representative["frame_index"]))
        status = representative["threshold_status"]
        image = image_by_group[group["group_id"]]
        clip_id = str(group["window_id"]).split(":", 1)[0]
        record = {
            "group_id": group["group_id"], "window_id": group["window_id"],
            "clip_id": clip_id, "scene_split": videos[clip_id]["split"],
            "sampling_type": group["sampling_type"], "group_size": len(members),
            "first_frame": members[0]["frame_index"],
            "middle_frame": representative["frame_index"],
            "last_frame": members[-1]["frame_index"],
            "representative_candidate_key": representative["candidate_key"],
            "component_label": representative["component_label"],
            "component_area": representative["component_area"],
            "component_peak_difference": representative["component_peak_difference"],
            "component_center_x": representative["center_x"],
            "component_center_y": representative["center_y"],
            "raw_analysis_box": list(representative["raw_analysis_box"]),
            "T90_status": "ACCEPT" if status[90]["accepted"] else "REJECT",
            "T90_reason": status[90]["reason_code"],
            "T90_selected_analysis_box": (list(status[90]["selected_analysis_box"])
                                           if status[90]["selected_analysis_box"] else None),
            "T100_status": "ACCEPT" if status[100]["accepted"] else "REJECT",
            "T100_reason": status[100]["reason_code"],
            "T100_selected_analysis_box": (list(status[100]["selected_analysis_box"])
                                            if status[100]["selected_analysis_box"] else None),
            "T110_status": "ACCEPT" if status[110]["accepted"] else "REJECT",
            "T110_reason": status[110]["reason_code"],
            "T110_selected_analysis_box": (list(status[110]["selected_analysis_box"])
                                            if status[110]["selected_analysis_box"] else None),
            "baseline_main_count": len(baseline_by_frame[key]),
            "T100_final_count": len(final_t100_by_frame[key]),
            "strategy_under_review": "fill_only_T100",
            "sensitivity_controls": "fill_only_T90|fill_only_T110",
            "source_video_sha256": videos[clip_id]["sha256"],
            **bound_hashes,
            "review_image_path": image["path"], "review_image_sha256": image["sha256"],
            "sample_seed": args.seed,
            "quota_assignment_window": group["quota_assignment_window"],
            "inclusion_probability": group["inclusion_probability"],
            "review_class": "", "same_frame_new_target": "",
            "duplicate_of_baseline": "", "duplicate_baseline_number": "",
            "crop_usable": "", "occlusion": "", "truncation_reason": "",
            "geometry_preference": "", "reviewer": "", "reviewed_at": "",
            "review_basis": "", "review_note": "",
        }
        manifest.append(record)
        groups_document.append({
            "group_id": group["group_id"], "window_id": group["window_id"],
            "sampling_type": group["sampling_type"],
            "inclusion_probability": group["inclusion_probability"],
            "member_count": len(members),
            "members": [{
                **{key_name: value for key_name, value in member.items()
                   if key_name != "threshold_status"},
                "raw_analysis_box": list(member["raw_analysis_box"]),
                "t100_selected_analysis_box": list(member["t100_selected_analysis_box"]),
                "threshold_status": {
                    str(threshold): {**entry,
                                     "selected_analysis_box": (list(entry["selected_analysis_box"])
                                                               if entry["selected_analysis_box"] else None)}
                    for threshold, entry in member["threshold_status"].items()}
            } for member in members],
        })
    manifest_path = args.output / f"review_manifest{args.artifact_suffix}.csv"
    groups_path = args.output / f"temporal_groups{args.artifact_suffix}.json"
    instructions_path = args.output / f"REVIEW_INSTRUCTIONS{args.artifact_suffix}.md"
    write_csv(manifest_path, manifest)
    groups_path.write_text(json.dumps({
        "association_contract": {
            "gap_source_frames_max": GROUP_GAP, "raw_box_inclusive_iou_min": GROUP_IOU,
            "center_axis_delta_max_analysis_pixels": GROUP_CENTER_DELTA,
            "chain_span_source_frames_max": MAX_CHAIN_SPAN,
            "multiple_match_order": "IoU desc, squared center distance asc, previous label asc, group id asc",
            "partition": "window_id and stable/sensitive stratum",
        },
        "all_group_counts": dict(Counter(group["sampling_type"] for group in groups)),
        "selected_groups": groups_document,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    instructions_path.write_text(
        "# Guarded fill-only T100 paired review (readable layout v2)\n\n"
        "Review each row using its group image. The three stacked sections are the first, "
        "middle and last members of the deterministic temporal group. Each section shows a "
        "color-keyed baseline overview, one separate exact ROI crop for each M0-M3 slot, the "
        "T100 final overview, the selected small box in magenta, its raw component in yellow, "
        "and separate exact T90/T100/T110 ROI crops. Never infer a baseline number from "
        "overlapping text: match the box color to its labeled ROI tile.\n\n"
        "Allowed `review_class`: " + ", ".join(REVIEW_CLASSES) + ". Set "
        "`same_frame_new_target`, `duplicate_of_baseline`, and `crop_usable` to yes/no/uncertain. "
        "When duplicate_of_baseline=yes, fill `duplicate_baseline_number` (M0..M3). Use "
        "`geometry_preference` values T90, T100, T110, equivalent, none, or uncertain. "
        "Record scene occlusion separately from box truncation. Background fragments, merged "
        "targets, other_ignore, unusable crops, and truncation require a note. Set "
        "`review_basis=human_visual_review`, reviewer and reviewed_at. All human fields start "
        "blank. This tool does not import any sample into training.\n",
        encoding="utf-8")
    receipt_path = args.output / f"receipt{args.artifact_suffix}.json"
    receipt = {
        "status": "pending_explicit_human_review_training_imported_false",
        "strategy_under_review": "fill_only_T100",
        "sensitivity_controls": ["fill_only_T90", "fill_only_T110"],
        "review_classes": list(REVIEW_CLASSES),
        "human_fields_initialized_blank": True,
        "ped_iou_0p25_gate": ped_gate,
        "sampling": {
            "seed": args.seed, "target_total_groups": 60,
            "target_per_window": WINDOW_TARGET, "target_stable_per_window": STABLE_TARGET,
            "target_sensitive_per_window": SENSITIVE_TARGET,
            "candidate_count": len(candidates), "group_count": len(groups),
            "selected_group_count": len(selected_groups),
            "global_unique_group_shortfall": max(0, 60 - len(selected_groups)),
            "window_receipts": sampling_receipts,
            "transfer_rule": (
                "Within each window, unavailable stable quota transfers to sensitive, then "
                "unavailable sensitive quota transfers to stable; remaining capacity is filled "
                "stable then sensitive. Remaining per-window deficits receive fixed-seed groups "
                "from other windows with unused unique groups. If the global unique-group pool "
                "is below 60, the shortfall is reported and groups are never duplicated. Visual "
                "content never enters selection."),
        },
        "association_contract": {
            "gap_source_frames_max": GROUP_GAP, "raw_box_iou_min": GROUP_IOU,
            "center_each_axis_delta_max_analysis_pixels": GROUP_CENTER_DELTA,
            "chain_span_source_frames_max": MAX_CHAIN_SPAN,
        },
        "input_receipts": {
            "guarded_report": {"path": str(args.report.resolve()),
                               "sha256": bound_hashes["guarded_report_sha256"]},
            "selected_candidates": {"path": str(selected_path.resolve()),
                                    "sha256": bound_hashes["selected_candidates_sha256"]},
            "decision_events": {"path": str(events_path.resolve()),
                                "sha256": bound_hashes["decision_events_sha256"]},
            "window_metrics": {"path": str(metrics_path.resolve()),
                               "sha256": bound_hashes["window_metrics_sha256"]},
            "catalog": {"path": str(args.catalog.resolve()),
                        "sha256": bound_hashes["catalog_sha256"]},
            "guarded_tool": {"path": str(guarded_tool.resolve()), "sha256": digest(guarded_tool)},
            "review_tool": {"path": str(script_path.resolve()),
                            "sha256": bound_hashes["review_tool_sha256"]},
            "videos": {clip: {"path": str(data["path"].resolve()), "sha256": data["sha256"],
                              "split": data["split"]} for clip, data in videos.items()},
        },
        "outputs": {
            "review_manifest": {"path": manifest_path.name, "sha256": digest(manifest_path)},
            "temporal_groups": {"path": groups_path.name, "sha256": digest(groups_path)},
            "instructions": {"path": instructions_path.name, "sha256": digest(instructions_path)},
            "group_images": image_receipts, "contact_sheets": sheets,
        },
        "boundary": (
            "Development train/validation frames only. Sampling uses candidate geometry and a "
            "fixed seed, never visual judgment or annotations. Empty human fields are not "
            "labels. No image is imported into training. Geometry review is not detection or "
            "classification accuracy evidence."),
    }
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    return receipt


def self_test() -> None:
    base = {
        "window_id": "clip:0-99", "sampling_type": "stable", "component_area": 6,
        "component_peak_difference": 80, "t100_selected_analysis_box": (1, 1, 4, 4),
        "threshold_status": {t: {"accepted": True, "reason_code": "FILL_EMPTY_SLOT",
                                 "selected_analysis_box": (1, 1, 4, 4)} for t in THRESHOLDS},
        "center_x": 2.5, "center_y": 2.5,
    }
    rows = []
    for index, (frame, box) in enumerate(((0, (1, 1, 4, 4)), (5, (2, 1, 5, 4)),
                                          (31, (2, 1, 5, 4)), (37, (2, 1, 5, 4)))):
        rows.append({**base, "candidate_key": f"c{index}", "frame_index": frame,
                     "component_label": index + 1, "raw_analysis_box": box})
    grouped = temporal_groups(rows)
    sizes = sorted(len(group["members"]) for group in grouped)
    assert sizes == [1, 1, 2], sizes
    assert all(group["last_frame"] - group["first_frame"] <= MAX_CHAIN_SPAN for group in grouped)
    edge_frame = np.zeros((80, 100, 3), np.uint8)
    edge_frame[:, :, 1] = 80
    edge = {**rows[0], "frame_index": 0, "component_label": 9,
            "candidate_key": "edge", "raw_analysis_box": (0, 0, 1, 1),
            "t100_selected_analysis_box": (0, 0, 5, 15)}
    selected_box = source_box(edge["t100_selected_analysis_box"], 100, 80)
    assert selected_box == (0, 0, 29, 79)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "source.bin"
        source.write_bytes(b"bound-input")
        expected = digest(source)
        require_hash(source, expected, "fixture")
        source.write_bytes(b"tampered")
        try:
            require_hash(source, expected, "fixture")
        except ValueError:
            pass
        else:
            raise AssertionError("hash mismatch was not rejected")
        panel = render_member(edge_frame, "FIRST", edge, [], [])
        assert panel.shape == (800, 1900, 3)
        image_path = root / "edge.jpg"
        assert cv2.imwrite(str(image_path), panel)
        assert digest(image_path)
    try:
        reject_sealed(Path("blind_holdout"))
    except ValueError:
        pass
    else:
        raise AssertionError("sealed input guard did not trigger")
    print("PASS: grouping gaps/chain split, boundary rendering, input hash and sealed-path guard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path,
                        default=Path("evaluation/python_references/guarded_final4_arbitration_report.json"))
    parser.add_argument("--catalog", type=Path,
                        default=Path("evaluation/public_data/virat_ground_v2/catalog.json"))
    parser.add_argument("--output", type=Path,
                        default=Path("evaluation/candidate_reviews/guarded_fill_only_T100_paired_review"))
    parser.add_argument("--seed", default=DEFAULT_SEED)
    parser.add_argument(
        "--artifact-suffix", default="",
        help="append a safe suffix such as _v2 to every generated artifact")
    parser.add_argument("--self-test", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.self_test:
        self_test()
        return
    receipt = run(args)
    print(json.dumps({"status": receipt["status"],
                      "selected_groups": receipt["sampling"]["selected_group_count"],
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
