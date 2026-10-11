`timescale 1ns / 1ps

// Overlapped fixed-coefficient postprocess for one atomic MAC result triple.
module road_postprocess_stream
(
	input i_clk,
	input i_rstn,
	input i_table_valid,
	input [9:0]i_table_addr,
	input signed [15:0]i_table_data,
	output o_table_ready,
	output o_table_loaded,
	output o_table_fault,
	input i_input_valid,
	input [95:0]i_result_data,
	input i_result_fault,
	input i_layer,
	input [3:0]i_position,
	input [4:0]i_channel_base,
	input [2:0]i_lane_mask,
	output o_input_ready,
	input i_output_ready,
	output o_output_valid,
	output signed [7:0]o_output_data,
	output [15:0]o_output_tag,
	output o_fault,
	output [1:0]o_result_queue_count,
	output [3:0]o_meta_count,
	output o_pre_busy,
	output o_silu_busy,
	output o_post_busy,
	output o_pre_accept,
	output o_silu_accept,
	output o_post_accept
);

	localparam signed [31:0]PRE_FACTOR_ALPHA = 32'sd1;
	localparam signed [31:0]PRE_FACTOR_BETA = 32'sd3;
	localparam signed [31:0]PRE_FACTOR_GAMMA = 32'sd5;
	localparam [5:0]PRE_SHIFT_ALPHA = 6'd0;
	localparam [5:0]PRE_SHIFT_BETA = 6'd2;
	localparam [5:0]PRE_SHIFT_GAMMA = 6'd4;
	localparam signed [31:0]POST_FACTOR = 32'sd1;
	localparam [5:0]POST_SHIFT = 6'd4;

	reg [95:0]reg_group_data_head;
	reg [95:0]reg_group_data_tail;
	reg reg_group_layer_head;
	reg reg_group_layer_tail;
	reg [3:0]reg_group_position_head;
	reg [3:0]reg_group_position_tail;
	reg [4:0]reg_group_channel_head;
	reg [4:0]reg_group_channel_tail;
	reg [2:0]reg_group_mask_head;
	reg [2:0]reg_group_mask_tail;
	reg [1:0]cnt_result_queue;

	reg [15:0]reg_meta_fifo [0:7];
	reg [2:0]cnt_meta_read;
	reg [2:0]cnt_meta_write;
	reg [3:0]cnt_meta;
	reg [3:0]cnt_pre_inflight;
	reg [3:0]cnt_post_inflight;
	reg flag_fatal;

	wire [1:0]wire_selected_lane;
	wire signed [31:0]wire_scalar_data;
	wire signed [31:0]wire_pre_factor;
	wire [5:0]wire_pre_shift;
	wire signed [63:0]wire_scalar_extended;
	wire signed [63:0]wire_factor_extended;
	wire signed [63:0]wire_pre_product;
	wire [4:0]wire_scalar_channel;
	wire [15:0]wire_scalar_tag;
	wire flag_scalar_valid;
	wire flag_scalar_last;
	wire flag_group_push;
	wire flag_group_pop;
	wire flag_base_aligned;
	wire flag_lane_shape_valid;
	wire flag_input_shape_fault;
	wire flag_input_accept;
	wire flag_fault_event;

	wire flag_pre_advance;
	wire flag_pre_accept;
	wire pre_result_valid;
	wire signed [15:0]pre_result_data;
	wire [15:0]pre_result_tag;
	wire pre_result_fault;

	wire silu_input_ready;
	wire silu_table_ready;
	wire silu_table_loaded;
	wire silu_table_fault;
	wire silu_output_valid;
	wire signed [15:0]silu_output_data;
	wire flag_silu_accept;
	wire flag_silu_output_ready;

	wire flag_post_advance;
	wire flag_post_accept;
	wire post_result_valid;
	wire signed [15:0]post_result_data;
	wire [15:0]post_result_tag;
	wire post_result_fault;
	wire flag_output_accept;
	wire signed [63:0]wire_post_product;
	wire signed [7:0]wire_output_saturated;
	wire flag_pipeline_empty;
	wire flag_table_forward;

	assign wire_selected_lane = reg_group_mask_head[0] ? 2'd0 :
	                            reg_group_mask_head[1] ? 2'd1 : 2'd2;
	assign wire_scalar_data = (wire_selected_lane == 2'd0) ? $signed(reg_group_data_head[31:0]) :
	                          (wire_selected_lane == 2'd1) ? $signed(reg_group_data_head[63:32]) :
	                                                                $signed(reg_group_data_head[95:64]);
	assign wire_pre_factor = (wire_selected_lane == 2'd0) ? PRE_FACTOR_ALPHA :
	                         (wire_selected_lane == 2'd1) ? PRE_FACTOR_BETA : PRE_FACTOR_GAMMA;
	assign wire_pre_shift = (wire_selected_lane == 2'd0) ? PRE_SHIFT_ALPHA :
	                        (wire_selected_lane == 2'd1) ? PRE_SHIFT_BETA : PRE_SHIFT_GAMMA;
	assign wire_scalar_extended = {{32{wire_scalar_data[31]}}, wire_scalar_data};
	assign wire_factor_extended = {{32{wire_pre_factor[31]}}, wire_pre_factor};
	assign wire_pre_product = $signed(wire_scalar_extended) * $signed(wire_factor_extended);
	assign wire_scalar_channel = reg_group_channel_head + {3'd0, wire_selected_lane};
	assign wire_scalar_tag = {reg_group_layer_head, reg_group_position_head, wire_scalar_channel, 6'd0};
	assign flag_scalar_valid = (cnt_result_queue != 2'd0) && (reg_group_mask_head != 3'd0) &&
	                           silu_table_loaded && (~flag_fatal);
	assign flag_scalar_last = (reg_group_mask_head == (3'b001 << wire_selected_lane));

	assign flag_base_aligned = (i_channel_base == 5'd0) || (i_channel_base == 5'd3) ||
	                           (i_channel_base == 5'd6) || (i_channel_base == 5'd9) ||
	                           (i_channel_base == 5'd12) || (i_channel_base == 5'd15) ||
	                           (i_channel_base == 5'd18) || (i_channel_base == 5'd21);
	assign flag_lane_shape_valid = i_layer ? (i_lane_mask == 3'b111) :
	                               ((i_lane_mask == 3'b001) || (i_lane_mask == 3'b010) ||
	                                (i_lane_mask == 3'b100));
	assign flag_input_shape_fault = (~flag_base_aligned) || (~flag_lane_shape_valid) ||
	                                (i_layer && (i_channel_base > 5'd21)) ||
	                                ((~i_layer) && ((i_channel_base + {3'd0, (i_lane_mask[2] ? 2'd2 : i_lane_mask[1] ? 2'd1 : 2'd0)}) > 5'd15));
	assign o_input_ready = (cnt_result_queue < 2'd2) && silu_table_loaded &&
	                       (~silu_table_fault) && (~i_table_valid) && (~flag_fatal);
	assign flag_input_accept = i_input_valid && o_input_ready;
	assign flag_group_push = flag_input_accept && (~i_result_fault) && (~flag_input_shape_fault);
	assign flag_group_pop = flag_pre_accept && flag_scalar_last;

	assign flag_silu_accept = pre_result_valid && (~pre_result_fault) &&
	                          (cnt_meta < 4'd8) && silu_input_ready && (~flag_fatal);
	assign flag_pre_advance = (~pre_result_valid) || flag_silu_accept;
	assign flag_pre_accept = flag_pre_advance && flag_scalar_valid;

	assign flag_post_advance = (~post_result_valid) ||
	                           (i_output_ready && (~post_result_fault) && (~flag_fatal));
	assign flag_silu_output_ready = flag_post_advance && (cnt_meta != 4'd0) && (~flag_fatal);
	assign flag_post_accept = silu_output_valid && flag_silu_output_ready;
	assign flag_output_accept = o_output_valid && i_output_ready;
	assign wire_post_product = $signed(silu_output_data) * $signed(POST_FACTOR);
	assign wire_output_saturated = ($signed(post_result_data) > 16'sd127) ? 8'sd127 :
	                               ($signed(post_result_data) < -16'sd128) ? -8'sd128 :
	                               post_result_data[7:0];
	assign flag_fault_event = (flag_input_accept && (i_result_fault || flag_input_shape_fault)) ||
	                          (pre_result_valid && pre_result_fault) ||
	                          (post_result_valid && post_result_fault) || silu_table_fault;
	assign flag_pipeline_empty = (cnt_result_queue == 2'd0) && (cnt_pre_inflight == 4'd0) &&
	                             (cnt_meta == 4'd0) && (cnt_post_inflight == 4'd0);
	assign flag_table_forward = i_table_valid && flag_pipeline_empty && (~flag_fatal);

	assign o_table_ready = silu_table_ready && flag_pipeline_empty && (~flag_fatal);
	assign o_table_loaded = silu_table_loaded;
	assign o_table_fault = silu_table_fault;
	assign o_output_valid = post_result_valid && (~post_result_fault) && (~flag_fatal);
	assign o_output_data = wire_output_saturated;
	assign o_output_tag = post_result_tag;
	assign o_fault = flag_fatal || o_table_fault;
	assign o_result_queue_count = cnt_result_queue;
	assign o_meta_count = cnt_meta;
	assign o_pre_busy = (cnt_pre_inflight != 4'd0);
	assign o_silu_busy = (cnt_meta != 4'd0);
	assign o_post_busy = (cnt_post_inflight != 4'd0);
	assign o_pre_accept = flag_pre_accept;
	assign o_silu_accept = flag_silu_accept;
	assign o_post_accept = flag_post_accept;

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_group_data_head <= 96'd0;
			reg_group_data_tail <= 96'd0;
			reg_group_layer_head <= 1'b0;
			reg_group_layer_tail <= 1'b0;
			reg_group_position_head <= 4'd0;
			reg_group_position_tail <= 4'd0;
			reg_group_channel_head <= 5'd0;
			reg_group_channel_tail <= 5'd0;
			reg_group_mask_head <= 3'd0;
			reg_group_mask_tail <= 3'd0;
			cnt_result_queue <= 2'd0;
		end else if(flag_fault_event)begin
			reg_group_mask_head <= 3'd0;
			reg_group_mask_tail <= 3'd0;
			cnt_result_queue <= 2'd0;
		end else begin
			case({flag_group_push, flag_group_pop})
				2'b10:begin
					cnt_result_queue <= cnt_result_queue + 1'b1;
					if(cnt_result_queue == 2'd0)begin
						reg_group_data_head <= i_result_data;
						reg_group_layer_head <= i_layer;
						reg_group_position_head <= i_position;
						reg_group_channel_head <= i_channel_base;
						reg_group_mask_head <= i_lane_mask;
					end else begin
						reg_group_data_tail <= i_result_data;
						reg_group_layer_tail <= i_layer;
						reg_group_position_tail <= i_position;
						reg_group_channel_tail <= i_channel_base;
						reg_group_mask_tail <= i_lane_mask;
						if(flag_pre_accept)begin
							reg_group_mask_head <= reg_group_mask_head & ~(3'b001 << wire_selected_lane);
						end
					end
				end
				2'b01:begin
					cnt_result_queue <= cnt_result_queue - 1'b1;
					if(cnt_result_queue == 2'd2)begin
						reg_group_data_head <= reg_group_data_tail;
						reg_group_layer_head <= reg_group_layer_tail;
						reg_group_position_head <= reg_group_position_tail;
						reg_group_channel_head <= reg_group_channel_tail;
						reg_group_mask_head <= reg_group_mask_tail;
					end else begin
						reg_group_mask_head <= 3'd0;
					end
				end
				2'b11:begin
					cnt_result_queue <= cnt_result_queue;
					if(cnt_result_queue == 2'd2)begin
						reg_group_data_head <= reg_group_data_tail;
						reg_group_layer_head <= reg_group_layer_tail;
						reg_group_position_head <= reg_group_position_tail;
						reg_group_channel_head <= reg_group_channel_tail;
						reg_group_mask_head <= reg_group_mask_tail;
						reg_group_data_tail <= i_result_data;
						reg_group_layer_tail <= i_layer;
						reg_group_position_tail <= i_position;
						reg_group_channel_tail <= i_channel_base;
						reg_group_mask_tail <= i_lane_mask;
					end else begin
						reg_group_data_head <= i_result_data;
						reg_group_layer_head <= i_layer;
						reg_group_position_head <= i_position;
						reg_group_channel_head <= i_channel_base;
						reg_group_mask_head <= i_lane_mask;
					end
				end
				default:begin
					if(flag_pre_accept)begin
						reg_group_mask_head <= reg_group_mask_head & ~(3'b001 << wire_selected_lane);
					end
				end
			endcase
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_meta_read <= 3'd0;
			cnt_meta_write <= 3'd0;
			cnt_meta <= 4'd0;
		end else if(flag_fault_event)begin
			cnt_meta_read <= 3'd0;
			cnt_meta_write <= 3'd0;
			cnt_meta <= 4'd0;
		end else begin
			if(flag_silu_accept)begin
				reg_meta_fifo[cnt_meta_write] <= pre_result_tag;
				cnt_meta_write <= cnt_meta_write + 1'b1;
			end
			if(flag_post_accept)begin
				cnt_meta_read <= cnt_meta_read + 1'b1;
			end
			case({flag_silu_accept, flag_post_accept})
				2'b10: cnt_meta <= cnt_meta + 1'b1;
				2'b01: cnt_meta <= cnt_meta - 1'b1;
				default: cnt_meta <= cnt_meta;
			endcase
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_pre_inflight <= 4'd0;
			cnt_post_inflight <= 4'd0;
			flag_fatal <= 1'b0;
		end else if(flag_fault_event)begin
			cnt_pre_inflight <= 4'd0;
			cnt_post_inflight <= 4'd0;
			flag_fatal <= 1'b1;
		end else begin
			case({flag_pre_accept, flag_silu_accept})
				2'b10: cnt_pre_inflight <= cnt_pre_inflight + 1'b1;
				2'b01: cnt_pre_inflight <= cnt_pre_inflight - 1'b1;
				default: cnt_pre_inflight <= cnt_pre_inflight;
			endcase
			case({flag_post_accept, flag_output_accept})
				2'b10: cnt_post_inflight <= cnt_post_inflight + 1'b1;
				2'b01: cnt_post_inflight <= cnt_post_inflight - 1'b1;
				default: cnt_post_inflight <= cnt_post_inflight;
			endcase
			flag_fatal <= flag_fatal;
		end
	end

	road_round_shift road_round_shift_Inst_pre(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_advance(flag_pre_advance),
		.i_input_valid(flag_scalar_valid),
		.i_product(wire_pre_product),
		.i_shift(wire_pre_shift),
		.i_tag(wire_scalar_tag),
		.o_result_valid(pre_result_valid),
		.o_result_data(pre_result_data),
		.o_result_tag(pre_result_tag),
		.o_fault(pre_result_fault)
	);

	silu_shared_unit silu_shared_unit_Inst_shared(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_table_valid(flag_table_forward),
		.i_table_addr(i_table_addr),
		.i_table_data(i_table_data),
		.i_input_valid(pre_result_valid && (~pre_result_fault) && (cnt_meta < 4'd8) && (~flag_fatal)),
		.i_input_data(pre_result_data),
		.i_output_ready(flag_silu_output_ready),
		.o_table_ready(silu_table_ready),
		.o_input_ready(silu_input_ready),
		.o_output_valid(silu_output_valid),
		.o_output_data(silu_output_data),
		.o_table_loaded(silu_table_loaded),
		.o_table_fault(silu_table_fault)
	);

	road_round_shift road_round_shift_Inst_post(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_advance(flag_post_advance),
		.i_input_valid(silu_output_valid && (cnt_meta != 4'd0) && (~flag_fatal)),
		.i_product(wire_post_product),
		.i_shift(POST_SHIFT),
		.i_tag(reg_meta_fifo[cnt_meta_read]),
		.o_result_valid(post_result_valid),
		.o_result_data(post_result_data),
		.o_result_tag(post_result_tag),
		.o_fault(post_result_fault)
	);

endmodule
