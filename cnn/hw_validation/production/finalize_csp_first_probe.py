"""Recheck the retained CSP diagnostic receipts without rerunning simulation."""
import json
import re
from datetime import datetime
from pathlib import Path

from run_csp_first_probe import OUT, check_hashes, digest, validate_receipt


def load(name, root=OUT):
    return json.loads((root / name).read_text(encoding="utf-8"))


def main(root=OUT, count=10, validator=validate_receipt, gate_name="full_gate_with_tb.json", wrapper_source_checked=False):
    binding = load("input_binding.json", root)
    check_hashes(binding["original_sha256"])
    check_hashes(binding["staged_sha256"])
    status = load("status.json", root)
    if status["status"] != f"PASS_CSP_FIRST_LOCAL_PROBE_{count}_OF_{count}":
        raise ValueError("not a completed diagnostic simulation")
    cases = load("case_receipts.json", root)["cases"]
    if [case["case"] for case in cases] != list(range(count)):
        raise ValueError("incomplete case list")
    warnings = []
    for case in cases:
        text = (root / case["log"]).read_text(encoding="utf-8")
        if validator(case["case"], text) != case["receipt"]:
            raise ValueError("receipt/log disagreement")
        if re.search(r"\*\* (?:Error|Fatal):", text):
            raise ValueError("simulation error hidden by receipt")
        warnings.append(dict(case=case["case"], lines=[line for line in text.splitlines()
            if "Warning:" in line]))
    gate = load(gate_name, root)
    if set(gate["checks"]) != {"compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"}:
        raise ValueError("unexpected public gate schema")
    report = dict(as_of=datetime.now().astimezone().isoformat(),
        finalization_source_sha256=digest(Path(__file__)),
        diagnostic_cases_passed=count, input_hashes_rechecked=len(binding["original_sha256"]),
        staged_hashes_rechecked=len(binding["staged_sha256"]),
        strict_gate_errors=gate["errors"], strict_gate_warnings=gate["strict_warnings"],
        strict_gate_checks=gate["checks"], delivery_ready=gate["delivery_ready"],
        external_ModelSim_compile_errors=status["compile_errors"],
        external_ModelSim_compile_warnings=status["compile_warnings"],
        runtime_warnings=warnings, formal_acceptance=False,
        source_spec_crosscheck_passed=False,
        wrapper_source_spec_crosscheck_passed=wrapper_source_checked,
        testbench_source_spec_crosscheck_passed=False,
        source_spec_issue="wrapper source/port-name crosscheck recorded separately; TB documentation is no-source only, full source/spec closure remains unapproved",
        limits=["single top-left 4x4x12 first residual only", "host TB schedules groups and memory access",
            "native reads and write packing are TB checks, not RTL DMA or actual DDR",
            "no right/bottom/interior tile, next residual, whole network, physical timing or board evidence"],
        report_sha256={str(p.relative_to(root)): digest(p) for p in root.rglob("*")
            if p.is_file() and p.name != "execution_checks.json"})
    with (root / "execution_checks.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(f"DIAGNOSTIC_{count}_OF_{count} delivery_ready={gate['delivery_ready']} strict_errors={gate['errors']}")


if __name__ == "__main__":
    main()
