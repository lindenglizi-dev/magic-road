"""Static graph contract for the dormant QAT diagnostic."""
import unittest

from cnn.hw_validation.production.diagnose_qat import comparison_names
from cnn.hw_validation.production.graph import build_graph


class DiagnoseQATContractTest(unittest.TestCase):
    def test_nonconv_outputs_are_tracked_beside_all_convolutions(self):
        graph = build_graph()
        convolutions, tracked = comparison_names(graph)
        self.assertEqual(len(convolutions), 67)
        self.assertTrue(set(graph["outputs"]).isdisjoint(convolutions))
        self.assertTrue(set(graph["outputs"]).issubset(tracked))
        self.assertEqual(len(tracked), len(convolutions) + len(graph["outputs"]))


if __name__ == "__main__":
    unittest.main()
