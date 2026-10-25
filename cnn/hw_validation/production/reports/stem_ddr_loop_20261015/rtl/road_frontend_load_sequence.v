`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026/10/15
// Design Name: Fixed frontend load sequence
// Module Name: road_frontend_load_sequence
// Description: Loop counters with synchronous data ROMs
// Simulations: tests/tb_frontend_load_sequence.v
// Referrences: requirements.txt, reference.py
// Dependencies: loop_table.hex, loop_parameters.hex, loop_pixels.hex
// Version: V1.0
// Revision Date: 2026/10/15
// History: 2026/10/15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO project
// 开发人员: Codex
// 创建日期: 2026年10月15日
// 设计名称: 固定前端循环加载
// 模块名称: road_frontend_load_sequence
// 模块说明: 阶段与计数产生命令头，数据ROM只保存实际数值
// 仿真工程: tests/tb_frontend_load_sequence.v
// 参考资料: requirements.txt, reference.py
// 依赖文件: 三份冻结数据ROM
// 当前版本: V1.0
// 修订日期: 2026年10月15日
// 修订历史: 2026年10月15日 V1.0 Codex 创建文件
module road_frontend_load_sequence
(
	//---------------全局信号---------------//
	input i_clk, // 与外层序列器同一计算时钟
	input i_rstn, // 低有效复位使阶段回到装表起点
	//---------------用户接口---------------//
	input i_fetch, // 取数沿更新命令输出
	input i_advance, // 仅在当前命令完成后推进
	output [63:0]o_command // 同步返回并保持的原格式命令
);
	//-------------状态参数区域-------------//
	localparam [4:0] ST_TABLE = 5'd0; // 装满共享激活表
	localparam [4:0] ST_STEM_WEIGHT = 5'd1; // 首层卷积权重
	localparam [4:0] ST_STEM_BIAS = 5'd2; // 首层偏置
	localparam [4:0] ST_STEM_MULTIPLIER = 5'd3; // 首层前重定标乘数
	localparam [4:0] ST_STEM_SHIFT = 5'd4; // 首层前重定标移位
	localparam [4:0] ST_STEM_POST = 5'd5; // 首层后重定标记录
	localparam [4:0] ST_STEM_PIXELS = 5'd6; // 当前九乘九彩色halo
	localparam [4:0] ST_STEM_START = 5'd7; // 发起当前首层小块
	localparam [4:0] ST_STEM_EXPORT = 5'd8; // 等当前首层导出写完
	localparam [4:0] ST_SELECT = 5'd9; // 切换到下采样所有者
	localparam [4:0] ST_DOWN_WEIGHT = 5'd10; // 深度卷积系数
	localparam [4:0] ST_DOWN_BIAS = 5'd11; // 深度卷积偏置
	localparam [4:0] ST_POINT_WEIGHT = 5'd12; // 逐点卷积系数
	localparam [4:0] ST_POINT_BIAS = 5'd13; // 逐点卷积偏置
	localparam [4:0] ST_DOWN_MULTIPLIER = 5'd14; // 下采样两层的前乘数
	localparam [4:0] ST_DOWN_CONTROL = 5'd15; // 下采样移位及后参数
	localparam [4:0] ST_DOWN_HALO = 5'd16; // 从真实DDR重建下采样halo
	localparam [4:0] ST_DOWN_START = 5'd17; // 发起当前下采样计算
	localparam [4:0] ST_DOWN_EXPORT = 5'd18; // 等下采样结果全部导出
	localparam [4:0] ST_DONE = 5'd19; // 外层验证计数后终止

	//---------------计数信号---------------//
	reg [9:0]cnt_item = 0; // 当前数据段内的装载地址
	reg [10:0]cnt_parameter = 0; // 两阶段参数的连续ROM游标
	reg [11:0]cnt_pixel = 0; // 十六块彩色halo的连续游标
	reg [3:0]cnt_stem_tile = 0; // 已完成的首层小块索引
	reg [1:0]cnt_down_tile = 0; // 已完成的下采样小块索引

	//--------------状态机信号--------------//
	reg [4:0]state_current = 0; // 当前加载或执行阶段
	reg [4:0]state_next = 0; // 消费当前命令后进入的阶段

	//--------------寄存器信号--------------//
	reg [15:0]reg_table[0:1023]; // 原共享SiLU有符号表
	reg [31:0]reg_parameters[0:2047]; // 原权重、偏置和定标载荷
	reg [8:0]reg_pixels[0:4095]; // 补零标志及RGB无符号样本

	//---------------输出信号---------------//
	reg [63:0]command_o = 0; // 保持至下次取数的完整命令

	//-------------输出信号连线-------------//
	assign o_command = command_o; // 外层沿用原解码位段

	//-----------输出信号处理区域-----------//
	// 所有ROM仅在FETCH沿读取，ADVANCE不改变已返回载荷。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			command_o <= 64'd0;
		end else if(i_fetch == 1'b1)begin
			case(state_current)
				ST_TABLE:begin command_o <= {4'd0, 1'b0, cnt_item, 3'd0, 14'd0, {16{reg_table[cnt_item][15]}}, reg_table[cnt_item]}; end
				ST_STEM_WEIGHT,ST_DOWN_WEIGHT:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd2, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_STEM_BIAS,ST_DOWN_BIAS:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd3, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_STEM_MULTIPLIER,ST_POINT_WEIGHT:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd4, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_STEM_SHIFT,ST_POINT_BIAS:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd5, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_STEM_POST,ST_DOWN_MULTIPLIER:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd6, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_DOWN_CONTROL:begin command_o <= {4'd1, 1'b0, cnt_item, 3'd7, 14'd0, reg_parameters[cnt_parameter]}; end
				ST_STEM_PIXELS:begin command_o <= {4'd1, 1'b0, cnt_item, 2'd0, reg_pixels[cnt_pixel][8], 38'd0, reg_pixels[cnt_pixel][7:0]}; end
				ST_STEM_START,ST_DOWN_START:begin command_o <= 64'h2000000000000000; end
				ST_STEM_EXPORT:begin command_o <= 64'h3000000000000000; end
				ST_SELECT:begin command_o <= 64'h4000000000000001; end
				ST_DOWN_HALO:begin command_o <= 64'h5000000000000000; end
				ST_DOWN_EXPORT:begin command_o <= 64'h6000000000000000; end
				ST_DONE:begin command_o <= 64'h7000000000000000; end
				default:begin command_o <= 64'hf000000000000000; end
			endcase
		end
	end

	//--------------状态机区域--------------//
	// 复位立即取消旧阶段；外层的首个FETCH仍从表项零开始。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_TABLE;
		end else begin
			state_current <= state_next;
		end
	end

	// 每次ADVANCE只消费一条命令；等待算术或DDR时全部保持。
	always@(*)begin
		state_next = state_current;
		if(i_advance == 1'b1)begin
			case(state_current)
				ST_TABLE:begin if(cnt_item == 10'd1023)begin state_next = ST_STEM_WEIGHT; end end
				ST_STEM_WEIGHT:begin if(cnt_item == 10'd431)begin state_next = ST_STEM_BIAS; end end
				ST_STEM_BIAS:begin if(cnt_item == 10'd15)begin state_next = ST_STEM_MULTIPLIER; end end
				ST_STEM_MULTIPLIER:begin if(cnt_item == 10'd15)begin state_next = ST_STEM_SHIFT; end end
				ST_STEM_SHIFT:begin if(cnt_item == 10'd15)begin state_next = ST_STEM_POST; end end
				ST_STEM_POST:begin if(cnt_item == 10'd1)begin state_next = ST_STEM_PIXELS; end end
				ST_STEM_PIXELS:begin if(cnt_item == 10'd242)begin state_next = ST_STEM_START; end end
				ST_STEM_START:begin state_next = ST_STEM_EXPORT; end
				ST_STEM_EXPORT:begin state_next = cnt_stem_tile == 4'd15 ? ST_SELECT : ST_STEM_PIXELS; end
				ST_SELECT:begin state_next = ST_DOWN_WEIGHT; end
				ST_DOWN_WEIGHT:begin if(cnt_item == 10'd143)begin state_next = ST_DOWN_BIAS; end end
				ST_DOWN_BIAS:begin if(cnt_item == 10'd15)begin state_next = ST_POINT_WEIGHT; end end
				ST_POINT_WEIGHT:begin if(cnt_item == 10'd383)begin state_next = ST_POINT_BIAS; end end
				ST_POINT_BIAS:begin if(cnt_item == 10'd23)begin state_next = ST_DOWN_MULTIPLIER; end end
				ST_DOWN_MULTIPLIER:begin if(cnt_item == 10'd39)begin state_next = ST_DOWN_CONTROL; end end
				ST_DOWN_CONTROL:begin if(cnt_item == 10'd43)begin state_next = ST_DOWN_HALO; end end
				ST_DOWN_HALO:begin state_next = ST_DOWN_START; end
				ST_DOWN_START:begin state_next = ST_DOWN_EXPORT; end
				ST_DOWN_EXPORT:begin state_next = cnt_down_tile == 2'd3 ? ST_DONE : ST_DOWN_HALO; end
				ST_DONE:begin state_next = ST_DONE; end
				default:begin state_next = ST_DONE; end
			endcase
		end
	end

	//-----------状态任务处理区域-----------//
	// 段内地址只随已完成命令增加，换段时回到零。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_item <= 10'd0;
		end else if(i_advance == 1'b1)begin
			if(state_current != state_next)begin cnt_item <= 10'd0; end
			else begin cnt_item <= cnt_item + 10'd1; end
		end
	end

	// 参数游标跨RGB阶段保留，选择下采样后接着读取同一小ROM。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_parameter <= 11'd0;
		end else if(i_advance == 1'b1)begin
			case(state_current)
				ST_STEM_WEIGHT,ST_STEM_BIAS,ST_STEM_MULTIPLIER,ST_STEM_SHIFT,ST_STEM_POST,
				ST_DOWN_WEIGHT,ST_DOWN_BIAS,ST_POINT_WEIGHT,ST_POINT_BIAS,ST_DOWN_MULTIPLIER,ST_DOWN_CONTROL:begin
					cnt_parameter <= cnt_parameter + 11'd1;
				end
				default:begin end
			endcase
		end
	end

	// 每个像素载荷包含原padding种类，保持原入口中心化行为。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_pixel <= 12'd0;
		end else if(i_advance && state_current == ST_STEM_PIXELS)begin
			cnt_pixel <= cnt_pixel + 12'd1;
		end
	end

	// 完成首层导出后才选择下一块，最多执行十六次。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_stem_tile <= 4'd0;
		end else if(i_advance && state_current == ST_STEM_EXPORT && cnt_stem_tile != 4'd15)begin
			cnt_stem_tile <= cnt_stem_tile + 4'd1;
		end
	end

	// 当前下采样输出全部消费后才推进消费者索引。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_down_tile <= 2'd0;
		end else if(i_advance && state_current == ST_DOWN_EXPORT && cnt_down_tile != 2'd3)begin
			cnt_down_tile <= cnt_down_tile + 2'd1;
		end
	end

	//--------------初始化区域--------------//
	// 固定数据文件只用于本四块回归；真实层输入在后续由DDR提供。
	initial begin
		$readmemh("loop_table.hex",reg_table);
		$readmemh("loop_parameters.hex",reg_parameters);
		$readmemh("loop_pixels.hex",reg_pixels);
	end
endmodule
