"""Bound the existing spec-generation failure and preserve its stack trace."""
from datetime import datetime, timezone
import faulthandler
import json
from pathlib import Path
import site
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        output = Path(sys.argv[2])
        sys.path[:0] = [str(SKILL), *sys.argv[3:]]
        faulthandler.dump_traceback_later(5)
        from scripts.python.workflow.cli import main as cli_main
        probe = ROOT / "round_internal_probe"
        sys.argv = ["write-spec", "write-spec", "--settings", str(ROOT.parent / "settings.json"),
                    "--spec", str(probe / "road_round_internal_probe.contract.json"),
                    "--out-dir", str(output / "bundle"), "--no-state"]
        for path in sorted((probe / "rtl").glob("*.v")):
            sys.argv.extend(["--source", str(path)])
        return cli_main()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "reports" / ("spec_diagnosis_" + stamp)
    output.mkdir(parents=True, exist_ok=False)
    # Use the real base executable: a Windows venv launcher would leave its child alive on timeout.
    command = [sys._base_executable, "-B", "-X", "utf8", str(Path(__file__).resolve()),
               "--worker", str(output), *site.getsitepackages()]
    process = subprocess.Popen(command, cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        stdout, stderr = process.communicate(timeout=5)
    (output / "stdout.log").write_bytes(stdout)
    (output / "stderr.log").write_bytes(stderr)
    report = {"command": command, "cwd": str(PROJECT), "pid": process.pid,
              "timeout_seconds": 15, "timed_out": timed_out, "returncode": process.returncode,
              "old_valid_bundle_overwritten": False, "training_or_td_run": False,
              "status": "generation_timeout" if timed_out else
                        ("generated_isolated_bundle" if process.returncode == 0 else "generation_failed")}
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({**report, "report": str(output / "report.json")}))
    print(stderr.decode("utf-8", errors="replace")[-4000:])
    return 1 if timed_out else process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
