#!/usr/bin/env python3
"""Deterministic integer-floor oracle for the two registered requantizers."""
import argparse
from pathlib import Path
import random

BASE = Path(__file__).resolve().parents[1]
MIN_RAW, MAX_RAW = -(2**31), 2**31 - 1


def expected(raw, shift):
    scaled = raw // (2**shift)
    return max(-128, min(127, scaled)), int(scaled < -128 or scaled > 127), max(0, min(127, scaled))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=BASE / 'reports' / 'requant_unit_vectors')
    args = parser.parse_args()
    assert expected(-1, 1) == (-1, 0, 0)
    assert expected(-257, 1) == (-128, 1, 0)
    assert expected(-256, 1) == (-128, 0, 0)
    assert expected(255, 1) == (127, 0, 127)
    assert expected(256, 1) == (127, 1, 127)
    assert expected(MIN_RAW, 31) == (-1, 0, 0)
    assert expected(MAX_RAW, 31) == (0, 0, 0)
    rng = random.Random(20261024)
    cases = []
    addresses = [0, 1, 131071, 131072, 262142, 262143]
    for shift in range(32):
        factor = 2**shift
        raw_values = [MIN_RAW, MAX_RAW, -1, 0, 1]
        for boundary in [-128 * factor, 127 * factor, 128 * factor, -factor, factor]:
            raw_values.extend([boundary - 1, boundary, boundary + 1])
        raw_values.extend(rng.randint(MIN_RAW, MAX_RAW) for _ in range(8))
        for raw in dict.fromkeys(raw_values):
            if not MIN_RAW <= raw <= MAX_RAW:
                continue
            index = len(cases)
            addr = addresses[(index // 2) % 6] if index % 2 == 0 else rng.randrange(2**18)
            row = [0, 511, 255, 256, 1, 510][index % 6]
            col = [511, 0, 256, 255, 510, 1][index % 6]
            cases.append((raw, shift, addr, index % 4, row, col, *expected(raw, shift)))
    assert {case[1] for case in cases} == set(range(32))
    assert set(addresses) <= {case[2] for case in cases}
    assert {case[1] for case in cases if case[7]} == set(range(24))
    assert all(case[6] in (-1, 0) for case in cases if case[1] == 31)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    path = args.out_dir / 'cases.txt'
    path.write_text(str(len(cases)) + '\n' + '\n'.join(' '.join(map(str, case)) for case in cases) + '\n', encoding='ascii')
    print(f'PASS REQUANT_VECTORS cases={len(cases)} shifts=32 saturated={sum(case[7] for case in cases)} path={path}')


if __name__ == '__main__':
    main()
