"""Extract actual routed path checks and bind the complete implementation input closure."""
from collections import Counter
import json
import re
import run

ROOT = run.ROOT
PHYSICAL = ROOT / "physical_attempt2"


def paths(path):
    counts = Counter()
    worst = {}
    cross = {}
    current = {}
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            if line.startswith("Slack               :"):
                current = {"slack_ns": float(line.split(":", 1)[1].strip().removesuffix("ns"))}
            elif current and line.startswith(("Begin Point", "End Point", "Check Type", "Process")):
                key, value = (part.strip() for part in line.split(":", 1))
                current[key] = value
                if key == "Process":
                    kind = current["Check Type"]
                    counts[kind] += 1
                    if kind not in worst or current["slack_ns"] < worst[kind]["slack_ns"]:
                        worst[kind] = current.copy()
                    clocks = [re.search(r"clock (.+?)  \{", current.get(k, "")) for k in ("Begin Point", "End Point")]
                    if all(clocks) and clocks[0][1] != clocks[1][1]:
                        group = clocks[0][1] + " -> " + clocks[1][1] + " / " + kind
                        if group not in cross:
                            cross[group] = {"reported_checks": 0, "worst_ns": current["slack_ns"]}
                        cross[group]["reported_checks"] += 1
                        cross[group]["worst_ns"] = min(cross[group]["worst_ns"], current["slack_ns"])
                    current = {}
    return {"reported_checks": dict(counts), "worst": worst, "cross_clock": cross}


def main():
    work = run.fresh("evidence")
    source_manifest = json.loads((PHYSICAL / "input_manifest.json").read_text(encoding="utf-8"))
    changed = [name for name, sha in source_manifest.items() if run.digest(run.Path(name)) != sha]
    assert not changed, changed
    assert run.digest(PHYSICAL / "selftest_program.hex") == run.digest(ROOT / "program/selftest_program.hex")
    inputs = [run.Path(p) for p in source_manifest]
    inputs += [PHYSICAL / n for n in ("selftest_program.hex", "board.adc", "board.sdc", "build.tcl", "road_board_selftest_top.al")]
    inputs += [p for p in (ROOT / "official/PLL").rglob("*") if p.is_file()]
    inputs += [run.TD]
    run.save(work / "physical_input_closure.json", {
        "captured_after_implementation": True,
        "rtl_checked_against_pre_run_manifest": True,
        "program_copy_matches_reference": True,
        "files": {str(p): run.digest(p) for p in inputs}})
    result = {}
    for name in ("all_endpoints.timing", "internal_reg_to_reg.timing", "compute_reset_sync.timing",
                 "pixel_reset_sync.timing", "compute_reset_distribution.timing", "hdmi_reset_distribution.timing",
                 "dsp_inputs.timing", "dsp_outputs.timing", "eram_inputs.timing", "eram_outputs.timing"):
        result[name] = paths(PHYSICAL / name)
    run.save(work / "timing_checks.json", result)
    netlist = (PHYSICAL / "gate_netlist.v").read_text(encoding="utf-8")
    run.save(work / "mapped_primitives.json", {
        "dsp_instances": len(re.findall(r"^  PH1P_PHY_DSPSIOU_V2\s", netlist, re.M)),
        "eram_instances": len(re.findall(r"^  PH1P_PHY_ERAM_V2\s", netlist, re.M)),
        "nonzero_init00_parameters": sum(int(h, 16) != 0 for h in re.findall(r"\.INIT_00\(256'h([0-9a-fA-F]+)\)", netlist)),
        "initialization_only_structurally_observed_not_board_verified": True})
    mapped = ROOT / "mapped_simulation/mapped.log"
    if mapped.exists():
        codes, undriven = Counter(), Counter()
        with mapped.open(encoding="utf-8", errors="replace") as stream:
            for line in stream:
                if "Warning:" not in line:
                    continue
                match = re.search(r"(vopt-\d+|vsim-\d+)", line)
                if match:
                    codes[match[1]] += 1
                    if match[1] == "vopt-2958":
                        undriven["open_n_export_stub" if "open_n" in line else "other"] += 1
        run.save(work / "mapped_warning_categories.json", {
            "codes": dict(codes), "undriven_categories": dict(undriven),
            "all_ports_individually_closed": False,
            "zero_warning_claim": False})
    final_files = [p for folder in ("rtl", "core", "tests", "build", "program", "spec", "official")
                   for p in (ROOT / folder).rglob("*") if p.is_file()]
    final_files += [ROOT / n for n in ("run.py", "mapped_check.py", "evidence.py", "status.json",
                                     "契约与滚动状态.txt", "首板自主计算自检_实测报告.txt")]
    final_files += [PHYSICAL / n for n in ("gate.db", "pr.db", "gate_netlist.v", "routed_netlist.v",
                                         "final_timing.rpt", "route.area", "route.qor", "td.log")]
    final_files += [ROOT / "simulation_attempt3/receipt.json", ROOT / "mapped_simulation/receipt.json"]
    final_files += [run.Path(p) for p in json.loads((ROOT / "simulation_attempt3/receipt.json").read_text(encoding="utf-8"))["vendor_models"]]
    run.save(work / "candidate_final_freeze.json", {str(p): run.digest(p) for p in final_files})
    run.check()
    print(json.dumps({"output": str(work), "worst_ns": {k: v["slack_ns"] for k, v in result["all_endpoints.timing"]["worst"].items()},
                      "frozen_files": len(final_files)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
