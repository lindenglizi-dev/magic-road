"""单算术链前端验证；只写本目录，不修改旧核、生产和训练。"""
import argparse
import ast
import csv
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "stem_down2_handoff_20261011"
spec = importlib.util.spec_from_file_location("full_helpers", ROOT.parent / "down2_full_tensor_20261010/run.py")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
helpers.ROOT = ROOT
save, sha, fresh, command = helpers.save, helpers.sha, helpers.fresh, helpers.command
STEM = BASE / "rtl/road_stem_tile_scheduler.v"
VECTORS = BASE / "vectors"


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in records.items() if sha(Path(name)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def freeze():
    assert not (ROOT / "frozen.json").exists(), "不覆盖冻结清单"
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    paths = [*helpers.CORE.glob("*.v"), *VECTORS.iterdir(), STEM, BASE / "status.json",
             BASE / "cycle_summary.json", BASE / "artifact_manifest.json", BASE / "reference.json",
             BASE / "tests/tb_stem_down2.v", BASE / "tests/stem_driver.vh",
             ROOT.parent / "down2_full_tensor_20261010/run.py", helpers.MSIM / "vlog.exe", helpers.MSIM / "vsim.exe"]
    records.update({str(path): sha(path) for path in paths if path.is_file()})
    save(ROOT / "frozen.json", records)
    check()


def gate():
    check()
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    for folder in ("rtl", "tests"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / folder,
                 "--include-testbench", "--external-interface-source", helpers.CORE,
                 "--external-interface-source", STEM,
                 "--json", work / (folder + ".json"), "--markdown", work / (folder + ".md")],
                work, folder, allowed=(0, 1, 2))
    check()


