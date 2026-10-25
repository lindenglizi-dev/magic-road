"""C9 result publisher cycle model; stdlib only, no FINAL97 table storage.

step() returns outputs immediately before the active edge, then advances state.
Both reset-release edges suppress transfers; the third edge may accept a start.
"""

import argparse
import hashlib
import json
from pathlib import Path


DEFAULTS = {
    "i_rstn": 1, "i_cancel": 0, "i_start_valid": 0,
    "i_start_epoch": 0, "i_start_task_id": 0, "i_start_source_frame_id": 0,
    "i_start_model_id": 0, "i_start_capture_ms": 0, "i_now_ms": 0,
    "i_pipeline_start_ready": 1, "i_entry_valid": 0, "i_entry": 0,
    "i_result_frame_token": 0, "i_result_count": 0, "i_result_done": 0,
    "i_pipeline_fault": 0, "i_table_entry_ready": 1, "i_table_meta_ready": 1,
    "i_table_copy_ack": 0, "i_table_busy": 0, "i_table_error": 0,
}
WIDTHS = {
    **{name: 1 for name in DEFAULTS},
    **{name: 32 for name in ("i_start_epoch", "i_start_task_id",
                           "i_start_source_frame_id", "i_start_model_id",
                           "i_result_frame_token")},
    "i_start_capture_ms": 64, "i_now_ms": 64, "i_entry": 97,
    "i_result_count": 7,
}


def pack_metadata(epoch, task, source, model, count, capture, completion):
    """SRIF1: status[136:135] is always zero for a sealed success."""
    return (epoch | (task << 32) | (source << 64) | (model << 96)
            | (count << 128) | (capture << 137) | (completion << 201))


