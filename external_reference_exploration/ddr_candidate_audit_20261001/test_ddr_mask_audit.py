"""Synthetic tests only. No user's video is read."""
from __future__ import annotations

import unittest
import cv2
import numpy as np
from ddr_mask_audit import (audit_mask, canonical, keep_runs, match_report,
                            require_binary, rle_partition)


class AuditTests(unittest.TestCase):
    def assert_partition(self, mask):
        labels, info = rle_partition(require_binary(mask))
        _, reference = cv2.connectedComponents(require_binary(mask), connectivity=8,
                                              ltype=cv2.CV_32S)
        np.testing.assert_array_equal(canonical(labels), canonical(reference))
        return info

    def test_empty_and_full(self):
        self.assert_partition(np.zeros((8, 8), np.uint8))
        self.assert_partition(np.ones((8, 8), np.uint8))

    def test_bridge_multiple_old_labels(self):
        m = np.zeros((8, 8), np.uint8)
        m[0, [0, 3, 7]] = 1
        m[1, :] = 1
        d = self.assert_partition(m)
        self.assertEqual(d['reference_labels_allocated'], 3)
        self.assertEqual(d['reference_union_operations'], 2)

    def test_diagonal_and_row_boundaries(self):
        self.assert_partition(np.eye(8, dtype=np.uint8))
        m = np.zeros((8, 8), np.uint8)
        m[:, 0] = 1
        m[:, -1] = 1
        self.assert_partition(m)

    def test_multiframe_does_not_reuse_state(self):
        busy = (np.indices((8, 8)).sum(axis=0) % 2).astype(np.uint8)
        self.assert_partition(busy)
        d = self.assert_partition(np.zeros_like(busy))
        self.assertEqual(d['reference_labels_allocated'], 0)

    def test_random_masks(self):
        rng = np.random.default_rng(20261001)
        for shape in [(8, 8), (16, 16)]:
            for probability in [.05, .2, .5, .8]:
                for _ in range(16):
                    self.assert_partition((rng.random(shape) < probability).astype(np.uint8))

    def test_thin_tall_component_can_pass_area_but_fail_run(self):
        mask = np.zeros((48, 16), np.uint8)
        mask[4:44, 5:8] = 1  # 3 * 40 = 120 foreground pixels
        obj = [{'id': 'synthetic_thin_component', 'class': 'synthetic',
                'bbox_xyxy': [5, 4, 8, 44]}]
        old = audit_mask(mask, 5, 100, 4, None, None, obj)
        new = audit_mask(mask, 1, 100, 4, None, None, obj)
        self.assertEqual(old['area_qualified_candidate_count'], 0)
        self.assertEqual(new['area_qualified_candidate_count'], 1)
        self.assertEqual(new['proposal_matching']['top_k']['matched'], 1)
        self.assertIsNone(old['capacity_proxy_failure'])

    def test_one_run_per_row_can_require_many_labels(self):
        mask = np.zeros((80, 8), np.uint8)
        mask[::2, 1:6] = 1
        r = audit_mask(mask, 5, 1, 4, 32, 64, None)
        self.assertEqual(r['row_run_peak_after_filter'], 1)
        self.assertEqual(r['reference_labels_allocated'], 40)
        self.assertTrue(r['capacity_proxy_failure'])

    def test_shadow_values_rejected(self):
        with self.assertRaises(ValueError):
            require_binary(np.array([[0, 127, 255]], np.uint8))

    def test_maximum_cardinality_not_greedy(self):
        # GT 0 can use both boxes, GT 1 can use only box 0 at IoU >= .5.
        boxes = [[0, 0, 6, 10], [4, 0, 10, 10]]
        objects = [{'id': 'a', 'class': 'ped', 'bbox_xyxy': [0, 0, 10, 10]},
                   {'id': 'b', 'class': 'vehicle', 'bbox_xyxy': [0, 0, 6, 10]}]
        r = match_report(boxes, objects)
        self.assertEqual(r['matched'], 2)
        r = match_report(boxes[:1], objects)
        self.assertEqual(r['matched'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
