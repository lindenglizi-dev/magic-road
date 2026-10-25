"""最小边界测试：真实halo、残差极值、MAC尾lane/负例和地址跨块。"""
import copy
import unittest
import numpy as np
from cnn.hw_validation.production import export_qat_csp_first as export


class CspFirstTests(unittest.TestCase):
    def test_halo_real_border_vs_missing_context(self):
        source = np.arange(8*8*24, dtype=np.int16).astype(np.int8).reshape(8, 8, 24)
        halo = export.halo_window(source)
        np.testing.assert_array_equal(halo[1:, 1:], source[:5, :5, 12:])
        self.assertFalse(halo[0].any())
        self.assertFalse(halo[:, 0].any())
        for origin in ((4, 4), (2, 0), (-4, 0), (72, 0)):
            with self.assertRaises(ValueError):
                export.halo_window(source, origin)

    def test_all_signed8_residual_pairs(self):
        first, second = np.meshgrid(np.arange(-128, 128, dtype=np.int16), np.arange(-128, 128, dtype=np.int16))
        total, saturated = export.add_residual(first.astype(np.int8), second.astype(np.int8))
        np.testing.assert_array_equal(total, first+second)
        np.testing.assert_array_equal(saturated, np.minimum(127, np.maximum(-128, first+second)))
        self.assertEqual((total.min(), total.max()), (-256, 254))
        with self.assertRaises(ValueError):
            export.add_residual(first, second)

    def test_MAC_tail_lane_and_negative_cases(self):
        act = np.arange(-6, 6, dtype=np.int8)
        weights = np.array([np.arange(12), -np.arange(12), np.ones(12)], dtype=np.int8)
        biases = np.array([-7, 3, 5], dtype=np.int32)
        task = dict(layer="pw", **export.mac_task(act, weights, biases, [[0, 0, c] for c in range(3)]))
        golden = {"pw": (weights.astype(np.int32) @ act.astype(np.int32) + biases).reshape(1, 1, 3)}
        self.assertEqual(export.verify_mac_tasks([task], golden), 3)
        self.assertEqual(task["groups"][1]["input_mask"], 15)
        for mutation in ("masked", "first", "output", "duplicate"):
            bad = copy.deepcopy(task)
            if mutation == "masked":
                bad["groups"][1]["activation_hex"] = f"{int(bad['groups'][1]['activation_hex'], 16) | (1 << 32):016x}"
            elif mutation == "first":
                bad["groups"][1]["first"] = True
            elif mutation == "output":
                bad["output_mask"] = 1
            with self.assertRaises(ValueError):
                export.verify_mac_tasks([bad, bad] if mutation == "duplicate" else [bad], golden)

    def test_tile_address_byte_lanes(self):
        base = 56311808
        self.assertEqual(export.address(base, 128, 24, 0, 0, 12), base+12)
        self.assertEqual(export.address(base, 128, 24, 0, 1, 12), base+36)
        self.assertEqual(export.address(base, 128, 24, 0, 4, 12), base+384+12)
        self.assertEqual(export.address(base, 128, 24, 4, 0, 12), base+32*384+12)
        for c in range(12, 24):
            address = export.address(base, 128, 24, 0, 0, c)
            beat, lane = (address & ~15)//2, address & 15
            self.assertEqual(beat*2+lane, address)
            self.assertEqual(beat % 8, 0)


if __name__ == "__main__":
    unittest.main()
