"""MAC接受控制单属性诊断；输出只写本候选，历史依赖只读。"""
import argparse
from collections import Counter
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "control_operand_hold_20261009"
spec = importlib.util.spec_from_file_location("frozen_control_build", BASE / "run.py")
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
app, old, build, tools = control.app, control.app.old, control.build, control.tools
for module in (control, app, old, build, tools):
    module.ROOT = ROOT
old.BASE = BASE
build.BASE = BASE
MAC, save = build.MAC, build.save
RUNNER = "down2_dynamic_tile_runner.v"
DECLARATION = "\twire flag_mac_input_accept;"
ATTRIBUTE = "\t(* max_fanout = 16 *) wire flag_mac_input_accept;"


def frozen():
    path = ROOT / "frozen.json"
    if not path.exists():
        records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
        records.update({str(BASE / name): sha for name, sha in json.loads(
            (BASE / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        records.update({str(p): tools.digest(p) for p in BASE.rglob("*")
            if p.is_file() and "work" not in p.relative_to(BASE).parts})
        dependencies = [Path(module.__file__) for module in (control, app, old, build, tools)]
        dependencies += [tools.TD, build.MSIM / "vsim.exe", build.MSIM / "vlog.exe",
            *[MAC / "physical_opt" / name for name in ("build.tcl", "shell.sdc", "shell.adc")],
            ROOT.parents[3] / "model.py", ROOT.parents[3] / "contract.json",
            ROOT.parents[1] / "graph_artifacts/graph.json",
            ROOT.parents[1] / "deployment_contract.json"]
        records.update({str(p): tools.digest(p) for p in dependencies})
        save(path, records)
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if tools.digest(Path(name)) != sha]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def bindings():
    assert all(module.ROOT == ROOT for module in (control, app, old, build, tools))
    assert old.BASE == BASE and build.BASE == BASE
    save(ROOT / "path_bindings.json", {"writable_roots": {name: str(module.ROOT)
        for name, module in (("control", control), ("app", app), ("old", old), ("build", build), ("tools", tools))},
        "comparison_readonly_base": str(old.BASE), "engineering_readonly_template": str(tools.BASE),
        "collect_readonly_parser": str(ROOT.parent / "dw_task_overlap_20261009/collect.py"),
        "all_stage_workdirs_under_candidate": True})


def prepare():
    for source, target in (("rtl", "baseline"), ("rtl", "rtl"),
                           ("interfaces", "interfaces"), ("tests", "tests")):
        assert not (ROOT / target).exists(), "prepare仅执行一次"
        shutil.copytree(BASE / source, ROOT / target)
    for name in ("inspect_undriven.tcl", "dw_task_overlap.wave.json"):
        shutil.copyfile(BASE / name, ROOT / name)
    assert len(list((ROOT / "rtl").glob("*.v"))) == 8
    save(ROOT / "input_manifest.json", {str(p): tools.digest(p) for directory in
        (ROOT / "baseline", ROOT / "tests", ROOT / "interfaces") for p in directory.rglob("*") if p.is_file()})
    work = tools.fresh("preflight")
    result = tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings",
        tools.SKILL / "config/defaults.json"], work, "dependencies", allowed=(0, 1))
    dependency = json.loads(result[result.index("{"):])
    save(work / "dependencies.json", dependency)
    assert dependency["required_ok"]
    save(ROOT / "authorization.json", {"user_request": "按照这个计划进行，直到必须重新考虑或反馈",
        "scope": "P1A独立候选及相关测试构建和隔离TD诊断",
        "strict_gate_waived": False, "isolated_diagnostics_despite_historical_gate_failures": True,
        "kernel_interface_numeric_ii_reset_change_authorized": False,
        "new_timing_exceptions_authorized": False, "training_or_board_authorized": False})
    save(ROOT / "status.json", {"stage": "baseline_frozen", "deployment_release": False,
        "production_modified": False, "physical_rebuilt": False})


def review():
    work = tools.fresh("baseline_review")
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
        "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
        ROOT / "baseline" / RUNNER, "--report-json", work / "review.json"], work, "review", allowed=(0, 1, 2))
    assert (work / "review.json").exists()
    build.gate("baseline")


