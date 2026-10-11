"""Fail closed unless the frozen physical source closure still matches."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "prebuild_manifest.json"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_entry(path_text: str, expected: str) -> None:
    path = Path(path_text) if ":/" in path_text else ROOT / path_text
    if not path.is_file() or digest(path) != expected:
        raise SystemExit(f"PREBUILD_MISMATCH {path}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
for entry in manifest["source_read_order"]:
    check_entry(entry["path"], entry["sha256"])
for name, expected_hash in manifest["flow_sha256"].items():
    check_entry(name.removesuffix("_prebuild"), expected_hash)
for name, expected_hash in manifest["functional_evidence_sha256"].items():
    check_entry(name, expected_hash)
for name, expected_hash in manifest["tool_sha256"].items():
    check_entry(name, expected_hash)
print("PASS physical prebuild source closure")
