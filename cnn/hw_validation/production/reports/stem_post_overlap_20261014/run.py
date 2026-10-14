"""Stem任务/后处理重叠；复用现有参考、仿真与报告工具，只输出本目录。"""
import argparse
import csv
import importlib.util
from itertools import islice
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "load_commit_pipeline_20261014"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


previous = load("stem_overlap_previous", SOURCE / "run.py")
weight, rom, helpers = previous.weight, previous.rom, previous.helpers
for module in (previous, previous.bank, weight, rom, helpers):
    module.ROOT = ROOT
sha, save, fresh, command = helpers.sha, helpers.save, helpers.fresh, helpers.command


def check(full=False):
    records = json.loads((ROOT / ("frozen.json" if full else "critical_frozen.json")).read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / ("full_frozen_check.json" if full else "frozen_check.json"), {"checked": len(records), "changed": changed})
    assert not changed, changed
    reused = json.loads((ROOT / "reused_sources.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == value for name, value in reused.items())


for module in (previous, previous.bank, weight, rom, helpers):
    module.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((SOURCE / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((SOURCE / "artifact_manifest.json").read_text(encoding="utf-8")))
    critical = [*SOURCE.joinpath("rtl").glob("*.v"), *helpers.CORE.glob("*.v"),
                SOURCE / "physical_attempt2/pr.db", SOURCE / "physical_attempt2/physical_summary.json",
                SOURCE / "physical/frontend.sdc", SOURCE / "physical/frontend.adc",
                ROOT.parents[4] / "user_source/hdl_source/design_top_wrapper.v"]
    critical = {str(p): sha(p) for p in critical}
    records.update(critical)
    save(ROOT / "frozen.json", records)
    save(ROOT / "critical_frozen.json", critical)
    for folder in ("rtl", "tests", "artifacts", "vectors"):
        shutil.copytree(SOURCE / folder, ROOT / folder, dirs_exist_ok=True)
    shutil.copytree(SOURCE / "rtl", ROOT / "baseline_rtl")
    for name in ("reference.py", "reference_receipt.json", "address_reference.py"):
        shutil.copyfile(SOURCE / name, ROOT / name)
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v") if p.name != "road_stem_tile_scheduler.v"})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_STEM_OVERLAP", "baseline_commit": "52da7fa2",
                               "strict_delivery_ready": False, "arithmetic_interface_ii_changed": False})
    check(full=True)


def review():
    work = fresh("review")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review",
             "--target", ROOT / "rtl/road_stem_tile_scheduler.v", "--report-json", work / "stem.json"],
            work, "stem", allowed=(0, 1, 2))
    check()


def gate():
    work = fresh("gate")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    for folder in ("baseline_rtl", "rtl"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / folder / "road_stem_tile_scheduler.v",
                 "--json", work / (folder + ".json"), "--markdown", work / (folder + ".md")],
                work, folder, allowed=(0, 1, 2))
    check()


def simulate():
    check()
    work = fresh("simulation")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    sources = work / "sources"
    sources.mkdir()
    for folder in ("rtl", "tests"):
        for path in (ROOT / folder).iterdir():
            if path.suffix in (".v", ".vh"):
                shutil.copyfile(path, sources / path.name)
    old = json.loads((SOURCE / "simulation_attempt2/vlog.command.json").read_text(encoding="utf-8"))["command"]
    args = [arg for arg in old if Path(arg).parent != SOURCE / "simulation_attempt2/sources"
            and not str(arg).startswith("+incdir+")]
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([*args, "+incdir+" + sources.as_posix(), *sorted(sources.glob("*.v"))], work, "vlog")
    modes = ("tb_rom_down2", "tb_rom_reader", "tb_parameter_prefetch", "scheduler_storage",
             "normal", "stalls", "control", "counter_prepare")
    results = []
    for mode in modes:
        old_args = json.loads((SOURCE / "simulation_attempt2" / (mode + ".command.json")).read_text(encoding="utf-8"))["command"]
        args = ["+REPORT=" + (work / ("cycles.csv" if mode == "tb_rom_down2" else mode + ".csv")).as_posix()
                if str(arg).startswith("+REPORT=") else
                "+DUMP=" + (work / (mode + "_output.hex")).as_posix() if str(arg).startswith("+DUMP=") else
                "+VECTORS=" + (ROOT / "vectors").as_posix() if str(arg).startswith("+VECTORS=") and mode.startswith("tb_") else
                "+WORDS=" + (ROOT / "vectors/rom_words.hex").as_posix() if str(arg).startswith("+WORDS=") else arg
                for arg in old_args]
        if mode in ("normal", "stalls"):
            vector_dir = Path(next(str(a).split("=", 1)[1] for a in args if str(a).startswith("+VECTORS=")))
            assert all((vector_dir / name).is_file() for name in ("rgb.hex", "stem_acc.hex", "stem_stages.hex")), vector_dir
        output = command(args, work, mode)
        assert "TB_PASS" in output
        if mode in ("normal", "stalls"):
            # down2完全未改；随机反压发生时刻可因Stem结束提前而变，不能要求stalls逐周期相同。
            assert sha(work / (mode + "_output.hex")) == sha(SOURCE / "simulation_attempt2" / (mode + "_output.hex"))
            if mode == "normal":
                assert (work / "normal.csv").read_bytes() == (SOURCE / "simulation_attempt2/normal.csv").read_bytes()
        results.append({"mode": mode, "status": "PASS"})
    save(work / "receipt.json", {"status": "PASS", "results": results,
         "source_hashes": {str(p): sha(p) for p in sources.iterdir()},
         "core_hashes": {str(p): sha(p) for p in helpers.CORE.glob("*.v")},
         "outputs_identical": True, "normal_down2_cycles_identical": True,
         "stalls_cycle_comparison": "Different arrival phase; report both without claiming improvement from this alone"})
    summarize_cycles(work)
    check()


