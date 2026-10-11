"""比较真实STA及映射证据；不改变RTL、约束或失败状态。"""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

import run

ROOT, BASE, tools, save = run.ROOT, run.BASE, run.tools, run.save
parser_spec = importlib.util.spec_from_file_location("frozen_path_reader",
    ROOT.parent / "dw_task_overlap_20261009/collect.py")
reader = importlib.util.module_from_spec(parser_spec)
parser_spec.loader.exec_module(reader)


def breakdown(records):
    result = {}
    for scope in ("internal", "external"):
        rows = [row for row in records if row["external"] == (scope == "external")]
        result[scope] = {}
        for kind in ("setup", "hold", "recovery", "removal"):
            group = [row for row in rows if row["kind"] == kind]
            negative = [row for row in group if row["slack_ns"] < 0]
            result[scope][kind] = {"worst_ns": min((row["slack_ns"] for row in group), default=None),
                "reported_path_records": len(group), "negative_path_records": len(negative),
                "unique_failed_endpoints": len({row["end"] for row in negative}),
                "reported_corners": sorted({row["corner"] for row in group}),
                "worst_path": min(group, key=lambda row: row["slack_ns"]) if group else None}
    return result


def main():
    physical = Path(json.loads((ROOT / "physical_current.json").read_text(encoding="utf-8"))["work"])
    physical.resolve().relative_to(ROOT)
    assert physical == ROOT / "physical"
    db_hash = tools.digest(physical / "pr.db")
    work = tools.fresh("mapping_query")
    shutil.copyfile(ROOT / "inspect_mapping.tcl", work / "inspect.tcl")
    log = tools.command([tools.TD, "inspect.tcl"], work, "td", timeout=300)
    assert "MAPPING_QUERY_DONE" in log and "ERROR:" not in log
    assert tools.digest(physical / "pr.db") == db_hash
    save(work / "receipt.json", {"read_only_db_sha256": db_hash,
        "script_sha256": tools.digest(work / "inspect.tcl"),
        "accept_net_records": [line for line in log.splitlines() if line.startswith("ACCEPT_NET")],
        "query_scope": "acceptance-control mapped nets and clock summary; not full undriven primitive proof"})
    traces = []
    old_sim = Path(json.loads((BASE / "simulation_current.json").read_text(encoding="utf-8"))["work"])
    new_sim = Path(json.loads((ROOT / "simulation_current.json").read_text(encoding="utf-8"))["work"])
    for suite in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        for suffix in ("_trace.csv", "_windows.csv"):
            a, b = old_sim / (suite + suffix), new_sim / (suite + suffix)
            traces.append({"file": b.name, "reference_sha256": tools.digest(a),
                "candidate_sha256": tools.digest(b), "byte_identical": a.read_bytes() == b.read_bytes()})
    save(ROOT / "trace_comparison.json", {"scope": "fresh RTL traces and windows versus direct reference",
        "traces": traces, "all_identical": all(row["byte_identical"] for row in traces)})
    assert all(row["byte_identical"] for row in traces), "活动轨迹不同须重新逐拍归因，不复用旧分解"
    versions = {}
    for label, directory in (("two_endpoint_reference", BASE), ("mac_ce_attribute_candidate", ROOT)):
        summary = json.loads((directory / "physical_analysis.json").read_text(encoding="utf-8"))
        report = directory / "physical/coverage_100000_all_paths.timing"
        rows = reader.paths(report)
        negative = [row for row in rows if row["slack_ns"] < 0 and not row["external"]]
        versions[label] = {"resources_including_shell": summary["resources_including_shell"],
            "checks": breakdown(rows), "internal_negative_path_records": negative,
            "internal_failure_launch_counts": dict(Counter(row["begin"] for row in negative)),
            "source_manifest": summary["source_manifest"], "report_sha256": tools.digest(report),
            "pr_db_sha256": tools.digest(directory / "physical/pr.db")}
    gate_text = (physical / "gate_netlist.v").read_text(encoding="utf-8")
    mapped_lines = [line for line in gate_text.splitlines() if "flag_mac_input_accept" in line]
    td_log = (physical / "td.log").read_text(encoding="utf-8", errors="replace")
    candidate = versions["mac_ce_attribute_candidate"]
    assert all(row["reported_path_records"] > 0 for row in candidate["checks"]["internal"].values()), \
        "缺少适用内部检查，不能把无报告当通过"
    internal_failed = sum(row["unique_failed_endpoints"] for row in candidate["checks"]["internal"].values())
    result = {"versions": versions, "core_cycles_reference_and_candidate": 1687,
        "additional_latency_cycles": 0, "same_complete_counter_rows": 64,
        "max_fanout_attribute_in_gate_netlist": "max_fanout=16" in gate_text,
        "mapped_acceptance_lines": mapped_lines,
        "mapping_query": str(work.relative_to(ROOT)),
        "synthesis_zeroing_warning_lines": [line for line in td_log.splitlines() if "SYN-5025" in line],
        "setup_hold_recovery_removal_internal_all_nonnegative_in_report": internal_failed == 0,
        "check_corner_boundary": "TD reports select path-specific worst slow/fast corners; not independent signoff of every corner",
        "full_primitive_zeroing_closed": False, "external_signed_off": False, "strict_delivery_ready": False,
        "full_network_fps_proven": False,
        "next_decision": "内部仍失败时不晋升；按实际目标网负载及失败族决定是否需冻结核局部分发授权。"}
    save(ROOT / "physical_comparison.json", result)
    print(json.dumps({"internal": candidate["checks"]["internal"],
        "attribute_recognized": result["max_fanout_attribute_in_gate_netlist"],
        "mapping_query": result["mapping_query"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    run.frozen()
    try:
        main()
    finally:
        run.frozen()
