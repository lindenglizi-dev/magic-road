"""部署整数语义的边界检查，不作为训练精度证据。"""

import unittest
from fractions import Fraction

import numpy as np

from cnn.integer import conv2d, exponent, postprocess, requantize, resize_area
from cnn.integer import encode_multiplier, round_div_even, sigmoid, silu, tables


class IntegerContractTests(unittest.TestCase):
    def test_round_even_signed(self):
        source = np.arange(-31, 32, dtype=np.int64)
        for divisor in (1, 2, 4, 25):
            expected = [round(int(value) / divisor) for value in source]
            np.testing.assert_array_equal(round_div_even(source, divisor), expected)
        np.testing.assert_array_equal(requantize(np.array([-300, -5, -3, 3, 5, 300]), 1, 1),
                                      [-128, -2, -2, 2, 2, 127])
        with self.assertRaises(OverflowError):
            requantize(np.array([1 << 31]), 1, 0)

    def test_resize_single_round(self):
        source = np.full((720, 1280, 3), 255, dtype=np.uint8)
        np.testing.assert_array_equal(resize_area(source), 255)
        source[:5, :5, :] = np.arange(25).reshape(5, 5, 1)
        output = resize_area(source)
        kernel = np.array([[2, 2, 1, 0, 0], [0, 0, 1, 2, 2]])
        for y in range(2):
            for x in range(2):
                expected = round(float(np.sum(np.arange(25).reshape(5, 5)
                                             * kernel[y, :, None] * kernel[x, None, :])) / 25)
                self.assertEqual(output[y, x, 0], expected)
        self.assertEqual(output.shape, (288, 512, 3))

    def test_resize_matches_full_frame_reference(self):
        source = np.random.default_rng(42).integers(0, 256, (720, 1280, 3), np.uint8)
        blocks = source.astype(np.int32).reshape(144, 5, 256, 5, 3)
        kernel = np.array([[2, 2, 1, 0, 0], [0, 0, 1, 2, 2]], dtype=np.int32)
        total = np.einsum('aibjc,ui,vj->aubvc', blocks, kernel, kernel,
                          optimize=True).reshape(288, 512, 3)
        np.testing.assert_array_equal(resize_area(source), round_div_even(total, 25))
        # Exhaust every attainable accumulator, including all rounding boundaries.
        accumulators = np.arange(6376, dtype=np.uint16)
        np.testing.assert_array_equal((accumulators + 12) // 25,
                                      round_div_even(accumulators, 25))

    def test_requant_full_width_and_int16_stage(self):
        source = np.array([-(1 << 31), -7, -5, -3, 3, 5, 7, (1 << 31) - 1])
        for multiplier in (0, 1, (1 << 31) - 1):
            for shift in (0, 1, 31, 62):
                expected = [max(-32768, min(32767,
                            round(Fraction(int(value) * multiplier, 1 << shift))))
                            for value in source]
                np.testing.assert_array_equal(
                    requantize(source, multiplier, shift, -32768, 32767), expected)
        for scale in (0.125, 0.5, 1.0, 2.0):
            multiplier, shift = encode_multiplier(scale)
            self.assertEqual(Fraction(multiplier, 1 << shift), Fraction(scale))
        for scale in (0, -1, float('inf'), float('nan'), 2.0 ** 40):
            with self.assertRaises(ValueError):
                encode_multiplier(scale)
        with self.assertRaises(OverflowError):
            round_div_even(np.array([-(1 << 63)], dtype=np.int64), 2)
        with self.assertRaises(OverflowError):
            requantize(np.array([(1 << 64) - 1], dtype=np.uint64), 1, 0)
        with self.assertRaises(ValueError):
            requantize(np.array([1.5]), 1, 0)

    def test_tables_and_tails(self):
        self.assertEqual(len(tables()["silu"]), 1024)
        self.assertEqual(len(tables()["exp"]), 256)
        np.testing.assert_array_equal(silu(np.array([-32768, -2048, 0, 2048, 32767])),
                                      [0, 0, 0, 2048, 32767])
        np.testing.assert_array_equal(sigmoid(np.array([-32768, -2048, 0, 2048, 32767])),
                                      [0, 0, 32768, 65535, 65535])
        values = np.arange(-32768, 32768)
        self.assertEqual(silu(values).dtype, np.int16)
        self.assertTrue(np.all(np.diff(sigmoid(values).astype(np.int64)) >= 0))
        self.assertEqual(int(exponent(np.array([-5000]))[0]), int(tables()["exp"][0]))

    def test_standard_and_depthwise_convolution(self):
        image = np.arange(18, dtype=np.int8).reshape(3, 3, 2)
        weights = np.ones((2, 2, 3, 3), dtype=np.int8)
        np.testing.assert_array_equal(conv2d(image, weights, np.array([-1, 1])), [[[152, 154]]])
        depthwise = np.ones((2, 1, 3, 3), dtype=np.int8)
        np.testing.assert_array_equal(conv2d(image, depthwise, np.array([0, 0]), groups=2),
                                      [[[72, 81]]])

    def test_classwise_nms_and_coordinate_mapping(self):
        heads = [np.full((288 // stride, 512 // stride, 7), -2048, dtype=np.int16)
                 for stride in (4, 8, 16)]
        heads[0][10, 10, :4] = [0, 0, 0, 0]
        heads[0][10, 10, 4:] = [2048, 2048, 2048]
        # 同一位置的两类允许同时存在，不能跨类NMS。
        detections = postprocess(heads, (39322, 39322))
        self.assertEqual([item["label"] for item in detections], [0, 1])
        self.assertEqual(detections[0]["box_source"], [95, 95, 105, 105])
        self.assertEqual(detections[0]["score_uint16"], 65534)

    def test_convolution_bias_and_accumulator_limits(self):
        image = np.array([[[-128]]], dtype=np.int8)
        weight = np.array([[[[1]]]], dtype=np.int8)
        # A non-INT32 bias must not be accepted merely because the MAC cancels it.
        with self.assertRaisesRegex(OverflowError, 'bias'):
            conv2d(image, weight, np.array([1 << 31], dtype=np.int64))
        with self.assertRaisesRegex(OverflowError, '累加'):
            conv2d(image, weight, np.array([-(1 << 31)], dtype=np.int64))
        with self.assertRaises(OverflowError):
            conv2d(image, weight, np.array([(1 << 64) - 1], dtype=np.uint64))
        with self.assertRaises(ValueError):
            conv2d(image, weight, np.array([0.5]))
        np.testing.assert_array_equal(
            conv2d(image, weight, np.array([(1 << 31) - 1], dtype=np.int32)),
            [[[(1 << 31) - 129]]])


if __name__ == "__main__":
    unittest.main()
