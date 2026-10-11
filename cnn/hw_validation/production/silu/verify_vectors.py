"""Audit the shared SiLU contract and export deterministic local RTL vectors."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np


THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parents[3]
GENERATED_DIR = THIS_DIR / "generated"
SOURCE_TABLE = PROJECT_ROOT / "cnn" / "artifacts" / "shared_tables_v2" / "silu.hex"
EXPECTED_INTEGER_HASH = "441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040"
EXPECTED_TABLE_HASH = "05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6"

sys.path.insert(0, str(PROJECT_ROOT))
from cnn import integer  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words_to_hex(values: np.ndarray) -> str:
    return "".join(f"{int(value) & 0xffff:04x}\n" for value in values)


def rtl_address(raw: int) -> int:
    """Mirror the RTL arithmetic-shift RNE quotient for signed divide by four."""
    quotient = raw >> 2
    remainder = raw & 3
    increment = remainder == 3 or (remainder == 2 and (quotient & 1) == 1)
    return quotient + int(increment) + 512


def rtl_reference(raw: int, table: np.ndarray) -> int:
    if raw <= -2048:
        return 0
    if raw >= 2048:
        return raw
    address = rtl_address(raw)
    if address == 1024:
        return 2047
    return int(table[address])


def main() -> None:
    integer_path = PROJECT_ROOT / "cnn" / "integer.py"
    if sha256(integer_path) != EXPECTED_INTEGER_HASH:
        raise RuntimeError("cnn/integer.py hash changed; re-review the numeric authority")
    if sha256(SOURCE_TABLE) != EXPECTED_TABLE_HASH:
        raise RuntimeError("published silu.hex hash changed; re-review the table authority")

    source_words = np.array(
        [int(line, 16) for line in SOURCE_TABLE.read_text(encoding="ascii").splitlines()],
        dtype=np.uint16,
    ).view(np.int16)
    model_words = np.asarray(integer.tables()["silu"], dtype=np.int16)
    if source_words.shape != (1024,) or not np.array_equal(source_words, model_words):
        raise AssertionError("published table differs from cnn.integer.tables()['silu']")
    if int(integer.tables()["silu_upper"]) != 2047:
        raise AssertionError("hardwired upper endpoint changed")

    domain = np.arange(-32768, 32768, dtype=np.int64)
    golden = integer.silu(domain).astype(np.int16)
    mirrored = np.array([rtl_reference(int(raw), source_words) for raw in domain], dtype=np.int16)
    if not np.array_equal(golden, mirrored):
        mismatch = int(np.flatnonzero(golden != mirrored)[0])
        raise AssertionError(f"RTL-formula mismatch at raw={mismatch - 32768}")

    expected_asset = PROJECT_ROOT / "cnn" / "artifacts" / "shared_tables_v2" / "silu_golden.hex"
    if words_to_hex(golden).encode("ascii") != expected_asset.read_bytes():
        raise AssertionError("published exhaustive golden differs from cnn.integer.silu")

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    local_table = GENERATED_DIR / "silu_table.hex"
    local_golden = GENERATED_DIR / "silu_expected.hex"
    local_table.write_text(words_to_hex(source_words), encoding="ascii", newline="\n")
    local_golden.write_text(words_to_hex(golden), encoding="ascii", newline="\n")

    report = {
        "status": "passed",
        "input_codes_checked": 65536,
        "table_words_checked": 1024,
        "integer_source_sha256": sha256(integer_path),
        "source_table_sha256": sha256(SOURCE_TABLE),
        "local_table_sha256": sha256(local_table),
        "local_expected_sha256": sha256(local_golden),
        "silu_upper": 2047,
        "address_examples": {
            "raw_minus_2047": rtl_address(-2047),
            "raw_minus_2_tie": rtl_address(-2),
            "raw_plus_2_tie": rtl_address(2),
            "raw_plus_2047": rtl_address(2047),
        },
    }
    report_path = GENERATED_DIR / "python_vector_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
