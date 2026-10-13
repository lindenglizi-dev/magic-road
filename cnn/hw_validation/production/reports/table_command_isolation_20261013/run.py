"""验证装表命令隔离候选；复用冻结前端工具，所有输出限定本目录。"""
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
PREVIOUS = ROOT.parent / "stem_weight_address_20261011"
SHARED = ROOT.parent / "frontend_shared_core_20261011"
TOP = ROOT / "rtl/road_frontend_shared_core.v"
STEM = ROOT / "rtl/road_stem_tile_scheduler.v"
TOOL = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")

spec = importlib.util.spec_from_file_location("table_shared_run", SHARED / "run.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
shared.ROOT = shared.helpers.ROOT = ROOT
shared.STEM = STEM
save, sha, command, fresh = shared.save, shared.sha, shared.command, shared.fresh


def setup():
    assert not (ROOT / "frozen.json").exists(), "不覆盖已冻结候选"
    records = json.loads((PREVIOUS / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((PREVIOUS / "artifact_manifest.json").read_text(encoding="utf-8")))
    for path in (PREVIOUS / "frozen.json", PREVIOUS / "artifact_manifest.json",
                 *sorted((PREVIOUS / "physical").rglob("*"))):
        if path.is_file():
            records[str(path)] = sha(path)
    records[str(TOOL)] = sha(TOOL)
    save(ROOT / "frozen.json", records)

    copied = []
    for folder, suffixes in (("rtl", {".v"}), ("tests", {".v", ".vh"})):
        destination = ROOT / folder
        destination.mkdir(exist_ok=True)
        for source in sorted((PREVIOUS / folder).iterdir()):
            target = destination / source.name
            if source.is_file() and source.suffix in suffixes and not target.exists():
                shutil.copyfile(source, target)
                copied.append(str(target.relative_to(ROOT)))
    baseline_sources = {str(path.relative_to(ROOT)): sha(path)
                        for path in sorted((ROOT / "rtl").glob("*.v"))}
    save(ROOT / "baseline_sources.json", baseline_sources)
    save(ROOT / "status.json", {"stage": "FROZEN_BEFORE_TABLE_COMMAND_REPAIR",
         "copied": copied, "head": "750deef5",
         "not_deployment": True})
    check()


def baseline():
    check()
    baseline_sources = json.loads((ROOT / "baseline_sources.json").read_text(encoding="utf-8"))
    assert sha(TOP) == baseline_sources[str(TOP.relative_to(ROOT))], "基线动作必须在修改顶层前运行"
    work = fresh("baseline")
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.validation.generated_deliverable_gate import main;"
             "raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, TOP,
             "--external-interface-source", shared.helpers.CORE,
             "--external-interface-source", STEM,
             "--json", work / "old_top.json", "--markdown", work / "old_top.md"],
            work, "old_top", allowed=(0, 1, 2))
    report = json.loads((work / "old_top.json").read_text(encoding="utf-8"))
    assert report["checks"]["compile"]["status"] == "passed"
    assert report["checks"]["ast"]["status"] in ("passed", "failed")
    renderer = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
                "from scripts.python.toolchain.wavedrom_runtime import main;"
                "raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", renderer, "check"],
            work, "renderer")
    check()


