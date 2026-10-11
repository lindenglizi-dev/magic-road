"""Small CPU test for fail-closed cache rebinding and hard-link publication."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from .disk_cache import DiskCachedDataset, assert_item_equal, build_cache, preprocessing_identity
from .rebind_road_cache import rebind_cache
from .train import FullFrameDataset, load_dataset_manifest, sha256


class RebindRoadCacheTest(unittest.TestCase):
    def test_exact_rebind_uses_hardlink_and_preserves_old_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            declared = []
            for index in range(4):
                y, x = np.indices((48 + index, 80 - index))
                rgb = np.stack(((x + 13 * index) % 256, (3 * y) % 256,
                                (2 * x + 5 * y) % 256), axis=-1).astype(np.uint8)
                image = root / f"{index}.png"
                cv2.imwrite(str(image), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                declared.append({
                    "image": image.name,
                    "boxes": [] if index == 0 else [[1, 2, 50, 80]],
                    "labels": [] if index == 0 else [index % 2],
                    "ignore_boxes": [[100, 80, 160, 100]],
                    "scene_id": f"scene{index}",
                    "split": "val" if index == 3 else "train",
                    "source_sha256": sha256(image),
                    "source_frame": index,
                    "annotation_complete": True,
                    "incomplete_frame": False,
                    "preprocess": {"raw_image": True},
                })
            manifest = root / "dataset.json"
            manifest.write_text(json.dumps({
                "schema_version": 1, "task": "detection", "input_size": [512, 288],
                "classes": ["person", "vehicle"], "training_eligible": True,
                "images": declared,
            }), encoding="utf-8")
            _, rows = load_dataset_manifest(manifest)
            old_root = root / "old"
            with patch("cnn.disk_cache.shutil.disk_usage") as usage:
                usage.return_value.free = 50 * (1 << 30)
                metadata = build_cache(manifest, rows, old_root)

            old_index = json.loads((old_root / "index.json").read_text(encoding="utf-8"))
            old_index["preprocessing"]["source_sha256"]["train.py"] = "0" * 64
            (old_root / "index.json").write_text(json.dumps(old_index, indent=2), encoding="utf-8")
            old_index_bytes = (old_root / "index.json").read_bytes()
            old_index_sha256 = sha256(old_root / "index.json")
            current_train_sha256 = preprocessing_identity()["source_sha256"]["train.py"]

            with self.assertRaisesRegex(ValueError, "index SHA-256"):
                rebind_cache(manifest, old_root, root / "bad", root / "bad.json",
                             expected_old_index_sha256="f" * 64,
                             expected_manifest_sha256=sha256(manifest),
                             expected_rgb_sha256=metadata["rgb_sha256"],
                             expected_train_sha256=current_train_sha256, expected_records=4)
            self.assertFalse((root / "bad").exists())

            new_root, report = root / "new", root / "receipt.json"
            result = rebind_cache(
                manifest, old_root, new_root, report,
                expected_old_index_sha256=old_index_sha256,
                expected_manifest_sha256=sha256(manifest),
                expected_rgb_sha256=metadata["rgb_sha256"],
                expected_train_sha256=current_train_sha256, expected_records=4)
            self.assertEqual(result["status"],
                             "passed_full_development_cache_rebind_CPU_equivalence")
            self.assertEqual((old_root / "index.json").read_bytes(), old_index_bytes)
            self.assertTrue(os.path.samefile(old_root / "rgb.bin", new_root / "rgb.bin"))
            self.assertEqual(result["maximum_compared_difference"], 0)
            raw = FullFrameDataset(rows, "train")
            cached = DiskCachedDataset(rows, "train", manifest, new_root,
                                       expected_index_sha256=result["cache_index_sha256"])
            assert_item_equal(raw[0], cached[0])
            self.assertTrue(report.is_file())


if __name__ == "__main__":
    unittest.main()
