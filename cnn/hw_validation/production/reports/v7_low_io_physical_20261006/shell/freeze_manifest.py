"""Freeze the low-I/O shell source, dependency, vector, and tool hash closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHAIN = HERE.parent.parent / "v7_onchip_chain_20261006"


def record(path: Path) -> dict[str, object]:
    """Return a stable absolute path, byte count, and SHA-256 record."""
    payload = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def main() -> None:
    """Write the final closure without modifying any frozen dependency."""
    shell_files = [
        HERE / "road_low_io_physical_shell.v",
        HERE / "tb_road_low_io_physical_shell.v",
        HERE / "road_low_io_physical_shell.contract.json",
        HERE / "requirements.md",
        HERE / "codegen_plan.md",
        HERE / "low_io_protocol_reference.py",
        HERE / "generate_signed_shell_vectors.py",
        HERE / "analyze_shell_trace.py",
        HERE / "generate_phase_cycle_csv.py",
        HERE / "freeze_manifest.py",
        HERE / "shell_cycle_summary.json",
        HERE / "shell_phase_cycles.csv",
        HERE / "strict_shell.json",
        HERE / "strict_shell.md",
        HERE / "strict_tb.json",
        HERE / "strict_tb_included.json",
        HERE / "strict_tb_included.md",
        HERE / "modelsim_shell_compile_frozen_c7bd.log",
        HERE / "modelsim_shell_run_frozen_c7bd.log",
        HERE / "spec" / "low_io_physical" / "road_low_io_physical_shell_spec.md",
        HERE / "eight_gate_status.json",
        HERE / "validation_receipt.json",
        HERE / "validation_report.md",
        HERE / "commands_and_results.md",
        HERE / "unresolved_issues.md",
    ]
    shell_files.extend(sorted((HERE / "spec" / "low_io_physical" / "waveforms").glob("*")))
    shell_files.extend(sorted((HERE / "inputs").glob("*")))
    dependency_files = [
        CHAIN / "road_onchip_chain.v",
        CHAIN / "inputs" / "road_mac_probe.v",
        CHAIN / "inputs" / "road_round_shift.v",
        CHAIN / "inputs" / "silu_shared_unit.v",
        CHAIN / "inputs" / "ph1p_logic_eram.v",
        CHAIN / "inputs" / "ph1p_phy_gsr.v",
    ]
    tool_files = [
        Path("D:/modeltech64_2020.4/win64/vlog.exe"),
        Path("D:/modeltech64_2020.4/win64/vsim.exe"),
        Path("E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe"),
    ]
    result = {
        "status": "FUNCTIONAL_PASS_STRICT_FAIL_PHYSICAL_PENDING",
        "top_module": "road_low_io_physical_shell",
        "top_io_bits": 38,
        "frozen_shell_sha256": hashlib.sha256((HERE / "road_low_io_physical_shell.v").read_bytes()).hexdigest(),
        "shell_files": [record(path) for path in shell_files],
        "frozen_dependencies": [record(path) for path in dependency_files],
        "tools": [record(path) for path in tool_files],
        "simulation": {"cases": 14, "errors": 0, "vendor_model_warnings": 2},
        "strict_gate": {
            "shell_errors": 667,
            "testbench_excluded_diagnostic_errors": 93,
            "testbench_included_errors": 219,
            "strict_warnings": 0,
            "delivery_ready": False,
        },
    }
    (HERE / "frozen_manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"MANIFEST_PASS shell_sha256={result['frozen_shell_sha256']}")


if __name__ == "__main__":
    main()