def summarize_cycles(work):
    records = {}
    for mode in ("normal", "stalls"):
        stem = list(csv.DictReader((work / (mode + ".csv.stem.csv")).open(encoding="utf-8")))
        down = list(csv.DictReader((work / (mode + ".csv")).open(encoding="utf-8")))
        assert len(stem) == 2304 and len(down) == 576
        for row in stem:
            assert sum(int(row["bin" + str(i)]) for i in range(8)) == int(row["core"])
            assert all(int(row[k]) == 256 for k in ("acc", "pre", "silu", "post", "commits", "exports"))
        records[mode] = {"stem": {k: sum(int(row[k]) for row in stem) for k in stem[0] if k != "tile"},
                         "down2": {k: sum(int(row[k]) for row in down) for k in down[0] if k != "tile"}}
    baseline_stem = 10911744
    assert records["normal"]["stem"]["core"] < baseline_stem
    save(ROOT / "cycle_summary.json", {"candidate": records, "baseline_normal_stem_core": baseline_stem,
         "baseline_normal_frontend_core": 11883456,
         "normal_stem_saved_cycles": baseline_stem - records["normal"]["stem"]["core"],
         "scope": "3 of 67 convolutions, no complete network/DDR/FPS",
         "mutually_exclusive_bins": ["output_stall", "pp_admission_stall", "commit", "mac_accept",
                                     "prepare_send_other", "mac_wait", "final_pp_drain", "advance_other"]})


