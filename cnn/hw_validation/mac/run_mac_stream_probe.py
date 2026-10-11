"""Run Python layout checks and the local Icarus dynamic MAC wrapper test."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VECTOR_PATH = ROOT / "mac_vectors.txt"
EXPECTED_VECTOR_SHA256 = "7d170353a69a7303d982443a53315515b3c3aab7a167fa2d912b7de2d5741792"


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout, end="")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.stdout


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    iverilog = shutil.which("iverilog")
    vvp = shutil.which("vvp")
    if not iverilog or not vvp:
        raise SystemExit("configured local iverilog and vvp are required")
    if _sha256(VECTOR_PATH) != EXPECTED_VECTOR_SHA256:
        raise SystemExit("the frozen 1031-vector core corpus changed")

    _run([sys.executable, "-m", "unittest", "-v", "test_mac_stream_reference.py"])
    with tempfile.TemporaryDirectory(prefix="mac_stream_probe_") as directory:
        simulation = str(Path(directory) / "mac_stream_probe.vvp")
        _run(
            [
                iverilog,
                "-g2001",
                "-Wall",
                "-s",
                "tb_road_mac_stream_probe",
                "-o",
                simulation,
                "road_mac_probe.v",
                "road_mac_stream_probe.v",
                "tb_road_mac_stream_probe.v",
            ]
        )
        transcript = _run([vvp, simulation, f"+VECTORS={VECTOR_PATH}"])
    required = "VERILOG-GEN-RESULT PASS cases=1031 errors=0 reset=1 dynamic_words=12 io=140"
    if required not in transcript:
        raise SystemExit("self-checking wrapper testbench did not publish the required PASS transcript")

    for name in (
        "road_mac_probe.v",
        "road_mac_stream_probe.v",
        "tb_road_mac_stream_probe.v",
        "mac_stream_reference.py",
        "mac_vectors.txt",
    ):
        print(f"SHA256 {name} {_sha256(ROOT / name)}")
    print("MAC-STREAM-PROBE-RUNNER PASS vectors=1031 dynamic_words=12 io=140")


if __name__ == "__main__":
    main()
