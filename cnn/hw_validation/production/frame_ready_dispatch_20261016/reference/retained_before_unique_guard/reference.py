"""Two-slot frame dispatcher cycle model. step returns preedge outputs.

The only frame identity storage is contexts[0:2], indexed by physical slot.
Reset assertion is immediate; the caller supplies a synchronous reset release.
"""

import argparse
import hashlib
import json
from pathlib import Path


DEFAULTS = {
    "i_rstn": 1, "i_epoch": 3, "i_model_id": 41,
    "i_identity_valid": 0, "i_identity_payload": 0,
    "i_slot_free_mask": 3, "i_slot_ready_mask": 0,
    "i_slot_reading_mask": 0, "i_slot_quarantine_mask": 0,
    "i_slot_epochs": 0, "i_slot_frame_ids": 0, "i_slot_timestamps": 0,
    "i_claim_ready": 0, "i_job_ready": 0,
    "i_task_done": 0, "i_task_done_id": 0,
    "i_last_read_valid": 0, "i_last_read_slot": 0,
    "i_last_read_epoch": 0, "i_last_read_frame_id": 0,
}
WIDTHS = {
    **{name: 1 for name in DEFAULTS},
    **{name: 32 for name in ("i_epoch", "i_model_id", "i_task_done_id",
                            "i_last_read_epoch", "i_last_read_frame_id")},
    **{name: 2 for name in ("i_slot_free_mask", "i_slot_ready_mask",
                           "i_slot_reading_mask", "i_slot_quarantine_mask")},
    "i_identity_payload": 128, "i_slot_epochs": 64,
    "i_slot_frame_ids": 64, "i_slot_timestamps": 128,
}
BASES = (0x03400000, 0x03480000)


def identity(epoch, frame, capture):
    return (epoch << 96) | (frame << 64) | capture


def descriptor(slot, context, task, model):
    epoch = context >> 96
    frame = (context >> 64) & 0xFFFFFFFF
    capture = context & ((1 << 64) - 1)
    return (slot | (BASES[slot] << 1) | (epoch << 33) | (task << 65)
            | (frame << 97) | (model << 129) | (capture << 161))


