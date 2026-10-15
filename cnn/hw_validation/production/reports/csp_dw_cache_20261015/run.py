"""固定首残差DW缓存及真实计算回归；旧调度和算术核保持不变。"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "csp_tile_schedule_20261015"
BASE = ROOT.parent / "qat_g10_csp_first_closure_20261015_v2"
spec = importlib.util.spec_from_file_location("csp_existing_tools", PREVIOUS / "run.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)
tools.ROOT = ROOT
sha, save, fresh, command, check = tools.sha, tools.save, tools.fresh, tools.command, tools.check


def setup():
    assert not (ROOT / "frozen.json").exists()
    paths = [BASE / name for name in ("status.json", "input_binding.json", "execution_checks.json", "spec_contract.json")]
    paths += list(BASE.joinpath("rtl").glob("*.v")) + list(BASE.joinpath("reused").glob("*.v"))
    paths += list(BASE.joinpath("vectors").glob("*.hex"))
    paths += [BASE / "tests/tb_csp_first_probe.v", PREVIOUS / "run.py", PREVIOUS / "rtl/road_csp_tile_schedule.v",
              PREVIOUS / "status.json", PREVIOUS / "simulation_attempt6/receipt.json"]
    save(ROOT / "frozen.json", {str(p): sha(p) for p in paths})
    (ROOT / "reused").mkdir(exist_ok=True)
    for folder in ("rtl", "reused"):
        for path in (BASE / folder).glob("*.v"):
            shutil.copyfile(path, ROOT / "reused" / path.name)
    save(ROOT / "requirements.json", {"classification": ["generate", "validate"], "baseline_commit": "a40e50d4",
         "scope": "192 logical-byte DW output cache with PW read adapter; task/halo/parameters still TB",
         "physical_layout": "8 banks x 32 rows; bank=c%8,row=pixel*2+c//8;256 allocated bytes,192 valid",
         "phases": ["capture 192 unique DW output accepts", "read immutable PW groups", "common reset before reuse"],
         "contracts": ["no read before all unique DW values stored", "one-clock registered response and elastic slot",
                       "duplicate/out-of-range write causes sticky fault", "reset cancels validity, no RAM power-up dependence"],
         "unchanged": ["arithmetic core", "wrapper", "scheduler", "MAC II", "numerical contract", "production"],
         "codegen_plan": ["Python bank model", "interface spec", "banked RTL", "unit stress tests", "17 actual arithmetic regressions"],
         "public_gates": ["compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"]})
    check()


def specs():
    work = fresh("specifications")
    ports = [("i_clk", "input", 1, "100MHz同域时钟"), ("i_rstn", "input", 1, "共同异步取消，释放由现顶层保证"),
             ("i_write_valid", "input", 1, "DW实际结果写请求，保持到接受"),
             ("i_write_index", "input", 8, "DW局部HWC索引0..191，非法索引被接受后置错但不写内存"),
             ("i_write_data", "input", 8, "真实DW INT8输出"), ("o_write_ready", "output", 1, "采集阶段且健康时允许写"),
             ("o_loaded", "output", 1, "全部192个不同地址已被接收"), ("o_write_count", "output", 8, "唯一有效写计数0..192"),
             ("o_fault", "output", 1, "重复/越界写粘滞故障，共同复位清除"),
             ("i_read_valid", "input", 1, "PW组读请求，保持到ready"), ("i_read_pixel", "input", 4, "4×4局部pixel索引"),
             ("i_read_group", "input", 1, "0=通道0..7；1=通道8..11及四零lane"),
             ("o_read_ready", "output", 1, "完整采集且响应槽可容纳才接受"), ("i_output_ready", "input", 1, "PW操作数端真实接受"),
             ("o_output_valid", "output", 1, "读响应一槽，反压保持"), ("o_output_data", "output", 64, "8个低字节优先INT8"),
             ("o_output_mask", "output", 8, "ff或0f，末组四零lane"),
             ("o_output_pixel", "output", 4, "与载荷同步的pixel"), ("o_output_group", "output", 1, "与载荷同步的组号")]
    timing = {"id": "read", "scenario": "read", "title": "完整采集后注册读取及响应保持",
              "description": "最后一字节写入之后开放读，接受读的上升沿后产生响应；停顿时数据和元数据保持。",
              "wavejson": {"signal": [{"name": "clk", "wave": "p......"}, {"name": "loaded", "wave": "01....."},
                  {"name": "read_valid", "wave": "0.10..."}, {"name": "output_valid", "wave": "0..1..0"},
                  {"name": "output_ready", "wave": "0....1."}, {"name": "output_data", "wave": "x..=..x", "data": ["held group"]}]}}
    module = {"name": "road_csp_dw_cache", "feature": "csp_cache", "rtl_path": "road_csp_dw_cache.v",
              "description": "固定首残差DW→PW八bank缓存，不含DDR或算术",
              "interfaces": {"protocol": "discrete", "ports": [{"name": n, "direction": d, "width": w,
                  "role": "native", "description": desc, "clock_domain": "i_clk"} for n, d, w, desc in ports]},
              "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
              "reset": {"name": "i_rstn", "active": "low", "synchronous": False}, "parameters": [],
              "behavior": ["采集阶段只写不读，全部192个唯一结果到齐后只读不写。",
                           "每读请求一个上升沿后产生64bit注册响应；一槽可同拍出入。",
                           "reset清有效位/计数/响应，不清RAM；恢复后必须完整重写，禁止旧响应泄漏。"],
              "constraints": ["仅4×4×12单tile；跨tile复用必须共同复位，本轮不引入epoch/DMA协议。",
                              "256物理字节中仅192有效；写读阶段互斥，不依赖同址碰撞或上电内容。"],
              "corner_cases": ["最后一字节、索引191/192/255、重复写、请求/响应停顿、复位中断。"],
              "verification_cases": ["32组数据对拍、随机写序、长响应反压、未满不读、故障及复位；17项真实计算回归。"],
              "timing_diagrams": [timing]}
    cases = [(module, "rtl", True)]
    # 原TB有task端口，源码解析仍单列；同名规格只声明已确认的真实顶层完成端口。
    for name, port in (("tb_csp_dw_cache", "o_test_done"), ("tb_csp_first_probe", "o_test_complete")):
        cases.append(({"name": name, "feature": "csp_cache_test", "rtl_path": name + ".v",
            "description": "缓存握手及实际计算回归，不是整网或DDR验收",
            "interfaces": {"protocol": "discrete", "ports": [{"name": port, "direction": "output", "width": 1,
                "role": "test_complete", "description": "全部检查通过后置位", "clock_domain": "clk"}]},
            "clock": {"name": "clk", "edge": "posedge", "frequency_hz": 100000000, "internal": True},
            "reset": {"name": "rstn", "active": "low", "synchronous": False, "internal": True},
            "parameters": [], "behavior": module["behavior"], "constraints": ["仅测试，不可综合"],
            "corner_cases": module["corner_cases"], "verification_cases": module["verification_cases"],
            "timing_diagrams": [timing]}, "tests", False))
    for data, folder, crosscheck in cases:
        name = data["name"]
        path = work / (name + ".json")
        save(path, {"modules": [data]})
        args = [sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"),
                "write-spec", "--spec", path, "--out-dir", work / name, "--no-state"]
        if crosscheck and (ROOT / folder / (name + ".v")).exists():
            args += ["--source", ROOT / folder / (name + ".v")]
        command(args, ROOT, str(work.relative_to(ROOT) / name))
        target = ROOT / folder
        target.mkdir(exist_ok=True)
        bundle = work / name / "spec" / data["feature"]
        shutil.copyfile(bundle / (name + "_spec.md"), target / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", target / "waveforms", dirs_exist_ok=True)
    check()


def simulate(cases=None):
    check()
    ref = json.loads((ROOT / "reference/receipt.json").read_text(encoding="utf-8"))
    assert ref["status"] == "PASS"
    assert sha(ROOT / "reference.py") == ref["source_sha256"]
    assert all(sha(ROOT / p) == digest for p, digest in ref["inputs"].items())
    assert all(sha(ROOT / "reference" / p) == digest for p, digest in ref["artifacts"].items())
    work = fresh("simulation")
    snapshots = work / "sources"
    snapshots.mkdir()
    sources = list(ROOT.joinpath("rtl").glob("*.v")) + list(ROOT.joinpath("tests").glob("*.v")) + list(ROOT.joinpath("reused").glob("*.v"))
    for path in sources:
        shutil.copyfile(path, snapshots / path.name)
    vendor = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
    actual = sorted(snapshots.glob("*.v")) + [vendor / "ph1p_logic_eram.v", vendor / "ph1p_phy_gsr.v"]
    manifest = {str(p): sha(p) for p in [*sources, *actual, *ROOT.joinpath("reference").glob("*.hex"),
                *BASE.joinpath("vectors").glob("*.hex"), ROOT / "run.py", ROOT / "reference.py", ROOT / "reference/receipt.json"]}
    shutil.copyfile(ROOT / "run.py", work / "runner_snapshot.py")
    save(work / "input_manifest.json", manifest)
    for path in (ROOT / "reused").glob("*.v"):
        original = BASE / ("rtl" if path.name == "road_csp_first_probe.v" else "reused") / path.name
        assert sha(path) == sha(original), (path, "frozen dependency changed")
    command([tools.MSIM / "vlib.exe", "work"], work, "vlib")
    text = command([tools.MSIM / "vlog.exe", "-work", "work", *actual], work, "vlog")
    assert "Errors: 0, Warnings: 0" in text, text
    results = {}
    for case in (range(-1, 18) if cases is None else cases):
        top = "tb_csp_dw_cache" if case == -1 else "tb_csp_first_probe"
        vectors = ROOT / "reference" if case == -1 else BASE / "vectors"
        name = "cache_unit" if case == -1 else "case_" + str(case)
        output = command([tools.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top,
             "+CASE=" + str(case), "+VECTORS=" + vectors.as_posix(), "-do",
             "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, name)
        expected = "TB_PASS_CSP_DW_CACHE" if case == -1 else "CSP_FIRST_EXPECTED_FAULT" if case in (6, 7, 8, 12, 13) else "CSP_FIRST_PASS"
        failures = [line for line in output.splitlines() if "** Fatal:" in line or "** Error:" in line or "Failed to open readmem" in line]
        assert not failures, (name, failures, str(work / (name + ".log")))
        assert expected in output, (name, output[-4000:])
        if case >= 0 and case not in (6, 7, 8, 12, 13):
            receipt = re.search(r"CSP_FIRST_PASS case=(\d+) generation=(\d+) groups=(\d+) tasks=(\d+) outputs=(\d+) acc=(\d+) pre=(\d+) silu=(\d+) post=(\d+) sums=(\d+) cycles=(\d+)", output)
            assert receipt, name
            values = list(map(int, receipt.groups()))
            assert values[0] == case and values[1] == (2 if case in (3, 4, 5, 11, 14, 17) else 1), values
            expected_counts = [12, 6, 16, 16, 16, 16, 16, 16] if case in (9, 15) else [320, 160, 384, 384, 384, 384, 384, 192]
            assert values[2:10] == expected_counts, values
        elif case >= 0:
            assert f"CSP_FIRST_EXPECTED_FAULT case={case} outputs=0" in output, name
        results[name] = [line for line in output.splitlines() if "CSP_" in line]
    assert all(sha(p) == digest for p, digest in manifest.items())
    save(work / "receipt.json", {"status": "PASS", "results": results, "input_manifest_sha256": sha(work / "input_manifest.json"),
         "actual_arithmetic_executed": True, "DDR_executed": False, "hardware_scheduler_integrated": False})
    check()


def review():
    work = fresh("review")
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.workflow.cli"), "review",
             "--target", BASE / "tests/tb_csp_first_probe.v", "--report-json", work / "frozen_tb.json"],
            work, "frozen_tb", allowed=(0, 1, 2))
    check()


def finalize():
    check()
    sim = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    simulation = json.loads(sim.read_text(encoding="utf-8"))
    assert simulation["status"] == "PASS" and len(simulation["results"]) == 19
    gate_path = sorted(ROOT.glob("gate*/full.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    strict = {}
    for name in ("cache", "full"):
        data = json.loads((gate_path / (name + ".json")).read_text(encoding="utf-8"))
        strict[name] = {"errors": data["errors"], "strict_warnings": data["strict_warnings"],
                        "delivery_ready": data["delivery_ready"], "checks": data["checks"]}
    save(ROOT / "strict_summary.json", strict)
    baseline = json.loads((BASE / "status.json").read_text(encoding="utf-8"))
    comparison = {}
    for case in baseline["cases"]:
        old = re.search(r"cycles=(\d+)", case["receipt"])
        new = re.search(r"cycles=(\d+)", "\n".join(simulation["results"]["case_" + str(case["case"])]))
        if old and new:
            comparison[str(case["case"])] = {"baseline": int(old[1]), "cache": int(new[1]), "delta": int(new[1])-int(old[1])}
    save(ROOT / "cycle_comparison.json", {"cases": comparison,
         "scope": "same frozen arithmetic/vectors, TB driven task and cache handshake; not pure hardware scheduler",
         "normal_delta": "128 PW cache reads x3 extra serial TB clocks=384; random case has shifted LFSR phase, not identical stall replay"})
    save(ROOT / "status.json", {"status": "CACHE_AND_18_ARITHMETIC_REGRESSIONS_PASS_NOT_DELIVERY_READY",
         "simulation_receipt": str(sim.relative_to(ROOT)), "logical_bytes": 192, "physical_bytes": 256,
         "original_cases": 17, "new_backpressure_cases": 1, "cache_unit_pass": True,
         "actual_DW_writes": 192, "actual_PW_reads": 128, "arithmetic_and_wrapper_changed": False,
         "scheduler_integrated": False, "DDR_executed": False, "synthesis_run": False,
         "production_delivery_ready": False, "normal_cycles": comparison["0"],
         "remaining": ["strict control/readability gates", "hardware operand adapter and task completion binding",
                       "local cache reuse without whole-core reset", "integrated physical implementation", "full graph/DDR"]})
    paths = [p for p in ROOT.rglob("*") if p.is_file() and "work" not in p.parts and p.name != "artifact_manifest.json"
             and "__pycache__" not in p.parts]
    save(ROOT / "artifact_manifest.json", {str(p.relative_to(ROOT)): sha(p) for p in paths})


def gate():
    work = fresh("gate")
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.validation.generated_deliverable_gate"),
             ROOT / "rtl", "--json", work / "cache.json", "--markdown", work / "cache.md"], work, "cache", allowed=(0, 1))
    closure = work / "closure"
    for folder in ("rtl", "tests", "reused"):
        (closure / folder).mkdir(parents=True)
        for path in (ROOT / folder).glob("*.v"):
            shutil.copyfile(path, closure / folder / path.name)
    command([sys.executable, "-B", "-X", "utf8", "-c", tools.entry("scripts.python.validation.generated_deliverable_gate"),
             closure, "--include-testbench", "--json", work / "full.json", "--markdown", work / "full.md"], work, "full", allowed=(0, 1))
    check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "dependency", "specs", "simulate", "simulate_focus", "gate", "check", "review", "finalize"))
    action = parser.parse_args().action
    if action == "dependency": tools.dependency()
    elif action == "simulate_focus": simulate([17])
    else: globals()[action]()
