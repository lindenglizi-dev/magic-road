"""固定PW48小块的本地对拍与隔离实现；复用工具，不写旧目录。"""
import argparse
from collections import Counter
import csv
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "stem_post_overlap_20261014"
CORE = ROOT.parent / "board_selftest_20261010/core"
REPO = ROOT.parents[4]
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
CORE_NAMES = ("road_mac_probe.v", "road_dynamic_postprocess.v", "road_dynamic_requant.v", "road_round_shift.v", "silu_shared_unit.v")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


helpers = load("pw48_existing_helpers", ROOT.parent / "down2_full_tensor_20261010/run.py")
helpers.ROOT = ROOT
sha, save, fresh, command = helpers.sha, helpers.save, helpers.fresh, helpers.command


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [p for p, value in frozen.items() if sha(Path(p)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def setup():
    assert not (ROOT / "frozen.json").exists()
    paths = [*SOURCE.joinpath("rtl").glob("*.v"), *[CORE / name for name in CORE_NAMES],
        SOURCE / "artifact_manifest.json", SOURCE / "physical_route_attempt2/pr.db", SOURCE / "status.json",
        SOURCE / "physical_route_attempt2/physical_summary.json", SOURCE / "simulation_attempt2/receipt.json",
        REPO / "cnn/integer.py", REPO / "cnn/hw_validation/production/graph_artifacts/graph.json",
        REPO / "cnn/hw_validation/production/deployment_contract.json", REPO / "user_source/hdl_source/design_top_wrapper.v",
        SOURCE / "artifacts/manifest.json", SOURCE / "artifacts/numeric_test.bin"]
    save(ROOT / "frozen.json", {str(p): sha(p) for p in paths})
    save(ROOT / "status.json", {"status": "REFERENCE_PASS_RTL_CANDIDATE", "baseline_commit": "2e872d9c",
        "arithmetic_interface_numeric_ii_changed": False, "production_delivery_ready": False})
    check()


def entry(module):
    return f"import sys;sys.path.insert(0,{str(SKILL)!r});from {module} import main;raise SystemExit(main())"


def dependency():
    work = fresh("dependency")
    paths = [TD, helpers.MSIM / "vlog.exe", helpers.MSIM / "vsim.exe", SKILL / "SKILL.md",
             Path("C:/Users/lenovo/.codex/skills/erie-remote-ssh/SKILL.md")]
    assert all(p.is_file() for p in paths)
    save(work / "paths.json", {str(p): sha(p) for p in paths})
    command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.toolchain.wavedrom_runtime"), "check"], work, "renderer")
    check()


def specifications():
    work = fresh("specifications")
    template = json.loads((SOURCE / "specifications/spec.json").read_text(encoding="utf-8"))
    scheduler = template["modules"][0]
    scheduler.update(name="road_pw_tile_scheduler", rtl_path="road_pw_tile_scheduler.v", feature="pw_fixed_tile",
        description="固定48→48 PW，8激活bank/24权重bank；六组预取，已有PP接受任务后继续计算。")
    for p in scheduler["interfaces"]["ports"]:
        if p["name"] == "i_load_addr": p["width"] = 12
        if p["name"] == "o_output_index": p["width"] = 10
        p["description"] = p["description"].replace("Stem", "PW48").replace("27", "48").replace("255", "767")
        descriptions = {"i_load_kind": "0 signed输入、2权重、3bias、4premul、5shift、6post；1/7非法。",
            "i_load_addr": "各类严格连续的逻辑标量地址；输入0..767，权重0..2303，通道参数0..47。",
            "i_load_data": "signed INT8以32位符号扩展承载；bias为signed32，其余范围见执行契约。",
            "o_mac_last": "当前归约组5；六组共48个有效乘积。", "o_mac_mask": "固定8'hff，48输入没有尾lane。",
            "o_pp_mask": "固定3'b111，48输出没有尾通道。", "o_pp_tags": "三路完整tag=position×48+channel，范围0..767。",
            "o_output_index": "HWC真实缓存读索引0..767，只在输出握手后推进。"}
        if p["name"] in descriptions: p["description"] = descriptions[p["name"]]
    scheduler["constraints"] = ["仅固定48→48、1×1、4×4；不支持任意形状，不改变当前核端口、II或数值。",
        "测试参数不是训练权重；资源/时序只对应实际验证顶层，不代表整机。"]
    scheduler["behavior"] = ["16位置×16输出组，256任务，各6组/48项，MAC first只加一次bias，内部signed33末组检查INT32。",
        "输入HWC768字节，权重OIHW2304字节；装载游标只做bank重排，不改变包；每bank96项。",
        "类别0 signed激活、2权重、3bias、4premul、5shift、6post；完整六类及1024表后才能启动。",
        "首组PREPARE；SEND接受g同沿保管g+1，反压保持当前组；MAC与PP端口、数值和II不变。",
        "已有PP接受结果后推进下一任务；按独立tag0..767提交，768项齐全才done，真实缓存导出完才可复用。",
        "reset立即取消事务和装载完整性；非法记录、溢出及错误返回禁止发布。"]
    scheduler["corner_cases"] = ["7/8、47/48、767/768、2303/2304、地址零重装、INT32边界、末组故障、反压及复位。"]
    scheduler["verification_cases"] = ["四组黄金向量全阶段对拍、连续六组、随机/长反压、满队列、复位取消和窄口实际导出。"]
    scheduler["timing_diagrams"] = [{"id": "prefetch", "scenario": "prefetch", "title": "六组归约与后处理重叠",
        "description": "只在接受沿保管下一组；末组结果被PP接受后推进下一任务，不等待旧PP全部输出。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p........."}, {"name": "mac_valid", "wave": "01.....0.."},
            {"name": "group", "wave": "x======x..", "data": ["0", "1", "2", "3", "4", "5"]},
            {"name": "pp_accept", "wave": "0.......10"}, {"name": "next_task", "wave": "0........1"}]}}]
    top = json.loads(json.dumps(scheduler))
    top.update(name="road_pw_validation_top", rtl_path="road_pw_validation_top.v", description="42位诊断窄口；动态装载全部操作数及表，不含ROM/视频。")
    ports = [("i_clk", "input", 1), ("i_rstn", "input", 1), ("i_rx_valid", "input", 1),
        ("i_rx_data", "input", 16), ("o_rx_ready", "output", 1), ("o_tx_valid", "output", 1),
        ("o_tx_data", "output", 16), ("i_tx_ready", "input", 1), ("o_busy", "output", 1),
        ("o_done", "output", 1), ("o_fault", "output", 1), ("o_parameters_ready", "output", 1)]
    top["interfaces"]["ports"] = [{"name": n, "direction": d, "width": w, "clock_domain": "i_clk",
        "role": "diagnostic", "description": "窄口同步诊断信号；语义见执行契约。"} for n, d, w in ports]
    assert sum(w for _, _, w in ports) == 42
    top["behavior"] = ["16位header/low/high组成完整装载；部分包内的控制字是数据，不能启动。",
        "8000后接1024表项；8001启动；8002逐项导出index/data及F000；8003快照core低/高16；8004/8005控制commit。",
        "异步断言两级同步释放，最早第三上升沿接受。复位后全部重装，未导出缓存不能被装载覆盖。",
        "TX等待ready保持字，实际缓存只在数据字接受后推进；无checksum替代逐项值。"]
    top["timing_diagrams"] = [{"id": "packet", "scenario": "packet", "title": "完整窄口装载后提交",
        "description": "header/low/high先缓存，下一拍向调度器提出完整32位记录，等待ready时保持。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p......"}, {"name": "rx_valid", "wave": "01110.."},
            {"name": "rx_word", "wave": "x===x..", "data": ["header", "low", "high"]},
            {"name": "load_valid", "wave": "0...10."}, {"name": "load_accept", "wave": "0...10."}]}}]
    for module in (scheduler, top):
        path = work / (module["name"] + ".json")
        save(path, {"modules": [module]})
        command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.workflow.cli"), "write-spec",
                 "--spec", path, "--source", ROOT / "rtl" / module["rtl_path"], "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / module["name"]))
        bundle = work / "spec/pw_fixed_tile"
        shutil.copyfile(bundle / (module["name"] + "_spec.md"), ROOT / "rtl" / (module["name"] + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def tb_specifications():
    work = fresh("test_specifications")
    template = json.loads((SOURCE / "protocol_specifications/spec.json").read_text(encoding="utf-8"))
    for name in ("tb_pw_tile", "tb_pw_narrow"):
        module = json.loads(json.dumps(template["modules"][0]))
        module.update(name=name, rtl_path=name + ".v", feature="pw_testbench", description="PW48数值/协议实测，不代表模型精度或整网FPS。")
        module["behavior"] = ["四组向量对拍实际MAC/pre/SiLU/post/提交及输出；互斥状态统计与端点周期相等。",
            "随机/512拍反压、完整性、复位、最终故障；窄口逐字导出并覆盖done同拍export。"]
        module["corner_cases"] = ["16位置、48通道、768写回、六组归约、部分包/部分表与复位。"]
        module["verification_cases"] = ["TB_PASS_PW_TILE 或 TB_PASS_PW_NARROW；实际ModelSim收据另存。"]
        module["timing_diagrams"] = [{"id": "check", "scenario": "check", "title": "对拍与完整提交",
            "description": "测试结束前逐项比较；输出完成之前不得通过。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p....."}, {"name": "checks", "wave": "01..0."},
                {"name": "export_done", "wave": "0...10"}, {"name": "o_test_done", "wave": "0....1"}]}}]
        path = work / (name + ".json")
        save(path, {"modules": [module]})
        # 已记录的task端口误识别未豁免：仅渲染已确认单输出，实际源码另由ModelSim验证。
        command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.workflow.cli"), "write-spec",
                 "--spec", path, "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / "spec/pw_testbench"
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)


