"""参数接入单变量候选：旧文件只读，所有运行输出限定到本目录。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "rom_down2_prefetch_20261010"
spec = importlib.util.spec_from_file_location("frozen_rom_run", BASE / "run.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ROOT = ROOT
base.tools.ROOT = ROOT
tools, SKILL, MSIM = base.tools, base.SKILL, base.MSIM
digest, save = base.digest, base.save
COMPUTE, ROM = base.COMPUTE, base.ROM


def check():
    manifest = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in manifest.items() if digest(Path(name)) != value]
    unchanged = [p.name for p in (BASE / "rtl").glob("*.v")
                 if p.name != "road_rom_down2_top.v"]
    candidate_changed = [name for name in unchanged
                         if digest(ROOT / "rtl" / name) != digest(BASE / "rtl" / name)]
    save(ROOT / "frozen_check.json", {"checked": len(manifest), "old_files_changed": changed,
                                      "frozen_rtl_changed": candidate_changed})
    assert not changed and not candidate_changed, (changed, candidate_changed)


base.check = check


def prepare():
    assert not (ROOT / "frozen.json").exists(), "禁止覆盖候选或旧基线"
    records = {}
    for p in BASE.rglob("*"):
        if p.is_file() and not any(part in ("work", "__pycache__", "checkpoint")
                                   for part in p.relative_to(BASE).parts):
            records[str(p)] = digest(p)
    save(ROOT / "frozen.json", records)
    for name in ("rtl", "tests", "vectors", "artifacts"):
        shutil.copytree(BASE / name, ROOT / name)
    shutil.copy2(BASE / "joint.sdc", ROOT / "joint.sdc")
    shutil.copy2(BASE / "rtl/road_rom_down2_top.v", ROOT / "baseline_top.v.txt")
    save(ROOT / "status.json", {"stage": "prepared", "production_modified": False,
         "bitstream_generated": False, "candidate": 1, "maximum_structural_candidates": 2})
    check()
    work = tools.fresh("preflight")
    output = tools.command([sys.executable, "-B", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
                   "check", "--settings", SKILL / "config/defaults.json",
                   "--state-path", work / "dependency_state.json"], work, "dependencies", allowed=(0, 1))
    assert json.loads(output[output.index("{"):])["required_ok"]
    print("PREPARED", len(records), flush=True)


def gate():
    # 与旧12模块完全同范围；另保留修改前的 formatter-AST 证据。
    base.gate()


def gate_testbench():
    work = tools.fresh("testbench_gate")
    previous = Path(json.loads((ROOT / "gate_current.json").read_text())["work"])
    args = json.loads((previous / "testbench.command.json").read_text())["command"]
    args = [arg.replace(str(previous), str(work)) for arg in args]
    tools.command(args, work, "testbench", allowed=(0, 1), timeout=600)
    save(ROOT / "testbench_gate_current.json", {"work": str(work)})


def reference():
    work = tools.fresh("reference")
    log = tools.command([sys.executable, "-B", ROOT / "ingress_reference.py"], work, "model")
    assert "INGRESS_REFERENCE_PASS" in log
    save(work / "receipt.json", {"passed": True, "source_sha256": digest(ROOT / "ingress_reference.py")})


def specification():
    work = tools.fresh("s")
    previous = json.loads((BASE / "s/spec.json").read_text(encoding="utf-8"))["modules"]
    modules = [m for m in previous if m["name"] in ("road_rom_down2_top", "tb_rom_down2")]
    top = next(m for m in modules if m["name"] == "road_rom_down2_top")
    top["behavior"] = [
        "50位外部端口不变；两级同步释放后自动从冻结TEST ROM装参数及1024项SiLU表。",
        "仅参数流增加pending1/kind3/address11/data32单笔寄存，空时接收，不支持同拍排出补入。",
        "预取器ready只确认进入缓冲；runner valid&&ready才确认参数提交，反压时payload保持。",
        "pref_done、table_loaded、沿前pending=0且无fault才登记external_owner，末笔消费同拍不移交。",
        "halo和表保持原直通接口；最后halo握手后的下一拍允许start。",
        "故障当拍禁止runner参数有效，下一沿清pending/owner；复位立即取消、重新完整预取。",
        "保持MAC/动态重定标/RNE/SiLU/缓存及II；启动周期单列，小块核心应仍1687周期。"]
    top["timing_diagrams"] = [{"id": "entry", "title": "单笔参数保持与提交", "scenario": "entry",
        "description": "在capture沿锁存，受阻保持，consume沿释放；owner另在已空的后续沿登记。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
          {"name": "pref_valid", "wave": "01.0...."}, {"name": "pref_ready", "wave": "10..1..."},
          {"name": "pending", "wave": "01..0..."}, {"name": "runner_ready", "wave": "0..1...."},
          {"name": "runner_valid", "wave": "01..0..."}, {"name": "pref_done", "wave": "0...1..."},
          {"name": "table_loaded", "wave": "0...1..."}, {"name": "external_owner", "wave": "0....1.."}]}}]
    tb = json.loads(json.dumps(next(m for m in modules if m["name"] == "tb_rom_down2")))
    tb["name"] = "tb_rom_ingress"
    tb["rtl_path"] = "tests/tb_rom_ingress.v"
    tb["clock"]["name"] = "clk"
    tb["reset"]["name"] = "rstn"
    tb["behavior"] = ["验证参数缓冲守恒、长反压、末笔排空、阶段隔离及各装载位置复位。",
        "使用测试平台force注入runner ready背压；不是新增部署端口或真实外设协议。"]
    modules.append(tb)
    save(work / "spec.json", {"modules": modules})
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", work / "spec.json",
        "--out-dir", work / "g", "--no-state"], work, "write", allowed=(0, 1, 2), timeout=120)
    for module in modules:
        source = ROOT / module["rtl_path"]
        companion = work / "g/spec/r" / ("tests" if source.parent.name == "tests" else "") / (source.stem + "_spec.md")
        assert companion.exists(), companion
        shutil.copy2(companion, source.with_name(companion.name))
        shutil.copytree(companion.parent / "waveforms", source.parent / "waveforms", dirs_exist_ok=True)
    save(ROOT / "specification_current.json", {"work": str(work)})


def synthesize():
    assert (ROOT / "simulation_current.json").exists(), "先完成联合功能回归"
    assert (ROOT / "ingress_current.json").exists(), "先完成边界压力测试"
    work = ROOT / "physical"
    assert not work.exists(), "同一结构候选只综合一次，失败记录不覆盖"
    work.mkdir()
    sources = [p for p in sorted((ROOT / "rtl").glob("*.v"))
               if p.name != "road_dynamic_overlap_low_io_top.v"]
    name = tools.project(work, "layer_shell", sources)
    project = work / name
    text = project.read_text(encoding="utf-8")
    text = text.replace("<LABEL>road_dynamic_overlap_low_io_top</LABEL>",
                        "<LABEL>road_rom_down2_top</LABEL>")
    text = text.replace("<MODULE>road_dynamic_overlap_low_io_top</MODULE>",
                        "<MODULE>road_rom_down2_top</MODULE>")
    project.write_text(text, encoding="utf-8")
    shutil.copy2(project, work / "project_input.al")
    shutil.copy2(ROOT / "joint.sdc", work / "joint.sdc")
    for label in ("synthesize.tcl", "route.tcl"):
        shutil.copy2(ROOT / label, work / label)
    save(work / "input_manifest.json", {str(p): digest(p) for p in sources +
         [ROOT / "joint.sdc", ROOT / "synthesize.tcl", ROOT / "route.tcl"]})
    log = tools.command([tools.TD, "synthesize.tcl"], work, "synthesis", timeout=900)
    assert "INGRESS_SYNTHESIS_DONE" in log and "ERROR:" not in log
    original = (BASE / "physical_attempt2/gate_netlist.v").read_text(encoding="utf-8")
    candidate = (work / "gate_netlist.v").read_text(encoding="utf-8")
    clean = lambda value: re.sub(r"(?m)^//.*(?:Date|Time|Generated).*\n", "", value)
    assert clean(original) != clean(candidate), "目标网表未变，不进行重复布局布线"
    evidence = {"source_changed": digest(ROOT / "rtl/road_rom_down2_top.v") != digest(BASE / "rtl/road_rom_down2_top.v"),
        "gate_netlist_changed": True,
        "buffer_register_mentions": len(re.findall(r"reg_pref_(?:kind|address|data)|flag_pref_pending", candidate)),
        "phase_register_mentions": len(re.findall(r"flag_external_owner", candidate)),
        "manual_cone_review_required": True, "route_allowed": False}
    assert evidence["buffer_register_mentions"] and evidence["phase_register_mentions"], evidence
    save(work / "novelty.json", evidence)
    print("SYNTHESIS_DONE_REVIEW_CONE_BEFORE_ROUTE", flush=True)


def route():
    work = ROOT / "physical"
    evidence = json.loads((work / "novelty.json").read_text(encoding="utf-8"))
    assert evidence.get("route_allowed"), "关键锥尚未人工核对"
    manifest = json.loads((work / "input_manifest.json").read_text(encoding="utf-8"))
    assert all(digest(Path(p)) == value for p, value in manifest.items())
    log = tools.command([tools.TD, "route.tcl"], work, "route", timeout=1800)
    assert "JOINT_PHYSICAL_DONE" in log and "ERROR:" not in log
    assert "STA coverage        : 100.00%" in (work / "final_timing.rpt").read_text()
    save(ROOT / "physical_current.json", {"work": str(work)})
    print("ROUTE_DONE", flush=True)


def ingress():
    work = tools.fresh("ingress")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    manifest = json.loads((base.ROM / "vendor_simulation/input_manifest.json").read_text())
    sources = [Path(p) for p in manifest if "sim_release" in p]
    sources += [p for p in sorted((ROOT / "rtl").glob("*.v"))
                if p.name != "road_dynamic_overlap_low_io_top.v"]
    sources += [ROOT / "tests/tb_rom_ingress.v"]
    tools.command([MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([MSIM / "vlog.exe", "+incdir+" + (ROOT / "rtl").as_posix(), "-work", "work", *sources], work, "vlog")
    log = tools.command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_rom_ingress",
        "+VECTORS=" + (ROOT / "vectors").as_posix(), "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "vsim", timeout=600)
    assert "TB_PASS_ROM_INGRESS" in log and "Fatal:" not in log and "** Error:" not in log
    save(work / "receipt.json", {"all_passed": True, "vendor_model": True,
         "sources": {str(p): digest(p) for p in sources}})
    save(ROOT / "ingress_current.json", {"work": str(work)})
    print("INGRESS_PASS", flush=True)


def collect():
    import csv
    sys.modules["run"] = sys.modules[__name__]
    descriptor = importlib.util.spec_from_file_location("frozen_collector", BASE / "collect.py")
    collector = importlib.util.module_from_spec(descriptor)
    descriptor.loader.exec_module(collector)
    result = {"test_parameters_only": True, "production_modified": False, "bitstream_generated": False,
              "external_signed_off": False, "whole_network_fps_proven": False}
    simulation = Path(json.loads((ROOT / "simulation_current.json").read_text())["work"])
    result["cycles"] = list(csv.DictReader((simulation / "cycles.csv").open(encoding="utf-8")))
    result["numeric_inputs"] = {}
    for folder in ("vectors", "artifacts", "rtl/artifacts"):
        for path in (ROOT / folder).rglob("*"):
            if path.is_file():
                assert digest(path) == digest(BASE / folder / path.relative_to(ROOT / folder))
                result["numeric_inputs"][str(path.relative_to(ROOT))] = digest(path)
    result["parameter_include_sha256"] = digest(ROOT / "rtl/parameter_fields.vh")
    result["tool_hashes"] = {str(path): digest(path) for path in
        (Path(sys.executable), tools.TD, MSIM / "vlog.exe", MSIM / "vsim.exe")}
    for label in ("simulation", "ingress", "regression"):
        work = Path(json.loads((ROOT / (label + "_current.json")).read_text())["work"])
        receipt = json.loads((work / "receipt.json").read_text())
        assert receipt["all_passed"] and all(digest(Path(p)) == value for p, value in receipt["sources"].items())
        result[label] = {"work": str(work.relative_to(ROOT)), "all_passed": True}
    work = Path(json.loads((ROOT / "gate_current.json").read_text())["work"])
    full = json.loads((work / "full.json").read_text(encoding="utf-8"))
    tbwork = Path(json.loads((ROOT / "testbench_gate_current.json").read_text())["work"])
    tb = json.loads((tbwork / "testbench.json").read_text(encoding="utf-8"))
    result["strict_gates"] = {"full": {key: full[key] for key in ("errors", "strict_warnings", "checks")},
                              "testbench": {key: tb[key] for key in ("errors", "strict_warnings", "checks")}}
    work = ROOT / "physical"
    manifest = json.loads((work / "input_manifest.json").read_text())
    assert all(digest(Path(p)) == value for p, value in manifest.items())
    area = (work / "joint_route.area").read_text(encoding="utf-8")
    result["resources_including_shell"] = {key: int(re.search(r"^#" + key + r"\s+(\d+)", area, re.M).group(1))
                                           for key in ("IO", "slice", "reg", "lut6", "dsp", "eram")}
    result["timing"] = {name: collector.timing(work / (name + ".timing")) for name in
        ("all_paths", "internal", "external_reset", "eram_outputs", "eram_inputs", "dsp_outputs", "dsp_inputs")}
    initial = collector.rom_initialization(work / "routed_netlist.v")
    assert initial == collector.rom_initialization(BASE / "physical_attempt2/routed_netlist.v")
    result["rom_initialization_parameters_unchanged"] = 56 * 80
    final = (work / "final_timing.rpt").read_text()
    assert "Both (Slow and Fast)" in final
    result["sta_coverage_percent"] = float(re.search(r"STA coverage\s+:\s+([\d.]+)%", final).group(1))
    result["synthesis_zeroing_warnings"] = [line for line in (work / "synthesis.log").read_text().splitlines() if "SYN-5025" in line]
    result["routed_db_sha256"] = digest(work / "pr.db")
    result["frozen_files_check"] = json.loads((ROOT / "frozen_check.json").read_text())
    result["implementation_inputs"] = manifest
    result["project_input_sha256"] = digest(work / "project_input.al")
    failed = [row for row in result["timing"]["all_paths"]["negative"] if not row["external"]]
    result["internal_failure_groups"] = {}
    for label, marker in (("pre_round_enable", "u_pre/u_round/"),
                          ("mac_weight", "reg_mac_weight"), ("rom_output_enable", "word_data_o")):
        rows = [row for row in failed if marker in row["end"]]
        result["internal_failure_groups"][label] = {
            "negative_records": len(rows), "unique_failed_endpoints": len({row["end"] for row in rows}),
            "worst_ns": min((row["slack_ns"] for row in rows), default=None)}
    result["candidate_promoted"] = False
    result["decision"] = "内部setup未通过；保留旧基线。下一步涉及冻结核使能/装载路径，需集中批准后另立候选。"
    save(ROOT / "result.json", result)
    summary = result["timing"]["all_paths"]["summary"]
    save(ROOT / "status.json", {"stage": "physical_failed_not_promoted", "resources": result["resources_including_shell"],
         "internal": summary["internal"], "external": summary["external"], "strict_delivery_passed": False,
         "internal_register_report": result["timing"]["internal"]["summary"]["internal"],
         "candidate_promoted": False, "decision": result["decision"],
         "production_modified": False, "bitstream_generated": False})
    print(json.dumps({"resources": result["resources_including_shell"],
        "internal": {kind: {"wns": row["worst"]["slack_ns"] if row["worst"] else None,
                            "failed_endpoints": row["unique_failed_endpoints"]} for kind, row in summary["internal"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "check", "reference", "specification", "gate", "gate_testbench", "simulate", "regression", "ingress", "synthesize", "route", "collect"))
    stage = parser.parse_args().stage
    if stage != "prepare":
        check()
    try:
        if stage in ("simulate", "regression"):
            getattr(base, stage)()
        else:
            globals()[stage]()
    finally:
        if (ROOT / "frozen.json").exists():
            check()
