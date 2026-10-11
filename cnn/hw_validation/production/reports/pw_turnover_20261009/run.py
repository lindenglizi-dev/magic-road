"""PW 首组预取的有界验证；复用冻结工具，不在旧目录运行构建。"""
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parent / "runtime_layer_integration_20261009"
spec = importlib.util.spec_from_file_location("frozen_tools", PREV / "run_candidate.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
CORE = [tools.BASE / "rtl" / name for name in (
    "road_mac_probe.v", "road_dynamic_postprocess.v", "road_dynamic_requant.v",
    "road_round_shift.v", "silu_shared_unit.v")]
ADAPTER = PREV / "rtl/road_down2_dynamic_adapter.v"
SHELL = PREV / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"
RUNNER = ROOT / "rtl/down2_dynamic_tile_runner.v"
TB = ROOT / "tests/tb_down2_dynamic_overlap.v"


def frozen():
    path = ROOT / "frozen.json"
    if not path.exists():
        records = json.loads((tools.PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
        records.update(json.loads((tools.PREVIOUS / "additional_frozen.json").read_text(encoding="utf-8")))
        for parent in (tools.PREVIOUS, PREV):
            records.update({str(parent / name): value for name, value in json.loads(
                (parent / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        for source in [*CORE, ADAPTER, SHELL, PREV / "measured_evidence.json", PREV / "status.json"]:
            records[str(source)] = tools.digest(source)
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if tools.digest(Path(name)) != sha]
    (ROOT / "frozen_check.json").write_text(json.dumps(
        {"checked": len(records), "changed": changed}, indent=2), encoding="utf-8")
    assert not changed, changed


def schedule_reference():
    tasks = [(position, group) for position in range(16) for group in range(8)]
    for index, (position, group) in enumerate(tasks[:-1]):
        next_position = position + (group == 7)
        next_group = 0 if group == 7 else group + 1
        assert (next_position, next_group) == tasks[index + 1]
        assert 0 <= next_position * 16 + 7 < 256
        assert 0 <= (next_group * 3 + 2) * 16 + 7 < 384
        assert next_group * 3 + 2 < 24
    result = {"tasks": len(tasks), "prefetch_transitions": len(tasks) - 1,
              "final_task_prefetch": False, "numerical_contract": "unchanged",
              "start_rule": "next first only after prior result acceptance"}
    (ROOT / "schedule_reference.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result)


def review():
    work = tools.fresh("review")
    tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
        "check", "--settings", tools.SKILL / "config/defaults.json", "--state-path", work / "dependencies.json"],
        work, "dependencies", allowed=(0, 1, 2))
    entry = f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
        PREV / "rtl/down2_dynamic_tile_runner.v", "--report-json", work / "baseline.json"],
        work, "baseline", allowed=(0, 1, 2))
    print("REVIEW", work)


def simulate(baseline=False):
    work = tools.fresh("baseline" if baseline else "candidate")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    sources += CORE + [ADAPTER, PREV / "rtl/down2_dynamic_tile_runner.v" if baseline else RUNNER, TB]
    tools.command([msim / "vlib.exe", "work"], work, "vlib")
    tools.command([msim / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for case in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        log = tools.command([msim / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_down2_dynamic_overlap",
            f"+VECTORS={(PREV / 'vectors' / case).as_posix()}", f"+REPORT={(work / (case + '.csv')).as_posix()}",
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, case)
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in log and "Fatal:" not in log and "** Error:" not in log
        results[case] = [line for line in log.splitlines() if "LAYER_OVERLAP_PASS" in line or "TB_PASS" in line]
        print(case, *results[case], sep="\n", flush=True)
    (work / "receipt.json").write_text(json.dumps({"results": results,
        "sources": {str(path): tools.digest(path) for path in sources}}, indent=2), encoding="utf-8")


def physical():
    work = tools.fresh("physical")
    sources = [SHELL, RUNNER, ADAPTER, *CORE]
    tools.project(work, "layer_shell", sources)
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        (work / name).write_bytes((PREV / "physical_attempt2" / name).read_bytes())
    (work / "input_manifest.json").write_text(json.dumps(
        {str(path): tools.digest(path) for path in sources}, indent=2), encoding="utf-8")
    print("PHYSICAL_WORK", work, flush=True)
    log = tools.command([tools.TD, "build.tcl"], work, "td", timeout=3600)
    print(log[-1800:])


def gates():
    work = tools.fresh("gates")
    entry = f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    results = {}
    for label, runner in (("baseline", PREV / "rtl/down2_dynamic_tile_runner.v"), ("candidate", RUNNER)):
        closure = work / label
        closure.mkdir()
        for source in [SHELL, runner, ADAPTER, *CORE,
                       ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v"]:
            shutil.copyfile(source, closure / source.name)
        tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, closure,
            "--json", work / f"{label}.json", "--markdown", work / f"{label}.md"],
            work, label, allowed=(0, 1, 2))
        results[label] = json.loads((work / f"{label}.json").read_text(encoding="utf-8"))
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / "tests", "--include-testbench",
        "--json", work / "testbench.json", "--markdown", work / "testbench.md"],
        work, "testbench", allowed=(0, 1, 2))
    a, b = [results[label]["delivery_issues_by_rule"] for label in ("baseline", "candidate")]
    delta = {rule: b.get(rule, 0)-a.get(rule, 0) for rule in a.keys() | b.keys() if a.get(rule, 0)!=b.get(rule, 0)}
    (work / "comparison.json").write_text(json.dumps({"errors": [results[label]["errors"] for label in (
        "baseline", "candidate")], "delta_by_rule": delta}, indent=2), encoding="utf-8")
    print("GATES", work, "ERRORS", [results[label]["errors"] for label in ("baseline", "candidate")])


def specs():
    work = tools.fresh("s")
    # Reuse the canonical baseline port contract; no new Verilog parser.
    contract = json.loads((PREV / "s/down2_dynamic_tile_runner.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["description"] = "PW next-first preparation in existing registers; frozen arithmetic and interfaces."
    module["behavior"] += ["During PW WAIT address the next task first group; current result metadata remain unchanged.",
        "Capture next operands only on successful prior result acceptance; next first still obeys MAC ready and reservation.",
        "Skip127 PW STORAGE cycles; first task still uses STORAGE. Final task and fault never capture a successor."]
    module["verification_cases"] = ["Same40 layer scenarios per revision, all640 values at each arithmetic stage and384 exports.",
        "Random phase relative to core start; MAC/commit stability, four PW reset positions, full queue and final-lane overflow."]
    module["timing_diagrams"].append({"id": "pw_next_first", "title": "PW task turnover without STORAGE",
        "scenario": "pw_next_first", "description": "No backpressure: first atE0, last atE1, prior result acceptedE8, next firstE9. II within task remains1.",
        "wavejson": {"signal": [{"name": "clk", "wave": "p.........."},
            {"name": "MAC first accepted", "wave": "10.......10"},
            {"name": "MAC last accepted", "wave": "010.......1"},
            {"name": "WAIT and next operand address", "wave": "0.1......0."},
            {"name": "prior result accepted and next operand captured", "wave": "0.......10."}],
            "head": {"tick": 0}}})
    path = work / "contract.json"
    path.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    source = work / RUNNER.name
    shutil.copyfile(RUNNER, source)
    entry = f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
        "--out-dir", work / "g", "--source", source, "--no-state"], work, "spec", allowed=(0, 1, 2))
    generated = work / "g/spec/r/down2_dynamic_tile_runner_spec.md"
    assert generated.exists(), generated
    shutil.copyfile(generated, RUNNER.with_name("down2_dynamic_tile_runner_spec.md"))
    shutil.copytree(generated.parent / "waveforms", RUNNER.parent / "waveforms", dirs_exist_ok=True)
    tb_contract = dict(module, name="tb_down2_dynamic_overlap", rtl_path=TB.name,
                       interfaces={"protocol": "discrete", "ports": []})
    path = work / "tb.json"
    path.write_text(json.dumps({"modules": [tb_contract]}, indent=2), encoding="utf-8")
    staged_tb = work / TB.name
    shutil.copyfile(TB, staged_tb)
    log = tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
        "--out-dir", work / "g", "--source", staged_tb, "--no-state"], work, "tb_spec", allowed=(0, 1, 2))
    assert "ports must be non-empty" in log
    print("SPEC_PASS_RUNNER TB_CANONICAL_REJECTED_PORTLESS", work)


def shell_sim(gate=False):
    work = tools.fresh("shell_gate" if gate else "shell_rtl")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    sources += [ROOT / "physical/gate_netlist.v"] if gate else [*CORE, RUNNER, ADAPTER, SHELL]
    sources += [ROOT / "tests/tb_runtime_layer_shell.v"]
    tools.command([msim / "vlib.exe", "work"], work, "vlib")
    tools.command([msim / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for case in ("fixed_stress", "dynamic_stress"):
        log = tools.command([msim / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_runtime_layer_shell",
            f"+VECTORS={(PREV / 'vectors' / case).as_posix()}", "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, case)
        assert "TB_PASS_RUNTIME_LAYER_SHELL" in log and "Fatal:" not in log and "** Error:" not in log
        results[case] = next(line for line in log.splitlines() if "TB_PASS_RUNTIME" in line)
        print(case, results[case], flush=True)
    (work / "receipt.json").write_text(json.dumps({"results": results, "sdf": False,
        "sources": {str(path): tools.digest(path) for path in sources}}, indent=2), encoding="utf-8")


def zeroing():
    work = tools.fresh("z")
    name = tools.project(work, "layer_shell", [SHELL, RUNNER, ADAPTER, *CORE])
    path = work / name
    path.write_text(path.read_text(encoding="utf-8").replace("<LABEL>road_dynamic_overlap_low_io_top</LABEL>",
        "<LABEL>down2_dynamic_tile_runner</LABEL>").replace("<MODULE>road_dynamic_overlap_low_io_top</MODULE>",
        "<MODULE>down2_dynamic_tile_runner</MODULE>"), encoding="utf-8")
    script = f"""import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project {name} -single_run
elaborate -top down2_dynamic_tile_runner
set dead [get_nets -filter {{DRIVER_COUNT == 0}} *]
foreach net $dead {{
    puts "DEAD_RECORD [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}}
puts "MODEL_QUERY_DONE"
close_project
"""
    (work / "inspect.tcl").write_text(script, encoding="utf-8")
    log = tools.command([tools.TD, "inspect.tcl"], work, "td", timeout=180)
    assert "MODEL_QUERY_DONE" in log and "ERROR:" not in log
    records = [line for line in log.splitlines() if line.startswith("DEAD_RECORD")]
    loaded = [line for line in records if "PINS 0 DRIVER 0" not in line]
    (work / "receipt.json").write_text(json.dumps({"records": records, "loaded": loaded}, indent=2), encoding="utf-8")
    assert not loaded, loaded
    print("NEW_RUNNER_UNDRIVEN", len(records), "WITH_LOAD", len(loaded))


if __name__ == "__main__":
    frozen()
    try:
        {"review": review, "reference": schedule_reference, "baseline": lambda: simulate(True),
         "candidate": simulate, "physical": physical, "gates": gates, "specs": specs,
         "shell_rtl": shell_sim, "shell_gate": lambda: shell_sim(True), "zeroing": zeroing}[sys.argv[1]]()
    finally:
        frozen()
