"""Evaluate one exported QAT package on the frozen replay-G10 development17."""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections.abc import Mapping
from pathlib import Path

import numpy as np
import torch

from cnn.evaluate import load_validation_subset
from cnn.integer import postprocess
from cnn.metrics import report
from cnn.train import FullFrameDataset, dataset_content_hash, protocol_hash, sha256
from cnn.hw_validation.production.run_trained_integer import (
    BASELINE, CHECKPOINT_HASH, PROJECT, TRAIN_HASH, VALIDATION, VAL_HASH, centered, save)
from cnn.hw_validation.production.trained_integer import load_package

SOURCE = PROJECT / "cnn/reports/replay_g10_integer_20261013_v2"
SOURCE_PACKAGE = SOURCE / "package"
SOURCE_MANIFEST_HASH = "64ad4e3284c4fdf90fa9f9ddc468db00159c46b152a13d440753030a979624f9"
SOURCE_PTQ_HASH = "c3ef17250ff7568f197060a8ff6f94423037266599b0113d789ad6164457dbb3"
BASELINE_HASH = "fc70c1afe78b45ceb2c5d8e17076586aa353fb6fd4bcd474122cf9094e6296b2"
VALIDATION_CONTENT_HASH = "373af83998b9cf08f9ba3715416415486c82ec050df8cbab2aefb5835876e3d0"
FORMAT = "road-qat-resume-v1"
UPDATES = 10
SAMPLES_PER_UPDATE = 22
PURPOSE = "QAT_G10_DEVELOPMENT_CANDIDATE"
POSTPROCESS = {"top_k_per_class": 128, "max_boxes_per_class": 32,
               "nms_iou": 0.5, "score_floor_uint16": 3276}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_checkpoint(state: Mapping, source_manifest: Mapping,
                         baseline: Mapping) -> dict:
    count = state.get("trained_steps")
    history = state.get("sample_history")
    if (state.get("format") != FORMAT or state.get("checkpoint_kind") != "training"
            or state.get("phase") != "qat" or state.get("candidate") is not True
            or state.get("formal_acceptance") is not False
            or type(count) is not int or count != UPDATES
            or state.get("next_update") != count
            or state.get("presentations") != count * SAMPLES_PER_UPDATE
            or state.get("actual_samples_per_update") != SAMPLES_PER_UPDATE
            or state.get("gradients_pending") is not False
            or not isinstance(history, list) or len(history) != count
            or not isinstance(state.get("model"), Mapping) or not state["model"]
            or not isinstance(state.get("optimizer"), Mapping)
            or not isinstance(state.get("rng_state"), Mapping)):
        raise ValueError("checkpoint is not a completed 10-update QAT candidate")
    for update, row in enumerate(history, 1):
        lists = [row.get(name) for name in ("indices", "keys", "groups")]
        if (row.get("update") != update or row.get("actual_samples") != SAMPLES_PER_UPDATE
                or any(not isinstance(value, list) or len(value) != SAMPLES_PER_UPDATE
                       for value in lists)
                or not all(math.isfinite(float(row.get(name, math.nan)))
                           for name in ("loss", "gradient_norm_before_clip"))):
            raise ValueError(f"checkpoint sample history invalid at update {update}")
    identity = state.get("identity")
    protocol = state.get("training_protocol")
    expected = {
        "source_checkpoint_sha256": CHECKPOINT_HASH,
        "architecture_hash": baseline["architecture_hash"],
        "dataset_sha256": TRAIN_HASH,
        "dataset_content_sha256": source_manifest["provenance"]["calibration_content_sha256"],
        "graph_sha256": protocol_hash(source_manifest["graph"]),
        "scales_sha256": protocol_hash(source_manifest["scales"]),
        "source_package_manifest_sha256": SOURCE_MANIFEST_HASH,
        "source_payload_sha256": source_manifest["payload_sha256"],
        "quantization_sha256": source_manifest["provenance"]["quantization_sha256"],
    }
    if (not isinstance(identity, Mapping) or not isinstance(protocol, Mapping)
            or any(identity.get(name) != value for name, value in expected.items())
            or identity.get("protocol_sha256") != protocol_hash(dict(protocol))
            or not isinstance(identity.get("source_sha256"), Mapping)
            or not identity["source_sha256"]
            or protocol.get("total_updates") != UPDATES
            or protocol.get("actual_samples_per_update") != SAMPLES_PER_UPDATE):
        raise ValueError("checkpoint identity or training protocol differs from frozen QAT inputs")
    return dict(identity)


