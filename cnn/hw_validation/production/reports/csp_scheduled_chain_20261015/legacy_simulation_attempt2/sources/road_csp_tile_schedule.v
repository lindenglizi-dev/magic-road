`timescale 1ns / 1ps
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Fixed first residual tile schedule
// Module Name: road_csp_tile_schedule
// Description: Two-group descriptors, advance only after complete local commit
// Simulations: tb_csp_tile_schedule
// Referrences: road_csp_tile_schedule_spec.md
// Dependencies: None
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 Codex Create file
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 首残差固定tile任务顺序
// 模块名称: road_csp_tile_schedule
// 模块说明: 末路本地写入接受后推进，不代表DDR可见
// 仿真工程: tb_csp_tile_schedule
// 参考资料: road_csp_tile_schedule_spec.md
// 依赖文件: 无
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 Codex 创建文件
module road_csp_tile_schedule(
    input i_clk, // 同域100MHz时钟
    input i_rstn, // 共同异步低有效取消，释放由现顶层保证
    input i_start, // 仅start_ready时接受
    input i_table_loaded, // 来自核的完整装表许可
    input i_group_ready, // 适配器及计算核共同接收本组
    input i_task_done, // 末路有效结果已被本地存储接收
    input i_core_fault, // 外部计算故障，必须共同复位
    output o_start_ready, // 空闲且完整装表才能启动
    output o_group_valid, // 组描述符整体保持到握手
    output o_first, // 本任务首组
    output o_last, // 本任务末组
    output o_pw, // 当前阶段为PW
    output [1:0]o_y, // 输出tile行坐标
    output [1:0]o_x, // DW三点起点或PW单点横坐标
    output [3:0]o_channel, // DW通道或PW三通道起点
    output [2:0]o_output_mask, // 有效输出路，DW尾点仅一路
    output [7:0]o_input_mask, // 八输入槽有效掩码
    output [7:0]o_task_index, // 固定任务索引零至一百五十九
    output o_busy, // 本tile任务尚未完整结束
    output o_done, // 全部本地提交后的单拍完成
    output o_fault // 粘滞故障，复位前不发布
);
    //-----------------状态与计数-----------------//
    localparam [1:0]ST_IDLE = 2'd0; // 等待完整装表及启动
    localparam [1:0]ST_SEND = 2'd1; // 两组逐次接受
    localparam [1:0]ST_WAIT = 2'd2; // 等待最后一个结果提交
    reg [1:0]state_current; // 当前协议状态
    reg [1:0]state_next; // 完整默认的下一状态
    reg flag_pw; // DW完成之后切换PW
    reg flag_group; // 零表示首组，一表示末组
    reg [1:0]reg_y; // 四行输出计数
    reg [1:0]reg_x; // DW零或三，PW零至三
    reg [3:0]reg_channel; // DW逐通道，PW每三通道
    reg [7:0]reg_task_index; // 单调递增有界任务索引
    reg flag_done_o; // 完成事件寄存
    reg flag_fault_o; // 协议故障寄存
    reg flag_done_seen; // 当前完成高电平已经消费，回低之前不得再消费
    //-----------------事件与掩码-----------------//
    wire flag_start; // 启动真实握手
    wire flag_group_accept; // 本组真实握手
    wire flag_task_accept; // 本任务所有结果已本地提交
    wire flag_early_done; // 归约尚未送完却提前完成
    wire flag_cancel; // 故障优先于任何新接受
    wire flag_final; // 当前为最后任务
    wire flag_tail; // DW一空间点尾任务
    wire [7:0]wire_last_mask; // 不同阶段的第二组掩码
    //-----------------接口与事件-----------------//
    assign flag_early_done = (state_current == ST_SEND) && i_task_done && !flag_done_seen; // 已消费的高电平尾部不是新的提前完成
    assign flag_cancel = flag_fault_o || i_core_fault || flag_early_done; // 故障即时关闭组发布
    assign o_start_ready = i_rstn && (state_current == ST_IDLE) && i_table_loaded && !flag_cancel; // 完整启动条件
    assign o_group_valid = i_rstn && (state_current == ST_SEND) && !flag_cancel; // 反压时状态及载荷保持
    assign flag_start = i_start && o_start_ready; // 不随裸start推进
    assign flag_group_accept = o_group_valid && i_group_ready; // 不随裸ready推进
    assign flag_task_accept = (state_current == ST_WAIT) && i_task_done && !flag_done_seen && !flag_cancel; // 每段完成高电平只消费一次
    assign flag_final = reg_task_index == 8'd159; // 有界终点
    assign flag_tail = !flag_pw && reg_x == 2'd3; // DW尾点禁止写另外两路
    assign wire_last_mask = flag_pw ? 8'h0f : flag_tail ? 8'h01 : 8'h7f; // PW十二槽，DW九或十五槽
    assign o_first = !flag_group; // 当前组边界随描述符保持
    assign o_last = flag_group; // 每个任务恰好两组
    assign o_pw = flag_pw; // 固定阶段标志
    assign o_y = reg_y; // 直接导出时序寄存
    assign o_x = reg_x; // 不在外部重复推导位置
    assign o_channel = reg_channel; // 逻辑通道，不是物理lane
    assign o_output_mask = flag_tail ? 3'b001 : 3'b111; // 缺失空间路屏蔽
    assign o_input_mask = flag_group ? wire_last_mask : 8'hff; // 首组八输入都属于并集
    assign o_task_index = reg_task_index; // 背压期间不变化
    assign o_busy = state_current != ST_IDLE; // 有界单tile占有
    assign o_done = flag_done_o && i_rstn && !flag_cancel; // 取消优先于成功
    assign o_fault = i_rstn && flag_cancel; // 共同复位无条件撤销故障发布
    //-----------------三段状态机-----------------//
    // 当前状态只在工作沿更新，共同复位即时回空闲。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            state_current <= ST_IDLE;
        end else begin
            state_current <= state_next;
        end
    end

    // 完整默认赋值避免组合锁存，取消具有最高优先级。
    always @(*) begin
        state_next = state_current;
        case (state_current)
            ST_IDLE: begin
                if (flag_start) state_next = ST_SEND;
            end
            ST_SEND: begin
                if (flag_group_accept && flag_group) state_next = ST_WAIT;
            end
            ST_WAIT: begin
                if (flag_task_accept) begin
                    if (flag_final) state_next = ST_IDLE;
                    else state_next = ST_SEND;
                end
            end
            default: state_next = ST_IDLE;
        endcase
        if (flag_cancel) state_next = ST_IDLE;
    end

    // ponytail: 仅固定首残差tile计数；后续整图遍历由图控制器负责，不在这里扩展微码。
    // 接受本组只改组号；本地末路提交才改空间、通道及任务号。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_pw <= 1'b0;
            flag_group <= 1'b0;
            reg_y <= 2'd0;
            reg_x <= 2'd0;
            reg_channel <= 4'd0;
            reg_task_index <= 8'd0;
        end else begin
            if (flag_start) begin
                flag_pw <= 1'b0;
                flag_group <= 1'b0;
                reg_y <= 2'd0;
                reg_x <= 2'd0;
                reg_channel <= 4'd0;
                reg_task_index <= 8'd0;
            end else if (flag_group_accept) begin
                flag_group <= 1'b1;
            end else if (flag_task_accept && !flag_final) begin
                flag_group <= 1'b0;
                reg_task_index <= reg_task_index + 8'd1;
                if (!flag_pw) begin
                    if (reg_x == 2'd0) begin
                        reg_x <= 2'd3;
                    end else begin
                        reg_x <= 2'd0;
                        if (reg_channel != 4'd11) begin
                            reg_channel <= reg_channel + 4'd1;
                        end else begin
                            reg_channel <= 4'd0;
                            if (reg_y != 2'd3) reg_y <= reg_y + 2'd1;
                            else begin
                                reg_y <= 2'd0;
                                flag_pw <= 1'b1;
                            end
                        end
                    end
                end else begin
                    if (reg_channel != 4'd9) begin
                        reg_channel <= reg_channel + 4'd3;
                    end else begin
                        reg_channel <= 4'd0;
                        if (reg_x != 2'd3) reg_x <= reg_x + 2'd1;
                        else begin
                            reg_x <= 2'd0;
                            reg_y <= reg_y + 2'd1;
                        end
                    end
                end
            end
        end
    end

    // 末任务的本地提交只产生一个时钟周期的完成事件。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_done_o <= 1'b0;
        else flag_done_o <= flag_task_accept && flag_final;
    end

    // 故障不可由重新启动清除，防止错误任务被误当成完成。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_fault_o <= 1'b0;
        else if (i_core_fault || flag_early_done) flag_fault_o <= 1'b1;
    end

    // 完成事件跨状态保持资格，必须观察回低才接收下一次完成。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_done_seen <= 1'b0;
        else if (!i_task_done) flag_done_seen <= 1'b0;
        else if (flag_task_accept) flag_done_seen <= 1'b1;
    end
endmodule
