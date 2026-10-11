"""Subset selection is label-blind, hashes evaluated bytes, and fails closed."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .evaluate import load_validation_subset
from .train import dataset_content_hash, sha256


class ValidationSubsetTest(unittest.TestCase):
    def test_binding_selection_and_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            for index in range(7):
                image = root / f'{index}.jpg'
                image.write_bytes(bytes([index]))
                rows.append(dict(image=image.name, boxes=[], labels=[], ignore_boxes=[],
                                 source_sha256=sha256(image), scene_id=f'scene{index}',
                                 source_frame=index, split='train' if index == 0 else 'val',
                                 incomplete_frame=False, preprocess={'raw_image': True}))
            document = dict(schema_version=1, task='detection', input_size=[512, 288],
                            classes=['person', 'vehicle'], training_eligible=True, images=rows)
            path = root / 'dataset.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            expected = dataset_content_hash([
                dict(image=row['image'], image_sha256=row['source_sha256']) for row in rows])
            with patch('cnn.evaluate.sha256', wraps=sha256) as hashes:
                selected, total = load_validation_subset(path, expected, 2)
                self.assertEqual(total, 6)
                self.assertEqual([row['image'] for row in selected], ['1.jpg', '4.jpg'])
                self.assertEqual(hashes.call_count, 2)
            with self.assertRaisesRegex(ValueError, 'identity'):
                load_validation_subset(path, '0' * 64, 2)
            # Explicit development-domain mode skips TRAINING identity, never JPEG integrity.
            self.assertEqual(len(load_validation_subset(path, None, 2)[0]), 2)
            (root / '1.jpg').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'source hash'):
                load_validation_subset(path, expected, 2)
            with self.assertRaisesRegex(ValueError, 'source hash'):
                load_validation_subset(path, None, 2)
            rows[-1]['split'] = 'newtest'
            path.write_text(json.dumps(document), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'development-only'):
                load_validation_subset(path, expected, 2)


if __name__ == '__main__':
    unittest.main()
