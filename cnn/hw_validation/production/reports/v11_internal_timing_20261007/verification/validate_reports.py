"""Narrow structural validation for the final v11 verification artifacts."""
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
for name in ("elastic_contract.json", "deep_review.json", "turnaround_analysis.json",
             "cycle_budget.json", "hash_manifest.json", "verification_summary.json"):
    json.loads((HERE / name).read_text(encoding="utf-8"))

summary = json.loads((HERE / "verification_summary.json").read_text(encoding="utf-8"))
assert summary["status"] == "FUNCTIONAL_AND_LEGACY_REGRESSION_PASS"
assert summary["standalone_rtl"]["latency"] == "24 valid after NBA / 25 first transfer edge"
assert summary["runner_rtl"]["checked_intermediate_and_writeback_values"] == 640
assert summary["runner_rtl"]["no_stall_endpoint_cycles"] == 5433
assert json.loads((HERE / "hash_manifest.json").read_text(encoding="utf-8"))["all_copy_hashes_match"]
print("FINAL_REPORT_VALIDATION_PASS")
