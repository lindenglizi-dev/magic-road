"""Compile the v11 RTL candidate inside the v11 guard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guard import run


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.parents[4]
RTL = ROOT / "rtl"
V9 = ROOT.parent / "v9_mac_stream_20261007"
V7 = ROOT.parent / "v7_minimal_chain_20261006"
IVERILOG = PROJECT.parents[1] / ".tools" / "iverilog" / "bin" / "iverilog.exe"

raise SystemExit(
    run(
        [
            str(IVERILOG),
            "-g2005",
            "-i",
            "-s",
            "down2_overlap_tile_runner",
            "-o",
            str(RTL / "evidence" / "down2_overlap_tile_runner.vvp"),
            str(RTL / "down2_overlap_tile_runner.v"),
            str(RTL / "road_postprocess_stream.v"),
            str(V9 / "core" / "road_mac_probe.v"),
            str(V7 / "inputs" / "road_round_shift.v"),
            str(V7 / "inputs" / "silu_shared_unit.v"),
        ],
        RTL,
        Path("rtl/evidence/compile_attempt2.log"),
    )
)
