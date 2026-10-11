"""Check v11 physical-flow preparation without requiring candidate RTL yet."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V11 = ROOT.parent
V10_PHYSICAL = V11.parent / "v10_postprocess_overlap_20261007" / "physical"

for name in ("extract_v10_internal_violations.py", "discover_hardblocks.py", "analyze_postroute.py"):
    ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)

for name in ("road_postprocess_low_io_top.v", "tb_road_postprocess_low_io_top.v"):
    current = (ROOT / name).read_text(encoding="utf-8")
    frozen = (V10_PHYSICAL / name).read_text(encoding="utf-8")
    if current.rstrip("\n") != frozen.rstrip("\n"):
        raise SystemExit(f"FAIL copied shell text differs from frozen v10: {name}")

build = (ROOT / "build.tcl").read_text(encoding="utf-8")
for forbidden in ("bitgen", "generate_bitstream", "program_flash", "download_bit"):
    if forbidden in build.lower():
        raise SystemExit(f"FAIL forbidden build command: {forbidden}")
if "-ep_num 100000" not in build:
    raise SystemExit("FAIL full endpoint report cap missing")

sdc = (ROOT / "shell.sdc").read_text(encoding="utf-8")
for forbidden in ("set_false_path", "set_multicycle_path", "set_max_delay", "set_min_delay"):
    if forbidden in sdc:
        raise SystemExit(f"FAIL timing exception present: {forbidden}")
if sdc.count("0.000") < 4:
    raise SystemExit("FAIL diagnostic zero-delay boundary missing")

project = (ROOT / "road_postprocess_low_io_top.al").read_text(encoding="utf-8")
if "v11_internal_timing_20261007/physical" not in project:
    raise SystemExit("FAIL project path is not v11 physical")
for source in ("road_postprocess_low_io_top.v", "../rtl/down2_overlap_tile_runner.v",
               "../rtl/road_postprocess_stream.v", "road_mac_probe.v",
               "road_round_shift.v", "silu_shared_unit.v"):
    if source not in project:
        raise SystemExit(f"FAIL source closure missing {source}")

candidate = [V11 / "rtl" / "down2_overlap_tile_runner.v",
             V11 / "rtl" / "road_postprocess_stream.v"]
state = "READY_FOR_FUNCTIONAL_FREEZE" if all(path.is_file() for path in candidate) else "WAITING_CANDIDATE_RTL"
print(f"PASS physical build preparation state={state}")
