#!/usr/bin/env python3
"""Causal failure-source sidecar for the reviewed VIRAT 010107 scene.

The tool verifies sealed inputs, replays the candidate path once from frame zero,
and binds every reviewed row back to its exact component.  It records diagnostic
features and three preregistered small-branch keep rules.  It does not change
boxes, train a model, use annotations, tune thresholds, or access sealed data.
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
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import cv2
import numpy as np


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from candidate_chain_reference import CandidateChainReference  # noqa: E402
from fixed_budget_candidate_prototype import (  # noqa: E402
    Component,
    extract_components,
    inclusive_iou,
)
from guarded_final4_arbitration import Config, guarded_select  # noqa: E402


DEFAULT_REVIEW = (
    PROJECT / "evaluation/scene_extensions/virat_010107_02_t100_review_v1"
    / "canonical_review_manifest.csv"
)
DEFAULT_SCENE = PROJECT / "evaluation/scene_extensions/virat_010107_02_t100"
DEFAULT_CANDIDATES = DEFAULT_SCENE / "candidates.csv"
DEFAULT_REPORT = DEFAULT_SCENE / "report.json"
DEFAULT_OUTPUT = (
    PROJECT / "evaluation/scene_extensions/virat_010107_failure_sources_v1"
)

EXPECTED_ROWS = 83
STRATEGY = "fill_only_T100"
ANALYSIS_WIDTH = 256
ANALYSIS_HEIGHT = 144
SAMPLE_STRIDE = 5
LEARN_FRAMES = 4
FOREGROUND_THRESHOLD = 20
MAIN_MIN_AREA = 16
PERSPECTIVE_THRESHOLD = 100
PEAK_FLOOR = 40
WARMUP_FRAMES = 120
RUN_RAW_THRESHOLDS = (0.5, 0.75)
TRACK_MAX_GAP = 5
TRACK_IOU = 0.3
TRACK_CENTER_DELTA = 3.0
FORBIDDEN = re.compile(r"(^|[/\\_.-])(blind|holdout|reserve|test)($|[/\\_.-])", re.I)

POLICIES = (
    "small_run_raw_ge_0p5",
    "small_run_raw_ge_0p75",
    "small_causal_2_of_3",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha512(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def guard_path(path: Path) -> None:
    if FORBIDDEN.search(str(path).replace("\\", "/")):
        raise ValueError(f"sealed path rejected: {path}")


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


def parse_box(value: str) -> tuple[int, int, int, int]:
    parsed = json.loads(value)
    if not isinstance(parsed, list) or len(parsed) != 4:
        raise ValueError(f"invalid inclusive box: {value!r}")
    box = tuple(int(item) for item in parsed)
    if box[0] > box[2] or box[1] > box[3]:
        raise ValueError(f"inverted inclusive box: {value!r}")
    return box


def box_json(box: tuple[int, int, int, int]) -> str:
    return json.dumps(list(box), separators=(",", ":"))


def box_area(box: tuple[int, int, int, int]) -> int:
    return (box[2] - box[0] + 1) * (box[3] - box[1] + 1)


def center(box: tuple[int, int, int, int]) -> tuple[float, float]:
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)


def fmt(value: float) -> str:
    if not math.isfinite(value):
        raise ValueError("non-finite diagnostic value")
    return f"{value:.9g}"


def array_stats(values: np.ndarray, prefix: str) -> dict[str, Any]:
    flat = values.reshape(-1)
    if not flat.size:
        raise ValueError(f"empty array for {prefix}")
    float_values = flat.astype(np.float64)
    return {
        f"{prefix}_mean": fmt(float(float_values.mean())),
        f"{prefix}_std": fmt(float(float_values.std())),
        f"{prefix}_min": int(flat.min()),
        f"{prefix}_max": int(flat.max()),
    }


def labels_for(mask: np.ndarray) -> np.ndarray:
    _, labels = cv2.connectedComponents((mask != 0).astype(np.uint8), connectivity=8)
    return labels


def intersecting_component_count(labels: np.ndarray,
                                 box: tuple[int, int, int, int]) -> int:
    x0, y0, x1, y1 = box
    values = np.unique(labels[y0:y1 + 1, x0:x1 + 1])
    return int(np.count_nonzero(values))


def crop(array: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    x0, y0, x1, y1 = box
    return array[y0:y1 + 1, x0:x1 + 1]


@dataclass
class Track:
    track_id: str
    first_frame: int
    last_frame: int
    last_box: tuple[int, int, int, int]
    hits: deque[int] = field(default_factory=deque)
    consecutive: int = 1


class GeometryTracker:
    """One-to-one causal association using only past and current raw boxes."""

    def __init__(self) -> None:
        self.tracks: dict[str, Track] = {}
        self.next_id = 0

    def _eligible_edges(
        self,
        frame_index: int,
        boxes: Sequence[tuple[int, int, int, int]],
    ) -> list[tuple[float, float, int, str, int]]:
        edges = []
        for candidate_index, candidate_box in enumerate(boxes):
            cx, cy = center(candidate_box)
            for track_id, track in self.tracks.items():
                gap = frame_index - track.last_frame
                if gap < 1 or gap > TRACK_MAX_GAP:
                    continue
                tx, ty = center(track.last_box)
                iou = inclusive_iou(candidate_box, track.last_box)
                dx, dy = abs(cx - tx), abs(cy - ty)
                if iou < TRACK_IOU and not (dx <= TRACK_CENTER_DELTA and dy <= TRACK_CENTER_DELTA):
                    continue
                edges.append((-iou, dx + dy, gap, track_id, candidate_index))
        return sorted(edges)

    def update(
        self,
        frame_index: int,
        boxes: Sequence[tuple[int, int, int, int]],
    ) -> list[dict[str, Any]]:
        assignments: dict[int, str] = {}
        used_tracks: set[str] = set()
        for _, _, _, track_id, candidate_index in self._eligible_edges(frame_index, boxes):
            if candidate_index in assignments or track_id in used_tracks:
                continue
            assignments[candidate_index] = track_id
            used_tracks.add(track_id)

        output: list[dict[str, Any]] = []
        for index, candidate_box in enumerate(boxes):
            if index in assignments:
                track = self.tracks[assignments[index]]
                previous_gap: int | None = frame_index - track.last_frame
                track.consecutive = track.consecutive + 1 if previous_gap == 1 else 1
                track.last_frame = frame_index
                track.last_box = candidate_box
                track.hits.append(frame_index)
            else:
                track_id = f"geometry_track_{self.next_id:05d}"
                self.next_id += 1
                track = Track(track_id, frame_index, frame_index, candidate_box,
                              deque([frame_index]), 1)
                self.tracks[track_id] = track
                previous_gap = None
            while track.hits and frame_index - track.hits[0] > TRACK_MAX_GAP:
                track.hits.popleft()
            recent3 = sum(frame_index - hit <= 2 for hit in track.hits)
            recent5 = sum(frame_index - hit <= 4 for hit in track.hits)
            output.append({
                "causal_track_id": track.track_id,
                "causal_recent_3_frame_hits": recent3,
                "causal_recent_5_frame_hits": recent5,
                "causal_track_age_frames": frame_index - track.first_frame + 1,
                "causal_consecutive_hits": track.consecutive,
                "causal_previous_gap_frames": "" if previous_gap is None else previous_gap,
            })
        return output


def semantic_label(row: Mapping[str, str]) -> str:
    if row["review_class"] == "ped":
        return "ped"
    if row["review_class"] == "invalid":
        return "invalid"
    if row["review_class"] == "ignore" and row.get("semantic_subtype") == "rider_bicycle":
        return "rider"
    raise ValueError(f"unsupported reviewed label for {row.get('sample_id')}")


def validate_inputs(review: Path, candidates: Path, scene_report: Path,
                    output: Path) -> dict[str, Any]:
    for path in (review, candidates, scene_report, output):
        guard_path(path.resolve())
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")

    scene_dir = scene_report.parent
    artifact_hashes_path = scene_dir / "artifact_hashes.json"
    receipt_path = scene_dir / "receipt.json"
    review_receipt_path = review.parent / "receipt.json"
    for path in (artifact_hashes_path, receipt_path, review_receipt_path):
        guard_path(path.resolve())
        if not path.is_file():
            raise ValueError(f"missing receipt input: {path}")
    artifact_hashes = json.loads(artifact_hashes_path.read_text(encoding="utf-8"))
    scene_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    review_receipt = json.loads(review_receipt_path.read_text(encoding="utf-8"))
    if sha256(candidates) != artifact_hashes.get("candidates.csv"):
        raise ValueError("sealed candidates.csv hash mismatch")
    if sha256(scene_report) != artifact_hashes.get("report.json"):
        raise ValueError("sealed report.json hash mismatch")
    if sha256(artifact_hashes_path) != scene_receipt.get("artifact_hashes_sha256"):
        raise ValueError("scene artifact-hash receipt mismatch")
    if sha256(review) != review_receipt.get("artifact_hashes", {}).get(review.name):
        raise ValueError("canonical review manifest hash mismatch")

    report = json.loads(scene_report.read_text(encoding="utf-8"))
    video = Path(report["inputs"]["video"]["path"])
    guard_path(video.resolve())
    if sha256(video) != report["inputs"]["video"]["sha256"]:
        raise ValueError("source video SHA256 mismatch")
    if sha512(video) != report["inputs"]["video"]["sha512"]:
        raise ValueError("source video SHA512 mismatch")
    dependencies = {
        "tools/candidate_chain_reference.py": TOOLS / "candidate_chain_reference.py",
        "tools/fixed_budget_candidate_prototype.py": TOOLS / "fixed_budget_candidate_prototype.py",
        "tools/guarded_final4_arbitration.py": TOOLS / "guarded_final4_arbitration.py",
    }
    expected_dependencies = report["inputs"]["dependency_hashes"]
    for key, path in dependencies.items():
        if sha256(path) != expected_dependencies[key]:
            raise ValueError(f"candidate dependency differs from sealed replay: {key}")
    contract = report["candidate_contract"]
    expected_contract = {
        "main_min_area": MAIN_MIN_AREA,
        "peak_floor": PEAK_FLOOR,
        "perspective_threshold": PERSPECTIVE_THRESHOLD,
        "final_budget": 4,
        "no_replacement": True,
    }
    for key, expected in expected_contract.items():
        if contract.get(key) != expected:
            raise ValueError(f"scene contract mismatch for {key}")
    if report["causal_timing"]["warmup_frames_not_scored"] != WARMUP_FRAMES:
        raise ValueError("warmup frame contract mismatch")
    return {
        "report": report,
        "video": video,
        "artifact_hashes_path": artifact_hashes_path,
        "scene_receipt_path": receipt_path,
        "review_receipt_path": review_receipt_path,
        "dependency_paths": dependencies,
    }


def index_rows(rows: Sequence[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if value in indexed:
            raise ValueError(f"duplicate {key}: {value}")
        indexed[value] = row
    return indexed


def identity_assertions(
    review_rows: Sequence[dict[str, str]],
    candidate_index: Mapping[str, dict[str, str]],
) -> dict[int, list[dict[str, str]]]:
    if len(review_rows) != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} reviewed rows, got {len(review_rows)}")
    if len({row["sample_id"] for row in review_rows}) != EXPECTED_ROWS:
        raise ValueError("review sample_id values are not unique")
    by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    compare_fields = (
        "candidate_id", "frame_index", "slot", "branch", "component_label",
        "component_area", "component_peak_difference", "raw_analysis_box",
        "selected_analysis_box",
    )
    for row in review_rows:
        sealed = candidate_index.get(row["candidate_id"])
        if sealed is None:
            raise ValueError(f"review candidate missing from sealed table: {row['candidate_id']}")
        if sealed["strategy"] != STRATEGY:
            raise ValueError(f"review candidate is not {STRATEGY}: {row['candidate_id']}")
        for field in compare_fields:
            if field.endswith("_box"):
                equal = parse_box(row[field]) == parse_box(sealed[field])
            else:
                equal = row[field] == sealed[field]
            if not equal:
                raise ValueError(f"sealed identity mismatch {row['sample_id']} field={field}")
        by_frame[int(row["frame_index"])].append(row)
    for frame_rows in by_frame.values():
        frame_rows.sort(key=lambda row: int(row["slot"]))
    return by_frame


def feature_row(
    review: Mapping[str, str],
    component: Component,
    selected_box: tuple[int, int, int, int],
    result: Mapping[str, Any],
    stage_labels: Mapping[str, np.ndarray],
    track: Mapping[str, Any] | None,
) -> dict[str, Any]:
    raw_box = component.box
    gray = result["gray"]
    background = result["background"]
    difference = result["difference"]
    raw_mask = result["raw_mask"]
    clean_mask = result["clean_mask"]
    run_mask = result["run_filtered_mask"]
    signed = gray.astype(np.int16) - background.astype(np.int16)

    raw_gray = crop(gray, raw_box)
    raw_background = crop(background, raw_box)
    raw_signed = crop(signed, raw_box)
    raw_abs = crop(difference, raw_box)
    component_pixels = stage_labels["run"] == component.label
    component_signed = signed[component_pixels]
    component_abs = difference[component_pixels]

    raw_pixels = int(crop(raw_mask, raw_box).sum())
    clean_pixels = int(crop(clean_mask, raw_box).sum())
    run_pixels = int(crop(run_mask, raw_box).sum())
    if raw_pixels <= 0 or clean_pixels <= 0 or run_pixels <= 0:
        raise AssertionError(f"selected component has an empty prerequisite stage: {review['sample_id']}")
    if int(component_pixels.sum()) != component.area:
        raise AssertionError(f"component label/area mismatch: {review['sample_id']}")

    raw_width = raw_box[2] - raw_box[0] + 1
    raw_height = raw_box[3] - raw_box[1] + 1
    selected_width = selected_box[2] - selected_box[0] + 1
    selected_height = selected_box[3] - selected_box[1] + 1
    ratio = run_pixels / raw_pixels
    branch = review["branch"]
    is_small = branch == "small_component_experimental"
    if not is_small and branch != "main_area_topk":
        raise ValueError(f"unsupported branch: {branch}")

    row: dict[str, Any] = {
        "sample_id": review["sample_id"],
        "candidate_id": review["candidate_id"],
        "frame_index": review["frame_index"],
        "interval_id": review["interval_id"],
        "slot": review["slot"],
        "branch": branch,
        "review_class": review["review_class"],
        "semantic_subtype": review.get("semantic_subtype", ""),
        "semantic_label": semantic_label(review),
        "candidate_condition": review["candidate_condition"],
        "component_label": component.label,
        "component_area": component.area,
        "component_peak_difference": component.peak_difference,
        "raw_analysis_box": box_json(raw_box),
        "selected_analysis_box": box_json(selected_box),
        "raw_bbox_width": raw_width,
        "raw_bbox_height": raw_height,
        "raw_bbox_area": box_area(raw_box),
        "raw_bbox_component_fill_ratio": fmt(component.area / box_area(raw_box)),
        "selected_bbox_width": selected_width,
        "selected_bbox_height": selected_height,
        "selected_bbox_area": box_area(selected_box),
        "expansion_area_ratio": fmt(box_area(selected_box) / box_area(raw_box)),
        "expansion_left": raw_box[0] - selected_box[0],
        "expansion_top": raw_box[1] - selected_box[1],
        "expansion_right": selected_box[2] - raw_box[2],
        "expansion_bottom": selected_box[3] - raw_box[3],
        "raw_bbox_center_x": fmt(center(raw_box)[0]),
        "raw_bbox_center_y": fmt(center(raw_box)[1]),
        "raw_bbox_raw_pixels": raw_pixels,
        "raw_bbox_clean_pixels": clean_pixels,
        "raw_bbox_run_pixels": run_pixels,
        "clean_over_raw_survival": fmt(clean_pixels / raw_pixels),
        "run_over_raw_survival": fmt(ratio),
        "run_over_clean_survival": fmt(run_pixels / clean_pixels),
        "raw_stage_intersecting_components": intersecting_component_count(stage_labels["raw"], raw_box),
        "clean_stage_intersecting_components": intersecting_component_count(stage_labels["clean"], raw_box),
        "run_stage_intersecting_components": intersecting_component_count(stage_labels["run"], raw_box),
        "component_signed_gray_minus_background_mean": fmt(float(component_signed.mean())),
        "component_signed_gray_minus_background_min": int(component_signed.min()),
        "component_signed_gray_minus_background_max": int(component_signed.max()),
        "component_signed_positive_fraction": fmt(float(np.mean(component_signed > 0))),
        "component_signed_negative_fraction": fmt(float(np.mean(component_signed < 0))),
        "component_abs_difference_mean": fmt(float(component_abs.mean())),
        "component_abs_difference_max": int(component_abs.max()),
        "diag_keep_run_raw_ge_0p5": "yes" if (not is_small or ratio >= 0.5) else "no",
        "diag_keep_run_raw_ge_0p75": "yes" if (not is_small or ratio >= 0.75) else "no",
        "signed_polarity_filter_applied": "no",
    }
    row.update(array_stats(raw_gray, "raw_bbox_gray"))
    row.update(array_stats(raw_background, "raw_bbox_background"))
    row.update(array_stats(raw_signed, "raw_bbox_signed_gray_minus_background"))
    row.update(array_stats(raw_abs, "raw_bbox_abs_difference"))
    row.update(array_stats(crop(gray, selected_box), "selected_bbox_gray"))
    row.update(array_stats(crop(background, selected_box), "selected_bbox_background"))
    row.update(array_stats(crop(difference, selected_box), "selected_bbox_abs_difference"))
    if is_small:
        if track is None:
            raise AssertionError("small candidate lacks causal geometry track")
        row.update(track)
        row["diag_keep_causal_2_of_3"] = (
            "yes" if int(track["causal_recent_3_frame_hits"]) >= 2 else "no"
        )
    else:
        row.update({
            "causal_track_id": "",
            "causal_recent_3_frame_hits": "",
            "causal_recent_5_frame_hits": "",
            "causal_track_age_frames": "",
            "causal_consecutive_hits": "",
            "causal_previous_gap_frames": "",
            "diag_keep_causal_2_of_3": "yes",
        })
    return row


def replay(
    video: Path,
    report: Mapping[str, Any],
    review_by_frame: Mapping[int, list[dict[str, str]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {video}")
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    expected_clip = report["clip"]
    if (frame_count, width, height) != (
        expected_clip["frame_count"], expected_clip["width"], expected_clip["height"]
    ) or not math.isclose(fps, expected_clip["fps"], rel_tol=0.0, abs_tol=1e-6):
        raise ValueError("decoded video metadata differs from sealed report")

    chain = CandidateChainReference(
        learn_frames=LEARN_FRAMES,
        threshold=FOREGROUND_THRESHOLD,
        min_neighbors=3,
        min_area=MAIN_MIN_AREA,
        update_enable=True,
        freeze_foreground=True,
        min_run=2,
        top_k=4,
        sample_stride=SAMPLE_STRIDE,
    )
    fill_config = Config(
        STRATEGY, "guarded_fill_only", PERSPECTIVE_THRESHOLD,
        PEAK_FLOOR, None, None, False,
    )
    tracker = GeometryTracker()
    features: list[dict[str, Any]] = []
    matched_ids: set[str] = set()
    decoded = 0
    small_tracked = 0
    try:
        for frame_index in range(frame_count):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"decode stopped at frame {frame_index}/{frame_count}")
            decoded += 1
            result = chain.process_bgr(frame, frame_index)
            if frame_index < WARMUP_FRAMES:
                continue
            components = extract_components(result["run_filtered_mask"], result["difference"])
            selected, _, diagnostics = guarded_select(
                components, fill_config, ANALYSIS_WIDTH, ANALYSIS_HEIGHT
            )
            if diagnostics["final_candidates"] > 4:
                raise AssertionError("final candidate budget exceeded")
            small_entries = [
                entry for entry in selected
                if entry["branch"] == "small_component_experimental"
            ]
            track_rows = tracker.update(
                frame_index, [tuple(entry["raw_box"]) for entry in small_entries]
            )
            small_tracked += len(small_entries)
            track_by_key = {
                (entry["component"].label, tuple(entry["selected_box"])): track
                for entry, track in zip(small_entries, track_rows)
            }
            if frame_index not in review_by_frame:
                continue

            stage_labels = {
                "raw": labels_for(result["raw_mask"]),
                "clean": labels_for(result["clean_mask"]),
                "run": labels_for(result["run_filtered_mask"]),
            }
            for review in review_by_frame[frame_index]:
                slot = int(review["slot"])
                if slot >= len(selected):
                    raise AssertionError(f"replay slot missing for {review['sample_id']}")
                entry = selected[slot]
                component: Component = entry["component"]
                raw_box = tuple(entry["raw_box"])
                selected_box = tuple(entry["selected_box"])
                replay_id = f"{STRATEGY}:f{frame_index:06d}:slot{slot}:cc{component.label}"
                assertions = {
                    "candidate_id": replay_id == review["candidate_id"],
                    "branch": entry["branch"] == review["branch"],
                    "component_label": component.label == int(review["component_label"]),
                    "component_area": component.area == int(review["component_area"]),
                    "component_peak_difference": (
                        component.peak_difference == int(review["component_peak_difference"])
                    ),
                    "raw_analysis_box": raw_box == parse_box(review["raw_analysis_box"]),
                    "selected_analysis_box": (
                        selected_box == parse_box(review["selected_analysis_box"])
                    ),
                }
                if not all(assertions.values()):
                    failed = [key for key, value in assertions.items() if not value]
                    raise AssertionError(
                        f"causal replay identity mismatch for {review['sample_id']}: {failed}"
                    )
                track = track_by_key.get((component.label, selected_box))
                features.append(feature_row(
                    review, component, selected_box, result, stage_labels, track
                ))
                matched_ids.add(review["sample_id"])
    finally:
        capture.release()
    if decoded != frame_count:
        raise AssertionError("video was not decoded exactly once from frame zero")
    expected_ids = {
        row["sample_id"] for rows in review_by_frame.values() for row in rows
    }
    if matched_ids != expected_ids or len(features) != EXPECTED_ROWS:
        raise AssertionError("review/replay coverage is not 83/83")
    features.sort(key=lambda row: int(str(row["sample_id"])[2:]))
    return features, {
        "decoded_frames": decoded,
        "decoded_from_frame_zero": True,
        "single_decode_pass": True,
        "reviewed_candidates_matched": len(matched_ids),
        "reviewed_candidates_expected": EXPECTED_ROWS,
        "small_outputs_geometry_tracked": small_tracked,
        "geometry_tracks_created": tracker.next_id,
    }


def ablation(features: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    groups = ("all", "main_area_topk", "small_component_experimental")
    for policy in POLICIES:
        keep_field = f"diag_keep_{policy.removeprefix('small_')}"
        for branch in groups:
            for label in ("ped", "invalid", "rider"):
                population = [
                    row for row in features
                    if row["semantic_label"] == label
                    and (branch == "all" or row["branch"] == branch)
                ]
                retained = [row for row in population if row[keep_field] == "yes"]
                deleted = len(population) - len(retained)
                if branch == "main_area_topk" and deleted:
                    raise AssertionError(f"{policy} changed main branch")
                rows.append({
                    "policy": policy,
                    "scope": "small_only_no_box_change",
                    "branch": branch,
                    "semantic_label": label,
                    "before_count": len(population),
                    "retained_count": len(retained),
                    "deleted_count": deleted,
                    "retained_rate": "" if not population else fmt(len(retained) / len(population)),
                    "main_unchanged": (
                        "yes" if branch == "main_area_topk" else "not_applicable"
                    ),
                })
    return rows


def polarity_summary(features: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch in ("main_area_topk", "small_component_experimental"):
        for label in ("ped", "invalid", "rider"):
            group = [
                row for row in features
                if row["branch"] == branch and row["semantic_label"] == label
            ]
            if not group:
                continue
            means = [float(row["component_signed_gray_minus_background_mean"]) for row in group]
            positive = [float(row["component_signed_positive_fraction"]) for row in group]
            negative = [float(row["component_signed_negative_fraction"]) for row in group]
            rows.append({
                "branch": branch,
                "semantic_label": label,
                "count": len(group),
                "mean_signed_gray_minus_background": sum(means) / len(means),
                "mean_positive_fraction": sum(positive) / len(positive),
                "mean_negative_fraction": sum(negative) / len(negative),
                "filter_applied": False,
            })
    return rows


def decision_markdown(ablation_rows: Sequence[Mapping[str, Any]]) -> str:
    small = [row for row in ablation_rows if row["branch"] == "small_component_experimental"]
    lookup = {(row["policy"], row["semantic_label"]): row for row in small}
    lines = [
        "# VIRAT 010107 失败来源诊断",
        "",
        "本 sidecar 从第 0 帧单次因果重放，并完成 83/83 审核候选的身份、分支、组件标签和框映射核对。",
        "",
        "## 预注册小分支诊断",
        "",
    ]
    labels = (("ped", "行人"), ("invalid", "无效候选"), ("rider", "骑行者"))
    for policy in POLICIES:
        parts = []
        for key, title in labels:
            row = lookup[(policy, key)]
            parts.append(
                f"{title}保留 {row['retained_count']}/{row['before_count']}，删除 {row['deleted_count']}"
            )
        lines.append(f"- `{policy}`：" + "；".join(parts) + "。")
    lines.extend([
        "",
        "所有诊断仅作用于 small 分支并保持原框不变；main 分支逐项验证为全部保留。",
        "signed `gray-background` 极性只作为失败来源特征记录，没有参与筛选。",
        "这些结果是固定门槛的开发诊断，不是阈值搜索、模型训练或硬件改动依据。",
        "",
    ])
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    review = args.review.resolve()
    candidates = args.candidates.resolve()
    scene_report = args.scene_report.resolve()
    output = args.output.resolve()
    validation = validate_inputs(review, candidates, scene_report, output)
    review_headers, review_rows = read_csv(review)
    _, candidate_rows = read_csv(candidates)
    required_review = {
        "sample_id", "candidate_id", "frame_index", "slot", "branch",
        "component_label", "component_area", "component_peak_difference",
        "raw_analysis_box", "selected_analysis_box", "review_class",
        "semantic_subtype", "candidate_condition", "interval_id",
    }
    if not required_review.issubset(review_headers):
        raise ValueError(f"review manifest lacks fields: {sorted(required_review - set(review_headers))}")
    candidate_index = index_rows(candidate_rows, "candidate_id")
    review_by_frame = identity_assertions(review_rows, candidate_index)
    features, replay_receipt = replay(
        validation["video"], validation["report"], review_by_frame
    )
    ablation_rows = ablation(features)

    output.mkdir(parents=True, exist_ok=True)
    feature_path = output / "failure_source_features.csv"
    ablation_path = output / "ablation.csv"
    report_path = output / "report.json"
    decision_path = output / "DECISION.md"
    receipt_path = output / "receipt.json"
    feature_headers = list(features[0])
    ablation_headers = list(ablation_rows[0])
    write_csv(feature_path, feature_headers, features)
    write_csv(ablation_path, ablation_headers, ablation_rows)

    input_hashes = {
        "canonical_review_manifest.csv": sha256(review),
        "candidates.csv": sha256(candidates),
        "scene_report.json": sha256(scene_report),
        "scene_artifact_hashes.json": sha256(validation["artifact_hashes_path"]),
        "scene_receipt.json": sha256(validation["scene_receipt_path"]),
        "review_receipt.json": sha256(validation["review_receipt_path"]),
        "video": sha256(validation["video"]),
    }
    dependency_hashes = {
        str(path.relative_to(PROJECT)).replace("\\", "/"): sha256(path)
        for path in validation["dependency_paths"].values()
    }
    counts = {
        "reviewed_rows": len(features),
        "by_branch": dict(sorted(Counter(row["branch"] for row in features).items())),
        "by_semantic_label": dict(sorted(Counter(row["semantic_label"] for row in features).items())),
        "by_condition": dict(sorted(Counter(row["candidate_condition"] for row in features).items())),
    }
    report = {
        "schema": "virat_failure_source_analysis_v1",
        "scope": {
            "scene": validation["report"]["clip"]["clip_id"],
            "development_only": True,
            "annotations_accessed": False,
            "blind_holdout_or_test_accessed": False,
            "model_training_performed": False,
            "threshold_search_performed": False,
            "boxes_modified": False,
            "rtl_modified": False,
        },
        "inputs": {
            "paths": {
                "review": str(review),
                "candidates": str(candidates),
                "scene_report": str(scene_report),
                "video": str(validation["video"]),
            },
            "sha256": input_hashes,
            "dependency_sha256": dependency_hashes,
            "script_sha256": sha256(SCRIPT),
        },
        "identity_assertions": {
            "review_to_sealed_candidates": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_candidate_id": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_branch": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_component_label": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_raw_box": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "causal_replay_selected_box": f"{EXPECTED_ROWS}/{EXPECTED_ROWS}",
            "status": "pass",
        },
        "replay": replay_receipt,
        "feature_contract": {
            "signed_difference": "int16 gray-background before deployed post-frame background update",
            "absolute_difference": "uint8 abs(gray-background), threshold 20",
            "stages": ["raw threshold mask", "center-preserving 3x3 cleanup", "row min-run=2"],
            "stage_component_count": "8-connected nonzero labels intersecting the inclusive raw component bbox",
            "run_raw_survival": "run-filter mask pixels / raw-threshold mask pixels inside inclusive raw bbox",
            "geometry": "inclusive analysis-grid boxes; main is unexpanded; small uses sealed T100 expansion",
        },
        "causal_tracker_contract": {
            "population": "selected fill-only small outputs on every scored frame",
            "inputs": "raw component boxes and frame indices only; annotations and review labels are not used",
            "association": (
                "one-to-one greedy by IoU descending, center L1 distance ascending, gap ascending, "
                "track id then candidate order; eligible if gap<=5 and IoU>=0.3 or both center-axis deltas<=3"
            ),
            "recent_3_frame_hits": "current plus earlier hits in [frame-2, frame]",
            "recent_5_frame_hits": "current plus earlier hits in [frame-4, frame]",
            "causal_2_of_3": "keep small iff recent_3_frame_hits>=2",
        },
        "preregistered_diagnostics": {
            "small_run_raw_ge_0p5": "keep small iff run/raw survival >=0.5",
            "small_run_raw_ge_0p75": "keep small iff run/raw survival >=0.75",
            "small_causal_2_of_3": "keep small iff geometry track has >=2 hits in current 3-frame window",
            "shared_scope": "small branch only; main unchanged; boxes unchanged",
            "signed_polarity": "diagnostic only; no keep/drop rule",
        },
        "counts": counts,
        "ablation": ablation_rows,
        "signed_polarity_summary": polarity_summary(features),
        "limitations": [
            "The replay is algorithmic Python, not cycle-accurate RTL CCL or overflow timing.",
            "Human labels describe the 83 sampled review representatives, not all per-frame candidates.",
            "The geometry tracker is a diagnostic association and is not an object tracker or annotation match.",
            "Only the preregistered 0.5, 0.75 and 2-of-3 rules are evaluated; no optimum is selected.",
        ],
    }
    write_json(report_path, report)
    decision_path.write_text(decision_markdown(ablation_rows), encoding="utf-8")

    output_files = [feature_path, ablation_path, report_path, decision_path]
    artifact_hashes = {path.name: sha256(path) for path in output_files}
    receipt = {
        "schema": "virat_failure_source_receipt_v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script_sha256": sha256(SCRIPT),
        "input_hashes": input_hashes,
        "artifact_hashes": artifact_hashes,
        "receipt_self_hash_included": False,
        "assertions": {
            "reviewed_candidate_identity_83_of_83": True,
            "decoded_once_from_frame_zero": True,
            "main_unaffected_by_all_diagnostics": True,
            "signed_polarity_filter_applied": False,
            "threshold_search_performed": False,
            "annotation_accessed": False,
        },
    }
    write_json(receipt_path, receipt)
    parsed = json.loads(receipt_path.read_text(encoding="utf-8"))
    for name, expected in parsed["artifact_hashes"].items():
        if sha256(output / name) != expected:
            raise RuntimeError(f"artifact readback hash mismatch: {name}")
    if parsed["script_sha256"] != sha256(SCRIPT):
        raise RuntimeError("script readback hash mismatch")
    return {
        "output": str(output),
        "rows": len(features),
        "receipt_sha256": sha256(receipt_path),
        "artifact_hashes": artifact_hashes,
        "ablation": ablation_rows,
    }


def self_test() -> None:
    try:
        guard_path(Path("x/blind_reserve/y"))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("sealed path guard failed")
    assert parse_box("[1,2,3,4]") == (1, 2, 3, 4)
    assert box_area((1, 2, 3, 4)) == 9
    mask = np.zeros((6, 8), np.uint8)
    mask[1:3, 1:3] = 1
    mask[4, 6:8] = 1
    labels = labels_for(mask)
    assert intersecting_component_count(labels, (0, 0, 3, 3)) == 1
    assert intersecting_component_count(labels, (0, 0, 7, 5)) == 2

    tracker = GeometryTracker()
    first = tracker.update(10, [(10, 10, 12, 12)])[0]
    second = tracker.update(11, [(10, 10, 12, 12)])[0]
    third = tracker.update(13, [(11, 10, 13, 12)])[0]
    assert first["causal_recent_3_frame_hits"] == 1
    assert second["causal_recent_3_frame_hits"] == 2
    assert second["causal_consecutive_hits"] == 2
    assert third["causal_previous_gap_frames"] == 2
    assert third["causal_recent_3_frame_hits"] == 2
    assert third["causal_recent_5_frame_hits"] == 3
    assert first["causal_track_id"] == second["causal_track_id"] == third["causal_track_id"]

    fake = []
    for branch, label, keep in (
        ("main_area_topk", "ped", "yes"),
        ("small_component_experimental", "ped", "no"),
        ("small_component_experimental", "invalid", "yes"),
        ("small_component_experimental", "rider", "no"),
    ):
        fake.append({
            "branch": branch,
            "semantic_label": label,
            "diag_keep_run_raw_ge_0p5": keep,
            "diag_keep_run_raw_ge_0p75": keep,
            "diag_keep_causal_2_of_3": keep,
        })
    result = ablation(fake)
    main_rows = [row for row in result if row["branch"] == "main_area_topk"]
    assert all(row["deleted_count"] == 0 for row in main_rows)
    print("SELF_TEST PASS")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--scene-report", type=Path, default=DEFAULT_REPORT)
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
