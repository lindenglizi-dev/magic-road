"""Frozen train16 score/geometry attribution; no training or threshold selection."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import shutil
import time

import numpy as np
import torch

from cnn import integer, metrics
from cnn.hw_validation.production import probe_half_scales as shared
from cnn.hw_validation.production import probe_keep_stem as keep
from cnn.hw_validation.production.trained_integer import IntegerModel, encode_parameters, float_forward

base, diag = shared.base, shared.diag
OUT = base.PROJECT / "cnn/reports/score_box_diagnosis16_20261014_v1"
FLOOR = 3276 / 65536
MODES = ("control", "uniform_half", "keep_stem", "float_q7_8_reference")


def raw_grid(heads):
    boxes, scores = [], []
    for head, stride in zip(heads, (4, 8, 16), strict=True):
        if head.shape != (288 // stride, 512 // stride, 7) or head.dtype != np.int16:
            raise ValueError("invalid frozen head")
        y, x = np.indices(head.shape[:2])
        center = (head[..., :2].astype(np.int64) + np.stack((x, y), -1) * 256) * stride
        size = integer.round_div_even(integer.exponent(head[..., 2:4]).astype(np.int64) * stride, 4)
        half = integer.round_div_even(size, 2)
        boxes.append(np.clip(np.concatenate((center - half, center + half), -1),
                             0, [512 * 256, 288 * 256] * 2).reshape(-1, 4))
        probabilities = integer.sigmoid(head[..., 4:]).astype(np.int64)
        scores.append(integer.round_div_even(probabilities[..., :1] * probabilities[..., 1:],
                                             65536).reshape(-1, 2))
    return np.concatenate(boxes), np.concatenate(scores)


def stages(heads):
    """Trace the real early-stop pipeline, then compare every final field."""
    boxes, scores = raw_grid(heads)
    positive = (boxes[:, 0] < boxes[:, 2]) & (boxes[:, 1] < boxes[:, 3])
    traces, detections = [], []
    for label in (0, 1):
        floor = np.flatnonzero(scores[:, label] >= 3276).tolist()
        top = sorted(floor, key=lambda cell: (-int(scores[cell, label]), cell))[:128]
        kept, suppressed, invalid, visited = [], {}, [], []
        for cell in top:
            visited.append(cell)
            if not positive[cell]:
                invalid.append(cell)
                continue
            blocker = next((previous for previous in kept
                            if integer._overlap_half(boxes[cell].tolist(), boxes[previous].tolist())), None)
            if blocker is not None:
                suppressed[cell] = blocker
                continue
            kept.append(cell)
            box = boxes[cell].tolist()
            detections.append(dict(label=label, score_uint16=int(scores[cell, label]), cell_id=cell,
                box_q8=box, box_source=integer.round_div_even(boxes[cell] * 5, 512).tolist()))
            if len(kept) == 32:
                break
        traces.append(dict(floor=floor, top128=top, kept=kept, invalid_visited=invalid,
            suppressed_by=suppressed, unvisited_after_cap=top[len(visited):]))
    if detections != integer.postprocess(heads, (3276, 3276)):
        raise AssertionError("instrumented postprocess differs from official output")
    return boxes, scores, positive, traces, detections


def match_trace(predictions, truth, ignores, label):
    """GT identities only; official matcher remains the numerical authority."""
    ground = [row for row in truth if row["label"] == label]
    ranked = sorted(((i, p) for i, p in enumerate(predictions) if p["label"] == label),
                    key=lambda pair: (-pair[1]["score"], pair[0]))
    matched, records = set(), []
    for index, prediction in ranked:
        local = [(i, gt) for i, gt in enumerate(ground) if gt["image_id"] == prediction["image_id"]]
        best = max(((metrics.overlap(prediction["box"], gt["box"]), i) for i, gt in local
                    if i not in matched), default=(0., -1), key=lambda pair: (pair[0], -pair[1]))
        gt_id, tp, fp, ignored = None, 0, 0, 0
        if best[0] >= .5:
            matched.add(best[1])
            gt_id, tp = ground[best[1]]["gt_id"], 1
        elif not any(metrics.overlap(prediction["box"], gt["box"]) >= .5 for _, gt in local) and any(
                region["image_id"] == prediction["image_id"] and region["label"] in (-1, label)
                and metrics.overlap(prediction["box"], region["box"], crowd=region.get("crowd", False)) >= .5
                for region in ignores):
            ignored = 1
        else:
            fp = 1
        records.append(dict(prediction_index=index, score=prediction["score"], gt_id=gt_id,
                            tp=tp, fp=fp, ignored=ignored))
    official = metrics._match(predictions, truth, ignores, label, .5)
    for field, expected in zip(("score", "tp", "fp", "ignored"), official[:4], strict=True):
        np.testing.assert_array_equal([r[field] for r in records], expected)
    if len(ground) != official[4]:
        raise AssertionError("GT count mismatch")
    active = [r for r in records if not r["ignored"]]
    tp = np.cumsum([r["tp"] for r in active])
    fp = np.cumsum([r["fp"] for r in active])
    curve = [dict(rank=i + 1, score=r["score"], precision=float(tp[i] / (tp[i] + fp[i])),
                  recall=float(tp[i] / max(len(ground), 1))) for i, r in enumerate(active)]
    return records, curve


def ious(boxes, target):
    boxes = boxes.astype(np.float64) / 256
    intersection = np.maximum(0, np.minimum(boxes[:, 2:], target[2:])
                              - np.maximum(boxes[:, :2], target[:2])).prod(axis=1)
    union = ((boxes[:, 2:] - boxes[:, :2]).prod(axis=1)
             + (target[2] - target[0]) * (target[3] - target[1]) - intersection)
    return np.divide(intersection, union, out=np.zeros_like(intersection), where=union > 0)


def inspect_gt(boxes, scores, positive, traces, truth, assignments):
    result = []
    assigned = {r["gt_id"]: r for r in assignments if r["tp"]}
    for gt in truth:
        label, trace = gt["label"], traces[gt["label"]]
        overlap = ious(boxes, gt["box"])
        support = (overlap >= .5) & positive
        counts = {"raw_positive_IoU50": int(support.sum())}
        for stage in ("floor", "top128", "kept", "invalid_visited", "unvisited_after_cap"):
            counts[stage] = int(support[trace[stage]].sum())
        counts["suppressed"] = int(support[list(trace["suppressed_by"])].sum())
        match = assigned.get(gt["gt_id"])
        if match:
            reason = "matched_at_0_5" if match["score"] >= .5 else "matched_final_below_0_5"
        elif counts["kept"]:
            reason = "final_support_but_greedy_assignment_competition"
        elif counts["unvisited_after_cap"]:
            reason = "matching_top_candidate_unvisited_after_cap_not_proven_NMS_survivor"
        elif counts["suppressed"]:
            reason = "matching_top_candidate_NMS_suppressed"
        elif counts["floor"]:
            reason = "matching_floor_candidate_outside_top128"
        elif counts["raw_positive_IoU50"]:
            reason = "raw_geometry_support_only_below_score_floor"
        else:
            reason = "no_raw_grid_box_IoU50"
        candidates = np.flatnonzero(support)
        best = (min(candidates.tolist(), key=lambda c: (-int(scores[c, label]), c))
                if len(candidates) else None)
        result.append(dict(gt, support_counts=counts, diagnostic_reason=reason,
            final_match=match, best_raw_geometry_IoU=float(overlap.max()),
            highest_score_IoU50_cell=best,
            highest_score_IoU50_uint16=int(scores[best, label]) if best is not None else None))
    return result


def run():
    started = time.perf_counter()
    dataset, control, uniform, folded, _, identity = shared.bind_inputs()
    old_keep = base.read(keep.OUT / "identity.json")
    old_uniform = base.read(shared.OUT / "identity.json")
    if shared.protocol_hash(uniform.scales) != old_uniform["half_scales_sha256"]:
        raise ValueError("uniform-half scales differ from frozen experiment")
    for prior in (old_uniform, old_keep):
        shared.check_identity(prior)
    scales = keep.keep_stem_scales(control.graph, control.scales)
    if shared.protocol_hash(scales) != old_keep["half_scales_sha256"]:
        raise ValueError("keep-Stem scales differ from frozen experiment")
    parameters, _ = encode_parameters(control.graph, folded, scales)
    keep_model = IntegerModel(control.graph, parameters, scales)
    models = dict(control=control, uniform_half=uniform, keep_stem=keep_model)
    for path in (Path(__file__), Path(__file__).with_name("test_diagnose_score_boxes.py"),
                 base.PROJECT / "cnn/metrics.py", Path(keep.__file__)):
        identity["sources"][str(path.relative_to(base.PROJECT)).replace("\\", "/")] = shared.sha256(path)
    for root in (shared.OUT, keep.OUT):
        for name in ("identity.json", "train16.json", "status.json"):
            path = root / name
            identity["fixed_inputs"][str(path)] = shared.sha256(path)
    OUT.mkdir(parents=True, exist_ok=False)
    for folder in ("sources", "cases", "heads"):
        (OUT / folder).mkdir()
    for name in identity["sources"]:
        target = OUT / "sources" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.PROJECT / name, target)
    base.save(OUT / "identity.json", identity)
    base.save(OUT / "contract.json", dict(training_updates=0, gpu=False, modes=MODES,
        score_floor_uint16=3276, fixed_diagnostic_threshold=.5, top128_per_class=True,
        NMS="integer strict IoU>.5", GT_match="official greedy IoU>=.5 with ignore",
        PR_AP="all frozen deployed outputs down to 3276/65536; floor-truncated; not raw-grid AP",
        threshold_selection=False, formal_acceptance=False,
        raw_geometry_support="not evidence of a semantic detection; stage support can overlap",
        scope="same selected 16 training images; no development inference or gate change"))
    aggregate = {mode: [] for mode in MODES}
    truth_all, ignores_all, gt_rows = [], [], {mode: [] for mode in MODES}
    domains = {}
    with torch.inference_mode():
        for sample in base.read(diag.OUT / "selection.json")["samples"]:
            index = sample["train_index"]
            image, _, key = dataset[index]
            row, data = dataset.rows[index], base.centered(image)
            truth = [dict(image_id=key, gt_id=f"{key}#gt{i}", label=int(label), box=box)
                     for i, (label, box) in enumerate(zip(row["labels"], row["boxes"], strict=True))]
            metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
            ignores = [dict(image_id=key, box=box, **meta)
                       for box, meta in zip(row["ignore_boxes"], metadata, strict=True)]
            truth_all.extend(truth)
            ignores_all.extend(ignores)
            domains[key] = row["sampling_group"]
            floating = float_forward(control.graph, folded, data.astype(np.float32))
            reference = [np.rint(floating[name].astype(np.float64) * 256) for name in control.graph["outputs"]]
            saturation = [int(np.count_nonzero((head < -32768) | (head > 32767))) for head in reference]
            reference = [np.clip(head, -32768, 32767).astype(np.int16) for head in reference]
            del floating
            case = dict(key=key, train_index=index, group=row["sampling_group"], truth=truth, ignores=ignores,
                        float_reference_head_saturation=saturation, modes={})
            for mode in MODES:
                heads = reference if mode == MODES[-1] else models[mode].forward(data)[0]
                np.savez_compressed(OUT / "heads" / f"train_{index:02d}_{mode}.npz", *heads)
                boxes, scores, positive, traces, detections = stages(heads)
                predictions = [dict(image_id=key, label=d["label"], score=d["score_uint16"] / 65536,
                    box=[v / 256 for v in d["box_q8"]], cell_id=d["cell_id"]) for d in detections]
                assignments = sum((match_trace(predictions, truth, ignores, label)[0] for label in (0, 1)), [])
                details = inspect_gt(boxes, scores, positive, traces, truth, assignments)
                if mode != MODES[-1]:
                    prior_root = keep.OUT if mode == "keep_stem" else shared.OUT
                    prior_mode = "control" if mode == "control" else "half"
                    prior = base.read(prior_root / "cases" / f"train_{index:02d}.json")[prior_mode]["detections"]
                    for label, name in enumerate(("person", "vehicle")):
                        for threshold in (.05, .5):
                            if metrics.evaluate(predictions, truth, ignores, label=label, threshold=threshold) != prior[name][str(threshold)]:
                                raise AssertionError("frozen experiment per-frame metrics changed")
                case["modes"][mode] = dict(detections=detections, stages=traces, GT=details,
                    at_floor={str(label): metrics.evaluate(predictions, truth, ignores, label=label, threshold=FLOOR)
                              for label in (0, 1)},
                    at_0_5={str(label): metrics.evaluate(predictions, truth, ignores, label=label, threshold=.5)
                            for label in (0, 1)})
                aggregate[mode].extend(predictions)
                gt_rows[mode].extend(details)
            base.save(OUT / "cases" / f"train_{index:02d}.json", case)
            print(json.dumps(dict(completed=len(domains), key=key)), flush=True)
    summary = dict(images=len(domains), truth=truth_all, ignores=ignores_all, modes={}, differences={})
    for mode in MODES:
        predictions = aggregate[mode]
        groups = {}
        for group in ("all", "new", "replay"):
            def selected(rows):
                return [r for r in rows if group == "all" or domains[r["image_id"]] == group]
            p, t, ig = selected(predictions), selected(truth_all), selected(ignores_all)
            groups[group] = dict(metrics=metrics.report(p, t, ig, thresholds=(.5, .5)),
                at_floor={str(label): metrics.evaluate(p, t, ig, label=label, threshold=FLOOR) for label in (0, 1)},
                PR={str(label): match_trace(p, t, ig, label)[1] for label in (0, 1)})
        summary["modes"][mode] = dict(groups=groups, predictions=predictions,
            GT_reason_counts={str(label): dict(Counter(r["diagnostic_reason"] for r in gt_rows[mode]
                                                       if r["label"] == label)) for label in (0, 1)})
        if mode != "control":
            summary["differences"][mode] = {}
            for threshold in (FLOOR, .05, .5):
                before = {r["gt_id"] for r in gt_rows["control"] if r["final_match"]
                          and r["final_match"]["score"] >= threshold}
                after = {r["gt_id"] for r in gt_rows[mode] if r["final_match"]
                         and r["final_match"]["score"] >= threshold}
                summary["differences"][mode][str(threshold)] = dict(lost=sorted(before - after), gained=sorted(after - before))
    shared.check_identity(identity)
    base.save(OUT / "summary.json", summary)
    base.save(OUT / "status.json", dict(status="COMPLETED_TRAIN16_DIAGNOSIS_NO_TRAINING",
        training_updates=0, total_experimental_updates=36, formal_acceptance=False,
        CUDA_initialized=torch.cuda.is_initialized(), seconds=time.perf_counter() - started,
        exact_postprocess_comparisons=64, official_match_array_parity=True,
        summary_sha256=shared.sha256(OUT / "summary.json")))


if __name__ == "__main__":
    diag.runtime_guard()
    run()