def _validate_candidate(manifest: Mapping, source_manifest: Mapping, identity: Mapping,
                        checkpoint_hash: str) -> None:
    provenance = manifest.get("provenance", {})
    if (manifest.get("graph") != source_manifest.get("graph")
            or manifest.get("scales") != source_manifest.get("scales")
            or manifest.get("generator_sha256") != identity.get("source_sha256", {}).get(
                "cnn/hw_validation/production/trained_integer.py")
            or provenance.get("purpose") != PURPOSE
            or provenance.get("checkpoint_sha256") != checkpoint_hash
            or provenance.get("source_checkpoint_sha256") != CHECKPOINT_HASH
            or provenance.get("trained_steps") != UPDATES
            or provenance.get("identity") != identity
            or provenance.get("qat_exact_fixed_weight_scales") is not True):
        raise ValueError("exported package is not bound to the supplied completed QAT checkpoint")


def _validate_support_gates(package: Path, state: Mapping, identity: Mapping,
                            manifest: Mapping, checkpoint_hash: str) -> None:
    resume = read(package.parent / "integration_check_v2/CPU_resume_check.json")
    exported = read(package.parent / "export_parity.json")
    if (resume.get("passed") is not True or resume.get("identity") != identity
            or resume.get("protocol") != state["training_protocol"]
            or resume.get("continuous_updates") != 2
            or resume.get("resumed_second_update_exact") is not True
            or resume.get("presentations") != 44 or resume.get("negative_cases") != 4
            or resume.get("candidate_training_started") is not False
            or resume.get("cuda_initialized") is not False):
        raise ValueError("QAT checkpoint restore gate missing, stale, or failed")
    if (exported.get("passed") is not True or exported.get("identity") != identity
            or exported.get("checkpoint_sha256") != checkpoint_hash
            or exported.get("payload_sha256") != manifest["payload_sha256"]
            or exported.get("formal_acceptance") is not False):
        raise ValueError("QAT updated-weight export parity gate missing, stale, or failed")


