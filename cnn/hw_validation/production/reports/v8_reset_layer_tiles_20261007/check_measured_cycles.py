"""Audit reset regression trace and actual tile counter/endpoint evidence."""
import csv
import json
import re
from pathlib import Path


def check_shell(root):
    previous = json.loads((root.parent / "v7_low_io_physical_20261006/shell/shell_cycle_summary.json").read_text(encoding="utf-8"))
    with (root / "reset/shell_cycle_trace.csv").open(encoding="utf-8", newline="") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]
    names = {0: "mac", 1: "pre_requant", 2: "pre_requant", 3: "pre_requant",
             4: "silu", 5: "silu", 6: "post_requant", 7: "post_requant",
             8: "commit", 9: "commit", 10: "commit", 11: "fault"}
    runs = []
    cancelled = 0
    start = None
    for index, row in enumerate(rows):
        if not row["rstn"]:
            cancelled += start is not None
            start = None
            continue
        if start is None and row["core_input"]:
            start = index
        if start is not None and row["shell_state"] == 6 and index + 1 < len(rows) and rows[index + 1]["shell_state"] == 7:
            buckets = dict.fromkeys(("mac", "pre_requant", "silu", "post_requant", "commit", "fault"), 0)
            for sample in rows[start:index]:
                buckets[names[sample["chain_state"]]] += 1
            delta = row["cycle"] - rows[start]["cycle"]
            assert sum(buckets.values()) == delta
            old = previous["runs"][len(runs)]
            assert delta == old["endpoint_delta_cycles"] and buckets == old["exclusive_stage_cycles"], (old, delta, buckets)
            runs.append({"name": old["name"], "core_cycles": delta, "buckets": buckets})
            start = None
    assert len(runs) == len(previous["runs"]) == 11
    assert cancelled == len(previous["cancelled_runs"]) == 1
    return {"completed_runs": runs, "cancelled_runs": cancelled, "baseline_core_cycles": runs[0]["core_cycles"]}


def check_tiles(root):
    log = (root / "layers/modelsim_run_complete.log").read_text(encoding="utf-8")
    assert "TB_PASS_DOWN2_TILE" in log and "TB_ERROR_" not in log and "TB_FAIL_" not in log
    core = []
    for line in log.splitlines():
        if "# CYCLE_RESULT " in line:
            values = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
            assert values["core"] == values["endpoint"]
            assert values["core"] == sum(values[name] for name in (
                "mac", "pre", "silu", "post", "writeback", "storage_wait", "scheduler_idle"))
            core.append(values)
    assert len(core) == 4
    assert [item["core"] for item in core] == [27393, 27393, 27393, 14081]
    exports = [{key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
               for line in log.splitlines() if "EXPORT_RESULT " in line]
    assert len(exports) == 4 and all(item["transfers"] == 384 for item in exports)
    assert all(item["cycles"] == 449 for item in exports)
    preloads = [{key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
                for line in log.splitlines() if "PRELOAD_RESULT " in line]
    assert len(preloads) == 4
    assert [item["endpoint"] for item in preloads] == [2894, 2894, 2894, 1692]
    assert all(item["table_writes"] == 1024 for item in preloads)
    assert [item["cache_writes"] for item in preloads] == [1864, 1864, 1864, 664]
    assert "RESET_RESULT in_flight_cancel=pass ghost_window=20" in log
    assert "FAULT_RESULT mac_overflow_atomic_publish=pass" in log
    layers = [{key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)}
              for line in log.splitlines() if "LAYER_CYCLE_RESULT " in line]
    assert len(layers) == 4
    stages = ("mac", "pre", "silu", "post", "writeback", "storage_wait", "scheduler_idle")
    for item, total in zip(layers, core):
        for layer in ("dw", "pw"):
            assert item[layer + "_core"] == sum(item[layer + "_" + stage] for stage in stages)
        assert item["dw_core"] + item["pw_core"] == total["core"]
        for stage in stages:
            assert item["dw_" + stage] + item["pw_" + stage] == total[stage]
    assert [item["dw_core"] for item in layers] == [13312, 13312, 13312, 0]
    assert all(item["pw_core"] == 14081 for item in layers)
    return {"core": core, "layers": layers, "preload": preloads, "export": exports,
            "limits": "storage_wait denotes fixed local-array read preparation, not measured DDR wait; preload elapsed cycles include table writes and task gaps"}


def main():
    root = Path(__file__).resolve().parent
    result = {"status": "INDEPENDENT_MEASURED_CYCLES_PASS",
              "reset_regression": check_shell(root), "layer_tiles": check_tiles(root)}
    (root / "independent_measured_cycles.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "old_and_new_core_cycles": 436,
                      "complete_shell_runs": 11, "tile_core_cycles": [item["core"] for item in result["layer_tiles"]["core"]]}))


if __name__ == "__main__":
    main()
