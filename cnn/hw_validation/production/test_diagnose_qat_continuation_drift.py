import unittest

import numpy as np

from cnn.hw_validation.production.diagnose_qat import comparison_names
from cnn.hw_validation.production.diagnose_qat_continuation_drift import (
    CHANNELS, GROUPS, head_breakdown, head_layout)
from cnn.hw_validation.production.trained_integer import load_package
from cnn.hw_validation.production import train_qat as base


class DriftDiagnosisContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = load_package(base.BASE / "package")[0].graph

    def test_actual_graph_outputs_and_heads(self):
        convs, tracked = comparison_names(self.graph)
        roots, heads = head_layout(self.graph)
        self.assertEqual((len(convs), len(tracked)), (67, 70))
        self.assertEqual(set(roots), set(self.graph["outputs"]))
        self.assertEqual(set(roots.values()), {"head2", "head3", "head4"})
        self.assertTrue(heads)
        self.assertTrue(all(name.split(".", 1)[0] in set(roots.values()) for name in heads))

    def test_seven_channel_breakdown(self):
        reference = np.zeros((2, 3, 7), dtype=np.float64)
        actual = np.arange(42, dtype=np.float64).reshape(2, 3, 7)
        result = head_breakdown(reference, actual)
        self.assertEqual(set(result["groups"]), set(GROUPS))
        self.assertEqual(set(result["channels"]), set(CHANNELS))
        self.assertEqual(sum(len(indices) for indices in GROUPS.values()), 7)


if __name__ == "__main__":
    unittest.main()
