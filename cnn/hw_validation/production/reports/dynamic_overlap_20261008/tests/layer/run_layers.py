"""Run the isolated overlapped DW/PW layer regression with frozen fixtures."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPORT = HERE.parents[1]
BASE = REPORT.parent / "diagnostic_repair_20261008"
RTL = REPORT / "rtl"
MODEL = BASE / "model" / "ph1p_logic_eram_runtime_model.v"
FIRST = HERE / "successful_first_run_20261008_222812"
MSIM = Path("D:/modeltech64_2020.4/win64")
FIXTURES = {
    "original": BASE / "layer" / "vectors",
    "stress": BASE / "layer" / "stress_bias_contract_host" / "vectors",
}
SOURCES = [
    RTL / "down2_dynamic_tile_runner.v",
    RTL / "road_down2_dynamic_adapter.v",
    RTL / "road_mac_probe.v",
    RTL / "road_dynamic_postprocess.v",
    RTL / "road_dynamic_requant.v",
    RTL / "road_round_shift.v",
    RTL / "silu_shared_unit.v",
    MODEL,
    HERE / "tb_down2_dynamic_overlap.v",
]


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(args: list[object], log: Path) -> None:
    first_failure = log.with_name(log.stem + ".first_failure" + log.suffix)
    if log.exists() and not first_failure.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        if "** Error:" in text or "Fatal:" in text or "AssertionError" in text:
            shutil.copy2(log, first_failure)
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run(
            [str(item) for item in args],
            cwd=HERE,
            stdout=stream,
            stderr=subprocess.STDOUT,
            check=False,
        )
    assert result.returncode == 0, (result.returncode, log)


def check_fixture(path: Path) -> dict[str, str]:
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["files"].items():
        assert sha(path / name) == digest, name
    needed = {
        "silu.hex", "dw_weights.hex", "dw_biases.hex", "pw_weights.hex",
        "pw_biases.hex",
        *(f"{case}_{kind}.hex" for case in ("edge", "interior", "bottom_right")
          for kind in ("halo", "output", "acc", "commit", "stages")),
    }
    assert all((path / name).is_file() for name in needed)
    for case in ("edge", "interior", "bottom_right"):
        records = path / f"{case}_records.json"
        if records.is_file():
            expected = [value & 0xFFFFFFFF
                        for row in json.loads(records.read_text(encoding="utf-8"))
                        for value in (row["pre"], row["silu"], row["post"])]
            actual = [int(line, 16) for line in
                      (path / f"{case}_stages.hex").read_text(encoding="ascii").splitlines()]
            assert actual == expected, records
    return {name: sha(path / name) for name in sorted(needed)}


def parse_cases(path: Path) -> list[dict[str, int]]:
    rows = []
    names = None
    for line in path.read_text(encoding="utf-8").splitlines():
        values = line.split(",")
        if names is None:
            names = values
        else:
            rows.append(dict(zip(names, map(int, values))))
    assert len(rows) == 7
    return rows


def main() -> None:
    fixture_hashes = {name: check_fixture(path) for name, path in FIXTURES.items()}
    assert all(path.is_file() for path in SOURCES), "RTL is not root-ready"
    first_receipt = json.loads((FIRST / "receipt.json").read_text(encoding="utf-8"))
    for name, digest in first_receipt["sources"].items():
        path = Path(name)
        if path.parent == RTL or path == MODEL:
            assert sha(path) == digest, path
    source_hashes = {str(path): sha(path) for path in SOURCES}

    work = HERE / "work"
    if not work.exists():
        run([MSIM / "vlib.exe", "work"], HERE / "vlib.log")
    run([MSIM / "vlog.exe", "-work", "work", *SOURCES], HERE / "vlog.log")

    summaries = {}
    for name, vectors in FIXTURES.items():
        csv = HERE / f"{name}_cycles.csv"
        log = HERE / f"{name}_simulation.log"
        run([
            MSIM / "vsim.exe", "-c", "-lib", "work", "tb_down2_dynamic_overlap",
            f"+VECTORS={vectors.as_posix()}", f"+REPORT={csv.as_posix()}",
            "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0",
        ], log)
        text = log.read_text(encoding="utf-8")
        assert "TB_PASS_DOWN2_DYNAMIC_OVERLAP" in text
        assert "** Error:" not in text and "Fatal:" not in text
        rows = parse_cases(csv)
        assert all(row["acc"] == 640 and row["pre"] == 640 and row["silu"] == 640
                   and row["post"] == 640 and row["commit"] == 640
                   and row["export"] == 384 for row in rows)
        assert all(row["dw_endpoint"] + row["pw_endpoint"] == row["endpoint"]
                   and row["table_writes"] == 1024 and row["preload_writes"] == 1864
                   and row["export_cycles"] >= 384 for row in rows)
        summaries[name] = rows

    old_lines = (BASE / "layer" / "stress_bias_contract_host" / "layer_cycles.csv").read_text(
        encoding="utf-8"
    ).splitlines()[1:]
    old_no_stall = [int(line.split(",")[1]) for line in old_lines
                    if line.split(",")[0] in ("0", "1", "2", "6")]
    assert old_no_stall == [20633] * 4
    for rows in summaries.values():
        assert all(row["endpoint"] < 20633 for row in rows if row["case"] in (0, 1, 2, 6))

    assert source_hashes == {str(path): sha(path) for path in SOURCES}
    receipt = {
        "status": "OVERLAPPED_LAYER_FUNCTION_PASS_NOT_PHYSICAL_OR_DEPLOYMENT",
        "old_serial_baseline_cycles": 20633,
        "old_baseline_is_comparison_only": True,
        "coverage_per_case": {
            "acc": 640, "pre": 640, "silu": 640, "post": 640,
            "commit": 640, "export": 384,
            "dw_mac_groups": 384, "pw_mac_groups": 256,
            "dw_batches": 256, "pw_batches": 128,
        },
        "sources": source_hashes,
        "rtl_and_model_unchanged_from_successful_first_run": True,
        "fixtures": fixture_hashes,
        "modelsim": {name: sha(MSIM / name) for name in ("vlib.exe", "vlog.exe", "vsim.exe")},
        "results": summaries,
        "artifacts": {
            name: sha(HERE / name) for name in (
                "original_cycles.csv", "stress_cycles.csv",
                "original_simulation.log", "stress_simulation.log",
                "original_simulation.first_failure.log",
            )
        },
        "preserved_initial_failure": "testbench fwrite format count; RTL compiled with zero errors",
        "preserved_successful_first_run": {
            path.name: sha(path) for path in sorted(FIRST.iterdir()) if path.is_file()
        },
        "measurement_semantics": {
            "endpoint_bins": "mutually exclusive priority: writeback stall, capacity wait, commit, MAC issue, input/storage wait, task close, drain, other",
            "activity": "pre/silu/post busy and active_overlap are non-exclusive activity measures and must not be added to endpoint bins",
            "phase_split": "dw_endpoint plus pw_endpoint equals endpoint for every case",
        },
        "limits": [
            "fixed TEST-package multipliers/shifts, not deployment QAT parameters",
            "digital layer simulation only; no DDR, whole-network, physical timing, accuracy, board, or bitstream evidence",
        ],
    }
    (HERE / "receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("OVERLAPPED_LAYER_PASS fixtures=2 cases=14 baseline=20633")


if __name__ == "__main__":
    main()
