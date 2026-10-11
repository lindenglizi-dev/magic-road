"""Recompile and rerun only the corrected standalone v11 testbench."""
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "verification" / "regression_candidate"
VSIM = Path(r"D:\modeltech64_2020.4\win64")
sys.path.insert(0, str(ROOT))
import guard


def checked(command: list[str], log_name: str) -> None:
    code = guard.run(command, WORK, WORK / log_name, timeout=1200)
    if code:
        raise SystemExit(code)


checked(
    [str(VSIM / "vlog.exe"), "-work", "work", "-l", "vlog_postprocess_attempt3.log",
     "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_round_shift.v",
     "silu_shared_unit.v", "road_postprocess_stream.v", "tb_road_postprocess_stream.v"],
    "guard_vlog_postprocess_attempt3.log",
)
checked(
    [str(VSIM / "vsim.exe"), "-c", "-l", "vsim_postprocess_attempt3.log",
     "work.PH1P_PHY_GSR", "work.tb_road_postprocess_stream", "-do",
     "run 18 ms; quit -f"],
    "guard_vsim_postprocess_attempt3.log",
)
print("RERUN_POSTPROCESS_COMPLETE")
