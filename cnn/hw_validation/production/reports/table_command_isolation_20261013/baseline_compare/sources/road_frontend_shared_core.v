`timescale 1ns / 1ps

// Stem/down2互斥复用一个MAC和一个后处理链；不包含整帧存储和DDR。
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
    reg flag_owner_down2; // 只在无在途、无未导出结果时改变。
    reg flag_unexported; // done之后必须完成真实输出读口握手。
    reg flag_address_fault; // Stem的窄地址不得静默截断。
    wire flag_commands, flag_idle, flag_table_enable;
    wire s_load_ready, d_load_ready, s_busy, d_busy, s_done, d_done, s_fault, d_fault;
    wire [31:0]s_core_cycles, d_core_cycles;
    wire s_output_valid, d_output_valid, s_export_done, d_export_done;
    wire [7:0]s_output_data, s_output_index, d_output_data;
    wire [8:0]d_output_index;
    wire s_mac_valid, s_mac_ready, s_mac_first, s_mac_last, s_mac_result_valid, s_mac_result_ready, s_mac_fault;
    wire d_mac_valid, d_mac_ready, d_mac_first, d_mac_last, d_mac_result_valid, d_mac_result_ready, d_mac_fault;
    wire [7:0]s_mac_mask, d_mac_mask;
    wire [63:0]s_mac_activation, d_mac_activation;
    wire [191:0]s_mac_weight, d_mac_weight;
    wire [95:0]s_mac_bias, d_mac_bias, s_mac_result, d_mac_result;
    wire s_pp_valid, s_pp_ready, s_pp_output_valid, s_pp_output_ready;
    wire d_pp_valid, d_pp_ready, d_pp_output_valid, d_pp_output_ready, d_pp_input_fault;
    wire [95:0]s_pp_acc, d_pp_acc, s_pp_multipliers, d_pp_multipliers;
    wire [17:0]s_pp_shifts, d_pp_shifts;
    wire [31:0]s_pp_post_multiplier, d_pp_post_multiplier;
    wire [5:0]s_pp_post_shift, d_pp_post_shift;
    wire [2:0]s_pp_mask, d_pp_mask;
    wire [47:0]s_pp_tags, d_pp_tags;
    wire mac_ready, mac_result_valid, mac_fault;
    wire [95:0]mac_result;
    wire pp_ready, pp_valid, pp_int16, pp_fault, pp_table_ready;
    wire signed [15:0]pp_data;
    wire [15:0]pp_tag;
    wire [1:0]pp_queue_count;
    wire [3:0]pp_pending_count, pp_meta_count;
    wire pp_pre_busy, pp_silu_busy, pp_post_busy, pp_pre_accept, pp_silu_accept, pp_post_accept;

    assign o_selected_down2=flag_owner_down2;
    assign o_fault=flag_address_fault || s_fault || d_fault || pp_fault || (mac_result_valid && mac_fault);
    // 两调度器load_ready仅在IDLE成立；勿回读依赖PP ready的发射valid形成组合环。
    assign flag_idle=s_load_ready && d_load_ready && !s_busy && !d_busy &&
                     !mac_result_valid && !pp_valid &&
                     pp_pending_count==4'd0 && pp_queue_count==2'd0 &&
                     !pp_pre_busy && !pp_silu_busy && !pp_post_busy;
    assign o_select_ready=i_rstn && flag_idle && !flag_unexported && !o_done && !o_fault &&
                          !i_start && !i_load_valid && !i_export_start && !i_table_valid;
    // 等待交接/装表的valid不能阻止旧主排空；命令优先级由各ready及准入条件决定。
    assign flag_commands=i_rstn && !o_fault;
    assign flag_table_enable=i_rstn && flag_idle && !flag_unexported && !o_done && !o_fault &&
                             !i_start && !i_load_valid && !i_export_start;
    assign o_table_ready=flag_table_enable && pp_table_ready;
    assign o_table_fault=pp_fault; // 与旧adapter一致，是后处理聚合故障，不是仅表错误。
    assign o_load_ready=flag_commands && !flag_unexported && !o_done &&
                        (flag_owner_down2 ? d_load_ready : s_load_ready);
    assign o_busy=flag_owner_down2 ? d_busy : s_busy;
    assign o_done=flag_owner_down2 ? d_done : s_done;
    assign o_core_cycles=flag_owner_down2 ? d_core_cycles : s_core_cycles;
    assign o_output_valid=flag_owner_down2 ? d_output_valid : s_output_valid;
    assign o_output_data=flag_owner_down2 ? d_output_data : s_output_data;
    assign o_output_index=flag_owner_down2 ? d_output_index : {1'b0,s_output_index};
    assign o_export_done=flag_owner_down2 ? d_export_done : s_export_done;
    assign s_mac_ready=!flag_owner_down2 && mac_ready;
    assign d_mac_ready=flag_owner_down2 && mac_ready;
    assign s_mac_result_valid=!flag_owner_down2 && mac_result_valid;
    assign d_mac_result_valid=flag_owner_down2 && mac_result_valid;
    assign s_mac_result=mac_result;
    assign d_mac_result=mac_result;
    assign s_mac_fault=mac_fault;
    assign d_mac_fault=mac_fault;
    assign s_pp_ready=!flag_owner_down2 && pp_ready;
    assign d_pp_ready=flag_owner_down2 && pp_ready;
    assign s_pp_output_valid=!flag_owner_down2 && pp_valid;
    assign d_pp_output_valid=flag_owner_down2 && pp_valid;

    // 同一复位立即取消两个调度器及算术链；释放由调用者同步，之后重装完整表。
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) begin
            flag_owner_down2<=1'b0;
            flag_unexported<=1'b0;
            flag_address_fault<=1'b0;
        end else begin
            if(i_select_valid && o_select_ready) flag_owner_down2<=i_select_down2;
            if(o_done) flag_unexported<=1'b1;
            if(o_export_done) flag_unexported<=1'b0;
            if(i_load_valid && o_load_ready && !flag_owner_down2 && i_load_addr[10:9]!=2'd0)
                flag_address_fault<=1'b1;
        end
    end

    road_stem_tile_scheduler u_stem(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_loaded(o_table_loaded),
        .i_load_valid(i_load_valid && o_load_ready && !flag_owner_down2 && i_load_addr[10:9]==2'd0),
        .i_load_kind(i_load_kind),.i_load_addr(i_load_addr[8:0]),.i_load_data(i_load_data),.o_load_ready(s_load_ready),
        .i_start(i_start && flag_commands && !flag_unexported && !o_done && !flag_owner_down2),
        .o_busy(s_busy),.o_done(s_done),.o_fault(s_fault),.o_core_cycles(s_core_cycles),
        .o_mac_valid(s_mac_valid),.i_mac_ready(s_mac_ready),.o_mac_first(s_mac_first),.o_mac_last(s_mac_last),
        .o_mac_mask(s_mac_mask),.o_mac_activation(s_mac_activation),.o_mac_weight(s_mac_weight),.o_mac_bias(s_mac_bias),
        .i_mac_result_valid(s_mac_result_valid),.o_mac_result_ready(s_mac_result_ready),.i_mac_result(s_mac_result),.i_mac_fault(s_mac_fault),
        .o_pp_valid(s_pp_valid),.i_pp_ready(s_pp_ready),.o_pp_acc(s_pp_acc),.o_pp_multipliers(s_pp_multipliers),
        .o_pp_shifts(s_pp_shifts),.o_pp_post_multiplier(s_pp_post_multiplier),.o_pp_post_shift(s_pp_post_shift),
        .o_pp_mask(s_pp_mask),.o_pp_tags(s_pp_tags),.i_pp_valid(s_pp_output_valid),.o_pp_ready(s_pp_output_ready),
        .i_pp_data(pp_data),.i_pp_tag(pp_tag),.i_pp_int16(pp_int16),.i_pp_fault(pp_fault),
        .i_commit_ready(i_commit_ready),.i_export_start(i_export_start && flag_commands && !flag_owner_down2),
        .o_output_valid(s_output_valid),.i_output_ready(i_output_ready && !flag_owner_down2),
        .o_output_data(s_output_data),.o_output_index(s_output_index),.o_export_done(s_export_done)
    );

    road_down2_tile_scheduler u_down2(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_loaded(o_table_loaded),
        .i_load_valid(i_load_valid && o_load_ready && flag_owner_down2),
        .i_load_kind(i_load_kind),.i_load_addr(i_load_addr),.i_load_data(i_load_data),.o_load_ready(d_load_ready),
        .i_start(i_start && flag_commands && !flag_unexported && !o_done && flag_owner_down2),.i_pw_only(1'b0),
        .i_commit_ready(i_commit_ready),.o_busy(d_busy),.o_done(d_done),.o_fault(d_fault),.o_core_cycles(d_core_cycles),
        .i_export_start(i_export_start && flag_commands && flag_owner_down2),.i_output_ready(i_output_ready && flag_owner_down2),
        .o_output_valid(d_output_valid),.o_output_data(d_output_data),.o_output_index(d_output_index),.o_export_done(d_export_done),
        .o_mac_valid(d_mac_valid),.i_mac_ready(d_mac_ready),.o_mac_first(d_mac_first),.o_mac_last(d_mac_last),
        .o_mac_mask(d_mac_mask),.o_mac_activation(d_mac_activation),.o_mac_weight(d_mac_weight),.o_mac_bias(d_mac_bias),
        .i_mac_result_valid(d_mac_result_valid),.o_mac_result_ready(d_mac_result_ready),.i_mac_result(d_mac_result),.i_mac_fault(d_mac_fault),
        .o_pp_valid(d_pp_valid),.i_pp_ready(d_pp_ready),.o_pp_acc(d_pp_acc),.o_pp_multipliers(d_pp_multipliers),
        .o_pp_shifts(d_pp_shifts),.o_pp_post_multiplier(d_pp_post_multiplier),.o_pp_post_shift(d_pp_post_shift),
        .o_pp_mask(d_pp_mask),.o_pp_tags(d_pp_tags),.o_pp_input_fault(d_pp_input_fault),
        .i_pp_valid(d_pp_output_valid),.o_pp_ready(d_pp_output_ready),.i_pp_data(pp_data),.i_pp_tag(pp_tag),
        .i_pp_int16(pp_int16),.i_pp_fault(pp_fault),.i_pp_result_queue_count(pp_queue_count),
        .i_pp_meta_count(pp_pending_count),.i_pp_pre_busy(pp_pre_busy),.i_pp_silu_busy(pp_silu_busy),
        .i_pp_post_busy(pp_post_busy),.i_pp_pre_accept(pp_pre_accept),.i_pp_silu_accept(pp_silu_accept),.i_pp_post_accept(pp_post_accept),
        .o_debug_valid(),.o_debug_phase(),.o_debug_layer(),.o_debug_position(),.o_debug_channel(),.o_debug_value(),
        .o_preload_writes(),.o_mac_cycles(),.o_pre_cycles(),.o_silu_cycles(),.o_post_cycles(),.o_writeback_cycles(),
        .o_storage_wait_cycles(),.o_scheduler_idle_cycles(),.o_export_cycles(),.o_result_queue_count(),
        .o_result_reserved(),.o_meta_count(),.o_mac_result_count(),.o_pre_accept_count(),.o_silu_accept_count(),
        .o_post_accept_count(),.o_writeback_count()
    );

    road_mac_probe u_mac(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_input_valid(flag_owner_down2 ? d_mac_valid : s_mac_valid),
        .o_input_ready(mac_ready),.i_first(flag_owner_down2 ? d_mac_first : s_mac_first),
        .i_last(flag_owner_down2 ? d_mac_last : s_mac_last),.i_lane_mask(flag_owner_down2 ? d_mac_mask : s_mac_mask),
        .i_activation_data(flag_owner_down2 ? d_mac_activation : s_mac_activation),
        .i_weight_data(flag_owner_down2 ? d_mac_weight : s_mac_weight),.i_bias_data(flag_owner_down2 ? d_mac_bias : s_mac_bias),
        .i_result_ready(flag_owner_down2 ? d_mac_result_ready : s_mac_result_ready),
        .o_result_valid(mac_result_valid),.o_result_data(mac_result),.o_fault(mac_fault)
    );

    road_dynamic_postprocess u_pp(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_valid(i_table_valid && flag_table_enable),
        .i_table_addr(i_table_addr),.i_table_data(i_table_data),.o_table_ready(pp_table_ready),.o_table_loaded(o_table_loaded),
        .i_input_valid(flag_owner_down2 ? d_pp_valid : s_pp_valid),.o_input_ready(pp_ready),
        .i_accumulators(flag_owner_down2 ? d_pp_acc : s_pp_acc),
        .i_pre_multipliers(flag_owner_down2 ? d_pp_multipliers : s_pp_multipliers),
        .i_pre_shifts(flag_owner_down2 ? d_pp_shifts : s_pp_shifts),
        .i_post_multiplier(flag_owner_down2 ? d_pp_post_multiplier : s_pp_post_multiplier),
        .i_post_shift(flag_owner_down2 ? d_pp_post_shift : s_pp_post_shift),.i_activate(1'b1),
        .i_lane_mask(flag_owner_down2 ? d_pp_mask : s_pp_mask),.i_tags(flag_owner_down2 ? d_pp_tags : s_pp_tags),
        .i_input_fault(flag_owner_down2 && d_pp_input_fault),
        .i_output_ready(flag_owner_down2 ? d_pp_output_ready : s_pp_output_ready),
        .o_output_valid(pp_valid),.o_output_data(pp_data),.o_output_tag(pp_tag),.o_output_int16(pp_int16),.o_fault(pp_fault),
        .o_queue_count(pp_queue_count),.o_pending_count(pp_pending_count),.o_meta_count(pp_meta_count),
        .o_pre_busy(pp_pre_busy),.o_silu_busy(pp_silu_busy),.o_post_busy(pp_post_busy),
        .o_pre_accept(pp_pre_accept),.o_silu_accept(pp_silu_accept),.o_post_accept(pp_post_accept)
    );
endmodule
