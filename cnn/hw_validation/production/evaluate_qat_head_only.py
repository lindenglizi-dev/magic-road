"""Evaluate the authorized head-only H5 package on frozen development17."""
from __future__ import annotations

import argparse
import json
import os
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
from cnn.hw_validation.production import train_qat_head_only as runner
from cnn.hw_validation.production.evaluate_qat import (
    BASELINE, BASELINE_HASH, POSTPROCESS, PROJECT, SOURCE, SOURCE_MANIFEST_HASH,
    SOURCE_PTQ_HASH, VALIDATION, VALIDATION_CONTENT_HASH, _delta, read)
from cnn.hw_validation.production.run_trained_integer import CHECKPOINT_HASH, VAL_HASH, centered, save
from cnn.hw_validation.production.trained_integer import load_package

PARENT_EVAL = runner.frozen.OUT / "evaluation/development17.json"
PARENT_EVAL_HASH = "10052bdaeaff450beb86ad5cd079eaae98df4325ccb2c2a881835d64364be09a"
PARENT_MANIFEST = runner.frozen.OUT / "package/manifest.json"
PARENT_MANIFEST_HASH = runner.continuation.PARENT_ARTIFACTS["package/manifest.json"]
PURPOSE = "QAT_HEAD_ONLY_G5_DEVELOPMENT_CANDIDATE"
SOURCES = (
    "cnn/hw_validation/production/evaluate_qat_head_only.py",
    "cnn/hw_validation/production/test_evaluate_qat_head_only.py",
    "cnn/hw_validation/production/evaluate_qat.py",
    "cnn/hw_validation/production/train_qat_head_only.py",
    "cnn/hw_validation/production/train_qat_numpy235.py",
    "cnn/hw_validation/production/train_qat_frozen_stem_continue.py",
    "cnn/hw_validation/production/diagnose_qat_continuation_drift.py",
    "cnn/hw_validation/production/trained_integer.py",
    "cnn/evaluate.py", "cnn/metrics.py", "cnn/integer.py", "cnn/train.py")


def _gate(candidate: Mapping, parent: Mapping) -> dict:
    delta = _delta(candidate, parent)
    ap50 = {name: candidate["classes"][name]["ap50"] >= parent["classes"][name]["ap50"]
            for name in ("person", "vehicle")}
    recall = {name: candidate["classes"][name]["recall"] >= parent["classes"][name]["recall"]
              for name in ("person", "vehicle")}
    mean_gain = sum(delta[name]["ap50"] for name in ("person", "vehicle")) / 2
    return {"class_ap50_not_below_parent": ap50,
            "class_recall_at_0_5_not_below_parent": recall,
            "mean_ap50_gain_pp_vs_parent": mean_gain,
            "passed": all(ap50.values()) and all(recall.values()) and mean_gain >= 1.0}


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
            or provenance.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or provenance.get("trained_steps") != runner.UPDATES
            or provenance.get("local_head_only_updates") != runner.UPDATES
            or provenance.get("global_qat_updates") != runner.GLOBAL_UPDATES
            or provenance.get("identity") != identity
            or provenance.get("trainable_parameter_tensors") != 42
            or provenance.get("frozen_parameter_tensors") != 92
            or provenance.get("qat_exact_fixed_weight_scales") is not True):
        raise ValueError("package is not bound to completed head-only H5")


def _snapshot_sources(output: Path, training_sources: Mapping) -> dict:
    folder = output / "source_snapshot"
    folder.mkdir()
    hashes = {}
    for index, relative in enumerate(SOURCES):
        source, target = PROJECT / relative, folder / f"{index:02d}_{Path(relative).name}"
        digest = sha256(source)
        shutil.copyfile(source, target)
        if sha256(source) != digest or sha256(target) != digest:
            raise ValueError(f"evaluation source changed while snapshotting: {relative}")
        hashes[relative] = digest
    save(output / "source_snapshot.json", {
        "status": "PRE_INFERENCE_SOURCE_SNAPSHOT", "evaluation_source_sha256": hashes,
        "training_source_sha256": dict(training_sources),
        "snapshot_files": sorted(path.name for path in folder.iterdir())})
    return hashes


def _validate_training_snapshots(training_sources: Mapping) -> None:
    for folder in (runner.CHECK_DIR / "sources", runner.OUT / "execution/sources"):
        if not folder.is_dir():
            raise ValueError(f"missing training source snapshot: {folder}")
        expected_names = []
        for index, (relative, digest) in enumerate(training_sources.items()):
            snapshot = folder / f"{index}_{Path(relative).name}"
            expected_names.append(snapshot.name)
            if sha256(snapshot) != digest:
                raise ValueError(f"training source snapshot differs: {snapshot}")
        if sorted(path.name for path in folder.iterdir()) != sorted(expected_names):
            raise ValueError(f"training source snapshot membership differs: {folder}")


