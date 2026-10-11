"""当前单归约上下文的条件周期下界；不是全网运行或DDR测量。"""
import json
from math import ceil
from pathlib import Path

from run import ROOT, tools


def main():
    graph_path = ROOT.parents[1] / "graph_artifacts/graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    rows = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        height, width, cout = node["output_shape_hwc"]
        cin = node["input_shape_hwc"][2]
        kernel = node["kernel"][0]
        dw = kernel == 3 and node["groups"] == cin
        kind = "dw" if dw else "pw" if kernel == 1 else "stem"
        groups = (3 if node["stride"][0] == 2 else 2) if dw else ceil(cin*kernel*kernel/8)
        tasks = height*ceil(width/3)*cout if dw else height*width*ceil(cout/3)
        rows.append({"layer": node["name"], "kind": kind, "groups": groups, "tasks": tasks,
                     "conditional_cycles": tasks*(groups+7)})
    totals = {kind: sum(row["conditional_cycles"] for row in rows if row["kind"] == kind)
              for kind in ("stem", "dw", "pw")}
    # The final task needs no next-first gap; subtract one cycle for each layer.
    lower = sum(totals.values())-len(rows)
    result = {"source": str(graph_path), "graph_sha256": tools.digest(graph_path),
        "label": "CONDITIONAL_SINGLE_CONTEXT_MAC_LOWER_BOUND_NOT_MEASURED_FPS",
        "assumptions": ["Current frozen MAC, one reduction context, II1 within each task.",
            "No task overlap: last closes input until registered terminal result acceptance.",
            "No stalls; all arithmetic groups and next first operands immediately available.",
            "DW three spatial outputs per row, stride1 G2 or stride2 G3; PW three channels.",
            "G+7 first-to-first spacing: current RTL pipeline, observed G2 spacing9.",
            "Last task of each convolution subtracts1 because next-first is not required.",
            "Postprocess/DDR/non-convolution/start/drain overhead is omitted, not zero in deployment."],
        "rows": rows, "raw_totals": totals, "last_task_correction": len(rows),
        "conditional_lower_bound": lower, "budget_5fps_100mhz": 20000000,
        "excess": lower-20000000, "model_changed": False}
    assert len(rows)==67 and lower>20000000
    (ROOT / "layer_budget.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(totals, "lower", lower, "excess", result["excess"])


if __name__ == "__main__":
    main()
