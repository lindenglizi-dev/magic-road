"""检查冻结物理输入，并完整汇总当前 TD 报告；不把报告存在等同于时序通过。"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT.parent
PREVIOUS = CANDIDATE.parent / "stem_weight_address_20261011"
MANIFEST = ROOT / "source_manifest.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def port_bits(source):
    totals = {"input": 0, "output": 0, "inout": 0}
    pattern = re.compile(
        r"\b(input|output|inout)\s+(?:wire\s+|reg\s+)?(?:signed\s+)?"
        r"(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])?\s*([A-Za-z_]\w*)"
    )
    for direction, high, low, _ in pattern.findall(source):
        totals[direction] += abs(int(high) - int(low)) + 1 if high else 1
    return totals


def preflight():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures, resolved = [], []
    for item in manifest["sources"]:
        path = (ROOT / item["path"]).resolve()
        actual = digest(path) if path.is_file() else None
        resolved.append({"path": str(path), "expected": item["sha256"], "actual": actual})
        if actual != item["sha256"]:
            failures.append(f"source hash mismatch: {path}")

    top_path = (ROOT / manifest["sources"][0]["path"]).resolve()
    bits = port_bits(top_path.read_text(encoding="utf-8"))
    expected = manifest["io"]
    wanted = {"input": expected["input_bits_including_clock"],
              "output": expected["output_bits"], "inout": 0}
    if bits != wanted:
        failures.append(f"top I/O changed: {bits}, expected {wanted}")
    if sum(bits.values()) > expected["device_capacity_bits_from_prior_actual_report"]:
        failures.append("top I/O exceeds device capacity evidence")

    top = top_path.read_text(encoding="utf-8")
    for module, pattern in {
        "road_mac_probe": r"\broad_mac_probe\s+u_mac\s*\(",
        "road_dynamic_postprocess": r"\broad_dynamic_postprocess\s+u_pp\s*\(",
    }.items():
        count = len(re.findall(pattern, top))
        if count != manifest["expected_source_instances"][module]:
            failures.append(f"expected one {module} source instance, found {count}")
    source_paths = {(ROOT / item["path"]).resolve().name:
                    (ROOT / item["path"]).resolve() for item in manifest["sources"]}
    pp = source_paths["road_dynamic_postprocess.v"].read_text(encoding="utf-8")
    silu = source_paths["silu_shared_unit.v"].read_text(encoding="utf-8")
    if len(re.findall(r"\bsilu_shared_unit\s+u_silu\s*\(", pp)) != 1:
        failures.append("expected one shared SiLU source instance")
    if len(re.findall(r"\bPH1P_LOGIC_ERAM\s*#\s*\(", silu)) != 1:
        failures.append("expected one SiLU ERAM source primitive")

    # TD writes this attribute with a bare ampersand; normalize only the parser copy.
    project_text = (ROOT / "road_frontend_shared_core.al").read_text(encoding="utf-8")
    project_tree = ET.fromstring(project_text.replace('"UsedInP&R"', '"UsedInP&amp;R"'))
    project_sources = {
        node.attrib["Path"]
        for node in project_tree.findall(
            ".//Source_Files/Verilog/File")
    }
    manifest_sources = {item["path"] for item in manifest["sources"]}
    if project_sources != manifest_sources:
        failures.append("TD project source list differs from source_manifest.json")
    build = (ROOT / "build.tcl").read_text(encoding="utf-8").lower()
    if re.search(r"\b(bitgen|generate_bit|write_bitstream)\b", build):
        failures.append("bitstream command found in build.tcl")
    sdc = (ROOT / "frontend.sdc").read_text(encoding="utf-8").lower()
    if re.search(r"\bset_(false_path|multicycle_path|max_delay|min_delay)\b", sdc):
        failures.append("timing exception found in frontend.sdc")

    result = {"status": "FAIL" if failures else "PASS_PREPARED_NOT_EXECUTED",
              "io_bits": bits, "io_total": sum(bits.values()), "sources": resolved,
              "failures": failures, "td_executed": False}
    output = ROOT / "preflight.json"
    attempt = 1
    while output.exists():
        attempt += 1
        output = ROOT / f"preflight_attempt{attempt}.json"
    save(output, result)
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


def _finish_record(record, stats, negative):
    if not record or "check" not in record:
        return
    check = record["check"].lower()
    value = record["slack_ns"]
    item = stats.setdefault(check, {"reported_paths": 0, "worst_slack_ns": None})
    item["reported_paths"] += 1
    item["worst_slack_ns"] = value if item["worst_slack_ns"] is None else min(
        item["worst_slack_ns"], value)
    if value >= 0 or "begin" not in record or "end" not in record:
        return
    begin, end = record["begin"], record["end"]
    scope = ("raw_reset" if begin == "i_rstn" else
             "external_input" if begin.startswith("i_") else
             "external_output" if end.startswith("o_") else "internal")
    candidate = {"check": check, "slack_ns": value, "begin": begin,
                 "end": end, "scope": scope}
    key = (check, end)
    if key not in negative or value < negative[key]["slack_ns"]:
        negative[key] = candidate


def read_timing(path, keep_negative=False):
    stats, negative, processes, coverage = {}, {}, set(), set()
    record = None
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            match = re.match(r"\s*Slack\s*:\s*(-?\d+(?:\.\d+)?)ns", line)
            if match:
                _finish_record(record, stats, negative)
                record = {"slack_ns": float(match[1])}
                continue
            match = re.match(r"\s*Begin Point\s*:\s*(\S+)", line)
            if match and record is not None:
                record["begin"] = match[1]
                continue
            match = re.match(r"\s*End Point\s*:\s*(\S+)", line)
            if match and record is not None:
                record["end"] = match[1]
                continue
            match = re.match(r"\s*Check Type\s*:\s*(\S+)", line)
            if match and record is not None:
                record["check"] = match[1]
                continue
            match = re.match(r"\s*Process\s*:\s*(\S+)", line)
            if match:
                processes.add(match[1])
                continue
            match = re.search(r"STA coverage\s*:\s*([^\r\n]+)", line)
            if match:
                coverage.add(match[1].strip())
    _finish_record(record, stats, negative)
    result = {"checks": stats, "processes": sorted(processes), "coverage": sorted(coverage)}
    return result, list(negative.values()) if keep_negative else []


def parse_area(text):
    result = {}
    for key, pattern in {
        "io": r"#IO\s+(\d+)\s+out of\s+(\d+)",
        "slice": r"#slice\s+(\d+)\s+out of\s+(\d+)",
        "mslice": r"#mslice\s+(\d+)\s+out of\s+(\d+)",
        "lslice": r"#lslice\s+(\d+)\s+out of\s+(\d+)",
        "lut6": r"#lut6\s+(\d+)\s+out of\s+(\d+)",
        "dsp": r"#dsp\s+(\d+)\s+out of\s+(\d+)",
        "eram": r"#eram\s+(\d+)\s+out of\s+(\d+)",
    }.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[key] = {"used": int(match[1]), "available": int(match[2])}
    match = re.search(r"#reg\s+(\d+)", text, re.IGNORECASE)
    if match:
        result["registers"] = int(match[1])
    result["hierarchy_rows"] = {
        module: len(re.findall(rf"\|[^\n]*\|{module}\s*\|", text))
        for module in ("road_mac_probe", "road_dynamic_postprocess", "silu_shared_unit")
    }
    return result


def ram_source_lines(report):
    result = {}
    pattern = re.compile(r"^\s*(\S+)\s*\|[^|]*\|[^|]*\((\d+)\)\s*\|")
    with report.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            match = pattern.match(line)
            if match:
                result[match[1]] = int(match[2])
    return result


def failure_family(record, ram_lines, rtl_lines):
    end = record["end"]
    if end.startswith(("reg_table_", "u_table_")):
        return "table_command_register"
    if end.startswith("u_stem/reg_mac_weight"):
        return "stem_weight"
    if end.startswith("u_down2/reg_mac_weight"):
        return "down2_weight"
    if end.startswith("u_down2/reg_mac_activation"):
        return "down2_activation"
    if end.startswith("u_down2/cnt_output"):
        return "down2_output_counter"
    if end.startswith("u_pp/u_pre/u_round/"):
        return "pre_round_ce"
    cell = end.rsplit(".", 1)[0]
    line_number = ram_lines.get(cell)
    if end.endswith(".we") and line_number and line_number <= len(rtl_lines):
        source = rtl_lines[line_number - 1]
        for token, family in (("reg_halo", "down2_halo_we"),
                              ("reg_dw_cache", "down2_dw_cache_we"),
                              ("reg_dw_weight", "down2_dw_weight_we"),
                              ("reg_pw_weight", "down2_pw_weight_we")):
            if token in source:
                return family
        return "ram_we_other"
    return "other_internal"


def grouped_failures(records, ram_report, rtl):
    ram_lines = ram_source_lines(ram_report)
    rtl_lines = rtl.read_text(encoding="utf-8").splitlines()
    groups = {}
    for record in records:
        if record["scope"] != "internal":
            continue
        name = failure_family(record, ram_lines, rtl_lines)
        item = groups.setdefault(name, {"failed_check_endpoints": 0, "worst_slack_ns": None})
        item["failed_check_endpoints"] += 1
        item["worst_slack_ns"] = (record["slack_ns"] if item["worst_slack_ns"] is None else
                                  min(item["worst_slack_ns"], record["slack_ns"]))
    for name in ("table_command_register", "stem_weight", "down2_weight",
                 "down2_activation", "down2_output_counter", "pre_round_ce",
                 "down2_halo_we", "down2_dw_cache_we", "down2_dw_weight_we",
                 "down2_pw_weight_we", "ram_we_other", "other_internal"):
        groups.setdefault(name, {"failed_check_endpoints": 0, "worst_slack_ns": None})
    return groups


def internal_ram_failures(records):
    return [item for item in records if item["scope"] == "internal"
            and "/ramread" in item["end"] and item["end"].endswith(".we")]


def summarize():
    if preflight():
        return 1
    required = ["frontend_route.area", "frontend_route_ram.rpt", "internal_all_checks.timing",
                "external_reset_entry.timing", "diagnostic_inputs_to_regs.timing",
                "regs_to_diagnostic_outputs.timing", "all_endpoints.timing",
                "all_endpoints_include_ignored.timing", "dsp_outputs_all_checks.timing",
                "dsp_inputs_all_checks.timing", "all_eram_outputs_all_checks.timing",
                "all_eram_inputs_all_checks.timing", "timing_ignored.rpt", "all_violations.timing",
                "final_timing.rpt", "td_launcher.log", "pr.db"]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        print("Missing TD outputs: " + ", ".join(missing), file=sys.stderr)
        return 2

    log = (ROOT / "td_launcher.log").read_text(encoding="utf-8", errors="replace")
    report_failures = []
    if "REPORT_COMPLETION_DONE" not in log:
        report_failures.append("missing REPORT_COMPLETION_DONE")
    if 'finish command "route"' not in log:
        report_failures.append("route did not finish")
    if "TMR-2509" in log or "TMR-2507" in log:
        report_failures.append("TD timing report command failed")

    area = parse_area((ROOT / "frontend_route.area").read_text(encoding="utf-8", errors="replace"))
    if area.get("hierarchy_rows") != {
            "road_mac_probe": 1, "road_dynamic_postprocess": 1, "silu_shared_unit": 1}:
        report_failures.append("required routed hierarchy rows are not unique")
    if not 1 <= area.get("eram", {}).get("used", 0) <= 108:
        report_failures.append("no valid routed ERAM usage")
    if len(re.findall(r"ERAM_RECORD .*u_silu", log)) != 1:
        report_failures.append("shared SiLU ERAM source instance was duplicated or removed")

    timing, inventory, internal_inventory = {}, [], []
    names = ("internal_all_checks", "external_reset_entry", "diagnostic_inputs_to_regs",
             "regs_to_diagnostic_outputs", "all_endpoints", "all_endpoints_include_ignored",
             "dsp_outputs_all_checks", "dsp_inputs_all_checks",
             "all_eram_outputs_all_checks", "all_eram_inputs_all_checks")
    for name in names:
        timing[name], found = read_timing(
            ROOT / (name + ".timing"),
            keep_negative=name in ("internal_all_checks", "all_endpoints_include_ignored"))
        if name == "internal_all_checks":
            internal_inventory = found
        elif name == "all_endpoints_include_ignored":
            inventory = found
    if not {"setup", "hold"} <= set(timing["internal_all_checks"]["checks"]):
        report_failures.append("internal register setup/hold report is incomplete")
    if not {"recovery", "removal"} <= set(timing["external_reset_entry"]["checks"]):
        report_failures.append("external reset recovery/removal report is incomplete")

    normal = timing["all_endpoints"]["checks"]
    including = timing["all_endpoints_include_ignored"]["checks"]
    ignored_delta = {name: including.get(name, {}).get("reported_paths", 0) -
                     normal.get(name, {}).get("reported_paths", 0)
                     for name in set(normal) | set(including)}
    save(ROOT / "failed_endpoint_inventory.json", sorted(
        inventory, key=lambda item: (item["scope"], item["check"], item["end"])))
    save(ROOT / "internal_register_failed_endpoint_inventory.json", sorted(
        internal_inventory, key=lambda item: (item["check"], item["end"])))
    scope_counts = dict(Counter(item["scope"] + ":" + item["check"] for item in inventory))
    current_groups = grouped_failures(
        internal_inventory, ROOT / "frontend_route_ram.rpt",
        CANDIDATE / "rtl/road_down2_tile_scheduler.v")
    all_report_internal_ram = internal_ram_failures(inventory)
    all_report_ram_groups = grouped_failures(
        all_report_internal_ram,
        ROOT / "frontend_route_ram.rpt",
        CANDIDATE / "rtl/road_down2_tile_scheduler.v")
    old_inventory = json.loads((PREVIOUS / "failed_endpoint_inventory.json").read_text(encoding="utf-8"))
    old_full_groups = grouped_failures(old_inventory, PREVIOUS / "physical/frontend_route_ram.rpt",
                                       PREVIOUS / "rtl/road_down2_tile_scheduler.v")
    _, old_internal_inventory = read_timing(
        PREVIOUS / "physical/internal_all_checks.timing", keep_negative=True)
    old_internal_groups = grouped_failures(
        old_internal_inventory, PREVIOUS / "physical/frontend_route_ram.rpt",
        PREVIOUS / "rtl/road_down2_tile_scheduler.v")
    old_summary = json.loads((PREVIOUS / "physical_summary.json").read_text(encoding="utf-8"))

    negative_checks = {name: value for name, value in including.items()
                       if value["worst_slack_ns"] is not None and value["worst_slack_ns"] < 0}
    internal_negative = len(internal_inventory)
    internal_ram_negative = len(all_report_internal_ram)
    timing_failures = ([f"negative {name} slack {value['worst_slack_ns']} ns"
                        for name, value in sorted(negative_checks.items())] +
                       ([f"{internal_negative} dedicated register-to-register failed check/endpoints"]
                        if internal_negative else []) +
                       ([f"{internal_ram_negative} internal RAM write-enable failures in all-endpoint report"]
                        if internal_ram_negative else []))
    status = ("REPORT_INCOMPLETE" if report_failures else
              "IMPLEMENTED_WITH_TIMING_VIOLATIONS" if timing_failures else
              "IMPLEMENTED_TIMING_PASS_DIAGNOSTIC_ONLY")
    summary = {
        "status": status, "device": "PH1P35MDG324-3", "clock_mhz": 100,
        "resources": area, "timing": timing,
        "failed_endpoints_including_ignored": scope_counts,
        "unique_failed_check_endpoint_pairs": len(inventory),
        "internal_register_failed_endpoint_count": internal_negative,
        "internal_register_failed_endpoint_inventory":
            "internal_register_failed_endpoint_inventory.json",
        "all_report_internal_failed_endpoint_count":
            sum(item["scope"] == "internal" for item in inventory),
        "all_report_internal_ram_failed_endpoint_count": internal_ram_negative,
        "all_report_internal_ram_failure_groups": all_report_ram_groups,
        "internal_timing_pass": internal_negative == 0 and not any(
            item["scope"] == "internal" for item in inventory),
        "ignored_path_count_delta": ignored_delta,
        "ignored_report_sha256": digest(ROOT / "timing_ignored.rpt"),
        "all_violations_report_sha256": digest(ROOT / "all_violations.timing"),
        "internal_failure_groups": current_groups,
        "comparison": {
            "baseline": "stem_weight_address_20261011",
            "old_authoritative_summary_groups":
                old_summary.get("comparison", {}).get("new_internal_failures"),
            "old_full_report_groups_reclassified": old_full_groups,
            "old_dedicated_internal_groups_reparsed": old_internal_groups,
            "new_dedicated_internal_groups": current_groups,
            "resource_deltas": {key: area[key]["used"] - old_summary["resources"][key]["used"]
                                for key in ("dsp", "eram", "slice", "mslice", "lslice", "lut6")},
            "constraint_bytes_identical": {name: digest(ROOT / name) ==
                                             digest(PREVIOUS / "physical" / name)
                                             for name in ("frontend.sdc", "frontend.adc", "build.tcl")},
        },
        "database_sha256": digest(ROOT / "pr.db"),
        "source_manifest": "source_manifest.json",
        "report_failures": report_failures, "timing_failures": timing_failures,
        "failures": report_failures + timing_failures,
        "external_contract": "zero I/O delay, automatic pins, raw reset entry; not board signoff",
        "completion": "actual top routed; all endpoint/ignored and RAM reports parsed; no bitstream",
        "not_deployment": True,
    }
    regime = ROOT / "optimization_regime.json"
    if regime.is_file():
        summary["optimization_regime"] = json.loads(regime.read_text(encoding="utf-8"))
    summary["summary_generator_sha256"] = digest(Path(__file__))
    save(ROOT / "physical_summary.json", summary)
    rows = "\n".join(
        f"| {name} | {value['failed_check_endpoints']} | {value['worst_slack_ns']} |"
        for name, value in current_groups.items())
    (ROOT / "物理结果.md").write_text(
        "# 装表命令隔离候选物理结果\n\n"
        f"状态：`{status}`。器件 PH1P35MDG324-3，目标 100 MHz。\n\n"
        "| 内部端点组 | 失败端点数 | 最差裕量 ns |\n|---|---:|---:|\n" + rows + "\n\n"
        f"专用内部寄存器报告失败端点：{internal_negative}；全报告内部RAM写使能失败端点：{internal_ram_negative}。\n\n"
        "已单独保留旧36个RNE CE端点、halo写使能、DW cache写使能及其他RAM写使能分类；"
        "旧权威摘要与本次重解析结果并列，不合并口径。\n"
        "外部I/O为零延迟诊断假设和自动引脚，不是板级接口签核。\n",
        encoding="utf-8")
    print(json.dumps({"status": status, "resources": area,
                      "internal_failure_groups": current_groups,
                      "all_report_internal_ram_failure_groups": all_report_ram_groups,
                      "report_failures": report_failures,
                      "timing_failures": timing_failures}, indent=2))
    return 1 if summary["failures"] else 0


def self_test():
    stats, negative = {}, {}
    _finish_record({"slack_ns": -0.25, "check": "setup", "begin": "u_a/q.clk",
                    "end": "u_b/d.d"}, stats, negative)
    _finish_record({"slack_ns": 0.10, "check": "hold", "begin": "i_data",
                    "end": "u_b/d.d"}, stats, negative)
    assert stats["setup"] == {"reported_paths": 1, "worst_slack_ns": -0.25}
    assert list(negative.values())[0]["scope"] == "internal"
    for begin, end in (("i_load_addr[1]", "u_down2/ramread0.we"),
                       ("i_rstn", "u_mac/ramread1.we"),
                       ("u_stem/q.clk", "u_pp/ramread2.we")):
        _finish_record({"slack_ns": -0.2, "check": "setup", "begin": begin,
                        "end": end}, stats, negative)
    ram_failures = internal_ram_failures(list(negative.values()))
    assert len(ram_failures) == 1 and ram_failures[0]["end"] == "u_pp/ramread2.we"
    rtl = [""] * 530
    rtl[507] = "next = reg_halo[index];"
    assert failure_family({"end": "u_down2/ramread0_syn_1.we"},
                          {"u_down2/ramread0_syn_1": 508}, rtl) == "down2_halo_we"
    rtl[529] = "next = reg_dw_cache[index];"
    assert failure_family({"end": "u_down2/ramread9_syn_1.we"},
                          {"u_down2/ramread9_syn_1": 530}, rtl) == "down2_dw_cache_we"
    assert port_bits("input [9:0] a,\noutput reg b\n") == {
        "input": 10, "output": 1, "inout": 0}
    print("PHYSICAL_REPORT_SELF_TEST_PASS")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preflight", "summarize", "self-test"))
    raise SystemExit({"preflight": preflight, "summarize": summarize,
                      "self-test": self_test}[parser.parse_args().action]())
