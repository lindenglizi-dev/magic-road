"""绑定首残差tile的实际布局布线，保留外部/复位/严格门禁未通过状态。"""
from datetime import datetime
import json
from pathlib import Path
import re

import run_csp_first_probe as base

OUT = base.BASE / "csp_tile_integrated_20261015_v2"
PHYSICAL = OUT / "physical_attempt4"


def main():
    binding = json.loads((OUT / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    frozen = json.loads((PHYSICAL / "input_manifest.json").read_text(encoding="utf-8"))
    base.check_hashes(frozen)
    assert base.digest(PHYSICAL / "source_gate.db") == base.digest(OUT / "synthesis/gate.db")
    assert (PHYSICAL / "frontend.sdc").read_bytes() == (OUT / "synthesis/frontend.sdc").read_bytes()
    for path in (PHYSICAL / "sources").glob("*.v"):
        source = OUT / ("rtl" if (OUT / "rtl" / path.name).exists() else "reused") / path.name
        assert base.digest(source) == base.digest(path)
    summary = json.loads((PHYSICAL / "physical_summary.json").read_text(encoding="utf-8"))
    status = json.loads((PHYSICAL / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "ROUTED_INTERNAL_PASS_EXTERNAL_OPEN"
    assert summary["mapping_blockers"] == [] and summary["failed_endpoints"] == []
    internal = summary["reports"]["internal_all_checks"]["checks"]
    assert internal["setup"]["reported_paths"] == internal["hold"]["reported_paths"] == 7970
    assert internal["setup"]["worst_slack_ns"] == 0.484 and internal["hold"]["worst_slack_ns"] == 0.021
    normal = summary["reports"]["all_endpoints"]
    expanded = summary["reports"]["all_endpoints_include_ignored"]
    assert normal == expanded
    assert expanded["coverage"] == ["90.21%"]
    checks = (PHYSICAL / "check_timing_verbose.rpt").read_text(encoding="utf-8")
    findings = dict(re.findall(r"^\d+\. checking (.+?)\((\d+)\)",checks,re.M))
    findings = {key.strip():int(value) for key,value in findings.items()}
    for key in ("no clock","clock definition","invalid constraint","combinational loops","no path constraints",
                "shadowed/ignored timing exception constraints"):
        assert findings[key] == 0,(key,findings[key])
    assert findings["no input delay"] == 51 and findings["no output delay"] == 75
    area = summary["resources"]
    assert area["slice"]["used"] == 5396 and area["dsp"]["used"] == 30 and area["eram"]["used"] == 1
    assert area["hierarchy_rows"] == {"road_mac_probe":1,"road_dynamic_postprocess":1,"silu_shared_unit":1}
    # 真正的失败证据必须保持失败，尤其不能把0%覆盖率误解释成零违例。
    bad = OUT / "physical_attempt2"
    assert json.loads((bad / "status.json").read_text(encoding="utf-8"))["status"] == "PHYSICAL_FAILED_NO_RETRY"
    assert "STA coverage        : 0.00%" in (bad / "final_timing.rpt").read_text(encoding="utf-8")
    assert "missing actual internal timing checks" in (bad / "status.json").read_text(encoding="utf-8")
    result = dict(as_of=datetime.now().astimezone().isoformat(),source_directory="physical_attempt4",
        original_hashes_rechecked=len(binding["original_sha256"]),staged_hashes_rechecked=len(binding["staged_sha256"]),
        physical_input_hashes_rechecked=len(frozen),RTL_unchanged=True,clock_constraints_unchanged=True,
        internal_setup_hold_pass=True,internal_setup_ns=0.484,internal_hold_ns=0.021,
        internal_setup_paths=7970,internal_hold_paths=7970,full_report_scored_setup_paths=17953,
        full_report_scored_hold_paths=18163,STA_coverage_percent=90.21,
        all_scored_failed_endpoints=0,resources=area,check_timing_counts=findings,
        actual_DDR=False,full_CSP2_layer=False,full_graph=False,
        external_IO_timing_qualified=False,raw_reset_recovery_removal_qualified=False,
        formal_whole_system_timing_pass=False,strict_delivery_pass=False,
        bitstream_or_board=False,training_updates=0,production_delivery_ready=False,
        empty_STA_report_negative_rejected=True,
        source_gate_sha256=base.digest(PHYSICAL / "source_gate.db"),routed_database_sha256=base.digest(PHYSICAL / "pr.db"),
        finalizer_sha256=base.digest(Path(__file__)))
    base.save(OUT / "physical_final_checks.json",result)
    previous = json.loads((OUT / "status.json").read_text(encoding="utf-8"))
    if not (OUT / "status_before_physical.json").exists():
        base.save(OUT / "status_before_physical.json",previous)
    previous.update(status="FIRST_RESIDUAL_TILE_FUNCTION_AND_INTERNAL_SETUP_HOLD_PASS_INTEGRATION_OPEN",
        physical_internal_setup_hold_pass=True,physical_report="physical_attempt4/physical_summary.json",
        physical_resources=area,external_timing_qualified=False,raw_reset_timing_qualified=False,
        strict_gate_passed=False,production_delivery_ready=False,physical_final_checks="physical_final_checks.json")
    # 旧physical_timing_passed意指完整签核，不因局部内部通过改为true。
    previous["physical_timing_passed"] = False
    base.save(OUT / "status.json",previous)
    print("SEALED_ROUTED_INTERNAL_SETUP_HOLD_PASS_5396_SLICE_30DSP_1ERAM",flush=True)


if __name__ == "__main__":
    main()
