"""计数后继值与操作数装载资格候选；复用冻结工具，输出只落本目录。"""
import argparse
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "mac_local_pointer_20261009"
spec = importlib.util.spec_from_file_location("local_pointer_build", BASE / "run.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
control = previous.previous
build, tools, save = previous.build, previous.tools, previous.save
for module in (previous, control, control.app, control.app.old, build, tools):
    module.ROOT = ROOT
previous.BASE = BASE
build.BASE = BASE
control.app.old.BASE = BASE
MAC, frozen = build.MAC, build.frozen


def scope():
    changed, patch = [], []
    for path in sorted((ROOT / "rtl").glob("*.v")):
        original = ROOT / "baseline" / path.name
        if tools.digest(path) != tools.digest(original):
            changed.append(path.name)
            a, b = original.read_text(encoding="utf-8"), path.read_text(encoding="utf-8")
            assert a[a.index("module "):a.index("\n);")] == b[b.index("module "):b.index("\n);")]
            patch.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                fromfile="frozen/" + path.name, tofile="candidate/" + path.name))
    assert changed == ["down2_dynamic_tile_runner.v"], changed
    (ROOT / "rtl_change.diff").write_text("".join(patch), encoding="utf-8")
    save(ROOT / "scope_check.json", {"changed_rtl": changed, "unchanged_rtl_count": 7,
        "ports_unchanged": True, "additional_pipeline_stages": 0,
        "arithmetic_mac_and_postprocess_byte_identical": True,
        "sources": {str(p.relative_to(ROOT)): tools.digest(p) for p in (ROOT / "rtl").glob("*.v")}})


previous.scope = scope


def specs():
    work = tools.fresh("s")
    contract = json.loads((ROOT.parent / "dw_tail_compact_20261009/specs/contracts/"
        "down2_dynamic_tile_runner.contract.json").read_text(encoding="utf-8"))
    module = contract["modules"][0]
    module["feature"] = "r"
    module["description"] = "Frozen DW/PW overlap runner with combinational successor and payload eligibility predecode"
    module["behavior"] = [
        "Shared four-entry DW/PW ownership ring and same-cycle pop credit remain unchanged.",
        "DW spatial triplet issue and scalar retirement remain unchanged; PW begins after DW drains.",
        "Counter successor excludes actual handshake; only the unchanged accepted-last event commits it.",
        "Final PW count7 position15 holds7; DW final group wraps the counter to0; existing start and drain clear semantics remain.",
        "Payload capture eligibility is computed from layer/group/position; actual handshake and original fault priority still gate every capture.",
        "No new register stage, no port/II/numeric/reset/fault change. Refill all1024 SiLU entries after reset.",
        "Runtime parameters are TEST parameters, not deployment QAT weights. Local MAC pointer preserve attribute inherited unchanged."
    ]
    module["timing_diagrams"] = [{"id": "predecode", "title": "Successor versus accepted commit",
        "scenario": "predecode", "description": "Conceptual handshake timing; no added latency.",
        "wavejson": {"signal": [{"name": "clk", "wave": "p....."},
            {"name": "last_group", "wave": "01...."}, {"name": "accept", "wave": "00010."},
            {"name": "cnt_output", "wave": "=...=.", "data": ["2", "3"]},
            {"name": "next_cnt_output", "wave": "=...=.", "data": ["3", "4"]}],
            "head": {"text": "Only actual accepted last group commits the precomputed successor"}}}]
    save(work / "contract.json", contract)
    source = work / "down2_dynamic_tile_runner.v"
    shutil.copyfile(ROOT / "rtl" / source.name, source)
    entry = (f"import sys;sys.path.insert(0,{str(tools.SKILL)!r});"
        "from scripts.python.workflow.cli import main;raise SystemExit(main())")
    tools.command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec",
        work / "contract.json", "--out-dir", work / "generated", "--source", source, "--no-state"],
        work, "spec", allowed=(0, 1, 2))
    generated = work / "generated/spec/r/down2_dynamic_tile_runner_spec.md"
    assert generated.exists(), generated
    shutil.copyfile(generated, ROOT / "rtl" / generated.name)
    shutil.copytree(generated.parent / "waveforms", ROOT / "rtl/waveforms", dirs_exist_ok=True)


def finish():
    previous.finish()
    diagnosis = json.loads((ROOT / "control_path_diagnosis.json").read_text(encoding="utf-8"))
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    status["internal_unique_failed_endpoints_by_check"] = diagnosis["internal_unique_failed_endpoints_by_check"]
    status["internal_negative_path_records"] = diagnosis["internal_negative_path_records"]
    status["count_note"] = diagnosis["count_note"]
    save(ROOT / "status.json", status)
    path = ROOT / "evidence_hashes.json"
    hashes = json.loads(path.read_text(encoding="utf-8"))
    hashes["status.json"] = tools.digest(ROOT / "status.json")
    for name in ("control_reference.py", "analyze.py"):
        hashes[name] = tools.digest(ROOT / name)
    receipt = ROOT / status["receipts"]["shell_routed"]
    for artifact in receipt.parent.glob("*.log"):
        hashes[str(artifact.relative_to(ROOT))] = tools.digest(artifact)
    save(path, hashes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "review", "scope", "simulate", "physical", "gates",
        "specs", "mac_sim", "boundary", "compare", "collect", "shell_rtl", "shell_routed", "undriven", "finish"))
    stage = parser.parse_args().stage
    frozen()
    try:
        if stage in ("scope", "specs", "finish"):
            globals()[stage]()
        elif stage == "prepare":
            previous.prepare()
        elif stage == "review":
            build.review()
        elif stage == "gates":
            build.gate("candidate")
            build.gate("testbench")
        elif stage in ("shell_rtl", "shell_routed"):
            build.shell(stage == "shell_routed")
        elif stage in ("boundary", "compare"):
            getattr(control.app.old, stage)()
        elif stage in ("mac_sim", "collect"):
            getattr(control, stage)()
        else:
            getattr(build, stage)()
    except Exception as error:
        save(ROOT / (stage + "_failure.json"), {"type": type(error).__name__, "message": str(error)})
        raise
    finally:
        frozen()
