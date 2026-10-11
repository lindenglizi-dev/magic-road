"""Verify the final v10 physical evidence manifest without modifying the baseline."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


manifest = json.loads((ROOT / "physical_evidence_manifest.json").read_text(encoding="utf-8"))
status = json.loads((ROOT / "physical_status.json").read_text(encoding="utf-8"))
failures = []

for section in ("sources", "functional_evidence", "implementation_databases",
                "primary_raw_reports", "guard_receipts", "derived_reports"):
    for name, expected in manifest[section].items():
        path = (ROOT / name).resolve()
        if not path.is_file():
            failures.append(f"missing {section}:{name}")
        elif digest(path) != expected:
            failures.append(f"hash {section}:{name}")

frozen = ROOT.parent / "frozen_previous.json"
if digest(frozen) != manifest["frozen_previous_manifest_sha256"]:
    failures.append("frozen_previous_manifest_sha256")
if status["status"] != manifest["status"]:
    failures.append("status mismatch")
if status["build_rerun"] or status["bitstream_generated"]:
    failures.append("forbidden flow action recorded")
if status["timing"]["setup_internal"] != 7:
    failures.append("internal setup classification")
if status["timing"]["hold_path_records"] + status["timing"]["removal_path_records"] != 233:
    failures.append("min-check classification")

if failures:
    raise SystemExit("FAIL physical evidence: " + ", ".join(failures))
print("PASS physical evidence manifest")
