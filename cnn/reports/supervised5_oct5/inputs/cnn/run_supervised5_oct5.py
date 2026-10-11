"""One isolated supervised batch: frozen epoch 7 -> epoch 12, then stop."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from . import run_road_epoch as segment
from .run_road_overnight import continuation, verify_evaluation

ROOT = segment.ROOT
SOURCE = (ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5/"
          "cnn/runs/person_native_recovery_20261004/epoch_0006.pt")
SOURCE_SHA = "17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42"
SOURCE_PROTOCOL_SHA = "66b17c5fcae093e34f5db15794f017196c361b76402bf71dba6031d44a8ad43e"
OLD256 = (ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5/"
          "cnn/reports/person_native_recovery_20261004/epoch_7_val256.json")
OLD256_SHA = "501282373e41cdc3a26a3b66f61097c95562878bab8012a0fa588eee18ec1ec8"
FULL_BASELINE = ROOT / "cnn/reports/supervised5_baseline_20261005/epoch7_full_val.json"
FULL_BASELINE_LOG = ROOT / "cnn/reports/supervised5_baseline_20261005/full_val.stdout.log"
OUTPUT = ROOT / "cnn/runs/supervised5_oct5"
RUN = ROOT / "cnn/reports/supervised5_oct5"
REPORTS = RUN / "segments"
MODEL_SHA = "403c41b0d2acf7fe789f0f96e9470a60abed9ae23989618a69f61f3f9e00ac4c"
LOSS_SHA = "8bc33d05abd15c00af35627e550d815212387ab6ddc3074f4f023fc9dd09cf79"
TARGET_EPOCH = 12
MAX_SECONDS = 3 * 3600
MAX_BASELINE_WAIT_SECONDS = 30 * 60


def validate_source(checkpoint):
    from . import train
    train.ensure_resume_eligible(checkpoint)
    protocol = checkpoint["training_protocol"]
    expected = {
        "format": "road-yolo-checkpoint-v2", "epoch": 6, "trained_steps": 2086,
        "dataset_sha256": segment.DATASET_SHA,
        "dataset_content_sha256": segment.CONTENT_SHA,
        "architecture_hash": segment.ARCHITECTURE_SHA,
        "training_protocol_sha256": SOURCE_PROTOCOL_SHA, "effective_batch": 64,
    }
    if any(checkpoint.get(key) != value for key, value in expected.items()):
        raise ValueError("not the frozen complete epoch-7 supervised state")
    if (train.protocol_hash(protocol) != SOURCE_PROTOCOL_SHA or protocol["epochs"] != 40
            or protocol["warmup_epochs"] != 5 or protocol["mosaic"] is not False
            or protocol.get("phase") != "supervised"
            or protocol.get("teacher_cache_sha256") is not None):
        raise ValueError("epoch-7 protocol is not supervised no-Mosaic continuation")
    for key in ("model", "optimizer", "scaler", "rng_state"):
        if not isinstance(checkpoint.get(key), dict):
            raise ValueError("missing complete training state: " + key)


def validate_baseline(report, expected_images):
    if (report.get("checkpoint_sha256") != SOURCE_SHA
            or report.get("checkpoint_epoch_number") != 7
            or report.get("checkpoint_optimizer_steps") != 2086
            or report.get("dataset_sha256") != segment.DATASET_SHA
            or report.get("dataset_content_sha256") != segment.CONTENT_SHA
            or report.get("architecture_hash") != segment.ARCHITECTURE_SHA
            or report.get("image_count") != expected_images
            or report.get("total_validation_images") != 5151
            or report.get("validation_subset") is not (expected_images != 5151)
            or report.get("acceptance_eligible") is not False):
        raise ValueError(f"invalid frozen epoch-7 baseline identity ({expected_images} images)")


def comparison(candidate, baseline):
    classes = {}
    for name in ("person", "vehicle"):
        current = candidate["diagnostic_metrics_at_0_5"]["classes"][name]
        old = baseline["diagnostic_metrics_at_0_5"]["classes"][name]
        keys = ("precision", "recall", "ap", "ap50", "ap50_95")
        classes[name] = {"candidate": {key: current[key] for key in keys},
                         "baseline": {key: old[key] for key in keys},
                         "delta_percentage_points": {
                             key: 100 * (current[key] - old[key]) for key in keys}}
    tolerance_pp = 1e-12
    passed = (classes["person"]["delta_percentage_points"]["ap50"] >= 1 - tolerance_pp
              and classes["vehicle"]["delta_percentage_points"]["ap50"] >= -1 - tolerance_pp)
    return {"classes": classes, "gate_metric": "ap50_percentage_point_delta",
            "gate_thresholds": {"person_min": 1.0, "vehicle_min": -1.0},
            "floating_point_tolerance_pp": tolerance_pp,
            "development_heuristic_pass": passed,
            "formal_statistical_significance": False}


def configure_segment():
    segment.COCO, segment.COCO_SHA = SOURCE, SOURCE_SHA
    segment.OUTPUT, segment.REPORTS = OUTPUT, REPORTS
    segment.PROTOCOL_SHA = SOURCE_PROTOCOL_SHA
    segment.EXPECTED_MODEL_SHA = {"model.py": MODEL_SHA, "loss.py": LOSS_SHA}


def completed_baseline_summary(path):
    if not path.exists():
        return None
    lines = [line for line in path.read_text(
        encoding="utf-8", errors="replace").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        summary = json.loads(lines[-1])
    except json.JSONDecodeError:
        return None
    required = ("thresholds", "metrics", "timing_seconds")
    return summary if isinstance(summary, dict) and all(key in summary for key in required) else None


def run_segment(arguments):
    before = set(REPORTS.glob("segment_*")) if REPORTS.exists() else set()
    saved = sys.argv
    try:
        sys.argv = ["run_road_epoch"] + arguments
        code = segment.main()
    finally:
        sys.argv = saved
    created = set(REPORTS.glob("segment_*")) - before
    if len(created) != 1:
        raise ValueError("segment launcher did not create exactly one report directory")
    report_path = created.pop() / "report.json"
    return code, report_path, json.loads(report_path.read_text(encoding="utf-8"))


def evaluate(checkpoint, output, max_images, log, deadline):
    command = [sys._base_executable, "-u", "-B", "-m", "cnn.evaluate",
               "--checkpoint", str(checkpoint), "--dataset", str(segment.DATASET),
               "--output", str(output), "--device", "cpu", "--threads", "2"]
    if max_images:
        command += ["--max-images", str(max_images)]
    remaining = deadline - time.time()
    if remaining <= 0:
        raise TimeoutError("three-hour batch deadline reached before CPU evaluation")
    with log.open("x", encoding="utf-8") as stream:
        subprocess.run(command, cwd=ROOT, env=segment.worker_environment(), stdout=stream,
                       stderr=subprocess.STDOUT, check=True, timeout=remaining,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    return json.loads(output.read_text(encoding="utf-8"))


def main():
    class DeadlineReached(Exception):
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait-baseline", action="store_true",
                        help="wait at most 30 minutes for the already-running full baseline")
    options = parser.parse_args()
    if OUTPUT.exists() or RUN.exists():
        raise FileExistsError("supervised-five batch already reserved; never duplicate or restart")
    if segment.sha256(SOURCE) != SOURCE_SHA or segment.sha256(OLD256) != OLD256_SHA:
        raise ValueError("frozen epoch-7 source or val256 baseline changed")

    import torch
    checkpoint = torch.load(SOURCE, map_location="cpu", weights_only=False)
    validate_source(checkpoint)
    del checkpoint
    old256 = json.loads(OLD256.read_text(encoding="utf-8"))
    validate_baseline(old256, 256)

    RUN.mkdir()
    started = time.time()
    deadline = started + MAX_SECONDS
    source_paths = list((ROOT / "cnn").glob("*.py"))
    sources = {path.name: segment.sha256(path) for path in source_paths}
    full_baseline_sha = None
    state = {
        "status": "waiting_full_baseline", "owner_pid": os.getpid(),
        "started_at": datetime.now().astimezone().isoformat(), "deadline_unix": deadline,
        "start_epoch": 7, "target_epoch": TARGET_EPOCH, "additional_epochs": 5,
        "last_completed_epoch": 7, "source_checkpoint": str(SOURCE),
        "source_checkpoint_sha256": SOURCE_SHA,
        "initialization": "full_model_optimizer_scaler_RNG_continuation_no_warmup_reset",
        "training_schedule": "original_40_epoch_schedule", "mosaic": False,
        "dataset_scope": "VisDrone2019-VID aerial; no IntersectionFlow training data",
        "source_sha256": sources, "segments": [], "acceptance_eligible": False,
        "formal_acceptance": False, "development_continue_eligible": False,
    }

    def publish():
        state["updated_at"] = datetime.now().astimezone().isoformat()
        temporary = RUN / "status.tmp"
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(RUN / "status.json")

    def verify_sources():
        if {path.name: segment.sha256(path) for path in (ROOT / "cnn").glob("*.py")} != sources:
            raise ValueError("Python sources changed during supervised-five batch")
        if segment.sha256(SOURCE) != SOURCE_SHA or segment.sha256(OLD256) != OLD256_SHA:
            raise ValueError("frozen epoch-7 input changed during supervised-five batch")
        if full_baseline_sha is not None and segment.sha256(FULL_BASELINE) != full_baseline_sha:
            raise ValueError("full epoch-7 baseline changed during supervised-five batch")

    try:
        publish()
        wait_until = min(deadline, started + MAX_BASELINE_WAIT_SECONDS)
        while True:
            if FULL_BASELINE.exists() and completed_baseline_summary(FULL_BASELINE_LOG):
                break
            if not options.wait_baseline:
                raise FileNotFoundError("complete full baseline is not ready; pass --wait-baseline")
            if time.time() >= wait_until:
                raise TimeoutError("full baseline was not completed within 30 minutes")
            state["baseline_wait_seconds"] = time.time() - started
            publish()
            time.sleep(5)
        full_baseline = json.loads(FULL_BASELINE.read_text(encoding="utf-8"))
        validate_baseline(full_baseline, 5151)
        full_baseline_sha = segment.sha256(FULL_BASELINE)
        state.update(full_baseline=str(FULL_BASELINE),
                     full_baseline_sha256=full_baseline_sha, status="preflight")
        publish()
        verify_sources()

        inputs = RUN / "inputs"
        (inputs / "cnn").mkdir(parents=True)
        for path in source_paths:
            shutil.copyfile(path, inputs / "cnn" / path.name)
        shutil.copyfile(FULL_BASELINE, inputs / "epoch7_full_val.json")
        shutil.copyfile(OLD256, inputs / "epoch7_val256.json")
        if any(segment.sha256(inputs / "cnn" / path.name) != sources[path.name]
               for path in source_paths):
            raise ValueError("Python input snapshot differs from active source")
        if (segment.sha256(inputs / "epoch7_full_val.json") != full_baseline_sha
                or segment.sha256(inputs / "epoch7_val256.json") != OLD256_SHA):
            raise ValueError("baseline input snapshot differs from validated reports")
        state["input_snapshot"] = str(inputs)
        publish()

        configure_segment()
        OUTPUT.mkdir()
        shutil.copyfile(SOURCE, OUTPUT / "last.pt")
        if segment.sha256(OUTPUT / "last.pt") != SOURCE_SHA:
            raise ValueError("independent full-state copy differs from frozen source")

        code, report_path, report = run_segment(["--parity"])
        if code or report.get("status") != "passed_GPU_resume_parity":
            raise ValueError("new-source GPU AMP resume parity did not pass")
        state["segments"].append({"kind": "tiny_GPU_AMP_resume_equivalence",
                                  "scope": "resume mechanism only; not full-network accuracy",
                                  "report": str(report_path),
                                  "sha256": segment.sha256(report_path)})
        state["status"] = "training"
        publish()

        for _ in range(16):
            verify_sources()
            code, report_path, report = run_segment([
                "--no-mosaic", "--stop-after-epoch", str(TARGET_EPOCH),
                "--deadline-unix", str(deadline), "--supervisor-pid", str(os.getpid())])
            state["segments"].append({"kind": "supervised", "report": str(report_path),
                                      "status": report.get("status"),
                                      "sha256": segment.sha256(report_path)})
            complete = report.get("checkpoints", {}).get("last.pt", {})
            if complete.get("valid"):
                state["last_completed_epoch"] = complete["epoch"] + 1
            pause = report_path.parent / "pause.json"
            reason = json.loads(pause.read_text(encoding="utf-8"))["reason"] if pause.exists() else None
            action = continuation(report, code, reason)
            publish()
            if action == "resume_same_epoch":
                continue
            if action == "stop_deadline":
                state["status"] = "paused_deadline_no_retry"
                raise DeadlineReached
            break
        else:
            raise ValueError("segment cap reached; no unlimited retry loop")
        if state["last_completed_epoch"] != TARGET_EPOCH:
            raise ValueError("batch did not finish exactly five new epochs")

        verify_sources()
        state["status"] = "evaluating"
        publish()
        candidate = OUTPUT / "epoch_0011.pt"
        full_path, subset_path = RUN / "epoch12_full_val.json", RUN / "epoch12_val256.json"
        full = evaluate(candidate, full_path, 0, RUN / "full_val.log", deadline)
        subset = evaluate(candidate, subset_path, 256, RUN / "val256.log", deadline)
        verify_evaluation(full, full_baseline, TARGET_EPOCH, candidate)
        verify_evaluation(subset, old256, TARGET_EPOCH, candidate)
        comparisons = {"full5151": comparison(full, full_baseline),
                       "old256": comparison(subset, old256)}
        eligible = all(value["development_heuristic_pass"] for value in comparisons.values())
        state.update(status="completed_epoch12_evaluated", comparisons=comparisons,
                     evaluation_reports={
                         "full5151": {"path": str(full_path), "sha256": segment.sha256(full_path)},
                         "old256": {"path": str(subset_path), "sha256": segment.sha256(subset_path)}},
                     acceptance_eligible=False, formal_acceptance=False,
                     development_continue_eligible=eligible,
                     continuation_to_epochs_10_15_20_requires_new_authorization=True,
                     distillation_started=False)
    except DeadlineReached:
        pass
    except BaseException as error:
        state.update(status="stopped_error_no_retry", error=repr(error), acceptance_eligible=False)
    finally:
        try:
            verify_sources()
            state["source_freeze_verified"] = True
        except Exception as error:
            state.update(status="stopped_error_no_retry", error=repr(error),
                         source_freeze_verified=False, acceptance_eligible=False,
                         development_continue_eligible=False)
        state["total_seconds"] = time.time() - started
        publish()
        print(json.dumps({"status": state["status"], "report": str(RUN / "status.json")}), flush=True)
    return int(state["status"] == "stopped_error_no_retry")


if __name__ == "__main__":
    raise SystemExit(main())
