"""单个 Stem 独立银行诊断：固定原接口，综合结构门未通过则不进入布局。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
BASE = REPORTS / "prefetch_admission_20261014"
LAST = REPORTS / "load_bank_local_20261014"
SOURCE = REPORTS / "weight_address_stem_write_20261013"

spec = importlib.util.spec_from_file_location("independent_bank_helpers", LAST / "run.py")
prior = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = prior
spec.loader.exec_module(prior)
for helper in (prior, prior.prior, prior.prior.prior, prior.prior.prior.helpers):
    helper.ROOT = ROOT
sha, save, command, fresh = prior.sha, prior.save, prior.command, prior.fresh


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in frozen.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed
    reused = json.loads((ROOT / "reused_sources.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == value for name, value in reused.items())


for helper in (prior, prior.prior, prior.prior.prior):
    helper.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    frozen = json.loads((LAST / "frozen.json").read_text(encoding="utf-8"))
    frozen.update(json.loads((LAST / "artifact_manifest.json").read_text(encoding="utf-8")))
    frozen.update(json.loads((LAST / "compression_receipt.json").read_text(encoding="utf-8"))["content_hashes"])
    frozen.update({str(p): sha(p) for p in LAST.iterdir() if p.is_file()})
    save(ROOT / "frozen.json", frozen)
    for folder in ("rtl", "tests", "vectors", "artifacts"):
        shutil.copytree(SOURCE / folder, ROOT / folder)
    shutil.copytree(SOURCE / "rtl", ROOT / "baseline_rtl")
    for name in ("reference.py", "reference_receipt.json", "address_reference.py"):
        shutil.copyfile(SOURCE / name, ROOT / name)
    shutil.copyfile(LAST / "tests/tb_load_bank_equivalence.v", ROOT / "tests/tb_load_bank_equivalence.v")
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v") if p.name != "road_stem_tile_scheduler.v"})
    save(ROOT / "baseline_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "baseline_rtl").glob("*.v")})
    save(ROOT / "status.json", {"status": "FROZEN_BEFORE_SINGLE_BANK", "baseline_commit": "60b37283",
         "production_modified": False, "strict_delivery_ready": False, "test_only": True})
    check()


def review():
    work = fresh("review_original")
    skill = prior.prior.prior.helpers.SKILL
    entry = f"import sys;sys.path.insert(0,{str(skill)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
        ROOT / "baseline_rtl/road_stem_tile_scheduler.v", "--report-json", work / "stem.json"],
        work, "stem", allowed=(0, 1, 2))
    check()


def reference():
    result = prior.load_previous("independent_bank_reference", ROOT / "bank_reference.py").self_check()
    save(ROOT / "bank_reference_receipt.json", {**result, "source_sha256": sha(ROOT / "bank_reference.py")})
    check()


def synthesize():
    """实际完整顶层，只做到 gate.db；不默认运行布局布线。"""
    check()
    receipt = json.loads(sorted(ROOT.glob("simulation*/receipt.json"), key=lambda p: p.stat().st_mtime)[-1].read_text(encoding="utf-8"))
    assert receipt["full_cycles_and_outputs_identical"]
    tested = {Path(name).name: value for name, value in receipt["source_hashes"].items()}
    assert all(sha(p) == tested[p.name] for p in (ROOT / "rtl").glob("*.v"))
    work = fresh("synthesis")
    physical = SOURCE / "physical"
    for name in ("road_rom_current_down2_top.al", "frontend.adc", "frontend.sdc"):
        shutil.copyfile(physical / name, work / name)
    project = work / "road_rom_current_down2_top.al"
    text = project.read_text(encoding="utf-8")
    text = text.replace((SOURCE / "physical").as_posix(), work.as_posix())
    text = text.replace(SOURCE.as_posix(), ROOT.as_posix())
    text = text.replace(str(SOURCE), str(ROOT))
    project.write_text(text, encoding="utf-8")
    shutil.copytree(ROOT / "artifacts", work / "artifacts")
    output = command([prior.prior.prior.TD, (ROOT / "synthesis_only.tcl").as_posix()], work, "td")
    assert "SINGLE_BANK_SYNTHESIS_DONE_NOT_PLACED" in output
    assert (work / "gate.db").is_file() and (work / "gate_netlist.v").is_file()
    save(work / "receipt.json", {"status": "SYNTHESIZED_NOT_PLACED", "source_hashes":
         {str(p): sha(p) for p in (ROOT / "rtl").glob("*.v")}, "outputs":
         {str(work / name): sha(work / name) for name in ("gate.db", "gate_netlist.v", "gate.qor")},
         "no_bitstream": True})
    check()


def gate():
    check()
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(prior.prior.prior.helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    for target, name in ((ROOT / "rtl/road_stem_tile_scheduler.v", "stem"),
                         (ROOT / "tests/tb_load_bank_equivalence.v", "testbench")):
        closure = ["--external-interface-source", ROOT / "rtl"] if name == "testbench" else []
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, target, "--include-testbench",
            "--external-interface-source", prior.prior.prior.helpers.CORE,
            *closure,
            "--external-interface-source", ROOT.parents[2] / "interfaces/ph1p_eram_interface_complete.v",
            "--json", work / (name + ".json"), "--markdown", work / (name + ".md")], work, name, allowed=(0, 1, 2))
    check()


def specifications():
    work = fresh("specifications")
    entry = f"import sys;sys.path.insert(0,{str(prior.prior.prior.helpers.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    stem = json.loads((REPORTS / "stem_weight_address_20261011/specifications/stem.json").read_text(encoding="utf-8"))
    module = stem["modules"][0]
    module["feature"] = "independent_stem_bank"
    module["description"] = "逻辑64..127独立64字节RAM；其余368字节紧密存放，总容量432字节。"
    module["behavior"].extend(["单一存储写进程，接受同沿写；原loaded/cursor/fault所在进程不变。",
        "0..63同址；64..127读独立bank低6位；128..431读余下bank地址减64。纯地址变换不含许可。",
        "复位不清存储，取消资格/游标/完整性；装载II1、算术/接口/核心周期不变。"])
    module["verification_cases"].append("逐沿5531328存储比较、原8组同输出/周期回归及真实完整顶层综合RAM结构门。")
    module["timing_diagrams"] = [{"id": "cross_bank", "title": "接收同沿跨独立银行写入", "scenario": "cross_bank",
        "description": "原许可和完成沿不变；只改变存储归属，数据不延迟。",
        "wavejson": {"signal": [{"name": "clk", "wave": "p....."}, {"name": "valid_ready", "wave": "01..0."},
            {"name": "logical_address", "wave": "x===x.", "data": ["63", "64", "127"]},
            {"name": "remaining_we", "wave": "010..."}, {"name": "middle_we", "wave": "0.1.0."}]}}]
    contracts = [(stem, ROOT / "rtl/road_stem_tile_scheduler.v")]
    template = json.loads((LAST / "test_specification/spec.json").read_text(encoding="utf-8"))
    for name in ("tb_load_bank_equivalence", "tb_scheduler_storage"):
        contract = json.loads(json.dumps(template))
        item = contract["modules"][0]
        item["name"] = name
        item["rtl_path"] = name + ".v"
        item["feature"] = name
        item["description"] = "独立银行物理视图适配：测试按显式逻辑地址映射观察；不在硬件中增加镜像或别名。"
        if name == "tb_scheduler_storage":
            item["behavior"] = ["原存储/ready枚举测试不变，仅Stem权重观察改为middle64和remaining368的双射。",
                "DW 18432次选权重比较、Stem725笔完整加载、最后加载到start无气泡及故障复位。"]
            item["verification_cases"] = ["TB_PASS_SCHEDULER_STORAGE；原测试覆盖保持。"]
        contracts.append((contract, ROOT / "tests" / (name + ".v")))
    for contract, source in contracts:
        item = contract["modules"][0]
        path = work / (source.stem + ".json")
        save(path, contract)
        # 既有task的input被规格工具误当模块端口；此TB仅用已确认的真实模块头契约。
        source_check = ["--source", source] if source.stem != "tb_scheduler_storage" else []
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", path,
            *source_check, "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / source.stem))
        bundle = work / "spec" / item["feature"]
        shutil.copyfile(bundle / (source.stem + "_spec.md"), source.with_name(source.stem + "_spec.md"))
        shutil.copytree(bundle / "waveforms", source.parent / "waveforms", dirs_exist_ok=True)


def finalize():
    check()
    mapping = json.loads((ROOT / "mapping_receipt.json").read_text(encoding="utf-8"))
    assert not mapping["structural_gate"]["physical_run_authorized_by_structure"]
    assert mapping["rom_init_identical"]["pass"]
    paths = (ROOT / "simulation/receipt.json", ROOT / "load_compare/receipt.json", ROOT / "pending_check/receipt.json")
    assert all(json.loads(path.read_text(encoding="utf-8"))["status"] == "PASS" for path in paths)
    before = json.loads((ROOT / "review_original/stem.json").read_text(encoding="utf-8"))
    after = json.loads((ROOT / "gate_attempt2/stem.json").read_text(encoding="utf-8"))
    save(ROOT / "strict_summary.json", {"scope": "Stem definition only, not old whole closure counts",
        "original": {key: before[key] for key in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")},
        "candidate": {key: after[key] for key in ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")},
        "tb_full_closure_matrix_published": False,
        "tb_matrix_reason": "Unchanged DW single-line empty default fails formatter external-interface parsing; original logs retained",
        "actual_external_modelsim": "PASS", "actual_external_td_synthesis": "PASS",
        "actual_placement_route_sta": "NOT_RUN_STRUCTURAL_GATE_REJECTED", "delivery_ready": False})
    save(ROOT / "status.json", {"status": "REJECTED_AT_MAPPING_GATE_BASELINE_RETAINED",
        "baseline_commit": "60b37283", "retained_directory": str(BASE / "physical"),
        "candidate_retained_for_diagnostics": False, "baseline_internal_setup_failures": 3,
        "baseline_worst_setup_ns": -0.095, "candidate_internal_setup_failures": None,
        "candidate_full_timing_measured": False, "functional_regression": "PASS_SAME_OUTPUTS_AND_CYCLES",
        "mapping_reason": mapping["structural_gate"]["reason"],
        "production_modified": False, "arithmetic_interface_ii_reset_numeric_changed": False,
        "strict_delivery_ready": False, "test_only": True,
        "no_training_board_flash_bitstream": True})
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*") if p.is_file()
        and p.suffix in (".py", ".v", ".vh", ".json", ".tcl", ".txt", ".md", ".svg")
        and p.name not in ("artifact_manifest.json", "gate_netlist.v")
        and not any(part.startswith(("gate", "review")) for part in p.relative_to(ROOT).parts[:-1])
        and "work" not in p.relative_to(ROOT).parts})


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "review", "reference", "dependency", "gate",
        "bank_compare", "simulate", "pending_regression", "synthesize", "specifications", "finalize"))
    action = parser.parse_args().action
    (globals().get(action) or getattr(prior, action, None) or getattr(prior.prior, action, None)
     or getattr(prior.prior.prior, action))()
