#!/usr/bin/env python3
"""Fixed-mask software audit, NOT a video replay or RTL-equivalent model.

Compares the declared current minimum run length against keeping all runs.
Uses OpenCV 8-connected components as an independent partition reference.
See README_zh.md for input contracts and interpretation boundaries.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np


def require_binary(mask: np.ndarray) -> np.ndarray:
    if mask.ndim != 2 or not all(mask.shape):
        raise ValueError("Each mask must be a nonempty two-dimensional array")
    if not np.isin(mask, [0, 1, 255]).all():
        raise ValueError("Masks may contain only 0, 1, 255; resolve shadow/unknown values explicitly")
    return np.ascontiguousarray(mask != 0, dtype=np.uint8)


def row_runs(row: np.ndarray) -> list[tuple[int, int]]:
    """Inclusive start and end coordinates."""
    padded = np.pad(row.astype(np.int8), (1, 1))
    edges = np.diff(padded)
    return [(int(a), int(b) - 1) for a, b in zip(np.flatnonzero(edges == 1),
                                               np.flatnonzero(edges == -1))]


def keep_runs(mask: np.ndarray, minimum: int) -> tuple[np.ndarray, int, int]:
    if minimum < 1:
        raise ValueError("Minimum run length must be positive")
    out = np.zeros_like(mask)
    peak = total = 0
    for y, row in enumerate(mask):
        runs = [(a, b) for a, b in row_runs(row) if b - a + 1 >= minimum]
        peak = max(peak, len(runs))
        total += len(runs)
        for a, b in runs:
            out[y, a:b + 1] = 1
    return out, peak, total


def rle_partition(mask: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Independent unlimited-storage run reference. Merged IDs are not recycled.

    Allocates only if a run touches no run from the previous row. Unions
    distinct roots of every overlap. This allocation policy is explicit,
    and is not assumed identical to the user's software or RTL.
    """
    parent = [0]
    labels = np.zeros(mask.shape, dtype=np.int32)
    previous: list[tuple[int, int, int]] = []
    unions = bridges = 0

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for y, row in enumerate(mask):
        current: list[tuple[int, int, int]] = []
        j = 0
        for a, b in row_runs(row):
            while j < len(previous) and previous[j][1] < a - 1:
                j += 1
            roots: set[int] = set()
            k = j
            while k < len(previous) and previous[k][0] <= b + 1:
                roots.add(find(previous[k][2]))
                k += 1
            if not roots:
                root = len(parent)
                parent.append(root)
            else:
                root = min(roots)
                if len(roots) > 1:
                    bridges += 1
                for other in roots:
                    if other != root:
                        parent[other] = root
                        unions += 1
            labels[y, a:b + 1] = root
            current.append((a, b, root))
        previous = current
    lookup = np.array([find(x) for x in range(len(parent))], dtype=np.int32)
    return lookup[labels], {"reference_labels_allocated": len(parent) - 1,
                            "reference_union_operations": unions,
                            "reference_multi_root_bridge_runs": bridges}


def canonical(labels: np.ndarray) -> np.ndarray:
    """Canonicalize by first raster occurrence; numeric label IDs are arbitrary."""
    values, first = np.unique(labels, return_index=True)
    ordered = values[np.argsort(first)]
    ordered = ordered[ordered != 0]
    lut = np.zeros(int(labels.max()) + 1, dtype=np.int32)
    for i, value in enumerate(ordered, 1):
        lut[int(value)] = i
    return lut[labels]


def iou(a: list[float], b: list[float]) -> float:
    w = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = w * h
    union = ((a[2] - a[0]) * (a[3] - a[1]) +
             (b[2] - b[0]) * (b[3] - b[1]) - intersection)
    return intersection / union if union > 0 else 0.0


def match_report(boxes: list[list[int]], objects: list[dict[str, Any]],
                 threshold: float = 0.5) -> dict[str, Any]:
    """Maximum-cardinality, class-blind, one-to-one matching at IoU >= threshold.

    Ties are deterministic but may differ from another evaluator. Reports
    explicitly list the assignment. This is not classification accuracy.
    """
    scores = [[iou(obj["bbox_xyxy"], box) for box in boxes] for obj in objects]
    edges = [sorted((j for j, score in enumerate(row) if score >= threshold),
                    key=lambda j: (-row[j], j)) for row in scores]
    owners: dict[int, int] = {}

    def augment(i: int, seen: set[int]) -> bool:
        for j in edges[i]:
            if j in seen:
                continue
            seen.add(j)
            if j not in owners or augment(owners[j], seen):
                owners[j] = i
                return True
        return False

    for i in range(len(objects)):
        augment(i, set())
    by_gt = {i: j for j, i in owners.items()}
    per_object = []
    classes: dict[str, dict[str, int]] = {}
    for i, obj in enumerate(objects):
        category = obj["class"]
        counts = classes.setdefault(category, {"matched": 0, "total": 0})
        counts["total"] += 1
        counts["matched"] += int(i in by_gt)
        per_object.append({"id": obj["id"], "class": category,
                           "max_iou": max(scores[i], default=0.0),
                           "matched_candidate_index": by_gt.get(i)})
    return {"iou_threshold": threshold, "matched": len(owners),
            "total": len(objects), "by_class": classes, "objects": per_object}


