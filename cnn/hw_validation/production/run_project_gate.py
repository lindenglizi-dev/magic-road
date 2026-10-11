"""Run original/fixed full gates and negative regressions in separate processes."""
from datetime import datetime, timezone
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
OVERLAY = ROOT / "checker_overlay"
PROBE = ROOT / "round_internal_probe"
RULES = ("vg_contract_liveness.py", "quality_gate_structure_rules.py")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regress(output):
    """Use real Verilog inputs and the existing formatter, not hand-built ASTs."""
    from scripts.python.quality.vg_semantic_facts import build_vg_facts
    from scripts.python.quality.vg_contract_liveness import evaluate_liveness_gate
    from scripts.python.quality.quality_gate_structure_rules import _region_rules
    from scripts.python.quality.formatter_ast import create_formatter_backend
    from scripts.python.quality.deliverable_gate import run_verilog_deliverable_gate
    backend = create_formatter_backend()
    def module(name, ports, body="", params=""):
        return f"module {name}{params}\n(\n{ports}\n);\n{body.replace(';', ';' + chr(10))}\nendmodule\n"

    parent = module("parent", "output [7:0] result", "wire [7:0] bus; {body} assign result=bus;")
    child = module("child", "output [7:0] value", "assign value=8'h35;")
    cases = {
        "known_output": (parent.format(body="child u(.value(bus));") + child, True),
        "real_undriven": (parent.format(body=""), False),
        "child_output_undriven": (parent.format(body="child u(.value(bus));") +
                                  module("child", "output [7:0] value"), False),
        "child_partial_bus": (parent.format(body="child u(.value(bus));") +
                              module("child", "output [7:0] value", "assign value[3:0]=4'h5;"), False),
        "local_partial_bus": (parent.format(body="assign bus[3:0]=4'h5;"), False),
        "child_internal_multidriver": (parent.format(body="child u(.value(bus));") +
            module("child", "output [7:0] value", "assign value=8'h35; assign value=8'h36;"), True),
        "input_not_driver": (parent.format(body="child u(.value(bus));") +
                             module("child", "input [7:0] value"), False),
        "unknown_module": (parent.format(body="unknown u(.value(bus));"), False),
        "partial_bus": (parent.format(body="child u(.value(bus[3:0]));") +
                        module("child", "output [3:0] value", "assign value=4'h3;"), False),
        "width_mismatch": (parent.format(body="child u(.value(bus));") +
                           module("child", "output [6:0] value", "assign value=7'h35;"), False),
        "parameter_width": (parent.format(body="child #(.WIDTH(7)) u(.value(bus));") +
                            module("child", "output [WIDTH-1:0] value", "assign value=0;",
                                   "\n#(\nparameter WIDTH=8\n)"), False),
        "two_child_drivers": (parent.format(body="child u(.value(bus)); child v(.value(bus));") + child, False),
        "local_and_child_driver": (parent.format(body="assign bus=8'h00; child u(.value(bus));") + child, False),
        "concatenated_actual": (parent.format(body="child u(.value({bus[7:4],bus[3:0]}));") + child, False),
        "inout_unresolved": (parent.format(body="child u(.value(bus));") +
                             module("child", "inout [7:0] value"), False),
        "positional_unresolved": (parent.format(body="child u(bus);") + child, False),
        "generated_unresolved": (parent.format(body="child u(.value(bus));") +
                                 module("child", "output [7:0] value",
                                        "generate\nif(1) begin : gen_data\nassign value=8'h35;\nend\nendgenerate"), False),
    }
    results = {}
    for name, (text, expected) in cases.items():
        # Fixtures use the upstream formatter's supported multiline instance form.
        for header in ("child u", "child v", "unknown u", "child #(.WIDTH(7)) u"):
            for actual in (".value(bus)", ".value(bus[3:0])",
                           ".value({bus[7:4],bus[3:0]})", "bus"):
                text = text.replace(header + "(" + actual + ");",
                                    header + "(\n" + actual + "\n);")
        text = text.replace(";", ";\n")
        text = text.replace(" u(", " source_Inst(").replace(" v(", " second_Inst(")
        fixture = output / "fixtures" / name
        fixture.mkdir(parents=True)
        (fixture / "input.v").write_text(text, encoding="utf-8")
        facts = build_vg_facts(fixture, include_testbench=False)
        assert not facts.parse_errors, name
        modules = [item for source in facts.sources for item in source.report.get("modules", [])]
        assert modules and modules[0].get("ports") and modules[0].get("decls"), name
        result = evaluate_liveness_gate(facts, "VG153")
        accepted = result.status == "passed"
        results[name] = {"expected_accept": expected, "actual_accept": accepted,
                         "passed": accepted == expected, "status": result.status,
                         "fixture_sha256": sha(fixture / "input.v")}
        if name == "child_internal_multidriver":
            full = run_verilog_deliverable_gate(fixture, strict=True, include_testbench=False)
            count = full["delivery_issues_by_rule"].get("VG141", 0)
            results["child_internal_multidriver_full_gate"] = {
                "passed": not full["delivery_ready"] and count > 0,
                "vg141_findings": count, "note": "VG153 is liveness; VG141 owns local multi-driver detection"}
    other = backend.REGION_TITLES["other_signal"]
    assign = backend.REGION_TITLES["other_assign"]
    regions = {
        "substring_titles": ([other, assign], True),
        "wrong_order": ([assign, other], False),
        "duplicate_banner": ([other, other], False),
        "ordinary_comment_not_banner": (["// 其他信号连线 其他信号"], False),
        "no_banner": (["wire signal;"], False),
    }
    module = {"counts": {"decls": 3}, "instances": []}
    for name, (lines, expected) in regions.items():
        issues = _region_rules("\n".join(lines), "fixture.v", module, strict=True)
        results[name] = {"expected_accept": expected, "actual_accept": not issues,
                         "passed": (not issues) == expected}
    missing_instance_region = _region_rules(other, "fixture.v",
        {"counts": {"decls": 3}, "instances": [{}]}, strict=True)
    results["missing_instance_banner"] = {
        "passed": any(issue.rule == "regions.instances_last" for issue in missing_instance_region)}
    for path in sorted((PROBE / "rtl").glob("*.v")):
        original = path.read_text(encoding="utf-8")
        formatted = backend.format_text(original, source_path=path)
        again = backend.format_text(formatted, source_path=path)
        results[path.stem + "_formatter_fixed_point"] = {
            "passed": formatted == again and formatted == original,
            "source_sha256": sha(path)}
    return results


