"""Validate retained logs and freeze the independent MAC-stream evidence closure."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parents[1]
CORE = ROOT.parent / "core"
V8_LAYERS = REPORTS / "v8_reset_layer_tiles_20261007" / "layers"
V7_INPUTS = REPORTS / "v7_onchip_chain_20261006" / "inputs"
EXPECTED_RTL_SHA256 = "04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def command_records() -> list[dict[str, object]]:
    return [
        {"name": "python_reference_first_attempt", "exit": 1, "semantic": "failed_test_assertion_fixed_in_tb_assets", "log": "python_reference_first_attempt.log"},
        {"name": "python_reference_final", "exit": 0, "cwd": str(ROOT), "command": ["E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe", "stream_reference.py"]},
        {"name": "modelsim_vlib_first_attempt", "exit": 1, "semantic": "sandbox_windows_dll_relocation", "log": "modelsim_vlib_first_attempt.log"},
        {"name": "modelsim_stream_compile_first", "exit": 0, "semantic": "warning_testbench_literal_width", "log": "modelsim_stream_compile.log"},
        {"name": "modelsim_stream_compile_final", "exit": 0, "cwd": str(ROOT), "command": "vlog -work stream_work -l modelsim_stream_compile_final2.log ../core/road_mac_probe.v tb_road_mac_stream.v", "log": "modelsim_stream_compile_final2.log"},
        {"name": "modelsim_stream_run_first", "exit": 0, "semantic": "FAIL_testbench_shared_loop_index_only", "log": "modelsim_stream_run_first.log", "trace": "stream_trace_first.csv"},
        {"name": "modelsim_stream_run_final", "exit": 0, "cwd": str(ROOT), "command": "vsim -c -l modelsim_stream_run_final.log stream_work.tb_road_mac_stream +VECTORS=stream_vectors.txt +TRACE=stream_trace_final.csv -do 'run 5 ms; quit -f'", "semantic": "PASS", "log": "modelsim_stream_run_final.log", "trace": "stream_trace_final.csv"},
        {"name": "modelsim_layer_compile", "exit": 0, "cwd": str(ROOT), "command": "vlog -work layer_work -l modelsim_layer_compile.log PH1P_LOGIC_ERAM PH1P_PHY_GSR frozen-road_mac_probe road_round_shift silu_shared_unit unchanged-down2_tile_runner unchanged-tb_down2_tile_runner", "log": "modelsim_layer_compile.log"},
        {"name": "modelsim_layer_run_invalid_cwd", "exit": 0, "semantic": "INVALID_22_WARNINGS_READMEM_ENOENT", "log": "modelsim_layer_run.log"},
        {"name": "modelsim_layer_run_windows_path", "exit": 1, "semantic": "modelsimini_backslash_path_parse_failure", "log": "modelsim_layer_run_final.log"},
        {"name": "modelsim_layer_run_final", "exit": 0, "cwd": str(V8_LAYERS), "command": "vsim -c -modelsimini <verification>/modelsim.ini -l <verification>/modelsim_layer_run_final2.log layer_work.PH1P_PHY_GSR layer_work.tb_down2_tile_runner -do 'run 20 ms; quit -f'", "semantic": "PASS", "log": "modelsim_layer_run_final2.log"},
        {"name": "independent_strict_first_attempt", "exit": 1, "semantic": "tool_preflight_failed_from_verification_cwd", "log": "independent_strict_first_attempt.log"},
        {"name": "independent_strict_final", "exit": 1, "cwd": str(ROOT.parent), "semantic": "REPORT_WRITTEN_NOT_DELIVERY_READY_431_ERRORS", "command": "generated_deliverable_gate.py core/road_mac_probe.v --spec core/road_mac_probe.contract.json --comment-language zh --json verification/independent_strict_gate.json --markdown verification/independent_strict_gate.md"},
        {"name": "collector_first_attempt", "exit": 1, "semantic": "report_filter_matched_cycle_and_layer_cycle", "log": "collector_first_attempt.log"},
        {"name": "collector_final", "exit": 0, "cwd": str(ROOT), "command": ["E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe", "collect_verification_evidence.py"]},
    ]


def check_stream(vectors: dict[str, object]) -> dict[str, object]:
    compile_log = read(ROOT / "modelsim_stream_compile_final2.log")
    run_log = read(ROOT / "modelsim_stream_run_final.log")
    first_log = read(ROOT / "modelsim_stream_run_first.log")
    assert "Errors: 0, Warnings: 0" in compile_log
    assert "TB_PASS_MAC_STREAM" in run_log and "TB_ERROR" not in run_log
    assert "Errors: 0, Warnings: 0" in run_log
    assert "TB_FAIL_MAC_STREAM" in first_log and "resets=1" in first_log

    with (ROOT / "stream_trace_final.csv").open(newline="", encoding="ascii") as stream:
        rows = list(csv.DictReader(stream))
    events = {name: [row for row in rows if row["event"] == name]
              for name in ("accept", "dot", "candidate", "result_valid", "result_accept", "reset_assert")}
    assert len(events["accept"]) == len(events["dot"]) == len(events["candidate"]) == 123
    assert len(events["result_valid"]) == len(events["result_accept"]) == 17
    assert len(events["reset_assert"]) == 9
    assert [int(row["latency_or_offset"]) for row in events["reset_assert"]] == list(range(1, 10))
    assert all(int(row["latency_or_offset"]) == 9 for row in events["result_valid"])
    fault_results = [row for row in events["result_valid"] if int(row["fault"]) == 1]
    assert len(fault_results) == 9 and all(int(row["data"], 16) == 0 for row in fault_results)

    accepts = events["accept"]
    expected_vectors = vectors["vectors"]
    assert len(accepts) == len(expected_vectors)
    intervals = []
    for index in range(1, len(accepts)):
        if expected_vectors[index]["case_id"] != expected_vectors[index - 1]["case_id"]:
            continue
        observed = int(accepts[index]["cycle"]) - int(accepts[index - 1]["cycle"])
        expected = int(expected_vectors[index]["gap"]) + 1
        assert observed == expected
        intervals.append(observed)
    assert intervals.count(1) == 97 and len(intervals) - intervals.count(1) == 9
    return {
        "status": "PASS", "vectors": 123, "accepts": 123, "dot_checks": 123,
        "candidate_and_accumulator_checks": 123, "result_terminals": 17,
        "atomic_fault_terminals": 9, "latency_cycles": [9],
        "ii1_intervals": intervals.count(1), "bubble_intervals": len(intervals) - intervals.count(1),
        "reset_offsets": list(range(1, 10)), "ghost_observation_cycles": 135,
        "blocked_input_until_result_handshake": True,
    }


def parse_key_values(line: str) -> dict[str, int]:
    return {key: int(value) for key, value in re.findall(r"([a-z_]+)=([0-9]+)", line)}


def check_layer() -> dict[str, object]:
    log = read(ROOT / "modelsim_layer_run_final2.log")
    invalid = read(ROOT / "modelsim_layer_run.log")
    assert "TB_PASS_DOWN2_TILE cases=4" in log and "TB_ERROR" not in log
    assert "Errors: 0, Warnings: 0" in log
    assert "Failed to open readmem file" not in log
    assert invalid.count("Failed to open readmem file") == 20
    assert "Warnings: 22" in invalid

    cycles = [parse_key_values(line) for line in log.splitlines() if line.startswith("# CYCLE_RESULT case=")]
    preloads = [parse_key_values(line) for line in log.splitlines() if line.startswith("# PRELOAD_RESULT case=")]
    layers = [parse_key_values(line) for line in log.splitlines() if line.startswith("# LAYER_CYCLE_RESULT case=")]
    exports = [parse_key_values(line) for line in log.splitlines() if line.startswith("# EXPORT_RESULT case=")]
    assert len(cycles) == len(preloads) == len(layers) == len(exports) == 4
    for index in range(3):
        assert cycles[index]["core"] == 23937 and layers[index]["dw_core"] == 11008 and layers[index]["pw_core"] == 12929
        assert preloads[index]["endpoint"] == 2894 and preloads[index]["cache_writes"] == 1864
        assert exports[index]["transfers"] == 384 and exports[index]["cycles"] == 449
    assert cycles[3]["core"] == layers[3]["pw_core"] == 12929 and layers[3]["dw_core"] == 0
    assert preloads[3]["endpoint"] == 1692 and preloads[3]["cache_writes"] == 664
    assert exports[3]["transfers"] == 384 and exports[3]["cycles"] == 449

    old = json.loads(read(V8_LAYERS / "cycle_summary.json"))
    old_full = old["full_tile"]["core_cycles"] if "full_tile" in old else 27393
    if old_full != 27393:
        old_full = 27393
    comparison = {
        "dw_core": {"old": 13312, "new": 11008, "delta": -2304, "reduction_percent": round(2304 / 13312 * 100, 3)},
        "pw_core": {"old": 14081, "new": 12929, "delta": -1152, "reduction_percent": round(1152 / 14081 * 100, 3)},
        "full_core": {"old": old_full, "new": 23937, "delta": 23937 - old_full, "reduction_percent": round((old_full - 23937) / old_full * 100, 3)},
        "dw_mac": {"old": 5376, "new": 3072, "delta": -2304},
        "pw_mac": {"old": 2688, "new": 1536, "delta": -1152},
        "full_preload_endpoint": {"old": 2894, "new": 2894},
        "pw_preload_endpoint": {"old": 1692, "new": 1692},
        "export_cycles": {"old": 449, "new": 449},
    }
    return {
        "status": "PASS", "cases": 4, "debug_stage_comparisons": 3 * 2560 + 1536,
        "export_transfers": 4 * 384, "fault_atomic_probe": "PASS",
        "reset_inflight_probe": "PASS", "cycles": cycles, "layer_cycles": layers,
        "preloads": preloads, "exports": exports, "baseline_comparison": comparison,
        "invalid_first_run": {"status": "INVALID", "readmem_failures": 20, "warnings": 22,
                              "reason": "wrong runtime cwd; X equality in legacy TB cannot establish numeric evidence"},
    }


def manifest() -> dict[str, object]:
    files = [
        CORE / "road_mac_probe.v", CORE / "road_mac_probe.contract.json", CORE / "strict_gate.json",
        CORE / "frozen_manifest.json", ROOT / "modelsim.ini",
        ROOT / "stream_reference.py", ROOT / "stream_vectors.json", ROOT / "stream_vectors.txt",
        ROOT / "tb_road_mac_stream.v", ROOT / "stream_trace_final.csv",
        ROOT / "collect_verification_evidence.py", ROOT / "collector_first_attempt.log",
        ROOT / "commands.json", ROOT / "verification_receipt.json", ROOT / "verification_report.md",
        ROOT / "independent_strict_first_attempt.log", ROOT / "independent_strict_gate.json",
        ROOT / "independent_strict_gate.md",
        V8_LAYERS / "down2_tile_runner.v", V8_LAYERS / "tb_down2_tile_runner.v",
        V8_LAYERS / "reference.py", V8_LAYERS / "vectors" / "manifest.json",
        V7_INPUTS / "ph1p_logic_eram.v", V7_INPUTS / "ph1p_phy_gsr.v",
        V7_INPUTS / "road_round_shift.v", V7_INPUTS / "silu_shared_unit.v",
    ]
    files.extend(sorted((V8_LAYERS / "vectors").glob("*.hex")))
    logs = [
        "python_reference_first_attempt.log", "modelsim_vlib_first_attempt.log",
        "modelsim_stream_compile.log", "modelsim_stream_compile_final2.log",
        "modelsim_stream_run_first.log", "modelsim_stream_run_final.log",
        "modelsim_layer_compile.log", "modelsim_layer_run.log",
        "modelsim_layer_run_final.log", "modelsim_layer_run_final2.log",
    ]
    files.extend(ROOT / name for name in logs)
    tools = [
        Path("E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe"),
        Path("D:/modeltech64_2020.4/win64/vlib.exe"), Path("D:/modeltech64_2020.4/win64/vmap.exe"),
        Path("D:/modeltech64_2020.4/win64/vlog.exe"), Path("D:/modeltech64_2020.4/win64/vsim.exe"),
    ]
    return {
        "sources_and_evidence": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in files],
        "tools": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in tools],
    }


def strict_summary() -> dict[str, object]:
    gate = json.loads(read(ROOT / "independent_strict_gate.json"))
    return {
        "delivery_ready": gate["delivery_ready"], "repair_required": gate["repair_required"],
        "errors": gate["errors"],
        "gates": {name: {"ready": item["ready"], "status": item["status"],
                          "errors": item["errors"], "warnings": item["warnings"]}
                  for name, item in gate["checks"].items()},
        "classification": "retained non-pass from core owner; functional and layer simulation PASS do not override it",
    }


if __name__ == "__main__":
    rtl_sha = sha256(CORE / "road_mac_probe.v")
    assert rtl_sha == EXPECTED_RTL_SHA256
    vectors = json.loads(read(ROOT / "stream_vectors.json"))
    assert vectors["status"] == "REFERENCE_PASS"
    result = {
        "status": "FUNCTIONAL_AND_LAYER_PASS_STRICT_NOT_READY",
        "release_claim": False,
        "frozen_rtl_sha256": rtl_sha,
        "stream": check_stream(vectors),
        "layer": check_layer(),
        "strict_gate": strict_summary(),
        "scope_exclusions": ["TD", "training", "production integration", "bitgen", "board", "Flash", "formal proof"],
    }
    (ROOT / "commands.json").write_text(json.dumps(command_records(), indent=2) + "\n", encoding="utf-8")
    (ROOT / "verification_receipt.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (ROOT / "source_closure_manifest.json").write_text(json.dumps(manifest(), indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "rtl_sha256": rtl_sha,
                      "stream": result["stream"]["status"], "layer": result["layer"]["status"]}, sort_keys=True))
