"""仅收集本候选证据：校验输入、初始化和路径分类，不调用硬件工具或改旧文件。"""
from collections import Counter
import json
from pathlib import Path
import re
from run import ROOT, digest, save, frozen, scope, package_check

# Reuse the existing dw_task_overlap collector's TD path-record format.
PATH = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                  r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)\s+Process\s+:\s+(\w+)")


def paths(path):
    return [{"slack_ns": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner, "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in PATH.findall(path.read_text(encoding="utf-8", errors="replace"))]


def summary(records):
    result = {}
    for external in (False, True):
        selected = [r for r in records if r["external"] == external]
        result["external" if external else "internal"] = {kind: {
            "paths": len(group), "negative_endpoints": len({r["end"] for r in group if r["slack_ns"] < 0}),
            "worst": min(group, key=lambda r: r["slack_ns"]), "corners": sorted({r["corner"] for r in group})}
            for kind in sorted({r["kind"] for r in selected}) if (group := [r for r in selected if r["kind"] == kind])}
    return result


def initialization(path):
    rows = re.findall(r"PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s*\\(\S+)\s*\((.*?)\);", path.read_text(), re.S)
    assert len(rows) == 56, (path, len(rows))
    result = {}
    for parameters, name, ports in rows:
        values = dict(re.findall(r"\.(INIT(?:P)?_[0-9A-F]{2})\(256'h([0-9A-F]+)\)", parameters))
        assert len(values) == 80 and name not in result
        result[name] = values
    return result


def main():
    frozen()
    scope()
    package_check()
    physical = ROOT / "continuous_physical"
    manifest = json.loads((physical / "input_manifest.json").read_text())
    assert all(digest(Path(name)) == sha for name, sha in manifest.items())
    reports = {}
    for name in ("coverage_100000_all_paths", "internal_reg_to_reg", "external_reset_entry",
                 "regs_to_diagnostic_outputs", "eram_outputs_all", "eram_inputs_all"):
        reports[name] = summary(paths(physical / (name + ".timing")))
    negative = [r for r in paths(physical / "coverage_100000_violations.timing") if r["slack_ns"] < 0]
    assert len(negative) == 1000 and all(r["external"] and r["begin"] == "i_rstn" and r["kind"] == "removal" for r in negative)
    text = (physical / "final_timing.rpt").read_text()
    assert "STA coverage        : 100.00%" in text and "Both (Slow and Fast)" in text
    area = (physical / "rom_route.area").read_text()
    resources = {name: int(re.search(r"^#" + name + r"\s+(\d+)", area, re.M)[1])
                 for name in ("IO", "slice", "reg", "lut6", "eram", "dsp")}
    assert resources["eram"] == 56 and resources["dsp"] == 0 and resources["IO"] == 35
    original = ROOT / "synthesis_attempt3/gate_netlist.v"
    assert initialization(original) == initialization(physical / "gate_netlist.v") == initialization(physical / "routed_netlist.v")
    checks = (physical / "check_timing_verbose.rpt").read_text()
    assert "checking no clock(0)" in checks and "checking invalid constraint(0)" in checks
    assert "checking combinational loops(0)" in checks
    gate_results = {}
    for label in ("baseline", "candidate", "testbench"):
        pointer = json.loads((ROOT / f"gate_{label}_current.json").read_text())
        gate = json.loads((Path(pointer["work"]) / "gate.json").read_text(encoding="utf-8"))
        gate_results[label] = {k: gate[k] for k in ("errors", "strict_warnings", "delivery_ready", "checks")}
        assert gate["checks"]["compile"]["parse_errors"] == 0
    for name in ("vendor_simulation", "mapped_readback"):
        assert json.loads((ROOT / name / "receipt.json").read_text())["all_passed"]
    prezero = Path(json.loads((ROOT / "prezero_current.json").read_text())["work"])
    assert json.loads((prezero / "receipt.json").read_text())["no_loaded_undriven_nets"]
    result = {"physical": str(physical), "resources_including_crc_probe": resources,
        "sta_coverage_percent": 100.0, "corners_enabled": "Slow/Fast Max/Min", "reports": reports,
        "negative_paths": negative, "negative_counts": dict(Counter(r["kind"] for r in negative)),
        "eram_init_parameters_preserved": 56 * 80, "gate": gate_results, "prezero_receipt": str(prezero / "receipt.json"),
        "clock_warning": "check_timing definition(1): local/generated wording; XML says primary; both continuous and imported runs reproduce it; unresolved",
        "full_mapped_control_simulation": "cancelled_cost_limit_not_passed", "physical_eram_readback": "passed_143360_bytes",
        "external_reset_signed_off": False, "strict_delivery": False, "sdf_simulation": False,
        "trained_model": False, "full_network_or_5fps_proven": False}
    save(ROOT / "result.json", result)
    save(ROOT / "status.json", {"stage": "rom_diagnostic_complete_with_open_reset_clock_and_strict_gates",
        "resources_including_crc_probe": resources, "internal_negative_paths": 0,
        "external_removal_endpoints": 1000, "sta_coverage_percent": 100.0,
        "package_readback_passed": True, "physical_init_preserved": True, "old_files_unchanged": True,
        "production_modified": False, "training_started": False, "bitstream_generated": False, "board_or_flash": False,
        "deployment_release": False, "details": "result.json"})
    frozen()
    report = ROOT / "ROM验证结果与下一步.md"
    local_links = [target for target in re.findall(r"\]\(([^)]+)\)", report.read_text(encoding="utf-8"))
                   if not target.startswith(("https:", "http:"))]
    assert all((ROOT / target).exists() for target in local_links), local_links
    save(ROOT / "evidence_hashes.json", {str(p.relative_to(ROOT)): digest(p) for p in ROOT.rglob("*")
        if p.is_file() and "work" not in p.relative_to(ROOT).parts and "__pycache__" not in p.parts
        and p.name != "evidence_hashes.json"})
    print(json.dumps({"resources": resources, "negative": result["negative_counts"], "strict": {
        k: [v["errors"], v["strict_warnings"]] for k, v in gate_results.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
