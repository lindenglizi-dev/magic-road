"""旧3项违例版的单次局部布局验证；不改RTL/SDC，不生成位流。"""
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
BASE = REPORTS / "prefetch_admission_20261014/physical"
LAST = REPORTS / "stem_independent_bank_20261014"
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
GUIDE = TD.parents[1] / "doc/SWUG/SWUG105_TCL_Command_User_Guide.pdf"
spec = importlib.util.spec_from_file_location("locality_helpers", REPORTS / "rom_current_down2_20261013/run.py")
prior = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = prior
spec.loader.exec_module(prior)
prior.ROOT = prior.helpers.ROOT = ROOT
sha, save, fresh, command = prior.sha, prior.save, prior.fresh, prior.command


def check():
    records = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in records.items() if sha(Path(name)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(records), "changed": changed})
    assert not changed, changed


prior.check = check


def setup():
    assert not (ROOT / "frozen.json").exists()
    records = json.loads((LAST / "frozen.json").read_text(encoding="utf-8"))
    records.update(json.loads((LAST / "artifact_manifest.json").read_text(encoding="utf-8")))
    records.update({str(p): sha(p) for p in LAST.iterdir() if p.is_file()})
    records.update({str(p): sha(p) for p in (TD, GUIDE)})
    save(ROOT / "frozen.json", records)
    save(ROOT / "status.json", {"status": "FROZEN_INSPECT_BEFORE_SINGLE_LOCALITY_CANDIDATE",
        "baseline_commit": "60b37283", "initial_head": "e8f473f3", "rtl_changed": False,
        "sdc_adc_changed": False, "test_only": True, "strict_delivery_ready": False})
    work = fresh("documentation")
    command(["D:/texlive/2026/bin/windows/pdftotext.exe", "-layout", GUIDE, work / "td_tcl.txt"], work, "extract")
    assert "place" in (work / "td_tcl.txt").read_text(encoding="utf-8")
    check()


def help_commands():
    work = fresh("command_help")
    output = command([TD, (ROOT / "command_help.tcl").as_posix()], work, "td")
    assert "LOCALITY_COMMAND_HELP_DONE" in output


def gate():
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(prior.helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    source = REPORTS / "weight_address_stem_write_20261013/rtl/road_stem_tile_scheduler.v"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, source,
        "--json", work / "stem.json", "--markdown", work / "stem.md"], work, "stem", allowed=(0, 1, 2))


