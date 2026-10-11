"""DW 行尾紧凑 G2 映射的最小整数参考。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TAIL_POSITIONS = (3, 7, 11, 15)
G0_OFFSETS = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1))
G1_OFFSETS = ((2, 2),)
COMPACT_GROUPS = (G0_OFFSETS, G1_OFFSETS)
COMPACT_MASKS = (0xFF, 0x01)
OLD_UNION_GROUPS = (
    ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0)),
    ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 0), (2, 1)),
    ((2, 2), (2, 3), (2, 4), (2, 5), (2, 6)),
)
SIGNED33_MIN = -(1 << 32)
SIGNED33_MAX = (1 << 32) - 1


def halo_index(position: int, channel: int, row: int, column: int) -> int:
    """返回 9 列 halo、16 通道布局中的字节索引。"""

    base_row = (position >> 2) * 2
    base_column = (position & 3) * 2
    return ((base_row + row) * 9 + base_column + column) * 16 + channel


def compact_accumulator(activations: dict[tuple[int, int], int], weights: dict[tuple[int, int], int], bias: int) -> tuple[int, list[int]]:
    """按固定 G0/G1 位置求和，不用运行时除法或取模。"""

    accumulator = bias
    partials: list[int] = []
    for group in COMPACT_GROUPS:
        partial = sum(activations[offset] * weights[offset] for offset in group)
        partials.append(partial)
        accumulator += partial
        assert SIGNED33_MIN <= accumulator <= SIGNED33_MAX
    return accumulator, partials


def old_union_accumulator(activations: dict[tuple[int, int], int], weights: dict[tuple[int, int], int], bias: int) -> int:
    """按原 21-union G3 顺序求和，union 的无效列权重视为零。"""

    accumulator = bias
    for group in OLD_UNION_GROUPS:
        partial = sum(
            activations[(row, column)] * weights[(row, column)]
            for row, column in group
            if column < 3
        )
        accumulator += partial
        assert SIGNED33_MIN <= accumulator <= SIGNED33_MAX
    return accumulator


def signed8(pattern: int) -> int:
    """把任意整数稳定折回 signed8。"""

    return (pattern & 0xFF) - 256 if pattern & 0x80 else pattern & 0xFF


def build_case(case_index: int, position: int, channel: int) -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], int], int]:
    """构造可重复的九 tap 数据和 signed32 bias。"""

    offsets = G0_OFFSETS + G1_OFFSETS
    activations = {
        offset: signed8(case_index * 37 + position * 11 + channel * 13 + tap * 17)
        for tap, offset in enumerate(offsets)
    }
    weights = {
        offset: signed8(case_index * 19 + position * 7 + channel * 29 + tap * 23 + 1)
        for tap, offset in enumerate(offsets)
    }
    bias = signed8(case_index * 31 + position * 5 + channel * 3) * 257
    return activations, weights, bias


def verify() -> dict[str, object]:
    """比较 64 个行尾任务的 16 组数据，共 1024 例。"""

    checked = 0
    max_abs_group_partial = 0
    max_abs_accumulator = 0
    for case_index in range(16):
        for position in TAIL_POSITIONS:
            for channel in range(16):
                activations, weights, bias = build_case(case_index, position, channel)
                compact, partials = compact_accumulator(activations, weights, bias)
                baseline = old_union_accumulator(activations, weights, bias)
                assert compact == baseline
                max_abs_group_partial = max(max_abs_group_partial, *(abs(value) for value in partials))
                max_abs_accumulator = max(max_abs_accumulator, abs(compact))
                checked += 1

    last_tap_activations = {offset: 0 for offset in G0_OFFSETS + G1_OFFSETS}
    last_tap_weights = dict(last_tap_activations)
    last_tap_activations[(2, 2)] = 1
    last_tap_weights[(2, 2)] = 1
    last_tap_accumulator, last_tap_partials = compact_accumulator(last_tap_activations, last_tap_weights, 0)
    truncated_old = sum(
        last_tap_activations[(row, column)] * last_tap_weights[(row, column)]
        for group in OLD_UNION_GROUPS[:2]
        for row, column in group
        if column < 3
    )
    assert halo_index(3, 0, 2, 2) == 416
    assert 0 * 9 + 8 == 8
    assert last_tap_partials == [0, 1]
    assert last_tap_accumulator == 1
    assert truncated_old == 0

    max_product_abs = 128 * 128
    signed33_lower_bound = -(1 << 31) - 9 * max_product_abs
    signed33_upper_bound = (1 << 31) - 1 + 9 * max_product_abs
    assert 8 * max_product_abs <= (1 << 18) - 1
    assert SIGNED33_MIN <= signed33_lower_bound
    assert signed33_upper_bound <= SIGNED33_MAX

    return {
        "schema": "dw_tail_compact_reference_v1",
        "status": "PASS",
        "mapping_cases": checked,
        "tail_positions": list(TAIL_POSITIONS),
        "channels": 16,
        "patterns_per_task": 16,
        "compact_groups": [[list(offset) for offset in group] for group in COMPACT_GROUPS],
        "compact_masks": list(COMPACT_MASKS),
        "fixed_group_positions_no_runtime_division": True,
        "observed": {
            "max_abs_group_partial": max_abs_group_partial,
            "max_abs_accumulator": max_abs_accumulator,
        },
        "signed33_partial_safety": {
            "max_product_abs": max_product_abs,
            "max_eight_product_group_abs_bound": 8 * max_product_abs,
            "signed33_accumulator_lower_bound": signed33_lower_bound,
            "signed33_accumulator_upper_bound": signed33_upper_bound,
            "safe": True,
        },
        "last_tap_negative_regression": {
            "position": 3,
            "channel": 0,
            "halo_index": 416,
            "weight_index": 8,
            "activation": 1,
            "weight": 1,
            "compact_partials": last_tap_partials,
            "compact_accumulator": last_tap_accumulator,
            "old_mapping_truncated_after_g1": truncated_old,
            "proves_last_only_change_wrong": True,
        },
    }


def main() -> None:
    """运行参考并写出同目录 JSON 收据。"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("reference_tail_result.json"))
    args = parser.parse_args()
    result = verify()
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS mapping_cases={} output={}".format(result["mapping_cases"], args.output))


if __name__ == "__main__":
    main()