def audit_mask(mask: np.ndarray, minimum: int, min_area: int, top_k: int,
               usable_labels: int | None, run_capacity: int | None,
               objects: list[dict[str, Any]] | None) -> dict[str, Any]:
    mask = require_binary(mask)
    filtered, run_peak, run_total = keep_runs(mask, minimum)
    ours, demand = rle_partition(filtered)
    n, reference, stats, _ = cv2.connectedComponentsWithStats(
        filtered, connectivity=8, ltype=cv2.CV_32S)
    partition_ok = bool(np.array_equal(canonical(ours), canonical(reference)))
    if not partition_ok:
        raise RuntimeError("Independent RLE/OpenCV partition mismatch: stop interpreting results")
    components = []
    for label in range(1, n):
        x, y, w, h, area = map(int, stats[label])
        components.append({"area": area, "bbox_xyxy": [x, y, x + w, y + h]})
    # Stable explicitly declared area ordering; not assumed equal to production tie-breaks.
    components.sort(key=lambda c: (-c["area"], c["bbox_xyxy"][1],
                                   c["bbox_xyxy"][0], c["bbox_xyxy"][3],
                                   c["bbox_xyxy"][2]))
    qualified = [c for c in components if c["area"] >= min_area]
    top = qualified[:top_k]
    reasons = []
    if usable_labels is not None and demand["reference_labels_allocated"] > usable_labels:
        reasons.append("reference_label_budget_exceeded")
    if run_capacity is not None and run_peak > run_capacity:
        reasons.append("reference_row_run_budget_exceeded")
    # None means the full two-capacity predicate cannot be evaluated.
    known_failure: bool | None = bool(reasons) if reasons else (
        False if usable_labels is not None and run_capacity is not None else None)
    result: dict[str, Any] = {
        "minimum_run": minimum, "foreground_pixels_before_run_filter": int(mask.sum()),
        "foreground_pixels_after_run_filter": int(filtered.sum()),
        "row_run_peak_after_filter": run_peak, "total_runs_after_filter": run_total,
        **demand, "reference_component_count": n - 1,
        "reference_rle_opencv_partition_equal": partition_ok,
        "area_qualified_candidate_count": len(qualified),
        "top_k_candidate_count": len(top), "capacity_proxy_failure": known_failure,
        "capacity_proxy_reasons": reasons,
        "components_before_area_filter": components,
        "area_qualified_candidates": qualified, "top_k_candidates": top,
    }
    if objects is not None:
        result["proposal_matching"] = {
            "before_area_filter": match_report([c["bbox_xyxy"] for c in components], objects),
            "area_qualified": match_report([c["bbox_xyxy"] for c in qualified], objects),
            "top_k": match_report([c["bbox_xyxy"] for c in top], objects),
            "capacity_adjusted_top_k": None if known_failure is None else match_report(
                [] if known_failure else [c["bbox_xyxy"] for c in top], objects),
        }
    return result


