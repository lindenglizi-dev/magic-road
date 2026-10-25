"""Compile and run the thirteen direct sequence cases with ModelSim."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
RUN = HERE / "case0"
RECEIPTS = HERE / "receipts"
PASS_RE = re.compile(
    r"TB_PASS_STEM_DDR_SEQUENCE case=(\d+) status=(\d+) error=(\d+) generation=(\d+) "
    r"cycles=(\d+) W=(\d+) R=(\d+) Stem=(\d+) halo=(\d+) pad=(\d+) PW=(\d+) "
    r"acc/pre/silu/post=(\d+)/(\d+)/(\d+)/(\d+) table=(\d+) "
    r"StemStages=(\d+)/(\d+)/(\d+)/(\d+) DWStages=(\d+)/(\d+)/(\d+)/(\d+) "
    r"PWStages=(\d+)/(\d+)/(\d+)/(\d+)"
)
EXPECTED = {
    0: (1, 0, "PASS"),
    1: (1, 0, "PASS"),
    2: (1, 0, "PASS"),
    3: (2, 5, "PASS_EXPECTED_READ_CORRUPTION"),
    4: (2, 7, "PASS_EXPECTED_RESPONSE_ERROR"),
    5: (1, 0, "PASS_RESET_RERUN"),
    6: (1, 0, "PASS_RESET_RERUN"),
    7: (1, 0, "PASS_RESET_RERUN"),
    8: (1, 0, "PASS_RESET_RERUN"),
    9: (1, 0, "PASS_RESET_RERUN"),
    10: (1, 0, "PASS_RESET_RERUN"),
    11: (2, 9, "PASS_EXPECTED_TIMEOUT"),
    12: (2, 1, "PASS_EXPECTED_POST_PASS_FAULT"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(command: list[str], log: Path) -> str:
    result = subprocess.run(command, cwd=RUN, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}; see {log}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=Path(r"D:\modeltech64_2020.4\win64"))
    parser.add_argument("--vendor", type=Path, default=Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p"))
    args = parser.parse_args()
    tools = {name: args.model / f"{name}.exe" for name in ("vlib", "vlog", "vsim")}
    vendor_sources = [args.vendor / "ph1p_phy_gsr.v", args.vendor / "ph1p_logic_eram.v"]
    required = [*tools.values(), *vendor_sources]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing ModelSim/vendor input: " + ", ".join(missing))

    RUN.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    for vector in sorted((ROOT / "vectors").glob("*.hex")):
        shutil.copy2(vector, RUN / vector.name)
    if not (RUN / "work").exists():
        run([str(tools["vlib"]), "work"], RUN / "vlib.stdout.log")

    reused = sorted((ROOT / "reused").glob("*.v"), key=lambda path: path.name)
    sources = [*vendor_sources, *reused, ROOT / "rtl" / "road_stem_ddr_sequence.v",
               ROOT / "tests" / "tb_stem_ddr_sequence.v"]
    compile_command = [str(tools["vlog"]), "-work", "work", "-l", "compile.log",
                       f"+incdir+{ROOT / 'rtl'}", *(str(path) for path in sources)]
    run(compile_command, RUN / "vlog.stdout.log")
    compile_text = (RUN / "compile.log").read_text(encoding="utf-8", errors="replace")
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_text)
    if not summaries or tuple(map(int, summaries[-1])) != (0, 0):
        raise RuntimeError("ModelSim compile was not 0 errors / 0 warnings")

    version = run([str(tools["vsim"]), "-version"], RUN / "vsim_version.log").strip().splitlines()[0]
    receipts = []
    run_commands = []
    for case_id in range(13):
        command = [str(tools["vsim"]), "-c", "-lib", "work", "PH1P_PHY_GSR",
                   "tb_stem_ddr_sequence", f"+CASE={case_id}", f"+VECTORS={ROOT / 'vectors'}",
                   "-l", f"case{case_id}.log", "-do",
                   "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
        output = run(command, RUN / f"case{case_id}.stdout.log")
        transcript = (RUN / f"case{case_id}.log").read_text(encoding="utf-8", errors="replace")
        match = PASS_RE.search(output + "\n" + transcript)
        if not match:
            raise RuntimeError(f"case {case_id} did not print the PASS receipt")
        values = list(map(int, match.groups()))
        if values[0] != case_id or (values[1], values[2]) != EXPECTED[case_id][:2]:
            raise RuntimeError(f"case {case_id} terminal mismatch: {values[:3]}")
        receipt = {
            "case": case_id,
            "result": EXPECTED[case_id][2],
            "status": values[1],
            "error": values[2],
            "generation": values[3],
            "cycles": values[4],
            "writes": values[5],
            "reads": values[6],
            "stem": values[7],
            "halo": values[8],
            "padding_pixels": values[9],
            "pw": values[10],
            "acc_pre_silu_post": values[11:15],
            "table_entries": values[15],
            "stem_acc_pre_silu_post": values[16:20],
            "dw_acc_pre_silu_post": values[20:24],
            "pw_acc_pre_silu_post": values[24:28],
            "log": f"../case0/case{case_id}.log",
        }
        (RECEIPTS / f"case{case_id:02d}.json").write_text(
            json.dumps(receipt, separators=(",", ":")) + "\n", encoding="utf-8")
        receipts.append(receipt)
        run_commands.append(command)

    compiled_hashes = {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                       for path in [*reused, ROOT / "rtl" / "road_stem_ddr_sequence.v",
                                    ROOT / "tests" / "tb_stem_ddr_sequence.v"]}
    manifest = {
        "result": "PASS_13_OF_13",
        "date": "2026-10-14",
        "simulator": version,
        "clock_mhz": 100,
        "timeout_cycles": 20000,
        "compile_log": "../case0/compile.log",
        "compile_errors": 0,
        "compile_warnings": 0,
        "tb_sha256": sha256(ROOT / "tests" / "tb_stem_ddr_sequence.v"),
        "dut_sha256": sha256(ROOT / "rtl" / "road_stem_ddr_sequence.v"),
        "program_sha256": sha256(ROOT / "vectors" / "program.hex"),
        "reference_json_sha256": sha256(ROOT / "reference.json"),
        "cases": list(range(13)),
        "case_cycles": {str(item["case"]): item["cycles"] for item in receipts},
        "compiled_source_sha256": compiled_hashes,
        "vendor_source_sha256": {str(path): sha256(path) for path in vendor_sources},
        "compile_command": compile_command,
        "run_commands": run_commands,
    }
    (RECEIPTS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS_13_OF_13", json.dumps(manifest["case_cycles"], separators=(",", ":")))


if __name__ == "__main__":
    main()
