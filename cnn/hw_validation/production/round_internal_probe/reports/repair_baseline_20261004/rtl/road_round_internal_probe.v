`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     road_round_internal_probe
// Module Name:     road_round_internal_probe
// Description:     description/road_round_internal_probe_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_round_internal_probe
//
// Referrences:
// File Format      File Name
// 1.Book           road_round_internal_probe.contract.json
//
// Dependencies:
// Module Name      Version
//
// Version:         V1.0
// Revision Date:   2026/10/04 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/04       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月04日
// 设计名称:        road_round_internal_probe
// 模块名称:        road_round_internal_probe
// 模块说明:        Description/road_round_internal_probe_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_round_internal_probe
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_round_internal_probe.contract.json
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026/10/04       V1.0        Erie              创建文件

module road_round_internal_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 探针与舍入流水工作时钟
	input i_rstn,                               // 外部异步低有效复位

	//----------------RESULT接口----------------//

	//RESULT接口
	output o_result_valid,                      // 下游边界本拍接收结果
	output [15:0]o_result_data,                 // 下游边界接收数值位型
	output [15:0]o_result_tag,                  // 下游边界接收源身份
	output o_result_fault,                      // 下游边界接收故障标志
	output [63:0]o_checksum,                    // 已消费结果令牌异或校验
	output o_error,                             // 故障标志与源序列不一致
	output [15:0]o_result_count                 // 已纳入校验的结果数
);

	//--------------模块实例化信号--------------//
	//road_round_reset_gen--RESET接口
	//road_round_internal_probe_core--全局信号
	wire wire_core_rstn;                        // 两拍同步释放的功能复位

	//-----------------输出信号-----------------//
	//RESULT接口
	wire result_valid_o;                         // 功能核心结果有效桥
	wire [15:0]result_data_o;                   // 功能核心结果数值桥
	wire [15:0]result_tag_o;                    // 功能核心结果身份桥
	wire result_fault_o;                         // 功能核心故障标志桥
	wire [63:0]checksum_o;                       // 功能核心动态摘要桥
	wire error_o;                                // 功能核心协议错误桥
	wire [15:0]cnt_result_o;                     // 功能核心结果计数桥

	//---------------输出信号连线---------------//
	//RESULT接口
	assign o_result_valid = result_valid_o;     // 发布功能核心结果有效
	assign o_result_data = result_data_o;       // 发布功能核心结果数值
	assign o_result_tag = result_tag_o;         // 发布功能核心结果身份
	assign o_result_fault = result_fault_o;     // 发布功能核心故障标志
	assign o_checksum = checksum_o;             // 发布功能核心动态摘要
	assign o_error = error_o;                   // 发布功能核心协议错误
	assign o_result_count = cnt_result_o;       // 发布功能核心结果计数

	//--------------模块实例化区域--------------//
	// 独立复位发生器限定外部异步复位只到两个同步触发器。
	road_round_reset_gen road_round_reset_gen_Inst_release( // 实例化两级复位释放器
		.i_clk(i_clk),                          // 使用唯一工作时钟
		.i_rstn(i_rstn),                        // 接收外部异步低有效复位
		.o_rstn(wire_core_rstn)                 // 输出同步释放功能复位
	);

	// 功能核心只把复位当作模块输入，不在内部生成复位。
	road_round_internal_probe_core road_round_internal_probe_core_Inst_datapath( // 实例化探针功能核心
		.i_clk(i_clk),                          // 使用唯一工作时钟
		.i_rstn(wire_core_rstn),                // 接收同步释放功能复位
		.o_result_valid(result_valid_o),        // 发布逐令牌结果有效
		.o_result_data(result_data_o),          // 发布舍入结果位型
		.o_result_tag(result_tag_o),            // 发布源身份
		.o_result_fault(result_fault_o),        // 发布非法移位标志
		.o_checksum(checksum_o),                // 发布动态结果摘要
		.o_error(error_o),                      // 发布协议错误锁存
		.o_result_count(cnt_result_o)           // 发布已消费结果数量
	);

endmodule
