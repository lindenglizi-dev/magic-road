module road_mac_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 百兆工作时钟
	input i_rstn,                               // 异步低有效复位

	//-----------------用户接口-----------------//
	input i_input_valid,                        // 输入负载保持有效标志
	input i_first,                              // 当前组以偏置替代历史累加值
	input i_last,                               // 当前组结束本次归约序列
	input [7:0]i_lane_mask,                     // 八条输入通道共享使能掩码
	input [63:0]i_activation_data,              // 八个低字节优先有符号激活值
	input [191:0]i_weight_data,                 // 三组八通道低字节优先权重
	input [95:0]i_bias_data,                    // 三个低字优先有符号偏置
	input i_result_ready,                       // 下游允许接受保持型终态
	output o_input_ready,                       // 当前序列允许接受输入组
	output o_result_valid,                      // 结果负载保持有效标志
	output [95:0]o_result_data,                 // 三个低字优先INT32结果
	output o_fault                              // 任一路末组INT32越界标志
);
endmodule
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
    output o_fault,
    output [1:0]o_queue_count,
    output [3:0]o_pending_count,
    output [3:0]o_meta_count,
    output o_pre_busy,
    output o_silu_busy,
    output o_post_busy,
    output o_pre_accept,
    output o_silu_accept,
    output o_post_accept
);
endmodule
