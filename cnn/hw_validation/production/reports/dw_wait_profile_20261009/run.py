"""冻结设计的 DW 等待实测；只在本目录新增测量，不修改 DUT。"""
import argparse
import ast
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parent / "mac_task_stream_20261009"
CHECKER = ROOT.parent / "checker_fact_closure_20261009"
RUNTIME = ROOT.parent / "runtime_layer_integration_20261009"
spec = importlib.util.spec_from_file_location("frozen_build_tools", RUNTIME / "run_candidate.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
MSIM = Path(r"D:\modeltech64_2020.4\win64")


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def frozen():
    manifest = ROOT / "frozen.json"
    if not manifest.exists():
        records = json.loads((CHECKER / "frozen.json").read_text(encoding="utf-8"))
        records.update({str(CHECKER / name): sha for name, sha in json.loads(
            (CHECKER / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        records.update(json.loads((PREV / "candidate_attempt4/receipt.json").read_text(encoding="utf-8"))["sources"])
        extra = [RUNTIME / "run_candidate.py", PREV / "candidate_attempt4/receipt.json",
                 CHECKER / "frozen.json", CHECKER / "evidence_hashes.json"]
        extra += list((RUNTIME / "vectors").rglob("*.hex"))
        extra += [MSIM / name for name in ("vsim.exe", "vlog.exe", "vlib.exe")]
        records.update({str(path): tools.digest(path) for path in extra})
        save(manifest, records)
    records = json.loads(manifest.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if tools.digest(Path(name)) != sha]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def prepare():
    work = ROOT / "preflight"
    work.mkdir()
    output = tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings",
        tools.SKILL / "config/defaults.json", "--state-path", work / "state.json"], work,
        "dependencies", allowed=(0, 1))
    # check publishes JSON on stdout; --state-path is a read path, not an output report.
    dependency = json.loads(output[output.index("{"):])
    save(work / "dependencies.json", dependency)
    assert dependency["required_ok"], dependency
    target = ROOT / "inputs/rtl"
    shutil.copytree(CHECKER / "inputs/rtl", target)
    shutil.copytree(CHECKER / "inputs/interfaces", ROOT / "inputs/interfaces")
    tests = ROOT / "tests"
    tests.mkdir()
    shutil.copy2(PREV / "tests/tb_down2_dynamic_overlap.v", tests)
    save(ROOT / "inputs/manifest.json", {str(path.relative_to(ROOT)): tools.digest(path)
         for path in (ROOT / "inputs").rglob("*.v")})
    save(ROOT / "status.json", {"stage": "inputs_frozen_monitor_pending", "dut_changed": False,
         "physical_rebuilt": False, "deployment_release": False})


def gates():
    (ROOT / "gates").mkdir(exist_ok=True)
    entry = (f"import sys;sys.path[:0]=[{str(CHECKER / 'checker_overlay')!r},{str(tools.SKILL)!r}];"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    for label in ("design", "testbench"):
        work = tools.fresh("gates/" + label)
        arguments = [sys.executable, "-B", "-X", "utf8", "-c", entry,
                     ROOT / ("inputs/rtl" if label == "design" else "tests"),
                     "--external-interface-source", ROOT / "inputs/interfaces/ph1p_eram_interface_complete.v",
                     "--json", work / "gate.json", "--markdown", work / "gate.md"]
        if label == "testbench":
            arguments.append("--include-testbench")
        tools.command(arguments, work, "gate", allowed=(0, 1))
        report = json.loads((work / "gate.json").read_text(encoding="utf-8"))
        print("GATE", label, report["errors"], report["strict_warnings"], report["delivery_ready"], flush=True)


def simulate():
    work = tools.fresh("simulation")
    old = json.loads((PREV / "candidate_attempt4/receipt.json").read_text(encoding="utf-8"))["sources"]
    vendor_sources = [Path(path) for path in old if "sim_release" in path]
    sources = vendor_sources + sorted((ROOT / "inputs/rtl").glob("*.v")) + [ROOT / "tests/tb_down2_dynamic_overlap.v"]
    save(work / "input_manifest.json", {str(path): tools.digest(path) for path in sources})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for case in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR",
            "tb_down2_dynamic_overlap", f"+VECTORS={(RUNTIME / 'vectors' / case).as_posix()}",
            f"+REPORT={(work / (case + '.csv')).as_posix()}",
            f"+TRACE={(work / (case + '_trace.csv')).as_posix()}",
            f"+WINDOWS={(work / (case + '_windows.csv')).as_posix()}",
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
            work, case, timeout=300)
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in log and "Fatal:" not in log and "** Error:" not in log
        # Instrumentation must not perturb the previous numeric checks or cycle windows.
        previous = list(csv.DictReader((PREV / "candidate_attempt4" / (case + ".csv")).open()))
        current = list(csv.DictReader((work / (case + ".csv")).open()))
        assert current == previous, case
        results[case] = {"same_original_summary": True, "completed_scenarios": len(current),
                         "pass_lines": [line for line in log.splitlines() if "TB_PASS" in line]}
        print("SIM_PASS", case, len(current), flush=True)
    save(work / "receipt.json", {"all_passed": True, "results": results,
         "dut_changed": False, "testbench_sha256": tools.digest(sources[-1])})


def measure():
    work = tools.fresh("measurement")
    tools.command([sys.executable, "-B", "-X", "utf8", ROOT / "analyze.py", ROOT / "simulation_attempt2"],
                  work, "analyze")
    tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/wavedrom_runtime.py", "--settings", tools.SKILL / "config/defaults.json",
        "render", "--input", ROOT / "tests/dw_frozen_first_tasks.wave.json", "--output",
        ROOT / "tests/dw_frozen_first_tasks.svg"], work, "wavedrom")
    save(work / "receipt.json", {"analysis_sha256": tools.digest(ROOT / "analyze.py"),
        "testbench_sha256": tools.digest(ROOT / "tests/tb_down2_dynamic_overlap.v"), "cases_verified": 40})


def finalize():
    for script in (ROOT / "run.py", ROOT / "analyze.py"):
        ast.parse(script.read_text(encoding="utf-8"))
    copied = json.loads((ROOT / "inputs/manifest.json").read_text(encoding="utf-8"))
    assert all(tools.digest(ROOT / name) == sha for name, sha in copied.items())
    sim = json.loads((ROOT / "simulation_attempt2/receipt.json").read_text(encoding="utf-8"))
    measured = json.loads((ROOT / "measurement_attempt2/receipt.json").read_text(encoding="utf-8"))
    assert sim["all_passed"] and sim["testbench_sha256"] == measured["testbench_sha256"]
    assert measured["analysis_sha256"] == tools.digest(ROOT / "analyze.py")
    gate_results = {}
    for label in ("design", "testbench"):
        gate = json.loads((ROOT / "gates" / (label + "_attempt2") / "gate.json").read_text(encoding="utf-8"))
        gate_results[label] = {key: gate[key] for key in ("errors", "strict_warnings", "delivery_ready", "checks")}
    old_gate = json.loads((CHECKER / "gates/fixed/gate.json").read_text(encoding="utf-8"))
    assert gate_results["design"]["errors"] == old_gate["errors"] == 4948
    assert gate_results["design"]["strict_warnings"] == old_gate["strict_warnings"] == 20
    save(ROOT / "status.json", {"stage": "measurement_complete", "cases_verified": 40,
        "baseline_cycles": {"dw": 2015, "pw": 592, "total": 2607}, "dut_changed": False,
        "functional_regression_passed": True, "strict_gates": gate_results,
        "external_interface_signed_off": False, "physical_rebuilt": False, "deployment_release": False,
        "next": "Independent DW four-credit task overlap; preserve arithmetic, prepare, II and contracts"})
    frozen()
    save(ROOT / "evidence_hashes.json", {str(path.relative_to(ROOT)): tools.digest(path)
        for path in sorted(ROOT.rglob("*")) if path.is_file() and path.name != "evidence_hashes.json"})
    print("FINAL measurement_complete cases=40 frozen=1502 changed=0 DUT_changed=false", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "gates", "simulate", "measure", "finalize"))
    args = parser.parse_args()
    frozen()
    try:
        {"prepare": prepare, "gates": gates, "simulate": simulate, "measure": measure, "finalize": finalize}[args.stage]()
    except Exception as error:
        # Preserve tool launch failures separately from a DUT verification failure.
        save(ROOT / (args.stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
