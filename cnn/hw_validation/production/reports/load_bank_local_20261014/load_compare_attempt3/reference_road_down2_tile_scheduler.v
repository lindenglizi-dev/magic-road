`timescale 1ns / 1ps

// Frozen down2 tile scheduler with the shared MAC and postprocess cores outside.
module reference_road_down2_tile_scheduler
(
	input i_clk,
	input i_rstn,
	input i_table_loaded,
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
	output [31:0]o_writeback_count,
	input i_mac_ready,
	input i_mac_result_valid,
	input [95:0]i_mac_result,
	input i_mac_fault,
	output o_mac_valid,
	output o_mac_first,
	output o_mac_last,
	output [7:0]o_mac_mask,
	output [63:0]o_mac_activation,
	output [191:0]o_mac_weight,
	output [95:0]o_mac_bias,
	output o_mac_result_ready,
	input i_pp_ready,
	input i_pp_valid,
	input signed [15:0]i_pp_data,
	input [15:0]i_pp_tag,
	input i_pp_int16,
	input i_pp_fault,
	input [1:0]i_pp_result_queue_count,
	input [3:0]i_pp_meta_count,
	input i_pp_pre_busy,
	input i_pp_silu_busy,
	input i_pp_post_busy,
	input i_pp_pre_accept,
	input i_pp_silu_accept,
	input i_pp_post_accept,
	output o_pp_valid,
	output [95:0]o_pp_acc,
	output [95:0]o_pp_multipliers,
	output [17:0]o_pp_shifts,
	output [31:0]o_pp_post_multiplier,
	output [5:0]o_pp_post_shift,
	output [2:0]o_pp_mask,
	output [47:0]o_pp_tags,
	output o_pp_input_fault,
	output o_pp_ready
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
	// Nine independent taps share a four-bit channel read address; external OIHW is unchanged.
	reg signed [7:0]reg_dw_weight_top_left [0:15];
	reg signed [7:0]reg_dw_weight_top_middle [0:15];
	reg signed [7:0]reg_dw_weight_top_right [0:15];
	reg signed [7:0]reg_dw_weight_middle_left [0:15];
	reg signed [7:0]reg_dw_weight_center [0:15];
	reg signed [7:0]reg_dw_weight_middle_right [0:15];
	reg signed [7:0]reg_dw_weight_bottom_left [0:15];
	reg signed [7:0]reg_dw_weight_bottom_middle [0:15];
	reg signed [7:0]reg_dw_weight_bottom_right [0:15];
	wire [71:0]wire_dw_channel_weights;
	// Commit one edge after validated acceptance; the existing start/storage boundary covers this edge.
	reg flag_dw_weight_write_pending;
	reg [7:0]reg_dw_weight_write_address;
	reg signed [7:0]reg_dw_weight_write_data;
	reg signed [31:0]reg_dw_bias [0:15];
	reg signed [7:0]reg_pw_weight [0:383];
	reg signed [31:0]reg_pw_bias [0:23];
	// Forty active channels only: DW channels first, followed by PW channels.
	reg [31:0]reg_pre_multiplier [0:39];
	reg [5:0]reg_pre_shift [0:39];
	reg [31:0]reg_post_multiplier [0:1];
	reg [5:0]reg_post_shift [0:1];
	reg [5:0]cnt_expected_multiplier;
	reg [5:0]cnt_expected_control;
	reg flag_multiplier_loaded;
	reg flag_control_loaded;

	reg [3:0]state_current;
	reg flag_layer_pw;
	reg flag_busy_o;
	reg flag_done_o;
	reg flag_fault_o;
	reg flag_load_fault;
	reg flag_tile_valid;
	reg flag_export_done_o;
	reg flag_result_reserved;                    // DW active triplet valid; no longer MAC credit state
	reg [8:0]reg_dw_active_meta;                 // Retiring DW {position, channel}, independent of issuer
	// Shared DW/PW first-to-result ownership ring; never derive result tags from issue counters.
	reg [8:0]reg_pw_task_meta [0:3];
	// Parameter payload shares the existing ownership ring; validity comes from its count.
	reg [151:0]reg_task_parameters_alpha;
	reg [151:0]reg_task_parameters_beta;
	reg [151:0]reg_task_parameters_gamma;
	reg [151:0]reg_task_parameters_delta;
	reg [151:0]reg_head_parameters;
	reg [151:0]reg_dw_active_parameters;
	reg [1:0]ptr_pw_meta_read;
	reg [1:0]ptr_pw_meta_write;
	reg [2:0]cnt_pw_meta;
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
	reg [4:0]next_cnt_output_prepared;            // Counter value after a last-group transfer
	reg [4:0]reg_cnt_output_prepared;             // Prepared before the existing last-group edge

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
	(* max_fanout = 16 *) wire flag_mac_input_accept;
	wire flag_mac_result_ready_local;
	wire flag_mac_result_accept;
	wire flag_can_reserve;
	wire flag_pw_first_accept;
	wire flag_pw_result_accept;
	wire flag_shared_meta_push;                  // Either layer reserves one MAC ownership tag
	wire flag_shared_meta_pop;                   // Either layer transfers the matching MAC result
	wire flag_dw_first_accept;                   // DW issuer reserves ownership on accepted first group
	wire flag_dw_last_accept;                    // DW issuer may advance only after accepted final group
	wire flag_dw_result_accept;                  // DW MAC result moves from queue into the active slot
	wire flag_dw_post_accept;                    // One scalar from the active triplet enters postprocess
	wire flag_dw_active_last_accept;             // Last scalar frees or replaces the active slot
	wire flag_dw_fault_pop;                      // Faulting DW head is accepted only to cancel the block
	wire flag_fault_flush;                       // Any terminal fault stops issue and invalidates publication
	wire flag_mac_fault_accept;
	wire flag_pw_prepare_next;

	wire pp_input_ready;
	wire pp_output_valid;
	wire signed [7:0]pp_output_data;
	wire [15:0]pp_output_tag;
	wire pp_output_int16;
	wire pp_fault;
	wire [1:0]pp_result_queue_count;
	wire [3:0]pp_meta_count;
	wire pp_pre_busy;
	wire pp_silu_busy;
	wire pp_post_busy;
	wire pp_pre_accept;
	wire pp_silu_accept;
	wire pp_post_accept;
	wire pp_table_loaded;
	wire flag_commit_accept;

	wire [4:0]wire_pw_group_base;
	wire [3:0]wire_pw_prepare_position;
	wire [2:0]wire_pw_prepare_output;
	wire [1:0]wire_mac_prepare_group;
	wire [3:0]wire_dw_active_position;            // Retiring spatial-group origin
	wire [4:0]wire_dw_active_channel;             // Retiring logical DW channel
	wire [1:0]wire_dw_active_lane;                // Physical PP lane selected by logical channel
	wire [4:0]wire_dw_active_channel_base;        // Three-channel PP parameter-group base
	wire [2:0]wire_result_lane_mask;
	wire [4:0]wire_result_channel_base;
	wire [1:0]wire_dw_issue_count;                // Spatial outputs produced by the issuer task
	wire [1:0]wire_dw_post_count;                 // Scalars remaining in the active triplet identity
	wire signed [31:0]wire_dw_post_scalar;
	wire [95:0]wire_pp_result_data;
	wire [3:0]wire_pp_position;
	wire [4:0]wire_pp_channel_beta;
	wire [4:0]wire_pp_channel_gamma;
	wire [15:0]wire_pp_tag_alpha;
	wire [15:0]wire_pp_tag_beta;
	wire [15:0]wire_pp_tag_gamma;
	wire flag_pp_input_valid;
	wire flag_pp_input_accept;
	wire flag_pp_shape_fault;
	wire flag_mac_last_group;
	wire flag_load_accept;
	wire flag_output_accept;
	wire flag_start_accept;
	reg [5:0]reg_dw_issue_parameter_base;
	wire [5:0]wire_issue_parameter_base;
	wire [5:0]wire_issue_parameter_beta;
	wire [5:0]wire_issue_parameter_gamma;
	wire [151:0]wire_issue_parameters;
	wire [151:0]wire_pp_parameters;
	wire flag_multiplier_load_valid;
	wire flag_control_load_valid;
	wire flag_halo_load_write;
	wire flag_dw_weight_load_write;
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

	// Preserve the runner's MAC/PP signal names as aliases for waveform comparison.
	assign mac_input_ready = i_mac_ready;
	assign wire_dw_channel_weights = {
		reg_dw_weight_bottom_right[cnt_output[3:0]], reg_dw_weight_bottom_middle[cnt_output[3:0]],
		reg_dw_weight_bottom_left[cnt_output[3:0]], reg_dw_weight_middle_right[cnt_output[3:0]],
		reg_dw_weight_center[cnt_output[3:0]], reg_dw_weight_middle_left[cnt_output[3:0]],
		reg_dw_weight_top_right[cnt_output[3:0]], reg_dw_weight_top_middle[cnt_output[3:0]],
		reg_dw_weight_top_left[cnt_output[3:0]]};
	assign mac_result_valid = i_mac_result_valid;
	assign mac_result_data = i_mac_result;
	assign mac_fault = i_mac_fault;
	assign pp_input_ready = i_pp_ready;
	assign pp_output_valid = i_pp_valid;
	assign pp_output_data = i_pp_data[7:0];
	assign pp_output_tag = i_pp_tag;
	assign pp_output_int16 = i_pp_int16;
	assign pp_fault = i_pp_fault;
	assign pp_result_queue_count = i_pp_result_queue_count;
	assign pp_meta_count = i_pp_meta_count;
	assign pp_pre_busy = i_pp_pre_busy;
	assign pp_silu_busy = i_pp_silu_busy;
	assign pp_post_busy = i_pp_post_busy;
	assign pp_pre_accept = i_pp_pre_accept;
	assign pp_silu_accept = i_pp_silu_accept;
	assign pp_post_accept = i_pp_post_accept;
	assign pp_table_loaded = i_table_loaded;

	assign wire_pw_group_base = {cnt_output[2:0], 1'b0} + {2'b00, cnt_output[2:0]};
	// Last handshake advances the issuer; the separate descriptor ring owns result tags.
	assign flag_pw_prepare_next = flag_layer_pw && (state_current == ST_MAC_SEND) &&
	                              (cnt_mac_group == 2'd1);
	assign wire_pw_prepare_position = (flag_pw_prepare_next && (cnt_output == 5'd7)) ?
	                                  cnt_position + 4'd1 : cnt_position;
	assign wire_pw_prepare_output = flag_pw_prepare_next ?
	                                cnt_output[2:0] + 3'd1 : cnt_output[2:0];
	assign wire_mac_prepare_group = flag_pw_prepare_next ? 2'd0 :
	                                (flag_layer_pw && (state_current == ST_MAC_SEND) &&
	                                 (cnt_mac_group == 2'd0)) ? 2'd1 : cnt_mac_group;
	assign wire_dw_active_position = reg_dw_active_meta[8:5];
	assign wire_dw_active_channel = reg_dw_active_meta[4:0];
	assign wire_dw_active_lane = ((wire_dw_active_channel == 5'd0) ||
	                              (wire_dw_active_channel == 5'd3) ||
	                              (wire_dw_active_channel == 5'd6) ||
	                              (wire_dw_active_channel == 5'd9) ||
	                              (wire_dw_active_channel == 5'd12) ||
	                              (wire_dw_active_channel == 5'd15)) ? 2'd0 :
	                             ((wire_dw_active_channel == 5'd1) ||
	                              (wire_dw_active_channel == 5'd4) ||
	                              (wire_dw_active_channel == 5'd7) ||
	                              (wire_dw_active_channel == 5'd10) ||
	                              (wire_dw_active_channel == 5'd13)) ? 2'd1 : 2'd2;
	assign wire_dw_active_channel_base = wire_dw_active_channel - {3'd0, wire_dw_active_lane};
	assign wire_result_lane_mask = flag_layer_pw ? 3'b111 : (3'b001 << wire_dw_active_lane);
	assign wire_result_channel_base = flag_layer_pw ? reg_pw_task_meta[ptr_pw_meta_read][4:0] :
	                                                    wire_dw_active_channel_base;
	assign wire_dw_issue_count = (cnt_position[1:0] == 2'd0) ? 2'd3 : 2'd1;
	assign wire_dw_post_count = (wire_dw_active_position[1:0] == 2'd0) ? 2'd3 : 2'd1;
	assign wire_dw_post_scalar = (cnt_dw_post_lane == 2'd0) ? $signed(reg_dw_triplet_result[31:0]) :
	                                  (cnt_dw_post_lane == 2'd1) ? $signed(reg_dw_triplet_result[63:32]) :
	                                                                       $signed(reg_dw_triplet_result[95:64]);
	assign wire_pp_result_data = flag_layer_pw ? mac_result_data :
	                             (wire_dw_active_lane == 2'd0) ? {64'd0, wire_dw_post_scalar} :
	                             (wire_dw_active_lane == 2'd1) ? {32'd0, wire_dw_post_scalar, 32'd0} :
	                                                        {wire_dw_post_scalar, 64'd0};
	assign wire_pp_position = flag_layer_pw ? reg_pw_task_meta[ptr_pw_meta_read][8:5] :
	                                          wire_dw_active_position + cnt_dw_post_lane;
	assign wire_pp_channel_beta = wire_result_channel_base + 5'd1;
	assign wire_pp_channel_gamma = wire_result_channel_base + 5'd2;
	assign wire_pp_tag_alpha = {flag_layer_pw, wire_pp_position, wire_result_channel_base, 6'd0};
	assign wire_pp_tag_beta = {flag_layer_pw, wire_pp_position, wire_pp_channel_beta, 6'd0};
	assign wire_pp_tag_gamma = {flag_layer_pw, wire_pp_position, wire_pp_channel_gamma, 6'd0};
	assign flag_pp_shape_fault = flag_layer_pw ?
	                             ((wire_result_lane_mask != 3'b111) ||
	                              (wire_result_channel_base > 5'd21)) :
	                             ~(((wire_result_lane_mask == 3'b001) &&
	                                (wire_result_channel_base <= 5'd15)) ||
	                               ((wire_result_lane_mask == 3'b010) &&
	                                (wire_result_channel_base <= 5'd14)) ||
	                               ((wire_result_lane_mask == 3'b100) &&
	                                (wire_result_channel_base <= 5'd13)));
	assign flag_can_reserve = (cnt_pw_meta < 3'd4) || flag_shared_meta_pop;
	assign flag_mac_last_group = flag_layer_pw ? (cnt_mac_group == 2'd1) :
	                                               (cnt_mac_group == 2'd2);
	assign flag_mac_input_valid = (state_current == ST_MAC_SEND) &&
	                              ((cnt_mac_group != 2'd0) || flag_can_reserve) &&
	                              (~pp_fault) && (~flag_load_fault) && (~flag_fault_o) &&
	                              (~(mac_result_valid && mac_fault));
	assign flag_mac_input_accept = flag_mac_input_valid && mac_input_ready;
	assign flag_mac_result_ready_local = flag_layer_pw ?
	                                     ((cnt_pw_meta != 3'd0) && flag_busy_o && (~pp_fault) &&
	                                      (mac_fault || (pp_table_loaded && pp_input_ready))) :
	                                     ((cnt_pw_meta != 3'd0) && flag_busy_o && (~pp_fault) &&
	                                      (mac_fault || (~flag_result_reserved) ||
	                                       flag_dw_active_last_accept));
	assign flag_mac_result_accept = mac_result_valid && flag_mac_result_ready_local;
	assign flag_pw_first_accept = flag_layer_pw && flag_mac_input_accept && (cnt_mac_group == 2'd0);
	assign flag_pw_result_accept = flag_layer_pw && flag_mac_result_accept;
	assign flag_dw_first_accept = (~flag_layer_pw) && flag_mac_input_accept &&
	                              (cnt_mac_group == 2'd0);
	assign flag_shared_meta_push = flag_pw_first_accept || flag_dw_first_accept;
	assign flag_dw_last_accept = (~flag_layer_pw) && flag_mac_input_accept && flag_mac_last_group;
	assign flag_dw_result_accept = (~flag_layer_pw) && flag_mac_result_accept;
	assign flag_shared_meta_pop = flag_pw_result_accept || flag_dw_result_accept;
	assign flag_dw_post_accept = (~flag_layer_pw) && flag_pp_input_accept;
	assign flag_dw_active_last_accept = flag_dw_post_accept &&
	                                    (cnt_dw_post_lane + 1'b1 == wire_dw_post_count);
	assign flag_dw_fault_pop = flag_dw_result_accept && mac_fault;
	assign flag_mac_fault_accept = (flag_pw_result_accept && mac_fault) || flag_dw_fault_pop;
	assign flag_fault_flush = pp_fault || flag_load_fault || flag_mac_fault_accept;
	assign flag_pp_input_valid = flag_layer_pw ?
	                             ((cnt_pw_meta != 3'd0) && flag_busy_o && mac_result_valid && (~mac_fault) && (~pp_fault)) :
	                             (flag_result_reserved && flag_busy_o && (~pp_fault) &&
	                              (~(mac_result_valid && mac_fault)) &&
	                              (pp_result_queue_count < 2'd2));
	assign flag_pp_input_accept = flag_pp_input_valid && pp_input_ready;
	assign flag_commit_accept = pp_output_valid && i_commit_ready && flag_busy_o && (~flag_mac_fault_accept);
	assign flag_load_accept = i_load_valid && o_load_ready;
	assign flag_output_accept = o_output_valid && i_output_ready;
	assign flag_start_accept = i_start && (state_current == ST_IDLE) &&
	                           pp_table_loaded && (~pp_fault) && (~flag_load_fault) &&
	                           flag_multiplier_loaded && flag_control_loaded &&
	                           flag_pw_weight_loaded && flag_pw_bias_loaded &&
	                           (i_pw_only ? flag_dw_cache_loaded :
	                           (flag_halo_loaded && flag_dw_weight_loaded && flag_dw_bias_loaded));
	assign wire_issue_parameter_base = flag_layer_pw ?
	                                   6'd16 + {1'b0, wire_pw_group_base} : reg_dw_issue_parameter_base;
	assign wire_issue_parameter_beta = wire_issue_parameter_base + 6'd1;
	assign wire_issue_parameter_gamma = wire_issue_parameter_base + 6'd2;
	assign wire_issue_parameters = {reg_post_shift[flag_layer_pw], reg_post_multiplier[flag_layer_pw],
	                                reg_pre_shift[wire_issue_parameter_gamma],
	                                reg_pre_shift[wire_issue_parameter_beta],
	                                reg_pre_shift[wire_issue_parameter_base],
	                                reg_pre_multiplier[wire_issue_parameter_gamma],
	                                reg_pre_multiplier[wire_issue_parameter_beta],
	                                reg_pre_multiplier[wire_issue_parameter_base]};
	assign wire_pp_parameters = flag_layer_pw ? reg_head_parameters : reg_dw_active_parameters;
	assign flag_multiplier_load_valid = (i_load_addr < 11'd40) && (~i_load_data[31]);
	assign flag_control_load_valid = (i_load_addr < 11'd40 || i_load_addr == 11'd42 || i_load_addr == 11'd43) ?
	                                (i_load_data >= 32'sd0 && i_load_data <= 32'sd62) :
	                                ((i_load_addr == 11'd40 || i_load_addr == 11'd41) && (~i_load_data[31]));
	assign flag_halo_load_write = flag_load_accept && (i_load_kind == 3'd0) &&
	                              ((i_load_addr == cnt_expected_halo) || (i_load_addr == 11'd0));
	assign flag_dw_weight_load_write = flag_load_accept && (i_load_kind == 3'd2) &&
	                                  ((i_load_addr == cnt_expected_dw_weight) || (i_load_addr == 11'd0));
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
	assign o_result_reserved = flag_result_reserved || (cnt_pw_meta != 3'd0);
	assign o_meta_count = pp_meta_count;
	assign o_mac_result_count = cnt_mac_results;
	assign o_pre_accept_count = cnt_pre_accepts;
	assign o_silu_accept_count = cnt_silu_accepts;
	assign o_post_accept_count = cnt_post_accepts;
	assign o_writeback_count = cnt_writebacks;
	assign o_mac_valid = flag_mac_input_valid;
	assign o_mac_first = (cnt_mac_group == 2'd0);
	assign o_mac_last = flag_mac_last_group;
	assign o_mac_mask = reg_mac_mask;
	assign o_mac_activation = reg_mac_activation;
	assign o_mac_weight = reg_mac_weight;
	assign o_mac_bias = reg_mac_bias;
	assign o_mac_result_ready = flag_mac_result_ready_local;
	assign o_pp_valid = flag_pp_input_valid;
	assign o_pp_acc = wire_pp_result_data;
	assign o_pp_multipliers = wire_pp_parameters[95:0];
	assign o_pp_shifts = wire_pp_parameters[113:96];
	assign o_pp_post_multiplier = wire_pp_parameters[145:114];
	assign o_pp_post_shift = wire_pp_parameters[151:146];
	assign o_pp_mask = wire_result_lane_mask;
	assign o_pp_tags = {wire_pp_tag_gamma, wire_pp_tag_beta, wire_pp_tag_alpha};
	assign o_pp_input_fault = (flag_layer_pw ? mac_fault : 1'b0) || flag_pp_shape_fault;
	assign o_pp_ready = i_commit_ready && flag_busy_o;

	// Decode the issuing DW channel, never the retiring head or active triplet.
	always@(*)begin
		case(cnt_output)
			5'd0, 5'd1, 5'd2: reg_dw_issue_parameter_base = 6'd0;
			5'd3, 5'd4, 5'd5: reg_dw_issue_parameter_base = 6'd3;
			5'd6, 5'd7, 5'd8: reg_dw_issue_parameter_base = 6'd6;
			5'd9, 5'd10, 5'd11: reg_dw_issue_parameter_base = 6'd9;
			5'd12, 5'd13, 5'd14: reg_dw_issue_parameter_base = 6'd12;
			default: reg_dw_issue_parameter_base = 6'd15;
		endcase
	end

	// Explicit register banks preserve the old head on a full-ring simultaneous pop/push.
	always@(*)begin
		case(ptr_pw_meta_read)
			2'd0: reg_head_parameters = reg_task_parameters_alpha;
			2'd1: reg_head_parameters = reg_task_parameters_beta;
			2'd2: reg_head_parameters = reg_task_parameters_gamma;
			default: reg_head_parameters = reg_task_parameters_delta;
		endcase
	end

	// No payload reset tree: the original asynchronous reset cancels ring/active ownership.
	always@(posedge i_clk)begin
		if(i_rstn && flag_shared_meta_push)begin
			case(ptr_pw_meta_write)
				2'd0: reg_task_parameters_alpha <= wire_issue_parameters;
				2'd1: reg_task_parameters_beta <= wire_issue_parameters;
				2'd2: reg_task_parameters_gamma <= wire_issue_parameters;
				default: reg_task_parameters_delta <= wire_issue_parameters;
			endcase
		end
		if(i_rstn && (~flag_fault_flush) && flag_dw_result_accept && (~mac_fault))begin
			reg_dw_active_parameters <= reg_head_parameters;
		end
	end

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
						if((spatial_lane < wire_dw_issue_count) &&
						   (union_column >= spatial_lane * 2) &&
						   (union_column < spatial_lane * 2 + 3))begin
							weight_index = union_row * 3 +
							               union_column - spatial_lane * 2;
							next_mac_weight[spatial_lane * 64 + lane_index * 8 +:8] =
								wire_dw_channel_weights[weight_index * 8 +:8];
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
				next_mac_activation[lane_index * 8 +:8] = reg_dw_cache[wire_pw_prepare_position * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_mask[lane_index] = 1'b1;
				output_channel = wire_pw_prepare_output * 3;
				next_mac_weight[lane_index * 8 +:8] = reg_pw_weight[output_channel * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_weight[64 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 1) * 16 + wire_mac_prepare_group * 8 + lane_index];
				next_mac_weight[128 + lane_index * 8 +:8] = reg_pw_weight[(output_channel + 2) * 16 + wire_mac_prepare_group * 8 + lane_index];
			end
			next_mac_bias[31:0] = reg_pw_bias[wire_pw_prepare_output * 3];
			next_mac_bias[63:32] = reg_pw_bias[wire_pw_prepare_output * 3 + 1];
			next_mac_bias[95:64] = reg_pw_bias[wire_pw_prepare_output * 3 + 2];
		end
	end

	always@(*)begin
		next_cnt_output_prepared = cnt_output;
		if(flag_layer_pw)begin
			if(cnt_output < 5'd7)begin
				next_cnt_output_prepared = cnt_output + 5'd1;
			end else if(cnt_position < 4'd15)begin
				next_cnt_output_prepared = 5'd0;
			end
		end else if(cnt_output < 5'd15)begin
			next_cnt_output_prepared = cnt_output + 5'd1;
		end else begin
			next_cnt_output_prepared = 5'd0;
		end
	end

	// Every legal last group follows a non-last edge with this task identity stable.
	// PW group zero supplies the minimum preparation edge; no ready-dependent data enters here.
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_cnt_output_prepared <= 5'd0;
		end else begin
			reg_cnt_output_prepared <= next_cnt_output_prepared;
		end
	end

	// Shared descriptor and MAC queues reserve/pop on identical events, including fault pop.
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			ptr_pw_meta_read <= 2'd0;
			ptr_pw_meta_write <= 2'd0;
			cnt_pw_meta <= 3'd0;
			reg_pw_task_meta[0] <= 9'd0;
			reg_pw_task_meta[1] <= 9'd0;
			reg_pw_task_meta[2] <= 9'd0;
			reg_pw_task_meta[3] <= 9'd0;
		end else begin
			if(flag_shared_meta_push)begin
				reg_pw_task_meta[ptr_pw_meta_write] <= flag_layer_pw ?
				                                               {cnt_position, wire_pw_group_base} :
				                                               {cnt_position, cnt_output};
				ptr_pw_meta_write <= ptr_pw_meta_write + 2'd1;
			end
			if(flag_shared_meta_pop)begin
				ptr_pw_meta_read <= ptr_pw_meta_read + 2'd1;
			end
			case({flag_shared_meta_push, flag_shared_meta_pop})
				2'b10: cnt_pw_meta <= cnt_pw_meta + 3'd1;
				2'b01: cnt_pw_meta <= cnt_pw_meta - 3'd1;
				default: cnt_pw_meta <= cnt_pw_meta;
			endcase
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
			flag_result_reserved <= 1'b0;
			reg_dw_active_meta <= 9'd0;
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
			if(flag_fault_flush)begin
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
				// The old active scalar is consumed before a simultaneous result installs the new triplet.
				if(flag_dw_result_accept && (~mac_fault))begin
					reg_dw_triplet_result <= mac_result_data;
					reg_dw_active_meta <= reg_pw_task_meta[ptr_pw_meta_read];
					cnt_dw_post_lane <= 2'd0;
					flag_result_reserved <= 1'b1;
				end else if(flag_dw_active_last_accept)begin
					cnt_dw_post_lane <= 2'd0;
					flag_result_reserved <= 1'b0;
				end else if(flag_dw_post_accept)begin
					cnt_dw_post_lane <= cnt_dw_post_lane + 1'b1;
				end
				if(flag_dw_post_accept)begin
					flag_debug_valid_o <= 1'b1;
					reg_debug_phase_o <= 2'd0;
					flag_debug_layer_o <= 1'b0;
					reg_debug_position_o <= wire_pp_position;
					reg_debug_channel_o <= wire_dw_active_channel;
					reg_debug_value_o <= wire_dw_post_scalar;
				end
				// Keep the legacy debug arbitration: MAC event wins over simultaneous commit.
				if(flag_pw_result_accept)begin
					flag_debug_valid_o <= 1'b1;
					reg_debug_phase_o <= 2'd0;
					flag_debug_layer_o <= 1'b1;
					reg_debug_position_o <= wire_pp_position;
					reg_debug_channel_o <= wire_result_channel_base;
					reg_debug_value_o <= $signed(mac_result_data[31:0]);
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
							if(flag_mac_last_group)begin
								if(flag_layer_pw)begin
									cnt_mac_group <= 2'd0;
									if((cnt_output == 5'd7) && (cnt_position == 4'd15))begin
										state_current <= ST_PW_DRAIN;
									end else begin
										reg_mac_activation <= next_mac_activation;
										reg_mac_weight <= next_mac_weight;
										reg_mac_bias <= next_mac_bias;
										reg_mac_mask <= next_mac_mask;
										if(cnt_output == 5'd7)begin
											cnt_position <= cnt_position + 4'd1;
										end
									end
								end else if(flag_dw_last_accept)begin
									cnt_mac_group <= 2'd0;
									if((cnt_output == 5'd15) && (cnt_position == 4'd15))begin
										state_current <= ST_DW_DRAIN;
									end else begin
										if(cnt_output == 5'd15)begin
											if(cnt_position[1:0] == 2'd0)begin
												cnt_position <= cnt_position + 4'd3;
											end else begin
												cnt_position <= cnt_position + 1'b1;
											end
										end
										state_current <= ST_STORAGE;
									end
								end
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
					ST_DW_DRAIN:begin
						if((cnt_dw_writes == 9'd256) && (cnt_pw_meta == 3'd0) &&
						   (~flag_result_reserved) && (~mac_result_valid))begin
							flag_layer_pw <= 1'b1;
							cnt_position <= 4'd0;
							cnt_mac_group <= 2'd0;
							state_current <= ST_STORAGE;
						end
					end
					ST_PW_DRAIN:begin
						if((cnt_pw_writes == 9'd384) && (cnt_pw_meta == 3'd0))begin
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
			end else begin
				case(state_current)
					ST_IDLE:begin
						if(flag_start_accept)begin
							cnt_output <= 5'd0;
						end
					end
					ST_MAC_SEND:begin
						if(flag_mac_input_accept && flag_mac_last_group)begin
							cnt_output <= reg_cnt_output_prepared;
						end
					end
					ST_DW_DRAIN:begin
						if(cnt_dw_writes == 9'd256)begin
							cnt_output <= 5'd0;
						end
					end
					default:begin
					end
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
			cnt_expected_multiplier <= 6'd0;
			cnt_expected_control <= 6'd0;
			flag_multiplier_loaded <= 1'b0;
			flag_control_loaded <= 1'b0;
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
					3'd6:begin
						if(flag_multiplier_load_valid &&
						   ((i_load_addr == cnt_expected_multiplier) || (i_load_addr == 11'd0)))begin
							reg_pre_multiplier[i_load_addr] <= i_load_data;
							flag_multiplier_loaded <= (i_load_addr == 11'd39);
							cnt_expected_multiplier <= (i_load_addr == 11'd39) ? 6'd0 : i_load_addr[5:0] + 6'd1;
						end else begin
							flag_load_fault <= 1'b1;
						end
					end
					3'd7:begin
						if(flag_control_load_valid &&
						   ((i_load_addr == cnt_expected_control) || (i_load_addr == 11'd0)))begin
							if(i_load_addr < 11'd40)begin
								reg_pre_shift[i_load_addr] <= i_load_data[5:0];
							end else if(i_load_addr < 11'd42)begin
								reg_post_multiplier[i_load_addr[0]] <= i_load_data;
							end else begin
								reg_post_shift[i_load_addr[0]] <= i_load_data[5:0];
							end
							flag_control_loaded <= (i_load_addr == 11'd43);
							cnt_expected_control <= (i_load_addr == 11'd43) ? 6'd0 : i_load_addr[5:0] + 6'd1;
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

	// Reset cancels a queued write; memory validity is rebuilt by the unchanged full-load protocol.
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_dw_weight_write_pending <= 1'b0;
			reg_dw_weight_write_address <= 8'd0;
			reg_dw_weight_write_data <= 8'sd0;
		end else begin
			flag_dw_weight_write_pending <= flag_dw_weight_load_write;
			if(flag_dw_weight_load_write)begin
				// OIHW index c*9+tap becomes {tap,channel} only on the preload path.
				reg_dw_weight_write_address <= (i_load_addr[7:0] % 8'd9) * 8'd16 +
				                               (i_load_addr[7:0] / 8'd9);
				reg_dw_weight_write_data <= i_load_data[7:0];
			end
		end
	end

	// Single owner: only registered write control/address/data reach the replicated weight storage.
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
		end else if(flag_dw_weight_write_pending)begin
			case(reg_dw_weight_write_address[7:4])
				4'd0: reg_dw_weight_top_left[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd1: reg_dw_weight_top_middle[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd2: reg_dw_weight_top_right[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd3: reg_dw_weight_middle_left[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd4: reg_dw_weight_center[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd5: reg_dw_weight_middle_right[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd6: reg_dw_weight_bottom_left[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd7: reg_dw_weight_bottom_middle[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				4'd8: reg_dw_weight_bottom_right[reg_dw_weight_write_address[3:0]] <= reg_dw_weight_write_data;
				default: begin end
			endcase
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
				   (state_current == ST_MAC_WAIT) || (state_current == ST_DW_POST) ||
				   ((~flag_layer_pw) && ((cnt_pw_meta != 3'd0) || flag_result_reserved)))begin
					cnt_mac_cycles <= cnt_mac_cycles + 1'b1;
				end
				if(pp_pre_busy)begin cnt_pre_cycles <= cnt_pre_cycles + 1'b1; end
				if(pp_silu_busy)begin cnt_silu_cycles <= cnt_silu_cycles + 1'b1; end
				if(pp_post_busy)begin cnt_post_cycles <= cnt_post_cycles + 1'b1; end
				if(pp_output_valid)begin cnt_writeback_cycles <= cnt_writeback_cycles + 1'b1; end
				if((pp_output_valid && (~i_commit_ready)) ||
				   ((state_current == ST_MAC_SEND) && (cnt_mac_group == 2'd0) && (~flag_can_reserve)) ||
				   ((~flag_layer_pw) && flag_result_reserved &&
				    ((~pp_input_ready) || (pp_result_queue_count == 2'd2))))begin
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

endmodule
