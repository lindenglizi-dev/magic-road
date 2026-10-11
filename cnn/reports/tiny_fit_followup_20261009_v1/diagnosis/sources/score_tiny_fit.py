"""Score one completed tiny-fit diagnostic checkpoint on its 32 training images."""
import argparse
import json
from pathlib import Path

import torch

from .dataset import _refuse_blind
from .model import RoadYOLOS4
from .prepare_tiny_fit import OUTPUT, ROOT, guard_row, score_fit, write_json
from .train import CLASS_CONTRACT, load_dataset_snapshot, sha256


CONTRACT = OUTPUT / "training_contract_proposed.json"
PREFLIGHT = OUTPUT / "preflight_receipt.json"
MANIFEST = OUTPUT / "tiny_fit32_manifest.json"
BASELINE = OUTPUT / "e7_training_fit_baseline.json"
CONTRACT_SHA = "5b2d4bbfe92d159d21e4d0284605eb35db4e7de2671c992f6c6862c720616a3f"
PREFLIGHT_SHA = "9d648d6652aa0f63916f5ea66a218ea6f78f04bc7cb49488ce9440a8112264d3"
ARCHITECTURE_SHA = "106ccd0f223b1cefaff8e36408d3968aee3e4a1703d17e27786db58eb8124595"
INFERENCE_SOURCES = ("prepare_tiny_fit.py", "dataset.py", "model.py", "integer.py", "metrics.py")


def validate_candidate(checkpoint: dict, contract: dict) -> None:
    """Validate only checkpoint metadata; perform no I/O or model construction."""
    expected = {
        "format": "road-yolo-checkpoint-v2",
        "phase": "supervised",
        "checkpoint_kind": "diagnostic",
        "interrupted": False,
        "architecture_hash": ARCHITECTURE_SHA,
        "class_contract": CLASS_CONTRACT,
        "dataset_sha256": "eebe5269aac34d5577767168dffe167399aa6d8b8c232c1578774d855f3d0afd",
        "dataset_content_sha256": "8f8e7d66199ffe8ced0ab6289c33dfbd658c056abf267f4968237c4c00271877",
        "training_protocol": contract.get("protocol"),
        "training_protocol_sha256": "856034b2b2d73c5a1d36deb928cdb5738cd9ccf215a52ca471f055113767971e",
    }
    if (contract.get("dataset_sha256") != expected["dataset_sha256"]
            or contract.get("dataset_content_sha256") != expected["dataset_content_sha256"]
            or contract.get("protocol_sha256") != expected["training_protocol_sha256"]
            or contract.get("optimizer_update_cap") != 300
            or contract.get("protocol", {}).get("optimizer_steps_per_epoch") != 4
            or contract.get("protocol", {}).get("checkpoint_kind") != "diagnostic"):
        raise ValueError("tiny-fit contract identity mismatch")
    for name, value in expected.items():
        if checkpoint.get(name) != value:
            raise ValueError(f"candidate {name} mismatch")
    epoch, steps = checkpoint.get("epoch"), checkpoint.get("trained_steps")
    if (type(epoch) is not int or type(steps) is not int or not 1 <= steps <= 300
            or steps != (epoch + 1) * 4):
        raise ValueError("candidate is not a complete bounded tiny-fit epoch")
    if not isinstance(checkpoint.get("model"), dict):
        raise ValueError("candidate has no model state")


def _metric_delta(candidate: dict, baseline: dict) -> dict:
    keys = ("precision", "recall", "ap50")
    return {name: {key: candidate["classes"][name][key] - baseline["classes"][name][key]
                   for key in keys} for name in ("person", "vehicle")}


def score_candidate(checkpoint: Path, output: Path) -> dict:
    checkpoint, output = checkpoint.resolve(), output.resolve()
    _refuse_blind(checkpoint)
    if (not output.is_relative_to(OUTPUT) or output.suffix.lower() != ".json"
            or output.exists() or not output.parent.is_dir()):
        raise ValueError("output must be a new JSON report under the tiny-fit v2 report directory")
    if sha256(CONTRACT) != CONTRACT_SHA or sha256(PREFLIGHT) != PREFLIGHT_SHA:
        raise ValueError("tiny-fit contract/preflight receipt changed")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    for name in INFERENCE_SOURCES:
        if sha256(ROOT / "cnn" / name) != preflight["source_sha256"].get(name):
            raise ValueError(f"CPU-scoring source changed: {name}")
    for path in (MANIFEST, BASELINE):
        if sha256(path) != preflight["artifacts"].get(path.name):
            raise ValueError(f"prepared scoring artifact changed: {path.name}")
    if sha256(MANIFEST) != contract["dataset_sha256"]:
        raise ValueError("tiny-fit manifest identity mismatch")
    raw_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for row in raw_manifest.get("images", []):
        guard_row(row)  # Reject forbidden paths before any source image is opened.
    _, snapshot = load_dataset_snapshot(MANIFEST)
    if (snapshot.dataset_content_sha256 != contract["dataset_content_sha256"]
            or sum(row["split"] == "train" for row in snapshot.rows) != 32):
        raise ValueError("tiny-fit image content/split identity mismatch")

    candidate = torch.load(checkpoint, map_location="cpu", weights_only=False)
    validate_candidate(candidate, contract)
    model = RoadYOLOS4().cpu()
    if model.architecture_hash() != ARCHITECTURE_SHA:
        raise ValueError("runtime RoadYOLO architecture changed")
    model.load_state_dict(candidate["model"], strict=True)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    result = score_fit(model, snapshot.rows, MANIFEST, candidate, sha256(checkpoint))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    result.update(
        status="tiny_fit_candidate_training_fit_same_as_train_NOT_validation",
        scoring_scope="verified tiny-fit candidate on all 32 training rows; NOT validation",
        candidate_identity=dict(format=candidate["format"], phase=candidate["phase"],
            checkpoint_kind=candidate["checkpoint_kind"], interrupted=candidate["interrupted"],
            epoch_number=candidate["epoch"] + 1, trained_steps=candidate["trained_steps"],
            checkpoint_sha256=result["checkpoint_sha256"],
            dataset_sha256=candidate["dataset_sha256"],
            dataset_content_sha256=candidate["dataset_content_sha256"],
            training_protocol_sha256=candidate["training_protocol_sha256"],
            architecture_hash=candidate["architecture_hash"], class_contract=candidate["class_contract"]),
        baseline_identity=dict(report=str(BASELINE), report_sha256=sha256(BASELINE),
            checkpoint_sha256=baseline["checkpoint_sha256"], status=baseline["status"]),
        baseline_delta_at_0_5=_metric_delta(result["diagnostic_metrics_at_0_5"],
                                             baseline["diagnostic_metrics_at_0_5"]),
        inference="FP32_CNN_plus_fixed_point_postprocess_NOT_INT8",
        formal_acceptance=False)
    write_json(output, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    score_candidate(args.checkpoint, args.output)
    print(str(args.output.resolve()), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
