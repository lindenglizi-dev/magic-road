"""Evaluate the fixed frozen-Stem G10-to-G20 continuation on development17."""
import argparse
import json
import math
import shutil
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
from cnn.hw_validation.production import train_qat_numpy235 as runtime
from cnn.hw_validation.production.evaluate_qat import (
    BASELINE, BASELINE_HASH, POSTPROCESS, PROJECT, SOURCE, SOURCE_MANIFEST_HASH,
    SOURCE_PTQ_HASH, VALIDATION, VALIDATION_CONTENT_HASH, _delta, read)
from cnn.hw_validation.production.run_trained_integer import CHECKPOINT_HASH, VAL_HASH, centered, save
from cnn.hw_validation.production.trained_integer import load_package

runtime.install()
runner = runtime.continuation
PARENT_EVAL = runner.PARENT_OUT / "evaluation/development17.json"
PARENT_EVAL_HASH = "10052bdaeaff450beb86ad5cd079eaae98df4325ccb2c2a881835d64364be09a"
PARENT_MANIFEST = runner.PARENT_OUT / "package/manifest.json"
PARENT_MANIFEST_HASH = runner.PARENT_ARTIFACTS["package/manifest.json"]
PURPOSE = "QAT_G20_CONTINUATION_DEVELOPMENT_CANDIDATE"
SAMPLES = 22
SOURCES = (
    "cnn/hw_validation/production/evaluate_qat_continuation.py",
    "cnn/hw_validation/production/evaluate_qat.py",
    "cnn/hw_validation/production/train_qat_frozen_stem_continue.py",
    "cnn/hw_validation/production/train_qat_numpy235.py",
    "cnn/hw_validation/production/probe_qat_numpy235.py",
    "cnn/hw_validation/production/trained_integer.py",
    "cnn/evaluate.py", "cnn/metrics.py", "cnn/integer.py", "cnn/train.py")


