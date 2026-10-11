"""Run the overlap reference and the isolated ModelSim core regression."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone


HERE = Path(__file__).resolve().parent
REPORT = HERE.parent
RTL = REPORT / "rtl"
DIAGNOSTIC = REPORT.parent / "diagnostic_repair_20261008" / "candidate_sim"
ERAM_MODEL = REPORT.parent / "diagnostic_repair_20261008" / "model" / "ph1p_logic_eram_runtime_model.v"
MODELSIM = Path("D:/modeltech64_2020.4/win64")
SOURCES = [RTL / name for name in (
    "road_dynamic_postprocess.v", "road_dynamic_requant.v",
    "road_round_shift.v", "silu_shared_unit.v")]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, cwd, log_name):
    result = subprocess.run([str(item) for item in command], cwd=cwd,
                            text=True, encoding="utf-8", errors="replace",
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (cwd / log_name).write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"{Path(command[0]).name} failed ({result.returncode}); see {cwd / log_name}")
    return result.stdout


def main():
    reference_output = run([sys.executable, "-B", "-X", "utf8", HERE / "reference.py"], HERE,
                           "reference.log")
    marker = next(line for line in reference_output.splitlines() if "REFERENCE_PASS" in line)
    old_results = REPORT.parent / "dynamic_control_timing_20261008" / "candidate" / "results.csv"
    reference_receipt = {
        "status": "PYTHON_REFERENCE_PASS",
        "marker": marker,
        "reference_sha256": sha256(HERE / "reference.py"),
        "input_sha256": {
            "batches.txt": sha256(DIAGNOSTIC / "batches.txt"),
            "table.hex": sha256(DIAGNOSTIC / "table.hex"),
            "saved_results.csv": sha256(old_results),
        },
        "boundary": "Numeric and logical scheduling contract only; no cycle-accurate wrapper or hardware claim.",
    }
    (HERE / "reference_receipt.json").write_text(
        json.dumps(reference_receipt, indent=2) + "\n", encoding="utf-8")
    if "--reference-only" in sys.argv:
        print(marker)
        return
    missing = [str(path) for path in [*SOURCES, ERAM_MODEL, HERE / "tb_road_dynamic_postprocess.v"]
               if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing core regression inputs: " + ", ".join(missing))
    for name in ("batches.txt", "table.hex"):
        shutil.copyfile(DIAGNOSTIC / name, HERE / name)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = HERE / "runs" / stamp
    run_dir.mkdir(parents=True)
    for name in ("batches.txt", "table.hex"):
        shutil.copyfile(HERE / name, run_dir / name)
    run([MODELSIM / "vlib.exe", "work"], run_dir, "vlib.log")
    run([MODELSIM / "vlog.exe", "-work", "work", f"+incdir+{HERE}",
         *SOURCES, ERAM_MODEL, HERE / "tb_road_dynamic_postprocess.v"], run_dir, "vlog.log")
    transcript = run([MODELSIM / "vsim.exe", "-c", "-lib", "work",
                      "tb_road_dynamic_postprocess", "-do",
                      "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],
                     run_dir, "simulation.log")
    if "TB_PASS_DYNAMIC_OVERLAP" not in transcript or "Fatal:" in transcript or "** Error:" in transcript:
        raise AssertionError("core regression did not produce a clean pass marker")
    receipt = {
        "status": "CORE_SIMULATION_PASS_NOT_PHYSICAL_SIGNOFF",
        "timestamp_utc": stamp,
        "run_directory": str(run_dir),
        "source_sha256": {path.name: sha256(path) for path in SOURCES},
        "test_sha256": sha256(HERE / "tb_road_dynamic_postprocess.v"),
        "simulation_model_sha256": {ERAM_MODEL.name: sha256(ERAM_MODEL)},
        "vector_sha256": {name: sha256(HERE / name) for name in ("batches.txt", "table.hex")},
        "tool_sha256": {name: sha256(MODELSIM / name)
                        for name in ("vlib.exe", "vlog.exe", "vsim.exe")},
        "pass_marker": next(line for line in transcript.splitlines()
                            if "TB_PASS_DYNAMIC_OVERLAP" in line),
        "boundary": "Core ready/valid, arithmetic, ordered retirement, fault, and reset simulation only; no synthesis, timing, board, DDR, or full-network claim.",
    }
    (HERE / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt["pass_marker"])


if __name__ == "__main__":
    main()
