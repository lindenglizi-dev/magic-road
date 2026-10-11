"""Run the runner whitespace-equivalence proof inside the v11 guard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from guard import run


raise SystemExit(
    run(
        [sys.executable, str(Path(__file__).with_name("check_runner_whitespace_equivalence.py"))],
        Path(__file__).resolve().parents[1],
        Path("rtl/evidence/runner_whitespace_equivalence.log"),
    )
)
