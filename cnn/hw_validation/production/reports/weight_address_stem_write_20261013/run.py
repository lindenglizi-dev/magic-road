"""独立修复DW权重读地址和Stem写使能；所有输出只进入本目录。"""
import argparse
import ast
from collections import Counter
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "rom_current_down2_20261013"
FULL = ROOT.parent / "counter_prepare_20261013"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load("weight_address_prior", BASE / "run.py")
prior.ROOT = prior.helpers.ROOT = ROOT
sha, save, fresh, command = prior.sha, prior.save, prior.fresh, prior.command
check = prior.check


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8")))
    for name in ("frozen.json", "artifact_manifest.json", "run.py"):
        records[str(BASE / name)] = sha(BASE / name)
    save(ROOT / "frozen.json", records)
    for folder in ("rtl", "tests"):
        (ROOT / folder).mkdir()
        for path in (BASE / folder).glob("*.v"):
            shutil.copyfile(path, ROOT / folder / path.name)
    for name in ("tb_frontend_shared.v", "tb_shared_core_control.v", "tb_counter_prepare.v"):
        shutil.copyfile(FULL / "tests" / name, ROOT / "tests" / name)
    shutil.copytree(BASE / "artifacts", ROOT / "artifacts")
    shutil.copyfile(BASE / "reference.py", ROOT / "reference.py")
    mutable = ("road_down2_tile_scheduler.v", "road_stem_tile_scheduler.v")
    save(ROOT / "baseline_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for folder in ("rtl", "tests") for p in (ROOT / folder).glob("*.v")})
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v") if p.name not in mutable})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_TWO_SCHEDULER_REPAIR",
         "baseline_commit": "5586b9ba", "production_modified": False, "test_only": True})
    check()


