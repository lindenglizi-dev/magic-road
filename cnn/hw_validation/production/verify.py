"""Re-run this CPU/RTL milestone and record evidence without training or programming."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
TOOLS = PROJECT.parents[1] / ".tools" / "iverilog" / "bin"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "reports" / stamp
    output.mkdir(parents=True, exist_ok=False)
    checks = {}

    def run(name, command, cwd, required_text=None):
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=60)
        content = completed.stdout + completed.stderr
        (output / (name + ".log")).write_text(content, encoding="utf-8")
        passed = completed.returncode == 0 and (not required_text or required_text in content)
        checks[name] = {"passed": passed, "command": list(map(str, command)),
                        "cwd": str(cwd), "returncode": completed.returncode,
                        "log_sha256": sha(output / (name + ".log"))}
        print(f"{name}: {'PASS' if passed else 'FAIL'}", flush=True)
        return passed

    run("cpu_graph_package", [sys.executable, "-B", "-X", "utf8", "-m", "unittest", "-v",
                              "test_graph.py", "test_numeric_package.py"], ROOT, "OK")
    run("cpu_requant_product", [sys.executable, "-B", "-X", "utf8", "requant_product.py"],
        ROOT, '"status": "cpu_exact_product_passed"')

    graph = json.loads((ROOT / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "numeric_artifacts/manifest.json").read_text(encoding="utf-8"))
    round_dir = ROOT / "round"
    vectors = json.loads((round_dir / "vectors.json").read_text(encoding="utf-8"))
    current_sources = all(sha(PROJECT / path) == digest for path, digest in graph["source_sha256"].items())
    current_package = (package["graph_source_sha256"] == graph["source_sha256"]
                       and package["generator_sha256"] == sha(ROOT / "numeric_package.py")
                       and package["payload_sha256"] == sha(ROOT / "numeric_artifacts/numeric_test.bin")
                       and package["physical_sha256"] == sha(ROOT / "numeric_artifacts/numeric_test_padded.bin")
                       and len(package["lane_files"]) == 56
                       and all(lane["sha256"] == sha(ROOT / "numeric_artifacts" / lane["name"])
                               for lane in package["lane_files"]))
    current_vectors = (vectors["vector_sha256"] == sha(round_dir / "vectors.dath")
                       and vectors["reference_sha256"] == sha(round_dir / "reference.py"))
    checks["frozen_artifacts"] = {"passed": current_sources and current_package and current_vectors,
                                  "graph_sources_current": current_sources,
                                  "package_current": current_package, "vectors_current": current_vectors}
    print(f"frozen_artifacts: {'PASS' if checks['frozen_artifacts']['passed'] else 'FAIL'}", flush=True)

    case_count = vectors["cases"]
    if not isinstance(case_count, int) or not 0 < case_count <= 16384:
        raise ValueError("invalid vector count")
    if run("round_compile", [str(TOOLS / "iverilog.exe"), "-g2001", "-s", "tb_road_round_shift",
                              "-o", str(output / "round.vvp"), "road_round_shift.v",
                              "tb_road_round_shift.v"], round_dir):
        run("round_sim", [str(TOOLS / "vvp.exe"), str(output / "round.vvp"),
                           f"+COUNT={case_count}"], round_dir,
            f"PASS round cases={case_count} intermediate={2 * case_count}")

    gate_path = round_dir / "gate_group_pass.json"
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    current_gate = (round_dir / "road_round_shift.v").stat().st_mtime_ns <= gate_path.stat().st_mtime_ns
    checks["round_strict_gate"] = {"passed": current_gate and gate["delivery_ready"],
                                    "current": current_gate, "errors": gate["errors"],
                                    "strict_warnings": gate["strict_warnings"],
                                    "matrix": gate["checks"], "path": str(gate_path),
                                    "sha256": sha(gate_path)}
    print(f"round_strict_gate: {'PASS' if checks['round_strict_gate']['passed'] else 'BLOCKED'}", flush=True)

    td_path = ROOT / "reports/round_td_20261004.json"
    td = json.loads(td_path.read_text(encoding="utf-8"))
    td_current = len(td["runs"]) == 2 and all(
        run["source_sha256"] == sha(round_dir / "road_round_shift.v")
        and all(sha(Path(run["directory"]) / name) == expected
                for name, expected in run["evidence_sha256"].items())
        for run in td["runs"])
    checks["round_routed_timing"] = {
        "passed": td_current and all(run["setup_passed"] and run["hold_passed"]
                                     for run in td["runs"]),
        "current": td_current, "path": str(td_path), "sha256": sha(td_path),
        "runs": [{key: run[key] for key in
                  ("directory", "resources", "timing_ns", "setup_passed", "hold_passed",
                   "native_hold_repair", "board_safe")} for run in td["runs"]]}
    print(f"round_routed_timing: {'PASS' if checks['round_routed_timing']['passed'] else 'BLOCKED'}", flush=True)

    probe_dir = ROOT / "round_internal_probe"
    probe_status = json.loads((probe_dir / "status.json").read_text(encoding="utf-8"))
    probe_numeric_path = probe_dir / probe_status["numeric_report"]
    probe_numeric = json.loads(probe_numeric_path.read_text(encoding="utf-8"))
    probe_gate_path = probe_dir / probe_status["gate_path"]
    probe_gate = json.loads(probe_gate_path.read_text(encoding="utf-8"))
    checker_current = True
    if "checker_receipt" in probe_status:
        checker_path = probe_dir / probe_status["checker_receipt"]
        checker = json.loads(checker_path.read_text(encoding="utf-8"))
        overlay = ROOT / "checker_overlay"
        skill = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
        checker_current = (
            sha(checker_path) == probe_status["checker_receipt_sha256"]
            and checker["status"] == "passed_project_checker"
            and checker["fixed_gate_sha256"] == sha(probe_gate_path)
            and checker["runner_sha256"] == sha(ROOT / "run_project_gate.py")
            and checker["overlay_sha256"] == {
                path.relative_to(overlay).as_posix(): sha(path) for path in overlay.rglob("*.py")}
            and all(sha(probe_dir / name) == expected for name, expected in checker["input_sha256"].items())
            and all(sha(skill / name) == expected for name, expected in checker["runtime_source_sha256"].items())
            and all(sha(skill / name) == expected for name, expected in checker["rule_configuration_sha256"].items()))
    probe_current = (
        checker_current and sha(probe_numeric_path) == probe_status["numeric_report_sha256"]
        and sha(probe_gate_path) == probe_status["gate_sha256"]
        and all(sha(probe_dir / name) == expected for name, expected in
                probe_numeric["source_sha256"].items())
        and sha(probe_dir / "rtl/road_round_shift.v") == sha(round_dir / "road_round_shift.v"))
    checks["internal_probe_binding"] = {"passed": probe_current,
                                         "checker_current": checker_current,
                                         "status_sha256": sha(probe_dir / "status.json")}
    if probe_current and run("internal_probe_compile", [
            str(TOOLS / "iverilog.exe"), "-g2001", "-Wall", "-s", "tb_road_round_internal_probe",
            "-o", str(output / "internal_probe.vvp"), "rtl/road_round_shift.v",
            "rtl/road_round_reset_gen.v", "rtl/road_round_internal_probe_core.v",
            "rtl/road_round_internal_probe.v", "tb/tb_road_round_internal_probe.v"], probe_dir):
        run("internal_probe_sim", [str(TOOLS / "vvp.exe"), str(output / "internal_probe.vvp")],
            probe_dir, "PASS probe generated=192 results=168 stalls=68 faults=3 checksum=0000000100001486")
    checks["internal_probe_strict_gate"] = {
        "passed": probe_current and probe_gate["delivery_ready"],
        "current": probe_current, "path": str(probe_gate_path), "sha256": sha(probe_gate_path),
        "errors": probe_gate["errors"], "strict_warnings": probe_gate["strict_warnings"]}
    print(f"internal_probe_strict_gate: {'PASS' if checks['internal_probe_strict_gate']['passed'] else 'BLOCKED'}", flush=True)

    silu_dir = ROOT / "silu"
    run("silu_python", [sys.executable, "-B", "-X", "utf8", str(silu_dir / "verify_vectors.py")],
        PROJECT, '"input_codes_checked": 65536')
    if run("silu_compile", [str(TOOLS / "iverilog.exe"), "-g2001", "-Wall", "-s", "tb_silu_shared_unit",
                             "-o", str(output / "silu.vvp"), str(silu_dir / "silu_shared_unit.v"),
                             str(silu_dir / "tb_ph1p_logic_eram_runtime_model.v"),
                             str(silu_dir / "tb_silu_shared_unit.v")], PROJECT):
        run("silu_sim", [str(TOOLS / "vvp.exe"), str(output / "silu.vvp")], PROJECT,
            "TB_PASS inputs=65536 latency=5 ii=1 table_words=1024")
    silu_gate_path = silu_dir / "reports/gate_attempt_6.json"
    silu_gate = json.loads(silu_gate_path.read_text(encoding="utf-8"))
    current_silu_gate = (silu_dir / "silu_shared_unit.v").stat().st_mtime_ns <= silu_gate_path.stat().st_mtime_ns
    checks["silu_strict_gate"] = {"passed": current_silu_gate and silu_gate["delivery_ready"],
                                  "current": current_silu_gate, "errors": silu_gate["errors"],
                                  "strict_warnings": silu_gate["strict_warnings"],
                                  "matrix": silu_gate["checks"], "path": str(silu_gate_path),
                                  "sha256": sha(silu_gate_path)}
    print(f"silu_strict_gate: {'PASS' if checks['silu_strict_gate']['passed'] else 'BLOCKED'}", flush=True)

    ph1p_report_path = output / "ph1p_semantic.json"
    if run("ph1p_interface_adapter", [sys.executable, "-B", "-X", "utf8",
            str(ROOT / "ph1p/run_ph1p_semantic_check.py"), "--rtl", str(silu_dir / "silu_shared_unit.v"),
            "--vendor-source", r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p\ph1p_logic_eram.v",
            "--skill-root", r"C:\Users\lenovo\.codex\skills\readable-verilog-generator",
            "--output", str(ph1p_report_path)], PROJECT, '"interface_support_ready": true'):
        ph1p = json.loads(ph1p_report_path.read_text(encoding="utf-8"))
        checks["ph1p_semantic_supplement"] = {
            "passed": ph1p["semantic_gate"]["delivery_ready"],
            "path": str(ph1p_report_path), "sha256": sha(ph1p_report_path),
            "issues": ph1p["semantic_gate"]["delivery_issues_by_rule"],
            "scope": "Interface-only supplement; does not replace the original strict gate or prove RAM timing"}
        print(f"ph1p_semantic_supplement: {'PASS' if checks['ph1p_semantic_supplement']['passed'] else 'BLOCKED'}", flush=True)

    baseline = json.loads((ROOT.parent / "reports/production_before.json").read_text(encoding="utf-8"))
    changes = [path for path, digest in baseline["files"].items() if sha(PROJECT / path) != digest]
    checks["production_unchanged"] = {"passed": not changes, "changed_paths": changes,
                                       "baseline_sha256": sha(ROOT.parent / "reports/production_before.json")}
    passed = all(check["passed"] for check in checks.values())
    report = {"status": "passed_component_milestone" if passed else "blocked_no_hardware_release",
              "utc": stamp, "checks": checks, "graph_summary": graph["summary"],
              "scope": "CPU graph/package, standalone rounding/SiLU RTL and rounding routed timing; not a complete CNN or board test",
              "source_sha256": {path.relative_to(ROOT).as_posix(): sha(path)
                                for path in ROOT.rglob("*") if path.suffix in (".py", ".v")},
              "remaining": ["strict gate closure", "shared MAC and two requantization stages",
                            "tile/DMA controller and DDR semantics", "complete network cycle simulation",
                            "TD resource/setup/hold", "board verification", "trained integer model accuracy"]}
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (ROOT / "latest_report.json").write_text(json.dumps({"report": str(output / "report.json"),
                                                        "status": report["status"]}, indent=2) + "\n", encoding="utf-8")
    print(str(output / "report.json"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
