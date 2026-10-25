"""Train-only, four-frame numeric localization of rejected frozen-Stem G20 drift."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import torch

from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production.diagnose_qat import (
    add_endpoints, comparison_names, finalized_endpoints, parameter_differences, summarized)
from cnn.hw_validation.production.diagnose_trained_integer import error
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import centered
from cnn.hw_validation.production.trained_integer import IntegerModel, float_forward, load_package
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset, protocol_hash, sha256


OUTPUT = base.PROJECT / "cnn/reports/qat_g20_drift_20261014_v1/numeric"
NUMPY_ROOT = base.PROJECT.parents[1] / ".tools/road_yolo_numpy_235_20261014/numpy"
PARENT_REPORT = base.PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1"
PARENT_CHECKPOINT = base.PROJECT / "cnn/runs/qat_frozen_stem_g10_20261014_v1/last.pt"
PARENT_CHECKPOINT_SHA256 = "f58ce4501104e818c8a6fb10e378d7e7668b937b1332f3530180d4806029d3dd"
PARENT_MANIFEST_SHA256 = "93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b"
G20_REPORT = base.PROJECT / "cnn/reports/qat_frozen_stem_g20_numpy235_20261014_v2"
G20_CHECKPOINT = base.PROJECT / "cnn/runs/qat_frozen_stem_g20_numpy235_20261014_v2/last.pt"
G20_CHECKPOINT_SHA256 = "36136fa83b37d4d8c4960d22fb5126e3326d984ffce0f4bd3136c24494bdb284"
G20_MANIFEST_SHA256 = "896f8a6350e968e435ab3ec5c84ca7a2c8205ade194481d35478262799a90927"
COMPARISONS = (
    "g20_integer_vs_parent_integer",
    "parent_float_vs_original_float",
    "g20_float_vs_original_float",
    "parent_integer_vs_parent_float",
    "g20_integer_vs_g20_float",
)
CHANNELS = ("tx", "ty", "tw", "th", "objectness", "person_logit", "vehicle_logit")
GROUPS = {"box_regression": (0, 1, 2, 3), "objectness_score": (4,), "class_scores": (5, 6)}


def head_layout(graph: dict) -> tuple[dict[str, str], list[str]]:
    """Derive head roots from the actual output concat inputs, not a name guess."""
    by_output = {node.get("output"): node for node in graph["nodes"] if "output" in node}
    roots = {}
    for output in graph["outputs"]:
        node = by_output.get(output)
        if node is None or node["op"] != "concat_view" or len(node["inputs"]) != 2:
            raise ValueError(f"{output}: expected two-input prediction concat")
        root_set = {name.split(".", 1)[0] for name in node["inputs"]}
        if len(root_set) != 1 or not all(name.endswith((".reg_out", ".cls_out")) for name in node["inputs"]):
            raise ValueError(f"{output}: prediction branches changed")
        roots[output] = root_set.pop()
    if len(set(roots.values())) != len(graph["outputs"]):
        raise ValueError("prediction outputs do not have distinct head roots")
    convs = [node["name"] for node in graph["nodes"] if node["op"] == "conv"]
    head_names = [name for name in convs if name.split(".", 1)[0] in set(roots.values())]
    if not head_names or any(not any(name.startswith(root + ".") for name in head_names)
                             for root in roots.values()):
        raise ValueError("actual graph has an incomplete head layer set")
    return roots, head_names


def head_breakdown(reference: np.ndarray, actual: np.ndarray) -> dict:
    if reference.shape != actual.shape or reference.shape[-1] != 7:
        raise ValueError("prediction head must be matching HWC tensors with seven channels")
    return {
        "all_7_channels": error(reference, actual),
        "groups": {name: error(reference[..., indices], actual[..., indices])
                   for name, indices in GROUPS.items()},
        "channels": {name: error(reference[..., index], actual[..., index])
                     for index, name in enumerate(CHANNELS)},
    }


def summarize_breakdowns(rows: list[dict]) -> dict:
    return {
        "all_7_channels": summarized([row["all_7_channels"] for row in rows]),
        "groups": {name: summarized([row["groups"][name] for row in rows]) for name in GROUPS},
        "channels": {name: summarized([row["channels"][name] for row in rows]) for name in CHANNELS},
    }


def hybrid_integer(g20: IntegerModel, parent: IntegerModel, selected: set[str]) -> IntegerModel:
    parameters = {name: {field: value.copy() for field, value in fields.items()}
                  for name, fields in g20.parameters.items()}
    for name in selected:
        for field in ("weights", "bias"):
            parameters[name][field] = parent.parameters[name][field].copy()
    model = IntegerModel(g20.graph, parameters, g20.scales)
    for name, fields in model.parameters.items():
        for field, value in fields.items():
            expected = (parent.parameters[name][field]
                        if name in selected and field in {"weights", "bias"}
                        else g20.parameters[name][field])
            np.testing.assert_array_equal(value, expected)
    return model


def _dequant(values: dict, model: IntegerModel, name: str) -> np.ndarray:
    return values[name].astype(np.float64) * model.scales[name]


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_checkpoint(state: dict, manifest: dict, *, parent: bool) -> dict:
    identity = state.get("identity", {})
    expected_steps, expected_format = ((10, base.FORMAT) if parent else (20, continuation.FORMAT))
    purpose = ("QAT_G10_DEVELOPMENT_CANDIDATE" if parent
               else "QAT_G20_CONTINUATION_DEVELOPMENT_CANDIDATE")
    provenance = manifest.get("provenance", {})
    if (state.get("format") != expected_format or state.get("checkpoint_kind") != "training"
            or state.get("candidate") is not True or state.get("formal_acceptance") is not False
            or state.get("trained_steps") != expected_steps or state.get("next_update") != expected_steps
            or identity.get("source_checkpoint_sha256") != base.CHECKPOINT_HASH
            or identity.get("dataset_sha256") != base.TRAIN_HASH
            or provenance.get("purpose") != purpose or provenance.get("trained_steps") != expected_steps
            or provenance.get("identity") != identity
            or provenance.get("qat_exact_fixed_weight_scales") is not True):
        raise ValueError("checkpoint/package identity or completion schema changed")
    return identity


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output != OUTPUT.resolve() or output.exists():
        raise ValueError("--output must be the new fixed numeric diagnosis directory")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise ValueError("CUDA_VISIBLE_DEVICES must be -1")
    if np.__version__ != "2.3.5" or not Path(np.__file__).resolve().is_relative_to(NUMPY_ROOT.resolve()):
        raise ValueError("diagnosis requires the isolated NumPy 2.3.5 runtime")
    if torch.cuda.is_available() or torch.cuda.is_initialized():
        raise ValueError("CUDA must remain unavailable and uninitialized")
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    started = time.perf_counter()

    fixed = ((base.CHECKPOINT, base.CHECKPOINT_HASH), (base.TRAIN, base.TRAIN_HASH),
             (PARENT_CHECKPOINT, PARENT_CHECKPOINT_SHA256),
             (PARENT_REPORT / "package/manifest.json", PARENT_MANIFEST_SHA256),
             (G20_CHECKPOINT, G20_CHECKPOINT_SHA256),
             (G20_REPORT / "package/manifest.json", G20_MANIFEST_SHA256))
    for path, digest in fixed:
        if sha256(path) != digest:
            raise ValueError(f"frozen input changed: {path}")

    _payload, snapshot = load_dataset_snapshot(base.TRAIN)
    dataset = make_frame_dataset(snapshot.rows, "train", base.TRAIN, mosaic=False)
    if len(dataset) != 86 or snapshot.manifest_sha256 != base.TRAIN_HASH:
        raise ValueError("expected the frozen 86-frame training split")

    original_state = torch.load(base.CHECKPOINT, map_location="cpu", weights_only=False)
    original_model = RoadYOLOS4().eval()
    original_model.load_state_dict(original_state["model"], strict=True)
    if (original_state["architecture_hash"] != original_model.architecture_hash()
            or original_state["dataset_content_sha256"] != snapshot.dataset_content_sha256):
        raise ValueError("original FP32 source identity changed")
    original_folded = original_model.folded_conv_state()

    parent_integer, parent_manifest = load_package(PARENT_REPORT / "package")
    g20_integer, g20_manifest = load_package(G20_REPORT / "package")
    parent_state = torch.load(PARENT_CHECKPOINT, map_location="cpu", weights_only=False)
    g20_state = torch.load(G20_CHECKPOINT, map_location="cpu", weights_only=False)
    parent_identity = _validate_checkpoint(parent_state, parent_manifest, parent=True)
    g20_identity = _validate_checkpoint(g20_state, g20_manifest, parent=False)
    if (parent_manifest["payload_sha256"] != "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
            or g20_manifest["payload_sha256"] != "e1621603bd71e611a79187460832e4a7d32c8d600e442100ea4cdcb8b9ab7655"
            or parent_integer.graph != g20_integer.graph or parent_integer.scales != g20_integer.scales
            or protocol_hash(parent_integer.graph) != parent_identity["graph_sha256"]
            or protocol_hash(parent_integer.scales) != parent_identity["scales_sha256"]
            or parent_identity["graph_sha256"] != g20_identity["graph_sha256"]
            or parent_identity["scales_sha256"] != g20_identity["scales_sha256"]
            or parent_identity["architecture_hash"] != g20_identity["architecture_hash"]
            or parent_identity["dataset_content_sha256"] != snapshot.dataset_content_sha256
            or g20_identity["dataset_content_sha256"] != snapshot.dataset_content_sha256
            or g20_identity.get("parent_checkpoint_sha256") != PARENT_CHECKPOINT_SHA256):
        raise ValueError("graph/scales/payload/source ancestry binding changed")
    for identity in (parent_identity, g20_identity):
        if any(sha256(base.PROJECT / name) != digest for name, digest in identity["source_sha256"].items()):
            raise ValueError("training source closure changed")

    parent_qat = QATExactModel.from_package(
        base.BASE / "package", original_folded, base.BASE / "quantization.json").eval()
    parent_qat.load_state_dict(parent_state["model"], strict=True)
    g20_qat = QATExactModel.from_package(
        base.BASE / "package", original_folded, base.BASE / "quantization.json").eval()
    g20_qat.load_state_dict(g20_state["model"], strict=True)
    for model, packaged in ((parent_qat, parent_integer), (g20_qat, g20_integer)):
        encoded = model.integer_parameters()
        if any(not np.array_equal(value, packaged.parameters[name][field])
               for name, fields in encoded.items() for field, value in fields.items()):
            raise ValueError("checkpoint does not reproduce its integer package")
    parent_folded, g20_folded = parent_qat.folded_state(), g20_qat.folded_state()

    graph = parent_integer.graph
    conv_names, tracked_names = comparison_names(graph)
    roots, head_names = head_layout(graph)
    if len(conv_names) != 67 or len(tracked_names) != 70:
        raise ValueError("frozen 67-convolution/three-output graph changed")
    head_set = set(head_names)
    hybrid_head = hybrid_integer(g20_integer, parent_integer, head_set)
    hybrid_nonhead = hybrid_integer(g20_integer, parent_integer, set(conv_names) - head_set)

    sample_rows = [{"train_index": index, "key": dataset.rows[index]["teacher_key"],
                    "image": dataset.rows[index]["image"], "image_sha256": dataset.rows[index]["image_sha256"]}
                   for index in range(4)]
    sources = [Path(__file__), Path(__file__).with_name("test_diagnose_qat_continuation_drift.py"),
               Path(__file__).with_name("diagnose_qat.py"),
               Path(__file__).with_name("diagnose_trained_integer.py"),
               Path(__file__).with_name("trained_integer.py"), Path(__file__).with_name("qat_exact.py"),
               Path(__file__).with_name("train_qat.py"),
               Path(__file__).with_name("train_qat_frozen_stem_continue.py"),
               Path(__file__).with_name("train_qat_numpy235.py"),
               base.PROJECT / "cnn/model.py", base.PROJECT / "cnn/train.py",
               base.PROJECT / "cnn/dataset.py", base.PROJECT / "cnn/integer.py",
               Path(__file__).with_name("graph.py"), Path(__file__).with_name("deployment_contract.json")]
    source_hashes = {str(path.relative_to(base.PROJECT)).replace("\\", "/"): sha256(path) for path in sources}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(exist_ok=False)
    snapshots = output / "source_snapshot"
    snapshots.mkdir()
    copied = {}
    for index, (relative, digest) in enumerate(source_hashes.items()):
        target = snapshots / f"{index:02d}_{Path(relative).name}"
        shutil.copyfile(base.PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError("source snapshot copy mismatch")
        copied[target.name] = {"source": relative, "sha256": digest}
    base.save(output / "source_snapshot.json", {
        "captured_before_inference": True, "source_sha256": source_hashes,
        "copies": copied, "sample_identity": sample_rows,
    })

    by_layer = {name: {comparison: [] for comparison in COMPARISONS} for name in tracked_names}
    endpoint_totals = {"parent_g10": {}, "g20": {}}
    head_rows = {comparison: {name: [] for name in graph["outputs"]} for comparison in COMPARISONS}
    hybrid_rows = {kind: {name: [] for name in graph["outputs"]}
                   for kind in ("g20_with_parent_head_weights_bias", "g20_with_parent_nonhead_weights_bias")}
    cases = []
    with torch.inference_mode():
        for index in range(4):
            image, _target_not_used, key = dataset[index]
            data = centered(image)
            original_values = float_forward(graph, original_folded, data.astype(np.float32))
            parent_float = float_forward(graph, parent_folded, data.astype(np.float32))
            g20_float = float_forward(graph, g20_folded, data.astype(np.float32))
            _, parent_stats, parent_values = parent_integer.forward(data, capture=True)
            _, g20_stats, g20_values = g20_integer.forward(data, capture=True)
            _, _, hybrid_head_values = hybrid_head.forward(data, capture=True)
            _, _, hybrid_nonhead_values = hybrid_nonhead.forward(data, capture=True)
            add_endpoints(endpoint_totals["parent_g10"], parent_stats, conv_names)
            add_endpoints(endpoint_totals["g20"], g20_stats, conv_names)
            case_layers = {}
            for name in tracked_names:
                parent_int = _dequant(parent_values, parent_integer, name)
                g20_int = _dequant(g20_values, g20_integer, name)
                comparisons = {
                    "g20_integer_vs_parent_integer": error(parent_int, g20_int),
                    "parent_float_vs_original_float": error(original_values[name], parent_float[name]),
                    "g20_float_vs_original_float": error(original_values[name], g20_float[name]),
                    "parent_integer_vs_parent_float": error(parent_float[name], parent_int),
                    "g20_integer_vs_g20_float": error(g20_float[name], g20_int),
                }
                case_layers[name] = comparisons
                for comparison, value in comparisons.items():
                    by_layer[name][comparison].append(value)
                if name in graph["outputs"]:
                    arrays = {
                        "g20_integer_vs_parent_integer": (parent_int, g20_int),
                        "parent_float_vs_original_float": (original_values[name], parent_float[name]),
                        "g20_float_vs_original_float": (original_values[name], g20_float[name]),
                        "parent_integer_vs_parent_float": (parent_float[name], parent_int),
                        "g20_integer_vs_g20_float": (g20_float[name], g20_int),
                    }
                    for comparison, pair in arrays.items():
                        head_rows[comparison][name].append(head_breakdown(*pair))
                    hybrid_rows["g20_with_parent_head_weights_bias"][name].append(head_breakdown(
                        parent_int, _dequant(hybrid_head_values, hybrid_head, name)))
                    hybrid_rows["g20_with_parent_nonhead_weights_bias"][name].append(head_breakdown(
                        parent_int, _dequant(hybrid_nonhead_values, hybrid_nonhead, name)))
            cases.append({"train_index": index, "key": key, "layers": case_layers})
            print(f"train-only G20 drift diagnosis {index + 1}/4", flush=True)

    summary = {name: {comparison: summarized(by_layer[name][comparison])
                      for comparison in COMPARISONS} for name in tracked_names}
    if (any(sha256(path) != digest for path, digest in fixed)
            or any(sha256(base.PROJECT / name) != digest for name, digest in source_hashes.items())):
        raise ValueError("frozen input or diagnostic source changed during inference")
    endpoints = {kind: finalized_endpoints(rows) for kind, rows in endpoint_totals.items()}
    layer_summary = [{"name": name, "comparisons": summary[name],
                      "endpoint_occupancy_not_clipping": {
                          "parent_g10": endpoints["parent_g10"][name], "g20": endpoints["g20"][name]}}
                     for name in conv_names]
    report = {
        "schema_version": 1,
        "status": "completed_train_only_G20_drift_diagnosis_not_accuracy",
        "scope": "fixed first four of 86 training frames; training targets constructed but unused; no validation data read",
        "inputs": {
            "original_fp32_checkpoint_sha256": base.CHECKPOINT_HASH,
            "training_manifest_sha256": snapshot.manifest_sha256,
            "training_content_sha256": snapshot.dataset_content_sha256,
            "parent_checkpoint_sha256": PARENT_CHECKPOINT_SHA256,
            "parent_package_manifest_sha256": PARENT_MANIFEST_SHA256,
            "parent_payload_sha256": parent_manifest["payload_sha256"],
            "g20_checkpoint_sha256": G20_CHECKPOINT_SHA256,
            "g20_package_manifest_sha256": G20_MANIFEST_SHA256,
            "g20_payload_sha256": g20_manifest["payload_sha256"],
            "graph_sha256": parent_identity["graph_sha256"],
            "scales_sha256": parent_identity["scales_sha256"],
            "architecture_hash": parent_identity["architecture_hash"],
        },
        "runtime": {"python": sys.version, "numpy_version": np.__version__,
                    "numpy_file": str(Path(np.__file__).resolve()), "torch_version": torch.__version__,
                    "device": "cpu", "cpu_threads": 2, "cuda_visible_devices": "-1"},
        "sample_identity": sample_rows,
        "sample_identity_sha256": protocol_hash(sample_rows),
        "source_sha256": source_hashes,
        "parent_training_source_identity": parent_identity["source_sha256"],
        "g20_training_source_identity": g20_identity["source_sha256"],
        "actual_head_layout": {"output_to_root": roots, "head_convolution_names": head_names,
                               "nonhead_convolution_count": len(conv_names) - len(head_names)},
        "comparisons": list(COMPARISONS),
        "parameter_differences_parent_g10_to_g20": parameter_differences(
            conv_names, parent_folded, g20_folded, parent_integer, g20_integer),
        "layer_summary": layer_summary,
        "top_layer_errors": {comparison: sorted(
            ({"name": name, **summary[name][comparison]} for name in conv_names),
            key=lambda row: row["normalized_rmse_mean"], reverse=True)[:10]
            for comparison in COMPARISONS},
        "output_head_channel_group_summary": {comparison: {
            name: summarize_breakdowns(rows) for name, rows in heads.items()}
            for comparison, heads in head_rows.items()},
        "controlled_weight_bias_localization": {
            kind: {"restored_layer_names": (head_names if "parent_head" in kind
                                             else [name for name in conv_names if name not in head_set]),
                   "output_drift_vs_parent_g10_integer": {
                       name: summarize_breakdowns(rows) for name, rows in heads.items()}}
            for kind, heads in hybrid_rows.items()},
        "endpoint_occupancy_not_clipping": endpoints,
        "cases": cases,
        "checks": {"identity_bindings_passed": True, "checkpoint_to_package_codes_exact": True,
                   "source_snapshots_precede_inference": True, "optimizer_created": False,
                   "training_updates": 0, "validation_inference": False, "ground_truth_used": False,
                   "candidate_exported": False, "model_selection_performed": False, "gpu_used": False},
        "interpretation_limits": [
            "Endpoint occupancy is not an exact clipping count.",
            "The two in-memory weight/bias restorations keep G20 quantization coefficients and scales; they are diagnostic and not additive.",
            "Output drift attribution on four training frames is not AP causality, accuracy evaluation, candidate selection, or deployment qualification.",
        ],
        "seconds": time.perf_counter() - started,
    }
    base.save(output / "diagnosis.json", report)
    print(json.dumps({"status": report["status"], "output": str(output)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
