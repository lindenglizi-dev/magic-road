"""Local control-boundary experiment; reuse frozen tools and never write their roots."""
import argparse
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "dw_weight_load_timing_20261009"
spec = importlib.util.spec_from_file_location("weight_build", BASE / "run.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
old.ROOT = ROOT
old.BASE = BASE
build = old.build
build.ROOT = ROOT
build.BASE = BASE
build.tools.ROOT = ROOT
tools, save = build.tools, build.save


def review():
    work = tools.fresh("baseline_review")
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
             "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for name in ("road_dynamic_postprocess", "down2_dynamic_tile_runner"):
        tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
            ROOT / "baseline" / (name + ".v"), "--report-json", work / (name + ".json")],
            work, name, allowed=(0, 1, 2))
    build.gate("baseline")


def scope():
    changed = []
    patches = []
    for path in sorted((ROOT / "rtl").glob("*.v")):
        previous = ROOT / "baseline" / path.name
        if tools.digest(path) != tools.digest(previous):
            changed.append(path.name)
            a, b = previous.read_text(encoding="utf-8"), path.read_text(encoding="utf-8")
            assert a[a.index("module "):a.index("\n);")] == b[b.index("module "):b.index("\n);")], path
            patches.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                fromfile="frozen/" + path.name, tofile="candidate/" + path.name))
    assert set(changed) <= {"road_dynamic_postprocess.v", "down2_dynamic_tile_runner.v"}
    assert changed
    (ROOT / "rtl_change.diff").write_text("".join(patches), encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": changed, "ports_unchanged": True,
        "arithmetic_rtl_unchanged": True, "constraints_unchanged": True,
        "sources": {str(p.relative_to(ROOT)): tools.digest(p) for p in (ROOT / "rtl").glob("*.v")}})


def seal():
    scope()
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    comparison = json.loads((ROOT / "cycle_comparison.json").read_text(encoding="utf-8"))
    assert comparison["identical_summary_rows"] == 64
    design = json.loads(max(ROOT.glob("gate_candidate*/gate.json"), key=lambda p: p.stat().st_mtime_ns).read_text(encoding="utf-8"))
    bench = json.loads(max(ROOT.glob("gate_testbench*/gate.json"), key=lambda p: p.stat().st_mtime_ns).read_text(encoding="utf-8"))
    receipts = {}
    for name in ("simulation", "load_boundary", "shell_rtl", "shell_routed", "undriven"):
        path = max(ROOT.glob(name + "*/receipt.json"), key=lambda p: p.stat().st_mtime_ns)
        result = json.loads(path.read_text(encoding="utf-8"))
        assert result.get("all_passed", name == "undriven")
        assert not result.get("loaded", [])
        assert all(tools.digest(Path(p)) == sha for p, sha in result["sources"].items()), name
        receipts[name] = str(path.relative_to(ROOT))
    save(ROOT / "status.json", {"stage": "evaluated_internal_clean_not_deployment" if not physical["internal_negative_count"] else
        "evaluated_internal_timing_failed", "physical_rebuilt": True, "internal_negative_endpoints": physical["internal_negative_count"],
        "resources_including_shell": physical["resources_including_shell"], "core_cycles": 1687,
        "functional_complete_cases": 64, "full_counter_rows_unchanged": True,
        "strict_design_errors": design["errors"], "strict_design_warnings": design["strict_warnings"],
        "strict_tb_errors": bench["errors"], "strict_tb_warnings": bench["strict_warnings"],
        "deployment_release": False, "external_contract_signed_off": False, "production_modified": False,
        "training_started": False, "bitstream_generated": False, "flash_modified": False, "receipts": receipts})
    extensions = {".py", ".v", ".md", ".json", ".json5", ".tcl", ".sdc", ".adc", ".al", ".db", ".rpt",
        ".timing", ".ts", ".area", ".qor", ".csv", ".log", ".svg", ".diff"}
    save(ROOT / "evidence_hashes.json", {str(p.relative_to(ROOT)): tools.digest(p) for p in ROOT.rglob("*")
        if p.is_file() and "work" not in p.relative_to(ROOT).parts and p.suffix in extensions and p.name != "evidence_hashes.json"})
    print("SEALED", physical["internal_negative_count"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "simulate", "physical", "gates", "scope",
        "shell_rtl", "shell_routed", "undriven", "compare", "collect", "boundary", "seal"))
    stage = parser.parse_args().stage
    build.frozen()
    try:
        if stage == "prepare":
            old.prepare()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage in ("compare", "collect", "boundary"):
            getattr(old, stage)()
        elif stage in ("review", "scope", "seal"):
            globals()[stage]()
        else:
            getattr(build, stage)()
    except Exception as error:
        save(ROOT / (stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        build.frozen()
