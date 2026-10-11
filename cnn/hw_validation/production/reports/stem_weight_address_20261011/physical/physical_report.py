"""Preflight the frozen closure and summarize retained TD physical evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "source_manifest.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    failures = []
    resolved = []
    for item in manifest["sources"]:
        path = (ROOT / item["path"]).resolve()
        actual = digest(path) if path.is_file() else None
        resolved.append({"path": str(path), "expected": item["sha256"], "actual": actual})
        if actual != item["sha256"]:
            failures.append(f"source hash mismatch: {path}")

    top = (ROOT / manifest["sources"][0]["path"]).resolve().read_text(encoding="utf-8")
    bits = port_bits(top)
    expected = manifest["io"]
    if bits != {"input": expected["input_bits_including_clock"], "output": expected["output_bits"], "inout": 0}:
        failures.append(f"top I/O changed: {bits}")
    total = sum(bits.values())
    if total > expected["device_capacity_bits_from_prior_actual_report"]:
        failures.append(f"I/O {total} exceeds device capacity evidence {expected['device_capacity_bits_from_prior_actual_report']}")

    required = {
        "road_mac_probe": r"\broad_mac_probe\s+u_mac\s*\(",
        "road_dynamic_postprocess": r"\broad_dynamic_postprocess\s+u_pp\s*\(",
    }
    for module, pattern in required.items():
        count = len(re.findall(pattern, top))
        if count != manifest["expected_source_instances"][module]:
            failures.append(f"expected one {module} instance, found {count}")

    pp = (ROOT / "../../board_selftest_20261010/core/road_dynamic_postprocess.v").resolve().read_text(encoding="utf-8")
    silu = (ROOT / "../../board_selftest_20261010/core/silu_shared_unit.v").resolve().read_text(encoding="utf-8")
    if len(re.findall(r"\bsilu_shared_unit\s+u_silu\s*\(", pp)) != 1:
        failures.append("expected one shared SiLU source instance")
    if len(re.findall(r"\bPH1P_LOGIC_ERAM\s*#\s*\(", silu)) != 1:
        failures.append("expected one SiLU ERAM primitive source instance")

    project_sources = {
        node.attrib["Path"] for node in ET.parse(ROOT / "road_frontend_shared_core.al").findall(".//Source_Files/Verilog/File")
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

    result = {
        "status": "FAIL" if failures else "PASS_PREPARED_NOT_EXECUTED",
        "io_bits": bits,
        "io_total": total,
        "exceeds_historical_64_bit_target": total > expected["historical_narrow_target_bits"],
        "within_prior_device_capacity_evidence": total <= expected["device_capacity_bits_from_prior_actual_report"],
        "sources": resolved,
        "failures": failures,
        "td_executed": False,
    }
    output = ROOT / "preflight.json"
    attempt = 1
    while output.exists():
        attempt += 1
        output = ROOT / f"preflight_attempt{attempt}.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


def parse_timing(text):
    checks = {}
    pattern = re.compile(
        r"Slack\s*:\s*(-?\d+(?:\.\d+)?)ns.*?Check Type\s*:\s*(setup|hold|recovery|removal)",
        re.IGNORECASE | re.DOTALL,
    )
    for slack, check in pattern.findall(text):
        record = checks.setdefault(check.lower(), {"reported_paths": 0, "worst_slack_ns": None})
        value = float(slack)
        record["reported_paths"] += 1
        record["worst_slack_ns"] = value if record["worst_slack_ns"] is None else min(record["worst_slack_ns"], value)
    return checks


def parse_area(text):
    result = {}
    for key, pattern in {
        "io": r"#IO\s+(\d+)\s+out of\s+(\d+)",
        "mslice": r"#mslice\s+(\d+)\s+out of\s+(\d+)",
        "dsp": r"#dsp\s+(\d+)\s+out of\s+(\d+)",
        "eram": r"#eram\s+(\d+)\s+out of\s+(\d+)",
    }.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[key] = {"used": int(match.group(1)), "available": int(match.group(2))}
    result["hierarchy_rows"] = {
        module: len(re.findall(rf"\|[^\n]*\|{module}\s*\|", text))
        for module in ("road_mac_probe", "road_dynamic_postprocess", "silu_shared_unit")
    }
    return result


def summarize():
    if preflight():
        return 1
    area_path = ROOT / "frontend_route.area"
    timing_path = ROOT / "internal_all_checks.timing"
    missing = [str(path) for path in (area_path, timing_path, ROOT / "final_timing.rpt") if not path.is_file()]
    if missing:
        print("Missing TD outputs: " + ", ".join(missing), file=sys.stderr)
        return 2
    area = parse_area(area_path.read_text(encoding="utf-8", errors="replace"))
    timing = parse_timing(timing_path.read_text(encoding="utf-8", errors="replace"))
    required_checks = {"setup", "hold", "recovery", "removal"}
    failures = []
    if set(timing) != required_checks:
        failures.append(f"internal check types incomplete: {sorted(timing)}")
    if area.get("eram", {}).get("used") != 1:
        failures.append(f"expected one routed SiLU ERAM, got {area.get('eram')}")
    for module, count in area.get("hierarchy_rows", {}).items():
        if count != 1:
            failures.append(f"expected one routed hierarchy row for {module}, got {count}")
    summary = {
        "status": "FAIL" if failures else "TD_REPORTS_PARSED",
        "device": "PH1P35MDG324-3",
        "clock_mhz": 100,
        "resources": area,
        "internal_timing": timing,
        "external_io_timing": "diagnostic zero-delay only; not board signoff",
        "failures": failures,
    }
    (ROOT / "physical_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    rows = "\n".join(
        f"| {name} | {value['reported_paths']} | {value['worst_slack_ns']} |"
        for name, value in sorted(timing.items())
    )
    markdown = (
        "# 实际共享前端物理结果\n\n"
        f"状态：`{summary['status']}`。器件 PH1P35MDG324-3，目标 100 MHz。\n\n"
        "| 内部检查 | 报告路径数 | 最差裕量 ns |\n|---|---:|---:|\n" + rows + "\n\n"
        f"资源：`{json.dumps(area, ensure_ascii=False)}`。\n\n"
        "外部 I/O 使用零延迟诊断假设和自动引脚，只用于隔离实现，不是板级接口签核。\n"
    )
    (ROOT / "物理结果.md").write_text(markdown, encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 1 if failures else 0


def self_test():
    timing = parse_timing(
        "Slack : -0.2ns\nCheck Type : setup\nSlack : 0.1ns\nCheck Type : hold\n"
        "Slack : 0.3ns\nCheck Type : recovery\nSlack : -0.4ns\nCheck Type : removal\n"
    )
    assert timing["setup"]["worst_slack_ns"] == -0.2
    assert timing["removal"]["reported_paths"] == 1
    area = parse_area("#IO 143 out of 160\n#eram 1 out of 108\n| u_mac |road_mac_probe |")
    assert area["io"] == {"used": 143, "available": 160}
    assert area["hierarchy_rows"]["road_mac_probe"] == 1
    print("SELF_TEST_PASS")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preflight", "summarize", "self-test"))
    args = parser.parse_args()
    raise SystemExit({"preflight": preflight, "summarize": summarize, "self-test": self_test}[args.action]())
