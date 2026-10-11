#!/usr/bin/env python3
"""Compare Python candidate boxes/areas with an existing RTL replay receipt."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(python_summary: Path, rtl_objects: Path,
            frame_manifest: Path | None = None) -> dict[str, object]:
    summary = json.loads(python_summary.read_text(encoding="utf-8"))
    with rtl_objects.open(encoding="utf-8-sig", newline="") as handle:
        rtl_rows = list(csv.DictReader(handle))
    summary_frames = summary["frames"]
    processed = int(summary["processed_frames"])
    source_to_replay = None
    if frame_manifest is not None:
        manifest = json.loads(frame_manifest.read_text(encoding="utf-8"))
        source_to_replay = {int(row["source_frame"]): int(row["replay_frame"])
                            for row in manifest["frame_map"]}
        if sorted(source_to_replay.values()) != list(range(len(source_to_replay))):
            raise ValueError("frame manifest replay ids must be contiguous from zero")
        summary_frames = [frame for frame in summary_frames
                          if int(frame["frame_index"]) in source_to_replay]
        if len(summary_frames) != len(source_to_replay):
            raise ValueError("Python summary does not cover every frame in the replay manifest")
        processed = len(source_to_replay)
    rtl_frames = sorted({int(row["frame"]) for row in rtl_rows})
    if rtl_frames != list(range(processed)):
        raise ValueError("RTL objects receipt does not cover every Python replay frame")

    python_candidates = {
        ((source_to_replay[int(frame["frame_index"])] if source_to_replay is not None
          else int(frame["frame_index"])), slot): {
            key: int(candidate[key]) for key in ("xmin", "ymin", "xmax", "ymax", "area")}
        for frame in summary_frames
        for slot, candidate in enumerate(frame["candidates"])
    }
    rtl_candidates = {
        (int(row["frame"]), int(row["slot"])): {
            key: int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax", "area")}
        for row in rtl_rows if row["valid"] == "1"
    }
    mismatches = []
    for key in sorted(set(python_candidates) | set(rtl_candidates)):
        if python_candidates.get(key) != rtl_candidates.get(key):
            mismatches.append({
                "replay_frame": key[0], "slot": key[1],
                "python": python_candidates.get(key), "rtl": rtl_candidates.get(key),
            })
    return {
        "status": "pass_exact_bbox_and_area" if not mismatches else "mismatch",
        "processed_frames": processed,
        "python_candidate_count": len(python_candidates),
        "rtl_candidate_count": len(rtl_candidates),
        "exact_match_count": len(set(python_candidates) | set(rtl_candidates)) - len(mismatches),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "python_summary": str(python_summary.resolve()),
        "python_summary_sha256": digest(python_summary),
        "rtl_objects": str(rtl_objects.resolve()),
        "rtl_objects_sha256": digest(rtl_objects),
        "frame_manifest_sha256": digest(frame_manifest) if frame_manifest is not None else None,
        "boundary": (
            "This proves ordered top-four bbox and area agreement for these replay frames. "
            "It does not prove cycle-level internal label equivalence, MAX_RUN/MAX_LABEL overflow "
            "behavior, classifier correctness, continuous-capture throughput, or CDC safety."),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-summary", type=Path, required=True)
    parser.add_argument("--rtl-objects", type=Path, required=True)
    parser.add_argument("--frame-manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare(args.python_summary, args.rtl_objects, args.frame_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "status", "processed_frames", "python_candidate_count", "rtl_candidate_count",
        "exact_match_count", "mismatch_count")}, indent=2))
    if result["mismatch_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