def gate():
    work = fresh("gate")
    for folder in ("rtl", "tests"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry("scripts.python.validation.generated_deliverable_gate"),
                 ROOT / folder, "--json", work / (folder + ".json"), "--markdown", work / (folder + ".md")],
                work, folder, allowed=(0, 1, 2))
    check()


def simulate():
    check()
    reference = json.loads((ROOT / "reference_receipt.json").read_text(encoding="utf-8"))
    assert reference["status"] == "TEST_ONLY_NOT_TRAINED_NOT_ACCURACY_EVIDENCE"
    work = fresh("simulation")
    snapshots = work / "sources"
    snapshots.mkdir()
    for p in [*(ROOT / "rtl").glob("*.v"), *(ROOT / "tests").glob("*.v")]:
        shutil.copyfile(p, snapshots / p.name)
    sources = [*sorted(snapshots.glob("*.v")), *[CORE / name for name in CORE_NAMES]]
    args = json.loads((SOURCE / "simulation_attempt2/vlog.command.json").read_text(encoding="utf-8"))["command"]
    vendor = [a for a in args if "sim_release" in str(a)]
    for case in ("cls_package", "reg_package", "extrema_channel_scale", "zero_bias_limits"):
        assert all((ROOT / (case + "_" + field + ".hex")).is_file() for field in
                   ("input", "weights", "bias", "pre_multiplier", "pre_shift", "post_params", "acc", "pre", "silu", "post"))
    assert (ROOT / "silu_table.hex").is_file()
    hashes = {str(p): sha(p) for p in [*sources, *sorted(ROOT.glob("*.hex")), ROOT / "reference_receipt.json"]}
    save(work / "input_manifest.json", hashes)
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([helpers.MSIM / "vlog.exe", "-work", "work", *vendor, *sources], work, "vlog")
    results = {}
    for name in ("tb_pw_tile", "tb_pw_narrow"):
        output = command([helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", name,
            "+VECTORS=" + ROOT.as_posix(), "+REPORT=" + (work / (name + ".csv")).as_posix(),
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name)
        assert "TB_PASS_PW_" in output
        results[name] = [line for line in output.splitlines() if "TB_PASS_PW_" in line]
    assert all(sha(Path(p)) == value for p, value in hashes.items())
    save(work / "receipt.json", {"status": "PASS", "results": results, "input_manifest_sha256": sha(work / "input_manifest.json"),
        "core_unchanged": True, "numeric_package_test_only": True})
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PHYSICAL_PENDING", "strict_delivery_ready": False})
    check()


def physical():
    check()
    receipts = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)
    assert receipts and json.loads(receipts[-1].read_text(encoding="utf-8"))["status"] == "PASS"
    work = fresh("physical")
    sources = [*(ROOT / "rtl").glob("*.v"), *[CORE / name for name in CORE_NAMES]]
    project = (SOURCE / "physical/project_input.al").read_text(encoding="utf-8")
    project = project.replace((SOURCE / "physical").as_posix(), work.as_posix()).replace("road_rom_current_down2_top", "road_pw_validation_top")
    records = "\n".join(f'<File Path="{p.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{index}"/></FileInfo></File>' for index, p in enumerate(sources, 1))
    project = re.sub(r"<Verilog>.*?</Verilog>", "<Verilog>\n" + records + "\n</Verilog>", project, flags=re.S)
    (work / "road_pw_validation_top.al").write_text(project, encoding="utf-8")
    (work / "project_input.al").write_text(project, encoding="utf-8")
    shutil.copyfile(SOURCE / "physical/frontend.adc", work / "frontend.adc")
    sdc = """create_clock -name probe_clk -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]
set inputs [get_ports {i_rstn i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*] o_busy o_done o_fault o_parameters_ready}]
if {[llength $inputs] != 19 || [llength $outputs] != 22} {error "PW diagnostic IO count changed"}
set_input_delay -clock [get_clocks probe_clk] -max 0.000 $inputs
set_input_delay -clock [get_clocks probe_clk] -min 0.000 $inputs
set_output_delay -clock [get_clocks probe_clk] -max 0.000 $outputs
set_output_delay -clock [get_clocks probe_clk] -min 0.000 $outputs
"""
    (work / "frontend.sdc").write_text(sdc, encoding="utf-8")
    original = (SOURCE / "physical/build.tcl").read_text(encoding="utf-8")
    script = original[:original.index("export_db before_replication.db")].replace("road_rom_current_down2_top", "road_pw_validation_top")
    script += """route
export_db pr.db
write_verilog routed_netlist.v -implement -top road_pw_validation_top
report_area -verbose -io_info -file frontend_route.area
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file all_endpoints_include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file all_violations.timing
set all_regs [get_regs -hier *]
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_all_checks.timing
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $dsp_cells] == 0 || [llength $eram_cells] == 0} {error "Arithmetic or SiLU removed"}
set dsp_outputs [get_pins -of $dsp_cells -filter {DIRECTION == output} *]
set dsp_inputs [get_pins -of $dsp_cells -filter {DIRECTION == input} *]
set eram_outputs [get_pins -of $eram_cells -filter {DIRECTION == output} *]
set eram_inputs [get_pins -of $eram_cells -filter {DIRECTION == input} *]
report_timing_path -from $dsp_outputs -ep_num 100000 -path_num 1 -file dsp_outputs_all_checks.timing
report_timing_path -to $dsp_inputs -ep_num 100000 -path_num 1 -file dsp_inputs_all_checks.timing
report_timing_path -from $eram_outputs -ep_num 100000 -path_num 1 -file eram_outputs_all_checks.timing
report_timing_path -to $eram_inputs -ep_num 100000 -path_num 1 -file eram_inputs_all_checks.timing
report_timing_path -from [get_ports i_rstn] -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
puts "REPORT_COMPLETION_DONE"
close_project
exit
"""
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", script, re.M)
    (work / "build.tcl").write_text(script, encoding="utf-8")
    hashes = {str(p): sha(p) for p in [*sources, work / "build.tcl", work / "frontend.sdc", work / "frontend.adc", work / "project_input.al"]}
    save(work / "input_manifest.json", hashes)
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PHYSICAL_RUNNING", "physical_scope": "PW48+MAC+PP+SiLU+narrow_shell; no full ROM/video", "strict_delivery_ready": False})
    try:
        output = command([TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in output and 'finish command "route"' in output
    except Exception as error:
        save(ROOT / "status.json", {"status": "PHYSICAL_ATTEMPT_FAILED", "directory": str(work), "error": repr(error),
            "functional_pass": True, "strict_delivery_ready": False})
        raise
    finally:
        save(work / "input_check_after.json", {"same": all(sha(Path(p)) == v for p, v in hashes.items())})
        check()
    summarize_physical(work)


def project_provenance():
    # 第二次TD已自动把绝对源路径存为相对路径；恢复初始字节并以初始哈希核对，不覆盖原same=false记录。
    work = ROOT / "physical_attempt2"
    sources = [*(ROOT / "rtl").glob("*.v"), *[CORE / name for name in CORE_NAMES]]
    project = (SOURCE / "physical/project_input.al").read_text(encoding="utf-8")
    project = project.replace((SOURCE / "physical").as_posix(), work.as_posix()).replace("road_rom_current_down2_top", "road_pw_validation_top")
    rows = "\n".join(f'<File Path="{p.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{index}"/></FileInfo></File>' for index, p in enumerate(sources, 1))
    project = re.sub(r"<Verilog>.*?</Verilog>", "<Verilog>\n" + rows + "\n</Verilog>", project, flags=re.S)
    snapshot = work / "project_input_reconstructed.al"
    snapshot.write_text(project, encoding="utf-8")
    hashes = json.loads((work / "input_manifest.json").read_text(encoding="utf-8"))
    actual = work / "road_pw_validation_top.al"
    assert sha(snapshot) == hashes[str(actual)]
    assert all(sha(Path(p)) == value for p, value in hashes.items() if Path(p) != actual)
    def fingerprint(text):
        tree = ET.fromstring(text.replace("UsedInP&R", "UsedInP&amp;R"))
        files = {(work / n.attrib["Path"]).resolve().as_posix(): sorted((a.attrib["Name"], a.attrib["Val"]) for a in n.findall("FileInfo/Attr"))
                 for n in tree.findall(".//Source_Files/Verilog/File")}
        return {"sources": files, "hardware": ET.tostring(tree.find("HardWare")).decode(), "top": ET.tostring(tree.find("TOP_MODULE")).decode()}
    before, after = fingerprint(project), fingerprint(actual.read_text(encoding="utf-8"))
    assert before == after
    save(work / "project_provenance.json", {"status": "PASS", "initial_bytes_reconstructed_sha256": sha(snapshot),
         "original_after_record_retained": "same=false because TD reformats and relativizes project paths",
         "source_paths_attributes_hardware_top_unchanged": True, "other_inputs_unchanged": True})


def memory_query():
    source = ROOT / "physical_attempt2"
    work = fresh("memory_query")
    shutil.copyfile(source / "pr.db", work / "source.db")
    project = (source / "road_pw_validation_top.al").read_text(encoding="utf-8").replace(source.as_posix(), work.as_posix())
    (work / "road_pw_validation_top.al").write_text(project, encoding="utf-8")
    script = """import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_pw_validation_top.al -single_run
import_db source.db
report_ram_utilization -file ram.rpt
puts "MEMORY_QUERY_DONE"
close_project
exit
"""
    (work / "query.tcl").write_text(script, encoding="utf-8")
    digest = sha(source / "pr.db")
    output = command([TD, "query.tcl"], work, "td_launcher")
    assert "MEMORY_QUERY_DONE" in output and sha(source / "pr.db") == digest
    save(work / "receipt.json", {"status": "PASS", "original_database_sha256": digest, "original_db_unchanged": True})


def summarize_physical(work):
    parser = load("pw48_existing_timing_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    records, negatives = {}, []
    for name in ("all_endpoints", "all_endpoints_include_ignored", "internal_all_checks", "external_reset_entry",
                 "dsp_outputs_all_checks", "dsp_inputs_all_checks", "eram_outputs_all_checks", "eram_inputs_all_checks"):
        stats, failed = parser.read_timing(work / (name + ".timing"), keep_negative=True)
        records[name] = stats
        if name == "all_endpoints_include_ignored": negatives = failed
    internal = [row for row in negatives if row["scope"] == "internal"]
    area = parser.parse_area((work / "frontend_route.area").read_text(encoding="utf-8"))
    assert area["io"]["used"] == 42
    save(work / "physical_summary.json", {"device": "PH1P35MDG324-3", "clock_mhz": 100, "resources": area,
        "reports": records, "internal_failed_endpoints": internal, "internal_timing_pass": not internal,
        "database_sha256": sha(work / "pr.db"),
        "test_only": True, "scope": "PW48+MAC+dynamic_PP+SiLU+narrow_shell; no full ROM or video"})
    save(work / "failed_endpoint_inventory.json", negatives)
    save(ROOT / "status.json", {"status": "INTERNAL_PASS_EXTERNAL_STRICT_OPEN" if not internal else "INTERNAL_TIMING_FAILED",
        "internal_failed_endpoints": len(internal), "functional_pass": True, "strict_delivery_ready": False})


def finalize():
    check()
    physical_dir = ROOT / "physical_attempt2"
    physical_data = json.loads((physical_dir / "physical_summary.json").read_text(encoding="utf-8"))
    database_sha256 = sha(physical_dir / "pr.db")
    query_receipt = json.loads((ROOT / "memory_query/receipt.json").read_text(encoding="utf-8"))
    assert database_sha256 == query_receipt["original_database_sha256"]
    physical_data["database_sha256"] = database_sha256
    save(physical_dir / "physical_summary.json", physical_data)
    assert json.loads((physical_dir / "project_provenance.json").read_text(encoding="utf-8"))["status"] == "PASS"
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    assert json.loads((simulation / "receipt.json").read_text(encoding="utf-8"))["status"] == "PASS"
    inputs = json.loads((simulation / "input_manifest.json").read_text(encoding="utf-8"))
    for p, value in inputs.items():
        assert sha(Path(p)) == value
        candidate = ROOT / "rtl" / Path(p).name
        if candidate.exists(): assert sha(candidate) == value
    physical_inputs = json.loads((physical_dir / "input_manifest.json").read_text(encoding="utf-8"))
    assert all(sha(Path(p)) == value for p, value in physical_inputs.items() if not p.endswith(".al"))
    rows = [{k: int(v) for k, v in row.items()} for row in csv.DictReader((simulation / "tb_pw_tile.csv").open(encoding="utf-8"))]
    assert len(rows) == 5
    normal = [r for r in rows if r["stall_mode"] == 0 and r["case_id"] in (0, 1)]
    assert len(normal) == 2 and all(r["core_cycles"] == 3874 for r in normal)
    partition = ("prepare", "send_accept", "send_stall", "mac_wait_accept", "mac_wait_stall", "drain", "advance")
    assert all(sum(r[k] for k in partition) == r["core_cycles"] for r in rows)
    save(ROOT / "cycle_summary.json", {"cases": rows, "normal_tile_core": 3874,
        "mutually_exclusive_partition": partition, "activity_counters_not_additive": ["raw_pre_busy", "raw_silu_busy", "raw_post_busy"],
        "table_reload_entries": 1024, "scalar_payload_records": 3218,
        "measured_narrow": list(csv.DictReader((simulation / "tb_pw_narrow.csv").open(encoding="utf-8"))),
        "scope": "Fixed 4x4 PW48 test vectors, no full-layer sequencer or DDR"})
    old = json.loads((SOURCE / "layer_cycle_ledger.json").read_text(encoding="utf-8"))
    head_names = {"head2.cls_pw.conv", "head2.reg_pw.conv"}
    for row in old["layers"]:
        if row["name"] in head_names:
            assert row["output_shape_hwc"] == [72, 128, 48]
            row.update(measurement_kind="test_parameter_4x4_tile", measured_tile_core=3874, tiles=576,
                       conditional_full_layer_core=3874 * 576)
    projected = 4579776 + 2 * 3874 * 576
    assert projected == 9042624
    old.update(verified_full_tensor_layers=3, additional_fixed_tile_shapes=2,
        conditional_5layer_core=projected, remaining_5fps_budget=20000000 - projected,
        limits="Only first3 layers are full-tensor RTL; next2 are repeated-shape tile projections. Remaining62, DDR/nonconv/NMS not measured.")
    save(ROOT / "layer_cycle_ledger.json", old)
    ram = (ROOT / "memory_query/ram.rpt").read_text(encoding="utf-8")
    section = ram.split("ERAM20K Usage", 1)[1].split("Distributed RAM Usage", 1)[0]
    records = re.findall(r"^\s*(\S+)\s*\|\s*(\S+\.v\((\d+)\))", section, re.M)
    assert len(records) == 16
    counts = Counter(int(line) if "scheduler" in name else "SiLU" for name, _, line in records)
    assert counts == {107: 2, 115: 6, 278: 3, 279: 3, 154: 1, "SiLU": 1}, counts
    save(ROOT / "ram_allocation.json", {"status": "OBSERVED", "source_sha256": sha(ROOT / "rtl/road_pw_tile_scheduler.v"),
        "input": 2, "weights": 6, "bias": 3, "pre_multiplier": 3, "output": 1, "silu": 1,
        "raw_ram_records": records, "conditional_video40_rom56_total": 112,
        "next_single_variable": "Split bias/pre_multiplier into three 16-deep output-lane banks; verify actual mapping, no promised count"})
    gate_dir = sorted(ROOT.glob("gate*/rtl.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    gates = {}
    for name in ("rtl", "tests"):
        value = json.loads((gate_dir / (name + ".json")).read_text(encoding="utf-8"))
        gates[name] = {k: value[k] for k in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
    save(ROOT / "strict_summary.json", {"objects": gates, "delivery_ready": False,
        "rtl_control_parser_failed": True, "actual_modelsim": "PASS", "actual_td_internal": physical_data["internal_timing_pass"],
        "limits": "Parse-fallback findings are not independent proven hardware defects; not a strict pass or waiver"})
    failed = json.loads((physical_dir / "failed_endpoint_inventory.json").read_text(encoding="utf-8"))
    external = dict(Counter(r["scope"] + ":" + r["check"] for r in failed))
    checks = physical_data["reports"]["internal_all_checks"]["checks"]
    save(ROOT / "status.json", {"status": "TILE_FUNCTION_INTERNAL_TIMING_PASS_INTEGRATION_RAM_OPEN",
        "baseline_commit": "2e872d9c", "normal_pw48_tile_core": 3874, "internal_failed_endpoints": len(physical_data["internal_failed_endpoints"]),
        "physical_resources": physical_data["resources"], "conditional_5layer_core": projected,
        "remaining_62layer_and_io_budget": 20000000 - projected, "strict_delivery_ready": False,
        "next": "Three shallow parameter banks to reduce observed6ERAM before expanding shapes", "test_only": True})
    text = f"""RoadYOLO PW48固定小块：阶段结果与下一步（2026-10-15）

当前未通过：严格RTL控制解析/交付门；外部窄口及原始复位时序；与ROM/视频融合后的存储与整机资源；完整67层、真实QAT及精度/FPS验收。
本次完成：新48→48小块的真实算术/逐级对拍和新实际顶层布局布线，未改旧核、生产、训练或位流。

1. 代码和边界
rtl/road_pw_tile_scheduler.v：固定4×4、48→48 PW，输入HWC，权重OIHW；8输入bank、24权重bank，装载仅重排，不改数值。
rtl/road_pw_validation_top.v：42位I/O、16位窄口，全部操作数/量化参数及1024表项动态装入；含两级复位释放、完整包保管和真实缓存导出。
复用既有road_mac_probe、dynamic PP、round和SiLU源码，接口、signed33、末组INT32、RNE、复位及MAC II均未改。
每tile256任务，1536组，36864 MAC，768输出；每路48项，未推广192项合法上限。
两组参数来自冻结TEST_ONLY包的head2.cls_pw.conv/reg_pw.conv，另加极值和INT32边界；不等于训练权重。

2. 通过的功能测试
Python：bank双射、48项signed33逐前缀、六组矩阵对直接卷积及整数算子链通过。
ModelSim：simulation_attempt3两TB通过，0 errors；供应商模型INIT_FILE警告保留。
cls/reg/极值/INT32边界逐项比较MAC、pre、SiLU、post、提交和实际导出。
覆盖随机反压、512拍满队列、连续重装、部分装载/表、非法记录、MAC/PP中复位及末任务故障禁止发布。
窄口3218个成功fixture scalar包、1024表项；两次各768项index/data对拍，包含TX反压、状态两字及错误F001。
修复的具体壳层错误：done同周期只看旧flag_unexported会吞掉已握手export，或放入装表；改为flag_unexported||s_done，共同门控，并新增同拍回归。

3. 实测周期，不把不同窗口混用
正常cls/reg小块均3874核心拍；装载窗口3220/3223，导出769。后者多3拍是不完整start检查，不是核心变慢。
随机reg：core3875、export991；512满队列应力：core4375；不能把故障早退出算加速。
核心互斥分解：PREPARE256（6.61%）、有效MAC送入1536（39.65%）、MAC等待1792（46.26%，其中256拍接受结果）、推进256（6.61%）、末排空34（0.88%）。
总和3874，正常MAC输入反压为0；剩余主损失在任务关闭/周转，不是未填满8输入lane。
pre/SiLU/post原始busy分别3328/2048/3328，彼此重叠，禁止相加代表耗时；每级实际输出768项。
窄口fixture窗口21359拍，含TB主动插入的包间节拍；第一次core计数4376、窄口观察窗口4379，第二次3874/3876，导出窗口3244/3243。
窄口窗口不是DDR吞吐，也不是算术核吞吐；窗口之间控制空隙不隐含纳入其他计数，详见CSV和TB起止注释。

4. 真实物理结果
PH1P35MDG324-3，100 MHz，新实际顶层为PW48缓存/调度+MAC+动态PP+SiLU+窄口，不含完整56块ROM或视频模板。
30 DSP、3806 Slice、16 ERAM、42 I/O；PLB728/2652。
内部setup {checks['setup']['worst_slack_ns']:+.3f}ns，hold {checks['hold']['worst_slack_ns']:+.3f}ns，recovery {checks['recovery']['worst_slack_ns']:+.3f}ns，removal {checks['removal']['worst_slack_ns']:+.3f}ns；全端点含ignored及DSP/ERAM报告核对，内部失败端点0。
最差内部setup：PP退休读指针→scheduler写回计数CE，5级逻辑，布线占79%。hold余量仅20ps，仍偏紧，不宣称生产裕量充分。
外部失败分类：{external}。ERAM专项的负setup/hold属于外部入口/出口，不能当内部通过或整机通过互相替代。
无无时钟、组合环、无路径约束项；dummy node两类及SYN-5025告警保留，不自动豁免。

5. ERAM为什么仍需优化
从实际pr.db只读导出的RAM映射：input2、weight6、output1、SiLU1、bias3、pre_multiplier3，总16。
48×32的bias/pre数组各因三路读映射成3块，深度浅，浪费ERAM容量；不是CNN新增了更多DSP，也不是时序失败。
若直接叠加本壳16+完整ROM56+留存视频模板40，达到112>108，尚未算其余共享/适配。
这只是非共享直叠加的条件警告，不是假装已综合整机；同样不能拿不含ROM的新壳3806 Slice去对比旧壳13479声称整机省了近万Slice。

6. 帧周期账本
前三卷积已有完整张量RTL核心4579776拍；两个S4 PW单层各576个相同形状tile，条件外推各2231424拍。
五层条件合计9042624拍，20M预算还剩10957376拍给62卷积及全部DDR、非卷积、解码/NMS开销。
这里只是3层完整回归+2层小块形状外推，不是5层整帧硬件闭环。layer_cycle_ledger.json仍把剩余层标为未测，不宣称整网5FPS。

7. 失败记录与门禁
首轮simulation因runner指向不存在的vectors/而失败；实际向量在本目录。修正路径并加文件预检，原日志保留。
首轮TD未打开工程：新源记录缺BelongTo/CompileOrder。补齐已验证模板字段后完成第二轮；不是CNN综合失败。
首轮spec工具cwd过窄导致source越界；改回本验证根目录，规格及周期图通过，不改工具安全规则。
TD自动将AL绝对路径改为相对路径并重排XML，原input_check_after same=false保留；重建初始AL字节与初始hash完全一致，语义指纹及所有其他源/约束一致，见project_provenance.json。
新RTL严格门{gates['rtl']['errors']}条含控制解析失败和级联规则；TB{gates['tests']['errors']}条单独保留。不能把它们与旧Stem585条相加，也不能视作这些数量的已证实硬件错误。
compile/ast/readability/comment/naming/profile/testbench/toolchain八项原矩阵见strict_summary.json；真实ModelSim与TD成功另列，不宣布严格交付通过。
未安装的独立readable-python/script技能不冒充通过；本地原有Python/构建链已实际执行。

8. 下一步：只改一个存储变量，不先缩网
冻结本目录源码、数据库、向量和周期。建立独立候选，将bias及pre系数按三输出lane拆为三个16深浅bank，替代48深三读数组。
目标先消除这6块低利用率ERAM；预计可改善但必须看实际映射，不能提前宣布16→10。
保持窄口/算术接口、数值、六组预取、PP重叠和3874正常核心周期；同向量回归后再实现，禁止新增时序例外。
随后扩充真实96/192输入PW及stride1 DW的周期覆盖，复用已有down2调度经验；若任务周转仍占预算主要部分，单列该变量而不混改网络。
只有含DDR/后处理的完整预算明确仍不达标，再评唯一H24备选。未完成上述证据前不删除S4或放宽验收。
"""
    (ROOT / "阶段报告与下一步.txt").write_text(text, encoding="utf-8")
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*")
        if p.is_file() and p.name != "artifact_manifest.json" and "work" not in p.relative_to(ROOT).parts
        and p.suffix in (".py", ".v", ".json", ".md", ".txt", ".tcl", ".sdc", ".adc", ".al", ".hex", ".csv", ".svg", ".json5", ".timing", ".rpt", ".log", ".area")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "dependency", "specifications", "tb_specifications", "gate", "simulate", "physical", "project_provenance", "memory_query", "finalize"))
    globals()[parser.parse_args().action]()
