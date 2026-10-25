"""Run the existing Head Top-K suite into an isolated evidence directory."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys


ATTEMPT = Path(__file__).resolve().parent
VERIFICATION = ATTEMPT.parents[1]
RUNNER = VERIFICATION / "run_rtl.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    spec = importlib.util.spec_from_file_location("head_topk_existing_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load existing runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.BUILD = ATTEMPT / "build"
    runner.REPORTS = ATTEMPT
    sys.argv = [str(RUNNER), "--suite", "all", "--timeout", "600"]
    returncode = runner.main()

    summary_path = ATTEMPT / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    compiler = Path(summary["compiler"])
    runtime_text = shutil.which("vvp")
    if not runtime_text:
        raise SystemExit("vvp disappeared after suite run")
    runtime = Path(runtime_text)
    summary["isolated_attempt"] = {
        "execution_environment": "same local host, sandbox escalation",
        "original_reports_preserved": True,
        "requested_suite": "all",
        "requested_timeout_seconds_per_step": 600,
        "driver": str(Path(__file__).resolve()),
        "driver_sha256": sha256(Path(__file__).resolve()),
        "existing_runner_sha256": sha256(RUNNER),
        "prepare_vectors_sha256": sha256(VERIFICATION / "prepare_vectors.py"),
        "compiler_sha256": sha256(compiler),
        "runtime_sha256": sha256(runtime),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"ESCALATED_ATTEMPT_RETURN={returncode} summary={summary_path}")
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