def _delta(candidate: Mapping, reference: Mapping) -> dict:
    return {name: {field: 100 * (candidate["classes"][name][field]
                                  - reference["classes"][name][field])
                   for field in ("precision", "recall", "ap50", "ap50_95")}
            for name in ("person", "vehicle")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    started = time.perf_counter()

    frozen = ((VALIDATION, VAL_HASH), (BASELINE, BASELINE_HASH),
              (SOURCE / "development17.json", SOURCE_PTQ_HASH),
              (SOURCE_PACKAGE / "manifest.json", SOURCE_MANIFEST_HASH))
    for path, expected in frozen:
        if sha256(path) != expected:
            raise ValueError(f"frozen evaluation input changed: {path}")
    baseline, old_ptq = read(BASELINE), read(SOURCE / "development17.json")
    source_manifest = read(SOURCE_PACKAGE / "manifest.json")
    if (baseline.get("checkpoint_sha256") != CHECKPOINT_HASH
            or baseline.get("dataset_sha256") != VAL_HASH
            or baseline.get("evaluated_image_content_sha256") != VALIDATION_CONTENT_HASH
            or baseline.get("image_count") != 17
            or baseline.get("postprocess_contract") != POSTPROCESS
            or old_ptq.get("checkpoint_sha256") != CHECKPOINT_HASH
            or old_ptq.get("dataset_sha256") != VAL_HASH
            or old_ptq.get("evaluated_image_content_sha256") != VALIDATION_CONTENT_HASH
            or old_ptq.get("baseline_sha256") != BASELINE_HASH
            or old_ptq.get("postprocess_contract") != POSTPROCESS
            or old_ptq.get("truth") != baseline.get("truth")
            or old_ptq.get("ignores") != baseline.get("ignores")):
        raise ValueError("FP32 or maxabs PTQ development17 baseline identity mismatch")

    checkpoint_hash = sha256(args.checkpoint)
    # This evaluator accepts only trusted local training artifacts; map all tensors to CPU.
    state = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    identity = _validate_checkpoint(state, source_manifest, baseline)
    if (identity.get("torch_version") != torch.__version__
            or identity.get("numpy_version") != np.__version__
            or identity.get("python_executable_sha256") != sha256(Path(sys._base_executable))):
        raise ValueError("evaluation runtime differs from the frozen QAT runtime")
    for name, expected in identity["source_sha256"].items():
        path = (PROJECT / name).resolve()
        if not path.is_relative_to(PROJECT.resolve()) or sha256(path) != expected:
            raise ValueError(f"QAT training source changed: {name}")
    integer, manifest = load_package(args.package)
    _validate_candidate(manifest, source_manifest, identity, checkpoint_hash)
    _validate_support_gates(args.package, state, identity, manifest, checkpoint_hash)

    rows, total = load_validation_subset(VALIDATION, None, 17)
    dataset = FullFrameDataset(rows, "val")
    content_hash = dataset_content_hash(dataset.rows)
    if total != 17 or content_hash != VALIDATION_CONTENT_HASH:
        raise ValueError("development17 image content or selection changed")

    args.output.mkdir(parents=True, exist_ok=False)
    predictions, truth, ignores, timings, statistics = [], [], [], [], []
    for index, row in enumerate(dataset.rows):
        image, _, _ = dataset[index]
        stage = time.perf_counter()
        heads, stats, _ = integer.forward(centered(image))
        timings.append(time.perf_counter() - stage)
        statistics.append({"image": row["image"], "nodes": stats})
        detections = postprocess(heads, (POSTPROCESS["score_floor_uint16"],) * 2,
                                 POSTPROCESS["top_k_per_class"], POSTPROCESS["max_boxes_per_class"])
        predictions.extend({"image_id": row["image"], "label": item["label"],
                            "box": [value / 256 for value in item["box_q8"]],
                            "score": item["score_uint16"] / 65536}
                           for item in detections)
        truth.extend({"image_id": row["image"], "label": label, "box": box}
                     for label, box in zip(row["labels"], row["boxes"], strict=True))
        metadata = row.get("ignore_metadata",
                           [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
        ignores.extend({"image_id": row["image"], "label": region["label"], "box": box,
                        "crowd": region["crowd"]}
                       for box, region in zip(row["ignore_boxes"], metadata, strict=True))
        print(f"QAT integer development validation {index + 1}/17 "
              f"({timings[-1]:.2f}s CPU forward)", flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("development17 GT or ignore protocol changed")

    metrics = report(predictions, truth, ignores, thresholds=(.5, .5))
    fp32 = baseline["diagnostic_metrics_at_0_5"]
    ptq = old_ptq["diagnostic_metrics_at_0_5"]
    delta_fp32, delta_ptq = _delta(metrics, fp32), _delta(metrics, ptq)
    mean_gain_ptq = sum(delta_ptq[name]["ap50"] for name in ("person", "vehicle")) / 2
    mean_drop_fp32 = -sum(delta_fp32[name]["ap50"] for name in ("person", "vehicle")) / 2
    class_ap50_not_below_ptq = {
        name: metrics["classes"][name]["ap50"] >= ptq["classes"][name]["ap50"]
        for name in ("person", "vehicle")}
    restoration_passed = all(class_ap50_not_below_ptq.values()) and mean_gain_ptq >= 1.
    sources = ["cnn/hw_validation/production/evaluate_qat.py",
               "cnn/hw_validation/production/trained_integer.py", "cnn/evaluate.py",
               "cnn/metrics.py", "cnn/integer.py", "cnn/train.py"]
    input_hashes = {
        "checkpoint_sha256": checkpoint_hash,
        "candidate_manifest_sha256": sha256(args.package / "manifest.json"),
        "candidate_payload_sha256": manifest["payload_sha256"],
        "candidate_physical_sha256": manifest["physical_sha256"],
        "validation_dataset_sha256": VAL_HASH,
        "evaluated_image_content_sha256": content_hash,
        "fp32_baseline_sha256": BASELINE_HASH,
        "maxabs_ptq_report_sha256": SOURCE_PTQ_HASH,
        "source_package_manifest_sha256": SOURCE_MANIFEST_HASH,
    }
    result = {
        "status": "QAT_G10_development17_diagnostic_not_formal_acceptance",
        "inference": "exported_QAT_INT8_CNN_INT32_bias_acc_INT16_Q7.8_heads_fixed_postprocess",
        "image_count": 17, "dataset_sha256": VAL_HASH,
        "evaluated_image_content_sha256": content_hash,
        "postprocess_contract": POSTPROCESS, "diagnostic_metrics_at_0_5": metrics,
        "delta_pp_vs_FP32": delta_fp32,
        "delta_pp_vs_maxabs_PTQ": delta_ptq,
        "references": {"FP32_replay_G10": fp32, "maxabs_PTQ": ptq},
        "predictions": predictions, "truth": truth, "ignores": ignores,
        "cpu_forward_seconds": timings, "input_hashes": input_hashes,
        "training_identity": identity,
        "source_sha256": {name: sha256(PROJECT / name) for name in sources},
        "acceptance_eligible": False, "formal_acceptance": False,
        "limitation": (baseline["limitation"]
                       + "; same 17 development frames only; QAT candidate is not independent acceptance"),
    }
    save(args.output / "development17.json", result)
    save(args.output / "saturation_diagnostics.json", statistics)
    save(args.output / "evaluation_gate.json", {
        "status": ("PASS_QAT_G10_DEVELOPMENT17_RESTORATION"
                   if restoration_passed else "FAIL_QAT_G10_DEVELOPMENT17_RESTORATION"),
        "criteria_frozen_before_candidate_results": True,
        "scope": "same17_development_budget_continuation_diagnostic_not_final_acceptance",
        "required_gates": {"numeric_package_and_full_integer_forward": True,
                           "checkpoint_restore": True, "training_sources": True,
                           "updated_weight_export_parity": True},
        "recovery_criteria": {
            "each_class_ap50_not_below_initial_maxabs_PTQ": True,
            "mean_ap50_gain_vs_initial_maxabs_PTQ_at_least_pp": 1.0,
        },
        "observed": {"class_ap50_not_below_initial_maxabs_PTQ": class_ap50_not_below_ptq,
                     "mean_ap50_gain_pp_vs_initial_maxabs_PTQ": mean_gain_ptq,
                     "mean_ap50_drop_pp_vs_FP32": mean_drop_fp32,
                     "formal_quantization_drop_at_most_1pp": mean_drop_fp32 <= 1.},
        "restoration_passed": restoration_passed,
        "old256_continuation_eligible": restoration_passed,
        "formal_acceptance": False,
    })
    save(args.output / "status.json", {
        "status": "completed_QAT_G10_exported_package_development17_evaluation",
        "input_hashes": input_hashes, "cpu_only": True,
        "cuda_initialized": torch.cuda.is_initialized(), "training_started": False,
        "full_integer_forward": True, "image_count": 17,
        "metrics_at_score_0_5": metrics,
        "delta_pp_vs_FP32": result["delta_pp_vs_FP32"],
        "delta_pp_vs_maxabs_PTQ": result["delta_pp_vs_maxabs_PTQ"],
        "restoration_passed": restoration_passed,
        "old256_continuation_eligible": restoration_passed,
        "formal_quantization_drop_at_most_1pp": mean_drop_fp32 <= 1.,
        "production_release": False, "RTL_compared": False,
        "formal_acceptance": False, "seconds": time.perf_counter() - started,
    })
    print(json.dumps({"metrics": metrics, "delta_pp_vs_FP32": result["delta_pp_vs_FP32"],
                      "delta_pp_vs_maxabs_PTQ": result["delta_pp_vs_maxabs_PTQ"]},
                     ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