def _validate_checkpoint(state: Mapping, parent: Mapping, contract: Mapping) -> dict:
    identity, protocol, ancestry = (contract.get(name) for name in
                                    ("identity", "protocol", "ancestry"))
    if not all(isinstance(value, Mapping) for value in (identity, protocol, ancestry)):
        raise ValueError("continuation contract identity, protocol, or ancestry is missing")
    history = state.get("sample_history")
    if (state.get("format") != runner.FORMAT or state.get("checkpoint_kind") != "training"
            or state.get("phase") != "qat" or state.get("candidate") is not True
            or state.get("formal_acceptance") is not False
            or state.get("trained_steps") != runner.STOP or state.get("next_update") != runner.STOP
            or state.get("presentations") != runner.STOP * SAMPLES
            or state.get("segment_start_update") != runner.START
            or state.get("segment_trained_steps") != runner.SEGMENT_UPDATES
            or state.get("segment_presentations") != runner.SEGMENT_UPDATES * SAMPLES
            or state.get("global_qat_updates") != runner.GLOBAL_QAT_UPDATES
            or state.get("actual_samples_per_update") != SAMPLES
            or state.get("gradients_pending") is not False
            or state.get("identity") != identity or state.get("training_protocol") != protocol
            or state.get("ancestry") != ancestry or not isinstance(history, list)
            or len(history) != runner.STOP or history[:runner.START] != parent.get("sample_history")
            or not isinstance(state.get("model"), Mapping) or not state["model"]
            or not isinstance(state.get("optimizer"), Mapping)
            or set(state.get("rng_state", {})) != {"python", "numpy", "torch", "cuda"}
            or not state["rng_state"]["cuda"]):
        raise ValueError("checkpoint is not the completed strict G10-to-G20 continuation")
    if (parent.get("trained_steps") != runner.START or parent.get("presentations") != 220
            or parent.get("identity") != ancestry.get("parent_identity")
            or parent.get("training_protocol") != ancestry.get("parent_training_protocol")
            or ancestry.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or ancestry.get("parent_trained_steps") != runner.START
            or ancestry.get("parent_presentations") != 220
            or ancestry.get("parent_identity_sha256") != protocol_hash(parent["identity"])
            or ancestry.get("parent_training_protocol_sha256") != protocol_hash(parent["training_protocol"])
            or ancestry.get("parent_sample_history_sha256") != protocol_hash(parent["sample_history"])):
        raise ValueError("checkpoint ancestry does not bind the reviewed G10 parent")
    parent_path = str(runner.PARENT.relative_to(PROJECT)).replace("\\", "/")
    transition = identity.get("runtime_transition", {})
    if (ancestry.get("parent_checkpoint") != parent_path
            or identity.get("source_checkpoint_sha256") != CHECKPOINT_HASH
            or identity.get("numpy_version") != "2.3.5"
            or parent["identity"].get("numpy_version") != "2.4.6"
            or transition.get("source_numpy_version") != "2.4.6"
            or transition.get("current_numpy_version") != "2.3.5"
            or transition.get("intentional") is not True
            or transition.get("control_result_sha256") != runtime.CONTROL_RESULT_SHA256
            or transition.get("runtime_receipt_sha256") != runtime.RUNTIME_RECEIPT_SHA256
            or transition.get("cross_runtime_parent_integer_sha256") != runtime.CROSS_RUNTIME_SHA256
            or identity.get("protocol_sha256") != protocol_hash(protocol)
            or identity.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or identity.get("parent_identity") != parent["identity"]
            or identity.get("parent_identity_sha256") != protocol_hash(parent["identity"])
            or identity.get("parent_training_protocol") != parent["training_protocol"]
            or identity.get("parent_training_protocol_sha256") != protocol_hash(parent["training_protocol"])
            or identity.get("parent_sample_history_sha256") != protocol_hash(parent["sample_history"])
            or identity.get("parent_decision_sha256") != runner.PARENT_ARTIFACTS["decision.json"]
            or identity.get("parent_control_comparison_sha256")
            != runner.PARENT_ARTIFACTS["control_comparison.json"]
            or identity.get("parent_export_parity_sha256")
            != runner.PARENT_ARTIFACTS["export_parity.json"]
            or not isinstance(identity.get("source_sha256"), Mapping)
            or not identity["source_sha256"]
            or contract.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or Path(contract.get("source_checkpoint", "")).resolve() != runner.PARENT.resolve()
            or protocol.get("prior_branch_updates") != 10 or protocol.get("segment_updates") != 10
            or protocol.get("total_updates") != 20
            or protocol.get("global_qat_updates_after_segment") != 30
            or protocol.get("overall_budget_cap") != 100 or protocol.get("schedule_cycle") != 2
            or protocol.get("cpu_resume_check_threads") != runtime.CPU_CHECK_THREADS
            or protocol.get("gpu_worker_threads") != 2
            or protocol.get("runtime_transition") != identity.get("runtime_transition")
            or not isinstance(protocol.get("schedule_cycle_sha256"), str)
            or len(protocol["schedule_cycle_sha256"]) != 64
            or protocol.get("actual_samples_per_update") != SAMPLES
            or protocol.get("frozen_layers") != ["stem.conv"]
            or protocol.get("frozen_fields") != ["weight", "bias"]
            or contract.get("segment_start_update") != 10
            or contract.get("planned_segment_updates") != 10
            or contract.get("cumulative_branch_updates") != 20
            or contract.get("global_qat_updates_after_segment") != 30
            or contract.get("overall_qat_budget_cap") != 100
            or contract.get("actual_samples_per_update") != SAMPLES
            or contract.get("automatic_retry") is not False
            or contract.get("automatic_continuation") is not False
            or contract.get("formal_acceptance") is not False):
        raise ValueError("continuation protocol or 30/100 budget accounting differs")
    for index, row in enumerate(history[runner.START:], runner.START):
        lists = [row.get(name) for name in ("indices", "keys", "groups")]
        if (row.get("update") != index + 1 or row.get("schedule_update") != index - 9
                or row.get("schedule_cycle") != 2 or row.get("actual_samples") != SAMPLES
                or row.get("frozen_stem_unchanged") is not True
                or any(not isinstance(value, list) or len(value) != SAMPLES for value in lists)
                or not all(math.isfinite(float(row.get(name, math.nan)))
                           for name in ("loss", "gradient_norm_before_clip"))):
            raise ValueError(f"continuation history invalid at branch update {index + 1}")
    for field in ("layers.0.weight", "layers.0.bias"):
        if field not in state["model"] or field not in parent["model"] \
                or not torch.equal(state["model"][field], parent["model"][field]):
            raise ValueError("frozen Stem differs from the G10 parent")
    return dict(identity)


