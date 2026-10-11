"""Audit ROI pixels/provenance and summarize coverage without training a model."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from road_evaluation import audit_dataset


def summarize(root: Path) -> dict[str, object]:
    rows = audit_dataset(root)
    manifest = root / "manifest.csv"
    counts = lambda keys: {"/".join(key): value for key, value in sorted(Counter(
        tuple(row[field] for field in keys) for row in rows).items())}
    scene_splits = {}
    for row in rows:
        scene_splits.setdefault(row["scene_id"], set()).add(row["split"])
    return {
        "status": "pass",
        "checks": ["required provenance", "source hashes", "32x32 ROI pixels and hashes",
                   "scene/source-family/source-hash/pixel-hash split leakage", "label conflicts"],
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "sample_count": len(rows),
        "counts_by_split_label": counts(("split", "label")),
        "counts_by_split_roi_source": counts(("split", "roi_source")),
        "counts_by_scene": counts(("scene_id",)),
        "scene_splits": {scene: sorted(splits) for scene, splits in sorted(scene_splits.items())},
        "coverage": {
            "splits": sorted({row["split"] for row in rows}),
            "labels": sorted({row["label"] for row in rows}),
            "roi_sources": sorted({row["roi_source"] for row in rows}),
        },
        "readiness": {
            "fit_ready": all(any(row["split"] == split and row["label"] == label
                                 for row in rows)
                             for split in ("train", "val") for label in ("ped", "vehicle")),
            "invalid_evaluation_ready": any(row["label"] == "invalid" for row in rows),
            "test_present": any(row["split"] == "test" for row in rows),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(args.dataset.resolve())
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
