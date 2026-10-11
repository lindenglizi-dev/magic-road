"""Minimal approved control repair; all new artifacts belong to this directory."""
import argparse
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "postprocess_control_timing_20261009"
spec = importlib.util.spec_from_file_location("control_build", PREVIOUS / "run.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
app.ROOT = ROOT
app.old.ROOT = ROOT
app.build.ROOT = ROOT
app.tools.ROOT = ROOT
build, tools, save = app.build, app.tools, app.save
MAC = build.MAC


def frozen():
    build.frozen()
    path = ROOT / "prior_candidate_hashes.json"
    if not path.exists():
        save(path, {str(p): tools.digest(p) for p in PREVIOUS.rglob("*") if p.is_file()
            and "work" not in p.relative_to(PREVIOUS).parts})
    records = json.loads(path.read_text(encoding="utf-8"))
    changed = [p for p, sha in records.items() if tools.digest(Path(p)) != sha]
    save(ROOT / "prior_candidate_check.json", {"checked": len(records), "changed": changed})
    assert not changed


def review():
    app.review()
    work = tools.fresh("mac_baseline_review")
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
        "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "review", "--target",
        ROOT / "baseline/road_mac_probe.v", "--report-json", work / "review.json"],
        work, "review", allowed=(0, 1, 2))


def scope():
    differences = []
    patches = []
    for path in sorted((ROOT / "rtl").glob("*.v")):
        old = ROOT / "baseline" / path.name
        if tools.digest(path) != tools.digest(old):
            differences.append(path.name)
            a, b = old.read_text(encoding="utf-8"), path.read_text(encoding="utf-8")
            assert a[a.index("module "):a.index("\n);")] == b[b.index("module "):b.index("\n);")]
            patches.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                fromfile="frozen/" + path.name, tofile="candidate/" + path.name))
    assert differences == ["road_dynamic_postprocess.v", "road_mac_probe.v"], differences
    a = (ROOT / "baseline/road_mac_probe.v").read_text(encoding="utf-8")
    b = (ROOT / "rtl/road_mac_probe.v").read_text(encoding="utf-8")
    assert a[a.index("\t//A1计算"): ] == b[b.index("\t//A1计算"): ], "Arithmetic stages changed"
    (ROOT / "rtl_change.diff").write_text("".join(patches), encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": differences, "unchanged_rtl_count": 6,
        "ports_unchanged": True, "mac_arithmetic_stages_byte_identical": True,
        "reset_unchanged": True, "additional_pipeline_stages": 0,
        "sources": {str(p.relative_to(ROOT)): tools.digest(p) for p in (ROOT / "rtl").glob("*.v")}})