class Publisher:
    """Five-state transactional publisher, with two reset-release flops."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "IDLE"
        self.release = 0
        self.metadata = 0
        self.accepted_count = 0

    def step(self, **updates):
        inputs = DEFAULTS | updates
        assert not (updates.keys() - DEFAULTS.keys()), "unknown input"
        for name, value in inputs.items():
            assert isinstance(value, int) and 0 <= value < (1 << WIDTHS[name]), name
        if not inputs["i_rstn"]:
            self.reset()
        released = self.release == 3 and bool(inputs["i_rstn"])
        task = (self.metadata >> 32) & 0xFFFFFFFF
        capture = (self.metadata >> 137) & 0xFFFFFFFFFFFFFFFF
        token_ok = inputs["i_result_frame_token"] == task
        common_failure = bool(inputs["i_cancel"] or inputs["i_pipeline_fault"]
                              or inputs["i_table_error"])
        run_failure = common_failure or bool(
            inputs["i_entry_valid"] and (not token_ok or self.accepted_count >= 64)
        ) or bool(inputs["i_result_done"] and (
            inputs["i_entry_valid"] or not token_ok
            or inputs["i_result_count"] != self.accepted_count
            or self.accepted_count > 64 or inputs["i_now_ms"] < capture
        ))
        meta_failure = common_failure or bool(inputs["i_entry_valid"])
        preseal_failure = ((self.state == "RUN" and run_failure)
                           or (self.state == "META" and meta_failure))
        start_allowed = bool(released and self.state == "IDLE"
                             and not common_failure and not inputs["i_table_busy"]
                             and inputs["i_table_entry_ready"])
        start_ready = bool(start_allowed and inputs["i_pipeline_start_ready"])
        forwarding = released and self.state == "RUN" and not run_failure
        outputs = {
            "o_start_ready": int(start_ready),
            "o_pipeline_start_valid": int(start_allowed and inputs["i_start_valid"]),
            "o_pipeline_frame_token": inputs["i_start_task_id"] if self.state == "IDLE" else task,
            "o_pipeline_model_id": inputs["i_start_model_id"] if self.state == "IDLE" else (self.metadata >> 96) & 0xFFFFFFFF,
            "o_pipeline_cancel": int(released and (self.state == "ABORT" or (
                inputs["i_cancel"] and self.state != "WAIT_ACK"))),
            "o_entry_ready": int(forwarding and inputs["i_table_entry_ready"]),
            "o_table_entry_valid": int(forwarding and inputs["i_entry_valid"]),
            "o_table_entry": inputs["i_entry"],
            "o_table_meta_valid": int(released and self.state == "META" and not meta_failure),
            "o_table_metadata": self.metadata,
            "o_table_abort": int(released and (self.state == "ABORT" or preseal_failure)),
            "o_busy": int(released and self.state != "IDLE"),
            "o_error": int(released and self.state == "ABORT"),
        }
        if not inputs["i_rstn"]:
            return outputs
        self.release = ((self.release << 1) | 1) & 3
        if not released:
            return outputs
        if self.state == "IDLE":
            if outputs["o_start_ready"] and inputs["i_start_valid"]:
                self.metadata = pack_metadata(
                    inputs["i_start_epoch"], inputs["i_start_task_id"],
                    inputs["i_start_source_frame_id"], inputs["i_start_model_id"],
                    0, inputs["i_start_capture_ms"], 0)
                self.accepted_count = 0
                self.state = "RUN"
        elif self.state == "RUN":
            if run_failure:
                self.state = "ABORT"
            elif inputs["i_result_done"]:
                self.metadata |= (self.accepted_count << 128) | (inputs["i_now_ms"] << 201)
                self.state = "META"
            elif outputs["o_table_entry_valid"] and inputs["i_table_entry_ready"]:
                self.accepted_count += 1
        elif self.state == "META":
            if meta_failure:
                self.state = "ABORT"
            elif outputs["o_table_meta_valid"] and inputs["i_table_meta_ready"]:
                self.state = "WAIT_ACK"
        elif self.state == "WAIT_ACK":
            if inputs["i_table_copy_ack"]:
                self.accepted_count = 0
                self.state = "IDLE"
        elif self.state == "ABORT":
            self.accepted_count = 0
            self.state = "IDLE"
        else:
            raise AssertionError("illegal state")
        assert 0 <= self.accepted_count <= 64
        return outputs


def self_check():
    """Exercise transaction boundaries, not neural-network calculations."""
    checked = []
    trace = []

    def tick(model, case, **inputs):
        state = model.state
        outputs = model.step(**inputs)
        trace.append({"case": case, "state_before": state, "inputs": inputs,
                      "outputs": outputs, "state_after": model.state,
                      "accepted_after": model.accepted_count})
        return outputs

    def ready_model(case):
        model = Publisher()
        for _ in range(2):
            assert tick(model, case, i_start_valid=1)["o_start_ready"] == 0
        assert model.state == "IDLE"
        return model

    def started(case, count=0):
        model = ready_model(case)
        assert tick(model, case, i_start_valid=1, i_start_epoch=3,
                    i_start_task_id=17, i_start_source_frame_id=29,
                    i_start_model_id=41, i_start_capture_ms=100)["o_pipeline_start_valid"]
        for index in range(count):
            outputs = tick(model, case, i_entry_valid=1, i_entry=index + 1,
                           i_result_frame_token=17)
            assert outputs["o_table_entry_valid"] and outputs["o_entry_ready"]
        return model

    def expect_abort(model, case, **inputs):
        outputs = tick(model, case, **inputs)
        assert outputs["o_table_abort"] and not outputs["o_table_meta_valid"]
        assert not outputs["o_table_entry_valid"] and not outputs["o_entry_ready"]
        assert model.state == "ABORT"
        outputs = tick(model, case)
        assert outputs["o_pipeline_cancel"] and outputs["o_error"] and outputs["o_table_abort"]
        assert model.state == "IDLE" and model.accepted_count == 0
        assert not tick(model, case)["o_error"]
        checked.append(case)

    for count in (0, 1, 64):
        case = f"success_{count}"
        model = started(case, count)
        outputs = tick(model, case, i_result_done=1, i_result_frame_token=17,
                       i_result_count=count, i_now_ms=123)
        assert not outputs["o_table_meta_valid"] and model.state == "META"
        expected = pack_metadata(3, 17, 29, 41, count, 100, 123)
        for _ in range(19):
            outputs = tick(model, case, i_table_meta_ready=0, i_start_task_id=99, i_now_ms=999)
            assert outputs["o_table_meta_valid"] and outputs["o_table_metadata"] == expected
        assert tick(model, case)["o_table_meta_valid"] and model.state == "WAIT_ACK"
        for _ in range(3):
            outputs = tick(model, case, i_cancel=1, i_pipeline_fault=1, i_table_error=1,
                           i_entry_valid=1, i_start_valid=1)
            assert outputs["o_busy"] and not any(outputs[name] for name in (
                "o_table_abort", "o_pipeline_cancel", "o_start_ready", "o_table_meta_valid"))
            assert outputs["o_table_metadata"] == expected
        tick(model, case, i_table_copy_ack=1, i_cancel=1, i_pipeline_fault=1)
        assert model.state == "IDLE" and model.accepted_count == 0
        checked.append(case)

    for signal in ("i_cancel", "i_pipeline_fault", "i_table_error", "i_table_busy"):
        model = ready_model("start_block_" + signal)
        outputs = tick(model, "start_block_" + signal, i_start_valid=1, **{signal: 1})
        assert not outputs["o_pipeline_start_valid"] and model.state == "IDLE"
        checked.append("start_block_" + signal)
    for signal in ("i_pipeline_start_ready", "i_table_entry_ready"):
        model = ready_model("start_block_" + signal)
        outputs = tick(model, "start_block_" + signal, i_start_valid=1, **{signal: 0})
        assert not outputs["o_start_ready"] and model.state == "IDLE"
        assert outputs["o_pipeline_start_valid"] == int(signal == "i_pipeline_start_ready")
        checked.append("start_block_" + signal)

    model = started("entry_stall")
    for _ in range(29):
        outputs = tick(model, "entry_stall", i_entry_valid=1, i_entry=123456,
                       i_result_frame_token=17, i_table_entry_ready=0)
        assert outputs["o_table_entry_valid"] and outputs["o_table_entry"] == 123456
        assert not outputs["o_entry_ready"] and model.accepted_count == 0
    tick(model, "entry_stall", i_entry_valid=1, i_result_frame_token=17)
    assert model.accepted_count == 1
    checked.append("entry_stall")

    failures = {
        "entry_65": (64, {"i_entry_valid": 1, "i_result_frame_token": 17}),
        "entry_token": (1, {"i_entry_valid": 1, "i_result_frame_token": 18}),
        "done_with_entry": (1, {"i_entry_valid": 1, "i_result_done": 1, "i_result_frame_token": 17, "i_result_count": 1, "i_now_ms": 100}),
        "done_count": (1, {"i_result_done": 1, "i_result_frame_token": 17, "i_result_count": 0, "i_now_ms": 100}),
        "done_count_65": (64, {"i_result_done": 1, "i_result_frame_token": 17, "i_result_count": 65, "i_now_ms": 100}),
        "done_token": (1, {"i_result_done": 1, "i_result_frame_token": 18, "i_result_count": 1, "i_now_ms": 100}),
        "done_time": (1, {"i_result_done": 1, "i_result_frame_token": 17, "i_result_count": 1, "i_now_ms": 99}),
        "run_cancel": (1, {"i_cancel": 1, "i_entry_valid": 1, "i_result_frame_token": 17}),
        "run_fault": (1, {"i_pipeline_fault": 1, "i_entry_valid": 1, "i_result_frame_token": 17}),
        "run_table_error": (1, {"i_table_error": 1}),
        "done_cancel": (0, {"i_cancel": 1, "i_result_done": 1, "i_result_frame_token": 17, "i_now_ms": 100}),
    }
    for case, (count, inputs) in failures.items():
        expect_abort(started(case, count), case, **inputs)

    for signal in ("i_cancel", "i_pipeline_fault", "i_table_error", "i_entry_valid"):
        case = "meta_" + signal
        model = started(case)
        tick(model, case, i_result_done=1, i_result_frame_token=17, i_now_ms=100)
        expect_abort(model, case, i_table_meta_ready=1, **{signal: 1})

    model = started("fault_feedback")
    outputs = tick(model, "fault_feedback", i_pipeline_fault=1)
    assert outputs["o_table_abort"] and not outputs["o_pipeline_cancel"]
    assert tick(model, "fault_feedback")["o_pipeline_cancel"]
    checked.append("fault_feedback")

    model = ready_model("held_cancel")
    for _ in range(7):
        outputs = tick(model, "held_cancel", i_cancel=1, i_start_valid=1)
        assert outputs["o_pipeline_cancel"] and not outputs["o_start_ready"]
        assert not outputs["o_table_abort"] and model.state == "IDLE"
    checked.append("held_cancel")

    model = ready_model("consecutive_tokens")
    for task in (17, 88, 0xFFFFFFFF):
        outputs = tick(model, "consecutive_tokens", i_start_valid=1, i_start_task_id=task,
                       i_start_epoch=0xFFFFFFFF, i_start_source_frame_id=task,
                       i_start_model_id=0xFFFFFFFF, i_start_capture_ms=(1 << 64) - 1)
        assert outputs["o_pipeline_start_valid"] and model.state == "RUN"
        tick(model, "consecutive_tokens", i_result_done=1, i_result_frame_token=task,
             i_now_ms=(1 << 64) - 1)
        expected = pack_metadata(0xFFFFFFFF, task, task, 0xFFFFFFFF, 0,
                                 (1 << 64) - 1, (1 << 64) - 1)
        outputs = tick(model, "consecutive_tokens")
        assert outputs["o_table_metadata"] == expected and expected.bit_length() == 265
        assert ((expected >> 135) & 3) == 0 and model.state == "WAIT_ACK"
        tick(model, "consecutive_tokens", i_table_copy_ack=1)
        assert model.state == "IDLE"
    checked.append("consecutive_tokens")

    for phase in ("IDLE", "RUN", "META", "WAIT_ACK", "ABORT"):
        case = "reset_" + phase
        model = ready_model(case) if phase == "IDLE" else started(case, 1)
        if phase in ("META", "WAIT_ACK"):
            tick(model, case, i_result_done=1, i_result_frame_token=17, i_result_count=1, i_now_ms=100)
            if phase == "WAIT_ACK":
                tick(model, case)
        if phase == "ABORT":
            tick(model, case, i_pipeline_fault=1)
        assert model.state == phase
        outputs = tick(model, case, i_rstn=0, i_start_valid=1, i_entry_valid=1)
        assert not any(outputs[name] for name in ("o_start_ready", "o_pipeline_start_valid", "o_entry_ready", "o_table_entry_valid", "o_table_meta_valid", "o_table_abort", "o_pipeline_cancel", "o_busy", "o_error"))
        assert model.metadata == model.accepted_count == 0 and model.state == "IDLE"
        for _ in range(2):
            assert not tick(model, case, i_start_valid=1)["o_pipeline_start_valid"]
        assert tick(model, case, i_start_valid=1, i_start_task_id=88)["o_pipeline_start_valid"]
        checked.append(case)

    return {"status": "passed", "cases": checked, "case_count": len(checked),
            "cycles": len(trace), "trace": trace,
            "scope": "publisher cycle semantics only; no RTL/CDC/resource/timing/board claim"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path)
    arguments = parser.parse_args()
    result = self_check()
    if arguments.out_dir:
        arguments.out_dir.mkdir(parents=True, exist_ok=True)
        trace = result.pop("trace")
        (arguments.out_dir / "cycle_trace.json").write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")
        result["reference_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        (arguments.out_dir / "self_check_receipt.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "trace"}))
