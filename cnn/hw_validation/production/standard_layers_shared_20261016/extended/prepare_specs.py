"""固定六层视图寻址参考与十层候选规格；不复制物理缓存。"""

import ast
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parents[1]


def source_address(layer, y, x, channel, graph):
    node = graph["nodes"][layer]
    width, channels = node["input_shape_hwc"][1:]
    views = {55: (24, 58331136, 48, 58499072, 24),
             64: (12, 58613760, 24, 58945536, 12),
             73: (24, 59224064, 48, 59392000, 24)}
    if layer in views:
        half, left, parent_channels, right, right_channels = views[layer]
        base = left if channel < half else right
        channels = parent_channels if channel < half else right_channels
        channel = channel if channel < half else channel - half
    else:
        parent = next(row for row in graph["nodes"] if row.get("output") == node["inputs"][0])
        base = parent["storage"]["base"]
    return base + (((y // 4) * (width // 4) + x // 4) * 16 + (y % 4) * 4 + x % 4) * channels + channel


def main():
    graph = json.loads((PRODUCTION / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    # 只执行既有stdlib地址函数的原AST节点，避免为地址参考导入torch或生成新图。
    path = PRODUCTION / "graph.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "resolve_byte_address")
    namespace = {"math": math, "Any": object}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), namespace)
    checked = 0
    for layer in (46, 55, 64, 65, 73, 74):
        node = graph["nodes"][layer]
        height, width, channels = node["input_shape_hwc"]
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1), (height // 2, width // 2)):
            for channel in range(channels):
                assert source_address(layer, y, x, channel, graph) == namespace["resolve_byte_address"](graph, node["inputs"][0], y, x, channel)
                checked += 1
    base_spec = json.loads((HERE.parent / "spec_input.json").read_text(encoding="utf-8"))
    base_spec["behavior"] += ["十层固定case候选，base四层保持；Cin96需要12权重组和1536字节完整覆盖。", "三个concat输入按原graph视图选择两个物理存储，不物化拼接，不重复做残差加法。"]
    base_spec["verification_cases"] += ["六层新增代表tile与虚拟concat物理地址对拍", "1536字节索引及12组权重不截断"]
    for name, value in (("spec_input.json", base_spec), ("address_reference.json", {"status": "PASS", "coordinates_checked": checked, "source": "graph.resolve_byte_address original AST", "physical_or_layer_execution": False})):
        (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"FIXED_VIEW_ADDRESS_REFERENCE_PASS checked={checked}")


if __name__ == "__main__":
    main()
