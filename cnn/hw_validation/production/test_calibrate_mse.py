import unittest
from copy import deepcopy
import numpy as np

from cnn.hw_validation.production.calibrate_mse import (
    BINS, CHECKPOINT_HASH, POSTPROCESS, add_histogram, choose_scale, validate_baseline)


class CalibrationTests(unittest.TestCase):
    def test_baseline_identity_guard(self):
        baseline = {'checkpoint_sha256': CHECKPOINT_HASH, 'image_count': 17,
                    'diagnostic_metrics_at_0_5': {'protocol': 'road_greedy_101point_ap_v1'},
                    'postprocess_contract': POSTPROCESS}
        validate_baseline(baseline)
        for key in baseline:
            changed = deepcopy(baseline)
            changed[key] = {} if isinstance(changed[key], dict) else None
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_baseline(changed)

    def test_clipping_follows_rounded_codes(self):
        histogram = np.zeros((3, BINS))
        maximum = 127.
        centres = np.linspace(-maximum, maximum, BINS, endpoint=False) + maximum / BINS
        histogram[0] = 1
        histogram[1] = centres
        histogram[2] = centres**2
        _, candidates = choose_scale(histogram, maximum)
        for candidate in candidates:
            rounded = np.rint(centres / candidate['scale'])
            expected = np.mean((rounded < -128) | (rounded > 127))
            self.assertEqual(candidate['histogram_clipped_fraction'], expected)

    def test_moments_and_outliers(self):
        values = np.concatenate([np.linspace(-.25, 2, 100000), [32.0]])
        histogram = np.zeros((3, BINS))
        add_histogram(histogram, values, 32.)
        self.assertEqual(histogram[0].sum(), len(values))
        self.assertAlmostEqual(histogram[1].sum(), values.sum())
        self.assertAlmostEqual(histogram[2].sum(), (values**2).sum())
        best, candidates = choose_scale(histogram, 32.)
        self.assertLess(best['scale'], 32 / 127)
        self.assertLess(best['mse'], candidates[-1]['mse'])
        exact = lambda s: np.mean((np.clip(np.rint(values / s), -128, 127) * s - values)**2)
        self.assertLess(exact(best['scale']), exact(32 / 127))
        with self.assertRaises(ValueError):
            add_histogram(histogram, np.array([33.]), 32.)
        with self.assertRaises(ValueError):
            add_histogram(histogram, np.array([float('nan')]), 32.)


if __name__ == '__main__':
    unittest.main()
