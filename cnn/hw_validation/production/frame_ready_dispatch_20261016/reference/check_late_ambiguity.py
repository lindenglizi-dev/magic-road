"""Run the same late-native-key negative cases against retained and repaired models."""

import hashlib
import importlib.util
import json
from pathlib import Path


def load_model(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probe(module, stage):
    model = module.Dispatcher()
    environment = {"i_slot_free_mask": 0, "i_slot_ready_mask": 0,
                   "i_slot_reading_mask": 0, "i_slot_quarantine_mask": 0,
                   "i_slot_epochs": 3 | (3 << 32), "i_slot_frame_ids": 10 | (11 << 32),
                   "i_slot_timestamps": 100 | (110 << 64)}
    model.step(**environment, i_identity_valid=1, i_identity_payload=module.identity(3, 10, 100))
    environment["i_slot_ready_mask"] = 1
    if stage != "IDLE":
        model.step(**environment)
    if stage in ("JOB", "RUN"):
        model.step(**environment, i_claim_ready=1)
        environment["i_slot_ready_mask"], environment["i_slot_reading_mask"] = 0, 1
    if stage == "RUN":
        model.step(**environment, i_job_ready=1)
    assert model.state == stage
    environment["i_slot_frame_ids"] = 10 | (10 << 32)
    events = {"i_last_read_valid": 1, "i_last_read_slot": 0,
              "i_last_read_epoch": 3, "i_last_read_frame_id": 10} if stage == "RUN" else {}
    outputs = model.step(**environment, i_claim_ready=1, i_job_ready=1, **events)
    expected_state = "IDLE" if stage in ("IDLE", "CLAIM") else "FAULT"
    passed = (not outputs["o_claim_valid"] and not outputs["o_job_valid"]
              and not outputs["o_last_read_consumed"] and model.error
              and model.state == expected_state)
    return {"stage": stage, "requirement_passed": passed, "outputs": outputs,
            "actual_state_after": model.state, "expected_state_after": expected_state,
            "actual_error_after": model.error,
            "inputs": module.DEFAULTS | environment | {"i_claim_ready": 1, "i_job_ready": 1} | events}


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    before_path = directory / "retained_before_unique_guard" / "reference.py"
    after_path = directory.parent / "reference.py"
    before = load_model(before_path, "dispatcher_before_guard")
    after = load_model(after_path, "dispatcher_after_guard")
    stages = ("IDLE", "CLAIM", "JOB", "RUN")
    result = {"scope": "same four late duplicate native-key cases; no incoming identity event",
              "before": [probe(before, stage) for stage in stages],
              "after": [probe(after, stage) for stage in stages],
              "sha256": {"before_reference": hashlib.sha256(before_path.read_bytes()).hexdigest(),
                         "after_reference": hashlib.sha256(after_path.read_bytes()).hexdigest()}}
    result["before_requirement_failures"] = sum(not item["requirement_passed"] for item in result["before"])
    result["after_requirement_failures"] = sum(not item["requirement_passed"] for item in result["after"])
    (directory / "late_ambiguity_regression.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    assert result["before_requirement_failures"] == 4
    assert result["after_requirement_failures"] == 0
    print(json.dumps({name: result[name] for name in ("before_requirement_failures", "after_requirement_failures", "sha256")}))
