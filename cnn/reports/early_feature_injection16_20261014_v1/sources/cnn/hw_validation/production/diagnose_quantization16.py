"""Bounded train-only attribution of same-weight float/integer deployment error."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import torch
from torch.nn import functional as F

from cnn.integer import postprocess, requantize, silu
from cnn.metrics import evaluate
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset, protocol_hash, sha256
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_numpy235 as runtime
from cnn.hw_validation.production.diagnose_qat_continuation_drift import (
    PARENT_CHECKPOINT, PARENT_CHECKPOINT_SHA256, PARENT_REPORT, PARENT_MANIFEST_SHA256,
    head_breakdown, summarize_breakdowns)
from cnn.hw_validation.production.diagnose_trained_integer import error
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.trained_integer import (
    float_forward, nonconv, conv_exact, load_package)

OUT = base.PROJECT / "cnn/reports/quantization_error16_20261014_v1"
NUMPY_ROOT = base.PROJECT.parents[1] / ".tools/road_yolo_numpy_235_20261014/numpy"


def select_indices(rows):
    """Round-robin source strata, alternating sparse/dense labels; no predictions."""
    selected = []
    for group in ("new", "replay"):
        buckets = defaultdict(list)
        for index, row in enumerate(rows):
            if row["split"] != "train":
                raise ValueError("selection accepts training rows only")
            if row["sampling_group"] == group:
                buckets[(row["camera_id"], row["scene_id"])].append(index)
        for indices in buckets.values():
            indices.sort(key=lambda i: (len(rows[i]["boxes"]),
                min((b[3] - b[1] for b in rows[i]["boxes"]), default=0), rows[i]["teacher_key"]))
        picked, turn = [], 0
        while len(picked) < 8:
            progressed = False
            for key in sorted(buckets):
                if buckets[key] and len(picked) < 8:
                    picked.append(buckets[key].pop(0 if turn % 2 == 0 else -1))
                    progressed = True
            if not progressed:
                raise ValueError(f"fewer than eight training rows in {group}")
            turn += 1
        selected.extend(picked)
    if len(set(selected)) != 16:
        raise ValueError("duplicate diagnostic sample")
    return selected


def float_conv(node, source, weight, bias):
    nchw = torch.from_numpy(np.ascontiguousarray(source.transpose(2, 0, 1))).unsqueeze(0)
    value = F.conv2d(nchw, weight, bias, stride=node["stride"],
                     padding=node["padding"], groups=node["groups"])
    return value[0].permute(1, 2, 0).numpy().copy()


def usage(codes, scale):
    if codes.dtype != np.int8:
        raise ValueError("feature usage requires INT8")
    flat = codes.reshape(-1, codes.shape[-1])
    distinct = [int(np.count_nonzero(np.bincount(flat[:, c].astype(np.int16) + 128,
                                                minlength=256))) for c in range(flat.shape[1])]
    absolute = np.abs(codes.astype(np.int16))
    return {"scale": scale, "zero_fraction": float(np.mean(codes == 0)),
            "distinct_codes": int(np.unique(codes).size), "channel_distinct_codes": distinct,
            "channel_zero_fraction": np.mean(flat == 0, axis=0).tolist(),
            "channel_max_abs_code": np.max(absolute, axis=(0, 1)).tolist(),
            "abs_code_p50_p99_p999_max": np.quantile(absolute, [.5, .99, .999, 1]).tolist()}


def unclipped(values, multiplier, shift):
    # Accumulators and positive INT32 multipliers have products strictly within INT64.
    return requantize(values, multiplier, shift, -(1 << 62), (1 << 62) - 1)


def feature_rows(model, folded, floating, captured):
    result = {}
    for node in model.graph["nodes"]:
        if node["op"] == "conv":
            name, source_name = node["name"], node["inputs"][0]
            weight, bias = folded[name]
            local_pre = float_conv(node, captured[source_name].astype(np.float32)
                                   * model.scales[source_name], weight, bias)
            local = (F.silu(torch.from_numpy(local_pre)).numpy()
                     if node["dtype"] == "int8" else local_pre)
            pre_raw = unclipped(captured[name + ":acc"],
                                model.parameters[name]["pre_multiplier"], model.parameters[name]["pre_shift"])
            np.testing.assert_array_equal(np.clip(pre_raw, -32768, 32767).astype(np.int16), captured[name + ":pre"])
            counts = {"pre_clipped": int(np.count_nonzero((pre_raw < -32768) | (pre_raw > 32767))),
                      "pre_values": int(pre_raw.size)}
            if node["dtype"] == "int8":
                p = model.parameters[name]
                post_raw = unclipped(silu(captured[name + ":pre"]), p["post_multiplier"], p["post_shift"])
                np.testing.assert_array_equal(np.clip(post_raw, -128, 127).astype(np.int8), captured[name])
                counts["post_clipped"] = int(np.count_nonzero((post_raw < -128) | (post_raw > 127)))
            rows = {name: local}
        else:
            inputs = {name: captured[name].astype(np.float32) * model.scales[name]
                      for name in node["inputs"]}
            rows = nonconv(node, inputs)
            counts = {}
            if node["op"] == "residual_view":
                raw = sum(captured[name].astype(np.int16) for name in node["inputs"])
                counts = {"residual_clipped": int(np.count_nonzero((raw < -128) | (raw > 127)))}
        for name, local in rows.items():
            actual = captured[name].astype(np.float64) * model.scales[name]
            row = {"op": node["op"], "cumulative": error(floating[name], actual),
                   "local_same_integer_input": error(local, actual), "clipping": counts}
            if captured[name].dtype == np.int8:
                row["usage"] = usage(captured[name], model.scales[name])
                row["float_abs_p99_in_codes"] = float(np.quantile(np.abs(floating[name]), .99) / model.scales[name])
            result[name] = row
    return result


def detections(heads, row):
    predictions = [dict(image_id=row["teacher_key"], label=d["label"],
        box=[v / 256 for v in d["box_q8"]], score=d["score_uint16"] / 65536)
        for d in postprocess(heads, (3276, 3276))]
    truth = [dict(image_id=row["teacher_key"], label=label, box=box)
             for label, box in zip(row["labels"], row["boxes"], strict=True)]
    metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
    ignores = [dict(image_id=row["teacher_key"], box=box, **meta)
               for box, meta in zip(row["ignore_boxes"], metadata, strict=True)]
    return {name: {str(threshold): evaluate(predictions, truth, ignores, label=label,
                                          threshold=threshold, iou=.5)
                   for threshold in (.05, .5)} for label, name in enumerate(("person", "vehicle"))}


def injected_forward(model, image, name, ideal):
    """Diagnostic single-tensor oracle injection, re-encoded at its unchanged scale."""
    values = {"input": image}
    target = next(n for n in model.graph["nodes"] if n.get("output") == name)
    if target["op"] != "conv" or target["dtype"] != "int8":
        raise ValueError("injection requires a feature convolution")
    for node in model.graph["nodes"]:
        if node["op"] != "conv":
            values.update(nonconv(node, values))
            continue
        p, key = model.parameters[node["name"]], node["output"]
        if key == name:
            value = np.clip(np.rint(ideal / model.scales[key]), -128, 127).astype(np.int8)
        else:
            acc = conv_exact(values[node["inputs"][0]], p["weights"], p["bias"],
                             node["stride"][0], node["padding"][0], node["groups"])
            pre = requantize(acc, p["pre_multiplier"], p["pre_shift"], -32768, 32767).astype(np.int16)
            value = (requantize(silu(pre), p["post_multiplier"], p["post_shift"]).astype(np.int8)
                     if node["dtype"] == "int8" else pre)
        values[key] = value
    return [values[name] for name in model.graph["outputs"]]


def runtime_guard():
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1" or os.environ.get("PYTORCH_NVML_BASED_CUDA_CHECK") != "1":
        raise ValueError("CPU diagnosis requires hidden CUDA and NVML availability guard")
    if np.__version__ != "2.3.5" or not Path(np.__file__).resolve().is_relative_to(NUMPY_ROOT.resolve()):
        raise ValueError("isolated NumPy 2.3.5 required")
    if torch.cuda.is_available() or torch.cuda.is_initialized():
        raise ValueError("CUDA unexpectedly available/initialized")
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)


def prepare():
    runtime.native_runtime_identity()
    fixed = [(base.CHECKPOINT, base.CHECKPOINT_HASH), (base.TRAIN, base.TRAIN_HASH),
             (base.BASE / "package/manifest.json", base.MANIFEST_HASH),
             (PARENT_CHECKPOINT, PARENT_CHECKPOINT_SHA256),
             (PARENT_REPORT / "package/manifest.json", PARENT_MANIFEST_SHA256)]
    for path, expected in fixed:
        if sha256(path) != expected:
            raise ValueError(f"frozen input changed: {path}")
    _, snapshot = load_dataset_snapshot(base.TRAIN)
    receipt = runtime.expected_cache_receipt()
    binding = runtime.transition_cache_binding(snapshot, receipt)
    dataset = make_frame_dataset(snapshot.rows, "train", base.TRAIN, mosaic=False,
        cache_root=binding.root, cache_index_sha256=binding.index_sha256, cache_binding=binding)
    if len(dataset) != 86:
        raise ValueError("expected 86 training frames")
    original = torch.load(base.CHECKPOINT, map_location="cpu", weights_only=False)
    source = RoadYOLOS4().eval()
    source.load_state_dict(original["model"], strict=True)
    if original["dataset_content_sha256"] != snapshot.dataset_content_sha256:
        raise ValueError("dataset content differs from frozen source")
    initial, initial_manifest = load_package(base.BASE / "package")
    qat, qat_manifest = load_package(PARENT_REPORT / "package")
    state = torch.load(PARENT_CHECKPOINT, map_location="cpu", weights_only=False)
    if qat_manifest["provenance"]["identity"] != state["identity"] or state["trained_steps"] != 10:
        raise ValueError("QAT parent identity mismatch")
    original_folded = source.folded_conv_state()
    module = QATExactModel.from_package(base.BASE / "package", original_folded, base.BASE / "quantization.json")
    module.load_state_dict(state["model"], strict=True)
    for name, fields in module.integer_parameters().items():
        for field, expected in fields.items():
            np.testing.assert_array_equal(qat.parameters[name][field], expected)
    folded = {name: tuple(t.detach().cpu() for t in pair) for name, pair in module.folded_state().items()}
    scales = {name: np.asarray(row["weight_scale"]) for name, row in base.read(base.BASE / "quantization.json").items()}
    return dataset, {"original": (initial, original_folded, initial_manifest),
                     "qat_g10": (qat, folded, qat_manifest)}, scales, fixed, binding


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("measure", "inject"))
    args = parser.parse_args()
    runtime_guard()
    started = time.perf_counter()
    dataset, models, weight_scales, fixed, binding = prepare()
    selection = [{"train_index": index, "key": dataset.rows[index]["teacher_key"],
                  "group": dataset.rows[index]["sampling_group"], "camera_id": dataset.rows[index]["camera_id"],
                  "scene_id": dataset.rows[index]["scene_id"], "image": dataset.rows[index]["image"],
                  "image_sha256": dataset.rows[index]["image_sha256"],
                  "person_boxes": dataset.rows[index]["labels"].count(0),
                  "vehicle_boxes": dataset.rows[index]["labels"].count(1),
                  "heights_network_pixels": [b[3] - b[1] for b in dataset.rows[index]["boxes"]]}
                 for index in select_indices(dataset.rows)]
    sources = [Path(__file__), *[base.PROJECT / name for name in (
        "cnn/model.py", "cnn/train.py", "cnn/dataset.py", "cnn/disk_cache.py", "cnn/integer.py", "cnn/metrics.py",
        "cnn/hw_validation/production/trained_integer.py", "cnn/hw_validation/production/qat_exact.py",
        "cnn/hw_validation/production/train_qat_numpy235.py",
        "cnn/hw_validation/production/graph.py", "cnn/hw_validation/production/diagnose_trained_integer.py",
        "cnn/hw_validation/production/diagnose_qat_continuation_drift.py")]]
    source_hashes = {str(p.relative_to(base.PROJECT)).replace("\\", "/"): sha256(p) for p in sources}
    identity = {"fixed_inputs": {str(p): h for p, h in fixed}, "selection_sha256": protocol_hash(selection),
                "sources": source_hashes, "cache_index_sha256": binding.index_sha256,
                "payloads": {name: manifest["payload_sha256"] for name, (_, _, manifest) in models.items()}}
    if args.stage == "measure":
        OUT.mkdir(parents=True, exist_ok=False)
        (OUT / "sources").mkdir()
        for path in sources:
            target = OUT / "sources" / path.relative_to(base.PROJECT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        base.save(OUT / "selection.json", {"rule": select_indices.__doc__, "samples": selection,
            "predictions_used_for_selection": False, "validation_used_for_selection": False,
            "selection_sha256": identity["selection_sha256"]})
        base.save(OUT / "identity.json", identity)
    elif base.read(OUT / "identity.json") != identity:
        raise ValueError("injection identity differs from completed measurement")
    stage = OUT / args.stage
    stage.mkdir(exist_ok=False)
    all_cases, head_rows = [], {name: defaultdict(list) for name in models}
    inject_names = []
    if args.stage == "inject":
        summary = base.read(OUT / "measure/summary.json")
        inject_names = [row["name"] for row in summary["top_local_feature_errors"]["original"][:3]]
        base.save(stage / "contract.json", {"layers": inject_names, "selection_source": "train-only local error ranking",
            "operation": "replace single feature tensor with same-weight FP32 value re-encoded at unchanged scale",
            "not_deployable": True, "not_additive_causal_attribution": True, "validation_used": False})
    with torch.inference_mode():
        for number, sample in enumerate(selection):
            index = sample["train_index"]
            image, _, key = dataset[index]
            if key != sample["key"]:
                raise ValueError("actual sample differs from pinned selection")
            data, row = base.centered(image), dataset.rows[index]
            case = {"sample": sample, "models": {}}
            for label, (model, folded, _) in models.items():
                floating = float_forward(model.graph, folded, data.astype(np.float32))
                if args.stage == "measure":
                    heads, _, captures = model.forward(data, capture=True)
                    quantized_weights = {name: (torch.from_numpy((model.parameters[name]["weights"]
                        * weight_scales[name][:, None, None, None]).astype(np.float32)), bias)
                        for name, (_, bias) in folded.items()}
                    weights_only = float_forward(model.graph, quantized_weights, data.astype(np.float32))
                    features = feature_rows(model, folded, floating, captures)
                    for name, item in features.items():
                        item["weights_only_cumulative"] = error(floating[name], weights_only[name])
                    channels = {name: head_breakdown(floating[name], head.astype(np.float64) / 256)
                                for name, head in zip(model.graph["outputs"], heads, strict=True)}
                    for name, values in channels.items():
                        head_rows[label][name].append(values)
                    qheads = [np.clip(np.rint(floating[name].astype(np.float64) * 256), -32768, 32767).astype(np.int16)
                              for name in model.graph["outputs"]]
                    case["models"][label] = {"features": features, "heads": channels,
                        "training_GT_integer": detections(heads, row),
                        "training_GT_float_with_only_Q7_8_head_encoding": detections(qheads, row)}
                    del captures, weights_only, features
                else:
                    baseline_heads, _, _ = model.forward(data)
                    injections = {}
                    for name in inject_names:
                        heads = injected_forward(model, data, name, floating[name])
                        injections[name] = {"heads": {output: head_breakdown(floating[output], head.astype(np.float64) / 256)
                            for output, head in zip(model.graph["outputs"], heads, strict=True)},
                            "training_GT": detections(heads, row)}
                    case["models"][label] = {"baseline_heads": {output: head_breakdown(floating[output], head.astype(np.float64) / 256)
                        for output, head in zip(model.graph["outputs"], baseline_heads, strict=True)}, "injections": injections}
                del floating
            base.save(stage / f"case_{number:02d}.json", case)
            all_cases.append(case)
            print(json.dumps({"stage": args.stage, "completed": number + 1, "total": 16, "key": key}), flush=True)
    if args.stage == "measure":
        averages = {}
        for label in models:
            names = all_cases[0]["models"][label]["features"]
            averages[label] = {}
            for name in names:
                items = [case["models"][label]["features"][name] for case in all_cases]
                average = {"name": name, "op": items[0]["op"], **{kind + "_nrmse_mean": float(np.mean(
                    [item[kind]["normalized_rmse"] for item in items]))
                    for kind in ("cumulative", "local_same_integer_input", "weights_only_cumulative")}}
                average["clipping_total"] = {key: sum(item["clipping"].get(key, 0) for item in items)
                                             for key in {key for item in items for key in item["clipping"]}}
                if "usage" in items[0]:
                    average.update(scale=items[0]["usage"]["scale"], zero_fraction_mean=float(np.mean(
                        [item["usage"]["zero_fraction"] for item in items])), float_abs_p99_in_codes_mean=float(np.mean(
                        [item["float_abs_p99_in_codes"] for item in items])))
                averages[label][name] = average
        result = {"layers": averages, "top_local_feature_errors": {label: sorted(
            [row for name, row in rows.items() if row["op"] == "conv" and "scale" in row],
            key=lambda row: row["local_same_integer_input_nrmse_mean"], reverse=True)[:10]
            for label, rows in averages.items()}, "heads": {label: {name: summarize_breakdowns(rows)
                for name, rows in heads.items()} for label, heads in head_rows.items()}}
    else:
        result = {"injected_layers": inject_names, "cases": len(all_cases)}
    for path, expected in fixed:
        if sha256(path) != expected:
            raise ValueError("frozen model/data/package changed during diagnosis")
    if any(sha256(base.PROJECT / name) != expected for name, expected in source_hashes.items()):
        raise ValueError("diagnostic source changed during inference")
    result.update(status="completed_train_only_diagnosis", images=16, models=list(models),
        seconds=time.perf_counter() - started, training_updates=0, optimizer_created=False,
        validation_inference=False, candidate_exported=False, gpu_used=False,
        cuda_initialized=torch.cuda.is_initialized(), identity_sha256=protocol_hash(identity),
        runtime={"python": sys.version, "numpy": np.__version__, "numpy_file": str(np.__file__), "torch": torch.__version__})
    base.save(stage / "summary.json", result)


if __name__ == "__main__":
    main()
