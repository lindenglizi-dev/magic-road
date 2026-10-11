"""Run the frozen legacy regression matrix in fresh v11-local directories."""
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
VERIFY = ROOT / "verification"
MODELTECH = Path(r"D:\modeltech64_2020.4\win64")
IVERILOG = Path(r"E:\project\qiansai\.tools\iverilog\bin")
sys.path.insert(0, str(ROOT))
import guard


def checked(suite: str, command: list[str], log_name: str, timeout: int = 1200) -> None:
    work = VERIFY / suite
    code = guard.run(command, work, work / log_name, timeout=timeout)
    if code:
        raise SystemExit(f"{suite}: {command[0]} returned {code}")


def modelsim(suite: str, sources: list[str], top: list[str], duration: str,
             plusargs: list[str] | None = None) -> None:
    checked(suite, [str(MODELTECH / "vlib.exe"), "work"], "guard_vlib.log", 120)
    checked(suite, [str(MODELTECH / "vlog.exe"), "-work", "work", "-l", "vlog.log",
                    *sources], "guard_vlog.log")
    checked(suite, [str(MODELTECH / "vsim.exe"), "-c", "-l", "vsim.log", *top,
                    *(plusargs or []), "-do", f"run {duration}; quit -f"], "guard_vsim.log")


def main() -> None:
    modelsim(
        "regression_v9_mac",
        ["road_mac_probe.v", "tb_road_mac_stream.v"],
        ["work.tb_road_mac_stream"], "5 ms",
        ["+VECTORS=stream_vectors.txt", "+TRACE=stream_trace_fresh.csv"],
    )
    layer_sources = ["ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_mac_probe.v",
                     "road_round_shift.v", "silu_shared_unit.v", "down2_tile_runner.v",
                     "tb_down2_tile_runner.v"]
    for suite in ("regression_v9_serial_layers", "regression_v8_layers"):
        modelsim(suite, layer_sources, ["work.PH1P_PHY_GSR", "work.tb_down2_tile_runner"],
                 "20 ms")
    shell_sources = ["ph1p_logic_eram.v", "ph1p_phy_gsr.v", "road_mac_probe.v",
                     "road_round_shift.v", "silu_shared_unit.v", "road_onchip_chain.v",
                     "road_low_io_physical_shell.v", "road_low_io_reset_shell.v",
                     "tb_road_low_io_reset_shell_regression_v9.v",
                     "tb_road_low_io_reset_shell_v9.v"]
    suite = "regression_v9_shell"
    checked(suite, [str(MODELTECH / "vlib.exe"), "work"], "guard_vlib.log", 120)
    checked(suite, [str(MODELTECH / "vlog.exe"), "-work", "work", "-l", "vlog.log",
                    *shell_sources], "guard_vlog.log")
    checked(suite, [str(MODELTECH / "vsim.exe"), "-c", "-l", "vsim_shell14.log",
                    "work.PH1P_PHY_GSR", "work.tb_road_low_io_reset_shell_regression",
                    "-do", "run 2 ms; quit -f"], "guard_vsim_shell14.log")
    checked(suite, [str(MODELTECH / "vsim.exe"), "-c", "-l", "vsim_reset6.log",
                    "work.PH1P_PHY_GSR", "work.tb_road_low_io_reset_shell",
                    "-do", "run 1 ms; quit -f"], "guard_vsim_reset6.log")
    suite = "regression_round_7042"
    checked(suite, [str(IVERILOG / "iverilog.exe"), "-g2001", "-s",
                    "tb_road_round_shift_stall", "-o", "round_stall.vvp",
                    "road_round_shift.v", "tb_road_round_shift_stall.v"],
            "guard_compile.log")
    checked(suite, [str(IVERILOG / "vvp.exe"), "round_stall.vvp", "+COUNT=7042"],
            "guard_simulate.log")
    modelsim(
        "regression_silu_65536",
        ["ph1p_logic_eram.v", "ph1p_phy_gsr.v", "silu_shared_unit.v",
         "tb_silu_shared_unit.v"],
        ["work.PH1P_PHY_GSR", "work.tb_silu_shared_unit"], "2 ms",
    )
    print("LEGACY_REGRESSIONS_COMPLETE")


if __name__ == "__main__":
    main()