def _validate_package(manifest: Mapping, parent_manifest: Mapping, identity: Mapping,
                      checkpoint_hash: str) -> None:
    provenance = manifest.get("provenance", {})
    if (manifest.get("graph") != parent_manifest.get("graph")
            or manifest.get("scales") != parent_manifest.get("scales")
            or manifest.get("generator_sha256") != identity.get("source_sha256", {}).get(
                "cnn/hw_validation/production/trained_integer.py")
            or provenance.get("purpose") != PURPOSE
            or provenance.get("checkpoint_sha256") != checkpoint_hash
            or provenance.get("source_checkpoint_sha256") != CHECKPOINT_HASH
            or provenance.get("trained_steps") != 20
            or provenance.get("cumulative_qat_updates") != 20
            or provenance.get("global_qat_updates") != 30
            or provenance.get("segment_qat_updates") != 10
            or provenance.get("identity") != identity
            or provenance.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or provenance.get("parent_identity") != identity.get("parent_identity")
            or provenance.get("qat_exact_fixed_weight_scales") is not True):
        raise ValueError("package is not bound to the completed G20 continuation")


def _continuation_gate(candidate: Mapping, parent: Mapping) -> dict:
    delta = _delta(candidate, parent)
    ap50 = {name: candidate["classes"][name]["ap50"] >= parent["classes"][name]["ap50"]
            for name in ("person", "vehicle")}
    recall = {name: candidate["classes"][name]["recall"] >= parent["classes"][name]["recall"]
              for name in ("person", "vehicle")}
    mean_gain = sum(delta[name]["ap50"] for name in ("person", "vehicle")) / 2
    return {"class_ap50_not_below_parent": ap50, "class_recall_at_0_5_not_below_parent": recall,
            "mean_ap50_gain_pp_vs_parent": mean_gain,
            "passed": all(ap50.values()) and all(recall.values()) and mean_gain >= 1.0}


