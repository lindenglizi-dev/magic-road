#!/usr/bin/env python3
"""Narrow checks for the fixed HOG324 augmentation experiment."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from hog_svm_augmentation_diagnostic import (  # noqa: E402
    augment_roi,
    augmentation_rows,
    grouped_metrics,
    quantization_scope_gate,
    quantization_ranges,
)


class HogSvmAugmentationTest(unittest.TestCase):
    def test_mirror_and_translation_replicate_edges(self) -> None:
        roi = np.arange(32 * 32, dtype=np.uint16).reshape(32, 32).astype(np.uint8)
        self.assertTrue(np.array_equal(augment_roi(roi, True, 0, 0), roi[:, ::-1]))
        right = augment_roi(roi, False, 2, 0)
        self.assertTrue(np.array_equal(right[:, 0], roi[:, 0]))
        self.assertTrue(np.array_equal(right[:, 1], roi[:, 0]))
        self.assertTrue(np.array_equal(right[:, 2:], roi[:, :-2]))
        up = augment_roi(roi, False, 0, -2)
        self.assertTrue(np.array_equal(up[:-2], roi[2:]))
        self.assertTrue(np.array_equal(up[-2], roi[-1]))
        self.assertTrue(np.array_equal(up[-1], roi[-1]))

    def test_each_original_and_class_keep_total_weight(self) -> None:
        roi = np.zeros((32, 32), dtype=np.uint8)
        originals = [
            {"sample_key": "p", "truth": "ped", "roi": roi},
            {"sample_key": "v", "truth": "vehicle", "roi": roi + 1},
        ]
        rows, audit = augmentation_rows(
            originals, [(False, 0, 0), (False, -2, 0), (True, 0, 0)]
        )
        for key in ("p", "v"):
            self.assertAlmostEqual(sum(row["sample_weight"] for row in rows if row["sample_key"] == key), 1.0)
        self.assertEqual(audit["class_total_sample_weight"], {"ped": 1.0, "vehicle": 1.0})

    def test_scene_class_group_is_explicit(self) -> None:
        rows = grouped_metrics([{
            "dataset": "official_val", "truth": "ped", "scene_id": "scene-a",
            "track_id": "", "visibility": "", "frame_index": 1,
            "baseline_float_prediction": "vehicle", "new_float_prediction": "ped",
            "baseline_quantized_prediction": "vehicle", "new_quantized_prediction": "ped",
        }])
        result = next(row for row in rows if row["group_type"] == "scene_class")
        self.assertEqual(result["group_value"], "scene-a|ped")
        self.assertEqual(result["new_quantized_correct"], 1)
        self.assertIsNone(result["invalid_FAR"])

    def test_quantization_bounds_include_bias_and_all_products(self) -> None:
        weights = np.resize(np.asarray([32767, -32768]), 324)
        ranges = quantization_ranges({"weight_q": weights, "bias_q": -3})
        legal = ranges["legal_hog_descriptor_bound_full_weight_storage"]
        full = ranges["full_13bit_feature_port_and_full_weight_storage"]
        self.assertEqual(legal["feature_q_range"], [0, 4096])
        self.assertEqual(full["feature_q_range"], [0, 8191])
        self.assertGreater(full["required_signed_bits"], legal["required_signed_bits"])

    def test_margin_gate_allows_near_flip_and_rejects_unexplained_flip(self) -> None:
        near = {
            "sample_key": "near", "truth": "ped", "new_float_prediction": "ped",
            "new_quantized_prediction": "vehicle", "abs_float_quantized_error": 0.002,
            "abs_float_margin": 0.0025, "float_margin_exceeds_own_quantization_error": False,
        }
        self.assertTrue(quantization_scope_gate([near], 0.001)["sign_flip_margin_condition_passed"])
        far = {**near, "sample_key": "far", "abs_float_margin": 0.01}
        self.assertFalse(quantization_scope_gate([far], 0.001)["sign_flip_margin_condition_passed"])


if __name__ == "__main__":
    unittest.main()
