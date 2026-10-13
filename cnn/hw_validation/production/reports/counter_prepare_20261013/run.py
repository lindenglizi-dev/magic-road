"""局部计数准备寄存器候选；复用原仿真/门禁，所有输出限制在本目录。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "parameter_prefetch_20261013"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load("counter_prefetch_runner", BASE / "run.py")
table = prior.prior
shared = table.shared
prior.ROOT = table.ROOT = shared.ROOT = shared.helpers.ROOT = ROOT
table.TOP = ROOT / "rtl/road_frontend_shared_core.v"
prior.STEM = table.STEM = shared.STEM = ROOT / "rtl/road_stem_tile_scheduler.v"
save, sha, fresh, command = table.save, table.sha, table.fresh, table.command
check = table.check


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    for folder in (BASE, ROOT.parent / "placement_seed_20261013"):
        records.update(json.loads((folder / "artifact_manifest.json").read_text(encoding="utf-8")))
        for name in ("frozen.json", "artifact_manifest.json", "run.py"):
            records[str(folder / name)] = sha(folder / name)
    save(ROOT / "frozen.json", records)
    for name in ("rtl", "tests"):
        (ROOT / name).mkdir()
        for path in (BASE / name).iterdir():
            if path.suffix in (".v", ".vh"):
                shutil.copyfile(path, ROOT / name / path.name)
    save(ROOT / "baseline_sources.json", {str(path.relative_to(ROOT)): sha(path)
         for name in ("rtl", "tests") for path in (ROOT / name).iterdir()})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_COUNTER_REPAIR", "baseline_commit": "46083305"})
    check()


def baseline_gate():
    check()
    work = fresh("baseline_gate")
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / "rtl",
             "--external-interface-source", shared.helpers.CORE,
             "--json", work / "rtl.json", "--markdown", work / "rtl.md"],
            work, "rtl", allowed=(0, 1, 2))
    result = json.loads((work / "rtl.json").read_text(encoding="utf-8"))
    assert result["checks"]["compile"]["status"] == "passed"
    check()


def reference():
    check()
    result = load("counter_reference", ROOT / "reference.py").self_check()
    save(ROOT / "reference_receipt.json", {**result, "sha256": sha(ROOT / "reference.py")})
    assert result["status"] == "PASS"
    check()


def dependency():
    check()
    paths = json.loads((BASE / "dependency.json").read_text(encoding="utf-8"))["paths"]
    paths["reference"] = str(ROOT / "reference.py")
    assert all(Path(path).is_file() for path in paths.values())
    save(ROOT / "dependency.json", {"status": "PASS", "paths": paths,
         "hashes": {name: sha(Path(path)) for name, path in paths.items()}})
    work = fresh("dependency_check")
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "check"], work, "renderer")
    check()


def specifications():
    check()
    work = fresh("specifications")
    contract = json.loads((BASE / "specifications/road_down2_tile_scheduler.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["feature"] = "counter_prepare"
    module["description"] = "每拍提前准备最后组后的5位输出计数；原接受沿提交，接口和周期不变。"
    module["behavior"].extend([
        "准备寄存器每拍计算：DW小于15加一否则0；PW小于7加一，否则非最后位置清0、最后位置保持。",
        "每个合法last接受前至少已有一拍当前layer/position/output稳定，PW group0提供最短准备窗口。",
        "cnt_output仅在原last接受沿提交准备值，IDLE/start及DW_DRAIN清零、PP/load故障保持优先级不变。",
        "异步复位同时清零准备寄存器；算术、元数据、端口、II和外部延迟不变。"])
    module["verification_cases"].append("Python可达状态转移枚举、RTL准备值不变量/原递推逐拍检查、原完整回归及全量周期比较。")
    module["timing_diagrams"] = [{"id": "prepared_counter", "title": "PW两组连续接受与准备值",
        "scenario": "prepared_counter", "description": "每个上升沿前的值；group0接受沿刷新准备值，group1接受沿提交；反压保持原计数。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
            {"name": "group", "wave": "========", "data": ["0", "1", "0", "1", "0", "1", "0", "1"]},
            {"name": "accept", "wave": "1......."},
            {"name": "cnt_output", "wave": "=.=.=.=.", "data": ["k", "k+1", "k+2", "k+3"]},
            {"name": "prepared", "wave": "x=.=.=.=", "data": ["k+1", "k+2", "k+3", "k+4"]}]}}]
    path = work / "road_down2_tile_scheduler.json"
    save(path, contract)
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
             "--source", ROOT / "rtl/road_down2_tile_scheduler.v", "--out-dir", work, "--no-state"], ROOT,
            str(work.relative_to(ROOT) / "write_spec"))
    bundle = work / "spec/counter_prepare"
    shutil.copyfile(bundle / "road_down2_tile_scheduler_spec.md", ROOT / "rtl/road_down2_tile_scheduler_spec.md")
    shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms")
    check()


def simulate():
    prior.simulate()
    work = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    output = command([shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_counter_prepare",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "counter_prepare")
    assert "TB_PASS_COUNTER_PREPARE" in output
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    receipt["extra_results"].append({"top": "tb_counter_prepare", "status": "PASS"})
    save(work / "receipt.json", receipt)
    cycles = table._cycles(work / "receipt.json")
    old = json.loads((BASE / "cycle_summary.json").read_text(encoding="utf-8"))["candidate"]
    save(ROOT / "cycle_summary.json", {"candidate": cycles, "frozen_baseline": old, "identical": cycles == old})
    assert cycles == old, "Same vectors must retain every cycle/event/bin count"
    check()


def test_specifications():
    check()
    work = fresh("test_specifications")
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    monitor_ports = {"clk": 1, "rstn": 1, "state": 4, "layer_pw": 1, "position": 4,
        "count": 5, "prepared": 5, "accept": 1, "last_group": 1, "start_accept": 1,
        "dw_writes": 9, "pp_fault": 1, "load_fault": 1}
    for filename in ("tb_counter_prepare", "tb_frontend_shared", "tb_shared_core_control"):
        modules = []
        for name in (["counter_prepared_check", filename] if filename == "tb_counter_prepare" else [filename]):
            ports = monitor_ports if name == "counter_prepared_check" else {}
            modules.append({"name": name, "feature": "counter_verification", "rtl_path": filename + ".v",
                "description": "独立验证观察器或测试平台；不参与综合及生产数据路径。",
                "interfaces": {"protocol": "discrete", "ports": [{"name": port, "direction": "input",
                    "width": width, "clock_domain": "clk", "role": port,
                    "description": "只读观察被测调度器沿前状态或驱动测试时钟复位。"} for port, width in ports.items()]},
                "parameters": [], "clock": {"name": "clk", "edge": "posedge", "frequency_hz": 100000000},
                "reset": {"name": "rstn", "active": "low", "synchronous": False,
                          "values": "观察count/prepared立即清零；测试平台控制恢复与合法重新装载。"},
                "behavior": ["沿前按旧递推计算expected，沿后1ns检查count；合法末组接受时检查准备值。",
                             "全量顶层保持原向量和RNG，normal/stalls各要求147456次合法末组接受。",
                             "定向计数测试包含force原语，属于递推/优先级/复位分支测试，不代替合法完整事务。"],
                "constraints": ["仅仿真，不可综合；不证明亚稳态、物理时序或整网FPS。"],
                "corner_cases": ["PW连续两组、DW回绕、PW最终保持、长停顿、故障保持、异步复位、旧直接清零分支。"],
                "verification_cases": ["原完整顶层normal/stalls/control；1024个定向计数变体和7组明确复位身份。"],
                "timing_diagrams": [{"id": "edge_check", "title": "计数沿前预测与沿后检查", "scenario": "edge_check",
                    "description": "图示两个接受沿；实际观察器在每个上升沿后1ns逐项检查。",
                    "wavejson": {"signal": [{"name": "clk", "wave": "p....."},
                        {"name": "last_accept", "wave": "01010."},
                        {"name": "count", "wave": "=.=.=.", "data": ["k", "k+1", "k+2"]}]}}]})
        contract = work / (filename + ".json")
        save(contract, {"modules": modules})
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
            "--source", ROOT / "tests" / (filename + ".v"), "--out-dir", work, "--no-state"], ROOT,
            str(work.relative_to(ROOT) / filename))
    bundle = work / "spec/counter_verification"
    for path in bundle.glob("*_spec.md"):
        shutil.copyfile(path, ROOT / "tests" / path.name)
    shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms")
    check()


def physical():
    check()
    receipt_path = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS" and any(p["top"] == "tb_counter_prepare" for p in receipt["extra_results"])
    tested = {Path(name).name: digest for name, digest in receipt["source_hashes"].items()}
    assert all(tested[p.name] == sha(p) for p in (ROOT / "rtl").glob("*.v"))
    assert json.loads((ROOT / "cycle_summary.json").read_text(encoding="utf-8"))["identical"]
    work = fresh("physical")
    for name in ("frontend.sdc", "frontend.adc", "build.tcl"):
        shutil.copyfile(BASE / "physical" / name, work / name)
    project = (BASE / "physical/road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace((BASE / "physical").as_posix(), work.as_posix())
    assert BASE.as_posix() not in project
    (work / "road_frontend_shared_core.al").write_text(project, encoding="utf-8")
    manifest = json.loads((BASE / "physical/source_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        item["sha256"] = sha((work / item["path"]).resolve())
    manifest["execution_authorization"] = "Isolated cycle-exact counter preparation, unchanged core/II/ports, no bitstream"
    save(work / "source_manifest.json", manifest)
    parser = load("counter_preflight", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    parser.ROOT, parser.CANDIDATE, parser.MANIFEST = work, ROOT, work / "source_manifest.json"
    assert parser.preflight() == 0
    before = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
    save(work / "source_check_before.json", before)
    save(work / "tool_hash.json", {str(table.TOOL): sha(table.TOOL), "build.tcl": sha(work / "build.tcl")})
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_TD_RUNNING", "cycles_identical": True})
    try:
        output = command([table.TOOL, "build.tcl"], work, "td_launcher")
        assert 'finish command "route"' in output and "REPORT_COMPLETION_DONE" in output
    finally:
        after = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
        save(work / "source_check_after.json", after)
        assert after == before
        check()
    report()


def report():
    work = sorted(ROOT.glob("physical*/pr.db"), key=lambda p: p.stat().st_mtime)[-1].parent
    parser = load("counter_physical_report", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    parser.ROOT, parser.CANDIDATE, parser.MANIFEST = work, ROOT, work / "source_manifest.json"
    parser.PREVIOUS = ROOT.parent / "stem_weight_address_20261011"
    assert parser.summarize() in (0, 1)
    current = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    old = json.loads((BASE / "physical/physical_summary.json").read_text(encoding="utf-8"))
    save(ROOT / "comparison.json", {"baseline": str(BASE), "old": old, "new": current,
         "constraints_and_build_identical": all(sha(work / name) == sha(BASE / "physical" / name)
         for name in ("frontend.sdc", "frontend.adc", "build.tcl"))})
    save(ROOT / "status.json", {"status": current["status"], "internal_timing_pass": current["internal_timing_pass"],
         "cycles_identical": True, "coefficients": "TEST_ONLY", "not_deployment": True})
    check()


def internal_memory_reports():
    check()
    physical = ROOT / "physical"
    work = fresh("internal_memory_timing")
    parser = load("counter_memory_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    memories = parser.ram_source_lines(physical / "frontend_route_ram.rpt")
    assert memories and all("{" not in name and "}" not in name for name in memories)
    names = " ".join("{" + name + "}" for name in memories)
    build = ("import_device ph1_35p.db -package PH1P35MDG324 -speed 3\n"
        "import_db ../physical/pr.db\nupdate_timing -mode final\n"
        "set regs [get_regs -hier *]\n"
        "set dsps [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]\n"
        f"set memories [get_cells -hier [list {names}]]\n"
        f"if {{[llength $memories] != {len(memories)}}} {{error {{RAM object count mismatch}}}}\n"
        "set dsp_inputs [get_pins -of $dsps -filter {DIRECTION == input} *]\n"
        "set dsp_outputs [get_pins -of $dsps -filter {DIRECTION == output} *]\n"
        "set memory_inputs [get_pins -of $memories -filter {DIRECTION == input} *]\n"
        "set memory_outputs [get_pins -of $memories -filter {DIRECTION == output} *]\n"
        "set internal_sources [concat $regs $dsp_outputs $memory_outputs]\n"
        "puts \"INTERNAL_MEMORY_OBJECTS regs=[llength $regs] dsps=[llength $dsps] memories=[llength $memories] sources=[llength $internal_sources]\"\n"
        "report_timing_path -from $internal_sources -to $memory_inputs -ep_num 100000 -path_num 1 -file internal_to_memory.timing\n"
        "report_timing_path -from $internal_sources -to $dsp_inputs -ep_num 100000 -path_num 1 -file internal_to_dsp.timing\n"
        "report_timing_path -from $memory_outputs -to $regs -ep_num 100000 -path_num 1 -file memory_to_registers.timing\n"
        "report_timing_path -from $dsp_outputs -to $regs -ep_num 100000 -path_num 1 -file dsp_to_registers.timing\n"
        "puts {INTERNAL_MEMORY_REPORTS_DONE}\nexit\n")
    (work / "build.tcl").write_text(build, encoding="utf-8")
    before = sha(physical / "pr.db")
    output = command([table.TOOL, "build.tcl"], work, "td_launcher")
    assert "INTERNAL_MEMORY_REPORTS_DONE" in output
    result = {"database_sha256": before, "memory_objects": len(memories), "reports": {}}
    negatives = []
    for name in ("internal_to_memory", "internal_to_dsp", "memory_to_registers", "dsp_to_registers"):
        stats, found = parser.read_timing(work / (name + ".timing"), keep_negative=True)
        result["reports"][name] = stats
        negatives.extend(found)
    assert sha(physical / "pr.db") == before
    result["failed_endpoints"] = negatives
    result["status"] = "FAIL" if negatives else "PASS_INTERNAL_MEMORY_DSP_DIAGNOSTIC"
    save(work / "summary.json", result)
    check()


def summarize():
    check()
    work = sorted(ROOT.glob("gate*/rtl.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    save(ROOT / "strict_summary.json", {name: {key: value for key, value in
         json.loads((work / (name + ".json")).read_text(encoding="utf-8")).items()
         if key in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
         for name in ("rtl", "tests")})
    selected = {}
    record = {}
    with (ROOT / "physical/internal_all_checks.timing").open(encoding="utf-8") as stream:
        for line in stream:
            slack = re.match(r"Slack\s*:\s*(-?[\d.]+)ns", line)
            end = re.match(r"End Point\s*:\s*(\S+)", line)
            if slack:
                record = {"slack_ns": float(slack[1])}
            elif end:
                record["end"] = end[1]
            elif line.startswith("Check Type") and "setup" in line and "end" in record:
                endpoint = record["end"]
                family = ("output_counter" if endpoint.startswith("u_down2/cnt_output") else
                          "prepared_counter" if endpoint.startswith("u_down2/reg_cnt_output_prepared") else
                          "parameter_bank" if endpoint.startswith("u_down2/reg_task_parameters") else None)
                if family and (family not in selected or record["slack_ns"] < selected[family]["slack_ns"]):
                    selected[family] = dict(record)
    assert set(selected) == {"output_counter", "prepared_counter", "parameter_bank"}
    save(ROOT / "target_path_summary.json", selected)
    supplement = json.loads((ROOT / "internal_memory_timing/summary.json").read_text(encoding="utf-8"))
    assert supplement["status"] == "PASS_INTERNAL_MEMORY_DSP_DIAGNOSTIC"
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    status["internal_memory_dsp_timing"] = supplement["status"]
    status["decision"] = "ACCEPT_COUNTER_PREPARATION_AS_NEXT_DIAGNOSTIC_BASELINE"
    status["strict_delivery_ready"] = False
    status["testbench_spec_writer"] = "Zero-port testbench unsupported; failed attempt retained; companion documents supplied separately"
    save(ROOT / "status.json", status)
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in sorted(ROOT.rglob("*"))
         if path.is_file() and path.name != "artifact_manifest.json" and path.suffix not in (".wlf", ".pyc")
         and "work" not in path.relative_to(ROOT).parts})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "baseline_gate", "reference", "dependency",
        "specifications", "test_specifications", "gate", "simulate", "physical", "report", "internal_memory_reports", "summarize"))
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    action = cli.parse_args().action
    (table.gate if action == "gate" else globals()[action])()