class Dispatcher:
    """Bounded scheduler; no image memory, DMA queue or inferred last read."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.contexts = [None, None]
        self.state = "IDLE"
        self.selected = 0
        self.prefer = 0
        self.next_task = 1
        self.task = 0
        self.model = 0
        self.mismatch = 0
        self.done_seen = False
        self.released = False
        self.error = False
        self.wrap_fault = False

    def step(self, **updates):
        values = DEFAULTS | updates
        assert not (updates.keys() - DEFAULTS.keys()), "unknown input"
        for name, value in values.items():
            assert isinstance(value, int) and 0 <= value < (1 << WIDTHS[name]), name
        if not values["i_rstn"]:
            self.reset()
        epochs = [(values["i_slot_epochs"] >> (32 * slot)) & 0xFFFFFFFF for slot in range(2)]
        frames = [(values["i_slot_frame_ids"] >> (32 * slot)) & 0xFFFFFFFF for slot in range(2)]
        timestamps = [(values["i_slot_timestamps"] >> (64 * slot)) & ((1 << 64) - 1) for slot in range(2)]

        def mask(name, slot):
            return bool(values[name] & (1 << slot))

        def matches(slot, context):
            return context is not None and epochs[slot] == (context >> 96) and frames[slot] == ((context >> 64) & 0xFFFFFFFF)

        incoming = values["i_identity_payload"]
        incoming_epoch = incoming >> 96
        incoming_frame = (incoming >> 64) & 0xFFFFFFFF
        candidates = [slot for slot in range(2) if not mask("i_slot_free_mask", slot)
                      and not mask("i_slot_quarantine_mask", slot)
                      and epochs[slot] == incoming_epoch and frames[slot] == incoming_frame]
        identity_bad = incoming_epoch != values["i_epoch"] or len(candidates) != 1
        target = candidates[0] if len(candidates) == 1 else 0
        duplicate = not identity_bad and self.contexts[target] is not None and (self.contexts[target] >> 64) == (incoming >> 64)
        identity_ready = identity_bad or duplicate or self.contexts[target] is None
        context = self.contexts[self.selected]
        selected_match = matches(self.selected, context)
        preclaim_ok = selected_match and mask("i_slot_ready_mask", self.selected) and not any(
            mask(name, self.selected) for name in ("i_slot_free_mask", "i_slot_reading_mask", "i_slot_quarantine_mask"))
        owned_ok = selected_match and mask("i_slot_reading_mask", self.selected) and not any(
            mask(name, self.selected) for name in ("i_slot_free_mask", "i_slot_quarantine_mask"))
        last_ok = bool(self.state == "RUN" and not self.released and owned_ok
                       and values["i_last_read_slot"] == self.selected
                       and values["i_last_read_epoch"] == (context >> 96)
                       and values["i_last_read_frame_id"] == ((context >> 64) & 0xFFFFFFFF))
        active = bool(values["i_rstn"])
        outputs = {
            "o_identity_ready": int(active and self.state != "FAULT" and identity_ready),
            "o_claim_valid": int(active and self.state == "CLAIM" and preclaim_ok),
            "o_claim_slot": self.selected,
            "o_claim_epoch": (context >> 96) if context is not None else 0,
            "o_claim_frame_id": ((context >> 64) & 0xFFFFFFFF) if context is not None else 0,
            "o_job_valid": int(active and self.state == "JOB" and owned_ok),
            "o_job_descriptor": descriptor(self.selected, context or 0, self.task, self.model),
            "o_job_timestamp_mismatch": self.mismatch,
            "o_last_read_consumed": int(active and values["i_last_read_valid"] and last_ok),
            "o_release_slot": self.selected,
            "o_release_epoch": (context >> 96) if context is not None else 0,
            "o_release_frame_id": ((context >> 64) & 0xFFFFFFFF) if context is not None else 0,
            "o_busy": int(active and self.state != "IDLE"),
            "o_error": int(active and self.error),
            "o_task_wrap_fault": int(active and self.wrap_fault),
        }
        if not active:
            return outputs
        previous_contexts = self.contexts.copy()
        retire_before = self.done_seen and self.released
        if values["i_identity_valid"] and outputs["o_identity_ready"]:
            if identity_bad or duplicate:
                self.error = True
            else:
                self.contexts[target] = incoming
        if values["i_task_done"]:
            if self.state == "RUN" and values["i_task_done_id"] == self.task and not self.done_seen:
                self.done_seen = True
            else:
                self.error = True
        if values["i_last_read_valid"]:
            if last_ok:
                self.released = True
            else:
                self.error = True
        if self.state == "IDLE":
            eligible = []
            for slot in range(2):
                stored = previous_contexts[slot]
                if stored is not None and mask("i_slot_quarantine_mask", slot):
                    self.contexts[slot] = None
                    self.error = True
                elif matches(slot, stored) and mask("i_slot_ready_mask", slot) and not any(
                        mask(name, slot) for name in ("i_slot_free_mask", "i_slot_reading_mask", "i_slot_quarantine_mask")):
                    eligible.append(slot)
            if eligible and not self.wrap_fault:
                self.selected = self.prefer if self.prefer in eligible else eligible[0]
                self.prefer = 1 - self.selected
                self.task = self.next_task
                self.model = values["i_model_id"]
                self.mismatch = int(timestamps[self.selected] != (previous_contexts[self.selected] & ((1 << 64) - 1)))
                self.done_seen = False
                self.released = False
                self.state = "CLAIM"
        elif self.state == "CLAIM":
            if not preclaim_ok:
                self.contexts[self.selected] = None
                self.error = True
                self.state = "IDLE"
            elif outputs["o_claim_valid"] and values["i_claim_ready"]:
                self.state = "JOB"
        elif self.state == "JOB":
            if not owned_ok:
                self.error = True
                self.state = "FAULT"
            elif outputs["o_job_valid"] and values["i_job_ready"]:
                if self.next_task == 0xFFFFFFFF:
                    self.wrap_fault = True
                else:
                    self.next_task += 1
                self.state = "RUN"
        elif self.state == "RUN":
            # A released input may be recaptured while the old task still runs.
            if not self.released and not owned_ok:
                self.error = True
                self.state = "FAULT"
            elif retire_before:
                self.contexts[self.selected] = None
                self.state = "IDLE"
        return outputs


def self_check():
    """Runnable protocol scenarios with explicit external slot lifecycle facts."""
    trace = []
    cases = []

    def tick(model, case, environment, **updates):
        inputs = DEFAULTS | environment | updates
        before = model.state
        outputs = model.step(**inputs)
        trace.append({"case": case, "inputs": inputs, "outputs": outputs,
                      "state_before": before, "state_after": model.state,
                      "contexts_after": model.contexts.copy(), "next_task_after": model.next_task,
                      "task_after": model.task, "done_after": model.done_seen,
                      "released_after": model.released})
        return outputs

    def environment():
        return {"i_slot_free_mask": 0, "i_slot_ready_mask": 0,
                "i_slot_reading_mask": 0, "i_slot_quarantine_mask": 0,
                "i_slot_epochs": 3 | (3 << 32), "i_slot_frame_ids": 10 | (11 << 32),
                "i_slot_timestamps": 91 | (110 << 64)}

    def running(case, selected=0):
        model, env = Dispatcher(), environment()
        env["i_slot_ready_mask"] = 1 << selected
        context = identity(3, 10 + selected, 100 + selected * 10)
        assert tick(model, case, env, i_identity_valid=1, i_identity_payload=context)["o_identity_ready"]
        tick(model, case, env)
        assert model.state == "CLAIM" and model.selected == selected
        assert tick(model, case, env, i_claim_ready=1)["o_claim_valid"]
        assert model.state == "JOB" and model.next_task == 1
        env["i_slot_ready_mask"] = 0
        env["i_slot_reading_mask"] = 1 << selected
        outputs = tick(model, case, env, i_job_ready=1)
        assert outputs["o_job_valid"] and model.state == "RUN" and model.next_task == 2
        assert outputs["o_job_descriptor"] == descriptor(selected, context, 1, 41)
        assert outputs["o_job_timestamp_mismatch"] == int(selected == 0)
        return model, env

    def last_inputs(model):
        return {"i_last_read_valid": 1, "i_last_read_slot": model.selected,
                "i_last_read_epoch": 3, "i_last_read_frame_id": 10 + model.selected}

    for ordering in ("done_first", "last_first", "simultaneous"):
        model, env = running(ordering)
        if ordering == "done_first":
            outputs = tick(model, ordering, env, i_task_done=1, i_task_done_id=1)
            assert not outputs["o_last_read_consumed"] and not model.released
            for _ in range(4):
                tick(model, ordering, env)
                assert model.state == "RUN" and model.contexts[0] is not None
            assert tick(model, ordering, env, **last_inputs(model))["o_last_read_consumed"]
        elif ordering == "last_first":
            assert tick(model, ordering, env, **last_inputs(model))["o_last_read_consumed"]
            env["i_slot_reading_mask"] = 0
            env["i_slot_free_mask"] = 1
            for _ in range(4):
                tick(model, ordering, env)
                assert model.state == "RUN" and not model.error
            tick(model, ordering, env, i_task_done=1, i_task_done_id=1)
        else:
            assert tick(model, ordering, env, i_task_done=1, i_task_done_id=1,
                        **last_inputs(model))["o_last_read_consumed"]
        assert model.state == "RUN" and model.done_seen and model.released
        tick(model, ordering, env)
        assert model.state == "IDLE" and model.contexts[0] is None
        cases.append(ordering)

    for ready_first in (False, True):
        case = "ready_first" if ready_first else "identity_first"
        model, env = Dispatcher(), environment()
        env["i_slot_ready_mask"] = int(ready_first)
        if ready_first:
            tick(model, case, env)
            assert model.state == "IDLE"
        tick(model, case, env, i_identity_valid=1, i_identity_payload=identity(3, 10, 100))
        for _ in range(8):
            if not ready_first:
                assert not tick(model, case, env)["o_job_valid"] and model.state == "IDLE"
        env["i_slot_ready_mask"] = 1
        tick(model, case, env)
        assert model.state == "CLAIM"
        cases.append(case)

    model, env = Dispatcher(), environment()
    for slot in (0, 1):
        tick(model, "ready_bypass_roundrobin", env, i_identity_valid=1,
             i_identity_payload=identity(3, 10 + slot, 100 + 10 * slot))
    env["i_slot_ready_mask"] = 2
    tick(model, "ready_bypass_roundrobin", env)
    assert model.selected == 1 and model.contexts[0] is not None
    cases.append("ready_bypass_roundrobin")

    for wrong in ("epoch", "frame", "ambiguous", "duplicate", "duplicate_capture"):
        case = "identity_" + wrong
        model, env = Dispatcher(), environment()
        good = identity(3, 10, 100)
        tick(model, case, env, i_identity_valid=1, i_identity_payload=good)
        incoming = good
        if wrong == "epoch":
            incoming = identity(4, 10, 100)
        elif wrong == "frame":
            incoming = identity(3, 99, 100)
        elif wrong == "ambiguous":
            env["i_slot_frame_ids"] = 10 | (10 << 32)
        elif wrong == "duplicate_capture":
            incoming = identity(3, 10, 101)
        outputs = tick(model, case, env, i_identity_valid=1, i_identity_payload=incoming)
        assert outputs["o_identity_ready"] and model.error and model.contexts[0] == good
        assert model.state == "IDLE" and not outputs["o_claim_valid"]
        cases.append(case)

    model, env = Dispatcher(), environment()
    case = "claim_job_stalls"
    env["i_slot_ready_mask"] = 1
    tick(model, case, env, i_identity_valid=1, i_identity_payload=identity(3, 10, 100))
    tick(model, case, env)
    for _ in range(11):
        outputs = tick(model, case, env)
        assert outputs["o_claim_valid"] and model.state == "CLAIM" and model.next_task == 1
    tick(model, case, env, i_claim_ready=1)
    env["i_slot_ready_mask"], env["i_slot_reading_mask"] = 0, 1
    expected = descriptor(0, identity(3, 10, 100), 1, 41)
    for _ in range(13):
        outputs = tick(model, case, env)
        assert outputs["o_job_valid"] and outputs["o_job_descriptor"] == expected
        assert outputs["o_job_timestamp_mismatch"] and model.next_task == 1
    tick(model, case, env, i_job_ready=1, i_task_done=1, i_task_done_id=1, **last_inputs(model))
    assert model.state == "RUN" and model.error and not model.done_seen and not model.released
    cases.append(case)

    for violation in ("early_last", "wrong_slot", "wrong_epoch", "wrong_frame", "wrong_done", "duplicate_done", "duplicate_last"):
        case = violation
        model, env = running(case)
        event = last_inputs(model)
        if violation == "early_last":
            model = Dispatcher()
            env = environment()
        elif violation == "wrong_slot":
            event["i_last_read_slot"] = 1
        elif violation == "wrong_epoch":
            event["i_last_read_epoch"] = 4
        elif violation == "wrong_frame":
            event["i_last_read_frame_id"] = 11
        elif violation == "wrong_done":
            event = {"i_task_done": 1, "i_task_done_id": 2}
        elif violation == "duplicate_done":
            event = {"i_task_done": 1, "i_task_done_id": 1}
            tick(model, case, env, **event)
        elif violation == "duplicate_last":
            tick(model, case, env, **event)
        outputs = tick(model, case, env, **event)
        assert model.error and not outputs["o_last_read_consumed"]
        cases.append(case)

    model, env = running("recapture_backpressure")
    tick(model, "recapture_backpressure", env, **last_inputs(model))
    env["i_slot_reading_mask"] = 0
    env["i_slot_frame_ids"] = 20 | (11 << 32)
    newer = identity(3, 20, 200)
    for _ in range(9):
        outputs = tick(model, "recapture_backpressure", env, i_identity_valid=1, i_identity_payload=newer)
        assert not outputs["o_identity_ready"] and model.contexts[0] == identity(3, 10, 100)
        assert not model.error
    tick(model, "recapture_backpressure", env, i_task_done=1, i_task_done_id=1)
    outputs = tick(model, "recapture_backpressure", env, i_identity_valid=1, i_identity_payload=newer)
    assert not outputs["o_identity_ready"] and model.state == "IDLE"
    assert tick(model, "recapture_backpressure", env, i_identity_valid=1, i_identity_payload=newer)["o_identity_ready"]
    assert model.contexts[0] == newer
    cases.append("recapture_backpressure")

    for stage in ("CLAIM", "JOB", "RUN"):
        for violation in ("quarantine", "free", "identity"):
            case = stage + "_guard_" + violation
            model, env = running(case)
            if stage != "RUN":
                model.state = stage
                if stage == "CLAIM":
                    env["i_slot_reading_mask"], env["i_slot_ready_mask"] = 0, 1
            if violation == "quarantine":
                env["i_slot_quarantine_mask"] = 1
            elif violation == "free":
                env["i_slot_free_mask"] = 1
                env["i_slot_reading_mask"] = 0
                env["i_slot_ready_mask"] = 0
            else:
                env["i_slot_frame_ids"] = 99 | (11 << 32)
            outputs = tick(model, case, env, i_claim_ready=1, i_job_ready=1, **last_inputs(model))
            assert not outputs["o_claim_valid"] and not outputs["o_job_valid"] and not outputs["o_last_read_consumed"]
            assert model.error and model.state == ("IDLE" if stage == "CLAIM" else "FAULT")
            if stage != "CLAIM":
                outputs = tick(model, case, environment(), i_job_ready=1, i_task_done=1, i_task_done_id=1,
                               i_identity_valid=1, i_identity_payload=identity(3, 11, 110))
                assert not outputs["o_identity_ready"] and model.contexts[1] is None
                assert model.state == "FAULT" and model.contexts[0] is not None
            cases.append(case)

    model, env = running("task_wrap")
    model.state, model.next_task, model.task = "JOB", 0xFFFFFFFF, 0xFFFFFFFF
    outputs = tick(model, "task_wrap", env, i_job_ready=1)
    assert outputs["o_job_valid"] and model.wrap_fault and model.next_task == 0xFFFFFFFF
    assert ((outputs["o_job_descriptor"] >> 65) & 0xFFFFFFFF) == 0xFFFFFFFF
    tick(model, "task_wrap", env, i_task_done=1, i_task_done_id=0xFFFFFFFF, **last_inputs(model))
    tick(model, "task_wrap", env)
    env["i_slot_reading_mask"], env["i_slot_ready_mask"] = 0, 2
    tick(model, "task_wrap", env, i_identity_valid=1, i_identity_payload=identity(3, 11, 110))
    for _ in range(3):
        outputs = tick(model, "task_wrap", env, i_claim_ready=1, i_job_ready=1)
        assert not outputs["o_claim_valid"] and not outputs["o_job_valid"] and model.state == "IDLE"
    cases.append("task_wrap")

    for stage in ("IDLE", "CLAIM", "JOB", "RUN", "FAULT"):
        case = "reset_" + stage
        model, env = running(case)
        model.state = stage
        outputs = tick(model, case, env, i_rstn=0, i_job_ready=1, i_claim_ready=1, **last_inputs(model))
        assert not any(outputs[name] for name in ("o_identity_ready", "o_claim_valid", "o_job_valid", "o_last_read_consumed", "o_busy", "o_error", "o_task_wrap_fault"))
        assert model.contexts == [None, None] and model.next_task == 1 and model.state == "IDLE"
        cases.append(case)
    return {"status": "PASS", "case_count": len(cases), "cases": cases,
            "cycles": len(trace), "trace": trace,
            "scope": "controlled single-domain dispatcher semantics; not actual slots/DDR/CDC/NN/display evidence"}


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
