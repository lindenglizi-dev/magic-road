"""Create a machine-readable structural audit of the routed TD netlist.

This script does not modify the design.  It inventories every DSP SIOU,
distributed-RAM hard controller, ERAM, reset-release register copy, and the
dummy timing endpoints reported by TD.
"""

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
        instance = compact(lines[index][:-1])
        body_start = index + 1
        index = body_start
        while index < len(lines) and "));" not in lines[index]:
            index += 1
        if index >= len(lines):
            raise RuntimeError(f"unterminated {primitive} instance {instance}")
        body = "\n".join(lines[body_start : index + 1])
        pins = {
            match.group(1): compact(match.group(2))
            for match in re.finditer(
                r"\.(\w+)\((.*?)\)(?=,\s*\.\w+\(|\s*\);)", body, re.DOTALL
            )
        }
        params = compact("\n".join(lines[start + 1 : body_start - 1]))
        items.append(
            {
                "instance": instance.rstrip(),
                "source_line": start + 1,
                "parameters": params,
                "pins": pins,
            }
        )
        index += 1
    return items


def classify(expr: str) -> str:
    has_open = bool(re.search(r"\bopen_n\d+\b", expr))
    has_const = bool(re.search(r"\b\d+'[bBoOdDhH][0-9a-fA-F_xXzZ]+\b", expr))
    scrubbed = re.sub(r"\b\d+'[bBoOdDhH][0-9a-fA-F_xXzZ]+\b", "", expr)
    scrubbed = re.sub(r"\bopen_n\d+\b", "", scrubbed)
    scrubbed = re.sub(r"[{}(),\[\]:\d\s]", "", scrubbed)
    has_signal = bool(scrubbed)
    kinds = []
    if has_signal:
        kinds.append("dynamic")
    if has_const:
        kinds.append("constant")
    if has_open:
        kinds.append("open")
    return "mixed_" + "_".join(kinds) if len(kinds) > 1 else (kinds[0] if kinds else "empty")


def pin_record(expr: str) -> dict[str, str]:
    return {"expression": expr, "classification": classify(expr)}


def collect_vector_bits(text: str, stem: str) -> list[int]:
    pattern = re.compile(rf"{re.escape(stem)}(?:_[ab])?\s*\[(\d+)(?::(\d+))?\]")
    bits: set[int] = set()
    for high_text, low_text in pattern.findall(text):
        high = int(high_text)
        if low_text:
            low = int(low_text)
            bits.update(range(min(high, low), max(high, low) + 1))
        else:
            bits.add(high)
    return sorted(bits)


