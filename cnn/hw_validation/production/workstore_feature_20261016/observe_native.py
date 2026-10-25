"""在同一封存工作仓TB上观察实际请求/native/响应端点，不添加RAM探针。"""
from pathlib import Path
import re
import shutil

import run

ROOT = Path(__file__).resolve().parent


def measure(rows):
    pending, result = {}, {"byte": [], "weight": []}
    last = {"byte": 0, "weight": 0}
    for row in rows:
        for channel, prefix in (("byte", "b"), ("weight", "w")):
            if row[prefix+"accept"] != last[channel]:
                assert row[prefix+"accept"] == last[channel]+1 and channel not in pending
                pending[channel] = row["sample"]
                last[channel] = row[prefix+"accept"]
            if row[prefix+"valid"] and channel in pending:
                result[channel].append(row["sample"]-pending.pop(channel))
    assert result["byte"] and result["weight"]
    assert set(result["byte"]) == {2} and set(result["weight"]) == {4}
    return result


def main():
    target = ROOT/"storage_frozen"
    run.check_binding(target)
    folder = ROOT/"native_endpoint_observation_attempt3"
    folder.mkdir(exist_ok=False)
    shutil.copy2(ROOT/"native_endpoint.tcl", folder/"observe.tcl")
    shutil.copytree(target/"workstore_case0/work", folder/"work")
    argv = [run.MODEL/"vsim.exe", "-c", "-voptargs=+acc", "-lib", "work", "PH1P_PHY_GSR",
            "tb_feature_workstore", "+CASE=0", "-do", "observe.tcl"]
    records = []
    output, code = run.command(argv, folder, "simulation.log", records, timeout=60)
    assert code == 0 and "** Error:" not in output
    rows = [{key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
            for line in re.findall(r"NATIVE_ENDPOINT sample=\d+ [^\r\n]*", output)]
    assert len(rows) == 300
    measured = measure(rows)
    negative = [dict(row) for row in rows]
    first = next(index for index, row in enumerate(negative) if row["bvalid"])
    negative[first]["sample"] += 1
    try:
        measure(negative)
    except AssertionError:
        pass
    else:
        raise AssertionError("wrong response timing escaped checker")
    run.check_binding(target)
    run.save(folder/"receipt.json", dict(status="PASS_ACTUAL_NATIVE_ENDPOINT_OBSERVATION",
        sample_period_ns=10, sample_offset_after_rising_edge_ns=2,
        byte_request_to_response_valid_cycles=sorted(set(measured["byte"])),
        weight_request_to_response_valid_cycles=sorted(set(measured["weight"])),
        byte_observed_responses=len(measured["byte"]), weight_observed_responses=len(measured["weight"]),
        complete_case_pass=False, same_frozen_TB=True, synthesis=False, script_sha256=run.digest(Path(__file__)),
        tcl_sha256=run.digest(folder/"observe.tcl"),
        input_binding_sha256=run.digest(target/"input_binding.json"), log_sha256=run.digest(folder/"simulation.log"),
        mutated_timing_negative_rejected=True))
    print("PASS_ACTUAL_NATIVE_ENDPOINTS", {key: sorted(set(value)) for key, value in measured.items()})


if __name__ == "__main__":
    main()
