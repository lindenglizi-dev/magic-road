"""Replay frozen strict gates with the existing project checker overlay."""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parents[1]
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
OVERLAY = PRODUCTION / "checker_overlay"
RUN_PROJECT_GATE = PRODUCTION / "run_project_gate.py"
OUTPUT = HERE / "checker_replay"
RAW_GATES = HERE / "gates_attempt2"
PRIOR_REGRESSION_RECEIPT = OUTPUT / "regression" / "receipt.json"
PH1P_NAME = "ph1p_eram_interface_complete.v"
MODES = ("baseline", "candidate")
ORIGIN_MODULES = (
    "scripts.python.quality.formatter_backend.parse_mixin",
    "scripts.python.quality.quality_gate_structure_rules",
    "scripts.python.quality.vg_comb_targets",
    "scripts.python.quality.vg_contract_liveness",
    "scripts.python.quality.vg_expression_rules",
    "scripts.python.workflow.spec_document",
)
EXAMPLE_RULES = ("VG085", "VG097", "VG122", "VG136", "VG144", "VG145", "VG146", "VG147", "VG153")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def local_path(path: Path, label: str) -> Path:
    resolved = (path if path.is_absolute() else HERE / path).resolve()
    if resolved == HERE.resolve() or not resolved.is_relative_to(HERE.resolve()):
        raise ValueError(f"{label} must be a child of {HERE}")
    return resolved


def load_gate_summary(path: Path) -> dict[str, object]:
    report = json.loads(path.read_text(encoding="utf-8"))
    examples = {rule: [] for rule in EXAMPLE_RULES}
    for issue in report["issues"]:
        rule = issue.get("rule_id") or issue.get("code")
        if rule not in examples or len(examples[rule]) >= 3:
            continue
        evidence = issue.get("evidence") or {}
        examples[rule].append(
            {
                "location": f"{issue.get('path')}:{issue.get('line')}",
                "problem": issue.get("problem") or issue.get("message"),
                "evidence": evidence.get("source_excerpt") or evidence.get("detail"),
            }
        )
    summary = {
        "errors": report["errors"],
        "strict_warnings": report["strict_warnings"],
        "delivery_ready": report["delivery_ready"],
        "issues_by_rule": report["delivery_issues_by_rule"],
        "checks": report["checks"],
        "representative_findings": {rule: items for rule, items in examples.items() if items},
    }
    del report
    gc.collect()
    return summary


