"""Build and exhaustively verify the pinned 103-frame QAT cache on CPU."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import torch

from cnn.disk_cache import assert_item_equal, build_cache, open_validated_cache
from cnn.train import load_dataset_snapshot, make_frame_dataset, sha256


DATASET = ROOT / "cnn/reports/ac_optimization_20261013_v1/trial/dataset.json"
EXPECTED_DATASET_SHA256 = "5b25180c25d1f3835ea5248b107f19d2fc39cfac166500c45c87c2dfde08fd59"
OUTPUT = Path(__file__).resolve().parent
CACHE = OUTPUT / "cache"
RECEIPT = OUTPUT / "cache_receipt.json"
SOURCE_FILES = (
    ROOT / "cnn/disk_cache.py",
    ROOT / "cnn/train.py",
    ROOT / "cnn/dataset.py",
    ROOT / "cnn/integer.py",
    Path(__file__).resolve(),
)


def main() -> None:
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise ValueError("CUDA_VISIBLE_DEVICES must be empty for this CPU-only task")
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise ValueError("PYTHONDONTWRITEBYTECODE=1 is required")
    if CACHE.exists() or RECEIPT.exists():
        raise FileExistsError("cache and receipt are exclusive immutable outputs")

    staging_parent = os.environ.get("CACHE_STAGING_PARENT")
    build_root = (Path(staging_parent).resolve() / "qat_g10_20261013_v1_cache_build"
                  if staging_parent else CACHE)
    if build_root.exists():
        raise FileExistsError(f"exclusive cache staging path exists: {build_root}")

    torch.set_num_threads(2)
    _, snapshot = load_dataset_snapshot(DATASET)
    counts = {split: sum(row["split"] == split for row in snapshot.rows)
              for split in ("train", "val")}
    if (snapshot.manifest_sha256 != EXPECTED_DATASET_SHA256
            or len(snapshot.rows) != 103 or counts != {"train": 86, "val": 17}):
        raise ValueError("pinned dataset identity or split counts changed")

    metadata = build_cache(DATASET, snapshot.rows, build_root)
    if build_root != CACHE:
        shutil.move(str(build_root), str(CACHE))
    index_sha256 = sha256(CACHE / "index.json")
    binding = open_validated_cache(snapshot, CACHE, index_sha256)
    checks = []
    for split in ("train", "val"):
        raw = make_frame_dataset(snapshot.rows, split, DATASET)
        disk = make_frame_dataset(
            snapshot.rows,
            split,
            DATASET,
            cache_root=CACHE,
            cache_index_sha256=index_sha256,
            cache_binding=binding,
        )
        for index in range(len(raw)):
            assert_item_equal(raw[index], disk[index])
        checks.append({
            "name": "raw_vs_disk_exact",
            "split": split,
            "count": len(raw),
            "fields": ["centered_input", "boxes", "labels", "ignore_boxes", "key"],
            "maximum_compared_difference": 0,
            "status": "passed",
        })

    receipt = {
        "schema_version": 1,
        "passed": True,
        "status": "passed_exact_CPU_cache_compatibility",
        "dataset": str(DATASET.resolve()),
        "dataset_sha256": snapshot.manifest_sha256,
        "dataset_content_sha256": snapshot.dataset_content_sha256,
        "cache_root": str(CACHE.resolve()),
        "cache_index_sha256": index_sha256,
        "rgb_sha256": metadata["rgb_sha256"],
        "cached_images": len(snapshot.rows),
        "split_counts": counts,
        "cache_bytes": metadata["rgb_bytes"],
        "checks": checks,
        "cache_binding": "open_validated_cache passed index, RGB blob, manifest, content, rows, sources, and preprocessing identity",
        "source_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                           for path in SOURCE_FILES},
        "preprocessing": metadata["preprocessing"],
        "existing_cache_search": {
            "indexes_checked": 15,
            "exact_dataset_sha256_matches": 0,
            "exact_dataset_content_sha256_matches": 0,
        },
        "device": "cpu",
        "cpu_threads": 2,
        "gpu_used": False,
        "training_started": False,
        "staging_used": build_root != CACHE,
        "note": "No exact compatible existing index was found; created a new approximately 46 MB compatibility cache. Older caches were preserved.",
    }
    with RECEIPT.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
