`timescale 1ns / 1ps

// Isolated overlap runner for one frozen down2 4x4 output tile.
module down2_overlap_tile_runner
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
	input i_commit_ready,
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
	output [31:0]o_export_cycles,
	output [1:0]o_result_queue_count,
	output o_result_reserved,
	output [3:0]o_meta_count,
	output [31:0]o_mac_result_count,
	output [31:0]o_pre_accept_count,
	output [31:0]o_silu_accept_count,
	output [31:0]o_post_accept_count,
	output [31:0]o_writeback_count
);

	localparam [3:0]ST_IDLE = 4'd0;
	localparam [3:0]ST_STORAGE = 4'd1;
	localparam [3:0]ST_MAC_SEND = 4'd2;
	localparam [3:0]ST_MAC_WAIT = 4'd3;
	localparam [3:0]ST_DW_DRAIN = 4'd4;
	localparam [3:0]ST_PW_DRAIN = 4'd5;
	localparam [3:0]ST_DONE = 4'd6;
	localparam [3:0]ST_FAULT = 4'd7;
	localparam [3:0]ST_EXPORT = 4'd8;
	localparam [3:0]ST_DW_POST = 4'd9;

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
	reg flag_result_reserved;
	reg [3:0]cnt_position;
	reg [4:0]cnt_output;
	reg [1:0]cnt_mac_group;
	reg [8:0]cnt_export;
	reg [8:0]cnt_dw_writes;
	reg [8:0]cnt_pw_writes;
	reg [95:0]reg_dw_triplet_result;
	reg [1:0]cnt_dw_post_lane;

	reg [63:0]reg_mac_activation;
	reg [191:0]reg_mac_weight;
	reg [95:0]reg_mac_bias;
	reg [7:0]reg_mac_mask;
	reg [63:0]next_mac_activation;
	reg [191:0]next_mac_weight;
	reg [95:0]next_mac_bias;
	reg [7:0]next_mac_mask;

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
	reg [31:0]cnt_mac_results;
	reg [31:0]cnt_pre_accepts;
	reg [31:0]cnt_silu_accepts;
	reg [31:0]cnt_post_accepts;
	reg [31:0]cnt_writebacks;
	reg flag_cnt_output_clear;
	reg flag_cnt_output_increment;

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
	wire flag_mac_input_valid;
	wire flag_mac_input_accept;
	wire flag_mac_result_ready_local;
	wire flag_mac_result_accept;
	wire flag_can_reserve;

	wire pp_input_ready;
	wire pp_output_valid;
	wire signed [7:0]pp_output_data;
	wire [15:0]pp_output_tag;
	wire pp_fault;
	wire [1:0]pp_result_queue_count;
	wire [3:0]pp_meta_count;
	wire pp_pre_busy;
	wire pp_silu_busy;
	wire pp_post_busy;
	wire pp_pre_accept;
	wire pp_silu_accept;
	wire pp_post_accept;
	wire pp_table_ready;
	wire pp_table_loaded;
	wire pp_table_fault;
	wire flag_commit_accept;

	wire [4:0]wire_pw_group_base;
	wire [1:0]wire_mac_prepare_group;
	wire [1:0]wire_dw_lane;
	wire [4:0]wire_dw_channel_base;
	wire [2:0]wire_result_lane_mask;
	wire [4:0]wire_result_channel_base;
	wire [1:0]wire_dw_post_count;
	wire signed [31:0]wire_dw_post_scalar;
	wire [95:0]wire_pp_result_data;
	wire [3:0]wire_pp_position;
	wire flag_pp_input_valid;
	wire flag_pp_input_accept;
	wire flag_mac_last_group;
	wire flag_table_enable;
	wire flag_load_accept;
	wire flag_output_accept;
	wire flag_start_accept;
	wire flag_halo_load_write;
	wire flag_dw_cache_load_address_valid;
	wire flag_dw_cache_load_write;
	wire flag_dw_cache_commit_address_valid;
	wire flag_dw_cache_commit_write;
	wire flag_dw_cache_write;
	wire [8:0]wire_dw_cache_commit_address_full;
	wire [7:0]wire_dw_cache_write_address;
	wire signed [7:0]wire_dw_cache_write_data;

	integer lane_index;
	integer kernel_index;
	integer halo_index;
	integer weight_index;
	integer output_channel;
	integer union_row;
	integer union_column;
	integer halo_row;
	integer halo_column;
	integer spatial_lane;

	assign wire_pw_group_base = {cnt_output[2:0], 1'b0} + {2'b00, cnt_output[2:0]};
	assign wire_mac_prepare_group = (flag_layer_pw && (state_current == ST_MAC_SEND) &&
	                                 (cnt_mac_group == 2'd0)) ? 2'd1 : cnt_mac_group;
	assign wire_dw_lane = ((cnt_output == 5'd0) || (cnt_output == 5'd3) ||
	                       (cnt_output == 5'd6) || (cnt_output == 5'd9) ||
	                       (cnt_output == 5'd12) || (cnt_output == 5'd15)) ? 2'd0 :
	                      ((cnt_output == 5'd1) || (cnt_output == 5'd4) ||
	                       (cnt_output == 5'd7) || (cnt_output == 5'd10) ||
	                       (cnt_output == 5'd13)) ? 2'd1 : 2'd2;
	assign wire_dw_channel_base = cnt_output - {3'd0, wire_dw_lane};
	assign wire_result_lane_mask = flag_layer_pw ? 3'b111 : (3'b001 << wire_dw_lane);
	assign wire_result_channel_base = flag_layer_pw ? wire_pw_group_base : wire_dw_channel_base;
	assign wire_dw_post_count = (cnt_position[1:0] == 2'd0) ? 2'd3 : 2'd1;
	assign wire_dw_post_scalar = (cnt_dw_post_lane == 2'd0) ? $signed(reg_dw_triplet_result[31:0]) :
	                                  (cnt_dw_post_lane == 2'd1) ? $signed(reg_dw_triplet_result[63:32]) :
	                                                                       $signed(reg_dw_triplet_result[95:64]);
	assign wire_pp_result_data = flag_layer_pw ? mac_result_data :
	                             (wire_dw_lane == 2'd0) ? {64'd0, wire_dw_post_scalar} :
	                             (wire_dw_lane == 2'd1) ? {32'd0, wire_dw_post_scalar, 32'd0} :
	                                                        {wire_dw_post_scalar, 64'd0};
	assign wire_pp_position = flag_layer_pw ? cnt_position : cnt_position + cnt_dw_post_lane;
	assign flag_can_reserve = (flag_result_reserved == 1'b0) ?
	                          ((pp_result_queue_count < 2'd2) && (~pp_fault)) :
	                          ((~flag_result_reserved) && (~pp_fault));
	assign flag_mac_last_group = flag_layer_pw ? (cnt_mac_group == 2'd1) :
	                                               (cnt_mac_group == 2'd2);
	assign flag_mac_input_valid = (state_current == ST_MAC_SEND) &&
	                              ((cnt_mac_group != 2'd0) || flag_can_reserve);
	assign flag_mac_input_accept = flag_mac_input_valid && mac_input_ready;
	assign flag_mac_result_ready_local = (state_current == ST_MAC_WAIT) && flag_result_reserved &&
	                                     (flag_layer_pw ? ((pp_result_queue_count < 2'd2) &&
	                                                       pp_table_loaded && (~pp_fault)) : (~pp_fault));
	assign flag_mac_result_accept = mac_result_valid && flag_mac_result_ready_local;
	assign flag_pp_input_valid = flag_layer_pw ?
	                             ((state_current == ST_MAC_WAIT) && flag_result_reserved && mac_result_valid) :
	                             ((state_current == ST_DW_POST) && flag_result_reserved &&
	                              (pp_result_queue_count < 2'd2));
	assign flag_pp_input_accept = flag_pp_input_valid && pp_input_ready;
	assign flag_commit_accept = pp_output_valid && i_commit_ready && flag_busy_o;
	assign flag_table_enable = (state_current == ST_IDLE) && (~i_start) && (~i_export_start);
	assign flag_load_accept = i_load_valid && o_load_ready;
	assign flag_output_accept = o_output_valid && i_output_ready;
	assign flag_start_accept = i_start && (~i_table_valid) && (state_current == ST_IDLE) &&
	                           pp_table_loaded && (~pp_fault) && (~flag_load_fault) &&
	                           flag_pw_weight_loaded && flag_pw_bias_loaded &&
	                           (i_pw_only ? flag_dw_cache_loaded :
	                           (flag_halo_loaded && flag_dw_weight_loaded && flag_dw_bias_loaded));
	assign flag_halo_load_write = flag_load_accept && (i_load_kind == 3'd0) &&
	                              ((i_load_addr == cnt_expected_halo) || (i_load_addr == 11'd0));
	assign flag_dw_cache_load_address_valid = (i_load_addr <= 11'd255);
	assign flag_dw_cache_load_write = flag_load_accept && (i_load_kind == 3'd1) &&
	                                  flag_dw_cache_load_address_valid &&
	                                  ((i_load_addr == cnt_expected_dw_cache) || (i_load_addr == 11'd0));
	assign wire_dw_cache_commit_address_full = {1'b0, pp_output_tag[14:11], 4'b0} +
	                                           {4'd0, pp_output_tag[10:6]};
	assign flag_dw_cache_commit_address_valid = (wire_dw_cache_commit_address_full <= 9'd255);
	assign flag_dw_cache_commit_write = flag_commit_accept && (~pp_output_tag[15]) &&
	                                    flag_dw_cache_commit_address_valid;
	assign flag_dw_cache_write = flag_dw_cache_commit_write || flag_dw_cache_load_write;
	assign wire_dw_cache_write_address = flag_dw_cache_commit_write ?
	                                     wire_dw_cache_commit_address_full[7:0] : i_load_addr[7:0];
	assign wire_dw_cache_write_data = flag_dw_cache_commit_write ? pp_output_data : i_load_data[7:0];

	assign o_table_ready = pp_table_ready && flag_table_enable;
	assign o_table_loaded = pp_table_loaded;
	assign o_table_fault = pp_table_fault;
	assign o_load_ready = (state_current == ST_IDLE) && (~i_start) && (~i_export_start) &&
	                      (~flag_load_fault) && (~pp_fault);
	assign o_busy = flag_busy_o;
	assign o_done = flag_done_o;
	assign o_fault = flag_fault_o || flag_load_fault || pp_fault;
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
	assign o_result_queue_count = pp_result_queue_count;
	assign o_result_reserved = flag_result_reserved;
	assign o_meta_count = pp_meta_count;
	assign o_mac_result_count = cnt_mac_results;
	assign o_pre_accept_count = cnt_pre_accepts;
	assign o_silu_accept_count = cnt_silu_accepts;
	assign o_post_accept_count = cnt_post_accepts;
	assign o_writeback_count = cnt_writebacks;

	always@(*)begin
		next_mac_activation = 64'd0;
		next_mac_weight = 192'd0;
		next_mac_bias = 96'd0;
		next_mac_mask = 8'd0;
		kernel_index = 0;
		halo_index = 0;
		weight_index = 0;
		output_channel = 0;
		union_row = 0;
		union_column = 0;
		halo_row = 0;
		halo_column = 0;
		spatial_lane = 0;
		if(flag_layer_pw == 1'b0)begin
			for(lane_index = 0; lane_index < 8; lane_index = lane_index + 1)begin
				kernel_index = cnt_mac_group * 8 + lane_index;
				if(kernel_index < 21)begin
					union_row = kernel_index / 7;
					union_column = kernel_index % 7;
					halo_row = ((cnt_position >> 2) * 2) + union_row;
					halo_column = ((cnt_position & 4'h3) * 2) + union_column;
					if(halo_column < 9)begin
						halo_index = (halo_row * 9 + halo_column) * 16 + cnt_output;
						next_mac_activation[lane_index * 8 +:8] = reg_halo[halo_index];
					end
					next_mac_mask[lane_index] = 1'b1;
					for(spatial_lane = 0; spatial_lane < 3; spatial_lane = spatial_lane + 1)begin
						if((spatial_lane < wire_dw_post_count) &&
						   (union_column >= spatial_lane * 2) &&
						   (union_column < spatial_lane * 2 + 3))begin
							weight_index = cnt_output * 9 + union_row * 3 +
							               union_column - spatial_lane * 2;
							next_mac_weight[spatial_lane * 64 + lane_index * 8 +:8] =
								reg_dw_weight[weight_index];
						end
					end
				end
			end
			next_mac_bias[31:0] = reg_dw_bias[cnt_output];
			if(cnt_position[1:0] == 2'd0)begin
				next_mac_bias[63:32] = next_mac_bias[31:0];
				next_mac_bias[95:64] = next_mac_bias[31:0];
			end
		end else begin
			for(lane_index = 0; lane_index < 8; lane_index = lane_index + 1)begin
				next_mac_activation[lane_index * 8 +:8] = reg_dw_cache[cnt_position * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_mask[lane_index] = 1'b1;
				output_channel = cnt_output * 3;
				next_mac_weight[lane_index * 8 +:8] = reg_pw_weight[output_channel * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_weight[64 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 1) * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_weight[128 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 2) * 16 + wire_mac_prepare_group * 8 + lane_index];
			end
			next_mac_bias[31:0] = reg_pw_bias[cnt_output * 3];
			next_mac_bias[63:32] = reg_pw_bias[cnt_output * 3 + 1];
			next_mac_bias[95:64] = reg_pw_bias[cnt_output * 3 + 2];
		end
	end

	always@(*)begin
		flag_cnt_output_clear = 1'b0;
		flag_cnt_output_increment = 1'b0;
		case(state_current)
			ST_IDLE:begin
				if(flag_start_accept)begin
					flag_cnt_output_clear = 1'b1;
				end
			end
			ST_MAC_WAIT:begin
				if(flag_mac_result_accept)begin
					if(mac_fault)begin
					end else if(flag_layer_pw == 1'b0)begin
					end else begin
						if(cnt_output < 5'd7)begin
							flag_cnt_output_increment = 1'b1;
						end else if(cnt_position < 4'd15)begin
							flag_cnt_output_clear = 1'b1;
						end
					end
				end
			end
			ST_DW_POST:begin
				if(flag_pp_input_accept)begin
					if(cnt_dw_post_lane + 1'b1 == wire_dw_post_count)begin
						if(cnt_output < 5'd15)begin
							flag_cnt_output_increment = 1'b1;
						end else if(cnt_position[1:0] == 2'd0)begin
							flag_cnt_output_clear = 1'b1;
						end else if(cnt_position < 4'd15)begin
							flag_cnt_output_clear = 1'b1;
						end
					end
				end
			end
			ST_DW_DRAIN:begin
				if(cnt_dw_writes == 9'd256)begin
					flag_cnt_output_clear = 1'b1;
				end
			end
			default:begin
				flag_cnt_output_clear = 1'b0;
				flag_cnt_output_increment = 1'b0;
			end
		endcase
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
			flag_result_reserved <= 1'b0;
			cnt_position <= 4'd0;
			cnt_mac_group <= 2'd0;
			cnt_export <= 9'd0;
			cnt_dw_writes <= 9'd0;
			cnt_pw_writes <= 9'd0;
			reg_dw_triplet_result <= 96'd0;
			cnt_dw_post_lane <= 2'd0;
			reg_mac_activation <= 64'd0;
			reg_mac_weight <= 192'd0;
			reg_mac_bias <= 96'd0;
			reg_mac_mask <= 8'd0;
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
			if(pp_fault || flag_load_fault)begin
				flag_busy_o <= 1'b0;
				flag_fault_o <= 1'b1;
				flag_tile_valid <= 1'b0;
				flag_result_reserved <= 1'b0;
				state_current <= ST_FAULT;
			end else begin
				if(flag_commit_accept)begin
					flag_debug_valid_o <= 1'b1;
					reg_debug_phase_o <= 2'd3;
					flag_debug_layer_o <= pp_output_tag[15];
					reg_debug_position_o <= pp_output_tag[14:11];
					reg_debug_channel_o <= pp_output_tag[10:6];
					reg_debug_value_o <= {{24{pp_output_data[7]}}, pp_output_data};
					if(pp_output_tag[15])begin
						cnt_pw_writes <= cnt_pw_writes + 1'b1;
					end else begin
						cnt_dw_writes <= cnt_dw_writes + 1'b1;
					end
				end
				case(state_current)
					ST_IDLE:begin
						if(flag_start_accept)begin
							flag_layer_pw <= i_pw_only;
							flag_busy_o <= 1'b1;
							flag_fault_o <= 1'b0;
							flag_tile_valid <= 1'b0;
							flag_result_reserved <= 1'b0;
							cnt_position <= 4'd0;
							cnt_mac_group <= 2'd0;
							cnt_dw_writes <= 9'd0;
							cnt_pw_writes <= 9'd0;
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
						if(flag_mac_input_accept)begin
							if(cnt_mac_group == 2'd0)begin
								flag_result_reserved <= 1'b1;
							end
							if(flag_mac_last_group)begin
								state_current <= ST_MAC_WAIT;
							end else begin
								cnt_mac_group <= cnt_mac_group + 1'b1;
								if(flag_layer_pw)begin
									reg_mac_activation <= next_mac_activation;
									reg_mac_weight <= next_mac_weight;
									reg_mac_bias <= next_mac_bias;
									reg_mac_mask <= next_mac_mask;
									state_current <= ST_MAC_SEND;
								end else begin
									state_current <= ST_STORAGE;
								end
							end
						end
					end
					ST_MAC_WAIT:begin
						if(flag_mac_result_accept)begin
							cnt_mac_group <= 2'd0;
							if(mac_fault)begin
								flag_result_reserved <= 1'b0;
								flag_busy_o <= 1'b0;
								flag_fault_o <= 1'b1;
								flag_tile_valid <= 1'b0;
								state_current <= ST_FAULT;
							end else if(flag_layer_pw == 1'b0)begin
								reg_dw_triplet_result <= mac_result_data;
								cnt_dw_post_lane <= 2'd0;
								state_current <= ST_DW_POST;
							end else begin
								flag_result_reserved <= 1'b0;
								flag_debug_valid_o <= 1'b1;
								reg_debug_phase_o <= 2'd0;
								flag_debug_layer_o <= 1'b1;
								reg_debug_position_o <= cnt_position;
								reg_debug_channel_o <= wire_result_channel_base;
								reg_debug_value_o <= $signed(mac_result_data[31:0]);
								if(cnt_output < 5'd7)begin
									state_current <= ST_STORAGE;
								end else if(cnt_position < 4'd15)begin
									cnt_position <= cnt_position + 1'b1;
									state_current <= ST_STORAGE;
								end else begin
									state_current <= ST_PW_DRAIN;
								end
							end
						end
					end
					ST_DW_POST:begin
						if(flag_pp_input_accept)begin
							flag_debug_valid_o <= 1'b1;
							reg_debug_phase_o <= 2'd0;
							flag_debug_layer_o <= 1'b0;
							reg_debug_position_o <= wire_pp_position;
							reg_debug_channel_o <= cnt_output;
							reg_debug_value_o <= wire_dw_post_scalar;
							if(cnt_dw_post_lane + 1'b1 == wire_dw_post_count)begin
								flag_result_reserved <= 1'b0;
								cnt_dw_post_lane <= 2'd0;
								if(cnt_output < 5'd15)begin
									state_current <= ST_STORAGE;
								end else if(cnt_position[1:0] == 2'd0)begin
									cnt_position <= cnt_position + 2'd3;
									state_current <= ST_STORAGE;
								end else if(cnt_position < 4'd15)begin
									cnt_position <= cnt_position + 1'b1;
									state_current <= ST_STORAGE;
								end else begin
									state_current <= ST_DW_DRAIN;
								end
							end else begin
								cnt_dw_post_lane <= cnt_dw_post_lane + 1'b1;
							end
						end
					end
					ST_DW_DRAIN:begin
					if(cnt_dw_writes == 9'd256)begin
						flag_layer_pw <= 1'b1;
						cnt_position <= 4'd0;
						cnt_mac_group <= 2'd0;
							state_current <= ST_STORAGE;
						end
					end
					ST_PW_DRAIN:begin
						if(cnt_pw_writes == 9'd384)begin
							state_current <= ST_DONE;
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
						flag_result_reserved <= 1'b0;
						state_current <= ST_FAULT;
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
						flag_tile_valid <= 1'b0;
						flag_result_reserved <= 1'b0;
						state_current <= ST_FAULT;
					end
				endcase
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_output <= 5'd0;
		end else begin
			if(pp_fault || flag_load_fault)begin
			end else if(flag_cnt_output_clear)begin
				cnt_output <= 5'd0;
			end else if(flag_cnt_output_increment)begin
				cnt_output <= cnt_output + 1'b1;
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
		end else begin
			if(flag_load_accept)begin
				cnt_preload_writes <= cnt_preload_writes + 1'b1;
				case(i_load_kind)
					3'd0:begin
						if(flag_halo_load_write)begin
							flag_halo_loaded <= (i_load_addr == 11'd1295);
							cnt_expected_halo <= (i_load_addr == 11'd1295) ? 11'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd1:begin
						if(flag_dw_cache_load_address_valid &&
						   ((i_load_addr == cnt_expected_dw_cache) || (i_load_addr == 11'd0)))begin
							flag_dw_cache_loaded <= (i_load_addr == 11'd255);
							cnt_expected_dw_cache <= (i_load_addr == 11'd255) ? 9'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd2:begin
						if((i_load_addr == cnt_expected_dw_weight) || (i_load_addr == 11'd0))begin
							reg_dw_weight[i_load_addr] <= i_load_data[7:0];
							flag_dw_weight_loaded <= (i_load_addr == 11'd143);
							cnt_expected_dw_weight <= (i_load_addr == 11'd143) ? 8'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd3:begin
						if((i_load_addr == cnt_expected_dw_bias) || (i_load_addr == 11'd0))begin
							reg_dw_bias[i_load_addr] <= i_load_data;
							flag_dw_bias_loaded <= (i_load_addr == 11'd15);
							cnt_expected_dw_bias <= (i_load_addr == 11'd15) ? 5'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd4:begin
						if((i_load_addr == cnt_expected_pw_weight) || (i_load_addr == 11'd0))begin
							reg_pw_weight[i_load_addr] <= i_load_data[7:0];
							flag_pw_weight_loaded <= (i_load_addr == 11'd383);
							cnt_expected_pw_weight <= (i_load_addr == 11'd383) ? 9'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd5:begin
						if((i_load_addr == cnt_expected_pw_bias) || (i_load_addr == 11'd0))begin
							reg_pw_bias[i_load_addr] <= i_load_data;
							flag_pw_bias_loaded <= (i_load_addr == 11'd23);
							cnt_expected_pw_bias <= (i_load_addr == 11'd23) ? 5'd0 : i_load_addr + 1'b1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					default: flag_load_fault <= 1'b1;
				endcase
			end
			if(flag_commit_accept && pp_output_tag[15])begin
				reg_output_cache[pp_output_tag[14:11] * 24 + pp_output_tag[10:6]] <= pp_output_data;
			end
			if(flag_dw_cache_write)begin
				reg_dw_cache[wire_dw_cache_write_address] <= wire_dw_cache_write_data;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
		end else if(flag_halo_load_write)begin
			reg_halo[i_load_addr] <= i_load_data[7:0];
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
			cnt_mac_results <= 32'd0;
			cnt_pre_accepts <= 32'd0;
			cnt_silu_accepts <= 32'd0;
			cnt_post_accepts <= 32'd0;
			cnt_writebacks <= 32'd0;
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
				cnt_mac_results <= 32'd0;
				cnt_pre_accepts <= 32'd0;
				cnt_silu_accepts <= 32'd0;
				cnt_post_accepts <= 32'd0;
				cnt_writebacks <= 32'd0;
			end else if(flag_busy_o)begin
				cnt_core_cycles <= cnt_core_cycles + 1'b1;
				if((state_current == ST_STORAGE) || (state_current == ST_MAC_SEND) ||
				   (state_current == ST_MAC_WAIT) || (state_current == ST_DW_POST))begin
					cnt_mac_cycles <= cnt_mac_cycles + 1'b1;
				end
				if(pp_pre_busy)begin cnt_pre_cycles <= cnt_pre_cycles + 1'b1; end
				if(pp_silu_busy)begin cnt_silu_cycles <= cnt_silu_cycles + 1'b1; end
				if(pp_post_busy)begin cnt_post_cycles <= cnt_post_cycles + 1'b1; end
				if(pp_output_valid)begin cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1; end
				if((pp_output_valid && (~i_commit_ready)) ||
				   ((state_current == ST_MAC_SEND) && (cnt_mac_group == 2'd0) && (~flag_can_reserve)) ||
				   ((state_current == ST_DW_POST) && (~pp_input_ready)))begin
					cnt_storage_wait_cycles <= cnt_storage_wait_cycles + 1'b1;
				end else if((state_current == ST_DW_DRAIN) || (state_current == ST_PW_DRAIN))begin
					cnt_scheduler_idle_cycles <= cnt_scheduler_idle_cycles + 1'b1;
				end
			end
			if(flag_mac_result_accept)begin cnt_mac_results <= cnt_mac_results + 1'b1; end
			if(pp_pre_accept)begin cnt_pre_accepts <= cnt_pre_accepts + 1'b1; end
			if(pp_silu_accept)begin cnt_silu_accepts <= cnt_silu_accepts + 1'b1; end
			if(pp_post_accept)begin cnt_post_accepts <= cnt_post_accepts + 1'b1; end
			if(flag_commit_accept)begin cnt_writebacks <= cnt_writebacks + 1'b1; end
			if(i_export_start && (state_current == ST_IDLE))begin
				cnt_export_cycles <= 32'd0;
			end else if(state_current == ST_EXPORT)begin
				cnt_export_cycles <= cnt_export_cycles + 1'b1;
			end
		end
	end

	road_mac_probe road_mac_probe_Inst_tile(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_input_valid(flag_mac_input_valid),
		.i_first(cnt_mac_group == 2'd0),
		.i_last(flag_mac_last_group),
		.i_lane_mask(reg_mac_mask),
		.i_activation_data(reg_mac_activation),
		.i_weight_data(reg_mac_weight),
		.i_bias_data(reg_mac_bias),
		.i_result_ready(flag_mac_result_ready_local),
		.o_input_ready(mac_input_ready),
		.o_result_valid(mac_result_valid),
		.o_result_data(mac_result_data),
		.o_fault(mac_fault)
	);

	road_postprocess_stream road_postprocess_stream_Inst_tile(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_table_valid(i_table_valid && flag_table_enable),
		.i_table_addr(i_table_addr),
		.i_table_data(i_table_data),
		.o_table_ready(pp_table_ready),
		.o_table_loaded(pp_table_loaded),
		.o_table_fault(pp_table_fault),
		.i_input_valid(flag_pp_input_valid),
		.i_result_data(wire_pp_result_data),
		.i_result_fault(flag_layer_pw ? mac_fault : 1'b0),
		.i_layer(flag_layer_pw),
		.i_position(wire_pp_position),
		.i_channel_base(wire_result_channel_base),
		.i_lane_mask(wire_result_lane_mask),
		.o_input_ready(pp_input_ready),
		.i_output_ready(i_commit_ready && flag_busy_o),
		.o_output_valid(pp_output_valid),
		.o_output_data(pp_output_data),
		.o_output_tag(pp_output_tag),
		.o_fault(pp_fault),
		.o_result_queue_count(pp_result_queue_count),
		.o_meta_count(pp_meta_count),
		.o_pre_busy(pp_pre_busy),
		.o_silu_busy(pp_silu_busy),
		.o_post_busy(pp_post_busy),
		.o_pre_accept(pp_pre_accept),
		.o_silu_accept(pp_silu_accept),
		.o_post_accept(pp_post_accept)
	);

endmodule