def dependency():
    check()
    paths = {
        "python": Path(sys.executable),
        "numpy": Path(np.__file__),
        "vlog": shared.helpers.MSIM / "vlog.exe",
        "vsim": shared.helpers.MSIM / "vsim.exe",
        "td": TOOL,
        "readable_verilog": shared.helpers.SKILL / "SKILL.md",
        "remote_skill": shared.helpers.SKILL.parent / "erie-remote-ssh/SKILL.md",
        "reference": ROOT / "reference.py",
        "physical_report": ROOT / "physical_report.py",
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    save(ROOT / "dependency.json", {"status": "FAIL" if missing else "PASS",
         "paths": {name: str(path) for name, path in paths.items()},
         "hashes": {name: sha(path) for name, path in paths.items() if path.is_file()},
         "missing": missing, "installation_attempted": False})
    assert not missing, missing
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    ast.parse((ROOT / "physical_report.py").read_text(encoding="utf-8"))
    work = fresh("dependency_check")
    command([sys.executable, "-B", ROOT / "physical_report.py", "self-test"],
            work, "physical_report_self_test")
    print("DEPENDENCY_PASS", flush=True)


def reference():
    check()
    path = ROOT / "reference.py"
    module_spec = importlib.util.spec_from_file_location("table_command_reference", path)
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    result = module.self_check()
    assert result["status"] == "PASS"
    save(ROOT / "reference_receipt.json", {**result, "script": str(path), "sha256": sha(path)})
    check()


def specifications():
    check()
    work = fresh("specifications")
    ports = [{"name": name, "direction": direction,
              "width": abs(int(high) - int(low)) + 1 if high else 1,
              "clock_domain": "i_clk", "role": name,
              "description": "沿用冻结142位顶层接口；valid保持到ready，复位立即取消。"}
             for direction, high, low, name in re.findall(
                 r"\b(input|output)\s+(?:wire\s+|reg\s+)?(?:signed\s+)?"
                 r"(?:\[\s*(\d+)\s*:\s*(\d+)\s*\])?\s*(\w+)\s*[,\n]",
                 TOP.read_text(encoding="utf-8"))]
    module = {
        "name": TOP.stem, "feature": "table_command_isolation", "rtl_path": TOP.name,
        "description": "共享前端以单项暂存隔离装表准入和后处理推进；其余调度与数值链冻结。",
        "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
        "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
        "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                  "values": "立即取消暂存命令和旧事务；同步释放后重新装满1024项表。"},
        "behavior": [
            "外部table valid&&ready表示wrapper已保管地址和数据；后续时钟才向PP实际提交。",
            "暂存valid、地址和数据在PP未接收时保持；运行期未接受的table_valid不阻断旧事务排空。",
            "允许同拍提交前项并接收后项；末项提交时拒绝不能执行的非零后继项。",
            "完整装表后仅地址0可开始重装；o_table_loaded只反映PP真实状态。",
            "装表命令待提交期间禁止start、load、export和select；数值、II和调度器接口不变。",
        ],
        "constraints": ["仅修复共享wrapper，不改Stem/down2、算术核、约束、生产工程或位流流程。",
                        "动态系数仍为TEST_ONLY；不代表部署QAT、DDR闭环或整网性能。"],
        "corner_cases": ["连续1024项、push/pop同拍、PP反压、输入气泡、运行中提前装表、",
                         "末项后继、已加载后非法非零、待处理时命令封锁、复位取消。"],
        "verification_cases": ["Python逐拍协议参考；专用装表TB；冻结control/normal/stalls；Stem地址TB。"],
        "timing_diagrams": [{
            "id": "table_buffer", "title": "装表命令暂存与提交",
            "scenario": "table_buffer",
            "description": "接收发生于T0，T1起向PP提交；反压时暂存负载保持。",
            "wavejson": {"signal": [
                {"name": "clk", "wave": "p......."},
                {"name": "in_valid", "wave": "01.0...."},
                {"name": "in_ready", "wave": "01.0...."},
                {"name": "pending", "wave": "0.1...0."},
                {"name": "pp_ready", "wave": "0...1..."},
                {"name": "pp_valid", "wave": "0.1...0."},
                {"name": "address", "wave": "x.=...x", "data": ["held command"]},
            ]},
        }],
    }
    contract = work / "road_frontend_shared_core.json"
    save(contract, {"modules": [module]})
    entry = (f"import sys;sys.path.insert(0,{str(shared.helpers.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec",
             "--spec", contract, "--source", TOP, "--out-dir", work, "--no-state"],
            ROOT, str(work.relative_to(ROOT) / "write_spec"))
    generated = work / "spec/table_command_isolation/road_frontend_shared_core_spec.md"
    assert generated.is_file()
    shutil.copyfile(generated, TOP.with_name("road_frontend_shared_core_spec.md"))
    shutil.copytree(work / "spec/table_command_isolation/waveforms",
                    ROOT / "rtl/waveforms", dirs_exist_ok=True)
    check()


def gate():
    shared.gate()


def _compile(work, rtl_root):
    sources = work / "sources"
    sources.mkdir()
    for path in sorted(rtl_root.glob("*.v")):
        shutil.copyfile(path, sources / path.name)
    for path in sorted((ROOT / "tests").iterdir()):
        if path.name in ("tb_frontend_shared.v", "shared_stem_driver.vh"):
            shutil.copyfile(path, sources / path.name)
    receipt_path = ROOT.parent / "mac_ce_fanout_local_20261010/shell_rtl/vlog.command.json"
    vendor = [path for path in json.loads(receipt_path.read_text(encoding="utf-8"))["command"]
              if "sim_release" in str(path)]
    command([shared.helpers.MSIM / "vlib.exe", "work"], work, "vlib")
    command([shared.helpers.MSIM / "vlog.exe", "-work", "work",
             "+incdir+" + sources.as_posix(), *vendor,
             *sorted(shared.helpers.CORE.glob("*.v")), *sorted(sources.glob("*.v"))],
            work, "vlog")
    return sources, vendor