def specifications():
    work = fresh("specifications")
    template = SOURCE / "specifications_attempt2/road_stem_tile_scheduler.json"
    contract = json.loads(template.read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["feature"] = "stem_post_overlap"
    module["description"] = "MAC结果被现有PP队列接受后立即推进任务；按独立提交序号校验返回，完整tile排空后发布。"
    module["behavior"].extend(["现有PP保管完整任务tag/参数；本调度器不新增FIFO。",
        "MAC_WAIT接受结果后进入ADVANCE，下一任务不等待前任务PP结果；末任务转POST_WAIT，cnt_written达到256后DONE。",
        "PP提交可与PREPARE/SEND/MAC_WAIT重叠；高8位tag必须0、低8位等于cnt_written，计数256后禁止额外写入。"])
    module["timing_diagrams"] = [{"id": "overlap", "scenario": "overlap", "title": "下一任务与上一任务后处理重叠",
        "description": "已有PP入口接受A后启动B；A按原tag写回，B的当前通道不参与A返回校验。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
            {"name": "task", "wave": "=..=....", "data": ["A", "B"]},
            {"name": "pp_accept_A", "wave": "010....."}, {"name": "mac_task_B", "wave": "0..1...."},
            {"name": "commit_A", "wave": "0...1110"}, {"name": "last_task_drain_done", "wave": "0......1"}]}}]
    path = work / "spec.json"
    save(path, contract)
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
             "--source", ROOT / "rtl/road_stem_tile_scheduler.v", "--out-dir", work, "--no-state"],
            ROOT, str(work.relative_to(ROOT) / "write_spec"))
    bundle = work / "spec/stem_post_overlap"
    shutil.copyfile(bundle / "road_stem_tile_scheduler_spec.md", ROOT / "rtl/road_stem_tile_scheduler_spec.md")
    shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def focused():
    work = fresh("protocol")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    snapshot = work / "tb_stem_overlap_protocol.v"
    shutil.copyfile(ROOT / "tests/tb_stem_overlap_protocol.v", snapshot)
    sources = [*sorted((ROOT / "rtl").glob("*.v")), *sorted(helpers.CORE.glob("*.v")),
               snapshot]
    old = json.loads((SOURCE / "simulation_attempt2/vlog.command.json").read_text(encoding="utf-8"))["command"]
    vendor = [arg for arg in old if "sim_release" in str(arg)]
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([helpers.MSIM / "vlog.exe", "-work", "work", *vendor, *sources], work, "vlog")
    output = command([helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_stem_overlap_protocol",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "protocol")
    assert "TB_PASS_STEM_OVERLAP" in output
    save(work / "receipt.json", {"status": "PASS", "source_hashes": {str(p): sha(p) for p in sources}})
    check()


def tb_specification():
    work = fresh("protocol_specifications")
    contract = json.loads((SOURCE / "test_specification_attempt3/spec.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    name = "tb_stem_overlap_protocol"
    module.update(name=name, rtl_path=name + ".v", feature="stem_overlap_protocol",
                  description="真实共享算术链的重叠、满队列反压、错误tag、末任务故障与五个阶段复位专项。")
    module["behavior"] = ["实际PP pending满8项时阻止新结果准入，保持已出现的输出载荷512拍。",
        "MAC在旧PP结果在途时继续接受；96个batch的256输出按tag0..255完整提交和导出。",
        "分别在MAC/pre/SiLU/post/提交反压位置复位，整表及参数重装后恢复。",
        "强制非法/重复tag与最后任务MAC故障，只作负向验证，不计入加速周期。"]
    module["verification_cases"] = ["TB_PASS_STEM_OVERLAP_PROTOCOL；队列满、380次实际MAC接受重叠、512拍长反压、五个复位点和故障恢复。"]
    module["timing_diagrams"] = [{"id": "stall", "scenario": "stall", "title": "满队列与长反压保持",
        "description": "只在真实握手时推进；恢复ready后完整排空，不能提前done。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......"},
            {"name": "commit_ready", "wave": "10...1."}, {"name": "pp_valid", "wave": "01....."},
            {"name": "pending", "wave": "=.=..=.", "data": ["growing", "8(full)", "draining"]},
            {"name": "done", "wave": "0.....1"}]}}]
    path = work / "spec.json"
    save(path, contract)
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    # 工具对TB的task输入存在已记录的模块端口误识别；按实际单输出契约渲染，ModelSim负责源码验证。
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
             "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / "render"))
    bundle = work / "spec/stem_overlap_protocol"
    shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
    shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)


def profile(baseline=False):
    # 只增加被动观察器；已有完整数值回归不重复执行，首tile逐阶段和导出仍由原TB验证。
    original = SOURCE / "simulation_attempt2" if baseline else sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    work = fresh("profile_baseline" if baseline else "profile")
    shutil.copytree(original / "work", work / "work")
    shutil.copyfile(ROOT / "tests/tb_stem_profile.v", work / "tb_stem_profile.v")
    command([helpers.MSIM / "vlog.exe", "-work", "work", work / "tb_stem_profile.v"], work, "vlog")
    args = json.loads((original / "normal.command.json").read_text(encoding="utf-8"))["command"]
    args.insert(args.index("tb_frontend_shared") + 1, "tb_stem_profile")
    args = ["+REPORT=" + (work / "tile.csv").as_posix() if str(a).startswith("+REPORT=") else
            "+DUMP=" + (work / "tile_output.hex").as_posix() if str(a).startswith("+DUMP=") else a for a in args]
    log = command(args, work, "profile")
    line = next(line for line in log.splitlines() if "TB_PASS_STEM_PROFILE" in line)
    values = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
    save(work / "receipt.json", {"status": "PASS", "cycles": values,
         "observer_sha256": sha(work / "tb_stem_profile.v"), "numeric_receipt_sha256": sha(original / "receipt.json"),
         "scope": "First top-left golden Stem tile; raw stage busy overlaps and is not summed into core cycles"})
    check()


