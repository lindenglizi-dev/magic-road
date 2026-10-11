"""汇总同源对拍及实际物理证据，保留外部时序和严格门禁未签核。"""
from collections import Counter
import csv
import difflib
import json
import re
from pathlib import Path

from run import ROOT, PREV, FROZEN_PW, CORE, OLD_CORE, RUNNER, TB, tools, frozen

PATH = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                  r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)\s+Process\s+:\s+(\w+)")


def paths(path):
    return [{"slack": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner, "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in PATH.findall(path.read_text(encoding="utf-8"))]


def main():
    frozen()
    physical = ROOT / "physical_opt"
    area = (physical / "shell_route.area").read_text(encoding="utf-8")
    resources = {name: int(re.search(r"(?m)^#"+name+r"\s+(\d+)", area)[1])
                 for name in ("slice", "dsp", "eram", "IO", "reg")}
    timing = {}
    for name in ("internal_reg_to_reg", "functional_reset_distribution", "reset_sync_interstage",
                 "external_reset_entry", "dsp_all", "eram_all", "dsp_inputs_all", "eram_inputs_all"):
        rows = paths(physical / (name + ".timing"))
        timing[name] = {"paths": len(rows), "minima": {kind: min(row["slack"] for row in rows if row["kind"]==kind)
            for kind in sorted({row["kind"] for row in rows})},
            "internal_minima": {kind: min(row["slack"] for row in rows if row["kind"]==kind and not row["external"])
                for kind in sorted({row["kind"] for row in rows if not row["external"]})},
            "negative": [row for row in rows if row["slack"]<0]}
    negative = [row for row in paths(physical / "coverage_100000_violations.timing") if row["slack"]<0]
    gates = max((path for path in ROOT.glob("gates*") if (path / "comparison.json").exists()),
                key=lambda path: (path / "comparison.json").stat().st_mtime_ns)
    cycles = {}
    for label in ("baseline", "candidate"):
        work = max((path for path in ROOT.glob(label+"*") if (path / "receipt.json").exists()),
                   key=lambda path: (path / "receipt.json").stat().st_mtime_ns)
        cycles[label] = {}
        for path in sorted(work.glob("*.csv")):
            rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(path.open(encoding="utf-8"))]
            assert len(rows)==10
            for row in rows:
                assert sum(row[key] for key in ("writeback_stall", "capacity_wait", "commit_cycle", "mac_issue",
                    "input_wait", "task_close", "drain", "other"))==row["endpoint"]
                assert row["dw_endpoint"]+row["pw_endpoint"]==row["endpoint"]
                assert all(row[key]==640 for key in ("acc", "pre", "silu", "post", "commit"))
                assert row["export"]==384 and row["pw_firsts"]==128
                assert sum(row[key] for key in ("pw_idle", "pw_storage", "pw_send", "pw_wait", "pw_dw_drain",
                    "pw_drain", "pw_done", "pw_fault", "pw_export", "pw_dw_post"))==row["pw_endpoint"]
            cycles[label][path.stem] = rows
    old = (FROZEN_PW / "rtl/down2_dynamic_tile_runner.v").read_text(encoding="utf-8").splitlines(True)
    new = RUNNER.read_text(encoding="utf-8").splitlines(True)
    (ROOT / "runner.patch").write_text("".join(difflib.unified_diff(old, new,
        fromfile="frozen_pw_prefetch_runner", tofile="mac_task_stream_runner")), encoding="utf-8")
    old_mac = OLD_CORE[0].read_text(encoding="utf-8")
    new_mac = CORE[0].read_text(encoding="utf-8")
    arithmetic_marker = "\t//-------------主要任务处理区域-------------//"
    assert old_mac.split(arithmetic_marker)[1] == new_mac.split(arithmetic_marker)[1]
    assert old_mac.split("\tassign base_alpha")[1].split("\t//---------------输出信号连线")[0] == new_mac.split(
        "\tassign base_alpha")[1].split("\t//---------------输出信号连线")[0]
    (ROOT / "mac.patch").write_text("".join(difflib.unified_diff(old_mac.splitlines(True), new_mac.splitlines(True),
        fromfile="frozen_mac", tofile="four_credit_mac")), encoding="utf-8")
    result = {"status": "FUNCTION_PASS_INTERNAL_TIMING_FAILED" if any(not row["external"] for row in negative)
              else "FUNCTION_AND_INTERNAL_TIMING_PASS_NOT_DEPLOYMENT_RELEASE",
        "release": False, "parameter_origin": "TEST_NOT_QAT", "resources_including_shell": resources,
        "timing": timing, "negative_categories": dict(Counter(("external_" if row["external"] else "internal_")+
            row["kind"] for row in negative)), "violations": negative, "cycles": cycles,
        "strict_comparison": json.loads((gates / "comparison.json").read_text(encoding="utf-8")),
        "strict_states": {key: value["status"] for key, value in json.loads(
            (gates / "candidate.json").read_text(encoding="utf-8"))["checks"].items()},
        "testbench_strict": {key: value for key, value in json.loads(
            (gates / "testbench.json").read_text(encoding="utf-8")).items() if key in (
                "errors", "strict_warnings", "checks", "delivery_ready")},
        "arithmetic_A0_A5_source_unchanged": True,
        "new_runner_undriven": json.loads((ROOT / "z_attempt3/receipt.json").read_text(encoding="utf-8")),
        "shell_rtl": json.loads((ROOT / "shell_rtl_attempt3/receipt.json").read_text(encoding="utf-8")),
        "shell_gate": json.loads((ROOT / "shell_gate_attempt3/receipt.json").read_text(encoding="utf-8")),
        "shell_routed_opt": json.loads((ROOT / "shell_routed_opt/receipt.json").read_text(encoding="utf-8")),
        "mac_standalone": json.loads((ROOT / "mac_sim_attempt3/receipt.json").read_text(encoding="utf-8")),
        "checker_replay": json.loads((ROOT / "checker_replay_final/report.json").read_text(encoding="utf-8")),
        "netlist_warnings": json.loads((ROOT / "analysis/final_netlist_warning_summary.json").read_text(encoding="utf-8")),
        "external_interface_signed_off": False, "whole_network_verified": False,
        "reset_ready": "1 during reset; original sequential reset cancels all acceptance",
        "physical_strategy": json.loads((physical / "strategy.json").read_text(encoding="utf-8")),
        "layer_budget": json.loads((ROOT / "layer_budget.json").read_text(encoding="utf-8")),
        "frozen": json.loads((ROOT / "frozen_check.json").read_text(encoding="utf-8")),
        "physical_source_manifest": json.loads((physical / "input_manifest.json").read_text(encoding="utf-8")),
        "td_sha256": tools.digest(tools.TD)}
    result["strict_project_errors"] = result["checker_replay"]["modes"]["candidate"]["replay"]["errors"]
    assert all(tools.digest(Path(name))==sha for name, sha in result["physical_source_manifest"].items())
    assert tools.digest(physical / "shell.sdc")==tools.digest(ROOT / "physical_attempt3/shell.sdc")
    assert tools.digest(physical / "shell.adc")==tools.digest(ROOT / "physical_attempt3/shell.adc")
    assert result["physical_source_manifest"]==json.loads((ROOT / "physical_attempt3/input_manifest.json").read_text(encoding="utf-8"))
    assert result["shell_routed_opt"]["sources"][str(physical / "routed_netlist.v")]==tools.digest(physical / "routed_netlist.v")
    result["physical_comparison"] = {}
    for name in ("physical", "physical_attempt2", "physical_attempt3", "physical_opt"):
        work = ROOT / name
        rows = [row for row in paths(work / "coverage_100000_violations.timing") if row["slack"]<0]
        text = (work / "shell_route.area").read_text(encoding="utf-8")
        result["physical_comparison"][name] = {
            "resources_including_shell": {key: int(re.search(r"(?m)^#"+key+r"\s+(\d+)", text)[1])
                for key in ("slice", "dsp", "eram", "IO", "reg")},
            "negative_categories": dict(Counter(("external_" if row["external"] else "internal_")+row["kind"] for row in rows))}
    (ROOT / "measured_evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "status.json").write_text(json.dumps({key: value for key, value in result.items()
        if key not in ("violations", "cycles", "shell_rtl", "shell_gate", "shell_routed_opt", "new_runner_undriven", "checker_replay", "netlist_warnings")},
        ensure_ascii=False, indent=2), encoding="utf-8")
    artifacts = [path for path in ROOT.rglob("*") if path.is_file() and
        path.name != "evidence_hashes.json" and path.suffix in (".v", ".py", ".tcl", ".sdc", ".adc", ".al", ".db",
            ".csv", ".svg", ".md", ".json", ".log", ".timing", ".rpt", ".area") and
        not any(part in ("work", "baseline", "candidate", "__pycache__") for part in path.relative_to(ROOT).parts[:-1])]
    (ROOT / "evidence_hashes.json").write_text(json.dumps({str(path.relative_to(ROOT)): tools.digest(path)
        for path in artifacts}, indent=2), encoding="utf-8")
    print(json.dumps({"resources": resources, "negative_categories": result["negative_categories"],
        "timing": {key: value["minima"] for key, value in timing.items()}}, indent=2))


if __name__ == "__main__":
    main()
