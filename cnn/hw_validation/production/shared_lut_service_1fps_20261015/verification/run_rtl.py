"""Compile and run the bounded shared-LUT service testbench with local Icarus."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def executable(root: Path, name: str) -> Path:
    candidates = [root.parent.parent / ".tools/iverilog/bin" / name, Path(r"C:\iverilog\bin") / name]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit(f"missing local tool: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    verification = Path(__file__).resolve().parent
    package = verification.parent
    project = verification.parents[4]
    dut = package / "rtl/road_shared_lut_service.v"
    tb = verification / "tb_road_shared_lut_service.v"
    assets = verification / "assets"
    build = verification / "build"
    reports = verification / "reports"
    build.mkdir(exist_ok=True)
    reports.mkdir(exist_ok=True)
    if not dut.is_file():
        raise SystemExit(f"DUT not ready: {dut}")

    subprocess.run([sys.executable, str(verification / "prepare_vectors.py"), "--check"], check=True)
    iverilog = executable(project, "iverilog.exe")
    vvp = executable(project, "vvp.exe")
    image = build / "tb_road_shared_lut_service.vvp"
    compile_command = [str(iverilog), "-g2012", "-Wall", "-s", "tb_road_shared_lut_service", "-o", str(image), str(tb), str(dut)]
    started = time.time()
    compiled = subprocess.run(compile_command, text=True, capture_output=True, timeout=args.timeout)
    (reports / "compile.log").write_text(compiled.stdout + compiled.stderr, encoding="utf-8")

    receipt = {
        "status": "COMPILE_FAILED" if compiled.returncode else "COMPILED",
        "simulator": "iverilog/vvp",
        "compiler": str(iverilog),
        "compiler_mode": "-g2012 (sources target Verilog-2001)",
        "compiler_returncode": compiled.returncode,
        "compile_command": compile_command,
        "run_parameters": {"clock_hz": 100_000_000, "timeout_seconds": args.timeout, "rom_words": 7168},
        "source_sha256": {path.name: digest(path) for path in (dut, tb, verification / "prepare_vectors.py", Path(__file__))},
        "input_sha256": {path.name: digest(path) for path in sorted(assets.iterdir()) if path.is_file()},
        "elapsed_seconds": round(time.time() - started, 3),
    }
    if compiled.returncode:
        (reports / "summary.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"RTL_COMPILE_FAIL returncode={compiled.returncode} receipt=reports/summary.json")
        return 1

    plusargs = [f"+ROM={assets / 'physical_words_160.hex'}"]
    run_command = [str(vvp), str(image), *plusargs]
    simulated = subprocess.run(run_command, text=True, capture_output=True, timeout=args.timeout, cwd=verification)
    output = simulated.stdout + simulated.stderr
    (reports / "simulation.log").write_text(output, encoding="utf-8")
    passed = simulated.returncode == 0 and "TB_PASS_SHARED_LUT" in output and "TB_FAIL" not in output
    receipt.update(
        {
            "status": "PASS" if passed else "SIM_FAILED",
            "simulation_returncode": simulated.returncode,
            "run_command": run_command,
            "metrics": [line for line in output.splitlines() if line.startswith("METRIC ")],
            "elapsed_seconds": round(time.time() - started, 3),
        }
    )
    (reports / "summary.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(output, end="")
    print(f"RTL_SUITE_{receipt['status']} compiler_returncode=0 receipt=reports/summary.json")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