def profile_baseline():
    profile(baseline=True)


def profile_specification():
    work = fresh("profile_specifications")
    contract = json.loads((ROOT / "protocol_specifications/spec.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    name = "tb_stem_profile"
    module.update(name=name, rtl_path=name + ".v", feature="stem_cycle_observer",
                  description="与原黄金值TB共同展开的被动周期观察器，不驱动设计。")
    module["behavior"] = ["只统计原TB首个Stem小块；原逐阶段及导出对拍继续执行。",
        "FSM五类状态计数互斥且相加等于core；pre/SiLU/post忙计数允许重叠，禁止相加代表耗时。",
        "完成256次提交及导出后验证core一致并结束；不测故障退出的加速。"]
    module["corner_cases"] = ["观察器仅用于无停顿首tile；其他位置与反压由完整数值回归覆盖。"]
    module["verification_cases"] = ["TB_PASS_STEM_PROFILE core=1566；五类FSM计数相加1566，commits=256。"]
    module["timing_diagrams"] = [{"id": "overlap", "scenario": "overlap", "title": "计算与后处理重叠计时",
        "description": "一个时钟周期可同时属于MAC状态和PP忙；总耗时只统计一次。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p....."}, {"name": "core_busy", "wave": "01...0"},
            {"name": "mac_task", "wave": "x====x", "data": ["0", "1", "2", "last"]},
            {"name": "pp_busy", "wave": "0.1..0"}, {"name": "export_done", "wave": "0....1"}]}}]
    save(work / "spec.json", contract)
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", work / "spec.json",
             "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / "render"))
    bundle = work / "spec/stem_cycle_observer"
    shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
    shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)


def place():
    check()
    receipt = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    assert json.loads(receipt.read_text(encoding="utf-8"))["status"] == "PASS"
    work = fresh("physical")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    for name in ("frontend.sdc", "frontend.adc"):
        shutil.copyfile(SOURCE / "physical" / name, work / name)
    template = (SOURCE / "physical/project_input.al").read_text(encoding="utf-8")
    template = template.replace((SOURCE / "physical").as_posix(), work.as_posix())
    template = template.replace((SOURCE / "rtl").as_posix(), (ROOT / "rtl").as_posix())
    (work / "road_rom_current_down2_top.al").write_text(template, encoding="utf-8")
    (work / "project_input.al").write_text(template, encoding="utf-8")
    script = (SOURCE / "physical/build.tcl").read_text(encoding="utf-8")
    stop = "export_db before_replication.db"
    script = script[:script.index(stop) + len(stop)] + """
write_verilog placed_netlist.v -implement -top road_rom_current_down2_top
puts "CONTROL_QUERY_BEGIN"
foreach pattern {u_compute/u_pp/u_pre/u_round/i_advance* u_rom/cnt_wait_b_n*} {
 set family [get_nets -hier $pattern]
 if {[llength $family] == 0} {error "Missing control family $pattern"}
 foreach net $family {report_nets $net -connection -pin_display_limit 2000}
}
puts "CONTROL_QUERY_END"
puts "SOURCE_PLACEMENT_DONE"
close_project
exit
"""
    (work / "build.tcl").write_text(script, encoding="utf-8")
    bound = [*(ROOT / "rtl").glob("*.v"), *helpers.CORE.glob("*.v"),
             *[work / name for name in ("frontend.sdc", "frontend.adc", "project_input.al", "build.tcl")]]
    hashes = {str(p): sha(p) for p in bound}
    save(work / "input_manifest.json", hashes)
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PLACEMENT_RUNNING", "directory": str(work),
                               "strict_delivery_ready": False})
    try:
        log = command([rom.TD, "build.tcl"], work, "td_launcher")
        assert "SOURCE_PLACEMENT_DONE" in log
    finally:
        save(work / "input_check_after.json", {"same": all(sha(Path(p)) == v for p, v in hashes.items())})
        check()
    query = log.split("CONTROL_QUERY_BEGIN", 1)[1].split("CONTROL_QUERY_END", 1)[0]
    families = {"ADVANCE": [], "ROM": []}
    for block in query.split("RUN-1001 : Net: ")[1:]:
        name = block.splitlines()[0].strip()
        count = int(re.search(r"Loads\s*\|\s*(\d+)", block).group(1))
        key = "ADVANCE" if name.startswith("u_compute/u_pp/u_pre/u_round/i_advance") else "ROM"
        families[key].append({"net": name, "sinks": count})
    assert all(families.values())
    selected = {key: max(values, key=lambda v: (v["sinks"], v["net"])) for key, values in families.items()}
    save(work / "selected_controls.json", {"families": families, "selected": selected,
                                         "selection": "largest observed branch in each unchanged control family"})


