"""Rebind an immutable road RGB cache after a train-only source change.

The old cache is never modified.  Every record is compared with the current
raw loader on CPU before a hard-linked blob and new index are published.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import time

import cv2
import numpy as np
import torch

try:
    from .disk_cache import (CONTRACT, RECORD_BYTES, SHAPE, assert_item_equal,
                             fingerprint, preprocessing_identity)
    from .train import (FullFrameDataset, dataset_content_hash, load_dataset_manifest,
                        reject_cache_qa, sha256)
except ImportError:  # python cnn/rebind_road_cache.py
    from disk_cache import (CONTRACT, RECORD_BYTES, SHAPE, assert_item_equal,
                            fingerprint, preprocessing_identity)
    from train import (FullFrameDataset, dataset_content_hash, load_dataset_manifest,
                       reject_cache_qa, sha256)


EXPECTED_OLD_INDEX_SHA256 = "646db6bcd11ab8ff55b9fb024480ab0b015842f7a9495a890a9b947aa153e170"
EXPECTED_MANIFEST_SHA256 = "ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4"
EXPECTED_RGB_SHA256 = "cb01e0c54596ab66e2418b926eabda2ce5236db41e082786355933f18bef1758"
EXPECTED_TRAIN_SHA256 = "adb634b9ae29b89c6dde782bc72e870069c267e1090372ad2466c1a599ee17dc"
EXPECTED_RECORDS = 24_201
SOURCE_NAMES = {"disk_cache.py", "train.py", "dataset.py", "integer.py"}


class ExistingBlobDataset(FullFrameDataset):
    """Current target/Mosaic behavior backed by the already-verified old blob."""

    def __init__(self, rows, split, blob, entries, *, mosaic=False, seed=42):
        super().__init__(rows, split, mosaic=mosaic, seed=seed)
        self.blob = blob
        self.entries = [entry for row, entry in zip(rows, entries, strict=True)
                        if row["split"] == split]

    def _load(self, index):
        entry, row = self.entries[index], self.rows[index]
        with self.blob.open("rb") as stream:
            stream.seek(entry["offset"])
            encoded = stream.read(RECORD_BYTES)
        if (len(encoded) != RECORD_BYTES
                or hashlib.sha256(encoded).hexdigest() != entry["rgb_sha256"]):
            raise ValueError("missing or corrupt original RGB cache record")
        target = {
            "boxes": torch.tensor(row["boxes"], dtype=torch.float32).reshape(-1, 4),
            "labels": torch.tensor(row["labels"], dtype=torch.long),
            "ignore_boxes": torch.tensor(row["ignore_boxes"], dtype=torch.float32).reshape(-1, 4),
        }
        pixels = np.frombuffer(encoded, np.uint8).reshape(SHAPE).copy()
        return pixels, target, row["teacher_key"]


def _assert_target_key(raw_item, row):
    expected = {
        "boxes": torch.tensor(row["boxes"], dtype=torch.float32).reshape(-1, 4),
        "labels": torch.tensor(row["labels"], dtype=torch.long),
        "ignore_boxes": torch.tensor(row["ignore_boxes"], dtype=torch.float32).reshape(-1, 4),
    }
    for field, value in expected.items():
        torch.testing.assert_close(raw_item[1][field], value, rtol=0, atol=0)
    if raw_item[2] != row["teacher_key"]:
        raise AssertionError("teacher key differs from the shared row contract")


def rebind_cache(manifest: Path, old_root: Path, new_root: Path, output: Path, *,
                 expected_old_index_sha256: str = EXPECTED_OLD_INDEX_SHA256,
                 expected_manifest_sha256: str = EXPECTED_MANIFEST_SHA256,
                 expected_rgb_sha256: str = EXPECTED_RGB_SHA256,
                 expected_train_sha256: str = EXPECTED_TRAIN_SHA256,
                 expected_records: int = EXPECTED_RECORDS) -> dict:
    if new_root.exists():
        raise FileExistsError(new_root)
    if output.exists():
        raise FileExistsError(output)
    output_pending = output.with_suffix(output.suffix + ".pending")
    if output_pending.exists():
        raise FileExistsError(output_pending)
    if torch.cuda.is_initialized():
        raise RuntimeError("cache rebind must start without CUDA initialization")

    started = time.perf_counter()
    old_index_path = old_root / "index.json"
    old_blob = old_root / "rgb.bin"
    old_index_bytes = old_index_path.read_bytes()
    old_index_sha256 = hashlib.sha256(old_index_bytes).hexdigest()
    if old_index_sha256 != expected_old_index_sha256:
        raise ValueError("original cache index SHA-256 receipt mismatch")
    manifest_sha256 = sha256(manifest)
    if manifest_sha256 != expected_manifest_sha256:
        raise ValueError("dataset manifest SHA-256 receipt mismatch")

    declared = json.loads(manifest.read_text(encoding="utf-8"))
    reject_cache_qa(declared)
    if (len(declared.get("images", [])) != expected_records
            or any(row.get("split") not in ("train", "val") for row in declared["images"])):
        raise ValueError("rebind requires the complete development manifest; no newtest/cache QA")

    old_metadata = json.loads(old_index_bytes)
    entries = old_metadata.get("entries", [])
    if (old_metadata.get("contract") != CONTRACT or old_metadata.get("status") != "complete"
            or old_metadata.get("dataset_sha256") != manifest_sha256
            or len(entries) != expected_records
            or old_metadata.get("rgb_bytes") != expected_records * RECORD_BYTES
            or old_metadata.get("rgb_sha256") != expected_rgb_sha256
            or old_blob.stat().st_size != old_metadata["rgb_bytes"]):
        raise ValueError("original cache metadata, size, or RGB receipt mismatch")

    identity_before = preprocessing_identity()
    if identity_before["source_sha256"].get("train.py") != expected_train_sha256:
        raise ValueError("current train.py SHA-256 is not the approved pause patch")
    old_identity = old_metadata.get("preprocessing", {})
    old_sources = old_identity.get("source_sha256", {})
    current_sources = identity_before["source_sha256"]
    if set(old_sources) != SOURCE_NAMES or set(current_sources) != SOURCE_NAMES:
        raise ValueError("unexpected preprocessor source identity set")
    if old_sources["train.py"] == current_sources["train.py"]:
        raise ValueError("rebind requires a changed train.py identity")
    if any(old_sources[name] != current_sources[name]
           for name in SOURCE_NAMES - {"train.py"}):
        raise ValueError("a preprocessor source other than train.py changed")
    if ({key: value for key, value in old_identity.items() if key != "source_sha256"}
            != {key: value for key, value in identity_before.items() if key != "source_sha256"}):
        raise ValueError("preprocessing contract or library identity changed")

    # Prove every required publication operation before the expensive pass.
    # A failed run may leave this directory, hard link, and pending files, but
    # readers still reject it because index.json is deliberately absent.
    new_root.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    new_root.mkdir()
    new_blob = new_root / "rgb.bin"
    os.link(old_blob, new_blob)
    if (not os.path.samefile(old_blob, new_blob)
            or new_blob.stat().st_size != old_metadata["rgb_bytes"]):
        raise ValueError("new RGB blob is not an exact hard link to the original")
    pending = new_root / "index.pending.json"
    with pending.open("xb") as stream:
        stream.flush()
        os.fsync(stream.fileno())
    with output_pending.open("x", encoding="utf-8") as stream:
        json.dump({"status": "verification_in_progress_not_published"}, stream)
        stream.flush()
        os.fsync(stream.fileno())

    torch.set_num_threads(2)
    cv2.setNumThreads(2)
    _, rows = load_dataset_manifest(manifest)
    if (len(rows) != expected_records
            or dataset_content_hash(rows) != old_metadata.get("dataset_content_sha256")):
        raise ValueError("normalized dataset content differs from the original cache")

    raw = {split: FullFrameDataset(rows, split) for split in ("train", "val")}
    local_index = {"train": 0, "val": 0}
    rgb_digest = hashlib.sha256()
    verified = 0
    with old_blob.open("rb") as stream:
        for global_index, (row, entry) in enumerate(zip(rows, entries, strict=True)):
            if (entry.get("image") != row["image"]
                    or entry.get("offset") != global_index * RECORD_BYTES
                    or entry.get("row_sha256") != fingerprint(row)
                    or entry.get("source_sha256") != row["image_sha256"]):
                raise ValueError(f"original cache row mismatch at {global_index}")
            encoded = stream.read(RECORD_BYTES)
            if (len(encoded) != RECORD_BYTES
                    or hashlib.sha256(encoded).hexdigest() != entry.get("rgb_sha256")):
                raise ValueError(f"original RGB record mismatch at {global_index}")
            index = local_index[row["split"]]
            raw_item = raw[row["split"]]._load(index)
            local_index[row["split"]] += 1
            if (raw_item[0].shape != SHAPE or raw_item[0].dtype != np.uint8
                    or not np.array_equal(raw_item[0], np.frombuffer(encoded, np.uint8).reshape(SHAPE))):
                raise AssertionError(f"current raw RGB differs at {global_index}")
            _assert_target_key(raw_item, row)
            rgb_digest.update(encoded)
            verified += 1
            if verified % 1000 == 0 or verified == expected_records:
                print(f"verify records {verified}/{expected_records} "
                      f"{time.perf_counter() - started:.1f}s", flush=True)
        if stream.read(1):
            raise ValueError("original RGB blob has trailing bytes")
    if rgb_digest.hexdigest() != expected_rgb_sha256:
        raise ValueError("whole RGB SHA-256 mismatch after the one-pass comparison")

    mosaic_checks = []
    raw_train = FullFrameDataset(rows, "train", mosaic=True, seed=42)
    cached_train = ExistingBlobDataset(rows, "train", old_blob, entries, mosaic=True, seed=42)
    indices = np.linspace(0, len(raw_train) - 1, min(32, len(raw_train)), dtype=int)
    for epoch in (0, 1):
        raw_train.set_epoch(epoch, True)
        cached_train.set_epoch(epoch, True)
        for index in indices:
            assert_item_equal(raw_train[int(index)], cached_train[int(index)])
        mosaic_checks.append(dict(epoch=epoch, count=len(indices), kind="bounded_exact_Mosaic"))

    identity_after = preprocessing_identity()
    if (identity_after != identity_before or sha256(manifest) != manifest_sha256
            or hashlib.sha256(old_index_path.read_bytes()).hexdigest() != old_index_sha256
            or torch.cuda.is_initialized()):
        raise ValueError("source identity changed during CPU equivalence verification")

    if (not os.path.samefile(old_blob, new_blob)
            or new_blob.stat().st_size != old_metadata["rgb_bytes"]):
        raise ValueError("new RGB blob is not an exact hard link to the original")

    new_metadata = dict(old_metadata)
    new_metadata["preprocessing"] = identity_before
    new_metadata["rebind"] = {
        "old_cache_index_sha256": old_index_sha256,
        "migration_source_sha256": sha256(Path(__file__)),
        "verified_records": verified,
        "mosaic_checks": mosaic_checks,
        "rgb_storage": "windows_hardlink_same_file",
    }
    with pending.open("w", encoding="utf-8") as stream:
        json.dump(new_metadata, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    identity_pre_publish = preprocessing_identity()
    if (identity_pre_publish != identity_before or sha256(manifest) != manifest_sha256
            or hashlib.sha256(old_index_path.read_bytes()).hexdigest() != old_index_sha256):
        raise ValueError("identity changed before new index publication")
    pending.rename(new_root / "index.json")
    new_index_sha256 = sha256(new_root / "index.json")

    result = {
        "status": "passed_full_development_cache_rebind_CPU_equivalence",
        "old_cache_index_sha256": old_index_sha256,
        "cache_index_sha256": new_index_sha256,
        "dataset_sha256": manifest_sha256,
        "dataset_content_sha256": old_metadata["dataset_content_sha256"],
        "rgb_sha256": expected_rgb_sha256,
        "preprocessing": identity_before,
        "preprocessing_after": identity_pre_publish,
        "cached_images": verified,
        "cache_bytes": old_metadata["rgb_bytes"],
        "maximum_compared_difference": 0,
        "checks": [
            {"kind": "all_raw_RGB_targets_and_keys", "count": verified},
            *mosaic_checks,
            {"kind": "hardlink_same_file", "count": 1},
        ],
        "old_cache_preserved": True,
        "rgb_storage": "windows_hardlink_no_duplicate_payload",
        "source_files_before_after_equal": identity_before == identity_pre_publish,
        "device": "cpu",
        "cpu_threads": 2,
        "gpu_used": False,
        "training_started": False,
        "verification_seconds": time.perf_counter() - started,
        "limitation": "CPU cache equivalence only; no GPU training, accuracy, newtest, or FPGA evidence.",
    }
    with output_pending.open("w", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    output_pending.rename(output)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path,
                        default=root / "data" / "visdrone_vid_train" / "raw_manifest" / "dataset.json")
    parser.add_argument("--old-cache", type=Path,
                        default=root / "data" / "cache_road_full_development_20261003")
    parser.add_argument("--new-cache", type=Path,
                        default=root / "data" / "cache_road_pause_20261003")
    parser.add_argument("--output", type=Path,
                        default=root / "reports" / "cache_road_pause_rebind_20261003.json")
    args = parser.parse_args()
    rebind_cache(args.dataset.resolve(), args.old_cache.resolve(),
                 args.new_cache.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
