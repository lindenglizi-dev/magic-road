"""Check final branch receipts against files and raw violation types, without waivers."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_hashes(base, entries):
    for name, expected in entries.items():
        with (base / name).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        assert actual == expected, (base / name, expected, actual)
    return len(entries)


def main():
    root = Path(__file__).resolve().parent
    physical = root / "physical"
    receipt = read(physical / "physical_validation_receipt.json")
    checked = verify_hashes(physical, receipt["artifacts"])
    checked += verify_hashes(physical, receipt["external_read_only_evidence"])
    status = read(physical / "physical_status.json")
    assert status["overall_status"] == "DIAGNOSTIC_COMPLETE_SIGNOFF_FAIL"
    assert status["sta"]["setup_wns_ns"] == 0.090
    assert status["sta"]["min_wns_ns"] == -0.950
    assert status["sta"]["min_violating_endpoints"] == 34
    violations = (physical / "full_20000_violations.timing").read_text(encoding="utf-8")
    types = Counter(re.findall(r"^Check Type\s*:\s*(\w+)", violations, re.MULTILINE))
    assert types == {"hold": 31, "removal": 3}, types
    checks = (physical / "fresh2_check_timing_verbose.rpt").read_text(encoding="utf-8")
    assert "There is 1 local clock" in checks
    assert "There is 1 generated clock that is not connected to its master clock" in checks
    assert not receipt["assertions"]["timing_exceptions_added"]
    assert not receipt["assertions"]["ignored_paths_present"]
    assert not receipt["assertions"]["bitgen_invoked"]

    reset = root / "reset"
    hashes = read(reset / "SOURCE_AND_VECTOR_HASHES.json")
    for section in ("candidate", "frozen_rtl", "vendor_simulation_models", "final_functional_evidence"):
        checked += verify_hashes(reset, hashes[section])
    checked += verify_hashes(reset / hashes["frozen_vector_source"], hashes["frozen_vectors"])
    for name, marker in (("modelsim_reset_run.log", "TB_PASS_RESET cases=6 errors=0"),
                         ("modelsim_regression_run.log", "TB_PASS_LOW_IO cases=14 errors=0")):
        assert marker in (reset / name).read_text(encoding="utf-8")

    layers = root / "layers"
    layer_receipt = read(layers / "validation_receipt.json")
    checked += verify_hashes(layers, {
        "modelsim_compile_final.log": layer_receipt["compile"]["log_sha256"],
        "modelsim_run_complete.log": layer_receipt["simulation"]["log_sha256"],
        "strict_gate.json": layer_receipt["strict_gate"]["json_sha256"],
        "strict_gate.md": layer_receipt["strict_gate"]["markdown_sha256"]})
    inputs = root.parent / "v7_onchip_chain_20261006/inputs"
    for name, expected in layer_receipt["source_hashes"].items():
        if name == "graph.json":
            path = root.parent.parent / "graph_artifacts/graph.json"
        elif name == "model.py":
            path = root.parents[3] / "model.py"
        elif (layers / name).is_file():
            path = layers / name
        else:
            path = inputs / name
        checked += verify_hashes(path.parent, {path.name: expected})
    assert not layer_receipt["strict_gate"]["delivery_ready"]
    assert layer_receipt["strict_gate"]["errors"] == 319
    result = {"status": "STAGE_EVIDENCE_CONSISTENCY_PASS_NOT_SIGNOFF",
              "hashes_checked": checked, "raw_violation_types": dict(types),
              "clock_definition_warnings_retained": True,
              "delivery_ready": False}
    (root / "stage_evidence_audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