def import_run_project_gate():
    spec = importlib.util.spec_from_file_location("project_run_project_gate", RUN_PROJECT_GATE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {RUN_PROJECT_GATE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def regression_worker(output: Path) -> int:
    sys.path[:0] = [str(OVERLAY), str(SKILL)]
    project_gate = import_run_project_gate()
    results = project_gate.regress(output)
    origins = {}
    for name in ORIGIN_MODULES:
        module = __import__(name, fromlist=["*"])
        path = Path(module.__file__).resolve()
        origins[name] = {"path": str(path), "sha256": sha256(path)}
    write_json(
        output / "receipt.json",
        {
            "python": sys.version,
            "python_executable": sys.executable,
            "sys_path_prefix": [str(OVERLAY), str(SKILL)],
            "origins": origins,
            "regressions": results,
            "all_regressions_passed": all(item["passed"] for item in results.values()),
        },
    )
    return 0 if all(item["passed"] for item in results.values()) else 1


def prepare_inputs() -> dict[str, dict[str, str]]:
    input_hashes = {}
    interface_sources = {
        mode: RAW_GATES / mode / PH1P_NAME
        for mode in MODES
    }
    interface_source_hashes = {
        mode: sha256(path) for mode, path in interface_sources.items()
    }
    if len(set(interface_source_hashes.values())) != 1:
        raise RuntimeError("baseline/candidate PH1P interface sources differ")
    interface_source = interface_sources["candidate"]
    interface_target = OUTPUT / "interfaces" / PH1P_NAME
    interface_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(interface_source, interface_target)
    for mode in MODES:
        source = RAW_GATES / mode
        closure = OUTPUT / "inputs" / mode
        closure.mkdir(parents=True, exist_ok=True)
        hashes = {}
        for path in sorted(source.glob("*.v")):
            if path.name == PH1P_NAME:
                continue
            target = closure / path.name
            shutil.copy2(path, target)
            hashes[path.name] = sha256(path)
        if (closure / PH1P_NAME).exists() or len(hashes) != 8:
            raise RuntimeError(f"invalid copied closure for {mode}")
        input_hashes[mode] = hashes
    input_hashes["external_interface_sources"] = interface_source_hashes
    input_hashes["external_interface"] = {PH1P_NAME: sha256(interface_target)}
    return input_hashes


def gate_command(mode: str) -> list[str]:
    closure = OUTPUT / "inputs" / mode
    result = OUTPUT / mode
    interface = OUTPUT / "interfaces" / PH1P_NAME
    bootstrap = (
        "import sys;"
        f"sys.path[:0]=[{str(OVERLAY)!r},{str(SKILL)!r}];"
        "from scripts.python.validation.generated_deliverable_gate import main;"
        "raise SystemExit(main())"
    )
    return [
        sys.executable,
        "-B",
        "-X",
        "utf8",
        "-c",
        bootstrap,
        str(closure),
        "--external-interface-source",
        str(interface),
        "--json",
        str(result / "gate.json"),
        "--markdown",
        str(result / "gate.md"),
    ]


def run_command(command: list[str], log: Path) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=OUTPUT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    return {
        "command": command,
        "cwd": str(OUTPUT),
        "returncode": completed.returncode,
        "log_sha256": sha256(log),
    }


def rule_delta(original: dict[str, int], fixed: dict[str, int]) -> dict[str, int]:
    return {
        rule: fixed.get(rule, 0) - original.get(rule, 0)
        for rule in sorted(set(original) | set(fixed))
        if fixed.get(rule, 0) != original.get(rule, 0)
    }


def category_counts(rules: dict[str, int]) -> dict[str, dict[str, int]]:
    groups = {
        "width_and_arithmetic": ("VG085", "VG097", "VG122", "VG125", "VG137", "VG138"),
        "driver_and_feedback": ("VG136", "VG141", "VG153"),
        "state_contract": ("VG144",),
        "source_and_operation_budget": ("VG145", "VG146", "VG147"),
        "format_comment_naming": (
            "VG004", "VG007", "VG013", "VG015", "VG040", "VG060", "VG061", "VG062",
            "VG063", "VG064", "VG067", "VG068", "VG069", "VG070", "VG156", "VG157",
        ),
    }
    return {
        name: {rule: rules[rule] for rule in members if rules.get(rule)}
        for name, members in groups.items()
    }


def render_report(report: dict[str, object]) -> str:
    raw_label = report["raw_gate_label"]
    lines = [
        "# Project checker overlay strict replay",
        "",
        "> Snapshot warning: this run is bound to the SHA-256-identified files currently under",
        f"> `{raw_label}/baseline` and `{raw_label}/candidate`. This replay is bound to the",
        "> selected same-attempt original/fixed pair; it is not a strict delivery or deployment",
        "> release while findings remain.",
        "",
        "Pair binding: `baseline` is the original closure and `candidate` is the fixed closure",
        f"from the same `{raw_label}` snapshot. Both copied closures contain the same eight RTL roots,",
        "and their identical PH1P source is supplied only as an external interface.",
        "",
        "The replay used copied closures under this directory, excluded PH1P from ordinary roots,",
        "and supplied it only through the registered `--external-interface-source` option.",
        "No RTL, checker, original report, TD, training, synthesis, or board state was modified.",
        "",
        "## Results",
        "",
        "| mode | raw errors | replay errors | delta | ready |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for mode in MODES:
        item = report["modes"][mode]
        lines.append(
            f"| {mode} | {item['raw']['errors']} | {item['replay']['errors']} | "
            f"{item['replay']['errors'] - item['raw']['errors']:+d} | {item['replay']['delivery_ready']} |"
        )
    lines.extend(["", "## Remaining categories", ""])
    for mode in MODES:
        lines.append(f"### {mode}")
        lines.append("")
        for category, values in report["modes"][mode]["remaining_categories"].items():
            detail = ", ".join(f"{rule}={count}" for rule, count in values.items()) or "none"
            lines.append(f"- `{category}`: {detail}")
        lines.append("")
    lines.extend(["## Representative remaining findings", ""])
    for rule, items in report["modes"]["candidate"]["replay"]["representative_findings"].items():
        rendered = "; ".join(
            f"`{item['location']}` `{item['evidence']}`" for item in items
        )
        lines.append(f"- `{rule}`: {rendered}")
    lines.append("")
    lines.extend(
        [
            "## Checker and regression evidence",
            "",
            f"- Existing `run_project_gate.py::regress(output)` reused: "
            f"`{report['regression']['all_regressions_passed']}`.",
            f"- Imported module origins and SHA-256 values come from "
            f"`{report['regression_receipt']['path']}` "
            f"(`{report['regression_receipt']['sha256']}`).",
            "- Full raw/replay rule deltas, commands, input hashes, overlay hashes, and public matrices",
            "  are recorded in `report.json` and `commands.json`.",
            "- Gate return code 1 is expected while strict findings remain; report publication and",
            "  regression worker must return usable evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    global OUTPUT, RAW_GATES
    parser = argparse.ArgumentParser()
    parser.add_argument("--regression-worker", type=Path)
    parser.add_argument("--raw-gates", type=Path, default=RAW_GATES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.regression_worker is not None:
        return regression_worker(args.regression_worker)

    RAW_GATES = local_path(args.raw_gates, "--raw-gates")
    OUTPUT = local_path(args.output, "--output")
    if RAW_GATES == OUTPUT:
        raise ValueError("--raw-gates and --output must differ")
    if not RAW_GATES.is_dir():
        raise FileNotFoundError(RAW_GATES)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    input_hashes = prepare_inputs()
    commands = {}
    for mode in MODES:
        (OUTPUT / mode).mkdir(parents=True, exist_ok=True)
        commands[mode] = run_command(gate_command(mode), OUTPUT / mode / "run.log")
        if commands[mode]["returncode"] not in (0, 1):
            raise RuntimeError(f"{mode} gate execution failed")

    regression_receipt = OUTPUT / "regression" / "receipt.json"
    if regression_receipt.exists():
        commands["regression"] = {
            "reused_existing_receipt": True,
            "receipt_sha256": sha256(regression_receipt),
        }
    elif PRIOR_REGRESSION_RECEIPT.exists():
        regression_receipt = PRIOR_REGRESSION_RECEIPT
        commands["regression"] = {
            "reused_prior_receipt": str(regression_receipt.relative_to(HERE)),
            "receipt_sha256": sha256(regression_receipt),
            "note": "No duplicate regression run; prior 28-case receipt is content-addressed here.",
        }
    else:
        regression_command = [
            sys.executable,
            "-B",
            "-X",
            "utf8",
            str(Path(__file__).resolve()),
            "--regression-worker",
            str(OUTPUT / "regression"),
        ]
        commands["regression"] = run_command(regression_command, OUTPUT / "regression" / "run.log")
        if commands["regression"]["returncode"] != 0:
            raise RuntimeError("checker regressions failed")
    write_json(OUTPUT / "commands.json", commands)

    modes = {}
    for mode in MODES:
        raw = load_gate_summary(RAW_GATES / f"{mode}.json")
        replay = load_gate_summary(OUTPUT / mode / "gate.json")
        modes[mode] = {
            "raw_report_sha256": sha256(RAW_GATES / f"{mode}.json"),
            "replay_report_sha256": sha256(OUTPUT / mode / "gate.json"),
            "raw": raw,
            "replay": replay,
            "delta_by_rule": rule_delta(raw["issues_by_rule"], replay["issues_by_rule"]),
            "remaining_categories": category_counts(replay["issues_by_rule"]),
        }
    regression = json.loads(regression_receipt.read_text(encoding="utf-8"))
    report = {
        "status": "overlay_replay_complete_snapshot_not_final_or_strict_release",
        "raw_gate_label": RAW_GATES.relative_to(HERE).as_posix(),
        "candidate_revision": (
            f"SHA-256-bound {RAW_GATES.relative_to(HERE).as_posix()}/candidate snapshot; "
            "selected fixed raw-gate input, not a strict delivery or deployment release"
        ),
        "pair_binding": {
            "original": f"{RAW_GATES.relative_to(HERE).as_posix()}/baseline -> {OUTPUT.relative_to(HERE).as_posix()}/inputs/baseline",
            "fixed": f"{RAW_GATES.relative_to(HERE).as_posix()}/candidate -> {OUTPUT.relative_to(HERE).as_posix()}/inputs/candidate",
            "fixed_revision": "selected raw-gate snapshot",
            "relationship": "same selected baseline/candidate pair; SHA-256-bound below",
        },
        "scope": "copied baseline/candidate closures; PH1P registered external interface; no testbench/toolchain/TD/training",
        "source_unchanged": all(
            sha256(RAW_GATES / mode / name) == digest
            for mode in MODES
            for name, digest in input_hashes[mode].items()
        ),
        "inputs": input_hashes,
        "script_sha256": sha256(Path(__file__).resolve()),
        "run_project_gate_sha256": sha256(RUN_PROJECT_GATE),
        "overlay_sha256": {
            path.relative_to(OVERLAY).as_posix(): sha256(path)
            for path in sorted(OVERLAY.rglob("*.py"))
        },
        "commands": commands,
        "regression_receipt": {
            "path": str(regression_receipt.relative_to(HERE)),
            "sha256": sha256(regression_receipt),
        },
        "regression": regression,
        "modes": modes,
        "limitations": [
            "Strict style/profile and strong operation-budget findings remain blocking.",
            "Replay does not authorize RTL latency, handshake, numeric, reset, or interface changes.",
            "Testbench and external toolchain evidence remain outside this replay.",
        ],
    }
    write_json(OUTPUT / "report.json", report)
    (OUTPUT / "report.md").write_text(render_report(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": report["status"],
                "baseline_errors": modes["baseline"]["replay"]["errors"],
                "candidate_errors": modes["candidate"]["replay"]["errors"],
                "regressions_passed": regression["all_regressions_passed"],
                "report": str(OUTPUT / "report.json"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
