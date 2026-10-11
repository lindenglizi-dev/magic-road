"""Run one recoverable road-training segment, with independent protection."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time

from .training_watchdog import HARD_SECONDS, SOFT_SECONDS, watchdog

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
COCO = ROOT / "cnn/runs/coco_full_pretrain300/last.pt"
CACHE = ROOT / "cnn/data/cache_road_recovery_20261003"
CACHE_RECEIPT = ROOT / "cnn/reports/cache_road_recovery_migration_20261003.json"
CACHE_RECEIPT_SHA = "9d0217972add8bdbc546e88914844d51665c9106e6f2448fb6c1311bfb70e330"
OUTPUT = ROOT / "cnn/runs/road40_from_coco6_segmented_20261003"
REPORTS = ROOT / "cnn/reports/road_segmented_20261003"
COCO_SHA = "51da8c3289ef5ffa24fe9df01567657b8254a9ef982cdef379f12c3437b068d4"
DATASET_SHA = "ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4"
CONTENT_SHA = "45458e231d561e45c364e09b2913e90a2182af6dd0d158b71f09bf903e2851ad"
PROTOCOL_SHA = "bcda54929c3656fc7ab7a385ec84f0af55b1597c13206b91558db95762ecc328"
ARCHITECTURE_SHA = "106ccd0f223b1cefaff8e36408d3968aee3e4a1703d17e27786db58eb8124595"
GPU_UUID = "GPU-a85887e6-358e-1ebb-cf09-81b558fa321a"
EXPECTED_MODEL_SHA = {
    "model.py": "403c41b0d2acf7fe789f0f96e9470a60abed9ae23989618a69f61f3f9e00ac4c",
    "loss.py": "dc1c2c6423a154bb4eecd579fc7433345197557b1caa8fcb78435c95dcb01adb",
}
ROAD_OUTPUT = OUTPUT
ROAD_REPORTS = REPORTS
ROAD_PROTOCOL_SHA = PROTOCOL_SHA
ROAD20_SHA = "61edd64aa14409e5d8df9aeed7e519440e41ead353e551134b774bcc038bf94c"
NATIVE2 = ROOT / "cnn/runs/person_ab_20261004_native/epoch_0001.pt"
NATIVE2_SHA = "18656b87e00ad97ccace996ed306c83d3224869db8d94be91335f3f2e581319d"
RECOVERY_OUTPUT = ROOT / "cnn/runs/person_native_recovery_20261004"
RECOVERY_REPORTS = ROOT / "cnn/reports/person_native_recovery_20261004"


def configure_person_ab(arm):
    """Separate weights-only experiment; never mutate the original road run."""
    global COCO, COCO_SHA, OUTPUT, REPORTS, PROTOCOL_SHA
    if arm not in ("native", "mosaic"):
        raise ValueError("invalid fixed person experiment arm")
    with (ROAD_OUTPUT / "train_log.jsonl").open(encoding="utf-8") as stream:
        start = json.loads(stream.readline())
    protocol = start["training_protocol"]
    encoded = json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if hashlib.sha256(encoded).hexdigest() != ROAD_PROTOCOL_SHA:
        raise ValueError("original road training protocol changed")
    checkpoint = ROAD_OUTPUT / "epoch_0019.pt"
    if sha256(checkpoint) != ROAD20_SHA:
        raise ValueError("frozen epoch20 checkpoint changed")
    protocol = {**protocol, "mosaic": arm == "mosaic"}
    encoded = json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
    PROTOCOL_SHA = hashlib.sha256(encoded).hexdigest()
    COCO, COCO_SHA = checkpoint, ROAD20_SHA
    OUTPUT = ROOT / f"cnn/runs/person_ab_20261004_{arm}"
    REPORTS = ROOT / f"cnn/reports/person_ab_20261004/{arm}"


def configure_person_recovery():
    """Continue the native arm's full training state in a separate five-epoch run."""
    global COCO, COCO_SHA, OUTPUT, REPORTS
    configure_person_ab("native")
    if sha256(NATIVE2) != NATIVE2_SHA:
        raise ValueError("native epoch2 source changed")
    COCO, COCO_SHA = NATIVE2, NATIVE2_SHA
    OUTPUT, REPORTS = RECOVERY_OUTPUT, RECOVERY_REPORTS / "segments"
    if not any((OUTPUT / name).is_file() for name in
               ("last.pt", "last_resume.pt", "last_resume.prev.pt")):
        raise ValueError("recovery requires copied full state; weights-only initialization forbidden")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def worker_environment():
    # Launch the actual Python process, not the Windows venv redirector PID.
    site = Path(sys.executable).parent.parent / "Lib/site-packages"
    return {**os.environ, "PYTHONPATH": os.pathsep.join(
        [str(ROOT), str(site), os.environ.get("PYTHONPATH", "")])}


