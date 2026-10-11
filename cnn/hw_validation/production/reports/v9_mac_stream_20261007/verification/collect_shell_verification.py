"""Build the standalone receipt for the v9 38-bit shell regressions."""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V9 = ROOT.parent
REPORTS = V9.parent
V8 = REPORTS / "v8_reset_layer_tiles_20261007"
V7_CHAIN = REPORTS / "v7_onchip_chain_20261006"
V7_SHELL = REPORTS / "v7_low_io_physical_20261006"
EXPECTED_MAC_SHA = "04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def record(path):
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def checked_log(name, marker, warnings):
    path = ROOT / name
    text = path.read_text(encoding="utf-8", errors="replace")
    assert marker in text
    assert "TB_ERROR" not in text and "TB_FAIL" not in text
    assert "Failed to open" not in text and "ENOENT" not in text
    assert f"Errors: 0, Warnings: {warnings}" in text
    warning_lines = [line for line in text.splitlines() if "** Warning:" in line]
    assert len(warning_lines) == warnings
    if warnings:
        assert all("ph1p_logic_eram.v(165)" in line and "INIT_FILE" in line for line in warning_lines)
    return record(path)


def main():
    mac = V9 / "core/road_mac_probe.v"
    assert digest(mac) == EXPECTED_MAC_SHA

    regression_tb_old = V8 / "reset/tb_road_low_io_reset_shell_regression.v"
    reset_tb_old = V8 / "reset/tb_road_low_io_reset_shell.v"
    regression_tb_copy = ROOT / "shell_v9_tb/tb_road_low_io_reset_shell_regression_v9.v"
    reset_tb_copy = ROOT / "shell_v9_tb/tb_road_low_io_reset_shell_v9.v"
    assert digest(regression_tb_old) == digest(regression_tb_copy)
    assert digest(reset_tb_old) == digest(reset_tb_copy)

    full_compile = ROOT / "modelsim_shell_v9_compile.log"
    final_tb_compile = ROOT / "modelsim_shell_v9_tb_recompile_final.log"
    for path in (full_compile, final_tb_compile):
        text = path.read_text(encoding="utf-8", errors="replace")
        assert "Errors: 0, Warnings: 0" in text

    regression_log = checked_log(
        "modelsim_shell_v9_regression_run_final.log",
        "TB_PASS_LOW_IO cases=14 errors=0 io_bits=38 max_packets=96 max_groups=24 max_terms=192",
        2,
    )
    reset_log = checked_log(
        "modelsim_shell_v9_reset_run_final.log",
        "TB_PASS_RESET cases=6 errors=0 release_stages=2 first_consume_edge=3",
        2,
    )
    baseline_log = (ROOT / "shell_baseline_hash_audit_final.log").read_text(encoding="utf-8")
    assert '"status": "BASELINES_UNCHANGED"' in baseline_log
    assert '"previous_stage_files": 250' in baseline_log
    assert '"legacy_files": 360' in baseline_log

    cycles = json.loads((ROOT / "shell_measured_cycles.json").read_text(encoding="utf-8"))
    assert cycles["status"] == "SHELL_TRACE_ACCOUNTING_PASS"
    assert len(cycles["completed_runs"]) == 11
    assert len(cycles["cancelled_runs"]) == 1
    base = cycles["completed_runs"][0]
    assert base["core_cycles"] == 396
    assert base["exclusive_stage_cycles"] == {
        "mac": 48,
        "pre_requant": 132,
        "silu": 84,
        "post_requant": 120,
        "commit": 12,
        "fault": 0,
    }

    sources = [
        V7_CHAIN / "inputs/ph1p_logic_eram.v",
        V7_CHAIN / "inputs/ph1p_phy_gsr.v",
        mac,
        V7_CHAIN / "inputs/road_round_shift.v",
        V7_CHAIN / "inputs/silu_shared_unit.v",
        V7_CHAIN / "road_onchip_chain.v",
        V7_SHELL / "shell/road_low_io_physical_shell.v",
        V8 / "reset/road_low_io_reset_shell.v",
        regression_tb_copy,
        reset_tb_copy,
    ]
    input_names = [
        "silu_table.hex",
        "expected_features_16.hex",
        "mac_16_channels.txt",
        "expected_features_13.hex",
        "mac_13_channels.txt",
        "expected_features_saturation.hex",
        "signed_case_1_expected.hex",
        "signed_case_1.txt",
        "signed_case_2_expected.hex",
        "signed_case_2.txt",
        "signed_case_9_expected.hex",
        "signed_case_9.txt",
        "signed_case_10.txt",
    ]
    inputs = [V7_SHELL / "shell/inputs" / name for name in input_names]

    evidence_names = [
        "modelsim_shell_v9_compile.log",
        "modelsim_shell_v9_tb_recompile_final.log",
        "modelsim_shell_v9_regression_run_final.log",
        "modelsim_shell_v9_reset_run_final.log",
        "shell_cycle_trace.csv",
        "shell_measured_cycles.json",
        "shell_trace_analysis.log",
        "shell_baseline_hash_audit_final.log",
        "modelsim_shell_v9_vlib_first_attempt.log",
        "modelsim_shell_v9_compile_first_attempt.log",
        "modelsim_shell_v9_regression_run.log",
        "modelsim_shell_regression_run.log",
        "modelsim_shell_reset_run.log",
    ]
    evidence = [record(ROOT / name) for name in evidence_names if (ROOT / name).exists()]

    receipt = {
        "schema": "v9_mac_stream_shell_verification_receipt_v1",
        "status": "SHELL_FUNCTIONAL_PASS",
        "scope": "Frozen 38-bit synchronous-release shell with the frozen v9 MAC; verification-only ModelSim library and outputs.",
        "frozen_mac": record(mac),
        "source_closure": [record(path) for path in sources],
        "golden_inputs": [record(path) for path in inputs],
        "testbench_identity": {
            "regression_original": record(regression_tb_old),
            "regression_copy": record(regression_tb_copy),
            "reset_original": record(reset_tb_old),
            "reset_copy": record(reset_tb_copy),
            "identical": True,
            "timing_assertion_changes": "none",
            "numeric_expectation_changes": "none",
        },
        "compile": {
            "status": "pass",
            "full": record(full_compile),
            "final_exact_tb_recompile": record(final_tb_compile),
            "errors": 0,
            "warnings": 0,
        },
        "regressions": {
            "base_14_cases": {
                "status": "pass",
                "simulation_time_ns": 405785,
                "errors": 0,
                "warnings": 2,
                "log": regression_log,
            },
            "reset_6_cases": {
                "status": "pass",
                "simulation_time_ns": 41440,
                "errors": 0,
                "warnings": 2,
                "release_stages": 2,
                "first_consume_edge": 3,
                "log": reset_log,
            },
            "warning_scope": "Only the two pre-existing PH1P_LOGIC_ERAM INIT_FILE part-select warnings; no file-open/readmem warning.",
        },
        "measured_cycles": cycles,
        "baseline_integrity": {
            "status": "pass_after_final_v9_runs",
            "previous_stage_files": 250,
            "legacy_files": 360,
            "manifest_sha256": "e57298b84834624e361a3baa49623d3313cdfae9bdb368d62bbffba858274393",
            "audit_log": record(ROOT / "shell_baseline_hash_audit_final.log"),
        },
        "boundary_incident": {
            "occurred": True,
            "description": "An earlier unchanged-TB run used the old v8/reset working directory and overwrote its relative shell_cycle_trace.csv output. This was an out-of-scope write even though the file was subsequently restored.",
            "affected_path": str(V8 / "reset/shell_cycle_trace.csv"),
            "restored_from": str(V7_SHELL / "review/shell_cycle_trace.csv"),
            "restored_sha256": "8177bc890522004a5cb7b75680e6201ab3f303295ae97bd20aec80893969b44b",
            "post_restore_audit": "All 250 previous-stage and 360 legacy files match their frozen manifests.",
            "production_rtl_modified": False,
        },
        "invalid_attempts": [
            {
                "log": "modelsim_shell_regression_run.log",
                "reason": "Ran from the old v8 working directory; numerically passed but invalid for v9 scope and caused the disclosed trace overwrite.",
            },
            {
                "log": "modelsim_shell_reset_run.log",
                "reason": "Ran from the old v8 working directory; superseded by the final v9-cwd run.",
            },
            {
                "log": "modelsim_shell_v9_regression_run.log",
                "reason": "Absolute vector path exceeded the unchanged 128-byte TB task argument and was truncated; 8 errors and 3 warnings. Superseded by exact old relative paths from the v9 cwd.",
            },
            {
                "logs": ["modelsim_shell_v9_vlib_first_attempt.log", "modelsim_shell_v9_compile_first_attempt.log"],
                "reason": "Known sandbox DLL relocation launch failure; no system repair was attempted.",
            },
        ],
        "commands": [
            "vlib shell_work_v9_lib",
            "vmap -modelsimini modelsim.ini shell_work_v9_lib shell_work_v9_lib",
            "vlog -modelsimini modelsim.ini -work shell_work_v9_lib <frozen source closure> <copied old TBs>",
            "vsim -c -modelsimini modelsim.ini -l modelsim_shell_v9_regression_run_final.log shell_work_v9_lib.PH1P_PHY_GSR shell_work_v9_lib.tb_road_low_io_reset_shell_regression -do {run 2 ms; quit -f}",
            "vsim -c -modelsimini modelsim.ini -l modelsim_shell_v9_reset_run_final.log shell_work_v9_lib.PH1P_PHY_GSR shell_work_v9_lib.tb_road_low_io_reset_shell -do {run 1 ms; quit -f}",
            "E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe analyze_shell_trace.py",
            "E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe ../check_baseline.py",
        ],
        "evidence": evidence,
        "excluded": ["DUT edits", "layer-runner edits", "TD", "training", "bitgen", "board", "Flash"],
    }
    (ROOT / "shell_verification_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )

    table = []
    for run in cycles["completed_runs"]:
        buckets = run["exclusive_stage_cycles"]
        table.append(
            f"| {run['name']} | {run['core_cycles']} | {buckets['mac']} | "
            f"{buckets['pre_requant']} | {buckets['silu']} | {buckets['post_requant']} | "
            f"{buckets['commit']} | {buckets['fault']} | {run['old_core_cycles']} |"
        )
    report = """# v9 frozen-MAC 38-bit shell verification

Status: **PASS** for the frozen functional shell scope.

- Frozen MAC SHA-256: `04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`.
- The copied 14-case and 6-case TB sources are byte-identical to the v8 originals. Numeric and timing assertions were not changed.
- Final runs used only the v9 verification working directory and a separate `shell_work_v9_lib` ModelSim library.
- 14-case shell regression: `TB_PASS_LOW_IO`, 405785 ns, 0 errors, 2 known ERAM warnings.
- 6-case reset regression: `TB_PASS_RESET`, 41440 ns, two-stage release and first consume on edge 3, 0 errors, 2 known ERAM warnings.
- No final log contains a failed-open, ENOENT, readmem, `TB_ERROR`, or `TB_FAIL` indication.
- Final post-run freeze audit: v8 250 files and legacy 360 files unchanged.

## Mutually exclusive core-cycle accounting

Each half-open core interval is assigned to exactly one chain-state bucket. The old cycles are comparison data only; the old 436-cycle base is not asserted for the new MAC.

| Run | New core | MAC | Pre-requant | SiLU | Post-requant | Commit | Fault | Old core |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
""" + "\n".join(table) + """

The new base16 and tail13 windows are 396 cycles: 48 MAC + 132 pre-requant + 84 SiLU + 120 post-requant + 12 commit + 0 fault. The non-MAC buckets are unchanged from the old baseline; only the MAC bucket falls from 88 to 48.

## Retained failures and scope incident

- The first sandbox launches failed with the known Windows DLL relocation error; logs are retained and the same scoped ModelSim commands were rerun outside the sandbox.
- The first v9-cwd 14-case attempt used an absolute vector path longer than the unchanged TB's 128-byte task argument. It failed with 8 errors and 3 warnings. The final run restored the exact old relative paths, which resolve correctly from `verification`, and passed.
- Before the final v9-only runs, an earlier unchanged-TB run was mistakenly launched from the old v8 reset directory and overwrote its relative `shell_cycle_trace.csv`. That was an out-of-scope write. The file was restored from a frozen identical v7 copy to SHA-256 `8177bc890522004a5cb7b75680e6201ab3f303295ae97bd20aec80893969b44b`; subsequent full 250+360-file audits pass. This history is disclosed even though the restored content now matches.

This supplemental receipt does not modify the already frozen main verification closure or authorize TD, training, bitgen, board, or Flash work.
"""
    (ROOT / "shell_verification_report.md").write_text(report, encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "mac_sha256": receipt["frozen_mac"]["sha256"],
        "base_core_cycles": base["core_cycles"],
        "base_buckets": base["exclusive_stage_cycles"],
        "receipt": str(ROOT / "shell_verification_receipt.json"),
    }))


if __name__ == "__main__":
    main()
