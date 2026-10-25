`timescale 1ns / 1ps

// Company: RoadYOLO
// Engineer: C8
// Create Date: 2026-10-16
// Design Name: Fixed line-event boxes and result age
// Module Name: road_box_age_overlay
// Description: Two registered video stages with a final live-invalid color mask.
// Simulations: ../tests
// Referrences: ../interfaces.json
// Dependencies: road_box_line_overlay, frozen road_age_overlay
// Version: V1.0
// Revision Date: 2026-10-16
// History: Create file
// 版权归属: RoadYOLO
// 开发人员: C8
// 创建日期: 2026-10-16
// 设计名称: 行事件框与结果年龄合成
// 模块名称: road_box_age_overlay
// 模块说明: 两拍视频寄存保持对齐，实时失效屏蔽已排队框色
// 仿真工程: ../tests
// 参考资料: ../interfaces.json
// 依赖文件: 行事件框模块与冻结年龄文字模块
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 创建文件
module road_box_age_overlay (
	input         i_clk,                   // 既有HDMI像素时钟
	input         i_rstn,                  // 已同步释放的像素域共同复位
	input         i_sof,                   // 与活动表切换共用的消隐帧边界
	input         i_vsync,                 // mixer输出的原VS
	input         i_hsync,                 // mixer输出的原HS
	input         i_de,                    // mixer输出的原有效区
	input  [23:0] i_rgb,                   // 文字与框之外保留的原颜色
	input         i_table_active_valid,    // 完整活动表存在，包括正常空表
	input  [6:0]  i_table_count,           // 未截断的活动框数，合法零至64
	input  [96:0] i_table_entry,           // 原表唯一异步读口的数据
	input         i_table_draw_valid,      // 实时身份、时间及年龄绘制许可
	input  [63:0] i_age_upper_ms,          // 原表保守年龄，未知为全一
	output [5:0]  o_table_read_index,      // 行消隐扫描的唯一原表读地址
	output        o_vsync,                 // 与最终RGB等延迟两拍
	output        o_hsync,                 // 与最终RGB等延迟两拍
	output        o_de,                    // 与最终RGB等延迟两拍
	output [23:0] o_rgb,                   // AGE优先、实时许可失效不留排队框色
	output        o_line_ready,            // 当前行端点事件图已完整准备
	output        o_prepare_busy,          // 只准备行事件，不反压视频
	output [8:0]  o_last_prepare_cycles,   // 最近一次行扫描周期，不含SOF全清
	output        o_fault                  // 行准备/格式或计数协议异常保持
);
	//------------模块实例化信号------------//
	// 框层与文字层各只有一个视频寄存边界。
	wire [23:0] wire_box_rgb;              // 框层一拍颜色
	wire wire_box_vsync;                  // 框层一拍VS
	wire wire_box_hsync;                  // 框层一拍HS
	wire wire_box_de;                     // 框层一拍DE
	wire wire_box_sof;                    // 框层一拍消隐边界，供文字对齐
	wire [23:0] wire_age_rgb;              // AGE叠加后的两拍颜色
	wire wire_age_vsync;                  // AGE叠加后的两拍VS
	wire wire_age_hsync;                  // AGE叠加后的两拍HS
	wire wire_age_de;                     // AGE叠加后的两拍DE

	//--------------寄存器信号--------------//
	// 原图影子只为最终撤销框色，不增加图像缓存或框表。
	reg [23:0] reg_raw_first = 0;           // 原图经过第一个像素寄存边界
	reg [23:0] reg_raw_second = 0;          // 与最终AGE颜色对应的原始像素

	//-------------输出信号连线-------------//
	// 固定框色非白，AGE仅白墨点；所以白色像素无须撤回。
	assign o_rgb = (!i_table_draw_valid && (wire_age_rgb != 24'hffffff))
	             ? reg_raw_second : wire_age_rgb;                          // 即时去掉任何已排队的绿色/青色框，保留文字
	assign o_vsync = wire_age_vsync;                                       // VS不经额外组合延迟级
	assign o_hsync = wire_age_hsync;                                       // HS同样保留两拍
	assign o_de = wire_age_de;                                             // DE不因扫描或许可暂停

	//-----------主要任务处理区域-----------//
	// 原图影子与框层第一拍同边沿采样。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			reg_raw_first <= 24'd0;
		end else begin
			reg_raw_first <= i_rgb;
		end
	end

	// 与AGE第二拍同步，不能拿当前未延迟原图替换旧像素。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			reg_raw_second <= 24'd0;
		end else begin
			reg_raw_second <= reg_raw_first;
		end
	end

	//------------模块实例化区域------------//
	// 唯一表读口只由行扫描所有者驱动，不复制完整活动框表。
	road_box_line_overlay BoxLine_Inst (
		.i_clk(i_clk), .i_rstn(i_rstn), .i_sof(i_sof),
		.i_vsync(i_vsync), .i_hsync(i_hsync), .i_de(i_de), .i_rgb(i_rgb),
		.i_table_active_valid(i_table_active_valid), .i_table_count(i_table_count),
		.i_table_entry(i_table_entry), .i_table_draw_valid(i_table_draw_valid),
		.o_table_read_index(o_table_read_index),
		.o_vsync(wire_box_vsync), .o_hsync(wire_box_hsync),
		.o_de(wire_box_de), .o_rgb(wire_box_rgb), .o_sof(wire_box_sof),
		.o_line_ready(o_line_ready), .o_prepare_busy(o_prepare_busy),
		.o_last_prepare_cycles(o_last_prepare_cycles), .o_fault(o_fault)
	);

	// 旧AGE源码只读；输入SOF已经和框层RGB等延迟一拍。
	road_age_overlay AgeText_Inst (
		.i_clk(i_clk), .i_rstn(i_rstn), .i_sof(wire_box_sof),
		.i_vsync(wire_box_vsync), .i_hsync(wire_box_hsync),
		.i_de(wire_box_de), .i_rgb(wire_box_rgb),
		.i_age_upper_ms(i_age_upper_ms), .i_table_draw_valid(i_table_draw_valid),
		.o_vsync(wire_age_vsync), .o_hsync(wire_age_hsync),
		.o_de(wire_age_de), .o_rgb(wire_age_rgb), .o_draw_permit()
	);
endmodule
