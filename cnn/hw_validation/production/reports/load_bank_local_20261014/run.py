"""同周期局部写许可候选；只在本目录生成诊断，不改变原核/接口。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
BASE = REPORTS / "prefetch_admission_20261014"
SOURCE = REPORTS / "weight_address_stem_write_20261013"
MUTABLE = ("road_stem_tile_scheduler.v", "road_down2_tile_scheduler.v")

def load_previous(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load_previous("bank_load_helpers", SOURCE / "run.py")
prior.ROOT = prior.prior.ROOT = prior.prior.helpers.ROOT = ROOT
sha, save, command, fresh = prior.sha, prior.save, prior.command, prior.fresh


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed
    reused = json.loads((ROOT / "reused_sources.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == value for name, value in reused.items())


prior.check = prior.prior.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    frozen = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    for name in ("artifact_manifest.json", "local_checkpoint.json"):
        frozen.update(json.loads((BASE / name).read_text(encoding="utf-8")))
    frozen.update(json.loads((BASE / "compression_receipt.json").read_text(encoding="utf-8"))["content_hashes"])
    frozen.update({str(p): sha(p) for p in BASE.iterdir() if p.is_file()})
    save(ROOT / "frozen.json", frozen)
    for folder in ("rtl", "tests", "vectors", "artifacts"):
        shutil.copytree(SOURCE / folder, ROOT / folder)
    shutil.copytree(SOURCE / "rtl", ROOT / "baseline_rtl")
    for name in ("reference.py", "reference_receipt.json", "address_reference.py"):
        shutil.copyfile(SOURCE / name, ROOT / name)
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v") if p.name not in MUTABLE})
    save(ROOT / "baseline_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "baseline_rtl").glob("*.v")})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_BANK_LOCAL_LOAD", "baseline_commit": "60b37283",
         "numeric_interface_ii_reset_changes": False, "test_only": True, "strict_delivery_ready": False})
    check()


def baseline_gate():
    work = fresh("baseline_gate")
    entry = (f"import sys;sys.path.insert(0,{str(prior.prior.helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / "baseline_rtl",
             "--external-interface-source", prior.prior.helpers.CORE,
             "--external-interface-source", ROOT / "baseline_rtl",
             "--external-interface-source", ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v",
             "--json", work / "rtl.json", "--markdown", work / "rtl.md"], work, "rtl", allowed=(0, 1, 2))
    check()


def review():
    work = fresh("review")
    entry = (f"import sys;sys.path.insert(0,{str(prior.prior.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for name in MUTABLE:
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target", ROOT / "rtl" / name,
                 "--report-json", work / (Path(name).stem + ".json")], work, Path(name).stem, allowed=(0, 1, 2))
    check()


def normalize_check():
    entry = (f"import sys;sys.path.insert(0,{str(prior.prior.helpers.SKILL)!r});"
             "from scripts.python.quality.verify_verilog_comment_only import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry,
             ROOT / "baseline_rtl/road_down2_tile_scheduler.v", ROOT / "rtl/road_down2_tile_scheduler.v"],
            ROOT, "whitespace_token_check")


def bank_compare():
    work = fresh("load_compare")
    sources = []
    for name in MUTABLE:
        original = ROOT / "baseline_rtl" / name
        module_name = original.stem
        text = original.read_text(encoding="utf-8")
        assert text.count("module " + module_name) == 1
        target = work / ("reference_" + name)
        target.write_text(text.replace("module " + module_name, "module reference_" + module_name, 1), encoding="utf-8")
        sources.extend((target, ROOT / "rtl" / name))
    sources.append(ROOT / "tests/tb_load_bank_equivalence.v")
    command([prior.prior.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([prior.prior.helpers.MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    log = command([prior.prior.helpers.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_load_bank_equivalence",
        "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "compare")
    assert "TB_PASS_LOAD_BANK_EQ" in log
    save(work / "receipt.json", {"status": "PASS", "sources": {str(p): sha(p) for p in sources},
        "reference_module_name_only_adaptation": True, "scope": "All 432 Stem weight and 1296 halo bytes each edge; loader metadata, X address, fault/reset"})
    check()


def specifications():
    work = fresh("specifications")
    templates = (SOURCE / "specifications/road_down2_tile_scheduler.json",
                 REPORTS / "stem_weight_address_20261011/specifications/stem.json")
    entry = (f"import sys;sys.path.insert(0,{str(prior.prior.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for template in templates:
        contract = json.loads(template.read_text(encoding="utf-8"))
        module = contract["modules"][0]
        name = module["name"]
        module["feature"] = "bank_local_load"
        module["description"] = "64项静态写银行译码；原平面数组与读路径、许可、完成/故障沿不变。"
        module["behavior"].append("同一接受沿仅选一个64项银行，低6位作局部地址；数组容量和读索引不变，无新增寄存拍。")
        module["verification_cases"].extend(["baseline/candidate逐沿全存储与元数据锁步；连续、气泡、边界、越界、复位、X地址",
                                              "原ROM和共享前端数值/周期回归；实际顶层完整内部STA"])
        module["timing_diagrams"].append({"id": "bank_write", "title": "同沿装载跨银行与末项完成",
            "scenario": "bank_write", "description": "接收沿写入，次间隔已可读；没有新增pending或ready延迟。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p......"},
                {"name": "load_valid", "wave": "011.0.."}, {"name": "load_ready", "wave": "1......"},
                {"name": "address", "wave": "x===x..", "data": ["63", "64", "last"]},
                {"name": "write_bank", "wave": "x===x..", "data": ["0", "1", "tail"]},
                {"name": "loaded", "wave": "0...1.."}]}})
        path = work / (name + ".json")
        save(path, contract)
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
                 "--source", ROOT / "rtl" / (name + ".v"), "--out-dir", work, "--no-state"],
                 ROOT, str(work.relative_to(ROOT) / name))
        bundle = work / "spec/bank_local_load"
        shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "rtl" / (name + "_spec.md"))
        shutil.copytree(bundle / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def tb_specification():
    work = fresh("test_specification")
    name = "tb_load_bank_equivalence"
    contract = {"modules": [{"name": name, "feature": "load_equivalence", "rtl_path": name + ".v",
        "description": "原源与候选装载器锁步；每沿比较432权重和1296 halo字节及许可/完成/故障。",
        "interfaces": {"protocol": "discrete", "ports": [{"name": "o_test_done", "direction": "output",
            "width": 1, "clock_domain": "clk", "role": "test_complete", "description": "全部断言通过后置1并结束仿真。"}]},
        "parameters": [], "clock": {"name": "clk", "frequency_hz": 100000000, "edge": "posedge", "internal": True},
        "reset": {"name": "rstn", "active": "low", "synchronous": False, "internal": True},
        "behavior": ["相同输入同时驱动原源与候选；NBA后逐项case inequality比较全部目标数组和装载元数据。",
            "先连续装载，再有界气泡；逐类越界/乱序/非法类型/数据、装载中异步复位及全X地址点测。",
            "内部DW ready在reset期间沿原IDLE表达式可为高；必须立即取消写入，不能伪造ready=0的内部契约。"],
        "constraints": ["测试专用，不综合，不属于数值精度或完整CNN FPS证据。"],
        "corner_cases": ["63/64、127/128、639/640、703/704、431/432、1295/1296及地址0重启。"],
        "verification_cases": ["TB_PASS_LOAD_BANK_EQ；5531328字节比较，原8组回归和专门pending reset另行记录。"],
        "timing_diagrams": [{"id": "lockstep", "title": "接受沿后对比存储", "scenario": "lockstep",
            "description": "同输入分别作用于原源和候选，NBA后比较，不允许新增写入拍。",
            "wavejson": {"signal": [{"name": "clk", "wave": "p....."},
                {"name": "valid_ready", "wave": "01.0.."}, {"name": "old_write", "wave": "01.0.."},
                {"name": "new_write", "wave": "01.0.."}, {"name": "compare_after_edge", "wave": "0.10.."}]}}]}]}
    save(work / "spec.json", contract)
    entry = (f"import sys;sys.path.insert(0,{str(prior.prior.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", work / "spec.json",
        "--source", ROOT / "tests" / (name + ".v"), "--out-dir", work, "--no-state"], ROOT,
        str(work.relative_to(ROOT) / "write_spec"))
    bundle = work / "spec/load_equivalence"
    shutil.copyfile(bundle / (name + "_spec.md"), ROOT / "tests" / (name + "_spec.md"))
    shutil.copytree(bundle / "waveforms", ROOT / "tests/waveforms", dirs_exist_ok=True)


def physical():
    """重综合真实新RTL；保留两条已证实的物理分流，不沿用旧资源。"""
    check()
    receipts = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)
    receipt = json.loads(receipts[-1].read_text(encoding="utf-8"))
    assert receipt["full_cycles_and_outputs_identical"]
    focused = json.loads(sorted(ROOT.glob("load_compare*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].read_text(encoding="utf-8"))
    assert focused["status"] == "PASS"
    tested = {Path(name).name: value for name, value in receipt["source_hashes"].items()}
    assert all(tested[p.name] == sha(p) for p in (ROOT / "rtl").glob("*.v"))
    work = fresh("physical")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    source_physical = SOURCE / "physical"
    for name in ("frontend.sdc", "frontend.adc"):
        shutil.copyfile(BASE / "physical" / name, work / name)
    project = (source_physical / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(source_physical.as_posix(), work.as_posix())
    sources = [*sorted((ROOT / "rtl").glob("*.v")), *sorted(prior.prior.helpers.CORE.glob("*.v"))]
    source_xml = "\n".join(f'<File Path="{p.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/>'
        '<Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/>'
        f'<Attr Name="CompileOrder" Val="{i}"/></FileInfo></File>' for i, p in enumerate(sources, 1))
    project = re.sub(r"<Verilog>.*?</Verilog>", lambda match: "<Verilog>\n" + source_xml + "\n</Verilog>", project, flags=re.S)
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    (work / "project_input.al").write_text(project, encoding="utf-8")
    build = (source_physical / "build.tcl").read_text(encoding="utf-8")
    # Exact nets are asserted after new elaboration; naming drift must fail, never target another net.
    optimization = '''export_db before_replication.db
write_verilog before_replication.v -implement -top road_rom_current_down2_top
set advance [get_nets -hier {u_compute/u_pp/u_pre/u_round/i_advance_dup_2}]
if {[llength $advance] != 1} {error {Frozen advance net changed after synthesis}}
phys_opt -force_replication_on_nets {u_compute/u_pp/u_pre/u_round/i_advance_dup_2} -fanout_threshold 128
set admission [get_nets -hier {u_rom/cnt_wait_b_n_dup_4}]
if {[llength $admission] != 1} {error {Frozen ROM admission net changed after synthesis}}
puts "TARGET_BEFORE_BEGIN"
report_nets $admission -connection -pin_display_limit 2000
puts "TARGET_BEFORE_END"
write_verilog before_rom_clone.v -implement -top road_rom_current_down2_top
phys_opt -force_replication_on_nets {u_rom/cnt_wait_b_n_dup_4} -fanout_threshold 16
'''
    build = build.replace("\nroute\n", "\n" + optimization + "route\n", 1)
    build = build.replace("report_area -verbose -io_info", '''puts "TARGET_AFTER_BEGIN"
report_nets [get_nets -hier {u_rom/cnt_wait_b_n*}] -connection -pin_display_limit 2000
puts "TARGET_AFTER_END"
report_area -verbose -io_info''', 1)
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", build, re.M)
    (work / "build.tcl").write_text(build, encoding="utf-8")
    bound = [*sources, work / "frontend.sdc", work / "frontend.adc", work / "project_input.al", work / "build.tcl",
             *sorted((work / "artifacts").iterdir()), *sorted((ROOT / "rtl/artifacts").iterdir())]
    before = {str(p): sha(p) for p in bound if p.is_file()}
    save(work / "input_manifest.json", before)
    save(ROOT / "status.json", {"status": "FUNCTIONAL_PASS_PHYSICAL_RUNNING", "baseline_commit": "60b37283",
         "directory": str(work), "test_only": True, "strict_delivery_ready": False})
    try:
        log = command([prior.prior.TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in log and 'finish command "route"' in log
        assert "PHY-8075 ERROR" not in log and "PHY-8023 ERROR" not in log
    except Exception as error:
        save(ROOT / "status.json", {"status": "PHYSICAL_ATTEMPT_FAILED", "error": repr(error), "directory": str(work)})
        raise
    finally:
        after = {str(p): sha(p) for p in bound if p.is_file()}
        save(work / "input_check_after.json", {"same": before == after, "hashes": after})
        assert before == after
        check()
    prior.prior.report()


def rom_check():
    work = fresh("rom_connection")
    command([sys.executable, "-B", "-X", "utf8", ROOT / "check_rom_control.py"], work, "check")


def rom_negative():
    command([sys.executable, "-B", "-X", "utf8", ROOT / "test_rom_control_check.py"], ROOT, "rom_negative")


def compress():
    helper = load_previous("bank_load_compression", REPORTS / "control_fanout_20261014/run.py")
    helper.ROOT = helper.prior.ROOT = helper.prior.helpers.ROOT = ROOT
    helper.check = check
    helper.compress()


def finalize():
    check()
    work = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    candidate = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    baseline = json.loads((BASE / "physical/physical_summary.json").read_text(encoding="utf-8"))
    counts = lambda value: len(value["internal_failed_endpoints"])
    worst = lambda value: min((row["slack_ns"] for row in value["internal_failed_endpoints"]), default=0.0)
    adopted = counts(candidate) < counts(baseline) or (counts(candidate) == counts(baseline) and worst(candidate) > worst(baseline))
    resources = candidate["resources"]
    assert resources["slice"]["used"] <= 21216 and resources["dsp"]["used"] <= 40 and resources["eram"]["used"] <= 108
    save(ROOT / "comparison.json", {"baseline_commit": "60b37283", "baseline": baseline, "candidate": candidate,
        "retained_directory": str(work if adopted else BASE / "physical"), "candidate_retained_for_diagnostics": adopted,
        "resource_delta": {name: resources[name]["used"] - baseline["resources"][name]["used"] for name in ("slice", "dsp", "eram", "io")},
        "logical_cycles_identical": True, "test_parameters_only": True})
    records = {}
    for folder in ("rtl", "tests"):
        path = ROOT / "gate" / (folder + ".json")
        value = json.loads(path.read_text(encoding="utf-8"))
        records[folder] = {"path": str(path), "sha256": sha(path), "errors": value["errors"],
                          "strict_warnings": value["strict_warnings"], "checks": value["checks"],
                          "by_rule": value["delivery_issues_by_rule"]}
    save(ROOT / "strict_summary.json", {"original_full_gate_exit": 2, "original_matrix_unpublished": True,
        "original_reason": "single-line empty default case normalization",
        "token_preserving_whitespace_check": "PASS", "candidate": records, "delivery_ready": False,
        "actual_simulation": "PASS", "actual_physical_internal": candidate["internal_timing_pass"]})
    save(ROOT / "status.json", {"status": "INTERNAL_TIMING_PASS_STRICT_EXTERNAL_OPEN" if candidate["internal_timing_pass"] else
         "CANDIDATE_IMPROVED_INTERNAL_OPEN" if adopted else "CANDIDATE_REJECTED_TIMING_BASELINE_RETAINED",
         "baseline_commit": "60b37283", "candidate_retained_for_diagnostics": adopted,
         "retained_directory": str(work if adopted else BASE / "physical"),
         "candidate_internal_failures": counts(candidate), "baseline_internal_failures": counts(baseline),
         "candidate_worst_internal_slack_ns": worst(candidate), "numeric_and_cycles_pass": True,
         "production_modified": False, "strict_delivery_ready": False, "test_only": True})
    artifacts = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".py", ".v", ".vh", ".json", ".tcl", ".txt", ".md", ".svg")
                 and p.name != "artifact_manifest.json" and "work" not in p.relative_to(ROOT).parts
                 and p.name not in ("gate_netlist.v", "routed_netlist.v", "before_replication.v", "before_rom_clone.v")]
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in artifacts})


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "baseline_gate", "review", "normalize_check", "bank_compare", "dependency", "reference", "tb_specification",
        "gate", "specifications", "simulate", "pending_regression", "physical", "rom_check", "rom_negative", "compress", "finalize"))
    action = parser.parse_args().action
    (globals().get(action) or getattr(prior, action, None) or getattr(prior.prior, action))()
