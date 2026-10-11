"""Run the two priority v11 candidate simulations through the freeze guard."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "verification" / "regression_candidate"
VSIM = Path(r"D:\modeltech64_2020.4\win64")
sys.path.insert(0, str(ROOT))
import guard


def checked(command: list[str], log_name: str, timeout: int = 1200) -> None:
    code = guard.run(command, WORK, WORK / log_name, timeout=timeout)
    if code:
        raise SystemExit(code)


def main() -> None:
    checked([str(VSIM / "vlib.exe"), "work"], "guard_vlib.log", 120)
    common = [
        "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_round_shift.v",
        "silu_shared_unit.v", "road_postprocess_stream.v",
    ]
    checked(
        [str(VSIM / "vlog.exe"), "-work", "work", "-l", "vlog_postprocess.log",
         *common, "tb_road_postprocess_stream.v"],
        "guard_vlog_postprocess.log",
    )
    checked(
        [str(VSIM / "vsim.exe"), "-c", "-l", "vsim_postprocess.log",
         "work.PH1P_PHY_GSR", "work.tb_road_postprocess_stream", "-do",
         "run 18 ms; quit -f"],
        "guard_vsim_postprocess.log",
    )
    checked(
        [str(VSIM / "vlog.exe"), "-work", "work", "-l", "vlog_runner.log",
         "ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_mac_probe.v",
         "road_round_shift.v", "silu_shared_unit.v", "road_postprocess_stream.v",
         "down2_overlap_tile_runner.v", "tb_down2_overlap_tile_runner.v"],
        "guard_vlog_runner.log",
    )
    checked(
        [str(VSIM / "vsim.exe"), "-c", "-l", "vsim_runner.log",
         "work.PH1P_PHY_GSR", "work.tb_down2_overlap_tile_runner", "-do",
         "run 20 ms; quit -f"],
        "guard_vsim_runner.log",
    )
    print("RUN_CANDIDATE_COMPLETE")


if __name__ == "__main__":
    main()
