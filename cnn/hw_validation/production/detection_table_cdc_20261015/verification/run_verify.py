"""Run retained dual-clock SRIF1 time and detection-table checks."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path(r"D:\modeltech64_2020.4\win64")
PYTHON = Path(r"D:\Python313\python.exe")
CASES = {
    0: ("time_multims", "tb_road_time_snapshot"),
    1: ("time_watchdog_recovery", "tb_road_time_snapshot"),
    10: ("table_counts_random", "tb_road_detection_table_cdc"),
    11: ("table_stall_pending_sof", "tb_road_detection_table_cdc"),
    12: ("table_reset_positions", "tb_road_detection_table_cdc"),
    13: ("table_metadata_age", "tb_road_detection_table_cdc"),
    14: ("table_abort_errors", "tb_road_detection_table_cdc"),
    20: ("time_table_integrated", "tb_time_table_integrated"),
}
PASS_PATTERNS = {
    "tb_road_time_snapshot": re.compile(
        r"TB_PASS_TIME case=(\d+) src_cycles=(\d+) dst_cycles=(\d+) ticks=(\d+) "
        r"updates=(\d+) req_update_min=(\d+) req_update_max=(\d+) "
        r"roundtrip_min=(\d+) roundtrip_max=(\d+) watchdog_invalid=(\d+) "
        r"watchdog_elapsed=(\d+)"
    ),
    "tb_road_detection_table_cdc": re.compile(
        r"TB_PASS_TABLE case=(\d+) src_cycles=(\d+) dst_cycles=(\d+) tables=(\d+) "
        r"entries=(\d+) acks=(\d+) updates=(\d+) max_wait=(\d+) resets=(\d+) "
        r"src_errors=(\d+) burst_entries=(\d+)"
    ),
    "tb_time_table_integrated": re.compile(
        r"TB_PASS_INTEGRATED case=(\d+) src_cycles=(\d+) dst_cycles=(\d+) "
        r"time_updates=(\d+) tables=(\d+) acks=(\d+) active_updates=(\d+) "
        r"copy_wait=(\d+) watchdog_invalid=(\d+)"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, log: Path) -> str:
    result = subprocess.run(
        command, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf-8", errors="replace",
    )
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}; see {log}"
        )
    return result.stdout


def relative_hashes(paths: list[Path]) -> dict[str, str]:
    return {path.relative_to(ROOT).as_posix(): sha256(path) for path in paths}


def materialize_reference_vectors(work: Path) -> tuple[Path, Path, Path, Path]:
    vectors = json.loads((ROOT / "reference" / "vectors.json").read_text(encoding="utf-8"))
    cases = vectors["table_cases"]
    if [case["count"] for case in cases] != [0, 1, 32, 33, 64]:
        raise RuntimeError("CPU reference table-case order changed")
    metadata_path = work / "cpu_table_metadata.hex"
    entries_path = work / "cpu_table_entries.hex"
    metadata_path.write_text(
        "\n".join(case["metadata_hex_265"] for case in cases) + "\n", encoding="ascii"
    )
    flattened: list[str] = []
    for case in cases:
        entries = case["entry_hex_97"]
        if len(entries) != case["count"]:
            raise RuntimeError(f"CPU reference count mismatch for count={case['count']}")
        flattened.extend(entries + ["0" * 25] * (64 - len(entries)))
    entries_path.write_text("\n".join(flattened) + "\n", encoding="ascii")
    diagnostics = vectors["diagnostic_copy_cases"]
    if [case["result_status"] for case in diagnostics] != [1, 2, 3]:
        raise RuntimeError("CPU diagnostic-case order changed")
    diagnostic_metadata_path = work / "cpu_diagnostic_metadata.hex"
    diagnostic_entries_path = work / "cpu_diagnostic_entries.hex"
    diagnostic_metadata_path.write_text(
        "\n".join(case["metadata_hex_265"] for case in diagnostics) + "\n", encoding="ascii"
    )
    diagnostic_entries_path.write_text(
        "\n".join(case["entry_hex_97"] for case in diagnostics) + "\n", encoding="ascii"
    )
    return metadata_path, entries_path, diagnostic_metadata_path, diagnostic_entries_path


def execute(case_id: int, work: Path) -> dict[str, object]:
    case_name, top = CASES[case_id]
    tools = {name: MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")}
    rtl_by_top = {
        "tb_road_time_snapshot": [ROOT / "rtl" / "road_time_snapshot.v"],
        "tb_road_detection_table_cdc": [ROOT / "rtl" / "road_detection_table_cdc.v"],
        "tb_time_table_integrated": [
            ROOT / "rtl" / "road_time_snapshot.v",
            ROOT / "rtl" / "road_detection_table_cdc.v",
        ],
    }
    rtl_sources = rtl_by_top[top]
    tb = ROOT / "tests" / f"{top}.v"
    reference_sources = [
        ROOT / "reference" / "contract.json",
        ROOT / "reference" / "reference_srif.py",
        ROOT / "reference" / "vectors.json",
        ROOT / "reference" / "manifest.sha256",
        ROOT / "age_telemetry_reference.py",
    ]
    specification_sources = [
        ROOT / "requirements.txt", ROOT / "interfaces.json", ROOT / "codegen_plan.json",
    ]
    required = [PYTHON, *tools.values(), *rtl_sources, tb, *reference_sources, *specification_sources]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing frozen verification input: " + ", ".join(missing))

    metadata_vector, entries_vector, diagnostic_metadata, diagnostic_entries = (
        materialize_reference_vectors(work)
    )
    reference_stdout = run(
        [str(PYTHON), "-B", "-X", "utf8", str(ROOT / "reference" / "reference_srif.py")],
        work, work / "reference_selfcheck.log",
    )
    if "SRIF1_REFERENCE_PASS" not in reference_stdout:
        raise RuntimeError("CPU reference self-check PASS marker absent")
    age_stdout = run(
        [str(PYTHON), "-B", "-X", "utf8", str(ROOT / "age_telemetry_reference.py")],
        work, work / "age_telemetry_selfcheck.log",
    )
    if "AGE_TELEMETRY_PASS" not in age_stdout:
        raise RuntimeError("age telemetry reference self-check PASS marker absent")

    run([str(tools["vlib"]), "work"], work, work / "vlib.stdout.log")
    compile_command = [
        str(tools["vlog"]), "-work", "work", "-l", "compile.log",
        *(str(path) for path in [*rtl_sources, tb]),
    ]
    run(compile_command, work, work / "vlog.stdout.log")
    compile_text = (work / "compile.log").read_text(encoding="utf-8", errors="replace")
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_text)
    if not summaries or tuple(map(int, summaries[-1])) != (0, 0):
        raise RuntimeError(f"compile was not clean; see {work / 'compile.log'}")

    run_command = [
        str(tools["vsim"]), "-c", "-t", "1ps", "-lib", "work", top,
        f"+CASE={case_id}", f"+TABLE_META={metadata_vector.name}",
        f"+TABLE_ENTRIES={entries_vector.name}", f"+DIAG_META={diagnostic_metadata.name}",
        f"+DIAG_ENTRIES={diagnostic_entries.name}", "-l", "simulation.log", "-do",
        "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0",
    ]
    stdout = run(run_command, work, work / "vsim.stdout.log")
    transcript = (work / "simulation.log").read_text(encoding="utf-8", errors="replace")
    match = PASS_PATTERNS[top].search(stdout + "\n" + transcript)
    if not match:
        raise RuntimeError(f"PASS receipt absent; retained failure: {work}")
    values = list(map(int, match.groups()))
    if values[0] != case_id:
        raise RuntimeError(f"wrong case receipt {values[0]}, expected {case_id}")

    version = run([str(tools["vsim"]), "-version"], work, work / "vsim_version.log")
    receipt: dict[str, object] = {
        "result": "PASS_" + case_name.upper(),
        "case": case_id,
        "testbench": top,
        "simulator": version.splitlines()[0],
        "source_clock": {"period_ps": 10000, "nominal_hz": 100000000},
        "destination_clock": {
            "period_ps": 13334,
            "actual_hz": 1_000_000_000_000 / 13334,
            "nominal_hz": 75000000,
            "initial_phase_ps": 2300,
        },
        "compiled_source_sha256": relative_hashes([*rtl_sources, tb]),
        "reference_sha256": relative_hashes(reference_sources),
        "specification_sha256": relative_hashes(specification_sources),
        "runner_sha256": sha256(Path(__file__)),
        "compile_command": compile_command,
        "run_command": run_command,
        "evidence_boundary": (
            "controlled component CDC simulation; the Python oracle specifies values and "
            "events but is not evidence of hardware time CDC, physical CDC sign-off, board, "
            "bitstream, or end-to-end detector execution"
        ),
    }
    if top == "tb_road_time_snapshot":
        receipt.update({
            "source_cycles": values[1], "destination_cycles": values[2],
            "ticks": values[3], "destination_updates": values[4],
            "request_to_update_dst_cycles_min": values[5],
            "request_to_update_dst_cycles_max": values[6],
            "busy_roundtrip_src_cycles_min": values[7],
            "busy_roundtrip_src_cycles_max": values[8],
            "watchdog_invalid_events": values[9],
            "watchdog_elapsed_dst_cycles": values[10],
        })
    elif top == "tb_road_detection_table_cdc":
        receipt.update({
            "source_cycles": values[1], "destination_cycles": values[2],
            "sealed_tables": values[3], "accepted_entries": values[4],
            "copy_acknowledgements": values[5], "active_updates": values[6],
            "maximum_copy_wait_dst_cycles": values[7], "common_resets": values[8],
            "source_error_pulses": values[9],
            "continuous_source_burst_entries": values[10],
        })
    else:
        receipt.update({
            "source_cycles": values[1], "destination_cycles": values[2],
            "destination_time_updates": values[3], "sealed_tables": values[4],
            "copy_acknowledgements": values[5], "active_updates": values[6],
            "blocked_copy_wait_dst_cycles": values[7],
            "watchdog_invalid_events": values[8],
            "time_connection": "road_time_snapshot destination outputs directly drive table time inputs",
        })
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, required=True, choices=sorted(CASES))
    args = parser.parse_args()
    case_name, _ = CASES[args.case]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    work = ROOT / "verification" / f"{case_name}_{stamp}"
    work.mkdir(parents=True)
    (work / "attempt.json").write_text(
        json.dumps({"case": args.case, "name": case_name, "started": stamp}, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        receipt = execute(args.case, work)
    except Exception as error:
        (work / "failure.json").write_text(
            json.dumps({"case": args.case, "name": case_name, "error": str(error)}, indent=2) + "\n",
            encoding="utf-8",
        )
        raise
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": receipt["result"], "work": str(work)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
