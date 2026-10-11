"""Freeze deterministic internal-probe traffic with the production RNE oracle."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ROUND_REFERENCE = ROOT.parent / "round" / "reference.py"
SEED = 0x1D872B41C9E6A5F3
MASK64 = (1 << 64) - 1


def load_expected():
    spec = importlib.util.spec_from_file_location("production_round_reference", ROUND_REFERENCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("production round reference is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.expected


def signed_product(state: int) -> int:
    word = ((state >> 63) << 63) | ((state >> 63) << 62) | (state & ((1 << 62) - 1))
    return word - (1 << 64) if word >> 63 else word


def generate(count: int) -> tuple[list[str], dict[str, int]]:
    if not 1 <= count <= 65_536:
        raise ValueError("count must fit the 16-bit tag space")
    expected = load_expected()
    state = SEED
    checksum = 0
    valid_count = 0
    fault_count = 0
    lines = []
    for tag in range(count):
        product = signed_product(state)
        shift = tag & 63
        valid = int((tag & 7) != 0)
        result, fault = expected(product, shift)
        word = ((valid << 103) | (tag << 87) | (fault << 86)
                | ((result & 0xFFFF) << 70) | (shift << 64) | (product & MASK64))
        lines.append(f"{word:032x}")
        if valid:
            valid_count += 1
            fault_count += fault
            checksum ^= (fault << 32) | (tag << 16) | (0 if fault else result & 0xFFFF)
        feedback = ((state >> 63) ^ (state >> 62)) & 1
        state = ((state << 1) & MASK64) | feedback
    return lines, {"generated": count, "valid": valid_count, "faults": fault_count,
                   "checksum": checksum}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=192)
    args = parser.parse_args()
    lines, summary = generate(args.count)
    content = "\n".join(lines) + "\n"
    vector_path = ROOT / "vectors.dath"
    vector_path.write_text(content, encoding="ascii", newline="\n")
    report = {
        **summary,
        "seed": SEED,
        "oracle": "production/round/reference.py::expected",
        "reference_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "oracle_sha256": hashlib.sha256(ROUND_REFERENCE.read_bytes()).hexdigest(),
        "vector_sha256": hashlib.sha256(content.encode("ascii")).hexdigest(),
    }
    (ROOT / "vectors.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
