"""新布局的28端ROM许可分组检查；复用旧字面提取，不改变历史67端契约。"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "prefetch_admission_20261014"))
from check_replication import pins, driver
from run import sha, save, prior

prior.helpers.ROOT = ROOT


def check():
    work = ROOT / "physical"
    log = (work / "td_launcher.log").read_text(encoding="utf-8")
    before = log.split("TARGET_BEFORE_BEGIN", 1)[1].split("TARGET_BEFORE_END", 1)[0]
    after = log.split("TARGET_AFTER_BEGIN", 1)[1].split("TARGET_AFTER_END", 1)[0]
    original_sinks = pins(before, "Load pin(s):")
    assert len(original_sinks) == len(set(original_sinks)) == 28
    before_drivers = pins(before, "Driver pin(s):")
    assert len(before_drivers) == 1
    original, _ = driver((work / "before_rom_clone.v").read_text(encoding="utf-8"), before_drivers[0])
    netlist = (work / "routed_netlist.v").read_text(encoding="utf-8")
    actual_sinks, groups = [], {}
    for block in after.split("RUN-1001 : Net: ")[1:]:
        loads = pins(block, "Load pin(s):")
        if not set(loads).intersection(original_sinks):
            continue
        drivers = pins(block, "Driver pin(s):")
        assert len(drivers) == 1
        actual, _ = driver(netlist, drivers[0])
        assert actual == original
        route_type = re.search(r"Route Type\s*\|\s*(\S+)", block).group(1)
        assert route_type in ("global", "local")
        groups[block.splitlines()[0]] = {"loads": len(loads), "driver": drivers[0], "route_type": route_type}
        actual_sinks.extend(loads)
    assert len(actual_sinks) == len(set(actual_sinks)) == 28
    assert set(actual_sinks) == set(original_sinks)
    result = {"status": "PASS_BOUNDED_28_SINK_ROM_CONTROL", "groups": groups, "missing_duplicate_extra": 0,
        "before_sink_count": 28, "driver_fields": original,
        "before_netlist_sha256": sha(work / "before_rom_clone.v"), "after_netlist_sha256": sha(work / "routed_netlist.v"),
        "scope": "Only this layout's original 28-sink branch; not prior 67-sink layout, full formal or gate simulation"}
    save(work / "rom_control_equivalence.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    check()
