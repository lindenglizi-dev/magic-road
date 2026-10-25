"""Prepare deterministic RTL vectors from the saved postprocess golden artifacts.

This script performs no CNN inference.  It only checks and indexes existing
heads/DECODED160 files and exports the shared numeric LUT contents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
GOLDEN = ROOT / "cnn/hw_validation/production/postprocess_golden_2fps_20261015"
ASSETS = HERE / "assets"
PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
MODEL_ID = "B35D4A66"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(path: Path) -> int:
    with path.open("r", encoding="ascii") as stream:
        return sum(1 for line in stream if line.strip())


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def render_hex(values: list[int]) -> str:
    return "".join(f"{value:04x}\n" for value in values)


def case_entry(name: str) -> dict:
    folder = GOLDEN / "artifacts" / name
    heads = folder / "heads_cell_order_112.hex"
    decoded = folder / "top128_decoded_160.hex"
    sorted_rows = read_jsonl(folder / "top128_sorted.jsonl")
    counts = [sum(row["label"] == label for row in sorted_rows) for label in (0, 1)]
    if line_count(heads) != 12096:
        raise ValueError(f"{name}: heads line count is not 12096")
    if line_count(decoded) != sum(counts):
        raise ValueError(f"{name}: DECODED160 count disagrees with sorted metadata")
    return {
        "name": name,
        "heads": relative(heads),
        "decoded160": relative(decoded),
        "person_count": counts[0],
        "vehicle_count": counts[1],
        "heads_sha256": sha256(heads),
        "decoded160_sha256": sha256(decoded),
    }


def build_outputs() -> dict[Path, str]:
    manifest = json.loads((GOLDEN / "delivery_manifest.json").read_text(encoding="utf-8"))
    if manifest["payload_sha256"] != PAYLOAD_SHA256:
        raise ValueError("saved golden payload identity changed")

    boundary_path = GOLDEN / "boundary_vectors.json"
    boundary = json.loads(boundary_path.read_text(encoding="utf-8"))
    names = ["real_image"] + [case["name"] for case in boundary["pipeline_cases"]]

    sys.path.insert(0, str(ROOT))
    from cnn.integer import tables  # pylint: disable=import-outside-toplevel

    numeric = tables()
    sigmoid = [int(value) for value in numeric["sigmoid"]]
    exponent = [int(value) for value in numeric["exp"]]
    if len(sigmoid) != 1024 or len(exponent) != 256:
        raise ValueError("shared LUT dimensions changed")

    cases = [case_entry(name) for name in names]
    cases_manifest = {
        "schema": 1,
        "scope": "saved vectors only; no CNN inference or training",
        "payload_sha256": PAYLOAD_SHA256,
        "model_id32": MODEL_ID,
        "boundary_vectors_sha256": sha256(boundary_path),
        "lut_source": relative(ROOT / "cnn/integer.py"),
        "cases": cases,
    }
    outputs = {
        ASSETS / "sigmoid_lut_16.hex": render_hex(sigmoid),
        ASSETS / "exp_lut_16.hex": render_hex(exponent),
        ASSETS / "cases.json": json.dumps(cases_manifest, ensure_ascii=False, indent=2) + "\n",
    }
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify generated files without changing them")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check:
        mismatches = [str(path) for path, text in outputs.items()
                      if not path.is_file() or path.read_text(encoding="utf-8") != text]
        if mismatches:
            print("VECTOR_CHECK_FAIL " + " ".join(mismatches))
            return 1
        print("VECTOR_CHECK_PASS cases=11 sigmoid=1024 exp=256 inference=0")
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    print("VECTOR_PREP_PASS cases=11 sigmoid=1024 exp=256 inference=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