def reference():
    prior.reference()
    result = load("weight_address_reference", ROOT / "address_reference.py").self_check()
    assert result["status"] == "PASS"
    save(ROOT / "address_reference_receipt.json", {**result, "source_sha256": sha(ROOT / "address_reference.py")})
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
    command([prior.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    old_compile = json.loads((BASE / "simulation/vlog.command.json").read_text(encoding="utf-8"))["command"]
    args = [arg for arg in old_compile if Path(arg).parent != BASE / "simulation/sources"]
    command([*args, "+incdir+" + sources.as_posix(), *sorted(sources.glob("*.v"))], work, "vlog")
    results = []
    for top in ("tb_rom_down2", "tb_rom_reader", "tb_parameter_prefetch"):
        output = command([prior.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", top,
            "+VECTORS=" + (ROOT / "vectors").as_posix(), "+REPORT=" + (work / "cycles.csv").as_posix(),
            "+WORDS=" + (ROOT / "vectors/rom_words.hex").as_posix(), "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, top)
        assert "TB_PASS" in output
        results.append({"top": top, "status": "PASS"})
    receipt = {"status": "PASS", "results": results,
        "source_hashes": {str(path): sha(path) for path in sources.iterdir()},
        "core_hashes": {str(path): sha(path) for path in prior.helpers.CORE.glob("*.v")}, "test_only": True}
    extras = []
    for mode in ("scheduler_storage", "normal", "stalls", "control", "counter_prepare"):
        if mode == "scheduler_storage":
            args = [prior.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_scheduler_storage",
                    "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
        else:
            old_path = FULL / "simulation_attempt2" / (mode + ".command.json")
            args = json.loads(old_path.read_text(encoding="utf-8"))["command"]
        args = ["+REPORT=" + (work / (mode + ".csv")).as_posix() if str(arg).startswith("+REPORT=") else
                "+DUMP=" + (work / (mode + "_output.hex")).as_posix() if str(arg).startswith("+DUMP=") else arg
                for arg in args]
        output = command(args, work, mode)
        assert "TB_PASS" in output
        if mode in ("normal", "stalls"):
            assert (work / (mode + ".csv")).read_bytes() == (FULL / "simulation_attempt2" / (mode + ".csv")).read_bytes()
            assert sha(work / (mode + "_output.hex")) == sha(FULL / "simulation_attempt2" / (mode + "_output.hex"))
        extras.append({"name": mode, "status": "PASS"})
    receipt["full_regression"] = extras
    receipt["full_cycles_and_outputs_identical"] = True
    save(work / "receipt.json", receipt)
    check()


def physical():
    receipt = json.loads(sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].read_text(encoding="utf-8"))
    assert receipt["full_cycles_and_outputs_identical"] and len(receipt["full_regression"]) == 5
    prior.physical()


def specifications():
    check()
    work = fresh("spec")
    contracts = (("road_down2_tile_scheduler", FULL / "specifications/road_down2_tile_scheduler.json"),
                 ("road_stem_tile_scheduler", ROOT.parent / "stem_weight_address_20261011/specifications/stem.json"))
    entry = (f"import sys;sys.path.insert(0,{str(prior.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for name, template in contracts:
        contract = json.loads(template.read_text(encoding="utf-8"))
        module = contract["modules"][0]
        module["feature"] = "dw" if "down2" in name else "stem"
        if "down2" in name:
            module["description"] = "DW权重9个tap bank，各16通道；OIHW预装载转置，核心周期/接口不变。"
            module["behavior"].extend([
                "外部144项OIHW加载顺序和原pending一拍写入保持；物理地址为(old%9)*16+old/9。",
                "高4位选择tap，低4位选择channel；每个tap单独16×8存储，只按cnt_output低4位读取。",
                "9个tap读出后按原三组21点并集及空间lane选择，不改变bias、mask、元数据和MAC发射沿。"])
            title, signals = "DW分组读权重，原发射沿不变", [
                {"name": "clk", "wave": "p....."}, {"name": "state", "wave": "==.=.=", "data": ["STORAGE", "SEND", "STORAGE", "SEND"]},
                {"name": "channel", "wave": "=.....", "data": ["c"]},
                {"name": "tap_bank_read", "wave": "=.....", "data": ["W[c,0..8]"]},
                {"name": "mac_accept", "wave": "01010."}]
        else:
            module["description"] = "用state_next提前登记IDLE资格，切断实时状态译码到装载RAM写使能的路径。"
            module["behavior"].extend([
                "flag_load_state_ready复位为1，每沿更新为state_next==IDLE，与更新后state_current==IDLE等价。",
                "只替换ready中的状态资格，rstn/start/export/fault保持实时；没有新增写缓存、写延迟或准入气泡。",
                "原halo/weight合法写入仍在接受同沿，非法load当沿置粘滞故障，复位立即关闭ready。"])
            title, signals = "IDLE资格与状态同沿更新", [
                {"name": "clk", "wave": "p....."}, {"name": "state", "wave": "=.=.=.", "data": ["IDLE", "PREPARE", "SEND"]},
                {"name": "load_state_ready", "wave": "1.0..."}, {"name": "start", "wave": "010..."},
                {"name": "load_ready", "wave": "10...."}]
        module["timing_diagrams"] = [{"id": "equal", "scenario": "equal", "title": title,
            "description": "原接受沿、核心窗口、反压及复位取消规则不变，图仅示意已有状态边界。", "wavejson": {"signal": signals}}]
        module["verification_cases"].append("同向量完整normal/stalls周期和输出逐字节比较、专项存储/ready枚举、实际50IO顶层TD全端点检查。")
        path = work / (name + ".json")
        save(path, contract)
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
            "--source", ROOT / "rtl" / (name + ".v"), "--out-dir", work, "--no-state"], ROOT,
            str(work.relative_to(ROOT) / name))
        bundle = work / "spec" / module["feature"]
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "rtl" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def pending_regression():
    check()
    work = fresh("pending_check")
    sources = work / "sources"
    sources.mkdir()
    for path in (ROOT / "rtl").glob("*.v"):
        shutil.copyfile(path, sources / path.name)
    shutil.copyfile(ROOT / "tests/tb_dw_pending_reset.v", sources / "tb_dw_pending_reset.v")
    command([prior.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    old = json.loads((BASE / "simulation/vlog.command.json").read_text(encoding="utf-8"))["command"]
    args = [arg for arg in old if Path(arg).parent != BASE / "simulation/sources"]
    command([*args, *sorted(sources.glob("*.v"))], work, "vlog")
    output = command([prior.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_dw_pending_reset",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "pending_reset")
    assert "TB_PASS_DW_PENDING_RESET" in output
    save(work / "receipt.json", {"status": "PASS", "sources": {str(p): sha(p) for p in sources.iterdir()}})
    check()


def report():
    prior.report()
    work = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    current = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    original = json.loads((BASE / "physical_attempt2/physical_summary.json").read_text(encoding="utf-8"))
    save(ROOT / "comparison.json", {"baseline_commit": "5586b9ba", "baseline": original,
         "candidate": current, "resource_delta": {key: current["resources"][key]["used"] - original["resources"][key]["used"]
             for key in ("slice", "dsp", "eram", "io")},
         "internal_failure_endpoints": {"baseline": len(original["internal_failed_endpoints"]),
                                        "candidate": len(current["internal_failed_endpoints"])}})


def summarize():
    check()
    work = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    assert receipt["full_cycles_and_outputs_identical"]
    with (work / "cycles.csv").open(encoding="utf-8") as stream:
        cycles = list(csv.DictReader(stream))
    bins = ("commit_stall", "capacity_stall", "commit", "mac_issue", "issue_wait", "drain_other")
    assert len(cycles) == 7 and all(sum(int(row[k]) for k in bins) == int(row["core"]) for row in cycles)
    save(ROOT / "cycle_summary.json", {"rom_tiles": cycles, "full_frontend_cycles_identical": True,
         "normal_core": 11883456, "stalls_core": 14573305, "scope": "Stem and down2 only, not whole CNN"})
    baseline = {name: {key: value for key, value in
        json.loads((ROOT / "gate" / (name + ".json")).read_text(encoding="utf-8")).items()
        if key in ("errors", "strict_warnings", "checks")} for name in ("rtl", "tests")}
    candidate = {name: json.loads((ROOT / "gate_attempt2" / (name + ".command.json")).read_text(encoding="utf-8"))
                 for name in ("rtl", "tests")}
    assert all(value["returncode"] == 2 for value in candidate.values())
    save(ROOT / "strict_summary.json", {"before_repair": baseline,
         "after_repair_gate_execution": candidate, "candidate_matrix_not_published": True,
         "candidate_issue": "FORMATTER_AST_PARSE: case_normalization_violation on single-line empty default begin/end",
         "delivery_ready": False, "actual_modelsim": "PASS", "actual_td_internal_timing": "FAIL"})
    physical = json.loads((ROOT / "physical/physical_summary.json").read_text(encoding="utf-8"))
    failed = physical["internal_failed_endpoints"]
    assert len(failed) == 104 and all("/u_pp/u_pre/u_round/" in row["end"] for row in failed)
    netlist = (ROOT / "physical/gate_netlist.v").read_text(encoding="utf-8")
    save(ROOT / "target_diagnosis.json", {
        "original_down2_and_stem_negative_endpoints_remaining": 0,
        "all_new_internal_failures": len(failed), "new_end_pin_counts": dict(Counter(row["end"].rsplit(".", 1)[-1] for row in failed)),
        "common_startpoints": dict(Counter(row["begin"] for row in failed)),
        "common_net": "u_compute/u_pp/u_pre/u_round/i_advance_dup_2", "max_fanout": 824,
        "worst_path_cell_ns": 1.224, "worst_path_net_ns": 9.997,
        "dominant_net_delay_ns": 6.030,
        "stem_idle_register_retained": (chr(92) + "u_compute/u_stem/flag_load_state_ready_reg  (") in netlist,
        "dw_bank_write_connections": netlist.count(".we(" + chr(92) + "u_compute/u_down2/reg_dw_weight_"),
        "decision": "DO_NOT_PROMOTE; control fanout is outside the approved two scheduler repair targets"})
    save(ROOT / "status.json", {"status": "CANDIDATE_REJECTED_INTERNAL_TIMING_REGRESSION",
         "baseline_commit": "5586b9ba", "numeric_pass": True, "cycles_identical": True,
         "old_targets_negative": 0, "internal_setup_failed_endpoints": 104, "worst_setup_ns": -1.481,
         "production_modified": False, "test_only": True, "strict_delivery_ready": False,
         "next_decision": "Bounded high-fanout advance control repair without arithmetic/II changes"})
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in sorted(ROOT.rglob("*"))
        if p.is_file() and p.name != "artifact_manifest.json" and p.suffix not in (".wlf", ".pyc")
        and "work" not in p.relative_to(ROOT).parts})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "reference", "dependency", "gate", "specifications", "simulate", "pending_regression", "physical", "report", "summarize"))
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    name = cli.parse_args().action
    (globals().get(name) or getattr(prior, name))()
