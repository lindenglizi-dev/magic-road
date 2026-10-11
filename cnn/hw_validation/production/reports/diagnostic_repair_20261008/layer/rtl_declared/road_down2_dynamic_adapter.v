`timescale 1ns / 1ps

// Fixed TEST-package adapter; not a deployment parameter loader.
// ponytail: one in-flight batch; reuse the serial core instead of adding a FIFO.
module road_down2_dynamic_adapter(
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
    reg flag_pending;
    reg [15:0]reg_last_tag;
    wire core_ready;
    wire core_fault;
    wire signed [15:0]wire_result;
    wire [4:0]wire_channel_beta = i_channel_base + 5'd1;
    wire [4:0]wire_channel_gamma = i_channel_base + 5'd2;
    wire [15:0]wire_tag_alpha = {i_layer,i_position,i_channel_base,6'd0};
    wire [15:0]wire_tag_beta = {i_layer,i_position,wire_channel_beta,6'd0};
    wire [15:0]wire_tag_gamma = {i_layer,i_position,wire_channel_gamma,6'd0};
    wire flag_shape_fault = i_layer ? (i_lane_mask != 3'b111 || i_channel_base > 5'd21) :
        !((i_lane_mask == 3'b001 && i_channel_base <= 5'd15) ||
          (i_lane_mask == 3'b010 && i_channel_base <= 5'd14) ||
          (i_lane_mask == 3'b100 && i_channel_base <= 5'd13));
    assign o_input_ready = core_ready && !i_table_valid;
    assign o_fault = core_fault;
    assign o_table_fault = core_fault; // Aggregate fatal status; not table-only telemetry.
    assign o_output_data = wire_result[7:0]; // Core already saturates activated INT8.
    assign o_result_queue_count = {1'b0,flag_pending};
    assign o_meta_count = flag_pending ? 4'd1 : 4'd0;
    // Legacy overlap counters are unavailable for this unchanged serial core.
    // Testbench observes actual core states; these pins must not be used for timing.
    assign o_pre_busy = 1'b0;
    assign o_silu_busy = 1'b0;
    assign o_post_busy = 1'b0;
    assign o_pre_accept = 1'b0;
    assign o_silu_accept = 1'b0;
    assign o_post_accept = 1'b0;
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_pending <= 1'b0;
            reg_last_tag <= 16'd0;
        end else if (core_fault) begin
            flag_pending <= 1'b0;
        end else if (i_input_valid && o_input_ready) begin
            flag_pending <= 1'b1;
            reg_last_tag <= i_lane_mask[2] ? wire_tag_gamma :
                            i_lane_mask[1] ? wire_tag_beta : wire_tag_alpha;
        end else if (o_output_valid && i_output_ready && o_output_tag == reg_last_tag) begin
            flag_pending <= 1'b0;
        end
    end
    road_dynamic_postprocess u_chain(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_table_valid(i_table_valid),.i_table_addr(i_table_addr),.i_table_data(i_table_data),
        .o_table_ready(o_table_ready),.o_table_loaded(o_table_loaded),
        .i_input_valid(i_input_valid && !i_table_valid),.o_input_ready(core_ready),
        .i_accumulators(i_result_data),
        .i_pre_multipliers({32'd65536,32'd65536,32'd65536}),
        .i_pre_shifts({6'd24,6'd24,6'd24}),
        .i_post_multiplier(32'd16777216),.i_post_shift(6'd31),.i_activate(1'b1),
        .i_lane_mask(i_lane_mask),.i_tags({wire_tag_gamma,wire_tag_beta,wire_tag_alpha}),
        .i_input_fault(i_result_fault || flag_shape_fault),
        .i_output_ready(i_output_ready),.o_output_valid(o_output_valid),
        .o_output_data(wire_result),.o_output_tag(o_output_tag),.o_output_int16(),
        .o_fault(core_fault)
    );
endmodule
