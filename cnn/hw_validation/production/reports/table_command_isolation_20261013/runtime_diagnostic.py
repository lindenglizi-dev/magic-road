"""从已冻结 gate.db 运行关闭后布线优化的实际布线诊断；不重读约束、不生成位流。"""
import importlib.util
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parent
CHECKPOINT = ROOT / "physical_attempt3"
TOOL = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
GATE_SHA256 = "0d9a237a174d69bd543e9d9b852b69b20cf81004031d94eeef78d40dd797b5c3"

spec = importlib.util.spec_from_file_location("table_candidate_run", ROOT / "run.py")
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
save, sha, command, fresh = candidate.save, candidate.sha, candidate.command, candidate.fresh


def source_hashes(work, manifest):
    return {item["path"]: sha((work / item["path"]).resolve())
            for item in manifest["sources"]}


def runtime_build():
    parent = (CHECKPOINT / "build.tcl").read_text(encoding="utf-8").splitlines()
    start = parent.index("set_param place effort high")
    old_tail = parent[start:]
    high = "set_param route post_route_opt high"
    extra = "set_param route postrt_opt_extra_round 4"
    assert old_tail.count(high) == 1
    assert old_tail.count(extra) == 1
    assert old_tail[-1] == "close_project"

    new_tail = ["set_param route post_route_opt off" if line == high else line
                for line in old_tail if line not in (extra, "close_project")]
    old_reports = old_tail[old_tail.index("report_param"):old_tail.index("close_project")]
    new_reports = new_tail[new_tail.index("report_param"):]
    assert new_reports == old_reports, "报告、端点范围或完成标记不得改变"

    prefix = [
        "# Runtime diagnostic imported from the frozen gate checkpoint; no bitstream.",
        "import_device ph1_35p.db -package PH1P35MDG324 -speed 3",
        "import_db gate.db",
        "update_timing",
        "set imported_clocks [get_clocks *]",
        "if {[llength $imported_clocks] != 1} { error \"Expected one imported frontend clock\" }",
        "set imported_clock_name [get_property NAME $imported_clocks]",
        "if {![string equal $imported_clock_name {frontend_clk}]} { error \"Expected imported frontend_clk\" }",
        "report_clock_summary -clocks $imported_clocks -expand_buckets -debug -file imported_clock_before_place.rpt",
        "puts \"FRONTEND_IMPORTED_CLOCK $imported_clock_name count=[llength $imported_clocks]\"",
        "",
    ]
    build = "\n".join(prefix + new_tail + ["exit"]) + "\n"
    for forbidden in ("open_project", "read_sdc", "read_adc", "close_project", "bitgen"):
        assert forbidden not in build
    return build, {
        "checkpoint_build_sha256": sha(CHECKPOINT / "build.tcl"),
        "first_reused_line": "set_param place effort high",
        "only_parameter_change": {"route.post_route_opt": {"from": "high", "to": "off"}},
        "omitted_checkpoint_parameter": "set_param route postrt_opt_extra_round 4",
        "reports_and_endpoint_commands_unchanged": True,
        "constraint_commands_replayed": False,
        "project_opened": False,
        "bitstream_requested": False,
        "classification": "actual routed runtime diagnostic; not equivalent to high+4 closure recipe",
    }


