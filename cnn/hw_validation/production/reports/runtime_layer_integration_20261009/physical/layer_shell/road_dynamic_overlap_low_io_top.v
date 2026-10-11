`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/07 00:00:00
// Design Name:     road_dynamic_overlap_low_io_top
// Module Name:     road_dynamic_overlap_low_io_top
// Description:     road_dynamic_overlap_low_io_top_spec.md
// Simulations:     shell regression retained beside this source
//
// Referrences:
// File Format      File Name
// 1.Markdown       road_dynamic_overlap_low_io_top_spec.md
//
// Dependencies:
// Module Name                    Version
// down2_dynamic_tile_runner      V1.0
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
// 设计名称:        road_dynamic_overlap_low_io_top
// 模块名称:        road_dynamic_overlap_low_io_top
// 模块说明:        road_dynamic_overlap_low_io_top_spec.md
// 仿真工程:        本目录窄口回归
//
// 参考资料:
// 文件格式         文件名称
// 1.Markdown       road_dynamic_overlap_low_io_top_spec.md
//
// 依赖文件:
// 模块名称                       版本
// down2_dynamic_tile_runner      V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月07日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月07日   V1.0        Erie              创建文件

module road_dynamic_overlap_low_io_top
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 一百兆诊断时钟
	input i_rstn,                               // 异步低有效外部复位

	//------------------RX接口------------------//
	input i_rx_valid,                           // 十六位接收有效
	input [15:0]i_rx_data,                      // 命令或动态负载字
	output o_rx_ready,                          // 接收许可

	//------------------TX接口------------------//
	output o_tx_valid,                          // 结果响应有效
	output [15:0]o_tx_data,                     // 索引结果或完成字
	input i_tx_ready                            // 结果响应接收许可
);

	//---------------状态参数区域---------------//
	//窄口命令解析与导出阶段
	localparam [3:0]ST_IDLE = 4'd0;
	localparam [3:0]ST_TABLE = 4'd1;
	localparam [3:0]ST_LOAD_DESCRIPTOR = 4'd2;
	localparam [3:0]ST_LOAD_LOW = 4'd3;
	localparam [3:0]ST_LOAD_HIGH = 4'd4;
	localparam [3:0]ST_LOAD_WAIT = 4'd5;
	localparam [3:0]ST_EXPORT_WAIT = 4'd6;
	localparam [3:0]ST_EXPORT_META = 4'd7;
	localparam [3:0]ST_EXPORT_DATA = 4'd8;
	localparam [3:0]ST_EXPORT_REPORT = 4'd9;
	localparam [3:0]ST_ERROR_REPORT = 4'd10;
	localparam [3:0]ST_STATUS_SEND = 4'd11;

	//命令字
	localparam [15:0]CMD_TABLE_BEGIN = 16'h1000;
	localparam [15:0]CMD_LOAD_BEGIN = 16'h2000;
	localparam [15:0]CMD_START_DW_PW = 16'h3000;
	localparam [15:0]CMD_START_PW_ONLY = 16'h3001;
	localparam [15:0]CMD_EXPORT = 16'h4000;
	localparam [15:0]CMD_STATUS = 16'h5000;
	localparam [15:0]CMD_COMMIT_BLOCK = 16'h6000;
	localparam [15:0]CMD_COMMIT_ALLOW = 16'h6001;

	//---------------状态机信号-----------------//
	reg [3:0]state_current = ST_IDLE;            // 当前窄口阶段
	reg [3:0]state_next = ST_IDLE;               // 下一窄口阶段

	//---------------寄存器信号-----------------//
	//两级异步断言同步释放
	reg reg_release_meta = 1'b0;                // 复位释放第一级
	reg reg_release_done = 1'b0;                // 复位释放第二级

	//运行时装载与命令保持
	reg [9:0]reg_table_addr = 10'd0;             // 隐式递增表地址
	reg [2:0]reg_load_kind = 3'd0;               // 动态装载类别
	reg [10:0]reg_load_addr = 11'd0;             // 动态装载地址
	reg [15:0]reg_load_low = 16'd0;              // 三十二位数据低半字
	reg signed [31:0]reg_load_data = 32'sd0;     // 完整动态装载数据
	reg reg_load_pending = 1'b0;                // 等待runner接收的装载项
	reg reg_start = 1'b0;                       // 单拍启动脉冲
	reg reg_pw_only = 1'b0;                     // 启动模式
	reg reg_export_start = 1'b0;                // 单拍导出脉冲
	reg reg_export_done_seen = 1'b0;            // 保留导出完成事件
	reg reg_runner_done_seen = 1'b0;            // 保留runner单拍完成事件
	reg reg_commit_ready = 1'b0;                // 动态写回许可不得常量折叠
	reg reg_shell_fault = 1'b0;                 // 窄口协议故障保持
	reg [4:0]cnt_status_index = 5'd0;            // 三十一字状态快照索引

	//runner状态与十五个三十二位计数快照
	reg [15:0]reg_snapshot_flags = 16'd0;
	reg [31:0]reg_snapshot_preload = 32'd0;
	reg [31:0]reg_snapshot_core = 32'd0;
	reg [31:0]reg_snapshot_mac_cycles = 32'd0;
	reg [31:0]reg_snapshot_pre_cycles = 32'd0;
	reg [31:0]reg_snapshot_silu_cycles = 32'd0;
	reg [31:0]reg_snapshot_post_cycles = 32'd0;
	reg [31:0]reg_snapshot_writeback_cycles = 32'd0;
	reg [31:0]reg_snapshot_storage_wait = 32'd0;
	reg [31:0]reg_snapshot_scheduler_idle = 32'd0;
	reg [31:0]reg_snapshot_export_cycles = 32'd0;
	reg [31:0]reg_snapshot_mac_results = 32'd0;
	reg [31:0]reg_snapshot_pre_accepts = 32'd0;
	reg [31:0]reg_snapshot_silu_accepts = 32'd0;
	reg [31:0]reg_snapshot_post_accepts = 32'd0;
	reg [31:0]reg_snapshot_writebacks = 32'd0;

	//--------------模块实例化信号--------------//
	//runner命令与状态
	wire runner_table_ready;
	wire runner_table_loaded;
	wire runner_table_fault;
	wire runner_load_ready;
	wire runner_busy;
	wire runner_done;
	wire runner_fault;
	wire runner_output_valid;
	wire signed [7:0]runner_output_data;
	wire [8:0]runner_output_index;
	wire runner_export_done;

	//runner结构与周期观察量
	wire runner_debug_valid;
	wire [1:0]runner_debug_phase;
	wire runner_debug_layer;
	wire [3:0]runner_debug_position;
	wire [4:0]runner_debug_channel;
	wire signed [31:0]runner_debug_value;
	wire [31:0]runner_preload_writes;
	wire [31:0]runner_core_cycles;
	wire [31:0]runner_mac_cycles;
	wire [31:0]runner_pre_cycles;
	wire [31:0]runner_silu_cycles;
	wire [31:0]runner_post_cycles;
	wire [31:0]runner_writeback_cycles;
	wire [31:0]runner_storage_wait_cycles;
	wire [31:0]runner_scheduler_idle_cycles;
	wire [31:0]runner_export_cycles;
	wire [1:0]runner_result_queue_count;
	wire runner_result_reserved;
	wire [3:0]runner_meta_count;
	wire [31:0]runner_mac_result_count;
	wire [31:0]runner_pre_accept_count;
	wire [31:0]runner_silu_accept_count;
	wire [31:0]runner_post_accept_count;
	wire [31:0]runner_writeback_count;

	//-----------------标志信号-----------------//
	wire flag_interface_open;                   // 两级释放完成且外部复位高
	wire flag_rx_transfer;                      // 实际接收握手
	wire flag_tx_transfer;                      // 实际发送握手
	wire flag_table_transfer;                   // 实际表项握手
	wire flag_load_transfer;                    // 实际动态装载握手

	//-----------------其他信号-----------------//
	reg rx_ready_o = 1'b0;                      // 内部接收许可代理
	reg tx_valid_o = 1'b0;                      // 内部发送有效代理
	reg [15:0]tx_data_o = 16'd0;                // 内部发送数据代理
	reg [15:0]dec_status_word = 16'd0;          // 当前快照字选择
	wire runner_table_valid;
	wire runner_load_valid;
	wire runner_output_ready;

	//---------------其他信号连线---------------//
	assign flag_interface_open = i_rstn & reg_release_done;
	assign flag_rx_transfer = i_rx_valid & rx_ready_o & flag_interface_open;
	assign flag_tx_transfer = tx_valid_o & i_tx_ready & flag_interface_open;
	assign runner_table_valid = (state_current == ST_TABLE) & i_rx_valid & flag_interface_open;
	assign flag_table_transfer = runner_table_valid & runner_table_ready;
	assign runner_load_valid = (state_current == ST_LOAD_WAIT) & reg_load_pending;
	assign flag_load_transfer = runner_load_valid & runner_load_ready;
	assign runner_output_ready = (state_current == ST_EXPORT_DATA) & i_tx_ready & flag_interface_open;

	//---------------输出信号连线---------------//
	assign o_rx_ready = rx_ready_o & flag_interface_open;
	assign o_tx_valid = tx_valid_o & flag_interface_open;
	assign o_tx_data = tx_data_o;

	//-----------主要任务处理区域-----------//
	//外部复位异步断言并用两拍同步释放
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release_meta <= 1'b0;
		end else begin
			reg_release_meta <= 1'b1;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release_done <= 1'b0;
		end else begin
			reg_release_done <= reg_release_meta;
		end
	end

	//状态寄存器
	always@(posedge i_clk or negedge reg_release_done)begin
		if(reg_release_done == 1'b0)begin
			state_current <= ST_IDLE;
		end else begin
			state_current <= state_next;
		end
	end

	//状态转移只依赖真实握手与runner状态
	always@(*)begin
		state_next = state_current;
		case(state_current)
			ST_IDLE:begin
				if(flag_rx_transfer)begin
					case(i_rx_data)
						CMD_TABLE_BEGIN: state_next = runner_busy ? ST_ERROR_REPORT : ST_TABLE;
						CMD_LOAD_BEGIN: state_next = runner_busy ? ST_ERROR_REPORT : ST_LOAD_DESCRIPTOR;
						CMD_START_DW_PW: state_next = runner_busy ? ST_ERROR_REPORT : ST_IDLE;
						CMD_START_PW_ONLY: state_next = runner_busy ? ST_ERROR_REPORT : ST_IDLE;
						CMD_EXPORT: state_next = (runner_busy || (~reg_runner_done_seen) || runner_fault) ? ST_ERROR_REPORT : ST_EXPORT_WAIT;
						CMD_STATUS: state_next = ST_STATUS_SEND;
						CMD_COMMIT_BLOCK: state_next = ST_IDLE;
						CMD_COMMIT_ALLOW: state_next = ST_IDLE;
						default: state_next = ST_ERROR_REPORT;
					endcase
				end
			end
			ST_TABLE:begin
				if(flag_table_transfer && (reg_table_addr == 10'd1023))begin
					state_next = ST_IDLE;
				end
			end
			ST_LOAD_DESCRIPTOR:begin
				if(flag_rx_transfer)begin
					state_next = (i_rx_data[12:11] == 2'b00) ? ST_LOAD_LOW : ST_ERROR_REPORT;
				end
			end
			ST_LOAD_LOW:begin
				if(flag_rx_transfer)begin
					state_next = ST_LOAD_HIGH;
				end
			end
			ST_LOAD_HIGH:begin
				if(flag_rx_transfer)begin
					state_next = ST_LOAD_WAIT;
				end
			end
			ST_LOAD_WAIT:begin
				if(flag_load_transfer)begin
					state_next = ST_IDLE;
				end
			end
			ST_EXPORT_WAIT:begin
				if(runner_output_valid)begin
					state_next = ST_EXPORT_META;
				end else if(reg_export_done_seen)begin
					state_next = ST_EXPORT_REPORT;
				end
			end
			ST_EXPORT_META:begin
				if(flag_tx_transfer)begin
					state_next = ST_EXPORT_DATA;
				end
			end
			ST_EXPORT_DATA:begin
				if(flag_tx_transfer)begin
					state_next = ST_EXPORT_WAIT;
				end
			end
			ST_EXPORT_REPORT:begin
				if(flag_tx_transfer)begin
					state_next = ST_IDLE;
				end
			end
			ST_ERROR_REPORT:begin
				if(flag_tx_transfer)begin
					state_next = ST_IDLE;
				end
			end
			ST_STATUS_SEND:begin
				if(flag_tx_transfer && (cnt_status_index == 5'd30))begin
					state_next = ST_IDLE;
				end
			end
			default: state_next = ST_ERROR_REPORT;
		endcase
	end

	//状态命令冻结后逐字选择，三十二位字段均低半字在前
	always@(*)begin
		case(cnt_status_index)
			5'd0: dec_status_word = reg_snapshot_flags;
			5'd1: dec_status_word = reg_snapshot_preload[15:0];
			5'd2: dec_status_word = reg_snapshot_preload[31:16];
			5'd3: dec_status_word = reg_snapshot_core[15:0];
			5'd4: dec_status_word = reg_snapshot_core[31:16];
			5'd5: dec_status_word = reg_snapshot_mac_cycles[15:0];
			5'd6: dec_status_word = reg_snapshot_mac_cycles[31:16];
			5'd7: dec_status_word = reg_snapshot_pre_cycles[15:0];
			5'd8: dec_status_word = reg_snapshot_pre_cycles[31:16];
			5'd9: dec_status_word = reg_snapshot_silu_cycles[15:0];
			5'd10: dec_status_word = reg_snapshot_silu_cycles[31:16];
			5'd11: dec_status_word = reg_snapshot_post_cycles[15:0];
			5'd12: dec_status_word = reg_snapshot_post_cycles[31:16];
			5'd13: dec_status_word = reg_snapshot_writeback_cycles[15:0];
			5'd14: dec_status_word = reg_snapshot_writeback_cycles[31:16];
			5'd15: dec_status_word = reg_snapshot_storage_wait[15:0];
			5'd16: dec_status_word = reg_snapshot_storage_wait[31:16];
			5'd17: dec_status_word = reg_snapshot_scheduler_idle[15:0];
			5'd18: dec_status_word = reg_snapshot_scheduler_idle[31:16];
			5'd19: dec_status_word = reg_snapshot_export_cycles[15:0];
			5'd20: dec_status_word = reg_snapshot_export_cycles[31:16];
			5'd21: dec_status_word = reg_snapshot_mac_results[15:0];
			5'd22: dec_status_word = reg_snapshot_mac_results[31:16];
			5'd23: dec_status_word = reg_snapshot_pre_accepts[15:0];
			5'd24: dec_status_word = reg_snapshot_pre_accepts[31:16];
			5'd25: dec_status_word = reg_snapshot_silu_accepts[15:0];
			5'd26: dec_status_word = reg_snapshot_silu_accepts[31:16];
			5'd27: dec_status_word = reg_snapshot_post_accepts[15:0];
			5'd28: dec_status_word = reg_snapshot_post_accepts[31:16];
			5'd29: dec_status_word = reg_snapshot_writebacks[15:0];
			default: dec_status_word = reg_snapshot_writebacks[31:16];
		endcase
	end

	//状态输出保证ready-valid停顿期间数值稳定
	always@(*)begin
		rx_ready_o = 1'b0;
		tx_valid_o = 1'b0;
		tx_data_o = 16'd0;
		case(state_current)
			ST_IDLE: rx_ready_o = 1'b1;
			ST_TABLE: rx_ready_o = runner_table_ready;
			ST_LOAD_DESCRIPTOR: rx_ready_o = 1'b1;
			ST_LOAD_LOW: rx_ready_o = 1'b1;
			ST_LOAD_HIGH: rx_ready_o = 1'b1;
			ST_EXPORT_META:begin
				tx_valid_o = runner_output_valid;
				tx_data_o = 16'h8000 | {7'd0, runner_output_index};
			end
			ST_EXPORT_DATA:begin
				tx_valid_o = runner_output_valid;
				tx_data_o = 16'h9000 | {8'd0, runner_output_data};
			end
			ST_EXPORT_REPORT:begin
				tx_valid_o = 1'b1;
				tx_data_o = {4'hc, runner_fault, reg_shell_fault, 10'd0};
			end
			ST_ERROR_REPORT:begin
				tx_valid_o = 1'b1;
				tx_data_o = 16'he001;
			end
			ST_STATUS_SEND:begin
				tx_valid_o = 1'b1;
				tx_data_o = dec_status_word;
			end
			default:begin
				rx_ready_o = 1'b0;
				tx_valid_o = 1'b0;
				tx_data_o = 16'd0;
			end
		endcase
	end

	//装载、启动、导出与动态写回许可寄存器
	always@(posedge i_clk or negedge reg_release_done)begin
		if(reg_release_done == 1'b0)begin
			reg_table_addr <= 10'd0;
			reg_load_kind <= 3'd0;
			reg_load_addr <= 11'd0;
			reg_load_low <= 16'd0;
			reg_load_data <= 32'sd0;
			reg_load_pending <= 1'b0;
			reg_start <= 1'b0;
			reg_pw_only <= 1'b0;
			reg_export_start <= 1'b0;
			reg_export_done_seen <= 1'b0;
			reg_runner_done_seen <= 1'b0;
			reg_commit_ready <= 1'b0;
			reg_shell_fault <= 1'b0;
			cnt_status_index <= 5'd0;
			reg_snapshot_flags <= 16'd0;
			reg_snapshot_preload <= 32'd0;
			reg_snapshot_core <= 32'd0;
			reg_snapshot_mac_cycles <= 32'd0;
			reg_snapshot_pre_cycles <= 32'd0;
			reg_snapshot_silu_cycles <= 32'd0;
			reg_snapshot_post_cycles <= 32'd0;
			reg_snapshot_writeback_cycles <= 32'd0;
			reg_snapshot_storage_wait <= 32'd0;
			reg_snapshot_scheduler_idle <= 32'd0;
			reg_snapshot_export_cycles <= 32'd0;
			reg_snapshot_mac_results <= 32'd0;
			reg_snapshot_pre_accepts <= 32'd0;
			reg_snapshot_silu_accepts <= 32'd0;
			reg_snapshot_post_accepts <= 32'd0;
			reg_snapshot_writebacks <= 32'd0;
		end else begin
			reg_start <= 1'b0;
			reg_export_start <= 1'b0;
			if((state_current == ST_IDLE) && flag_rx_transfer)begin
				case(i_rx_data)
					CMD_TABLE_BEGIN: reg_table_addr <= 10'd0;
					CMD_START_DW_PW:begin
						if(~runner_busy)begin
							reg_start <= 1'b1;
							reg_pw_only <= 1'b0;
							reg_runner_done_seen <= 1'b0;
						end
					end
					CMD_START_PW_ONLY:begin
						if(~runner_busy)begin
							reg_start <= 1'b1;
							reg_pw_only <= 1'b1;
							reg_runner_done_seen <= 1'b0;
						end
					end
					CMD_EXPORT:begin
						if((~runner_busy) && reg_runner_done_seen && (~runner_fault))begin
							reg_export_start <= 1'b1;
							reg_export_done_seen <= 1'b0;
						end
					end
					CMD_STATUS:begin
						cnt_status_index <= 5'd0;
						reg_snapshot_flags <= {1'b0, runner_export_done, reg_commit_ready,
							reg_shell_fault, runner_fault, reg_runner_done_seen,
							runner_busy, runner_table_fault, runner_table_loaded,
							runner_result_reserved, runner_result_queue_count,
							runner_meta_count};
						reg_snapshot_preload <= runner_preload_writes;
						reg_snapshot_core <= runner_core_cycles;
						reg_snapshot_mac_cycles <= runner_mac_cycles;
						reg_snapshot_pre_cycles <= runner_pre_cycles;
						reg_snapshot_silu_cycles <= runner_silu_cycles;
						reg_snapshot_post_cycles <= runner_post_cycles;
						reg_snapshot_writeback_cycles <= runner_writeback_cycles;
						reg_snapshot_storage_wait <= runner_storage_wait_cycles;
						reg_snapshot_scheduler_idle <= runner_scheduler_idle_cycles;
						reg_snapshot_export_cycles <= runner_export_cycles;
						reg_snapshot_mac_results <= runner_mac_result_count;
						reg_snapshot_pre_accepts <= runner_pre_accept_count;
						reg_snapshot_silu_accepts <= runner_silu_accept_count;
						reg_snapshot_post_accepts <= runner_post_accept_count;
						reg_snapshot_writebacks <= runner_writeback_count;
					end
					CMD_COMMIT_BLOCK: reg_commit_ready <= 1'b0;
					CMD_COMMIT_ALLOW: reg_commit_ready <= 1'b1;
					default:begin
						if((i_rx_data != CMD_LOAD_BEGIN) && (i_rx_data != CMD_TABLE_BEGIN))begin
							reg_shell_fault <= 1'b1;
						end
					end
				endcase
			end
			if(flag_table_transfer && (reg_table_addr != 10'd1023))begin
				reg_table_addr <= reg_table_addr + 10'd1;
			end
			if((state_current == ST_LOAD_DESCRIPTOR) && flag_rx_transfer)begin
				reg_load_kind <= i_rx_data[15:13];
				reg_load_addr <= i_rx_data[10:0];
				if(i_rx_data[12:11] != 2'b00)begin
					reg_shell_fault <= 1'b1;
				end
			end
			if((state_current == ST_LOAD_LOW) && flag_rx_transfer)begin
				reg_load_low <= i_rx_data;
			end
			if((state_current == ST_LOAD_HIGH) && flag_rx_transfer)begin
				reg_load_data <= {i_rx_data, reg_load_low};
				reg_load_pending <= 1'b1;
			end else if(flag_load_transfer)begin
				reg_load_pending <= 1'b0;
			end
			if(runner_export_done)begin
				reg_export_done_seen <= 1'b1;
			end else if((state_current == ST_EXPORT_REPORT) && flag_tx_transfer)begin
				reg_export_done_seen <= 1'b0;
			end
			if((state_current == ST_ERROR_REPORT) && flag_tx_transfer)begin
				reg_shell_fault <= 1'b1;
			end
			if(runner_done)begin
				reg_runner_done_seen <= 1'b1;
			end
			if((state_current == ST_STATUS_SEND) && flag_tx_transfer && (cnt_status_index != 5'd30))begin
				cnt_status_index <= cnt_status_index + 1'b1;
			end
		end
	end

	//----------------模块实例化----------------//
	down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_shell(
		.i_clk(i_clk),
		.i_rstn(reg_release_done),
		.i_table_valid(runner_table_valid),
		.i_table_addr(reg_table_addr),
		.i_table_data(i_rx_data),
		.o_table_ready(runner_table_ready),
		.o_table_loaded(runner_table_loaded),
		.o_table_fault(runner_table_fault),
		.i_load_valid(runner_load_valid),
		.i_load_kind(reg_load_kind),
		.i_load_addr(reg_load_addr),
		.i_load_data(reg_load_data),
		.o_load_ready(runner_load_ready),
		.i_start(reg_start),
		.i_pw_only(reg_pw_only),
		.i_commit_ready(reg_commit_ready),
		.o_busy(runner_busy),
		.o_done(runner_done),
		.o_fault(runner_fault),
		.i_export_start(reg_export_start),
		.i_output_ready(runner_output_ready),
		.o_output_valid(runner_output_valid),
		.o_output_data(runner_output_data),
		.o_output_index(runner_output_index),
		.o_export_done(runner_export_done),
		.o_debug_valid(runner_debug_valid),
		.o_debug_phase(runner_debug_phase),
		.o_debug_layer(runner_debug_layer),
		.o_debug_position(runner_debug_position),
		.o_debug_channel(runner_debug_channel),
		.o_debug_value(runner_debug_value),
		.o_preload_writes(runner_preload_writes),
		.o_core_cycles(runner_core_cycles),
		.o_mac_cycles(runner_mac_cycles),
		.o_pre_cycles(runner_pre_cycles),
		.o_silu_cycles(runner_silu_cycles),
		.o_post_cycles(runner_post_cycles),
		.o_writeback_cycles(runner_writeback_cycles),
		.o_storage_wait_cycles(runner_storage_wait_cycles),
		.o_scheduler_idle_cycles(runner_scheduler_idle_cycles),
		.o_export_cycles(runner_export_cycles),
		.o_result_queue_count(runner_result_queue_count),
		.o_result_reserved(runner_result_reserved),
		.o_meta_count(runner_meta_count),
		.o_mac_result_count(runner_mac_result_count),
		.o_pre_accept_count(runner_pre_accept_count),
		.o_silu_accept_count(runner_silu_accept_count),
		.o_post_accept_count(runner_post_accept_count),
		.o_writeback_count(runner_writeback_count)
	);

endmodule
