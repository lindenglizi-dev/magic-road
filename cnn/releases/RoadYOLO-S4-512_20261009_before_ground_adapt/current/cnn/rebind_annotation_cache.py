"""Create a read-only annotation/subset view over an immutable RGB cache."""
from __future__ import annotations

import argparse
import gc
import json
import os
from pathlib import Path
import shutil
import time

import cv2
import numpy as np
import torch

try:
    from . import disk_cache
    from .disk_cache import (CONTRACT, SHAPE, SUBSET_LAYOUT,
                             DiskCachedDataset, _validated_cache, fingerprint,
                             preprocessing_identity)
    from .train import (FullFrameDataset, dataset_content_hash,
                        load_dataset_manifest, sha256)
except ImportError:  # python cnn/rebind_annotation_cache.py
    import disk_cache
    from disk_cache import (CONTRACT, SHAPE, SUBSET_LAYOUT,
                            DiskCachedDataset, _validated_cache, fingerprint,
                            preprocessing_identity)
    from train import (FullFrameDataset, dataset_content_hash,
                       load_dataset_manifest, sha256)


def _receipt(value: str, name: str) -> str:
    value = value.lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be an exact SHA-256 receipt")
    return value


def _row_key(row: dict) -> tuple[str, str]:
    image = Path(row["image"])
    if not image.is_absolute():
        raise ValueError("annotation rebind requires absolute image paths")
    return os.path.normcase(str(image.resolve())), row["image_sha256"]


def _unchanged_source_identity(old: dict, new: dict) -> bool:
    return all(old.get(field) == new.get(field) for field in
               ("split", "preprocess", "scene_id", "source_frame", "source_sha256",
                "teacher_key"))


def _source_identity(row: dict) -> dict:
    return {field: row.get(field) for field in
            ("split", "preprocess", "scene_id", "source_frame", "source_sha256",
             "teacher_key")}


def _unpublished_cached_dataset(rows: list[dict], split: str, root: Path,
                                entries: list[dict]) -> DiskCachedDataset:
    """Use the production cache loader before index.json makes the view readable."""
    dataset = object.__new__(DiskCachedDataset)
    FullFrameDataset.__init__(dataset, rows, split)
    dataset.root = root
    dataset.entries = [entry for row, entry in zip(rows, entries, strict=True)
                       if row["split"] == split]
    return dataset


