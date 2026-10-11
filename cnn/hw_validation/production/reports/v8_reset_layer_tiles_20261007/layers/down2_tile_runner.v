`timescale 1ns / 1ps

// Isolated validation runner for one frozen down2 4x4 output tile.
module down2_tile_runner
(
	input i_clk,
	input i_rstn,
	input i_table_valid,
	input [9:0]i_table_addr,
	input signed [15:0]i_table_data,
	output o_table_ready,
	output o_table_loaded,
	output o_table_fault,
	input i_load_valid,
	input [2:0]i_load_kind,
	input [10:0]i_load_addr,
	input signed [31:0]i_load_data,
	output o_load_ready,
	input i_start,
	input i_pw_only,
	output o_busy,
	output o_done,
	output o_fault,
	input i_export_start,
	input i_output_ready,
	output o_output_valid,
	output signed [7:0]o_output_data,
	output [8:0]o_output_index,
	output o_export_done,
	output o_debug_valid,
	output [1:0]o_debug_phase,
	output o_debug_layer,
	output [3:0]o_debug_position,
	output [4:0]o_debug_channel,
	output signed [31:0]o_debug_value,
	output [31:0]o_preload_writes,
	output [31:0]o_core_cycles,
	output [31:0]o_mac_cycles,
	output [31:0]o_pre_cycles,
	output [31:0]o_silu_cycles,
	output [31:0]o_post_cycles,
	output [31:0]o_writeback_cycles,
	output [31:0]o_storage_wait_cycles,
	output [31:0]o_scheduler_idle_cycles,
	output [31:0]o_export_cycles
);

	localparam [3:0]ST_IDLE = 4'd0;
	localparam [3:0]ST_STORAGE = 4'd1;
	localparam [3:0]ST_MAC_SEND = 4'd2;
	localparam [3:0]ST_MAC_WAIT = 4'd3;
	localparam [3:0]ST_PRE_SEND = 4'd4;
	localparam [3:0]ST_PRE_WAIT = 4'd5;
	localparam [3:0]ST_SILU_SEND = 4'd6;
	localparam [3:0]ST_SILU_WAIT = 4'd7;
	localparam [3:0]ST_POST_SEND = 4'd8;
	localparam [3:0]ST_POST_WAIT = 4'd9;
	localparam [3:0]ST_WRITE = 4'd10;
	localparam [3:0]ST_NEXT = 4'd11;
	localparam [3:0]ST_DONE = 4'd12;
	localparam [3:0]ST_FAULT = 4'd13;
	localparam [3:0]ST_EXPORT = 4'd14;

	localparam signed [31:0]PRE_FACTOR_ALPHA = 32'sd1;
	localparam signed [31:0]PRE_FACTOR_BETA = 32'sd3;
	localparam signed [31:0]PRE_FACTOR_GAMMA = 32'sd5;
	localparam [5:0]PRE_SHIFT_ALPHA = 6'd0;
	localparam [5:0]PRE_SHIFT_BETA = 6'd2;
	localparam [5:0]PRE_SHIFT_GAMMA = 6'd4;
	localparam signed [31:0]POST_FACTOR = 32'sd1;
	localparam [5:0]POST_SHIFT = 6'd4;

	reg signed [7:0]reg_halo [0:1295];
	reg signed [7:0]reg_dw_cache [0:255];
	reg signed [7:0]reg_output_cache [0:383];
	reg signed [7:0]reg_dw_weight [0:143];
	reg signed [31:0]reg_dw_bias [0:15];
	reg signed [7:0]reg_pw_weight [0:383];
	reg signed [31:0]reg_pw_bias [0:23];

	reg [3:0]state_current;
	reg flag_layer_pw;
	reg flag_busy_o;
	reg flag_done_o;
	reg flag_fault_o;
	reg flag_load_fault;
	reg flag_tile_valid;
	reg flag_export_done_o;
	reg [3:0]cnt_position;
	reg [4:0]cnt_output;
	reg cnt_mac_group;
	reg [1:0]cnt_post_slot;
	reg [8:0]cnt_export;

	reg [63:0]reg_mac_activation;
	reg [191:0]reg_mac_weight;
	reg [95:0]reg_mac_bias;
	reg [7:0]reg_mac_mask;
	reg [63:0]next_mac_activation;
	reg [191:0]next_mac_weight;
	reg [95:0]next_mac_bias;
	reg [7:0]next_mac_mask;
	reg [95:0]reg_mac_result;
	reg signed [31:0]reg_accumulator;
	reg signed [15:0]reg_pre_value;
	reg signed [15:0]reg_silu_value;
	reg signed [7:0]reg_post_value;
	reg signed [31:0]reg_pre_factor;
	reg [5:0]reg_pre_shift;
	reg [15:0]reg_round_tag;

	reg flag_debug_valid_o;
	reg [1:0]reg_debug_phase_o;
	reg flag_debug_layer_o;
	reg [3:0]reg_debug_position_o;
	reg [4:0]reg_debug_channel_o;
	reg signed [31:0]reg_debug_value_o;

	reg [31:0]cnt_preload_writes;
	reg [31:0]cnt_core_cycles;
	reg [31:0]cnt_mac_cycles;
	reg [31:0]cnt_pre_cycles;
	reg [31:0]cnt_silu_cycles;
	reg [31:0]cnt_post_cycles;
	reg [31:0]cnt_writeback_cycles;
	reg [31:0]cnt_storage_wait_cycles;
	reg [31:0]cnt_scheduler_idle_cycles;
	reg [31:0]cnt_export_cycles;
	reg [31:0]cnt_dw_core_cycles;
	reg [31:0]cnt_dw_mac_cycles;
	reg [31:0]cnt_dw_pre_cycles;
	reg [31:0]cnt_dw_silu_cycles;
	reg [31:0]cnt_dw_post_cycles;
	reg [31:0]cnt_dw_writeback_cycles;
	reg [31:0]cnt_dw_storage_wait_cycles;
	reg [31:0]cnt_dw_scheduler_idle_cycles;
	reg [31:0]cnt_pw_core_cycles;
	reg [31:0]cnt_pw_mac_cycles;
	reg [31:0]cnt_pw_pre_cycles;
	reg [31:0]cnt_pw_silu_cycles;
	reg [31:0]cnt_pw_post_cycles;
	reg [31:0]cnt_pw_writeback_cycles;
	reg [31:0]cnt_pw_storage_wait_cycles;
	reg [31:0]cnt_pw_scheduler_idle_cycles;
	reg [10:0]cnt_expected_halo;
	reg [8:0]cnt_expected_dw_cache;
	reg [7:0]cnt_expected_dw_weight;
	reg [4:0]cnt_expected_dw_bias;
	reg [8:0]cnt_expected_pw_weight;
	reg [4:0]cnt_expected_pw_bias;
	reg flag_halo_loaded;
	reg flag_dw_cache_loaded;
	reg flag_dw_weight_loaded;
	reg flag_dw_bias_loaded;
	reg flag_pw_weight_loaded;
	reg flag_pw_bias_loaded;

	wire mac_input_ready;
	wire mac_result_valid;
	wire [95:0]mac_result_data;
	wire mac_fault;
	wire round_result_valid;
	wire signed [15:0]round_result_data;
	wire [15:0]round_result_tag;
	wire round_fault;
	wire silu_input_ready;
	wire silu_table_ready;
	wire silu_output_valid;
	wire signed [15:0]silu_output_data;
	wire silu_table_loaded;
	wire silu_table_fault;
	wire signed [63:0]round_product;
	wire [5:0]round_shift;
	wire [15:0]round_tag;
	wire signed [7:0]post_saturated;
	wire [4:0]current_channel;
	wire [4:0]pw_group_base;
	wire [1:0]dw_output_slot;
	wire flag_table_enable;
	wire flag_load_accept;
	wire flag_output_accept;
	wire flag_start_accept;

	integer lane_index;
	integer kernel_index;
	integer halo_index;
	integer weight_index;
	integer output_channel;

	assign pw_group_base = {cnt_output[2:0], 1'b0} + {2'b00, cnt_output[2:0]};
	assign dw_output_slot = ((cnt_output == 5'd0) || (cnt_output == 5'd3) ||
	                         (cnt_output == 5'd6) || (cnt_output == 5'd9) ||
	                         (cnt_output == 5'd12) || (cnt_output == 5'd15)) ? 2'd0 :
	                        ((cnt_output == 5'd1) || (cnt_output == 5'd4) ||
	                         (cnt_output == 5'd7) || (cnt_output == 5'd10) ||
	                         (cnt_output == 5'd13)) ? 2'd1 : 2'd2;
	assign current_channel = flag_layer_pw ? (pw_group_base + {3'd0, cnt_post_slot}) : cnt_output;
	assign post_saturated = ($signed(round_result_data) > 16'sd127) ? 8'sd127 :
	                        ($signed(round_result_data) < -16'sd128) ? -8'sd128 :
	                        round_result_data[7:0];
	assign round_product = (state_current == ST_PRE_SEND) ? ($signed(reg_accumulator) * $signed(reg_pre_factor)) :
	                       ($signed(reg_silu_value) * $signed(POST_FACTOR));
	assign round_shift = (state_current == ST_PRE_SEND) ? reg_pre_shift : POST_SHIFT;
	assign round_tag = reg_round_tag;
	assign flag_table_enable = (state_current == ST_IDLE) && (~i_start) && (~i_export_start);
	assign flag_start_accept = i_start && (~i_table_valid) && (state_current == ST_IDLE) && silu_table_loaded && (~silu_table_fault) &&
	                           (~flag_load_fault) && flag_pw_weight_loaded && flag_pw_bias_loaded &&
	                           (i_pw_only ? flag_dw_cache_loaded : (flag_halo_loaded && flag_dw_weight_loaded && flag_dw_bias_loaded));
	assign flag_load_accept = i_load_valid && o_load_ready;
	assign flag_output_accept = o_output_valid && i_output_ready;

	assign o_table_ready = silu_table_ready && flag_table_enable;
	assign o_table_loaded = silu_table_loaded;
	assign o_table_fault = silu_table_fault;
	assign o_load_ready = (state_current == ST_IDLE) && (~i_start) && (~i_export_start) && (~flag_load_fault);
	assign o_busy = flag_busy_o;
	assign o_done = flag_done_o;
	assign o_fault = flag_fault_o | flag_load_fault | silu_table_fault;
	assign o_output_valid = (state_current == ST_EXPORT);
	assign o_output_data = reg_output_cache[cnt_export];
	assign o_output_index = cnt_export;
	assign o_export_done = flag_export_done_o;
	assign o_debug_valid = flag_debug_valid_o;
	assign o_debug_phase = reg_debug_phase_o;
	assign o_debug_layer = flag_debug_layer_o;
	assign o_debug_position = reg_debug_position_o;
	assign o_debug_channel = reg_debug_channel_o;
	assign o_debug_value = reg_debug_value_o;
	assign o_preload_writes = cnt_preload_writes;
	assign o_core_cycles = cnt_core_cycles;
	assign o_mac_cycles = cnt_mac_cycles;
	assign o_pre_cycles = cnt_pre_cycles;
	assign o_silu_cycles = cnt_silu_cycles;
	assign o_post_cycles = cnt_post_cycles;
	assign o_writeback_cycles = cnt_writeback_cycles;
	assign o_storage_wait_cycles = cnt_storage_wait_cycles;
	assign o_scheduler_idle_cycles = cnt_scheduler_idle_cycles;
	assign o_export_cycles = cnt_export_cycles;

	always@(*)begin
		next_mac_activation = 64'd0;
		next_mac_weight = 192'd0;
		next_mac_bias = 96'd0;
		next_mac_mask = 8'd0;
		kernel_index = 0;
		halo_index = 0;
		weight_index = 0;
		output_channel = 0;
		if(flag_layer_pw == 1'b0)begin
			for(lane_index = 0; lane_index < 8; lane_index = lane_index + 1)begin
				kernel_index = cnt_mac_group * 8 + lane_index;
				if(kernel_index < 9)begin
					halo_index = ((((cnt_position >> 2) * 2 + kernel_index / 3) * 9 +
					              ((cnt_position & 4'h3) * 2 + kernel_index % 3)) * 16 + cnt_output);
					next_mac_activation[lane_index * 8 +:8] = reg_halo[halo_index];
					next_mac_mask[lane_index] = 1'b1;
					weight_index = cnt_output * 9 + kernel_index;
					case(dw_output_slot)
						0: next_mac_weight[lane_index * 8 +:8] = reg_dw_weight[weight_index];
						1: next_mac_weight[64 + lane_index * 8 +:8] = reg_dw_weight[weight_index];
						default: next_mac_weight[128 + lane_index * 8 +:8] = reg_dw_weight[weight_index];
					endcase
				end
			end
			case(dw_output_slot)
				0: next_mac_bias[31:0] = reg_dw_bias[cnt_output];
				1: next_mac_bias[63:32] = reg_dw_bias[cnt_output];
				default: next_mac_bias[95:64] = reg_dw_bias[cnt_output];
			endcase
		end else begin
			for(lane_index = 0; lane_index < 8; lane_index = lane_index + 1)begin
				next_mac_activation[lane_index * 8 +:8] = reg_dw_cache[cnt_position * 16 + cnt_mac_group * 8 + lane_index];
				next_mac_mask[lane_index] = 1'b1;
				output_channel = cnt_output * 3;
				next_mac_weight[lane_index * 8 +:8] = reg_pw_weight[output_channel * 16 + cnt_mac_group * 8 + lane_index];
				next_mac_weight[64 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 1) * 16 + cnt_mac_group * 8 + lane_index];
				next_mac_weight[128 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 2) * 16 + cnt_mac_group * 8 + lane_index];
			end
			next_mac_bias[31:0] = reg_pw_bias[cnt_output * 3];
			next_mac_bias[63:32] = reg_pw_bias[cnt_output * 3 + 1];
			next_mac_bias[95:64] = reg_pw_bias[cnt_output * 3 + 2];
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;
			flag_layer_pw <= 1'b0;
			flag_busy_o <= 1'b0;
			flag_done_o <= 1'b0;
			flag_fault_o <= 1'b0;
			flag_tile_valid <= 1'b0;
			flag_export_done_o <= 1'b0;
			cnt_position <= 4'd0;
			cnt_output <= 5'd0;
			cnt_mac_group <= 1'b0;
			cnt_post_slot <= 2'd0;
			cnt_export <= 9'd0;
			reg_mac_activation <= 64'd0;
			reg_mac_weight <= 192'd0;
			reg_mac_bias <= 96'd0;
			reg_mac_mask <= 8'd0;
			reg_mac_result <= 96'd0;
			reg_accumulator <= 32'sd0;
			reg_pre_value <= 16'sd0;
			reg_silu_value <= 16'sd0;
			reg_post_value <= 8'sd0;
			reg_pre_factor <= PRE_FACTOR_ALPHA;
			reg_pre_shift <= PRE_SHIFT_ALPHA;
			reg_round_tag <= 16'd0;
			flag_debug_valid_o <= 1'b0;
			reg_debug_phase_o <= 2'd0;
			flag_debug_layer_o <= 1'b0;
			reg_debug_position_o <= 4'd0;
			reg_debug_channel_o <= 5'd0;
			reg_debug_value_o <= 32'sd0;
		end else begin
			flag_done_o <= 1'b0;
			flag_export_done_o <= 1'b0;
			flag_debug_valid_o <= 1'b0;
			case(state_current)
				ST_IDLE:begin
					if(flag_start_accept)begin
						flag_layer_pw <= i_pw_only;
						flag_busy_o <= 1'b1;
						flag_fault_o <= 1'b0;
						flag_tile_valid <= 1'b0;
						cnt_position <= 4'd0;
						cnt_output <= 5'd0;
						cnt_mac_group <= 1'b0;
						cnt_post_slot <= 2'd0;
						state_current <= ST_STORAGE;
					end else if(i_export_start && flag_tile_valid)begin
						cnt_export <= 9'd0;
						state_current <= ST_EXPORT;
					end
				end
				ST_STORAGE:begin
					reg_mac_activation <= next_mac_activation;
					reg_mac_weight <= next_mac_weight;
					reg_mac_bias <= next_mac_bias;
					reg_mac_mask <= next_mac_mask;
					state_current <= ST_MAC_SEND;
				end
				ST_MAC_SEND:begin
					if(mac_input_ready)begin
						if(cnt_mac_group == 1'b0)begin
							cnt_mac_group <= 1'b1;
							state_current <= ST_STORAGE;
						end else begin
							state_current <= ST_MAC_WAIT;
						end
					end
				end
				ST_MAC_WAIT:begin
					if(mac_result_valid)begin
						if(mac_fault)begin
							state_current <= ST_FAULT;
						end else begin
							reg_mac_result <= mac_result_data;
							cnt_post_slot <= flag_layer_pw ? 2'd0 : dw_output_slot;
							if(flag_layer_pw)begin
								reg_accumulator <= $signed(mac_result_data[31:0]);
								reg_pre_factor <= PRE_FACTOR_ALPHA;
								reg_pre_shift <= PRE_SHIFT_ALPHA;
								reg_round_tag <= {1'b1, cnt_position, pw_group_base, 6'd1};
							end else begin
								case(dw_output_slot)
									0:begin reg_accumulator <= $signed(mac_result_data[31:0]); reg_pre_factor <= PRE_FACTOR_ALPHA; reg_pre_shift <= PRE_SHIFT_ALPHA; end
									1:begin reg_accumulator <= $signed(mac_result_data[63:32]); reg_pre_factor <= PRE_FACTOR_BETA; reg_pre_shift <= PRE_SHIFT_BETA; end
									default:begin reg_accumulator <= $signed(mac_result_data[95:64]); reg_pre_factor <= PRE_FACTOR_GAMMA; reg_pre_shift <= PRE_SHIFT_GAMMA; end
								endcase
								reg_round_tag <= {1'b0, cnt_position, cnt_output, 6'd1};
							end
							flag_debug_valid_o <= 1'b1;
							reg_debug_phase_o <= 2'd0;
							flag_debug_layer_o <= flag_layer_pw;
							reg_debug_position_o <= cnt_position;
							reg_debug_channel_o <= flag_layer_pw ? cnt_output * 3 : cnt_output;
							if(flag_layer_pw)begin
								reg_debug_value_o <= $signed(mac_result_data[31:0]);
							end else begin
								case(dw_output_slot)
									0: reg_debug_value_o <= $signed(mac_result_data[31:0]);
									1: reg_debug_value_o <= $signed(mac_result_data[63:32]);
									default: reg_debug_value_o <= $signed(mac_result_data[95:64]);
								endcase
							end
							state_current <= ST_PRE_SEND;
						end
					end
				end
				ST_PRE_SEND:begin
					state_current <= ST_PRE_WAIT;
				end
				ST_PRE_WAIT:begin
					if(round_result_valid)begin
						if(round_fault || (round_result_tag != reg_round_tag))begin
							state_current <= ST_FAULT;
						end else begin
							reg_pre_value <= round_result_data;
							flag_debug_valid_o <= 1'b1;
							reg_debug_phase_o <= 2'd1;
							flag_debug_layer_o <= flag_layer_pw;
							reg_debug_position_o <= cnt_position;
							reg_debug_channel_o <= current_channel;
							reg_debug_value_o <= {{16{round_result_data[15]}}, round_result_data};
							state_current <= ST_SILU_SEND;
						end
					end
				end
				ST_SILU_SEND:begin
					if(silu_input_ready)begin
						state_current <= ST_SILU_WAIT;
					end
				end
				ST_SILU_WAIT:begin
					if(silu_output_valid)begin
						reg_silu_value <= silu_output_data;
						reg_round_tag <= {flag_layer_pw, cnt_position, current_channel, 6'd2};
						flag_debug_valid_o <= 1'b1;
						reg_debug_phase_o <= 2'd2;
						flag_debug_layer_o <= flag_layer_pw;
						reg_debug_position_o <= cnt_position;
						reg_debug_channel_o <= current_channel;
						reg_debug_value_o <= {{16{silu_output_data[15]}}, silu_output_data};
						state_current <= ST_POST_SEND;
					end
				end
				ST_POST_SEND:begin
					state_current <= ST_POST_WAIT;
				end
				ST_POST_WAIT:begin
					if(round_result_valid)begin
						if(round_fault || (round_result_tag != reg_round_tag))begin
							state_current <= ST_FAULT;
						end else begin
							reg_post_value <= post_saturated;
							flag_debug_valid_o <= 1'b1;
							reg_debug_phase_o <= 2'd3;
							flag_debug_layer_o <= flag_layer_pw;
							reg_debug_position_o <= cnt_position;
							reg_debug_channel_o <= current_channel;
							reg_debug_value_o <= {{16{round_result_data[15]}}, round_result_data};
							state_current <= ST_WRITE;
						end
					end
				end
				ST_WRITE:begin
					if(flag_layer_pw)begin
						reg_output_cache[cnt_position * 24 + current_channel] <= reg_post_value;
					end else begin
						reg_dw_cache[cnt_position * 16 + cnt_output] <= reg_post_value;
					end
					state_current <= ST_NEXT;
				end
				ST_NEXT:begin
					if(flag_layer_pw == 1'b0)begin
						cnt_mac_group <= 1'b0;
						if(cnt_output < 5'd15)begin
							cnt_output <= cnt_output + 1'b1;
							state_current <= ST_STORAGE;
						end else if(cnt_position < 4'd15)begin
							cnt_position <= cnt_position + 1'b1;
							cnt_output <= 5'd0;
							state_current <= ST_STORAGE;
						end else begin
							flag_layer_pw <= 1'b1;
							cnt_position <= 4'd0;
							cnt_output <= 5'd0;
							cnt_post_slot <= 2'd0;
							state_current <= ST_STORAGE;
						end
					end else if(cnt_post_slot < 2'd2)begin
						cnt_post_slot <= cnt_post_slot + 1'b1;
						case(cnt_post_slot)
							2'd0:begin reg_accumulator <= $signed(reg_mac_result[63:32]); reg_pre_factor <= PRE_FACTOR_BETA; reg_pre_shift <= PRE_SHIFT_BETA; end
							default:begin reg_accumulator <= $signed(reg_mac_result[95:64]); reg_pre_factor <= PRE_FACTOR_GAMMA; reg_pre_shift <= PRE_SHIFT_GAMMA; end
						endcase
						reg_round_tag <= {1'b1, cnt_position, pw_group_base + {3'd0, cnt_post_slot} + 5'd1, 6'd1};
						flag_debug_valid_o <= 1'b1;
						reg_debug_phase_o <= 2'd0;
						flag_debug_layer_o <= 1'b1;
						reg_debug_position_o <= cnt_position;
						reg_debug_channel_o <= pw_group_base + {3'd0, cnt_post_slot} + 5'd1;
						reg_debug_value_o <= (cnt_post_slot == 2'd0) ? $signed(reg_mac_result[63:32]) : $signed(reg_mac_result[95:64]);
						state_current <= ST_PRE_SEND;
					end else begin
						cnt_mac_group <= 1'b0;
						cnt_post_slot <= 2'd0;
						if(cnt_output < 5'd7)begin
							cnt_output <= cnt_output + 1'b1;
							state_current <= ST_STORAGE;
						end else if(cnt_position < 4'd15)begin
							cnt_position <= cnt_position + 1'b1;
							cnt_output <= 5'd0;
							state_current <= ST_STORAGE;
						end else begin
							state_current <= ST_DONE;
						end
					end
				end
				ST_DONE:begin
					flag_busy_o <= 1'b0;
					flag_done_o <= 1'b1;
					flag_tile_valid <= 1'b1;
					state_current <= ST_IDLE;
				end
				ST_FAULT:begin
					flag_busy_o <= 1'b0;
					flag_fault_o <= 1'b1;
					flag_tile_valid <= 1'b0;
					state_current <= ST_IDLE;
				end
				ST_EXPORT:begin
					if(flag_output_accept)begin
						if(cnt_export == 9'd383)begin
							flag_export_done_o <= 1'b1;
							state_current <= ST_IDLE;
						end else begin
							cnt_export <= cnt_export + 1'b1;
						end
					end
				end
				default:begin
					flag_busy_o <= 1'b0;
					flag_fault_o <= 1'b1;
					state_current <= ST_IDLE;
				end
			endcase
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_dw_core_cycles <= 32'd0;
			cnt_dw_mac_cycles <= 32'd0;
			cnt_dw_pre_cycles <= 32'd0;
			cnt_dw_silu_cycles <= 32'd0;
			cnt_dw_post_cycles <= 32'd0;
			cnt_dw_writeback_cycles <= 32'd0;
			cnt_dw_storage_wait_cycles <= 32'd0;
			cnt_dw_scheduler_idle_cycles <= 32'd0;
			cnt_pw_core_cycles <= 32'd0;
			cnt_pw_mac_cycles <= 32'd0;
			cnt_pw_pre_cycles <= 32'd0;
			cnt_pw_silu_cycles <= 32'd0;
			cnt_pw_post_cycles <= 32'd0;
			cnt_pw_writeback_cycles <= 32'd0;
			cnt_pw_storage_wait_cycles <= 32'd0;
			cnt_pw_scheduler_idle_cycles <= 32'd0;
		end else if(flag_start_accept)begin
			cnt_dw_core_cycles <= 32'd0;
			cnt_dw_mac_cycles <= 32'd0;
			cnt_dw_pre_cycles <= 32'd0;
			cnt_dw_silu_cycles <= 32'd0;
			cnt_dw_post_cycles <= 32'd0;
			cnt_dw_writeback_cycles <= 32'd0;
			cnt_dw_storage_wait_cycles <= 32'd0;
			cnt_dw_scheduler_idle_cycles <= 32'd0;
			cnt_pw_core_cycles <= 32'd0;
			cnt_pw_mac_cycles <= 32'd0;
			cnt_pw_pre_cycles <= 32'd0;
			cnt_pw_silu_cycles <= 32'd0;
			cnt_pw_post_cycles <= 32'd0;
			cnt_pw_writeback_cycles <= 32'd0;
			cnt_pw_storage_wait_cycles <= 32'd0;
			cnt_pw_scheduler_idle_cycles <= 32'd0;
		end else if(flag_busy_o)begin
			if(flag_layer_pw)begin
				cnt_pw_core_cycles <= cnt_pw_core_cycles + 1'b1;
				case(state_current)
					ST_MAC_SEND, ST_MAC_WAIT: cnt_pw_mac_cycles <= cnt_pw_mac_cycles + 1'b1;
					ST_PRE_SEND, ST_PRE_WAIT: cnt_pw_pre_cycles <= cnt_pw_pre_cycles + 1'b1;
					ST_SILU_SEND, ST_SILU_WAIT: cnt_pw_silu_cycles <= cnt_pw_silu_cycles + 1'b1;
					ST_POST_SEND, ST_POST_WAIT: cnt_pw_post_cycles <= cnt_pw_post_cycles + 1'b1;
					ST_WRITE: cnt_pw_writeback_cycles <= cnt_pw_writeback_cycles + 1'b1;
					ST_STORAGE: cnt_pw_storage_wait_cycles <= cnt_pw_storage_wait_cycles + 1'b1;
					default: cnt_pw_scheduler_idle_cycles <= cnt_pw_scheduler_idle_cycles + 1'b1;
				endcase
			end else begin
				cnt_dw_core_cycles <= cnt_dw_core_cycles + 1'b1;
				case(state_current)
					ST_MAC_SEND, ST_MAC_WAIT: cnt_dw_mac_cycles <= cnt_dw_mac_cycles + 1'b1;
					ST_PRE_SEND, ST_PRE_WAIT: cnt_dw_pre_cycles <= cnt_dw_pre_cycles + 1'b1;
					ST_SILU_SEND, ST_SILU_WAIT: cnt_dw_silu_cycles <= cnt_dw_silu_cycles + 1'b1;
					ST_POST_SEND, ST_POST_WAIT: cnt_dw_post_cycles <= cnt_dw_post_cycles + 1'b1;
					ST_WRITE: cnt_dw_writeback_cycles <= cnt_dw_writeback_cycles + 1'b1;
					ST_STORAGE: cnt_dw_storage_wait_cycles <= cnt_dw_storage_wait_cycles + 1'b1;
					default: cnt_dw_scheduler_idle_cycles <= cnt_dw_scheduler_idle_cycles + 1'b1;
				endcase
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_preload_writes <= 32'd0;
			cnt_expected_halo <= 11'd0;
			cnt_expected_dw_cache <= 9'd0;
			cnt_expected_dw_weight <= 8'd0;
			cnt_expected_dw_bias <= 5'd0;
			cnt_expected_pw_weight <= 9'd0;
			cnt_expected_pw_bias <= 5'd0;
			flag_halo_loaded <= 1'b0;
			flag_dw_cache_loaded <= 1'b0;
			flag_dw_weight_loaded <= 1'b0;
			flag_dw_bias_loaded <= 1'b0;
			flag_pw_weight_loaded <= 1'b0;
			flag_pw_bias_loaded <= 1'b0;
			flag_load_fault <= 1'b0;
		end else if(flag_load_accept)begin
			cnt_preload_writes <= cnt_preload_writes + 1'b1;
			case(i_load_kind)
				3'd0:begin
					if((i_load_addr == cnt_expected_halo) || (i_load_addr == 11'd0))begin
						reg_halo[i_load_addr] <= i_load_data[7:0];
						flag_halo_loaded <= (i_load_addr == 11'd1295);
						cnt_expected_halo <= (i_load_addr == 11'd1295) ? 11'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				3'd1:begin
					if((i_load_addr == cnt_expected_dw_cache) || (i_load_addr == 11'd0))begin
						reg_dw_cache[i_load_addr] <= i_load_data[7:0];
						flag_dw_cache_loaded <= (i_load_addr == 11'd255);
						cnt_expected_dw_cache <= (i_load_addr == 11'd255) ? 9'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				3'd2:begin
					if((i_load_addr == cnt_expected_dw_weight) || (i_load_addr == 11'd0))begin
						reg_dw_weight[i_load_addr] <= i_load_data[7:0];
						flag_dw_weight_loaded <= (i_load_addr == 11'd143);
						cnt_expected_dw_weight <= (i_load_addr == 11'd143) ? 8'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				3'd3:begin
					if((i_load_addr == cnt_expected_dw_bias) || (i_load_addr == 11'd0))begin
						reg_dw_bias[i_load_addr] <= i_load_data;
						flag_dw_bias_loaded <= (i_load_addr == 11'd15);
						cnt_expected_dw_bias <= (i_load_addr == 11'd15) ? 5'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				3'd4:begin
					if((i_load_addr == cnt_expected_pw_weight) || (i_load_addr == 11'd0))begin
						reg_pw_weight[i_load_addr] <= i_load_data[7:0];
						flag_pw_weight_loaded <= (i_load_addr == 11'd383);
						cnt_expected_pw_weight <= (i_load_addr == 11'd383) ? 9'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				3'd5:begin
					if((i_load_addr == cnt_expected_pw_bias) || (i_load_addr == 11'd0))begin
						reg_pw_bias[i_load_addr] <= i_load_data;
						flag_pw_bias_loaded <= (i_load_addr == 11'd23);
						cnt_expected_pw_bias <= (i_load_addr == 11'd23) ? 5'd0 : i_load_addr + 1'b1;
					end else begin flag_load_fault <= 1'b1; end
				end
				default: flag_load_fault <= 1'b1;
			endcase
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_core_cycles <= 32'd0;
			cnt_mac_cycles <= 32'd0;
			cnt_pre_cycles <= 32'd0;
			cnt_silu_cycles <= 32'd0;
			cnt_post_cycles <= 32'd0;
			cnt_writeback_cycles <= 32'd0;
			cnt_storage_wait_cycles <= 32'd0;
			cnt_scheduler_idle_cycles <= 32'd0;
			cnt_export_cycles <= 32'd0;
		end else begin
			if(flag_start_accept)begin
				cnt_core_cycles <= 32'd0;
				cnt_mac_cycles <= 32'd0;
				cnt_pre_cycles <= 32'd0;
				cnt_silu_cycles <= 32'd0;
				cnt_post_cycles <= 32'd0;
				cnt_writeback_cycles <= 32'd0;
				cnt_storage_wait_cycles <= 32'd0;
				cnt_scheduler_idle_cycles <= 32'd0;
			end else if(flag_busy_o)begin
				cnt_core_cycles <= cnt_core_cycles + 1'b1;
				case(state_current)
					ST_MAC_SEND, ST_MAC_WAIT: cnt_mac_cycles <= cnt_mac_cycles + 1'b1;
					ST_PRE_SEND, ST_PRE_WAIT: cnt_pre_cycles <= cnt_pre_cycles + 1'b1;
					ST_SILU_SEND, ST_SILU_WAIT: cnt_silu_cycles <= cnt_silu_cycles + 1'b1;
					ST_POST_SEND, ST_POST_WAIT: cnt_post_cycles <= cnt_post_cycles + 1'b1;
					ST_WRITE: cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1;
					ST_STORAGE: cnt_storage_wait_cycles <= cnt_storage_wait_cycles + 1'b1;
					default: cnt_scheduler_idle_cycles <= cnt_scheduler_idle_cycles + 1'b1;
				endcase
			end
			if(i_export_start && (state_current == ST_IDLE))begin
				cnt_export_cycles <= 32'd0;
			end else if(state_current == ST_EXPORT)begin
				cnt_export_cycles <= cnt_export_cycles + 1'b1;
			end
		end
	end

	road_mac_probe road_mac_probe_Inst_tile(
		.i_clk(i_clk), .i_rstn(i_rstn),
		.i_input_valid(state_current == ST_MAC_SEND),
		.i_first(cnt_mac_group == 1'b0), .i_last(cnt_mac_group == 1'b1),
		.i_lane_mask(reg_mac_mask), .i_activation_data(reg_mac_activation),
		.i_weight_data(reg_mac_weight), .i_bias_data(reg_mac_bias),
		.i_result_ready(state_current == ST_MAC_WAIT),
		.o_input_ready(mac_input_ready), .o_result_valid(mac_result_valid),
		.o_result_data(mac_result_data), .o_fault(mac_fault)
	);

	road_round_shift road_round_shift_Inst_tile(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_advance(1'b1),
		.i_input_valid((state_current == ST_PRE_SEND) || (state_current == ST_POST_SEND)),
		.i_product(round_product), .i_shift(round_shift), .i_tag(round_tag),
		.o_result_valid(round_result_valid), .o_result_data(round_result_data),
		.o_result_tag(round_result_tag), .o_fault(round_fault)
	);

	silu_shared_unit silu_shared_unit_Inst_tile(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_table_valid(i_table_valid && flag_table_enable),
		.i_table_addr(i_table_addr), .i_table_data(i_table_data),
		.i_input_valid(state_current == ST_SILU_SEND), .i_input_data(reg_pre_value),
		.i_output_ready(state_current == ST_SILU_WAIT), .o_table_ready(silu_table_ready),
		.o_input_ready(silu_input_ready), .o_output_valid(silu_output_valid),
		.o_output_data(silu_output_data), .o_table_loaded(silu_table_loaded),
		.o_table_fault(silu_table_fault)
	);

endmodule
