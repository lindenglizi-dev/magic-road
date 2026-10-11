"""DW 四槽候选的独立构建；只在本目录写入证据，不改冻结输入。"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "dw_wait_profile_20261009"
MAC = ROOT.parent / "mac_task_stream_20261009"
RUNTIME = ROOT.parent / "runtime_layer_integration_20261009"
CHECKER = ROOT.parent / "checker_fact_closure_20261009"
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
    path = ROOT / "frozen.json"
    if not path.exists():
        records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
        records.update({str(BASE / name): sha for name, sha in json.loads(
            (BASE / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        records.update({str(p): tools.digest(p) for p in [BASE / "evidence_hashes.json",
            BASE / "frozen.json", tools.TD, *[(MAC / "physical_opt" / n)
            for n in ("build.tcl", "shell.sdc", "shell.adc")]]})
        save(path, records)
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if tools.digest(Path(name)) != sha]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def prepare():
    shutil.copytree(BASE / "inputs/rtl", ROOT / "baseline")
    shutil.copytree(BASE / "inputs/rtl", ROOT / "rtl")
    shutil.copytree(BASE / "inputs/interfaces", ROOT / "interfaces")
    (ROOT / "tests").mkdir()
    shutil.copyfile(BASE / "tests/tb_down2_dynamic_overlap.v", ROOT / "tests/tb_down2_dynamic_overlap.v")
    work = tools.fresh("preflight")
    result = tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings",
        tools.SKILL / "config/defaults.json"], work, "dependencies", allowed=(0, 1))
    dependency = json.loads(result[result.index("{"):])
    save(work / "dependencies.json", dependency)
    assert dependency["required_ok"]
    save(ROOT / "status.json", {"stage": "baseline_frozen", "production_modified": False,
        "deployment_release": False, "physical_rebuilt": False})


def gate(label):
    work = tools.fresh("gate_" + label)
    entry = (f"import sys;sys.path[:0]=[{str(CHECKER / 'checker_overlay')!r},{str(tools.SKILL)!r}];"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    args = [sys.executable, "-B", "-X", "utf8", "-c", entry,
        ROOT / ("baseline" if label == "baseline" else "tests" if label == "testbench" else "rtl"),
        "--external-interface-source", ROOT / "interfaces/ph1p_eram_interface_complete.v",
        "--json", work / "gate.json", "--markdown", work / "gate.md"]
    # Existing interface snapshot uses the exact vendor interface filename.
    args[args.index("--external-interface-source") + 1] = next((ROOT / "interfaces").glob("*.v"))
    if label == "testbench":
        args.append("--include-testbench")
    tools.command(args, work, "gate", allowed=(0, 1))
    result = json.loads((work / "gate.json").read_text(encoding="utf-8"))
    print("GATE", label, result["errors"], result["strict_warnings"], result["delivery_ready"], flush=True)


def review():
    work = tools.fresh("baseline_review")
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
        ROOT / "baseline/down2_dynamic_tile_runner.v", "--report-json", work / "review.json"],
        work, "review", allowed=(0, 1, 2))
    gate("baseline")


def simulate():
    work = tools.fresh("simulation")
    source_receipt = json.loads((MAC / "candidate_attempt4/receipt.json").read_text(encoding="utf-8"))
    sources = [Path(name) for name in source_receipt["sources"] if "sim_release" in name]
    sources += sorted((ROOT / "rtl").glob("*.v")) + [ROOT / "tests/tb_down2_dynamic_overlap.v"]
    save(work / "input_manifest.json", {str(p): tools.digest(p) for p in sources})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for name in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        result = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR",
            "tb_down2_dynamic_overlap", f"+VECTORS={(RUNTIME / 'vectors' / name).as_posix()}",
            f"+REPORT={(work / (name + '.csv')).as_posix()}",
            f"+TRACE={(work / (name + '_trace.csv')).as_posix()}",
            f"+WINDOWS={(work / (name + '_windows.csv')).as_posix()}",
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
            work, name, timeout=300)
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in result and "Fatal:" not in result and "** Error:" not in result
        with (work / (name + ".csv")).open() as stream:
            summaries = list(csv.DictReader(stream))
        assert [int(row["case"]) for row in summaries] == list(range(16)), "Missing complete recovery case"
        results[name] = {"summary": summaries, "pass_lines": [line for line in result.splitlines() if "PASS" in line]}
        print("SIM_PASS", name, "base_cycles", summaries[0]["endpoint"], flush=True)
    save(work / "receipt.json", {"all_passed": True, "results": results,
        "sources": {str(p): tools.digest(p) for p in sources}})
    save(ROOT / "simulation_current.json", {"work": str(work)})


def physical():
    work = tools.fresh("physical")
    sources = sorted((ROOT / "rtl").glob("*.v"))
    tools.project(work, "layer_shell", sources)
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        shutil.copyfile(MAC / "physical_opt" / name, work / name)
    save(work / "input_manifest.json", {str(p): tools.digest(p) for p in sources})
    print("PHYSICAL_WORK", work, flush=True)
    result = tools.command([tools.TD, "build.tcl"], work, "td", timeout=3600)
    assert "ERROR:" not in result and (work / "pr.db").exists()
    print("PHYSICAL_DONE", result[-1200:], flush=True)
    save(ROOT / "physical_current.json", {"work": str(work)})


def measure():
    work = tools.fresh("measurement")
    sim = json.loads((ROOT / "simulation_current.json").read_text(encoding="utf-8"))["work"]
    tools.command([sys.executable, "-B", "-X", "utf8", ROOT / "measure.py", sim], work, "measure")
    tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL / "scripts/python/toolchain/wavedrom_runtime.py",
        "--settings", tools.SKILL / "config/defaults.json", "render", "--input", ROOT / "dw_task_overlap.wave.json",
        "--output", ROOT / "dw_task_overlap.svg"], work, "wavedrom")


def specs():
    work = tools.fresh("specs")
    contract = json.loads((MAC / "s/contract.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["description"] = "DW four-credit issue/retire overlap with frozen arithmetic and external ports"
    module["reset"]["values"] = "Asynchronous cancellation. Runner load-ready can remain high in reset; upstream must not transfer. The unchanged38bit shell masks external ready/valid until its two-stage release completes. Reload all1024 SiLU entries and all operand/parameter banks before start."
    module["behavior"] = ["Same signed33/INT32 fault, bias once, first/last, II and reset contracts as frozen dependencies.",
        "Shared four-entry9bit descriptor ring reserves on each first acceptance and pops on MAC result acceptance.",
        "DW issue preserves preparation before every group; result retirement uses one existing96bit active triplet and new9bit identity.",
        "Active identity drives channel coefficients, one-hot scalar lane and position, never advanced issuer counters.",
        "DW active last scalar may accept at the same edge as next MAC result; new result identity/data wins replacement.",
        "Fault cancels whole tile publication, blocks younger work; old ownership remains invalid until common reset.",
        "PW starts only after256 DW commits and all descriptor/active/MAC ownership is empty. Runtime TEST parameters are not QAT deployment."]
    module["timing_diagrams"] = [{"id": "dw_task_overlap", "title": "DW real task overlap", "scenario": "dw_task_overlap",
        "description": "Actual first36 busy samples from same frozen fixed_original case0; MAC last is meaningful only with accept.",
        "wavejson": json.loads((ROOT / "dw_task_overlap.wave.json").read_text(encoding="utf-8"))}]
    save(work / "contract.json", contract)
    source = work / "down2_dynamic_tile_runner.v"
    shutil.copyfile(ROOT / "rtl/down2_dynamic_tile_runner.v", source)
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec",
        work / "contract.json", "--out-dir", work / "generated", "--source", source,
        "--no-state"], work, "spec", allowed=(0, 1, 2))
    generated = work / "generated/spec/r/down2_dynamic_tile_runner_spec.md"
    assert generated.exists()
    shutil.copyfile(generated, ROOT / "rtl/down2_dynamic_tile_runner_spec.md")
    shutil.copytree(generated.parent / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def shell(routed=False):
    work = tools.fresh("shell_routed" if routed else "shell_rtl")
    receipt = json.loads((MAC / "candidate_attempt4/receipt.json").read_text(encoding="utf-8"))
    sources = [Path(name) for name in receipt["sources"] if "sim_release" in name]
    if routed:
        physical_work = Path(json.loads((ROOT / "physical_current.json").read_text(encoding="utf-8"))["work"])
        manifest = json.loads((physical_work / "input_manifest.json").read_text(encoding="utf-8"))
        assert all(tools.digest(Path(name)) == sha for name, sha in manifest.items())
        sources.append(physical_work / "routed_netlist.v")
    else:
        sources += sorted((ROOT / "rtl").glob("*.v"))
    sources.append(ROOT / "tests/tb_runtime_layer_shell.v")
    sim_work = Path(json.loads((ROOT / "simulation_current.json").read_text(encoding="utf-8"))["work"])
    sim_receipt = json.loads((sim_work / "receipt.json").read_text(encoding="utf-8"))
    cycles = int(sim_receipt["results"]["fixed_original"]["summary"][0]["endpoint"])
    save(work / "input_manifest.json", {str(p): tools.digest(p) for p in sources})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for name in ("fixed_stress", "dynamic_stress"):
        result = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_runtime_layer_shell",
            f"+VECTORS={(RUNTIME / 'vectors' / name).as_posix()}", f"+CORE_CYCLES={cycles}", "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name, timeout=600 if routed else 300)
        assert "TB_PASS_RUNTIME_LAYER_SHELL" in result and "Fatal:" not in result and "** Error:" not in result
        results[name] = [line for line in result.splitlines() if "PASS" in line]
        print("SHELL_PASS", "routed" if routed else "rtl", name, cycles, flush=True)
    save(work / "receipt.json", {"all_passed": True, "routed": routed, "sdf_annotated": False,
        "core_cycles": cycles, "results": results, "sources": {str(p): tools.digest(p) for p in sources}})


def undriven():
    work = tools.fresh("undriven")
    sources = sorted((ROOT / "rtl").glob("*.v"))
    tools.project(work, "layer_shell", sources)
    shutil.copyfile(ROOT / "inspect_undriven.tcl", work / "inspect.tcl")
    log = tools.command([tools.TD, "inspect.tcl"], work, "td", timeout=180)
    assert "MODEL_QUERY_DONE" in log and "ERROR:" not in log
    records = [line for line in log.splitlines() if line.startswith("DEAD_RECORD")]
    loaded = [line for line in records if "PINS 0 DRIVER 0" not in line]
    save(work / "receipt.json", {"records": records, "loaded": loaded,
        "scope": "elaborated top net query; not a complete mapped primitive pin proof",
        "sources": {str(p): tools.digest(p) for p in sources}})
    assert not loaded, loaded
    print("UNDRIVEN_QUERY", len(records), "WITH_LOAD", len(loaded), flush=True)


def seal():
    sim_work = Path(json.loads((ROOT / "simulation_current.json").read_text(encoding="utf-8"))["work"])
    receipts = {"runner": sim_work / "receipt.json", "shell_rtl": ROOT / "shell_rtl_attempt2/receipt.json",
        "shell_routed": ROOT / "shell_routed_attempt2/receipt.json"}
    for path in receipts.values():
        receipt = json.loads(path.read_text(encoding="utf-8"))
        assert receipt["all_passed"]
        assert all(tools.digest(Path(name)) == sha for name, sha in receipt["sources"].items())
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    design = json.loads((ROOT / "gate_candidate_attempt3/gate.json").read_text(encoding="utf-8"))
    bench = json.loads((ROOT / "gate_testbench_attempt3/gate.json").read_text(encoding="utf-8"))
    analysis = json.loads((ROOT / "analysis.json").read_text(encoding="utf-8"))
    assert sum(len(cases) for cases in analysis["sets"].values()) == 64
    save(ROOT / "status.json", {"stage": "dw_overlap_evaluated_physical_not_passed",
        "production_modified": False, "deployment_release": False, "physical_rebuilt": True,
        "functional_complete_cases": 64, "core_cycles": 1687, "previous_core_cycles": 2607,
        "internal_negative_endpoints": physical["internal_negative_count"],
        "physical_timing_ready": False, "external_contract_signed_off": False,
        "resources_including_shell": physical["resources_including_shell"],
        "shell_rtl": "passed_6_tiles_2304_bytes", "shell_routed": "passed_6_tiles_2304_bytes_no_sdf",
        "design_gate": {"errors": design["errors"], "strict_warnings": design["strict_warnings"],
            "delivery_ready": design["delivery_ready"]},
        "testbench_gate": {"errors": bench["errors"], "strict_warnings": bench["strict_warnings"],
            "delivery_ready": bench["delivery_ready"]},
        "receipts": {name: str(path.relative_to(ROOT)) for name, path in receipts.items()},
        "training_started": False, "bitstream_generated": False, "flash_modified": False,
        "next_action": "Isolated DW weight load write-enable timing repair; keep arithmetic, ports, II and contracts."})
    extensions = {".py", ".v", ".md", ".json", ".tcl", ".sdc", ".adc", ".al", ".db", ".rpt",
        ".timing", ".ts", ".area", ".qor", ".csv", ".log", ".svg"}
    evidence = {str(path.relative_to(ROOT)): tools.digest(path) for path in ROOT.rglob("*")
        if path.is_file() and "work" not in path.relative_to(ROOT).parts and path.suffix in extensions
        and path.name != "evidence_hashes.json"}
    save(ROOT / "evidence_hashes.json", evidence)
    print("SEALED_EVALUATION", len(evidence), "PHYSICAL_NOT_PASSED", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "simulate", "physical", "gates", "measure", "specs", "shell_rtl", "shell_routed", "undriven", "seal"))
    args = parser.parse_args()
    frozen()
    try:
        if args.stage == "gates":
            gate("candidate")
            gate("testbench")
        elif args.stage in ("shell_rtl", "shell_routed"):
            shell(args.stage == "shell_routed")
        elif args.stage == "undriven":
            undriven()
        elif args.stage == "seal":
            seal()
        else:
            {"prepare": prepare, "review": review, "simulate": simulate, "physical": physical,
             "measure": measure, "specs": specs}[args.stage]()
    except Exception as error:
        save(ROOT / (args.stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