def specifications():
    check()
    work = fresh("specifications")
    entry = f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    for source in sorted((ROOT / "rtl").glob("*.v")):
        ports = [{"name": name, "direction": direction, "width": int(high) + 1 if high else 1,
                  "clock_domain": "i_clk", "role": name,
                  "description": "单时钟固定前端接口；有效负载保持到ready，完整表和参数后才能计算；复位立即取消。"}
                 for direction, high, name in re.findall(
                     r"\b(input|output)\s+(?:signed\s+)?(?:\[(\d+):0\])?\s*(\w+)\s*[,\n]", source.read_text(encoding="utf-8"))]
        module = {"name": source.stem, "feature": "shared_frontend", "rtl_path": source.name,
                  "description": "冻结Stem/down2调度对唯一MAC及动态后处理的互斥共享，不含DDR和整帧存储。",
                  "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
                  "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
                  "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                            "values": "立即取消在途及所有loaded状态；调用者同步释放；重新装满1024项表与参数。"},
                  "behavior": ["Stem4×4×16，down2 DW4×4×16再PW4×4×24，原数值、算术核和II不变。",
                               "共享顶层owner只在两个调度器空闲、算术排空且结果导出完成时切换；未导出结果禁止覆盖。",
                               "表只装一次后可切换算子；复位后不允许继续使用旧表。",
                               "顺序装载由各调度器按既有kind编码验证，数据必须保持直至ready；故障只可复位恢复。"],
                  "constraints": ["独立功能候选，TEST_ONLY动态系数；没有部署QAT或真实DDR完成语义。",
                                  "不声称全网5FPS或生产时序通过；本次不增加任务重叠。"],
                  "corner_cases": ["部分表和halo、尾lane、未导出交接、背压、复位取消、非法装载。"],
                  "verification_cases": ["同冻结2304Stem及576down2全量阶段/缓存读口比较；单算术链共享。"],
                  "timing_diagrams": [{"id": "handoff", "title": "排空后切换", "scenario": "handoff",
                      "description": "压缩示意；busy和未导出均阻止切换，导出完成后的空闲拍允许握手。",
                      "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
                          {"name": "busy", "wave": "1.0....."}, {"name": "unexported", "wave": "0.1..0.."},
                          {"name": "select_valid", "wave": "0.....10"}, {"name": "select_ready", "wave": "0.....1."},
                          {"name": "owner_down2", "wave": "0......1"}]}}]}
        if source.stem == "road_frontend_shared_core":
            module["behavior"].extend([
                "选择请求允许在busy时保持valid到ready；旧主继续排空及导出。done同拍也禁止换主。",
                "装表请求可提前等待；只有实际空闲准入后的table_valid才进入后处理，不以原始valid阻断PP。",
                "装载/start/export优先于装表，装表优先于选择；选择valid未握手不封锁旧主命令。",
                "公共Stem地址超过511置粘滞fault，不截断为9位；完成后导出前禁止新装载/start。",
            ])
        else:
            module["description"] = "冻结down2调度器的机械提取，MAC及PP外置；调度、缓存、计数主体不变。"
            module["behavior"] = [
                "仅IDLE装载：kind0 halo1296，kind1 PW-only缓存256，kind2 DW权重144，kind3 DW偏置16。",
                "kind4 PW权重384，kind5 PW偏置24，kind6 pre乘数40，kind7 controls44，必须完整顺序装载。",
                "DW按同通道三相邻空间点映射，三组输入；PW按三输出通道两组输入；保留四项归约所有权环。",
                "o_pp_tags按{layer,position,channel,6'b0}编码，shape故障与MAC故障沿原adapter转送。",
                "输出已激活INT8；取i_pp_data低8位写真实DW/output缓存；完整384项PW结果才发布。",
                "PP的i_pp_meta_count是pending/retirement数，不是SiLU元数据队列数；busy计数与重叠忙计数分别保留。",
            ]
        contract = work / (source.stem + ".json")
        save(contract, {"modules": [module]})
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
                 "--source", source, "--out-dir", work, "--no-state"], ROOT,
                str(work.relative_to(ROOT) / source.stem), allowed=(0, 1, 2))
        generated = work / "spec/shared_frontend" / (source.stem + "_spec.md")
        assert generated.exists(), source
        shutil.copyfile(generated, source.with_name(source.stem + "_spec.md"))
    shutil.copytree(work / "spec/shared_frontend/waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def simulate():
    check()
    work = fresh("simulation")
    sources = work / "sources"
    sources.mkdir()
    for folder in ("rtl", "tests"):
        for path in (ROOT / folder).iterdir():
            if path.suffix in (".v", ".vh"):
                shutil.copyfile(path, sources / path.name)
    shutil.copyfile(STEM, sources / STEM.name)
    receipt_path = ROOT.parent / "mac_ce_fanout_local_20261010/shell_rtl/vlog.command.json"
    vendor = [path for path in json.loads(receipt_path.read_text())["command"] if "sim_release" in str(path)]
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([helpers.MSIM / "vlog.exe", "-work", "work", "+incdir+" + sources.as_posix(),
             *vendor, *sorted(helpers.CORE.glob("*.v")), *sorted(sources.glob("*.v"))], work, "vlog")
    results = []
    for top, mode in (("tb_shared_core_control", "control"), ("tb_frontend_shared", "normal"), ("tb_frontend_shared", "stalls")):
        print("SIMULATING", mode, flush=True)
        output = command([helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top,
            "+VECTORS=" + VECTORS.as_posix(), "+MODE=" + mode,
            "+REPORT=" + (work / (mode + ".csv")).as_posix(),
            "+DUMP=" + (work / (mode + "_output.hex")).as_posix(), "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, mode)
        assert "TB_PASS" in output, work / (mode + ".log")
        if mode != "control":
            actual = np.array([int(v, 16) for v in (work / (mode + "_output.hex")).read_text().split()], dtype=np.uint8)
            actual = actual.view(np.int8).reshape(18, 32, 4, 4, 24).transpose(0, 2, 1, 3, 4).reshape(72, 128, 24)
            assert np.array_equal(actual, np.load(VECTORS / "expected_pw_hwc.npy"))
        results.append({"mode": mode, "status": "PASS", "mismatches": 0,
                        "lines": [line for line in output.splitlines() if "STEM_TOTAL" in line or "TB_PASS" in line]})
        save(work / "receipt.json", {"status": "PASS" if len(results) == 3 else "PARTIAL", "results": results,
             "source_hashes": {str(p): sha(p) for p in sources.iterdir()}, "vendor_models": vendor,
             "vector_reference_sha256": sha(BASE / "reference.json")})
        print("SIM_PASS", mode, flush=True)
    check()


def finish():
    check()
    simulations = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)
    receipt = json.loads(simulations[-1].read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS" and len(receipt["results"]) == 3
    for filename, digest in receipt["source_hashes"].items():
        p = Path(filename)
        live = STEM if p.name == STEM.name else ROOT / ("rtl" if p.name.startswith("road_") else "tests") / p.name
        assert sha(p) == digest == sha(live), live
    cycles = {}
    for mode in ("normal", "stalls"):
        cycles[mode] = {}
        for layer, suffix, count in (("stem", ".csv.stem.csv", 2304), ("down2", ".csv", 576)):
            with (simulations[-1].parent / (mode + suffix)).open(encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            assert len(rows) == count
            totals = {key: sum(int(row[key]) for row in rows) for key in rows[0] if key != "tile"}
            assert sum(totals[f"bin{i}"] for i in range(8)) == totals["core"]
            cycles[mode][layer] = totals
    old = json.loads((BASE / "cycle_summary.json").read_text(encoding="utf-8"))
    for layer in ("stem", "down2"):
        assert cycles["normal"][layer]["core"] == old["normal"][layer]["core"]
    save(ROOT / "cycle_summary.json", cycles)
    gates = sorted(ROOT.glob("gate*"), key=lambda p: p.stat().st_mtime)[-1]
    matrix = {}
    for name in ("rtl", "tests"):
        data = json.loads((gates / (name + ".json")).read_text(encoding="utf-8"))
        matrix[name] = {key: data[key] for key in ("errors", "strict_warnings", "checks")}
    for path in ROOT.glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"))
    physical_path = ROOT / "physical_completion/summary.json"
    physical = json.loads(physical_path.read_text(encoding="utf-8")) if physical_path.exists() else None
    save(ROOT / "status.json", {"status": "SINGLE_CORE_FUNCTIONAL_PASS_NOT_DEPLOYMENT_READY",
         "simulation": str(simulations[-1].relative_to(ROOT)), "strict_gate": matrix,
         "physical": physical,
         "unique_arithmetic_instances": {"road_mac_probe": 1, "road_dynamic_postprocess": 1},
         "frozen_kernel_modified": False, "coefficients": "TEST_ONLY, not QAT",
         "not_done": ["close actual top timing and strict gates" if physical else "TD resources and timing for the new actual top", "full ROM shared front-end integration",
                      "matched vendor DDR memory model and real transfer loop", "remaining 64 convolutions and graph control",
                      "deployment QAT, whole-network FPGA postprocess and board FPS"]})
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in sorted(ROOT.rglob("*"))
         if path.is_file() and path.name != "artifact_manifest.json" and path.suffix not in (".wlf", ".pyc")
         and "work" not in path.relative_to(ROOT).parts})
    print("SINGLE_CORE_FUNCTIONAL_PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "check", "gate", "specifications", "simulate", "finish"))
    globals()[parser.parse_args().action]()
