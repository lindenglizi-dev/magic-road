"""ROM接到冻结共享前端；输出只在本目录，不执行历史脚本的写入入口。"""
import argparse
import ast
from collections import Counter
import csv
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "counter_prepare_20261013"
ROM = ROOT.parent / "rom_down2_prefetch_20261010"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


helpers = load("rom_current_helpers", ROOT.parent / "down2_full_tensor_20261010/run.py")
helpers.ROOT = ROOT
sha, save, fresh, command = helpers.sha, helpers.save, helpers.fresh, helpers.command
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed
    baseline = json.loads((ROOT / "reused_sources.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == value for name, value in baseline.items())


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8")))
    for name in ("frozen.json", "artifact_manifest.json", "run.py"):
        records[str(BASE / name)] = sha(BASE / name)
    paths = [*(ROM / "artifacts").iterdir(), *(ROM / "rtl").glob("*.v"),
             *(ROM / "tests").glob("*.v"), ROM / "reference.py", ROM / "status.json", TD]
    records.update({str(path): sha(path) for path in paths if path.is_file()})
    save(ROOT / "frozen.json", records)
    (ROOT / "rtl").mkdir()
    (ROOT / "tests").mkdir()
    for path in (BASE / "rtl").glob("*.v"):
        shutil.copyfile(path, ROOT / "rtl" / path.name)
    for name in ("road_numeric_rom_reader.v", "road_yolo_numeric_rom_group.v", "road_down2_parameter_prefetch.v"):
        shutil.copyfile(ROM / "rtl" / name, ROOT / "rtl" / name)
    shutil.copytree(ROM / "artifacts", ROOT / "artifacts")
    for name in ("tb_rom_down2.v", "tb_rom_reader.v", "tb_parameter_prefetch.v"):
        if (ROM / "tests" / name).is_file():
            shutil.copyfile(ROM / "tests" / name, ROOT / "tests" / name)
    save(ROOT / "reused_sources.json", {str(path.relative_to(ROOT)): sha(path) for path in (ROOT / "rtl").glob("*.v")})
    save(ROOT / "status.json", {"status": "PREPARED_ROM_AND_FROZEN_COMPUTE", "baseline_commit": "33b2e3fe",
         "model_parameters": "SCHEMA2_TEST_ONLY", "production_modified": False})
    check()


def reference():
    check()
    module = load("rom_current_reference", ROOT / "reference.py")
    module.prepare()
    check()


def dependency():
    check()
    paths = json.loads((BASE / "dependency.json").read_text(encoding="utf-8"))["paths"]
    paths["reference"] = str(ROOT / "reference.py")
    assert all(Path(path).is_file() for path in paths.values())
    save(ROOT / "dependency.json", {"status": "PASS", "paths": paths,
         "hashes": {name: sha(Path(path)) for name, path in paths.items()}})
    work = fresh("dependency_check")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "check"], work, "renderer")


def gate():
    check()
    work = fresh("gate")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    interface = ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v"
    for folder in ("rtl", "tests"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / folder,
            "--include-testbench", "--external-interface-source", helpers.CORE,
            "--external-interface-source", ROOT / "rtl", "--external-interface-source", interface,
            "--json", work / (folder + ".json"), "--markdown", work / (folder + ".md")],
            work, folder, allowed=(0, 1, 2))
    check()


