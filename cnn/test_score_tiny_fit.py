"""Pure fail-closed checks for tiny-fit candidate metadata."""
import copy
import json

from .score_tiny_fit import CONTRACT, ARCHITECTURE_SHA, validate_candidate
from .train import CLASS_CONTRACT


def main():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    good = dict(format="road-yolo-checkpoint-v2", phase="supervised",
        checkpoint_kind="diagnostic", interrupted=False, epoch=2, trained_steps=12,
        architecture_hash=ARCHITECTURE_SHA, class_contract=CLASS_CONTRACT,
        dataset_sha256=contract["dataset_sha256"],
        dataset_content_sha256=contract["dataset_content_sha256"],
        training_protocol=contract["protocol"],
        training_protocol_sha256=contract["protocol_sha256"], model={"weight": object()})
    validate_candidate(good, contract)
    cases = {
        "format": "road-yolo-resume-v3", "phase": "distill",
        "checkpoint_kind": "training", "interrupted": True,
        "architecture_hash": "0" * 64, "class_contract": {"0": "vehicle"},
        "dataset_sha256": "1" * 64, "dataset_content_sha256": "2" * 64,
        "training_protocol": {}, "training_protocol_sha256": "3" * 64,
        "trained_steps": 11,
    }
    for field, value in cases.items():
        bad = copy.deepcopy(good)
        bad[field] = value
        try:
            validate_candidate(bad, contract)
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe candidate accepted: {field}")
    for epoch, steps in ((-1, 0), (75, 304), (True, 8), (0, True)):
        bad = copy.deepcopy(good)
        bad.update(epoch=epoch, trained_steps=steps)
        try:
            validate_candidate(bad, contract)
        except ValueError:
            pass
        else:
            raise AssertionError(f"partial/out-of-bound candidate accepted: {epoch=}, {steps=}")
    changed_contract = copy.deepcopy(contract)
    changed_contract["dataset_sha256"] = "4" * 64
    try:
        validate_candidate(good, changed_contract)
    except ValueError:
        pass
    else:
        raise AssertionError("changed tiny-fit contract accepted")
    print("PASS tiny-fit candidate metadata fail-closed validation")


if __name__ == "__main__":
    main()
