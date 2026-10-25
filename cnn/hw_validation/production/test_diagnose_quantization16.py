"""Small regressions for train-only selection, exact clipping, and oracle injection."""
import unittest
import numpy as np

from cnn.hw_validation.production.diagnose_quantization16 import select_indices, unclipped, injected_forward


class DiagnosisTests(unittest.TestCase):
    def test_selection_is_balanced_distinct_and_train_only(self):
        rows = [dict(split="train", sampling_group=g, camera_id=f"c{i % 3}", scene_id=f"s{i % 3}",
                     boxes=[[0, 0, 2, i + 1]] * (i % 4), teacher_key=f"{g}{i:02d}")
                for g in ("new", "replay") for i in range(12)]
        selected = select_indices(rows)
        self.assertEqual(len(set(selected)), 16)
        self.assertEqual(sum(rows[i]["sampling_group"] == "new" for i in selected), 8)
        rows[0]["split"] = "val"
        with self.assertRaises(ValueError):
            select_indices(rows)

    def test_unclipped_distinguishes_endpoint_from_clipping(self):
        raw = unclipped(np.array([-129, -128, 127, 128], dtype=np.int32), 1, 0)
        self.assertEqual(int(((raw < -128) | (raw > 127)).sum()), 2)
        np.testing.assert_array_equal(raw, [-129, -128, 127, 128])

    def test_injection_reencodes_at_existing_scale(self):
        # Only the injected layer is computed; tiny HWC avoids a full-frame test.
        class Model:
            graph = {"nodes": [{"name": "feature", "output": "feature", "op": "conv", "dtype": "int8"}],
                     "outputs": ["feature"]}
            scales = {"feature": .5}
            parameters = {"feature": {}}
        actual = injected_forward(Model(), np.zeros((1, 1, 1), dtype=np.int8), "feature",
                                  np.array([[[-100., .75, 100.]]]))[0]
        np.testing.assert_array_equal(actual, np.array([[[-128, 2, 127]]], dtype=np.int8))


if __name__ == "__main__":
    unittest.main()