def specifications():
    check()
    work = fresh("specifications")
    source = ROOT / "rtl/road_rom_current_down2_top.v"
    ports = [{"name": name, "direction": direction, "width": int(high) + 1 if high else 1,
              "clock_domain": "i_clk", "role": name, "description": "固定单时钟验证接口，握手前保持负载；复位立即取消。"}
             for direction, high, name in re.findall(r"\b(input|output)\s+(?:signed\s+)?(?:\[(\d+):0\])?\s*(\w+)\s*[,\n]", source.read_text(encoding="utf-8"))]
    contract = {"modules": [{"name": source.stem, "feature": "rom_current_down2", "rtl_path": source.name,
        "description": "完整56ERAM数值ROM，经既有预取器与单项参数保持，接冻结共享前端的down2。",
        "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
        "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
        "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                  "values": "异步断言，两级同步释放；最早第三沿接受；重新选down2并装满参数及1024表项。"},
        "behavior": ["先在共享前端空闲时选择down2，之后释放预取器；ROM请求地址保持到接受，响应保持到消费。",
            "652笔参数经单项缓存保管后提交；满时不接收新参数，valid/kind/address/data在反压时保持。",
            "1024表项走共享前端既有装表缓冲；pref_done、参数缓存空、table_loaded后注册开放外部halo。",
            "halo1296字节完整后才接受start；现有DW/PW调度、量化、元数据、II不变；导出384个PW结果。",
            "故障屏蔽新提交/启动/输出，复位取消缓存、ROM响应与所有旧计算；只可复位恢复。"],
        "constraints": ["SCHEMA2 TEST权重；无真实QAT、DDR、完整67层或板级接口签核。",
                        "低IO诊断壳，无UART/AXI；含Stem共享前端保留，不重复造算术链。"],
        "corner_cases": ["表未满、末参数未提交、参数反压、边界tile、长反压、装载/运行中复位、非法halo地址。"],
        "verification_cases": ["13字段1676笔对拍、7个DW/PW场景逐阶段及读口对拍、ROM跨组/复位单测、实际TD资源及时序。"],
        "timing_diagrams": [{"id": "parameter_handoff", "title": "参数保管与整表完成后开放图像输入",
            "scenario": "parameter_handoff", "description": "省略ROM读取间隔；pending最后提交后，完整表实际装满才开放halo。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
                {"name": "pref_load_accept", "wave": "010....."},
                {"name": "pending", "wave": "0.1.0..."},
                {"name": "core_load_accept", "wave": "0..10..."},
                {"name": "pref_done", "wave": "0...1..."},
                {"name": "table_loaded", "wave": "0....1.."},
                {"name": "parameters_ready", "wave": "0.....1."}]}}]}]}
    path = work / "spec.json"
    save(path, contract)
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
        "--source", source, "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / "write_spec"))
    bundle = work / "spec/rom_current_down2"
    shutil.copyfile(bundle / (source.stem + "_spec.md"), source.with_name(source.stem + "_spec.md"))
    shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms")


