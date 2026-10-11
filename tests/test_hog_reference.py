"""Check the scalar HOG against independent OpenCV Sobel/vector accumulation."""
import sys
import unittest
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from hog_reference import extract_features, make_test_roi


class HogReferenceTests(unittest.TestCase):
    def test_sobel_features_and_bins(self):
        rng = np.random.default_rng(20261011)
        fixtures = [np.zeros((32, 32), np.uint8), np.full((32, 32), 255, np.uint8),
                    np.array(make_test_roi(), np.uint8),
                    (np.indices((32, 32)).sum(axis=0) % 2 * 255).astype(np.uint8)]
        fixtures += [rng.integers(0, 256, (32, 32), dtype=np.uint8) for _ in range(20)]
        yy, xx = np.indices((30, 30)) + 1
        for roi in fixtures:
            gx = cv2.Sobel(roi, cv2.CV_16S, 1, 0, ksize=3)[1:-1, 1:-1].astype(np.int64)
            gy = cv2.Sobel(roi, cv2.CV_16S, 0, 1, ksize=3)[1:-1, 1:-1].astype(np.int64)
            ax, ay = np.abs(gx), np.abs(gy)
            bins = np.where(2*ay <= ax, 0, np.where(2*ax <= ay, 2,
                            np.where((gx < 0) == (gy < 0), 1, 3)))
            expected = np.zeros(64, np.int64)
            np.add.at(expected, ((yy >> 3)*16 + (xx >> 3)*4 + bins).ravel(),
                      np.minimum(ax+ay, 0x7ff).ravel())
            features, counts = extract_features(roi.astype(int).tolist())
            np.testing.assert_array_equal(features, expected)
            np.testing.assert_array_equal(counts, np.bincount(bins.ravel(), minlength=4))
            self.assertEqual(sum(counts), 900)

    def test_invalid_shape_is_rejected(self):
        for roi in ([], [[0]*32]*31, [[0]*31]*32, [[0]*33]*32):
            with self.assertRaises(ValueError):
                extract_features(roi)


if __name__ == '__main__':
    unittest.main()
