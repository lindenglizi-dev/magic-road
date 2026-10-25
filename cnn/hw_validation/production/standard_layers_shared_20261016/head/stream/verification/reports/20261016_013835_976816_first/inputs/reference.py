"""固定预测张量读取地址与HWC7顺序参考；仅stdlib。"""

import ast
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parents[2]
INPUTS = {"i_clk": 1, "i_rstn": 1, "i_cancel": 1, "i_start_valid": 1,
          "i_start_frame_token": 32, "i_start_model_id": 32, "i_predictions_committed": 1,
          "i_read_ready": 1, "i_read_rsp_valid": 1, "i_read_rsp_address": 32,
          "i_read_rsp_data": 128, "i_read_error": 1, "i_cell_ready": 1}
OUTPUTS = {"o_start_ready": 1, "o_busy": 1, "o_done": 1, "o_fault": 1,
           "o_read_valid": 1, "o_read_address": 32, "o_read_rsp_ready": 1,
           "o_cell_valid": 1, "o_cell_data": 112, "o_cell_id": 14,
           "o_cell_frame_token": 32, "o_cell_model_id": 32}
SCALES = [(72, 128, 61919232, 60997632, "head2"),
          (36, 64, 62578688, 62345216, "head3"),
          (18, 32, 62771200, 62701568, "head4")]


def field_address(scale, y, x, field):
    _, width, reg_base, cls_base, _ = SCALES[scale]
    channels, channel, base = (5, field, reg_base) if field < 5 else (2, field - 5, cls_base)
    return base + ((((y // 4) * (width // 4) + x // 4) * 16 + (y % 4) * 4 + x % 4) * channels + channel) * 2


def main():
    graph = json.loads((PRODUCTION / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    path = PRODUCTION / "graph.py"
    function = next(node for node in ast.parse(path.read_text(encoding="utf-8")).body if isinstance(node, ast.FunctionDef) and node.name == "resolve_byte_address")
    namespace = {"math": math, "Any": object}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), namespace)
    cells = fields = 0
    for scale, (height, width, _, _, name) in enumerate(SCALES):
        for y in range(height):
            for x in range(width):
                for field in range(7):
                    tensor, channel = (name + ".reg_out", field) if field < 5 else (name + ".cls_out", field - 5)
                    actual = field_address(scale, y, x, field)
                    assert actual == namespace["resolve_byte_address"](graph, tensor, y, x, channel)
                    assert actual % 2 == 0 and actual % 16 <= 14
                    fields += 1
                cells += 1
    assert (cells, fields) == (12096, 84672)
    helper_path = PRODUCTION / "shared_lut_service_1fps_20261015/reference.py"
    module = importlib.util.spec_from_file_location("spec_helper", helper_path)
    helper = importlib.util.module_from_spec(module)
    module.loader.exec_module(helper)
    contract = {"inputs": INPUTS, "outputs": OUTPUTS,
                "verification": json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))["verification"]}
    spec = helper.specification("road_head_cell_stream", contract, [
        "仅全部预测写可见且start握手才锁定token/model，依次读取六个固定INT16张量。",
        "一未决128位读，全地址核验后才填行寄存器；每字段均偶数地址，不跨16字节行。",
        "一个112位cell寄存器，字段0..4回归、5..6分类，12096个cell按S4/S8/S16和逐行序发布。",
        "cell背压保持完整数据/编号/上下文；最后cell实际消费后done；故障与cancel保留owner到共同reset。"
    ], [{"name": "i_clk", "wave": "p..........."}, {"name": "read_valid", "wave": "01..0......."},
        {"name": "read_ready", "wave": "0..10......."}, {"name": "read_rsp_valid", "wave": "0....10....."},
        {"name": "cell_valid", "wave": "0.......1..0"}, {"name": "cell_ready", "wave": "0.........10"}])
    for name, value in (("ports.json", contract), ("spec_input.json", spec), ("reference_receipt.json", {"status": "PASS", "cells": cells, "fields": fields, "full_plane_producer_executed": False})):
        (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"HEAD_STREAM_REFERENCE_PASS cells={cells} fields={fields}")


if __name__ == "__main__":
    main()
