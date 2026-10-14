"""从冻结布局数据库验证一条推进控制网；所有新输出限定在本目录。"""
import argparse
import ast
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "weight_address_stem_write_20261013"
NET = "u_compute/u_pp/u_pre/u_round/i_advance_dup_2"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load("control_fanout_prior", ROOT.parent / "rom_current_down2_20261013/run.py")
prior.ROOT = prior.helpers.ROOT = ROOT
sha, save, command, fresh = prior.sha, prior.save, prior.command, prior.fresh


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in records.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    assert all(sha(Path(name)) == value for name, value in records.items())
    paths = [p for p in BASE.rglob("*") if p.is_file() and
             p.suffix not in (".pyc", ".wlf") and "work" not in p.relative_to(BASE).parts]
    records.update({str(p): sha(p) for p in paths})
    records[str(prior.TD)] = sha(prior.TD)
    save(ROOT / "frozen.json", records)
    shutil.copytree(BASE / "rtl", ROOT / "rtl")
    save(ROOT / "reused_sources.json", {str(p.relative_to(ROOT)): sha(p)
         for p in (ROOT / "rtl").glob("*.v")})
    save(ROOT / "status.json", {"status": "FROZEN_PHYSICAL_ONLY", "baseline_commit": "afd1ebd0",
         "target_net": NET, "rtl_changed": False, "test_only": True})
    check()


def physical(post_route=True, finish_route=False, incremental=False, pre_route=False):
    check()
    work = fresh("physical")
    original = BASE / "physical"
    for name in ("frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(original / name, work / name)
    source_database = (original / "gate.db" if pre_route else
                       ROOT / "physical_attempt2/pr.db" if finish_route else original / "pr.db")
    assert source_database.is_file()
    shutil.copyfile(source_database, work / "source_pr.db")
    project = (original / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(f'Path="{original.as_posix()}"', f'Path="{work.as_posix()}"')
    project = re.sub(r'(<File Path=")([^"]+)(")', lambda m:
        m[1] + (original / m[2]).resolve().as_posix() + m[3], project)
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    shutil.copyfile(work / "road_rom_current_down2_top.al", work / "project_input.al")
    reports = (original / "build.tcl").read_text(encoding="utf-8")
    reports = reports[reports.index("report_area -verbose -io_info"):]
    operation = ("route -incremental" if incremental else "place -eco -keep_pad\nroute -eco" if finish_route else
        f"phys_opt {'-post_route ' if post_route else ''}-force_replication_on_nets {{{NET}}} -fanout_threshold 128")
    before_target = ""
    if pre_route:
        original_build = (original / "build.tcl").read_text(encoding="utf-8")
        settings = original_build[original_build.index("set_param place effort high"):original_build.index("report_param")]
        before_target = settings + "report_param\nplace\nexport_db before_replication.db\nupdate_timing\n"
        operation = f"phys_opt -force_replication_on_nets {{{NET}}} -fanout_threshold 128\nroute"
    build = f'''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_pr.db
{before_target}update_timing
set target_net [get_nets -hier {{{NET}}}]
if {{[llength $target_net] != 1}} {{error "Expected exactly one target net"}}
puts "TARGET_BEFORE_BEGIN"
report_nets $target_net -connection -pin_display_limit 2000
puts "TARGET_BEFORE_END"
puts "REPLICATION_BEGIN"
{operation}
puts "REPLICATION_DONE"
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_current_down2_top
update_timing -mode final
puts "TARGET_AFTER_BEGIN"
report_nets [get_nets -hier {{*u_pre/u_round/i_advance*}}] -connection -pin_display_limit 2000
puts "TARGET_AFTER_END"
{reports}'''
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", build, re.M)
    (work / "build.tcl").write_text(build, encoding="utf-8")
    inputs = [work / name for name in ("source_pr.db", "frontend.sdc", "frontend.adc",
              "build.tcl", "project_input.al")]
    before = {str(p): sha(p) for p in inputs}
    save(work / "input_manifest.json", before)
    save(work / "operation.json", {"finish_route": finish_route, "incremental": incremental,
         "pre_route": pre_route, "post_route": post_route,
         "source_database": str(source_database), "sha256": sha(source_database)})
    save(ROOT / "status.json", {"status": "PHYSICAL_REPLICATION_RUNNING", "target_net": NET,
         "baseline_commit": "afd1ebd0", "directory": str(work), "rtl_changed": False})
    try:
        output = command([prior.TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in output
    except Exception as error:
        save(ROOT / "status.json", {"status": "PHYSICAL_ATTEMPT_FAILED", "error": repr(error),
             "directory": str(work), "rtl_changed": False})
        raise
    finally:
        after = {str(p): sha(p) for p in inputs}
        save(work / "input_check_after.json", {"same": before == after, "hashes": after})
        assert before == after
        check()
    report()


def replicate():
    physical(post_route=False)


def finish():
    physical(post_route=False, finish_route=True)


def incremental():
    physical(post_route=False, finish_route=True, incremental=True)


def preroute():
    physical(post_route=False, pre_route=True)


def compress():
    check()
    paths = sorted(ROOT.glob("physical*/*.timing"))
    before = {str(p): sha(p) for p in paths}
    save(ROOT / "compression_before.json", before)
    command(["compact.exe", "/C", "/S:" + str(ROOT), "/Q", "*.timing"], ROOT, "compression")
    after = {str(p): sha(p) for p in paths}
    save(ROOT / "compression_receipt.json", {"files": len(paths), "same": before == after,
         "logical_bytes": sum(p.stat().st_size for p in paths), "content_hashes": after})
    assert before == after
    check()


def finalize():
    check()
    work = ROOT / "physical_attempt5"
    result = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    failures = result["internal_failed_endpoints"]
    counts = dict(Counter(row["check"] for row in failures))
    assert counts == {"setup": 16, "recovery": 5} and len(failures) == 21
    assert result["routing_completed_after_replication"] and not result["internal_timing_pass"]
    assert all("u_pre/u_round" not in row["end"] for row in failures)
    equivalence = json.loads((work / "replication_equivalence.json").read_text(encoding="utf-8"))
    assert equivalence["sink_missing_duplicate_extra"] == 0 and len(equivalence["drivers"]) == 7
    assert all(sha(ROOT / "rtl" / p.name) == sha(p) for p in (BASE / "rtl").glob("*.v"))
    assert all(sha(work / name) == sha(BASE / "physical" / name) for name in
               ("frontend.sdc", "frontend.adc", "gate_netlist.v"))
    status = {"status": "INTERNAL_TIMING_FAILED_TARGET_CONTROL_REPAIRED", "baseline_commit": "afd1ebd0",
        "actual_physical_directory": str(work), "target_control_failures_before": 104,
        "target_control_failures_after": 0, "all_internal_failure_checks": 21,
        "failure_counts": counts, "worst_setup_ns": -0.810, "worst_recovery_ns": -0.055,
        "routing_completed_after_replication": True, "bounded_boolean_sink_equivalence": True,
        "rtl_changed": False, "logical_cycles_remeasured": False, "candidate_adopted": False,
        "strict_delivery_ready": False, "test_only": True,
        "next_scope": "ROM prefetch admission, PW reservation/commit and local ROM reset distribution"}
    save(ROOT / "status.json", status)
    save(ROOT / "strict_status.json", {"source_record": str(BASE / "strict_summary.json"),
         "source_record_sha256": sha(BASE / "strict_summary.json"), "rtl_sources_identical": True,
         "checks": {name: {"status": "not_rerun_prior_matrix_unpublished"} for name in
             ("compile", "ast", "readability", "comment", "naming", "profile", "testbench")},
         "toolchain": {"status": "failed", "physical_route_executed": True,
                       "internal_timing_pass": False}, "delivery_ready": False})
    paths = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".py", ".tcl", ".json", ".txt")
             and p.name != "artifact_manifest.json" and "rtl" not in p.relative_to(ROOT).parts]
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in paths})
    print(json.dumps(status, ensure_ascii=False, indent=2))


