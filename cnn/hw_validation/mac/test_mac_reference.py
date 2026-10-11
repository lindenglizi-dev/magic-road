import random
import tempfile
import unittest
from pathlib import Path

from mac_reference import Beat, INT32_MAX, INT32_MIN, MacReference, intermediate_banks, write_vectors


class MacReferenceTest(unittest.TestCase):
    def test_seeded_vectors_include_required_random_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vectors.txt"
            count = write_vectors(path, random_cases=1024, seed=42)
            self.assertEqual(count, 1031)
            self.assertEqual(len(path.read_text(encoding="ascii").splitlines()), 1031)

    def test_mask_and_negative_extrema(self) -> None:
        reference = MacReference()
        beat = Beat(
            True,
            True,
            0x81,
            (-128, 7, 8, 9, 10, 11, 12, 127),
            ((-128,) * 8, (127,) * 8, (-1,) * 8),
            (0, 0, 0),
        )
        outcome = reference.apply(beat)
        self.assertIsNotNone(outcome)
        self.assertFalse(outcome.fault)
        self.assertEqual(outcome.values, (128, -127, 1))

    def test_intermediate_banks_preserve_output_major_reduction_order(self) -> None:
        beat = Beat(
            True,
            True,
            0x0F,
            (1, 2, 3, 4, 5, 6, 7, 8),
            ((1,) * 8, (2,) * 8, (-1,) * 8),
            (0, 0, 0),
        )
        banks = intermediate_banks(beat)
        self.assertEqual(banks.products[:8], (1, 2, 3, 4, 0, 0, 0, 0))
        self.assertEqual(banks.pairs[:4], (3, 7, 0, 0))
        self.assertEqual(banks.quads[:2], (10, 0))
        self.assertEqual(banks.dots, (10, 20, -10))

    def test_multi_beat_bias_is_added_once(self) -> None:
        reference = MacReference()
        weights = ((1,) * 8, (2,) * 8, (-1,) * 8)
        self.assertIsNone(reference.apply(Beat(True, False, 0xFF, (1,) * 8, weights, (10, 20, 30))))
        outcome = reference.apply(Beat(False, True, 0x03, (4,) * 8, weights, (999, 999, 999)))
        self.assertIsNotNone(outcome)
        self.assertEqual(outcome.values, (26, 52, 14))

    def test_stall_and_reset_leave_no_hidden_commit(self) -> None:
        reference = MacReference()
        beat = Beat(True, False, 0xFF, (3,) * 8, ((1,) * 8,) * 3, (4, 5, 6))
        before = reference.accumulators
        self.assertIsNone(reference.apply(beat, accepted=False))
        self.assertEqual(reference.accumulators, before)
        self.assertIsNone(reference.apply(beat))
        reference.reset()
        self.assertEqual(reference.accumulators, (0, 0, 0))

    def test_positive_and_negative_overflow_fault(self) -> None:
        reference = MacReference()
        positive = Beat(True, True, 0x01, (1,) + (0,) * 7, ((1,) * 8,) * 3, (INT32_MAX, 0, 0))
        negative = Beat(True, True, 0x01, (-128,) + (0,) * 7, ((127,) * 8,) * 3, (INT32_MIN, 0, 0))
        self.assertTrue(reference.apply(positive).fault)
        self.assertTrue(reference.apply(negative).fault)

    def test_1024_seeded_numeric_results_are_int32_or_fault(self) -> None:
        rng = random.Random(42)
        reference = MacReference()
        for _ in range(1024):
            beat = Beat(
                True,
                True,
                rng.randint(0, 255),
                tuple(rng.randint(-128, 127) for _ in range(8)),
                tuple(tuple(rng.randint(-128, 127) for _ in range(8)) for _ in range(3)),
                tuple(rng.randint(-1_000_000, 1_000_000) for _ in range(3)),
            )
            outcome = reference.apply(beat)
            self.assertFalse(outcome.fault)
            self.assertTrue(all(INT32_MIN <= value <= INT32_MAX for value in outcome.values))


if __name__ == "__main__":
    unittest.main()
