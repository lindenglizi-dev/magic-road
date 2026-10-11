"""复用前端物理解析，比较单变量Stem地址修复；不修改RTL或约束。"""
import importlib.util
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PHYSICAL = ROOT / "physical"
spec = importlib.util.spec_from_file_location("physical_reader", PHYSICAL / "physical_report.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def path_inventory(text, negative_only=True):
    records = []
    for chunk in re.split(r"(?m)^Slack\s*:\s*", text)[1:]:
        slack = float(re.match(r"(-?\d+(?:\.\d+)?)ns", chunk)[1])
        if negative_only and slack >= 0:
            continue
        begin = re.search(r"Begin Point\s*:\s*(\S+)", chunk)[1]
        end = re.search(r"End Point\s*:\s*(\S+)", chunk)[1]
        check = re.search(r"Check Type\s*:\s*(\S+)", chunk)[1]
        scope = "raw_reset" if begin == "i_rstn" else "external_input" if begin.startswith("i_") else "external_output" if end.startswith("o_") else "internal"
        records.append({"check": check, "slack_ns": slack, "begin": begin, "end": end, "scope": scope})
    return records


def summarize():
    area_text = (PHYSICAL / "frontend_route.area").read_text(encoding="utf-8")
    area = reader.parse_area(area_text)
    for key in ("slice", "lslice", "lut6"):
        match = re.search(rf"#{key}\s+(\d+)\s+out of\s+(\d+)", area_text)
        assert match, key
        area[key] = {"used": int(match[1]), "available": int(match[2])}
    log = (PHYSICAL / "td_launcher.log").read_text(encoding="utf-8", errors="replace")
    completion = log
    assert "REPORT_COMPLETION_DONE" in completion
    assert "TMR-2509" not in log and "TMR-2507" not in log
    assert "finish command \"route\"" in log
    timing = {}
    for folder, names in ((PHYSICAL, ("internal_all_checks", "external_reset_entry",
                           "diagnostic_inputs_to_regs", "regs_to_diagnostic_outputs", "all_endpoints", "all_endpoints_include_ignored")),
                          (PHYSICAL, ("dsp_outputs_all_checks", "dsp_inputs_all_checks",
                                  "all_eram_outputs_all_checks", "all_eram_inputs_all_checks"))):
        for name in names:
            text = (folder / (name + ".timing")).read_text(encoding="utf-8", errors="replace")
            timing[name] = {"checks": reader.parse_timing(text),
                           "processes": sorted(set(re.findall(r"Process\s*:\s*(\S+)", text))),
                           "coverage": re.findall(r"STA coverage\s*:\s*([^\r\n]+)", text)}
    internal = timing["internal_all_checks"]["checks"]
    assert {"setup", "hold"} <= set(internal), internal
    reset = timing["external_reset_entry"]["checks"]
    assert {"recovery", "removal"} <= set(reset), reset
    assert area["hierarchy_rows"] == {"road_mac_probe": 1, "road_dynamic_postprocess": 1, "silu_shared_unit": 1}
    assert 1 <= area["eram"]["used"] <= 108 and 24 <= area["dsp"]["used"] <= 40
    assert area["slice"]["used"] <= 21216
    assert len(re.findall(r"ERAM_RECORD .*u_silu", completion)) == 1
    all_checks = timing["all_endpoints"]["checks"]
    negative_paths = path_inventory((PHYSICAL / "all_endpoints_include_ignored.timing").read_text(encoding="utf-8"))
    # TD can list the same endpoint more than once for different paths/corners.
    inventory = list({(r["check"], r["end"]): r for r in sorted(
        negative_paths, key=lambda r: r["slack_ns"], reverse=True)}.values())
    (ROOT / "failed_endpoint_inventory.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    result = {
        "status": "IMPLEMENTED_WITH_TIMING_VIOLATIONS" if any(
            v["worst_slack_ns"] < 0 for v in all_checks.values()) else "IMPLEMENTED_DIAGNOSTIC_ONLY",
        "resources": area, "timing": timing, "source_manifest": "physical/source_manifest.json",
        "database_sha256": reader.digest(PHYSICAL / "pr.db"),
        "failed_endpoints_including_ignored": dict(Counter(r["scope"] + ":" + r["check"] for r in inventory)),
        "negative_path_records_including_ignored": len(negative_paths),
        "unique_failed_check_endpoint_pairs": len(inventory),
        "completion": "New actual top P&R, unchanged old SDC/ADC, final marker verified; no bitstream.",
        "external_contract": "Zero IO delay, automatic pins, raw reset entry; not board signoff.",
        "not_deployment": True,
    }
    previous = ROOT.parent / "frontend_shared_core_20261011"
    old = json.loads((previous / "physical_completion/summary.json").read_text(encoding="utf-8"))
    old_inventory = json.loads((previous / "physical_completion/failed_endpoint_inventory.json").read_text(encoding="utf-8"))
    def groups(records):
        selected = [r for r in records if r["scope"] == "internal"]
        output = {}
        for name, predicate in (
            ("stem_weight", lambda r: r["end"].startswith("u_stem/reg_mac_weight")),
            ("down2_weight", lambda r: r["end"].startswith("u_down2/reg_weight")),
            ("down2_activation", lambda r: r["end"].startswith("u_down2/reg_activation")),
            ("down2_output_counter", lambda r: r["end"].startswith("u_down2/cnt_output")),
            ("other_internal", lambda r: not (r["end"].startswith("u_stem/reg_mac_weight") or r["end"].startswith("u_down2/reg_weight") or r["end"].startswith("u_down2/reg_activation") or r["end"].startswith("u_down2/cnt_output"))),
        ):
            paths = [r for r in selected if predicate(r)]
            output[name] = {"failed_check_endpoints": len(paths),
                            "worst_slack_ns": min((r["slack_ns"] for r in paths), default=None)}
        assert sum(item["failed_check_endpoints"] for item in output.values()) == len(selected)
        return output
    result["comparison"] = {
        "baseline": "frontend_shared_core_20261011 at cd4f6e2b",
        "old_internal_failures": groups(old_inventory), "new_internal_failures": groups(inventory),
        "resource_deltas": {key: area[key]["used"] - old["resources"][key]["used"] for key in ("dsp", "eram", "slice", "mslice", "lslice", "lut6")},
        "constraint_bytes_identical": {name: reader.digest(PHYSICAL / name) == reader.digest(previous / "physical_attempt2" / name)
                                       for name in ("frontend.sdc", "frontend.adc")},
    }
    all_paths = path_inventory((PHYSICAL / "all_endpoints_include_ignored.timing").read_text(encoding="utf-8"), negative_only=False)
    stem_paths = [r for r in all_paths if r["end"].startswith("u_stem/reg_mac_weight") and r["check"] == "setup"]
    assert stem_paths, "Stem权重端点不能缺失"
    result["comparison"]["stem_weight_worst_setup"] = min(stem_paths, key=lambda r: r["slack_ns"])
    assert all(result["comparison"]["constraint_bytes_identical"].values())
    netlist = (PHYSICAL / "routed_netlist.v").read_text(encoding="utf-8")
    dsp_blocks = netlist.split("PH1P_PHY_DSPSIOU_V2 #(")[1:]
    dsp_owners = Counter(re.search(r'\.MACRO\("([^/]+)', block)[1] for block in dsp_blocks)
    assert sum(dsp_owners.values()) == area["dsp"]["used"]
    result["dsp_hierarchy_counts"] = dict(dsp_owners)
    cycles = json.loads((ROOT / "cycle_summary.json").read_text(encoding="utf-8"))
    old_cycles = json.loads((previous / "cycle_summary.json").read_text(encoding="utf-8"))
    assert cycles == old_cycles, "本轮不能改变任何计时窗口/周期"
    result["core_cycles_unchanged"] = {mode: sum(cycles[mode][layer]["core"] for layer in ("stem", "down2"))
                                       for mode in ("normal", "stalls")}
    shared_spec = importlib.util.spec_from_file_location("candidate_run", ROOT / "run.py")
    run = importlib.util.module_from_spec(shared_spec)
    shared_spec.loader.exec_module(run)
    run.shared.check()
    (ROOT / "physical_summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    status.update({"status": result["status"], "physical": result, "stem_address_only": True})
    run.save(ROOT / "status.json", status)
    print(json.dumps({"status": result["status"], "resources": area, "comparison": result["comparison"],
                      "dsp_hierarchy_counts": dict(dsp_owners), "core_cycles": result["core_cycles_unchanged"]}, indent=2))


if __name__ == "__main__":
    sample = path_inventory("Slack : -0.5ns\nBegin Point : u_core/r.clk\nEnd Point : u_core/q.D\nCheck Type : setup\n"
                            "Slack : 0.1ns\nBegin Point : i_data\nEnd Point : u_core/q.D\nCheck Type : hold\n")
    assert len(sample) == 1 and sample[0]["scope"] == "internal" and sample[0]["slack_ns"] == -0.5
    summarize()
