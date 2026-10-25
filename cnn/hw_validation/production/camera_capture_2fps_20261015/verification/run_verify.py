"""Run retained camera capture component checks with ModelSim."""
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
VENDOR = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p")
SCALER_CASES = {
    0: ("scaler_numbered", "frame0_numbered_bars"),
    1: ("scaler_random", "frame1_random_seed20261015"),
    2: ("scaler_all255", "frame2_all255"),
    3: ("scaler_fault_recovery", "frame2_all255"),
    4: ("scaler_overload", "frame2_all255"),
}
SLOT_CASES = {
    10: "slots_lifecycle",
    11: "slots_protection",
    12: "slots_protocol",
    13: "slots_malformed_reset",
}
SCALER_PASS = re.compile(
    r"TB_PASS_AREA_RESIZE case=(\d+) cycles=(\d+) output_pixels=(\d+) output_beats=(\d+) "
    r"output_bytes=(\d+) first_output=(-?\d+) last_output=(-?\d+) frame_errors=(\d+) first_error=(-?\d+)"
)
SLOT_PASS = re.compile(
    r"TB_PASS_CAPTURE_SLOTS case=(\d+) cycles=(\d+) protocol_errors=(\d+) skipped=(\d+)"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, log: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}; see {log}")
    return result.stdout


def relative_hashes(paths: list[Path]) -> dict[str, str]:
    return {path.relative_to(ROOT).as_posix(): sha256(path) for path in paths}


def execute(case_id: int, work: Path) -> dict[str, object]:
    tools = {name: MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")}
    vendor_sources = [VENDOR / "ph1p_phy_gsr.v", VENDOR / "ph1p_logic_eram.v"]
    rtl_sources = sorted((ROOT / "rtl").glob("*.v"), key=lambda path: path.name)
    if case_id in SCALER_CASES:
        case_name, vector_stem = SCALER_CASES[case_id]
        top = "tb_road_area_resize"
        tb = ROOT / "tests" / "tb_road_area_resize.v"
        scaler_case = case_id
        input_vector = ROOT / "vectors" / f"{vector_stem}_awb96.hex"
        expected_vector = ROOT / "vectors" / f"{vector_stem}_rgb48_serial.hex"
        vector_sources = [input_vector, expected_vector]
        plusargs = [f"+CASE={scaler_case}", f"+INPUT={input_vector}", f"+EXPECTED={expected_vector}"]
    else:
        case_name = SLOT_CASES[case_id]
        top = "tb_road_capture_slots"
        tb = ROOT / "tests" / "tb_road_capture_slots.v"
        scaler_case = None
        vector_sources = []
        plusargs = [f"+CASE={case_id - 10}"]

    required = [*tools.values(), *vendor_sources, *rtl_sources, tb,
                ROOT / "reference" / "contract.json", *vector_sources]
    missing = [str(path) for path in required if not path.is_file()]
    if not rtl_sources:
        missing.append(str(ROOT / "rtl" / "*.v"))
    if missing:
        raise FileNotFoundError("missing frozen verification input: " + ", ".join(missing))

    run([str(tools["vlib"]), "work"], work, work / "vlib.stdout.log")
    sources = [*vendor_sources, *rtl_sources, tb]
    compile_command = [str(tools["vlog"]), "-work", "work", "-l", "compile.log",
                       *(str(path) for path in sources)]
    run(compile_command, work, work / "vlog.stdout.log")
    compile_text = (work / "compile.log").read_text(encoding="utf-8", errors="replace")
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_text)
    if not summaries or tuple(map(int, summaries[-1])) != (0, 0):
        raise RuntimeError(f"compile was not clean; see {work / 'compile.log'}")

    run_command = [str(tools["vsim"]), "-c", "-t", "1ps", "-lib", "work",
                   "PH1P_PHY_GSR", top, *plusargs, "-l", "simulation.log", "-do",
                   "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
    stdout = run(run_command, work, work / "vsim.stdout.log")
    transcript = (work / "simulation.log").read_text(encoding="utf-8", errors="replace")
    combined = stdout + "\n" + transcript
    match = SCALER_PASS.search(combined) if scaler_case is not None else SLOT_PASS.search(combined)
    if not match:
        raise RuntimeError(f"PASS receipt absent; retained failure: {work}")
    values = list(map(int, match.groups()))
    expected_case = scaler_case if scaler_case is not None else case_id - 10
    if values[0] != expected_case:
        raise RuntimeError(f"wrong case receipt: {values[0]} expected {expected_case}")

    common = {
        "result": "PASS_" + case_name.upper(),
        "case": case_id,
        "tb_case": expected_case,
        "simulator": run([str(tools["vsim"]), "-version"], work,
                         work / "vsim_version.log").splitlines()[0],
        "clock_mhz": 100,
        "compiled_source_sha256": relative_hashes([*rtl_sources, tb]),
        "vendor_source_sha256": {str(path): sha256(path) for path in vendor_sources},
        "reference_contract_sha256": sha256(ROOT / "reference" / "contract.json"),
        "input_vector_sha256": relative_hashes(vector_sources),
        "runner_sha256": sha256(Path(__file__)),
        "compile_command": compile_command,
        "run_command": run_command,
        "evidence_boundary": "controlled component inputs; not real camera, PAXI visibility, DDR retirement, board, bitstream or physical timing",
    }
    if scaler_case is not None:
        common.update({
            "cycles": values[1], "output_pixels": values[2], "output_beats": values[3],
            "output_bytes": values[4], "first_output_cycle_from_first_valid": values[5],
            "last_output_cycle_from_first_valid": values[6], "frame_error_cycles": values[7],
            "first_error_cycle_from_first_valid": values[8],
        })
    else:
        common.update({"cycles": values[1], "protocol_error_cycles": values[2],
                       "skipped_frame_cycles": values[3]})
    return common


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0)
    args = parser.parse_args()
    if args.case not in SCALER_CASES and args.case not in SLOT_CASES:
        raise ValueError("case must be 0..4 or 10..13")

    case_name = SCALER_CASES[args.case][0] if args.case in SCALER_CASES else SLOT_CASES[args.case]
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
