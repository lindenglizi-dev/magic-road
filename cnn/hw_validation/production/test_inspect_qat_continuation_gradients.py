"""Focused helpers for the bounded continuation-gradient diagnostic."""
import unittest

import torch

from cnn.hw_validation.production.inspect_qat_continuation_gradients import (
    parameter_group, weight_code_stats)


class ContinuationGradientHelpersTests(unittest.TestCase):
    def test_prediction_channel_groups(self):
        self.assertEqual([parameter_group("head2.reg_out", i) for i in range(5)],
                         ["prediction_reg4"] * 4 + ["prediction_obj1"])
        self.assertEqual(parameter_group("head4.cls_out", 1), "prediction_cls2")
        self.assertEqual(parameter_group("down2.dw.conv", 0), "nonhead")

    def test_outside_and_outward_counts(self):
        weight = torch.tensor([[[[128.5]]], [[[-129.0]]], [[[1.0]]]])
        scale = torch.ones(3, dtype=torch.float64)
        gradient = torch.tensor([[[[-1.0]]], [[[1.0]]], [[[2.0]]]])
        result = weight_code_stats(weight, scale, gradient)
        self.assertEqual(result["outside_representable_interval"], 2)
        self.assertEqual(result["outside_with_gradient_descent_outward"], 2)
        self.assertEqual(result["rounded_code_out_of_range"], 2)
        self.assertEqual(result["torch_float32_vs_numpy_float64_encoded_difference"], 0)


if __name__ == "__main__":
    unittest.main()
