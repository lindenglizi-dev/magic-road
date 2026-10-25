`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-16
// Design Name: Fixed standard layer tile sequence
// Module Name: road_standard_layer_sequence
// Description: description/road_standard_layer_sequence_Design.pdf
// Simulations: testbench/vivado/2021.1/road_standard_layer_sequence
// Referrences: Frozen graph31 standard layers
// Dependencies: Actual tile client done retirement contract
// Version: V1.0
// Revision Date: 2026-10-16
// History: 2026-10-16 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-16
// 设计名称: 固定标准层逐tile发令
// 模块名称: road_standard_layer_sequence
// 模块说明: Description/road_standard_layer_sequence_Design.pdf
// 仿真工程: TestBench/Vivado/2021.1/road_standard_layer_sequence
// 参考资料: 冻结31标准层形状
// 依赖文件: 实际tile客户端退休完成契约
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 2026-10-16 V1.0 Codex 创建文件

module road_standard_layer_sequence
(
	//-----------------全局信号-----------------//
	input i_clk, // 同一计算域100MHz
	input i_rstn, // 所有客户共同低有效复位
	//-----------------用户接口-----------------//
	input i_cancel, // 取消后保持owner到共同reset
	input i_start_valid, // 固定整层任务请求
	input [6:0]i_layer_id, // 冻结graph节点号
	input i_tile_start_ready, // 当前tile客户端允许锁任务
	input i_tile_done, // 所有事务和写屏障退休后的单拍
	input i_tile_fault, // 当前客户端粘滞故障
	output o_start_ready, // 空闲且释放完毕才接整层
	output o_busy, // 整层中保持唯一计算owner
	output o_done, // 最后tile完整退休后单拍
	output o_fault, // 取消或错误不能冒充done
	output o_tile_start_valid, // 逐tile任务保持到ready
	output [6:0]o_layer_id, // 整层期间固定节点
	output [6:0]o_tile_y, // 输出四行对齐起点
	output [6:0]o_tile_x // 输出四列对齐起点
);
	//-------------状态参数区域-------------//
	localparam [2:0]ST_IDLE = 0; // 无未退休整层任务
	localparam [2:0]ST_CONFIG = 1; // 验证冻结层选择
	localparam [2:0]ST_ISSUE = 2; // 保持当前tile准入请求
	localparam [2:0]ST_WAIT = 3; // 等实际tile退休
	localparam [2:0]ST_ADVANCE = 4; // 推进下一tile坐标
	localparam [2:0]ST_FINISH = 5; // 层完成单拍仍持owner
	localparam [2:0]ST_FAULT = 6; // 错误保持至共同reset

	//--------------状态机信号--------------//
	reg [2:0]state_current = ST_IDLE; // 当前发令阶段
	reg [2:0]state_next = ST_IDLE; // 组合下一发令阶段

	//--------------寄存器信号--------------//
	reg [1:0]reg_release = 0; // 两沿释放新应用准入
	reg [6:0]reg_layer = 0; // 首握手冻结的卷积层
	reg [6:0]reg_y = 0; // 当前tile行起点
	reg [6:0]reg_x = 0; // 当前tile列起点

	//---------------标志信号---------------//
	reg flag_fault = 0; // 本地协议错误粘滞
	wire flag_last_column; // 当前tile为本行最后块
	wire flag_last_tile; // 当前tile为整层最后块
	wire flag_bad_done; // 没有未决任务却返回完成

	//---------------译码信号---------------//
	reg [6:0]dec_height = 0; // 冻结输出高度
	reg [7:0]dec_width = 0; // 冻结输出宽度

	//-------------其他信号连线-------------//
	assign flag_last_column = reg_x + 4 >= dec_width; // 固定宽度都四对齐
	assign flag_last_tile = flag_last_column && reg_y + 4 >= dec_height; // H18最后从y16开始
	assign flag_bad_done = i_tile_done && state_current != ST_WAIT; // 不接纳旧客户完成脉冲

	//-------------输出信号连线-------------//
	assign o_fault = flag_fault || i_cancel || i_tile_fault; // 下游错误立即撤成功许可
	assign o_start_ready = state_current == ST_IDLE && reg_release[1] && !o_fault; // 所有权空闲才接受
	assign o_busy = state_current != ST_IDLE; // 含完成拍和错误占有
	assign o_done = state_current == ST_FINISH && !o_fault; // 整层最后真实tile完成
	assign o_tile_start_valid = state_current == ST_ISSUE && reg_release[1] && !o_fault; // 等ready不推进
	assign o_layer_id = reg_layer; // 层身份不随外部扰动变化
	assign o_tile_y = reg_y; // 当前行起点保持
	assign o_tile_x = reg_x; // 当前列起点保持

	// 固定三组形状覆盖31节点，不接受任意外部形状或其它算子。
	always@(*)begin
		dec_height = 0;
		dec_width = 0;
		case(reg_layer)
			82,83,84,85,86,87,88:begin
				dec_height = 72;
				dec_width = 128;
			end
			12,13,55,64,65,90,91,92,93,94,95,96:begin
				dec_height = 36;
				dec_width = 64;
			end
			26,27,46,73,74,98,99,100,101,102,103,104:begin
				dec_height = 18;
				dec_width = 32;
			end
			default:begin
				dec_height = 0;
			end
		endcase
	end

	//--------------状态机区域--------------//
	// 共同断言后两沿释放，仅控制新应用任务准入。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_release <= 0;
		end else begin
			reg_release <= {reg_release[0],1'b1};
		end
	end

	// 发令状态在reset统一取消，不声称外部DDR已排空。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			state_current <= ST_IDLE;
		end else begin
			state_current <= state_next;
		end
	end

	// 一个tile完整退休后才允许发下一个。
	always@(*)begin
		state_next = state_current;
		case(state_current)
			// 只在start握手建立整层任务。
			ST_IDLE:begin
				if(i_start_valid && o_start_ready)begin
					state_next = ST_CONFIG;
				end
			end
			// 非冻结节点立即故障而非发出错误tile。
			ST_CONFIG:begin
				if(dec_height == 0)begin
					state_next = ST_FAULT;
				end else begin
					state_next = ST_ISSUE;
				end
			end
			// tile请求实际握手后才拥有未决任务。
			ST_ISSUE:begin
				if(o_tile_start_valid && i_tile_start_ready)begin
					state_next = ST_WAIT;
				end
			end
			// done代表客户所有在途响应与输出屏障已退休。
			ST_WAIT:begin
				if(i_tile_done)begin
					if(flag_last_tile)begin
						state_next = ST_FINISH;
					end else begin
						state_next = ST_ADVANCE;
					end
				end
			end
			// 独立一拍更新坐标，避免改动反压中payload。
			ST_ADVANCE:begin
				state_next = ST_ISSUE;
			end
			// 完成脉冲后归还整层owner。
			ST_FINISH:begin
				state_next = ST_IDLE;
			end
			// 只共同reset可结束故障占有。
			ST_FAULT:begin
				state_next = ST_FAULT;
			end
			// 非法状态不得假成功。
			default:begin
				state_next = ST_FAULT;
			end
		endcase
		if(o_fault || flag_bad_done)begin
			state_next = ST_FAULT;
		end
	end

	//-----------状态任务处理区域-----------//
	// 只有坐标、层身份和错误小寄存器，没有tile或权重存储。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_layer <= 0;
			reg_y <= 0;
			reg_x <= 0;
			flag_fault <= 0;
		end else begin
			if(state_next == ST_FAULT)begin
				flag_fault <= 1; // 错误不自动解除owner
			end
			if(i_start_valid && o_start_ready)begin
				reg_layer <= i_layer_id; // 唯一采样固定节点的握手沿
				reg_y <= 0; // 整层从首tile行开始
				reg_x <= 0; // 整层从首tile列开始
			end
			if(state_current == ST_ADVANCE)begin
				if(flag_last_column)begin
					reg_x <= 0; // 行尾回到首列
					reg_y <= reg_y + 7'd4; // 下一行tile起点
				end else begin
					reg_x <= reg_x + 7'd4; // 行内递增四列
				end
			end
		end
	end
endmodule
