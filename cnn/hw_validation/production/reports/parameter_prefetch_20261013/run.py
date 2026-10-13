"""复用冻结前端验证流程；本候选仅改变 down2 参数归属存储。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "table_command_isolation_20261013"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load_module("prefetch_existing_runner", BASE / "run.py")
prior.ROOT = prior.shared.ROOT = prior.shared.helpers.ROOT = ROOT
prior.PREVIOUS = BASE
prior.TOP = ROOT / "rtl/road_frontend_shared_core.v"
prior.STEM = prior.shared.STEM = ROOT / "rtl/road_stem_tile_scheduler.v"
save, sha, command, fresh = prior.save, prior.sha, prior.command, prior.fresh
check = prior.check


def setup():
    assert not (ROOT / "frozen.json").exists(), "不覆盖已冻结候选"
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8")))
    records.update({str(BASE / name): sha(BASE / name) for name in
                    ("frozen.json", "artifact_manifest.json", "run.py", "physical_report.py")})
    save(ROOT / "frozen.json", records)
    for folder in ("rtl", "tests"):
        (ROOT / folder).mkdir(exist_ok=True)
        for source in (BASE / folder).iterdir():
            if source.suffix in (".v", ".vh"):
                target = ROOT / folder / source.name
                assert not target.exists(), target
                shutil.copyfile(source, target)
    save(ROOT / "baseline_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in sorted((ROOT / "rtl").glob("*.v"))})
    check()


def reference():
    check()
    module = load_module("prefetch_reference", ROOT / "reference.py")
    result = module.self_check()
    assert result["status"] == "PASS"
    save(ROOT / "reference_receipt.json", {**result, "sha256": sha(ROOT / "reference.py")})
    check()


def dependency():
    paths = json.loads((BASE / "dependency.json").read_text(encoding="utf-8"))["paths"]
    paths["reference"] = str(ROOT / "reference.py")
    paths["physical_report"] = str(BASE / "physical_report.py")
    assert all(Path(path).is_file() for path in paths.values())
    save(ROOT / "dependency.json", {"status": "PASS", "paths": paths,
         "hashes": {name: sha(Path(path)) for name, path in paths.items()}})
    work = fresh("dependency_check")
    entry = (f"import sys;sys.path.insert(0,{str(prior.shared.helpers.SKILL)!r});"
             "from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "check"], work, "renderer")
    check()


def specifications():
    check()
    source = ROOT / "rtl/road_down2_tile_scheduler.v"
    work = fresh("specifications")
    ports = [{"name": name, "direction": direction,
              "width": int(high) + 1 if high else 1, "clock_domain": "i_clk",
              "role": name, "description": "冻结端口；仅 valid 与 ready 同时有效时接受，停顿保持负载。"}
             for direction, high, name in re.findall(
                 r"\b(input|output)\s+(?:signed\s+)?(?:\[(\d+):0\])?\s*(\w+)\s*[,\n]",
                 source.read_text(encoding="utf-8"))]
    module = {"name": source.stem, "feature": "parameter_prefetch", "rtl_path": source.name,
        "description": "复用四项任务所有权环，first握手预取量化参数，避免结果时再读通道参数RAM。",
        "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
        "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
        "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                  "values": "取消环和active有效性；数据不整阵列清零；调用者同步释放并完整重装表及参数。"},
        "behavior": [
            "原四项所有权环同一个first握手同时登记任务身份和152位参数，不增加队列或II。",
            "参数记录高到低为post_shift6、post_multiplier32、pre_shifts18、pre_multipliers96。",
            "PW参数索引16+输出组起始通道；DW索引为当前发射通道向下对齐到三通道组。",
            "PW结果使用旧队首记录；DW结果与参数、active_meta同拍保存，三空间点复用同一参数。",
            "满环同拍pop/push必须消费旧队首；DW末标量和新结果同拍时新active安装优先。",
            "原状态机、标签、mask、shape fault及数值核不变；fault终止后只能复位恢复。"],
        "constraints": ["TEST_ONLY参数，非部署QAT；无DDR、整网或板级通过声明。",
                        "接口与计算周期不变；完整RAM/DSP端点时序必须另测。"],
        "corner_cases": ["满环同址pop/push、DW active替换、尾通道15、长反压、故障与复位。"],
        "verification_cases": ["Python归属参考、原五类回归、专项参数对拍、实际顶层物理实现。"],
        "timing_diagrams": [{"id": "ownership", "title": "任务与参数同步所有权",
            "scenario": "ownership", "description": "事件示意，省略MAC在途周期；不表示固定MAC延迟。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p......."},
                {"name": "first_accept", "wave": "010....."},
                {"name": "owner_valid", "wave": "0.1...0."},
                {"name": "parameters", "wave": "x.=...x.", "data": ["held task parameters"]},
                {"name": "result_valid", "wave": "0...1.0."},
                {"name": "result_ready", "wave": "0....10."},
                {"name": "result_accept", "wave": "0....10."}]}}]}
    contract = work / "road_down2_tile_scheduler.json"
    save(contract, {"modules": [module]})
    entry = (f"import sys;sys.path.insert(0,{str(prior.shared.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
             "--source", source, "--out-dir", work, "--no-state"], ROOT,
             str(work.relative_to(ROOT) / "write_spec"))
    generated = work / "spec/parameter_prefetch"
    shutil.copyfile(generated / "road_down2_tile_scheduler_spec.md",
                    source.with_name("road_down2_tile_scheduler_spec.md"))
    shutil.copytree(generated / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def focused():
    check()
    work = fresh("focused")
    sources = [ROOT / "rtl/road_down2_tile_scheduler.v", ROOT / "tests/tb_parameter_prefetch.v"]
    for source in sources:
        shutil.copyfile(source, work / source.name)
    command([prior.shared.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([prior.shared.helpers.MSIM / "vlog.exe", "-work", "work",
             *[work / p.name for p in sources]], work, "vlog")
    output = command([prior.shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work",
        "tb_parameter_prefetch", "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "test")
    assert "TB_PASS_PARAMETER_PREFETCH" in output
    save(work / "receipt.json", {"status": "PASS", "source_hashes": {str(p): sha(p) for p in sources}})
    check()


def simulate():
    prior.simulate()
    work = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    output = command([prior.shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work",
        "PH1P_PHY_GSR", "tb_parameter_prefetch", "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
        work, "parameter_prefetch")
    assert "TB_PASS_PARAMETER_PREFETCH" in output
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    receipt["extra_results"].append({"top": "tb_parameter_prefetch", "status": "PASS"})
    save(work / "receipt.json", receipt)
    check()


def report(work):
    parser = load_module("prefetch_physical_parser", BASE / "physical_report.py")
    parser.ROOT, parser.CANDIDATE = work, ROOT
    parser.MANIFEST = work / "source_manifest.json"
    # Imported from its archive root, not a physical run directory: bind its historical comparison explicitly.
    parser.PREVIOUS = ROOT.parent / "stem_weight_address_20261011"
    code = parser.summarize()
    assert code in (0, 1)
    path = work / "physical_summary.json"
    result = json.loads(path.read_text(encoding="utf-8"))
    old = json.loads((BASE / "physical_runtime/physical_summary.json").read_text(encoding="utf-8"))
    result["comparison_to_parameter_prefetch_baseline"] = {
        "baseline": str(BASE / "physical_runtime"),
        "old_internal_register_failed": old["internal_register_failed_endpoint_count"],
        "old_internal_ram_failed": old["all_report_internal_ram_failed_endpoint_count"],
        "old_resources": old["resources"],
        "resource_deltas": {key: result["resources"][key]["used"] - old["resources"][key]["used"]
                            for key in ("dsp", "eram", "slice", "lut6")},
        "sdc_adc_unchanged": all(sha(work / name) == sha(BASE / "physical_runtime" / name)
                                 for name in ("frontend.sdc", "frontend.adc")),
        "place_route_parameters": "same explicit place settings and post_route_opt off; new RTL freshly synthesized",
    }
    save(path, result)
    check()


def physical():
    check()
    receipt_path = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS"
    assert any(item["top"] == "tb_parameter_prefetch" for item in receipt["extra_results"])
    tested = {Path(path).name: value for path, value in receipt["source_hashes"].items()}
    assert all(tested[path.name] == sha(path) for path in (ROOT / "rtl").glob("*.v"))
    baseline = json.loads((ROOT / "baseline_sources.json").read_text(encoding="utf-8"))
    for name in ("road_frontend_shared_core.v", "road_stem_tile_scheduler.v"):
        assert sha(ROOT / "rtl" / name) == baseline[str(Path("rtl") / name)]
    work = fresh("physical")
    for name in ("frontend.sdc", "frontend.adc"):
        shutil.copyfile(BASE / "physical_runtime" / name, work / name)
    project = (BASE / "physical_runtime/road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace((BASE / "physical_attempt3").as_posix(), work.as_posix())
    assert BASE.as_posix() not in project, "工程输出路径不得指向旧候选"
    (work / "road_frontend_shared_core.al").write_text(project, encoding="utf-8")
    manifest = json.loads((BASE / "physical_runtime/source_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        item["sha256"] = sha((work / item["path"]).resolve())
    manifest["execution_authorization"] = "Independent parameter prefetch candidate; same numerical/core/II/ports, actual top, no bitstream"
    save(work / "source_manifest.json", manifest)
    build = (BASE / "physical_attempt3/build.tcl").read_text(encoding="utf-8")
    assert build.count("set_param route post_route_opt high") == 1
    build = build.replace("set_param route post_route_opt high", "set_param route post_route_opt off")
    build = build.replace("set_param route postrt_opt_extra_round 4\n", "") + "exit\n"
    assert "bitgen" not in build
    (work / "build.tcl").write_text(build, encoding="utf-8")
    parser = load_module("prefetch_preflight", BASE / "physical_report.py")
    parser.ROOT, parser.CANDIDATE, parser.MANIFEST = work, ROOT, work / "source_manifest.json"
    assert parser.preflight() == 0
    before = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
    save(work / "source_check_before.json", before)
    save(work / "tool_hash.json", {str(prior.TOOL): sha(prior.TOOL),
         "build.tcl": sha(work / "build.tcl"), "summary_parser": sha(BASE / "physical_report.py")})
    try:
        output = command([prior.TOOL, "build.tcl"], work, "td_launcher")
    finally:
        after = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
        save(work / "source_check_after.json", after)
        assert after == before
        check()
    assert 'finish command "route"' in output and "REPORT_COMPLETION_DONE" in output
    report(work)


def summarize():
    prior.summarize()
    cycles = json.loads((ROOT / "cycle_summary.json").read_text(encoding="utf-8"))
    assert cycles["candidate"] == cycles["paired_old_top"], "同向量周期或事件计数发生变化"
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    status["paired_all_counters_identical"] = True
    status["not_done"] = ["one internal output-counter setup endpoint remains at -0.142 ns",
                          "external interface and raw-reset timing are not signed off",
                          "strict gates retain historical and new diagnostic failures",
                          "full ROM/DDR/network/QAT/board closure"]
    save(ROOT / "status.json", status)
    manifest = json.loads((ROOT / "artifact_manifest.json").read_text(encoding="utf-8"))
    manifest[str(ROOT / "status.json")] = sha(ROOT / "status.json")
    save(ROOT / "artifact_manifest.json", manifest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "reference", "dependency", "specifications", "gate", "focused", "simulate",
        "baseline_compare", "physical", "report", "summarize"))
    args = parser.parse_args()
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    if args.action in ("gate", "baseline_compare"):
        getattr(prior, args.action)()
    elif args.action == "report":
        report(sorted(ROOT.glob("physical*"), key=lambda p: p.stat().st_mtime)[-1])
    else:
        globals()[args.action]()
