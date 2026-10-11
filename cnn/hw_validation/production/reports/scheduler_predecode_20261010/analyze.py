"""只分析本候选证据；所有输出由现有受限保存函数写入本目录。"""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
from run import BASE, ROOT, tools, save, frozen


def gate_delta():
    old = json.loads((ROOT / "gate_baseline/gate.json").read_text(encoding="utf-8"))
    new = json.loads((ROOT / "gate_candidate/gate.json").read_text(encoding="utf-8"))
    a, b = old["delivery_issues_by_rule"], new["delivery_issues_by_rule"]
    changed = {key: b.get(key, 0) - a.get(key, 0) for key in sorted(a.keys() | b.keys())
               if a.get(key, 0) != b.get(key, 0)}
    # Ignore moved line numbers, not diagnostic identity; retain the full original gate reports.
    def identity(issue):
        return issue["code"], issue["path"], issue["message"], json.dumps(issue.get("metadata", {}), sort_keys=True)
    before = Counter(identity(issue) for issue in old["issues"])
    after = Counter(identity(issue) for issue in new["issues"])
    added = after - before
    save(ROOT / "gate_delta.json", {"baseline_errors": old["errors"], "candidate_errors": new["errors"],
        "delta_by_rule": changed, "checks": new["checks"],
        "added": [{"code": code, "path": path, "message": message, "metadata": json.loads(metadata), "count": count}
            for (code, path, message, metadata), count in added.items()],
        "new_counter_width_note": "Both 5bit additions are guarded: PW input0..6 yields1..7; DW input0..14 yields1..15. All32 binary values were checked in control_reference. No carry needed by the contract.",
        "cone_note": "Static operation-cone diagnostics are not routed logic levels or STA evidence; no waiver applied.",
        "production_delivery": False})
    print("GATE_DELTA", changed, "ADDED_IDENTITIES", len(added), flush=True)


def physical():
    current = Path(json.loads((ROOT / "physical_current.json").read_text(encoding="utf-8"))["work"])
    data = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    source = ROOT.parent / "dw_task_overlap_20261009/collect.py"
    spec = importlib.util.spec_from_file_location("physical_path_reader", source)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    records = reader.paths(current / "coverage_100000_all_paths.timing")
    groups = {}
    patterns = {"output_counter": r"/cnt_output_reg\[", "weight_capture": r"/reg_mac_weight_reg\[",
                "mac_dsp_ce": r"/road_mac_probe_Inst_tile/mult\d+_.*\.ce\["}
    for label, pattern in patterns.items():
        selected = [p for p in records if p["kind"] == "setup" and not p["external"] and re.search(pattern, p["end"])]
        groups[label] = {"count": len(selected), "negative": sum(p["slack_ns"] < 0 for p in selected),
                         "worst": min(selected, key=lambda p: p["slack_ns"]) if selected else None}
    routed = (current / "routed_netlist.v").read_text(encoding="utf-8")
    negative = [p for p in data["negative_paths"] if not p["external"]]
    unique_by_check = {kind: len({p["end"] for p in negative if p["kind"] == kind})
                       for kind in sorted({p["kind"] for p in negative})}
    launches = {}
    for launch in sorted({p["begin"] for p in negative}):
        cell = launch.rsplit(".", 1)[0]
        marker = "\\" + cell + "  ("
        body = routed.split(marker, 1)[1].split(");", 1)[0] if marker in routed else ""
        launches[launch] = {"negative_count": sum(p["begin"] == launch for p in negative),
            "packed_output_pins": dict(re.findall(r"\.(oqa|oqb)\((.*?)\)", body)),
            "warning": "A physical cell may pack unrelated registers. Its name alone does not identify the launch signal."}
    baselines = {}
    for name in ("control_operand_hold_20261009", BASE.name):
        old = json.loads((ROOT.parent / name / "physical_analysis.json").read_text(encoding="utf-8"))
        baselines[name] = {"internal": old["reports"]["coverage_100000_all_paths"]["internal"],
                           "resources_including_shell": old["resources_including_shell"]}
    save(ROOT / "control_path_diagnosis.json", {"timing_groups": groups, "negative_launch_mapping": launches,
        "internal_negative_path_records": len(negative),
        "internal_unique_failed_endpoints_by_check": unique_by_check,
        "count_note": "The same physical endpoint can appear under multiple launch path groups; do not call path records unique endpoints.",
        "baselines": baselines, "candidate_internal": data["reports"]["coverage_100000_all_paths"]["internal"],
        "candidate_resources_including_shell": data["resources_including_shell"],
        "scope": "Exact mapped-cell output pin lookup plus original STA reports, not an HDL parser or production signoff",
        "sources": {str(p): tools.digest(p) for p in (source, current / "routed_netlist.v",
            current / "coverage_100000_all_paths.timing", ROOT / "physical_analysis.json")}})
    print("PHYSICAL_DIAGNOSIS", {k: (v["count"], v["negative"]) for k, v in groups.items()}, flush=True)


if __name__ == "__main__":
    frozen()
    try:
        gate_delta()
        if (ROOT / "physical_analysis.json").exists():
            physical()
        receipts = list(ROOT.glob("shell_routed*/receipt.json"))
        if receipts:
            work = max(receipts, key=lambda p: p.stat().st_mtime_ns).parent
            logs = list(work.glob("*_stress.log"))
            save(ROOT / "netlist_warnings.json", {"not_waived": True,
                "counts_by_simulator_code": {p.name: dict(Counter(re.findall(
                    r"\((vopt-\d+|vsim-\d+)\)", p.read_text(encoding="utf-8", errors="replace")))) for p in logs},
                "scope": "Vendor primitive port/mode/width and optimizer warnings retained, not exhaustively closed",
                "sources": {str(p): tools.digest(p) for p in logs}})
    finally:
        frozen()
