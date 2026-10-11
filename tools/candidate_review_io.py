"""Fail-closed loading for reviewed CCL candidate sets."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


KNOWN_LABELS = {"ped", "vehicle", "invalid", "ignore"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_reviewed(candidate_root: Path, reviewed_path: Path, expected_split: str,
                  frame_root: Path | None = None) -> tuple[list[dict], dict]:
    candidate_root = candidate_root.resolve()
    reviewed_path = reviewed_path.resolve()
    if not reviewed_path.is_relative_to(candidate_root):
        raise ValueError("reviewed CSV must reside under its candidate root")
    provenance_path = candidate_root / "provenance.json"
    candidates_path = candidate_root / "candidates.csv"
    if not provenance_path.is_file() or not candidates_path.is_file():
        raise ValueError("candidate root lacks provenance.json or candidates.csv")
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if provenance.get("split") != expected_split:
        raise ValueError(
            f"candidate split {provenance.get('split')!r} does not match {expected_split!r}")
    with candidates_path.open(encoding="utf-8-sig", newline="") as handle:
        originals = {row["candidate_id"]: row for row in csv.DictReader(handle)}
    with reviewed_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or len({row["candidate_id"] for row in rows}) != len(rows):
        raise ValueError("reviewed candidates must be nonempty with unique ids")
    reviewed_ids = {row["candidate_id"] for row in rows}
    if reviewed_ids != set(originals):
        missing = sorted(set(originals) - reviewed_ids)
        extra = sorted(reviewed_ids - set(originals))
        raise ValueError(
            f"reviewed CSV must cover the complete candidate set; missing={missing}, extra={extra}")

    frame_map = None
    manifest_path = None
    if frame_root is not None:
        manifest_path = frame_root.resolve() / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("source_sha256") != provenance.get("source_sha256"):
            raise ValueError("frame manifest and candidate provenance source hashes differ")
        frame_map = {str(row["replay_frame"]): str(row["source_frame"])
                     for row in manifest["frame_map"]}

    immutable = ("replay_frame", "source_frame", "xmin", "ymin", "xmax", "ymax",
                 "geometry_class", "roi_path", "roi_sha256")
    for row in rows:
        candidate_id = row["candidate_id"]
        if candidate_id not in originals:
            raise ValueError(f"reviewed row has unknown candidate id: {candidate_id}")
        original = originals[candidate_id]
        if any(row.get(field) != original.get(field) for field in immutable):
            raise ValueError(f"reviewed row changed immutable candidate data: {candidate_id}")
        if row.get("label") not in KNOWN_LABELS:
            raise ValueError(f"reviewed row has invalid label: {candidate_id}")
        if frame_map is not None and frame_map.get(row["replay_frame"]) != row["source_frame"]:
            raise ValueError(f"reviewed row conflicts with frame manifest: {candidate_id}")
        roi_path = candidate_root / row["roi_path"]
        with Image.open(roi_path) as image:
            pixel_hash = hashlib.sha256(np.asarray(image.convert("L"), dtype=np.uint8).tobytes()).hexdigest()
        if pixel_hash != row["roi_sha256"]:
            raise ValueError(f"reviewed ROI pixel hash mismatch: {candidate_id}")
    receipt = {
        "candidate_root": str(candidate_root),
        "scene_id": provenance.get("scene_id"),
        "split": provenance["split"],
        "source_sha256": provenance.get("source_sha256"),
        "candidate_count": len(rows),
        "provenance_sha256": digest(provenance_path),
        "candidates_sha256": digest(candidates_path),
        "reviewed_sha256": digest(reviewed_path),
        "frame_manifest_sha256": digest(manifest_path) if manifest_path else None,
    }
    return rows, receipt
