"""Bounded candidate runner: never execute a frozen build in its old directory."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "retirement_lane_banks_20261009"
PREVIOUS = ROOT.parent / "step1_evidence_dynamic_20261009"
TD = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe")
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_frozen():
    frozen = json.loads((PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
    frozen.update(json.loads((PREVIOUS / "additional_frozen.json").read_text(encoding="utf-8")))
    frozen.update({str(PREVIOUS / name): value for name, value in json.loads(
                  (PREVIOUS / "evidence_hashes.json").read_text(encoding="utf-8")).items()})
    changed = [name for name, value in frozen.items() if digest(Path(name)) != value]
    (ROOT / "frozen_check.json").write_text(json.dumps({"checked": len(frozen), "changed": changed}, indent=2), encoding="utf-8")
    assert not changed, changed


def fresh(name):
    path = ROOT / name
    index = 1
    while path.exists():
        index += 1
        path = ROOT / f"{name}_attempt{index}"
    path.mkdir(parents=True)
    return path


def command(args, work, label, timeout=600, allowed=(0,)):
    assert work.resolve().is_relative_to(ROOT)
    log = work / f"{label}.log"
    assert not log.exists(), log
    with log.open("w", encoding="utf-8") as stream:
        try:
            result = subprocess.run(list(map(str, args)), cwd=work, stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            (work / f"{label}.command.json").write_text(json.dumps({"command": list(map(str, args)),
                    "cwd": str(work), "launch_error": str(error)}, indent=2), encoding="utf-8")
            raise
    (work / f"{label}.command.json").write_text(json.dumps({"command": list(map(str, args)),
            "cwd": str(work), "returncode": result.returncode}, indent=2), encoding="utf-8")
    assert result.returncode in allowed, (result.returncode, log)
    return log.read_text(encoding="utf-8", errors="replace")


def project(work, scope, sources=None):
    template_root = BASE / "physical" / scope
    template = next(template_root.glob("*.al"))
    content = template.read_text(encoding="utf-8")
    content = re.sub(r'<Project Version="3" Minor="2" Path="[^"]*">',
                     f'<Project Version="3" Minor="2" Path="{work.as_posix()}">', content)
    if sources is None:
        content = re.sub(r'<File Path="([^"]+)">', lambda match:
                         f'<File Path="{(template_root / match[1]).resolve().as_posix()}">', content)
    else:
        entries = "".join(f'<File Path="{source.as_posix()}"><FileInfo>'
                 f'<Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&amp;R" Val="true"/>'
                 f'<Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{order}"/>'
                 '</FileInfo></File>' for order, source in enumerate(sources, 1))
        content = re.sub(r'    <Source_Files>.*?    </Source_Files>',
                         f'    <Source_Files><Verilog>{entries}</Verilog></Source_Files>', content, flags=re.S)
    (work / template.name).write_text(content, encoding="utf-8")
    return template.name


def zeroing():
    work = fresh("zeroing_elaboration")
    name = project(work, "runtime_chain")
    script = (ROOT / "inspect_elaboration.tcl").read_text(encoding="utf-8").replace("PROJECT_FILE", name)
    (work / "inspect.tcl").write_text(script, encoding="utf-8")
    text = command([TD, "inspect.tcl"], work, "td", timeout=300)
    print(text[-6000:])


def zeroing_models(candidate=False):
    # Query each definition at its own top: TD returns ambiguous local names for
    # get_nets -hier before repeated child definitions are uniquified.
    work = fresh("zc" if candidate else "z")
    modules = ("road_dynamic_overlap_low_io_top", "down2_dynamic_tile_runner", "road_down2_dynamic_adapter",
               "road_mac_probe", "road_dynamic_postprocess", "road_dynamic_requant", "road_round_shift", "silu_shared_unit") if candidate else (
               "road_dynamic_chain_low_io_top", "road_dynamic_postprocess", "road_round_shift")
    source_paths = [ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"] + list((ROOT / "rtl").glob("*.v")) + [
        BASE / "rtl" / name for name in ("road_mac_probe.v", "road_dynamic_postprocess.v", "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")]
    all_records = {}
    for index, module in enumerate(modules):
        scope = work / str(index)
        scope.mkdir()
        template_top = "road_dynamic_overlap_low_io_top" if candidate else "road_dynamic_chain_low_io_top"
        project_name = project(scope, "layer_shell" if candidate else "runtime_chain", source_paths if candidate else None)
        project_path = scope / project_name
        text = project_path.read_text(encoding="utf-8").replace(f"<LABEL>{template_top}</LABEL>", f"<LABEL>{module}</LABEL>")
        text = text.replace(f"<MODULE>{template_top}</MODULE>", f"<MODULE>{module}</MODULE>")
        project_path.write_text(text, encoding="utf-8")
        script = f"""import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project {project_name} -single_run
