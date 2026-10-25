"""原算术的小整数参考和单任务退休检查；不改冻结核或模型包。"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parents[2] / "feature_blocks_shared_20261015" / "frozen_attempt2"
TABLE = FROZEN / "reference/csp2/parameters/silu.hex"


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def rne(value, shift):
    assert 0 <= shift <= 62
    if not shift:
        return value
    quotient, remainder = divmod(abs(value), 1 << shift)
    quotient += remainder > (1 << (shift - 1)) or (remainder == (1 << (shift - 1)) and quotient & 1)
    return -quotient if value < 0 else quotient


def sat(value, bits):
    return min((1 << (bits - 1)) - 1, max(-(1 << (bits - 1)), value))


def silu(value, table):
    if value < -2048:
        return 0
    if value > 2048:
        return value
    index = rne(value, 2) + 512
    return 2047 if index == 1024 else table[index]


def evaluate(groups, bias, multipliers, shifts, post_multiplier, post_shift, activate, table):
    acc = list(bias)
    for activation, weight, mask in groups:
        for lane in range(3):
            acc[lane] += sum(activation[i] * weight[lane][i] for i in range(8) if mask >> i & 1)
    assert all(-(1 << 31) <= item < (1 << 31) for item in acc)
    pre = [sat(rne(a * m, s), 16) for a, m, s in zip(acc, multipliers, shifts)]
    activation = [silu(item, table) for item in pre] if activate else []
    post = [sat(rne(item * post_multiplier, post_shift), 16) for item in activation]
    return dict(acc=acc, pre=pre, silu=activation, post=post,
                output=[sat(item, 8) for item in post] if activate else pre)


def retire(remaining, tags, tag, raw, activate, data):
    matches = sum(1 << lane for lane in range(3) if remaining >> lane & 1 and tags[lane] == tag)
    assert matches in (1, 2, 4), "unowned or repeated tag"
    assert raw == (not activate), "wrong output type"
    assert not activate or -128 <= data <= 127, "INT8 not sign extended"
    return remaining & ~matches


def self_check():
    assert [rne(v, 1) for v in (-5, -3, -1, 1, 3, 5)] == [-2, -2, 0, 0, 2, 2]
    assert [sat(v, 16) for v in (-40000, 0, 40000)] == [-32768, 0, 32767]
    left = 7
    for tag in (37, 71, 109):
        left = retire(left, [37, 71, 109], tag, True, False, -400)
    assert left == 0
    for tag, raw, data in ((37, False, 0), (999, True, 0), (37, True, 0)):
        try:
            retire(6, [37, 71, 109], tag, raw, False, data)
        except AssertionError:
            pass
        else:
            raise AssertionError("bad owner output accepted")
    table = [signed(int(line, 16), 16) for line in TABLE.read_text().splitlines()]
    assert len(table) == 1024
    assert silu(-2049, table) == 0 and silu(2049, table) == 2049
    return table


if __name__ == "__main__":
    self_check()
    print("OWNER_REFERENCE_PASS rne/saturation/table/retirement")
