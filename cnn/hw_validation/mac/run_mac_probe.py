"""Generate vectors, run Python checks, and execute the local Icarus MAC probe."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VECTOR_PATH = ROOT / "mac_vectors.txt"
SIM_PATH = ROOT / "mac_probe.vvp"


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

    _run([sys.executable, "-m", "unittest", "-v", "test_mac_reference.py"])
    _run([sys.executable, "mac_reference.py", "--vectors", str(VECTOR_PATH), "--random-cases", "1024", "--seed", "42"])
    _run([iverilog, "-g2005", "-Wall", "-s", "tb_road_mac_probe", "-o", str(SIM_PATH), "road_mac_probe.v", "tb_road_mac_probe.v"])
    transcript = _run([vvp, str(SIM_PATH), f"+VECTORS={VECTOR_PATH}"])
    if "VERILOG-GEN-RESULT PASS cases=1031 errors=0 reset=1" not in transcript:
        raise SystemExit("self-checking testbench did not publish the required PASS transcript")

    for name in ("mac_reference.py", "road_mac_probe.v", "tb_road_mac_probe.v", "mac_vectors.txt"):
        print(f"SHA256 {name} {_sha256(ROOT / name)}")
    print("MAC-PROBE-RUNNER PASS random=1024 seed=42 vectors=1031")


if __name__ == "__main__":
    main()
