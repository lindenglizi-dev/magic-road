"""冻结已定位的ROM请求接受控制，验证布线前局部分流；输出仅在本目录。"""
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
BASE = ROOT.parent / "control_fanout_20261014"
PHYSICAL = BASE / "physical_attempt5"
NET = "u_rom/cnt_wait_b_n_dup_4"
ADVANCE = "u_compute/u_pp/u_pre/u_round/i_advance_dup_2"
WRITE_ENABLES = (("u_compute/u_down2/flag_halo_load_write_syn_209", 7),
                ("u_compute/u_stem/reg_weight_n1_syn_dup_702", 7),
                ("u_compute/u_stem/reg_weight_n1_syn_dup_716", 5))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prior = load("prefetch_physical_helpers", ROOT.parent / "rom_current_down2_20261013/run.py")
prior.ROOT = prior.helpers.ROOT = ROOT
sha, save, command, fresh = prior.sha, prior.save, prior.command, prior.fresh


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, value in frozen.items() if sha(Path(name)) != value]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def setup():
    assert not (ROOT / "frozen.json").exists()
    frozen = json.loads((BASE / "frozen.json").read_text(encoding="utf-8"))
    frozen.update(json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8")))
    frozen.update(json.loads((BASE / "compression_receipt.json").read_text(encoding="utf-8"))["content_hashes"])
    paths = [PHYSICAL / name for name in ("before_replication.db", "pr.db", "routed_netlist.v",
        "gate_netlist.v", "frontend.sdc", "frontend.adc", "project_input.al", "input_manifest.json")]
    paths.extend((BASE / "rtl").glob("*.v"))
    paths.extend(BASE / name for name in ("frozen.json", "artifact_manifest.json", "compression_receipt.json"))
    frozen.update({str(p): sha(p) for p in paths})
    save(ROOT / "frozen.json", frozen)
    save(ROOT / "status.json", {"status": "FROZEN_ROM_ADMISSION_REPAIR", "baseline_commit": "8b8c3ac3",
         "rtl_changed": False, "target_net": NET, "test_only": True})
    check()


def physical(close_writes=False):
    check()
    work = fresh("physical")
    for name in ("frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(PHYSICAL / name, work / name)
    shutil.copyfile(PHYSICAL / "before_replication.db", work / "source_placed.db")
    project = (PHYSICAL / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(f'Path="{PHYSICAL.as_posix()}"', f'Path="{work.as_posix()}"')
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    shutil.copyfile(work / "road_rom_current_down2_top.al", work / "project_input.al")
    reports = (PHYSICAL / "build.tcl").read_text(encoding="utf-8")
    reports = reports[reports.index("report_area -verbose -io_info"):]
    write_steps, write_reports = "", ""
    if close_writes:
        write_steps = "write_verilog before_we_clone.v -implement -top road_rom_current_down2_top\n"
        for index, (name, count) in enumerate(WRITE_ENABLES):
            write_steps += f'''set write_net_{index} [get_nets -hier {{{name}}}]
if {{[llength $write_net_{index}] != 1}} {{error "Missing write enable {index}"}}
set write_sinks_{index} [get_pins -of $write_net_{index} -filter {{DIRECTION == input}} *]
if {{[llength $write_sinks_{index}] != {count}}} {{error "Unexpected write enable sink count {index}"}}
puts "WE_BEFORE_{index}_BEGIN"
report_nets $write_net_{index} -connection -pin_display_limit 2000
puts "WE_BEFORE_{index}_END"
phys_opt -force_replication_on_nets {{{name}}} -fanout_threshold 2
'''
            write_reports += f'''puts "WE_AFTER_{index}_BEGIN"
report_nets -of_pins $write_sinks_{index} -connection -pin_display_limit 2000
puts "WE_AFTER_{index}_END"
'''
    build = f'''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
update_timing
set inherited_net [get_nets -hier {{{ADVANCE}}}]
if {{[llength $inherited_net] != 1}} {{error "Missing frozen advance control net"}}
phys_opt -force_replication_on_nets {{{ADVANCE}}} -fanout_threshold 128
set target_net [get_nets -hier {{{NET}}}]
if {{[llength $target_net] != 1}} {{error "Expected exactly one ROM admission net"}}
puts "TARGET_BEFORE_BEGIN"
report_nets $target_net -connection -pin_display_limit 2000
puts "TARGET_BEFORE_END"
write_verilog before_rom_clone.v -implement -top road_rom_current_down2_top
puts "ROM_REPLICATION_BEGIN"
phys_opt -force_replication_on_nets {{{NET}}} -fanout_threshold 16
puts "ROM_REPLICATION_DONE"
{write_steps}
route
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_current_down2_top
update_timing -mode final
puts "TARGET_AFTER_BEGIN"
report_nets [get_nets -hier {{u_rom/cnt_wait_b_n*}}] -connection -pin_display_limit 2000
puts "TARGET_AFTER_END"
puts "ADVANCE_AFTER_BEGIN"
report_nets [get_nets -hier {{*u_pre/u_round/i_advance*}}] -connection -pin_display_limit 2000
puts "ADVANCE_AFTER_END"
{write_reports}
{reports}'''
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path)\b", build, re.M)
    (work / "build.tcl").write_text(build, encoding="utf-8")
    bound = [work / name for name in ("frontend.sdc", "frontend.adc", "source_placed.db", "project_input.al", "build.tcl")]
    before = {str(p): sha(p) for p in bound}
    save(work / "input_manifest.json", before)
    save(work / "operation.json", {"rom_fanout_threshold": 16, "close_writes": close_writes,
         "write_enable_targets": WRITE_ENABLES if close_writes else [], "rtl_changed": False})
    save(ROOT / "status.json", {"status": "ROM_ADMISSION_PHYSICAL_RUNNING", "baseline_commit": "8b8c3ac3",
         "directory": str(work), "rtl_changed": False, "test_only": True})
    try:
        output = command([prior.TD, "build.tcl"], work, "td_launcher")
        assert "REPORT_COMPLETION_DONE" in output and 'finish command "route"' in output
        assert "PHY-8075 ERROR" not in output and "PHY-8023 ERROR" not in output
    except Exception as error:
        save(ROOT / "status.json", {"status": "PHYSICAL_ATTEMPT_FAILED", "error": repr(error), "directory": str(work)})
        raise
    finally:
        after = {str(p): sha(p) for p in bound}
        save(work / "input_check_after.json", {"same": before == after, "hashes": after})
        assert before == after
        check()
    report()


def close():
    assert not (ROOT / "local_checkpoint.json").exists()
    checkpoint = {str(p): sha(p) for p in (ROOT / "physical").iterdir() if p.is_file()}
    save(ROOT / "local_checkpoint.json", checkpoint)
    physical(close_writes=True)
    assert all(sha(Path(name)) == value for name, value in checkpoint.items())


def report():
    prior.check = check
    prior.report()
    work = sorted(ROOT.glob("physical*/physical_summary.json"), key=lambda p: p.stat().st_mtime)[-1].parent
    current = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
    original = json.loads((PHYSICAL / "physical_summary.json").read_text(encoding="utf-8"))
    failures = current["internal_failed_endpoints"]
    counts = dict(Counter(row["check"] for row in failures))
    target_failures = [row for row in failures if "u_rom/reg_address" in row["end"]]
    save(ROOT / "comparison.json", {"baseline_commit": "8b8c3ac3", "baseline": original, "candidate": current,
         "resource_delta": {name: current["resources"][name]["used"] - original["resources"][name]["used"]
                            for name in ("slice", "dsp", "eram", "io")}})
    save(ROOT / "status.json", {"status": "INTERNAL_TIMING_PASS_EXTERNAL_OPEN" if not failures else "INTERNAL_TIMING_FAILED",
         "baseline_commit": "8b8c3ac3", "all_internal_failure_checks": len(failures), "failure_counts": counts,
         "target_rom_address_failures": len(target_failures), "rtl_changed": False,
         "strict_delivery_ready": False, "test_only": True})
    check()


def compress():
    helper = load("prefetch_compression", BASE / "run.py")
    helper.ROOT = helper.prior.ROOT = helper.prior.helpers.ROOT = ROOT
    helper.check = check
    helper.compress()


def finalize():
    check()
    checkpoint = json.loads((ROOT / "local_checkpoint.json").read_text(encoding="utf-8"))
    changed = [name for name, value in checkpoint.items() if sha(Path(name)) != value]
    save(ROOT / "local_checkpoint_check.json", {"checked": len(checkpoint), "changed": changed})
    assert not changed, changed
    selected, rejected = ROOT / "physical", ROOT / "physical_attempt2"
    first, second = (json.loads((path / "physical_summary.json").read_text(encoding="utf-8"))
                     for path in (selected, rejected))
    assert len(first["internal_failed_endpoints"]) == 3 and len(second["internal_failed_endpoints"]) == 15
    for path in (selected, rejected):
        receipt = json.loads((path / "replication_equivalence.json").read_text(encoding="utf-8"))
        assert receipt["missing_duplicate_extra"] == 0
        assert receipt["after_netlist_sha256"] == sha(path / "routed_netlist.v")
        log = (path / "td_launcher.log").read_text(encoding="utf-8")
        assert "REPORT_COMPLETION_DONE" in log and 'finish command "route"' in log
    assert json.loads((rejected / "write_replication_equivalence.json").read_text(encoding="utf-8"))["status"].startswith("PASS_")
    original = json.loads((PHYSICAL / "physical_summary.json").read_text(encoding="utf-8"))
    save(ROOT / "comparison.json", {"baseline_commit": "8b8c3ac3", "baseline": original,
         "retained_directory": str(selected), "retained_candidate": first,
         "rejected_directory": str(rejected), "rejected_candidate": second,
         "decision": "Retain ROM admission repair only; reject extra WE replication: 3 to 15 internal setup failures"})
    status = {"status": "INTERNAL_TIMING_FAILED_ROM_REPAIR_RETAINED", "baseline_commit": "8b8c3ac3",
        "actual_retained_directory": str(selected), "rejected_directory": str(rejected),
        "baseline_internal_failure_checks": 21, "all_internal_failure_checks": 3,
        "target_rom_address_failures": 0, "worst_internal_setup_ns": -0.095,
        "rejected_internal_failure_checks": 15, "routing_completed": True,
        "rtl_changed": False, "logical_cycles_remeasured": False,
        "production_candidate_adopted": False, "strict_delivery_ready": False, "test_only": True,
        "next_scope": "Same-cycle load-qualification decode feeding two Stem and one down2 RAM WE endpoints; no further blind replication"}
    save(ROOT / "status.json", status)
    save(ROOT / "strict_status.json", {"source_record": str(BASE / "strict_status.json"),
         "source_record_sha256": sha(BASE / "strict_status.json"), "rtl_sources_identical": True,
         "checks": {name: {"status": "not_rerun_prior_matrix_unpublished"} for name in
                    ("compile", "ast", "readability", "comment", "naming", "profile", "testbench")},
         "toolchain": {"status": "failed", "route_completed": True, "all_internal_failure_checks": 3},
         "delivery_ready": False})
    paths = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".py", ".tcl", ".json", ".txt")
             and p.name != "artifact_manifest.json"]
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in paths})
    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("setup", "check", "physical", "close", "report", "compress", "finalize"))
    globals()[cli.parse_args().action]()
