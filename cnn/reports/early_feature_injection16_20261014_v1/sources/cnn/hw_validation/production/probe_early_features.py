"""Three fixed early-feature injections at original scales; no training."""
from collections import Counter
from pathlib import Path
import json
import shutil
import time

import numpy as np
import torch

from cnn.hw_validation.production import diagnose_head_components as components

previous = components.previous
base, shared, diag = previous.base, previous.shared, previous.diag
OUT = base.PROJECT / "cnn/reports/early_feature_injection16_20261014_v1"
TARGETS = ("stem.conv", "down2.pw.conv", "csp2.out.conv")
MODES = ("control", *TARGETS)
DECISION_SHA = "6c842cda18b29708194a9080e645fc65cef58aa09b9dd740cd8a5ae405d00b47"


def injection_audit(ideal, scale, expected_shape):
    if ideal.shape != expected_shape or not np.isfinite(ideal).all() or not np.isfinite(scale) or scale <= 0:
        raise ValueError("invalid injection shape/value/scale")
    raw = np.rint(ideal / scale)
    codes = np.clip(raw, -128, 127).astype(np.int8)
    return codes, dict(scale=scale, values=int(raw.size),
        clipped=int(np.count_nonzero((raw < -128) | (raw > 127))),
        rounding_and_clipping_error=shared.energy_error(ideal, codes.astype(np.float64) * scale))


def continuation_gate(groups, control):
    checks = {}
    for label in ("person", "vehicle"):
        before, after = control["all"]["classes"][label], groups["all"]["classes"][label]
        checks[label + ":AP50_improves"] = after["ap50"] > before["ap50"]
        checks[label + ":TP_not_lower"] = after["tp"] >= before["tp"]
        checks[label + ":FP_not_higher"] = after["fp"] <= before["fp"]
        for domain in ("new", "replay"):
            checks[f"{domain}:{label}:AP50_not_lower"] = (
                groups[domain]["classes"][label]["ap50"] >= control[domain]["classes"][label]["ap50"])
    return dict(passed=all(checks.values()), checks=checks)


