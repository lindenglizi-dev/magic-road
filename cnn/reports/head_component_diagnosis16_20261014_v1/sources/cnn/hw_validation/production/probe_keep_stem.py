"""One fixed keep-Stem/half-other-features numerical control; no training."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time

import numpy as np
import torch

from cnn.hw_validation.production import probe_half_scales as shared
from cnn.hw_validation.production.trained_integer import (
    IntegerModel, encode_parameters, float_forward, write_package, load_package)

base, diag = shared.base, shared.diag
OUT = base.PROJECT / "cnn/reports/half_except_stem_20261014_v1"
RECIPE = "original_Stem_scale_half_other_INT8_features_v1"


def keep_stem_scales(graph, scales):
    if "stem.conv" not in scales:
        raise ValueError("missing frozen Stem tensor")
    for node in graph["nodes"]:
        names = node.get("inputs", []) + ([view["output"] for view in node["outputs"]]
                if node["op"] == "split_view" else [node["output"]])
        if node["op"] != "conv" and "stem.conv" in names:
            raise ValueError("Stem scale component changed; refusing partial branch scaling")
    result = shared.half_scales(graph, scales)
    result["stem.conv"] = scales["stem.conv"]
    return result


def bind_inputs():
    dataset, control, _, folded, _, old_identity = shared.bind_inputs()
    shared.check_identity(old_identity)
    scales = keep_stem_scales(control.graph, control.scales)
    parameters, metadata = encode_parameters(control.graph, folded, scales)
    old_metadata = base.read(base.BASE / "quantization.json")
    for name, fields in parameters.items():
        np.testing.assert_array_equal(fields["weights"], control.parameters[name]["weights"])
        if metadata[name]["weight_scale"] != old_metadata[name]["weight_scale"]:
            raise ValueError("weight quantization scale changed")
    for field, value in control.parameters["stem.conv"].items():
        np.testing.assert_array_equal(parameters["stem.conv"][field], value)
    probe_model = IntegerModel(control.graph, parameters, scales)
    identity = dict(old_identity, recipe=RECIPE, experiment_id=OUT.name,
                    half_scales_sha256=shared.protocol_hash(scales))
    identity["sources"] = dict(old_identity["sources"])
    for path in (Path(__file__), Path(__file__).with_name("test_probe_keep_stem.py")):
        identity["sources"][str(path.relative_to(base.PROJECT)).replace("\\", "/")] = shared.sha256(path)
    return dataset, control, probe_model, folded, metadata, identity


def train_probe():
    started = time.perf_counter()
    dataset, control, experiment, folded, metadata, identity = bind_inputs()
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / "sources").mkdir()
    (OUT / "cases").mkdir()
    for name in identity["sources"]:
        target = OUT / "sources" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.PROJECT / name, target)
    base.save(OUT / "identity.json", identity)
    base.save(OUT / "contract.json", {"recipe": RECIPE, "actual_changed_feature_scales": 103,
        "Stem_all_integer_parameters_unchanged": True, "weight_codes_and_scales_unchanged": True,
        "input_scale": 1, "raw_head_scale": 1 / 256, "selection_sha256": shared.SELECTION_SHA256,
        "criteria": "same frozen gate as uniform-half: all pooled heads decrease; domains do not increase; both classes TP>=control and FP<=control at score .5",
        "train86_only_after_train16_pass": True, "development_only_after_train86_pass": True,
        "training_updates": 0, "factor_search": False})
    base.save(OUT / "reencoding.json", {"scales": experiment.scales, "quantization": metadata,
        "Stem_fields_exact_control": True, "all_weight_codes_and_scales_exact_control": True})
    selected = [sample["train_index"] for sample in base.read(diag.OUT / "selection.json")["samples"]]
    cases = []
    with torch.inference_mode():
        for stage, indices in (("train16", selected), ("train86", [i for i in range(86) if i not in selected])):
            for index in indices:
                image, _, key = dataset[index]
                data, row = base.centered(image), dataset.rows[index]
                floating = float_forward(control.graph, folded, data.astype(np.float32))
                case = {"train_index": index, "key": key, "group": row["sampling_group"]}
                for mode, model in (("control", control), ("half", experiment)):
                    heads, _, values = model.forward(data, capture=True)
                    case[mode] = {"features": diag.feature_rows(model, folded, floating, values),
                        "clipping_energy": shared.clipping_energy(model, values),
                        "detections": diag.detections(heads, row),
                        "head_errors": {name: {group: shared.energy_error(floating[name][..., channels],
                            head.astype(np.float64)[..., channels] / 256) for group, channels in shared.GROUPS.items()}
                            for name, head in zip(model.graph["outputs"], heads, strict=True)}}
                    del values
                del floating
                base.save(OUT / "cases" / f"train_{index:02d}.json", case)
                cases.append(case)
                print(json.dumps({"stage": stage, "completed_total": len(cases), "key": key}), flush=True)
            summary = shared.summarize(cases, control.graph["outputs"])
            decision = shared.gate(summary, control.graph["outputs"])
            summary.update(gate=decision, recipe=RECIPE, training_updates=0, gpu_used=False,
                           seconds=time.perf_counter() - started)
            shared.check_identity(identity)
            base.save(OUT / f"{stage}.json", summary)
            if not decision["passed"]:
                base.save(OUT / "status.json", {"status": f"REJECTED_AT_{stage.upper()}_STOP",
                    "images": len(cases), "new_training_updates": 0, "global_candidate_updates": 36,
                    "development_inference": False, "package_exported": False,
                    "CUDA_initialized": torch.cuda.is_initialized(), "seconds": time.perf_counter() - started})
                return
    base.save(OUT / "status.json", {"status": "TRAIN86_PASSED_READY_FOR_DEVELOPMENT17",
        "images": 86, "new_training_updates": 0, "global_candidate_updates": 36,
        "development_inference": False, "package_exported": False, "CUDA_initialized": torch.cuda.is_initialized()})


def development():
    if (base.read(OUT / "status.json")["status"] != "TRAIN86_PASSED_READY_FOR_DEVELOPMENT17"
            or not base.read(OUT / "train86.json")["gate"]["passed"]):
        raise ValueError("train86 gate must pass before any development inference")
    training, _, experiment, _, _, identity = bind_inputs()
    if identity != base.read(OUT / "identity.json"):
        raise ValueError("experiment identity changed")
    from cnn.hw_validation.production.run_trained_integer import VALIDATION, VAL_HASH, BASELINE
    from cnn.evaluate import load_validation_subset
    from cnn.train import FullFrameDataset, dataset_content_hash
    if shared.sha256(VALIDATION) != VAL_HASH:
        raise ValueError("development manifest changed")
    rows, total = load_validation_subset(VALIDATION, None, 17)
    dataset, baseline = FullFrameDataset(rows, "val"), base.read(BASELINE)
    if total != 17 or dataset_content_hash(dataset.rows) != baseline["evaluated_image_content_sha256"]:
        raise ValueError("development content differs from frozen baseline")
    manifest = write_package(OUT / "package", experiment.graph, experiment.parameters, experiment.scales,
        {"purpose": "KEEP_STEM_HALF_FEATURES_DIAGNOSTIC_NOT_DEPLOYMENT", "identity": identity,
         "source_checkpoint_sha256": base.CHECKPOINT_HASH, "recipe": RECIPE,
         "train86_sha256": shared.sha256(OUT / "train86.json")})
    loaded, _ = load_package(OUT / "package")
    index = base.read(diag.OUT / "selection.json")["samples"][0]["train_index"]
    data = base.centered(training[index][0])
    _, _, expected = experiment.forward(data, capture=True)
    _, _, actual = loaded.forward(data, capture=True)
    if set(expected) != set(actual):
        raise ValueError("trace keys differ after package reload")
    for name in expected:
        np.testing.assert_array_equal(actual[name], expected[name])
    trace_names = [name for name in expected if not name.endswith(":acc")]
    base.save(OUT / "export_parity.json", {"trace_tensors": len(trace_names),
        "trace_values": sum(expected[name].size for name in trace_names),
        "accumulator_tensors": len(expected) - len(trace_names), "all_values_exact": True,
        "scope": "in_memory_integer_model_vs_reloaded_package_not_RTL"})
    del expected, actual
    predictions, truth, ignores = [], [], []
    with torch.inference_mode():
        for number, row in enumerate(dataset.rows):
            heads, _, _ = loaded.forward(base.centered(dataset[number][0]))
            predictions.extend(dict(image_id=row["image"], label=d["label"], box=[v / 256 for v in d["box_q8"]],
                score=d["score_uint16"] / 65536) for d in shared.postprocess(heads, (3276, 3276)))
            truth.extend(dict(image_id=row["image"], label=label, box=box)
                         for label, box in zip(row["labels"], row["boxes"], strict=True))
            metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
            ignores.extend(dict(image_id=row["image"], label=meta["label"], crowd=meta["crowd"], box=box)
                           for box, meta in zip(row["ignore_boxes"], metadata, strict=True))
            print(json.dumps({"stage": "development17", "completed": number + 1}), flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("development GT/ignore differs")
    shared.check_identity(identity)
    base.save(OUT / "development17.json", {"image_count": 17, "predictions": predictions, "truth": truth,
        "ignores": ignores, "diagnostic_metrics_at_0_5": shared.report(predictions, truth, ignores, thresholds=(.5, .5)),
        "recipe": RECIPE, "payload_sha256": manifest["payload_sha256"], "training_updates": 0,
        "formal_acceptance": False})
    base.save(OUT / "development_status.json", {"status": "COMPLETED_FIXED_DEVELOPMENT17", "training_started": False})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("probe", "development"))
    args = parser.parse_args()
    diag.runtime_guard()
    if args.stage == "probe":
        train_probe()
    else:
        development()
