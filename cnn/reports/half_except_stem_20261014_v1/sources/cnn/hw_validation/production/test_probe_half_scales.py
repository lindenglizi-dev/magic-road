"""Focused half-scale identity and stop-gate regressions."""
import copy
import unittest

import numpy as np

from cnn.hw_validation.production.probe_half_scales import half_scales, energy_error, pooled, gate


class HalfScaleTests(unittest.TestCase):
    def test_scale_change_preserves_input_heads_and_views(self):
        graph = {"nodes": [
            {"op": "conv", "output": "feature", "dtype": "int8"},
            {"op": "split_view", "inputs": ["feature"], "outputs": [{"output": "a"}, {"output": "b"}]},
            {"op": "conv", "output": "head", "dtype": "int16_q7_8"}]}
        original = {"input": 1., "feature": .2, "a": .2, "b": .2, "head": 1 / 256}
        self.assertEqual(half_scales(graph, original), dict(original, feature=.1, a=.1, b=.1))
        with self.assertRaises(ValueError):
            half_scales(graph, dict(original, extra=1.))

    def test_energy_pooling_uses_reference_power(self):
        rows = [energy_error(np.array([1.]), np.array([2.])),
                energy_error(np.array([100.]), np.array([101.]))]
        self.assertAlmostEqual(pooled(rows)["normalized_rmse"], np.sqrt(2 / 10001))
        self.assertGreater(pooled(rows)["mean_frame_normalized_rmse"], .5)

    def test_gate_rejects_FP_growth_or_domain_regression(self):
        summary = {"heads": {mode: {domain: {"h": {"all": {"normalized_rmse": error}}}
            for domain in ("all", "new", "replay")} for mode, error in (("control", 1.), ("half", .5))},
            "detections": {mode: {label: {"tp": 2, "fp": 1} for label in ("person", "vehicle")}
                           for mode in ("control", "half")}}
        self.assertTrue(gate(summary, ["h"])["passed"])
        changed = copy.deepcopy(summary)
        changed["detections"]["half"]["person"]["fp"] = 2
        self.assertFalse(gate(changed, ["h"])["passed"])
        changed = copy.deepcopy(summary)
        changed["heads"]["half"]["new"]["h"]["all"]["normalized_rmse"] = 1.1
        self.assertFalse(gate(changed, ["h"])["passed"])


if __name__ == "__main__":
    unittest.main()
