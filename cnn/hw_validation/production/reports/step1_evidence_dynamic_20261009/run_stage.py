"""Run bounded stage-one checks without writing any frozen directory."""

import argparse
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
BASE = REPORTS / "retirement_lane_banks_20261009"
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
VENDOR = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p")
COMMON = VENDOR.parent / "common"
MSIM = Path(r"D:\modeltech64_2020.4\win64")
FIXTURE = REPORTS / "diagnostic_repair_20261008" / "candidate_sim"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def publish(name, value):
    path = ROOT / name
    assert path.resolve().is_relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    paths = list((BASE / "rtl").glob("*.v"))
    paths += [BASE / "tests/tb_road_dynamic_postprocess.v", BASE / "tests/reference.py",
              BASE / "physical/physical_summary.json", BASE / "gates/rtl_gate.json",
              BASE / "gates/testbench_gate.json", FIXTURE / "batches.txt", FIXTURE / "table.hex"]
    for scope in ("runtime_chain", "layer_shell"):
        paths += [BASE / "physical" / scope / name for name in
                  ("gate.db", "pr.db", "gate_netlist.v", "routed_netlist.v", "shell.sdc", "shell.adc")]
    paths += list(VENDOR.glob("*.v"))
    paths += [MSIM / name for name in ("vlib.exe", "vlog.exe", "vsim.exe")]
    return {str(path): sha(path) for path in paths}


