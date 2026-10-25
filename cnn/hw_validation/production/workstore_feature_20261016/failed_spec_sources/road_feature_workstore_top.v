`timescale 1ns / 1ps
// ֱ�ӽ�����϶��㣺��ʵfeature�ͻ���Ψһ4ERAM�����ּ�ԭ����owner��
// ���ۺ���Դ�۲죬���ǰ弶I/O���㡢DDR�ջ���ʱ��ǩ�ˡ�
module road_feature_workstore_top(
    input  i_clk,
    input  i_rstn,
    input [3:0] i_block_id,
    output [3:0] o_block_id,
    input  i_start,
    input  i_cancel,
    output  o_start_ready,
    output  o_busy,
    output  o_done,
    output  o_fault,
    output [2:0] o_layer,
    output [6:0] o_tile_y,
    output [7:0] o_tile_x,
    output  o_parameter_valid,
    output [6:0] o_parameter_channel,
    output [4:0] o_parameter_group,
    output [2:0] o_parameter_window,
    input  i_parameter_ready,
    input  i_parameter_response_valid,
    output  o_parameter_response_ready,
    input [3:0] i_parameter_response_block_id,
    input [2:0] i_parameter_response_layer,
    input [6:0] i_parameter_response_channel,
    input [4:0] i_parameter_response_group,
    input [2:0] i_parameter_response_window,
    input [191:0] i_parameter_weight,
    input [247:0] i_parameter_data,
    input  i_parameter_error,
    output  o_read_valid,
    output [31:0] o_read_address,
    input  i_read_ready,
    input  i_read_response_valid,
    output  o_read_response_ready,
    input [31:0] i_read_response_address,
    input [127:0] i_read_response_data,
    input  i_read_error,
    output  o_write_valid,
    output [31:0] o_write_address,
    output [7:0] o_write_data,
    output [8:0] o_write_sum,
    input  i_write_ready,
    output  o_barrier_valid,
    input  i_barrier_ready,
    input [3:0] i_barrier_block_id,
    input [2:0] i_barrier_layer,
    input i_table_valid,
    input [9:0] i_table_addr,
    input signed [15:0] i_table_data,
    output o_table_ready,
    output o_table_loaded
);
    wire  link_i_table_loaded; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_core_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_core_ready; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_core_first; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_core_last; // ͬ���ڲ�ֱ���ӿ�
    wire [7:0] link_o_core_input_mask; // ͬ���ڲ�ֱ���ӿ�
    wire [63:0] link_o_core_activation; // ͬ���ڲ�ֱ���ӿ�
    wire [191:0] link_o_core_weight; // ͬ���ڲ�ֱ���ӿ�
    wire [95:0] link_o_core_bias; // ͬ���ڲ�ֱ���ӿ�
    wire [2:0] link_o_core_output_mask; // ͬ���ڲ�ֱ���ӿ�
    wire [47:0] link_o_core_tags; // ͬ���ڲ�ֱ���ӿ�
    wire [95:0] link_o_core_addresses; // ͬ���ڲ�ֱ���ӿ�
    wire [95:0] link_o_core_pre_multiplier; // ͬ���ڲ�ֱ���ӿ�
    wire [17:0] link_o_core_pre_shift; // ͬ���ڲ�ֱ���ӿ�
    wire [31:0] link_o_core_post_multiplier; // ͬ���ڲ�ֱ���ӿ�
    wire [5:0] link_o_core_post_shift; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_core_residual; // ͬ���ڲ�ֱ���ӿ�
    wire [23:0] link_o_core_bypass; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_core_output_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_core_output_ready; // ͬ���ڲ�ֱ���ӿ�
    wire [15:0] link_i_core_output_tag; // ͬ���ڲ�ֱ���ӿ�
    wire [31:0] link_i_core_output_address; // ͬ���ڲ�ֱ���ӿ�
    wire [7:0] link_i_core_output_data; // ͬ���ڲ�ֱ���ӿ�
    wire [8:0] link_i_core_output_sum; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_core_fault; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_byte_req_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_byte_req_ready; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_byte_req_write; // ͬ���ڲ�ֱ���ӿ�
    wire [11:0] link_o_byte_req_addr; // ͬ���ڲ�ֱ���ӿ�
    wire [7:0] link_o_byte_req_data; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_byte_rsp_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_byte_rsp_ready; // ͬ���ڲ�ֱ���ӿ�
    wire [7:0] link_i_byte_rsp_data; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_byte_rsp_error; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_weight_req_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_weight_req_ready; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_weight_req_write; // ͬ���ڲ�ֱ���ӿ�
    wire [4:0] link_o_weight_req_group; // ͬ���ڲ�ֱ���ӿ�
    wire [191:0] link_o_weight_req_data; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_weight_rsp_valid; // ͬ���ڲ�ֱ���ӿ�
    wire  link_o_weight_rsp_ready; // ͬ���ڲ�ֱ���ӿ�
    wire [191:0] link_i_weight_rsp_data; // ͬ���ڲ�ֱ���ӿ�
    wire  link_i_weight_rsp_error; // ͬ���ڲ�ֱ���ӿ�
    wire flag_client_fault; // �ͻ�����
    wire flag_store_fault; // ������Խ�����
    assign o_fault = flag_client_fault | flag_store_fault | link_i_core_fault; // ����ȥ��һ�����߹���
    assign o_table_loaded = link_i_table_loaded; // ʵ��ȫ��װ��״̬
    road_feature_blocks_client client_Inst(
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_block_id(i_block_id),
        .o_block_id(o_block_id),
        .i_start(i_start),
        .i_cancel(i_cancel),
        .i_table_loaded(link_i_table_loaded),
        .o_start_ready(o_start_ready),
        .o_busy(o_busy),
        .o_done(o_done),
        .o_fault(flag_client_fault),
        .o_layer(o_layer),
        .o_tile_y(o_tile_y),
        .o_tile_x(o_tile_x),
        .o_parameter_valid(o_parameter_valid),
        .o_parameter_channel(o_parameter_channel),
        .o_parameter_group(o_parameter_group),
        .o_parameter_window(o_parameter_window),
        .i_parameter_ready(i_parameter_ready),
        .i_parameter_response_valid(i_parameter_response_valid),
        .o_parameter_response_ready(o_parameter_response_ready),
        .i_parameter_response_block_id(i_parameter_response_block_id),
        .i_parameter_response_layer(i_parameter_response_layer),
        .i_parameter_response_channel(i_parameter_response_channel),
        .i_parameter_response_group(i_parameter_response_group),
        .i_parameter_response_window(i_parameter_response_window),
        .i_parameter_weight(i_parameter_weight),
        .i_parameter_data(i_parameter_data),
        .i_parameter_error(i_parameter_error),
        .o_read_valid(o_read_valid),
        .o_read_address(o_read_address),
        .i_read_ready(i_read_ready),
        .i_read_response_valid(i_read_response_valid),
        .o_read_response_ready(o_read_response_ready),
        .i_read_response_address(i_read_response_address),
        .i_read_response_data(i_read_response_data),
        .i_read_error(i_read_error),
        .o_write_valid(o_write_valid),
        .o_write_address(o_write_address),
        .o_write_data(o_write_data),
        .o_write_sum(o_write_sum),
        .i_write_ready(i_write_ready),
        .o_barrier_valid(o_barrier_valid),
        .i_barrier_ready(i_barrier_ready),
        .i_barrier_block_id(i_barrier_block_id),
        .i_barrier_layer(i_barrier_layer),
        .o_core_valid(link_o_core_valid),
        .i_core_ready(link_i_core_ready),
        .o_core_first(link_o_core_first),
        .o_core_last(link_o_core_last),
        .o_core_input_mask(link_o_core_input_mask),
        .o_core_activation(link_o_core_activation),
        .o_core_weight(link_o_core_weight),
        .o_core_bias(link_o_core_bias),
        .o_core_output_mask(link_o_core_output_mask),
        .o_core_tags(link_o_core_tags),
        .o_core_addresses(link_o_core_addresses),
        .o_core_pre_multiplier(link_o_core_pre_multiplier),
        .o_core_pre_shift(link_o_core_pre_shift),
        .o_core_post_multiplier(link_o_core_post_multiplier),
        .o_core_post_shift(link_o_core_post_shift),
        .o_core_residual(link_o_core_residual),
        .o_core_bypass(link_o_core_bypass),
        .i_core_output_valid(link_i_core_output_valid),
        .o_core_output_ready(link_o_core_output_ready),
        .i_core_output_tag(link_i_core_output_tag),
        .i_core_output_address(link_i_core_output_address),
        .i_core_output_data(link_i_core_output_data),
        .i_core_output_sum(link_i_core_output_sum),
        .i_core_fault(link_i_core_fault),
        .o_byte_req_valid(link_o_byte_req_valid),
        .i_byte_req_ready(link_i_byte_req_ready),
        .o_byte_req_write(link_o_byte_req_write),
        .o_byte_req_addr(link_o_byte_req_addr),
        .o_byte_req_data(link_o_byte_req_data),
        .i_byte_rsp_valid(link_i_byte_rsp_valid),
        .o_byte_rsp_ready(link_o_byte_rsp_ready),
        .i_byte_rsp_data(link_i_byte_rsp_data),
        .i_byte_rsp_error(link_i_byte_rsp_error),
        .o_weight_req_valid(link_o_weight_req_valid),
        .i_weight_req_ready(link_i_weight_req_ready),
        .o_weight_req_write(link_o_weight_req_write),
        .o_weight_req_group(link_o_weight_req_group),
        .o_weight_req_data(link_o_weight_req_data),
        .i_weight_rsp_valid(link_i_weight_rsp_valid),
        .o_weight_rsp_ready(link_o_weight_rsp_ready),
        .i_weight_rsp_data(link_i_weight_rsp_data),
        .i_weight_rsp_error(link_i_weight_rsp_error)
    );
    road_feature_workstore workstore_Inst(
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .o_fault(flag_store_fault),
        .i_byte_req_valid(link_o_byte_req_valid),
        .o_byte_req_ready(link_i_byte_req_ready),
        .i_byte_req_write(link_o_byte_req_write),
        .i_byte_req_addr(link_o_byte_req_addr),
        .i_byte_req_data(link_o_byte_req_data),
        .o_byte_rsp_valid(link_i_byte_rsp_valid),
        .i_byte_rsp_ready(link_o_byte_rsp_ready),
        .o_byte_rsp_data(link_i_byte_rsp_data),
        .o_byte_rsp_error(link_i_byte_rsp_error),
        .i_weight_req_valid(link_o_weight_req_valid),
        .o_weight_req_ready(link_i_weight_req_ready),
        .i_weight_req_write(link_o_weight_req_write),
        .i_weight_req_group(link_o_weight_req_group),
        .i_weight_req_data(link_o_weight_req_data),
        .o_weight_rsp_valid(link_i_weight_rsp_valid),
        .i_weight_rsp_ready(link_o_weight_rsp_ready),
        .o_weight_rsp_data(link_i_weight_rsp_data),
        .o_weight_rsp_error(link_i_weight_rsp_error)
    );
    road_csp_first_probe arithmetic_Inst(
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_input_fault(1'b0),
        .i_table_valid(i_table_valid),
        .i_table_addr(i_table_addr),
        .i_table_data(i_table_data),
        .o_table_ready(o_table_ready),
        .o_table_loaded(link_i_table_loaded),
        .i_input_valid(link_o_core_valid),
        .i_first(link_o_core_first),
        .i_last(link_o_core_last),
        .i_lane_mask(link_o_core_input_mask),
        .i_activation_data(link_o_core_activation),
        .i_weight_data(link_o_core_weight),
        .i_bias_data(link_o_core_bias),
        .i_output_mask(link_o_core_output_mask),
        .i_tags(link_o_core_tags),
        .i_addresses(link_o_core_addresses),
        .i_pre_multipliers(link_o_core_pre_multiplier),
        .i_pre_shifts(link_o_core_pre_shift),
        .i_post_multiplier(link_o_core_post_multiplier),
        .i_post_shift(link_o_core_post_shift),
        .i_residual(link_o_core_residual),
        .i_bypass_data(link_o_core_bypass),
        .i_output_ready(link_o_core_output_ready),
        .o_input_ready(link_i_core_ready),
        .o_output_valid(link_i_core_output_valid),
        .o_output_data(link_i_core_output_data),
        .o_output_tag(link_i_core_output_tag),
        .o_output_address(link_i_core_output_address),
        .o_output_sum(link_i_core_output_sum),
        .o_fault(link_i_core_fault)
    );
endmodule
