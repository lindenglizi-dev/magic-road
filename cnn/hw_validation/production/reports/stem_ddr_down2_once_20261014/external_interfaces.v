module road_frontend_shared_core(
    input i_clk,
    input i_rstn,
    input i_select_valid,
    input i_select_down2,
    output o_select_ready,
    output o_selected_down2,
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
    input i_commit_ready,
    output o_busy,
    output o_done,
    output o_fault,
    output [31:0]o_core_cycles,
    input i_export_start,
    input i_output_ready,
    output o_output_valid,
    output signed [7:0]o_output_data,
    output [8:0]o_output_index,
    output o_export_done
);
endmodule
module road_down2_tile_scheduler
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
endmodule
module road_stem_tile_scheduler(
	input i_clk,
	input i_rstn,
	input i_table_loaded,
	input i_load_valid,
	input [2:0]i_load_kind,
	input [8:0]i_load_addr,
	input signed [31:0]i_load_data,
	output o_load_ready,
	input i_start,
	output o_busy,
	output o_done,
	output o_fault,
	output [31:0]o_core_cycles,
	output o_mac_valid,
	input i_mac_ready,
	output o_mac_first,
	output o_mac_last,
	output [7:0]o_mac_mask,
	output [63:0]o_mac_activation,
	output [191:0]o_mac_weight,
	output [95:0]o_mac_bias,
	input i_mac_result_valid,
	output o_mac_result_ready,
	input [95:0]i_mac_result,
	input i_mac_fault,
	output o_pp_valid,
	input i_pp_ready,
	output [95:0]o_pp_acc,
	output [95:0]o_pp_multipliers,
	output [17:0]o_pp_shifts,
	output [31:0]o_pp_post_multiplier,
	output [5:0]o_pp_post_shift,
	output [2:0]o_pp_mask,
	output [47:0]o_pp_tags,
	input i_pp_valid,
	output o_pp_ready,
	input signed [15:0]i_pp_data,
	input [15:0]i_pp_tag,
	input i_pp_int16,
	input i_pp_fault,
	input i_commit_ready,
	input i_export_start,
	output o_output_valid,
	input i_output_ready,
	output signed [7:0]o_output_data,
	output [7:0]o_output_index,
	output o_export_done
);
endmodule
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
module road_dynamic_requant(
	input i_clk,
	input i_rstn,
	input i_input_valid,
	input signed [31:0]i_accumulator,
	input [30:0]i_multiplier,
	input [5:0]i_shift,
	input [15:0]i_tag,
	output o_input_ready,
	input i_output_ready,
	output o_output_valid,
	output signed [15:0]o_output_data,
	output [15:0]o_output_tag,
	output o_fault
);
endmodule
module road_round_shift
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 算术流水工作时钟
	input i_rstn,                               // 异步低有效取消复位

	//-----------------用户接口-----------------//
	input i_advance,                            // 外层控制的共同推进许可
	input i_input_valid,                        // 本次推进携带有效乘积
	input signed [63:0]i_product,               // 上游完整有符号乘积
	input [5:0]i_shift,                         // 非负二进制除数指数
	input [15:0]i_tag,                          // 与乘积绑定的结果身份

	//----------------RESULT接口----------------//

	//RESULT接口
	output o_result_valid,                      // 完成舍入的结果有效标志
	output [15:0]o_result_data,                 // 饱和后的有符号整数位型
	output [15:0]o_result_tag,                  // 原输入身份随结果返回
	output o_fault                              // 非法移位或乘积最小值标志
);
endmodule
module silu_shared_unit
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 单一工作时钟
	input i_rstn,                               // 低有效异步复位

	//-----------------用户接口-----------------//

	//TABLE接口
	input i_table_valid,                        // 运行时表项有效
	input [9:0]i_table_addr,                    // 严格递增装载地址
	input signed [15:0]i_table_data,            // 有符号Q7.8表项
	input i_input_valid,                        // 推理输入有效
	input signed [15:0]i_input_data,            // 有符号Q7.8输入
	input i_output_ready,                       // 下游结果接收能力
	output o_table_ready,                       // 当前表项接收许可
	output o_input_ready,                       // 当前输入接收许可
	output o_output_valid,                      // SiLU结果有效
	output signed [15:0]o_output_data,          // 有符号Q7.8结果
	output o_table_loaded,                      // 完整表已激活
	output o_table_fault                        // 装载顺序故障
);
endmodule
