"""仅为本批一次诊断综合建立直接接线顶层；不改变客户或冻结算术。"""
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import run

sys.path.insert(0, str(run.SKILL))
from scripts.python.quality.formatter_ast import build_ast_report_for_text


def main():
    target = ROOT/"rtl/road_feature_workstore_top.v"
    if target.exists() and "--spec" not in sys.argv and "--repair" not in sys.argv:
        raise ValueError("preserve previous diagnostic top")
    source = ROOT/"rtl/road_feature_blocks_client.v"
    ast = build_ast_report_for_text(source.read_text(encoding="utf-8"), source_path=source)
    assert ast["summary"]["parse_errors"] == 0 and len(ast["modules"]) == 1
    ports = ast["modules"][0]["ports"]
    core = dict(i_input_valid="o_core_valid", i_first="o_core_first", i_last="o_core_last",
        i_lane_mask="o_core_input_mask", i_activation_data="o_core_activation", i_weight_data="o_core_weight",
        i_bias_data="o_core_bias", i_output_mask="o_core_output_mask", i_tags="o_core_tags",
        i_addresses="o_core_addresses", i_pre_multipliers="o_core_pre_multiplier", i_pre_shifts="o_core_pre_shift",
        i_post_multiplier="o_core_post_multiplier", i_post_shift="o_core_post_shift", i_residual="o_core_residual",
        i_bypass_data="o_core_bypass", i_output_ready="o_core_output_ready", o_input_ready="i_core_ready",
        o_output_valid="i_core_output_valid", o_output_data="i_core_output_data", o_output_tag="i_core_output_tag",
        o_output_address="i_core_output_address", o_output_sum="i_core_output_sum", o_fault="i_core_fault")
    store_ports = [port for port in ports if port["name"].startswith(("i_byte_", "o_byte_", "i_weight_", "o_weight_"))]
    assert len(store_ports) == 18
    internal = {port["name"] for port in store_ports} | set(core.values()) | {"i_table_loaded"}
    external = [port for port in ports if port["name"] not in internal]
    assert len(set(core.values())) == len(core)
    if "--spec" in sys.argv:
        specs = []
        for port in external:
            width = port["width"]
            high, low = map(int, width[1:-1].split(":")) if width else (0, 0)
            specs.append(dict(name=port["name"], direction=port["direction"], width=abs(high-low)+1,
                              role="native", description=port["comment"] or "原客户同名端口直通"))
        for name, direction, width, description in (
            ("i_table_valid", "input", 1, "原owner装表有效"), ("i_table_addr", "input", 10, "共享SiLU表地址"),
            ("i_table_data", "input", 16, "同包Q7.8表项"), ("o_table_ready", "output", 1, "实际表项接受"),
            ("o_table_loaded", "output", 1, "1024项已装满许可")):
            specs.append(dict(name=name, direction=direction, width=width, role="native", description=description))
        contract = dict(name="physical_workstore_diagnostic", modules=[dict(name=target.stem,
            rtl_path="rtl/"+target.name, clock=dict(name="i_clk", edge="posedge", frequency_mhz=100),
            reset=dict(name="i_rstn", active="low", synchronous=False), interfaces=dict(ports=specs),
            behavior=["实际固定feature客户、唯一WIF1仓及冻结算术owner直接接线", "全部数据接口外露且无常量测试数据替代运算路径",
                      "共同reset且SiLU重新装表后才接任务；故障合并不掩盖", "仅诊断综合，不是板级引脚或整网顶层"],
            constraints=["100MHz同域，无新增时序例外", "共享仓4ERAM由实际综合确认，原核II/数值/复位不变", "只诊断综合，不运行布局布线或位流"],
            corner_cases=["byte/weight响应等待和背压", "共同复位取消旧响应，工作内容重新覆盖", "SPPF池化不经过MAC"],
            verification_cases=["与回归TB相同client/workstore/core源闭包和端口映射", "综合硬RAM及算术路径实际保留检查"],
            timing_diagrams=[dict(id="workstore", title="请求到真实提交后响应", scenario="native_store",
                description="具体周期以厂商模型测量为准；核心II不变",
                wavejson=dict(signal=[dict(name="i_clk", wave="p......"), dict(name="start", wave="010...."),
                    dict(name="native_access", wave="0..1..."), dict(name="response", wave="0...10."),
                    dict(name="core_valid", wave="0.....1")]))])])
        path = ROOT/"diagnostic_contract.json"
        content = json.dumps(contract, ensure_ascii=False, indent=2)
        print_patch(path, content)
        return
    declarations = [f'    {port["direction"]} {port["width"]} {port["name"]}' for port in external]
    declarations += ["    input i_table_valid", "    input [9:0] i_table_addr", "    input signed [15:0] i_table_data",
                     "    output o_table_ready", "    output o_table_loaded"]
    lines = ["`timescale 1ns / 1ps", "// 直接接线诊断顶层：真实feature客户、唯一4ERAM工作仓及原算术owner。",
             "// 仅综合资源观察，不是板级I/O顶层、DDR闭环或时序签核。", "module road_feature_workstore_top(",
             ",\n".join(declarations), ");"]
    for port in ports:
        if port["name"] in internal:
            lines.append(f'    wire {port["width"]} link_{port["name"]}; // 同域内部直连接口')
    lines += ["    wire flag_client_fault; // 客户故障",
              "    wire flag_store_fault; // 物理仓越界故障",
              "    assign o_fault = flag_client_fault | flag_store_fault | link_i_core_fault; // 不隐去任一所有者故障",
              "    assign o_table_loaded = link_i_table_loaded; // 实际全表装满状态"]
    mappings = []
    for port in ports:
        name = port["name"]
        actual = "flag_client_fault" if name == "o_fault" else ("link_"+name if name in internal else name)
        mappings.append(f"        .{name}({actual})")
    lines += ["    road_feature_blocks_client client_Inst(", ",\n".join(mappings), "    );"]
    mappings = ["        .i_clk(i_clk)", "        .i_rstn(i_rstn)", "        .o_fault(flag_store_fault)"]
    for port in store_ports:
        name = port["name"]
        counterpart = ("o_" if name.startswith("i_") else "i_")+name[2:]
        mappings.append(f"        .{counterpart}(link_{name})")
    lines += ["    road_feature_workstore workstore_Inst(", ",\n".join(mappings), "    );"]
    mappings = ["        .i_clk(i_clk)", "        .i_rstn(i_rstn)", "        .i_input_fault(1'b0)",
                "        .i_table_valid(i_table_valid)", "        .i_table_addr(i_table_addr)",
                "        .i_table_data(i_table_data)", "        .o_table_ready(o_table_ready)",
                "        .o_table_loaded(link_i_table_loaded)"]
    mappings += [f"        .{name}(link_{other})" for name, other in core.items()]
    lines += ["    road_csp_first_probe arithmetic_Inst(", ",\n".join(mappings), "    );", "endmodule", ""]
    # 生成仅接线资产；调用者保持apply_patch是唯一源文件写入口。
    print_patch(target, "\n".join(lines))


def print_patch(path, content):
    sections = ["*** Begin Patch"]
    if path.exists():
        assert "--repair" in sys.argv, "preserve previous asset"
        old = path.read_text(encoding="utf-8")
        snapshot = ROOT/"failed_spec_sources"/path.name
        assert not snapshot.exists(), "preserve previous failed input"
        sections += ["*** Add File: "+snapshot.as_posix(), *["+"+line for line in old.splitlines()]]
        sections += ["*** Update File: "+path.as_posix(), "@@", *["-"+line for line in old.splitlines()]]
    else:
        sections += ["*** Add File: "+path.as_posix()]
    sections += [*["+"+line for line in content.splitlines()], "*** End Patch"]
    print("\n".join(sections))


if __name__ == "__main__":
    main()
