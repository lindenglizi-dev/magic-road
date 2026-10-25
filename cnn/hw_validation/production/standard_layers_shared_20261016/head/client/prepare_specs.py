"""固定31层应用接口与空间窗口参考，无训练/新图/物理仓。"""

import ast
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCTION = ROOT.parent


def main():
    contract = json.loads((ROOT / "ports.json").read_text(encoding="utf-8"))
    for direction, name in (("inputs", "i_tile_y"), ("inputs", "i_barrier_tile_y"), ("outputs", "o_tile_y")):
        contract[direction][name] = 7
    contract["inputs"]["i_core_output_data"] = 16
    contract["inputs"]["i_core_output_int16"] = 1
    contract["outputs"]["o_write_data"] = 16
    contract["outputs"]["o_write_int16"] = 1
    contract["outputs"]["o_core_activate"] = 1
    # 固定stride1/2的独立直接窗口坐标覆盖，检查每一输出三点及单点。
    for stride in (1, 2):
        edge, union_width = 3 * stride + 3, 2 * stride + 3
        for row in range(4):
            for tail in (False, True):
                width = 3 if tail else union_width
                slots = [(row * stride + n // width) * edge + (3 * stride if tail else 0) + n % width for n in range(3 * width)]
                assert max(slots) < edge * edge and len(set(slots)) == len(slots)
                for lane in range(1 if tail else 3):
                    filtered = [slots[n] for n in range(3 * width) if lane * stride <= n % width < lane * stride + 3]
                    x = 3 * stride if tail else lane * stride
                    assert filtered == [(row * stride + ky) * edge + x + kx for ky in range(3) for kx in range(3)]
    for cout in (2, 5, 24, 48, 96):
        assert sum(min(3, cout - channel) for channel in range(0, cout, 3)) == cout
    graph = json.loads((PRODUCTION / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    source = PRODUCTION / "graph.py"
    function = next(node for node in ast.parse(source.read_text(encoding="utf-8")).body if isinstance(node, ast.FunctionDef) and node.name == "resolve_byte_address")
    namespace = {"math": math, "Any": object}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)
    checked = 0
    for layer, half, left, left_c, right in ((82, 12, 58613760, 24, 58945536), (90, 24, 59224064, 48, 59392000), (98, 48, 59543552, 96, 59637760)):
        node = graph["nodes"][layer]
        height, width, channels = node["input_shape_hwc"]
        assert channels == 2 * half
        for y, x in ((0, 0), (height - 1, width - 1), (height // 2, width // 2)):
            for channel in range(channels):
                base, physical_c, c = (left, left_c, channel) if channel < half else (right, half, channel - half)
                actual = base + (((y // 4) * (width // 4) + x // 4) * 16 + (y % 4) * 4 + x % 4) * physical_c + c
                assert actual == namespace["resolve_byte_address"](graph, node["inputs"][0], y, x, channel)
                checked += 1
    spec = json.loads((ROOT / "extended/spec_input.json").read_text(encoding="utf-8"))
    ports = spec["interfaces"]["ports"]
    for port in ports:
        direction = "inputs" if port["direction"] == "input" else "outputs"
        port["width"] = contract[direction][port["name"]]
    for name, direction in (("i_core_output_int16", "input"), ("o_write_int16", "output"), ("o_core_activate", "output")):
        ports.append({"name": name, "direction": direction, "width": 1, "role": name[2:], "description": "预测头原始INT16模式与实际写回类型，首组冻结后保持", "clock_domain": "i_clk"})
    spec["behavior"] += ["31固定卷积可选；stride1 DW并集15与末点9，分别四槽权重；输出H72/W128。", "六预测卷积INT16 pre-only；cls2/reg5尾mask只启用真实输出，输出写宽16+类型且字节地址乘二。"]
    for name, value in (("ports.json", contract), ("spec_input.json", spec), ("reference_check.json", {"status": "PASS", "head_stem_address_coordinates": checked, "dw_stride": [1, 2], "physical_execution": False})):
        (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"HEAD_APPLICATION_REFERENCE_PASS addresses={checked} stride1_union15 stride2_union21")


if __name__ == "__main__":
    main()
