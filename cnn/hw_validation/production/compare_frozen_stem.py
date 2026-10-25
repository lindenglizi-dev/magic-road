"""Compare the frozen-Stem control with the three frozen development17 references."""
from pathlib import Path

from cnn.train import sha256
from cnn.hw_validation.production.evaluate_qat import BASELINE, PROJECT, SOURCE, _delta, read
from cnn.hw_validation.production.run_trained_integer import save

NEW = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1"
OLD = PROJECT / "cnn/reports/qat_g10_20261013_v1"
OUTPUT = NEW / "control_comparison.json"
FIELDS = ("precision", "recall", "ap50", "ap50_95")
COMMON_IDENTITY = (
    "source_checkpoint_sha256", "architecture_hash", "dataset_sha256",
    "dataset_content_sha256", "graph_sha256", "scales_sha256",
    "source_package_manifest_sha256", "source_payload_sha256", "quantization_sha256",
    "sampling_sha256", "cache_index_sha256", "cache_rgb_sha256",
    "torch_version", "numpy_version", "python_executable_sha256")


def compact(metrics):
    return {name: {("precision_at_0_5" if field == "precision" else
                    "recall_at_0_5" if field == "recall" else field):
                   metrics["classes"][name][field] for field in FIELDS}
            for name in ("person", "vehicle")}


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    paths = {
        "new_training_contract": NEW / "training_contract.json",
        "old_training_contract": OLD / "training_contract.json",
        "previous_decision": OLD / "decision.json",
        "new_execution": NEW / "execution/report.json",
        "new_evaluation": NEW / "evaluation/development17.json",
        "new_evaluation_gate": NEW / "evaluation/evaluation_gate.json",
        "unfrozen_QAT_G10": OLD / "evaluation/development17.json",
        "initial_maxabs_PTQ": SOURCE / "development17.json",
        "FP32_replay_G10": BASELINE,
    }
    documents = {name: read(path) for name, path in paths.items()}
    new_contract, old_contract = (documents[name] for name in
                                  ("new_training_contract", "old_training_contract"))
    new_protocol, old_protocol = dict(new_contract["protocol"]), dict(old_contract["protocol"])
    if (new_protocol.get("frozen_layers") != ["stem.conv"]
            or new_protocol.get("frozen_fields") != ["weight", "bias"]
            or new_protocol.get("prior_qat_updates") != 10):
        raise ValueError("frozen-Stem protocol fields differ")
    for protocol in (new_protocol, old_protocol):
        protocol.pop("name")
    for field in ("frozen_layers", "frozen_fields", "prior_qat_updates"):
        new_protocol.pop(field)
    if new_protocol != old_protocol:
        raise ValueError("control protocol differs beyond the frozen-Stem treatment")

    new_identity, old_identity = new_contract["identity"], old_contract["identity"]
    if any(new_identity.get(key) != old_identity.get(key) for key in COMMON_IDENTITY):
        raise ValueError("control initializer, graph, scales, data, cache, sampling, or runtime differs")
    old_sources, new_sources = old_identity["source_sha256"], new_identity["source_sha256"]
    if any(new_sources.get(name) != digest for name, digest in old_sources.items()):
        raise ValueError("common training source closure differs")
    prior = documents["previous_decision"]
    previous_hash = sha256(paths["previous_decision"])
    previous_eval = documents["unfrozen_QAT_G10"]
    if (new_identity.get("previous_decision_sha256") != previous_hash
            or previous_eval["input_hashes"]["checkpoint_sha256"]
            != prior.get("candidate_checkpoint_sha256")
            or prior.get("updates_completed") != 10 or prior.get("continue_training") is not False):
        raise ValueError("previous rejected artifact is not bound to the control")

    new_eval = documents["new_evaluation"]
    execution = documents["new_execution"]
    if (execution.get("status") != "completed_frozen_stem_qat_G10"
            or execution.get("checkpoint_sha256") != new_eval["input_hashes"]["checkpoint_sha256"]):
        raise ValueError("completed control checkpoint does not match its evaluation")
    reports = {name: documents[name] for name in
               ("new_evaluation", "unfrozen_QAT_G10", "initial_maxabs_PTQ", "FP32_replay_G10")}
    reference = reports["FP32_replay_G10"]
    image_ids = sorted({row["image_id"] for row in reference["truth"]})
    for name, report in reports.items():
        if (report.get("image_count") != 17 or report.get("dataset_sha256") != reference["dataset_sha256"]
                or report.get("evaluated_image_content_sha256") != reference["evaluated_image_content_sha256"]
                or report.get("postprocess_contract") != reference["postprocess_contract"]
                or report.get("truth") != reference["truth"] or report.get("ignores") != reference["ignores"]
                or sorted({row["image_id"] for row in report["truth"]}) != image_ids):
            raise ValueError(f"{name}: development17 GT/ignore/postprocess/image identity differs")
    metrics = {name: report["diagnostic_metrics_at_0_5"] for name, report in reports.items()}
    gate = documents["new_evaluation_gate"]
    if (gate.get("criteria_frozen_before_candidate_results") is not True
            or gate.get("formal_acceptance") is not False
            or new_eval.get("acceptance_eligible") is not False
            or new_eval.get("formal_acceptance") is not False):
        raise ValueError("new recovery gate is missing or claims acceptance")
    if (new_contract.get("cumulative_qat_updates_after_trial") != 20
            or new_contract.get("overall_qat_budget_cap") != 100):
        raise ValueError("QAT budget accounting differs")
    save(OUTPUT, {
        "status": "FROZEN_STEM_CONTROL_DEVELOPMENT17_COMPARISON",
        "scope": "same17_control_only_not_formal_acceptance",
        "metrics": {name: compact(value) for name, value in metrics.items()},
        "delta_pp_vs_unfrozen_QAT_G10": _delta(metrics["new_evaluation"], metrics["unfrozen_QAT_G10"]),
        "delta_pp_vs_initial_maxabs_PTQ": _delta(metrics["new_evaluation"], metrics["initial_maxabs_PTQ"]),
        "delta_pp_vs_FP32_replay_G10": _delta(metrics["new_evaluation"], metrics["FP32_replay_G10"]),
        "recovery_gate": gate, "image_ids": image_ids,
        "qat_budget": {"updates_used": 20, "cap": 100, "remaining": 80},
        "bindings": {"previous_decision_sha256": previous_hash,
                     "prior_candidate_checkpoint_sha256": prior["candidate_checkpoint_sha256"],
                     "new_candidate_checkpoint_sha256": execution["checkpoint_sha256"]},
        "input_sha256": {name: sha256(path) for name, path in paths.items()},
        "source_sha256": sha256(Path(__file__)), "formal_acceptance": False,
    })


if __name__ == "__main__":
    main()
