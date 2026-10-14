"""单条官方ADC位置约束诊断；只写本目录，冻结RTL与SDC不变。"""
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
LAST = REPORTS / "stem_we_locality_20261014"
BASE = REPORTS / "prefetch_admission_20261014/physical"
spec = importlib.util.spec_from_file_location("constraint_helpers", LAST / "run.py")
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
old.ROOT = old.prior.ROOT = old.prior.helpers.ROOT = ROOT
sha, save, fresh, command = old.sha, old.save, old.fresh, old.command
TD = old.TD


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in records.items() if sha(Path(name)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


old.prior.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((LAST / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((LAST / "artifact_manifest.json").read_text(encoding="utf-8")))
    records.update({str(p): sha(p) for p in LAST.iterdir() if p.is_file()})
    save(ROOT / "frozen.json", records)
    check()
    work = fresh("physical")
    for name in ("source_placed.db", "frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(BASE / name, work / name)
    project = (BASE / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(BASE.as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    shutil.copyfile(work / "road_rom_current_down2_top.al", work / "project_input.al")
    shutil.copyfile(ROOT / "locality.adc", work / "locality.adc")
    save(work / "input_manifest.json", {str(work / name): sha(work / name) for name in
         ("source_placed.db", "frontend.sdc", "frontend.adc", "gate_netlist.v", "project_input.al", "locality.adc")})
    save(ROOT / "status.json", {"status": "FROZEN_ONE_ADC_LOCATION_PENDING",
        "baseline_commit": "60b37283", "initial_head": "9467c89d", "rtl_sdc_changed": False,
        "physical_constraints_added": 1, "timing_exceptions_added": 0, "test_only": True})


def place():
    check()
    work = ROOT / "physical"
    command([TD, (ROOT / "place.tcl").as_posix()], work, "place")
    validate_place()


def validate_place():
    work = ROOT / "physical"
    output = (work / "place.log").read_text(encoding="utf-8")
    assert "LOCATION_PLACED_NOT_ROUTED" in output, "No complete placement; inspect place.log"
    after = output.split("LOCATION_AFTER_BEGIN", 1)[1].split("LOCATION_AFTER_END", 1)[0]
    actual = re.search(r"Grid\s*\|\s*col=(\d+) row=(\d+)", after)
    assert actual and actual.groups() == ("36", "24"), "ADC accepted but actual position not as requested"
    assert re.search(r"Offset\s*\|\s*3\b", after), "Requested z3 not proven"
    assert "ERROR" not in output, "Native tool may return 0 after errors"
    assert (work / "local_placed.db").is_file()
    before = output.split("LOCATION_BEFORE_BEGIN", 1)[1].split("LOCATION_BEFORE_END", 1)[0]
    # Native report rows only: keep every input/output pin and its connected net.
    pattern = r"^RUN-1001 :\s*\d+\s*\|\s*(\S+)\s*\|\s*\[\s*\d+\s+\d+\]\s*\|\s*(.*?)\s*$"
    connections = [dict(re.findall(pattern, section.split('start command "report_cells -grid', 1)[0], re.M))
                   for section in (before, after)]
    assert len(connections[0]) == 41, "Require complete native target pin inventory"
    from connection_check import verify
    proof = verify(work, connections)
    save(work / "connection_check.json", proof)
    previous = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    if previous.get("status") == "FAILED_NO_AUTOMATIC_PROMOTION" and not (ROOT / "previous_check_failure.json").exists():
        save(ROOT / "previous_check_failure.json", previous)
    save(ROOT / "status.json", {"status": "ACTUAL_LOCATION_CONFIRMED_NOT_ROUTED", "position": "x36y24z3",
         "test_only": True, "rtl_sdc_changed": False})
    check()


def route():
    check()
    assert json.loads((ROOT / "status.json").read_text(encoding="utf-8"))["status"] == "ACTUAL_LOCATION_CONFIRMED_NOT_ROUTED"
    work = ROOT / "physical"
    build = "import_device ph1_35p.db -package PH1P35MDG324 -speed 3\nopen_project road_rom_current_down2_top.al -single_run\nimport_db local_placed.db\n"
    tail = (BASE / "build.tcl").read_text(encoding="utf-8").split("route\n", 1)[1]
    (work / "build.tcl").write_text(build + "route\n" + tail, encoding="utf-8")
    save(ROOT / "status.json", {"status": "CONFIRMED_LOCATION_ROUTING_AND_FULL_STA", "test_only": True})
    output = command([TD, "build.tcl"], work, "route")
    assert 'finish command "route"' in output and "REPORT_COMPLETION_DONE" in output
    assert "ERROR" not in output
    check()
    old.prior.report()


def inspect_final():
    work = ROOT / "physical"
    before_db = sha(work / "pr.db")
    output = command([TD, (ROOT / "final_inspect.tcl").as_posix()], work, "final_inspect")
    assert "FINAL_LOCATION_INSPECTION_DONE" in output and "ERROR" not in output
    after = output.split("FINAL_LOCATION_BEGIN", 1)[1].split("FINAL_LOCATION_END", 1)[0]
    assert re.search(r"Grid\s*\|\s*col=36 row=24\b", after)
    assert re.search(r"Offset\s*\|\s*3\b", after) and re.search(r"IsFixed\s*\|\s*True", after)
    pattern = r"^RUN-1001 :\s*\d+\s*\|\s*(\S+)\s*\|\s*\[\s*\d+\s+\d+\]\s*\|\s*(.*?)\s*$"
    pins = dict(re.findall(pattern, after, re.M))
    before = json.loads((work / "connection_check.json").read_text(encoding="utf-8"))["before"]
    from connection_check import verify
    proof = verify(work, [before, pins], "routed_netlist.v")
    assert sha(work / "pr.db") == before_db
    save(work / "final_connection_check.json", dict(proof, position="x36y24z3", database_unchanged=True))


def finish():
    check()
    work = ROOT / "physical"
    inputs = json.loads((work / "input_manifest.json").read_text(encoding="utf-8"))
    assert all(sha(Path(name)) == digest for name, digest in inputs.items())
    if (work / "connection_check.json").exists():
        from connection_check import verify
        proof = json.loads((work / "connection_check.json").read_text(encoding="utf-8"))
        assert verify(work, [proof["before"], proof["after"]]) == proof
    baseline = json.loads((BASE / "physical_summary.json").read_text(encoding="utf-8"))
    result = {"baseline_commit": "60b37283", "baseline": baseline,
        "input_files_unchanged": True, "rtl_sdc_changed": False,
        "added_physical_constraints": 1, "added_timing_exceptions": 0,
        "production_training_board_flash_bitstream": False,
        "strict_scope": "Unchanged Stem only; not full closure",
        "strict": json.loads((ROOT / "gate/stem.json").read_text(encoding="utf-8")),
        "python_script_strict_skills": "Not available; Python AST and actual command execution only"}
    guide = TD.parents[1] / "doc/TD_User_Guide_V6.2.pdf"
    result["official_constraint_reference"] = {"path": str(guide), "sha256": sha(guide),
         "section": "9.1 set_inst_assignment {inst_name} {attributes}; location=x*y*z*"}
    if (work / "physical_summary.json").exists():
        candidate = json.loads((work / "physical_summary.json").read_text(encoding="utf-8"))
        old_fail, new_fail = baseline["internal_failed_endpoints"], candidate["internal_failed_endpoints"]
        old_keys = {(row["check"], row["end"]) for row in old_fail}
        added = [row for row in new_fail if (row["check"], row["end"]) not in old_keys]
        better = (len(new_fail) < len(old_fail) and not added and
                  min((row["slack_ns"] for row in new_fail), default=0) > min(row["slack_ns"] for row in old_fail))
        result.update(candidate=candidate, new_failed_endpoints=added, retain_candidate=better,
                      decision="CANDIDATE_BETTER_NOT_PRODUCTION" if better else "RETAIN_OLD_BASELINE_REJECT_CANDIDATE")
        save(ROOT / "status.json", {"status": result["decision"], "internal_failed_endpoints": len(new_fail),
             "worst_internal_ns": min((row["slack_ns"] for row in new_fail), default=0),
             "retained_baseline": str(BASE), "test_only": True, "strict_delivery_ready": False})
    else:
        result.update(retain_candidate=False, decision="NO_NEW_ROUTED_TIMING_RETAIN_OLD_BASELINE")
    save(ROOT / "result.json", result)
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*") if p.is_file()
         and p.suffix in (".py", ".tcl", ".adc", ".sdc", ".json", ".log", ".rpt", ".txt", ".area", ".ts")
         and p.name != "artifact_manifest.json"})


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "place", "validate_place", "route", "inspect_final", "gate", "finish"))
    action = parser.parse_args().action
    try:
        old.gate() if action == "gate" else globals()[action]()
    except Exception as error:
        save(ROOT / "status.json", {"status": "FAILED_NO_AUTOMATIC_PROMOTION", "action": action,
             "error": repr(error), "retained_baseline": str(BASE), "test_only": True})
        raise