def route(repair=False):
    check()
    original = ROOT / "physical_route" if repair else sorted(ROOT.glob("physical*/selected_controls.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    selection = {"HALO": {"net": "u_compute/u_down2/flag_halo_load_write_dup_5", "sinks": 30}} if repair else json.loads((original / "selected_controls.json").read_text(encoding="utf-8"))["selected"]
    work = fresh("physical_route")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    for name in ("frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(original / name, work / name)
    shutil.copyfile(original / ("pr.db" if repair else "before_replication.db"), work / "source_placed.db")
    project = (original / "project_input.al").read_text(encoding="utf-8").replace(original.as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    (work / "project_input.al").write_text(project, encoding="utf-8")
    reports = (SOURCE / "physical_attempt2/build.tcl").read_text(encoding="utf-8")
    reports = reports[reports.index("report_area -verbose -io_info"):]
    script = """import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
update_timing
"""
    operations = (("HALO", 8),) if repair else (("ADVANCE", 128), ("ROM", 16))
    for label, threshold in operations:
        net = selection[label]["net"]
        script += f'''set target [get_nets -hier {{{net}}}]
if {{[llength $target] != 1}} {{error {{Exact {label} target missing}}}}
puts "{label}_BEFORE_BEGIN"
report_nets $target -connection -pin_display_limit 2000
puts "{label}_BEFORE_END"
write_verilog before_{label.lower()}_clone.v -implement -top road_rom_current_down2_top
'''
        if selection[label]["sinks"] > threshold:
            script += f"phys_opt -force_replication_on_nets {{{net}}} -fanout_threshold {threshold}\n"
    script += """route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_current_down2_top
"""
    patterns = {"ADVANCE": "u_compute/u_pp/u_pre/u_round/i_advance*", "ROM": "u_rom/cnt_wait_b_n*",
                "HALO": "u_compute/u_down2/flag_halo_load_write*"}
    for label, _ in operations:
        script += f'''puts "{label}_AFTER_BEGIN"
report_nets [get_nets -hier {{{patterns[label]}}}] -connection -pin_display_limit 2000
puts "{label}_AFTER_END"
'''
    script += reports
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", script, re.M)
    (work / "build.tcl").write_text(script, encoding="utf-8")
    save(work / "selected_controls.json", selection)
    bound = [*(ROOT / "rtl").glob("*.v"), *helpers.CORE.glob("*.v"),
             *[work / name for name in ("source_placed.db", "frontend.sdc", "frontend.adc", "project_input.al", "build.tcl")]]
    hashes = {str(p): sha(p) for p in bound}
    save(work / "input_manifest.json", hashes)
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_ROUTING_RUNNING", "directory": str(work),
                               "strict_delivery_ready": False})
    try:
        log = command([rom.TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in log and 'finish command "route"' in log
    finally:
        save(work / "input_check_after.json", {"same": all(sha(Path(p)) == v for p, v in hashes.items())})
        check()
    rom.report()


def repair_route():
    # 单次已观察失败控制网的物理修复；不改逻辑、约束或算术源，原失败数据库保留。
    failed = json.loads((ROOT / "diagnosis_initial.json").read_text(encoding="utf-8"))["internal"]
    assert len(failed) == 4 and all(row["check"] == "setup" and "reg_halo_write_" in row["end"] for row in failed)
    route(repair=True)


def finalize():
    check(full=True)
    path = sorted(ROOT.glob("physical_route*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1]
    current = json.loads(path.read_text(encoding="utf-8"))
    baseline = json.loads((SOURCE / "physical_attempt2/physical_summary.json").read_text(encoding="utf-8"))
    for control_check in ROOT.glob("physical_route*/control_replication_check.json"):
        assert json.loads(control_check.read_text(encoding="utf-8"))["status"] == "PASS"
    assert current["resources"]["slice"]["used"] <= 21216
    simulation = json.loads((ROOT / "simulation_attempt2/receipt.json").read_text(encoding="utf-8"))
    assert simulation["status"] == "PASS"
    for name, value in simulation["source_hashes"].items():
        if (ROOT / "rtl" / Path(name).name).exists():
            assert sha(ROOT / "rtl" / Path(name).name) == value, name
    assert all(sha(Path(name)) == value for name, value in simulation["core_hashes"].items())
    for input_check in ROOT.glob("physical*/input_check_after.json"):
        assert json.loads(input_check.read_text(encoding="utf-8"))["same"]
    adopted = current["internal_timing_pass"]
    cycles = json.loads((ROOT / "cycle_summary.json").read_text(encoding="utf-8"))
    normal = cycles["candidate"]["normal"]
    total = normal["stem"]["core"] + normal["down2"]["core"]
    assert total == 4579776
    profile_data = json.loads((ROOT / "profile/receipt.json").read_text(encoding="utf-8"))["cycles"]
    baseline_profile = json.loads((ROOT / "profile_baseline/receipt.json").read_text(encoding="utf-8"))["cycles"]
    assert baseline_profile["core"] == 4736 and baseline_profile["final_drain"] == 3200
    assert all(profile_data[k] == baseline_profile[k] for k in ("prepare", "send", "mac_wait", "advance"))
    save(ROOT / "comparison.json", {"baseline_commit": "52da7fa2", "baseline": baseline, "candidate": current,
        "candidate_adopted_for_next_validation": adopted, "resource_delta": {
            k: current["resources"][k]["used"] - baseline["resources"][k]["used"] for k in ("slice", "dsp", "eram", "io")},
        "baseline_normal_frontend_core": 11883456, "candidate_normal_frontend_core": total,
        "saved_cycles": 11883456 - total, "improvement_percent": (11883456 - total) * 100 / 11883456,
        "stem_raw_fsm_profile": profile_data, "baseline_stem_raw_fsm_profile": baseline_profile,
        "test_parameters_only": True, "production_delivery_ready": False})
    gate_records = {phase: json.loads((ROOT / "gate" / (phase + ".json")).read_text(encoding="utf-8"))
                    for phase in ("baseline_rtl", "rtl")}
    save(ROOT / "strict_summary.json", {"stem": {phase: {key: value[key] for key in
         ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")} for phase, value in gate_records.items()},
         "actual_modelsim": "PASS", "actual_td_complete_internal": adopted, "delivery_ready": False,
         "unchanged_down2_full_gate": "Prior parser/normalization failure retained; no whole-design strict pass claim"})
    graph_path = ROOT.parents[1] / "graph_artifacts/graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    measured = {"stem.conv": normal["stem"]["core"], "down2.dw.conv": normal["down2"]["dw_core"],
                "down2.pw.conv": normal["down2"]["pw_core"]}
    rows = [{"name": n["name"], "input_shape_hwc": n["input_shape_hwc"], "output_shape_hwc": n["output_shape_hwc"],
             "macs": n["macs"], "ideal_24mac_lower_bound": (n["macs"] + 23) // 24,
             "products_per_output": n["kernel"][0] * n["kernel"][1] * n["input_shape_hwc"][2] // n["groups"],
             "measured_normal_core": measured.get(n["name"]), "measured": n["name"] in measured}
            for n in graph["nodes"] if n["op"] == "conv"]
    assert len(rows) == 67 and sum(r["measured"] for r in rows) == 3
    assert max(r["products_per_output"] for r in rows) == 192
    save(ROOT / "layer_cycle_ledger.json", {"graph_sha256": sha(graph_path), "clock_mhz": 100,
         "frame_budget_5fps": 20000000, "measured_3conv_core": total, "remaining_budget_before_64conv_and_other": 20000000 - total,
         "layers": rows, "limits": "MAC lower bounds are not scheduled cycles; other 64 layers, DDR, non-conv and NMS unmeasured"})
    save(ROOT / "status.json", {"status": "INTERNAL_PASS_STRICT_EXTERNAL_OPEN" if adopted else "TIMING_FAILED_BASELINE_RETAINED",
         "candidate_adopted_for_next_validation": adopted, "functional_pass": True,
         "normal_frontend_core": total, "internal_failed_endpoints": len(current["internal_failed_endpoints"]),
         "strict_delivery_ready": False, "no_training_production_bitstream_board_flash": True})
    internal = current["reports"]["internal_all_checks"]["checks"]
    table = "\n".join(f"  {key}: {baseline['resources'][key]['used']} → {current['resources'][key]['used']}" for key in ("slice", "dsp", "eram", "io"))
    timing = "\n".join(f"  {key}: {value['worst_slack_ns']:+.3f} ns ({value['reported_paths']} paths)" for key, value in internal.items())
    with (path.parent / "internal_all_checks.timing").open(encoding="utf-8") as stream:
        first_path = "".join(islice(stream, 110))
    critical = "\n".join(line for line in first_path.splitlines() if re.match(
        r"^(Slack|Begin Point|End Point|Check Type|Process|Data Path Delay|Max Fanout)\s*:", line))
    area_text = (path.parent / "frontend_route.area").read_text(encoding="utf-8")
    plb = re.search(r"#plb\s+(\d+)\s+out of\s+(\d+)\s+(\S+)", area_text).groups()
    tool_diagnostics = {}
    for label, directory in (("baseline", SOURCE / "physical_attempt2"), ("candidate", path.parent)):
        value = (directory / "check_timing_verbose.rpt").read_text(encoding="utf-8")
        tool_diagnostics[label] = {"check_table": value.split("1. checking nets", 1)[0],
            "dsp_dummy_pins": sorted(re.findall(r"^\s+(u_compute/\S+\.(?:mul9_mode|mul9_signed))\s*$", value, re.M))}
    tool_diagnostics["dsp_dummy_pins_unchanged"] = tool_diagnostics["baseline"]["dsp_dummy_pins"] == tool_diagnostics["candidate"]["dsp_dummy_pins"]
    save(ROOT / "tool_diagnostics.json", tool_diagnostics)
    failures = "\n".join(f"  {key}: {value}" for key, value in current["all_failed_scope_counts"].items())
    text = f"""RoadYOLO Stem计算/后处理重叠阶段报告（2026-10-14—15）

一、结论和未通过项
功能通过；完整内部时序通过={adopted}，内部失败端点={len(current['internal_failed_endpoints'])}。
外部窄口/原始复位入口未签核，严格交付门未闭合，不等于整机通过。
仅固定测试参数；真实QAT、其余64卷积、完整DDR、后处理和板测尚不在本次证据范围。
回退版本52da7fa2及全部旧报告保持；full_frozen_check.json核对3400个旧文件，变化为0。

二、实际修改
只修改rtl/road_stem_tile_scheduler.v：MAC结果被现有PP队列接受即推进下一任务，最后任务才等待256项提交齐全。
当前发射位置不再用于校验旧返回；返回使用独立提交计数验证连续tag、int8符号扩展和输出类型。
复用PP既有2项入口和8项退休队列，不新增FIFO；算术核、接口、数值、MAC II和复位契约不变。
逐拍接口见逐拍方案.txt及rtl/road_stem_tile_scheduler_spec.md。

三、同向量实测周期（无反压、相同测量窗口）
Stem tile：4736 → 1566，减少66.93%。Stem整层：10911744 → 3608064。
down2 DW：630720，PW：340992，合计971712，完全未改。
前三卷积核心：11883456 → {total}，减少61.46%，省7303680拍。
原TB端点：14022597 → 6718917；含装载/导出及TB控制，不等于核心周期。
反压TB端点：17992384 → 8471654；到达相位随Stem变更，单独报告，不用其比例宣称核心加速。
5 FPS的20000000拍预算中，前三卷积核心占22.90%；剩15420224拍尚要承担64层及其他全部开销。
layer_cycle_ledger.json列出67层：仅3层有实测，其余明确未知；不从旧版整网估算直接减本次差值。

四、每tile周期来源
真实FSM互斥统计：准备384、送入384、MAC等待672、推进96、最终排空30，合计1566。
原串行后处理等待状态3200拍变为末尾30拍；其他四类状态未变，因此净省3170拍。
另按停顿原因优先分类：输出反压0、PP准入反压0、提交256、MAC接受384、准备/送入其余306、MAC等待其余578、末排空其余25、推进其余17。
两种互斥分类各自相加1566，不能横跨分类相加。
pre忙1216、SiLU忙736、post忙1216，彼此重叠，不能加成总周期；1521拍存在计算状态与PP在途重叠。
长反压专项另证实：8项pending满队列、512拍载荷保持、旧PP在途时380次MAC输入接受。
无停顿下未出现PP准入等待；剩余瓶颈在准备/MAC任务周转，不再是逐任务等待PP完成。

五、功能与协议证据
simulation_attempt2/receipt.json：原8组回归全通过，2304个Stem及576个down2 tile，全量阶段/导出对拍，输出哈希与旧版一致。
protocol_attempt2/receipt.json：256提交/导出、满队列、长反压、5个流水位置复位、2类tag故障、末任务MAC故障及恢复通过。
profile/receipt.json及profile_baseline/receipt.json：新旧黄金值TB上只加同一被动观察器，core计数与FSM和相符。
首次simulation/因封装脚本把完整帧向量误指向小tile目录而超时；保留失败日志，修正路径并加入文件预检后重跑，不归为RTL数值失败。
TB规格按已确认实际单输出渲染；工具的task参数误识别问题保留，实际编译执行由ModelSim验证。

六、实际物理结果（包含验证壳与ROM，不含视频模板）
器件PH1P35MDG324-3，100 MHz，I/O50，自动引脚及零诊断延迟，不可直接上板。
{table}
PLB实际{plb[0]}/{plb[1]}（{plb[2]}），虽Slice未满，布局余量已较紧；不能把本壳资源直接当作与视频模板融合后的资源。
内部reg-reg及功能复位检查：
{timing}
该报告首条setup关键路径：
{critical}
完整内部失败集合同时联合RAM/DSP到达及发出端点报告；最终采用目录：{path.parent.name}/physical_summary.json。
56块ROM、4480项INIT内容与冻结包一致；共享MAC/PP/SiLU各1实例。
综合仍保留SYN-5025“未驱动端点置零”总告警，工具该条没有列出逐针对象；本次不宣称该告警已经闭合。
动态输入和偏置的功能证据来自完整黄金值回归，物理保留证据来自实际网表/资源/ROM核对；不能拿两者代替全网表等价证明。
沿用已批准物理扇出修复：从实际新网表查询已知控制族，选782负载advance分支与33负载ROM分支，不写死旧dup后缀。
函数与负载集合由check_physical_controls.py核对；不新增时序例外。
首次布线出现4个halo装载地址/数据寄存器CE setup违例，最差-0.363ns，最差路径net延迟占84%；失败physical_route数据库和报告保留。
只追加一次物理候选：从首次pr.db对30负载flag_halo_load_write_dup_5按8负载目标进行局部原生复制并重新布线；不修改RTL。
全端点仍失败项：
{failures}
这些外部入口不能靠编造输入延迟或全局false path消除；保留真实外设契约未决状态。
全部适用角点、覆盖率、忽略路径、未约束/异常对象详见原始timing/rpt报告，不以摘要代替签核。
check_timing仍报告clock definition(1)及dummy node(2)两类历史告警；60个DSP mul9_mode/mul9_signed对象与基线逐项一致，但未据此豁免。
未驱动时钟、无路径约束、组合环及非法约束计数均为0；零诊断I/O延迟被约束不等于真实板级延迟已确定。
内部setup仅+0.022ns，余量很薄：作为下一阶段诊断基线，不作为有充分裕量的生产实现。

七、严格门与下一步
Stem严格诊断596 → 585，compile通过，其余严格检查仍未闭合；不是修复11个功能bug。
格式、注释、命名与语义规则均保留在gate/和strict_summary.json；未改动模块原失败状态沿用。
下一步以本候选内部时序{'通过版本继续' if adopted else '失败为停止条件，保持旧版本继续可独立参考工作'}，转向冻结图真实PW24/48/96与DW块的调度及周期覆盖，先填完层周期账本，不继续孤立微调Stem或先缩网。
优先参考层head2.cls_pw.conv与head2.reg_pw.conv：均48→48、128×72，每层21233664 MAC；再覆盖96→48与192→96融合PW。
冻结图全卷积每输出归约最长192项，没有推广现有合法上限；该检查不是其余64层RTL验证。
最值得单变量评估的是准备/任务周转开销；若要改算术接口或II，仍须单独决定。
真实量化参数未接入前，测试系数通过不代表模型部署；不宣称整网5FPS、识别精度或整机资源通过。
"""
    (ROOT / "阶段对比报告.txt").write_text(text, encoding="utf-8")
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*")
         if p.is_file() and p.name != "artifact_manifest.json" and "work" not in p.relative_to(ROOT).parts
         and p.suffix in (".py", ".v", ".vh", ".json", ".md", ".txt", ".tcl", ".sdc", ".adc", ".svg", ".json5", ".timing", ".rpt", ".log", ".area", ".qor", ".hex", ".csv", ".al", ".bin", ".mem", ".mif")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "review", "gate", "simulate", "specifications", "focused", "tb_specification", "profile", "profile_baseline", "profile_specification", "place", "route", "repair_route", "finalize"))
    globals()[parser.parse_args().action]()
