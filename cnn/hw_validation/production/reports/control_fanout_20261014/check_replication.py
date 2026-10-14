"""核对TD报告中的负载分区及六个已知LUT驱动；仅检查本次物理变换。"""
import json
from pathlib import Path
import re
import sys

from run import BASE, NET, ROOT, save, sha


def sinks(block):
    loads = block.split("Load pin(s):", 1)[1]
    return re.findall(r"RUN-1001 :\s+\d+\s*\|\s*(\S+)\s*\|", loads)


def driver_name(block):
    pins = block.split("Driver pin(s):", 1)[1].split("Load pin(s):", 1)[0]
    names = re.findall(r"RUN-1001 :\s+\d+\s*\|\s*(\S+)\s*\|", pins)
    assert len(names) == 1 and names[0].endswith(".ofa")
    return names[0][:-4]


def driver(text, name):
    # This is a bounded literal extraction, not a replacement HDL parser.
    instance = "\\" + name + " "
    position = text.index(instance)
    start = text.rfind("  PH1P_PHY_LSLICE #(", 0, position)
    end = text.index(");", position)
    block = text[start:end]
    fields = dict(re.findall(r"^\s*\.(\w+)\(([^\n]+)\)[,\s]*$", block, re.M))
    assert fields["OFA_SD"] == '"LUT5A"'
    assert fields["LUTMODE"] == '"DLUT5"'
    return fields


def check(work):
    log = (work / "td_launcher.log").read_text(encoding="utf-8")
    before = log.split("TARGET_BEFORE_BEGIN", 1)[1].split("TARGET_BEFORE_END", 1)[0]
    after = log.split("TARGET_AFTER_BEGIN", 1)[1].split("TARGET_AFTER_END", 1)[0]
    old_sinks = sinks(before)
    groups, drivers = {}, []
    for block in after.split("RUN-1001 : Net: ")[1:]:
        name = block.splitlines()[0]
        if name == NET or name.startswith(NET.rsplit("_", 1)[0] + "_"):
            groups[name] = sinks(block)
            drivers.append(driver_name(block))
    new_sinks = [pin for pins in groups.values() for pin in pins]
    assert len(old_sinks) == len(new_sinks) == 824
    assert len(set(old_sinks)) == len(set(new_sinks)) == 824
    assert set(old_sinks) == set(new_sinks)
    baseline = (BASE / "physical/routed_netlist.v").read_text(encoding="utf-8")
    candidate = (work / "routed_netlist.v").read_text(encoding="utf-8")
    original = driver(baseline, driver_name(before))
    values = []
    for name in drivers:
        actual = driver(candidate, name)
        output = actual.pop("ofa")
        expected = dict(original)
        expected.pop("ofa")
        assert actual == expected, (name, actual, expected)
        values.append({"instance": name, "output": output})
    result = {"status": "PASS_BOUNDED_BOOLEAN_AND_SINK_EQUIVALENCE", "work": str(work),
        "sink_count_before": 824, "sink_count_after": 824,
        "sink_missing_duplicate_extra": 0, "fanouts": {name: len(pins) for name, pins in groups.items()},
        "identical_driver_fields": expected, "drivers": values,
        "baseline_netlist_sha256": sha(BASE / "physical/routed_netlist.v"),
        "candidate_netlist_sha256": sha(work / "routed_netlist.v"),
        "limits": ["Literal LUT configuration and input-net identity, binary Boolean equivalence only",
                   "Not a whole-design formal check, gate simulation, X/Z or analog timing proof",
                   "Final routing and all timing endpoints are required separately"]}
    save(work / "replication_equivalence.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(check(ROOT / (sys.argv[1] if len(sys.argv) > 1 else "physical_attempt2")), ensure_ascii=False, indent=2))
