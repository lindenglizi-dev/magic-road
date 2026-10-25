"""RNE/saturation, invalid inputs, and the frozen continuation gate."""
import copy
import unittest
import numpy as np
from cnn.hw_validation.production import probe_early_features as probe


class ProbeTests(unittest.TestCase):
    def test_injection_audit(self):
        ideal = np.array([[[-100., -.75, -.25, .25, .75, 100.]]])
        codes, audit = probe.injection_audit(ideal, .5, ideal.shape)
        np.testing.assert_array_equal(codes, [[[-128, -2, 0, 0, 2, 127]]])
        self.assertEqual(audit["clipped"], 2)
        for scale, shape, data in ((0, ideal.shape, ideal), (.5, (1,), ideal),
                                   (.5, (1,), np.array([np.nan]))):
            with self.assertRaises(ValueError):
                probe.injection_audit(data, scale, shape)

    def test_gate_all_constraints_and_no_average_masking(self):
        before = {g: {"classes": {c: dict(ap50=.2, tp=10, fp=5) for c in ("person", "vehicle")}}
                  for g in ("all", "new", "replay")}
        after = copy.deepcopy(before)
        for label in ("person", "vehicle"):
            after["all"]["classes"][label]["ap50"] = .3
        self.assertTrue(probe.continuation_gate(after, before)["passed"])
        self.assertFalse(probe.continuation_gate(before, before)["passed"])
        for domain, label, field, value in (("all", "person", "tp", 9), ("all", "vehicle", "fp", 6),
                                           ("new", "vehicle", "ap50", .19), ("replay", "person", "ap50", .19)):
            bad = copy.deepcopy(after)
            bad[domain]["classes"][label][field] = value
            self.assertFalse(probe.continuation_gate(bad, before)["passed"])


if __name__ == "__main__":
    unittest.main()
