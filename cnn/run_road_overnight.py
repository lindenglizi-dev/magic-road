"""Authorized one-night continuation: epoch 20 or 2026-10-04 08:00 +08:00."""
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from .run_road_epoch import DATASET, OUTPUT, REPORTS, ROOT, sha256, worker_environment

DEADLINE_TEXT = "2026-10-04T08:00:00+08:00"
DEADLINE = datetime.fromisoformat(DEADLINE_TEXT).timestamp()
NIGHT = REPORTS / "overnight_20261004"
START = REPORTS / "segment_0008/report.json"
BASELINE = ROOT / "cnn/reports/road_epoch2_val256_cpu_20261004.json"


def continuation(report, exit_code, pause_reason):
    if exit_code or not report.get("recovery_checkpoint_verified"):
        raise ValueError("segment failed or checkpoint was not verified")
    if report["status"] == "completed_target_epoch":
        return "next_epoch"
    if report["status"] == "paused_resumable_segment":
        if pause_reason == "segment_soft_limit":
            return "resume_same_epoch"
        if pause_reason == "night_deadline":
            return "stop_deadline"
    raise ValueError("abnormal segment: stop without retry")


def verify_evaluation(result, baseline, epoch, checkpoint):
    for key in ("dataset_sha256", "image_count", "evaluated_image_content_sha256",
                "architecture_hash", "postprocess_contract", "truth", "ignores"):
        if result[key] != baseline[key]:
            raise ValueError("evaluation changed comparison identity: " + key)
    if (result["checkpoint_epoch_number"] != epoch
            or result["checkpoint_optimizer_steps"] != epoch * 298
            or result["checkpoint_sha256"] != sha256(checkpoint)
            or result["acceptance_eligible"] is not False):
        raise ValueError("evaluation checkpoint or scope mismatch")


def main():
    if time.time() >= DEADLINE - 120:
        raise ValueError("night authorization has expired or is too close to the cutoff")
    start = json.loads(START.read_text(encoding="utf-8"))
    if (start["status"] != "completed_target_epoch" or not start["recovery_checkpoint_verified"]
            or start["last_event"]["epoch_number"] != 3
            or sha256(OUTPUT / "last_resume.pt") != start["checkpoints"]["last_resume.pt"]["sha256"]):
        raise ValueError("night must start from the verified complete epoch 3 checkpoint")
    NIGHT.mkdir()  # Exclusive run directory also prevents a duplicate night launch.
    state = dict(status="starting", owner_pid=os.getpid(), deadline=DEADLINE_TEXT,
                 target_epoch=20, last_completed_epoch=3, current_target=4,
                 baseline_report_sha256=sha256(BASELINE), evaluations=[], segments=[],
                 acceptance_eligible=False)

    def publish():
        state["updated_at"] = datetime.now().astimezone().isoformat()
        temporary = NIGHT / "status.tmp"
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(NIGHT / "status.json")

    try:
        publish()
        iteration = 0
        while state["current_target"] <= 20:
            if time.time() >= DEADLINE - 120:
                state["status"] = "paused_deadline"
                break
            iteration += 1
            if iteration > 64:
                raise ValueError("excessive segments: stop instead of a restart loop")
            target = state["current_target"]
            log = NIGHT / f"segment_{iteration:04d}.log"
            errors = NIGHT / f"segment_{iteration:04d}.stderr.log"
            command = [sys._base_executable, "-u", "-B", "-m", "cnn.run_road_epoch",
                       "--stop-after-epoch", str(target), "--deadline-unix", str(DEADLINE),
                       "--supervisor-pid", str(os.getpid())]
            with log.open("x", encoding="utf-8") as out, errors.open("x", encoding="utf-8") as err:
                worker = subprocess.Popen(command, cwd=ROOT, env=worker_environment(),
                                          stdout=out, stderr=err,
                                          creationflags=subprocess.CREATE_NO_WINDOW)
                state.update(status="training", controller_pid=worker.pid, controller_log=str(log))
                publish()
                code = worker.wait()
            final = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
            report_path = Path(final["report"])
            if report_path.parent.parent.resolve() != REPORTS.resolve():
                raise ValueError("controller report is outside the authorized directory")
            report = json.loads(report_path.read_text(encoding="utf-8"))
            state["segments"].append(dict(report=str(report_path), status=report["status"],
                                          report_sha256=sha256(report_path)))
            pause = report_path.parent / "pause.json"
            reason = json.loads(pause.read_text())["reason"] if pause.exists() else None
            action = continuation(report, code, reason)
            if action == "stop_deadline":
                state["status"] = "paused_deadline"
                break
            if action == "resume_same_epoch":
                publish()
                continue
            state["last_completed_epoch"] = target
            if target % 5 == 0 and time.time() < DEADLINE - 120:
                state["status"] = "evaluating"
                publish()
                checkpoint = OUTPUT / f"epoch_{target - 1:04d}.pt"
                metrics = NIGHT / f"epoch_{target:02d}_val256.json"
                with (NIGHT / f"epoch_{target:02d}_evaluation.log").open("x", encoding="utf-8") as out:
                    subprocess.run([sys._base_executable, "-u", "-B", "-m", "cnn.evaluate",
                                    "--checkpoint", str(checkpoint), "--dataset", str(DATASET),
                                    "--output", str(metrics), "--device", "cpu", "--threads", "2",
                                    "--max-images", "256"], cwd=ROOT, env=worker_environment(),
                                   stdout=out, stderr=subprocess.STDOUT, check=True,
                                   timeout=min(180, DEADLINE - time.time()),
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                result = json.loads(metrics.read_text(encoding="utf-8"))
                baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
                verify_evaluation(result, baseline, target, checkpoint)
                state["evaluations"].append(dict(epoch=target, report=str(metrics),
                    report_sha256=sha256(metrics), metrics=result["diagnostic_metrics_at_0_5"],
                    p95_operating_points=result["p95_operating_points"]))
                publish()
            state["current_target"] = target + 1
            publish()
        else:
            state["status"] = "completed_epoch20"
    except BaseException as error:
        state.update(status="stopped_error_no_retry", error=repr(error))
    finally:
        state["controller_pid"] = None
        publish()
    print(json.dumps(state, ensure_ascii=False), flush=True)
    return 1 if state["status"] == "stopped_error_no_retry" else 0


if __name__ == "__main__":
    raise SystemExit(main())
