"""两个装载写口的一拍提交候选；复用冻结工具流程，输出只在本目录。"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
SOURCE = REPORTS / "weight_address_stem_write_20261013"
BASE = REPORTS / "prefetch_admission_20261014"
MUTABLE = ("road_stem_tile_scheduler.v", "road_down2_tile_scheduler.v")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bank = load("commit_bank_helpers", REPORTS / "load_bank_local_20261014/run.py")
weight, rom = bank.prior, bank.prior.prior
helpers = rom.helpers
for module in (bank, weight, rom, helpers):
    module.ROOT = ROOT
sha, save, command, fresh = helpers.sha, helpers.save, helpers.command, helpers.fresh


def check(full=False):
    manifest = "frozen.json" if full else "critical_frozen.json"
    records = json.loads((ROOT / manifest).read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / ("full_frozen_check.json" if full else "frozen_check.json"),
         {"checked": len(records), "changed": changed})
    assert not changed, changed
    reused = json.loads((ROOT / "reused_sources.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == value for name, value in reused.items())


for module in (bank, weight, rom, helpers):
    module.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    previous = REPORTS / "stem_location_eco_20261014"
    records = json.loads((previous / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((previous / "artifact_manifest.json").read_text(encoding="utf-8")))
    critical = [*SOURCE.joinpath("rtl").glob("*.v"), *helpers.CORE.glob("*.v"),
                *BASE.joinpath("physical").glob("*.sdc"), *BASE.joinpath("physical").glob("*.adc"),
                BASE / "physical/pr.db", BASE / "physical/physical_summary.json",
                BASE / "physical/build.tcl", ROOT.parents[4] / "user_source/hdl_source/top.v"]
    critical = {str(p): sha(p) for p in critical if p.is_file()}
    records.update(critical)
    save(ROOT / "frozen.json", records)
    save(ROOT / "critical_frozen.json", critical)
    for folder in ("rtl", "tests", "vectors", "artifacts"):
        shutil.copytree(SOURCE / folder, ROOT / folder, dirs_exist_ok=True)
    shutil.copytree(SOURCE / "rtl", ROOT / "baseline_rtl")
    for name in ("reference.py", "reference_receipt.json", "address_reference.py"):
        shutil.copyfile(SOURCE / name, ROOT / name)
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v") if p.name not in MUTABLE})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_COMMIT_PIPELINE", "baseline_commit": "60b37283",
         "working_head": "aef055f5", "internal_baseline_failures": 3, "strict_delivery_ready": False})
    check(full=True)


def focused():
    check()
    work = fresh("load_compare")
    sources = []
    for name in MUTABLE:
        original = ROOT / "baseline_rtl" / name
        value = original.read_text(encoding="utf-8")
        assert value.count("module " + original.stem) == 1
        path = work / ("reference_" + name)
        path.write_text(value.replace("module " + original.stem,
                                      "module reference_" + original.stem, 1), encoding="utf-8")
        sources.extend((path, ROOT / "rtl" / name))
    sources.append(ROOT / "tests/tb_load_commit_pipeline.v")
    command([helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([helpers.MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    output = command([helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_load_commit_pipeline",
         "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "compare")
    assert "TB_PASS_LOAD_COMMIT" in output
    save(work / "receipt.json", {"status": "PASS", "sources": {str(p): sha(p) for p in sources},
         "scope": "One-cycle memory commit; accept/ready/fault/start semantics, complete target arrays, reset cancellation"})
    check()


def physical():
    # 此辅助已包含新的RTL重综合、相同SDC、两条已验证控制网分流和全量STA。
    # focused收据路径/格式与辅助一致；不运行旧目录中的任何写入入口。
    bank.physical()


def focused_gates():
    work = fresh("focused_gate")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    for folder in ("baseline_rtl", "rtl"):
        for name in MUTABLE:
            label = folder + "_" + Path(name).stem
            command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / folder / name,
                     "--json", work / (label + ".json"), "--markdown", work / (label + ".md")],
                    work, label, allowed=(0, 1, 2))
    check()


def inspect_placed():
    check()
    work = fresh("placed_query")
    project = (ROOT / "physical/project_input.al").read_text(encoding="utf-8")
    project = project.replace((ROOT / "physical").as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    script = f'''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db {{{(ROOT / 'physical/before_replication.db').as_posix()}}}
puts "ADVANCE_QUERY_BEGIN"
report_nets [get_nets -hier {{u_compute/u_pp/u_pre/u_round/i_advance}}] -connection -pin_display_limit 2000
puts "ADVANCE_QUERY_END"
foreach net [get_nets -hier {{u_rom/cnt_wait_b_n*}}] {{
 puts "ROM_QUERY_BEGIN $net"
 report_nets $net -connection -pin_display_limit 2000
 puts "ROM_QUERY_END"
}}
close_project
exit
'''
    (work / "query.tcl").write_text(script, encoding="utf-8")
    log = command([rom.TD, "query.tcl"], work, "query")
    assert "ADVANCE_QUERY_END" in log and "ROM_QUERY_END" in log
    check()


def resume_physical():
    check()
    original = ROOT / "physical"
    work = fresh("physical")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    for name in ("frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(original / name, work / name)
    shutil.copyfile(original / "before_replication.db", work / "source_placed.db")
    project = (original / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(original.as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    (work / "project_input.al").write_text(project, encoding="utf-8")
    # 由本候选只读查询得到的同族确切对象；不把旧综合后缀当作逻辑身份。
    advance = "u_compute/u_pp/u_pre/u_round/i_advance"
    admission = "u_rom/cnt_wait_b_n_dup_3"
    query = (ROOT / "placed_query/query.log").read_text(encoding="utf-8")
    assert re.search(r"Loads\s*\|\s*850\b", query.split("ADVANCE_QUERY_BEGIN", 1)[1].split("ADVANCE_QUERY_END", 1)[0])
    block = query.split("ROM_QUERY_BEGIN " + admission + "\n", 1)[1].split("ROM_QUERY_END", 1)[0]
    assert re.search(r"Loads\s*\|\s*50\b", block)
    reports = (original / "build.tcl").read_text(encoding="utf-8")
    reports = reports[reports.index("report_area -verbose -io_info"):]
    operations = ""
    for label, net, threshold in (("ADVANCE", advance, 128), ("ROM", admission, 16)):
        operations += f'''set target [get_nets -hier {{{net}}}]
if {{[llength $target] != 1}} {{error {{Exact {label} target missing}}}}
puts "{label}_BEFORE_BEGIN"
report_nets $target -connection -pin_display_limit 2000
puts "{label}_BEFORE_END"
write_verilog before_{label.lower()}_clone.v -implement -top road_rom_current_down2_top
phys_opt -force_replication_on_nets {{{net}}} -fanout_threshold {threshold}
'''
    after = '''puts "ADVANCE_AFTER_BEGIN"
report_nets [get_nets -hier {u_compute/u_pp/u_pre/u_round/i_advance*}] -connection -pin_display_limit 2000
puts "ADVANCE_AFTER_END"
puts "ROM_AFTER_BEGIN"
report_nets [get_nets -hier {u_rom/cnt_wait_b_n*}] -connection -pin_display_limit 2000
puts "ROM_AFTER_END"
'''
    script = '''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
update_timing
''' + operations + '''route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_current_down2_top
''' + after + reports
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", script, re.M)
    (work / "build.tcl").write_text(script, encoding="utf-8")
    sources = [*(ROOT / "rtl").glob("*.v"), *helpers.CORE.glob("*.v")]
    bound = [*sources, *[work / name for name in ("source_placed.db", "frontend.sdc", "frontend.adc", "build.tcl", "project_input.al")]]
    hashes = {str(p): sha(p) for p in bound}
    save(work / "input_manifest.json", hashes)
    save(work / "functional_receipts.json", {str(p): sha(p) for p in
         (ROOT / "simulation_attempt2/receipt.json", ROOT / "load_compare_attempt4/receipt.json", ROOT / "pending_check/receipt.json")})
    save(ROOT / "status.json", {"status": "ROUTING_FROM_SAVED_PLACEMENT", "directory": str(work),
         "advance_sinks": 850, "rom_sinks": 50, "rtl_changed_after_simulation": False})
    try:
        log = command([rom.TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in log and 'finish command "route"' in log
    finally:
        save(work / "input_check_after.json", {"same": all(sha(Path(p)) == value for p, value in hashes.items())})
        check()
    rom.report()


def specifications():
    check()
    work = fresh("specifications")
    templates = (SOURCE / "specifications/road_down2_tile_scheduler.json",
                 REPORTS / "stem_weight_address_20261011/specifications/stem.json")
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for template in templates:
        contract = json.loads(template.read_text(encoding="utf-8"))
        module = contract["modules"][0]
        name = module["name"]
        module["feature"] = "registered_load_commit"
        module["description"] = "Stem权重或down2 halo接受时验证并注册；下一沿提交RAM，连续装载II=1。"
        module["behavior"].extend([
            "接收游标和loaded仍在合法接受沿更新；loaded表示完整接收，最后pending在下一沿落入RAM。",
            "写许可、地址、数据一起注册；写端仅依赖本地pending，不再次串联外部ready或故障判断。",
            "最后写项后紧接start的沿同时提交最后pending并进入准备状态；首个RAM读沿在其后。",
            "前项合法pending与新非法项同沿时，前项提交、新项置故障且不入队；结果有效性取消。",
            "复位即时清pending/完整性，不清存储；不插入装载气泡，不修改计算II或算术源码。"])
        module["verification_cases"].extend(["连续和带气泡装载、地址零重启、非法末项、待提交中复位",
                                             "末项到单拍start无丢失、真实计算读出、同向量完整回归、全端点STA"])
        module["timing_diagrams"] = [{"id": "commit", "scenario": "commit",
            "title": "接受与上一项写入重叠，末写后读取", "description": "沿N接收A，沿N+1写A并收B；最后提交可与start同沿，读取在下一沿。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p......"},
                {"name": "accept", "wave": "0110..."}, {"name": "accept_address", "wave": "x==x...", "data": ["A", "B(last)"]},
                {"name": "pending", "wave": "0.1.0.."}, {"name": "ram_commit", "wave": "0.110.."},
                {"name": "start_accept", "wave": "0..10.."}, {"name": "first_ram_read", "wave": "0...10."}]}}]
        path = work / (name + ".json")
        save(path, contract)
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
                 "--source", ROOT / "rtl" / (name + ".v"), "--out-dir", work, "--no-state"],
                ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / "spec/registered_load_commit"
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "rtl" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def tb_specification():
    work = fresh("test_specification")
    template = REPORTS / "load_bank_local_20261014/test_specification/spec.json"
    contract = json.loads(template.read_text(encoding="utf-8"))
    module = contract["modules"][0]
    name = "tb_load_commit_pipeline"
    module.update(name=name, rtl_path=name + ".v", feature="load_commit_equivalence",
                  description="延迟一拍写入的独立记分板；接收元数据与原源锁步，复位取消允许旧存储有意不同。")
    module["behavior"] = ["接受/ready/fault/cursor/loaded按原源逐沿比较。",
        "每个合法接受登记一项，下一沿更新期望存储；仅比较已初始化字节。",
        "复位清待提交模型，保留已提交字节；旧源取消前已写入的字节可与候选有意不同。",
        "432权重连续432拍、1296halo连续1296拍；末提交与单拍start同沿，首个MAC读数据完整。"]
    module["verification_cases"] = ["TB_PASS_LOAD_COMMIT checks=1728；精确连续耗时断言；完整首读和旧8组数值回归另记。"]
    module["timing_diagrams"] = [{"id": "queued_write", "scenario": "queued_write", "title": "记分板验证一拍提交",
        "description": "接收A/B连续两拍，候选存储晚一拍；元数据同沿，末项提交后完整数组一致。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p....."}, {"name": "accept", "wave": "0110.."},
            {"name": "legacy_write", "wave": "0110.."}, {"name": "candidate_write", "wave": "0.110."},
            {"name": "compare_complete_arrays", "wave": "0...10"}]}}]
    path = work / "spec.json"
    save(path, contract)
    entry = (f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    # TB内task的kind/address/data被source检查器误判为模块端口；按已确认的单输出契约渲染。
    # 此处不宣称自动端口核对通过；实际TB由ModelSim编译和执行，设计模块仍使用--source。
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
        "--out-dir", work, "--no-state"], ROOT,
        str(work.relative_to(ROOT) / "write_spec"))
    bundle = work / "spec/load_commit_equivalence"
    shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
    shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)


def finalize():
    check(full=True)
    current_path = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1]
    current = json.loads(current_path.read_text(encoding="utf-8"))
    baseline = json.loads((BASE / "physical/physical_summary.json").read_text(encoding="utf-8"))
    assert json.loads((current_path.parent / "control_replication_check.json").read_text(encoding="utf-8"))["status"] == "PASS"
    assert json.loads((ROOT / "physical/gate_commit_check.json").read_text(encoding="utf-8"))["status"] == "PASS"
    assert current["resources"]["slice"]["used"] <= 21216
    adopted = current["internal_timing_pass"]
    save(ROOT / "comparison.json", {"baseline": baseline, "candidate": current,
         "candidate_adopted": adopted, "retained_directory": str(current_path.parent if adopted else BASE / "physical"),
         "resource_delta": {k: current["resources"][k]["used"] - baseline["resources"][k]["used"] for k in ("slice", "dsp", "eram", "io")},
         "accept_to_write_latency_edges": 1, "load_ii": 1, "test_parameters_only": True})
    save(ROOT / "status.json", {"status": "INTERNAL_PASS_STRICT_EXTERNAL_OPEN" if adopted else "TIMING_FAILED_BASELINE_RETAINED",
         "candidate_internal_failures": len(current["internal_failed_endpoints"]),
         "worst_internal_ns": min((p["slack_ns"] for p in current["internal_failed_endpoints"]), default=None),
         "functional_pass": True, "strict_delivery_ready": False, "candidate_adopted": adopted})
    gate_records = {}
    for phase in ("baseline_rtl", "rtl"):
        gate_records[phase] = {}
        for name in MUTABLE:
            path = ROOT / "focused_gate" / (phase + "_" + Path(name).stem + ".json")
            value = json.loads(path.read_text(encoding="utf-8"))
            gate_records[phase][name] = {k: value[k] for k in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
    save(ROOT / "strict_summary.json", {"focused": gate_records, "full_gate_original_and_candidate_exit": 2,
         "full_matrix_unpublished_reason": "down2 control parser/normalization failed",
         "actual_modelsim": "PASS", "actual_td_complete_internal": current["internal_timing_pass"],
         "delivery_ready": False})
    receipt = json.loads((ROOT / "simulation_attempt2/receipt.json").read_text(encoding="utf-8"))
    assert receipt["full_cycles_and_outputs_identical"]
    save(ROOT / "cycle_summary.json", {"normal_core": 11883456, "normal_stem_tile_core": 4736,
         "normal_down2_tile_core": 1687, "normal_tb_endpoint": 14022597, "stalls_tb_endpoint": 17992384,
         "measurement": "complete normal/stalls regression, CSV and output files identical to frozen counter-prepare vectors",
         "load_ii": 1, "accept_to_write_latency_edges": 1, "first_read_and_start_latency_unchanged": True,
         "scope": "Stem and down2, 3 of 67 convolutions, no full-network FPS"})
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*")
         if p.is_file() and p.name != "artifact_manifest.json" and "work" not in p.relative_to(ROOT).parts
         and p.suffix in (".py", ".v", ".vh", ".json", ".md", ".txt", ".tcl", ".sdc", ".adc", ".svg", ".json5", ".timing", ".rpt", ".log", ".area", ".qor")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "reference", "review", "baseline_gate", "dependency",
        "focused", "simulate", "pending_regression", "gate", "focused_gates", "inspect_placed", "resume_physical", "specifications", "tb_specification", "physical", "finalize"))
    action = parser.parse_args().action
    (globals().get(action) or getattr(weight, action, None) or getattr(bank, action, None) or getattr(rom, action))()
