"""封存五级写回候选的真实回归、检查器负例、周期和未通过门禁。"""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess

import run_csp_first_probe as base

OUT = base.BASE / "csp_writeback_pipeline_20261015_v2"
PRIOR = base.BASE / "qat_g10_csp_first_closure_20261015_v2"


def main():
    binding = json.loads((OUT / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    status = json.loads((OUT / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "PASS_WRITEBACK_TRACE_AND_17_REAL_CORE_CASES_NOT_DELIVERY_READY"
    first = (OUT / "writeback_trace.hex").open(encoding="ascii")
    row = int(next(first), 16)
    first.close()
    negative = OUT / "trace_wrong_expected_ready.hex"
    negative.write_text(f"{row ^ (1 << 211):078x}\n", encoding="ascii")
    argv = [str(base.MODEL / "vsim.exe"), "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_writeback_trace",
            f"+TRACE={negative.as_posix()}", "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
    result = subprocess.run(argv, cwd=OUT / "run", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", timeout=60)
    (OUT / "run/trace_negative.log").write_text(result.stdout, encoding="utf-8")
    assert "TRACE control cycle=0" in result.stdout and "CSP_WRITEBACK_TRACE_PASS" not in result.stdout
    base.save(OUT / "negative_receipt.json", dict(argv=argv, cwd=str(OUT / "run"),
        exit_code=result.returncode, executable_sha256=base.digest(Path(argv[0])),
        input_sha256=base.digest(negative), mismatch_detected=True,
        scope="改变首拍期望ready；实际RTL与正常向量均不改变"))
    old = json.loads((PRIOR / "case_receipts.json").read_text(encoding="utf-8"))["cases"]
    new = json.loads((OUT / "case_receipts.json").read_text(encoding="utf-8"))["cases"]
    old = {case["case"]: case["receipt"] for case in old}
    comparison = []
    for case in new:
        before = re.search(r"cycles=(\d+)", old[case["case"]])
        after = re.search(r"cycles=(\d+)", case["receipt"])
        if after is not None:
            a, b = int(before[1]), int(after[1])
            comparison.append(dict(case=case["case"], baseline_cycles=a, candidate_cycles=b, delta=b-a))
    base.save(OUT / "cycle_comparison.json", dict(cases=comparison,
        normal_cycles=7807, baseline_normal_cycles=7167, normal_delta=640,
        normal_tasks=160, expected_extra_per_task=4,
        random_backpressure_note="输入与写ready由LFSR驱动；任务退休改变相位，不作同一stall序列优化比较",
        full_graph_or_DDR=False))
    gate = json.loads((OUT / "source_closure_gate.json").read_text(encoding="utf-8"))
    assert gate["delivery_ready"] is False
    wrapper_findings = [v for v in gate["findings"] if v.get("path") == "road_csp_first_probe.v"]
    base.save(OUT / "wrapper_findings.json", dict(
        scope="新包装在真实五个算术子核源码环境下的发现，不含其余核自身问题",
        counts=dict(Counter(v["code"] for v in wrapper_findings)), findings=wrapper_findings))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    closure = {str(p): base.digest(p) for p in (OUT / "source_closure").glob("*.v")}
    for path, sha in closure.items():
        original = OUT / ("rtl" if Path(path).name == "road_csp_first_probe.v" else "reused") / Path(path).name
        assert base.digest(original) == sha
    base.save(OUT / "final_checks.json", dict(as_of=datetime.now().astimezone().isoformat(),
        real_core_cases_passed=17, trace_cycles=status["trace_cycles"],
        trace_coverage=json.loads((OUT / "trace_coverage.json").read_text(encoding="utf-8")),
        negative_checker_case_passed=True,
        original_hashes_rechecked=len(binding["original_sha256"]),
        staged_hashes_rechecked=len(binding["staged_sha256"]),
        source_closure_sha256=closure, finalizer_sha256=base.digest(Path(__file__)),
        strict_errors=gate["errors"], strict_warnings=gate["strict_warnings"],
        checks={k: v.get("status") for k, v in gate["checks"].items()},
        actual_modelsim_passed=True, strict_delivery_passed=False,
        scheduler_cache_integrated=False, synthesis_or_physical=False,
        full_network_or_actual_DDR=False, training_updates=0, board_or_flash=False,
        production_delivery_ready=False))
    status.update(strict_gate_passed=False, strict_errors=gate["errors"],
                  strict_warnings=gate["strict_warnings"], negative_checker_case_passed=True,
                  scheduler_cache_integrated=False)
    base.save(OUT / "status.json", status)
    print("SEALED_TRACE_534084_CORE_CASES_17_STRICT_GATE_FAILED", flush=True)


if __name__ == "__main__":
    main()