def scope():
    names = sorted(p.name for p in (ROOT / "rtl").glob("*.v"))
    assert names == sorted(p.name for p in (BASE / "rtl").glob("*.v"))
    changed = []
    for name in names:
        baseline = (ROOT / "baseline" / name).read_bytes()
        assert baseline == (BASE / "rtl" / name).read_bytes(), name
        candidate = (ROOT / "rtl" / name).read_bytes()
        if baseline != candidate:
            changed.append(name)
            assert name == RUNNER
            assert candidate.count(ATTRIBUTE.encode()) == 1
            assert candidate.replace(ATTRIBUTE.encode(), DECLARATION.encode(), 1) == baseline
    assert changed == [RUNNER], changed
    a = (ROOT / "baseline" / RUNNER).read_text(encoding="utf-8")
    b = (ROOT / "rtl" / RUNNER).read_text(encoding="utf-8")
    patch = "".join(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
        fromfile="baseline/" + RUNNER, tofile="candidate/" + RUNNER))
    (ROOT / "rtl_change.diff").write_text(patch, encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": changed, "unchanged_rtl_count": 7,
        "only_change": "max_fanout=16 on existing MAC input acceptance wire",
        "arithmetic_ports_ii_reset_handshake_fault_cycles_unchanged": True,
        "constraints_unchanged": True, "additional_pipeline_stages": 0,
        "sources": {str(ROOT / "rtl" / name): tools.digest(ROOT / "rtl" / name) for name in names}})


def gate_compare():
    gates = {label: json.loads((ROOT / ("gate_" + label) / "gate.json").read_text(encoding="utf-8"))
             for label in ("baseline", "candidate", "testbench")}
    def findings(gate):
        return Counter((item.get("code") or item.get("rule", ""), str(item.get("line")), item.get("message", ""),
            Path(item.get("path") or (item.get("location") or {}).get("file") or "").name, item.get("severity", ""))
            for item in gate.get("issues", []))
    assert findings({"issues": [{"code": "probe", "path": None, "location": None}]})
    a, b = gates["baseline"], gates["candidate"]
    added = list((findings(b) - findings(a)).elements())
    removed = list((findings(a) - findings(b)).elements())
    # 仅审本次属性字面量的格式诊断；保留严格失败，不改检查器或交付门。
    reviewed_style = [item for item in added if item[0] == "VG138" and item[1] == "165"
                      and item[3] == RUNNER and item[2] == "常量未显式声明位宽和进制。"]
    unreviewed = [item for item in added if item not in reviewed_style]
    save(ROOT / "gate_comparison.json", {"baseline": {k: a[k] for k in ("errors", "strict_warnings", "delivery_ready")},
        "candidate": {k: b[k] for k in ("errors", "strict_warnings", "delivery_ready")},
        "added_finding_identities": added, "removed_finding_identities": removed,
        "reviewed_attribute_style_only": reviewed_style, "unreviewed_new_findings": unreviewed,
        "style_review_basis": "唯一差异为综合属性的正整数字面量16，不是数据通路操作数；scope逐字节证明其余不变。",
        "delivery_ready": False, "diagnostic_authorization": "authorization.json",
        "note": "Exit0不是门禁通过；继续前读取实际compile/parse及语义审查。"})
    assert a["checks"]["compile"]["status"] == b["checks"]["compile"]["status"] == "passed"
    assert b["checks"]["compile"]["parse_errors"] == 0
    assert not unreviewed, "新增未审阅门禁诊断，不自动进入功能或物理步骤"


def collect():
    previous_base = old.BASE
    try:
        old.BASE = ROOT.parent / "dw_task_overlap_20261009"
        old.collect()
    finally:
        old.BASE = previous_base
    # 原collect中的旧整网预算仅为兼容输出；新任务账以budget/current_tile_budget.json为准。
    save(ROOT / "legacy_budget_boundary.json", {"legacy_file": "layer_budget.json", "authoritative": False,
        "current_task_account": "budget/current_tile_budget.json", "full_network_fps_proven": False})


def functional():
    scope()
    gate_compare()
    for name, action in (("simulate", build.simulate), ("mac_sim", control.mac_sim),
                         ("boundary", old.boundary), ("compare", old.compare),
                         ("shell_rtl", lambda: build.shell(False))):
        print("FUNCTIONAL_STAGE", name, flush=True)
        action()


def implementation():
    scope()
    gate_compare()
    authorization = json.loads((ROOT / "authorization.json").read_text(encoding="utf-8"))
    assert authorization["isolated_diagnostics_despite_historical_gate_failures"]
    paths = [ROOT / "mac_sim/receipt.json", ROOT / "shell_rtl/receipt.json"]
    for pointer in ("simulation_current.json", "boundary_current.json"):
        work = Path(json.loads((ROOT / pointer).read_text(encoding="utf-8"))["work"])
        work.resolve().relative_to(ROOT)
        paths.append(work / "receipt.json")
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["all_passed"]
        assert all(tools.digest(Path(p)) == sha for p, sha in data["sources"].items())
    for name, action in (("undriven", build.undriven), ("physical", build.physical), ("collect", collect)):
        save(ROOT / "progress.json", {"stage": name, "functional_complete_cases": 64,
            "core_cycles": 1687, "deployment_release": False, "production_modified": False})
        print("IMPLEMENTATION_STAGE", name, flush=True)
        action()
    save(ROOT / "progress.json", {"stage": "physical_collected_pending_path_review",
        "functional_complete_cases": 64, "core_cycles": 1687, "deployment_release": False})


