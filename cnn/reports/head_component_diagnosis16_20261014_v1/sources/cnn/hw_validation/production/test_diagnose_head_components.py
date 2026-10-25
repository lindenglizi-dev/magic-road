"""Only intended channels change; identities and unchanged class are exact."""
import unittest
import numpy as np
from cnn.hw_validation.production import diagnose_head_components as diag


class ComponentTests(unittest.TestCase):
    def test_splice_all_recipes_and_input_preservation(self):
        source = [np.full((288 // s, 512 // s, 7), -7, dtype=np.int16) for s in (4, 8, 16)]
        ideal = [np.full(head.shape, 9, dtype=np.int16) for head in source]
        for channels in diag.RECIPES.values():
            output = diag.splice(source, ideal, channels)
            for actual, original, reference in zip(output, source, ideal, strict=True):
                for channel in range(7):
                    np.testing.assert_array_equal(actual[..., channel],
                        reference[..., channel] if channel in channels else original[..., channel])
                self.assertFalse(np.shares_memory(actual, original))
                self.assertTrue(np.all(original == -7))
                self.assertTrue(np.all(reference == 9))
        with self.assertRaises(ValueError):
            diag.splice(source, ideal, (7,))
        with self.assertRaises(ValueError):
            diag.splice(source[:2], ideal, ())
        with self.assertRaises(ValueError):
            diag.splice([head.astype(np.float32) for head in source], ideal, ())

    def test_class_isolation_and_box_topK(self):
        rng = np.random.default_rng(42)
        source = [rng.integers(-1500, 1500, (288 // s, 512 // s, 7), dtype=np.int16) for s in (4, 8, 16)]
        ideal = [rng.integers(-1500, 1500, head.shape, dtype=np.int16) for head in source]
        before = diag.previous.stages(source)
        for channels, label in (((5,), 1), ((6,), 0)):
            after = diag.previous.stages(diag.splice(source, ideal, channels))
            self.assertEqual([r for r in before[4] if r["label"] == label],
                             [r for r in after[4] if r["label"] == label])
        after = diag.previous.stages(diag.splice(source, ideal, (0, 1, 2, 3)))
        np.testing.assert_array_equal(before[1], after[1])
        for label in (0, 1):
            self.assertEqual(before[3][label]["floor"], after[3][label]["floor"])
            self.assertEqual(before[3][label]["top128"], after[3][label]["top128"])


if __name__ == "__main__":
    unittest.main()