def _frontend_modes(work, modes):
    results = []
    for mode in modes:
        output = command([shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work",
            "PH1P_PHY_GSR", "tb_frontend_shared", "+VECTORS=" + shared.VECTORS.as_posix(),
            "+MODE=" + mode, "+REPORT=" + (work / (mode + ".csv")).as_posix(),
            "+DUMP=" + (work / (mode + "_output.hex")).as_posix(), "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
            work, mode)
        assert "TB_PASS" in output
        actual = np.array([int(value, 16) for value in
                           (work / (mode + "_output.hex")).read_text().split()], dtype=np.uint8)
        actual = actual.view(np.int8).reshape(18, 32, 4, 4, 24).transpose(0, 2, 1, 3, 4).reshape(72, 128, 24)
        assert np.array_equal(actual, np.load(shared.VECTORS / "expected_pw_hwc.npy"))
        results.append({"mode": mode, "status": "PASS",
                        "lines": [line for line in output.splitlines()
                                  if "STEM_TOTAL" in line or "TB_PASS" in line]})
    return results


def baseline_compare():
    check()
    work = fresh("baseline_compare")
    sources, vendor = _compile(work, PREVIOUS / "rtl")
    results = _frontend_modes(work, ("normal", "stalls"))
    save(work / "receipt.json", {"status": "PASS", "results": results,
         "source_hashes": {str(path): sha(path) for path in sources.iterdir()},
         "vendor_models": vendor, "paired_tests_from": str(ROOT / "tests")})
    check()


def simulate():
    shared.simulate()
    work = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime)[-1].parent
    extra = []
    for test, marker in (("tb_stem_weight_address", "TB_PASS_STEM_WEIGHT_ADDRESS"),
                         ("tb_table_command_buffer", "TB_PASS")):
        if (ROOT / "tests" / (test + ".v")).is_file():
            output = command([shared.helpers.MSIM / "vsim.exe", "-c", "-lib", "work",
                              "PH1P_PHY_GSR", test, "-do",
                              "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
                             work, test.removeprefix("tb_"))
            assert marker in output
            extra.append({"top": test, "status": "PASS", "marker": marker})
    assert any(item["top"] == "tb_stem_weight_address" for item in extra)
    assert any(item["top"] == "tb_table_command_buffer" for item in extra)
    receipt = json.loads((work / "receipt.json").read_text(encoding="utf-8"))
    receipt["extra_results"] = extra
    receipt["source_hashes"] = {str(path): sha(path) for path in (work / "sources").iterdir()}
    save(work / "receipt.json", receipt)
    check()


def physical():
    check()
    baseline_sources = json.loads((ROOT / "baseline_sources.json").read_text(encoding="utf-8"))
    frozen_schedulers = {
        name: sha(ROOT / "rtl" / name)
        for name in ("road_stem_tile_scheduler.v", "road_down2_tile_scheduler.v")
    }
    assert all(digest == baseline_sources[str(Path("rtl") / name)]
               for name, digest in frozen_schedulers.items())
    reference_receipt = json.loads((ROOT / "reference_receipt.json").read_text(encoding="utf-8"))
    assert reference_receipt["status"] == "PASS"
    assert reference_receipt["sha256"] == sha(ROOT / "reference.py")
    simulation = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime)[-1]
    receipt = json.loads(simulation.read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS"
    assert any(item["top"] == "tb_table_command_buffer" and item["status"] == "PASS"
               for item in receipt.get("extra_results", []))
    simulated = {Path(name).name: digest for name, digest in receipt["source_hashes"].items()}
    current_rtl = {path.name: sha(path) for path in (TOP, STEM, ROOT / "rtl/road_down2_tile_scheduler.v")}
    assert all(simulated.get(name) == digest for name, digest in current_rtl.items())
    work = fresh("physical")
    old = PREVIOUS / "physical"
    for filename in ("frontend.sdc", "frontend.adc", "build.tcl"):
        shutil.copyfile(old / filename, work / filename)
        assert sha(work / filename) == sha(old / filename)
    shutil.copyfile(ROOT / "physical_report.py", work / "physical_report.py")

    manifest = json.loads((old / "source_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        item["sha256"] = sha((work / item["path"]).resolve())
    manifest["execution_authorization"] = (
        "Approved isolated table-command register repair after Python reference and full simulation; "
        "same PH1P35MDG324-3 100MHz diagnostic constraints, no bitstream.")
    save(work / "source_manifest.json", manifest)
    project = (old / "road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace(old.as_posix(), work.as_posix())
    (work / "road_frontend_shared_core.al").write_text(project, encoding="utf-8")
    command([sys.executable, "-B", work / "physical_report.py", "preflight"],
            work, "preflight_before")
    save(work / "tool_hash.json", {str(TOOL): sha(TOOL),
         "constraints_identical_to_previous": {
             name: sha(work / name) == sha(old / name)
             for name in ("frontend.sdc", "frontend.adc", "build.tcl")}})
    before = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
    save(work / "source_check_before.json", before)
    save(work / "frozen_scheduler_check.json", {"status": "PASS",
         "baseline": frozen_schedulers, "simulation": simulated,
         "current_physical_sources": current_rtl})
    output = command([TOOL, "build.tcl"], work, "td_launcher")
    assert "REPORT_COMPLETION_DONE" in output, "TD退出码不能替代完整报告结束标记"
    assert 'finish command "route"' in output
    after = {item["path"]: sha((work / item["path"]).resolve()) for item in manifest["sources"]}
    save(work / "source_check_after.json", after)
    assert after == before
    assert all(sha(ROOT / "rtl" / name) == digest
               for name, digest in frozen_schedulers.items())
    command([sys.executable, "-B", work / "physical_report.py", "summarize"],
            work, "summarize", allowed=(0, 1))
    check()


def _cycles(receipt_path):
    result = {}
    for mode in ("normal", "stalls"):
        result[mode] = {}
        for layer, suffix, count in (("stem", ".csv.stem.csv", 2304),
                                     ("down2", ".csv", 576)):
            with (receipt_path.parent / (mode + suffix)).open(encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            assert len(rows) == count
            totals = {key: sum(int(row[key]) for row in rows) for key in rows[0] if key != "tile"}
            assert sum(totals[f"bin{index}"] for index in range(8)) == totals["core"]
            result[mode][layer] = totals
    return result


def summarize():
    check()
    simulations = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime)
    assert simulations
    receipt = json.loads(simulations[-1].read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS" and len(receipt["results"]) == 3
    for filename, digest in receipt["source_hashes"].items():
        source = Path(filename)
        live = ROOT / ("rtl" if source.name.startswith("road_") else "tests") / source.name
        assert digest == sha(source) == sha(live), live
    cycles = _cycles(simulations[-1])
    baselines = sorted(ROOT.glob("baseline_compare*/receipt.json"), key=lambda path: path.stat().st_mtime)
    paired = _cycles(baselines[-1]) if baselines else None
    save(ROOT / "cycle_summary.json", {"candidate": cycles, "paired_old_top": paired,
         "comparison": "same adapted frontend TB and RNG" if paired else "not run"})

    gates = sorted(ROOT.glob("gate*"), key=lambda path: path.stat().st_mtime)
    strict = {}
    if gates:
        for name in ("rtl", "tests"):
            data = json.loads((gates[-1] / (name + ".json")).read_text(encoding="utf-8"))
            strict[name] = {key: data[key] for key in
                            ("errors", "strict_warnings", "checks", "delivery_issues_by_rule")}
    save(ROOT / "strict_summary.json", strict)

    physical_attempts = sorted((path.parent for path in ROOT.glob("physical*/physical_summary.json")),
                               key=lambda path: path.stat().st_mtime)
    physical_result = (json.loads((physical_attempts[-1] / "physical_summary.json").read_text(encoding="utf-8"))
                       if physical_attempts else None)
    status = physical_result["status"] if physical_result else "FUNCTIONAL_PASS_PHYSICAL_NOT_RUN"
    save(ROOT / "status.json", {"status": status,
         "simulation": str(simulations[-1].relative_to(ROOT)), "strict_gate": strict,
         "cycles": {"candidate": cycles, "paired_old_top": paired},
         "physical": physical_result, "coefficients": "TEST_ONLY, not deployment QAT",
         "not_done": ["strict readable gates remain historical debt" if strict else "strict gate not run",
                      "full DDR/network/board/QAT closure"]})
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in sorted(ROOT.rglob("*"))
         if path.is_file() and path.name != "artifact_manifest.json"
         and path.suffix not in (".wlf", ".pyc")
         and "work" not in path.relative_to(ROOT).parts})
    print(status, flush=True)


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in records.items()
               if not Path(name).is_file() or sha(Path(name)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    print("FROZEN_CHECK_PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "baseline", "dependency", "reference", "specifications",
        "spec", "gate", "baseline_compare", "simulate", "physical", "summarize", "check"))
    action = parser.parse_args().action
    (specifications if action == "spec" else globals()[action])()