def finish():
    scope()
    receipts = {}
    for name in ("simulation", "load_boundary", "mac_sim", "shell_rtl", "shell_routed", "undriven"):
        if name in ("simulation", "load_boundary"):
            pointer = "simulation_current.json" if name == "simulation" else "boundary_current.json"
            folder = Path(json.loads((ROOT / pointer).read_text(encoding="utf-8"))["work"])
            folder.resolve().relative_to(ROOT)
            path = folder / "receipt.json"
        else:
            path = ROOT / name / "receipt.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert not data.get("loaded", [])
        if name == "undriven":
            assert data["scope"] == "elaborated top net query; not a complete mapped primitive pin proof"
            assert all("PINS 0 DRIVER 0" in record for record in data["records"])
        else:
            assert data["all_passed"]
        assert all(tools.digest(Path(source)) == sha for source, sha in data["sources"].items())
        receipts[name] = str(path.relative_to(ROOT))
    comparison = json.loads((ROOT / "cycle_comparison.json").read_text(encoding="utf-8"))
    assert comparison["identical_summary_rows"] == 64
    assert comparison["old_core_cycles"] == comparison["new_core_cycles"] == 1687
    # 继承的活动分解须绑定最初测量trace，不只比较中间参考汇总计数。
    profile = json.loads((ROOT / "analysis.json").read_text(encoding="utf-8"))
    origin = Path(profile["simulation"])
    current = Path(json.loads((ROOT / "simulation_current.json").read_text(encoding="utf-8"))["work"])
    profile_traces = []
    for suite in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        for suffix in ("_trace.csv", "_windows.csv"):
            name = suite + suffix
            a, b = origin / name, current / name
            profile_traces.append({"name": name, "origin_sha256": tools.digest(a),
                "current_sha256": tools.digest(b), "byte_identical": a.read_bytes() == b.read_bytes()})
    save(ROOT / "profile_origin_comparison.json", {"original_profile_simulation": str(origin),
        "current_simulation": str(current), "traces": profile_traces,
        "all_identical": all(row["byte_identical"] for row in profile_traces)})
    assert all(row["byte_identical"] for row in profile_traces), "原活动分解输入不同，必须重新测量"
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    negatives = physical["negative_paths"]
    counts = {kind: len({p["end"] for p in negatives if p["kind"] == kind and not p["external"]})
              for kind in ("setup", "hold", "recovery", "removal")}
    gates = {label: json.loads((ROOT / ("gate_" + label) / "gate.json").read_text(encoding="utf-8"))
             for label in ("candidate", "testbench")}
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        assert tools.digest(ROOT / "physical" / name) == tools.digest(MAC / "physical_opt" / name)
    save(ROOT / "status.json", {"stage": "evaluated_internal_clean_not_deployment" if not any(counts.values())
        else "evaluated_internal_timing_failed", "receipts": receipts,
        "internal_unique_failed_endpoints_by_check": counts,
        "internal_timing": physical["reports"]["coverage_100000_all_paths"]["internal"],
        "resources_including_shell": physical["resources_including_shell"], "core_cycles": 1687,
        "strict_gates": {key: {k: value[k] for k in ("errors", "strict_warnings", "delivery_ready")}
            for key, value in gates.items()}, "physical_rebuilt": True, "sdf_simulation": False,
        "external_contract_signed_off": False, "production_modified": False, "deployment_release": False,
        "training_started": False, "bitstream_generated": False, "board_or_flash_used": False})
    frozen()
    files = [p for p in ROOT.rglob("*") if p.is_file() and "work" not in p.relative_to(ROOT).parts
             and p.name != "evidence_hashes.json"]
    save(ROOT / "evidence_hashes.json", {str(p.relative_to(ROOT)): tools.digest(p) for p in files})
    print("FINALIZED_INTERNAL_FAILURES", counts, "NOT_PRODUCTION_READY", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "scope", "gates", "gate_compare", "simulate",
        "mac_sim", "boundary", "compare", "shell_rtl", "functional", "implementation", "undriven", "physical", "collect", "shell_routed", "finish"))
    stage = parser.parse_args().stage
    frozen()
    bindings()
    try:
        if stage in ("prepare", "review", "scope", "gate_compare", "collect", "functional", "implementation", "finish"):
            globals()[stage]()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage in ("boundary", "compare"):
            getattr(old, stage)()
        elif stage == "mac_sim":
            control.mac_sim()
        else:
            getattr(build, stage)()
    except Exception as error:
        failure = tools.fresh(stage + "_failure")
        save(failure / "receipt.json", {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
