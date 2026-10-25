"""Saved-head counterfactuals only: no network forward, training or deployment."""
from collections import Counter
from pathlib import Path
import json
import shutil
import time

import numpy as np

from cnn.hw_validation.production import diagnose_score_boxes as previous

base, shared = previous.base, previous.shared
OUT = base.PROJECT / "cnn/reports/head_component_diagnosis16_20261014_v1"
PRIOR_REVIEW_SHA = "4bc61aed187852795ae675854797635259819c1d3fedcf2064b36f217586c904"
PRIOR_SUMMARY_SHA = "3bbacf27e0a0e2b4024152cdfe40b8e860d698da75c90427ef21dc113541a0b8"
RECIPES = {"control": (), "float_objectness": (4,), "float_person": (5,),
           "float_vehicle": (6,), "float_classes": (5, 6),
           "float_scores": (4, 5, 6), "float_boxes": (0, 1, 2, 3),
           "float_all_reference": tuple(range(7))}


def splice(control, reference, channels):
    if len(control) != 3 or len(reference) != 3 or tuple(channels) not in RECIPES.values():
        raise ValueError("not a frozen component recipe")
    result = []
    for source, ideal, stride in zip(control, reference, (4, 8, 16), strict=True):
        shape = (288 // stride, 512 // stride, 7)
        if source.shape != shape or ideal.shape != shape or source.dtype != np.int16 or ideal.dtype != np.int16:
            raise ValueError("head shape/dtype mismatch")
        output = source.copy()
        output[..., channels] = ideal[..., channels]
        result.append(output)
    return result


def load_heads(root, index, mode):
    with np.load(root / "heads" / f"train_{index:02d}_{mode}.npz", allow_pickle=False) as archive:
        if set(archive.files) != {"arr_0", "arr_1", "arr_2"}:
            raise ValueError("head archive fields changed")
        return [archive[f"arr_{i}"].copy() for i in range(3)]


def check_inputs(inputs, sources):
    for path, digest in {**inputs, **sources}.items():
        if shared.sha256(Path(path)) != digest:
            raise ValueError(f"input/source changed: {path}")


def run():
    started, prior = time.perf_counter(), previous.OUT
    review_path, summary_path = prior / "evidence_review.json", prior / "summary.json"
    if shared.sha256(review_path) != PRIOR_REVIEW_SHA or shared.sha256(summary_path) != PRIOR_SUMMARY_SHA:
        raise ValueError("prior frozen diagnosis identity changed")
    review, old = base.read(review_path), base.read(summary_path)
    indices = review["exact_unique_train_indices"]
    if len(indices) != len(set(indices)) or len(indices) != 16:
        raise ValueError("not the frozen 16 unique samples")
    inputs = {str(prior / name): digest for name, digest in review["artifacts"].items()}
    inputs.update({str(review_path): PRIOR_REVIEW_SHA, str(summary_path): PRIOR_SUMMARY_SHA})
    old_sources = base.read(prior / "identity.json")["sources"]
    sources = {str(base.PROJECT / name): digest for name, digest in old_sources.items()}
    for path in (Path(__file__), Path(__file__).with_name("test_diagnose_head_components.py")):
        sources[str(path)] = shared.sha256(path)
    check_inputs(inputs, sources)
    OUT.mkdir(parents=True, exist_ok=False)
    for folder in ("sources", "inputs", "cases"):
        (OUT / folder).mkdir()
    for path in sources:
        target = OUT / "sources" / Path(path).relative_to(base.PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    # Only consumed saved heads/cases are copied, not model/cache/image datasets.
    for index in indices:
        for mode in ("control", "float_q7_8_reference"):
            name = f"heads/train_{index:02d}_{mode}.npz"
            (OUT / "inputs/heads").mkdir(exist_ok=True)
            shutil.copyfile(prior / name, OUT / "inputs" / name)
        name = f"cases/train_{index:02d}.json"
        (OUT / "inputs/cases").mkdir(exist_ok=True)
        shutil.copyfile(prior / name, OUT / "inputs" / name)
    for name in ("evidence_review.json", "summary.json"):
        shutil.copyfile(prior / name, OUT / "inputs" / name)
    base.save(OUT / "identity.json", dict(experiment_id=OUT.name, inputs=inputs, sources=sources,
        prior_summary_sha256=PRIOR_SUMMARY_SHA, recipes=RECIPES,
        reference="original folded FP32 heads already rounded/clipped to Q7.8; same grid cell correspondence"))
    base.save(OUT / "contract.json", dict(recipes=RECIPES, training_updates=0, network_forwards=0,
        input_scope="fixed train16 saved heads only", threshold=.5, floor_uint16=3276,
        TopK=128, max_boxes_per_class=32, NMS="strict IoU>.5", GT_match="official IoU>=.5",
        threshold_selection=False, formal_acceptance=False, deployment_candidate=False,
        interpretation="ideal component counterfactual, not additive causality or attainable accuracy",
        stops="no further data, scale tuning, QAT, export or RTL changes"))
    all_predictions = {mode: [] for mode in RECIPES}
    all_GT = {mode: [] for mode in RECIPES}
    truth, ignores, domains = [], [], {}
    parity_checks = Counter()
    for index in indices:
        case = base.read(OUT / "inputs/cases" / f"train_{index:02d}.json")
        key = case["key"]
        if key in domains or key != review["exact_unique_frame_keys"][len(domains)]:
            raise ValueError("duplicate/reordered sample")
        domains[key] = case["group"]
        truth.extend(case["truth"])
        ignores.extend(case["ignores"])
        control = load_heads(OUT / "inputs", index, "control")
        reference = load_heads(OUT / "inputs", index, "float_q7_8_reference")
        output = dict(key=key, train_index=index, group=case["group"], modes={})
        baseline = None
        for mode, channels in RECIPES.items():
            heads = splice(control, reference, channels)
            boxes, scores, positive, stages, detections = previous.stages(heads)
            if mode == "control":
                baseline = (boxes, scores, stages, detections)
            if mode in ("control", "float_all_reference"):
                old_mode = "control" if mode == "control" else "float_q7_8_reference"
                if detections != case["modes"][old_mode]["detections"]:
                    raise AssertionError("counterfactual endpoint differs from prior evidence")
                parity_checks["endpoints"] += 1
            if mode in ("float_person", "float_vehicle"):
                unchanged_label = 1 if mode == "float_person" else 0
                if [d for d in detections if d["label"] == unchanged_label] != [d for d in baseline[3] if d["label"] == unchanged_label]:
                    raise AssertionError("class-specific swap changed the other class")
                parity_checks["other_class_unchanged"] += 1
            if mode == "float_boxes":
                np.testing.assert_array_equal(scores, baseline[1])
                for label in (0, 1):
                    for stage in ("floor", "top128"):
                        if stages[label][stage] != baseline[2][label][stage]:
                            raise AssertionError("box-only swap changed score/TopK")
                parity_checks["box_swap_score_topK_unchanged"] += 1
            elif mode != "float_all_reference":
                np.testing.assert_array_equal(boxes, baseline[0])
                parity_checks["score_swap_geometry_unchanged"] += 1
            predictions = [dict(image_id=key, label=d["label"], score=d["score_uint16"] / 65536,
                box=[v / 256 for v in d["box_q8"]], cell_id=d["cell_id"]) for d in detections]
            matches = sum((previous.match_trace(predictions, case["truth"], case["ignores"], label)[0]
                           for label in (0, 1)), [])
            details = previous.inspect_gt(boxes, scores, positive, stages, case["truth"], matches)
            output["modes"][mode] = dict(detections=detections, stages=stages, GT=details)
            all_predictions[mode].extend(predictions)
            all_GT[mode].extend(details)
        base.save(OUT / "cases" / f"train_{index:02d}.json", output)
        print(json.dumps(dict(completed=len(domains), key=key)), flush=True)
    if truth != old["truth"] or ignores != old["ignores"] or Counter(domains.values()) != {"new": 8, "replay": 8}:
        raise AssertionError("GT/ignore/order/domain differs from prior diagnosis")
    summary = dict(images=16, truth=truth, ignores=ignores, modes={}, transitions={})
    for mode in RECIPES:
        groups = {}
        for group in ("all", "new", "replay"):
            def selected(rows):
                return [r for r in rows if group == "all" or domains[r["image_id"]] == group]
            p, t, ig = selected(all_predictions[mode]), selected(truth), selected(ignores)
            groups[group] = dict(metrics=previous.metrics.report(p, t, ig, thresholds=(.5, .5)),
                floor={str(label): previous.metrics.evaluate(p, t, ig, label=label, threshold=previous.FLOOR)
                       for label in (0, 1)},
                PR={str(label): previous.match_trace(p, t, ig, label)[1] for label in (0, 1)})
            if mode in ("control", "float_all_reference"):
                old_mode = "control" if mode == "control" else "float_q7_8_reference"
                if groups[group]["metrics"] != old["modes"][old_mode]["groups"][group]["metrics"]:
                    raise AssertionError("endpoint metrics differ from frozen diagnosis")
        summary["modes"][mode] = dict(groups=groups, predictions=all_predictions[mode])
        summary["transitions"][mode] = {}
        for label in (0, 1):
            for threshold in (previous.FLOOR, .5):
                def matched_gt(which):
                    return {r["gt_id"] for r in all_GT[which] if r["label"] == label and r["final_match"]
                            and r["final_match"]["score"] >= threshold}
                before, after = matched_gt("control"), matched_gt(mode)
                summary["transitions"][mode][f"{label}:{threshold}"] = dict(lost=sorted(before - after),
                    gained=sorted(after - before), reasons=dict(Counter(
                        r["diagnostic_reason"] for r in all_GT[mode] if r["gt_id"] in before - after)))
    check_inputs(inputs, sources)
    base.save(OUT / "summary.json", summary)
    base.save(OUT / "status.json", dict(status="COMPLETED_SAVED_HEAD_COUNTERFACTUALS",
        seconds=time.perf_counter() - started, images=16, modes=8, exact_postprocess_comparisons=128,
        parity_checks=dict(parity_checks), official_match_array_parity=True,
        training_updates=0, network_forwards=0, total_experimental_updates=36,
        development_inference=False, formal_acceptance=False,
        CUDA_initialized=previous.torch.cuda.is_initialized(), summary_sha256=shared.sha256(OUT / "summary.json")))


if __name__ == "__main__":
    previous.diag.runtime_guard()
    run()
