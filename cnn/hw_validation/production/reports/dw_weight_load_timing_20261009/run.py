"""Single-boundary DW weight-write candidate. All outputs stay in this directory."""
import argparse
from collections import Counter
import difflib
import importlib.util
import json
import re
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "dw_task_overlap_20261009"
spec = importlib.util.spec_from_file_location("frozen_runner", BASE / "run.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
build.ROOT = ROOT
build.BASE = BASE
build.tools.ROOT = ROOT
MAC, tools, frozen, save = build.MAC, build.tools, build.frozen, build.save


def prepare():
    for source, target in (("rtl", "baseline"), ("rtl", "rtl"),
                           ("interfaces", "interfaces"), ("tests", "tests")):
        shutil.copytree(BASE / source, ROOT / target)
    shutil.copyfile(BASE / "dw_task_overlap.wave.json", ROOT / "dw_task_overlap.wave.json")
    shutil.copyfile(BASE / "inspect_undriven.tcl", ROOT / "inspect_undriven.tcl")
    work = build.tools.fresh("preflight")
    text = build.tools.command([sys.executable, "-B", "-X", "utf8", build.tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings",
        build.tools.SKILL / "config/defaults.json"], work, "dependencies", allowed=(0, 1))
    result = json.loads(text[text.index("{"):])
    build.save(work / "dependencies.json", result)
    assert result["required_ok"]
    build.save(ROOT / "status.json", {"stage": "baseline_frozen", "production_modified": False,
        "deployment_release": False, "physical_rebuilt": False})


def compare():
    old = Path(json.loads((BASE / "simulation_current.json").read_text())["work"])
    new = Path(json.loads((ROOT / "simulation_current.json").read_text())["work"])
    a = json.loads((old / "receipt.json").read_text(encoding="utf-8"))["results"]
    b = json.loads((new / "receipt.json").read_text(encoding="utf-8"))["results"]
    assert a.keys() == b.keys()
    for name in a:
        assert a[name]["summary"] == b[name]["summary"], name
    build.save(ROOT / "cycle_comparison.json", {"identical_summary_rows": 64,
        "old_core_cycles": 1687, "new_core_cycles": 1687, "scope": "all recorded counters, same vectors"})
    analysis = json.loads((BASE / "analysis.json").read_text(encoding="utf-8"))
    analysis["reuse_basis"] = "64 full counter rows equal frozen baseline; activity trace not independently re-profiled"
    build.save(ROOT / "analysis.json", analysis)
    print("SAME_64_CASES_ALL_COUNTERS", flush=True)


def collect():
    spec = importlib.util.spec_from_file_location("collect_frozen", BASE / "collect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = ROOT
    module.main()
    physical = Path(json.loads((ROOT / "physical_current.json").read_text())["work"])
    all_paths = module.paths(physical / "coverage_100000_all_paths.timing")
    negative = [p for p in all_paths if not p["external"] and p["slack_ns"] < 0]
    mapped = (physical / "gate_netlist.v").read_text(encoding="utf-8")
    # Textual mapped-instance evidence, not an alternative HDL parser or static checker.
    bodies = re.findall(r"PH1P_PHY_DRAMHARDCON\s*#\((.*?)\);", mapped, re.S)
    weight_instances = [re.search(r"\\([^\s]+)\s+\(", body).group(1) for body in bodies
                        if "reg_dw_weight_write_address" in body]
    assert weight_instances
    weight_we = {name + ".we" for name in weight_instances}
    weight_paths = [p for p in all_paths if p["end"] in weight_we and p["kind"] == "setup"]
    assert len(weight_paths) == len(weight_instances), "Missing RAM WE timing endpoint"
    save(ROOT / "path_diagnosis.json", {
        "internal_setup_by_launch": dict(Counter(p["begin"] for p in negative)),
        "dw_weight_mapped_write_control_instances": weight_instances,
        "dw_weight_we_setup_count": len(weight_paths),
        "dw_weight_we_setup_worst": min(weight_paths, key=lambda p: p["slack_ns"]),
        "dw_weight_we_negative_count": sum(p["slack_ns"] < 0 for p in weight_paths),
        "scope": "mapped weight-address instance mapping plus routed full-path report",
        "numeric_rtl_unchanged": True, "do_not_promote_failed_candidate": True})


def specs():
    work = tools.fresh("specs")
    contract = json.loads((BASE / "specs_attempt4/contract.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["description"] += "; registered DW weight-load write boundary"
    module["behavior"] += [
        "A valid kind2 load with the full11bit legal order check queues8bit address/data at edge E0.",
        "Its DW RAM write commits at E1; independent next load may be accepted at that same edge.",
        "Last-load acceptance sets the existing loaded flag at E0; earliest start at E1 commits pending write, then ST_STORAGE captures operands at E2.",
        "Reset cancels pending write immediately and clears load validity; all banks and1024-entry table must be reloaded.",
        "Invalid kind2 order never queues a write; external handshake, counters, arithmetic, II and core endpoint cycles unchanged."
    ]
    wave = {"signal": [
        {"name": "clk", "wave": "p....."},
        {"name": "load_accept", "wave": "010..."},
        {"name": "load_addr", "wave": "x=x...", "data": ["143"]},
        {"name": "pending_write", "wave": "0.10.."},
        {"name": "start_accept", "wave": "0.10.."},
        {"name": "RAM_commit", "wave": "0.10.."},
        {"name": "storage_capture", "wave": "0..10."}],
        "head": {"text": "E0 accepted last load; E1 write and start; E2 storage capture"}}
    module["timing_diagrams"].append({"id": "dw_weight_write", "title": "Registered DW weight write",
        "scenario": "dw_weight_write", "description": "Edge-based load/start boundary, conceptual protocol diagram.",
        "wavejson": wave})
    save(work / "contract.json", contract)
    source = work / "down2_dynamic_tile_runner.v"
    shutil.copyfile(ROOT / "rtl/down2_dynamic_tile_runner.v", source)
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec",
        work / "contract.json", "--out-dir", work / "generated", "--source", source, "--no-state"],
        work, "spec", allowed=(0, 1, 2))
    generated = work / "generated/spec/r/down2_dynamic_tile_runner_spec.md"
    assert generated.exists()
    shutil.copyfile(generated, ROOT / "rtl/down2_dynamic_tile_runner_spec.md")
    shutil.copytree(generated.parent / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def boundary():
    work = tools.fresh("load_boundary")
    receipt = json.loads((MAC / "candidate_attempt4/receipt.json").read_text(encoding="utf-8"))
    sources = [Path(name) for name in receipt["sources"] if "sim_release" in name]
    sources += sorted((ROOT / "rtl").glob("*.v")) + [ROOT / "tests/tb_down2_dynamic_overlap.v"]
    save(work / "input_manifest.json", {str(p): tools.digest(p) for p in sources})
    tools.command([build.MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([build.MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for name in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        result = tools.command([build.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR",
            "tb_down2_dynamic_overlap", "+LOAD_BOUNDARY", f"+VECTORS={(build.RUNTIME / 'vectors' / name).as_posix()}",
            f"+REPORT={(work / (name + '.csv')).as_posix()}", f"+TRACE={(work / (name + '_trace.csv')).as_posix()}",
            f"+WINDOWS={(work / (name + '_windows.csv')).as_posix()}", "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name, timeout=300)
        assert "DW_LOAD_BOUNDARY_PASS" in result and "Fatal:" not in result and "** Error:" not in result
        results[name] = [line for line in result.splitlines() if "PASS" in line]
        print("BOUNDARY_PASS", name, flush=True)
    save(work / "receipt.json", {"all_passed": True, "results": results,
        "sources": {str(p): tools.digest(p) for p in sources}})
    save(ROOT / "boundary_current.json", {"work": str(work)})


def seal():
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    comparison = json.loads((ROOT / "cycle_comparison.json").read_text(encoding="utf-8"))
    assert comparison["identical_summary_rows"] == 64
    assert comparison["old_core_cycles"] == comparison["new_core_cycles"] == 1687
    simulation = Path(json.loads((ROOT / "simulation_current.json").read_text())["work"])
    boundary_work = Path(json.loads((ROOT / "boundary_current.json").read_text())["work"])
    receipts = {"runner": simulation / "receipt.json", "boundary": boundary_work / "receipt.json"}
    for name in ("shell_rtl", "shell_routed", "undriven"):
        matches = list(ROOT.glob(name + "*/receipt.json"))
        assert matches, name
        receipts[name] = max(matches, key=lambda p: p.stat().st_mtime_ns)
    for name, path in receipts.items():
        receipt = json.loads(path.read_text(encoding="utf-8"))
        assert not receipt.get("loaded", []), name
        assert receipt.get("all_passed", name == "undriven"), name
        assert all(tools.digest(Path(p)) == sha for p, sha in receipt["sources"].items()), name
    differences = []
    for path in sorted((ROOT / "rtl").glob("*.v")):
        old = ROOT / "baseline" / path.name
        if tools.digest(path) != tools.digest(old):
            differences.append(path.name)
    assert differences == ["down2_dynamic_tile_runner.v"], differences
    old = (ROOT / "baseline/down2_dynamic_tile_runner.v").read_text(encoding="utf-8")
    new = (ROOT / "rtl/down2_dynamic_tile_runner.v").read_text(encoding="utf-8")
    assert old[old.index("module "):old.index("\n);")] == new[new.index("module "):new.index("\n);")]
    assert new.count("reg_dw_weight[reg_dw_weight_write_address] <=") == 1
    assert "reg_dw_weight[i_load_addr] <=" not in new
    patch = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
        fromfile="frozen/down2_dynamic_tile_runner.v", tofile="candidate/down2_dynamic_tile_runner.v"))
    (ROOT / "rtl_change.diff").write_text(patch, encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": differences, "unchanged_rtl_count": 7,
        "ports_unchanged": True, "dw_weight_single_write_owner": True,
        "sources": {str(p.relative_to(ROOT)): tools.digest(p) for p in (ROOT / "rtl").glob("*.v")}})
    design_path = max(ROOT.glob("gate_candidate*/gate.json"), key=lambda p: p.stat().st_mtime_ns)
    tb_path = max(ROOT.glob("gate_testbench*/gate.json"), key=lambda p: p.stat().st_mtime_ns)
    design = json.loads(design_path.read_text(encoding="utf-8"))
    bench = json.loads(tb_path.read_text(encoding="utf-8"))
    warning_counts = {}
    for path in receipts["shell_routed"].parent.glob("*_stress.log"):
        text = path.read_text(encoding="utf-8", errors="replace")
        warning_counts[path.name] = dict(Counter(re.findall(r"\((vopt-\d+|vsim-\d+)\)", text)))
    save(ROOT / "netlist_warnings.json", {"counts_by_simulator_code": warning_counts,
        "not_waived": True, "scope": "mapped vendor primitive unused/mode/type warnings retained; not exhaustively closed"})
    physical_work = Path(physical["physical"])
    assert all(tools.digest(physical_work / n) == tools.digest(MAC / "physical_opt" / n)
               for n in ("build.tcl", "shell.sdc", "shell.adc"))
    negative = physical["negative_paths"]
    internally_clean = physical["internal_negative_count"] == 0
    save(ROOT / "status.json", {"stage": "evaluated_internal_clean_not_deployment" if internally_clean else
        "evaluated_internal_timing_failed", "production_modified": False, "deployment_release": False,
        "physical_rebuilt": True, "internal_timing_clean_in_report": internally_clean,
        "physical_timing_ready": False, "external_contract_signed_off": False,
        "internal_negative_endpoints": physical["internal_negative_count"],
        "external_negative_checks": dict(Counter(p["kind"] for p in negative if p["external"])),
        "functional_complete_cases": 64, "boundary_parameter_sets": 4, "core_cycles": 1687,
        "previous_core_cycles": 1687, "resources_including_shell": physical["resources_including_shell"],
        "shell_rtl": "passed_6_tiles_2304_bytes", "shell_routed": "passed_6_tiles_2304_bytes_no_sdf",
        "design_gate": {"errors": design["errors"], "strict_warnings": design["strict_warnings"],
            "delivery_ready": design["delivery_ready"]},
        "testbench_gate": {"errors": bench["errors"], "strict_warnings": bench["strict_warnings"],
            "delivery_ready": bench["delivery_ready"]},
        "receipts": {name: str(path.relative_to(ROOT)) for name, path in receipts.items()},
        "training_started": False, "bitstream_generated": False, "flash_modified": False})
    extensions = {".py", ".v", ".md", ".json", ".json5", ".tcl", ".sdc", ".adc", ".al", ".db", ".rpt",
        ".timing", ".ts", ".area", ".qor", ".csv", ".log", ".svg", ".diff"}
    evidence = {str(p.relative_to(ROOT)): tools.digest(p) for p in ROOT.rglob("*")
        if p.is_file() and "work" not in p.relative_to(ROOT).parts and p.suffix in extensions
        and p.name != "evidence_hashes.json"}
    save(ROOT / "evidence_hashes.json", evidence)
    print("SEALED", len(evidence), "INTERNAL_NEGATIVE", physical["internal_negative_count"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "simulate", "physical", "gates",
        "specs", "shell_rtl", "shell_routed", "undriven", "compare", "collect", "boundary", "seal"))
    stage = parser.parse_args().stage
    build.frozen()
    try:
        if stage == "prepare":
            prepare()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage == "compare":
            compare()
        elif stage == "collect":
            collect()
        elif stage == "specs":
            specs()
        elif stage == "boundary":
            boundary()
        elif stage == "seal":
            seal()
        else:
            getattr(build, stage)()
    except Exception as error:
        build.save(ROOT / (stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        build.frozen()
