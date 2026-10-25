"""Run retained full-tensor ModelSim checks in a fresh directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path(r"D:\modeltech64_2020.4\win64")
VENDOR = Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p")
PASS_RE = re.compile(
    r"TB_PASS_FRONTEND_DDR case=(\d+) cycles=(\d+) writes=(\d+) reads=(\d+) "
    r"output=(\d+) halo=(\d+) stages=(\d+)/(\d+)/(\d+)/(\d+)"
)
FAULT_RE = re.compile(r"TB_PASS_EXPECTED_FAULT case=(\d+) status=(\d+) error=(\d+) cycles=(\d+)")
CASE_NAMES = {
    0: "normal", 1: "random_backpressure", 2: "stall_512", 3: "reset_cancel_recover",
    4: "response_error", 5: "dropped_response", 6: "post_pass_ddr_fault", 7: "corrupt_read_data",
}
EXPECTED_FAULTS = {4: 7, 5: 9, 6: 1, 7: 4}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, log: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    log.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}; see {log}")
    return result.stdout


def convert_words(source: Path, target: Path, fmt: str, transform=lambda value: value) -> None:
    data = source.read_bytes()
    size = struct.calcsize(fmt)
    if len(data) % size:
        raise ValueError(f"misaligned binary vector: {source}")
    width = size * 2
    with target.open("w", encoding="ascii", newline="\n") as stream:
        for (value,) in struct.iter_unpack(fmt, data):
            value = transform(value)
            stream.write(f"{value & ((1 << (size * 8)) - 1):0{width}x}\n")


def prepare_binary_vectors(directory: Path) -> dict[str, str]:
    vectors = ROOT / "vectors"
    generated = directory / "generated_vectors"
    generated.mkdir()
    jobs = {
        "stem_halo_values.hex": ("stem_halo_values_s8.bin", "<b", lambda x: x),
        "stem_halo_addr.hex": ("stem_halo_byte_addr_s32.bin", "<i", lambda x: x),
        "dw_halo_values.hex": ("dw_halo_values_s8.bin", "<b", lambda x: x),
        "dw_halo_addr.hex": ("dw_halo_byte_addr_s32.bin", "<i", lambda x: x),
        "stem_read_trace.hex": ("stem_read_trace_byte_addr_u32.bin", "<I", lambda x: x >> 1),
        "dw_read_trace.hex": ("dw_read_trace_byte_addr_u32.bin", "<I", lambda x: x >> 1),
    }
    for output, (source, fmt, transform) in jobs.items():
        convert_words(vectors / source, generated / output, fmt, transform)
    return {output: sha256(generated / output) for output in jobs}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=0)
    args = parser.parse_args()
    if args.case not in CASE_NAMES:
        raise ValueError("case must be 0..7")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    case_name = CASE_NAMES[args.case]
    work = ROOT / "verification" / f"{case_name}_{stamp}"
    work.mkdir(parents=True)
    generated_hashes = prepare_binary_vectors(work)
    raw_first = struct.unpack_from("<I", (ROOT / "vectors" / "stem_read_trace_byte_addr_u32.bin").read_bytes())[0]
    conversion_evidence = {
        "source_first_byte_address_decimal": raw_first,
        "source_first_byte_address_hex": f"0x{raw_first:08x}",
        "native_rule": "byte_address >> 1",
        "expected_first_native_hex": f"0x{raw_first >> 1:08x}",
        "generated_first_line": (work / "generated_vectors" / "stem_read_trace.hex").read_text(encoding="ascii").splitlines()[0],
        "prior_25_bit_read_evidence": "normal_20261015_160037_467022/simulation.log: expected=xxxxxxx",
    }
    (work / "conversion_evidence.json").write_text(json.dumps(conversion_evidence, indent=2) + "\n", encoding="utf-8")

    tools = {name: MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")}
    vendor_sources = [VENDOR / "ph1p_phy_gsr.v", VENDOR / "ph1p_logic_eram.v"]
    required = [*tools.values(), *vendor_sources]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing ModelSim/vendor input: " + ", ".join(missing))

    for name in ("rgb_pattern_words.hex", "combined_golden.hex", "loop_table.hex", "loop_parameters.hex"):
        shutil.copy2(ROOT / "vectors" / name, work)
    run([str(tools["vlib"]), "work"], work, work / "vlib.stdout.log")
    reused = sorted((ROOT / "reused").glob("*.v"), key=lambda path: path.name)
    sources = [*vendor_sources, *reused,
               ROOT / "rtl" / "road_frontend_layer_sequence.v",
               ROOT / "rtl" / "road_stem_ddr_sequence.v",
               ROOT / "tests" / "tb_frontend_ddr_tensor.v"]
    compile_command = [str(tools["vlog"]), "-work", "work", "-l", "compile.log",
                       *(str(path) for path in sources)]
    run(compile_command, work, work / "vlog.stdout.log")
    compile_text = (work / "compile.log").read_text(encoding="utf-8", errors="replace")
    summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_text)
    if not summaries or tuple(map(int, summaries[-1])) != (0, 0):
        raise RuntimeError(f"compile was not clean; see {work / 'compile.log'}")

    command = [str(tools["vsim"]), "-c", "-lib", "work", "PH1P_PHY_GSR",
               "tb_frontend_ddr_tensor", f"+CASE={args.case}",
               f"+VECTORS={ROOT / 'vectors'}", f"+GENERATED={work / 'generated_vectors'}",
               "-l", "simulation.log", "-do",
               "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
    output = run(command, work, work / "vsim.stdout.log")
    transcript = (work / "simulation.log").read_text(encoding="utf-8", errors="replace")
    combined = output + "\n" + transcript
    match = PASS_RE.search(combined)
    fault_match = FAULT_RE.search(combined)
    if args.case in EXPECTED_FAULTS:
        if not fault_match:
            raise RuntimeError(f"expected-fault receipt absent; retained failure: {work}")
        fault_values = list(map(int, fault_match.groups()))
        if fault_values[:3] != [args.case, 2, EXPECTED_FAULTS[args.case]]:
            raise RuntimeError(f"wrong expected-fault receipt: {fault_values[:3]}")
        values = [args.case, fault_values[3], 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        if not match:
            raise RuntimeError(f"PASS receipt absent; retained failure: {work}")
        values = list(map(int, match.groups()))
        if values[0] != args.case:
            raise RuntimeError(f"wrong case receipt: {values[0]}")

    receipt = {
        "result": "PASS_" + CASE_NAMES[args.case].upper(),
        "case": args.case,
        "simulator": run([str(tools["vsim"]), "-version"], work, work / "vsim_version.log").splitlines()[0],
        "clock_mhz": 100,
        "cycles": values[1],
        "writes": values[2],
        "reads": values[3],
        "output_bytes": values[4],
        "halo_accepts": values[5],
        "acc_pre_silu_post": values[6:10],
        "cycle_bins": ([int(item) for item in re.search(r"BINS ([0-9 ]+)", combined).group(1).split()]
                       if re.search(r"BINS ([0-9 ]+)", combined) else None),
        "expected_fault": EXPECTED_FAULTS.get(args.case),
        "compiled_source_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                                   for path in [*reused, *sources[-3:]]},
        "vendor_source_sha256": {str(path): sha256(path) for path in vendor_sources},
        "input_vector_sha256": {path.name: sha256(path) for path in sorted((ROOT / "vectors").iterdir()) if path.is_file()},
        "generated_vector_sha256": generated_hashes,
        "conversion_evidence": conversion_evidence,
        "compile_command": compile_command,
        "run_command": command,
    }
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": receipt["result"], "work": str(work), "cycles": values[1]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
