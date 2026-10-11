"""首板自检独立构建：所有工作目录和输出限制在当前候选，不生成位流。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
BASE = ROOT.parent / "mac_ce_fanout_local_20261010"
VECTORS = ROOT.parent / "runtime_layer_integration_20261009/vectors/dynamic_stress"
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
MSIM = Path(r"D:\modeltech64_2020.4\win64")
TD = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe")
SEND, EXPECT, POLL, CONTROL = range(4)
START_SEND, EXPORT_SEND = 4, 5


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def fresh(label):
    work = ROOT / label
    suffix = 1
    while work.exists():
        suffix += 1
        work = ROOT / f"{label}_attempt{suffix}"
    work.mkdir(parents=True)
    return work


def command(args, work, label, timeout=600, allowed=(0,)):
    work.resolve().relative_to(ROOT)
    log = work / (label + ".log")
    assert not log.exists(), log
    record = {"command": list(map(str, args)), "cwd": str(work)}
    try:
        with log.open("w", encoding="utf-8") as stream:
            result = subprocess.run(record["command"], cwd=work, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
        record["returncode"] = result.returncode
    except (OSError, subprocess.TimeoutExpired) as error:
        record["launch_error"] = str(error)
        save(work / (label + ".command.json"), record)
        raise
    save(work / (label + ".command.json"), record)
    assert result.returncode in allowed, (record, log)
    return log.read_text(encoding="utf-8", errors="replace")


def official_sources():
    hdl = PROJECT / "user_source/hdl_source"
    return [hdl / name for name in ("vtc/uivtc.v", "hdmi_tx.v", "hdmi_phy_warpper.v",
        "lane_lvds_10_1.v", "I2S_receiver.v", "audio_arc_calculate.v", "key_remove_shakes.v",
        "hdmi_1_4b_transmitter_core_wrapper.enc.v")]


def prepare():
    assert not (ROOT / "frozen.json").exists(), "prepare只运行一次，已存在时使用后续阶段"
    paths = [p for directory in (BASE / "rtl", BASE / "tests", BASE / "physical",
             VECTORS, PROJECT / "user_source/ip_source/PLL") for p in directory.rglob("*") if p.is_file()]
    paths += official_sources() + [PROJECT / "user_source/constraints_source/pin.adc",
        PROJECT / "td_project/camera_to_dsi_display.sdc", BASE / "status.json", TD,
        MSIM / "vsim.exe", MSIM / "vlog.exe"]
    save(ROOT / "frozen.json", {str(p): digest(p) for p in paths})
    shutil.copytree(BASE / "rtl", ROOT / "core")
    shutil.copytree(VECTORS, ROOT / "vectors")
    shutil.copytree(PROJECT / "user_source/ip_source/PLL", ROOT / "official/PLL")
    for source in official_sources():
        target = ROOT / "official" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    work = fresh("preflight")
    command([sys.executable, "-B", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py",
             "check", "--settings", SKILL / "config/defaults.json"], work, "dependencies", allowed=(0, 1))
    save(ROOT / "scope.json", {"task": "P0/P1 autonomous DW/PW selftest",
        "production_modified": False, "bitstream_or_board_or_flash": False,
        "original_kernel_modified": False, "new_timing_exceptions": False,
        "board_identity_and_pin_voltage_verified": False, "logical_io_bits": 6,
        "physical_diagnostic_not_production_release": True})
    check()


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [p for p, sha in frozen.items() if not Path(p).exists() or digest(Path(p)) != sha]
    copied = [p.name for p in (ROOT / "core").glob("*.v") if digest(p) != digest(BASE / "rtl" / p.name)]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed,
                                     "modified_copied_core": copied})
    assert not changed and not copied, (changed, copied)


def read_words(name):
    return [int(line, 16) for line in (ROOT / "vectors" / name).read_text().split()]


def program_reference():
    """先建立确定性发送/比较脚本；算术黄金值仍由冻结整数参考提供。"""
    program = []
    boundaries = []
    table = read_words("silu.hex")
    assert len(table) == 1024
    for case in ("edge", "interior", "bottom_right"):
        begin = len(program)
        program.append((CONTROL, 0))
        table_begin = len(program)
        program += [(SEND, 0x1000)] + [(SEND, value) for value in table]
        segments = [(0, case + "_halo.hex", 1296, True), (2, "dw_weights.hex", 144, True),
                    (3, "dw_biases.hex", 16, False), (4, "pw_weights.hex", 384, True),
                    (5, "pw_biases.hex", 24, False), (6, "multipliers.hex", 40, False),
                    (7, "controls.hex", 44, False)]
        records = 0
        for kind, name, count, signed_byte in segments:
            words = read_words(name)
            assert len(words) == count
            for address, value in enumerate(words):
                if signed_byte:
                    assert 0 <= value <= 255
                    value = value - 256 if value & 128 else value
                value &= 0xffffffff
                program += [(SEND, 0x2000), (SEND, (kind << 13) | address),
                            (SEND, value & 0xffff), (SEND, value >> 16)]
                records += 1
        assert records == 1948
        program += [(SEND, 0x6001), (START_SEND, 0x3000), (POLL, 1687), (EXPORT_SEND, 0x4000)]
        expected_begin = len(program)
        expected = read_words(case + "_output.hex")
        assert len(expected) == 384 and any(0 < v < 127 for v in expected)
        for index, value in enumerate(expected):
            program += [(EXPECT, 0x8000 | index), (EXPECT, 0x9000 | value)]
        program.append((EXPECT, 0xc000))
        boundaries.append({"case": case, "begin": begin, "table_begin": table_begin,
            "first_expected": expected_begin, "end": len(program), "load_records": records,
            "output_bytes": len(expected), "core_cycles": 1687})
    program.append((CONTROL, 1))
    assert len(program) < 32768
    out = ROOT / "program"
    out.mkdir(exist_ok=True)
    def emit(name, instructions):
        assert all(0 <= op <= 5 and 0 <= value <= 0xffff for op, value in instructions)
        words = [(op << 16) | value for op, value in instructions]
        words += [(CONTROL << 16) | 1] * (32768 - len(words))
        (out / name).write_text("".join(f"{word:05x}\n" for word in words), encoding="ascii")
    emit("selftest_program.hex", program)
    wrong = list(program)
    location = boundaries[0]["first_expected"] + 1
    wrong[location] = (EXPECT, wrong[location][1] ^ 1)
    emit("wrong_expected.hex", wrong)
    missing = program[:1] + program[1026:]
    emit("missing_table.hex", missing)
    save(out / "manifest.json", {"instructions": len(program), "physical_words": 32768,
        "word_bits": 19, "storage_bytes": 77824, "cases": boundaries,
        "reference_output_items": 1152, "first_wrong_expected_address": location,
        "schema": {"0": "SEND16", "1": "EXPECT16", "2": "POLL31_CORE1687",
                   "3/0": "LOCAL_RESET8", "3/1": "END_CHECK3_CASES_1152_ITEMS",
                   "4": "START_SEND16", "5": "EXPORT_SEND16"},
        "source_vector_hashes": {p.name: digest(p) for p in (ROOT / "vectors").glob("*.hex")}})
    print("REFERENCE_PASS instructions=", len(program), "items=1152", flush=True)


def simulation():
    work = fresh("simulation")
    shutil.copyfile(ROOT / "program/selftest_program.hex", work / "selftest_program.hex")
    shutil.copyfile(ROOT / "program/wrong_expected.hex", work / "wrong_expected.hex")
    shutil.copyfile(ROOT / "program/missing_table.hex", work / "missing_table.hex")
    old = json.loads((BASE / "shell_rtl/vlog.command.json").read_text())["command"]
    vendor = [p for p in old if "sim_release" in str(p)]
    sources = [*vendor, *sorted((ROOT / "core").glob("*.v")),
               ROOT / "rtl/road_board_selftest_player.v", ROOT / "rtl/road_selftest_display.v",
               ROOT / "tests/tb_board_selftest.v", ROOT / "tests/tb_selftest_display.v"]
    command([MSIM / "vlib.exe", "work"], work, "vlib")
    command([MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    receipts = []
    for case in ("normal", "stalls", "wrong", "missing", "timeout", "reset", "held_reset"):
        output = command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR",
            "tb_board_selftest", "+CASE=" + case, "+VECTORS=" + (ROOT / "vectors").as_posix(), "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, case)
        assert "TB_PASS_BOARD_SELFTEST" in output, output[-3000:]
        receipts.append({"case": case, "pass_line": re.findall(r".*TB_PASS_BOARD_SELFTEST.*", output)})
    output = command([MSIM / "vsim.exe", "-c", "-lib", "work", "tb_selftest_display", "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "display")
    assert "TB_PASS_SELFTEST_DISPLAY" in output
    save(work / "receipt.json", {"tests": receipts, "display": "passed",
        "vendor_models": vendor, "arithmetic_core_unchanged": True,
        "full_hdmi_encrypted_ip_simulated": False, "board_tested": False})
    check()


def gate():
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    for name in ("rtl", "core", "tests"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / name,
            "--json", work / (name + ".json"), "--markdown", work / (name + ".md")],
            work, name, allowed=(0, 1, 2))
    check()


def specifications():
    """显式接口合同经技能注册规格生成器核对源码并渲染周期图。"""
    definitions = {
        "road_board_selftest_player": [
            ("i_clk", "input", 1, "计算100MHz"), ("i_rstn", "input", 1, "源域已同步释放复位"),
            ("i_rx_ready", "input", 1, "原壳命令接收许可"), ("i_tx_valid", "input", 1, "原壳响应有效"),
            ("i_tx_data", "input", 16, "原壳响应字"), ("o_rx_valid", "output", 1, "发送有效保持至ready"),
            ("o_rx_data", "output", 16, "锁存的命令或负载字"), ("o_tx_ready", "output", 1, "仅比较/状态阶段开放"),
            ("o_core_rstn", "output", 1, "套间断言8拍释放后等8拍"),
            ("o_payload", "output", 256, "诊断包，只经冻结快照跨域")],
        "road_selftest_display": [
            ("i_clk", "input", 1, "源域100MHz"), ("i_rstn", "input", 1, "源域同步释放复位"),
            ("i_payload", "input", 256, "源域动态诊断包"), ("i_pixel_clk", "input", 1, "目标75MHz像素时钟"),
            ("i_pixel_rstn", "input", 1, "像素域同步释放复位"), ("i_vsync", "input", 1, "VTC消隐区VS"),
            ("i_de", "input", 1, "VTC有效像素"), ("o_rgb", "output", 24, "一拍延迟TEST状态色"),
            ("o_vsync", "output", 1, "一拍延迟VS"), ("o_de", "output", 1, "一拍延迟DE"),
            ("o_active_payload", "output", 256, "整帧冻结诊断快照")],
        "road_board_selftest_top": [
            ("i_sys_clk", "input", 1, "项目声明C4板载50MHz，实物待确认"),
            ("i_rstn", "input", 1, "项目声明R10外部低有效复位，立即取消"),
            ("o_tmds_blue_p", "output", 1, "官方通道0/G16，差分配对待核实"),
            ("o_tmds_green_p", "output", 1, "官方通道1/F17，差分配对待核实"),
            ("o_tmds_red_p", "output", 1, "官方通道2/H14，差分配对待核实"),
            ("o_tmds_clock_p", "output", 1, "官方TMDS时钟/C17")]
    }
    behavior = {
        "road_board_selftest_player": [
            "固定28774条19位脚本指令，32768词ROM；无板外脚本接口。地址等待一拍，下一拍锁存ROM，随后解码，握手后才推进PC。",
            "每套复位原壳并重装1024表项；1948项装载、允许提交、启动、31字轮询、384索引/字节对及C000。三套1152项才能PASS。",
            "状态首字检查table_loaded和三类fault，done且非busy后才检1687核心周期并导出。错误/500000周期超时优先FAIL并保存首错。",
            "payload从高到低：status2/state5/cases2/compared11/core32/preload32/export32/total32/first_pc15/expected16/actual16/error4/sent32/run_elapsed25。",
            "total=preload+run_elapsed+export，三者互斥；run_elapsed含启动命令握手后至完整完成状态响应，非纯核心周期。"] ,
        "road_selftest_display": [
            "req等于两拍同步ack时冻结payload并翻转req，直到ack返回前保持载荷。目标两拍同步req，仅VS上升沿采样完整载荷并确认。",
            "中间进度可以合并；终态保持且最终可发布。套间核复位不触碰CDC，全局复位取消双方请求并清active。",
            "固定TEST点阵、黄RUN/绿PASS/红FAIL、256位诊断带和显示本地心跳；RGB/VS/DE共同延迟一拍。无识别框。"],
        "road_board_selftest_top": [
            "外部仅6位逻辑接口，不引出诊断命令总线。实例化原8份计算RTL、固定播放器/显示、官方PLL/VTC/HDMI。",
            "raw_rstn=i_rstn AND PLL lock，立即取消；100MHz/75MHz各两拍同步释放。原计算壳自己的两级释放保持。",
            "PLL为100/75/375MHz相关时钟；VTC1280x720/1650x750约60.606Hz。HDMI跨像素/串行复位必须由真实STA确认。"]
    }
    work = fresh("specification")
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    for name, entries in definitions.items():
        if name == "road_board_selftest_player":
            signals = [{"name": "i_clk", "wave": "p......"}, {"name": "o_rx_valid", "wave": "01..0.."},
                       {"name": "i_rx_ready", "wave": "0..10.."},
                       {"name": "o_rx_data", "wave": "x=..x..", "data": ["locked word"]}]
            scenario = "send_backpressure"
            description = "有效后等待ready期间字和PC保持；消费边沿后回到地址等待/读ROM/解码，不能把脚本装载II当成核II。"
        elif name == "road_selftest_display":
            signals = [{"name": "request", "wave": "01......"},
                       {"name": "hold_payload", "wave": "x=.....x", "data": ["frozen"]},
                       {"name": "request_sync", "wave": "0..1...."},
                       {"name": "VS", "wave": "0....10."}, {"name": "ack", "wave": "0.....1."}]
            scenario = "snapshot_at_vs"
            description = "不同域示意而非固定跨域拍数；载荷在请求同步前已冻结，VS采样后ack返回，期间不覆盖。"
        else:
            signals = [{"name": "i_rstn", "wave": "01......"}, {"name": "pll_lock", "wave": "0..1...."},
                       {"name": "raw_rstn", "wave": "0..1...."}, {"name": "domain_release", "wave": "0....1.."},
                       {"name": "core_local_rstn", "wave": "0......."}]
            scenario = "startup_release"
            description = "PLL锁定后各域两级释放；播放器仍执行本地8拍复位和8拍等待，然后重新装表，不依赖SiLU初始化。"
        module = {"name": name, "feature": "board_selftest", "rtl_path": "rtl/" + name + ".v",
            "description": "独立首板计算自检，不是完整CNN或识别验收。",
            "interfaces": {"ports": [{"name": n, "direction": d, "width": w, "role": desc,
                                       "description": desc} for n, d, w, desc in entries]},
            "clock": {"domains": "100MHz计算；75MHz像素；375MHz串行，官方PLL相关时钟"},
            "reset": {"assertion": "异步立即取消", "release": "每域两拍；计算壳原协议保留"},
            "behavior": behavior[name], "constraints": ["PH1P35MDG324/-3，不增加时序例外。真实资源/时序待当前顶层验证。"],
            "corner_cases": ["发送反压、缺表、错字、超时、全局复位、套间局部复位、快照忙时终态。"],
            "verification_cases": ["tb_board_selftest正常/停顿/错误/缺表/超时/复位；tb_selftest_display。"],
            "timing_diagrams": [{"id": scenario, "title": name + "接口周期", "scenario": scenario,
                                  "description": description, "wavejson": {"signal": signals}}]}
        spec = work / (name + ".json")
        save(spec, {"modules": [module]})
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", spec,
                 "--out-dir", ROOT, "--source", ROOT / "rtl" / (name + ".v"), "--language", "zh"],
                 ROOT, work.name + "_" + name, timeout=120)


def physical():
    """实际首板顶层隔离诊断；即使失败也保留数据库/报告，不调用bitgen。"""
    work = fresh("physical")
    shutil.copyfile(ROOT / "program/selftest_program.hex", work / "selftest_program.hex")
    # 旧TD工程使用未转义的属性名；只规范读取副本，不修改旧工程。
    xml_text = (BASE / "physical/road_dynamic_overlap_low_io_top.al").read_text(encoding="utf-8")
    tree = ET.ElementTree(ET.fromstring(xml_text.replace("UsedInP&R", "UsedInP&amp;R")))
    project = tree.getroot()
    project.set("Path", work.as_posix())
    project.find("Name").text = "road_board_selftest_top"
    files = project.find("Source_Files")
    files.clear()
    sources = [*sorted((ROOT / "core").glob("*.v")), *sorted((ROOT / "rtl").glob("*.v")),
               *[ROOT / "official" / p.name for p in official_sources()]]
    group = ET.SubElement(files, "Verilog")
    for order, source in enumerate(sources, 1):
        info = ET.SubElement(ET.SubElement(group, "File", Path=source.as_posix()), "FileInfo")
        for key, value in (("UsedInSyn", "true"), ("UsedInP&R", "true"), ("BelongTo", "design_1"), ("CompileOrder", str(order))):
            ET.SubElement(info, "Attr", Name=key, Val=value)
    ip = ET.SubElement(files, "IP_FILE")
    info = ET.SubElement(ET.SubElement(ip, "File", Path=(ROOT / "official/PLL/PLL.xml").as_posix()), "FileInfo")
    for key, value in (("UsedInSyn", "true"), ("UsedInP&R", "true"), ("BelongTo", "design_1"), ("CompileOrder", "1")):
        ET.SubElement(info, "Attr", Name=key, Val=value)
    for name in ("LABEL", "MODULE"):
        project.find("TOP_MODULE/" + name).text = "road_board_selftest_top"
    tree.write(work / "road_board_selftest_top.al", encoding="utf-8", xml_declaration=True)
    for name in ("build.tcl", "board.sdc", "board.adc"):
        shutil.copyfile(ROOT / "build" / name, work / name)
    closure = sources + [work / name for name in ("selftest_program.hex", "board.adc", "board.sdc", "build.tcl", "road_board_selftest_top.al")]
    closure += [p for p in (ROOT / "official/PLL").rglob("*") if p.is_file()]
    save(work / "input_manifest.json", {str(p): digest(p) for p in closure})
    command([TD, "build.tcl"], work, "td", timeout=3600, allowed=(0, 1))
    check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "reference", "simulation", "gate", "specifications", "physical", "check"))
    stage = parser.parse_args().stage
    {"prepare": prepare, "reference": program_reference, "simulation": simulation,
     "gate": gate, "specifications": specifications, "physical": physical, "check": check}[stage]()