def worker(mode, output):
    sys.path[:0] = ([str(OVERLAY)] if mode == "fixed" else []) + [str(SKILL)]
    from scripts.python.quality import vg_contract_liveness, quality_gate_structure_rules
    from scripts.python.quality.deliverable_gate import (
        run_verilog_deliverable_gate, write_verilog_deliverable_gate_report)
    regressions = regress(output) if mode == "fixed" else {}
    spec = json.loads((PROBE / "road_round_internal_probe.contract.json").read_text(encoding="utf-8"))
    gate = run_verilog_deliverable_gate(PROBE / "rtl", spec=spec, strict=True, include_testbench=False)
    write_verilog_deliverable_gate_report(gate, json_path=output / "gate.json", markdown_path=output / "gate.md")
    receipt = {"mode": mode, "python": sys.version, "origins": {
        module.__name__: {"path": module.__file__, "sha256": sha(Path(module.__file__))}
        for module in (vg_contract_liveness, quality_gate_structure_rules)},
        "regressions": regressions, "gate_errors": gate["errors"],
        "gate_strict_warnings": gate["strict_warnings"], "gate_ready": gate["delivery_ready"]}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"mode": mode, "errors": gate["errors"], "warnings": gate["strict_warnings"],
                      "regressions_passed": all(item["passed"] for item in regressions.values())}))
    return 0  # gate failure is evidence in the receipt, not a subprocess execution failure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=("original", "fixed"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        return worker(args.worker, args.output)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "reports" / ("checker_" + stamp)
    output.mkdir(parents=True, exist_ok=False)
    before = {path.name: sha(path) for path in (PROBE / "rtl").glob("*.v")}
    inputs = [*(PROBE / "rtl").glob("*.v"), PROBE / "road_round_internal_probe.contract.json",
              PROBE / "vectors.dath", PROBE / "vectors.json", PROBE / "reference.py",
              PROBE / "tb/tb_road_round_internal_probe.v"]
    snapshot = output / "inputs"
    for path in inputs:
        target = snapshot / path.relative_to(PROBE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    patch = []
    upstream = SKILL / "scripts/python/quality"
    fixed = OVERLAY / "scripts/python/quality"
    for name in RULES:
        patch.extend(difflib.unified_diff((upstream / name).read_text(encoding="utf-8").splitlines(True),
                     (fixed / name).read_text(encoding="utf-8").splitlines(True),
                     fromfile="original/" + name, tofile="fixed/" + name))
    (output / "checker.patch").write_text("".join(patch), encoding="utf-8")
    commands = {}
    for mode in ("original", "fixed"):
        target = output / mode
        target.mkdir()
        command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve()),
                   "--worker", mode, "--output", str(target)]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
        (target / "run.log").write_text(completed.stdout + completed.stderr, encoding="utf-8")
        commands[mode] = {"command": command, "returncode": completed.returncode,
                          "log_sha256": sha(target / "run.log")}
        if completed.returncode:
            raise RuntimeError(f"{mode} worker failed: {target / 'run.log'}")
    original = json.loads((output / "original/gate.json").read_text(encoding="utf-8"))
    revised = json.loads((output / "fixed/gate.json").read_text(encoding="utf-8"))
    receipt = json.loads((output / "fixed/receipt.json").read_text(encoding="utf-8"))
    difference = set(original["delivery_issues_by_rule"]) | set(revised["delivery_issues_by_rule"])
    unchanged = before == {path.name: sha(path) for path in (PROBE / "rtl").glob("*.v")}
    passed = (revised["delivery_ready"] and revised["errors"] == 0 and revised["strict_warnings"] == 0
              and all(case["passed"] for case in receipt["regressions"].values())
              and difference <= {"VG031", "VG153"} and unchanged)
    document = ROOT.parents[4] / "嵌赛_CNN验证问题分析与完整解决方案.md"
    report = {"status": "passed_project_checker" if passed else "blocked_checker_regression",
              "source_sha256": before, "source_unchanged": unchanged,
              "input_sha256": {path.relative_to(PROBE).as_posix(): sha(path) for path in inputs},
              "runner_sha256": sha(Path(__file__)),
              "overlay_sha256": {path.relative_to(OVERLAY).as_posix(): sha(path)
                                   for path in OVERLAY.rglob("*.py")},
              "build_contract": {"top": "road_round_internal_probe", "macros": [],
                                 "parameter_overrides": [], "extra_library_sources": [],
                                 "source_files": sorted(before), "silu_included": False},
              "principles": {"path": str(document), "sha256": sha(document)},
              "commands": commands, "patch_sha256": sha(output / "checker.patch"),
              "runtime_source_sha256": {str(path.relative_to(SKILL)): sha(path)
                    for path in (SKILL / "scripts").rglob("*.py")},
              "rule_configuration_sha256": {str(path.relative_to(SKILL)): sha(path)
                    for directory in (SKILL / "assets", SKILL / "config")
                    for path in directory.rglob("*.json")},
              "original_issues": original["delivery_issues_by_rule"],
              "fixed_issues": revised["delivery_issues_by_rule"],
              "fixed_gate_sha256": sha(output / "fixed/gate.json"),
              "regressions": receipt["regressions"], "matrix": revised["checks"],
              "scope": "Four-module rounding probe; no SiLU, RAM, TD, full CNN or board evidence",
              "limitations": ["Parameterized, positional, partial or generated output connections remain blocked",
                              "testbench/toolchain native gates not_requested; external evidence separate",
                              "Required documentation regeneration remains unresolved"]}
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(output / "report.json"),
                      "original": report["original_issues"], "fixed": report["fixed_issues"],
                      "failed_regressions": [name for name, item in receipt["regressions"].items()
                                             if not item["passed"]]}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