elaborate -top {module}
set dead [get_nets -filter {{DRIVER_COUNT == 0}} *]
puts "DEFINITION {module} UNDRIVEN [llength $dead]"
foreach net $dead {{
    puts "DEAD_RECORD [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}}
report_nets $dead -connection -pin_display_limit 100
puts "MODEL_QUERY_DONE"
close_project
"""
        (scope / "inspect.tcl").write_text(script, encoding="utf-8")
        log = command([TD, "inspect.tcl"], scope, "td", timeout=180)
        assert "MODEL_QUERY_DONE" in log and "ERROR:" not in log and "Could not find net" not in log
        records = [line for line in log.splitlines() if line.startswith("DEFINITION") or line.startswith("DEAD_RECORD")]
        all_records[module] = records
        print(records[0], "with_load=", sum("PINS 0 DRIVER 0" not in line for line in records[1:]))
    (work / "receipt.json").write_text(json.dumps(all_records, indent=2), encoding="utf-8")


def compare_gates():
    import shutil
    work = fresh("gate_comparison")
    sources = list((BASE / "rtl").glob("*.v")) + [BASE / "physical/layer_shell/road_dynamic_overlap_low_io_top.v",
               ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v"]
    closure = work / "baseline"
    closure.mkdir()
    for source in sources:
        shutil.copyfile(source, closure / source.name)
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, closure, "--json", work / "baseline.json",
             "--markdown", work / "baseline.md"], work, "baseline", allowed=(0, 1, 2))
    old = json.loads((work / "baseline.json").read_text(encoding="utf-8"))
    new = json.loads((ROOT / "gates_attempt3/full_closure.json").read_text(encoding="utf-8"))
    a, b = old["delivery_issues_by_rule"], new["delivery_issues_by_rule"]
    delta = {rule: b.get(rule, 0) - a.get(rule, 0) for rule in sorted(a.keys() | b.keys()) if a.get(rule, 0) != b.get(rule, 0)}
    (work / "comparison.json").write_text(json.dumps({"baseline_errors": old["errors"], "candidate_errors": new["errors"],
                "baseline_warnings": old["strict_warnings"], "candidate_warnings": new["strict_warnings"], "delta_by_rule": delta}, indent=2), encoding="utf-8")
    print("STRICT_SAME_SCOPE", old["errors"], "->", new["errors"], "warnings", old["strict_warnings"], "->", new["strict_warnings"])


def simulate():
    work = fresh("layer_regression")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    sources += [BASE / "rtl" / name for name in ("road_mac_probe.v", "road_dynamic_postprocess.v",
                "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")]
    sources += [ROOT / "rtl/road_down2_dynamic_adapter.v", ROOT / "rtl/down2_dynamic_tile_runner.v",
                ROOT / "tests/layer/tb_down2_dynamic_overlap.v"]
    command([msim / "vlib.exe", "work"], work, "vlib")
    command([msim / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for case in ("fixed_original", "fixed_stress", "dynamic_original", "dynamic_stress"):
        text = command([msim / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_down2_dynamic_overlap",
                        f"+VECTORS={(ROOT / 'vectors' / case).as_posix()}",
                        f"+REPORT={(work / (case + '.csv')).as_posix()}",
                        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, case)
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in text and "Fatal:" not in text and "** Error:" not in text
        results[case] = [line for line in text.splitlines() if "LAYER_OVERLAP_PASS" in line or "TB_PASS" in line]
        print(case, *results[case], sep="\n")
    (work / "receipt.json").write_text(json.dumps({"results": results,
                "sources": {str(path): digest(path) for path in sources}}, indent=2), encoding="utf-8")


def gates():
    work = fresh("gates")
    command([sys.executable, "-B", "-X", "utf8", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
             "check", "--settings", SKILL / "config/defaults.json", "--state-path", work / "dependency_state.json"],
            work, "dependencies", allowed=(0, 1, 2))
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    import shutil
    closure = work / "source_closure"
    closure.mkdir()
    for source in [BASE / "rtl" / name for name in ("road_mac_probe.v", "road_dynamic_postprocess.v",
                  "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")] + list((ROOT / "rtl").glob("*.v")) + [
                  ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v",
                  ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v"]:
        shutil.copyfile(source, closure / source.name)
    for label, target in (("full_closure", closure), ("layer", ROOT / "rtl"), ("shell", ROOT / "physical/layer_shell"),
                           ("testbench", ROOT / "tests/layer")):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, target,
                 "--json", work / f"{label}.json", "--markdown", work / f"{label}.md", "--include-testbench"],
                work, label, allowed=(0, 1, 2))
        print("GATE", label, (work / f"{label}.json").exists())


def physical():
    work = fresh("physical")
    sources = [ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v",
               ROOT / "rtl/down2_dynamic_tile_runner.v", ROOT / "rtl/road_down2_dynamic_adapter.v"]
    sources += [BASE / "rtl" / name for name in ("road_mac_probe.v", "road_dynamic_postprocess.v",
                 "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")]
    project(work, "layer_shell", sources)
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        source = BASE / "physical/layer_shell" / name
        (work / name).write_bytes(source.read_bytes())
    (work / "input_manifest.json").write_text(json.dumps({str(path): digest(path) for path in sources}, indent=2), encoding="utf-8")
    print("PHYSICAL_WORK", work, flush=True)
    text = command([TD, "build.tcl"], work, "td", timeout=3600)
    print(text[-1800:])


def shell_sim(gate=False):
    work = fresh("shell_gate" if gate else "shell_rtl")
    msim = Path(r"D:\modeltech64_2020.4\win64")
    vendor = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release")
    sources = sorted((vendor / "ph1p").glob("*.v")) + sorted((vendor / "common").glob("*.v"))
    if gate:
        sources += [ROOT / "physical_attempt2/gate_netlist.v"]
    else:
        sources += [BASE / "rtl" / name for name in ("road_mac_probe.v", "road_dynamic_postprocess.v",
                     "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")]
        sources += list((ROOT / "rtl").glob("*.v"))
        sources += [ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"]
    sources += [ROOT / "tests/layer/tb_runtime_layer_shell.v"]
    command([msim / "vlib.exe", "work"], work, "vlib")
    command([msim / "vlog.exe", "-work", "work", *sources], work, "vlog")
    results = {}
    for case in ("fixed_stress", "dynamic_stress"):
        text = command([msim / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_runtime_layer_shell",
                        f"+VECTORS={(ROOT / 'vectors' / case).as_posix()}", "-do",
                        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, case)
        assert "TB_PASS_RUNTIME_LAYER_SHELL" in text and "Fatal:" not in text and "** Error:" not in text
        results[case] = next(line for line in text.splitlines() if "TB_PASS_RUNTIME" in line)
        print(case, results[case])
    (work / "receipt.json").write_text(json.dumps({"results": results,
                "sources": {str(path): digest(path) for path in sources}, "sdf": False}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    check_frozen()
    try:
        if sys.argv[1] == "zeroing":
            zeroing()
        elif sys.argv[1] == "zeroing_models":
            zeroing_models()
        elif sys.argv[1] == "zeroing_candidate":
            zeroing_models(True)
        elif sys.argv[1] == "compare_gates":
            compare_gates()
        elif sys.argv[1] == "simulate":
            simulate()
        elif sys.argv[1] == "gates":
            gates()
        elif sys.argv[1] == "physical":
            physical()
        elif sys.argv[1] == "shell_rtl":
            shell_sim()
        elif sys.argv[1] == "shell_gate":
            shell_sim(True)
        else:
            raise ValueError(sys.argv[1])
    finally:
        check_frozen()
