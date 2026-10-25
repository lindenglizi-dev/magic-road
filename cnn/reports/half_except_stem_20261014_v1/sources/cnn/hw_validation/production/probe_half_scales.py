"""One fixed half-feature-scale CPU probe, with train16/train86 continuation gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time

import numpy as np
import torch

from cnn.hw_validation.production import diagnose_quantization16 as diag
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production.trained_integer import (
    IntegerModel, encode_parameters, float_forward, load_package, write_package)
from cnn.integer import postprocess, silu
from cnn.metrics import report
from cnn.train import protocol_hash, sha256

OUT = base.PROJECT / "cnn/reports/half_feature_scale_20261014_v1"
SELECTION_SHA256 = "fdf1232bcb8bd4320ed4ba3e8e0dd578f6e779d6706dbd7160f42d3cbd33260f"
GROUPS = {"all": tuple(range(7)), "box": (0, 1, 2, 3), "objectness": (4,),
          "person": (5,), "vehicle": (6,)}


def half_scales(graph, scales):
    types = {"input": "input"}
    for node in graph["nodes"]:
        if node["op"] == "split_view":
            types.update({view["output"]: types[node["inputs"][0]] for view in node["outputs"]})
        else:
            types[node["output"]] = node["dtype"]
    if set(types) != set(scales) or any(kind not in ("input", "int8", "int16_q7_8") for kind in types.values()):
        raise ValueError("tensor type/scale closure differs from frozen graph")
    return {name: value * .5 if types[name] == "int8" else value for name, value in scales.items()}


def energy_error(reference, actual):
    if reference.shape != actual.shape or not np.isfinite(reference).all() or not np.isfinite(actual).all():
        raise ValueError("nonfinite or mismatched comparison")
    ref = reference.astype(np.float64)
    delta = actual.astype(np.float64) - ref
    sse, power = float(np.sum(delta * delta)), float(np.sum(ref * ref))
    return {"squared_error_sum": sse, "reference_square_sum": power, "values": int(ref.size),
            "normalized_rmse": float(np.sqrt(sse / max(power, 1e-30)))}


def pooled(rows):
    sse = sum(row["squared_error_sum"] for row in rows)
    power = sum(row["reference_square_sum"] for row in rows)
    return {"squared_error_sum": sse, "reference_square_sum": power,
            "normalized_rmse": float(np.sqrt(sse / max(power, 1e-30))),
            "mean_frame_normalized_rmse": float(np.mean([r["normalized_rmse"] for r in rows]))}


def clipping_energy(model, values):
    rows = {}
    for node in model.graph["nodes"]:
        name = node["name"]
        if node["op"] == "conv":
            p = model.parameters[name]
            raw = diag.unclipped(values[name + ":acc"], p["pre_multiplier"], p["pre_shift"])
            difference = (raw - values[name + ":pre"].astype(np.int64)).astype(np.float64) / 256
            row = {"pre_clipping_square_loss": float(np.sum(difference * difference))}
            if node["dtype"] == "int8":
                raw = diag.unclipped(silu(values[name + ":pre"]), p["post_multiplier"], p["post_shift"])
                difference = (raw - values[name].astype(np.int64)).astype(np.float64) * model.scales[name]
                row["post_clipping_square_loss"] = float(np.sum(difference * difference))
            rows[name] = row
        elif node["op"] == "residual_view":
            raw = sum(values[key].astype(np.int16) for key in node["inputs"])
            difference = (raw - values[name].astype(np.int16)).astype(np.float64) * model.scales[name]
            rows[name] = {"residual_clipping_square_loss": float(np.sum(difference * difference))}
    return rows


def summarize(cases, outputs):
    summary = {"image_count": len(cases), "heads": {}, "detections": {}, "clipping": {}, "worst_frames": {}}
    for mode in ("control", "half"):
        summary["heads"][mode] = {}
        for domain in ("all", "new", "replay"):
            selected = [case for case in cases if domain == "all" or case["group"] == domain]
            if not selected:
                continue
            summary["heads"][mode][domain] = {head: {group: pooled(
                [case[mode]["head_errors"][head][group] for case in selected])
                for group in GROUPS} for head in outputs}
        summary["detections"][mode] = {label: {field: sum(case[mode]["detections"][label]["0.5"][field]
            for case in cases) for field in ("tp", "fp", "fn")} for label in ("person", "vehicle")}
        nodes = cases[0][mode]["features"]
        summary["clipping"][mode] = {name: {**{field: sum(case[mode]["features"][name]["clipping"].get(field, 0)
            for case in cases) for field in cases[0][mode]["features"][name]["clipping"]},
            **{field: sum(case[mode]["clipping_energy"].get(name, {}).get(field, 0) for case in cases)
               for field in cases[0][mode]["clipping_energy"].get(name, {})}} for name in nodes}
        summary["worst_frames"][mode] = {head: sorted(
            [{"key": case["key"], "group": case["group"], **case[mode]["head_errors"][head]["all"]} for case in cases],
            key=lambda row: row["normalized_rmse"], reverse=True)[:3] for head in outputs}
    return summary


def gate(summary, outputs):
    checks = {}
    for domain in ("all", "new", "replay"):
        for head in outputs:
            before = summary["heads"]["control"][domain][head]["all"]["normalized_rmse"]
            after = summary["heads"]["half"][domain][head]["all"]["normalized_rmse"]
            checks[f"{domain}:{head}"] = after < before if domain == "all" else after <= before
    for label in ("person", "vehicle"):
        before, after = (summary["detections"][mode][label] for mode in ("control", "half"))
        checks[f"{label}:tp_not_lower"] = after["tp"] >= before["tp"]
        checks[f"{label}:fp_not_higher"] = after["fp"] <= before["fp"]
    return {"criteria_frozen_before_inference": True, "checks": checks, "passed": all(checks.values())}


def bind_inputs():
    if sha256(diag.OUT / "selection.json") != SELECTION_SHA256:
        raise ValueError("pinned train16 selection changed")
    dataset, models, _, fixed, binding = diag.prepare()
    control, folded, manifest = models["original"]
    scales = half_scales(control.graph, control.scales)
    parameters, metadata = encode_parameters(control.graph, folded, scales)
    old_metadata = base.read(base.BASE / "quantization.json")
    for name, fields in parameters.items():
        np.testing.assert_array_equal(fields["weights"], control.parameters[name]["weights"])
        if metadata[name]["weight_scale"] != old_metadata[name]["weight_scale"]:
            raise ValueError("weight scale changed")
    half = IntegerModel(control.graph, parameters, scales)
    fixed += [(diag.OUT / "selection.json", SELECTION_SHA256)]
    sources = [Path(__file__), Path(diag.__file__), Path(__file__).with_name("test_probe_half_scales.py")]
    old_sources = base.read(diag.OUT / "identity.json")["sources"]
    sources += [base.PROJECT / name for name in old_sources]
    sources += [base.PROJECT / "cnn/hw_validation/production/train_qat.py",
                base.PROJECT / "cnn/hw_validation/production/run_trained_integer.py", base.PROJECT / "cnn/evaluate.py"]
    source_hashes = {str(path.relative_to(base.PROJECT)).replace("\\", "/"): sha256(path) for path in set(sources)}
    for name, expected in old_sources.items():
        if source_hashes[name] != expected:
            raise ValueError("previous diagnostic source changed")
    identity = {"fixed_inputs": {str(path): digest for path, digest in fixed}, "sources": source_hashes,
                "original_payload_sha256": manifest["payload_sha256"], "half_scales_sha256": protocol_hash(scales),
                "cache_index_sha256": binding.index_sha256, "factor": .5}
    return dataset, control, half, folded, metadata, identity


def check_identity(identity):
    for path, digest in identity["fixed_inputs"].items():
        if sha256(Path(path)) != digest:
            raise ValueError("frozen input changed during probe")
    for path, digest in identity["sources"].items():
        if sha256(base.PROJECT / path) != digest:
            raise ValueError("source changed during probe")


def probe():
    started = time.perf_counter()
    dataset, control, half, folded, metadata, identity = bind_inputs()
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / "sources").mkdir()
    (OUT / "cases").mkdir()
    for name in identity["sources"]:
        target = OUT / "sources" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.PROJECT / name, target)
    base.save(OUT / "identity.json", identity)
    base.save(OUT / "contract.json", {"factor": .5, "weight_codes_and_scales_fixed": True,
        "input_scale": 1, "raw_head_scale": 1 / 256, "same_execution_engine_control": True,
        "selection_sha256": SELECTION_SHA256, "stage16_gate": "three pooled heads decrease; each domain/head not increase; both classes TP not lower and FP not higher at .5",
        "full86_only_after_stage16_pass": True, "development_only_after_full86_pass": True,
        "training_updates": 0, "GPU": False, "factor_search": False,
        "risk": "Old max-abs calibration extrema exceed half-range by construction; audit clipping and end-to-end effects."})
    base.save(OUT / "reencoding.json", {"scales": half.scales, "quantization": metadata,
        "weight_codes_unchanged": True, "weight_scales_unchanged": True, "integer_model_validation_passed": True})
    selected = [sample["train_index"] for sample in base.read(diag.OUT / "selection.json")["samples"]]
    cases = []
    with torch.inference_mode():
        for stage, indices in (("train16", selected), ("train86", [i for i in range(86) if i not in selected])):
            for index in indices:
                image, _, key = dataset[index]
                data, row = base.centered(image), dataset.rows[index]
                floating = float_forward(control.graph, folded, data.astype(np.float32))
                case = {"train_index": index, "key": key, "group": row["sampling_group"]}
                for mode, model in (("control", control), ("half", half)):
                    heads, _, captures = model.forward(data, capture=True)
                    case[mode] = {"features": diag.feature_rows(model, folded, floating, captures),
                        "clipping_energy": clipping_energy(model, captures), "detections": diag.detections(heads, row),
                        "head_errors": {name: {group: energy_error(floating[name][..., channels],
                            head.astype(np.float64)[..., channels] / 256) for group, channels in GROUPS.items()}
                            for name, head in zip(model.graph["outputs"], heads, strict=True)}}
                    del captures
                del floating
                base.save(OUT / "cases" / f"train_{index:02d}.json", case)
                cases.append(case)
                print(json.dumps({"stage": stage, "completed_total": len(cases), "key": key}), flush=True)
            summary = summarize(cases, control.graph["outputs"])
            decision = gate(summary, control.graph["outputs"])
            summary.update(gate=decision, scope="train_only_fixed_scale_mechanism_probe_not_accuracy_acceptance",
                           seconds=time.perf_counter() - started, training_updates=0, gpu_used=False)
            check_identity(identity)
            base.save(OUT / f"{stage}.json", summary)
            if not decision["passed"]:
                base.save(OUT / "status.json", {"status": f"REJECTED_AT_{stage.upper()}_STOP_NO_FACTOR_SEARCH",
                    "gate_passed": False, "images": len(cases), "new_training_updates": 0,
                    "global_candidate_updates": 36, "development_inference": False, "package_exported": False,
                    "CUDA_initialized": torch.cuda.is_initialized(), "seconds": time.perf_counter() - started})
                return
    base.save(OUT / "status.json", {"status": "TRAIN86_PASSED_READY_FOR_FIXED_DEVELOPMENT17",
        "gate_passed": True, "images": 86, "new_training_updates": 0, "global_candidate_updates": 36,
        "development_inference": False, "package_exported": False, "CUDA_initialized": torch.cuda.is_initialized()})


def development():
    status = base.read(OUT / "status.json")
    if status["status"] != "TRAIN86_PASSED_READY_FOR_FIXED_DEVELOPMENT17" or not base.read(OUT / "train86.json")["gate"]["passed"]:
        raise ValueError("full86 training gate has not passed")
    training, control, half, _, _, identity = bind_inputs()
    if identity != base.read(OUT / "identity.json"):
        raise ValueError("development identity differs from training probe")
    from cnn.hw_validation.production.run_trained_integer import VALIDATION, VAL_HASH, BASELINE
    from cnn.evaluate import load_validation_subset
    from cnn.train import FullFrameDataset, dataset_content_hash
    if sha256(VALIDATION) != VAL_HASH:
        raise ValueError("development manifest changed")
    rows, total = load_validation_subset(VALIDATION, None, 17)
    dataset = FullFrameDataset(rows, "val")
    baseline = base.read(BASELINE)
    if total != 17 or dataset_content_hash(dataset.rows) != baseline["evaluated_image_content_sha256"]:
        raise ValueError("development content differs")
    manifest = write_package(OUT / "package", half.graph, half.parameters, half.scales,
        {"purpose": "HALF_SCALE_DIAGNOSTIC_NOT_QAT_NOT_DEPLOYMENT", "source_checkpoint_sha256": base.CHECKPOINT_HASH,
         "factor": .5, "identity": identity, "train86_sha256": sha256(OUT / "train86.json")})
    loaded, _ = load_package(OUT / "package")
    image, _, _ = training[base.read(diag.OUT / "selection.json")["samples"][0]["train_index"]]
    _, _, expected = half.forward(base.centered(image), capture=True)
    _, _, actual = loaded.forward(base.centered(image), capture=True)
    if set(expected) != set(actual):
        raise ValueError("exported trace key mismatch")
    for name in expected:
        np.testing.assert_array_equal(actual[name], expected[name])
    trace_names = [name for name in expected if not name.endswith(":acc")]
    base.save(OUT / "export_parity.json", {"trace_tensors": len(trace_names),
        "trace_values": sum(expected[name].size for name in trace_names),
        "accumulator_tensors": len(expected) - len(trace_names), "all_values_exact": True,
        "scope": "in_memory_integer_model_vs_reloaded_parameter_package; not_RTL_or_independent_arithmetic_oracle"})
    del expected, actual
    predictions, truth, ignores = [], [], []
    with torch.inference_mode():
        for index, row in enumerate(dataset.rows):
            image, _, _ = dataset[index]
            heads, _, _ = loaded.forward(base.centered(image))
            predictions.extend(dict(image_id=row["image"], label=d["label"], box=[v / 256 for v in d["box_q8"]],
                                    score=d["score_uint16"] / 65536) for d in postprocess(heads, (3276, 3276)))
            truth.extend(dict(image_id=row["image"], label=label, box=box) for label, box in zip(row["labels"], row["boxes"], strict=True))
            metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
            ignores.extend(dict(image_id=row["image"], box=box, label=meta["label"], crowd=meta["crowd"])
                           for box, meta in zip(row["ignore_boxes"], metadata, strict=True))
            print(json.dumps({"stage": "development17", "completed": index + 1}), flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("development labels/ignore differ")
    check_identity(identity)
    base.save(OUT / "development17.json", {"image_count": 17, "predictions": predictions, "truth": truth,
        "ignores": ignores, "diagnostic_metrics_at_0_5": report(predictions, truth, ignores, thresholds=(.5, .5)),
        "package_payload_sha256": manifest["payload_sha256"], "formal_acceptance": False, "training_updates": 0})
    base.save(OUT / "development_status.json", {"status": "COMPLETED_FIXED_HALF_SCALE_DEVELOPMENT17",
        "training_started": False, "formal_acceptance": False})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("probe", "development"))
    args = parser.parse_args()
    diag.runtime_guard()
    if args.stage == "probe":
        probe()
    else:
        development()