def read_ready(process):
    lines = queue.Queue()
    threading.Thread(target=lambda: lines.put(process.stdout.readline()), daemon=True).start()
    message = json.loads(lines.get(timeout=20))
    if message.get("event") != "watchdog_ready":
        raise RuntimeError("independent watchdog failed; CUDA permission denied")
    return message


def stream_events(process, path, events):
    try:
        with path.open("x", encoding="utf-8") as stream:
            for line in process.stdout:
                stream.write(line)
                stream.flush()
                try:
                    value = json.loads(line)
                except ValueError:
                    continue
                if isinstance(value, dict) and value.get("event"):
                    events.put(value)
    except Exception as error:
        events.put(dict(event="stdout_reader_failed", error=repr(error)))
    finally:
        events.put(dict(event="worker_stdout_closed"))


def next_segment():
    REPORTS.mkdir(parents=True, exist_ok=True)
    indices = [int(path.name.split("_")[1]) for path in REPORTS.iterdir()
               if path.is_dir() and path.name.startswith("segment_")
               and path.name.split("_")[1].isdigit()]
    segment = REPORTS / f"segment_{max(indices, default=0) + 1:04d}"
    segment.mkdir()
    return segment


def summarize_checkpoints():
    # Called only after trainer exit, so this never doubles Torch RAM during training.
    import torch
    from . import train
    result = {}
    for name in ("last_resume.pt", "last_resume.prev.pt", "last.pt"):
        path = OUTPUT / name
        if not path.exists():
            continue
        try:
            state = torch.load(path, map_location="cpu", weights_only=False)
            train.ensure_resume_eligible(state)
            expected = {"dataset_sha256": DATASET_SHA, "dataset_content_sha256": CONTENT_SHA,
                        "architecture_hash": ARCHITECTURE_SHA,
                        "training_protocol_sha256": PROTOCOL_SHA,
                        "class_contract": train.CLASS_CONTRACT}
            if any(state.get(key) != value for key, value in expected.items()):
                raise ValueError("checkpoint is not the frozen road experiment")
            if train.protocol_hash(state["training_protocol"]) != PROTOCOL_SHA:
                raise ValueError("checkpoint protocol digest mismatch")
            train._validate_v3_cursors(state, train_size=19050, val_size=5151,
                                      batch_size=8, accum_steps=8,
                                      optimizer_steps_per_epoch=298, seed=42)
            for key in ("model", "optimizer", "rng_state", "scaler"):
                if not isinstance(state.get(key), dict):
                    raise ValueError("checkpoint missing " + key)
            fields = ("epoch", "epoch_index", "stage", "trained_steps", "next_microbatch",
                      "next_sample_cursor", "epoch_samples", "val_next_batch", "val_samples",
                      "metric")
            result[name] = {key: state[key] for key in fields if key in state}
            result[name].update(valid=True, sha256=sha256(path), format=state["format"])
        except Exception as error:
            result[name] = dict(valid=False, error=repr(error))
    return result


def validate_segment_result(result):
    """A clean exit/event alone is not evidence of a committed training state."""
    status = result["status"]
    if status not in ("paused_resumable_segment", "completed_first_epoch", "completed_target_epoch"):
        return
    event = result.get("last_event", {})
    expected_path = OUTPUT / ("last_resume.pt" if status == "paused_resumable_segment" else "last.pt")
    if event.get("event") != "completed_before_GPU" and not result.get("watchdog_pid"):
        raise ValueError("training completed without independent protection")
    if Path(event.get("checkpoint", "")).resolve() != expected_path.resolve():
        raise ValueError("completion event refers to a different checkpoint")
    state = result.get("checkpoints", {}).get(expected_path.name, {})
    if not state.get("valid") or state.get("trained_steps") != event.get("trained_steps"):
        raise ValueError("completion event has no matching valid checkpoint")
    if status == "paused_resumable_segment":
        for key in ("stage", "epoch_index", "next_microbatch", "next_sample_cursor", "val_next_batch"):
            if state.get(key) != event.get(key):
                raise ValueError("pause event cursor differs from committed checkpoint: " + key)
    else:
        target = result.get("stop_after_epoch", 1)
        if (state.get("epoch") != target - 1 or state.get("trained_steps") != 298 * target
                or event.get("epoch_number") != target):
            raise ValueError("target full road epoch has not completed")
    result["recovery_checkpoint_verified"] = True


