"""Run the candidate runner with additional read-only job-turnaround tracing."""
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
    [str(VSIM / "vlog.exe"), "-work", "work", "-l", "vlog_runner_turnaround.log",
     "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_mac_probe.v",
     "road_round_shift.v", "silu_shared_unit.v", "road_postprocess_stream.v",
     "down2_overlap_tile_runner.v", "tb_down2_overlap_tile_runner.v"],
    "guard_vlog_runner_turnaround.log",
)
checked(
    [str(VSIM / "vsim.exe"), "-c", "-l", "vsim_runner_turnaround.log",
     "work.PH1P_PHY_GSR", "work.tb_down2_overlap_tile_runner", "-do",
     "run 20 ms; quit -f"],
    "guard_vsim_runner_turnaround.log",
)
print("RUNNER_TURNAROUND_COMPLETE")
