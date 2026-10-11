"""仅验证Stem地址生成候选；复用冻结前端回归，所有输出限定本目录。"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "frontend_shared_core_20261011"
spec = importlib.util.spec_from_file_location("shared_run", PREVIOUS / "run.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
shared.ROOT = shared.helpers.ROOT = ROOT
shared.STEM = ROOT / "rtl/road_stem_tile_scheduler.v"
save, sha, command = shared.save, shared.sha, shared.command


def setup():
    assert not (ROOT / "frozen.json").exists(), "不覆盖已冻结候选"
    records = json.loads((PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((PREVIOUS / "artifact_manifest.json").read_text(encoding="utf-8")))
    records[str(PREVIOUS / "artifact_manifest.json")] = sha(PREVIOUS / "artifact_manifest.json")
    for source in (PREVIOUS / "physical_attempt2").iterdir():
        if source.is_file():
            records[str(source)] = sha(source)
    save(ROOT / "frozen.json", records)
    for folder in ("rtl", "tests"):
        shutil.copytree(PREVIOUS / folder, ROOT / folder)
    shutil.copyfile(shared.BASE / "rtl/road_stem_tile_scheduler.v", shared.STEM)
    shared.check()
    save(ROOT / "status.json", {"stage": "FROZEN_BEFORE_ADDRESS_REPAIR", "not_deployment": True})


def baseline():
    shared.check()
    work = shared.fresh("baseline_gate")
    entry = f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, shared.STEM,
             "--json", work / "stem.json", "--markdown", work / "stem.md"], work, "stem", allowed=(0, 1, 2))
    entry = f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "check"], work, "renderer")
    assert (shared.helpers.SKILL.parent / "erie-remote-ssh/SKILL.md").is_file()
    shared.check()


def reference():
    # 六个合法输出组，分路基址均为常量；无效尾路不访问权重。
    bases = ((0, 27, 54), (81, 108, 135), (162, 189, 216),
             (243, 270, 297), (324, 351, 378), (405, 0, 0))
    covered, valid, masked = set(), 0, 0
    for position in range(16):
        for group_index, channel in enumerate(range(0, 16, 3)):
            for group in range(4):
                for lane in range(8):
                    term = group * 8 + lane
                    for output_lane in range(3):
                        if term < 27 and channel + output_lane < 16:
                            old = (channel + output_lane) * 27 + term
                            new = bases[group_index][output_lane] + term
                            assert new == old and 0 <= new < 432 and new < (1 << 9)
                            covered.add(new)
                            valid += 1
                        else:
                            masked += 1
    assert covered == set(range(432)) and valid == 6912 and masked == 2304
    save(ROOT / "address_reference.json", {"status": "PASS", "valid_reads": valid,
         "masked_lanes": masked, "positions": 16, "max_address": max(covered),
         "address_bits": 9, "group_bases": bases, "pipeline_added": 0,
         "expected_normal_core_cycles": 11883456, "expected_stalls_core_cycles": 14573306})
    print("ADDRESS_REFERENCE_PASS", flush=True)


def specifications():
    shared.check()
    work = shared.fresh("specifications")
    ports = [{"name": name, "direction": direction, "width": int(high) + 1 if high else 1,
              "clock_domain": "i_clk", "role": name, "description": "沿用冻结Stem接口；valid保持到ready，复位立即取消。"}
             for direction, high, name in re.findall(
                 r"\b(input|output)\s+(?:signed\s+)?(?:\[(\d+):0\])?\s*(\w+)\s*[,\n]",
                 shared.STEM.read_text(encoding="utf-8"))]
    module = {"name": shared.STEM.stem, "feature": "stem_address", "rtl_path": shared.STEM.name,
        "description": "固定Stem的权重基址译码；只替换组合地址生成，不改变调度及算术链。",
        "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
        "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
        "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                  "values": "立即取消旧事务；同步释放后重新完整装载1024项表及全部参数/halo。"},
        "behavior": ["4×4输出tile，3输入16输出，3×3 stride2，9×9×3 halo，OIHW432字节权重。",
                     "输出通道组仅0/3/6/9/12/15，归约四组八lane，最后组仅前三lane有效。",
                     "权重地址=六组常量基址+9位零扩展term；合法地址0..431，输出尾路置零。",
                     "PREPARE注册到SEND；SEND背压时载荷保持，不增加寄存器、延迟或II。",
                     "偏置仅first加入；真实缓存256项完整写回后才可导出；故障只可复位恢复。"],
        "constraints": ["TEST_ONLY量化参数；仅前三个卷积验证；不含DDR/生产/位流。",
                        "调度FSM及全部算术源码冻结，非合法通道状态不扩展契约。"],
        "corner_cases": ["channel15尾路、group3尾lane、地址431、负权重、反压、装载/计算中复位。"],
        "verification_cases": ["Python地址穷举；RTL两组权重指纹穷举；冻结normal/stalls/control整帧回归。"],
        "timing_diagrams": [{"id": "weight_hold", "title": "原拍数及背压保持", "scenario": "weight_hold",
            "description": "PREPARE形成权重，SEND保持直至握手；无新增流水拍。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p......"},
                {"name": "state", "wave": "=.=..=.", "data": ["PREPARE", "SEND", "PREPARE"]},
                {"name": "mac_valid", "wave": "0.1..0."}, {"name": "mac_ready", "wave": "0...10."},
                {"name": "weight", "wave": "x.=...x", "data": ["registered payload held"]}]}}]}
    contract = work / "stem.json"
    save(contract, {"modules": [module]})
    entry = f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
             "--source", shared.STEM, "--out-dir", work, "--no-state"], ROOT,
            str(work.relative_to(ROOT) / "write_spec"))
    shutil.copyfile(work / "spec/stem_address/road_stem_tile_scheduler_spec.md",
                    shared.STEM.with_name("road_stem_tile_scheduler_spec.md"))
    shutil.copytree(work / "spec/stem_address/waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def simulate():
    shared.simulate()
    work = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    output = command([shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR",
                      "tb_stem_weight_address", "-do",
                      "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "address")
    assert "TB_PASS_STEM_WEIGHT_ADDRESS checks=18432" in output
    save(work / "address_receipt.json", {"status": "PASS", "checks": 18432, "mismatches": 0})
    shared.check()


def physical():
    shared.check()
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    assert json.loads(simulation.read_text(encoding="utf-8"))["status"] == "PASS"
    assert (simulation.parent / "address_receipt.json").exists()
    work = ROOT / "physical"
    work.mkdir()  # 不覆盖历史尝试。
    old = PREVIOUS / "physical_attempt2"
    for filename in ("frontend.sdc", "frontend.adc", "physical_report.py"):
        shutil.copyfile(old / filename, work / filename)
    manifest = json.loads((old / "source_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        if item["path"].endswith("road_stem_tile_scheduler.v"):
            item["path"] = "../rtl/road_stem_tile_scheduler.v"
        item["sha256"] = sha((work / item["path"]).resolve())
    manifest["execution_authorization"] = "User approved isolated Stem address repair, unchanged numeric/II/reset; no bitstream. Same full-vector control/normal/stalls and address enumeration must pass first."
    save(work / "source_manifest.json", manifest)
    project = (old / "road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace(old.as_posix(), work.as_posix()).replace(
        "../../stem_down2_handoff_20261011/rtl/road_stem_tile_scheduler.v", "../rtl/road_stem_tile_scheduler.v")
    (work / "road_frontend_shared_core.al").write_text(project, encoding="utf-8")
    build = (old / "build.tcl").read_text(encoding="utf-8").replace(
        'if {[llength $eram_cells] != 1} { error "Expected exactly one ERAM for the shared SiLU table" }',
        'if {[llength $eram_cells] < 1} { error "No retained ERAM" }\n'
        'set silu_count 0\nforeach cell $eram_cells {\n'
        '    puts "ERAM_RECORD [get_property NAME $cell]"\n'
        '    if {[string match {*u_silu*} [get_property NAME $cell]]} { incr silu_count }\n}\n'
        'if {$silu_count != 1} { error "Shared SiLU table was duplicated or removed" }')
    build = build.replace("silu_eram_", "all_eram_").replace(
        "# and all TD check types: setup, hold, recovery, and removal.",
        "# with applicable register-to-register setup/hold; reset checks are separate.")
    build = build.replace("close_project", 'puts "REPORT_COMPLETION_DONE"\nclose_project')
    (work / "build.tcl").write_text(build, encoding="utf-8")
    command([sys.executable, "-B", work / "physical_report.py", "preflight"], work, "preflight")
    tool = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
    save(work / "tool_hash.json", {str(tool): sha(tool), "constraint_unchanged":
         {name: sha(work / name) == sha(old / name) for name in ("frontend.sdc", "frontend.adc")}})
    save(ROOT / "status.json", {"stage": "TD_IMPLEMENTATION_RUNNING", "functional": "PASS",
         "strict_gate": "NOT_CLOSED", "not_deployment": True})
    output = command([tool, "build.tcl"], work, "td_launcher")
    assert "REPORT_COMPLETION_DONE" in output, "TD returncode alone does not prove completion"
    assert 'finish command "route"' in output
    shared.check()


def stem_gate():
    shared.check()
    work = shared.fresh("stem_gate")
    entry = f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, shared.STEM,
             "--json", work / "stem.json", "--markdown", work / "stem.md"], work, "stem", allowed=(0, 1, 2))


def finish():
    shared.finish()
    # shared.finish保留原有完整向量/源哈希检查，物理状态取本轮实际新实现。
    summary = ROOT / "physical_summary.json"
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    if summary.exists():
        physical_result = json.loads(summary.read_text(encoding="utf-8"))
        status.update({"status": physical_result["status"], "physical": physical_result})
    elif (ROOT / "physical/td_launcher.log").exists():
        status["status"] = "FUNCTIONAL_PASS_PHYSICAL_RESULT_PENDING"
    save(ROOT / "status.json", status)

    # status覆盖后刷新收据，避免沿用shared.finish中较早的状态哈希。
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in sorted(ROOT.rglob("*"))
         if path.is_file() and path.name != "artifact_manifest.json" and path.suffix not in (".wlf", ".pyc")
         and "work" not in path.relative_to(ROOT).parts})


def evidence():
    shared.check()
    old = (shared.BASE / "rtl/road_stem_tile_scheduler.v").read_text(encoding="utf-8")
    new = shared.STEM.read_text(encoding="utf-8")
    declaration = "\treg [8:0]next_weight_base[0:2]; // 六组合法输出通道的OIHW基址，不使用地址乘法器。\n"
    start = new.index("\t// 每路基址是输出通道乘27")
    end = new.index("\t// 27 项按 OIHW", start)
    reconstructed = (new[:start] + new[end:]).replace(declaration, "").replace(
        "reg_weight[next_weight_base[output_lane]+{4'd0,term[4:0]}]",
        "reg_weight[(cnt_channel+output_lane)*27+term]")
    assert reconstructed == old, "地址以外逻辑不得改变"
    for name in ("road_frontend_shared_core.v", "road_down2_tile_scheduler.v"):
        assert sha(ROOT / "rtl" / name) == sha(PREVIOUS / "rtl" / name)
    for source in (PREVIOUS / "tests").iterdir():
        if source.is_file():
            assert sha(ROOT / "tests" / source.name) == sha(source)
    cycles = json.loads((ROOT / "cycle_summary.json").read_text(encoding="utf-8"))
    assert cycles == json.loads((PREVIOUS / "cycle_summary.json").read_text(encoding="utf-8"))
    gates = {}
    for name, path in (("stem_before", ROOT / "baseline_gate/stem.json"),
                       ("stem_after", ROOT / "stem_gate/stem.json"),
                       ("rtl_closure", ROOT / "gate/rtl.json"), ("testbenches", ROOT / "gate/tests.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        gates[name] = {"raw_report": str(path.relative_to(ROOT)), "sha256": sha(path),
                       **{key: data[key] for key in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}}
    save(ROOT / "strict_summary.json", gates)
    save(ROOT / "surgical_check.json", {"status": "PASS", "only_weight_address_changed": True,
        "top_down2_tests_unchanged": True, "cycles_entire_dictionary_unchanged": True,
        "frozen_file_count": len(json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))),
        "limitations": ["严格门未闭合", "无端口TB的canonical规格生成不支持；失败保留并提供人工契约",
                        "readable-python/script技能不可用，Python AST不代替其门禁"]})
    print("SURGICAL_SCOPE_AND_CYCLES_PASS", flush=True)


def undriven():
    shared.check()
    work = shared.fresh("undriven")
    project = (ROOT / "physical/road_frontend_shared_core.al").read_text(encoding="utf-8")
    (work / "road_frontend_shared_core.al").write_text(project.replace(
        (ROOT / "physical").as_posix(), work.as_posix()), encoding="utf-8")
    shutil.copyfile(PREVIOUS / "undriven/inspect.tcl", work / "inspect.tcl")
    output = command(["E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe",
                      "inspect.tcl"], work, "inspect")
    assert "MODEL_QUERY_DONE" in output
    records = re.findall(r"DEAD_RECORD (\S+) PINS (\d+) DRIVER (\d+)", output)
    assert records, "不能用空查询证明未驱动不存在"
    connected = [record for record in records if int(record[1]) != 0]
    save(work / "receipt.json", {"status": "NO_CONNECTED_ZERO_DRIVER_NET_IN_QUERY" if not connected else "UNRESOLVED",
         "net_count": len(records), "connected_zero_driver_nets": connected,
         "limitation": "查询只覆盖可见展开网；厂商可选原语dummy端点及严格门禁仍未宣称闭合。"})
    assert not connected, connected
    shared.check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "baseline", "stem_gate", "reference", "specifications", "check", "gate", "simulate", "physical", "finish", "evidence", "undriven"))
    action = parser.parse_args().action
    (globals().get(action) or getattr(shared, action))()
