"""固定31卷积层逐tile指令参考，无算术/存储或训练。"""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRODUCTION = ROOT.parent


def main():
    layers = json.loads((PRODUCTION / "rom_two_client_20261015/remaining_layers.json").read_text(encoding="utf-8"))["layers"]
    jobs = []
    for layer in layers:
        height, width, _ = layer["output_shape_hwc"]
        positions = [(y, x) for y in range(0, height, 4) for x in range(0, width, 4)]
        assert width % 4 == 0 and height in (18, 36, 72)
        for index, (y, x) in enumerate(positions):
            jobs.append({"layer": layer["graph_index"], "y": y, "x": x, "last": index == len(positions) - 1, "valid_rows": min(4, height - y)})
    assert len(layers) == 31 and len(jobs) == 6240
    (HERE / "jobs22.hex").write_text("".join(f"{(int(row['last'])<<21)|(row['layer']<<14)|(row['y']<<7)|row['x']:06x}\n" for row in jobs), encoding="ascii")
    (HERE / "layers.json").write_text(json.dumps(layers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    inputs = {"i_clk": 1, "i_rstn": 1, "i_cancel": 1, "i_start_valid": 1, "i_layer_id": 7,
              "i_tile_start_ready": 1, "i_tile_done": 1, "i_tile_fault": 1}
    outputs = {"o_start_ready": 1, "o_busy": 1, "o_done": 1, "o_fault": 1,
               "o_tile_start_valid": 1, "o_layer_id": 7, "o_tile_y": 7, "o_tile_x": 7}
    helper_path = PRODUCTION / "shared_lut_service_1fps_20261015/reference.py"
    module = importlib.util.spec_from_file_location("spec_helper", helper_path)
    helper = importlib.util.module_from_spec(module)
    module.loader.exec_module(helper)
    spec = helper.specification("road_standard_layer_sequence", {"inputs": inputs, "outputs": outputs}, [
        "start握手锁存31个固定节点之一；形状case来自冻结graph，不接受任意外部H/W。",
        "逐tile发起并等待真实客户端done；客户端done契约要求全部未决消费且写屏障通过。",
        "x先增4，行尾y增4；最后tile done后整层done；受控端点只证明调度，不是整层计算。",
        "故障/cancel保持owner至共同reset，不以固定等待替代退休。"
    ], [{"name": "i_clk", "wave": "p.........."}, {"name": "tile_start_valid", "wave": "01..0....10"},
        {"name": "tile_start_ready", "wave": "0..10....10"}, {"name": "tile_done", "wave": "0......10.."}])
    (HERE / "spec_input.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("LAYER_SEQUENCE_REFERENCE_PASS layers=31 tiles=6240")


if __name__ == "__main__":
    main()
