"""CPU-first, fail-closed launcher for the post-review S experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_INIT_SHA256 = "17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42"
EXPECTED_TRAIN, EXPECTED_VAL = 19049, 5151
PROTOCOL = "post_review_s_v1"
TRAINING = {
    "phase": "supervised", "epochs": 5, "batch_size": 8, "accum_steps": 8,
    "lr": 0.001, "lr_schedule": "finetune_constant", "momentum": 0.9,
    "weight_decay": 0.0005, "clip_grad": 10.0, "seed": 42, "workers": 0,
    "device": "cuda", "amp": True, "mosaic": False,
    "checkpoint_every_seconds": 120.0,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def add_gate(gates: list[dict], name: str, detail: str, *, cpu: bool = False) -> None:
    gates.append({"gate": name, "detail": detail,
                  "blocks": ["validate_only", "execute"] if cpu else ["execute"]})


def pinned_json(path: Path, expected: str, name: str, gates: list[dict], *, cpu: bool = True
                ) -> dict | None:
    if not path.is_file():
        add_gate(gates, name + "_missing", str(path), cpu=cpu)
        return None
    actual = sha256(path)
    if actual != expected.lower():
        add_gate(gates, name + "_hash_mismatch", f"{actual} != {expected.lower()}", cpu=cpu)
        return None
    try:
        return load_json(path)
    except Exception as error:
        add_gate(gates, name + "_invalid_json", repr(error), cpu=cpu)
        return None


def validate_ground_evidence(args: argparse.Namespace, receipt: dict,
                             gates: list[dict], identities: dict) -> None:
    """Replay the real exporter from the retained signed patch."""
    try:
        from .prepare_ground48 import export_documents
        review_path = args.ground_manifest.parent / "review_manifest_teacher.json"
        verified_path = args.ground_manifest.parent / "ground48_verified_labels.json"
        signed_path = args.ground_manifest.parent / "review_patch_signed.json"
        ground = load_json(args.ground_manifest)
        verified = load_json(verified_path)
        rebuilt_verified, rebuilt_ground, rebuilt_receipt = export_documents(
            review_path, signed_path)
        if rebuilt_verified != verified or rebuilt_ground != ground:
            raise ValueError("retained signed patch does not reproduce exported ground truth")
        required = {**rebuilt_receipt,
                    "ground_val48_sha256": sha256(args.ground_manifest),
                    "ground48_verified_labels_json_sha256": sha256(verified_path),
                    "review_patch_signed_json_sha256": sha256(signed_path)}
        bad = {key: (receipt.get(key), expected) for key, expected in required.items()
               if receipt.get(key) != expected}
        if bad:
            raise ValueError(f"ground receipt binding mismatch: {bad}")
        identities.update(ground_dataset_id=receipt["dataset_id"], ground_signed_rows=48,
                          ground_export_replayed=True)
    except Exception as error:
        add_gate(gates, "ground_evidence_closure", repr(error))


def inspect(args: argparse.Namespace) -> tuple[list[dict], dict]:
    gates: list[dict] = []
    identities = {}
    for name, path, expected in (
            ("dataset", args.dataset, args.dataset_sha256),
            ("cache_index", args.cache / "index.json", args.cache_index_sha256),
            ("init_checkpoint", args.init_checkpoint, args.init_checkpoint_sha256)):
        if not path.is_file():
            add_gate(gates, name + "_missing", str(path), cpu=True)
            continue
        actual = sha256(path)
        identities[name + "_sha256"] = actual
        if actual != expected.lower():
            add_gate(gates, name + "_hash_mismatch", f"{actual} != {expected.lower()}", cpu=True)
    if args.init_checkpoint_sha256.lower() != EXPECTED_INIT_SHA256:
        add_gate(gates, "unapproved_initializer",
                 "initializer is not frozen E7", cpu=True)

    contract = pinned_json(args.experiment_contract, args.experiment_contract_sha256,
                           "experiment_contract", gates)
    if contract is not None:
        required = {
            "protocol": PROTOCOL, "training_authorized": True, "epochs": 5,
            "initial_stop_after_epoch": 2,
            "dataset_sha256": args.dataset_sha256.lower(),
            "cache_index_sha256": args.cache_index_sha256.lower(),
            "init_checkpoint_sha256": args.init_checkpoint_sha256.lower(),
            "output": str(args.output.resolve()),
            "train_images": EXPECTED_TRAIN, "val_images": EXPECTED_VAL,
        }
        bad = {key: (contract.get(key), expected) for key, expected in required.items()
               if contract.get(key) != expected}
        if bad:
            add_gate(gates, "experiment_contract_mismatch", repr(bad), cpu=True)
        identities["experiment_contract_status"] = contract.get("status")

    preflight = pinned_json(args.preflight, args.preflight_sha256, "preflight", gates)
    if preflight is not None:
        bindings = {
            "dataset_sha256": args.dataset_sha256.lower(),
            "cache_index_sha256": args.cache_index_sha256.lower(),
            "init_checkpoint_sha256": args.init_checkpoint_sha256.lower(),
            "train_images": EXPECTED_TRAIN, "val_images": EXPECTED_VAL,
        }
        bad = {key: (preflight.get(key), expected) for key, expected in bindings.items()
               if preflight.get(key) != expected}
        if bad:
            add_gate(gates, "preflight_binding_mismatch", repr(bad), cpu=True)
        if preflight.get("gpu_execution_ready") is not True:
            add_gate(gates, "preflight_not_GPU_ready",
                     f"status={preflight.get('status')!r}")
        identities["preflight_status"] = preflight.get("status")

    ground = pinned_json(args.ground_receipt, args.ground_receipt_sha256,
                         "ground_receipt", gates, cpu=False)
    if not args.ground_manifest.is_file():
        add_gate(gates, "ground_manifest_missing", str(args.ground_manifest))
    else:
        actual = sha256(args.ground_manifest)
        identities["ground_manifest_sha256"] = actual
        if actual != args.ground_manifest_sha256.lower():
            add_gate(gates, "ground_manifest_hash_mismatch",
                     f"{actual} != {args.ground_manifest_sha256.lower()}")
        else:
            try:
                ground_manifest = load_json(args.ground_manifest)
                if len(ground_manifest.get("images", [])) != 48:
                    add_gate(gates, "ground_manifest_not_48",
                             f"images={len(ground_manifest.get('images', []))}")
            except Exception as error:
                add_gate(gates, "ground_manifest_invalid_json", repr(error))
    if ground is not None:
        identities["ground_receipt_status"] = ground.get("status")
        if ground.get("status") == "validated_ready" and args.ground_manifest.is_file():
            validate_ground_evidence(args, ground, gates, identities)
        else:
            add_gate(gates, "ground_human_review_incomplete",
                     "requires 48 complete raw-seen six-check signed reviews and export closure")

    try:
        from . import training_watchdog
        watchdog = {
            "temperature_stop_c": training_watchdog.STOP_C,
            "telemetry_pause_seconds": training_watchdog.STALE_PAUSE_SECONDS,
            "telemetry_stop_seconds": training_watchdog.STALE_KILL_SECONDS,
            "soft_pause_seconds": training_watchdog.SOFT_SECONDS,
            "hard_stop_seconds": training_watchdog.HARD_SECONDS,
        }
        identities["watchdog"] = watchdog
        if watchdog != {"temperature_stop_c": 75, "telemetry_pause_seconds": 20,
                        "telemetry_stop_seconds": 30, "soft_pause_seconds": 26 * 60,
                        "hard_stop_seconds": 30 * 60}:
            add_gate(gates, "watchdog_contract_changed", repr(watchdog), cpu=True)
    except Exception as error:
        add_gate(gates, "watchdog_unavailable", repr(error), cpu=True)

    if args.continue_to_5:
        decision = (pinned_json(args.decision_proof, args.decision_proof_sha256,
                                "decision_proof", gates)
                    if args.decision_proof and args.decision_proof_sha256 else None)
        if decision is None:
            add_gate(gates, "S2_to_S5_decision_missing", "explicit passed decision is required")
        else:
            required = {
                "status": "passed", "development_continue_eligible": True,
                "continue_to_epoch": 5, "same_run": True,
                "dataset_sha256": args.dataset_sha256.lower(),
                "cache_index_sha256": args.cache_index_sha256.lower(),
                "output": str(args.output.resolve()),
            }
            bad = {key: (decision.get(key), expected) for key, expected in required.items()
                   if decision.get(key) != expected}
            if bad:
                add_gate(gates, "S2_to_S5_decision_failed", repr(bad))
    return gates, identities


def select_initialization(output: Path, init_checkpoint: Path,
                          continue_to_5: bool) -> tuple[str, Path, int]:
    output = output.resolve()
    if continue_to_5:
        checkpoint = output / "last.pt"
        if not checkpoint.is_file():
            raise FileNotFoundError("S2->S5 requires the same run's last.pt")
        return "resume_S2_same_run", checkpoint, 5
    for name in ("last_resume.pt", "last_resume.prev.pt"):
        checkpoint = output / name
        if checkpoint.is_file():
            return "resume_paused_same_run", checkpoint, 2
    if output.exists() and any(output.iterdir()):
        checkpoint = output / "last.pt"
        if checkpoint.is_file():
            return "resume_complete_epoch_same_run", checkpoint, 2
        raise FileExistsError("non-empty output has no recognized same-run checkpoint")
    return "init_E7_weights_only", init_checkpoint.resolve(), 2


def build_train_command(args: argparse.Namespace) -> tuple[list[str], str, int]:
    initialization, checkpoint, stop = select_initialization(
        args.output, args.init_checkpoint, args.continue_to_5)
    command = [sys._base_executable, "-u", "-B", "-m", "cnn.train",
               "--dataset", str(args.dataset.resolve()), "--output", str(args.output.resolve()),
               "--phase", "supervised", "--epochs", "5", "--stop-after-epoch", str(stop),
               "--batch-size", "8", "--accum-steps", "8", "--lr", "0.001",
               "--lr-schedule", "finetune_constant", "--momentum", "0.9",
               "--weight-decay", "0.0005", "--clip-grad", "10", "--seed", "42",
               "--workers", "0", "--device", "cuda", "--amp", "--no-mosaic",
               "--checkpoint-every-seconds", "120", "--input-cache", str(args.cache.resolve()),
               "--input-cache-index-sha256", args.cache_index_sha256.lower()]
    command += (["--init-checkpoint", str(checkpoint)] if initialization == "init_E7_weights_only"
                else ["--resume", str(checkpoint)])
    return command, initialization, stop


def worker_environment() -> dict[str, str]:
    site = Path(sys.executable).parent.parent / "Lib/site-packages"
    return {**os.environ, "PYTHONPATH": os.pathsep.join(
        [str(ROOT), str(site), os.environ.get("PYTHONPATH", "")])}


def read_json_line(process, timeout: float) -> dict:
    lines: queue.Queue[str] = queue.Queue()
    threading.Thread(target=lambda: lines.put(process.stdout.readline()), daemon=True).start()
    line = lines.get(timeout=timeout)
    value = json.loads(line)
    if not isinstance(value, dict):
        raise ValueError("subprocess handshake is not an object")
    return value


def validate_committed_event(event: dict, output: Path, stop_after_epoch: int) -> None:
    name = event.get("event")
    expected = output.resolve() / ("last_resume.pt" if name == "paused_segment" else "last.pt")
    if Path(event.get("checkpoint", "")).resolve() != expected:
        raise ValueError("completion event refers to a different output checkpoint")
    if name == "paused_segment":
        stage = event.get("stage")
        microbatch = event.get("next_microbatch")
        cursor = event.get("next_sample_cursor")
        val_batch = event.get("val_next_batch")
        if (stage not in {"train", "val"} or not all(
                isinstance(value, int) and value >= 0
                for value in (microbatch, cursor, val_batch))):
            raise ValueError("pause event has invalid resume cursors")
        if cursor != min(microbatch * 8, EXPECTED_TRAIN) or microbatch > 2382:
            raise ValueError("pause event sample and microbatch cursors disagree")
        if stage == "train" and (val_batch or (microbatch % 8 and microbatch != 2382)):
            raise ValueError("pause event is not at a complete update boundary")
        if stage == "val" and (microbatch != 2382 or cursor != EXPECTED_TRAIN
                               or val_batch > 644):
            raise ValueError("pause event validation cursor disagrees")
        return
    if (name not in {"paused_complete_epoch", "completed_before_GPU"}
            or event.get("epoch_number") != stop_after_epoch
            or event.get("trained_steps") != 298 * stop_after_epoch):
        raise ValueError("target epoch event is incomplete or has the wrong update count")


def run_validate_only(command: list[str]) -> dict:
    checked = command + ["--validate-only"]
    result = subprocess.run(checked, cwd=ROOT, env=worker_environment(), capture_output=True,
                            text=True, timeout=60 * 60,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    return {"command": checked, "exit_code": result.returncode,
            "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:]}


def run_protected(command: list[str], args: argparse.Namespace, *,
                  expected_ready: dict | None = None, completion_validator=None) -> dict:
    """Run exactly one owned segment. Never enumerate, stop, or retry another process."""
    pause = args.receipt.with_suffix(".pause.json")
    failure = args.receipt.with_suffix(".watchdog_failure.json")
    telemetry = args.receipt.with_suffix(".telemetry.jsonl")
    stderr_path = args.receipt.with_suffix(".stderr.log")
    stdout_path = args.receipt.with_suffix(".stdout.log")
    worker = monitor = None
    reader = None
    result = {"status": "starting", "command": command + ["--pause-request", str(pause),
                                                             "--supervised-start"]}
    try:
        with (stderr_path.open("x", encoding="utf-8") as error_log,
              stdout_path.open("x", encoding="utf-8") as output_log):
            worker = subprocess.Popen(result["command"], cwd=ROOT, env=worker_environment(),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=error_log, text=True, bufsize=1,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            result["trainer_pid"] = worker.pid
            lines: queue.Queue[str | None] = queue.Queue()
            def pump_stdout() -> None:
                try:
                    for value in worker.stdout:
                        lines.put(value)
                finally:
                    lines.put(None)
            reader = threading.Thread(target=pump_stdout, daemon=True)
            reader.start()
            preflight_deadline = time.monotonic() + args.preflight_timeout_seconds
            while True:
                try:
                    timeout = (1 if monitor is not None else
                               max(0.01, min(1, preflight_deadline - time.monotonic())))
                    line = lines.get(timeout=timeout)
                except queue.Empty:
                    if worker.poll() is not None:
                        break
                    if monitor is None and time.monotonic() >= preflight_deadline:
                        raise TimeoutError("CPU preflight did not produce a ready event in time")
                    if monitor is not None and monitor.poll() is not None:
                        raise RuntimeError("independent watchdog exited while trainer is alive")
                    continue
                if line is None:
                    # EOF can precede Windows process teardown; wait for the owned
                    # exit instead of treating that normal ordering as a failure.
                    worker.wait(timeout=60)
                    break
                if monitor is None and time.monotonic() >= preflight_deadline:
                    raise TimeoutError("CPU preflight did not produce a ready event in time")
                output_log.write(line)
                output_log.flush()
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                result["last_event"] = event
                if event.get("event") != "preflight_ready":
                    continue
                if monitor is not None:
                    raise RuntimeError("duplicate preflight_ready event")
                if event.get("trainer_pid") != worker.pid:
                    raise ValueError("preflight PID does not match owned trainer")
                if expected_ready is not None and any(
                        event.get(key) != value for key, value in expected_ready.items()):
                    raise ValueError("owned trainer preflight identity mismatch")
                monitor = subprocess.Popen(
                    [sys._base_executable, "-u", "-B", "-m", "cnn.run_post_review_s",
                     "--watchdog", str(worker.pid), str(os.getpid()), args.gpu_uuid,
                     str(failure), str(telemetry), str(pause)], cwd=ROOT,
                    env=worker_environment(), stdout=subprocess.PIPE, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW)
                ready = read_json_line(monitor, 20)
                if (ready.get("event") != "watchdog_ready"
                        or ready.get("trainer_pid") != worker.pid
                        or ready.get("owner_pid") != os.getpid()
                        or ready.get("initial", {}).get("uuid") != args.gpu_uuid):
                    raise RuntimeError("independent watchdog attachment failed")
                result.update(status="training", watchdog_pid=monitor.pid,
                              initial_gpu=ready["initial"])
                worker.stdin.write("GO\n")
                worker.stdin.flush()
            worker.wait(timeout=60)
            result["worker_exit_code"] = worker.returncode
            if failure.exists():
                result.update(status="hard_stopped",
                              failure=load_json(failure))
            elif worker.returncode:
                result["status"] = "failed_no_retry"
            elif completion_validator is not None:
                result.update(completion_validator(result.get("last_event", {})))
            elif result.get("last_event", {}).get("event") in {
                    "paused_segment", "paused_complete_epoch", "completed_before_GPU"}:
                stop = int(command[command.index("--stop-after-epoch") + 1])
                validate_committed_event(result["last_event"], args.output, stop)
                checkpoint = Path(result["last_event"]["checkpoint"])
                if not checkpoint.is_file():
                    raise FileNotFoundError("committed checkpoint is missing")
                result["checkpoint_sha256"] = sha256(checkpoint)
                result["status"] = "paused_or_completed_verified_by_event"
            else:
                raise RuntimeError("trainer ended without a committed pause/completion event")
    except BaseException as error:
        result.update(status="failed_no_retry", error=repr(error))
        if worker is not None and worker.poll() is None:
            from .training_watchdog import request_pause
            request_pause(pause, "launcher_exception")
            if worker.stdin is not None:
                worker.stdin.close()
            try:
                worker.wait(timeout=60)
            except subprocess.TimeoutExpired:
                worker.kill()  # The exact Popen-owned child only.
                worker.wait(timeout=5)
    finally:
        if monitor is not None:
            try:
                monitor.wait(timeout=8)
            except subprocess.TimeoutExpired:
                if worker is not None and worker.poll() is None:
                    worker.kill()
                    worker.wait(timeout=5)
                monitor.terminate()
                monitor.wait(timeout=5)
            monitor.stdout.close()
        if worker is not None:
            if worker.stdin is not None and not worker.stdin.closed:
                worker.stdin.close()
            worker.stdout.close()
        if reader is not None:
            reader.join(timeout=5)
    for name, path in (("stdout", stdout_path), ("stderr", stderr_path),
                       ("telemetry", telemetry), ("watchdog_failure", failure),
                       ("pause_request", pause)):
        if path.is_file():
            result[name] = {"path": str(path), "sha256": sha256(path)}
    return result


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--dataset-sha256", required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--cache-index-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--init-checkpoint", type=Path, required=True)
    parser.add_argument("--init-checkpoint-sha256", required=True)
    parser.add_argument("--experiment-contract", type=Path, required=True)
    parser.add_argument("--experiment-contract-sha256", required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--preflight-sha256", required=True)
    parser.add_argument("--ground-manifest", type=Path, required=True)
    parser.add_argument("--ground-manifest-sha256", required=True)
    parser.add_argument("--ground-receipt", type=Path, required=True)
    parser.add_argument("--ground-receipt-sha256", required=True)
    parser.add_argument("--decision-proof", type=Path)
    parser.add_argument("--decision-proof-sha256")
    parser.add_argument("--continue-to-5", action="store_true")
    parser.add_argument("--gpu-uuid")
    parser.add_argument("--preflight-timeout-seconds", type=float, default=3600.0)
    parser.add_argument("--receipt", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--validate-only", action="store_true")
    mode.add_argument("--execute", action="store_true")
    return parser


def main() -> int:
    if sys.argv[1:2] == ["--watchdog"]:
        from .training_watchdog import watchdog
        watchdog(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4],
                 *(Path(value) for value in sys.argv[5:8]))
        return 0
    args = build_parser().parse_args()
    if args.preflight_timeout_seconds <= 0:
        raise ValueError("--preflight-timeout-seconds must be positive")
    mode = "execute" if args.execute else "validate_only" if args.validate_only else "dry_run"
    gates, identities = inspect(args)
    try:
        command, initialization, stop = build_train_command(args)
    except Exception as error:
        add_gate(gates, "initialization_selection", repr(error), cpu=True)
        command, initialization, stop = [], "blocked", 5 if args.continue_to_5 else 2
    receipt = {
        "status": "inspected", "mode": mode, "training_started": False,
        "receipt_scope": "CPU_launcher_evidence_only_not_GPU_authorization",
        "placeholder_pins_present": any(value == "0" * 64 for value in (
            args.dataset_sha256, args.cache_index_sha256,
            args.experiment_contract_sha256, args.preflight_sha256,
            args.ground_manifest_sha256, args.ground_receipt_sha256)),
        "protocol": PROTOCOL, "parameters": TRAINING,
        "initialization": initialization, "stop_after_epoch": stop,
        "command": command, "identities": identities, "blocked_gates": gates,
        "source_sha256": {
            "run_post_review_s.py": sha256(Path(__file__)),
            "train.py": sha256(Path(__file__).with_name("train.py")),
            "training_watchdog.py": sha256(Path(__file__).with_name("training_watchdog.py")),
            "resume_state.py": sha256(Path(__file__).with_name("resume_state.py")),
        },
    }
    blockers = (gates if mode == "dry_run" else
                [gate for gate in gates if mode in gate["blocks"]])
    if mode == "dry_run":
        receipt["status"] = "dry_run_blocked" if blockers else "dry_run_ready"
    elif mode == "validate_only":
        if blockers:
            receipt["status"] = "validate_only_blocked"
        else:
            receipt["validation"] = run_validate_only(command)
            receipt["status"] = ("validate_only_passed" if
                                 receipt["validation"]["exit_code"] == 0 else
                                 "validate_only_failed")
    else:
        if not args.gpu_uuid:
            add_gate(gates, "gpu_uuid_missing", "--execute requires an owned GPU UUID")
            blockers.append(gates[-1])
        if blockers:
            receipt["status"] = "execute_refused"
        else:
            result = run_protected(command, args)
            receipt.update(training_started=True, protected_segment=result,
                           status=result["status"])
    write_receipt(args.receipt, receipt)
    print(json.dumps({"status": receipt["status"], "receipt": str(args.receipt),
                      "blocked_gates": [gate["gate"] for gate in blockers]}), flush=True)
    return 0 if receipt["status"] in {"dry_run_ready", "dry_run_blocked",
                                      "validate_only_passed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
