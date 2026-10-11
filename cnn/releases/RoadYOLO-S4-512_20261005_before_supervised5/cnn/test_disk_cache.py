"""One runnable CPU check: exact cache behavior and fail-closed boundaries."""
import json
from argparse import Namespace
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from . import disk_cache
from .disk_cache import (DiskCachedDataset, assert_item_equal, build_cache,
                         build_full_development, open_validated_cache,
                         preprocessing_identity)
from .train import (FullFrameDataset, load_dataset_manifest, load_dataset_snapshot,
                    make_frame_dataset, sha256)
from .evaluate import load_validation_subset
from .prepare_cache_pilot import select_pilot


class DiskCacheTest(unittest.TestCase):
    def test_exact_inputs_and_reject_stale_or_corrupt_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            # Unequal color lanes and aspect ratios exercise RGB and letterboxing.
            for index, shape in enumerate(((39, 91), (91, 39), (72, 128), (57, 67))):
                y, x = np.indices(shape)
                rgb = np.stack(((x + index * 17) % 256, (y * 3) % 256,
                                (x * 2 + y * 5) % 256), axis=-1).astype(np.uint8)
                path = root / f'{index}.png'
                cv2.imwrite(str(path), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                rows.append(dict(image=path.name, boxes=[] if index == 0 else [[1, 2, 50, 80]],
                                 labels=[] if index == 0 else [index % 2],
                                 ignore_boxes=[[100, 80, 160, 100]],
                                 ignore_metadata=[dict(label=-1, crowd=False)],
                                 scene_id=f'scene{index}', split='val' if index == 3 else 'train',
                                 source_sha256=sha256(path), source_frame=index,
                                 annotation_complete=True, incomplete_frame=False,
                                 preprocess=dict(raw_image=True)))
            manifest = root / 'dataset.json'
            manifest.write_text(json.dumps(dict(schema_version=1, task='detection',
                                               input_size=[512, 288], classes=['person', 'vehicle'],
                                               training_eligible=True, images=rows)), encoding='utf-8')
            _, rows = load_dataset_manifest(manifest)
            document = json.loads(manifest.read_text(encoding='utf-8'))
            selected = select_pilot(document, manifest, 2, 1)
            self.assertEqual([Path(row['image']).name for row in selected['images']],
                             ['0.png', '1.png', '3.png'])
            self.assertEqual(selected['images'][1]['boxes'], document['images'][1]['boxes'])
            self.assertEqual(selected['images'][1]['ignore_metadata'],
                             document['images'][1]['ignore_metadata'])
            with self.assertRaisesRegex(ValueError, 'development-only'):
                select_pilot(dict(document, images=[dict(document['images'][0], split='newtest')]),
                             manifest, 1, 1)
            cache_root = root / 'cache'
            with patch('cnn.disk_cache.shutil.disk_usage') as usage:
                usage.return_value.free = 50 * (1 << 30)
                build_cache(manifest, rows, cache_root)
            command = [sys.executable, '-B', '-m', 'cnn.train', '--dataset', str(manifest),
                       '--output', str(root / 'unused_run'), '--device', 'cpu', '--workers', '0',
                       '--input-cache', str(cache_root), '--input-cache-index-sha256',
                       sha256(cache_root / 'index.json'), '--validate-only']
            process = subprocess.run(command, capture_output=True, text=True, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            _, snapshot = load_dataset_snapshot(manifest)
            seen = []
            real_sha256 = disk_cache.sha256
            with patch('cnn.disk_cache.sha256', side_effect=lambda path: (
                    seen.append(Path(path).resolve()), real_sha256(path))[1]):
                binding = open_validated_cache(
                    snapshot, cache_root, sha256(cache_root / 'index.json'))
                for split in ('train', 'val'):
                    DiskCachedDataset(snapshot.rows, split, manifest, cache_root,
                                      binding=binding)
            self.assertEqual(seen.count((cache_root / 'rgb.bin').resolve()), 1)
            self.assertFalse(any(row['image_path'].resolve() in seen for row in snapshot.rows))
            with self.assertRaisesRegex(ValueError, 'binding does not match'):
                DiskCachedDataset(list(snapshot.rows), 'train', manifest, cache_root,
                                  binding=binding)
            plain = make_frame_dataset(rows, 'train', manifest)
            self.assertEqual(type(plain), FullFrameDataset)
            pinned = make_frame_dataset(rows, 'train', manifest, cache_root=cache_root,
                                        cache_index_sha256=sha256(cache_root / 'index.json'))
            assert_item_equal(plain[0], pinned[0])
            with self.assertRaisesRegex(ValueError, 'supplied together'):
                make_frame_dataset(rows, 'train', manifest, cache_root=cache_root)
            with self.assertRaisesRegex(ValueError, 'receipt mismatch'):
                make_frame_dataset(rows, 'train', manifest, cache_root=cache_root,
                                   cache_index_sha256='0' * 64)
            qa = dict(document, manifest_status='development_cache_pilot',
                      purpose='CPU_disk_cache_QA_only_not_accuracy_or_training')
            qa_path = root / 'qa.json'
            qa_path.write_text(json.dumps(qa), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'cache QA manifest'):
                load_dataset_manifest(qa_path)
            with self.assertRaisesRegex(ValueError, 'cache QA manifest'):
                load_validation_subset(qa_path, None, 2)
            self.assertEqual(len(load_dataset_manifest(qa_path, allow_cache_qa=True)[1]), 4)
            with patch('cnn.disk_cache.MAX_PILOT_IMAGES', 3):
                with self.assertRaisesRegex(ValueError, 'at most128'):
                    build_cache(manifest, rows, root / 'too_large')
                with patch('cnn.disk_cache.shutil.disk_usage') as usage:
                    usage.return_value.free = 50 * (1 << 30)
                    build_cache(manifest, rows, root / 'full', full_development=True)
            assert_item_equal(plain[0], DiskCachedDataset(rows, 'train', manifest, root / 'full')[0])
            with self.assertRaisesRegex(ValueError, 'every development row'):
                build_cache(manifest, rows[:-1], root / 'subset', full_development=True)
            with self.assertRaisesRegex(ValueError, 'cache QA manifest'):
                build_cache(qa_path, rows, root / 'qa_full', full_development=True)
            options = Namespace(dataset=manifest, dataset_sha256='0' * 64,
                                cache_dir=root / 'bad_receipt', output=root / 'report.json')
            with self.assertRaisesRegex(ValueError, 'matching dataset SHA-256'):
                build_full_development(options)
            newtest = root / 'newtest.json'
            newtest.write_text(json.dumps(dict(document, images=[
                dict(document['images'][0], split='newtest')])), encoding='utf-8')
            options.dataset, options.dataset_sha256 = newtest, sha256(newtest)
            with patch('cnn.disk_cache.load_dataset_manifest') as loader:
                with self.assertRaisesRegex(ValueError, 'no newtest'):
                    build_full_development(options)
                loader.assert_not_called()
            with patch('cnn.disk_cache.shutil.disk_usage') as usage:
                usage.return_value.free = 20 * (1 << 30)
                with self.assertRaisesRegex(ValueError, 'free-space reserve'):
                    build_cache(manifest, rows, root / 'no_space', full_development=True)
            self.assertFalse((root / 'no_space').exists())
            raw = FullFrameDataset(rows, 'train', mosaic=True)
            cached = DiskCachedDataset(rows, 'train', manifest, cache_root, mosaic=True)
            for epoch, mosaic in ((6, True), (7, True), (285, False)):
                raw.set_epoch(epoch, mosaic)
                cached.set_epoch(epoch, mosaic)
                for index in range(len(raw)):
                    assert_item_equal(raw[index], cached[index])
            with self.assertRaises(FileExistsError):
                build_cache(manifest, rows, cache_root)
            with patch('cnn.disk_cache.preprocessing_identity', return_value={}):
                with self.assertRaisesRegex(ValueError, 'stale cache'):
                    DiskCachedDataset(rows, 'train', manifest, cache_root)
            original_manifest = manifest.read_bytes()
            manifest.write_bytes(original_manifest + b' ')
            with self.assertRaisesRegex(ValueError, 'stale cache'):
                DiskCachedDataset(rows, 'train', manifest, cache_root)
            manifest.write_bytes(original_manifest)
            changed_rows = [dict(row) for row in rows]
            changed_rows[0]['labels'] = [1]
            with self.assertRaisesRegex(ValueError, 'stale source, row'):
                DiskCachedDataset(changed_rows, 'train', manifest, cache_root)
            source = rows[0]['image_path']
            original_source = source.read_bytes()
            source.write_bytes(original_source + b'x')
            with self.assertRaisesRegex(ValueError, 'stale source'):
                DiskCachedDataset(rows, 'train', manifest, cache_root)
            source.write_bytes(original_source)
            blob = cache_root / 'rgb.bin'
            with blob.open('r+b') as stream:
                stream.write(b'\xff')
            with self.assertRaisesRegex(ValueError, 'corrupt RGB'):
                cached._load(0)  # Detect corruption even after a reader was opened.
            with self.assertRaisesRegex(ValueError, 'corrupt cache'):
                DiskCachedDataset(rows, 'train', manifest, cache_root)
            with self.assertRaisesRegex(ValueError, 'corrupt cache'):
                open_validated_cache(snapshot, cache_root, sha256(cache_root / 'index.json'))
            with blob.open('r+b') as stream:
                stream.truncate(10)
            with self.assertRaisesRegex(ValueError, 'incomplete cache'):
                DiskCachedDataset(rows, 'train', manifest, cache_root)
            incomplete = root / 'incomplete'
            incomplete.mkdir()
            with self.assertRaises(FileNotFoundError):
                DiskCachedDataset(rows, 'train', manifest, incomplete)
            with self.assertRaisesRegex(ValueError, 'no newtest'):
                build_cache(manifest, [dict(rows[0], split='newtest')], root / 'rejected')
            self.assertEqual(preprocessing_identity()['pixel_order'], 'HWC_RGB')

    def test_preprocessing_ast_identity_ignores_unrelated_text(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.py'
            source.write_text('class Pixels:\n    def load(self):\n        return 1\n', encoding='utf-8')
            original = disk_cache._ast_sha256(source, name='Pixels', method='load')
            source.write_text('# unrelated\nclass Pixels:\n    def load(self):\n        return 1\n\nX = 2\n',
                              encoding='utf-8')
            self.assertEqual(original, disk_cache._ast_sha256(
                source, name='Pixels', method='load'))
            source.write_text('class Pixels:\n    def load(self):\n        return 2\n', encoding='utf-8')
            self.assertNotEqual(original, disk_cache._ast_sha256(
                source, name='Pixels', method='load'))


if __name__ == '__main__':
    unittest.main()