def dummy_nodes(check_text: str) -> list[dict[str, str]]:
    model = ""
    found: list[dict[str, str]] = []
    in_dummy = False
    for line in check_text.splitlines():
        if line.startswith("3. checking dummy nodes"):
            in_dummy = True
            continue
        if in_dummy and line.startswith("4. checking invalid constraints"):
            break
        match = re.match(r"DummyNode in Model: (\S+)", line)
        if match:
            model = match.group(1)
            continue
        endpoint = line.strip()
        if model and endpoint.startswith("road_low_io_physical_shell_Inst_reset/"):
            pin = endpoint.rsplit(".", 1)[-1]
            if model == "PH1P_PHY_DSPSIOU_V2" and pin in {"mul9_mode", "mul9_signed"}:
                category = "dsp_internal_mode_dummy"
            elif model == "PH1P_PHY_LSLICE" and pin == "ofa":
                category = "unused_lslice_output_dummy"
            else:
                category = "unclassified_dummy"
            found.append({"model": model, "endpoint": endpoint, "category": category})
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("netlist", type=Path)
    parser.add_argument("check_timing", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = args.netlist.read_text(encoding="utf-8", errors="replace")
    check_text = args.check_timing.read_text(encoding="utf-8", errors="replace")

    siou_raw = extract_instances(text, "PH1P_PHY_DSPSIOU_V2")
    mult_raw = extract_instances(text, "PH1P_PHY_DSPMULT_V2")
    dram_raw = extract_instances(text, "PH1P_PHY_DRAMHARDCON")
    eram_raw = extract_instances(text, "PH1P_PHY_ERAM_V2")
    mslice_raw = extract_instances(text, "PH1P_PHY_MSLICE")
    lslice_raw = extract_instances(text, "PH1P_PHY_LSLICE")

    mult_mode_nets = {
        pin: {item["pins"].get(pin, "") for item in mult_raw}
        for pin in ("mul9_mode", "mul9_signed")
    }
    dsp_items = []
    for item in siou_raw:
        pins = item["pins"]
        selected = {
            pin: pin_record(pins.get(pin, ""))
            for pin in ("ce", "rst", "xa", "y", "mul9_mode", "mul9_signed", "p")
        }
        selected["mul9_mode"]["paired_dspmult"] = str(
            pins.get("mul9_mode", "") in mult_mode_nets["mul9_mode"]
        ).lower()
        selected["mul9_signed"]["paired_dspmult"] = str(
            pins.get("mul9_signed", "") in mult_mode_nets["mul9_signed"]
        ).lower()
        dsp_items.append(
            {
                "instance": item["instance"],
                "source_line": item["source_line"],
                "sr_modes": re.findall(r"\.SR[0-3]MODE\(\"(.*?)\"\)", item["parameters"]),
                "pins": selected,
            }
        )

    dram_items = []
    for item in dram_raw:
        pins = item["pins"]
        dram_items.append(
            {
                "instance": item["instance"],
                "source_line": item["source_line"],
                "pins": {
                    pin: pin_record(pins.get(pin, ""))
                    for pin in ("byteaddr", "waddr", "wclk", "we", "wrst")
                },
            }
        )

    eram_items = []
    for item in eram_raw:
        pins = item["pins"]
        eram_items.append(
            {
                "instance": item["instance"],
                "source_line": item["source_line"],
                "pins": {
                    pin: pin_record(pins.get(pin, ""))
                    for pin in ("addra", "clka", "csa", "dia", "dia_extra", "wea", "doa", "doa_extra")
                },
            }
        )

    reset_copies = []
    for item in lslice_raw:
        if not str(item["instance"]).startswith("reg_release_done_reg_syn_"):
            continue
        pins = item["pins"]
        outputs = {pin: value for pin, value in pins.items() if pin in {"oqa", "oqb"}}
        if any("reg_release_meta" in value for value in outputs.values()):
            stage = "stage1_meta_single"
        elif any("reg_release_meta" in pins.get(pin, "") for pin in ("ima", "imb")):
            stage = "stage2_done_auto_replica"
        else:
            stage = "unclassified"
        reset_copies.append(
            {
                "instance": item["instance"],
                "source_line": item["source_line"],
                "stage": stage,
                "asr": pin_record(pins.get("asr", "")),
                "data": {pin: pin_record(pins[pin]) for pin in ("ima", "imb") if pin in pins},
                "outputs": {pin: pin_record(value) for pin, value in outputs.items()},
            }
        )

    ram_mslices = [item for item in mslice_raw if '.RAMMODE("DPRAM")' in item["parameters"]]
    ram_data_text = "\n".join(
        value
        for item in ram_mslices
        for pin, value in item["pins"].items()
        if pin in {"ima", "imb"}
    )
    dummy = dummy_nodes(check_text)
    mac_dsp = [
        item
        for item in dsp_items
        if "/road_mac_probe_Inst_chain/" in str(item["instance"])
    ]

    result = {
        "schema": "td-routed-netlist-audit-v1",
        "status": "WARNING_UNCLOSED_STRUCTURAL_DATA_PATHS_PRESENT",
        "interpretation": (
            "SYN-5025 is generic and not pin-specific. Dummy timing endpoints are inventoried, "
            "while dynamic functional operands, RAM controls, and RAM data are audited separately."
        ),
        "counts": {
            "dsp_siou": len(dsp_items),
            "dsp_mult": len(mult_raw),
            "dram_hardcon": len(dram_items),
            "eram": len(eram_items),
            "ram_mslices": len(ram_mslices),
            "reset_release_physical_regs": len(reset_copies),
            "dummy_endpoints": len(dummy),
            "dummy_dsp_mode_endpoints": sum(x["category"] == "dsp_internal_mode_dummy" for x in dummy),
            "dummy_lslice_outputs": sum(x["category"] == "unused_lslice_output_dummy" for x in dummy),
        },
        "mac_operand_coverage": {
            "mac_dsp_count": len(mac_dsp),
            "mac_dsp_with_dynamic_activation_xa": sum(
                "reg_activation_front" in item["pins"]["xa"]["expression"] for item in mac_dsp
            ),
            "mac_dsp_with_dynamic_weight_y": sum(
                "reg_weight_front" in item["pins"]["y"]["expression"] for item in mac_dsp
            ),
            "activation_bits_referenced": collect_vector_bits(text, "reg_activation_front"),
            "weight_bits_referenced": collect_vector_bits(text, "reg_weight_front"),
            "bias_bits_referenced": collect_vector_bits(text, "reg_bias_front"),
        },
        "distributed_ram_data_coverage": {
            "activation_packet_bits_on_ram_data": collect_vector_bits(ram_data_text, "reg_packet_activation"),
            "weight_packet_bits_on_ram_data": collect_vector_bits(ram_data_text, "reg_packet_weight"),
            "bias_packet_bits_on_ram_data": collect_vector_bits(ram_data_text, "reg_packet_bias"),
        },
        "reset_release_registers": reset_copies,
        "dsp_siou_instances": dsp_items,
        "dram_hardcon_instances": dram_items,
        "eram_instances": eram_items,
        "dummy_endpoints": dummy,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
