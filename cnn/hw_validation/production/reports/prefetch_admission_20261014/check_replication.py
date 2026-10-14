"""只核查本次ROM接受控制的LUT字面配置和接收端集合，不代替HDL解析器。"""
import json
import re
import sys

from run import ROOT, WRITE_ENABLES, save, sha


def pins(block, section):
    text = block.split(section, 1)[1]
    if section == "Driver pin(s):":
        text = text.split("Load pin(s):", 1)[0]
    return re.findall(r"RUN-1001 :\s+\d+\s*\|\s*(\S+)\s*\|", text)


def cell_fields(text, name):
    position = text.index("\\" + name + " ")
    start = text.rfind("  PH1P_PHY_LSLICE #(", 0, position)
    assert start >= 0
    end = text.index(");", position)
    return dict(re.findall(r"^\s*\.(\w+)\(([^()\n]*)\)\)?[,\s]*$", text[start:end], re.M))


def driver(text, pin):
    name, output = pin.rsplit(".", 1)
    assert output == "ofb"
    fields = cell_fields(text, name)
    assert fields["LUTMODE"] == '"DLUT5"' and fields["OFB_SD"] == '"LUTX"'
    output_net = fields.pop(output)
    assert all(name in fields for name in ("INIT_LUT5B", "LUT5B_SD2", "ia", "ib", "ic", "ie", "imb"))
    return fields, output_net


def check(work):
    log = (work / "td_launcher.log").read_text(encoding="utf-8")
    before = log.split("TARGET_BEFORE_BEGIN", 1)[1].split("TARGET_BEFORE_END", 1)[0]
    after = log.split("TARGET_AFTER_BEGIN", 1)[1].split("TARGET_AFTER_END", 1)[0]
    old_sinks = pins(before, "Load pin(s):")
    assert len(old_sinks) == len(set(old_sinks)) == 67
    original_driver = pins(before, "Driver pin(s):")
    assert len(original_driver) == 1
    original, _ = driver((work / "before_rom_clone.v").read_text(encoding="utf-8"), original_driver[0])
    netlist = (work / "routed_netlist.v").read_text(encoding="utf-8")
    groups, outputs, new_sinks = {}, [], []
    for block in after.split("RUN-1001 : Net: ")[1:]:
        loads = pins(block, "Load pin(s):")
        if not set(loads).intersection(old_sinks):
            continue
        name = block.splitlines()[0]
        actual_drivers = pins(block, "Driver pin(s):")
        assert len(actual_drivers) == 1
        actual, output_net = driver(netlist, actual_drivers[0])
        assert actual == original, (name, actual, original)
        route_type = re.search(r"Route Type\s*\|\s*(\S+)", block).group(1)
        assert route_type in ("global", "local"), (name, route_type)
        groups[name] = {"loads": len(loads), "route_type": route_type, "driver": actual_drivers[0]}
        outputs.append(output_net)
        new_sinks.extend(loads)
    assert len(new_sinks) == len(set(new_sinks)) == 67
    assert set(new_sinks) == set(old_sinks)
    result = {"status": "PASS_BOUNDED_BOOLEAN_SINK_AND_ROUTE_CHECK", "net_groups": groups,
        "sink_count_before": 67, "sink_count_after": 67, "missing_duplicate_extra": 0,
        "driver_function_fields": original, "outputs": outputs,
        "before_netlist_sha256": sha(work / "before_rom_clone.v"),
        "after_netlist_sha256": sha(work / "routed_netlist.v"),
        "scope": "Same LUT configuration, same scalar input nets, exact 67 sink partition; not whole-design formal or gate simulation"}
    save(work / "replication_equivalence.json", result)
    return result


