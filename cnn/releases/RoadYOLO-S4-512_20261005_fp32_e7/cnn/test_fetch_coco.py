"""Offline regression for download boundaries and empty-part retry."""
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from .fetch_coco import extract_images, fetch, select_images


class FetchTest(unittest.TestCase):
    def test_empty_partial_and_reuse(self):
        class Response:
            status = 200
            headers = {'Content-Length': '3'}

            def __enter__(self):
                self.reads = 0
                return self

            def __exit__(self, *args):
                pass

            def read(self, size):
                self.reads += 1
                return b'abc' if self.reads == 1 else b''

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'image.jpg'
            destination.with_suffix('.jpg.part').touch()
            with patch('urllib.request.urlopen', return_value=Response()) as request:
                receipt = fetch('train2017/000000000001.jpg', destination)
                self.assertEqual(receipt['bytes'], 3)
                self.assertTrue(fetch('train2017/000000000001.jpg', destination)['reused'])
                self.assertEqual(request.call_count, 1)
            with self.assertRaises(ValueError):
                fetch('../secret', destination)

    def test_selection_is_fixed(self):
        annotation = dict(images=[dict(id=1), dict(id=2)],
                          annotations=[dict(image_id=1, category_id=1),
                                       dict(image_id=2, category_id=2)])
        self.assertEqual(select_images(annotation, 2), annotation['images'])
        with self.assertRaises(ValueError):
            select_images(annotation, 0)

    def test_safe_archive_and_existing_integrity(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / 'images.zip'
            with zipfile.ZipFile(archive, 'w') as stream:
                stream.writestr('train2017/000000000001.jpg', b'abc')
            self.assertEqual(extract_images(archive, root / 'images', 'train2017'), 1)
            self.assertEqual(extract_images(archive, root / 'images', 'train2017'), 1)
            (root / 'images/train2017/000000000001.jpg').write_bytes(b'damaged')
            with self.assertRaises(ValueError):
                extract_images(archive, root / 'images', 'train2017')
            with zipfile.ZipFile(root / 'unsafe.zip', 'w') as stream:
                stream.writestr('train2017/000000000002.jpg', b'abc')
                stream.writestr('../outside.jpg', b'abc')
            with self.assertRaises(ValueError):
                extract_images(root / 'unsafe.zip', root / 'images', 'train2017')
            self.assertFalse((root / 'images/train2017/000000000002.jpg').exists())


if __name__ == '__main__':
    unittest.main()
