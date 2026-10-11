"""四槽跨任务 MAC 候选的有界验证；所有输出限定到本目录。"""
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parent / "runtime_layer_integration_20261009"
FROZEN_PW = ROOT.parent / "pw_turnover_20261009"
spec = importlib.util.spec_from_file_location("frozen_tools", PREV / "run_candidate.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
CORE = [tools.BASE / "rtl" / name for name in (
    "road_mac_probe.v", "road_dynamic_postprocess.v", "road_dynamic_requant.v",
    "road_round_shift.v", "silu_shared_unit.v")]
OLD_CORE = CORE.copy()
CORE[0] = ROOT / "rtl/road_mac_probe.v"
ADAPTER = PREV / "rtl/road_down2_dynamic_adapter.v"
SHELL = PREV / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"
RUNNER = ROOT / "rtl/down2_dynamic_tile_runner.v"
TB = ROOT / "tests/tb_down2_dynamic_overlap.v"


def frozen():
    path = ROOT / "frozen.json"
    if not path.exists():
        records = json.loads((tools.PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
        records.update(json.loads((tools.PREVIOUS / "additional_frozen.json").read_text(encoding="utf-8")))
        for parent in (tools.PREVIOUS, PREV, FROZEN_PW):
            records.update({str(parent / name): value for name, value in json.loads(
                (parent / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
        for source in [*OLD_CORE, ADAPTER, SHELL, PREV / "measured_evidence.json", PREV / "status.json",
                       FROZEN_PW / "rtl/down2_dynamic_tile_runner.v", FROZEN_PW / "run.py"]:
            records[str(source)] = tools.digest(source)
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, sha in records.items() if tools.digest(Path(name)) != sha]
    (ROOT / "frozen_check.json").write_text(json.dumps(
        {"checked": len(records), "changed": changed}, indent=2), encoding="utf-8")
    assert not changed, changed


def schedule_reference():
    import random
    rng = random.Random(42)
    # A first reserves capacity through pipeline AND FIFO until actual result pop.
    maximum = 0
    for groups in (1, 2, 3, 24):
        reserved = active = sent = received = 0
        pending, queue = [], []
        for cycle in range(20000):
            pop = bool(queue) and cycle > 100 and rng.randrange(4) != 0
            ready = bool(active) or reserved < 4 or pop
            accept = sent < 128 and ready and rng.randrange(5) != 0
            first = accept and active == 0
            last = accept and active == groups - 1
            if pop:
                assert queue.pop(0) == received
                received += 1
            due = [item for item in pending if item[0] == cycle]
            for _, task in due:
                assert len(queue) < 4
                queue.append(task)
            pending = [item for item in pending if item[0] != cycle]
            if last:
                pending.append((cycle + 6, sent))
                sent += 1
            if accept:
                active = 0 if last else active + 1
            reserved += int(first) - int(pop)
            maximum = max(maximum, reserved)
            assert 0 <= reserved <= 4
            assert reserved == len(queue) + len(pending) + int(bool(active))
            if received == 128:
                break
        assert received == sent == 128 and reserved == active == 0
    result = {"groups": [1, 2, 3, 24], "tasks_per_group_case": 128,
              "max_reserved": maximum, "credit_lifetime": "first_accept through result_pop",
              "full_active_reduction": "continuation never blocked by reserved count",
              "fault": "per-task atomic zero; runner invalid until common reset"}
    (ROOT / "schedule_reference.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result)


def review():
    work = tools.fresh("review")
    tools.command([sys.executable, "-B", "-X", "utf8", tools.SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
        "check", "--settings", tools.SKILL / "config/defaults.json", "--state-path", work / "dependencies.json"],
        work, "dependencies", allowed=(0, 1, 2))
    entry = f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    for label, source in (("mac", OLD_CORE[0]), ("runner", FROZEN_PW / "rtl/down2_dynamic_tile_runner.v")):
        tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
            source, "--report-json", work / f"{label}.json"], work, label, allowed=(0, 1, 2))
    print("REVIEW", work)


def simulate(baseline=False):
    work = tools.fresh("baseline" if baseline else "candidate")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    sources += (OLD_CORE if baseline else CORE) + [ADAPTER,
        FROZEN_PW / "rtl/down2_dynamic_tile_runner.v" if baseline else RUNNER, TB]
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


def physical(optimize=False):
    work = tools.fresh("physical_opt" if optimize else "physical")
    sources = [SHELL, RUNNER, ADAPTER, *CORE]
    tools.project(work, "layer_shell", sources)
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        (work / name).write_bytes((PREV / "physical_attempt2" / name).read_bytes())
    script = (work / "build.tcl").read_text(encoding="utf-8")
    script = script.replace('puts "OBJECT_COUNT all_regs=', '''set dsp_inputs [get_pins -of $dsp_cells -filter {DIRECTION == input} *]
set eram_inputs [get_pins -of $eram_cells -filter {DIRECTION == input} *]
report_timing_path -to $dsp_inputs -ep_num 100000 -path_num 1 -file dsp_inputs_all.timing
report_timing_path -to $eram_inputs -ep_num 100000 -path_num 1 -file eram_inputs_all.timing
puts "OBJECT_COUNT all_regs=''')
    if optimize:
        authority = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\doc\strategies\official_strategy_ph1.json")
        strategy = json.loads(authority.read_text(encoding="utf-8"))["TimingUltra"]
        assert strategy["is_syn"] == "phy" and len(strategy["params"]) == 14
        assert all(item["step"] in ("place", "route") for item in strategy["params"])
        commands = "\n".join(f"set_param {item['step']} {item['param']} {item['val']}" for item in strategy["params"])
        script = script.replace("\nplace\n", "\n" + commands + "\nreport_param\nplace\n")
        (work / "strategy.json").write_text(json.dumps({"source": str(authority),
            "sha256": tools.digest(authority), "strategy": strategy}, indent=2), encoding="utf-8")
    (work / "build.tcl").write_text(script, encoding="utf-8")
    (work / "input_manifest.json").write_text(json.dumps(
        {str(path): tools.digest(path) for path in sources}, indent=2), encoding="utf-8")
    print("PHYSICAL_WORK", work, flush=True)
    log = tools.command([tools.TD, "build.tcl"], work, "td", timeout=3600)
    print(log[-1800:])


def mac_sim():
    work = tools.fresh("mac_sim")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    reference = ROOT / "tests/mac_reference.py"
    tools.command([sys.executable, "-B", "-X", "utf8", reference], work, "reference")
    vectors = ROOT / "tests/vectors"
    sources = [CORE[0], ROOT / "tests/tb_mac_task_stream.v"]
    tools.command([msim / "vlib.exe", "work"], work, "vlib")
    tools.command([msim / "vlog.exe", "-sv", "-work", "work", *sources], work, "vlog")
    log = tools.command([msim / "vsim.exe", "-c", "-lib", "work", "tb_mac_task_stream",
        "+N_GROUPS=849", "+N_TASKS=119", f"+INPUTS={(vectors / 'mac_inputs.hex').as_posix()}",
        f"+EXPECTED={(vectors / 'mac_expected.hex').as_posix()}",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "simulation")
    assert "PASS mac_task_stream" in log and "Fatal:" not in log and "** Error:" not in log
    (work / "receipt.json").write_text(json.dumps({"result": [line for line in log.splitlines() if "PASS mac_task_stream" in line],
        "sources": {str(path): tools.digest(path) for path in sources}}, indent=2), encoding="utf-8")
    print(log[-1500:])


def gates():
    work = tools.fresh("gates")
    entry = f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    results = {}
    for label, runner in (("baseline", FROZEN_PW / "rtl/down2_dynamic_tile_runner.v"), ("candidate", RUNNER)):
        closure = work / label
        closure.mkdir()
        for source in [SHELL, runner, ADAPTER, *(OLD_CORE if label == "baseline" else CORE),
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
    print("RAW_GATES", work, "ERRORS", [results[label]["errors"] for label in ("baseline", "candidate")])
    # Preserve raw history, then always use the existing project checker facts.
    replay = tools.fresh("gates_overlay")
    tools.command([sys.executable, "-B", "-X", "utf8", ROOT / "checker_replay.py",
        "--raw-gates", work, "--output", replay], ROOT, replay.name)
    report = json.loads((replay / "report.json").read_text(encoding="utf-8"))
    print("PROJECT_GATES", replay, "ERRORS", [report["modes"][label]["replay"]["errors"]
        for label in ("baseline", "candidate")])


def specs():
    work = tools.fresh("s")
    # Reuse the canonical baseline port contract; no new Verilog parser.
    contract = json.loads((PREV / "s/down2_dynamic_tile_runner.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["description"] = "Four-credit PW task stream; frozen A0-A5 arithmetic, separate result descriptors."
    module["reset"]["values"] = "Asynchronous cancellation of credits, pipeline and descriptors; MAC ready=1 during reset exactly as frozen core, no valid transaction is accepted while reset asserted. Reload1024 table entries and parameters before runner start."
    module["behavior"] = ["Keep signed33 reduction, max24 groups/192 products per lane, final INT32 atomic zero fault, bias once and reduction II1.",
        "MAC first reserves one of four results until actual result pop, including time in A0-A5. Active reduction always accepts continuation.",
        "PW last acceptance advances issue position/channel; first acceptance pushes the matching descriptor. MAC result pop and descriptor pop are identical.",
        "PW parameters and tags come from descriptor head, never the new issue counters. Dynamic runtime TEST coefficients remain loaded through existing ports.",
        "Fault pop bypasses postprocess, invalidates entire tile and stops issuance. Already accepted successors remain owned until common reset; no soft cancellation.",
        "DW schedule unchanged. PW first operands prepared during previous last handshake; four-entry result and descriptor rings, no DDR or new external ports.",
        "No-stall down2 endpoint2607: DW2015 plus PW592; these are test-block cycles, not full network FPS."]
    module["verification_cases"] = ["Same40 layer scenarios per revision, all640 values at each arithmetic stage and384 exports.",
        "Random phase relative to core start; MAC/commit stability, four PW reset positions, full queue and final-lane overflow."]
    module["timing_diagrams"] = [{"id": "pw_task_stream", "title": "PW tasks overlap before prior result",
        "scenario": "pw_task_stream", "description": "First0/2/4/6, last1/3/5/7. First result pop8 can reuse credit. Sustained output depends on postprocess backpressure.",
        "wavejson": {"signal": [{"name": "clk", "wave": "p........."},
            {"name": "MAC first accepted", "wave": "1010101010"},
            {"name": "MAC last accepted", "wave": "0101010101"},
            {"name": "first descriptor/result pop", "wave": "0.......10"},
            {"name": "reserved credits", "wave": "=.=.=.=.=.", "data": [1,2,3,4,4]}],
            "head": {"tick": 0}}}]
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
    sys.path.insert(0, str(tools.SKILL))
    from scripts.python.quality.formatter_backend import VerilogFormatterEngine
    engine = VerilogFormatterEngine({"formatter": {"indent_style": "tab", "indent_size": 4}})
    _, _, ports, _ = engine._parse_module(CORE[0].read_text(encoding="utf-8"))
    def width(value):
        if not value: return 1
        hi, lo = value.strip("[]").split(":")
        return abs(int(hi) - int(lo)) + 1
    mac = dict(module, name="road_mac_probe", rtl_path="road_mac_probe.v",
        interfaces={"protocol": "discrete", "ports": [
            {"name": p.name, "direction": p.direction, "width": width(p.width),
             "role": p.name, "description": p.comment or p.name, "clock_domain": "i_clk"} for p in ports]})
    mac["behavior"] = module["behavior"][:2] + ["Legal tasks are contiguous, first exactly once and last within24 accepted groups. No interleaving or malformed-protocol tolerance is added.",
        "Result/fault stable until pop. Four slots are capacity-safe for any legal task; one-group tasks are not promised sustained II1.",
        "A0-A5 source unchanged; output ring stores fault bit96 and data bits95:0. Reset invalidates pointers/counts without relying on RAM initialization."]
    mac["corner_cases"] = ["Full credit with active reduction, simultaneous result pop and new first, random bubbles/backpressure.",
        "Positive/negative intermediate INT32 excursions recover within signed33; final overflow zeros all three lanes.",
        "Common asynchronous reset cancels all pipeline and queue ownership; ready=1 during reset matches old MAC, reset dominates all acceptance."]
    mac_path = work / "mac.json"
    mac_path.write_text(json.dumps({"modules": [mac]}, indent=2), encoding="utf-8")
    staged_mac = work / CORE[0].name
    shutil.copyfile(CORE[0], staged_mac)
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", mac_path,
        "--out-dir", work / "g", "--source", staged_mac, "--no-state"], work, "mac_spec", allowed=(0, 1, 2))
    shutil.copyfile(work / "g/spec/r/road_mac_probe_spec.md", CORE[0].with_name("road_mac_probe_spec.md"))
    shutil.copytree(work / "g/spec/r/waveforms", RUNNER.parent / "waveforms", dirs_exist_ok=True)
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


def shell_sim(gate=False, routed=False):
    work = tools.fresh("shell_routed_opt" if routed else "shell_gate" if gate else "shell_rtl")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    sources += [ROOT / "physical_opt/routed_netlist.v"] if routed else (
        [ROOT / "physical_attempt3/gate_netlist.v"] if gate else [*CORE, RUNNER, ADAPTER, SHELL])
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
         "candidate": simulate, "physical": physical, "physical_opt": lambda: physical(True),
         "gates": gates, "specs": specs,
         "shell_rtl": shell_sim, "shell_gate": lambda: shell_sim(True),
         "shell_routed_opt": lambda: shell_sim(routed=True), "zeroing": zeroing,
         "mac_sim": mac_sim}[sys.argv[1]]()
    finally:
        frozen()