def _report_ancestry(ancestry: Mapping) -> dict:
    result = dict(ancestry)
    streams = result.pop("parent_rng_state", None)
    if not isinstance(streams, Mapping) or set(streams) != {"python", "numpy", "torch", "cuda"}:
        raise ValueError("validated ancestry lost parent RNG streams")
    result["parent_rng_state"] = {
        "binding": "exact_values_validated_by_runner_validate_state_not_serialized",
        "parent_checkpoint_sha256": runner.PARENT_SHA256,
        "stream_names": ["python", "numpy", "torch", "cuda"]}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    if (os_value := os.environ.get("PYTORCH_NVML_BASED_CUDA_CHECK")) != "1":
        raise ValueError(f"PYTORCH_NVML_BASED_CUDA_CHECK must be 1, got {os_value!r}")
    if (os.environ.get("CUDA_VISIBLE_DEVICES") != "-1"
            or torch.cuda.is_available() or torch.cuda.is_initialized()):
        raise RuntimeError("evaluation requires CUDA_VISIBLE_DEVICES=-1")
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    started = time.perf_counter()
    frozen = ((VALIDATION, VAL_HASH), (BASELINE, BASELINE_HASH),
              (SOURCE / "development17.json", SOURCE_PTQ_HASH),
              (runner.PARENT, runner.PARENT_SHA256), (PARENT_EVAL, PARENT_EVAL_HASH),
              (PARENT_MANIFEST, PARENT_MANIFEST_HASH))
    for path, expected in frozen:
        if sha256(path) != expected:
            raise ValueError(f"frozen head-only evaluation input changed: {path}")
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
        raise ValueError("parent evaluation is not bound to frozen-Stem G10")

    dataset_train, window, _folded, identity, protocol, ancestry, parent = runner.prepare()
    state = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    runner.validate_state(state, identity, protocol, ancestry, parent,
                          dataset_train, window, candidate=True)
    checkpoint_hash = sha256(args.checkpoint)
    update_h5 = runner.RUN / f"update_H{runner.UPDATES}.pt"
    if (args.checkpoint.resolve() != (runner.RUN / "last.pt").resolve()
            or checkpoint_hash != sha256(update_h5)
            or state.get("local_trained_steps") != runner.UPDATES
            or state.get("trained_steps") != runner.UPDATES
            or state.get("next_update") != runner.UPDATES
            or state.get("next_local_update") != runner.UPDATES
            or state.get("local_update_label") != f"H{runner.UPDATES}"
            or state.get("presentations") != runner.UPDATES * protocol["actual_samples_per_update"]
            or state.get("global_qat_updates") != runner.GLOBAL_UPDATES
            or len(state.get("sample_history", [])) != runner.UPDATES
            or len(state.get("optimizer", {}).get("state", {})) != 42
            or len(identity.get("trainable_parameter_names", [])) != 42
            or len(identity.get("frozen_parameter_names", [])) != 92
            or identity.get("optimizer_name_mapping_sha256")
            != protocol_hash(identity.get("optimizer_name_mapping"))
            or ancestry.get("parent_identity", {}).get("numpy_version") != "2.4.6"):
        raise ValueError("final H5 cursor, optimizer, freeze, or parent binding differs")
    contract = read(runner.OUT / "training_contract.json")
    ancestry_receipt = contract.get("ancestry_receipt", {})
    if (contract.get("identity") != identity or contract.get("protocol") != protocol
            or ancestry_receipt.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or ancestry_receipt.get("parent_identity_sha256") != identity["parent_identity_sha256"]
            or ancestry_receipt.get("parent_sample_history_sha256") != identity["parent_sample_history_sha256"]
            or set(ancestry_receipt.get("parent_rng_streams", [])) != {"python", "numpy", "torch", "cuda"}
            or contract.get("planned_local_updates") != runner.UPDATES
            or contract.get("prior_global_qat_updates") != runner.PRIOR_GLOBAL_UPDATES
            or contract.get("global_qat_updates_after_segment") != runner.GLOBAL_UPDATES
            or contract.get("overall_qat_budget_cap") != protocol["overall_budget_cap"]
            or contract.get("actual_samples_per_update") != protocol["actual_samples_per_update"]
            or contract.get("additional_ram_hard_threshold") is not False
            or contract.get("automatic_retry") is not False
            or contract.get("automatic_continuation") is not False
            or contract.get("formal_acceptance") is not False):
        raise ValueError("head-only training contract differs")
    if (identity.get("numpy_version") != "2.3.5" or np.__version__ != "2.3.5"
            or identity.get("torch_version") != torch.__version__
            or identity.get("python_executable_sha256") != sha256(Path(sys._base_executable))
            or protocol.get("pytorch_nvml_based_cuda_check") != "1"
            or protocol.get("cpu_resume_check_threads") != 2
            or protocol.get("trainable_parameter_tensors") != 42
            or protocol.get("frozen_parameter_tensors") != 92
            or identity.get("authorization_receipt_sha256") != runner.AUTHORIZATION_SHA256):
        raise ValueError("runtime, authorization, or 42/92 protocol differs")
    for relative, expected in identity["source_sha256"].items():
        path = (PROJECT / relative).resolve()
        if not path.is_relative_to(PROJECT.resolve()) or sha256(path) != expected:
            raise ValueError(f"head-only training source changed: {relative}")
    _validate_training_snapshots(identity["source_sha256"])

    integer, manifest = load_package(args.package)
    parent_manifest = read(PARENT_MANIFEST)
    _validate_package(manifest, parent_manifest, identity, checkpoint_hash)
    gate, parity, execution = (read(path) for path in (
        runner.CHECK_DIR / "CPU_resume_check.json", runner.OUT / "export_parity.json",
        runner.OUT / "execution/report.json"))
    expected_receipt = {name: ancestry_receipt[name] for name in
                        ("parent_checkpoint_sha256", "parent_identity_sha256",
                         "parent_sample_history_sha256")}
    if (gate.get("passed") is not True or gate.get("identity") != identity
            or gate.get("protocol") != protocol or gate.get("ancestry_receipt") != expected_receipt
            or gate.get("optimizer_mapping_sha256") != identity["optimizer_name_mapping_sha256"]
            or gate.get("trainable_parameter_tensors") != 42
            or gate.get("frozen_parameter_tensors") != 92
            or gate.get("continuous_local_updates") != [1, 2]
            or gate.get("resumed_local_update") != 2
            or gate.get("resumed_second_update_exact") is not True
            or gate.get("negative_cases") != ["ancestry", "cursor", "frozen", "optimizer_name"]
            or gate.get("cpu_threads") != 2
            or gate.get("pytorch_nvml_based_cuda_check") != "1"
            or gate.get("optimizer_updates_published") != 0
            or gate.get("candidate_training_started") is not False
            or gate.get("cuda_initialized") is not False
            or parity.get("passed") is not True or parity.get("checkpoint_sha256") != checkpoint_hash
            or parity.get("payload_sha256") != manifest.get("payload_sha256")
            or parity.get("trace_tensors") != 181
            or parity.get("trained_steps") != runner.UPDATES
            or parity.get("local_head_only_updates") != runner.UPDATES
            or parity.get("global_qat_updates") != runner.GLOBAL_UPDATES
            or parity.get("parent_checkpoint_sha256") != runner.PARENT_SHA256
            or parity.get("identity") != identity or parity.get("formal_acceptance") is not False
            or execution.get("status") != "completed_qat_head_only_G5"
            or execution.get("checkpoint_sha256") != checkpoint_hash
            or execution.get("saved_local_updates") != runner.UPDATES
            or execution.get("global_qat_updates") != runner.GLOBAL_UPDATES
            or execution.get("all_saved_nonhead_parameter_tensors_unchanged") != 92
            or execution.get("parent_checkpoint_unchanged") is not True
            or execution.get("sources_unchanged") is not True
            or execution.get("formal_acceptance") is not False):
        raise ValueError("head-only CPU, export, or execution gate is stale or failed")

    rows, total = load_validation_subset(VALIDATION, None, 17)
    dataset = FullFrameDataset(rows, "val")
    content_hash = dataset_content_hash(dataset.rows)
    if total != 17 or content_hash != VALIDATION_CONTENT_HASH:
        raise ValueError("development17 selection changed")
    args.output.mkdir(parents=True, exist_ok=False)
    source_hashes = _snapshot_sources(args.output, identity["source_sha256"])
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
            "box": [value / 256 for value in item["box_q8"]], "score": item["score_uint16"] / 65536}
            for item in detections)
        truth.extend({"image_id": row["image"], "label": label, "box": box}
                     for label, box in zip(row["labels"], row["boxes"], strict=True))
        metadata = row.get("ignore_metadata", [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
        ignores.extend({"image_id": row["image"], "label": region["label"], "box": box,
                        "crowd": region["crowd"]}
                       for box, region in zip(row["ignore_boxes"], metadata, strict=True))
        print(f"head-only H5 development validation {index + 1}/17 ({timings[-1]:.2f}s CPU forward)", flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("development17 GT or ignore protocol changed")
    if any(sha256(PROJECT / name) != digest for name, digest in source_hashes.items()):
        raise ValueError("evaluation source changed after pre-inference snapshot")

    metrics = report(predictions, truth, ignores, thresholds=(.5, .5))
    references = {"parent_frozen_stem_G10": parent_eval["diagnostic_metrics_at_0_5"],
                  "FP32_replay_G10": baseline["diagnostic_metrics_at_0_5"],
                  "initial_maxabs_PTQ": ptq["diagnostic_metrics_at_0_5"]}
    deltas = {name: _delta(metrics, value) for name, value in references.items()}
    decision = _gate(metrics, references["parent_frozen_stem_G10"])
    inputs = {"checkpoint_sha256": checkpoint_hash,
        "candidate_manifest_sha256": sha256(args.package / "manifest.json"),
        "candidate_payload_sha256": manifest["payload_sha256"],
        "candidate_physical_sha256": manifest["physical_sha256"],
        "parent_checkpoint_sha256": runner.PARENT_SHA256,
        "parent_evaluation_sha256": PARENT_EVAL_HASH,
        "parent_manifest_sha256": PARENT_MANIFEST_HASH,
        "validation_dataset_sha256": VAL_HASH, "evaluated_image_content_sha256": content_hash,
        "fp32_baseline_sha256": BASELINE_HASH, "maxabs_ptq_report_sha256": SOURCE_PTQ_HASH,
        "source_package_manifest_sha256": SOURCE_MANIFEST_HASH,
        "authorization_receipt_sha256": runner.AUTHORIZATION_SHA256,
        "training_contract_sha256": sha256(runner.OUT / "training_contract.json")}
    result = {"status": "QAT_HEAD_ONLY_G5_DEVELOPMENT17_DIAGNOSTIC",
        "scope": "same17_development_only_not_formal_acceptance", "image_count": 17,
        "dataset_sha256": VAL_HASH, "evaluated_image_content_sha256": content_hash,
        "postprocess_contract": POSTPROCESS, "diagnostic_metrics_at_0_5": metrics,
        "delta_pp_vs_parent_frozen_stem_G10": deltas["parent_frozen_stem_G10"],
        "delta_pp_vs_FP32": deltas["FP32_replay_G10"],
        "delta_pp_vs_initial_maxabs_PTQ": deltas["initial_maxabs_PTQ"],
        "references": references, "predictions": predictions, "truth": truth, "ignores": ignores,
        "cpu_forward_seconds": timings, "input_hashes": inputs, "training_identity": identity,
        "ancestry": _report_ancestry(state["ancestry"]), "evaluation_source_sha256": source_hashes,
        "acceptance_eligible": False, "formal_acceptance": False,
        "automatic_continuation_authorized": False,
        "limitation": "same 17 development frames; no independent or formal acceptance"}
    save(args.output / "development17.json", result)
    save(args.output / "saturation_diagnostics.json", statistics)
    save(args.output / "evaluation_gate.json", {
        "status": "PASS_HEAD_ONLY_G5_CONTINUATION_GATE" if decision["passed"] else "FAIL_HEAD_ONLY_G5_CONTINUATION_GATE",
        "criteria_frozen_before_candidate_results": True,
        "scope": "same17_development_budget_diagnostic_not_formal_acceptance",
        "criteria": {"each_class_ap50_not_below_parent_G10": True,
                     "mean_ap50_gain_vs_parent_G10_at_least_pp": 1.0,
                     "each_class_recall_at_0_5_not_below_parent_G10": True},
        "observed": decision, "continuation_gate_passed": decision["passed"],
        "old256_started": False, "automatic_followup_started": False,
        "new_user_authorization_required": True, "formal_acceptance": False})
    save(args.output / "status.json", {"status": "completed_QAT_head_only_G5_development17",
        "input_hashes": inputs, "cpu_only": True, "cuda_initialized": torch.cuda.is_initialized(),
        "training_started": False, "image_count": 17, "full_integer_forward": True,
        "metrics_at_score_0_5": metrics, "continuation_gate_passed": decision["passed"],
        "automatic_followup_started": False, "formal_acceptance": False,
        "seconds": time.perf_counter() - started})
    print(json.dumps({"metrics": metrics, "deltas": deltas, "continuation_gate": decision},
                     ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
