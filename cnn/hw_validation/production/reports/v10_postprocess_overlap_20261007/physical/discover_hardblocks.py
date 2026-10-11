"""Discover this run's routed hard blocks and emit fail-closed TD reports."""

import argparse
import json
import re
from pathlib import Path


PRIMITIVES = (
    "PH1P_PHY_DSPSIOU_V2",
    "PH1P_PHY_DSPMULT_V2",
    "PH1P_PHY_ERAM_V2",
    "PH1P_PHY_DRAMHARDCON",
    "PH1P_PHY_MSLICE",
)


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_instances(text: str, primitive: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    found: list[dict[str, str]] = []
    index = 0
    while index < len(lines):
        if not lines[index].startswith(f"  {primitive}"):
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not re.match(r"^\s+(?:\\\S.*?|\S+)\s+\($", lines[index]):
            index += 1
        if index == len(lines):
            raise RuntimeError(f"instance missing for {primitive} at line {start + 1}")
        instance = compact(lines[index][:-1]).lstrip("\\")
        while index < len(lines) and "));" not in lines[index]:
            index += 1
        if index == len(lines):
            raise RuntimeError(f"unterminated instance {instance}")
        source = re.search(r"//\s*(\S.*?)\s*$", lines[index])
        found.append({"primitive": primitive, "instance": instance,
                      "source": source.group(1) if source else ""})
        index += 1
    return found


def tcl_objects(command: str, names: list[str]) -> str:
    return f"[{command} -hier -full_hier {{\n" + "\n".join(f"    {name}" for name in names) + "\n}]"


def build_export(groups: dict[str, list[dict[str, str]]]) -> str:
    dsp = groups["dsp_siou"]
    mac = groups["mac_dsp_siou"]
    eram = groups["eram"]
    dram = groups["dram"]
    return f"""# Generated from this run's routed netlist; do not hand-edit names.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set dsp_cells {tcl_objects('get_cells', [item['instance'] for item in dsp])}
set mac_dsp_cells {tcl_objects('get_cells', [item['instance'] for item in mac])}
set eram_cells {tcl_objects('get_cells', [item['instance'] for item in eram])}
set dram_cells {tcl_objects('get_cells', [item['instance'] for item in dram])}
set all_regs [get_regs -hier *]

foreach {{name objects minimum}} [list \
    dsp_cells $dsp_cells 24 \
    mac_dsp_cells $mac_dsp_cells 24 \
    eram_cells $eram_cells 1 \
    dram_cells $dram_cells 1 \
    all_regs $all_regs 1] {{
    if {{[llength $objects] < $minimum}} {{ error "$name minimum=$minimum actual=[llength $objects]" }}
}}

set dsp_pins [get_pins -of $dsp_cells]
set mac_dsp_pins [get_pins -of $mac_dsp_cells]
set eram_pins [get_pins -of $eram_cells]
set dram_pins [get_pins -of $dram_cells]
foreach {{name objects}} [list dsp_pins $dsp_pins mac_dsp_pins $mac_dsp_pins eram_pins $eram_pins dram_pins $dram_pins] {{
    if {{[llength $objects] == 0}} {{ error "$name is empty" }}
}}

report_timing_path -through $dsp_pins -ep_num 100000 -path_num 1 -file discovered_dsp_paths.timing
report_timing_path -through $mac_dsp_pins -ep_num 100000 -path_num 1 -file discovered_mac_dsp_paths.timing
report_timing_path -through $eram_pins -ep_num 100000 -path_num 1 -file discovered_eram_paths.timing
report_timing_path -through $dram_pins -ep_num 100000 -path_num 1 -file discovered_dram_paths.timing
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file discovered_all_reg_paths.timing

set object_count_file [open discovered_object_counts.txt w]
foreach {{name objects}} [list dsp_cells $dsp_cells mac_dsp_cells $mac_dsp_cells eram_cells $eram_cells dram_cells $dram_cells all_regs $all_regs dsp_pins $dsp_pins mac_dsp_pins $mac_dsp_pins eram_pins $eram_pins dram_pins $dram_pins] {{
    set line "OBJECT_COUNT $name=[llength $objects]"
    puts $line
    puts $object_count_file $line
}}
close $object_count_file

report_timing_summary -ep_num 100000 -path_num 1 -file discovered_coverage_100000_summary.rpt
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file discovered_coverage_100000_violations.timing
report_timing_exception -ep_num 100000 -path_num 1 -file discovered_timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file discovered_timing_ignored.rpt
check_timing -verbose -file discovered_check_timing_verbose.rpt
report_abnormal_timing_target -file discovered_abnormal_targets.rpt
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("netlist", type=Path)
    parser.add_argument("audit_json", type=Path)
    parser.add_argument("export_tcl", type=Path)
    args = parser.parse_args()
    text = args.netlist.read_text(encoding="utf-8", errors="replace")
    instances = {name: extract_instances(text, name) for name in PRIMITIVES}
    dsp_siou = instances["PH1P_PHY_DSPSIOU_V2"]
    mac_dsp = [item for item in dsp_siou
               if "road_mac_probe" in (item["instance"] + item["source"])]
    eram = instances["PH1P_PHY_ERAM_V2"]
    dram = instances["PH1P_PHY_DRAMHARDCON"]
    source_markers = {
        "runner": text.count("down2_overlap_tile_runner.v"),
        "postprocess": text.count("road_postprocess_stream.v"),
        "mac": text.count("road_mac_probe.v"),
        "round": text.count("road_round_shift.v"),
        "silu": text.count("silu_shared_unit.v"),
    }
    retained_names = {
        name: text.count(name)
        for name in ("reg_meta_fifo", "reg_result_queue", "reg_commit_ready",
                     "reg_feature", "reg_weight", "reg_bias", "reg_output")
    }
    failures = []
    if len(mac_dsp) != 24:
        failures.append(f"MAC DSP count {len(mac_dsp)} != 24")
    if len(eram) < 1:
        failures.append("SiLU/table ERAM primitive missing")
    if len(dram) < 1:
        failures.append("no routed DRAM controller: dynamic storage not proved")
    if not all(source_markers.values()):
        failures.append(f"source closure missing from routed netlist: {source_markers}")
    if retained_names["reg_commit_ready"] == 0:
        failures.append("runtime commit-ready control was optimized away")
    audit = {
        "schema": "v10-routed-hardblock-audit-v1",
        "status": "PASS" if not failures else "FAIL",
        "counts": {
            "dsp_siou": len(dsp_siou),
            "dsp_mult": len(instances["PH1P_PHY_DSPMULT_V2"]),
            "mac_dsp_siou": len(mac_dsp),
            "non_mac_dsp_siou": len(dsp_siou) - len(mac_dsp),
            "eram": len(eram),
            "dram_hardcon": len(dram),
            "mslice": len(instances["PH1P_PHY_MSLICE"]),
        },
        "source_markers": source_markers,
        "retained_name_occurrences": retained_names,
        "fixed_round_note": "Non-MAC DSP count may be zero because fixed pre/post coefficients may legally fold; this is not generic runtime-coefficient cost.",
        "failures": failures,
    }
    args.audit_json.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    groups = {"dsp_siou": dsp_siou, "mac_dsp_siou": mac_dsp,
              "eram": eram, "dram": dram}
    args.export_tcl.write_text(build_export(groups), encoding="utf-8")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