def run():
    started = time.perf_counter()
    decision_path = components.OUT / "decision.json"
    if shared.sha256(decision_path) != DECISION_SHA:
        raise ValueError("approved three-probe decision changed")
    dataset, control, _, folded, _, identity = shared.bind_inputs()
    old = base.read(previous.OUT / "identity.json")
    shared.check_identity(old)
    review_path, old_summary_path = previous.OUT / "evidence_review.json", previous.OUT / "summary.json"
    if (shared.sha256(review_path) != components.PRIOR_REVIEW_SHA
            or shared.sha256(old_summary_path) != components.PRIOR_SUMMARY_SHA):
        raise ValueError("frozen train16 control changed")
    review, old_summary = base.read(review_path), base.read(old_summary_path)
    indices = review["exact_unique_train_indices"]
    if len(indices) != len(set(indices)) or len(indices) != 16:
        raise ValueError("expected frozen 16 unique training indices")
    for name in TARGETS:
        node = next(n for n in control.graph["nodes"] if n.get("output") == name)
        if node["op"] != "conv" or node["dtype"] != "int8":
            raise ValueError("target not an INT8 convolution")
    for path, digest in ((decision_path, DECISION_SHA), (review_path, components.PRIOR_REVIEW_SHA),
                         (old_summary_path, components.PRIOR_SUMMARY_SHA)):
        identity["fixed_inputs"][str(path)] = digest
    for name, digest in review["artifacts"].items():
        identity["fixed_inputs"][str(previous.OUT / name)] = digest
    for path in (Path(__file__), Path(__file__).with_name("test_probe_early_features.py"),
                 Path(previous.__file__), Path(components.__file__)):
        identity["sources"][str(path.relative_to(base.PROJECT)).replace("\\", "/")] = shared.sha256(path)
    identity.update(experiment_id=OUT.name, targets=TARGETS, scales_sha256=shared.protocol_hash(control.scales),
        recipe="single FP32 feature reencoded RNE/sat8 at unchanged original scale; no model edits")
    # bind_inputs also constructs an unused half-scale model; only control is executed here.
    identity["unused_shared_half_scale_identity"] = identity.pop("half_scales_sha256")
    identity.pop("factor")
    shared.check_identity(identity)
    OUT.mkdir(parents=True, exist_ok=False)
    for folder in ("sources", "cases", "heads", "injected_features"):
        (OUT / folder).mkdir()
    for name in identity["sources"]:
        target = OUT / "sources" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.PROJECT / name, target)
    base.save(OUT / "identity.json", identity)
    base.save(OUT / "contract.json", dict(targets=TARGETS, max_training_images=16,
        original_scales_unchanged=True, one_tensor_at_a_time=True,
        unchanged_injection_preflight="first actual image, all three target tensors, exact final-head parity",
        fixed_score=.5, floor_uint16=3276, TopK=128, NMS="strict IoU>.5", max_boxes_per_class=32,
        continuation_gate=base.read(decision_path)["next_proposed_not_executed"]["continuation_gate"],
        formal_acceptance=False, deployment_candidate=False, training_updates=0,
        caveat="ideal injection still has original-scale rounding/clipping; failure does not exonerate a layer"))
    cases, predictions = [], {mode: [] for mode in MODES}
    truth, ignores, domains = [], [], {}
    preflight = []
    with torch.inference_mode():
        for number, index in enumerate(indices):
            image, _, key = dataset[index]
            row, data = dataset.rows[index], base.centered(image)
            prior_case = base.read(previous.OUT / "cases" / f"train_{index:02d}.json")
            gt = [dict(image_id=key, gt_id=f"{key}#gt{i}", label=int(label), box=box)
                  for i, (label, box) in enumerate(zip(row["labels"], row["boxes"], strict=True))]
            meta = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
            ig = [dict(image_id=key, box=box, **m) for box, m in zip(row["ignore_boxes"], meta, strict=True)]
            if (key != review["exact_unique_frame_keys"][number] or gt != prior_case["truth"]
                    or ig != prior_case["ignores"] or key in domains or row["split"] != "train"):
                raise ValueError("sample/labels/ignore/train split differ from frozen case")
            domains[key] = row["sampling_group"]
            truth.extend(gt)
            ignores.extend(ig)
            floating = diag.float_forward(control.graph, folded, data.astype(np.float32))
            heads, _, values = control.forward(data, capture=number == 0)
            saved_control = components.load_heads(previous.OUT, index, "control")
            saved_reference = components.load_heads(previous.OUT, index, "float_q7_8_reference")
            for output, actual, expected, ref in zip(control.graph["outputs"], heads, saved_control, saved_reference, strict=True):
                np.testing.assert_array_equal(actual, expected)
                np.testing.assert_array_equal(np.clip(np.rint(floating[output].astype(np.float64) * 256),
                                                      -32768, 32767).astype(np.int16), ref)
            if number == 0:
                for name in TARGETS:
                    ideal_original = values[name].astype(np.float64) * control.scales[name]
                    encoded, _ = injection_audit(ideal_original, control.scales[name], values[name].shape)
                    np.testing.assert_array_equal(encoded, values[name])
                    unchanged = diag.injected_forward(control, data, name, ideal_original)
                    for actual, expected in zip(unchanged, heads, strict=True):
                        np.testing.assert_array_equal(actual, expected)
                    preflight.append(dict(layer=name, reencoded_tensor_exact=True, all_three_heads_exact=True))
                base.save(OUT / "preflight.json", dict(image=key, checks=preflight, passed=True))
                del values
            case = dict(key=key, train_index=index, group=row["sampling_group"], truth=gt, ignores=ig, modes={})
            for mode in MODES:
                audit = None
                if mode == "control":
                    actual = heads
                else:
                    codes, audit = injection_audit(floating[mode], control.scales[mode], floating[mode].shape)
                    np.savez_compressed(OUT / "injected_features" / f"train_{index:02d}_{mode}.npz", codes=codes)
                    actual = diag.injected_forward(control, data, mode, floating[mode])
                np.savez_compressed(OUT / "heads" / f"train_{index:02d}_{mode}.npz", *actual)
                boxes, scores, positive, stages, detections = previous.stages(actual)
                if mode == "control" and detections != prior_case["modes"]["control"]["detections"]:
                    raise AssertionError("control postprocess differs from frozen diagnosis")
                p = [dict(image_id=key, label=d["label"], score=d["score_uint16"] / 65536,
                          box=[v / 256 for v in d["box_q8"]], cell_id=d["cell_id"]) for d in detections]
                assignments = sum((previous.match_trace(p, gt, ig, label)[0] for label in (0, 1)), [])
                case["modes"][mode] = dict(injection=audit, detections=detections, stages=stages,
                    GT=previous.inspect_gt(boxes, scores, positive, stages, gt, assignments),
                    head_errors={output: {group: shared.energy_error(floating[output][..., channels],
                        head.astype(np.float64)[..., channels] / 256) for group, channels in shared.GROUPS.items()}
                        for output, head in zip(control.graph["outputs"], actual, strict=True)})
                predictions[mode].extend(p)
            del floating
            base.save(OUT / "cases" / f"train_{index:02d}.json", case)
            cases.append(case)
            print(json.dumps(dict(completed=number + 1, total=16, key=key)), flush=True)
    if truth != old_summary["truth"] or ignores != old_summary["ignores"] or Counter(domains.values()) != {"new": 8, "replay": 8}:
        raise AssertionError("aggregate labels/order/groups differ")
    summary = dict(images=16, truth=truth, ignores=ignores, modes={}, gates={})
    for mode in MODES:
        groups, errors = {}, {}
        for domain in ("all", "new", "replay"):
            def selected(rows):
                return [r for r in rows if domain == "all" or domains[r["image_id"]] == domain]
            p, t, ig = selected(predictions[mode]), selected(truth), selected(ignores)
            groups[domain] = previous.metrics.report(p, t, ig, thresholds=(.5, .5))
            selected_cases = [c for c in cases if domain == "all" or c["group"] == domain]
            errors[domain] = {output: {group: shared.pooled(
                [c["modes"][mode]["head_errors"][output][group] for c in selected_cases])
                for group in shared.GROUPS} for output in control.graph["outputs"]}
            if mode == "control" and groups[domain] != old_summary["modes"]["control"]["groups"][domain]["metrics"]:
                raise AssertionError("control aggregate metrics changed")
        summary["modes"][mode] = dict(groups=groups, heads=errors, predictions=predictions[mode],
            injection_clipped=sum(c["modes"][mode]["injection"]["clipped"] for c in cases) if mode != "control" else None)
        if mode != "control":
            summary["gates"][mode] = continuation_gate(groups, summary["modes"]["control"]["groups"])
    shared.check_identity(identity)
    base.save(OUT / "summary.json", summary)
    passed = [name for name, result in summary["gates"].items() if result["passed"]]
    base.save(OUT / "status.json", dict(status="DIAGNOSTIC_GATE_PASSED_NOT_MODEL_REPAIR" if passed else "ALL_THREE_PROBES_REJECTED_STOP_BRANCH",
        passed_probes=passed, seconds=time.perf_counter() - started, training_updates=0,
        total_experimental_updates=36, CUDA_initialized=torch.cuda.is_initialized(),
        development_inference=False, formal_acceptance=False, deployment_candidate=False,
        exact_control_head_comparisons=48, exact_float_reference_head_comparisons=48,
        exact_postprocess_comparisons=64, original_tensor_injection_preflight=3,
        summary_sha256=shared.sha256(OUT / "summary.json")))


if __name__ == "__main__":
    diag.runtime_guard()
    run()