def inspect():
    work = fresh("inspection")
    shutil.copyfile(BASE / "pr.db", work / "reference_pr.db")
    shutil.copyfile(BASE / "source_placed.db", work / "source_placed.db")
    project = (BASE / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(BASE.as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    shutil.copyfile(work / "road_rom_current_down2_top.al", work / "project_input.al")
    before = {str(p): sha(p) for p in work.iterdir() if p.is_file() and p.name != "road_rom_current_down2_top.al"}
    save(work / "input_manifest.json", before)
    output = command([TD, (ROOT / "inspect.tcl").as_posix()], work, "td")
    assert "LOCALITY_INSPECTION_DONE" in output
    assert all(sha(Path(name)) == digest for name, digest in before.items())


def move():
    """只构建一个移动单元的placed候选，先保存前后连接供对比，尚不布线。"""
    work = fresh("physical")
    for name in ("source_placed.db", "frontend.sdc", "frontend.adc", "gate_netlist.v"):
        shutil.copyfile(BASE / name, work / name)
    project = (BASE / "project_input.al").read_text(encoding="utf-8")
    project = project.replace(BASE.as_posix(), work.as_posix())
    (work / "road_rom_current_down2_top.al").write_text(project, encoding="utf-8")
    shutil.copyfile(work / "road_rom_current_down2_top.al", work / "project_input.al")
    save(work / "input_manifest.json", {str(work / name): sha(work / name) for name in
        ("source_placed.db", "frontend.sdc", "frontend.adc", "gate_netlist.v", "project_input.al")})
    output = command([TD, (ROOT / "move.tcl").as_posix()], work, "move")
    assert "LOCALITY_MOVE_DONE_NOT_ROUTED" in output and (work / "local_placed.db").is_file()
    after = output.split("LOCALITY_AFTER_BEGIN", 1)[1].split("LOCALITY_AFTER_END", 1)[0]
    assert re.search(r'Grid\s*\|\s*col=36 row=24\b', after), "Command returned but target did not move"
    assert "Successfully moved 1 instances" in output and "ERROR" not in output and "skipped unknown instance" not in output


def move_compare():
    work = sorted(ROOT.glob("physical*/local_placed.db"), key=lambda path: path.stat().st_mtime)[-1].parent
    entry = f"import sys;sys.path.insert(0,{str(prior.helpers.SKILL)!r});from scripts.python.quality.verify_verilog_comment_only import main;raise SystemExit(main())"
    output = command([sys.executable, "-B", "-X", "utf8", "-c", entry,
        work / "before_move.v", work / "after_move.v"], work, "connections_unchanged")
    assert "PASS" in output
    save(work / "move_connection_receipt.json", {"status": "PASS_TOKEN_EQUIVALENT_PLACEMENT_ONLY",
        "before_sha256": sha(work / "before_move.v"), "after_sha256": sha(work / "after_move.v"),
        "scope": "All HDL tokens unchanged across native move; comment R_POSITION may change; not analog/timing proof"})


def compress():
    work = fresh("compression_check")
    before = {str(p): sha(p) for p in ROOT.rglob("*") if p.is_file() and p.suffix not in (".pyc", ".dmp")
              and p.name != "compression_receipt.json"}
    command(["compact.exe", "/C", "/S:" + str(ROOT), "/I", "/Q", "*"], work, "compression")
    assert all(sha(Path(name)) == digest for name, digest in before.items())
    save(ROOT / "compression_receipt.json", {"content_hashes": before, "same": True,
         "scope": "Only this new directory; no deletion; NTFS compression preserves bytes"})


def finalize():
    check()
    baseline = json.loads((BASE / "physical_summary.json").read_text(encoding="utf-8"))
    attempts = []
    for work in sorted(ROOT.glob("physical*")):
        log = work / "move.log"
        if not work.is_dir() or not log.is_file():
            continue
        text = log.read_text(encoding="utf-8")
        after = text.split("LOCALITY_AFTER_BEGIN", 1)[-1].split("LOCALITY_AFTER_END", 1)[0] if "LOCALITY_AFTER_BEGIN" in text else ""
        actual_grid = re.search(r'Grid\s*\|\s*col=(\d+) row=(\d+)', after)
        moved = re.search(r'Successfully moved (\d+) instances', text)
        attempts.append({"directory": str(work), "moved_instances": int(moved[1]) if moved else 0,
            "after_grid": list(map(int, actual_grid.groups())) if actual_grid else None,
            "error_lines": [line for line in text.splitlines() if "ERROR" in line or "skipped unknown instance" in line],
            "log_sha256": sha(log), "routed": (work / "pr.db").exists()})
    assert len(attempts) == 5 and all(row["moved_instances"] == 0 and not row["routed"] for row in attempts)
    assert all(row["after_grid"] in (None, [35, 22]) for row in attempts)
    frozen_inputs = json.loads((ROOT / "inspection/input_manifest.json").read_text(encoding="utf-8"))
    database_checks = {name: sha(Path(name)) == digest for name, digest in frozen_inputs.items() if name.endswith(".db")}
    assert all(database_checks.values())
    gate_data = json.loads((ROOT / "gate/stem.json").read_text(encoding="utf-8"))
    save(ROOT / "result.json", {"decision": "STOP_NATIVE_MOVE_BRANCH_NO_ROUTING", "attempts": attempts,
        "baseline_resources": baseline["resources"], "baseline_failed_endpoints": baseline["internal_failed_endpoints"],
        "candidate_timing_measured": False, "candidate_resources_measured": False,
        "inspection_databases_unchanged": database_checks,
        "strict": {key: gate_data[key] for key in ("checks", "errors", "strict_warnings", "delivery_ready")},
        "strict_scope": "Unchanged Stem definition; not full-closure production pass",
        "python_script_strict_skills": "Unavailable; syntax and actual commands only",
        "next_decision": "Approve one physical location constraint in isolated candidate and replace API move with re-placement; SDC/RTL unchanged"})
    save(ROOT / "status.json", {"status": "BLOCKED_NATIVE_MOVE_NAME_PARSING_NO_PHYSICAL_CANDIDATE",
        "retained_directory": str(BASE), "baseline_internal_setup_failures": 3, "baseline_worst_slack_ns": -0.095,
        "new_successful_moves": 0, "new_route_or_sta": False, "rtl_sdc_adc_changed": False,
        "production_training_board_flash_bitstream": False, "strict_delivery_ready": False,
        "awaiting": "One isolated physical-location constraint and re-placement approval"})
    save(ROOT / "artifact_manifest.json", {str(p): sha(p) for p in ROOT.rglob("*") if p.is_file()
        and p.suffix in (".py", ".tcl", ".json", ".txt", ".log", ".adc", ".sdc")
        and p.name not in ("artifact_manifest.json", "td_tcl.txt") and "gate" not in p.relative_to(ROOT).parts})


if __name__ == "__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "check", "help_commands", "gate", "inspect", "move", "move_compare", "compress", "finalize"))
    globals()[parser.parse_args().action]()