def report():
    prior.check = check
    prior.report()
    work = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    current = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    log = (work / "td_launcher.log").read_text(encoding="utf-8", errors="replace")
    operation = json.loads((work / "operation.json").read_text(encoding="utf-8")) if (work / "operation.json").exists() else {}
    after_net_report = log.split("TARGET_AFTER_BEGIN", 1)[-1].split("TARGET_AFTER_END", 1)[0]
    route_command = "route" if operation.get("pre_route") else "route -incremental" if operation.get("incremental") else "route -eco"
    routed = ((operation.get("finish_route", False) or operation.get("pre_route", False)) and f'finish command "{route_command}"' in log and
              "unrouted" not in after_net_report and "PHY-8075 ERROR" not in log and "PHY-8023 ERROR" not in log)
    current["routing_completed_after_replication"] = routed
    current["numeric_timing_pass_before_route_qualification"] = current["internal_timing_pass"]
    if not routed:
        current["internal_timing_pass"] = False
    save(work / "physical_summary.json", current)
    save(ROOT / "status.json", {"status": "INTERNAL_TIMING_PASS_EXTERNAL_OPEN" if current["internal_timing_pass"] else
         "ROUTING_NOT_COMPLETED_AFTER_REPLICATION" if not routed else "INTERNAL_TIMING_FAILED",
         "internal_timing_pass": current["internal_timing_pass"], "routing_completed_after_replication": routed,
         "rtl_changed": False, "strict_delivery_ready": False, "test_only": True})
    original = json.loads((BASE / "physical/physical_summary.json").read_text(encoding="utf-8"))
    save(ROOT / "comparison.json", {"baseline_commit": "afd1ebd0", "baseline": original,
         "candidate": current, "rtl_changed": False, "flow": "targeted physical replication from identical pr.db; see bound build.tcl",
         "resource_delta": {name: current["resources"][name]["used"] - original["resources"][name]["used"]
                            for name in ("slice", "dsp", "eram", "io")}})
    check()


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "physical", "replicate", "finish", "incremental", "preroute", "compress", "report", "finalize"))
    globals()[cli.parse_args().action]()