def main():
    candidate.check()
    assert sha(CHECKPOINT / "gate.db") == GATE_SHA256
    work = fresh("physical_runtime")

    for name in ("gate.db", "source_manifest.json", "road_frontend_shared_core.al",
                 "frontend.sdc", "frontend.adc"):
        shutil.copyfile(CHECKPOINT / name, work / name)
        assert sha(work / name) == sha(CHECKPOINT / name)
    shutil.copyfile(ROOT / "physical_report.py", work / "physical_report.py")
    assert sha(work / "physical_report.py") == sha(ROOT / "physical_report.py")
    for name in ("tool_hash.json", "source_check_before.json", "frozen_scheduler_check.json"):
        shutil.copyfile(CHECKPOINT / name, work / ("checkpoint_" + name))

    build, regime = runtime_build()
    (work / "build.tcl").write_text(build, encoding="utf-8")
    regime.update({
        "runtime_build_sha256": sha(work / "build.tcl"),
        "gate_checkpoint": str(CHECKPOINT / "gate.db"),
        "gate_checkpoint_sha256": GATE_SHA256,
    })
    save(work / "optimization_regime.json", regime)

    manifest = json.loads((work / "source_manifest.json").read_text(encoding="utf-8"))
    before = source_hashes(work, manifest)
    assert all(before[item["path"]] == item["sha256"] for item in manifest["sources"])
    save(work / "source_check_before.json", before)

    baseline = json.loads((ROOT / "baseline_sources.json").read_text(encoding="utf-8"))
    schedulers = {name: sha(ROOT / "rtl" / name)
                  for name in ("road_stem_tile_scheduler.v", "road_down2_tile_scheduler.v")}
    assert all(digest == baseline[str(Path("rtl") / name)]
               for name, digest in schedulers.items())
    simulation_path = sorted(ROOT.glob("simulation*/receipt.json"),
                             key=lambda path: path.stat().st_mtime)[-1]
    simulation = json.loads(simulation_path.read_text(encoding="utf-8"))
    simulated = {Path(name).name: digest
                 for name, digest in simulation["source_hashes"].items()}
    current = {path.name: sha(path) for path in
               (candidate.TOP, candidate.STEM, ROOT / "rtl/road_down2_tile_scheduler.v")}
    assert simulation["status"] == "PASS"
    assert all(simulated.get(name) == digest for name, digest in current.items())
    save(work / "frozen_scheduler_check.json", {
        "status": "PASS", "baseline": schedulers, "simulation": simulated,
        "current_physical_sources": current, "simulation_receipt": str(simulation_path)})

    checkpoint_tool = json.loads((CHECKPOINT / "tool_hash.json").read_text(encoding="utf-8"))
    tool_digest = sha(TOOL)
    assert checkpoint_tool[str(TOOL)] == tool_digest
    assert sha(work / "build.tcl") != sha(CHECKPOINT / "build.tcl")
    save(work / "tool_hash.json", {
        str(TOOL): tool_digest,
        "tool_identical_to_checkpoint": True,
        "gate_db": {"expected": GATE_SHA256, "actual": sha(work / "gate.db")},
        "cloned_inputs_identical_to_checkpoint": {
            name: sha(work / name) == sha(CHECKPOINT / name)
            for name in ("source_manifest.json", "road_frontend_shared_core.al",
                         "frontend.sdc", "frontend.adc")},
        "summary_generator_sha256": sha(work / "physical_report.py"),
        "checkpoint_file_identity": {
            "frontend.sdc": sha(work / "frontend.sdc") == sha(CHECKPOINT / "frontend.sdc"),
            "frontend.adc": sha(work / "frontend.adc") == sha(CHECKPOINT / "frontend.adc"),
            "build.tcl": sha(work / "build.tcl") == sha(CHECKPOINT / "build.tcl"),
        },
        "build_identical_to_checkpoint": False,
        "optimization_regime": "optimization_regime.json",
    })

    command([sys.executable, "-B", work / "physical_report.py", "preflight"],
            work, "preflight_before")
    try:
        output = command([TOOL, "build.tcl"], work, "td_launcher")
    finally:
        after = source_hashes(work, manifest)
        save(work / "source_check_after.json", after)
        assert after == before
        candidate.check()

    assert 'finish command "route"' in output
    assert "REPORT_COMPLETION_DONE" in output
    command([sys.executable, "-B", work / "physical_report.py", "summarize"],
            work, "summarize", allowed=(0, 1))
    candidate.check()
    print(f"RUNTIME_DIAGNOSTIC_DONE {work}", flush=True)


if __name__ == "__main__":
    main()
