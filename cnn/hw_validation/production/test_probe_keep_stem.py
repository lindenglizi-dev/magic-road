"""Regress the sole recipe change and branch-alignment guard."""
import unittest

from cnn.hw_validation.production.probe_keep_stem import keep_stem_scales


class KeepStemTests(unittest.TestCase):
    def test_only_Stem_is_exempted_from_feature_halving(self):
        graph = {"nodes": [{"op": "conv", "output": "stem.conv", "dtype": "int8"},
            {"op": "conv", "output": "feature", "dtype": "int8"},
            {"op": "split_view", "inputs": ["feature"], "outputs": [{"output": "a"}, {"output": "b"}]},
            {"op": "conv", "output": "head", "dtype": "int16_q7_8"}]}
        scales = {"input": 1., "stem.conv": .25, "feature": .2, "a": .2, "b": .2, "head": 1 / 256}
        self.assertEqual(keep_stem_scales(graph, scales), dict(scales, feature=.1, a=.1, b=.1))

    def test_changed_Stem_branch_is_rejected(self):
        graph = {"nodes": [{"op": "conv", "output": "stem.conv", "dtype": "int8"},
            {"op": "split_view", "inputs": ["stem.conv"], "outputs": [{"output": "a"}, {"output": "b"}]}]}
        with self.assertRaises(ValueError):
            keep_stem_scales(graph, {"input": 1., "stem.conv": .25, "a": .25, "b": .25})


if __name__ == "__main__":
    unittest.main()
