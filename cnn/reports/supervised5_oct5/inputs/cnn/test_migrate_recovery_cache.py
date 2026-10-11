"""Small CPU check for publish-once scoped-identity cache migration."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from .disk_cache import build_cache, open_validated_cache
from . import migrate_recovery_cache as migration
from .train import load_dataset_manifest, load_dataset_snapshot, sha256


class MigrateRecoveryCacheTest(unittest.TestCase):
    def test_hardlink_migration_uses_receipts_without_rereading_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            declared = []
            for index in range(2):
                rgb = np.full((32, 48, 3), (index + 1) * 40, dtype=np.uint8)
                image = root / f'{index}.png'
                cv2.imwrite(str(image), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                declared.append({
                    'image': image.name, 'boxes': [], 'labels': [], 'ignore_boxes': [],
                    'scene_id': f'scene{index}', 'split': 'train' if index == 0 else 'val',
                    'source_sha256': sha256(image), 'source_frame': index,
                    'annotation_complete': True, 'incomplete_frame': False,
                    'preprocess': {'raw_image': True},
                })
            manifest = root / 'dataset.json'
            manifest.write_text(json.dumps({
                'schema_version': 1, 'task': 'detection', 'input_size': [512, 288],
                'classes': ['person', 'vehicle'], 'training_eligible': True,
                'images': declared,
            }), encoding='utf-8')
            _, rows = load_dataset_manifest(manifest)
            old_root = root / 'old'
            with patch('cnn.disk_cache.shutil.disk_usage') as usage:
                usage.return_value.free = 50 * (1 << 30)
                metadata = build_cache(manifest, rows, old_root)
            full_receipt = root / 'full.json'
            full_receipt.write_text('{"status":"passed"}', encoding='utf-8')
            old_receipt = root / 'old.json'
            old_receipt.write_text(json.dumps({
                'cache_index_sha256': sha256(old_root / 'index.json'),
                'rgb_sha256': metadata['rgb_sha256'],
                'inherited_full_parity_receipt_sha256': sha256(full_receipt),
            }), encoding='utf-8')
            baseline = Path(__file__).parent / 'artifacts/recovery_source_baseline_20261003.json'
            new_root, output = root / 'new', root / 'migration.json'
            seen = []
            real_sha256 = migration.sha256
            with (patch.object(migration, 'OLD_INDEX_SHA256', sha256(old_root / 'index.json')),
                  patch.object(migration, 'OLD_RECEIPT_SHA256', sha256(old_receipt)),
                  patch.object(migration, 'FULL_PARITY_RECEIPT_SHA256', sha256(full_receipt)),
                  patch.object(migration, 'BASELINE_SHA256', sha256(baseline)),
                  patch.object(migration, 'RGB_SHA256', metadata['rgb_sha256']),
                  patch.object(migration, 'sha256', side_effect=lambda path: (
                      seen.append(Path(path).resolve()), real_sha256(path))[1])):
                result = migration.migrate_cache(
                    manifest, old_root, old_receipt, full_receipt, baseline,
                    new_root, output)
            self.assertEqual(result['status'],
                             'passed_scoped_preprocessing_identity_migration_no_pixel_reread')
            self.assertNotIn((old_root / 'rgb.bin').resolve(), seen)
            self.assertTrue(os.path.samefile(old_root / 'rgb.bin', new_root / 'rgb.bin'))
            self.assertEqual(result['cached_images'], 2)
            self.assertTrue(output.is_file())
            _, snapshot = load_dataset_snapshot(manifest)
            binding = open_validated_cache(snapshot, new_root, result['cache_index_sha256'])
            self.assertIs(binding.snapshot.rows, snapshot.rows)


if __name__ == '__main__':
    unittest.main()
