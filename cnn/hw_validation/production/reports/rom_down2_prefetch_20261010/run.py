"""ROM→down2独立接入；仅本目录可写，旧基线和失败证据只读。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
COMPUTE = REPORTS / "mac_ce_fanout_local_20261010"
ROM = REPORTS / "rom_schema2_mapping_20261010"
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MSIM = Path("D:/modeltech64_2020.4/win64")
spec = importlib.util.spec_from_file_location("local_tools", REPORTS / "runtime_layer_integration_20261009/run_candidate.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
digest = tools.digest


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snapshot():
    """完整复制两阶段及旧ROM证据；仅排除可再建的仿真work库。"""
    target = ROOT / "checkpoint"
    assert not target.exists(), "快照只创建一次，禁止覆盖"
    records = []
    for label, source in (("pre_rom_compute", COMPUTE), ("rom_diagnostic", ROM),
                          ("rom_original", ROOT.parents[2] / "rom")):
        for path in sorted(source.rglob("*")):
            if not path.is_file() or "work" in path.relative_to(source).parts or "__pycache__" in path.parts:
                continue
            copy = target / label / path.relative_to(source)
            copy.parent.mkdir(parents=True, exist_ok=True)
            before = digest(path)
            shutil.copy2(path, copy)
            assert digest(copy) == before == digest(path)
            records.append({"source": str(path), "snapshot": str(copy.relative_to(ROOT)), "sha256": before,
                            "bytes": path.stat().st_size})
    save(ROOT / "checkpoint_manifest.json", {"files": records, "bytes": sum(x["bytes"] for x in records),
         "excluded": ["ModelSim work libraries", "Python bytecode"], "overwrite_old_files": False})
    check()
    print("CHECKPOINT_VERIFIED", len(records), flush=True)


def check():
    manifest = json.loads((ROOT / "checkpoint_manifest.json").read_text(encoding="utf-8"))
    changed = [r["source"] for r in manifest["files"] if digest(Path(r["source"])) != r["sha256"]]
    damaged = [r["snapshot"] for r in manifest["files"] if digest(ROOT / r["snapshot"]) != r["sha256"]]
    save(ROOT / "checkpoint_check.json", {"checked": len(manifest["files"]), "old_files_changed": changed,
                                         "snapshot_damaged": damaged})
    assert not changed and not damaged, (changed, damaged)


def prepare():
    assert not (ROOT / "rtl").exists()
    (ROOT / "rtl").mkdir()
    for p in (COMPUTE / "rtl").glob("*.v"):
        shutil.copy2(p, ROOT / "rtl" / p.name)
    shutil.copy2(ROM / "rtl/road_yolo_numeric_rom_group.v", ROOT / "rtl/road_yolo_numeric_rom_group.v")
    shutil.copytree(ROM / "artifacts", ROOT / "artifacts")
    shutil.copytree(ROM / "artifacts", ROOT / "rtl/artifacts")
    (ROOT / "tests").mkdir()
    for p in (COMPUTE / "tests").glob("*.v"):
        shutil.copy2(p, ROOT / "tests" / p.name)
    save(ROOT / "status.json", {"stage": "frozen_and_prepared", "production_modified": False,
         "trained_parameters": False, "bitstream_generated": False})
    work = tools.fresh("preflight")
    output = tools.command([sys.executable, "-B", "-X", "utf8", SKILL /
        "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings", SKILL / "config/defaults.json"],
        work, "dependencies", allowed=(0, 1))
    dependency = json.loads(output[output.index("{"):])
    assert dependency["required_ok"]


def simulate():
    work = tools.fresh("simulation")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    sources = [Path(n) for n in json.loads((ROM / "vendor_simulation/input_manifest.json").read_text()).keys() if "sim_release" in n]
    sources += [p for p in sorted((ROOT / "rtl").glob("*.v")) if p.name != "road_dynamic_overlap_low_io_top.v"]
    sources += [ROOT / "tests/tb_rom_down2.v"]
    save(work / "input_manifest.json", {str(p): digest(p) for p in sources + [ROOT / "rtl/parameter_fields.vh"]})
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "+incdir+" + (ROOT / "rtl").as_posix(), "-work", "work", *sources], work, "vlog")
    log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_rom_down2",
        "+VECTORS=" + (ROOT / "vectors").as_posix(), "+REPORT=" + (work / "cycles.csv").as_posix(),
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim", timeout=600)
    assert "TB_PASS_ROM_DOWN2" in log and "Fatal:" not in log and "** Error:" not in log
    save(work / "receipt.json", {"all_passed": True, "vendor_model": True, "tiles": 7,
        "parameter_items_each_boot": 1676, "arithmetic_sources_changed": False,
        "sources": {str(p): digest(p) for p in sources}, "test_only": True})
    save(ROOT / "simulation_current.json", {"work": str(work)})
    print("ROM_DOWN2_SIMULATION_PASS", work, flush=True)


def reader():
    work = tools.fresh("reader")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    sources = [Path(n) for n in json.loads((ROM / "vendor_simulation/input_manifest.json").read_text()).keys() if "sim_release" in n]
    sources += [ROOT / "rtl" / n for n in ("road_yolo_numeric_rom_group.v", "road_numeric_rom_reader.v")]
    sources.append(ROOT / "tests/tb_rom_reader.v")
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_rom_reader",
        "+WORDS=" + (ROOT / "vectors/rom_words.hex").as_posix(),
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim", timeout=300)
    assert "TB_PASS_ROM_READER" in log and "Fatal:" not in log and "** Error:" not in log
    save(work / "receipt.json", {"all_passed": True, "bank_boundaries": 28, "words": 35,
         "reset_cancel": True, "response_hold_cycles": 17, "invalid_address": True,
         "sources": {str(p): digest(p) for p in sources}})
    save(ROOT / "reader_current.json", {"work": str(work)})


def gate():
    work = tools.fresh("gates")
    interface = ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v"
    overlay = REPORTS / "checker_fact_closure_20261009/checker_overlay"
    entry = f"import sys;sys.path[:0]=[{str(overlay)!r},{str(SKILL)!r}];from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    targets = (("full", ROOT / "rtl"), ("testbench", ROOT / "tests"))
    for label, target in targets:
        args = [sys.executable,"-B","-X","utf8","-c",entry,target,"--external-interface-source",interface,
                "--json",work / (label + ".json"),"--markdown",work / (label + ".md")]
        if label == "testbench": args.append("--include-testbench")
        tools.command(args,work,label,allowed=(0,1),timeout=600)
        data = json.loads((work / (label + ".json")).read_text(encoding="utf-8"))
        print("STRICT_GATE",label,data["errors"],data["strict_warnings"],data["checks"]["compile"]["status"],flush=True)
    save(ROOT / "gate_current.json", {"work": str(work)})


def regression():
    work = tools.fresh("regression")
    old_work = COMPUTE / "simulation_attempt2"
    compile_args = json.loads((old_work / "vlog.command.json").read_text())["command"]
    sources = [Path(p) for p in compile_args[3:]]
    for idx,p in enumerate(sources):
        if p.parent == COMPUTE / "rtl": sources[idx] = ROOT / "rtl" / p.name
        elif p.parent == COMPUTE / "tests": sources[idx] = ROOT / "tests" / p.name
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "-work", "work", *sources],work,"vlog")
    for suite in ("fixed_original","fixed_stress","dynamic_original","dynamic_stress"):
        args = json.loads((old_work / (suite + ".command.json")).read_text())["command"]
        args = [arg.replace(old_work.as_posix(), work.as_posix()).replace(str(old_work),str(work)) for arg in args]
        log = tools.command(args,work,suite,timeout=600)
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in log and "Fatal:" not in log and "** Error:" not in log
        for suffix in (".csv","_trace.csv","_windows.csv"):
            assert (work / (suite+suffix)).read_bytes() == (old_work / (suite+suffix)).read_bytes(), (suite,suffix)
    save(work / "receipt.json", {"all_passed":True,"same_vectors_same_cycles_and_traces":True,"cases":64,
          "sources":{str(p):digest(p) for p in sources}})
    save(ROOT / "regression_current.json", {"work":str(work)})


def physical():
    work = tools.fresh("physical")
    sources=[p for p in sorted((ROOT / "rtl").glob("*.v")) if p.name != "road_dynamic_overlap_low_io_top.v"]
    name=tools.project(work,"layer_shell",sources)
    project=work / name
    content=project.read_text(encoding="utf-8")
    for tag in ("LABEL","MODULE"):
        content=content.replace(f"<{tag}>road_dynamic_overlap_low_io_top</{tag}>",f"<{tag}>road_rom_down2_top</{tag}>")
    project.write_text(content,encoding="utf-8")
    project_input = work / "project_input.al"
    shutil.copy2(project, project_input)
    for name in ("joint.sdc","build.tcl"):
        shutil.copy2(ROOT / name,work / name)
    save(work / "input_manifest.json",{str(p):digest(p) for p in sources+[ROOT / "joint.sdc",ROOT / "build.tcl",project_input]})
    log=tools.command([tools.TD,"build.tcl"],work,"td",timeout=1800)
    assert "JOINT_PHYSICAL_DONE" in log and "ERROR:" not in log
    assert "STA coverage        : 100.00%" in (work / "final_timing.rpt").read_text()
    save(ROOT / "physical_current.json",{"work":str(work)})


def prefetch():
    work=tools.fresh("prefetch")
    sources=[ROOT / "rtl/road_down2_parameter_prefetch.v",ROOT / "tests/tb_parameter_prefetch.v"]
    tools.command([MSIM / "vlib.exe","work"],work,"vlib")
    tools.command([MSIM / "vlog.exe","-work","work",*sources],work,"vlog")
    log=tools.command([MSIM / "vsim.exe","-c","-lib","work","tb_parameter_prefetch",
        "+VECTORS="+(ROOT / "vectors").as_posix(),"-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],work,"vsim",timeout=300)
    assert "TB_PASS_PARAMETER_PREFETCH" in log and "Fatal:" not in log and "** Error:" not in log
    save(work / "receipt.json",{"all_passed":True,"random_and_long_backpressure":True,"shift63_rejected":True,
        "negative_multiplier_rejected":True,"reset_cancel":True,"sources":{str(p):digest(p) for p in sources},
        "endpoint":"controllable words endpoint; actual ROM separately covered by reader and joint tests"})
    save(ROOT / "prefetch_current.json",{"work":str(work)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("snapshot", "check", "prepare", "simulate", "reader", "gate", "regression", "physical", "prefetch"))
    stage = parser.parse_args().stage
    if stage != "snapshot":
        check()
    try:
        globals()[stage]()
    finally:
        if (ROOT / "checkpoint_manifest.json").exists():
            check()
