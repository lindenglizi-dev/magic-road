"""同一ADC的最小ECO流程诊断；旧全局重布局失败版也冻结，不修改RTL/SDC。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
FIRST = ROOT.parent / "stem_location_constraint_20261014"
spec = importlib.util.spec_from_file_location("eco_shared", FIRST / "run.py")
shared = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = shared
spec.loader.exec_module(shared)
shared.ROOT = shared.old.ROOT = shared.old.prior.ROOT = shared.old.prior.helpers.ROOT = ROOT
shared.LAST = FIRST
sha, save = shared.sha, shared.save


def setup():
    shared.setup()
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    records.update({str(path): sha(path) for path in FIRST.rglob("*") if path.is_file()})
    save(ROOT / "frozen.json", records)
    shared.check()


def finish():
    shared.check()
    work = ROOT / "physical"
    inputs = json.loads((work / "input_manifest.json").read_text(encoding="utf-8"))
    assert all(sha(Path(name)) == digest for name, digest in inputs.items())
    pins = json.loads((work / "connection_check.json").read_text(encoding="utf-8"))
    assert not pins["positioned"] and pins["literal_pins_identical"]
    assert not (work / "pr.db").exists() and not (work / "route.log").exists()
    # Remove only the known generated date line; retain every HDL line/attribute/comment.
    netlists = [(work / name).read_text(encoding="utf-8").splitlines() for name in ("before_place.v", "after_place.v")]
    assert all(lines[0].startswith("// Verilog netlist created") and re.fullmatch(
        r"// \w{3} \w{3} +\d+ \d{2}:\d{2}:\d{2} \d{4}", lines[1]) for lines in netlists)
    assert netlists[0][:1] + netlists[0][2:] == netlists[1][:1] + netlists[1][2:]
    first = json.loads((FIRST / "result.json").read_text(encoding="utf-8"))
    save(ROOT / "result.json", {"decision": "STOP_LOCATION_BRANCH_RETAIN_60b37283",
         "baseline_internal_setup_failures": 3, "baseline_worst_ns": -0.095,
         "global_replace_internal_setup_failures": len(first["candidate"]["internal_failed_endpoints"]),
         "global_replace_worst_internal_ns": min(row["slack_ns"] for row in first["candidate"]["internal_failed_endpoints"]),
         "global_replace_new_failed_endpoints": len(first["new_failed_endpoints"]),
         "eco_position_applied": False, "eco_pins_identical": True,
         "eco_netlist_identical_except_date": True, "eco_route_or_sta_run": False,
         "frozen_files_checked": len(json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))),
         "old_files_unchanged": True, "input_files_unchanged": True,
         "rtl_sdc_timing_exceptions_changed": False, "numeric_cycles_remeasured": False,
         "strict_reused_from": str(FIRST / "gate/stem.json"), "strict_record_sha256": sha(FIRST / "gate/stem.json"),
         "strict_delivery_ready": False, "training_production_board_bitstream_flash": False})
    save(ROOT / "status.json", {"status": "LOCATION_BRANCH_FINISHED_REJECT_BOTH_RETAIN_BASELINE",
         "retained_directory": str(shared.BASE), "setup_failures": 3, "worst_internal_ns": -0.095,
         "strict_delivery_ready": False, "test_only": True,
         "next_decision": "Approve a separate loader control/commit RTL candidate; no more blind location searches"})
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in ROOT.rglob("*") if path.is_file()
         and path.suffix in (".py", ".tcl", ".adc", ".sdc", ".json", ".txt", ".log", ".al", ".rpt")
         and path.name != "artifact_manifest.json"})


def place():
    shared.check()
    work = ROOT / "physical"
    output = shared.command([shared.TD, (ROOT / "place.tcl").as_posix()], work, "place")
    assert "LOCATION_PLACED_NOT_ROUTED" in output and "ERROR" not in output
    before, after = [output.split("LOCATION_" + name + "_BEGIN", 1)[1].split("LOCATION_" + name + "_END", 1)[0]
                     for name in ("BEFORE", "AFTER")]
    positioned = bool(re.search(r"Grid\s*\|\s*col=36 row=24\b", after) and
                      re.search(r"Offset\s*\|\s*3\b", after) and re.search(r"IsFixed\s*\|\s*True", after))
    pattern = r"^RUN-1001 :\s*\d+\s*\|\s*(\S+)\s*\|\s*\[\s*\d+\s+\d+\]\s*\|\s*(.*?)\s*$"
    pins = [dict(re.findall(pattern, part, re.M)) for part in (before, after)]
    assert len(pins[0]) == len(pins[1]) == 41
    save(work / "connection_check.json", {"positioned": positioned, "literal_pins_identical": pins[0] == pins[1],
         "before": pins[0], "after": pins[1], "flow": "place -eco, same single ADC"})
    assert positioned, "ECO did not apply the approved location; do not route"
    assert pins[0] == pins[1], "ECO changed target connections; stop, do not broaden equivalence checker"
    save(ROOT / "status.json", {"status": "ACTUAL_LOCATION_CONFIRMED_NOT_ROUTED", "position": "x36y24z3", "test_only": True})
    shared.check()


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "place", "route", "gate", "finish"))
    action = parser.parse_args().action
    try:
        if action in ("setup", "place", "finish"):
            globals()[action]()
        elif action == "gate":
            shared.old.gate()
        else:
            getattr(shared, action)()
    except Exception as error:
        failure = {"status": "STOP_ECO_BRANCH_RETAIN_OLD_BASELINE", "action": action, "error": repr(error), "test_only": True}
        save(ROOT / "status.json", failure)
        save(ROOT / (action + "_failure.json"), failure)
        raise
