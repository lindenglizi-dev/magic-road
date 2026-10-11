"""Render both v11 WaveJSON diagrams inside the v11 guard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guard import run


ROOT = Path(__file__).resolve().parents[2]
RTL = ROOT / "rtl"
WAVES = RTL / "waveforms"
WAVEDROM = Path(r"C:\Users\lenovo\AppData\Roaming\npm\wavedrom.CMD")

for stem in ("road_postprocess_stream_elastic_cut", "down2_overlap_tile_runner_timing_cut"):
    result = run(
        [str(WAVEDROM), "-i", str(WAVES / f"{stem}.json5"), "-s", str(WAVES / f"{stem}.svg")],
        RTL,
        Path(f"rtl/evidence/render_{stem}.log"),
    )
    if result:
        raise SystemExit(result)
