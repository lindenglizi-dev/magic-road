#!/usr/bin/env python3
"""Build a bounded human review package for VIRAT background subtypes.

Invalid candidates are deduplicated by the existing temporal_track_id and then
deterministically stratified by signed difference polarity and causal geometry
persistence.  Protection controls are the preregistered small ped/rider rows
that the 2-of-3 diagnostic would remove.  The video is decoded once from frame
zero with the sealed causal background/candidate reference.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import cv2
import numpy as np


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from analyze_virat_failure_sources import (  # noqa: E402
    GeometryTracker,
    box_area,
    box_json,
    guard_path,
    parse_box,
    sha256,
    sha512,
)
from candidate_chain_reference import CandidateChainReference  # noqa: E402
from fixed_budget_candidate_prototype import Component, extract_components, source_box  # noqa: E402
from guarded_final4_arbitration import Config, guarded_select  # noqa: E402


DEFAULT_REVIEW = (
    PROJECT / "evaluation/scene_extensions/virat_010107_02_t100_review_v1"
    / "canonical_review_manifest.csv"
)
DEFAULT_FEATURES = (
    PROJECT / "evaluation/scene_extensions/virat_010107_failure_sources_v1"
    / "failure_source_features.csv"
)
DEFAULT_CANDIDATES = (
    PROJECT / "evaluation/scene_extensions/virat_010107_02_t100/candidates.csv"
)
DEFAULT_VIDEO = (
    PROJECT / "public_data/raw/virat_ground_v2/video_original"
    / "VIRAT_S_010107_02_000282_000312.mp4"
)
DEFAULT_OUTPUT = (
    PROJECT / "evaluation/scene_extensions/virat_010107_background_subtype_review_v1"
)

EXPECTED_ROWS = 83
EXPECTED_CANDIDATES_SHA256 = "0b4f75eecb5aa92d07dee18fb4aa0b76069356b7e57ad8d7d6e93fddcaae39fd"
EXPECTED_VIDEO_SHA256 = "30e20c3bd2aac7d7585eba0e49b0322424d48d06ba8d399bcf5382d2ac0d0d6d"
EXPECTED_VIDEO_SHA512 = (
    "a65ff0da41b340ba85033e8e9423b239377151b7a133203f4328e0f697566441"
    "07b731ee5ec78377b3804ff4cd12677f4720d8d8ea421aecc7ff63955de07ecd"
)
EXPECTED_DEPENDENCIES = {
    "tools/candidate_chain_reference.py": "6ed7652dd51db9eb1a1debede3cfb74f8ca862f261e96fa4557fb30969ab766d",
    "tools/fixed_budget_candidate_prototype.py": "ec45a958cf05942dbae4655b0a6d7a4bd1acb7bc70acea0d182a1a7887a39486",
    "tools/guarded_final4_arbitration.py": "f53b4d3efbcdc65366f0a79813c5e885bd2b09800ab61cf17aed736d5d2194b7",
}

STRATEGY = "fill_only_T100"
LEARN_FRAMES = 4
WARMUP_FRAMES = 120
FOREGROUND_THRESHOLD = 20
MAIN_MIN_AREA = 16
PERSPECTIVE_THRESHOLD = 100
PEAK_FLOOR = 40
SAMPLE_STRIDE = 5
BRANCH_CAP = 12
CONTACT_SHEET_SIZE = 4
SUBTYPE_VALUES = (
    "shadow", "parking_line_related", "background_change", "other", "uncertain",
)
STRATA = (
    "negative_transient", "negative_persistent",
    "nonnegative_transient", "nonnegative_persistent",
)
FORBIDDEN = re.compile(r"(^|[/\\_.-])(blind|holdout|reserve|test)($|[/\\_.-])", re.I)


def file_hash(path: Path) -> str:
    return sha256(path)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    if not headers:
        raise ValueError(f"CSV has no header: {path}")
    return headers, rows


def write_csv(path: Path, headers: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(headers), extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def index_unique(rows: Sequence[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if not key or key in result:
            raise ValueError(f"blank or duplicate {field}: {key!r}")
        result[key] = row
    return result


def validate_inputs(review: Path, features: Path, candidates: Path,
                    video: Path, output: Path) -> dict[str, str]:
    for path in (review, features, candidates, video, output):
        if FORBIDDEN.search(str(path.resolve()).replace("\\", "/")):
            raise ValueError(f"sealed path rejected: {path}")
        guard_path(path.resolve())
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")
    review_receipt = review.parent / "receipt.json"
    feature_receipt = features.parent / "receipt.json"
    for path in (review_receipt, feature_receipt):
        if not path.is_file():
            raise ValueError(f"missing input receipt: {path}")
    review_meta = json.loads(review_receipt.read_text(encoding="utf-8"))
    feature_meta = json.loads(feature_receipt.read_text(encoding="utf-8"))
    if file_hash(review) != review_meta["artifact_hashes"].get(review.name):
        raise ValueError("canonical review manifest hash mismatch")
    if file_hash(features) != feature_meta["artifact_hashes"].get(features.name):
        raise ValueError("failure feature hash mismatch")
    failure_tool = TOOLS / "analyze_virat_failure_sources.py"
    if file_hash(failure_tool) != feature_meta["script_sha256"]:
        raise ValueError("failure feature producer script hash mismatch")
    if file_hash(candidates) != EXPECTED_CANDIDATES_SHA256:
        raise ValueError("sealed candidates.csv hash mismatch")
    if file_hash(video) != EXPECTED_VIDEO_SHA256 or sha512(video) != EXPECTED_VIDEO_SHA512:
        raise ValueError("official video hash mismatch")
    for relative, expected in EXPECTED_DEPENDENCIES.items():
        if file_hash(PROJECT / relative) != expected:
            raise ValueError(f"sealed candidate dependency changed: {relative}")
    return {
        "review_receipt": file_hash(review_receipt),
        "feature_receipt": file_hash(feature_receipt),
        "failure_tool": file_hash(failure_tool),
    }


def build_geometry_tracks(candidate_rows: Sequence[dict[str, str]]) -> dict[str, dict[str, Any]]:
    by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in candidate_rows:
        if row["strategy"] == STRATEGY:
            by_frame[int(row["frame_index"])].append(row)
    trackers = {
        "main_area_topk": GeometryTracker(),
        "small_component_experimental": GeometryTracker(),
    }
    output: dict[str, dict[str, Any]] = {}
    for frame_index in sorted(by_frame):
        frame_rows = sorted(by_frame[frame_index], key=lambda row: int(row["slot"]))
        for branch, tracker in trackers.items():
            branch_rows = [row for row in frame_rows if row["branch"] == branch]
            tracks = tracker.update(
                frame_index, [parse_box(row["raw_analysis_box"]) for row in branch_rows]
            )
            for row, track in zip(branch_rows, tracks):
                output[row["candidate_id"]] = track
    return output


def validate_identity(
    reviews: Sequence[dict[str, str]],
    features: Sequence[dict[str, str]],
    candidates: Sequence[dict[str, str]],
    track_map: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if len(reviews) != EXPECTED_ROWS or len(features) != EXPECTED_ROWS:
        raise ValueError("canonical review and failure features must each contain 83 rows")
    feature_by_sample = index_unique(features, "sample_id")
    candidate_by_id = index_unique(candidates, "candidate_id")
    combined: list[dict[str, Any]] = []
    for review in reviews:
        feature = feature_by_sample.get(review["sample_id"])
        sealed = candidate_by_id.get(review["candidate_id"])
        if feature is None or sealed is None:
            raise ValueError(f"identity source missing for {review['sample_id']}")
        if feature["candidate_id"] != review["candidate_id"]:
            raise ValueError(f"feature candidate_id mismatch for {review['sample_id']}")
        track = track_map.get(review["candidate_id"])
        if track is None:
            raise ValueError(f"geometry track missing for {review['sample_id']}")
        fields = ("branch", "component_label", "frame_index")
        for field in fields:
            if not (review[field] == feature[field] == sealed[field]):
                raise ValueError(f"three-source identity mismatch {review['sample_id']} {field}")
        for field in ("raw_analysis_box", "selected_analysis_box"):
            if not (
                parse_box(review[field]) == parse_box(feature[field]) == parse_box(sealed[field])
            ):
                raise ValueError(f"three-source box mismatch {review['sample_id']} {field}")
        if review["branch"] == "small_component_experimental":
            for field in (
                "causal_recent_3_frame_hits", "causal_recent_5_frame_hits",
                "causal_track_age_frames", "causal_consecutive_hits",
                "causal_previous_gap_frames",
            ):
                if str(track[field]) != feature[field]:
                    raise ValueError(f"small tracker mismatch {review['sample_id']} {field}")
        signed_mean = float(feature["component_signed_gray_minus_background_mean"])
        recent3 = int(track["causal_recent_3_frame_hits"])
        polarity = "nonnegative" if signed_mean >= 0 else "negative"
        persistence = "persistent" if recent3 >= 2 else "transient"
        combined.append({
            "review": review,
            "feature": feature,
            "sealed": sealed,
            "track": dict(track),
            "signed_mean": signed_mean,
            "stratum": f"{polarity}_{persistence}",
        })
    if len({item["review"]["sample_id"] for item in combined}) != EXPECTED_ROWS:
        raise ValueError("sample identity is not 83/83 unique")
    return combined


def round_robin_stratified(items: Sequence[dict[str, Any]], cap: int) -> list[dict[str, Any]]:
    if cap < 1:
        raise ValueError("cap must be positive")
    buckets: dict[str, list[dict[str, Any]]] = {stratum: [] for stratum in STRATA}
    for item in items:
        buckets[item["stratum"]].append(item)
    for values in buckets.values():
        values.sort(key=lambda item: (
            item["review"]["temporal_track_id"],
            int(item["review"]["frame_index"]),
            item["review"]["sample_id"],
        ))
    if len(items) <= cap:
        return sorted(items, key=lambda item: int(item["review"]["sample_id"][2:]))
    selected: list[dict[str, Any]] = []
    offsets = {stratum: 0 for stratum in STRATA}
    while len(selected) < cap:
        progressed = False
        for stratum in STRATA:
            offset = offsets[stratum]
            if offset < len(buckets[stratum]):
                selected.append(buckets[stratum][offset])
                offsets[stratum] += 1
                progressed = True
                if len(selected) == cap:
                    break
        if not progressed:
            break
    return selected


def select_review_items(combined: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    invalid = [item for item in combined if item["review"]["review_class"] == "invalid"]
    invalid.sort(key=lambda item: (
        int(item["review"]["frame_index"]), item["review"]["sample_id"]
    ))
    deduplicated: list[dict[str, Any]] = []
    seen_tracks: set[str] = set()
    for item in invalid:
        track_id = item["review"]["temporal_track_id"]
        if not track_id:
            raise ValueError("invalid candidate has blank temporal_track_id")
        if track_id in seen_tracks:
            continue
        seen_tracks.add(track_id)
        deduplicated.append(item)

    selected_invalid: list[dict[str, Any]] = []
    branch_receipt: dict[str, Any] = {}
    for branch in ("main_area_topk", "small_component_experimental"):
        available = [item for item in deduplicated if item["review"]["branch"] == branch]
        selected = round_robin_stratified(available, BRANCH_CAP)
        if len(available) <= BRANCH_CAP and len(selected) != len(available):
            raise AssertionError("short branch was not selected completely")
        if len(selected) > BRANCH_CAP:
            raise AssertionError("branch cap exceeded")
        selected_invalid.extend(selected)
        branch_receipt[branch] = {
            "available_after_global_track_dedup": len(available),
            "selected": len(selected),
            "available_by_stratum": dict(sorted(Counter(
                item["stratum"] for item in available
            ).items())),
            "selected_by_stratum": dict(sorted(Counter(
                item["stratum"] for item in selected
            ).items())),
            "shortage_rule": "select_all_without_duplication" if len(available) <= BRANCH_CAP else "not_applicable",
        }

    controls = [
        item for item in combined
        if item["review"]["branch"] == "small_component_experimental"
        and item["feature"]["diag_keep_causal_2_of_3"] == "no"
        and (
            item["review"]["review_class"] == "ped"
            or item["review"].get("semantic_subtype") == "rider_bicycle"
        )
    ]
    controls.sort(key=lambda item: int(item["review"]["sample_id"][2:]))
    control_counts = Counter(
        "rider" if item["review"].get("semantic_subtype") == "rider_bicycle" else "ped"
        for item in controls
    )
    if control_counts != Counter({"ped": 4, "rider": 1}):
        raise ValueError(f"protection control contract changed: {dict(control_counts)}")

    selected_ids = [item["review"]["sample_id"] for item in selected_invalid]
    if len(selected_ids) != len(set(selected_ids)):
        raise AssertionError("duplicate invalid sample selected")
    selected_tracks = [item["review"]["temporal_track_id"] for item in selected_invalid]
    if len(selected_tracks) != len(set(selected_tracks)):
        raise AssertionError("temporal_track_id deduplication failed")
    targets = selected_invalid + controls
    if len({item["review"]["sample_id"] for item in targets}) != len(targets):
        raise AssertionError("review package contains duplicate samples")
    return targets, {
        "invalid_before_track_dedup": len(invalid),
        "invalid_after_global_track_dedup": len(deduplicated),
        "temporal_tracks_unique": len(seen_tracks),
        "branch_selection": branch_receipt,
        "selected_invalid": len(selected_invalid),
        "protection_controls": len(controls),
        "protection_control_counts": dict(sorted(control_counts.items())),
        "total_panels": len(targets),
        "stratum_order": list(STRATA),
        "within_stratum_order": "temporal_track_id, frame_index, sample_id",
        "selection_algorithm": "round-robin across fixed strata until branch cap; no duplication",
    }


def context_box(source_candidate_box: tuple[int, int, int, int],
                width: int = 1280, height: int = 720) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = source_candidate_box
    candidate_w, candidate_h = x1 - x0 + 1, y1 - y0 + 1
    target_w = min(width, max(180, candidate_w * 3))
    target_h = min(height, max(180, candidate_h * 3))
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    left = max(0, min(int(round(cx - target_w / 2)), width - target_w))
    top = max(0, min(int(round(cy - target_h / 2)), height - target_h))
    return left, top, left + target_w - 1, top + target_h - 1


def resize_letterbox(image: np.ndarray, size: tuple[int, int],
                     background: tuple[int, int, int] = (28, 28, 28)) -> np.ndarray:
    target_w, target_h = size
    scale = min(target_w / image.shape[1], target_h / image.shape[0])
    resized = cv2.resize(image, (
        max(1, int(round(image.shape[1] * scale))),
        max(1, int(round(image.shape[0] * scale))),
    ), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_NEAREST)
    canvas = np.full((target_h, target_w, 3), background, np.uint8)
    x = (target_w - resized.shape[1]) // 2
    y = (target_h - resized.shape[0]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def label_tile(image: np.ndarray, label: str) -> np.ndarray:
    result = image.copy()
    cv2.rectangle(result, (0, 0), (result.shape[1] - 1, 27), (0, 0, 0), -1)
    cv2.putText(result, label, (8, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 1, cv2.LINE_AA)
    return result


def signed_visual(signed: np.ndarray) -> np.ndarray:
    signed16 = signed.astype(np.int16)
    result = np.zeros((*signed16.shape, 3), np.uint8)
    result[:, :, 2] = np.clip(signed16, 0, 255).astype(np.uint8)
    result[:, :, 0] = np.clip(-signed16, 0, 255).astype(np.uint8)
    result[:, :, 1] = np.minimum(32, np.abs(signed16)).astype(np.uint8)
    return result


def draw_analysis_boxes(image: np.ndarray, raw_box: tuple[int, int, int, int],
                        selected_box: tuple[int, int, int, int]) -> np.ndarray:
    result = image.copy()
    cv2.rectangle(result, raw_box[:2], raw_box[2:], (0, 255, 255), 1)
    cv2.rectangle(result, selected_box[:2], selected_box[2:], (255, 0, 255), 1)
    return result


def render_panel(
    item: Mapping[str, Any],
    current_frame: np.ndarray,
    neighbor_crops: Mapping[int, np.ndarray],
    diagnostic: Mapping[str, np.ndarray],
) -> np.ndarray:
    review = item["review"]
    raw_analysis = parse_box(review["raw_analysis_box"])
    selected_analysis = parse_box(review["selected_analysis_box"])
    raw_source = source_box(raw_analysis, SAMPLE_STRIDE)
    selected_source = parse_box(review["selected_source_box"])

    top = current_frame.copy()
    cv2.rectangle(top, raw_source[:2], raw_source[2:], (0, 255, 255), 2)
    cv2.rectangle(top, selected_source[:2], selected_source[2:], (255, 0, 255), 3)
    role = item["review_role"]
    title = (
        f"{review['sample_id']} | {role} | {review['branch']} | frame {review['frame_index']} | "
        f"stratum {item['stratum']}"
    )
    cv2.rectangle(top, (0, 0), (1279, 74), (0, 0, 0), -1)
    cv2.putText(top, title, (14, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.66,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(top, "yellow=raw component box | magenta=selected/expanded box",
                (14, 57), cv2.FONT_HERSHEY_SIMPLEX, 0.58,
                (0, 255, 255), 2, cv2.LINE_AA)
    if role == "protection_control":
        cv2.putText(top, "CONTROL: do not assign a background subtype",
                    (760, 57), cv2.FONT_HERSHEY_SIMPLEX, 0.58,
                    (0, 128, 255), 2, cv2.LINE_AA)

    neighbor_tiles = []
    for offset, label in ((-1, "frame-1 context"), (0, "current context"), (1, "frame+1 context")):
        tile = resize_letterbox(neighbor_crops[offset], (426, 240))
        neighbor_tiles.append(label_tile(tile, label))
    neighbors = np.hstack(neighbor_tiles)
    if neighbors.shape[1] < 1280:
        neighbors = cv2.copyMakeBorder(neighbors, 0, 0, 0, 1280 - neighbors.shape[1],
                                       cv2.BORDER_CONSTANT, value=(28, 28, 28))

    gray_bgr = cv2.cvtColor(diagnostic["gray"], cv2.COLOR_GRAY2BGR)
    background_bgr = cv2.cvtColor(diagnostic["background"], cv2.COLOR_GRAY2BGR)
    signed_bgr = signed_visual(
        diagnostic["gray"].astype(np.int16) - diagnostic["background"].astype(np.int16)
    )
    raw_bgr = cv2.cvtColor((diagnostic["raw_mask"] * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    clean_bgr = cv2.cvtColor((diagnostic["clean_mask"] * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    run_bgr = cv2.cvtColor((diagnostic["run_filtered_mask"] * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    diagnostic_inputs = (
        (gray_bgr, "analysis gray"),
        (background_bgr, "background estimate"),
        (signed_bgr, "signed diff: blue darker / red brighter"),
        (raw_bgr, "raw threshold mask"),
        (clean_bgr, "3x3 clean mask"),
        (run_bgr, "min-run mask"),
    )
    diagnostic_tiles = []
    for image, label in diagnostic_inputs:
        boxed = draw_analysis_boxes(image, raw_analysis, selected_analysis)
        diagnostic_tiles.append(label_tile(resize_letterbox(boxed, (213, 180)), label))
    diagnostics = np.hstack(diagnostic_tiles)
    if diagnostics.shape[1] < 1280:
        diagnostics = cv2.copyMakeBorder(
            diagnostics, 0, 0, 0, 1280 - diagnostics.shape[1],
            cv2.BORDER_CONSTANT, value=(28, 28, 28),
        )
    return np.vstack((top, neighbors, diagnostics))


def replay_and_collect(
    video: Path,
    combined: Sequence[dict[str, Any]],
    targets: Sequence[dict[str, Any]],
) -> tuple[dict[str, np.ndarray], dict[str, dict[int, np.ndarray]],
           dict[str, dict[str, np.ndarray]], dict[str, Any]]:
    review_by_frame: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for item in combined:
        review_by_frame[int(item["review"]["frame_index"])].append(item)
    target_by_frame: dict[int, list[dict[str, Any]]] = defaultdict(list)
    neighbor_requests: dict[int, list[tuple[str, int, tuple[int, int, int, int]]]] = defaultdict(list)
    for item in targets:
        review = item["review"]
        frame_index = int(review["frame_index"])
        target_by_frame[frame_index].append(item)
        context = context_box(parse_box(review["selected_source_box"]))
        for offset in (-1, 0, 1):
            neighbor_requests[frame_index + offset].append((review["sample_id"], offset, context))

    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {video}")
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count != 479:
        raise ValueError(f"unexpected frame count: {frame_count}")
    chain = CandidateChainReference(
        learn_frames=LEARN_FRAMES, threshold=FOREGROUND_THRESHOLD,
        min_neighbors=3, min_area=MAIN_MIN_AREA, update_enable=True,
        freeze_foreground=True, min_run=2, top_k=4, sample_stride=SAMPLE_STRIDE,
    )
    config = Config(
        STRATEGY, "guarded_fill_only", PERSPECTIVE_THRESHOLD,
        PEAK_FLOOR, None, None, False,
    )
    current_frames: dict[str, np.ndarray] = {}
    neighbor_crops: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    diagnostics: dict[str, dict[str, np.ndarray]] = {}
    identity_count = 0
    decoded = 0
    try:
        for frame_index in range(frame_count):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"decode stopped at frame {frame_index}/{frame_count}")
            decoded += 1
            for sample_id, offset, context in neighbor_requests.get(frame_index, []):
                x0, y0, x1, y1 = context
                neighbor_crops[sample_id][offset] = frame[y0:y1 + 1, x0:x1 + 1].copy()
            result = chain.process_bgr(frame, frame_index)
            if frame_index < WARMUP_FRAMES:
                continue
            components = extract_components(result["run_filtered_mask"], result["difference"])
            selected, _, _ = guarded_select(components, config, 256, 144)
            for item in review_by_frame.get(frame_index, []):
                review = item["review"]
                slot = int(review["slot"])
                if slot >= len(selected):
                    raise AssertionError(f"replay slot missing for {review['sample_id']}")
                entry = selected[slot]
                component: Component = entry["component"]
                candidate_id = f"{STRATEGY}:f{frame_index:06d}:slot{slot}:cc{component.label}"
                checks = (
                    candidate_id == review["candidate_id"],
                    entry["branch"] == review["branch"],
                    component.label == int(review["component_label"]),
                    component.box == parse_box(review["raw_analysis_box"]),
                    tuple(entry["selected_box"]) == parse_box(review["selected_analysis_box"]),
                )
                if not all(checks):
                    raise AssertionError(f"replay identity mismatch: {review['sample_id']}")
                identity_count += 1
            for item in target_by_frame.get(frame_index, []):
                sample_id = item["review"]["sample_id"]
                current_frames[sample_id] = frame.copy()
                diagnostics[sample_id] = {
                    key: result[key].copy()
                    for key in (
                        "gray", "background", "raw_mask", "clean_mask", "run_filtered_mask"
                    )
                }
    finally:
        capture.release()
    if decoded != frame_count or identity_count != EXPECTED_ROWS:
        raise AssertionError("single-pass replay coverage failed")
    target_ids = {item["review"]["sample_id"] for item in targets}
    if set(current_frames) != target_ids or set(diagnostics) != target_ids:
        raise AssertionError("target current-frame/diagnostic coverage failed")
    if any(set(neighbor_crops[sample_id]) != {-1, 0, 1} for sample_id in target_ids):
        raise AssertionError("neighbor crop coverage failed")
    return current_frames, dict(neighbor_crops), diagnostics, {
        "decoded_frames": decoded,
        "decoded_from_frame_zero": True,
        "single_video_decode_pass": True,
        "review_identity_matches": identity_count,
        "review_identity_expected": EXPECTED_ROWS,
        "annotation_accessed": False,
    }


def make_manifest_rows(
    targets: Sequence[dict[str, Any]], panel_receipts: Mapping[str, Mapping[str, str]]
) -> list[dict[str, Any]]:
    rows = []
    for index, item in enumerate(targets):
        review = item["review"]
        feature = item["feature"]
        role = item["review_role"]
        rows.append({
            "review_item_id": f"bs{index:04d}",
            "sample_id": review["sample_id"],
            "candidate_id": review["candidate_id"],
            "review_role": role,
            "background_truth_allowed": "yes" if role == "background_subtype_target" else "no",
            "control_instruction": (
                "" if role == "background_subtype_target"
                else "protection control: do not assign a background subtype"
            ),
            "frame_index": review["frame_index"],
            "interval_id": review["interval_id"],
            "branch": review["branch"],
            "temporal_track_id": review["temporal_track_id"],
            "source_review_class": review["review_class"],
            "source_semantic_subtype": review.get("semantic_subtype", ""),
            "selection_stratum": item["stratum"],
            "component_signed_gray_minus_background_mean": (
                feature["component_signed_gray_minus_background_mean"]
            ),
            "causal_recent_3_frame_hits": item["track"]["causal_recent_3_frame_hits"],
            "causal_recent_5_frame_hits": item["track"]["causal_recent_5_frame_hits"],
            "raw_analysis_box": review["raw_analysis_box"],
            "selected_analysis_box": review["selected_analysis_box"],
            "selected_source_box": review["selected_source_box"],
            "panel_path": panel_receipts[review["sample_id"]]["path"],
            "panel_sha256": panel_receipts[review["sample_id"]]["sha256"],
            "background_subtype": "",
            "reviewer": "",
            "reviewed_at": "",
            "review_note": "",
        })
    return rows


def render_contact_sheets(output: Path, panel_paths: Sequence[Path]) -> list[dict[str, Any]]:
    contact_dir = output / "contact_sheets"
    contact_dir.mkdir(parents=True, exist_ok=True)
    receipts = []
    for sheet_index, start in enumerate(range(0, len(panel_paths), CONTACT_SHEET_SIZE), start=1):
        selected = panel_paths[start:start + CONTACT_SHEET_SIZE]
        canvas = np.full((1040, 1240, 3), 245, np.uint8)
        for local_index, path in enumerate(selected):
            panel = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if panel is None:
                raise ValueError(f"cannot read rendered panel: {path}")
            thumb = resize_letterbox(panel, (600, 490), (245, 245, 245))
            row, col = divmod(local_index, 2)
            x, y = 20 + col * 610, 20 + row * 505
            canvas[y:y + 490, x:x + 600] = thumb
            cv2.putText(canvas, path.stem, (x + 8, y + 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)
        path = contact_dir / f"contact_sheet_{sheet_index:02d}.jpg"
        if not cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 92]):
            raise ValueError(f"cannot write contact sheet: {path}")
        receipts.append({
            "path": str(path.relative_to(output)).replace("\\", "/"),
            "sha256": file_hash(path),
            "panel_count": len(selected),
        })
    return receipts


def readme(selection: Mapping[str, Any]) -> str:
    return "\n".join([
        "# VIRAT 010107 background subtype review",
        "",
        "This package contains a bounded human review of deduplicated invalid candidates plus protection controls.",
        "",
        "## Human fields",
        "",
        "For rows with `review_role=background_subtype_target`, set `background_subtype` to exactly one of:",
        "`shadow`, `parking_line_related`, `background_change`, `other`, or `uncertain`.",
        "Also fill `reviewer`, `reviewed_at`, and optionally `review_note`.",
        "",
        "Rows with `review_role=protection_control` are known ped/rider controls removed by the causal 2-of-3 diagnostic.",
        "Do not assign them a background subtype; leave `background_subtype` blank and use `review_note` only for review comments.",
        "",
        "## Panel legend",
        "",
        "- Yellow: raw component box.",
        "- Magenta: selected or expanded candidate box.",
        "- Signed difference: blue means darker than background; red means brighter.",
        "- Masks show raw threshold, 3x3 cleanup, and row minimum-run stages.",
        "",
        f"Selected invalid candidates: {selection['selected_invalid']}; protection controls: {selection['protection_controls']}.",
        "Selection was deterministic and used no annotation or visual cherry-picking.",
        "",
    ])


def run(args: argparse.Namespace) -> dict[str, Any]:
    review = args.review.resolve()
    features = args.features.resolve()
    candidates = args.candidates.resolve()
    video = args.video.resolve()
    output = args.output.resolve()
    receipt_inputs = validate_inputs(review, features, candidates, video, output)
    _, review_rows = read_csv(review)
    _, feature_rows = read_csv(features)
    _, candidate_rows = read_csv(candidates)
    track_map = build_geometry_tracks(candidate_rows)
    combined = validate_identity(review_rows, feature_rows, candidate_rows, track_map)
    targets, selection_receipt = select_review_items(combined)
    invalid_ids = {
        item["review"]["sample_id"] for item in targets
        if item["review"]["review_class"] == "invalid"
    }
    for item in targets:
        item["review_role"] = (
            "background_subtype_target"
            if item["review"]["sample_id"] in invalid_ids else "protection_control"
        )

    current_frames, neighbor_crops, diagnostics, replay_receipt = replay_and_collect(
        video, combined, targets
    )
    output.mkdir(parents=True, exist_ok=True)
    panel_dir = output / "panels"
    panel_dir.mkdir(parents=True, exist_ok=True)
    panel_receipts: dict[str, dict[str, str]] = {}
    panel_paths: list[Path] = []
    for item in targets:
        sample_id = item["review"]["sample_id"]
        panel = render_panel(
            item, current_frames[sample_id], neighbor_crops[sample_id], diagnostics[sample_id]
        )
        path = panel_dir / f"panel_{sample_id}.png"
        if not cv2.imwrite(str(path), panel, [cv2.IMWRITE_PNG_COMPRESSION, 4]):
            raise ValueError(f"cannot write panel: {path}")
        panel_paths.append(path)
        panel_receipts[sample_id] = {
            "path": str(path.relative_to(output)).replace("\\", "/"),
            "sha256": file_hash(path),
        }
    contact_receipts = render_contact_sheets(output, panel_paths)

    manifest_rows = make_manifest_rows(targets, panel_receipts)
    manifest_path = output / "review_manifest.csv"
    manifest_headers = list(manifest_rows[0])
    write_csv(manifest_path, manifest_headers, manifest_rows)
    if manifest_path.read_bytes().startswith(b"PK"):
        raise AssertionError("review_manifest.csv is not a true CSV")
    human_fields = ("background_subtype", "reviewer", "reviewed_at", "review_note")
    if any(row[field] for row in manifest_rows for field in human_fields):
        raise AssertionError("human review fields were not initialized blank")

    report_path = output / "report.json"
    readme_path = output / "README.md"
    receipt_path = output / "receipt.json"
    input_hashes = {
        "canonical_review_manifest.csv": file_hash(review),
        "failure_source_features.csv": file_hash(features),
        "sealed_candidates.csv": file_hash(candidates),
        "official_video": file_hash(video),
        **receipt_inputs,
    }
    selection_by_role = dict(sorted(Counter(row["review_role"] for row in manifest_rows).items()))
    report = {
        "schema": "virat_background_subtype_review_v1",
        "scope": {
            "scene": "VIRAT_S_010107_02_000282_000312",
            "development_only": True,
            "annotation_accessed": False,
            "blind_holdout_or_test_accessed": False,
            "training_or_threshold_tuning_performed": False,
        },
        "inputs": {
            "paths": {
                "review": str(review),
                "failure_features": str(features),
                "candidates": str(candidates),
                "video": str(video),
            },
            "sha256": input_hashes,
            "script_sha256": file_hash(SCRIPT),
        },
        "identity_assertions": {
            "canonical_review_rows": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "review_feature_candidate_three_source_match": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_match": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "status": "pass",
        },
        "selection": selection_receipt,
        "selected_by_role": selection_by_role,
        "human_review_contract": {
            "authoritative_input": "review_manifest.csv",
            "background_subtype_allowed_values": list(SUBTYPE_VALUES),
            "human_fields_initialized_blank": list(human_fields),
            "protection_controls": "background_subtype must remain blank; controls are not background truth",
        },
        "panel_contract": {
            "native_current_frame": "1280x720 with raw and selected boxes",
            "neighbor_context": ["frame-1", "current", "frame+1"],
            "diagnostics": [
                "analysis gray", "background estimate", "signed gray-background",
                "raw threshold mask", "3x3 cleanup mask", "minimum-run mask",
            ],
            "signed_legend": "blue=darker than background; red=brighter than background",
        },
        "replay": replay_receipt,
        "outputs": {
            "review_manifest": "review_manifest.csv",
            "panel_count": len(panel_paths),
            "contact_sheet_count": len(contact_receipts),
            "contact_sheets": contact_receipts,
        },
        "limitations": [
            "The package samples at most twelve deduplicated invalid tracks per branch.",
            "Protection controls are semantic targets and must not be labelled as background.",
            "The Python candidate chain is algorithmic and does not model RTL cycle timing or overflow.",
        ],
    }
    write_json(report_path, report)
    readme_path.write_text(readme(selection_receipt), encoding="utf-8")

    output_files = [manifest_path, report_path, readme_path, *panel_paths]
    output_files.extend(output / item["path"] for item in contact_receipts)
    artifact_hashes = {
        str(path.relative_to(output)).replace("\\", "/"): file_hash(path)
        for path in output_files
    }
    receipt = {
        "schema": "virat_background_subtype_review_receipt_v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script_sha256": file_hash(SCRIPT),
        "input_hashes": input_hashes,
        "artifact_hashes": artifact_hashes,
        "receipt_self_hash_included": False,
        "assertions": {
            "three_source_identity_83_of_83": True,
            "causal_replay_identity_83_of_83": True,
            "selection_strata_recorded": True,
            "branch_cap_le_12": True,
            "invalid_temporal_tracks_unique": True,
            "protection_controls_4_ped_1_rider": True,
            "human_fields_blank": True,
            "review_manifest_is_true_csv": True,
            "panel_count_matches_manifest": len(panel_paths) == len(manifest_rows),
            "contact_sheet_panel_coverage": sum(
                item["panel_count"] for item in contact_receipts
            ) == len(panel_paths),
            "single_video_decode_from_frame_zero": True,
            "annotation_accessed": False,
        },
    }
    write_json(receipt_path, receipt)
    parsed = json.loads(receipt_path.read_text(encoding="utf-8"))
    for relative, expected in parsed["artifact_hashes"].items():
        if file_hash(output / relative) != expected:
            raise RuntimeError(f"artifact readback hash mismatch: {relative}")
    if parsed["script_sha256"] != file_hash(SCRIPT):
        raise RuntimeError("script readback hash mismatch")
    return {
        "output": str(output),
        "review_rows": len(manifest_rows),
        "selected_by_role": selection_by_role,
        "selection": selection_receipt,
        "receipt_sha256": file_hash(receipt_path),
    }


def self_test() -> None:
    try:
        guard_path(Path("x/blind_reserve/y"))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("sealed path guard failed")
    assert context_box((0, 0, 10, 10))[0:2] == (0, 0)
    fake: list[dict[str, Any]] = []
    for index, stratum in enumerate(STRATA):
        for repetition in range(4):
            fake.append({
                "stratum": stratum,
                "review": {
                    "temporal_track_id": f"t{index}_{repetition}",
                    "frame_index": str(index * 10 + repetition),
                    "sample_id": f"vr{index * 10 + repetition:05d}",
                },
            })
    selected = round_robin_stratified(fake, 12)
    assert len(selected) == 12
    assert Counter(item["stratum"] for item in selected) == Counter({s: 3 for s in STRATA})
    short = round_robin_stratified(fake[:3], 12)
    assert len(short) == 3 and len({id(item) for item in short}) == 3
    signed = np.array([[-20, 0, 30]], np.int16)
    visual = signed_visual(signed)
    assert visual[0, 0, 0] == 20 and visual[0, 2, 2] == 30
    image = np.zeros((720, 1280, 3), np.uint8)
    tile = resize_letterbox(image, (213, 180))
    assert tile.shape == (180, 213, 3)
    print("SELF_TEST PASS")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    result = run(args)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
