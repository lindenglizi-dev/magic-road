"""TD固定格式字面连接收据，非HDL解析器，不替代技能AST或时序分析。"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "prefetch_admission_20261014/physical/gate_netlist.v"
CELL = re.compile(r'^(PH1P_PHY_[A-Z0-9_]+|AL_MAP_LUT[1-6]) #\(\n(.*?)\n    (\S+)  \(\n(.*?)\);([^\n]*)', re.S)
PORT = re.compile(r'\.(\w+)\(([^()]*)\)')


def literal_records(path):
    text = path.read_text(encoding="utf-8")
    result = []
    line_number = 1
    for block in re.split(r"\n  (?=\S)", text):
        match = CELL.match(block)
        if match is None:
            line_number += block.count("\n") + 1
            continue
        kind, parameters, name, body, comment = match.groups()
        ports = dict(PORT.findall(body))
        assert ports and len(ports) == len(PORT.findall(body))
        result.append({"kind": kind, "name": name, "parameters": parameters,
                       "ports": ports, "source": comment, "line": line_number})
        line_number += block.count("\n") + 1
    assert any(row["kind"] == "PH1P_PHY_DRAMHARDCON" for row in result)
    assert sum(row["kind"] == "PH1P_PHY_ERAM_V2" for row in result) >= 56
    return text, result


def summarize(path, middle_line):
    text, cells = literal_records(path)
    # 仅AL_MAP_LUT输出o的精确字面驱动，不猜测未知原语或寄存器的内部行为。
    drivers = {row["ports"]["o"]: row for row in cells if row["kind"].startswith("AL_MAP_LUT")}
    assert len(drivers) == sum(row["kind"].startswith("AL_MAP_LUT") for row in cells)

    def cone(net, seen=()):
        assert net not in seen, ("combinational loop", net)
        if net not in drivers:
            return {"lut_depth": 0, "leaves": [net]}
        row = drivers[net]
        children = [cone(value, (*seen, net)) for name, value in row["ports"].items() if name != "o"]
        return {"lut_depth": 1 + max(child["lut_depth"] for child in children),
                "leaves": sorted(set(leaf for child in children for leaf in child["leaves"]))}

    rams = [row for row in cells if row["kind"] == "PH1P_PHY_DRAMHARDCON" and
            row["name"].startswith("\\u_compute/u_stem/")]
    middle = [row for row in rams if "reg_weight_middle" in row["ports"]["we"]] if middle_line else []
    weight = [row for row in rams if "reg_weight" in row["ports"]["we"]]
    bits = [row for row in cells if row["kind"] == "PH1P_PHY_MSLICE" and
            "RAMMODE(\"DPRAM\")" in row["parameters"] and
            f"road_stem_tile_scheduler.v({middle_line})" in row["source"]] if middle_line else []
    erams = [row for row in cells if row["kind"] == "PH1P_PHY_ERAM_V2"]
    return {"path": str(path), "ram_control_count": len(rams), "weight_ram_controls": len(weight),
        "weight_we_sink_counts": dict(Counter(row["ports"]["we"] for row in weight)),
        "we_cones": {net: cone(net) for net in sorted(set(row["ports"]["we"] for row in weight))},
        "middle_controls": middle, "middle_bit_cell_count": len(bits),
        "middle_data_connections": dict(Counter(row["ports"]["imb"] for row in bits)),
        "erams": [{"name": row["name"], "line": row["line"]} for row in erams],
        "luts": sum(row["kind"].startswith("AL_MAP_LUT") for row in cells),
        "rom_erams": sum(row["name"].startswith("\\u_rom/") for row in erams),
        "lut_depth_only_not_routed_delay": True}, text, cells


def qor(path):
    text = path.read_text(encoding="utf-8")
    return {name: int(re.search(r'\|\s*#' + name + r'\s*\|\s*(\d+)', text)[1])
            for name in ("registers", "luts", "slices", "RAMs", "DSPs")}


def run():
    work = sorted(ROOT.glob("synthesis*/receipt.json"), key=lambda path: path.stat().st_mtime)[-1].parent
    baseline, _, baseline_cells = summarize(BASE, 0)
    candidate, text, cells = summarize(work / "gate_netlist.v", 187)
    controls = candidate["middle_controls"]
    assert len(controls) == 24 and candidate["middle_bit_cell_count"] == 192
    address_direct = all(row["ports"]["waddr"] == "\\u_compute/u_down2/i_load_addr [5:1]" for row in controls)
    data_direct = all(re.fullmatch(r'\\u_compute/u_stem/i_load_data \[[0-7]\]', net)
                      for net in candidate["middle_data_connections"])
    # 目标byteaddr有共享地址owner选择和两次反相；按真实LUT INIT逐项验证。
    byteaddr = sorted(set(row["ports"]["byteaddr"] for row in controls))
    drivers = {row["ports"]["o"]: row for row in cells if row["kind"].startswith("AL_MAP_LUT")}
    inverted = drivers[byteaddr[0]]
    selected = drivers[inverted["ports"]["a"]]
    assert inverted["kind"] == "AL_MAP_LUT1" and ".INIT(2'h1)" in inverted["parameters"]
    assert selected["kind"] == "AL_MAP_LUT3" and ".INIT(8'h47)" in selected["parameters"]
    assert selected["ports"] == {"a": "\\i_load_addr[0]_dup_1 ", "b": "flag_external_owner",
                                  "c": "reg_pref_address[0]", "o": inverted["ports"]["a"]}
    for sample in range(8):
        external, owner, prefetched = sample & 1, (sample >> 1) & 1, (sample >> 2) & 1
        assert 1 - ((0x47 >> sample) & 1) == (external if owner else prefetched)
    erams_removed = sorted(set(row["name"] for row in baseline["erams"]) - set(row["name"] for row in candidate["erams"]))
    target = "\\u_compute/u_stem/reg_weight_middle_n1 "
    old_target = "\\u_compute/u_stem/reg_weight_n1_syn_98 "
    def rom_initializers(records):
        return {row["name"]: re.findall(r'\.INITP?_[0-9A-Fa-f]+\([^\n]*\)', row["parameters"])
                for row in records if row["kind"] == "PH1P_PHY_ERAM_V2" and row["name"].startswith("\\u_rom/")}
    old_init, new_init = rom_initializers(baseline_cells), rom_initializers(cells)
    assert len(new_init) == 56 and sum(map(len, new_init.values())) == 4480 and old_init == new_init
    baseline_qor = qor(ROOT.parent / "weight_address_stem_write_20261013/physical/gate.qor")
    candidate_qor = qor(work / "gate.qor")
    same_we_depth = candidate["we_cones"][target]["lut_depth"] == baseline["we_cones"][old_target]["lut_depth"]
    same_we_leaves = candidate["we_cones"][target]["leaves"] == baseline["we_cones"][old_target]["leaves"]
    increased_sinks = candidate["weight_we_sink_counts"][target] > baseline["weight_we_sink_counts"][old_target]
    assert same_we_depth and same_we_leaves and increased_sinks
    gate = {"independent_ram_group": True, "waddr_direct": address_direct, "data_direct": data_direct,
            "byteaddr_nets": byteaddr, "byteaddr_truth_cases": 8, "byteaddr_drivers": [selected, inverted],
            "target_we_lut_depth": candidate["we_cones"][target]["lut_depth"],
            "target_we_ram_sinks": candidate["weight_we_sink_counts"][target],
            "baseline_target_we_lut_depth": baseline["we_cones"][old_target]["lut_depth"],
            "baseline_target_we_ram_sinks": baseline["weight_we_sink_counts"][old_target],
            "we_leaves_identical": same_we_leaves, "we_improvement_proven": False,
            "eram_delta": len(candidate["erams"]) - len(baseline["erams"]),
            "erams_removed_names": erams_removed,
            "physical_run_authorized_by_structure": False,
            "reason": "REJECT: target WE retains 7 LUT levels and same leaves; sinks 21->24. No demonstrated control-path improvement"}
    result = {"baseline": baseline, "candidate": candidate, "structural_gate": gate,
              "gate_qor": {"baseline": baseline_qor, "candidate": candidate_qor,
                           "delta": {key: candidate_qor[key]-baseline_qor[key] for key in candidate_qor}},
              "rom_init_identical": {"cells": 56, "entries": 4480, "pass": True,
                                     "sha256": hashlib.sha256(json.dumps(new_init, sort_keys=True).encode()).hexdigest()},
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT / "mapping_receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(gate, ensure_ascii=False))


if __name__ == "__main__":
    run()
