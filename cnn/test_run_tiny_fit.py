"""CPU-only tiny-fit launcher bounds and fail-closed handshake checks."""
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from . import run_post_review_s as protected
from . import run_tiny_fit as tiny


def main():
    contract, command = tiny.verify_prepared()
    for key, value in (("--max-steps", "300"), ("--epochs", "75"),
                       ("--batch-size", "8"), ("--accum-steps", "1"),
                       ("--checkpoint-kind", "diagnostic"), ("--stop-after-epoch", "75")):
        assert command[command.index(key) + 1] == value
    assert "--resume" not in command and "--no-mosaic" in command and "--no-amp" in command
    for event in ({"event": "epoch"}, {"event": "paused_complete_epoch",
                  "epoch_number": 75, "trained_steps": 299, "checkpoint": str(tiny.RUN / "last.pt")}):
        try:
            tiny.verify_completion(event, contract)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid completion accepted")

    class Capture(io.StringIO):
        def close(self):
            pass

    class Worker:
        pid, returncode = 999, 0
        def __init__(self):
            self.stdin = Capture()
            self.stdout = io.StringIO(json.dumps(dict(event="preflight_ready", trainer_pid=999,
                                                     dataset_sha256="wrong")) + "\n")
        def poll(self):
            return 0
        def wait(self, **_kwargs):
            return 0

    with tempfile.TemporaryDirectory(dir=tiny.ROOT) as directory:
        args = SimpleNamespace(receipt=Path(directory) / "segment.json", gpu_uuid="unused",
                               output=Path(directory) / "run", preflight_timeout_seconds=5)
        worker = Worker()
        with patch.object(protected.subprocess, "Popen", return_value=worker) as launch:
            result = protected.run_protected(command, args, expected_ready=dict(dataset_sha256="expected"))
        assert result["status"] == "failed_no_retry"
        assert "identity mismatch" in result["error"]
        assert "GO" not in worker.stdin.getvalue() and launch.call_count == 1
    # stdout EOF may arrive while poll still reports a live process at teardown.
    class Teardown(Worker):
        def __init__(self):
            super().__init__()
            self.stdout = io.StringIO(json.dumps(dict(event="preflight_ready", trainer_pid=999,
                dataset_sha256="expected")) + "\n" + json.dumps(dict(event="finished")) + "\n")
            self.waits = []
        def poll(self):
            return None
        def wait(self, **kwargs):
            self.waits.append(kwargs)
            return 0
    with tempfile.TemporaryDirectory(dir=tiny.ROOT) as directory:
        args.receipt = Path(directory) / "segment.json"
        worker, monitor = Teardown(), Worker()
        monitor.stdout = io.StringIO(json.dumps(dict(event="watchdog_ready", trainer_pid=999,
            owner_pid=os.getpid(), initial=dict(uuid="unused"))) + "\n")
        def complete(event):
            assert event["event"] == "finished"
            return dict(status="verified")
        with patch.object(protected.subprocess, "Popen", side_effect=[worker, monitor]):
            result = protected.run_protected(command, args, expected_ready=dict(dataset_sha256="expected"),
                                             completion_validator=complete)
        assert result["status"] == "verified" and worker.stdin.getvalue() == "GO\n"
        assert dict(timeout=60) in worker.waits
    print("PASS tiny-fit budget, completion, identity rejection and EOF-before-exit regression")


if __name__ == "__main__":
    main()
