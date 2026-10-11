"""One actual mapped-top functional check; no RTL or timing-constraint modification."""
import json
import run

work = run.fresh("mapped_simulation")
vendor = json.loads((run.ROOT / "simulation_attempt2/receipt.json").read_text(encoding="utf-8"))["vendor_models"]
run.command([run.MSIM / "vlib.exe", "work"], work, "vlib")
run.command([run.MSIM / "vlog.exe", "-work", "work", *vendor,
             run.ROOT / "physical_attempt2/gate_netlist.v",
             run.ROOT / "tests/tb_mapped_board_selftest.v"], work, "vlog", timeout=300)
output = run.command([run.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_mapped_board_selftest",
    "-do", "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, "mapped", timeout=600)
assert "TB_PASS_MAPPED_BOARD_SELFTEST" in output, output[-3000:]
run.save(work / "receipt.json", {"pass_lines": [s for s in output.splitlines() if "TB_PASS_MAPPED" in s],
    "actual_td_gate_netlist_sha256": run.digest(run.ROOT / "physical_attempt2/gate_netlist.v"),
    "forced_clocks_or_operands_or_status": False, "timing_backannotated": False, "board_verified": False})
run.check()
