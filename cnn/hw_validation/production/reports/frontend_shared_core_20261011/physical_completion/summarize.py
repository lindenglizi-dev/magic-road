"""汇总同一布线数据库的实际证据；保留未通过状态，不修改RTL或约束。"""
import importlib.util
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PHYSICAL = ROOT.parent / "physical_attempt2"
spec = importlib.util.spec_from_file_location("physical_reader", PHYSICAL / "physical_report.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def path_inventory(text):
    records = []
    for chunk in re.split(r"(?m)^Slack\s*:\s*", text)[1:]:
        slack = float(re.match(r"(-?\d+(?:\.\d+)?)ns", chunk)[1])
        if slack >= 0:
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
    completion = (ROOT / "reports.log").read_text(encoding="utf-8", errors="replace")
    assert "REPORT_COMPLETION_DONE" in completion
    assert "TMR-2509" not in log and "TMR-2507" not in log
    assert "finish command \"route\"" in log
    timing = {}
    for folder, names in ((PHYSICAL, ("internal_all_checks", "external_reset_entry",
                           "diagnostic_inputs_to_regs", "regs_to_diagnostic_outputs", "all_endpoints", "all_endpoints_include_ignored")),
                          (ROOT, ("dsp_outputs_all_checks", "dsp_inputs_all_checks",
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
    assert area["eram"]["used"] == 4 and area["dsp"]["used"] == 32
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
        "resources": area, "timing": timing, "source_manifest": "../physical_attempt2/source_manifest.json",
        "database_sha256": reader.digest(PHYSICAL / "pr.db"),
        "failed_endpoints_including_ignored": dict(Counter(r["scope"] + ":" + r["check"] for r in inventory)),
        "negative_path_records_including_ignored": len(negative_paths),
        "unique_failed_check_endpoint_pairs": len(inventory),
        "original_build_stop": "Post-route assertion expected one total ERAM; actual has one SiLU and three inferred Stem memories. Original failure preserved.",
        "completion": "Read-only import of the same pr.db, no replacement P&R, no constraint change.",
        "external_contract": "Zero IO delay, automatic pins, raw reset entry; not board signoff.",
        "not_deployment": True,
    }
    (ROOT / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sample = path_inventory("Slack : -0.5ns\nBegin Point : u_core/r.clk\nEnd Point : u_core/q.D\nCheck Type : setup\n"
                            "Slack : 0.1ns\nBegin Point : i_data\nEnd Point : u_core/q.D\nCheck Type : hold\n")
    assert len(sample) == 1 and sample[0]["scope"] == "internal" and sample[0]["slack_ns"] == -0.5
    summarize()
