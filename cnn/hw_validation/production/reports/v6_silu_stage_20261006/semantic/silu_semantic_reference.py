"""Small executable contract for the four SiLU VG122 arithmetic sites."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PIPELINE_VALID_STAGES = (
    "flag_input_valid",
    "flag_round_valid",
    "flag_value_valid",
    "flag_address_valid",
    "flag_ram_valid",
    "output_valid_o",
)


def lookup_address(raw_value: int) -> int:
    """Match the RTL floor quotient plus nearest-even increment and +512 bias."""
    quotient, remainder = divmod(raw_value, 4)
    increment = remainder == 3 or (remainder == 2 and quotient % 2 == 1)
    return quotient + int(increment) + 512


def next_pending(current: int, accepted: bool, consumed: bool) -> int:
    """Apply the DUT's accepted-minus-consumed conservation update."""
    return current + int(accepted) - int(consumed)


def next_table_expected(current: int, address: int) -> int:
    """Apply one accepted table transfer; address zero is always a restart."""
    if address == 0:
        return 1
    if address != current or address == 1023:
        return 0
    return current + 1


def derive() -> dict[str, object]:
    all_lookup = [lookup_address(raw) for raw in range(-32768, 32768)]
    central_pairs = [
        (raw, lookup_address(raw)) for raw in range(-2047, 2048)
    ]

    expected = 0
    reachable_table_expected = {expected}
    legal_writes = []
    for address in range(1024):
        legal_writes.append(address)
        expected = next_table_expected(expected, address)
        reachable_table_expected.add(expected)

    pending = 0
    reachable_pending = {pending}
    for _ in PIPELINE_VALID_STAGES:
        pending = next_pending(pending, True, False)
        reachable_pending.add(pending)
    pending = next_pending(pending, True, True)
    reachable_pending.add(pending)
    for _ in PIPELINE_VALID_STAGES:
        pending = next_pending(pending, False, True)
        reachable_pending.add(pending)

    result = {
        "pipeline_valid_stages": list(PIPELINE_VALID_STAGES),
        "pending_capacity": len(PIPELINE_VALID_STAGES),
        "pending_reachable": sorted(reachable_pending),
        "pending_update": "accepted - consumed; simultaneous transfer and stall hold",
        "reset_cancel_pending": 0,
        "table_expected_reachable_range": [
            min(reachable_table_expected),
            max(reachable_table_expected),
        ],
        "table_expected_max": max(reachable_table_expected),
        "table_expected_1024_reachable": 1024 in reachable_table_expected,
        "legal_table_write_range": [min(legal_writes), max(legal_writes)],
        "lookup_full_int16_range": [min(all_lookup), max(all_lookup)],
        "lookup_central_non_bypass_range": [
            min(address for _, address in central_pairs),
            max(address for _, address in central_pairs),
        ],
        "lookup_address_zero_raw_inputs": [
            raw for raw, address in central_pairs if address == 0
        ],
        "lookup_endpoint_1024_raw_inputs": [
            raw for raw, address in central_pairs if address == 1024
        ],
    }

    assert result["pending_capacity"] == 6
    assert result["pending_reachable"] == list(range(7))
    assert reachable_table_expected == set(range(1024))
    assert result["table_expected_max"] == 1023
    assert result["table_expected_1024_reachable"] is False
    assert result["legal_table_write_range"] == [0, 1023]
    assert result["lookup_full_int16_range"] == [-7680, 8704]
    assert result["lookup_central_non_bypass_range"] == [0, 1024]
    assert result["lookup_address_zero_raw_inputs"] == [-2047, -2046]
    assert result["lookup_endpoint_1024_raw_inputs"] == [2046, 2047]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = derive()
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("PY_PASS four_vg122_semantics_closed")


if __name__ == "__main__":
    main()
