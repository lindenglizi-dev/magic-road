"""Read saved train16 evidence only; bind all modes and summarize GT churn."""
from collections import Counter
from pathlib import Path
import json
import numpy as np

from cnn.hw_validation.production import diagnose_score_boxes as diag


def review():
    base, shared, out = diag.base, diag.shared, diag.OUT
    identity = base.read(out / "identity.json")
    shared.check_identity(identity)
    summary, status = base.read(out / "summary.json"), base.read(out / "status.json")
    assert shared.sha256(out / "summary.json") == status["summary_sha256"]
    selection = base.read(diag.diag.OUT / "selection.json")["samples"]
    indices = [row["train_index"] for row in selection]
    assert len(indices) == len(set(indices)) == 16
    cases = [base.read(out / "cases" / f"train_{i:02d}.json") for i in indices]
    assert len({row["key"] for row in cases}) == 16
    assert [row["train_index"] for row in cases] == indices
    assert len(summary["truth"]) == 397
    assert Counter(row["group"] for row in cases) == {"new": 8, "replay": 8}
    actual = {row["key"]: row for row in cases}
    artifacts, changes = {}, {}
    for case in cases:
        for mode in diag.MODES:
            path = out / "heads" / f"train_{case['train_index']:02d}_{mode}.npz"
            artifacts[str(path.relative_to(out))] = shared.sha256(path)
            with np.load(path, allow_pickle=False) as archive:
                heads = [archive[f"arr_{i}"] for i in range(3)]
                assert diag.integer.postprocess(heads, (3276, 3276)) == case["modes"][mode]["detections"]
        artifacts[f"cases/train_{case['train_index']:02d}.json"] = shared.sha256(
            out / "cases" / f"train_{case['train_index']:02d}.json")
    for mode in ("uniform_half", "keep_stem"):
        changes[mode] = {}
        for label in (0, 1):
            rows = []
            for direction in ("lost", "gained"):
                for gt_id in summary["differences"][mode]["0.5"][direction]:
                    key = gt_id.split("#gt")[0]
                    case = actual[key]
                    before = next(r for r in case["modes"]["control"]["GT"] if r["gt_id"] == gt_id)
                    after = next(r for r in case["modes"][mode]["GT"] if r["gt_id"] == gt_id)
                    if before["label"] != label:
                        continue
                    rows.append(dict(gt_id=gt_id, direction=direction,
                        control_final_score=(before["final_match"] or {}).get("score"),
                        experiment_final_score=(after["final_match"] or {}).get("score"),
                        experiment_reason=after["diagnostic_reason"],
                        experiment_best_raw_geometry_IoU=after["best_raw_geometry_IoU"],
                        experiment_best_IoU50_score_uint16=after["highest_score_IoU50_uint16"]))
            changes[mode][str(label)] = dict(rows=rows,
                lost_reasons=dict(Counter(r["experiment_reason"] for r in rows if r["direction"] == "lost")),
                lost=sum(r["direction"] == "lost" for r in rows),
                gained=sum(r["direction"] == "gained" for r in rows))
    shared.check_identity(identity)
    result = dict(experiment_id=out.name, modes=diag.MODES,
        inherited_identity_note="identity.json binds shared uniform-half inputs; this supplement binds the four-mode diagnosis without overwriting it",
        control_scale_sha256=shared.protocol_hash(base.read(base.BASE / "package/manifest.json")["scales"]),
        uniform_scale_sha256=identity["half_scales_sha256"],
        keep_stem_scale_sha256=base.read(diag.keep.OUT / "identity.json")["half_scales_sha256"],
        float_reference_recipe="original folded FP32 forward; float64(head)*256; numpy.rint; clip[-32768,32767]; INT16; same integer postprocess",
        reference_recipe_sha256=shared.protocol_hash({"head_scale": 1 / 256, "round": "nearest_even",
            "min": -32768, "max": 32767, "checkpoint": base.CHECKPOINT_HASH}),
        float_head_saturations=sum(sum(c["float_reference_head_saturation"]) for c in cases),
        exact_unique_train_indices=indices, exact_unique_frame_keys=[c["key"] for c in cases],
        groups={"new": 8, "replay": 8}, GT_counts={"person": 291, "vehicle": 106},
        saved_head_postprocess_parity_comparisons=64, artifacts=artifacts,
        GT_changes=changes, summary_sha256=status["summary_sha256"],
        reviewer_source_sha256=shared.sha256(Path(__file__)),
        metric_note="use ap50/ap50_95 for floor-truncated AP; the generic ap field is threshold-.5 AP",
        formal_acceptance=False, training_updates=0)
    base.save(out / "evidence_review.json", result)
    print(json.dumps({"exact_unique_frames": 16, "saved_heads_parity": 64,
        "float_head_saturations": result["float_head_saturations"],
        "vehicle_changes": {m: {k: v for k, v in changes[m]["1"].items() if k != "rows"}
                            for m in changes}}))


if __name__ == "__main__":
    diag.diag.runtime_guard()
    review()
