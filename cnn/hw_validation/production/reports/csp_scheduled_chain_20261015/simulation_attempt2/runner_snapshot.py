"""接通固定任务调度、单事务取数及真实计算；保留所有旧版本。"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "csp_dw_cache_20261015"
SCHEDULE = ROOT.parent / "csp_tile_schedule_20261015"
VECTORS = ROOT.parent / "qat_g10_csp_first_closure_20261015_v2/vectors"
spec = importlib.util.spec_from_file_location("scheduled_existing_tools", SCHEDULE / "run.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
sha, save, fresh, command, check = tools.sha, tools.save, tools.fresh, tools.command, tools.check

PORTS = [
    ("i_clk", "input", 1, "同域100MHz时钟"), ("i_rstn", "input", 1, "共同异步取消，释放由现顶层保证"),
    ("i_start", "input", 1, "与start_ready握手启动一个固定tile"),
    ("i_table_valid", "input", 1, "仅空闲时允许顺序装表，启动与装表互斥"),
    ("i_table_addr", "input", 10, "原1024项表地址"), ("i_table_data", "input", 16, "原signed16表值"),
    ("o_start_ready", "output", 1, "表已满且完全空闲时允许启动"),
    ("o_table_ready", "output", 1, "真实装表准入"), ("o_table_loaded", "output", 1, "核的完整装表许可"),
    ("o_busy", "output", 1, "当前tile占有"), ("o_done", "output", 1, "所有任务末路提交后完成"),
    ("o_fault", "output", 1, "核/缓存/描述符故障，仅共同复位恢复"),
    ("o_operand_request_valid", "output", 1, "单个取数请求，保持到ready"),
    ("i_operand_request_ready", "input", 1, "取数端接收请求"),
    ("o_operand_request_descriptor", "output", 25, "沿冻结task/pw/y/x/channel/first/last/mask布局"),
    ("i_operand_response_valid", "input", 1, "取数响应，保持全部载荷到ready"),
    ("o_operand_response_ready", "output", 1, "已登记请求且尚未保存响应"),
    ("i_operand_response_descriptor", "input", 25, "必须回显当前唯一请求，失配置错不计算"),
    ("i_operand_activation", "input", 64, "仅DW采用；PW忽略此字段而读取实际缓存"),
    ("i_operand_weight", "input", 192, "三路八输入权重"), ("i_operand_bias", "input", 96, "三路INT32偏置"),
    ("i_operand_pre_multipliers", "input", 96, "三路真实前乘数"), ("i_operand_pre_shifts", "input", 18, "三路六位移位"),
    ("i_operand_post_multiplier", "input", 32, "当前层后乘数"), ("i_operand_post_shift", "input", 6, "当前层后移位"),
    ("i_operand_bypass", "input", 24, "PW残差三路原输入旁路"), ("i_operand_fault", "input", 1, "首组输入故障标志"),
    ("i_result_ready", "input", 1, "结果接收端的真实ready"),
    ("o_result_valid", "output", 1, "与DW缓存原子提交的结果valid"), ("o_result_data", "output", 8, "真实INT8结果"),
    ("o_result_tag", "output", 16, "RTL根据任务坐标派生的tag"), ("o_result_address", "output", 32, "冻结逻辑字节地址"),
    ("o_result_sum", "output", 9, "真实残差饱和前和"),
    ("o_group_accept", "output", 1, "MAC真实接收一组"), ("o_task_commit", "output", 1, "当前任务最后一路已实际提交"),
    ("o_request_accept", "output", 1, "取数请求真实接受"), ("o_cache_read_accept", "output", 1, "PW缓存请求真实接受"),
    ("o_cache_write_accept", "output", 1, "DW缓存字节真实接受"),
    ("o_cycle_reason", "output", 3, "0空闲/1MAC发射/2请求阶段/3响应等待接收/4缓存等待/5MAC等待/6写端反压/7其他流水提交")
]


def setup():
    assert not (ROOT / "frozen.json").exists()
    inputs = list(BASE.joinpath("reused").glob("*.v")) + [BASE / "rtl/road_csp_dw_cache.v", BASE / "run.py",
        BASE / "status.json", BASE / "simulation_attempt5/receipt.json", BASE / "artifact_manifest.json",
        SCHEDULE / "rtl/road_csp_tile_schedule.v", SCHEDULE / "run.py", SCHEDULE / "status.json"]
    inputs += list(VECTORS.glob("*.hex"))
    save(ROOT / "frozen.json", {str(p): sha(p) for p in inputs})
    for folder in ("rtl", "reused", "tests"):
        (ROOT / folder).mkdir(exist_ok=True)
    for path in BASE.joinpath("reused").glob("*.v"):
        shutil.copyfile(path, ROOT / "reused" / path.name)
    shutil.copyfile(SCHEDULE / "rtl/road_csp_tile_schedule.v", ROOT / "reused/road_csp_tile_schedule.v")
    shutil.copyfile(BASE / "rtl/road_csp_dw_cache.v", ROOT / "rtl/road_csp_dw_cache.v")
    save(ROOT / "interface.json", {"module": "road_csp_scheduled_chain", "ports": [
        {"name": n, "direction": d, "width": w, "description": desc} for n, d, w, desc in PORTS],
        "instance_names": {"wrapper": "u_compute", "scheduler": "u_schedule", "cache": "u_cache"},
        "descriptor": "[24:17]task,[16]pw,[15:14]y,[13:12]x,[11:8]channel,[7]first,[6]last,[5:3]mask,[2:0]zero",
        "provider": "one request outstanding; response descriptor echo; reset requires provider cancel; no DDR late returns",
        "cache_clear": "new cache candidate i_clear, synchronous, only idle tile boundary; sticky fault still reset-only",
        "result_addresses": {"dw": 56532992, "residual": 56643584}})
    save(ROOT / "requirements.json", {"classification": ["generate", "modify", "validate"], "baseline_commit": "366a471d",
         "scope": "hardware task and completion control, external same-clock operand provider, not DDR/ROM implementation",
         "codegen_plan": ["freeze", "Python schedule/join reference", "spec", "one-outstanding response adapter",
                          "derive tag/address", "cache local clear", "actual arithmetic regression", "strict gates"],
         "unchanged": ["scheduler source", "arithmetic source", "wrapper", "numeric contract", "MAC II", "production"],
         "public_gates": ["compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"]})
    check()


def review():
    work = fresh("review")
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "review",
             "--target", BASE / "rtl/road_csp_dw_cache.v", "--report-json", work / "original_cache.json"],
            work, "original_cache", allowed=(0, 1, 2))
    check()


def specs(crosscheck_sources=True):
    work = fresh("sp")
    module = {"name": "road_csp_scheduled_chain", "rtl_path": "road_csp_scheduled_chain.v", "feature": "scheduled_csp",
              "description": "固定首残差硬件调度及单事务取数；参数/halo端为内部provider，不是外设接口",
              "interfaces": {"protocol": "discrete", "ports": [dict(name=n, direction=d, width=w, role="native",
                  description=desc, clock_domain="i_clk") for n, d, w, desc in PORTS]},
              "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
              "reset": {"name": "i_rstn", "active": "low", "synchronous": False}, "parameters": [],
              "behavior": ["160任务/320组由冻结调度器产生；一笔取数在途，响应与PW缓存数据各锁存，齐备才送原核。",
                           "PW输入忽略provider activation，来自真实DW缓存；tag/逻辑地址由RTL坐标计算。",
                           "三路或单路结果全部实际提交才task_done；每次tile开始局部清缓存，不复位核或重装SiLU。",
                           "共同reset取消所有暂存；provider必须共同取消旧响应，本接口不能直接接DDR晚返回。"],
              "constraints": ["不改核端口/数值/II；串行请求适配可能增加组间间隔，按端点周期测量而不冒称II加速。",
                              "提供者在空闲装表时具有优先级，忙时装表不被接受；仅单上下文，不新增队列或外设。"],
              "corner_cases": ["响应先于/晚于缓存、长结果反压、首末组、1/3路提交、reset、双tile及失配响应。"],
              "verification_cases": ["实际acc/pre/SiLU/post/sum/地址/输出；随机provider与反压；故障及reset；旧回归单列。"],
              "timing_diagrams": [{"id": "join", "scenario": "join", "title": "取数与PW缓存汇合再发射",
                  "description": "同一个请求对应两路锁存；MAC真实接受后才推进组。",
                  "wavejson": {"signal": [{"name": "clk", "wave": "p......."}, {"name": "request_accept", "wave": "010....."},
                      {"name": "cache_capture", "wave": "0.10...."}, {"name": "payload_capture", "wave": "0...10.."},
                      {"name": "mac_accept", "wave": "0....10."}, {"name": "next_request", "wave": "0.....10"}]}}]}
    cache_template = sorted(BASE.glob("specifications*/road_csp_dw_cache.json"))[-1]
    cache = json.loads(cache_template.read_text(encoding="utf-8"))["modules"][0]
    cache["interfaces"]["ports"].insert(2, {"name": "i_clear", "direction": "input", "width": 1, "role": "native",
        "clock_domain": "i_clk", "description": "只在tile空闲边界同步清有效状态，不清RAM、不清sticky fault"})
    cache["behavior"].append("i_clear期间禁止接受读写，沿后清count/有效位/响应；fault只能共同reset清除。")
    cache["constraints"] = ["i_clear仅由空闲调度边界产生，不能取消在途计算或模拟DDR排空。"]
    tb = json.loads((BASE / "specifications_attempt3/tb_csp_first_probe.json").read_text(encoding="utf-8"))["modules"][0]
    tb.update(name="tb_csp_scheduled_chain", rtl_path="tb_csp_scheduled_chain.v", description="TB只做取数服务与结果比对，不逐任务驱动")
    tb["interfaces"]["ports"][0]["name"] = "o_test_done"
    for data, folder, crosscheck in ((module, "rtl", True), (cache, "rtl", True), (tb, "tests", False)):
        name = data["name"]
        output_name = "chain" if name == "road_csp_scheduled_chain" else "cache" if name == "road_csp_dw_cache" else "tb"
        path = work / (name + ".json")
        save(path, {"modules": [data]})
        argv = [sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "write-spec",
                "--spec", path, "--out-dir", work / output_name, "--no-state"]
        if crosscheck_sources and crosscheck and (ROOT / folder / (name + ".v")).exists(): argv += ["--source", ROOT / folder / (name + ".v")]
        command(argv, ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / output_name / "spec" / data["feature"]
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / folder / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / folder / "waveforms", dirs_exist_ok=True)
    check()


def simulate():
    check()
    ref = json.loads((ROOT / "reference/receipt.json").read_text(encoding="utf-8"))
    assert ref["status"] == "PASS" and sha(ROOT / "reference.py") == ref["source_sha256"]
    assert all(sha(p) == digest for p, digest in ref["input_sha256"].items())
    assert all(sha(ROOT / "reference" / p) == digest for p, digest in ref["output_sha256"].items())
    work = fresh("simulation")
    snapshots = work / "sources"
    snapshots.mkdir()
    sources = [p for folder in ("rtl", "tests", "reused") for p in (ROOT / folder).glob("*.v")]
    for path in sources: shutil.copyfile(path, snapshots / path.name)
    vendor = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
    actual = sorted(snapshots.glob("*.v")) + [vendor / "ph1p_logic_eram.v", vendor / "ph1p_phy_gsr.v"]
    manifest = {str(p): sha(p) for p in [*sources, *actual, *VECTORS.glob("*.hex"), *ROOT.joinpath("reference").glob("*.hex"),
                ROOT / "run.py", ROOT / "interface.json", ROOT / "reference.py", ROOT / "reference/receipt.json"]}
    save(work / "input_manifest.json", manifest)
    shutil.copyfile(ROOT / "run.py", work / "runner_snapshot.py")
    command([tools.MSIM / "vlib.exe", "work"], work, "vlib")
    output = command([tools.MSIM / "vlog.exe", "-work", "work", *actual], work, "vlog")
    assert "Errors: 0, Warnings: 0" in output, output
    results = {}
    for case in range(8):
        name = "case_" + str(case)
        output = command([tools.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_scheduled_chain",
            "+CASE=" + str(case), "+VECTORS=" + VECTORS.as_posix(), "+REFERENCE=" + (ROOT / "reference").as_posix(),
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name)
        failures = [line for line in output.splitlines() if "** Fatal:" in line or "** Error:" in line or "Failed to open readmem" in line]
        assert not failures, (name, failures, str(work / (name + ".log")))
        assert "CSP_SCHEDULED_EXPECTED_FAULT" in output if case >= 5 else "CSP_SCHEDULED_PASS" in output
        results[name] = [line for line in output.splitlines() if "CSP_SCHEDULED" in line]
    assert all(sha(p) == digest for p, digest in manifest.items())
    save(work / "receipt.json", {"status": "PASS", "results": results, "manifest_sha256": sha(work / "input_manifest.json"),
         "actual_arithmetic": True, "hardware_task_scheduler": True, "operand_provider": "TB, not ROM/DDR", "physical_run": False})
    check()


def gate():
    work = fresh("gate")
    for name, folders in (("candidate", ("rtl",)), ("full", ("rtl", "tests", "reused"))):
        closure = work / name
        for folder in folders:
            (closure / folder).mkdir(parents=True)
            for path in (ROOT / folder).glob("*.v"): shutil.copyfile(path, closure / folder / path.name)
        argv = [sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.validation.generated_deliverable_gate"),
                closure, "--json", work / (name + ".json"), "--markdown", work / (name + ".md")]
        if name == "full": argv.append("--include-testbench")
        command(argv, work, name, allowed=(0, 1))
    check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "review", "intent", "specs", "simulate", "gate", "check", "dependency"))
    action = parser.parse_args().action
    if action == "dependency": tools.dependency()
    elif action == "intent": specs(False)
    else: globals()[action]()
