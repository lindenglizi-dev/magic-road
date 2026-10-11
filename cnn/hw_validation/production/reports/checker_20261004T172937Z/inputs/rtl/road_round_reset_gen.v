`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     road_round_reset_gen
// Module Name:     road_round_reset_gen
// Description:     description/road_round_reset_gen_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_round_reset_gen
//
// Referrences:
// File Format      File Name
// 1.Book           road_round_reset_gen.contract.json
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
// 设计名称:        road_round_reset_gen
// 模块名称:        road_round_reset_gen
// 模块说明:        Description/road_round_reset_gen_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_round_reset_gen
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_round_reset_gen.contract.json
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

module road_round_reset_gen
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 复位释放同步时钟
	input i_rstn,                               // 外部异步低有效复位

	//----------------RESET接口-----------------//
	output o_rstn                               // 两拍同步释放低有效复位
);

	//----------------寄存器信号----------------//
	reg reg_reset_meta = 1'd0;                  // 复位释放同步第一拍
	reg reg_reset_release = 1'd0;               // 复位释放同步第二拍

	//-----------------输出信号-----------------//
	//RESET接口
	wire rstn_o;                                // 同步释放复位输出桥

	//---------------其他信号连线---------------//
	//其他信号连线
	//RESET接口
	assign rstn_o = reg_reset_release;          // 发布第二拍同步电平

	//---------------输出信号连线---------------//
	//RESET接口
	assign o_rstn = rstn_o;                     // 连接功能复位端口

	//-------------主要任务处理区域-------------//
	// 第一拍允许外部复位异步拉低，解除只发生在时钟边沿。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_reset_meta <= 1'd0;             // 异步进入复位
		end else begin
			reg_reset_meta <= 1'd1;             // 同步传递释放电平
		end
	end

	// 第二拍形成全部功能寄存器使用的复位树根。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_reset_release <= 1'd0;          // 异步保持功能复位
		end else begin
			reg_reset_release <= reg_reset_meta; // 第二拍同步释放
		end
	end

endmodule
