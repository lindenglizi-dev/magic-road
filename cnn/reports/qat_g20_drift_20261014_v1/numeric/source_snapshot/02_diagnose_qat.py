"""Train-only QAT loss diagnosis; run only if the bounded G10 candidate fails to recover."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time

import numpy as np
import torch

from cnn.hw_validation.production.diagnose_trained_integer import error
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import (
    CHECKPOINT, CHECKPOINT_HASH, PROJECT, TRAIN, TRAIN_HASH, centered, save, sha256,
)
from cnn.hw_validation.production.train_qat import BASE, FORMAT, MANIFEST_HASH, OUT, RUN, UPDATES
from cnn.hw_validation.production.trained_integer import float_forward, load_package
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset


QAT_CHECKPOINT = RUN / "last.pt"
OLD_PACKAGE = BASE / "package"
NEW_PACKAGE = OUT / "package"
COMPARISONS = (
    "old_ptq_integer_vs_original_float",
    "new_qat_integer_vs_original_float",
    "new_qat_integer_vs_updated_float",
    "updated_float_vs_original_float",
    "new_qat_integer_vs_old_ptq_integer",
)


def comparison_names(graph):
    convolutions = [node["name"] for node in graph["nodes"] if node["op"] == "conv"]
    tracked = convolutions + [name for name in graph["outputs"] if name not in convolutions]
    return convolutions, tracked


def summarized(errors):
    return {
        f"{field}_{kind}": float(function([row[field] for row in errors]))
        for field in ("normalized_rmse", "rmse", "max_abs_error")
        for kind, function in (("mean", np.mean), ("max", np.max))
    }


def add_endpoints(total, statistics, names):
    for name in names:
        source = statistics[name]
        row = total.setdefault(name, {
            "values": 0,
            "pre_endpoint_count": 0,
            "output_endpoint_count": 0,
            "acc_min": source["acc_min"],
            "acc_max": source["acc_max"],
        })
        row["values"] += source["values"]
        row["pre_endpoint_count"] += source["pre_endpoint_count"]
        row["output_endpoint_count"] += source["output_endpoint_count"]
        row["acc_min"] = min(row["acc_min"], source["acc_min"])
        row["acc_max"] = max(row["acc_max"], source["acc_max"])


def finalized_endpoints(total):
    return {name: dict(row,
                       pre_endpoint_occupancy=row["pre_endpoint_count"] / row["values"],
                       output_endpoint_occupancy=row["output_endpoint_count"] / row["values"])
            for name, row in total.items()}


def parameter_differences(names, original, updated, old_integer, new_integer):
    rows = []
    for name in names:
        old_weight, old_bias = (value.detach().cpu() for value in original[name])
        new_weight, new_bias = (value.detach().cpu() for value in updated[name])
        old_codes, new_codes = old_integer.parameters[name], new_integer.parameters[name]
        rows.append({
            "name": name,
            "weight_quant_code_difference_count": int(np.count_nonzero(
                old_codes["weights"] != new_codes["weights"])),
            "weight_quant_code_elements": int(old_codes["weights"].size),
            "bias_code_difference_count": int(np.count_nonzero(
                old_codes["bias"] != new_codes["bias"])),
            "bias_code_elements": int(old_codes["bias"].size),
            "float_weight_changed_count": int(torch.count_nonzero(old_weight != new_weight)),
            "float_weight_elements": old_weight.numel(),
            "float_bias_changed_count": int(torch.count_nonzero(old_bias != new_bias)),
            "float_bias_elements": old_bias.numel(),
            "float_weight_max_abs_change": float((old_weight - new_weight).abs().max()),
            "float_bias_max_abs_change": float((old_bias - new_bias).abs().max()),
        })
    count_fields = [key for key in rows[0] if key.endswith(("_count", "_elements"))]
    return {"layers": rows, "totals": {key: sum(row[key] for row in rows) for key in count_fields}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(PROJECT / "cnn/reports") or output.exists():
        raise ValueError("--output must be a new directory inside cnn/reports")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise ValueError("CUDA_VISIBLE_DEVICES must be empty")

    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    started = time.perf_counter()
    if sha256(CHECKPOINT) != CHECKPOINT_HASH or sha256(TRAIN) != TRAIN_HASH:
        raise ValueError("frozen original checkpoint or training manifest changed")
    if sha256(OLD_PACKAGE / "manifest.json") != MANIFEST_HASH:
        raise ValueError("old PTQ package manifest changed")

    _, snapshot = load_dataset_snapshot(TRAIN)
    dataset = make_frame_dataset(snapshot.rows, "train", TRAIN, mosaic=False)
    if len(dataset) != 86:
        raise ValueError("expected 86 training frames")
    original_state = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    original_model = RoadYOLOS4().eval()
    if original_state["architecture_hash"] != original_model.architecture_hash():
        raise ValueError("original checkpoint architecture changed")
    original_model.load_state_dict(original_state["model"], strict=True)
    if original_state["dataset_content_sha256"] != snapshot.dataset_content_sha256:
        raise ValueError("original checkpoint training content changed")
    original_folded = original_model.folded_conv_state()

    old_integer, old_manifest = load_package(OLD_PACKAGE)
    new_integer, new_manifest = load_package(NEW_PACKAGE)
    checkpoint_sha256 = sha256(QAT_CHECKPOINT)
    qat_state = torch.load(QAT_CHECKPOINT, map_location="cpu", weights_only=False)
    identity = qat_state.get("identity", {})
    if (qat_state.get("format") != FORMAT or qat_state.get("checkpoint_kind") != "training"
            or qat_state.get("phase") != "qat" or qat_state.get("candidate") is not True
            or qat_state.get("trained_steps") != UPDATES or qat_state.get("next_update") != UPDATES
            or qat_state.get("formal_acceptance") is not False
            or identity.get("source_checkpoint_sha256") != CHECKPOINT_HASH
            or identity.get("dataset_sha256") != TRAIN_HASH
            or identity.get("dataset_content_sha256") != snapshot.dataset_content_sha256
            or identity.get("source_package_manifest_sha256") != MANIFEST_HASH):
        raise ValueError("final QAT checkpoint identity or completion state differs")
    if any(sha256(PROJECT / name) != digest for name, digest in identity["source_sha256"].items()):
        raise ValueError("QAT training source identity changed")
    provenance = new_manifest.get("provenance", {})
    if (provenance.get("purpose") != "QAT_G10_DEVELOPMENT_CANDIDATE"
            or provenance.get("checkpoint_sha256") != checkpoint_sha256
            or provenance.get("source_checkpoint_sha256") != CHECKPOINT_HASH
            or provenance.get("trained_steps") != UPDATES
            or provenance.get("identity") != identity
            or provenance.get("qat_exact_fixed_weight_scales") is not True):
        raise ValueError("QAT package is not bound to the final checkpoint")
    if (old_manifest["provenance"]["checkpoint_sha256"] != CHECKPOINT_HASH
            or old_manifest["provenance"]["calibration_dataset_sha256"] != TRAIN_HASH
            or old_manifest["provenance"]["calibration_content_sha256"] != snapshot.dataset_content_sha256
            or old_integer.graph != new_integer.graph or old_integer.scales != new_integer.scales):
        raise ValueError("old/new package graph, scales, or source binding differs")

    qat_model = QATExactModel.from_package(
        OLD_PACKAGE, original_folded, BASE / "quantization.json").eval()
    qat_model.load_state_dict(qat_state["model"], strict=True)
    updated_folded = qat_model.folded_state()
    exported = qat_model.integer_parameters()
    if any(not np.array_equal(value, new_integer.parameters[name][field])
           for name, fields in exported.items() for field, value in fields.items()):
        raise ValueError("QAT checkpoint parameters do not reproduce the exported package")

    graph = old_integer.graph
    names, tracked_names = comparison_names(graph)
    if len(names) != 67:
        raise ValueError("frozen graph no longer has 67 convolutions")
    by_layer = {name: {comparison: [] for comparison in COMPARISONS} for name in tracked_names}
    old_endpoints, new_endpoints, cases = {}, {}, []
    with torch.inference_mode():
        for index in range(4):
            image, _, key = dataset[index]
            data = centered(image)
            original_values = float_forward(graph, original_folded, data.astype(np.float32))
            updated_values = float_forward(graph, updated_folded, data.astype(np.float32))
            _, old_statistics, old_values = old_integer.forward(data, capture=True)
            _, new_statistics, new_values = new_integer.forward(data, capture=True)
            add_endpoints(old_endpoints, old_statistics, names)
            add_endpoints(new_endpoints, new_statistics, names)
            layers = {}
            for name in tracked_names:
                old_dequantized = old_values[name].astype(np.float64) * old_integer.scales[name]
                new_dequantized = new_values[name].astype(np.float64) * new_integer.scales[name]
                comparisons = {
                    "old_ptq_integer_vs_original_float": error(original_values[name], old_dequantized),
                    "new_qat_integer_vs_original_float": error(original_values[name], new_dequantized),
                    "new_qat_integer_vs_updated_float": error(updated_values[name], new_dequantized),
                    "updated_float_vs_original_float": error(original_values[name], updated_values[name]),
                    "new_qat_integer_vs_old_ptq_integer": error(old_dequantized, new_dequantized),
                }
                layers[name] = comparisons
                for comparison, value in comparisons.items():
                    by_layer[name][comparison].append(value)
            cases.append({
                "train_index": index,
                "key": key,
                "layers": layers,
                "output_heads": {name: layers[name] for name in graph["outputs"]},
            })
            print(f"train-only QAT diagnosis {index + 1}/4", flush=True)

    old_endpoints = finalized_endpoints(old_endpoints)
    new_endpoints = finalized_endpoints(new_endpoints)
    comparison_summary = {
        name: {comparison: summarized(by_layer[name][comparison]) for comparison in COMPARISONS}
        for name in tracked_names
    }
    layer_summary = []
    for name in names:
        layer_summary.append({
            "name": name,
            "comparisons": comparison_summary[name],
            "endpoint_occupancy_not_clipping": {
                "old_ptq": old_endpoints[name],
                "new_qat": new_endpoints[name],
            },
        })
    summary_by_name = {row["name"]: row for row in layer_summary}
    output_heads = [{"name": name, "comparisons": comparison_summary[name],
                     "endpoint_occupancy_not_clipping": "not_applicable_nonconv_output"}
                    for name in graph["outputs"]]
    top_layer_errors = {
        comparison: sorted(
            ({"name": row["name"], **row["comparisons"][comparison]} for row in layer_summary),
            key=lambda row: row["normalized_rmse_mean"], reverse=True)[:10]
        for comparison in COMPARISONS
    }
    top_endpoint_occupancy = sorted(
        ({"name": name, **row} for name, row in new_endpoints.items()),
        key=lambda row: row["output_endpoint_occupancy"], reverse=True)[:10]
    parameters = parameter_differences(
        names, original_folded, updated_folded, old_integer, new_integer)

    sources = [Path(__file__), Path(__file__).with_name("diagnose_trained_integer.py"),
               Path(__file__).with_name("qat_exact.py"), Path(__file__).with_name("train_qat.py"),
               Path(__file__).with_name("trained_integer.py"),
               Path(__file__).with_name("run_trained_integer.py"),
               Path(__file__).with_name("test_diagnose_qat.py"),
               PROJECT / "cnn/model.py", PROJECT / "cnn/train.py", PROJECT / "cnn/dataset.py",
               PROJECT / "cnn/integer.py", Path(__file__).with_name("graph.py"),
               Path(__file__).with_name("deployment_contract.json")]
    report = {
        "schema_version": 1,
        "status": "completed_train_only_QAT_quantization_diagnosis_not_accuracy",
        "purpose": "run only if bounded QAT G10 does not recover; locate quantization loss",
        "scope": "first four training frames; no ground truth or validation data used",
        "input_sha256": {
            "original_fp32_checkpoint": CHECKPOINT_HASH,
            "training_manifest": TRAIN_HASH,
            "old_ptq_package_manifest": MANIFEST_HASH,
            "old_ptq_payload": old_manifest["payload_sha256"],
            "qat_checkpoint": checkpoint_sha256,
            "qat_package_manifest": sha256(NEW_PACKAGE / "manifest.json"),
            "qat_payload": new_manifest["payload_sha256"],
            "dataset_content": snapshot.dataset_content_sha256,
        },
        "source_sha256": {str(path.relative_to(PROJECT)).replace("\\", "/"): sha256(path)
                          for path in sources},
        "qat_training_source_identity": identity["source_sha256"],
        "identity_checks_passed": True,
        "frames": 4,
        "convolution_layers": 67,
        "comparisons": list(COMPARISONS),
        "output_heads": output_heads,
        "first_three_layers": [summary_by_name[name] for name in names[:3]],
        "top_layer_errors": top_layer_errors,
        "top_new_qat_endpoint_occupancy": top_endpoint_occupancy,
        "endpoint_interpretation": "Endpoint occupancy is not an exact clipping count.",
        "parameter_differences": parameters,
        "layer_summary": layer_summary,
        "cases": cases,
        "device": "cpu",
        "cpu_threads": 2,
        "gpu_used": False,
        "optimizer_created": False,
        "training_started": False,
        "ground_truth_used": False,
        "validation_split_used": False,
        "accuracy_measured": False,
        "model_selection_performed": False,
        "independent_FP64_oracle_rerun": False,
        "seconds": time.perf_counter() - started,
        "limitation": "Diagnostic attribution only; it does not select a new float model, measure accuracy, or prove FPGA behavior.",
    }
    output.mkdir(parents=True, exist_ok=False)
    save(output / "diagnosis.json", report)
    print(json.dumps({"status": report["status"], "output": str(output)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