def _snapshot_sources(output: Path) -> dict:
    folder = output / "source_snapshot"
    folder.mkdir()
    hashes = {}
    for index, relative in enumerate(SOURCES):
        source, target = PROJECT / relative, folder / f"{index:02d}_{Path(relative).name}"
        before = sha256(source)
        shutil.copyfile(source, target)
        if sha256(target) != before or sha256(source) != before:
            raise ValueError(f"evaluation source changed while snapshotting: {relative}")
        hashes[relative] = before
    save(output / "source_snapshot.json", {"status": "PRE_INFERENCE_SOURCE_SNAPSHOT",
        "source_sha256": hashes, "snapshot_files": sorted(path.name for path in folder.iterdir())})
    return hashes


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
              (runner.PARENT, runner.PARENT_SHA256), (PARENT_EVAL, PARENT_EVAL_HASH),
              (PARENT_MANIFEST, PARENT_MANIFEST_HASH))
    for path, expected in frozen:
        if sha256(path) != expected:
            raise ValueError(f"frozen continuation evaluation input changed: {path}")
    baseline, ptq, parent_eval = (read(path) for path in
                                  (BASELINE, SOURCE / "development17.json", PARENT_EVAL))
    for name, reference in (("initial PTQ", ptq), ("parent G10", parent_eval)):
        if (reference.get("image_count") != 17 or reference.get("dataset_sha256") != VAL_HASH
                or reference.get("evaluated_image_content_sha256") != VALIDATION_CONTENT_HASH
                or reference.get("postprocess_contract") != POSTPROCESS
                or reference.get("truth") != baseline.get("truth")
                or reference.get("ignores") != baseline.get("ignores")):
            raise ValueError(f"{name} development17 identity differs")
    if parent_eval.get("input_hashes", {}).get("checkpoint_sha256") != runner.PARENT_SHA256:
        raise ValueError("parent G10 evaluation is not bound to the continuation parent")

    parent = torch.load(runner.PARENT, map_location="cpu", weights_only=False)
    state = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    contract = read(runner.OUT / "training_contract.json")
    checkpoint_hash = sha256(args.checkpoint)
    identity = _validate_checkpoint(state, parent, contract)
    transition = identity.get("runtime_transition", {})
    if (identity.get("native_runtime") != runner.native_runtime_identity()
            or transition.get("cache_receipt_sha256") != sha256(runner.OUT / "cache_receipt.json")):
        raise ValueError("NumPy 2.3.5 runtime transition identity or receipt differs")
    if identity.get("native_runtime") != runner.native_runtime_identity():
        raise ValueError("evaluation native runtime differs from the continuation")
    if (identity.get("torch_version") != torch.__version__
            or identity.get("numpy_version") != np.__version__
            or identity.get("python_executable_sha256") != sha256(Path(sys._base_executable))):
        raise ValueError("evaluation runtime differs from the continuation runtime")
    for relative, expected in identity["source_sha256"].items():
        path = (PROJECT / relative).resolve()
        if not path.is_relative_to(PROJECT.resolve()) or sha256(path) != expected:
            raise ValueError(f"continuation training source changed: {relative}")
    integer, manifest = load_package(args.package)
    parent_manifest = read(PARENT_MANIFEST)
    _validate_package(manifest, parent_manifest, identity, checkpoint_hash)
    gate, parity, execution = (read(path) for path in (
        runner.CHECK_DIR / "CPU_resume_check.json", runner.OUT / "export_parity.json",
        runner.OUT / "execution/report.json"))
    if (gate.get("passed") is not True or gate.get("identity") != identity
            or gate.get("protocol") != state["training_protocol"]
            or gate.get("ancestry") != state["ancestry"]
            or gate.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or gate.get("parent_optimizer_momentum_states") != 132
            or gate.get("parent_history_rows") != 10
            or gate.get("continuous_global_updates") != [11, 12]
            or gate.get("resumed_global_update") != 12
            or gate.get("resumed_second_update_exact") is not True
            or gate.get("cumulative_presentations") != 264
            or gate.get("schedule_cycle") != 2
            or gate.get("schedule_cycle_sha256") != state["training_protocol"]["schedule_cycle_sha256"]
            or gate.get("cpu_rng_streams_compared") != ["python", "numpy", "torch"]
            or gate.get("parent_cpu_rng_restored") is not True
            or gate.get("cpu_threads") != state["training_protocol"].get("cpu_resume_check_threads")
            or gate.get("negative_cases") != 4 or gate.get("optimizer_updates_published") != 0
            or gate.get("candidate_training_started") is not False
            or gate.get("cuda_initialized") is not False
            or parity.get("passed") is not True or parity.get("checkpoint_sha256") != checkpoint_hash
            or parity.get("payload_sha256") != manifest["payload_sha256"]
            or parity.get("trace_tensors") != 181
            or parity.get("trained_steps") != 20 or parity.get("global_qat_updates") != 30
            or parity.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or parity.get("identity") != identity or parity.get("formal_acceptance") is not False
            or execution.get("status") != "completed_frozen_stem_qat_G20"
            or execution.get("checkpoint_sha256") != checkpoint_hash
            or execution.get("saved_updates") != 20 or execution.get("global_qat_updates") != 30
            or execution.get("all_saved_Stem_states_unchanged") is not True
            or execution.get("parent_checkpoint_unchanged") is not True
            or execution.get("sources_unchanged") is not True
            or execution.get("formal_acceptance") is not False):
        raise ValueError("continuation restore, export, or execution gate is stale or failed")

    rows, total = load_validation_subset(VALIDATION, None, 17)
    dataset = FullFrameDataset(rows, "val")
    content_hash = dataset_content_hash(dataset.rows)
    if total != 17 or content_hash != VALIDATION_CONTENT_HASH:
        raise ValueError("development17 selection changed")
    args.output.mkdir(parents=True)
    source_hashes = _snapshot_sources(args.output)
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
                            "score": item["score_uint16"] / 65536} for item in detections)
        truth.extend({"image_id": row["image"], "label": label, "box": box}
                     for label, box in zip(row["labels"], row["boxes"], strict=True))
        metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
        ignores.extend({"image_id": row["image"], "label": region["label"], "box": box,
                        "crowd": region["crowd"]}
                       for box, region in zip(row["ignore_boxes"], metadata, strict=True))
        print(f"G20 integer development validation {index + 1}/17 ({timings[-1]:.2f}s CPU forward)", flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("development17 GT or ignore protocol changed")
    if any(sha256(PROJECT / name) != digest for name, digest in source_hashes.items()):
        raise ValueError("evaluation source changed after the pre-inference snapshot")

    metrics = report(predictions, truth, ignores, thresholds=(.5, .5))
    references = {"parent_frozen_stem_G10": parent_eval["diagnostic_metrics_at_0_5"],
                  "FP32_replay_G10": baseline["diagnostic_metrics_at_0_5"],
                  "initial_maxabs_PTQ": ptq["diagnostic_metrics_at_0_5"]}
    deltas = {name: _delta(metrics, value) for name, value in references.items()}
    continuation = _continuation_gate(metrics, references["parent_frozen_stem_G10"])
    inputs = {"checkpoint_sha256": checkpoint_hash,
              "candidate_manifest_sha256": sha256(args.package / "manifest.json"),
              "candidate_payload_sha256": manifest["payload_sha256"],
              "candidate_physical_sha256": manifest["physical_sha256"],
              "parent_checkpoint_sha256": runner.PARENT_SHA256,
              "parent_evaluation_sha256": PARENT_EVAL_HASH,
              "parent_manifest_sha256": PARENT_MANIFEST_HASH,
              "validation_dataset_sha256": VAL_HASH,
              "evaluated_image_content_sha256": content_hash,
              "fp32_baseline_sha256": BASELINE_HASH,
              "maxabs_ptq_report_sha256": SOURCE_PTQ_HASH,
              "source_package_manifest_sha256": SOURCE_MANIFEST_HASH}
    inputs.update(numpy235_control_result_sha256=runtime.CONTROL_RESULT_SHA256,
                  numpy235_runtime_receipt_sha256=runtime.RUNTIME_RECEIPT_SHA256,
                  cross_runtime_parent_integer_sha256=runtime.CROSS_RUNTIME_SHA256,
                  transition_cache_receipt_sha256=sha256(runner.OUT / "cache_receipt.json"))
    result = {"status": "QAT_G20_CONTINUATION_DEVELOPMENT17_DIAGNOSTIC",
        "scope": "same17_development_only_not_formal_acceptance", "image_count": 17,
        "dataset_sha256": VAL_HASH, "evaluated_image_content_sha256": content_hash,
        "postprocess_contract": POSTPROCESS, "diagnostic_metrics_at_0_5": metrics,
        "delta_pp_vs_parent_frozen_stem_G10": deltas["parent_frozen_stem_G10"],
        "delta_pp_vs_FP32": deltas["FP32_replay_G10"],
        "delta_pp_vs_initial_maxabs_PTQ": deltas["initial_maxabs_PTQ"],
        "references": references, "predictions": predictions, "truth": truth, "ignores": ignores,
        "cpu_forward_seconds": timings, "input_hashes": inputs, "training_identity": identity,
        "ancestry": state["ancestry"], "evaluation_source_sha256": source_hashes,
        "acceptance_eligible": False, "formal_acceptance": False,
        "automatic_continuation_authorized": False,
        "limitation": "same 17 development frames; no independent or formal acceptance"}
    save(args.output / "development17.json", result)
    save(args.output / "saturation_diagnostics.json", statistics)
    save(args.output / "evaluation_gate.json", {
        "status": "PASS_G20_CONTINUATION_GATE" if continuation["passed"] else "FAIL_G20_CONTINUATION_GATE",
        "criteria_frozen_before_candidate_results": True,
        "scope": "same17_development_budget_diagnostic_not_formal_acceptance",
        "criteria": {"each_class_ap50_not_below_parent_G10": True,
                     "mean_ap50_gain_vs_parent_G10_at_least_pp": 1.0,
                     "each_class_recall_at_0_5_not_below_parent_G10": True},
        "observed": continuation, "continuation_gate_passed": continuation["passed"],
        "old256_new_model_only_followup_eligible": continuation["passed"],
        "automatic_followup_started": False, "new_user_authorization_required": True,
        "formal_acceptance": False})
    save(args.output / "status.json", {"status": "completed_QAT_G20_continuation_development17",
        "input_hashes": inputs, "cpu_only": True, "cuda_initialized": torch.cuda.is_initialized(),
        "training_started": False, "image_count": 17, "full_integer_forward": True,
        "metrics_at_score_0_5": metrics, "continuation_gate_passed": continuation["passed"],
        "automatic_followup_started": False, "formal_acceptance": False,
        "seconds": time.perf_counter() - started})
    print(json.dumps({"metrics": metrics, "deltas": deltas,
                      "continuation_gate": continuation}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
