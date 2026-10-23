#!/usr/bin/env python3
"""Generate deterministic row cases from the existing bit-exact Softmax model."""
from pathlib import Path
import random
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'lesson14_transformer_full' / 'reference'))
from softmax_fixed import LUT, approximate_exp_weights, softmax_fixed


def main():
    rom_file = BASE / 'lesson14_transformer_full' / 'rtl' / 'exp_lut_q16.hex'
    rom = tuple(int(word, 16) for word in rom_file.read_text(encoding='ascii').split())
    assert rom == LUT, 'RTL exponent ROM differs from the mathematical reference LUT'
    rng = random.Random(20261023)
    cases = [
        ('single_min_scale', [-2147483648], 1),
        ('extreme_pair_full_scale', [-2147483648, 2147483647], 65536),
        ('extreme_pair_min_scale', [2147483647, -2147483648], 1),
        ('equal_pair', [-17, -17], 65536),
        ('equal_max_row', [2147483647] * 64, 65536),
        ('bounded_full_scale', [rng.randint(-8, 8) for _ in range(64)], 65536),
        ('bounded_min_scale', [rng.randint(-200000, 200000) for _ in range(64)], 1),
        ('lut_clamp_boundary', [0, -1, -127, -128, -129, -130, -4096, -2147483648] * 8, 4096),
        ('mixed_extremes', [-2147483648, 2147483647, 0, -1] * 16, 65536),
    ]
    target = BASE / 'reports' / 'softmax_unit_vectors'
    target.mkdir(parents=True, exist_ok=True)
    lines = [str(len(cases))]
    for name, scores, scale in cases:
        expected = softmax_fixed(scores, scale)
        weights = approximate_exp_weights(scores, scale)
        assert len(expected) == len(scores) and all(0 <= value <= 255 for value in expected)
        lines.append(f'{len(scores)} {scale} {sum(weights)}')
        lines.extend(f'{score} {value}' for score, value in zip(scores, expected))
        print(f'{name}: len={len(scores)} scale={scale} sum_u8={sum(expected)}')
    (target / 'cases.txt').write_text('\n'.join(lines) + '\n', encoding='ascii')
    print(f'PASS SOFTMAX_VECTORS cases={len(cases)} lut_entries={len(rom)} path={target / "cases.txt"}')


if __name__ == '__main__':
    main()
