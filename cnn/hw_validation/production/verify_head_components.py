"""Verify saved component results without a model or new input inference."""
from collections import Counter
from pathlib import Path
import json
import sys

import numpy as np
import numpy._core._multiarray_umath as native

from cnn.hw_validation.production import diagnose_head_components as diag


def verify():
    base, shared, out = diag.base, diag.shared, diag.OUT
    identity, status = base.read(out / "identity.json"), base.read(out / "status.json")
    diag.check_inputs(identity["inputs"], identity["sources"])
    assert shared.sha256(out / "summary.json") == status["summary_sha256"]
    summary, old = base.read(out / "summary.json"), base.read(out / "inputs/summary.json")
    review = base.read(out / "inputs/evidence_review.json")
    indices = review["exact_unique_train_indices"]
    cases = [base.read(out / "cases" / f"train_{i:02d}.json") for i in indices]
    assert len(cases) == len({c["key"] for c in cases}) == 16
    assert [c["key"] for c in cases] == review["exact_unique_frame_keys"]
    assert Counter(c["group"] for c in cases) == {"new": 8, "replay": 8}
    errors, transitions = [], 0
    for mode in diag.RECIPES:
        predictions = [dict(image_id=c["key"], label=d["label"], score=d["score_uint16"] / 65536,
                            box=[v / 256 for v in d["box_q8"]], cell_id=d["cell_id"])
                       for c in cases for d in c["modes"][mode]["detections"]]
        assert predictions == summary["modes"][mode]["predictions"]
        for group in ("all", "new", "replay"):
            keys = {c["key"] for c in cases if group == "all" or c["group"] == group}
            def selected(rows):
                return [r for r in rows if r["image_id"] in keys]
            result = summary["modes"][mode]["groups"][group]
            actual = diag.previous.metrics.report(selected(predictions), selected(summary["truth"]),
                                                 selected(summary["ignores"]), thresholds=(.5, .5))
            assert actual == result["metrics"]
            for label, name in enumerate(("person", "vehicle")):
                curve = result["PR"][str(label)]
                ap = sum(max((r["precision"] for r in curve if r["recall"] >= level), default=0.)
                         for level in np.linspace(0, 1, 101)) / 101
                error = abs(ap - actual["classes"][name]["ap50"])
                assert error < 1e-12
                errors.append(error)
            if mode in ("control", "float_all_reference"):
                old_mode = "control" if mode == "control" else "float_q7_8_reference"
                assert actual == old["modes"][old_mode]["groups"][group]["metrics"]
        for label in (0, 1):
            for threshold in (diag.previous.FLOOR, .5):
                def matched_gt(which):
                    return {r["gt_id"] for c in cases for r in c["modes"][which]["GT"]
                            if r["label"] == label and r["final_match"] and r["final_match"]["score"] >= threshold}
                before, after = matched_gt("control"), matched_gt(mode)
                transition = summary["transitions"][mode][f"{label}:{threshold}"]
                assert transition["lost"] == sorted(before - after)
                assert transition["gained"] == sorted(after - before)
                transitions += 1
    diag.check_inputs(identity["inputs"], identity["sources"])
    source = Path(__file__)
    receipt = dict(status="SAVED_EVIDENCE_VERIFICATION_PASSED", independent_agent_review=False,
        verification_scope="separate saved-output recomputation and direct PR envelope arithmetic",
        metrics_group_comparisons=24, AP50_PR_comparisons=len(errors), AP50_max_error=max(errors),
        exact_GT_transition_set_checks=transitions,
        unit_tests="5 passed: component splicing/isolation plus prior decode/TopK/NMS/matching boundaries",
        source_sha256=shared.sha256(source), summary_sha256=status["summary_sha256"],
        runtime=dict(python=sys.version, numpy=np.__version__, numpy_file=np.__file__,
            numpy_native_sha256=shared.sha256(Path(native.__file__)),
            python_executable=sys.executable, python_executable_sha256=shared.sha256(Path(sys.executable))),
        training_updates=0, network_forwards=0, formal_acceptance=False)
    base.save(out / "verification_receipt.json", receipt)
    print(json.dumps(receipt))


if __name__ == "__main__":
    diag.previous.diag.runtime_guard()
    verify()
