"""CPU-only exact-forward, STE-gradient, and frozen-scale export checks."""
import time
import unittest
from pathlib import Path

import numpy as np
import torch

from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import CHECKPOINT, TRAIN, centered
from cnn.hw_validation.production.trained_integer import load_package


PROJECT = Path(__file__).resolve().parents[3]
REPORT = PROJECT / "cnn/reports/qat_exact_forward_20261013_v1"
BASELINE = PROJECT / "cnn/reports/replay_g10_integer_20261013_v2"


class QATExactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        state = torch.load(CHECKPOINT, weights_only=False, map_location="cpu")
        source = RoadYOLOS4().eval()
        source.load_state_dict(state["model"], strict=True)
        cls.integer, cls.manifest = load_package(BASELINE / "package")
        cls.folded = source.folded_conv_state()
        _, snapshot = load_dataset_snapshot(TRAIN)
        cls.image = make_frame_dataset(snapshot.rows, "train", TRAIN, mosaic=False)[0][0].unsqueeze(0)

    def setUp(self):
        self.qat = QATExactModel.from_package(
            BASELINE / "package", self.folded, BASELINE / "quantization.json")

    def test_real_frame_every_node_and_pre_are_exact(self):
        heads, trace = self.qat(self.image, capture=True)
        expected_heads, _, expected = self.integer.forward(centered(self.image[0]), capture=True)
        for actual, wanted in zip(heads, expected_heads, strict=True):
            np.testing.assert_array_equal(
                torch.round(actual.detach() * 256).to(torch.int16).permute(0, 2, 3, 1).numpy()[0], wanted)
        checked = 0
        for node in self.qat.graph["nodes"]:
            names = ([view["output"] for view in node["outputs"]]
                     if node["op"] == "split_view" else [node["output"]])
            for name in names:
                wanted = torch.from_numpy(expected[name].transpose(2, 0, 1)).unsqueeze(0)
                wanted = wanted.to(torch.float32) * self.qat.scales[name]
                torch.testing.assert_close(trace[name].detach(), wanted, rtol=0, atol=0)
                checked += 1
            if node["op"] == "conv":
                wanted = torch.from_numpy(expected[node["name"] + ":pre"].transpose(2, 0, 1)).unsqueeze(0)
                torch.testing.assert_close(trace[node["name"] + ":pre"].detach(),
                                           wanted.to(torch.float32) / 256, rtol=0, atol=0)
        self.assertEqual(checked, 113)

    def test_gradient_update_and_fixed_scale_export_roundtrip(self):
        before = [parameter.detach().clone() for parameter in self.qat.parameters()]
        optimizer = torch.optim.SGD(self.qat.parameters(), lr=1e-4)
        optimizer.zero_grad(set_to_none=True)
        heads = self.qat(self.image)
        loss = sum(head.square().mean() for head in heads)
        loss.backward()
        gradients = [parameter.grad for parameter in self.qat.parameters()]
        self.assertTrue(all(gradient is not None and torch.isfinite(gradient).all()
                            for gradient in gradients))
        self.assertGreater(sum(float(gradient.abs().sum()) for gradient in gradients), 0)
        optimizer.step()
        self.assertTrue(any(not torch.equal(old, new) for old, new in zip(before, self.qat.parameters(), strict=True)))

        expected, _, _ = self.qat.integer_forward(self.image)
        output = REPORT / "test_exports" / str(time.time_ns()) / "package"
        self.qat.export_package(output, {"purpose": "unit_test_updated_weights_not_candidate"})
        reloaded, manifest = load_package(output)
        actual, _, _ = reloaded.forward(centered(self.image[0]))
        for wanted, value in zip(expected, actual, strict=True):
            np.testing.assert_array_equal(wanted[0], value)
        self.assertTrue(manifest["provenance"]["qat_exact_fixed_weight_scales"])
        self.assertEqual(manifest["provenance"]["qat_export_scope"],
                         "numeric_selftest_not_quality_run")
        self.assertFalse(torch.cuda.is_available())
        self.assertFalse(torch.cuda.is_initialized())


if __name__ == "__main__":
    unittest.main()
