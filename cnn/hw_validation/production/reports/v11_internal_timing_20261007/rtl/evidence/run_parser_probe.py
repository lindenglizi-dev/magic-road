"""Run parser_probe inside the v11 guard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guard import run


raise SystemExit(
    run(
        [
            sys.executable,
            str(Path(__file__).with_name("parser_probe.py")),
            str(Path(__file__).resolve().parents[1] / "down2_overlap_tile_runner.v"),
        ],
        Path(__file__).resolve().parents[1],
        Path("rtl/evidence/runner_formatter_candidate.log"),
    )
)
