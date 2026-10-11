"""Independent scalar checks of frozen integer semantics, not RTL acceptance."""
import json
import sys
import hashlib
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1]))
from cnn.integer import requantize, silu, tables


def main():
    inputs = np.arange(-32768, 32768, dtype=np.int64)
    constants = tables()
    expected = []
    for value in inputs:
        value = int(value)
        address = round(Fraction(value, 4)) + 512
        if value <= -2048:
            output = 0
        elif value >= 2048:
            output = value
        elif address == 1024:
            output = constants["silu_upper"]
        else:
            output = int(constants["silu"][max(0, min(1023, address))])
        expected.append(output)
    np.testing.assert_array_equal(silu(inputs), expected)
    output_bytes = np.asarray(expected, dtype="<i2").tobytes()
    source = np.array([-(1 << 31), -32768, -7, -5, -3, -1, 0, 1, 3, 5, 7, (1 << 31) - 1])
    checked = 0
    requant_vectors = []
    for multiplier in (0, 1, 3, (1 << 31) - 1):
        for shift in range(63):
            expected = [max(-128, min(127, round(Fraction(int(value) * multiplier, 1 << shift))))
                        for value in source]
            np.testing.assert_array_equal(requantize(source, multiplier, shift), expected)
            requant_vectors.extend([int(value), multiplier, shift, output]
                                   for value, output in zip(source, expected, strict=True))
            checked += len(source)
    result = {"silu_all_int16_cases": 65536, "requant_scalar_cases": checked,
              "mismatches": 0,
              "silu_vector_input_order": "signed INT16 ascending -32768..32767",
              "silu_vector_output_format": "little-endian INT16",
              "silu_expected_sha256": hashlib.sha256(output_bytes).hexdigest(),
              "scope": "Python scalar vs frozen Python vector contract; LUT constants shared, no RTL proof"}
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/silu_all_int16_expected.bin").write_bytes(output_bytes)
    (ROOT / "reports/requant_vectors.json").write_text(
        json.dumps({"fields": ["int32_input", "multiplier", "shift", "int8_output"],
                    "vectors": requant_vectors}), encoding="utf-8")
    (ROOT / "reports/numeric_selfcheck.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
