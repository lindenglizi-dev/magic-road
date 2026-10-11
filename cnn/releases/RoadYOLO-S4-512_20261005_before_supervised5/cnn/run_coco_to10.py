"""Resume the existing COCO epoch6 checkpoint to a requested complete epoch."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from . import benchmark_cache_gpu as guard
from . import train

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "cnn/runs/coco_full_pretrain300"
CHECKPOINT = OUTPUT / "last.pt"
DATASET = ROOT / "cnn/data/coco_full/dataset.json"
SOURCE_SHA = "51da8c3289ef5ffa24fe9df01567657b8254a9ef982cdef379f12c3437b068d4"
COMMAND = [sys._base_executable, "-u", "-B", "-m", "cnn.train",
           "--dataset", str(DATASET), "--output", str(OUTPUT),
           "--resume", str(CHECKPOINT), "--epochs", "300",
           "--stop-after-epoch", "10", "--workers", "0",
           "--batch-size", "8", "--accum-steps", "8", "--amp", "--mosaic"]


def main():
    import torch

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stop-after-epoch", type=int, default=10)
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()
    target = options.stop_after_epoch
    if not 7 <= target <= 300:
        parser.error("--stop-after-epoch must be between 7 and 300")
    command = COMMAND.copy()
    command[command.index("--stop-after-epoch") + 1] = str(target)
    stamp = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d_%H%M%S")
    report = ROOT / f"cnn/reports/coco_resume6_to{target}_{stamp}.json"
    stdout = report.with_suffix(".stdout.log")
    stderr = report.with_suffix(".stderr.log")
    telemetry = report.with_suffix(".telemetry.jsonl")
    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    args = train.build_parser().parse_args(command[5:])
    protocol = train.protocol_for(args, 1849, None)
    train.ensure_resume_eligible(checkpoint, protocol)
    assert train.sha256(CHECKPOINT) == SOURCE_SHA
    assert checkpoint["epoch"] == 5 and checkpoint["trained_steps"] == 11094
    assert train.sha256(DATASET) == checkpoint["dataset_sha256"]
    source_epoch_sha = train.sha256(OUTPUT / "epoch_0005.pt")
    assert args.stop_after_epoch == target and args.max_steps == 0
    if options.check:
        subprocess.run([COMMAND[0], "-B", "-c",
                        "import sys,torch; from cnn import train; "
                        "assert torch.cuda.is_available(); print(sys.executable)"],
                       cwd=ROOT, check=True,
                       env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)})
        print(f"epoch6 identity, exact resume protocol and epoch{target} stop boundary PASS")
        return 0
    del checkpoint
    for path in (report, stdout, stderr, telemetry):
        if path.exists():
            raise FileExistsError(path)
    guard.HARD_SECONDS = 6 * 3600
    initial = guard.gpu_sample()
    initial["system_available_ram_bytes"] = guard.system_available_ram()
    if guard.stop_reason(initial, 0) or initial["system_available_ram_bytes"] < 6 * (1 << 30):
        raise RuntimeError("GPU/RAM admission failed")
    result = dict(status="starting", command=command, source_checkpoint_sha256=SOURCE_SHA,
                  source_epoch_checkpoint_sha256=source_epoch_sha,
                  start_epoch=6, target_epoch=target, workers=0,
                  training_protocol_sha256=train.protocol_hash(protocol), initial=initial,
                  temperature_stop_c=guard.STOP_C, RAM_reserve_bytes=guard.RAM_RESERVE,
                  hard_seconds=guard.HARD_SECONDS)
    started = time.monotonic()
    with stdout.open("x", encoding="utf-8") as out, stderr.open("x", encoding="utf-8") as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err,
                                   env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        result.update(status="running", training_pid=process.pid)
        report.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(dict(status="running", training_pid=process.pid, report=str(report))), flush=True)
        try:
            with telemetry.open("x", encoding="utf-8") as stream:
                while process.poll() is None:
                    sample = guard.gpu_sample(initial["uuid"])
                    sample["system_available_ram_bytes"] = guard.system_available_ram()
                    elapsed = time.monotonic() - started
                    stream.write(json.dumps(dict(elapsed_seconds=elapsed, **sample)) + "\n")
                    stream.flush()
                    reason = guard.stop_reason(sample, elapsed)
                    if reason:
                        raise RuntimeError(reason)
                    time.sleep(5)
            result["exit_code"] = process.returncode
            if process.returncode:
                raise RuntimeError(f"trainer exited with code {process.returncode}; see stderr log")
            final = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
            train.ensure_resume_eligible(final, protocol)
            assert final["epoch"] == target - 1 and final["trained_steps"] == 1849 * target
            assert final["dataset_sha256"] == train.sha256(DATASET)
            assert train.sha256(OUTPUT / "epoch_0005.pt") == source_epoch_sha
            assert (OUTPUT / f"epoch_{target - 1:04d}.pt").is_file()
            assert not (OUTPUT / f"epoch_{target:04d}.pt").exists()
            result.update(status="completed_target_epoch", completed_epochs=target,
                          checkpoint_sha256=train.sha256(CHECKPOINT), metric=final["metric"])
        except BaseException as error:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=30)
            result.update(status="failed_or_partial", error=repr(error), exit_code=process.returncode)
        finally:
            result["elapsed_seconds"] = time.monotonic() - started
            report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result), flush=True)
    return 0 if result["status"] == "completed_target_epoch" else 1


if __name__ == "__main__":
    raise SystemExit(main())
