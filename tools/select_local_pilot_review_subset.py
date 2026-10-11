#!/usr/bin/env python3
"""Select a model-blind, time-stratified local-pilot review subset."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


HUMAN_FIELDS = (
    "review_class", "semantic_subtype", "candidate_condition", "crop_usable",
    "reviewer", "reviewed_at", "review_note",
)
TIME_BINS = ((120, 439), (440, 759), (760, 1079))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def resize(image: np.ndarray, width: int, height: int) -> np.ndarray:
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--per-bin", default=20, type=int)
    args = parser.parse_args()
    pilot = args.pilot.resolve()
    output = args.output.resolve()
    source = pilot / "review_manifest.csv"
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")
    rows = read_csv(source)
    if any(row[field] for row in rows for field in HUMAN_FIELDS):
        raise ValueError("source human fields must remain blank")

    selected: list[dict[str, str]] = []
    bin_receipts = []
    for bin_index, (start, end) in enumerate(TIME_BINS):
        eligible = [row for row in rows if start <= int(row["frame_index"]) <= end]
        # Retain one representative per geometry track in each time bin.  The
        # deterministic SHA-256 rank depends only on identity, never on scores.
        by_track: dict[str, dict[str, str]] = {}
        for row in eligible:
            track = row["geometry_track_id"]
            rank = hashlib.sha256(row["candidate_id"].encode("utf-8")).hexdigest()
            previous = by_track.get(track)
            if previous is None or rank < previous["selection_rank_sha256"]:
                candidate = dict(row)
                candidate["selection_rank_sha256"] = rank
                by_track[track] = candidate
        chosen = sorted(by_track.values(), key=lambda item: item["selection_rank_sha256"])
        if len(chosen) < args.per_bin:
            raise ValueError(f"time bin {bin_index} has only {len(chosen)} unique tracks")
        for row in chosen[:args.per_bin]:
            row["review_subset_id"] = f"local60_{len(selected):03d}"
            row["selection_time_bin"] = f"f{start}_{end}"
            selected.append(row)
        bin_receipts.append({"frame_range_inclusive": [start, end],
                             "eligible_representatives": len(eligible),
                             "eligible_unique_tracks": len(by_track),
                             "selected": args.per_bin})

    # Put stable audit columns first while preserving every source field.
    ordered = []
    for row in selected:
        ordered.append({
            "review_subset_id": row.pop("review_subset_id"),
            "selection_time_bin": row.pop("selection_time_bin"),
            "selection_rank_sha256": row.pop("selection_rank_sha256"),
            **row,
        })
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / "review_manifest.csv"
    write_csv(manifest, ordered)

    sheets = []
    for sheet_number, offset in enumerate(range(0, len(ordered), 4), 1):
        canvas = np.full((940, 2040, 3), 245, np.uint8)
        page = ordered[offset:offset + 4]
        for local_index, row in enumerate(page):
            panel = cv2.imread(str(pilot / row["review_panel_path"]), cv2.IMREAD_COLOR)
            if panel is None:
                raise ValueError(f"cannot read panel for {row['sample_id']}")
            panel = resize(panel, 1000, 450)
            y, x = divmod(local_index, 2)
            left, top = 20 + x * 1010, 20 + y * 460
            canvas[top:top + 450, left:left + 1000] = panel
            cv2.putText(canvas, row["review_subset_id"], (left + 8, top + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, .65, (0, 0, 255), 2, cv2.LINE_AA)
        path = output / f"contact_sheet_{sheet_number:02d}.jpg"
        if not cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 92]):
            raise ValueError(f"cannot write {path}")
        sheets.append({"path": path.name, "sha256": digest(path),
                       "review_subset_ids": [row["review_subset_id"] for row in page]})

    report = {
        "schema": "local_pilot_model_blind_review_subset_v1",
        "source_manifest": str(source),
        "source_manifest_sha256": digest(source),
        "selection_policy": (
            "three fixed 320-frame bins; one source representative per geometry track per bin; "
            "rank by SHA256(candidate_id); first 20 per bin; no score or prediction used"
        ),
        "time_bins": bin_receipts,
        "selected_count": len(ordered),
        "human_fields_blank": list(HUMAN_FIELDS),
        "manifest_sha256": digest(manifest),
        "contact_sheets": sheets,
        "metric_boundary": (
            "Candidate-level review sample only; it cannot measure full-frame target misses or "
            "end-to-end recall without independent target annotations."
        ),
    }
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"selected_count": len(ordered), "output": str(output)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
