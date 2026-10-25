`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Fixed first CSP DW output cache
// Module Name: road_csp_dw_cache
// Description: road_csp_dw_cache_spec.md
// Simulations: tb_csp_dw_cache, tb_csp_first_probe
// Referrences: road_csp_dw_cache_spec.md
// Dependencies: None
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create fixed tile cache
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 首残差DW结果缓存
// 模块名称: road_csp_dw_cache
// 模块说明: road_csp_dw_cache_spec.md
// 仿真工程: tb_csp_dw_cache, tb_csp_first_probe
// 参考资料: road_csp_dw_cache_spec.md
// 依赖文件: 无
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建固定tile缓存
module road_csp_dw_cache(
    input i_clk, // 同域100MHz时钟
    input i_rstn, // 异步取消，共同复位释放由顶层保证
    input i_clear, // 空闲启动新tile时同步清有效位，不重置算术核或SiLU
    input i_write_valid, // 真实DW写请求，保持到ready
    input [7:0]i_write_index, // 局部HWC索引零至一百九十一
    input [7:0]i_write_data, // 实际DW后重定标INT8结果
    input i_read_valid, // PW八输入组读请求
    input [3:0]i_read_pixel, // 四乘四tile的像素索引
    input i_read_group, // 首八通道或末四通道
    input i_output_ready, // PW操作数端实际接收
    output o_write_ready, // 采集阶段且无故障时接收
    output o_loaded, // 一百九十二个不同位置全已接收
    output [7:0]o_write_count, // 只统计有效唯一写
    output o_fault, // 重复或越界写粘滞错误
    output o_read_ready, // 全部装满且响应槽可用
    output o_output_valid, // 一个注册响应槽
    output [63:0]o_output_data, // 低字节为输入lane零
    output [7:0]o_output_mask, // 首组全有效，末组低四路有效
    output [3:0]o_output_pixel, // 与读结果保持同一元数据
    output o_output_group // 与读结果保持同一组号
);
    //-----------------有效性及响应状态-----------------//
    reg [191:0]reg_written; // 未清RAM时仍必须逐地址重新写入
    reg [7:0]reg_write_count; // 唯一有效字节数，不按裸valid计数
    reg flag_fault_o; // 必须复位才能解除的写入错误
    reg flag_output_o; // 一槽响应占有
    reg [3:0]reg_output_pixel_o; // 响应像素索引
    reg flag_output_group_o; // 响应输入组号
    wire flag_index_valid; // 写地址在真实张量范围
    wire flag_duplicate; // 同tile重复写不能充当完整采集
    wire flag_write_accept; // DW输出实际接受
    wire flag_write_store; // 健康合法唯一写才触发RAM
    wire flag_read_accept; // PW请求真实接受
    wire [7:0]wire_write_pixel; // 除以十二的完整商，非法地址仍不写
    wire [7:0]wire_write_channel; // 十二通道余数
    wire [2:0]wire_write_bank; // 通道低三位选择八bank
    wire [4:0]wire_write_row; // 像素两组行地址
    wire [4:0]wire_read_row; // 同拍读取八bank共用行地址
    //-----------------同域握手及有界地址-----------------//
    assign flag_index_valid = i_write_index < 8'd192; // 不允许物理填充槽成为逻辑值
    assign flag_duplicate = flag_index_valid ? reg_written[i_write_index] : 1'b0; // 越界不索引有效位
    assign o_loaded = i_rstn && !i_clear && !flag_fault_o && reg_write_count == 8'd192; // 完整屏障在最后写沿之后开放
    assign o_write_ready = i_rstn && !i_clear && !flag_fault_o && reg_write_count < 8'd192; // 采集和读取阶段互斥
    assign flag_write_accept = i_write_valid && o_write_ready; // 不在结果反压时偷写
    assign flag_write_store = flag_write_accept && flag_index_valid && !flag_duplicate; // 非法写零副作用
    assign wire_write_pixel = i_write_index / 8'd12; // 固定常数地址换算，不改变张量布局
    assign wire_write_channel = i_write_index % 8'd12; // 固定十二通道
    assign wire_write_bank = wire_write_channel[2:0]; // 每组八个通道分bank
    assign wire_write_row = {wire_write_pixel[3:0],wire_write_channel[3]}; // 每像素两行
    assign wire_read_row = {i_read_pixel,i_read_group}; // 第一行八字节，第二行仅低四bank有效
    assign o_read_ready = o_loaded && (!flag_output_o || i_output_ready); // 一槽允许同沿出入
    assign flag_read_accept = i_read_valid && o_read_ready; // 仅握手才读RAM及锁存元数据
    assign o_output_valid = flag_output_o && o_loaded; // 复位或故障不发布旧响应
    assign o_output_mask = flag_output_group_o ? 8'h0f : 8'hff; // 无效尾lane必须为零
    assign o_output_pixel = reg_output_pixel_o; // 反压保持
    assign o_output_group = flag_output_group_o; // 反压保持
    assign o_write_count = reg_write_count; // 观察实际已写字节数
    assign o_fault = i_rstn && flag_fault_o; // 复位期间撤销错误发布

    // ponytail: 此探针只保留单tile；整图复用时需在层提交后本地清有效状态，不重装全核SiLU。
    // 有效位保护上电/复位后的未定义RAM，不复位RAM数据阵列。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_written <= 192'd0;
            reg_write_count <= 8'd0;
        end else if (i_clear) begin
            reg_written <= 192'd0; // 上一tile的物理RAM保留但不可读取
            reg_write_count <= 8'd0; // 新tile必须重新写满192个不同位置
        end else if (flag_write_store) begin
            reg_written[i_write_index] <= 1'b1;
            reg_write_count <= reg_write_count + 8'd1;
        end
    end

    // 越界和重复写一旦接受，禁止本tile后续读写及发布。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) flag_fault_o <= 1'b0;
        else if (flag_write_accept && (!flag_index_valid || flag_duplicate)) flag_fault_o <= 1'b1;
    end

    // 注册响应占有与数据同步；反压期间不改元数据。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_output_o <= 1'b0;
            reg_output_pixel_o <= 4'd0;
            flag_output_group_o <= 1'b0;
        end else if (i_clear) begin
            flag_output_o <= 1'b0; // 局部清理不允许旧响应跨tile发布
            reg_output_pixel_o <= 4'd0; // 撤销旧像素元数据
            flag_output_group_o <= 1'b0; // 撤销旧组号
        end else if (flag_read_accept) begin
            flag_output_o <= 1'b1;
            reg_output_pixel_o <= i_read_pixel;
            flag_output_group_o <= i_read_group;
        end else if (o_output_valid && i_output_ready) begin
            flag_output_o <= 1'b0;
        end
    end

    //-----------------八个同步读写bank-----------------//
    genvar bank;
    generate
        for (bank = 0; bank < 8; bank = bank + 1) begin: g_bank
            localparam [2:0]BANK_INDEX = bank; // 固定展开的物理bank号
            reg [7:0]mem_values [0:31]; // 每bank三十二字节，部分第二行槽不使用
            reg [7:0]reg_read_data_o; // 各bank的注册读数据
            assign o_output_data[bank*8 +: 8] = reg_read_data_o; // 拼接只做布线
            // 所有写发生在采集阶段，所有读发生在完成之后，无同址读写碰撞。
            always @(posedge i_clk) begin
                if (flag_write_store && wire_write_bank == BANK_INDEX) mem_values[wire_write_row] <= i_write_data;
            end
            // 未使用的第二组高四bank输出零，不读取未写的物理槽。
            always @(posedge i_clk or negedge i_rstn) begin
                if (!i_rstn) reg_read_data_o <= 8'd0;
                else if (flag_read_accept) begin
                    if (bank >= 4 && i_read_group) reg_read_data_o <= 8'd0;
                    else reg_read_data_o <= mem_values[wire_read_row];
                end
            end
        end
    endgenerate
endmodule
