`timescale 1ns / 1ps

// ponytail: 单批串行功能诊断，后续只在实测吞吐要求下恢复级间重叠。
module road_dynamic_postprocess(
	input i_clk,
	input i_rstn,
	input i_table_valid,
	input [9:0]i_table_addr,
	input signed [15:0]i_table_data,
	output o_table_ready,
	output o_table_loaded,
	input i_input_valid,
	input [95:0]i_accumulators,
	input [95:0]i_pre_multipliers,
	input [17:0]i_pre_shifts,
	input [31:0]i_post_multiplier,
	input [5:0]i_post_shift,
	input i_activate,
	input [2:0]i_lane_mask,
	input [47:0]i_tags,
	input i_input_fault,
	output o_input_ready,
	input i_output_ready,
	output o_output_valid,
	output signed [15:0]o_output_data,
	output [15:0]o_output_tag,
	output o_output_int16,
	output o_fault
);
	localparam ST_IDLE = 4'd0, ST_SELECT = 4'd1;
	localparam ST_PRE_SEND = 4'd2, ST_PRE_WAIT = 4'd3;
	localparam ST_SILU_SEND = 4'd4, ST_SILU_WAIT = 4'd5;
	localparam ST_POST_SEND = 4'd6, ST_POST_WAIT = 4'd7;
	localparam ST_EMIT = 4'd8;
	reg [3:0]state_current = 0;
	reg [3:0]state_next;
	reg [95:0]reg_accumulators = 0;
	reg [95:0]reg_pre_multipliers = 0;
	reg [17:0]reg_pre_shifts = 0;
	reg [30:0]reg_post_multiplier = 0;
	reg [5:0]reg_post_shift = 0;
	reg reg_activate = 0;
	reg [47:0]reg_tags = 0;
	reg [2:0]reg_work_mask = 0;
	reg [2:0]reg_emit_mask = 0;
	reg [1:0]reg_lane = 0;
	reg signed [15:0]reg_scalar = 0;
	reg signed [15:0]reg_result_alpha = 0;
	reg signed [15:0]reg_result_beta = 0;
	reg signed [15:0]reg_result_gamma = 0;
	reg flag_fatal = 0;
	wire flag_table_ready, flag_table_loaded, flag_table_fault;
	wire flag_silu_ready, flag_silu_valid;
	wire signed [15:0]wire_silu_data;
	wire flag_quant_ready, flag_quant_valid, flag_quant_fault;
	wire signed [15:0]wire_quant_data;
	wire [15:0]wire_quant_tag;
	wire [1:0]wire_emit_lane;
	wire flag_quant_send, flag_quant_receive;
	wire flag_bad_parameters;
	reg signed [31:0]wire_selected_accumulator;
	reg [30:0]wire_selected_multiplier;
	reg [5:0]wire_selected_shift;
	reg [15:0]wire_selected_tag;
	wire signed [31:0]wire_quant_accumulator;
	wire [30:0]wire_quant_multiplier;
	wire [5:0]wire_quant_shift;
	wire signed [15:0]wire_saturated;

	// 在接受整批前检查全部有效路，避免先发布好路再发现坏路。
	assign flag_bad_parameters = (i_lane_mask == 3'd0) ||
		(i_lane_mask[0] && (i_pre_multipliers[31] || i_pre_shifts[5:0] == 6'd63)) ||
		(i_lane_mask[1] && (i_pre_multipliers[63] || i_pre_shifts[11:6] == 6'd63)) ||
		(i_lane_mask[2] && (i_pre_multipliers[95] || i_pre_shifts[17:12] == 6'd63)) ||
		(i_activate && (i_post_multiplier[31] || i_post_shift == 6'd63));
	assign o_fault = flag_fatal || flag_table_fault;
	assign o_table_loaded = flag_table_loaded;
	assign o_table_ready = i_rstn && state_current == ST_IDLE && flag_table_ready && !o_fault;
	assign o_input_ready = i_rstn && state_current == ST_IDLE && flag_table_loaded && !o_fault;
	assign wire_emit_lane = reg_emit_mask[0] ? 2'd0 : reg_emit_mask[1] ? 2'd1 : 2'd2;
	assign o_output_valid = i_rstn && state_current == ST_EMIT && !o_fault;
	assign o_output_data = wire_emit_lane == 2'd0 ? reg_result_alpha :
		wire_emit_lane == 2'd1 ? reg_result_beta : reg_result_gamma;
	assign o_output_tag = wire_emit_lane == 2'd0 ? reg_tags[15:0] :
		wire_emit_lane == 2'd1 ? reg_tags[31:16] : reg_tags[47:32];
	assign o_output_int16 = !reg_activate;
	assign flag_quant_send = state_current == ST_PRE_SEND || state_current == ST_POST_SEND;
	assign flag_quant_receive = state_current == ST_PRE_WAIT || state_current == ST_POST_WAIT;
	assign wire_quant_accumulator = wire_selected_accumulator;
	assign wire_quant_multiplier = wire_selected_multiplier;
	assign wire_quant_shift = wire_selected_shift;
	assign wire_saturated = wire_quant_data > 16'sd127 ? 16'sd127 :
		wire_quant_data < -16'sd128 ? -16'sd128 : wire_quant_data;

	// 利用原 SELECT 拍锁存预重定标操作数，无新增拍或接口。
	// SiLU 返回拍直接准备后重定标操作数，移除乘法器前阶段选择器。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			wire_selected_accumulator <= 32'sd0;
			wire_selected_multiplier <= 31'd0;
			wire_selected_shift <= 6'd0;
			wire_selected_tag <= 16'd0;
		end else if (state_current == ST_SELECT) begin
			wire_selected_accumulator <= $signed(reg_accumulators[31:0]);
			wire_selected_multiplier <= reg_pre_multipliers[30:0];
			wire_selected_shift <= reg_pre_shifts[5:0];
			wire_selected_tag <= reg_tags[15:0];
			case (reg_work_mask[0] ? 2'd0 : reg_work_mask[1] ? 2'd1 : 2'd2)
			2'd1: begin
				wire_selected_accumulator <= $signed(reg_accumulators[63:32]);
				wire_selected_multiplier <= reg_pre_multipliers[62:32];
				wire_selected_shift <= reg_pre_shifts[11:6];
				wire_selected_tag <= reg_tags[31:16];
			end
			2'd2: begin
				wire_selected_accumulator <= $signed(reg_accumulators[95:64]);
				wire_selected_multiplier <= reg_pre_multipliers[94:64];
				wire_selected_shift <= reg_pre_shifts[17:12];
				wire_selected_tag <= reg_tags[47:32];
			end
			default: begin
			end
			endcase
		end else if (state_current == ST_SILU_WAIT && flag_silu_valid) begin
			wire_selected_accumulator <= {{16{wire_silu_data[15]}},wire_silu_data};
			wire_selected_multiplier <= reg_post_multiplier;
			wire_selected_shift <= reg_post_shift;
		end
	end

	// 状态寄存与下一状态独立，所有消费均检查实际握手。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			state_current <= ST_IDLE;
		end else begin
			state_current <= state_next;
		end
	end
	always @(*) begin
		state_next = state_current;
		case (state_current)
			ST_IDLE: begin
				if (i_input_valid && o_input_ready && !i_input_fault && !flag_bad_parameters) begin
					state_next = ST_SELECT;
				end
			end
			ST_SELECT: begin
				state_next = reg_work_mask == 3'd0 ? ST_EMIT : ST_PRE_SEND;
			end
			ST_PRE_SEND: begin
				if (flag_quant_ready) begin state_next = ST_PRE_WAIT; end
			end
			ST_PRE_WAIT: begin
				if (flag_quant_valid) begin state_next = reg_activate ? ST_SILU_SEND : ST_SELECT; end
			end
			ST_SILU_SEND: begin
				if (flag_silu_ready) begin state_next = ST_SILU_WAIT; end
			end
			ST_SILU_WAIT: begin
				if (flag_silu_valid) begin state_next = ST_POST_SEND; end
			end
			ST_POST_SEND: begin
				if (flag_quant_ready) begin state_next = ST_POST_WAIT; end
			end
			ST_POST_WAIT: begin
				if (flag_quant_valid) begin state_next = ST_SELECT; end
			end
			ST_EMIT: begin
				if (o_output_valid && i_output_ready && (reg_emit_mask == (3'b001 << wire_emit_lane))) begin
					state_next = ST_IDLE;
				end
			end
			default: begin state_next = ST_IDLE; end
		endcase
	end

	// 保存参数与完整三路结果；故障锁存直到复位，不导出半批。
	always @(posedge i_clk or negedge i_rstn) begin
		if (!i_rstn) begin
			reg_accumulators <= 0; reg_pre_multipliers <= 0; reg_pre_shifts <= 0;
			reg_post_multiplier <= 0; reg_post_shift <= 0; reg_activate <= 0;
			reg_tags <= 0; reg_work_mask <= 0; reg_emit_mask <= 0; reg_lane <= 0;
			reg_scalar <= 0; reg_result_alpha <= 0; reg_result_beta <= 0; reg_result_gamma <= 0;
			flag_fatal <= 0;
		end else begin
			if (flag_quant_valid && flag_quant_receive && (flag_quant_fault || wire_quant_tag != wire_selected_tag)) begin
				flag_fatal <= 1;
			end
			case (state_current)
				ST_IDLE: begin
				if (i_input_valid && o_input_ready) begin
					if (i_input_fault || flag_bad_parameters) begin
						flag_fatal <= 1;
					end else begin
						reg_accumulators <= i_accumulators; reg_pre_multipliers <= i_pre_multipliers;
						reg_pre_shifts <= i_pre_shifts; reg_post_multiplier <= i_post_multiplier[30:0];
						reg_post_shift <= i_post_shift; reg_activate <= i_activate;
						reg_tags <= i_tags; reg_work_mask <= i_lane_mask; reg_emit_mask <= i_lane_mask;
					end
				end
				end
				ST_SELECT: begin
					reg_lane <= reg_work_mask[0] ? 2'd0 : reg_work_mask[1] ? 2'd1 : 2'd2;
				end
				ST_PRE_WAIT: begin
				if (flag_quant_valid && flag_quant_receive) begin
					reg_scalar <= wire_quant_data;
					if (!reg_activate) begin
						reg_work_mask <= reg_work_mask & ~(3'b001 << reg_lane);
						case (reg_lane)
							2'd0: reg_result_alpha <= wire_quant_data;
							2'd1: reg_result_beta <= wire_quant_data;
							default: reg_result_gamma <= wire_quant_data;
						endcase
					end
				end
				end
				ST_SILU_WAIT: begin
					if (flag_silu_valid) begin reg_scalar <= wire_silu_data; end
				end
				ST_POST_WAIT: begin
				if (flag_quant_valid && flag_quant_receive) begin
					reg_work_mask <= reg_work_mask & ~(3'b001 << reg_lane);
					case (reg_lane)
						2'd0: reg_result_alpha <= wire_saturated;
						2'd1: reg_result_beta <= wire_saturated;
						default: reg_result_gamma <= wire_saturated;
					endcase
				end
				end
				ST_EMIT: begin
					if (o_output_valid && i_output_ready) begin
						reg_emit_mask <= reg_emit_mask & ~(3'b001 << wire_emit_lane);
					end
				end
				default: begin
				end
			endcase
		end
	end

	road_dynamic_requant u_dynamic_requant(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_input_valid(flag_quant_send && !o_fault),
		.i_accumulator(wire_quant_accumulator), .i_multiplier(wire_quant_multiplier),
		.i_shift(wire_quant_shift), .i_tag(wire_selected_tag), .o_input_ready(flag_quant_ready),
		.i_output_ready(flag_quant_receive), .o_output_valid(flag_quant_valid),
		.o_output_data(wire_quant_data), .o_output_tag(wire_quant_tag), .o_fault(flag_quant_fault)
	);
	silu_shared_unit u_silu(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_table_valid(i_table_valid && o_table_ready),
		.i_table_addr(i_table_addr), .i_table_data(i_table_data),
		.i_input_valid(state_current == ST_SILU_SEND && !o_fault), .i_input_data(reg_scalar),
		.i_output_ready(state_current == ST_SILU_WAIT), .o_table_ready(flag_table_ready),
		.o_input_ready(flag_silu_ready), .o_output_valid(flag_silu_valid),
		.o_output_data(wire_silu_data), .o_table_loaded(flag_table_loaded), .o_table_fault(flag_table_fault)
	);
endmodule
