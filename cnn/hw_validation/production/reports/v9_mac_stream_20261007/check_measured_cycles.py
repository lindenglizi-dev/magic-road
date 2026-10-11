"""Independently audit actual log counters; never derive cycles from MAC peaks."""
import hashlib
import csv
import json
import re
from pathlib import Path


def records(text, marker):
    result = []
    for line in text.splitlines():
        if line.startswith("# " + marker + " "):
            result.append({key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", line)})
    return result


def shell_cycles(root, previous):
    log = (root / "verification/modelsim_shell_v9_regression_run_final.log").read_text(encoding="utf-8")
    assert "TB_PASS_LOW_IO cases=14 errors=0" in log
    assert not any(word in log for word in ("ENOENT", "TB_ERROR", "TB_FAIL", "** Error"))
    with (root / "verification/shell_cycle_trace.csv").open(newline="", encoding="utf-8") as stream:
        rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(stream)]
    names = {0: "mac", 1: "pre_requant", 2: "pre_requant", 3: "pre_requant", 4: "silu",
             5: "silu", 6: "post_requant", 7: "post_requant", 8: "commit", 9: "commit",
             10: "commit", 11: "fault"}
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
            old = previous["reset_regression"]["completed_runs"][len(runs)]
            for key in buckets:
                if key != "mac":
                    assert buckets[key] == old["buckets"][key], (old["name"], key)
            runs.append({"name": old["name"], "old_core_cycles": old["core_cycles"],
                         "core_cycles": delta, "buckets": buckets})
            start = None
    assert len(runs) == 11 and cancelled == 1
    return {"completed_runs": runs, "cancelled_runs": cancelled}


def main():
    root = Path(__file__).resolve().parent
    path = root / "verification/modelsim_layer_run_final2.log"
    text = path.read_text(encoding="utf-8")
    assert "TB_PASS_DOWN2_TILE cases=4" in text
    assert "Errors: 0, Warnings: 0" in text
    assert not any(word in text for word in ("ENOENT", "TB_FAIL", "TB_ERROR", "** Warning", "** Error"))
    core = records(text, "CYCLE_RESULT")
    layers = records(text, "LAYER_CYCLE_RESULT")
    preload = records(text, "PRELOAD_RESULT")
    export = records(text, "EXPORT_RESULT")
    assert all(len(items) == 4 for items in (core, layers, preload, export))
    assert all([item["case"] for item in items] == list(range(4)) for items in (core, layers, preload, export))
    buckets = ("mac", "pre", "silu", "post", "writeback", "storage_wait", "scheduler_idle")
    old = json.loads((root.parent / "v8_reset_layer_tiles_20261007/independent_measured_cycles.json").read_text(encoding="utf-8"))
    comparisons = []
    for case, item in enumerate(core):
        assert item["core"] == item["endpoint"] == sum(item[key] for key in buckets)
        assert item["core"] == (12929 if case == 3 else 23937)
        for layer in ("dw", "pw"):
            assert layers[case][layer + "_core"] == sum(layers[case][layer + "_" + key] for key in buckets)
        assert layers[case]["dw_core"] == (0 if case == 3 else 11008)
        assert layers[case]["pw_core"] == 12929
        assert layers[case]["dw_core"] + layers[case]["pw_core"] == item["core"]
        assert preload[case]["table_writes"] == 1024
        assert preload[case]["endpoint"] == (1692 if case == 3 else 2894)
        assert preload[case]["cache_writes"] == (664 if case == 3 else 1864)
        assert export[case] == {"case": case, "transfers": 384, "cycles": 449}
        previous = old["layer_tiles"]["core"][case]
        for key in buckets:
            if key != "mac":
                assert item[key] == previous[key], (case, key)
        comparisons.append({"case": case, "old_core": previous["core"], "new_core": item["core"],
                            "saved_cycles": previous["core"] - item["core"],
                            "cycle_reduction_percent": 100 * (previous["core"] - item["core"]) / previous["core"]})
    result = {"status": "INDEPENDENT_MEASURED_CYCLES_PASS", "core": core, "layers": layers,
              "preload": preload, "export": export, "comparisons": comparisons,
              "log_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "scope": "Frozen runner/test parameters; disjoint state occupancy. Local storage preparation is not DDR latency. Physical timing is separate."}
    if (root / "verification/modelsim_shell_v9_regression_run_final.log").exists():
        result["shell"] = shell_cycles(root, old)
    graph = json.loads((root.parent.parent / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    activated = [node for node in graph["nodes"] if node["op"] == "conv" and node["name"].endswith(".conv")]
    prediction = [node for node in graph["nodes"] if node["op"] == "conv" and not node["name"].endswith(".conv")]
    assert len(activated) == 61 and len(prediction) == 6
    values = sum(node["output_shape_hwc"][0] * node["output_shape_hwc"][1] * node["output_shape_hwc"][2] for node in activated)
    assert values == 6833664
    result["conditional_serial_strategy"] = {
        "activation_output_values": values, "measured_pw_cycles_per_activation": 27,
        "non_overlapped_activation_cycles": values * 27,
        "non_overlapped_activation_seconds_at_100mhz": values * 27 / 100_000_000,
        "scope": "If the current scalar pre10/SiLU7/post10 non-overlap policy is copied to all 61 ConvBNAct nodes. Excludes MAC, DDR, pooling, predictions and postprocessing. Not a whole-network measurement or a limit on a redesigned pipeline."
    }
    (root / "independent_measured_cycles.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "comparisons": comparisons}))


if __name__ == "__main__":
    main()
