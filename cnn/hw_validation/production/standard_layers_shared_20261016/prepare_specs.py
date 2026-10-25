"""标准tile客户接口与空间打包参考；仅stdlib，不训练或分配物理工作仓。"""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = {
    "i_clk": 1, "i_rstn": 1, "i_cancel": 1, "i_start_valid": 1,
    "i_layer_id": 7, "i_tile_y": 6, "i_tile_x": 7, "i_table_loaded": 1,
    "i_parameter_ready": 1, "i_parameter_rsp_valid": 1,
    "i_parameter_rsp_layer": 7, "i_parameter_rsp_channel": 7,
    "i_parameter_rsp_window": 3, "i_parameter_rsp_group": 5,
    "i_parameter_weight": 192, "i_parameter_quant": 248, "i_parameter_error": 1,
    "i_read_ready": 1, "i_read_rsp_valid": 1, "i_read_rsp_address": 32,
    "i_read_rsp_data": 128, "i_read_error": 1, "i_write_ready": 1,
    "i_barrier_ready": 1, "i_barrier_layer": 7, "i_barrier_tile_y": 6, "i_barrier_tile_x": 7,
    "i_byte_req_ready": 1, "i_byte_rsp_valid": 1, "i_byte_rsp_data": 8, "i_byte_rsp_error": 1,
    "i_weight_req_ready": 1, "i_weight_rsp_valid": 1, "i_weight_rsp_data": 192, "i_weight_rsp_error": 1,
    "i_work_fault": 1, "i_core_ready": 1, "i_core_output_valid": 1,
    "i_core_output_tag": 16, "i_core_output_address": 32, "i_core_output_data": 8, "i_core_fault": 1,
}
OUTPUTS = {
    "o_start_ready": 1, "o_busy": 1, "o_done": 1, "o_fault": 1,
    "o_layer_id": 7, "o_tile_y": 6, "o_tile_x": 7,
    "o_parameter_valid": 1, "o_parameter_channel": 7, "o_parameter_window": 3,
    "o_parameter_group": 5, "o_parameter_rsp_ready": 1,
    "o_read_valid": 1, "o_read_address": 32, "o_read_rsp_ready": 1,
    "o_write_valid": 1, "o_write_address": 32, "o_write_data": 8,
    "o_barrier_valid": 1, "o_byte_req_valid": 1, "o_byte_req_write": 1,
    "o_byte_req_addr": 12, "o_byte_req_data": 8, "o_byte_rsp_ready": 1,
    "o_weight_req_valid": 1, "o_weight_req_write": 1, "o_weight_req_group": 5,
    "o_weight_req_data": 192, "o_weight_rsp_ready": 1,
    "o_core_valid": 1, "o_core_first": 1, "o_core_last": 1, "o_core_input_mask": 8,
    "o_core_activation": 64, "o_core_weight": 192, "o_core_bias": 96,
    "o_core_output_mask": 3, "o_core_tags": 48, "o_core_addresses": 96,
    "o_core_pre_multiplier": 96, "o_core_pre_shift": 18,
    "o_core_post_multiplier": 32, "o_core_post_shift": 6, "o_core_output_ready": 1,
}


def dw_cache_index(row, tail, group, lane):
    """21/9输入并集对应单通道9x9仓；尾点在第六输入列起始。"""
    sample = group * 8 + lane
    width = 3 if tail else 7
    return (row * 2 + sample // width) * 9 + (6 if tail else 0) + sample % width


def self_test():
    """对独立直接3x3窗口核验稀疏三输出权重的坐标覆盖。"""
    for row in range(4):
        for tail in (False, True):
            width = 3 if tail else 7
            count = 3 * width
            slots = [dw_cache_index(row, tail, n // 8, n % 8) for n in range(count)]
            assert len(set(slots)) == count and all(0 <= n < 81 for n in slots)
            for output in range(1 if tail else 3):
                selected = [slots[n] for n in range(count) if output * 2 <= n % width < output * 2 + 3]
                x = 6 if tail else output * 2
                direct = [(row * 2 + ky) * 9 + x + kx for ky in range(3) for kx in range(3)]
                assert selected == direct
    assert max(16 * cin for cin in (24, 48)) <= 3072


def main():
    self_test()
    path = HERE.parent / "shared_lut_service_1fps_20261015/reference.py"
    module = importlib.util.spec_from_file_location("spec_helper", path)
    helper = importlib.util.module_from_spec(module)
    module.loader.exec_module(helper)
    contract = {"inputs": INPUTS, "outputs": OUTPUTS,
                "verification": json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))["verification"]}
    signals = [{"name": "i_clk", "wave": "p..........."},
               {"name": "start_valid", "wave": "010........."},
               {"name": "byte_write_req", "wave": "0.1.0......."},
               {"name": "byte_write_rsp", "wave": "0....10....."},
               {"name": "weight_read_req", "wave": "0.....10...."},
               {"name": "weight_read_rsp", "wave": "0.......10.."},
               {"name": "core_valid", "wave": "0........1.0"},
               {"name": "core_ready", "wave": "0.........10"}]
    spec = helper.specification("road_standard_tile_client", contract, [
        "锁存固定graph层与对齐tile；一任务覆盖真实有效行和全部输出通道，不冒充整层。",
        "先完整覆盖WIF1 byte/weight使用范围，所有写响应退休后再读。DW逐通道81B，PW16*Cin。",
        "每组先同步读weight响应，再逐byte组装activation；发射保持至核ready；偏置仅first有效。",
        "输出逐tag核验mask、地址与唯一性；全部真实写接受后再发barrier；barrier身份核验后done。",
        "cancel/fault占有直到共同reset；不允许借此切owner或宣称DDR已排空。"
    ], signals)
    spec["clock_reset"] = {"clock": "i_clk 100MHz rising edge", "reset": "i_rstn async assert, two-edge sync release; all services common reset"}
    spec["constraints"] += ["C4独占工作仓实现；本客户无私有tile/weight数组", "首批仅INT8四层，不含INT16预测头或物理时序"]
    for name, value in (("ports.json", contract), ("spec_input.json", spec)):
        (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SCHEDULE_REFERENCE_PASS dw_union21_tail9 cache81 ports=" + str(len(INPUTS) + len(OUTPUTS)))


if __name__ == "__main__":
    main()
