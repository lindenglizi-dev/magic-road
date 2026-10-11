"""Audit this run's routed primitives and emit a fail-closed TD export script."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_instances(text: str, primitive: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    items: list[dict[str, object]] = []
    index = 0
    marker = f"  {primitive}"
    while index < len(lines):
        if not lines[index].startswith(marker):
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not re.match(r"^\s+(?:\\\S.*?|\S+)\s+\($", lines[index]):
            index += 1
        if index >= len(lines):
            raise RuntimeError(f"instance name not found for {primitive} at line {start + 1}")
        instance = compact(lines[index][:-1]).lstrip("\\")
        body_start = index + 1
        index = body_start
        while index < len(lines) and "));" not in lines[index]:
            index += 1
        if index >= len(lines):
            raise RuntimeError(f"unterminated {primitive} instance {instance}")
        body = "\n".join(lines[body_start : index + 1])
        pins = {
            match.group(1): compact(match.group(2))
            for match in re.finditer(r"\.(\w+)\((.*?)\)(?=,\s*\.\w+\(|\s*\);)", body, re.DOTALL)
        }
        source = re.search(r"//\s*(\S.*?)\s*$", lines[index])
        items.append(
            {
                "primitive": primitive,
                "instance": instance,
                "source_line": start + 1,
                "source": source.group(1) if source else "",
                "pins": pins,
            }
        )
        index += 1
    return items


def collect_vector_bits(text: str, stem: str) -> list[int]:
    pattern = re.compile(rf"{re.escape(stem)}(?:_[A-Za-z0-9]+)*\s*\[(\d+)(?::(\d+))?\]")
    bits: set[int] = set()
    for high_text, low_text in pattern.findall(text):
        high = int(high_text)
        if low_text:
            low = int(low_text)
            bits.update(range(min(high, low), max(high, low) + 1))
        else:
            bits.add(high)
    return sorted(bits)


def tcl_objects(command: str, names: list[str]) -> str:
    return f"[{command} -hier -full_hier {{\n" + "\n".join(f"    {name}" for name in names) + "\n}]"


def tcl_pins(instances: list[str], pins: list[str]) -> str:
    names = [f"{instance}.{pin}" for instance in instances for pin in pins]
    return tcl_objects("get_pins", names)


def build_export(
    siou: list[dict[str, object]],
    mult: list[dict[str, object]],
    mac_siou: list[dict[str, object]],
    eram: list[dict[str, object]],
    cache_dram: list[dict[str, object]],
    cache_mslice: list[dict[str, object]],
) -> str:
    siou_names = [str(item["instance"]) for item in siou]
    mult_names = [str(item["instance"]) for item in mult]
    mac_names = [str(item["instance"]) for item in mac_siou]
    eram_names = [str(item["instance"]) for item in eram]
    cache_dram_names = [str(item["instance"]) for item in cache_dram]
    cache_mslice_names = [str(item["instance"]) for item in cache_mslice]
    return f"""# Generated from this run's routed_netlist.v; do not hand-edit instance names.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set dsp_siou_cells {tcl_objects('get_cells', siou_names)}
set dsp_mult_cells {tcl_objects('get_cells', mult_names)}
set mac_dsp_siou_cells {tcl_objects('get_cells', mac_names)}
set dsp_reset_pins {tcl_pins(siou_names, ['rst[*]'])}
set dsp_operand_pins {tcl_pins(siou_names, ['xa[*]', 'y[*]'])}
set dsp_result_pins {tcl_pins(siou_names, ['p[*]'])}
set dsp_control_pins {tcl_pins(siou_names, ['ce[*]', 'inctrl[*]', 'muxctrl[*]', 'opctrl[*]'])}
set mac_dsp_operand_pins {tcl_pins(mac_names, ['xa[*]', 'y[*]'])}
set mac_dsp_result_pins {tcl_pins(mac_names, ['p[*]'])}
set dsp_mult_internal_pins [get_pins -of $dsp_mult_cells]