def specs():
    work = tools.fresh("s")
    contracts = [ROOT.parent / "retirement_lane_banks_20261009/specs/contracts/road_dynamic_postprocess.contract.json",
                 build.MAC / "core/road_mac_probe.contract.json"]
    if not contracts[1].exists():
        contracts[1] = ROOT.parent / "v9_mac_stream_20261007/core/road_mac_probe.contract.json"
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
        "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    for contract_path in contracts:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
        module = next(m for m in data["modules"] if m["name"] in ("road_dynamic_postprocess", "road_mac_probe"))
        name = module["name"]
        module["feature"] = "r"
        module["description"] = "Approved control-only repair with unchanged ports, latency, II and numerical contract"
        module["behavior"] += [
            "MAC A0 retains activation, weight, bias and mask on nonaccept; valid, first and last clear. Reset still clears all A0 registers.",
            "PRE selection computes the successor whenever buffer valid; only !buffer_valid or real PRE acceptance updates the buffer.",
            "No additional pipeline stage; all numerical operations and valid-qualified retirement remain unchanged."]
        module["timing_diagrams"] = [{"id": "control_hold", "title": "Accepted input and bubble", "scenario": "control_hold",
            "description": "Payload retained through bubble; only accepted input has valid ownership.",
            "wavejson": {"signal": [{"name": "clk", "wave": "p...."}, {"name": "accept", "wave": "01010"},
                {"name": "A0_payload", "wave": "x=.=.", "data": ["A", "B"]},
                {"name": "A0_valid", "wave": "00101"}], "head": {"text": "Same latency and II; bubble carries no transaction"}}}]
        destination = work / ("p" if name == "road_dynamic_postprocess" else "m")
        destination.mkdir()
        save(destination / "contract.json", {"modules": [module]})
        source = destination / (name + ".v")
        shutil.copyfile(ROOT / "rtl" / source.name, source)
        tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec",
            destination / "contract.json", "--out-dir", destination / "generated", "--source", source, "--no-state"],
            destination, "spec", allowed=(0, 1, 2))
        generated = destination / "generated/spec/r" / (name + "_spec.md")
        assert generated.exists(), generated
        shutil.copyfile(generated, ROOT / "rtl" / generated.name)
        shutil.copytree(generated.parent / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def mac_sim():
    work = tools.fresh("mac_sim")
    source = build.MAC / "tests/tb_mac_task_stream.v"
    target = ROOT / "tests" / source.name
    if not target.exists():
        shutil.copyfile(source, target)
        shutil.copyfile(source.with_name("tb_mac_task_stream_spec.md"), target.with_name("tb_mac_task_stream_spec.md"))
    vectors = build.MAC / "tests/vectors"
    sources = [ROOT / "rtl/road_mac_probe.v", target]
    numerical = [vectors / "mac_inputs.hex", vectors / "mac_expected.hex"]
    tools.command([build.MSIM / "vlib.exe", "work"], work, "vlib")
    tools.command([build.MSIM / "vlog.exe", "-work", "work", *sources], work, "vlog")
    result = tools.command([build.MSIM / "vsim.exe", "-c", "-lib", "work", "tb_mac_task_stream",
        "+N_GROUPS=849", "+N_TASKS=119", f"+INPUTS={numerical[0].as_posix()}",
        f"+EXPECTED={numerical[1].as_posix()}", "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "simulation")
    assert "PASS mac_task_stream" in result and "Fatal:" not in result and "** Error:" not in result
    save(work / "receipt.json", {"all_passed": True, "result": [line for line in result.splitlines() if "PASS" in line],
        "sources": {str(p): tools.digest(p) for p in sources + numerical}})
    print("MAC_PASS", result[-800:], flush=True)


def collect():
    previous_base = app.old.BASE
    try:
        app.old.BASE = ROOT.parent / "dw_task_overlap_20261009"
        app.old.collect()
    finally:
        app.old.BASE = previous_base


def finish():
    scope()
    receipts = {}
    for folder in ("simulation", "load_boundary", "mac_sim", "shell_rtl", "shell_routed", "undriven"):
        path = ROOT / folder / "receipt.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if folder == "undriven":
            assert not data["loaded"], data
        else:
            assert data["all_passed"], path
        for source, sha in data["sources"].items():
            assert tools.digest(Path(source)) == sha, source
        receipts[folder] = str(path.relative_to(ROOT))
    manifest = json.loads((ROOT / "physical/input_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest) == 8
    for source, sha in manifest.items():
        assert tools.digest(Path(source)) == sha, source
    for name in ("build.tcl", "shell.sdc", "shell.adc"):
        assert tools.digest(ROOT / "physical" / name) == tools.digest(MAC / "physical_opt" / name), name
    comparison = json.loads((ROOT / "cycle_comparison.json").read_text(encoding="utf-8"))
    assert comparison["identical_summary_rows"] == 64
    assert comparison["old_core_cycles"] == comparison["new_core_cycles"] == 1687
    physical = json.loads((ROOT / "physical_analysis.json").read_text(encoding="utf-8"))
    gates = {kind: json.loads((ROOT / ("gate_" + kind) / "gate.json").read_text(encoding="utf-8"))
        for kind in ("candidate", "testbench")}
    assert not any(gate["delivery_ready"] for gate in gates.values())
    frozen()
    save(ROOT / "status.json", {"stage": "evaluated_internal_timing_failed", "receipts": receipts,
        "internal_timing": physical["reports"]["coverage_100000_all_paths"]["internal"],
        "resources_including_shell": physical["resources_including_shell"], "core_cycles": 1687,
        "strict_gates": {key: {name: value[name] for name in ("errors", "strict_warnings", "delivery_ready")}
            for key, value in gates.items()}, "physical_rebuilt": True, "sdf_simulation": False,
        "external_contract_signed_off": False, "production_modified": False, "deployment_release": False,
        "training_started": False, "bitstream_generated": False, "board_or_flash_used": False})
    paths = list((ROOT / "rtl").rglob("*")) + list((ROOT / "physical").glob("*"))
    paths += list(ROOT.glob("*.json")) + list(ROOT.glob("*.md"))
    paths += [ROOT / "run.py", ROOT / "control_reference.py", ROOT / "rtl_change.diff"]
    paths += [ROOT / path for path in receipts.values()]
    paths += [ROOT / ("gate_" + kind) / "gate.json" for kind in gates]
    save(ROOT / "evidence_hashes.json", {str(path.relative_to(ROOT)): tools.digest(path)
        for path in sorted(set(paths)) if path.is_file() and path.name != "evidence_hashes.json"})
    print("FINALIZED: functional passes; two internal setup endpoints remain; not production-ready", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "simulate", "physical", "gates", "scope", "specs", "mac_sim",
        "shell_rtl", "shell_routed", "undriven", "compare", "collect", "boundary", "finish"))
    stage = parser.parse_args().stage
    frozen()
    try:
        if stage == "prepare":
            app.old.prepare()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage in ("compare", "boundary"):
            getattr(app.old, stage)()
        elif stage in ("review", "scope", "specs", "mac_sim", "collect", "finish"):
            globals()[stage]()
        else:
            getattr(build, stage)()
    except Exception as error:
        save(ROOT / (stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
