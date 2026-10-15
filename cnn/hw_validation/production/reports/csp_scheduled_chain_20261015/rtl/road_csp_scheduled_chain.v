`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Scheduled first CSP arithmetic chain
// Module Name: road_csp_scheduled_chain
// Description: road_csp_scheduled_chain_spec.md
// Simulations: tb_csp_scheduled_chain
// Referrences: road_csp_scheduled_chain_spec.md
// Dependencies: road_csp_tile_schedule, road_csp_dw_cache, road_csp_first_probe
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Connect fixed task and operand control
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 首残差固定任务计算链
// 模块名称: road_csp_scheduled_chain
// 模块说明: road_csp_scheduled_chain_spec.md
// 仿真工程: tb_csp_scheduled_chain
// 参考资料: road_csp_scheduled_chain_spec.md
// 依赖文件: road_csp_tile_schedule, road_csp_dw_cache, road_csp_first_probe
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 接通有界任务及取数
module road_csp_scheduled_chain(
    input i_clk, // 同域100MHz时钟
    input i_rstn, // 共同异步取消，provider必须共同清旧响应
    input i_start, // 固定tile启动请求
    input i_table_valid, // 空闲顺序装表请求，优先于启动
    input [9:0]i_table_addr, // 原SiLU表地址
    input [15:0]i_table_data, // 原signed16表值
    input i_operand_request_ready, // 内部取数端真实接受
    input i_operand_response_valid, // 响应及全部载荷保持到ready
    input [24:0]i_operand_response_descriptor, // 当前唯一请求的完整回显
    input [63:0]i_operand_activation, // 仅DW采用，PW忽略
    input [191:0]i_operand_weight, // 三输出路各八输入权重
    input [95:0]i_operand_bias, // 三路INT32偏置
    input [95:0]i_operand_pre_multipliers, // 三路前乘数
    input [17:0]i_operand_pre_shifts, // 三路移位
    input [31:0]i_operand_post_multiplier, // 当前层后乘数
    input [5:0]i_operand_post_shift, // 当前层后移位
    input [23:0]i_operand_bypass, // PW三路原输入旁路
    input i_operand_fault, // 保留首组输入故障语义
    input i_result_ready, // 真实结果接收端
    output o_start_ready, // 完全空闲且表已满
    output o_table_ready, // 实际允许原核接受表项
    output o_table_loaded, // 原核完整装表许可
    output o_busy, // 当前tile尚未提交完成
    output o_done, // 全部末路提交后的单周期完成
    output o_fault, // 共同复位前禁止恢复
    output o_operand_request_valid, // 固定组取数请求
    output [24:0]o_operand_request_descriptor, // 与冻结布局一致的组描述符
    output o_operand_response_ready, // 当前请求仅接受一次响应
    output o_result_valid, // 结果和DW缓存原子接受
    output [7:0]o_result_data, // 实际INT8结果
    output [15:0]o_result_tag, // RTL派生的结果标识
    output [31:0]o_result_address, // 冻结逻辑字节地址
    output [8:0]o_result_sum, // 原signed9残差和
    output o_group_accept, // MAC真实接收一组
    output o_task_commit, // 该任务最后一路实际提交
    output o_request_accept, // 取数请求真实接受
    output o_cache_read_accept, // PW缓存请求实际接受
    output o_cache_write_accept, // DW缓存字节实际接受
    output [2:0]o_cycle_reason // 互斥占用类别，不把重叠活动相加
);
    //-----------------单事务保存-----------------//
    reg flag_start_pending; // 一个周期的局部cache clear及启动保留
    reg flag_pending; // 唯一已接受且尚未送MAC的请求
    reg flag_payload; // 权重及参数已接收
    reg flag_activation; // PW缓存激活已接收
    reg [24:0]reg_descriptor; // 整组元数据不可与下一请求错配
    reg [63:0]reg_activation; // DW来自provider，PW只来自缓存
    reg [191:0]reg_weight; // 当前组三路权重
    reg [95:0]reg_bias; // 当前组三路偏置
    reg [95:0]reg_pre_multipliers; // 当前组三路前乘数
    reg [17:0]reg_pre_shifts; // 当前组三路移位
    reg [31:0]reg_post_multiplier; // 当前组后乘数
    reg [5:0]reg_post_shift; // 当前组后移位
    reg [23:0]reg_bypass; // 当前组旁路
    reg flag_operand_fault; // 当前组输入故障
    reg [1:0]reg_remaining; // 当前任务尚未接受的输出路数
    reg flag_task_done; // 只在末路实际提交沿产生脉冲
    reg flag_adapter_fault; // 失配响应或无所有权结果粘滞故障
    reg [2:0]reg_cycle_reason; // 组合完整赋值的观察类别
    //-----------------冻结调度接口-----------------//
    wire schedule_start_ready; // 冻结调度空闲准入
    wire schedule_valid; // 当前组描述符有效
    wire schedule_first; // 当前任务首组
    wire schedule_last; // 当前任务末组
    wire schedule_pw; // 当前任务为PW
    wire [1:0]schedule_y; // tile行
    wire [1:0]schedule_x; // tile列或DW三点起点
    wire [3:0]schedule_channel; // 逻辑通道
    wire [2:0]schedule_mask; // 有效输出路
    wire [7:0]schedule_input_mask; // 冻结输入mask，仅供观察校验
    wire [7:0]schedule_index; // 固定任务索引
    wire schedule_busy; // 冻结任务控制占有
    wire schedule_done; // 冻结完整tile完成
    wire schedule_fault; // 冻结控制故障
    //-----------------缓存及算术接口-----------------//
    wire cache_write_ready; // 真实DW缓存写端
    wire cache_loaded; // 全部DW值完整
    wire [7:0]cache_write_count; // 当前tile已写字节数
    wire cache_fault; // 缓存写入故障
    wire cache_read_ready; // 缓存读请求准入
    wire cache_output_valid; // 真实PW缓存响应
    wire [63:0]cache_output_data; // 实际DW派生的PW激活
    wire [7:0]cache_output_mask; // 实际缓存响应mask
    wire [3:0]cache_output_pixel; // 实际缓存响应位置
    wire cache_output_group; // 实际缓存响应组号
    wire cache_output_ready; // 本事务的激活槽可接收
    wire core_table_ready; // 原核表准入
    wire core_input_ready; // 原核接受组准入
    wire core_output_valid; // 原核真实结果有效
    wire [7:0]core_output_data; // 原核真实INT8
    wire [15:0]core_output_tag; // 原核真实标识
    wire [31:0]core_output_address; // 原核真实逻辑地址
    wire [8:0]core_output_sum; // 原核真实残差和
    wire core_output_ready; // 下游及缓存共同准入
    wire core_fault; // 原核原子故障
    wire flag_local_fault; // 不含调度自身，避免故障反馈组合环
    wire flag_global_fault; // 总取消条件
    wire flag_start_accept; // 外部tile启动接受
    wire flag_request_accept; // 描述符真实移交
    wire flag_response_accept; // 单事务参数真实接收
    wire flag_response_match; // 全部描述符位一致
    wire flag_cache_accept; // 激活槽真实接收缓存响应
    wire flag_mac_valid; // 全部数据齐备后送原MAC
    wire flag_mac_accept; // 原MAC真实接受
    wire flag_result_accept; // 原结果真实提交
    wire flag_result_owned; // 未接首组前不可发布结果
    wire flag_result_dw; // 当前结果写DW缓存
    wire flag_table_enable; // 装表与启动/运行互斥
    wire cache_write_valid; // 共同提交许可下的DW分支有效
    wire cache_read_valid; // PW请求与取数请求原子接受
    wire [7:0]wire_input_mask; // 当前锁存描述符的输入mask
    wire [15:0]wire_primary_index; // 当前任务第一路的局部HWC位置
    wire [47:0]wire_tags; // RTL按坐标生成的三路标识
    wire [95:0]wire_addresses; // RTL生成的三路逻辑地址

    //-----------------准入与原子接受-----------------//
    assign flag_local_fault = core_fault || cache_fault || flag_adapter_fault; // 不回接schedule_fault
    assign flag_global_fault = flag_local_fault || schedule_fault; // 故障即时关闭全部新接受
    assign o_fault = i_rstn && flag_global_fault; // 共同复位取消状态发布
    assign o_busy = flag_start_pending || schedule_busy || flag_pending || reg_remaining != 2'd0; // 有界单上下文占有
    assign flag_table_enable = !o_busy && !flag_global_fault; // 不在活动任务期间重启表
    assign o_table_ready = i_rstn && flag_table_enable && core_table_ready; // 原核真实表握手
    assign o_start_ready = i_rstn && !o_busy && schedule_start_ready && !i_table_valid && !flag_global_fault; // 空闲装表优先
    assign flag_start_accept = i_start && o_start_ready; // 先保留启动，再清本地缓存
    assign o_done = schedule_done && !flag_global_fault && i_rstn; // 故障不发布成功
    assign o_operand_request_descriptor = {schedule_index,schedule_pw,schedule_y,schedule_x,schedule_channel,schedule_first,schedule_last,schedule_mask,3'b000}; // 冻结25位布局
    assign o_operand_request_valid = i_rstn && schedule_valid && !flag_pending && (!schedule_pw || cache_read_ready) && !flag_global_fault; // 一个请求在途
    assign flag_request_accept = o_operand_request_valid && i_operand_request_ready; // 不随裸valid推进
    assign o_operand_response_ready = i_rstn && flag_pending && !flag_payload && !flag_global_fault; // 响应只登记一次
    assign flag_response_accept = i_operand_response_valid && o_operand_response_ready; // 参数真实接受
    assign flag_response_match = i_operand_response_descriptor == reg_descriptor; // 失配不能进入计算
    assign cache_read_valid = flag_request_accept && schedule_pw; // 与外部请求同拍，cache_ready已预留
    assign cache_output_ready = flag_pending && reg_descriptor[16] && !flag_activation && !flag_global_fault; // 只接本组缓存响应
    assign flag_cache_accept = cache_output_valid && cache_output_ready; // 激活真实入槽
    assign flag_mac_valid = flag_pending && flag_payload && (!reg_descriptor[16] || flag_activation) && schedule_valid && !flag_global_fault; // 单组汇合
    assign flag_mac_accept = flag_mac_valid && core_input_ready; // 只有此事件推进原调度组号
    assign flag_result_owned = reg_remaining != 2'd0; // 首组记录当前输出数
    assign flag_result_dw = core_output_tag < 16'd192; // 已冻结两段标识空间
    assign core_output_ready = i_rstn && i_result_ready && flag_result_owned && (!flag_result_dw || cache_write_ready) && !flag_global_fault; // 真实DW反压返回原核
    assign o_result_valid = i_rstn && core_output_valid && flag_result_owned && (!flag_result_dw || cache_write_ready) && !flag_global_fault; // 与缓存原子发布
    assign flag_result_accept = core_output_valid && core_output_ready; // 所有权只随实际写端接受释放
    assign cache_write_valid = core_output_valid && i_result_ready && flag_result_dw && flag_result_owned && !flag_global_fault; // 同域原子分支，不是独立外设接口
    assign o_result_data = core_output_data; // 数据随原核背压保持
    assign o_result_tag = core_output_tag; // 标识随原核背压保持
    assign o_result_address = core_output_address; // 地址随原核背压保持
    assign o_result_sum = core_output_sum; // 中间和与结果同步
    assign o_group_accept = flag_mac_accept; // 可观察真实MAC吞吐
    assign o_request_accept = flag_request_accept; // 可观察真实取数握手
    assign o_task_commit = flag_task_done; // 末路提交的注册脉冲
    assign o_cache_read_accept = cache_read_valid && cache_read_ready; // 实际PW读请求数
    assign o_cache_write_accept = cache_write_valid && cache_write_ready; // 实际DW存储字节数
    assign wire_input_mask = !reg_descriptor[6] ? 8'hff : reg_descriptor[16] ? 8'h0f : reg_descriptor[13:12] == 2'd3 ? 8'h01 : 8'h7f; // 与冻结组排布一致
    assign wire_primary_index = {12'd0,reg_descriptor[15:12]} * 16'd12 + {12'd0,reg_descriptor[11:8]}; // pixel×12+channel

    //-----------------标签与地址只做固定图派生-----------------//
    genvar lane;
    generate
        for (lane = 0; lane < 3; lane = lane + 1) begin: g_metadata
            localparam [15:0]PW_OFFSET = 16'd192 + lane; // PW三路不同输出通道
            localparam [15:0]DW_OFFSET = 16'd12 * lane; // DW三路相邻空间点
            wire [15:0]wire_lane_tag; // 无效路标识不参与原核检查或写回
            wire [31:0]wire_lane_address; // 明确扩展到32位再计算地址
            assign wire_lane_tag = reg_descriptor[3+lane] ? wire_primary_index + (reg_descriptor[16] ? PW_OFFSET : DW_OFFSET) : 16'd0;
            assign wire_lane_address = !reg_descriptor[3+lane] ? 32'd0 : reg_descriptor[16] ? 32'd56643584 + {16'd0,wire_lane_tag} - 32'd192 : 32'd56532992 + {16'd0,wire_lane_tag};
            assign wire_tags[lane*16 +: 16] = wire_lane_tag;
            assign wire_addresses[lane*32 +: 32] = wire_lane_address;
        end
    endgenerate

    //-----------------冻结模块实例-----------------//
    road_csp_tile_schedule u_schedule(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_start(flag_start_pending),.i_table_loaded(o_table_loaded),
        .i_group_ready(flag_mac_accept),.i_task_done(flag_task_done),.i_core_fault(flag_local_fault),
        .o_start_ready(schedule_start_ready),.o_group_valid(schedule_valid),.o_first(schedule_first),.o_last(schedule_last),
        .o_pw(schedule_pw),.o_y(schedule_y),.o_x(schedule_x),.o_channel(schedule_channel),.o_output_mask(schedule_mask),
        .o_input_mask(schedule_input_mask),.o_task_index(schedule_index),.o_busy(schedule_busy),.o_done(schedule_done),.o_fault(schedule_fault)
    );
    road_csp_dw_cache u_cache(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_start_pending),
        .i_write_valid(cache_write_valid),.i_write_index(core_output_tag[7:0]),.i_write_data(core_output_data),
        .o_write_ready(cache_write_ready),.o_loaded(cache_loaded),.o_write_count(cache_write_count),.o_fault(cache_fault),
        .i_read_valid(cache_read_valid),.i_read_pixel({schedule_y,schedule_x}),.i_read_group(schedule_last),.o_read_ready(cache_read_ready),
        .i_output_ready(cache_output_ready),.o_output_valid(cache_output_valid),.o_output_data(cache_output_data),
        .o_output_mask(cache_output_mask),.o_output_pixel(cache_output_pixel),.o_output_group(cache_output_group)
    );
    road_csp_first_probe u_compute(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_valid(i_table_valid && flag_table_enable),.i_table_addr(i_table_addr),.i_table_data(i_table_data),
        .o_table_ready(core_table_ready),.o_table_loaded(o_table_loaded),
        .i_input_valid(flag_mac_valid),.i_first(reg_descriptor[7]),.i_last(reg_descriptor[6]),.i_lane_mask(wire_input_mask),
        .i_activation_data(reg_activation),.i_weight_data(reg_weight),.i_bias_data(reg_bias),.i_output_mask(reg_descriptor[5:3]),
        .i_tags(wire_tags),.i_addresses(wire_addresses),.i_pre_multipliers(reg_pre_multipliers),.i_pre_shifts(reg_pre_shifts),
        .i_post_multiplier(reg_post_multiplier),.i_post_shift(reg_post_shift),.i_residual(reg_descriptor[16]),
        .i_bypass_data(reg_bypass),.i_input_fault(flag_operand_fault),.o_input_ready(core_input_ready),
        .i_output_ready(core_output_ready),.o_output_valid(core_output_valid),.o_output_data(core_output_data),
        .o_output_tag(core_output_tag),.o_output_address(core_output_address),.o_output_sum(core_output_sum),.o_fault(core_fault)
    );

    // 启动接受后一个周期清缓存；已经预留的启动不会被后到的装表请求打断。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_start_pending <= 1'b0;
        else flag_start_pending <= flag_start_accept;
    end

    // ponytail: 只保留一组请求和两个完成标志，不增加通用FIFO或跨任务MAC上下文。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_pending <= 1'b0;
            flag_payload <= 1'b0;
            flag_activation <= 1'b0;
            reg_descriptor <= 25'd0;
            reg_activation <= 64'd0;
            reg_weight <= 192'd0;
            reg_bias <= 96'd0;
            reg_pre_multipliers <= 96'd0;
            reg_pre_shifts <= 18'd0;
            reg_post_multiplier <= 32'd0;
            reg_post_shift <= 6'd0;
            reg_bypass <= 24'd0;
            flag_operand_fault <= 1'b0;
        end else begin
            if (flag_request_accept) begin
                flag_pending <= 1'b1;
                flag_payload <= 1'b0;
                flag_activation <= 1'b0;
                reg_descriptor <= o_operand_request_descriptor;
            end
            if (flag_response_accept && flag_response_match) begin
                flag_payload <= 1'b1;
                if (!reg_descriptor[16]) reg_activation <= i_operand_activation;
                reg_weight <= i_operand_weight;
                reg_bias <= i_operand_bias;
                reg_pre_multipliers <= i_operand_pre_multipliers;
                reg_pre_shifts <= i_operand_pre_shifts;
                reg_post_multiplier <= i_operand_post_multiplier;
                reg_post_shift <= i_operand_post_shift;
                reg_bypass <= i_operand_bypass;
                flag_operand_fault <= i_operand_fault;
            end
            if (flag_cache_accept) begin
                flag_activation <= 1'b1;
                reg_activation <= cache_output_data;
            end
            if (flag_mac_accept) begin
                flag_pending <= 1'b0;
                flag_payload <= 1'b0;
                flag_activation <= 1'b0;
            end
        end
    end

    // 原核三路可能连续返回，但只有最后一路实际提交才能驱动任务完成。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_remaining <= 2'd0;
            flag_task_done <= 1'b0;
        end else begin
            flag_task_done <= 1'b0;
            if (flag_mac_accept && reg_descriptor[7]) begin
                reg_remaining <= {1'b0,reg_descriptor[3]} + {1'b0,reg_descriptor[4]} + {1'b0,reg_descriptor[5]};
            end else if (flag_result_accept) begin
                reg_remaining <= reg_remaining - 2'd1;
                if (reg_remaining == 2'd1) flag_task_done <= 1'b1;
            end
        end
    end

    // 失配响应与无所有权输出不允许默默混入下一事务。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_adapter_fault <= 1'b0;
        else if ((flag_response_accept && !flag_response_match) || (core_output_valid && !flag_result_owned)) flag_adapter_fault <= 1'b1;
    end

    // 分类互斥；pre/SiLU/post原活动可重叠，不在这里相加当总周期。
    always @(*) begin
        reg_cycle_reason = 3'd0;
        if (o_busy) begin
            if (flag_mac_accept) reg_cycle_reason = 3'd1;
            else if (o_operand_request_valid) reg_cycle_reason = 3'd2;
            else if (flag_pending && !flag_payload) reg_cycle_reason = 3'd3;
            else if (flag_pending && reg_descriptor[16] && !flag_activation) reg_cycle_reason = 3'd4;
            else if (flag_pending) reg_cycle_reason = 3'd5;
            else if (core_output_valid && !core_output_ready) reg_cycle_reason = 3'd6;
            else reg_cycle_reason = 3'd7;
        end
    end
    assign o_cycle_reason = reg_cycle_reason; // 只作观测，不反馈控制
endmodule
