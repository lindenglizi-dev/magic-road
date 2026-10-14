"""复用字面字段核对，检查本布局两条控制网复制后的函数及负载集合。"""
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
path = ROOT.parent / "stem_location_constraint_20261014/connection_check.py"
spec = importlib.util.spec_from_file_location("commit_literal_fields", path)
literal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(literal)


def pins(text, section):
    block = text.split(section, 1)[1]
    if section == "Driver pin(s):":
        block = block.split("Load pin(s):", 1)[0]
    return re.findall(r"RUN-1001 :\s+\d+\s*\|\s*(\S+)\s*\|", block)


def function(text, name, output):
    assert output in ("ofa", "ofb")
    values = literal.fields(text, output, "\\" + name + " ")
    half = output[-1].upper()
    keys = ("LUTMODE", "INIT_LUT5" + half, output.upper() + "_SD",
            "LUT5A_SD0" if half == "A" else "LUT5B_SD2", "ia", "ib", "ic", "id", "ie")
    mode = values["LUTMODE"]
    assert mode in ('"DLUT5"', '"LUT6"')
    assert values[output.upper() + "_SD"] in ('"LUTX"', '"LUT5A"')
    if half == "A":
        keys = (*keys, "LUT5A_SD1")
        if values.get("LUT5A_SD1") == '"IMF"':
            keys = (*keys, "imf")
    if mode == '"LUT6"':
        keys = ("LUTMODE", "INIT_LUT5A", "INIT_LUT5B", "OFB_SD", "LUT5A_SD0", "LUT5B_SD2",
                "ia", "ib", "ic", "id", "ie", "imf")
    # IMB可代替第五个LUT输入，必须一并绑定，不能遗漏。
    if values.get(keys[3]) == '"IMB"':
        keys = (*keys, "imb")
    return {key: values.get(key) for key in keys}


def check():
    work = ROOT / "physical_attempt2"
    log = (work / "td_launcher.log").read_text(encoding="utf-8")
    routed = (work / "routed_netlist.v").read_text(encoding="utf-8")
    records = {}
    for label, expected in (("ADVANCE", 850), ("ROM", 50)):
        before = log.split(label + "_BEFORE_BEGIN", 1)[1].split(label + "_BEFORE_END", 1)[0]
        after = log.split(label + "_AFTER_BEGIN", 1)[1].split(label + "_AFTER_END", 1)[0]
        old_loads = pins(before, "Load pin(s):")
        assert len(old_loads) == len(set(old_loads)) == expected
        target = re.search(r"RUN-1001 : Net: (\S+)", before).group(1)
        driver = pins(before, "Driver pin(s):")
        assert len(driver) == 1
        output = driver[0].rsplit(".", 1)[1]
        original = function((work / ("before_" + label.lower() + "_clone.v")).read_text(encoding="utf-8"), target, output)
        all_loads, groups = [], {}
        for block in after.split("RUN-1001 : Net: ")[1:]:
            loads = pins(block, "Load pin(s):")
            if not set(loads).intersection(old_loads):
                continue
            name = block.splitlines()[0].strip()
            outputs = pins(block, "Driver pin(s):")
            assert len(outputs) == 1
            actual_output = outputs[0].rsplit(".", 1)[1]
            assert function(routed, name, actual_output) == original, name
            groups[name] = len(loads)
            all_loads.extend(loads)
        assert len(all_loads) == len(set(all_loads)) == expected and set(all_loads) == set(old_loads)
        records[label] = {"sinks": expected, "groups": groups, "lut_fields": original,
                          "missing_duplicate_extra": 0}
    result = {"status": "PASS", "controls": records,
              "scope": "Two known combinational control drivers only; not full-design formal equivalence"}
    (work / "control_replication_check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    check()
