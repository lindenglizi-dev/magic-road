"""One authorized tiny-fit diagnostic, protected by the existing owned watchdog."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time
from types import SimpleNamespace

import torch

from .prepare_tiny_fit import (CHECKPOINT, OUTPUT, ROOT, RUN, WEIGHT_SHA,
                               training_arguments, write_json)
from .run_post_review_s import load_json, run_protected, run_validate_only
from .train import build_parser, protocol_for, protocol_hash, sha256
from . import training_watchdog as protection

PREFLIGHT_SHA = "9d648d6652aa0f63916f5ea66a218ea6f78f04bc7cb49488ce9440a8112264d3"
CONTRACT_SHA = "5b2d4bbfe92d159d21e4d0284605eb35db4e7de2671c992f6c6862c720616a3f"
EXECUTION = OUTPUT / "execution_v1"


def verify_prepared():
    preflight_path = OUTPUT / "preflight_receipt.json"
    contract_path = OUTPUT / "training_contract_proposed.json"
    if sha256(preflight_path) != PREFLIGHT_SHA or sha256(contract_path) != CONTRACT_SHA:
        raise ValueError("prepared input receipt changed")
    preflight, contract = load_json(preflight_path), load_json(contract_path)
    for name, expected in preflight["artifacts"].items():
        path = (OUTPUT / name).resolve()
        if not path.is_relative_to(OUTPUT) or sha256(path) != expected:
            raise ValueError(f"prepared artifact changed: {name}")
    for name, expected in preflight["source_sha256"].items():
        if sha256(ROOT / "cnn" / name) != expected:
            raise ValueError(f"CPU-checked source changed: {name}")
    if sha256(CHECKPOINT) != WEIGHT_SHA:
        raise ValueError("frozen E7 changed")
    if (protection.STOP_C, protection.SOFT_SECONDS, protection.HARD_SECONDS,
            protection.STALE_PAUSE_SECONDS, protection.STALE_KILL_SECONDS) != (
            75, 1560, 1800, 20, 30):
        raise ValueError("protection limits changed")
    arguments = training_arguments(OUTPUT / "tiny_fit32_manifest.json", OUTPUT / "cache",
                                   contract["cache_index_sha256"])
    args = build_parser().parse_args(arguments)
    protocol = protocol_for(args, 4, None)
    if (arguments != contract["trainer_arguments"] or protocol != contract["protocol"]
            or protocol_hash(protocol) != contract["protocol_sha256"]
            or contract["optimizer_update_cap"] != 300
            or contract["wall_seconds_cap"] != 1800):
        raise ValueError("tiny-fit protocol changed")
    if RUN.exists():
        raise FileExistsError("tiny-fit run already exists; never restart automatically")
    return contract, [sys._base_executable, "-u", "-B", "-m", "cnn.train", *arguments,
                      "--stop-after-epoch", "75"]


def verify_completion(event, contract):
    """A diagnostic pause has no live checkpoint; retain only a complete epoch."""
    from .score_tiny_fit import validate_candidate
    name = event.get("event")
    if name not in {"paused_complete_epoch", "paused_segment"}:
        raise ValueError("tiny-fit ended without a recognized completion/pause event")
    if name == "paused_complete_epoch" and (
            event.get("epoch_number") != 75 or event.get("trained_steps") != 300
            or Path(event.get("checkpoint", "")).resolve() != RUN / "last.pt"):
        raise ValueError("tiny-fit final completion identity mismatch")
    checkpoint_path = RUN / "last.pt"
    if not checkpoint_path.exists():
        if name != "paused_segment":
            raise FileNotFoundError("missing completed tiny-fit checkpoint")
        return dict(status="paused_without_complete_epoch", checkpoint=None,
                    completed_optimizer_updates=0, observed_updates=event["trained_steps"])
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    validate_candidate(checkpoint, contract)
    if checkpoint["trained_steps"] > event["trained_steps"]:
        raise ValueError("saved progress exceeds observed pause progress")
    return dict(status="completed_300_updates" if name == "paused_complete_epoch" else
                "paused_latest_complete_epoch", checkpoint=str(checkpoint_path),
                checkpoint_sha256=sha256(checkpoint_path),
                completed_optimizer_updates=checkpoint["trained_steps"],
                completed_epochs=checkpoint["epoch"] + 1,
                observed_updates=event["trained_steps"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--gpu-uuid")
    args = parser.parse_args()
    contract, command = verify_prepared()
    validation = run_validate_only(command)
    if validation["exit_code"]:
        raise RuntimeError("real trainer CPU validation failed: " + repr(validation))
    if not args.execute:
        print(json.dumps(dict(status="CPU_entry_passed_NOT_training", command=command)), flush=True)
        return 0
    if not args.gpu_uuid:
        raise ValueError("execution requires the selected GPU UUID")
    EXECUTION.mkdir(exist_ok=False)
    sources = ["run_tiny_fit.py", "score_tiny_fit.py", "run_post_review_s.py",
               "training_watchdog.py", "benchmark_cache_gpu.py", *load_json(
                   OUTPUT / "preflight_receipt.json")["source_sha256"]]
    source_dir = EXECUTION / "sources"
    source_dir.mkdir()
    source_hashes = {}
    for name in dict.fromkeys(sources):
        source = ROOT / "cnn" / name
        source_hashes[name] = sha256(source)
        shutil.copy2(source, source_dir / name)
        if sha256(source_dir / name) != source_hashes[name]:
            raise ValueError("source snapshot copy mismatch")
    write_json(EXECUTION / "authorization.json", dict(
        status="authorized_one_segment", training_authorized=True,
        authorization="user: 快点进行啊; bounded next step confirmed in this chat",
        owner_pid=os.getpid(), started_unix=time.time(), GPU_uuid=args.gpu_uuid,
        initializer_sha256=WEIGHT_SHA, preflight_sha256=PREFLIGHT_SHA,
        proposed_contract_sha256=CONTRACT_SHA, contract=contract, command=command,
        optimizer_update_cap=300, hard_wall_seconds=1800, soft_pause_seconds=1560,
        temperature_stop_c=75, memory_threshold_enabled=False, automatic_retry=False,
        source_sha256=source_hashes, formal_acceptance=False))
    print(json.dumps(dict(event="authorized_controller_started", owner_pid=os.getpid(),
                          receipt=str(EXECUTION / "report.json"))), flush=True)
    options = SimpleNamespace(receipt=EXECUTION / "segment.json", output=RUN,
                              gpu_uuid=args.gpu_uuid, preflight_timeout_seconds=120)
    started = time.monotonic()
    result = run_protected(command, options, expected_ready=dict(
        dataset_sha256=contract["dataset_sha256"],
        dataset_content_sha256=contract["dataset_content_sha256"], resume=None),
        completion_validator=lambda event: verify_completion(event, contract))
    write_json(EXECUTION / "segment.json", result)
    receipt = dict(status=result["status"], protected_segment=result,
                   elapsed_seconds=time.monotonic() - started, automatic_retry=False,
                   formal_acceptance=False)
    events = [json.loads(line) for line in options.receipt.with_suffix(".stdout.log").read_text(
        encoding="utf-8").splitlines() if line.startswith("{")]
    epochs = [row for row in events if row.get("event") == "epoch"]
    steps = [row for row in events if row.get("event") == "step"]
    receipt["progress"] = dict(observed_updates=steps[-1]["optimizer_steps_completed"] if steps else 0,
        saved_complete_epochs=epochs[-1]["epoch_number"] if epochs else 0,
        first_epoch_loss=epochs[0]["train_loss"] if epochs else None,
        last_epoch_loss=epochs[-1]["train_loss"] if epochs else None,
        gradient_validation="trainer clips every update with error_if_nonfinite=True")
    telemetry_path = options.receipt.with_suffix(".telemetry.jsonl")
    if telemetry_path.exists():
        telemetry = [json.loads(line) for line in telemetry_path.read_text().splitlines()]
        samples = [row for row in telemetry if "temperature_c" in row]
        if samples:
            receipt["telemetry_summary"] = dict(samples=len(samples),
                peak_temperature_c=max(row["temperature_c"] for row in samples),
                peak_gpu_memory_mib=max(row["memory_mib"] for row in samples))
    # Scoring is CPU-only and cannot extend the protected GPU training budget.
    if (RUN / "last.pt").is_file():
        from .score_tiny_fit import score_candidate
        try:
            scored = score_candidate(RUN / "last.pt", EXECUTION / "training_fit.json")
            receipt["training_fit"] = dict(path=str(EXECUTION / "training_fit.json"),
                sha256=sha256(EXECUTION / "training_fit.json"),
                metrics=scored["diagnostic_metrics_at_0_5"])
        except Exception as error:
            receipt["scoring_error"] = repr(error)
    receipt["frozen_E7_unchanged"] = sha256(CHECKPOINT) == WEIGHT_SHA
    write_json(EXECUTION / "report.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return 0 if result["status"] == "completed_300_updates" and "training_fit" in receipt else 1


if __name__ == "__main__":
    raise SystemExit(main())