def rebind_annotation_cache(old_manifest: Path, old_cache: Path, new_manifest: Path,
                            new_cache: Path, report: Path, *,
                            old_manifest_sha256: str, old_index_sha256: str,
                            new_manifest_sha256: str) -> dict:
    """Validate all inputs on CPU, then publish only a new index and hard link."""
    old_manifest, old_cache, new_manifest, new_cache, report = map(
        lambda path: Path(path).resolve(),
        (old_manifest, old_cache, new_manifest, new_cache, report))
    expected_old_manifest = _receipt(old_manifest_sha256, "old manifest hash")
    expected_old_index = _receipt(old_index_sha256, "old cache index hash")
    expected_new_manifest = _receipt(new_manifest_sha256, "new manifest hash")
    if new_cache.exists():
        raise FileExistsError(new_cache)
    if report.exists() or report.with_suffix(report.suffix + ".pending").exists():
        raise FileExistsError(report)
    if torch.cuda.is_initialized():
        raise RuntimeError("annotation cache rebind must start without CUDA initialization")

    started = time.perf_counter()
    code_sha256_before = {
        "rebind_source_sha256": sha256(Path(__file__)),
        "disk_cache_source_sha256": sha256(Path(disk_cache.__file__)),
    }
    old_index_path = old_cache / "index.json"
    old_blob = old_cache / "rgb.bin"
    if sha256(old_manifest) != expected_old_manifest:
        raise ValueError("old manifest SHA-256 receipt mismatch")
    if sha256(new_manifest) != expected_new_manifest:
        raise ValueError("new manifest SHA-256 receipt mismatch")
    if sha256(old_index_path) != expected_old_index:
        raise ValueError("old cache index SHA-256 receipt mismatch")
    old_index = json.loads(old_index_path.read_text(encoding="utf-8"))
    if old_index.get("storage_layout") is not None:
        raise ValueError("annotation rebind source must be a legacy contiguous cache")
    del old_index

    free_before = shutil.disk_usage(new_cache.parent).free
    new_cache.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    new_cache.mkdir()
    pending_index = new_cache / "index.pending.json"
    pending_report = report.with_suffix(report.suffix + ".pending")
    pending_index.write_text('{"status":"verification_in_progress_not_published"}\n',
                             encoding="utf-8")
    pending_report.write_text('{"status":"verification_in_progress_not_published"}\n',
                              encoding="utf-8")
    new_blob = new_cache / "rgb.bin"
    os.link(old_blob, new_blob)
    if not os.path.samefile(old_blob, new_blob):
        raise ValueError("new RGB blob is not a hard link to the original")

    torch.set_num_threads(2)
    cv2.setNumThreads(2)
    identity = preprocessing_identity()
    old_payload, old_rows = load_dataset_manifest(old_manifest)
    del old_payload
    _, old_metadata, old_entries, _ = _validated_cache(
        old_rows, expected_old_manifest, dataset_content_hash(old_rows), old_cache,
        expected_old_index, verify_sources=True)
    if old_metadata["preprocessing"] != identity:
        raise ValueError("old cache preprocessing identity is not current")
    blob_sha256_before = sha256(old_blob)
    old_by_key = {}
    for row, entry in zip(old_rows, old_entries, strict=True):
        key = _row_key(row)
        if key in old_by_key:
            raise ValueError("old manifest has a duplicate absolute image/SHA identity")
        old_by_key[key] = (_source_identity(row), entry)
    old_row_count = len(old_rows)
    del old_rows
    gc.collect()

    new_payload, new_rows = load_dataset_manifest(new_manifest)
    del new_payload
    if len(new_rows) > old_row_count:
        raise ValueError("new manifest is not a subset of the old manifest")

    selected = []
    seen = set()
    for row in new_rows:
        key = _row_key(row)
        if key in seen:
            raise ValueError("new manifest has a duplicate absolute image/SHA identity")
        seen.add(key)
        source = old_by_key.get(key)
        if source is None:
            raise ValueError("new manifest row is not present in the old cache source")
        old_identity, old_entry = source
        if not _unchanged_source_identity(old_identity, row):
            raise ValueError("split or source/preprocess identity changed during annotation rebind")
        selected.append((row, old_entry))

    entries = [{
        "image": row["image"],
        "row_sha256": fingerprint(row),
        "source_sha256": row["image_sha256"],
        "offset": old_entry["offset"],
        "rgb_sha256": old_entry["rgb_sha256"],
    } for row, old_entry in selected]
    raw = {split: FullFrameDataset(new_rows, split) for split in ("train", "val")}
    cached = {split: _unpublished_cached_dataset(new_rows, split, new_cache, entries)
              for split in ("train", "val")}
    checks = []
    verified = 0
    for split in ("train", "val"):
        for index in range(len(raw[split])):
            raw_item = raw[split]._load(index)
            cached_item = cached[split]._load(index)
            if (raw_item[0].shape != SHAPE or raw_item[0].dtype != np.uint8
                    or not np.array_equal(raw_item[0], cached_item[0])):
                raise AssertionError(f"current raw RGB differs at {split} row {index}")
            for field in ("boxes", "labels", "ignore_boxes"):
                torch.testing.assert_close(raw_item[1][field], cached_item[1][field],
                                           rtol=0, atol=0)
            if raw_item[2] != cached_item[2]:
                raise AssertionError(f"teacher key differs at {split} row {index}")
            verified += 1
            if verified % 1000 == 0 or verified == len(entries):
                print(f"verify records {verified}/{len(entries)} "
                      f"{time.perf_counter() - started:.1f}s", flush=True)
        checks.append({
            "split": split,
            "kind": "all_raw_RGB_new_targets_and_teacher_keys_via_DiskCachedDataset_load",
            "count": len(raw[split]),
            "maximum_compared_difference": 0,
        })

    source_hashes = {
        "old_manifest_sha256": sha256(old_manifest),
        "old_cache_index_sha256": sha256(old_index_path),
        "old_rgb_sha256": sha256(old_blob),
        "new_manifest_sha256": sha256(new_manifest),
        **code_sha256_before,
    }
    if (source_hashes["old_manifest_sha256"] != expected_old_manifest
            or source_hashes["old_cache_index_sha256"] != expected_old_index
            or source_hashes["old_rgb_sha256"] != blob_sha256_before
            or source_hashes["new_manifest_sha256"] != expected_new_manifest
            or preprocessing_identity() != identity
            or torch.cuda.is_initialized()):
        raise ValueError("manifest, cache, blob, code identity, or CPU-only state changed")

    metadata = {
        "contract": CONTRACT,
        "status": "complete",
        "storage_layout": SUBSET_LAYOUT,
        "dataset_sha256": expected_new_manifest,
        "dataset_content_sha256": dataset_content_hash(new_rows),
        "preprocessing": identity,
        "entries": entries,
        "logical_record_count": len(entries),
        "rgb_bytes": old_metadata["rgb_bytes"],
        "rgb_sha256": old_metadata["rgb_sha256"],
        "physical_storage": {
            "record_count": len(old_entries),
            "rgb_bytes": old_metadata["rgb_bytes"],
            "rgb_sha256": old_metadata["rgb_sha256"],
            "origin_cache_root": str(old_cache),
            "origin_cache_index_sha256": expected_old_index,
            "origin_manifest": str(old_manifest),
            "origin_manifest_sha256": expected_old_manifest,
            "origin_dataset_content_sha256": old_metadata["dataset_content_sha256"],
        },
        "rebind": {
            "kind": "annotation_only_subset_zero_copy",
            "source_sha256": source_hashes,
            "excluded_records": len(old_entries) - len(entries),
            "new_targets_compared_to_old": False,
            "new_targets_compared_between_raw_and_cache": True,
        },
    }
    with pending_index.open("w", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    index_sha256 = sha256(pending_index)
    index_bytes = pending_index.stat().st_size
    free_after = shutil.disk_usage(new_cache.parent).free
    result = {
        "schema": "road_yolo_annotation_cache_rebind_receipt_v1",
        "status": "passed_annotation_only_subset_cache_rebind_CPU_equivalence",
        "cache_index_sha256": index_sha256,
        "dataset_sha256": expected_new_manifest,
        "dataset_content_sha256": metadata["dataset_content_sha256"],
        "old_cache_index_sha256": expected_old_index,
        "rgb_sha256": old_metadata["rgb_sha256"],
        "logical_records": len(entries),
        "physical_records": len(old_entries),
        "excluded_records": len(old_entries) - len(entries),
        "physical_rgb_bytes": old_metadata["rgb_bytes"],
        "additional_rgb_payload_bytes": 0,
        "new_index_bytes": index_bytes,
        "measured_free_space_delta_bytes": max(0, free_before - free_after),
        "hardlink_same_file": os.path.samefile(old_blob, new_blob),
        "hardlink_warning": "Both cache paths share immutable rgb.bin bytes; never modify either in place.",
        "source_sha256_before_publish": source_hashes,
        "checks": checks,
        "maximum_compared_difference": 0,
        "device": "cpu",
        "cpu_threads": 2,
        "gpu_used": False,
        "training_started": False,
        "optimizer_updates": 0,
        "accuracy_measured": False,
        "verification_seconds": time.perf_counter() - started,
        "limitation": "Cache/input equivalence only; no GPU training, accuracy, newtest, or FPGA evidence.",
    }
    with pending_report.open("w", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    if (sha256(old_manifest) != expected_old_manifest
            or sha256(old_index_path) != expected_old_index
            or sha256(old_blob) != blob_sha256_before
            or sha256(new_manifest) != expected_new_manifest
            or sha256(Path(__file__)) != source_hashes["rebind_source_sha256"]
            or sha256(Path(disk_cache.__file__)) != source_hashes["disk_cache_source_sha256"]
            or preprocessing_identity() != identity
            or not os.path.samefile(old_blob, new_blob)):
        raise ValueError("bound input changed before publication")
    pending_index.rename(new_cache / "index.json")
    pending_report.rename(report)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-manifest", type=Path, required=True)
    parser.add_argument("--old-manifest-sha256", required=True)
    parser.add_argument("--old-cache", type=Path, required=True)
    parser.add_argument("--old-index-sha256", required=True)
    parser.add_argument("--new-manifest", type=Path, required=True)
    parser.add_argument("--new-manifest-sha256", required=True)
    parser.add_argument("--new-cache", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rebind_annotation_cache(
        args.old_manifest, args.old_cache, args.new_manifest, args.new_cache, args.report,
        old_manifest_sha256=args.old_manifest_sha256,
        old_index_sha256=args.old_index_sha256,
        new_manifest_sha256=args.new_manifest_sha256)


if __name__ == "__main__":
    main()
