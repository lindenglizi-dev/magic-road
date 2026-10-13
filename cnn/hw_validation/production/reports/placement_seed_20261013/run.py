"""One placement-seed experiment; identical RTL, gate database and constraints."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "parameter_prefetch_20261013"
WORK = ROOT / "physical"
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
SEED_DOC = TD.parent.parent / "doc/scripts/MultiSeed.tcl"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


helpers = load("seed_existing_helpers", ROOT.parent / "down2_full_tensor_20261010/run.py")
helpers.ROOT = ROOT
sha, save, command = helpers.sha, helpers.save, helpers.command
parser = load("seed_existing_parser", ROOT.parent / "table_command_isolation_20261013/physical_report.py")
parser.ROOT, parser.CANDIDATE, parser.MANIFEST = WORK, ROOT, WORK / "source_manifest.json"
parser.PREVIOUS = ROOT.parent / "stem_weight_address_20261011"


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed
    if WORK.exists():
        for name in ("gate.db", "frontend.sdc", "frontend.adc"):
            assert sha(WORK / name) == sha(BASE / "physical" / name), name
        for path in (ROOT / "rtl").glob("*.v"):
            assert sha(path) == sha(BASE / "rtl" / path.name), path


def setup():
    assert not (ROOT / "frozen.json").exists(), "Do not overwrite a frozen experiment"
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8")))
    for path in (BASE / "frozen.json", BASE / "artifact_manifest.json", BASE / "run.py",
                 BASE / "physical/gate.db", TD, SEED_DOC, Path(parser.__file__), Path(helpers.__file__)):
        records[str(path)] = sha(path)
    save(ROOT / "frozen.json", records)
    check()
    WORK.mkdir()
    (ROOT / "rtl").mkdir()
    for path in (BASE / "rtl").glob("*.v"):
        shutil.copyfile(path, ROOT / "rtl" / path.name)
    for name in ("gate.db", "frontend.sdc", "frontend.adc", "source_manifest.json"):
        shutil.copyfile(BASE / "physical" / name, WORK / name)
    project = (BASE / "physical/road_frontend_shared_core.al").read_text(encoding="utf-8")
    project = project.replace((BASE / "physical").as_posix(), WORK.as_posix())
    assert BASE.as_posix() not in project
    (WORK / "road_frontend_shared_core.al").write_text(project, encoding="utf-8")
    old = (BASE / "physical/build.tcl").read_text(encoding="utf-8")
    prefix = (ROOT.parent / "table_command_isolation_20261013/physical_runtime/build.tcl").read_text(encoding="utf-8").split("set_param place effort high")[0]
    assert "set_param place seed $seed" in SEED_DOC.read_text(encoding="utf-8")
    suffix = old[old.index("set_param place effort high"):].replace("close_project\n", "")
    assert suffix.count("report_param\nplace\n") == 1
    suffix = suffix.replace("report_param\nplace\n", "set_param place seed 1\nputs {PLACEMENT_SEED_EXPERIMENT 1}\nreport_param\nplace\n")
    build = prefix + suffix
    assert "bitgen" not in build and "optimize_gate" not in build
    (WORK / "build.tcl").write_text(build, encoding="utf-8")
    save(ROOT / "experiment.json", {"baseline_commit": "46083305", "seed": 1,
         "maximum_runs": 1, "gate_database_sha256": sha(WORK / "gate.db"),
         "only_changed_physical_parameter": "set_param place seed 1",
         "same_synthesized_database": True, "rtl_changed": False,
         "functional_and_strict_evidence": "Inherited by matching frozen hashes, not rerun",
         "functional_receipt": str(BASE / "simulation/receipt.json"),
         "cycle_summary": str(BASE / "cycle_summary.json"),
         "strict_summary": str(BASE / "strict_summary.json"),
         "seed_api_source": str(SEED_DOC), "tool_sha256": sha(TD)})
    parser.self_test()
    assert parser.preflight() == 0
    check()


def physical():
    check()
    assert not (WORK / "td_launcher.log").exists(), "One run only; preserve failed evidence"
    manifest = json.loads((WORK / "source_manifest.json").read_text(encoding="utf-8"))
    before = {item["path"]: sha((WORK / item["path"]).resolve()) for item in manifest["sources"]}
    save(WORK / "source_check_before.json", before)
    save(ROOT / "status.json", {"status": "RUNNING_ONE_SEED_DIAGNOSTIC", "seed": 1})
    try:
        output = command([TD, "build.tcl"], WORK, "td_launcher")
        assert "PLACEMENT_SEED_EXPERIMENT 1" in output
        assert 'finish command "route"' in output and "REPORT_COMPLETION_DONE" in output
    except Exception as error:
        save(ROOT / "status.json", {"status": "EXECUTION_FAILED_NO_RETRY", "error": str(error)})
        raise
    finally:
        after = {item["path"]: sha((WORK / item["path"]).resolve()) for item in manifest["sources"]}
        save(WORK / "source_check_after.json", after)
        assert after == before
        check()
    report()


def report():
    check()
    clocks = ET.parse(WORK / "imported_clock_before_place.rpt").findall(".//clock")
    assert len(clocks) == 1 and clocks[0].attrib["freq"] == "100.000MHz"
    assert clocks[0].attrib["name"] == "frontend_clk"
    assert parser.summarize() in (0, 1)
    old = json.loads((BASE / "physical/physical_summary.json").read_text(encoding="utf-8"))
    new = json.loads((WORK / "physical_summary.json").read_text(encoding="utf-8"))
    comparison = {"baseline": str(BASE), "candidate": str(ROOT), "seed": 1}
    for label, value in (("baseline", old), ("candidate", new)):
        comparison[label + "_measurements"] = {"resources": value["resources"],
            "internal_checks": value["timing"]["internal_all_checks"],
            "all_report_internal_failed": value["all_report_internal_failed_endpoint_count"],
            "internal_timing_pass": value["internal_timing_pass"],
            "failed_scope_counts": value["failed_endpoints_including_ignored"]}
    save(ROOT / "comparison.json", comparison)
    selected = {}
    raw = (WORK / "all_endpoints_include_ignored.timing").read_text(encoding="utf-8")
    for block in re.split(r"(?m)(?=^Slack\s*:)", raw):
        end = re.search(r"End Point\s*:\s*(\S+)", block)
        slack = re.match(r"Slack\s*:\s*(-?[\d.]+)ns", block)
        if not end or not slack or not re.search(r"Check Type\s*:\s*setup", block):
            continue
        family = ("cnt_output" if end[1].startswith("u_down2/cnt_output") else
                  "parameter_enable" if end[1].startswith("u_down2/reg_task_parameters") else
                  "halo_write" if end[1] == "u_down2/ramread10_syn_10672.we" else None)
        if family and (family not in selected or float(slack[1]) < selected[family]["slack_ns"]):
            selected[family] = {"slack_ns": float(slack[1]), "end": end[1], "report_block": block}
    assert set(selected) == {"cnt_output", "parameter_enable", "halo_write"}
    save(ROOT / "target_path_evidence.json", selected)
    save(ROOT / "status.json", {"status": new["status"], "seed": 1,
         "internal_timing_pass": new["internal_timing_pass"], "rtl_unchanged": True,
         "decision": "REJECT_SEED1_KEEP_46083305_BASELINE",
         "not_done": ["External interface and raw reset signoff", "Strict gates",
                      "Full CNN/ROM/DDR/QAT/board closure"], "no_more_seed_runs": True})
    check()


def freeze_result():
    check()
    assert (WORK / "physical_summary.json").is_file()
    assert not (ROOT / "artifact_manifest.json").exists(), "Do not overwrite final evidence"
    save(ROOT / "artifact_manifest.json", {str(path): sha(path)
         for path in sorted(ROOT.rglob("*")) if path.is_file()})


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "physical", "report", "freeze_result"))
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    globals()[cli.parse_args().action]()
