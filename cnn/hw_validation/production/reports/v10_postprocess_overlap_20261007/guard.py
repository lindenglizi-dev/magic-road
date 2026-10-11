"""Bound runs to this candidate and preserve every prior validation byte."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
MANIFEST = ROOT / "frozen_previous.json"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bounded(path):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Working/output path outside candidate: {path}")
    return path


def freeze():
    entries = {}
    # All prior evidence, RTL, graph and validation scripts are read-only inputs.
    validation = ROOT.parents[2]
    for path in sorted(validation.rglob("*")):
        if path.is_file() and not path.is_relative_to(ROOT):
            entries[str(path)] = {"bytes": path.stat().st_size, "sha256": digest(path)}
    # Include production template sources/constraints, without training artifacts.
    for pattern in ("*.v", "*.vh", "*.sdc", "*.adc", "*.al"):
        for path in PROJECT.rglob(pattern):
            if path.is_file() and not path.is_relative_to(ROOT) and str(path) not in entries:
                entries[str(path)] = {"bytes": path.stat().st_size, "sha256": digest(path)}
    with MANIFEST.open("x", encoding="utf-8") as stream:
        json.dump({"root": str(ROOT), "files": entries}, stream, indent=2)
        stream.write("\n")
    return check()


def check():
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    failed = [name for name, entry in entries.items()
              if not Path(name).is_file() or Path(name).stat().st_size != entry["bytes"]
              or digest(Path(name)) != entry["sha256"]]
    if failed:
        raise RuntimeError(f"Frozen files changed: {failed}")
    previous = ROOT.parent / "v9_mac_stream_20261007"
    expected = {name for name in entries if Path(name).is_relative_to(previous)}
    current = {str(path) for path in previous.rglob("*") if path.is_file()}
    if current != expected:
        raise RuntimeError(f"Frozen v9 inventory changed: {current ^ expected}")
    return {"status": "FROZEN_FILES_UNCHANGED", "files": len(entries),
            "manifest_sha256": digest(MANIFEST)}


def run(command, cwd, log, timeout=1200, env=None):
    cwd, log = bounded(cwd), bounded(log)
    before = check()
    child_env = dict(os.environ if env is None else env)
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    child_env["PYTHONPYCACHEPREFIX"] = str(ROOT / ".python_cache")
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log.open("x", encoding="utf-8") as stream:
            result = subprocess.run(command, cwd=cwd, env=child_env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
        return result.returncode
    finally:
        after = check()
        receipt = log.with_suffix(log.suffix + ".guard.json")
        receipt.write_text(json.dumps({"command": command, "cwd": str(cwd),
                                      "before": before, "after": after}, indent=2) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    print(json.dumps(freeze() if args.freeze else check()))
