"""Compile and run the head decode/TopK RTL verification suites locally."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
ROOT = HERE.parents[4]
ASSETS = HERE / "assets"
BUILD = HERE / "build"
REPORTS = HERE / "reports"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def executable(name: str, fallback: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    path = Path(fallback)
    if path.is_file():
        return str(path)
    raise FileNotFoundError(f"required local tool not found: {name}")


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=timeout, check=False)


def compile_tb(timeout: int) -> tuple[Path, str, int]:
    compiler = executable("iverilog", "C:/iverilog/bin/iverilog.exe")
    BUILD.mkdir(parents=True, exist_ok=True)
    image = BUILD / "tb_road_head_decode_topk.vvp"
    sources = [
        PACKAGE / "rtl/road_candidate_ram.v",
        PACKAGE / "rtl/road_head_decode_topk.v",
        HERE / "tb_road_head_decode_topk.v",
    ]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing RTL source: " + ", ".join(missing))
    command = [compiler, "-g2012", "-s", "tb_road_head_decode_topk",
               "-o", str(image), *(str(path) for path in sources)]
    result = run(command, timeout)
    text = result.stdout + result.stderr
    (BUILD / "compile.log").write_text(text, encoding="utf-8", newline="\n")
    if result.returncode and (not image.is_file() or image.stat().st_size == 0):
        raise RuntimeError("iverilog compile failed without an image; see build/compile.log")
    return image, compiler, result.returncode


def plusarg(name: str, value: object) -> str:
    return f"+{name}={value}"


def simulate(image: Path, name: str, args: list[str], timeout: int) -> dict:
    runtime = executable("vvp", "C:/iverilog/bin/vvp.exe")
    result = run([runtime, str(image), *args], timeout)
    text = result.stdout + result.stderr
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"{name}.log").write_text(text, encoding="utf-8", newline="\n")
    passed = result.returncode == 0 and "TB_PASS" in text and "TB_FAIL" not in text
    metrics = [line for line in text.splitlines() if line.startswith("METRIC ")]
    return {"name": name, "passed": passed, "returncode": result.returncode,
            "metrics": metrics, "log": f"reports/{name}.log"}


def case_arguments(case: dict, mode: int, stall: int = 0) -> list[str]:
    return [
        plusarg("MODE", mode),
        plusarg("HEAD", ROOT / case["heads"]),
        plusarg("EXPECTED", ROOT / case["decoded160"]),
        plusarg("EXPECT_PERSON", case["person_count"]),
        plusarg("EXPECT_VEHICLE", case["vehicle_count"]),
        plusarg("SIGMOID", ASSETS / "sigmoid_lut_16.hex"),
        plusarg("EXP", ASSETS / "exp_lut_16.hex"),
        plusarg("STALL", stall),
        plusarg("MAX_CYCLES", 20_000_000),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("regression", "protocol", "reset", "all"), default="all")
    parser.add_argument("--case", default="all", help="one saved case name or all")
    parser.add_argument("--timeout", type=int, default=600, help="seconds per compile or simulation")
    args = parser.parse_args()

    prep = run([sys.executable, str(HERE / "prepare_vectors.py"), "--check"], args.timeout)
    if prep.returncode:
        print(prep.stdout + prep.stderr, end="")
        return 1
    manifest = json.loads((ASSETS / "cases.json").read_text(encoding="utf-8"))
    cases = {case["name"]: case for case in manifest["cases"]}
    selected = list(cases.values()) if args.case == "all" else [cases[args.case]]

    try:
        image, compiler, compile_returncode = compile_tb(args.timeout)
    except (FileNotFoundError, RuntimeError) as error:
        print(f"RUNNER_FAIL {error}")
        return 1

    results: list[dict] = []
    if args.suite in ("regression", "all"):
        for case in selected:
            stall = 1 if case["name"] == "threshold_equal_inclusive_and_below" else 0
            results.append(simulate(image, f"regression_{case['name']}",
                                    case_arguments(case, mode=0, stall=stall), args.timeout))
    if args.suite in ("protocol", "all"):
        case = cases["threshold_equal_inclusive_and_below"]
        results.append(simulate(image, "protocol", case_arguments(case, mode=1, stall=1), args.timeout))
    if args.suite in ("reset", "all"):
        case = cases["top128_ties_and_each32_total64"]
        results.append(simulate(image, "phase_reset", case_arguments(case, mode=2, stall=1), args.timeout))

    simulations_passed = bool(results) and all(item["passed"] for item in results)
    status = "PASS" if simulations_passed and compile_returncode == 0 else (
        "SIM_PASS_COMPILE_ABNORMAL" if simulations_passed else "FAIL")
    summary = {
        "status": status,
        "simulator": "iverilog/vvp",
        "compiler": compiler,
        "compiler_returncode": compile_returncode,
        "compiler_mode": "-g2012 (sources remain Verilog-2001)",
        "model_id32": manifest["model_id32"],
        "payload_sha256": manifest["payload_sha256"],
        "no_cnn_inference": True,
        "run_parameters": {
            "clock_hz": 100_000_000,
            "frame_token": "10203040",
            "watchdog_cycles": 20_000_000,
            "sealed_backpressure_cycles": 13,
            "selected_read_backpressure_cycles": 7,
            "input_and_lut_stall_case": "threshold_equal_inclusive_and_below",
        },
        "source_sha256": {
            "road_candidate_ram.v": sha256(PACKAGE / "rtl/road_candidate_ram.v"),
            "road_head_decode_topk.v": sha256(PACKAGE / "rtl/road_head_decode_topk.v"),
            "tb_road_head_decode_topk.v": sha256(HERE / "tb_road_head_decode_topk.v"),
            "cases.json": sha256(ASSETS / "cases.json"),
            "sigmoid_lut_16.hex": sha256(ASSETS / "sigmoid_lut_16.hex"),
            "exp_lut_16.hex": sha256(ASSETS / "exp_lut_16.hex"),
        },
        "results": results,
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    for item in results:
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['name']} {item['log']}")
        for metric in item["metrics"]:
            print(metric)
    if compile_returncode:
        print(f"TOOLCHAIN_WARNING iverilog_returncode={compile_returncode} generated_image_was_executed")
    print(f"RTL_SUITE_{summary['status']} runs={len(results)} simulator=iverilog/vvp")
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
