"""Small CPU regressions for annotation-only zero-copy cache views."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from .disk_cache import (DiskCachedDataset, RECORD_BYTES, assert_item_equal,
                         build_cache)
from .rebind_annotation_cache import rebind_annotation_cache
from .train import FullFrameDataset, load_dataset_manifest, sha256


class RebindAnnotationCacheTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        images = []
        for index in range(4):
            y, x = np.indices((288, 512))
            rgb = np.stack(((x + index) % 256, (y * 3 + index) % 256,
                            (x + y * 2 + index) % 256), axis=-1).astype(np.uint8)
            image = (self.root / f"image{index}.png").resolve()
            cv2.imwrite(str(image), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            images.append({
                "image": str(image),
                "boxes": [[10, 20, 30, 40]],
                "labels": [index % 2],
                "ignore_boxes": [],
                "scene_id": f"scene{index}",
                "split": "val" if index == 3 else "train",
                "source_sha256": sha256(image),
                "source_frame": index,
                "annotation_complete": True,
                "incomplete_frame": False,
                "preprocess": {"raw_image": True},
            })
        self.old_payload = {
            "schema_version": 1,
            "task": "detection",
            "input_size": [512, 288],
            "classes": ["person", "vehicle"],
            "training_eligible": True,
            "images": images,
        }
        self.old_manifest = self.root / "old.json"
        self.old_manifest.write_text(json.dumps(self.old_payload), encoding="utf-8")
        _, rows = load_dataset_manifest(self.old_manifest)
        self.old_cache = self.root / "old_cache"
        with patch("cnn.disk_cache.shutil.disk_usage") as usage:
            usage.return_value.free = 50 * (1 << 30)
            build_cache(self.old_manifest, rows, self.old_cache)

        self.new_payload = deepcopy(self.old_payload)
        del self.new_payload["images"][1]
        self.new_payload["images"][0]["boxes"] = []
        self.new_payload["images"][0]["labels"] = []
        self.new_payload["images"][0]["manual_review"] = {"decision": "delete_label"}
        self.new_manifest = self.root / "new.json"
        self.new_manifest.write_text(json.dumps(self.new_payload), encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def _rebind(self, name="view"):
        cache, report = self.root / name, self.root / f"{name}.json"
        result = rebind_annotation_cache(
            self.old_manifest, self.old_cache, self.new_manifest, cache, report,
            old_manifest_sha256=sha256(self.old_manifest),
            old_index_sha256=sha256(self.old_cache / "index.json"),
            new_manifest_sha256=sha256(self.new_manifest))
        return cache, report, result

    def _assert_view_rejected(self, cache, mutate, pattern):
        index_path = cache / "index.json"
        metadata = json.loads(index_path.read_text(encoding="utf-8"))
        mutate(metadata)
        index_path.write_text(json.dumps(metadata), encoding="utf-8")
        _, rows = load_dataset_manifest(self.new_manifest)
        with self.assertRaisesRegex(ValueError, pattern):
            DiskCachedDataset(rows, "train", self.new_manifest, cache,
                              expected_index_sha256=sha256(index_path))

    def test_deleted_annotation_and_subset_rebind_without_copy(self):
        cache, report, result = self._rebind()
        self.assertEqual(result["schema"], "road_yolo_annotation_cache_rebind_receipt_v1")
        self.assertEqual(result["logical_records"], 3)
        self.assertEqual(result["physical_records"], 4)
        self.assertEqual(result["excluded_records"], 1)
        self.assertEqual(result["additional_rgb_payload_bytes"], 0)
        self.assertEqual([check["count"] for check in result["checks"]], [2, 1])
        self.assertEqual(result["optimizer_updates"], 0)
        self.assertTrue((cache / "rgb.bin").samefile(self.old_cache / "rgb.bin"))
        self.assertTrue(report.is_file())
        _, rows = load_dataset_manifest(self.new_manifest)
        raw = FullFrameDataset(rows, "train")
        cached = DiskCachedDataset(rows, "train", self.new_manifest, cache,
                                   expected_index_sha256=result["cache_index_sha256"])
        np.testing.assert_array_equal(raw._load(0)[0], cached._load(0)[0])
        self.assertEqual(cached._load(0)[1]["labels"].numel(), 0)
        for split in ("train", "val"):
            raw = FullFrameDataset(rows, split)
            cached = DiskCachedDataset(rows, split, self.new_manifest, cache,
                                       expected_index_sha256=result["cache_index_sha256"])
            for index in range(len(raw)):
                assert_item_equal(raw[index], cached[index])

    def test_changed_preprocess_is_rejected_and_unpublished(self):
        self.new_payload["images"][0]["preprocess"] = {"raw_image": False}
        self.new_manifest.write_text(json.dumps(self.new_payload), encoding="utf-8")
        cache = self.root / "bad_preprocess"
        with self.assertRaisesRegex(ValueError, "source/preprocess identity"):
            self._rebind("bad_preprocess")
        self.assertTrue((cache / "index.pending.json").is_file())
        self.assertFalse((cache / "index.json").exists())

    def test_row_fingerprint_is_not_relaxed(self):
        cache, _, _ = self._rebind()
        self._assert_view_rejected(
            cache, lambda data: data["entries"][0].__setitem__("row_sha256", "0" * 64),
            "stale source, row, or cache offset")

    def test_duplicate_boolean_and_out_of_bounds_offsets_are_rejected(self):
        def swap_records(data):
            first, second = data["entries"][:2]
            first["offset"], second["offset"] = second["offset"], first["offset"]
            first["rgb_sha256"], second["rgb_sha256"] = (
                second["rgb_sha256"], first["rgb_sha256"])

        mutations = {
            "duplicate": lambda data: data["entries"][1].__setitem__(
                "offset", data["entries"][0]["offset"]),
            "boolean": lambda data: data["entries"][0].__setitem__("offset", True),
            "out_of_bounds": lambda data: data["entries"][0].__setitem__(
                "offset", data["rgb_bytes"]),
            "wrong_origin_record": swap_records,
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                cache, _, _ = self._rebind(name)
                self._assert_view_rejected(cache, mutate, "cache offset")

    def test_wrong_origin_index_hash_is_rejected(self):
        cache, _, _ = self._rebind()
        self._assert_view_rejected(
            cache,
            lambda data: data["physical_storage"].__setitem__(
                "origin_cache_index_sha256", "0" * 64),
            "stale subset cache origin")

    def test_changed_raw_source_leaves_only_pending_output(self):
        image = Path(self.old_payload["images"][0]["image"])
        pixels = cv2.imread(str(image), cv2.IMREAD_COLOR)
        pixels[0, 0] ^= 1
        cv2.imwrite(str(image), pixels)
        cache = self.root / "changed_raw"
        with self.assertRaises(ValueError):
            self._rebind("changed_raw")
        self.assertTrue((cache / "index.pending.json").is_file())
        self.assertFalse((cache / "index.json").exists())

    def test_corrupt_blob_leaves_only_pending_output(self):
        blob = self.old_cache / "rgb.bin"
        with blob.open("r+b") as stream:
            stream.seek(RECORD_BYTES)
            byte = stream.read(1)
            stream.seek(RECORD_BYTES)
            stream.write(bytes([byte[0] ^ 1]))
        cache = self.root / "corrupt_blob"
        with self.assertRaisesRegex(ValueError, "corrupt cache data"):
            self._rebind("corrupt_blob")
        self.assertTrue((cache / "index.pending.json").is_file())
        self.assertFalse((cache / "index.json").exists())

    def test_legacy_layout_still_requires_contiguous_offsets(self):
        _, rows = load_dataset_manifest(self.old_manifest)
        DiskCachedDataset(rows, "train", self.old_manifest, self.old_cache,
                          expected_index_sha256=sha256(self.old_cache / "index.json"))
        index_path = self.old_cache / "index.json"
        metadata = json.loads(index_path.read_text(encoding="utf-8"))
        metadata["entries"][1]["offset"] += RECORD_BYTES
        index_path.write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "cache offset"):
            DiskCachedDataset(rows, "train", self.old_manifest, self.old_cache,
                              expected_index_sha256=sha256(index_path))

    def test_missing_labels_is_rejected(self):
        del self.new_payload["images"][0]["labels"]
        self.new_manifest.write_text(json.dumps(self.new_payload), encoding="utf-8")
        with self.assertRaises((KeyError, ValueError)):
            self._rebind("missing_labels")


if __name__ == "__main__":
    unittest.main()
