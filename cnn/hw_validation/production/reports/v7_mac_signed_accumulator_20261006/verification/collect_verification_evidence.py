"""Collect immutable hashes and machine-check the signed33 simulation evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT.parent
PROJECT = ROOT.parents[5]
CANDIDATE = REPORT / "candidate" / "road_mac_probe.v"
LEGACY = PROJECT / "cnn" / "hw_validation" / "production" / "reports" / "v7_minimal_chain_20261006" / "inputs" / "road_mac_probe.v"
EXPECTED_CANDIDATE_SHA256 = "f8bf6cace6eb99bd9b915be5e27e1d38af4b3a2485ffeb6e87675d8bfc3478e8"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="ascii") as stream:
        return list(csv.DictReader(stream))


def check_candidate_trace(vectors: dict[str, object]) -> dict[str, object]:
    rows = records(ROOT / "modelsim_candidate_trace.csv")
    accepts = [row for row in rows if row["event"] == "accept"]
    terminals = [row for row in rows if row["event"] == "result_valid"]
    result_accepts = [row for row in rows if row["event"] == "result_accept"]
    resets = [row for row in rows if row["event"] == "reset_assert"]
    ready_results = [row for row in rows if row["event"] == "ready_high_result"]
    assert len(accepts) == len(vectors["vectors"]) == 84
    assert len(terminals) == len(result_accepts) == 12
    assert len(resets) == 10
    assert len(ready_results) == 1 and int(ready_results[0]["latency_or_stall"]) == 9

    expected_intervals = []
    observed_intervals = []
    for index in range(1, len(accepts)):
        previous = vectors["vectors"][index - 1]
        expected = 13 + previous["stall_cycles"] if previous["emit"] else 11
        observed = int(accepts[index]["cycle"]) - int(accepts[index - 1]["cycle"])
        assert observed == expected
        expected_intervals.append(expected)
        observed_intervals.append(observed)

    terminal_by_key = {(int(row["case"]), int(row["beat"])): row for row in terminals}
    faults = 0
    for vector in vectors["vectors"]:
        if not vector["emit"]:
            continue
        row = terminal_by_key[(vector["case_id"], vector["beat_id"])]
        assert int(row["latency_or_stall"]) == 9
        assert int(row["fault"]) == int(vector["fault"])
        expected_data = sum((value & 0xFFFFFFFF) << (32 * lane)
                            for lane, value in enumerate(vector["expected_data"]))
        assert int(row["data"], 16) == expected_data
        if vector["fault"]:
            faults += 1
            assert int(row["data"], 16) == 0

    reset_offsets = [int(row["beat"]) for row in resets]
    assert reset_offsets == [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
    return {
        "accepts": len(accepts),
        "terminals": len(terminals),
        "atomic_fault_terminals": faults,
        "result_accepts": len(result_accepts),
        "accept_interval_cycles": sorted(set(observed_intervals)),
        "expected_interval_cycles": sorted(set(expected_intervals)),
        "terminal_latency_cycles": sorted({int(row["latency_or_stall"]) for row in terminals}),
        "reset_offsets": reset_offsets,
        "ready_high_recovery_results": len(ready_results),
    }


def check_legacy_trace() -> dict[str, object]:
    rows = records(ROOT / "modelsim_legacy_negative_trace.csv")
    faults = [row for row in rows if row["event"] == "legacy_early_fault"]
    assert len(faults) == 2
    assert all(int(row["fault"]) == 1 for row in faults)
    assert all(int(row["latency_or_stall"]) == 9 for row in faults)
    assert all(int(row["data"], 16) == 0 for row in faults)
    return {"early_faults": 2, "latency_cycles": [9], "atomic_zero_payloads": 2}


def check_arithmetic(vectors: dict[str, object]) -> dict[str, object]:
    cases = {case["name"]: case for case in vectors["cases"]}
    positive_vectors = [vector for vector in vectors["vectors"]
                        if vector["case_name"] == "positive_excursion_recovers"]
    negative_vectors = [vector for vector in vectors["vectors"]
                        if vector["case_name"] == "negative_excursion_recovers"]
    assert all(value > (1 << 31) - 1 for value in positive_vectors[0]["candidate_signed34"])
    assert all(value < -(1 << 31) for value in negative_vectors[0]["candidate_signed34"])
    assert positive_vectors[1]["candidate_signed34"] == cases["positive_excursion_recovers"]["final"]
    assert negative_vectors[1]["candidate_signed34"] == cases["negative_excursion_recovers"]["final"]
    positive_endpoint = cases["maximum_positive_prefix_final_fault"]
    negative_endpoint = cases["maximum_negative_prefix_final_fault"]
    assert positive_endpoint["final"][0] == (1 << 31) - 1 + 192 * 16384
    assert negative_endpoint["final"][1] == -(1 << 31) + 192 * -16256
    assert positive_endpoint["fault"] and negative_endpoint["fault"]
    maximum = cases["maximum_192_terms_bias_extremes"]
    tail = cases["tail_mask_and_bias_once"]
    assert maximum["beats"] == 24 and maximum["terms"] == 192
    assert tail["final"] == [154, -258, 389]
    return {
        "three_lane_positive_recovery_partial": positive_vectors[0]["candidate_signed34"],
        "three_lane_positive_recovery_final": positive_vectors[1]["candidate_signed34"],
        "three_lane_negative_recovery_partial": negative_vectors[0]["candidate_signed34"],
        "three_lane_negative_recovery_final": negative_vectors[1]["candidate_signed34"],
        "maximum_terms": maximum["terms"],
        "maximum_beats": maximum["beats"],
        "legal_maximum_final": maximum["final"],
        "positive_proof_endpoint": positive_endpoint["final"][0],
        "negative_proof_endpoint": negative_endpoint["final"][1],
        "tail_mask_final": tail["final"],
    }


def strict_summary() -> dict[str, object]:
    gate = json.loads((ROOT / "tb_strict_gate.json").read_text(encoding="utf-8"))
    probe = json.loads((ROOT / "tb_strict_explicit_empty_probe.json").read_text(encoding="utf-8"))
    matrix = {}
    for name in ["compile", "ast", "readability", "comment", "naming", "profile", "testbench", "toolchain"]:
        check = gate["checks"][name]
        matrix[name] = {
            "ready": check["ready"],
            "status": check["status"],
            "errors": check["errors"],
            "warnings": check["warnings"],
        }
    assert not gate["delivery_ready"] and gate["repair_required"]
    assert not probe["delivery_ready"] and probe["repair_required"]
    return {
        "delivery_ready": gate["delivery_ready"],
        "repair_required": gate["repair_required"],
        "matrix": matrix,
        "entrypoint": "generated_deliverable_gate.py --include-testbench",
        "testbench_static_gate": "passed",
        "zero_port_ab_probe": {
            "source_change": "temporary copy only: module name; -> module name();",
            "original_primary_vg000": "only single module sources are currently supported",
            "explicit_empty_primary_vg000": "always header normalization failed",
            "delivery_ready": probe["delivery_ready"],
        },
        "classification": "Not a parser-only waiver. The dedicated static testbench gate passed, but the full strict entrypoint also found real local header, display-prefix, begin/end, naming, comment, and profile violations; formatter AST additionally cannot normalize this clock/task-oriented harness.",
        "claim": "strict gate retained as failed; functional simulation PASS is not promoted to readable-Verilog strict PASS",
    }


def command_records() -> list[dict[str, object]]:
    cwd = str(ROOT)
    candidate = str(CANDIDATE)
    legacy = str(LEGACY)
    tb = str(ROOT / "tb_road_mac_signed_accumulator.v")
    vectors = str(ROOT / "signed33_vectors.txt")
    return [
        {"name": "reference", "command": ["E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe", str(ROOT / "signed33_reference.py")], "cwd": str(PROJECT), "exit": 0, "log": "reference_run.log"},
        {"name": "modelsim_candidate_work_create", "command": ["D:/modeltech64_2020.4/win64/vlib.exe", "candidate_work"], "cwd": cwd, "exit": 0},
        {"name": "modelsim_legacy_work_create", "command": ["D:/modeltech64_2020.4/win64/vlib.exe", "legacy_work"], "cwd": cwd, "exit": 0},
        {"name": "modelsim_candidate_map_first_attempt", "command": ["D:/modeltech64_2020.4/win64/vmap.exe", "-modelsimini", "modelsim.ini", "candidate_work", str(ROOT / "candidate_work")], "cwd": cwd, "exit": 1, "log": "modelsim_vmap_first_attempt.log"},
        {"name": "modelsim_legacy_map_first_attempt", "command": ["D:/modeltech64_2020.4/win64/vmap.exe", "-modelsimini", "modelsim.ini", "legacy_work", str(ROOT / "legacy_work")], "cwd": cwd, "exit": 1, "log": "modelsim_vmap_first_attempt.log"},
        {"name": "modelsim_local_config_create", "command": ["D:/modeltech64_2020.4/win64/vmap.exe", "-c"], "cwd": cwd, "exit": 0},
        {"name": "modelsim_candidate_map", "command": ["D:/modeltech64_2020.4/win64/vmap.exe", "-modelsimini", "modelsim.ini", "candidate_work", str(ROOT / "candidate_work")], "cwd": cwd, "exit": 0},
        {"name": "modelsim_legacy_map", "command": ["D:/modeltech64_2020.4/win64/vmap.exe", "-modelsimini", "modelsim.ini", "legacy_work", str(ROOT / "legacy_work")], "cwd": cwd, "exit": 0},
        {"name": "modelsim_candidate_compile", "command": ["D:/modeltech64_2020.4/win64/vlog.exe", "-modelsimini", "modelsim.ini", "-work", "candidate_work", "-l", "modelsim_candidate_compile.log", candidate, tb], "cwd": cwd, "exit": 0, "log": "modelsim_candidate_compile.log"},
        {"name": "modelsim_candidate_run", "command": ["D:/modeltech64_2020.4/win64/vsim.exe", "-c", "-modelsimini", "modelsim.ini", "-l", "modelsim_candidate.log", "candidate_work.tb_road_mac_signed_accumulator", f"+VECTORS={vectors}", "+TRACE=modelsim_candidate_trace.csv", "-do", "run 2 ms; quit -f"], "cwd": cwd, "exit": 0, "log": "modelsim_candidate.log"},
        {"name": "modelsim_legacy_compile", "command": ["D:/modeltech64_2020.4/win64/vlog.exe", "-modelsimini", "modelsim.ini", "-work", "legacy_work", "-l", "modelsim_legacy_compile.log", legacy, tb], "cwd": cwd, "exit": 0, "log": "modelsim_legacy_compile.log"},
        {"name": "modelsim_legacy_negative_run", "command": ["D:/modeltech64_2020.4/win64/vsim.exe", "-c", "-modelsimini", "modelsim.ini", "-l", "modelsim_legacy_negative.log", "legacy_work.tb_road_mac_signed_accumulator", "+LEGACY_NEGATIVE", f"+VECTORS={vectors}", "+TRACE=modelsim_legacy_negative_trace.csv", "-do", "run 2 ms; quit -f"], "cwd": cwd, "exit": 0, "log": "modelsim_legacy_negative.log"},
        {"name": "iverilog_candidate_compile", "command": ["E:/project/qiansai/.tools/iverilog/bin/iverilog.exe", "-g2005", "-Wall", "-s", "tb_road_mac_signed_accumulator", "-o", str(ROOT / "candidate_check.vvp"), candidate, tb], "cwd": str(PROJECT), "exit": 0},
        {"name": "iverilog_candidate_run", "command": ["E:/project/qiansai/.tools/iverilog/bin/vvp.exe", str(ROOT / "candidate_check.vvp"), f"+VECTORS={vectors}", f"+TRACE={ROOT / 'iverilog_candidate_trace.csv'}"], "cwd": str(PROJECT), "exit": 0, "trace": "iverilog_candidate_trace.csv"},
        {"name": "iverilog_legacy_compile", "command": ["E:/project/qiansai/.tools/iverilog/bin/iverilog.exe", "-g2005", "-Wall", "-s", "tb_road_mac_signed_accumulator", "-o", str(ROOT / "legacy_check.vvp"), legacy, tb], "cwd": str(PROJECT), "exit": 0},
        {"name": "iverilog_legacy_run", "command": ["E:/project/qiansai/.tools/iverilog/bin/vvp.exe", str(ROOT / "legacy_check.vvp"), "+LEGACY_NEGATIVE", f"+VECTORS={vectors}", f"+TRACE={ROOT / 'iverilog_legacy_negative_trace.csv'}"], "cwd": str(PROJECT), "exit": 0, "trace": "iverilog_legacy_negative_trace.csv"},
        {"name": "tb_strict_gate", "command": ["E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe", "C:/Users/lenovo/.codex/skills/readable-verilog-generator/scripts/python/validation/generated_deliverable_gate.py", tb, "--spec", str(ROOT / "tb_road_mac_signed_accumulator.spec.json"), "--comment-language", "zh", "--include-testbench", "--json", str(ROOT / "tb_strict_gate.json"), "--markdown", str(ROOT / "tb_strict_gate.md")], "cwd": str(PROJECT), "exit": 0, "semantic_status": "delivery_ready=false", "log": "tb_strict_gate.json"},
        {"name": "tb_strict_explicit_empty_probe", "command": ["E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe", "C:/Users/lenovo/.codex/skills/readable-verilog-generator/scripts/python/validation/generated_deliverable_gate.py", "C:/Users/lenovo/AppData/Local/Temp/tb_road_mac_signed_accumulator_explicit_empty.v", "--spec", str(ROOT / "tb_road_mac_signed_accumulator.spec.json"), "--comment-language", "zh", "--include-testbench", "--json", str(ROOT / "tb_strict_explicit_empty_probe.json"), "--markdown", str(ROOT / "tb_strict_explicit_empty_probe.md")], "cwd": str(PROJECT), "exit": 0, "semantic_status": "delivery_ready=false", "log": "tb_strict_explicit_empty_probe.json"},
    ]


def manifest() -> dict[str, object]:
    sources = [
        CANDIDATE,
        LEGACY,
        REPORT / "coordinator" / "range_proof.json",
        REPORT / "candidate" / "strict_candidate_pass.json",
        ROOT / "signed33_reference.py",
        ROOT / "collect_verification_evidence.py",
        ROOT / "reference_run.log",
        ROOT / "verification_report.md",
        ROOT / "commands.json",
        ROOT / "verification_results.json",
        ROOT / "signed33_vectors.json",
        ROOT / "signed33_vectors.txt",
        ROOT / "tb_road_mac_signed_accumulator.v",
        ROOT / "tb_road_mac_signed_accumulator.spec.json",
        ROOT / "tb_road_mac_signed_accumulator.wavedrom.json",
        ROOT / "modelsim_candidate_compile.log",
        ROOT / "modelsim_candidate.log",
        ROOT / "modelsim_candidate_trace.csv",
        ROOT / "modelsim_legacy_compile.log",
        ROOT / "modelsim_legacy_negative.log",
        ROOT / "modelsim_legacy_negative_trace.csv",
        ROOT / "legacy_negative_first_attempt.log",
        ROOT / "modelsim_vmap_first_attempt.log",
        ROOT / "tb_strict_gate.json",
        ROOT / "tb_strict_gate.md",
        ROOT / "tb_strict_explicit_empty_probe.json",
        ROOT / "tb_strict_explicit_empty_probe.md",
    ]
    tools = [
        Path("E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe"),
        Path("E:/project/qiansai/.tools/iverilog/bin/iverilog.exe"),
        Path("E:/project/qiansai/.tools/iverilog/bin/vvp.exe"),
        Path("D:/modeltech64_2020.4/win64/vlog.exe"),
        Path("D:/modeltech64_2020.4/win64/vsim.exe"),
        Path("D:/modeltech64_2020.4/win64/vlib.exe"),
        Path("D:/modeltech64_2020.4/win64/vmap.exe"),
    ]
    return {
        "date": "2026-10-06 Asia/Shanghai",
        "sources": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in sources],
        "tools": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in tools],
    }


if __name__ == "__main__":
    candidate_sha = sha256(CANDIDATE)
    assert candidate_sha == EXPECTED_CANDIDATE_SHA256
    candidate_strict = json.loads((REPORT / "candidate" / "strict_candidate_pass.json").read_text(encoding="utf-8"))
    assert candidate_strict["delivery_ready"] and not candidate_strict["repair_required"]
    vectors = json.loads((ROOT / "signed33_vectors.json").read_text(encoding="utf-8"))
    assert vectors["status"] == "REFERENCE_PASS"
    candidate_log = (ROOT / "modelsim_candidate.log").read_text(encoding="utf-8", errors="replace")
    legacy_log = (ROOT / "modelsim_legacy_negative.log").read_text(encoding="utf-8", errors="replace")
    assert "VERILOG-GEN-RESULT PASS" in candidate_log and "Errors: 0, Warnings: 0" in candidate_log
    assert "VERILOG-GEN-NEGATIVE PASS" in legacy_log and "Errors: 0, Warnings: 0" in legacy_log
    result = {
        "status": "FUNCTIONAL_PASS_TESTBENCH_STRICT_FAIL",
        "release_claim": False,
        "candidate_sha256": candidate_sha,
        "candidate_strict_delivery_ready": True,
        "reference": {"status": vectors["status"], "cases": len(vectors["cases"]), "vectors": len(vectors["vectors"])},
        "arithmetic": check_arithmetic(vectors),
        "modelsim_candidate": check_candidate_trace(vectors),
        "modelsim_legacy_negative": check_legacy_trace(),
        "testbench_strict_gate": strict_summary(),
        "formal_proof_claim": False,
        "specialized_python_skill": "not installed; Python standard-library fallback used, no specialized Python strict claim",
        "scope_exclusions": ["TD", "training", "Flash", "physical timing", "unbounded malformed streams"],
    }
    (ROOT / "commands.json").write_text(json.dumps(command_records(), indent=2) + "\n", encoding="utf-8")
    (ROOT / "verification_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (ROOT / "baseline_manifest.json").write_text(json.dumps(manifest(), indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "candidate_sha256": candidate_sha,
                      "accepts": result["modelsim_candidate"]["accepts"],
                      "faults": result["modelsim_candidate"]["atomic_fault_terminals"],
                      "tb_strict_delivery_ready": result["testbench_strict_gate"]["delivery_ready"]}, sort_keys=True))
