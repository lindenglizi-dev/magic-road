"""按冻结图更新乐观周期预算；协议模型不是整网实测。"""
from collections import deque
import json
from math import ceil

from run import ROOT, tools


def stream_cycles(tasks, groups):
    """四个first到pop credit，A0至末组发布原流水，输出永远ready。"""
    due = deque()
    cycle = sent = received = reserved = active = queued = 0
    while received < tasks:
        pop = queued != 0
        if pop:
            queued -= 1
            received += 1
        while due and due[0] == cycle:
            due.popleft()
            queued += 1
        accept = sent < tasks and (active != 0 or reserved < 4 or pop)
        first = accept and active == 0
        if accept:
            if active == groups - 1:
                due.append(cycle + 6)
                sent += 1
                active = 0
            else:
                active += 1
        reserved += int(first) - int(pop)
        assert 0 <= reserved <= 4
        cycle += 1
    return cycle


def main():
    assert stream_cycles(4, 2) == 15
    path = ROOT.parents[1] / "graph_artifacts/graph.json"
    graph = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        height, width, cout = node["output_shape_hwc"]
        cin = node["input_shape_hwc"][2]
        kernel = node["kernel"][0]
        dw = kernel == 3 and node["groups"] == cin
        kind = "dw" if dw else "pw" if kernel == 1 else "stem"
        groups = (3 if node["stride"][0] == 2 else 2) if dw else ceil(cin * kernel * kernel / 8)
        tasks = height * ceil(width / 3) * cout if dw else height * width * ceil(cout / 3)
        # DW has not been streamed in this candidate; keep its old serial floor.
        mac = tasks * (groups + 7) - 1 if dw else stream_cycles(tasks, groups)
        scalar = height * width * cout
        rows.append({"layer": node["name"], "kind": kind, "tasks": tasks,
                     "groups": groups, "mac_model": mac, "scalar_II1_floor": scalar,
                     "optimistic_cycles": max(mac, scalar)})
    totals = {kind: sum(row["optimistic_cycles"] for row in rows if row["kind"] == kind)
              for kind in ("stem", "dw", "pw")}
    result = {"label": "OPTIMISTIC_PROTOCOL_BUDGET_NOT_FULL_NETWORK_SIMULATION",
              "graph": str(path), "graph_sha256": tools.digest(path), "rows": rows,
              "totals": totals, "sum": sum(totals.values()), "budget_5fps": 20000000,
              "assumptions": ["PW and Stem future schedulers use new four-credit ordered MAC; only down2 PW is RTL-measured now.",
                  "MAC result always ready; per-layer scalar lower floor assumes II1, not actual backpressure.",
                  "DW keeps serialized task floor; actual DW_POST, load/preparation and drain are additional.",
                  "DDR, ROM, non-convolution, postprocess latency/stalls and frame/control costs omitted.",
                  "Old 26488157 bound assumes last locks input, so no longer applies to streamed PW/Stem."],
              "measured_down2": {"dw": 2015, "pw": 592, "total": 2607,
                                  "source": "candidate same frozen vectors; TEST parameters"}}
    assert len(rows) == 67
    (ROOT / "layer_budget.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"totals": totals, "sum": result["sum"], "not_measured_FPS": True}))


if __name__ == "__main__":
    main()
