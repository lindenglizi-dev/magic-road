`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/07 00:00:00
// Design Name:     road_low_io_reset_shell
// Module Name:     road_low_io_reset_shell
// Description:     road_low_io_reset_shell_spec.md
// Simulations:     modelsim_reset_run.log
//
// Referrences:
// File Format      File Name
// 1.Book           road_low_io_reset_shell.contract.json
//
// Dependencies:
// Module Name                    Version
// road_low_io_physical_shell     V1.0
//
// Version:         V1.0
// Revision Date:   2026/10/07 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/07       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月07日
// 设计名称:        road_low_io_reset_shell
// 模块名称:        road_low_io_reset_shell
// 模块说明:        road_low_io_reset_shell_spec.md
// 仿真工程:        modelsim_reset_run.log
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_low_io_reset_shell.contract.json
//
// 依赖文件:
// 模块名称                       版本
// road_low_io_physical_shell     V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月07日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月07日   V1.0        Erie              创建文件

module road_low_io_reset_shell
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 一百兆诊断时钟
	input i_rstn,                               // 异步低有效外部复位

	//------------------RX接口------------------//
	input i_rx_valid,                           // 外部十六位接收有效
	input [15:0]i_rx_data,                      // 外部命令或负载数据
	output o_rx_ready,                          // 释放完成后的接收许可

	//------------------TX接口------------------//
	output o_tx_valid,                          // 释放完成后的发送有效
	output [15:0]o_tx_data,                     // 旧壳响应数据直通
	input i_tx_ready                            // 外部响应接收许可
);

	//--------------寄存器信号----------------//
	//两级异步断言同步释放链
	reg reg_release_meta = 1'b0;               // 仅由末级采样的第一级
	reg reg_release_done = 1'b0;               // 驱动旧壳复位的第二级

	//------------模块实例化信号------------//
	//旧三十八位物理壳连接
	wire shell_rx_ready;                       // 旧壳内部接收许可
	wire shell_tx_valid;                       // 旧壳内部发送有效
	wire [15:0]shell_tx_data;                  // 旧壳内部发送数据
	wire shell_rstn;                           // 末级寄存器派生的核复位
	wire shell_rx_valid;                       // 开放窗口内的接收有效
	wire shell_tx_ready;                       // 开放窗口内的发送许可

	//-----------------标志信号-----------------//
	//外部接口屏蔽条件
	wire flag_interface_open;                  // 外部复位高且两级释放完成

	//---------------其他信号连线---------------//
	//核复位与外部握手屏蔽
	assign shell_rstn = reg_release_done;      // 不增加组合复位路径
	assign flag_interface_open = i_rstn & reg_release_done; // 异步断言期立即屏蔽接口
	assign shell_rx_valid = i_rx_valid & flag_interface_open; // 等待期不向旧壳发布数据
	assign shell_tx_ready = i_tx_ready & flag_interface_open; // 等待期不消费旧壳响应

	//---------------输出信号连线---------------//
	//外部仅在同步释放后观察交易
	assign o_rx_ready = shell_rx_ready & flag_interface_open; // 复位与等待期强制为零
	assign o_tx_valid = shell_tx_valid & flag_interface_open; // 复位与等待期强制为零
	assign o_tx_data = shell_tx_data;           // 无效期数据不构成交易

	//-----------主要任务处理区域-----------//
	//第一级只采样外部释放
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release_meta <= 1'b0;              // 外部断言时异步清零
		end else begin
			reg_release_meta <= 1'b1;              // 首个上升沿记录释放
		end
	end

	//第二级仅采样第一级且驱动旧壳
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release_done <= 1'b0;              // 外部断言时异步清零
		end else begin
			reg_release_done <= reg_release_meta; // 第二个上升沿完成释放
		end
	end

	//----------------模块实例化----------------//
	//旧物理壳及其冻结计算链保持原文
	road_low_io_physical_shell road_low_io_physical_shell_Inst_reset(
		.i_clk(i_clk),                          // 共用一百兆时钟
		.i_rstn(shell_rstn),                    // 仅由同步释放末级驱动
		.i_rx_valid(shell_rx_valid),            // 屏蔽窗口外的旧接收帧
		.i_rx_data(i_rx_data),                  // 保持原十六位数据格式
		.o_rx_ready(shell_rx_ready),            // 旧壳接收许可
		.o_tx_valid(shell_tx_valid),            // 旧壳发送有效
		.o_tx_data(shell_tx_data),              // 旧壳发送数据
		.i_tx_ready(shell_tx_ready)             // 屏蔽窗口外的消费请求
	);

endmodule
