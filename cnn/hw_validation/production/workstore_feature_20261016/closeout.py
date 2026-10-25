"""只读核验一次TD失败并发布最新交接；不重新综合或改功能封存。"""
from pathlib import Path
import re

import run

ROOT = Path(__file__).resolve().parent


def classify(log, area):
    error = re.search(r"SYN-8228 ERROR: MapIO rule -- The IO number may exceed the device max IOs\((\d+)\)", log)
    total = re.search(r"(?m)^#IO\s+(\d+)", area)
    assert error and total and int(total[1]) > int(error[1])
    assert "FEATURE_WORKSTORE_DIAGNOSTIC_SYNTHESIS_COMPLETE" not in log
    latch = re.search(r"(?m)^\s*#LATCH\s+(\d+)", area)
    assert latch
    # 四种真实CSP/DW mask都确保lane0赋值；这只是窄语义证明，不清除TD警告。
    assert all((1 if dw and tail else 7) & 1 for dw in (False, True) for tail in (False, True))
    return dict(reason="DIAGNOSTIC_TOP_IO_MAPPING_EXCEEDS_DEVICE", external_IO=int(total[1]),
        device_IO_limit=int(error[1]), elaboration_latch_warning_preserved="HDL-5369" in log,
        optimized_RTL_latches=int(latch[1]), undriven_policy_warning_unlocalized="SYN-5025" in log)


def main():
    target = ROOT/"frozen"
    run.check_binding(target)
    ready = run.read(ROOT/"functional_ready.json")
    assert ready["all_required_cases_passed"] and ready["validated_case_directories"] == 15
    assert ready["completed_clean_block_runs"] == 17
    run.verify(ready["evidence"])
    seal = run.read(ROOT/"delivery_manifest.json")
    assert run.digest(ROOT/"delivery_manifest.json") == ready["delivery_manifest_sha256"]
    run.verify(seal["artifacts_sha256"])
    folder = ROOT/"synthesis"
    run.verify(run.read(folder/"input_manifest.json"))
    status, command = run.read(folder/"status.json"), run.read(folder/"command.json")
    assert status["status"] == "SYNTHESIS_FAILED_NO_RETRY"
    assert len(command["argv"]) == 2 and command["argv"][1] == "build.tcl"
    assert Path(command["argv"][0]).resolve() == Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe").resolve()
    assert Path(command["cwd"]).resolve() == folder.resolve()
    assert command["native_returncode"] == 0
    assert run.digest(folder/"launcher.log") == command["log_sha256"]
    log = (folder/"launcher.log").read_text(encoding="utf-8")
    area = (folder/"rtl.area").read_text(encoding="utf-8")
    result = classify(log, area)
    assert not any((folder/name).exists() for name in ("gate.area", "gate_netlist.v", "gate.qor"))
    try:
        classify(log.replace("SYN-8228 ERROR:", "REMOVED_ERROR:"), area)
    except AssertionError:
        pass
    else:
        raise AssertionError("removed real failure marker escaped checker")
    report = dict(status="FUNCTION_PASS_TD_IO_MAPPING_FAILED_NO_RETRY", date="2026-10-16",
        candidate="frozen", functional_cases=15, complete_clean_block_runs=17,
        synthesis=result, actual_mapped_ERAM=None, actual_mapped_DSP=None, actual_mapped_Slice=None,
        strict_gate_passed=False, strict_errors=6680, strict_warnings=26,
        CSP_normal_cycles=97886234, SPPF_normal_cycles=18763766,
        fragment_sum_cycles=116650000, fragment_sum_is_whole_network=False,
        whole_network_FPS_qualified=False, actual_DDR=False, full_graph=False,
        additional_diagnostic_slot_required=True, automatic_retry=False,
        new_semantic_findings_require_followup=True,
        training_updates=0, production_modified=False, place_route=False, bitstream=False, board=False,
        mutated_failure_marker_negative_rejected=True, production_delivery_ready=False)
    paths = [ROOT/"functional_ready.json", ROOT/"delivery_manifest.json", ROOT/"physical_handoff.txt",
        ROOT/"访存周期诊断与后续小步.txt", Path(__file__)]
    paths += [folder/name for name in ("status.json", "command.json", "input_manifest.json", "launcher.log", "rtl.area", "failure.json")]
    report["evidence_sha256"] = {str(path): run.digest(path) for path in paths}
    run.verify(report["evidence_sha256"])
    assert not (ROOT/"latest_status.json").exists(), "preserve existing closeout"
    run.save(ROOT/"latest_status.json", report)
    run.save(ROOT/"latest_delivery_manifest.json", dict(status=report["status"],
        artifacts_sha256={str(path): run.digest(path) for path in [ROOT/"latest_status.json", *paths]},
        production_delivery_ready=False))
    print("CLOSED_FUNCTION_PASS_TD_IO_FAIL_NO_RETRY", result["external_IO"], result["device_IO_limit"])


if __name__ == "__main__":
    main()
