#!/usr/bin/env python3
"""Bit-exact software reference for the current 32x32 RTL HOG front-end."""

from __future__ import annotations

import argparse
from pathlib import Path

ROI_SIZE = 32
FEATURE_COUNT = 64


def make_test_roi() -> list[list[int]]:
    """Return a deterministic texture that exercises all four direction bins."""
    return [
        [
            (x * 13 + y * 29 + ((x * y) & 31) * 5 +
             (96 if 7 <= x < 18 and 11 <= y < 25 else 0)) & 0xFF
            for x in range(ROI_SIZE)
        ]
        for y in range(ROI_SIZE)
    ]


def direction_bin(gx: int, gy: int) -> int:
    abs_gx = abs(gx)
    abs_gy = abs(gy)
    if 2 * abs_gy <= abs_gx:
        return 0
    if 2 * abs_gx <= abs_gy:
        return 2
    return 1 if (gx < 0) == (gy < 0) else 3


def extract_features(roi: list[list[int]]) -> tuple[list[int], list[int]]:
    """Match hog_sobel_gradient + hog_cell_histogram exactly."""
    features = [0] * FEATURE_COUNT
    bin_counts = [0] * 4

    for center_y in range(1, ROI_SIZE - 1):
        for center_x in range(1, ROI_SIZE - 1):
            left = (roi[center_y - 1][center_x - 1] +
                    2 * roi[center_y][center_x - 1] +
                    roi[center_y + 1][center_x - 1])
            right = (roi[center_y - 1][center_x + 1] +
                     2 * roi[center_y][center_x + 1] +
                     roi[center_y + 1][center_x + 1])
            upper = (roi[center_y - 1][center_x - 1] +
                     2 * roi[center_y - 1][center_x] +
                     roi[center_y - 1][center_x + 1])
            lower = (roi[center_y + 1][center_x - 1] +
                     2 * roi[center_y + 1][center_x] +
                     roi[center_y + 1][center_x + 1])
            gx = right - left
            gy = lower - upper
            magnitude = min(abs(gx) + abs(gy), 0x7FF)
            bin_index = direction_bin(gx, gy)
            cell_x = center_x >> 3
            cell_y = center_y >> 3
            feature_index = cell_y * 16 + cell_x * 4 + bin_index
            features[feature_index] += magnitude
            bin_counts[bin_index] += 1

    return features, bin_counts


def write_hex(path: Path, values: list[int], width: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    digits = (width + 3) // 4
    path.write_text(
        "".join(f"{value:0{digits}x}\n" for value in values),
        encoding="ascii",
    )


def read_hex(path: Path) -> list[int]:
    return [int(line.strip(), 16) for line in path.read_text(encoding="ascii").splitlines()
            if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true",
                        help="write deterministic ROI and expected feature files")
    parser.add_argument("--roi", type=Path, required=True)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--actual", type=Path)
    args = parser.parse_args()

    if args.generate:
        roi = make_test_roi()
        features, bin_counts = extract_features(roi)
        write_hex(args.roi, [pixel for row in roi for pixel in row], 8)
        write_hex(args.expected, features, 18)
        print("Generated ROI and 64 expected features; " +
              ", ".join(f"bin{i}={count}" for i, count in enumerate(bin_counts)))

    if args.actual is not None:
        expected = read_hex(args.expected)
        actual = read_hex(args.actual)
        if len(expected) != FEATURE_COUNT or len(actual) != FEATURE_COUNT:
            print(f"FAIL: feature count expected={len(expected)} actual={len(actual)}")
            return 1
        mismatches = [
            (index, exp, got)
            for index, (exp, got) in enumerate(zip(expected, actual))
            if exp != got
        ]
        if mismatches:
            for index, exp, got in mismatches[:10]:
                print(f"FAIL: feature[{index}] expected=0x{exp:05x} actual=0x{got:05x}")
            print(f"FAIL: {len(mismatches)} of {FEATURE_COUNT} features differ")
            return 1
        print("PASS: software and RTL HOG features match all 64 entries")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
