"""Generate independent exact rounding vectors; no GPU or training involved."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[3]))
from cnn.integer import requantize


def expected(product, shift):
    if not -(1 << 63) <= product < (1 << 63) or not 0 <= shift <= 63:
        raise ValueError("port value out of range")
    if product == -(1 << 63) or shift == 63:
        return 0, 1
    return max(-32768, min(32767, round(Fraction(product, 1 << shift)))), 0


def main():
    rng = random.Random(42)
    cases = []
    for shift in range(63):
        half = (1 << shift) // 2
        for quotient in (0, 1, 2, 3, 32766, 32767, 32768):
            for delta in (-1, 0, 1):
                value = (quotient << shift) + half + delta
                if 0 <= value < (1 << 63):
                    cases.extend(((value, shift), (-value, shift)))
        for value in (0, 1, -1, (1 << 62) - 1, -(1 << 62),
                      32767, 32768, -32768, -32769):
            cases.append((value, shift))
    cases.extend((rng.randrange(-(1 << 62), 1 << 62), rng.randrange(63))
                 for _ in range(4096))
    cases.extend(((-1, 63), (0, 63), (1, 63), (-(1 << 63), 0),
                  (-(1 << 63), 62)))
    for value in (-(1 << 31), -5, -3, -1, 0, 1, 3, 5, (1 << 31) - 1):
        for multiplier in (0, 1, 3, (1 << 31) - 1):
            for shift in range(63):
                output, fault = expected(value * multiplier, shift)
                actual = int(requantize(np.array(value), multiplier, shift,
                                        -32768, 32767))
                assert not fault and actual == output
    lines = []
    for tag, (value, shift) in enumerate(cases):
        output, fault = expected(value, shift)
        # [102:87] tag, [86] fault, [85:70] expected,
        # [69:64] shift, [63:0] signed product.
        word = ((tag << 87) | (fault << 86) | ((output & 65535) << 70)
                | (shift << 64) | (value & ((1 << 64) - 1)))
        lines.append(f"{word:032x}")
    content = "\n".join(lines) + "\n"
    (ROOT / "vectors.dath").write_text(content, encoding="ascii", newline="\n")
    report = {"cases": len(cases), "seed": 42,
              "reference_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "cross_checks_existing_requantize": 9 * 4 * 63,
              "vector_sha256": hashlib.sha256(content.encode()).hexdigest(),
              "oracle": "exact fractions.Fraction, nearest-even, int16 saturation",
              "scope": "Python only until corresponding RTL test passes"}
    (ROOT / "vectors.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