def load_annotations(path: Path | None) -> dict[int, dict[str, Any]] | None:
    if path is None:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("coordinate_convention") != "xyxy_half_open_in_mask_pixels":
        raise ValueError("Annotation coordinate convention must be xyxy_half_open_in_mask_pixels")
    frames: dict[int, dict[str, Any]] = {}
    for frame in data["frames"]:
        fid = frame["frame_id"]
        if type(fid) is not int or fid < 0 or fid in frames:
            raise ValueError("Annotation frame IDs must be unique nonnegative integers")
        h, w = frame["height"], frame["width"]
        if type(h) is not int or type(w) is not int or min(h, w) < 1:
            raise ValueError("Invalid annotation dimensions")
        ids: set[str] = set()
        for obj in frame["objects"]:
            if not isinstance(obj["id"], str) or not obj["id"] or obj["id"] in ids:
                raise ValueError("Each object's string ID must be unique within the frame")
            ids.add(obj["id"])
            if not isinstance(obj["class"], str) or not obj["class"]:
                raise ValueError("Object class must be explicitly supplied; no class remapping")
            box = np.asarray(obj["bbox_xyxy"], dtype=float)
            if box.shape != (4,) or not np.isfinite(box).all():
                raise ValueError("Invalid bbox")
            obj["bbox_xyxy"] = box.tolist()
            if obj.get("ignore", False) or obj.get("iscrowd", False):
                raise ValueError("Ignore/crowd objects need the project evaluator; do not silently include them")
            x0, y0, x1, y1 = box
            if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
                raise ValueError("BBox outside declared mask coordinates")
        frames[fid] = frame
    return frames


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mask-dir", required=True, type=Path)
    p.add_argument("--input-stage", required=True, choices=["after_cleanup_before_min_run"])
    p.add_argument("--current-min-run", required=True, type=int)
    p.add_argument("--min-area", required=True, type=int)
    p.add_argument("--top-k", type=int, default=4)
    p.add_argument("--usable-labels", type=int, default=None,
                   help="Foreground labels actually usable, excluding reserved IDs; omitted = unknown")
    p.add_argument("--run-capacity", type=int, default=None)
    p.add_argument("--annotations", type=Path)
    p.add_argument("--start-frame", type=int, default=120)
    p.add_argument("--end-frame", type=int, default=1079)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    for name in ("current_min_run", "min_area", "top_k", "usable_labels", "run_capacity"):
        value = getattr(args, name)
        if value is not None and value < 1:
            p.error(f"{name} must be positive")
    if args.start_frame < 0 or args.end_frame < args.start_frame:
        p.error("Invalid frame interval")
    if not args.mask_dir.is_dir():
        p.error("mask-dir must be an existing directory")
    if args.out.exists():
        p.error("Output already exists; choose a new path to preserve earlier evidence")
    entries: dict[int, Path] = {}
    for path in args.mask_dir.glob("*.npy"):
        m = re.fullmatch(r"(?:frame_)?(\d+)", path.stem)
        if m is None:
            p.error(f"Ambiguous frame filename: {path.name}; use frame_000120.npy")
        fid = int(m.group(1))
        if args.start_frame <= fid <= args.end_frame:
            if fid in entries:
                p.error(f"Duplicate frame ID: {fid}")
            entries[fid] = path
    if not entries:
        p.error("No masks in the requested interval")
    annotations = load_annotations(args.annotations)
    missing = sorted(set(range(args.start_frame, args.end_frame + 1)) - entries.keys())
    report: dict[str, Any] = {
        "status": "fixed_mask_software_diagnostic_not_video_replay",
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                     "opencv": cv2.__version__},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "declared_input_stage": args.input_stage,
        "input_provenance_verified": False,
        "requested_frame_interval": [args.start_frame, args.end_frame],
        "processed_frame_count": len(entries), "missing_frame_ids": missing,
        "settings": {k: getattr(args, k) for k in
                     ("current_min_run", "min_area", "top_k", "usable_labels", "run_capacity")},
        "matching_contract": "maximum cardinality; IoU >= 0.5; class blind; explicit deterministic ties",
        "annotation_sha256": hashlib.sha256(args.annotations.read_bytes()).hexdigest()
                             if args.annotations else None,
        "boundaries": ["Not RTL timing or overflow equivalence",
                       "Allocation policy and top-k tie-breaks may differ from production",
                       "Stored masks preserve original background history; no rollback counterfactual replay",
                       "No classifier, precision, FAR, recognition accuracy or safety acceptance claim",
                       "Reference RLE vs OpenCV checks this tool, not unavailable project source",
                       "Unannotated frames are not treated as empty scenes"],
        "frames": [],
    }
    for fid, path in sorted(entries.items()):
        mask = require_binary(np.load(path, allow_pickle=False))
        objects = None
        if annotations is not None and fid in annotations:
            frame = annotations[fid]
            if mask.shape != (frame["height"], frame["width"]):
                raise ValueError(f"Frame {fid}: mask/annotation dimensions differ")
            objects = frame["objects"]
        common = (args.min_area, args.top_k, args.usable_labels, args.run_capacity, objects)
        report["frames"].append({
            "frame_id": fid, "mask_path": str(path.resolve()),
            "mask_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "height": mask.shape[0], "width": mask.shape[1],
            "reference_current_min_run": audit_mask(mask, args.current_min_run, *common),
            "reference_keep_all_runs": audit_mask(mask, 1, *common),
        })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
    print(f"Audited {len(entries)} stored masks; missing in requested interval: {len(missing)}")
    print(f"Saved: {args.out}")
    print("This is not a causal video replay or measured improvement of the project.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
