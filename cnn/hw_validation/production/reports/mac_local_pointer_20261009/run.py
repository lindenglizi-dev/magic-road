"""MAC 本地读指针隔离候选；只在本目录输出，复用冻结验证流程。"""
import argparse
import difflib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "control_operand_hold_20261009"
spec = importlib.util.spec_from_file_location("held_control", BASE / "run.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
build, tools, save = previous.build, previous.tools, previous.save
for module in (previous, previous.app, previous.app.old, build, tools):
    module.ROOT = ROOT
build.BASE = BASE
previous.app.old.BASE = BASE
MAC, frozen = build.MAC, build.frozen


def scope():
    changes = []
    patch = []
    for path in sorted((ROOT / "rtl").glob("*.v")):
        original = ROOT / "baseline" / path.name
        if tools.digest(path) != tools.digest(original):
            changes.append(path.name)
            a = original.read_text(encoding="utf-8")
            b = path.read_text(encoding="utf-8")
            assert b.replace("(* preserve *) ", "", 1) == a
            assert b.count("(* preserve *) reg [1:0]ptr_result_read;") == 1
            patch.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                fromfile="frozen/" + path.name, tofile="candidate/" + path.name))
    assert changes == ["road_mac_probe.v"], changes
    (ROOT / "rtl_change.diff").write_text("".join(patch), encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": changes, "attribute_only": True,
        "unchanged_rtl_count": 7, "ports_arithmetic_ii_latency_reset_fault_unchanged": True,
        "sources": {str(p.relative_to(ROOT)): tools.digest(p) for p in (ROOT / "rtl").glob("*.v")}})


previous.scope = scope


def prepare():
    for source, target in (("rtl", "baseline"), ("rtl", "rtl"), ("interfaces", "interfaces"), ("tests", "tests")):
        shutil.copytree(BASE / source, ROOT / target)
    for name in ("inspect_undriven.tcl", "dw_task_overlap.wave.json"):
        shutil.copyfile(BASE / name, ROOT / name)
    work = tools.fresh("preflight")
    output = tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings",
        tools.SKILL / "config/defaults.json"], work, "dependencies", allowed=(0, 1))
    dependency = json.loads(output[output.index("{"):])
    save(work / "dependencies.json", dependency)
    assert dependency["required_ok"]
    save(ROOT / "status.json", {"stage": "baseline_frozen", "production_modified": False,
        "deployment_release": False, "physical_rebuilt": False})


