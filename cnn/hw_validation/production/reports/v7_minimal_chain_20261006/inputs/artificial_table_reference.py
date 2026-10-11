"""Deterministic contract for the isolated SiLU physical probe."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SAMPLES = (
    -4096, -2048, -2047, -7, -6, -5, -4, -3, -2,
    -1, 0, 1, 2, 3, 4, 2047, 2048, 4096,
)


def round_divide_by_four(value: int) -> int:
    """Match the DUT's signed floor quotient plus round-to-nearest-even step."""

    quotient, remainder = divmod(value, 4)
    if remainder > 2 or (remainder == 2 and quotient & 1):
        quotient += 1
    return quotient


def expected(value: int) -> int:
    """Apply the frozen probe table and the DUT's two bypass regions."""

    if value <= -2048:
        return 0
    if value >= 2048:
        return value
    address = round_divide_by_four(value) + 512
    if address == 1024:
        return 2047
    if not 0 <= address < 1024:
        raise AssertionError("central lookup escaped the 1024-entry table")
    return address - 512


def signed_extend_16(value: int) -> int:
    """Return the 32-bit bit pattern used by the RTL checksum."""

    value &= 0xFFFF
    return value | 0xFFFF0000 if value & 0x8000 else value


def main() -> None:
    results = [expected(value) for value in SAMPLES]
    checksum = 0
    for index, value in enumerate(results):
        checksum ^= signed_extend_16(value) ^ index
    report = {
        "samples": list(SAMPLES),
        "expected": results,
        "count": len(results),
        "checksum_hex": f"0x{checksum:08X}",
        "table": "entry[address] = signed(address) - 512 for address 0..1023",
        "coverage": ["table load", "central lookup", "negative bypass", "positive bypass", "continuous input", "output backpressure"],
        "scope": "probe traffic contract only; no TD, silicon, full-CNN, training, or board claim",
        "reference_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT / "contract_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