def run(command, work, name, timeout=300, allowed=(0,)):
    assert work.resolve().is_relative_to(ROOT)
    work.mkdir(parents=True, exist_ok=True)
    log = work / (name + ".log")
    if log.exists():
        raise FileExistsError(f"Retain previous attempt; choose a fresh directory: {log}")
    with log.open("w", encoding="utf-8") as stream:
        try:
            result = subprocess.run(list(map(str, command)), cwd=work, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            publish(str(log.relative_to(ROOT)) + ".command.json",
                    {"command": list(map(str, command)), "cwd": str(work), "launch_error": str(error)})
            raise
    publish(str(log.relative_to(ROOT)) + ".command.json",
            {"command": list(map(str, command)), "cwd": str(work), "exit_code": result.returncode})
    assert result.returncode in allowed, (result.returncode, log)
    return log.read_text(encoding="utf-8", errors="replace")


def prepare():
    publish("frozen.json", freeze())
    for name in ("batches.txt", "table.hex"):
        shutil.copyfile(FIXTURE / name, ROOT / name)
    packets = []
    expected = []
    for line in (FIXTURE / "batches.txt").read_text(encoding="ascii").splitlines():
        acc, mul, shift, post, post_shift, activate, mask, tags, result = map(
            lambda value: int(value, 16), line.split())
        packet = (acc | mul << 96 | shift << 192 | post << 210 | post_shift << 242 |
                  activate << 248 | mask << 249 | tags << 252)
        packets.append(f"{packet:076x}")
        for lane in range(3):
            if mask & (1 << lane):
                expected.append(f"{((2 if not activate else 0) << 32) | (((result >> (lane*16)) & 65535) << 16) | ((tags >> (lane*16)) & 65535):012x}")
    assert len(packets) == 330 and len(expected) == 604
    (ROOT / "packets.hex").write_text("\n".join(packets) + "\n", encoding="ascii")
    (ROOT / "expected.hex").write_text("\n".join(expected) + "\n", encoding="ascii")
    masks = [int(line.split()[6], 16) for line in (FIXTURE / "batches.txt").read_text().splitlines()]
    (ROOT / "masks.hex").write_text("\n".join(f"{value:x}" for value in masks) + "\n", encoding="ascii")
    command = [sys.executable, "-B", "-X", "utf8", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
               "check", "--settings", SKILL / "config/defaults.json", "--state-path", ROOT / "dependency_state.json"]
    run(command, ROOT / "preflight", "dependencies", allowed=(0, 1, 2))
    run([sys.executable, "-B", "-X", "utf8", BASE / "tests/reference.py"],
        ROOT / "preflight", "numeric_reference")
    publish("status.json", {"stage": "STEP1_PREPARED", "release": False,
                            "kernel_sources_modified": False, "training": "NOT_RUN"})
    print("PREPARED frozen files", len(freeze()), "packets=330 expected=604")


def shell_sim(mode):
    work = ROOT / mode
    attempt = 1
    while work.exists():
        attempt += 1
        work = ROOT / f"{mode}_attempt{attempt}"
    sources = sorted(VENDOR.glob("*.v")) + sorted(COMMON.glob("*.v"))
    if not (ROOT / "additional_frozen.json").exists():
        publish("additional_frozen.json", {str(path): sha(path) for path in COMMON.glob("*.v")})
    if mode == "shell_rtl":
        sources += [BASE / "rtl" / name for name in
                    ("road_dynamic_postprocess.v", "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")]
        sources.append(BASE / "physical/runtime_chain/road_dynamic_chain_low_io_top.v")
    else:
        sources.append(BASE / "physical/runtime_chain/gate_netlist.v")
    sources.append(ROOT / "tb_dynamic_shell_vectors.v")
    run([MSIM / "vlib.exe", "work"], work, "vlib")
    run([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    text = run([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_dynamic_shell_vectors",
                f"+VECTORS={ROOT.as_posix()}", "-do",
                "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
               work, "simulation", timeout=600)
    assert "TB_PASS_DYNAMIC_SHELL packets=330 outputs=604" in text
    assert "Fatal:" not in text and "** Error:" not in text
    publish(str(work.relative_to(ROOT)) + "/receipt.json", {"status": "PASS", "sources": {str(path): sha(path) for path in sources},
                                     "packets": 330, "outputs": 604,
                                     "vendor_models": "actual installed PH1P library; not the custom ERAM stand-in",
                                     "boundary": "serialized diagnostic chain only, not MAC/tile/whole-model/board/timing"})
    print(mode, "PASS packets=330 outputs=604")


def replay(mode):
    """Reuse the original regression, but keep every generated artifact here."""
    work = ROOT / mode
    attempt = 1
    while work.exists():
        attempt += 1
        work = ROOT / f"{mode}_attempt{attempt}"
    work.mkdir(parents=True)
    sources = sorted(VENDOR.glob("*.v")) + sorted(COMMON.glob("*.v"))
    names = ("road_dynamic_postprocess.v", "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")
    if mode == "representative_replay":
        names += ("road_mac_probe.v",)
        tb = ROOT / "tb_representative_chain.v"
        top = "tb_representative_chain"
    elif mode == "layer_replay":
        names += ("road_mac_probe.v", "road_down2_dynamic_adapter.v", "down2_dynamic_tile_runner.v")
        tb = BASE / "tests/layer/tb_down2_dynamic_overlap.v"
        top = "tb_down2_dynamic_overlap"
    else:
        tb = BASE / "tests/tb_road_dynamic_postprocess.v"
        top = "tb_road_dynamic_postprocess"
        for name in ("batches.txt", "table.hex"):
            shutil.copyfile(FIXTURE / name, work / name)
    sources += [BASE / "rtl" / name for name in names] + [tb]
    run([MSIM / "vlib.exe", "work"], work, "vlib")
    run([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    scenarios = {"core": []}
    if mode == "representative_replay":
        scenarios = {"representative": [f"+VECTORS={ROOT.as_posix()}"]}
    if mode == "layer_replay":
        fixture_root = FIXTURE.parent / "layer"
        scenarios = {"original": [f"+VECTORS={(fixture_root / 'vectors').as_posix()}"],
                     "stress": [f"+VECTORS={(fixture_root / 'stress_bias_contract_host/vectors').as_posix()}"]}
    markers = {}
    for case, args in scenarios.items():
        if mode == "layer_replay":
            args += [f"+REPORT={(work / (case + '_cycles.csv')).as_posix()}"]
        transcript = run([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top, *args,
                          "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
                         work, case, timeout=600)
        marker = {"layer_replay": "TB_PASS_DOWN2_DYNAMIC_OVERLAP", "core_replay": "TB_PASS_DYNAMIC_OVERLAP",
                  "representative_replay": "TB_PASS_REPRESENTATIVE"}[mode]
        assert marker in transcript and "Fatal:" not in transcript and "** Error:" not in transcript
        markers[case] = next(line for line in transcript.splitlines() if marker in line)
    publish(str(work.relative_to(ROOT)) + "/receipt.json",
            {"status": "PASS", "markers": markers, "sources": {str(path): sha(path) for path in sources},
             "vendor_models": "actual installed PH1P and TD common models", "old_runner_executed": False})
    print(mode, markers)


def check():
    old = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    if (ROOT / "additional_frozen.json").exists():
        old.update(json.loads((ROOT / "additional_frozen.json").read_text(encoding="utf-8")))
    changed = [name for name, digest in old.items() if sha(Path(name)) != digest]
    publish("frozen_check.json", {"checked": len(old), "changed": changed})
    assert not changed, changed
    print("FROZEN_UNCHANGED", len(old))


def warning_probe():
    tool = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe")
    work = ROOT / "syn5025_probe"
    if (work / "td.log").exists():
        attempt = 2
        work = ROOT / f"syn5025_probe_attempt{attempt}"
        while work.exists():
            attempt += 1
            work = ROOT / f"syn5025_probe_attempt{attempt}"
        work.mkdir()
        for name in ("road_driven_probe.v", "build.tcl"):
            shutil.copyfile(ROOT / "syn5025_probe" / name, work / name)
        template = (BASE / "physical/runtime_chain/road_dynamic_chain_low_io_top.al").read_text(encoding="utf-8")
        template = re.sub(r'<Project Version="3" Minor="2" Path="[^"]*">',
                          f'<Project Version="3" Minor="2" Path="{work.as_posix()}">', template)
        template = template.replace("road_dynamic_chain_low_io_top", "road_driven_probe")
        template = re.sub(r'    <Source_Files>.*?    </Source_Files>',
                         '    <Source_Files><Verilog><File Path="road_driven_probe.v"><FileInfo>'
                         '<Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/>'
                         '<Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="1"/>'
                         '</FileInfo></File></Verilog></Source_Files>', template, flags=re.S)
        (work / "road_driven_probe.al").write_text(template, encoding="utf-8")
    text = run([tool, "build.tcl"], work, "td", timeout=180)
    assert "PROBE_SYNTHESIS_DONE" in text
    publish(str(work.relative_to(ROOT)) + "/receipt.json", {"complete": True, "syn5025_in_fully_driven_design": "SYN-5025" in text,
            "boundary": "This tests warning specificity; it does not waive floating functional inputs in a CNN netlist."})
    print("SYN5025_PROBE_DONE generic_warning=", "SYN-5025" in text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "shell_rtl", "shell_gate", "core_replay", "layer_replay", "representative_replay", "warning_probe", "check"))
    mode = parser.parse_args().mode
    if mode == "prepare":
        prepare()
    elif mode == "check":
        check()
    else:
        try:
            if mode == "warning_probe":
                warning_probe()
            elif mode.endswith("replay"):
                replay(mode)
            else:
                shell_sim(mode)
        finally:
            check()