def simulate():
    check()
    assert json.loads((ROOT / "reference_receipt.json").read_text(encoding="utf-8"))["test_only"]
    work = fresh("simulation")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    sources = work / "sources"
    sources.mkdir()
    for folder in ("rtl", "tests"):
        for path in (ROOT / folder).glob("*.v"):
            shutil.copyfile(path, sources / path.name)
    vendor_receipt = ROOT.parent / "mac_ce_fanout_local_20261010/shell_rtl/vlog.command.json"
    vendor = [path for path in json.loads(vendor_receipt.read_text(encoding="utf-8"))["command"] if "sim_release" in str(path)]
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([helpers.MSIM / "vlog.exe", "-work", "work", *vendor, *sorted(helpers.CORE.glob("*.v")),
             *sorted(sources.glob("*.v"))], work, "vlog")
    results = []
    for top in ("tb_rom_down2", "tb_rom_reader", "tb_parameter_prefetch"):
        output = command([helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top,
            "+VECTORS=" + (ROOT / "vectors").as_posix(), "+REPORT=" + (work / "cycles.csv").as_posix(),
            "+WORDS=" + (ROOT / "vectors/rom_words.hex").as_posix(), "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, top)
        assert "TB_PASS" in output
        results.append({"top": top, "status": "PASS"})
    save(work / "receipt.json", {"status": "PASS", "results": results,
         "source_hashes": {str(path): sha(path) for path in sources.iterdir()},
         "core_hashes": {str(path): sha(path) for path in helpers.CORE.glob("*.v")},
         "vendor_models": vendor, "test_only": True})
    check()


def physical():
    check()
    receipt_path = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime)[-1]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS" and len(receipt["results"]) == 3
    tested = {Path(name).name: value for name, value in receipt["source_hashes"].items()}
    assert all(tested[path.name] == sha(path) for path in (ROOT / "rtl").glob("*.v"))
    work = fresh("physical")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    if not (ROOT / "rtl/artifacts").exists():
        shutil.copytree(ROOT / "artifacts", ROOT / "rtl/artifacts")
    shutil.copyfile(ROM / "physical_attempt2/joint.sdc", work / "frontend.sdc")
    shutil.copyfile(BASE / "physical/frontend.adc", work / "frontend.adc")
    top = "road_rom_current_down2_top"
    project = (BASE / "physical/road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace((BASE / "physical").as_posix(), work.as_posix()).replace("road_frontend_shared_core", top)
    sources = [*sorted((ROOT / "rtl").glob("*.v")), *sorted(helpers.CORE.glob("*.v"))]
    source_xml = "\n".join(
        f'<File Path="{Path(os.path.relpath(path, work)).as_posix()}"><FileInfo>'
        '<Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/>'
        f'<Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{index}"/>'
        '</FileInfo></File>' for index, path in enumerate(sources, 1))
    project = re.sub(r"<Verilog>.*?</Verilog>", "<Verilog>\n" + source_xml + "\n</Verilog>", project, flags=re.S)
    assert project.count('<Attr Name="UsedInSyn" Val="true"/>') >= len(sources)
    assert source_xml.count('<FileInfo>') == len(sources)
    (work / (top + ".al")).write_text(project, encoding="utf-8")
    (work / "project_input.al").write_text(project, encoding="utf-8")
    build = (BASE / "physical/build.tcl").read_text(encoding="utf-8").replace("road_frontend_shared_core", top)
    build = re.sub(r"set data_inputs \[get_ports \{[^}]*\}\]", "set data_inputs [get_ports {i_load_valid i_load_addr[*] i_load_data[*] i_start i_commit_ready i_export_start i_output_ready}]", build)
    build = re.sub(r"set data_outputs \[get_ports \{[^}]*\}\]", "set data_outputs [get_ports {o_load_ready o_parameters_ready o_busy o_done o_fault o_output_valid o_output_data[*] o_output_index[*] o_export_done}]", build)
    build = build.replace("!= 80", "!= 24").replace("Expected 80", "Expected 24").replace("!= 60", "!= 24").replace("Expected 60", "Expected 24")
    supplement = ("set ram_names {}\nset ram_file [open frontend_route_ram.rpt r]\n"
        "while {[gets $ram_file ram_line] >= 0} {\n"
        " if {[regexp {^\\s*(\\S+)\\s*\\|[^|]*\\|[^|]*\\([0-9]+\\)\\s*\\|} $ram_line unused ram_name]} {lappend ram_names $ram_name}\n}\n"
        "close $ram_file\nset memory_cells [get_cells -hier $ram_names]\n"
        "if {[llength $memory_cells] != [llength $ram_names]} {error {Memory object resolution incomplete}}\n"
        "set memory_inputs [get_pins -of $memory_cells -filter {DIRECTION == input} *]\n"
        "set memory_outputs [get_pins -of $memory_cells -filter {DIRECTION == output} *]\n"
        "set internal_sources [concat $all_regs $dsp_outputs $memory_outputs]\n"
        "report_timing_path -from $internal_sources -to $memory_inputs -ep_num 100000 -path_num 1 -file internal_to_memory.timing\n"
        "report_timing_path -from $internal_sources -to $dsp_inputs -ep_num 100000 -path_num 1 -file internal_to_dsp.timing\n"
        "report_timing_path -from $memory_outputs -to $all_regs -ep_num 100000 -path_num 1 -file memory_to_registers.timing\n"
        "report_timing_path -from $dsp_outputs -to $all_regs -ep_num 100000 -path_num 1 -file dsp_to_registers.timing\n"
        "puts \"ROM_CURRENT_MEMORY_OBJECTS [llength $memory_cells]\"\n")
    build = build.replace('puts "REPORT_COMPLETION_DONE"', supplement + 'puts "REPORT_COMPLETION_DONE"')
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", build, flags=re.M)
    (work / "build.tcl").write_text(build, encoding="utf-8")
    bound = [*sources, work / "frontend.sdc", work / "frontend.adc", work / "build.tcl", work / "project_input.al",
             *sorted((work / "artifacts").iterdir()), *sorted((ROOT / "rtl/artifacts").iterdir())]
    before = {str(path): sha(path) for path in bound}
    save(work / "input_manifest.json", before)
    save(work / "functional_receipt.json", {"path": str(receipt_path), "sha256": sha(receipt_path),
         "reference_receipt_sha256": sha(ROOT / "reference_receipt.json"), "tool_sha256": sha(TD)})
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PHYSICAL_RUNNING", "test_only": True})
    try:
        output = command([TD, "build.tcl"], work, "td_launcher")
        assert 'finish command "route"' in output and "REPORT_COMPLETION_DONE" in output, (
            "TD did not finish route and all reports; inspect " + str(work / "td_launcher.log"))
    except Exception as error:
        save(ROOT / "status.json", {"status": "PHYSICAL_ATTEMPT_FAILED", "directory": str(work),
             "error": repr(error), "functional_pass": True, "test_only": True})
        raise
    finally:
        after = {str(path): sha(path) for path in bound}
        save(work / "input_check_after.json", {"same": after == before, "hashes": after})
        assert after == before
        check()
    report()


def rom_initialization(path):
    result = {}
    for parameters, name, _ in re.findall(r"PH1P_PHY_ERAM_V2\s*#\((.*?)\)\s*\\(\S+)\s*\((.*?)\);", path.read_text(encoding="utf-8"), re.S):
        if "road_yolo_numeric_rom_group_Inst_" not in name:
            continue
        key = "/".join(name.split("/")[-2:])
        values = dict(re.findall(r"\.(INIT(?:P)?_[0-9A-F]{2})\(256'h([0-9A-F]+)\)", parameters))
        assert len(values) == 80 and key not in result
        result[key] = values
    assert len(result) == 56, (path, len(result))
    return result


def report():
    check()
    parser = load("rom_current_timing_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
    work = sorted(ROOT.glob("physical*/pr.db"), key=lambda path: path.stat().st_mtime)[-1].parent
    reports, failures, internal_failures = {}, [], []
    names = ("internal_all_checks", "all_endpoints", "all_endpoints_include_ignored", "external_reset_entry",
        "diagnostic_inputs_to_regs", "regs_to_diagnostic_outputs", "dsp_outputs_all_checks", "dsp_inputs_all_checks",
        "all_eram_outputs_all_checks", "all_eram_inputs_all_checks", "internal_to_memory", "internal_to_dsp",
        "memory_to_registers", "dsp_to_registers")
    for name in names:
        stats, negative = parser.read_timing(work / (name + ".timing"), keep_negative=True)
        reports[name] = stats
        if name == "all_endpoints_include_ignored":
            failures = negative
        if name in ("internal_all_checks", "internal_to_memory", "internal_to_dsp", "memory_to_registers", "dsp_to_registers"):
            internal_failures.extend(negative)
    internal_map = {}
    for row in [*internal_failures, *failures]:
        if row["scope"] == "internal":
            key = (row["check"], row["end"])
            if key not in internal_map or row["slack_ns"] < internal_map[key]["slack_ns"]:
                internal_map[key] = row
    area = parser.parse_area((work / "frontend_route.area").read_text(encoding="utf-8"))
    assert area["io"]["used"] == 50
    assert 0 < area["dsp"]["used"] <= 40 and 56 <= area["eram"]["used"] <= 108
    assert all(area["hierarchy_rows"][name] == 1 for name in
               ("road_mac_probe", "road_dynamic_postprocess", "silu_shared_unit"))
    assert all(reports["internal_all_checks"]["checks"][name]["reported_paths"] > 0
               for name in ("setup", "hold"))
    original_init = rom_initialization(ROM / "physical_attempt2/routed_netlist.v")
    assert rom_initialization(work / "gate_netlist.v") == original_init
    assert rom_initialization(work / "routed_netlist.v") == original_init
    normal = reports["all_endpoints"]["checks"]
    included = reports["all_endpoints_include_ignored"]["checks"]
    delta = {name: included[name]["reported_paths"] - normal[name]["reported_paths"] for name in included}
    result = {"device": "PH1P35MDG324-3", "clock_mhz": 100, "resources": area,
        "reports": reports, "internal_failed_endpoints": list(internal_map.values()),
        "internal_timing_pass": not internal_map, "all_failed_scope_counts": dict(Counter(row["scope"] + ":" + row["check"] for row in failures)),
        "rom_initialized_erams": 56, "rom_init_parameters_identical": 4480,
        "include_ignored_count_delta": delta, "database_sha256": sha(work / "pr.db"),
        "external_contract": "Zero IO delays and automatic pins, not board signoff", "test_only": True}
    save(work / "physical_summary.json", result)
    save(work / "failed_endpoint_inventory.json", failures)
    save(ROOT / "status.json", {"status": "INTERNAL_TIMING_PASS_EXTERNAL_OPEN" if not internal_map else "INTERNAL_TIMING_FAILED",
        "internal_timing_pass": not internal_map, "test_only": True, "strict_delivery_ready": False,
        "not_done": ["External interface/reset signoff", "Strict gates", "Real QAT/DDR/full network/board"]})
    check()


def summarize():
    check()
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime)[-1].parent
    with (simulation / "cycles.csv").open(encoding="utf-8") as stream:
        cycles = list(csv.DictReader(stream))
    assert len(cycles) == 7
    bins = ("commit_stall", "capacity_stall", "commit", "mac_issue", "issue_wait", "drain_other")
    assert all(sum(int(row[name]) for name in bins) == int(row["core"]) for row in cycles)
    save(ROOT / "cycle_summary.json", cycles)
    normal = [row for row in cycles if int(row["case"]) in (0, 1, 2, 6)]
    assert all(int(row["core"]) == 1687 and int(row["export"]) == 384 for row in normal)
    inherited = json.loads((BASE / "cycle_summary.json").read_text(encoding="utf-8"))["candidate"]["normal"]
    assert 1687 * 576 == inherited["down2"]["core"]
    save(ROOT / "bounded_cycle_budget.json", {
        "clock_mhz": 100, "test_parameters_only": True, "measured_tile_core": 1687,
        "measured_tile_export": 384, "measured_halo_window": 1297,
        "halo_payload_accepts": 1296, "normal_reset_to_parameters_ready": 7915,
        "tile_mutually_exclusive_bins": {name: int(normal[0][name]) for name in bins},
        "down2_tiles_in_frozen_graph": 576, "down2_core_conditional_projection": 1687 * 576,
        "inherited_full_frontend_core_not_rerun": inherited["stem"]["core"] + inherited["down2"]["core"],
        "limits": ["One tested tile shape and three positions, not a new full-tensor RTL run",
                   "ROM parameters load once after reset, not once per tile",
                   "DDR, layer switching, complete graph and NMS not measured; no whole-network FPS claim"]})
    gate = sorted(ROOT.glob("gate*/rtl.json"), key=lambda path: path.stat().st_mtime)[-1].parent
    save(ROOT / "strict_summary.json", {name: {key: value for key, value in
         json.loads((gate / (name + ".json")).read_text(encoding="utf-8")).items()
         if key in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
         for name in ("rtl", "tests")})
    review = {}
    for name in ("rtl", "tests"):
        issues = json.loads((gate / (name + ".json")).read_text(encoding="utf-8"))["issues"]
        review[name] = {"by_rule": dict(Counter(item["code"] for item in issues)),
            "semantic_review_required": [item for item in issues if item["code"] in
                ("VG084", "VG085", "VG097", "VG110", "VG113", "VG122", "VG132", "VG135", "VG137", "VG153")]}
    save(ROOT / "semantic_review_inventory.json", review)
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.name != "artifact_manifest.json" and path.suffix not in (".wlf", ".pyc")
        and "work" not in path.relative_to(ROOT).parts})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "reference", "dependency", "gate", "specifications", "simulate", "physical", "report", "summarize"))
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    globals()[cli.parse_args().action]()
