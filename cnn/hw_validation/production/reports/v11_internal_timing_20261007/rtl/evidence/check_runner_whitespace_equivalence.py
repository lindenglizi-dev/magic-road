"""Prove that the v11 runner change is whitespace-only."""
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT.parent / "v10_postprocess_overlap_20261007" / "rtl" / "down2_overlap_tile_runner.v"
CANDIDATE = ROOT / "rtl" / "down2_overlap_tile_runner.v"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_whitespace(path):
    return re.sub(r"\s+", "", path.read_text(encoding="utf-8"))


original_compact = without_whitespace(ORIGINAL)
candidate_compact = without_whitespace(CANDIDATE)
payload = {
    "status": "PASS" if original_compact == candidate_compact else "FAIL",
    "comparison": "all non-whitespace characters in order",
    "original_sha256": digest(ORIGINAL),
    "candidate_sha256": digest(CANDIDATE),
    "original_compact_sha256": hashlib.sha256(original_compact.encode()).hexdigest(),
    "candidate_compact_sha256": hashlib.sha256(candidate_compact.encode()).hexdigest(),
}
print(json.dumps(payload, sort_keys=True))
raise SystemExit(0 if payload["status"] == "PASS" else 1)
