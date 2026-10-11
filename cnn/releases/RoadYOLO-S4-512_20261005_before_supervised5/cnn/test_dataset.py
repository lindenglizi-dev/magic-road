from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

try:
    from . import dataset
except ImportError:
    import dataset


class DatasetTest(unittest.TestCase):
    def test_half_open_scale_and_type5(self) -> None:
        self.assertEqual(dataset._scaled_box(5, 10, 5, 10, 1280, 720),
                         [2.0, 4.0, 4.0, 8.0])
        self.assertEqual(dataset.VIRAT_LABEL[5], 1)
        self.assertNotIn(5, dataset.VIRAT_IGNORE)
        with self.assertRaises(ValueError):
            dataset._scaled_box(0, 0, -1, 10, 1280, 720)
        for invalid in (float('nan'), float('inf'), -float('inf')):
            with self.assertRaisesRegex(ValueError, 'finite'):
                dataset._scaled_box(invalid, 0, 10, 10, 1280, 720)

    def test_rider_is_not_inferred(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "objects.txt"
            path.write_text("7 1 0 0 0 20 10 5\n", encoding="utf-8")
            rows = dataset._read_virat(path)
            self.assertEqual(rows[0][0][-1], 5)
            self.assertEqual(dataset.VIRAT_LABEL[rows[0][0][-1]], 1)
            self.assertFalse(any(dataset.VIRAT_LABEL.get(row[-1]) == 0 for row in rows[0]))

    def test_incomplete_and_scene_gates_fail_closed(self) -> None:
        document = {
            "schema_version": 1, "task": "detection",
            "input_size": [dataset.WIDTH, dataset.HEIGHT],
            "classes": list(dataset.CLASSES),
            "images": [{
                "image": "one.png", "boxes": [[0, 0, 1, 1]], "labels": [0],
                "ignore_boxes": [], "scene_id": "only-one", "split": "train",
                "source_sha256": "0" * 64, "source_frame": 0,
                "incomplete_frame": True,
            }],
        }
        report = dataset.audit(document)
        self.assertFalse(report["formal_training_eligible"])
        self.assertEqual(report["incomplete_frames"], 1)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.png").write_bytes(b"not inspected before guard")
            path = root / "dataset.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete"):
                dataset.load_dataset(path)

    def test_coco_adapter_maps_crowd_to_ignore(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            images = root / "images"
            images.mkdir()
            cv2.imwrite(str(images / "one.png"), np.zeros((720, 1280, 3), np.uint8))
            annotation = root / "instances.json"
            annotation.write_text(json.dumps({
                "images": [{"id": 1, "file_name": "one.png", "width": 1280,
                            "height": 720}],
                "categories": [
                    {"id": 1, "name": "person"}, {"id": 2, "name": "bicycle"},
                    {"id": 3, "name": "car"}, {"id": 4, "name": "motorcycle"},
                    {"id": 6, "name": "bus"}, {"id": 8, "name": "truck"}],
                "annotations": [
                    {"image_id": 1, "category_id": 1, "bbox": [0, 0, 10, 10]},
                    {"image_id": 1, "category_id": 2, "bbox": [20, 20, 10, 10],
                     "iscrowd": 1},
                    {"id": 99, "image_id": 1, "category_id": 1,
                     "bbox": [10, 20, 5, 0], "area": 0}],
            }), encoding="utf-8")
            output = root / "out"
            adapted, provenance = dataset._coco_source(
                annotation, images, output, "pretrain", "https://example.invalid/source",
                "https://example.invalid/license", 1)
            result = {"images": adapted}
            self.assertEqual(result["images"][0]["labels"], [0])
            self.assertEqual(result["images"][0]["ignore_boxes"],
                             [[8.0, 8.0, 12.0, 12.0], [0.0, 0.0, 512.0, 288.0]])
            self.assertEqual(result['images'][0]['ignore_metadata'],
                             [{'label': 1, 'crowd': True}, {'label': -1, 'crowd': False}])
            self.assertEqual(provenance['degenerate_annotations'][0]['annotation_id'], 99)
            self.assertTrue(result["images"][0]["annotation_complete"])

    def test_raw_and_cached_pixels_match(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            images = root / 'source'
            images.mkdir()
            rng = np.random.default_rng(42)
            cv2.imwrite(str(images / 'one.jpg'), rng.integers(0, 256, (43, 91, 3), np.uint8))
            annotation = root / 'instances.json'
            annotation.write_text(json.dumps({
                'images': [{'id': 1, 'file_name': 'one.jpg', 'width': 91, 'height': 43}],
                'categories': [{'id': index + 1, 'name': name}
                               for index, name in enumerate(dataset.COCO_LABEL)],
                'annotations': [{'image_id': 1, 'category_id': 1, 'bbox': [1, 2, 20, 30]}]
            }), encoding='utf-8')
            cached, _ = dataset._coco_source(annotation, images, root / 'cached', 'train',
                                             'https://example/source', 'https://example/license')
            raw, _ = dataset._coco_source(annotation, images, root / 'raw', 'train',
                                          'https://example/source', 'https://example/license',
                                          raw_images=True, allowed_names={'one.jpg'})
            self.assertEqual(cached[0]['boxes'], raw[0]['boxes'])
            self.assertTrue(raw[0]['preprocess']['raw_image'])
            self.assertFalse((root / 'raw/images').exists())
            pixels = cv2.imread(str(images / 'one.jpg'))
            letterboxed, transform = dataset._letterbox_720(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB))
            self.assertEqual(raw[0]['preprocess']['letterbox_1280x720'], transform)
            cached_pixels = cv2.cvtColor(cv2.imread(str(root / 'cached' / cached[0]['image'])),
                                         cv2.COLOR_BGR2RGB)
            np.testing.assert_array_equal(cached_pixels, dataset.resize_area(letterboxed))

    def test_resize_contract(self) -> None:
        output = dataset.resize_area(np.zeros((720, 1280, 3), np.uint8))
        self.assertEqual(output.shape, (288, 512, 3))
        self.assertEqual(output.dtype, np.uint8)
        with self.assertRaises(ValueError):
            dataset.resize_area(np.zeros((288, 512, 3), np.uint8))


if __name__ == "__main__":
    unittest.main()