def main():
    if sys.argv[1:2] in (["--watchdog"], ["--watchdog-parity"]):
        if sys.argv[1] == "--watchdog-parity":
            from . import training_watchdog as protection
            protection.HARD_SECONDS, protection.SOFT_SECONDS = 295, 285
        watchdog(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4],
                 Path(sys.argv[5]), Path(sys.argv[6]), Path(sys.argv[7]),
                 float(sys.argv[8]) if len(sys.argv) > 8 else None,
                 int(sys.argv[9]) if len(sys.argv) > 9 else None)
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parity", action="store_true", help="bounded GPU resume regression, not training")
    parser.add_argument("--stop-after-epoch", type=int, default=1,
                        help="save and pause after this road epoch; retain the 40-epoch schedule")
    parser.add_argument("--deadline-unix", type=float,
                        help="absolute stop time; independent protector pauses 60 seconds earlier")
    parser.add_argument("--supervisor-pid", type=int, help="pin the owning overnight process too")
    parser.add_argument("--person-ab-arm", choices=("native", "mosaic"),
                        help="isolated epoch20 weights-only experiment, at most two epochs")
    parser.add_argument("--person-recovery-five", action="store_true",
                        help="full-state native epoch2 continuation, fixed stop at epoch7")
    options = parser.parse_args()
    if not 1 <= options.stop_after_epoch <= 40:
        parser.error("--stop-after-epoch must be between 1 and 40")
    if options.deadline_unix is not None and (options.parity or
            not math.isfinite(options.deadline_unix) or options.deadline_unix <= time.time()):
        parser.error("deadline must be a finite future timestamp for training")
    if options.supervisor_pid is not None and (options.supervisor_pid <= 0 or options.deadline_unix is None):
        parser.error("supervisor requires a positive PID and an absolute deadline")
    if options.person_ab_arm:
        if options.parity or options.stop_after_epoch > 2:
            parser.error("person A/B is non-parity training bounded to two epochs per arm")
        configure_person_ab(options.person_ab_arm)
    if options.person_recovery_five:
        if (options.parity or options.person_ab_arm or options.stop_after_epoch != 7
                or options.supervisor_pid is None):
            parser.error("native recovery requires an exclusive supervised epoch7 target")
        configure_person_recovery()
    if os.name != "nt":
        raise RuntimeError("fixed Windows local training experiment")
    if sha256(COCO) != COCO_SHA or sha256(DATASET) != DATASET_SHA:
        raise ValueError("original checkpoint/dataset identity changed")
    if any(sha256(ROOT / "cnn" / name) != value
           for name, value in EXPECTED_MODEL_SHA.items()):
        raise ValueError("network or loss changed")
    if not options.parity:
        proof_reports = ROAD_REPORTS if options.person_ab_arm or options.person_recovery_five else REPORTS
        proof = json.loads(max(proof_reports.glob("segment_*/parity.json")).read_text())
        if (proof.get("status") != "passed_GPU_AMP_segment_resume_equivalence"
                or proof.get("maximum_compared_difference") != 0
                or any(sha256(ROOT / "cnn" / name) != value
                       for name, value in proof["test_source_sha256"].items())):
            raise ValueError("GPU resume verification is missing or stale")
    if sha256(CACHE_RECEIPT) != CACHE_RECEIPT_SHA:
        raise ValueError("reviewed cache migration receipt changed")
    receipt = json.loads(CACHE_RECEIPT.read_text(encoding="utf-8"))
    index_sha = sha256(CACHE / "index.json")
    if (receipt.get("cache_index_sha256") != index_sha
            or receipt.get("dataset_sha256") != DATASET_SHA
            or receipt.get("dataset_content_sha256") != CONTENT_SHA
            or receipt.get("status") != "passed_scoped_preprocessing_identity_migration_no_pixel_reread"):
        raise ValueError("reviewed cache migration receipt mismatch")
    segment = next_segment()
    pause = segment / "pause.json"
    failure = segment / "watchdog_failure.json"
    telemetry = segment / "telemetry.jsonl"
    sources = {path.name: sha256(path) for path in (ROOT / "cnn").glob("*.py")}
    result = dict(status="preflight", segment=str(segment), output=str(OUTPUT),
                  source_checkpoint_sha256=COCO_SHA, dataset_sha256=DATASET_SHA,
                  cache_index_sha256=index_sha, source_sha256=sources,
                  hard_seconds=295 if options.parity else HARD_SECONDS,
                  soft_seconds=285 if options.parity else SOFT_SECONDS,
                  temperature_stop_c=75, memory_threshold_enabled=False,
                  stop_after_epoch=options.stop_after_epoch,
                  deadline_unix=options.deadline_unix,
                  supervisor_pid=options.supervisor_pid,
                  person_ab_arm=options.person_ab_arm,
                  person_recovery_five=options.person_recovery_five,
                  initialization=("native_epoch2_full_state_continuation"
                      if options.person_recovery_five else
                      "epoch20_weights_only_fresh_optimizer_rng_and_schedule"
                      if options.person_ab_arm else "original_road_experiment"),
                  acceptance_eligible=False)
    worker = monitor = reader = None
    events = queue.Queue()
    started = time.monotonic()
    gpu_started = None
    try:
        checkpoint = OUTPUT / "last_resume.pt"
        previous = OUTPUT / "last_resume.prev.pt"
        command = [sys._base_executable, "-u", "-B", "-m", "cnn.train",
                   "--dataset", str(DATASET), "--output", str(OUTPUT),
                   "--epochs", "40", "--stop-after-epoch", str(options.stop_after_epoch),
                   "--batch-size", "8", "--accum-steps", "8", "--workers", "0",
                   "--device", "cuda", "--input-cache", str(CACHE),
                   "--input-cache-index-sha256", index_sha,
                   "--checkpoint-every-steps", "10", "--checkpoint-every-seconds", "120",
                   "--pause-request", str(pause), "--supervised-start"]
        if options.person_ab_arm == "native" or options.person_recovery_five:
            command.append("--no-mosaic")
        if checkpoint.exists() or previous.exists():
            command += ["--resume", str(checkpoint if checkpoint.exists() else previous)]
        elif options.person_recovery_five:
            command += ["--resume", str(OUTPUT / "last.pt")]
        else:
            command += ["--init-checkpoint", str(COCO)]
        if options.parity:
            command = [sys._base_executable, "-u", "-B", "-m", "cnn.test_segment_resume",
                       "--gpu-parity", "--supervised-start", "--output", str(segment / "parity.json")]
        result["command"] = command
        with (segment / "stderr.log").open("x", encoding="utf-8") as error_log:
            worker = subprocess.Popen(command, cwd=ROOT, env=worker_environment(),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=error_log, text=True, bufsize=1,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            result["trainer_pid"] = worker.pid
            reader = threading.Thread(target=stream_events,
                                      args=(worker, segment / "stdout.log", events), daemon=True)
            reader.start()
            print(json.dumps(dict(event="CPU_preflight_started", trainer_pid=worker.pid,
                                  segment=str(segment), no_GPU_window_started=True)), flush=True)
            # Drain the committed final event even when exit beats the reader thread.
            while True:
                if monitor is not None and monitor.poll() is not None and worker.poll() is None:
                    raise RuntimeError("independent protector exited while trainer is alive")
                try:
                    event = events.get(timeout=1)
                except queue.Empty:
                    if monitor is not None and monitor.poll() is not None and worker.poll() is None:
                        raise RuntimeError("independent protector exited while trainer is alive")
                    continue
                name = event["event"]
                if name == "worker_stdout_closed":
                    break
                if name == "stdout_reader_failed":
                    raise RuntimeError(event["error"])
                if name == "preflight_ready":
                    if monitor is not None:
                        raise RuntimeError("duplicate preflight handshake")
                    actual_pid = event.get("trainer_pid", event.get("pid"))
                    if actual_pid != worker.pid:
                        raise ValueError("actual trainer PID does not match owned process")
                    result["preflight_seconds"] = time.monotonic() - started
                    monitor = subprocess.Popen(
                        [sys._base_executable, "-u", "-B", "-m", "cnn.run_road_epoch",
                         "--watchdog-parity" if options.parity else "--watchdog",
                         str(worker.pid), str(os.getpid()), GPU_UUID,
                         str(failure), str(telemetry), str(pause)] +
                        ([] if options.deadline_unix is None else [str(options.deadline_unix)]) +
                        ([] if options.supervisor_pid is None else [str(options.supervisor_pid)]),
                        cwd=ROOT, env=worker_environment(), stdout=subprocess.PIPE, text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW)
                    ready = read_ready(monitor)
                    if (ready.get("trainer_pid") != worker.pid
                            or ready.get("owner_pid") != os.getpid()
                            or ready.get("initial", {}).get("uuid") != GPU_UUID):
                        raise ValueError("independent watchdog identity mismatch")
                    gpu_started = ready["started_monotonic"]
                    result.update(status="training", watchdog_pid=monitor.pid,
                                  initial_gpu=ready["initial"])
                    worker.stdin.write("GO\n")
                    worker.stdin.flush()
                    print(json.dumps({**ready, "event": "GPU_segment_started"}), flush=True)
                else:
                    result["last_event"] = event
                    print(json.dumps(event), flush=True)
            worker.wait()
            reader.join(timeout=5)
            result["worker_exit_code"] = worker.returncode
            last = result.get("last_event", {})
            if failure.exists():
                result.update(status="hard_stopped", failure=json.loads(failure.read_text()))
            elif worker.returncode:
                result.update(status="failed", error="trainer exited; see stderr.log")
            elif options.parity and last.get("event") == "parity_passed":
                proof = json.loads((segment / "parity.json").read_text())
                if (monitor is None or proof.get("status") != "passed_GPU_AMP_segment_resume_equivalence"
                        or proof.get("maximum_compared_difference") != 0):
                    raise ValueError("GPU resume equivalence did not pass")
                result.update(status="passed_GPU_resume_parity", parity=proof)
            elif last.get("event") == "paused_segment":
                result["status"] = "paused_resumable_segment"
            elif last.get("event") in ("paused_complete_epoch", "completed_before_GPU"):
                result["status"] = ("completed_first_epoch" if options.stop_after_epoch == 1
                                    else "completed_target_epoch")
            else:
                raise RuntimeError("trainer ended without a committed pause/completion event")
    except BaseException as error:
        result.update(status="failed", error=repr(error))
        if worker is not None and worker.poll() is None:
            # No implicit restart. Ask the owned worker to leave at a safe boundary.
            from .training_watchdog import request_pause
            request_pause(pause, "controller_exception")
            if worker.stdin is not None:
                worker.stdin.close()
            try:
                worker.wait(timeout=60)
            except subprocess.TimeoutExpired:
                worker.kill()
                worker.wait(timeout=5)
    finally:
        if monitor is not None:
            try:
                monitor.wait(timeout=8)
            except subprocess.TimeoutExpired:
                if worker is not None and worker.poll() is None:
                    worker.kill()
                    worker.wait(timeout=5)
                monitor.terminate()  # Only after our trainer has exited.
                monitor.wait(timeout=5)
            monitor.stdout.close()
        if worker is not None:
            if worker.stdin is not None and not worker.stdin.closed:
                worker.stdin.close()
            worker.stdout.close()
        if reader is not None:
            reader.join(timeout=5)
        if gpu_started is not None:
            result["segment_seconds"] = time.monotonic() - gpu_started
        result["total_seconds"] = time.monotonic() - started
        if failure.exists():
            try:
                result.update(status="hard_stopped", failure=json.loads(failure.read_text()))
            except Exception as error:
                result.update(status="failed", failure_receipt_error=repr(error))
        result["original_checkpoint_sha256_after"] = sha256(COCO)
        if result["original_checkpoint_sha256_after"] != COCO_SHA or any(
                sha256(ROOT / "cnn" / name) != value for name, value in sources.items()):
            result.update(status="failed", error="source or original checkpoint changed during segment")
        try:
            result["checkpoints"] = summarize_checkpoints()
            validate_segment_result(result)
        except Exception as error:
            result.update(checkpoint_inspection_error=repr(error), recovery_checkpoint_verified=False)
            if result["status"] != "hard_stopped":
                result["status"] = "failed"
        if telemetry.exists():
            samples = []
            invalid_rows = 0
            try:
                for line in telemetry.read_text().splitlines():
                    try:
                        value = json.loads(line)
                        if not isinstance(value, dict):
                            raise ValueError("telemetry row is not an object")
                        samples.append(value)
                    except ValueError:
                        invalid_rows += 1  # A killed monitor may leave its final row incomplete.
                result["telemetry_sha256"] = sha256(telemetry)
            except Exception as error:
                result["telemetry_read_error"] = repr(error)
            valid = [sample for sample in samples if "temperature_c" in sample]
            result.update(telemetry_samples=len(samples),
                          incomplete_telemetry_rows=invalid_rows,
                          telemetry_warnings=sum(bool(sample.get("warning")) for sample in samples))
            if valid:
                result["peak_temperature_c"] = max(sample["temperature_c"] for sample in valid)
        with (segment / "report.json").open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
    print(json.dumps(dict(status=result["status"], report=str(segment / "report.json"))), flush=True)
    return 0 if result["status"] in ("paused_resumable_segment", "completed_first_epoch",
                                    "completed_target_epoch", "passed_GPU_resume_parity") else 1


if __name__ == "__main__":
    raise SystemExit(main())
