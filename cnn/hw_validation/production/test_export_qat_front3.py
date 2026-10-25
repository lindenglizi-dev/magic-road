"""Minimal independent rounding, ROM boundaries and loader negative checks."""
import unittest
import numpy as np
from cnn import integer
from cnn.hw_validation.production import export_qat_front3 as export


class Front3Tests(unittest.TestCase):
    def test_rom_crossing_and_invalid_ranges(self):
        data = bytes(range(60))
        self.assertEqual(export.word_bytes(data, 19, 4), bytes([19, 20, 21, 22]))
        self.assertEqual(export.word_bytes(data, 39, 4), bytes([39, 40, 41, 42]))
        for offset, length in ((-1, 1), (59, 2), (0, -1)):
            with self.assertRaises(ValueError):
                export.word_bytes(data, offset, length)

    def test_independent_RNE_saturation_and_entire_silu_domain(self):
        values = np.array([-7, -5, -3, -1, 1, 3, 5, 7], dtype=np.int32)
        np.testing.assert_array_equal(export.oracle_requantize(values, 1, 1, -128, 127), [-4, -2, -2, 0, 0, 2, 2, 4])
        np.testing.assert_array_equal(export.oracle_requantize(np.array([-129, 128]), 1, 0, -128, 127), [-128, 127])
        for shift in (-1, 63):
            with self.assertRaises(ValueError):
                export.round_even(1, shift)
        codes = np.arange(-32768, 32768, dtype=np.int32)
        constants = integer.tables()
        np.testing.assert_array_equal(export.oracle_silu(codes, constants["silu"], constants["silu_upper"]), integer.silu(codes))

    def test_loader_sign_extension_kind_and_stop(self):
        params = {name: dict(weights=np.array([-7, 2], dtype=np.int8), bias=np.array([-9]),
            pre_multiplier=np.array([100]), pre_shift=np.array([4]), post_multiplier=np.array([200]),
            post_shift=np.array([5])) for name in export.LAYERS}
        lut = np.array([-2, 3], dtype=np.int16)
        record = lambda op, address=0, kind=0, value=0: op << 60 | address << 49 | kind << 46 | int(value) & 0xffffffff
        program = [record(0, i, value=v) for i, v in enumerate(lut)]
        for mode, fields in enumerate(export.loader_fields(params)):
            if mode:
                program.append(record(4, value=1))
            for kind, values in fields.items():
                program.extend(record(1, i, kind, v) for i, v in enumerate(values))
        program += [record(7), 0, 0]
        self.assertGreater(export.verify_loader(program, params, lut), 0)
        for kind in ("bad_sign", "bad_kind", "after_stop"):
            bad = program.copy()
            if kind == "bad_sign":
                bad[2] = (bad[2] & ~0xffffffff) | 249
            elif kind == "bad_kind":
                bad[2] ^= 1 << 46
            else:
                bad[-1] = 1
            with self.assertRaises(ValueError):
                export.verify_loader(bad, params, lut)


if __name__ == "__main__":
    unittest.main()