def finish():
    scope()
    receipts = {}
    for folder in ("simulation", "load_boundary", "mac_sim", "shell_rtl", "shell_routed", "undriven"):
        path = max(ROOT.glob(folder + "*/receipt.json"), key=lambda p: p.stat().st_mtime_ns)
        data = json.loads(path.read_text(encoding="utf-8"))
        assert not data.get("loaded", []) and data.get("all_passed", folder == "undriven"), path
        assert all(tools.digest(Path(p)) == sha for p, sha in data["sources"].items()), path
        receipts[folder] = str(path.relative_to(ROOT))
    manifest = json.loads((ROOT / "physical/input_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest) == 8 and all(tools.digest(Path(p)) == sha for p, sha in manifest.items())
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        assert tools.digest(ROOT / "physical" / name) == tools.digest(BASE / "physical" / name), name
    comparison = json.loads((ROOT / "cycle_comparison.json").read_text(encoding="utf-8"))
    assert comparison["identical_summary_rows"] == 64 and comparison["new_core_cycles"] == 1687
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    internal = physical["reports"]["coverage_100000_all_paths"]["internal"]
    clean = not internal["negative"]
    gates = {kind: json.loads((ROOT / ("gate_" + kind) / "gate.json").read_text(encoding="utf-8"))
        for kind in ("candidate", "testbench")}
    assert not any(gate["delivery_ready"] for gate in gates.values())
    save(ROOT / "status.json", {"stage": "evaluated_internal_clean_not_deployment" if clean else
        "evaluated_internal_timing_failed", "internal_clean_in_report": clean, "internal_timing": internal,
        "resources_including_shell": physical["resources_including_shell"], "receipts": receipts,
        "core_cycles": 1687, "strict_gates": {key: {name: value[name]
            for name in ("errors", "strict_warnings", "delivery_ready")} for key, value in gates.items()},
        "external_contract_signed_off": False, "deployment_release": False, "production_modified": False,
        "candidate_promoted": False, "comparison_baseline": str(BASE),
        "physical_rebuilt": True, "sdf_simulation": False, "training_started": False,
        "bitstream_generated": False, "board_or_flash_used": False})
    build.frozen()
    paths = list((ROOT / "rtl").rglob("*")) + list((ROOT / "physical").glob("*"))
    paths += list(ROOT.glob("*.json")) + list(ROOT.glob("*.md"))
    paths += [ROOT / "run.py", ROOT / "rtl_change.diff"] + [ROOT / p for p in receipts.values()]
    paths += [ROOT / ("gate_" + key) / "gate.json" for key in gates]
    save(ROOT / "evidence_hashes.json", {str(p.relative_to(ROOT)): tools.digest(p)
        for p in sorted(set(paths)) if p.is_file() and p.name != "evidence_hashes.json"})
    print("INTERNAL_CLEAN", clean, flush=True)


def diagnose():
    path = ROOT.parent / "dw_task_overlap_20261009/collect.py"
    spec = importlib.util.spec_from_file_location("path_reader", path)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    records = reader.paths(ROOT / "physical/coverage_100000_all_paths.timing")
    groups = {}
    for label, pattern in (("mac_dsp_ce", r"road_mac_probe_Inst_tile/mult\d+_.*\.ce\["),
                           ("mac_local_pointer", r"road_mac_probe_Inst_tile/ptr_result_read_reg")):
        selected = [p for p in records if p["kind"] == "setup" and not p["external"] and
                    re.search(pattern, p["end"] if label == "mac_dsp_ce" else p["begin"])]
        groups[label] = {"count": len(selected), "negative": sum(p["slack_ns"] < 0 for p in selected),
                         "worst": min(selected, key=lambda p: p["slack_ns"]) if selected else None}
    pointers = {}
    for label, directory in (("baseline", BASE), ("candidate", ROOT)):
        text = (directory / "physical/gate_netlist.v").read_text(encoding="utf-8")
        pointers[label] = {name: len(re.findall(r"\\[^\s]*" + name + r"_reg\[[01]\]\s+\(", text))
            for name in ("ptr_result_read", "ptr_pw_meta_read")}
    assert pointers["candidate"]["ptr_result_read"] == 2, pointers
    assert pointers["candidate"]["ptr_pw_meta_read"] == 2, pointers
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    negative = [p for p in physical["negative_paths"] if not p["external"]]
    launch = "down2_dynamic_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/u_chain/u_post/u_round/fault_o_reg_syn_3"
    routed = (ROOT / "physical/routed_netlist.v").read_text(encoding="utf-8")
    body = routed.split("\\" + launch + "  (", 1)[1].split(");", 1)[0]
    assert ".oqb(\\down2_dynamic_tile_runner_Inst_shell/road_mac_probe_Inst_tile/ptr_result_read [0])" in body
    groups["packed_local_pointer_negative"] = {"count": sum(p["begin"] == launch + ".clk" for p in negative),
        "physical_cell": launch, "physical_pin": "oqb", "actual_q_signal": "MAC ptr_result_read[0]",
        "other_register_in_same_cell": "u_post/u_round/o_fault on oqa",
        "note": "The cell name is not the semantic launch register; name-only pointer matching above misses packed FFs"}
    save(ROOT / "local_pointer_diagnosis.json", {"mapped_pointer_registers": pointers,
        "timing_groups": groups, "scope": "Exact mapped instance-name and STA-record queries, not a second HDL parser",
        "sources": {str(p): tools.digest(p) for p in
            (ROOT / "physical/gate_netlist.v", ROOT / "physical/coverage_100000_all_paths.timing")}})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "scope", "simulate", "physical", "gates",
        "specs", "mac_sim", "boundary", "compare", "collect", "shell_rtl", "shell_routed", "undriven", "finish", "diagnose"))
    stage = parser.parse_args().stage
    build.frozen()
    try:
        if stage in ("prepare", "scope", "finish", "diagnose"):
            globals()[stage]()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage in ("boundary", "compare"):
            getattr(previous.app.old, stage)()
        elif stage in ("review", "specs", "mac_sim", "collect"):
            getattr(previous, stage)()
        else:
            getattr(build, stage)()
    except Exception as error:
        save(ROOT / (stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        build.frozen()
