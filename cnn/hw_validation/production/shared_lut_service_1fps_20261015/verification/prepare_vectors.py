"""Prepare test-only ROM words directly from the frozen G10 payload."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
ROM_WORD_BYTES = 20
ROM_WORDS = 7168
SIGMOID_OFFSET = 137_962
EXP_OFFSET = 140_010
SIGMOID_COUNT = 1024
EXP_COUNT = 256


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def table_values(payload: bytes, offset: int, count: int) -> list[int]:
    return [int.from_bytes(payload[offset + 2 * i : offset + 2 * i + 2], "little") for i in range(count)]


def render_words(payload: bytes) -> str:
    padded = payload + bytes(ROM_WORDS * ROM_WORD_BYTES - len(payload))
    # $readmemh writes the rightmost byte into bits 7:0, which is physical lane 0.
    return "".join(
        padded[start : start + ROM_WORD_BYTES][::-1].hex() + "\n"
        for start in range(0, len(padded), ROM_WORD_BYTES)
    )


def render_u16(values: list[int]) -> str:
    return "".join(f"{value:04x}\n" for value in values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify existing outputs without rewriting")
    args = parser.parse_args()

    verification = Path(__file__).resolve().parent
    project = verification.parents[4]
    payload_path = project / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package/numeric_test.bin"
    assets = verification / "assets"
    payload = payload_path.read_bytes()
    if sha256(payload_path) != PAYLOAD_SHA256:
        raise SystemExit("payload SHA-256 mismatch")
    if len(payload) > ROM_WORDS * ROM_WORD_BYTES:
        raise SystemExit("payload does not fit 7168x160 test ROM")

    outputs = {
        "physical_words_160.hex": render_words(payload),
        "sigmoid_expected_16.hex": render_u16(table_values(payload, SIGMOID_OFFSET, SIGMOID_COUNT)),
        "exp_expected_16.hex": render_u16(table_values(payload, EXP_OFFSET, EXP_COUNT)),
        "odd19_sigmoid_expected_16.hex": render_u16(table_values(payload, 19, SIGMOID_COUNT)),
        "odd39_exp_expected_16.hex": render_u16(table_values(payload, 39, EXP_COUNT)),
    }

    metadata = {
        "source": str(payload_path.relative_to(project)).replace("\\", "/"),
        "payload_bytes": len(payload),
        "payload_sha256": PAYLOAD_SHA256,
        "rom_word_bytes": ROM_WORD_BYTES,
        "rom_words": ROM_WORDS,
        "padding_bytes": ROM_WORDS * ROM_WORD_BYTES - len(payload),
        "sigmoid": {"offset": SIGMOID_OFFSET, "count": SIGMOID_COUNT},
        "exp": {"offset": EXP_OFFSET, "count": EXP_COUNT},
        "odd_relocation": {"sigmoid_offset": 19, "exp_offset": 39, "lane19_entries": 129},
        "inference_run": False,
    }
    outputs["input_receipt.json"] = json.dumps(metadata, indent=2) + "\n"

    if args.check:
        for name, content in outputs.items():
            target = assets / name
            if not target.is_file() or target.read_text(encoding="ascii") != content:
                raise SystemExit(f"stale or missing asset: {target}")
    else:
        assets.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (assets / name).write_text(content, encoding="ascii", newline="\n")

    print(
        "VECTOR_PREP_PASS "
        f"payload_bytes={len(payload)} rom_words={ROM_WORDS} sigmoid={SIGMOID_COUNT} exp={EXP_COUNT} inference=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
