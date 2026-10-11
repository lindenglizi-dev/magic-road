"""Generate shell-level vectors from the frozen signed33 MAC reference JSON."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "v7_mac_signed_accumulator_20261006" / "verification" / "signed33_vectors.json"
TABLE = HERE / "inputs" / "silu_table.hex"
CASE_IDS = (1, 2, 9, 10)


def pack_signed(values: list[int], bits: int) -> int:
    """Pack signed lane zero into the least-significant fixed-width field."""
    mask = (1 << bits) - 1
    return sum((value & mask) << (index * bits) for index, value in enumerate(values))


def round_even(value: int, shift: int) -> int:
    """Match the frozen nearest-even signed integer contract."""
    return round(Fraction(value, 1 << shift))


def feature(accumulator: int, channel: int, table: list[int]) -> int:
    """Apply the frozen fixed-factor pre, SiLU, and post transformations."""
    factors = (1, 3, 5)
    shifts = (0, 2, 4)
    pre = max(-32768, min(32767, round_even(accumulator * factors[channel], shifts[channel])))
    address = round_even(pre, 2) + 512
    if pre <= -2048:
        activated = 0
    elif pre >= 2048:
        activated = pre
    else:
        activated = 2047 if address == 1024 else table[address]
    return max(-128, min(127, round_even(activated, 4))) & 0xFF


def main() -> None:
    """Write four selected recovery, maximum, and final-fault case bundles."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    table_words = [int(word, 16) for word in TABLE.read_text(encoding="ascii").split()]
    table = [word - 65536 if word >= 32768 else word for word in table_words]
    case_by_id = {case["case_id"]: case for case in source["cases"]}
    vectors_by_id = {case_id: [] for case_id in CASE_IDS}
    for vector in source["vectors"]:
        if vector["case_id"] in vectors_by_id:
            vectors_by_id[vector["case_id"]].append(vector)
    for case_id in CASE_IDS:
        case = case_by_id[case_id]
        lines = []
        for vector in vectors_by_id[case_id]:
            activation = pack_signed(vector["activations"], 8)
            weight = sum(pack_signed(row, 8) << (output * 64) for output, row in enumerate(vector["weights"]))
            bias = pack_signed(vector["bias"], 32)
            lines.append(
                f"{int(vector['first'])} {int(vector['last'])} {vector['mask']:02x} "
                f"{activation:016x} {weight:048x} {bias:024x} 0 0 0 0 0 0 0"
            )
        (HERE / "inputs" / f"signed_case_{case_id}.txt").write_text("\n".join(lines) + "\n", encoding="ascii")
        expected = [0, 0, 0] if case["fault"] else [feature(value, channel, table) for channel, value in enumerate(case["final"])]
        (HERE / "inputs" / f"signed_case_{case_id}_expected.hex").write_text("\n".join(f"{value:02x}" for value in expected) + "\n", encoding="ascii")
    print("SIGNED_SHELL_VECTOR_PASS cases=1,2,9,10")


if __name__ == "__main__":
    main()