set eram_cells {tcl_objects('get_cells', eram_names)}
set eram_input_pins {tcl_pins(eram_names, ['addra[*]', 'dia[*]', 'dia_extra[*]', 'csa[*]', 'wea'])}
set eram_output_pins {tcl_pins(eram_names, ['doa[*]', 'doa_extra[*]'])}

set feature_cache_dram_cells {tcl_objects('get_cells', cache_dram_names)}
set feature_cache_mslice_cells {tcl_objects('get_cells', cache_mslice_names)}
set feature_cache_dram_pins [get_pins -of $feature_cache_dram_cells]
set feature_cache_mslice_pins [get_pins -of $feature_cache_mslice_cells]

set mac_regs [get_regs -hier {{*road_mac_probe_Inst_chain/*}}]
set mac_bias_regs [get_regs -hier {{*road_mac_probe_Inst_chain/reg_bias*}}]
set mac_valid_regs [get_regs -hier {{*road_mac_probe_Inst_chain/*valid*}}]
set mac_dot_regs [get_regs -hier {{*road_mac_probe_Inst_chain/reg_dot*}}]
set mac_accumulator_regs [get_regs -hier {{*road_mac_probe_Inst_chain/reg_accumulator*}}]

foreach {{name objects expected}} [list \
    dsp_siou_cells $dsp_siou_cells 26 \
    dsp_mult_cells $dsp_mult_cells 26 \
    mac_dsp_siou_cells $mac_dsp_siou_cells 24 \
    eram_cells $eram_cells 1 \
    feature_cache_dram_cells $feature_cache_dram_cells 1 \
    feature_cache_mslice_cells $feature_cache_mslice_cells 8] {{
    if {{[llength $objects] != $expected}} {{ error "$name expected=$expected actual=[llength $objects]" }}
}}
set object_count_lines {{}}
foreach {{name objects}} [list \
    dsp_reset_pins $dsp_reset_pins \
    dsp_operand_pins $dsp_operand_pins \
    dsp_result_pins $dsp_result_pins \
    dsp_control_pins $dsp_control_pins \
    mac_dsp_operand_pins $mac_dsp_operand_pins \
    mac_dsp_result_pins $mac_dsp_result_pins \
    dsp_mult_internal_pins $dsp_mult_internal_pins \
    eram_input_pins $eram_input_pins \
    eram_output_pins $eram_output_pins \
    feature_cache_dram_pins $feature_cache_dram_pins \
    feature_cache_mslice_pins $feature_cache_mslice_pins \
    mac_regs $mac_regs \
    mac_bias_regs $mac_bias_regs \
    mac_valid_regs $mac_valid_regs \
    mac_dot_regs $mac_dot_regs \
    mac_accumulator_regs $mac_accumulator_regs] {{
    if {{[llength $objects] == 0}} {{ error "$name is empty" }}
}}

report_timing_path -through $dsp_reset_pins -ep_num 20000 -path_num 1 -file dsp_reset_paths.timing
report_timing_path -through $dsp_operand_pins -ep_num 20000 -path_num 1 -file dsp_operand_paths.timing
report_timing_path -through $dsp_mult_internal_pins -ep_num 20000 -path_num 1 -file dsp_mult_internal_paths.timing
report_timing_path -through $dsp_result_pins -ep_num 20000 -path_num 1 -file dsp_result_paths.timing
report_timing_path -through $dsp_control_pins -ep_num 20000 -path_num 1 -file dsp_control_paths.timing
report_timing_path -through $mac_dsp_operand_pins -ep_num 20000 -path_num 1 -file mac_dsp_operand_paths.timing
report_timing_path -through $mac_dsp_result_pins -ep_num 20000 -path_num 1 -file mac_dsp_result_paths.timing
report_timing_path -from $mac_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_internal_reg_to_reg.timing
report_timing_path -from $mac_bias_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_bias_paths.timing
report_timing_path -from $mac_valid_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_valid_control_paths.timing
report_timing_path -from $mac_accumulator_regs -to $mac_accumulator_regs -ep_num 1000 -path_num 10 -file mac_a5_feedback_paths.timing
report_timing_path -from $mac_dot_regs -to $mac_accumulator_regs -ep_num 1000 -path_num 10 -file mac_dot_to_accumulator_paths.timing
report_timing_path -through $eram_input_pins -ep_num 20000 -path_num 1 -file eram_input_paths.timing
report_timing_path -through $eram_output_pins -ep_num 20000 -path_num 1 -file eram_output_paths.timing
report_timing_path -through $feature_cache_dram_pins -ep_num 20000 -path_num 1 -file feature_cache_dram_paths.timing
report_timing_path -through $feature_cache_mslice_pins -ep_num 20000 -path_num 1 -file feature_cache_data_paths.timing

foreach {{name objects}} [list \
    dsp_siou_cells $dsp_siou_cells \
    dsp_mult_cells $dsp_mult_cells \
    mac_dsp_siou_cells $mac_dsp_siou_cells \
    dsp_reset_pins $dsp_reset_pins \
    dsp_operand_pins $dsp_operand_pins \
    dsp_result_pins $dsp_result_pins \
    dsp_control_pins $dsp_control_pins \
    mac_dsp_operand_pins $mac_dsp_operand_pins \
    mac_dsp_result_pins $mac_dsp_result_pins \
    dsp_mult_internal_pins $dsp_mult_internal_pins \
    eram_cells $eram_cells \
    eram_input_pins $eram_input_pins \
    eram_output_pins $eram_output_pins \
    feature_cache_dram_cells $feature_cache_dram_cells \
    feature_cache_mslice_cells $feature_cache_mslice_cells \
    feature_cache_dram_pins $feature_cache_dram_pins \
    feature_cache_mslice_pins $feature_cache_mslice_pins \
    mac_regs $mac_regs \
    mac_bias_regs $mac_bias_regs \
    mac_valid_regs $mac_valid_regs \
    mac_dot_regs $mac_dot_regs \
    mac_accumulator_regs $mac_accumulator_regs] {{
    set line "OBJECT_COUNT $name=[llength $objects]"
    puts $line
    lappend object_count_lines $line
}}
set object_count_file [open discovered_object_counts.txt w]
foreach line $object_count_lines {{ puts $object_count_file $line }}
close $object_count_file

report_timing_summary -ep_num 20000 -path_num 1 -file discovered_full_timing_summary.rpt
report_timing_summary -viol_only -ep_num 20000 -path_num 1 -file discovered_full_violations.timing
report_timing_exception -ep_num 20000 -path_num 1 -file discovered_timing_exceptions.rpt
report_timing_ignored -ep_num 20000 -path_num 1 -file discovered_timing_ignored.rpt
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

    siou = extract_instances(text, "PH1P_PHY_DSPSIOU_V2")
    mult = extract_instances(text, "PH1P_PHY_DSPMULT_V2")
    eram = extract_instances(text, "PH1P_PHY_ERAM_V2")
    dram = extract_instances(text, "PH1P_PHY_DRAMHARDCON")
    mslice = extract_instances(text, "PH1P_PHY_MSLICE")
    mac_siou = [item for item in siou if "/road_mac_probe_Inst_chain/" in str(item["instance"])]
    cache_dram = [item for item in dram if item["source"].endswith("road_onchip_chain.v(292)")]
    cache_mslice = [
        item
        for item in mslice
        if item["source"].endswith("road_onchip_chain.v(292)")
        and "cache_result_data_o_b4" in " ".join(str(value) for value in item["pins"].values())
    ]

    activation_bits = collect_vector_bits("\n".join(str(item["pins"].get("xa", "")) for item in mac_siou), "reg_activation_front")
    weight_bits = collect_vector_bits("\n".join(str(item["pins"].get("y", "")) for item in mac_siou), "reg_weight_front")
    bias_bits = collect_vector_bits(text, "reg_bias_front")
    controls = {
        name: text.count(f"/road_mac_probe_Inst_chain/{name}")
        for name in (
            "flag_front_valid",
            "flag_quad_valid",
            "flag_dot_valid",
            "flag_final_valid_stage0",
            "flag_final_valid_stage1",
            "flag_final_valid_stage2",
            "flag_final_valid_stage3",
            "o_result_valid",
            "flag_candidate_fault",
            "flag_first_quad",
            "flag_first_dot",
            "flag_last_dot",
            "input_ready_o",
        )
    }
    absorbed_controls = {
        name: text.count(f"/road_mac_probe_Inst_chain/{name}")
        for name in ("flag_product_valid", "flag_pair_valid", "flag_candidate_valid")
    }
    accumulator_coverage = {
        name: collect_vector_bits(text, name)
        for name in ("reg_accumulator_alpha", "reg_accumulator_beta", "reg_accumulator_gamma")
    }
    absorbed_candidate_registers = {
        name: text.count(f"/road_mac_probe_Inst_chain/{name}")
        for name in ("reg_candidate_alpha", "reg_candidate_beta", "reg_candidate_gamma")
    }

    failures = []
    checks = (
        (len(siou) == 26, f"DSPSIOU count {len(siou)} != 26"),
        (len(mult) == 26, f"DSPMULT count {len(mult)} != 26"),
        (len(mac_siou) == 24, f"MAC DSPSIOU count {len(mac_siou)} != 24"),
        (len(eram) == 1, f"ERAM count {len(eram)} != 1"),
        (len(cache_dram) == 1, f"feature-cache DRAM count {len(cache_dram)} != 1"),
        (len(cache_mslice) == 8, f"feature-cache data MSLICE count {len(cache_mslice)} != 8"),
        (activation_bits == list(range(64)), "MAC activation coverage is not 64/64 bits"),
        (weight_bits == list(range(192)), "MAC weight coverage is not 192/192 bits"),
        (bias_bits == list(range(96)), "MAC bias coverage is not 96/96 bits"),
        (all(controls.values()), "one or more MAC valid/control signals disappeared"),
        (
            all(bits == list(range(33)) for bits in accumulator_coverage.values()),
            "one or more signed33 accumulators are not retained at 33/33 bits",
        ),
    )
    failures.extend(message for passed, message in checks if not passed)
    if failures:
        raise SystemExit("\n".join(failures))

    audit = {
        "schema": "v9-routed-hardblock-audit-v1",
        "status": "PASS",
        "counts": {
            "dsp_siou": len(siou),
            "dsp_mult": len(mult),
            "mac_dsp_siou": len(mac_siou),
            "eram": len(eram),
            "dram_hardcon": len(dram),
            "feature_cache_dram": len(cache_dram),
            "feature_cache_data_mslice": len(cache_mslice),
        },
        "mac_data_coverage": {
            "activation_bits": activation_bits,
            "weight_bits": weight_bits,
            "bias_bits": bias_bits,
            "valid_control_occurrences": controls,
            "source_valid_names_absorbed_by_synthesis": absorbed_controls,
            "source_candidate_register_names_absorbed_by_synthesis": absorbed_candidate_registers,
            "signed33_accumulator_bits": accumulator_coverage,
        },
        "dsp_siou_instances": siou,
        "dsp_mult_instances": mult,
        "eram_instances": eram,
        "feature_cache_dram_instances": cache_dram,
        "feature_cache_data_mslices": cache_mslice,
    }
    args.audit_json.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    args.export_tcl.write_text(build_export(siou, mult, mac_siou, eram, cache_dram, cache_mslice), encoding="utf-8")


if __name__ == "__main__":
    main()