def check_writes(work):
    """只检查本次三条组合WE网；不解析/放宽通用RTL门禁。"""
    log = (work / "td_launcher.log").read_text(encoding="utf-8")
    before_text = (work / "before_we_clone.v").read_text(encoding="utf-8")
    after_text = (work / "routed_netlist.v").read_text(encoding="utf-8")
    results = []
    for index, (target, count) in enumerate(WRITE_ENABLES):
        before = log.split(f"WE_BEFORE_{index}_BEGIN", 1)[1].split(f"WE_BEFORE_{index}_END", 1)[0]
        after = log.split(f"WE_AFTER_{index}_BEGIN", 1)[1].split(f"WE_AFTER_{index}_END", 1)[0]
        old_sinks = pins(before, "Load pin(s):")
        assert len(old_sinks) == len(set(old_sinks)) == count
        old_drivers = pins(before, "Driver pin(s):")
        assert len(old_drivers) == 1
        original_name, output = old_drivers[0].rsplit(".", 1)
        original = cell_fields(before_text, original_name)
        assert output in ("ofa", "ofb") and original["LUTMODE"] == '"DLUT5"'
        half = "A" if output == "ofa" else "B"
        keys = ["LUTMODE", f"INIT_LUT5{half}", f"{output.upper()}_SD",
                "LUT5A_SD0" if half == "A" else "LUT5B_SD2", "ia", "ib", "ic", "id", "ie"]
        # Both actual selectors use IC/ID, never the packed register's IMB input.
        assert original[keys[3]] in ('"IC"', '"ID"')
        expected = {key: original.get(key) for key in keys}
        groups, actual_sinks = {}, []
        for block in after.split("RUN-1001 : Net: ")[1:]:
            loads = pins(block, "Load pin(s):")
            assert set(loads).intersection(old_sinks)
            drivers = pins(block, "Driver pin(s):")
            assert len(drivers) == 1
            name, port = drivers[0].rsplit(".", 1)
            actual = cell_fields(after_text, name)
            assert port == output and {key: actual.get(key) for key in keys} == expected
            assert not any(actual.get(port) for port in ("oqa", "oqb", "oqc", "oqd"))
            route_type = re.search(r"Route Type\s*\|\s*(\S+)", block).group(1)
            assert route_type in ("global", "local")
            groups[block.splitlines()[0]] = {"driver": drivers[0], "loads": len(loads), "route_type": route_type}
            actual_sinks.extend(loads)
        assert len(actual_sinks) == len(set(actual_sinks)) == count
        assert set(actual_sinks) == set(old_sinks)
        results.append({"target": target, "sinks": count, "groups": groups, "lut_fields": expected,
                        "cloned_registered_outputs": 0})
    tag_cell = "u_compute/u_stem/cnt_channel_reg[1]_syn_54"
    original, actual = (cell_fields(text, tag_cell) for text in (before_text, after_text))
    tag_keys = [key for key in original if key.startswith("REGB") or key in
                ("ASRMUX", "CEBMUX", "CLKMUX", "LATCHMODE", "OQBMUX", "SSRMUX", "SSROVERCE", "asr", "imb", "oqb")]
    assert {key: original[key] for key in tag_keys} == {key: actual[key] for key in tag_keys}
    tag_net = original["oqb"]
    def refs(text):
        result = []
        for match in re.finditer(r"^\s*\.(\w+)\(" + re.escape(tag_net) + r"\)", text, re.M):
            start = text.rfind("\n    \\", 0, match.start())
            assert start >= 0
            instance = text[start:].splitlines()[1].strip().removesuffix("(").strip()
            result.append(instance + "." + match.group(1))
        return sorted(result)
    assert refs(before_text) == refs(after_text)
    assert sum(pin.endswith(".oqb") for pin in refs(after_text)) == 1
    result = {"status": "PASS_BOUNDED_WE_LUT_SINK_ROUTE_AND_PACKED_TAG_CHECK", "nets": results,
              "tag_cell": tag_cell, "tag_net": tag_net, "tag_registered_function_fields": tag_keys,
              "tag_connected_pins": refs(after_text),
              "before_netlist_sha256": sha(work / "before_we_clone.v"),
              "after_netlist_sha256": sha(work / "routed_netlist.v"),
              "scope": "Three fixed WE nets and packed tag boundary only; not full formal or gate simulation"}
    save(work / "write_replication_equivalence.json", result)
    return result


if __name__ == "__main__":
    work = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "physical")
    result = {"rom": check(work)}
    if (work / "before_we_clone.v").exists():
        result["writes"] = check_writes(work)
    print(json.dumps(result, ensure_ascii=False, indent=2))
