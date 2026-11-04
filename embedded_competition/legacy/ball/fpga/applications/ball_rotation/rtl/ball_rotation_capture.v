`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_rotation_capture
// Description: Four-pixel grayscale capture with frame-tagged dual banks
// Simulations: sim/tb_ball_rotation_capture.v
// Referrences: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// Dependencies: same-clock synchronous memories
// Version: V1.0
// Revision Date: 2026-10-20
// History: V1.0 Create file
// 版权归属: 用户工程
// 开发人员: Codex
// 创建日期: 2026-10-20
// 设计名称: 带标记小球旋转
// 模块名称: ball_rotation_capture
// 模块说明: Four-pixel grayscale capture with frame-tagged dual banks
// 仿真工程: sim/tb_ball_rotation_capture.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_rotation_capture (
    input i_clk, // 像素组时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 撤销采集并释放bank
    input i_enable, // 允许本次采集
    input [96-1:0] i_rgb, // 四个连续RGB像素
    input i_valid, // 当前像素组有效
    input i_sof, // 源帧首个有效像素组
    input [12-1:0] i_x, // 左侧像素横坐标
    input [12-1:0] i_y, // 当前行号
    input [32-1:0] i_frame, // 采集源帧编号
    input [64-1:0] i_tick, // 该源帧SOF时间
    input [16-1:0] i_epoch, // 该源帧配置代次
    input i_window_valid, // 窗口来自已完成追踪结果
    input [12-1:0] i_window_x, // 四像素对齐的采集左边界
    input [12-1:0] i_window_y, // 两行对齐的采集上边界
    input [2-1:0] i_release, // 每一位释放对应bank
    input i_read, // 处理支路请求同步读
    input i_read_bank, // 处理bank选择
    input [13-1:0] i_read_address, // 两个灰度单元组成一字的地址
    output [16-1:0] o_read_data, // 请求后一个时钟返回两个灰度
    output [2-1:0] o_busy, // bank从采集到释放一直占用
    output [2-1:0] o_ready, // 完整采集的bank
    output [64-1:0] o_frames, // 两个bank的源帧编号
    output [128-1:0] o_ticks, // 两个bank的采集时刻
    output [32-1:0] o_epochs, // 两个bank的代次
    output [24-1:0] o_origins_x, // 两个bank的窗口左边界
    output [24-1:0] o_origins_y, // 两个bank的窗口上边界
    output o_overrun // SOF请求的bank仍被占用
);

    reg [1:0] reg_busy_o,reg_ready_o;
    reg [63:0] reg_frames_o;
    reg [127:0] reg_ticks_o;
    reg [31:0] reg_epochs_o;
    reg [23:0] reg_origins_x_o,reg_origins_y_o;
    reg flag_capture,flag_bank,flag_overrun_o;
    reg [11:0] reg_origin_x,reg_origin_y;
    wire flag_allocate=i_enable && i_window_valid && !reg_busy_o[i_frame[0]];
    wire flag_active=i_sof ? flag_allocate : flag_capture;
    wire flag_current_bank=i_sof ? i_frame[0] : flag_bank;
    wire [11:0] wire_origin_x=i_sof ? i_window_x : reg_origin_x;
    wire [11:0] wire_origin_y=i_sof ? i_window_y : reg_origin_y;
    wire [12:0] wire_end_x={1'b0,wire_origin_x}+13'd256;
    wire [12:0] wire_end_y={1'b0,wire_origin_y}+13'd256;
    wire flag_inside=i_valid && flag_active && i_x >= wire_origin_x &&
        {1'b0,i_x} < wire_end_x && i_y >= wire_origin_y && {1'b0,i_y} < wire_end_y;
    reg [9:0] reg_weighted_left,reg_weighted_middle_left,reg_weighted_middle_right,reg_weighted_right;
    reg flag_weighted_valid,flag_weighted_bank,flag_weighted_odd;
    reg [5:0] reg_weighted_column;
    reg [6:0] reg_weighted_row;
    reg [17:0] reg_pairs;
    reg flag_pairs_valid,flag_pairs_bank,flag_pairs_odd;
    reg [5:0] reg_pairs_column;
    reg [6:0] reg_pairs_row;
    wire [17:0] wire_row_pairs;
    reg [17:0] reg_store_pairs;
    reg flag_store_valid,flag_store_bank;
    reg [12:0] reg_store_address;
    wire [9:0] wire_first_sum={1'b0,wire_row_pairs[17:9]}+{1'b0,reg_store_pairs[17:9]}+10'd2;
    wire [9:0] wire_second_sum={1'b0,wire_row_pairs[8:0]}+{1'b0,reg_store_pairs[8:0]}+10'd2;
    wire [15:0] wire_store_data={wire_first_sum[9:2],wire_second_sum[9:2]};
    wire [31:0] wire_bank_data;
    ball_component_store #(.C_DEPTH(64),.C_ADDR_BITS(6),.C_DATA_BITS(18)) row_Inst(
        .i_clk(i_clk),.i_read_enable(flag_pairs_valid && flag_pairs_odd),.i_read_address(reg_pairs_column),
        .i_write_enable(flag_pairs_valid && !flag_pairs_odd && !i_clear),.i_write_address(reg_pairs_column),
        .i_write_data(reg_pairs),.o_read_data(wire_row_pairs));
    genvar bank;
    generate
        for(bank=0;bank<2;bank=bank+1)begin:gen_gray_bank
            ball_component_store #(.C_DEPTH(8192),.C_ADDR_BITS(13),.C_DATA_BITS(16)) gray_Inst(
                .i_clk(i_clk),.i_read_enable(i_read && i_read_bank == bank),.i_read_address(i_read_address),
                .i_write_enable(flag_store_valid && flag_store_bank == bank && !i_clear),
                .i_write_address(reg_store_address),.i_write_data(wire_store_data),
                .o_read_data(wire_bank_data[bank*16 +:16]));
        end
    endgenerate
    // 所有权只由SOF分配和处理完成释放；绝不覆盖正在处理的bank。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_busy_o<=0;reg_ready_o<=0;reg_frames_o<=0;reg_ticks_o<=0;reg_epochs_o<=0;
            reg_origins_x_o<=0;reg_origins_y_o<=0;flag_capture<=0;flag_bank<=0;
            reg_origin_x<=0;reg_origin_y<=0;flag_overrun_o<=0;
        end else if(i_clear)begin
            reg_busy_o<=0;reg_ready_o<=0;flag_capture<=0;flag_overrun_o<=0;
        end else begin
            flag_overrun_o<=0;
            if(i_release[0])begin reg_busy_o[0]<=0;reg_ready_o[0]<=0;end
            if(i_release[1])begin reg_busy_o[1]<=0;reg_ready_o[1]<=0;end
            if(flag_store_valid && reg_store_address == 8191)begin reg_ready_o[flag_store_bank]<=1;end
            if(i_valid && i_sof)begin
                flag_capture<=flag_allocate;flag_bank<=i_frame[0];
                reg_origin_x<=i_window_x;reg_origin_y<=i_window_y;
                flag_overrun_o<=i_enable && i_window_valid && reg_busy_o[i_frame[0]];
                if(flag_allocate)begin
                    reg_busy_o[i_frame[0]]<=1;reg_ready_o[i_frame[0]]<=0;
                    reg_frames_o[i_frame[0]*32 +:32]<=i_frame;
                    reg_ticks_o[i_frame[0]*64 +:64]<=i_tick;
                    reg_epochs_o[i_frame[0]*16 +:16]<=i_epoch;
                    reg_origins_x_o[i_frame[0]*12 +:12]<=i_window_x;
                    reg_origins_y_o[i_frame[0]*12 +:12]<=i_window_y;
                end
            end
        end
    end
    // 灰度、水平相加、行缓冲、垂直相加各自保留坐标和bank标记。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_weighted_left<=0;reg_weighted_middle_left<=0;reg_weighted_middle_right<=0;reg_weighted_right<=0;
            flag_weighted_valid<=0;flag_weighted_bank<=0;flag_weighted_odd<=0;
            reg_weighted_column<=0;reg_weighted_row<=0;reg_pairs<=0;
            flag_pairs_valid<=0;flag_pairs_bank<=0;flag_pairs_odd<=0;reg_pairs_column<=0;reg_pairs_row<=0;
            reg_store_pairs<=0;flag_store_valid<=0;flag_store_bank<=0;reg_store_address<=0;
        end else if(i_clear)begin
            flag_weighted_valid<=0;flag_pairs_valid<=0;flag_store_valid<=0;
        end else begin
            flag_weighted_valid<=flag_inside;
            flag_weighted_bank<=flag_current_bank;
            flag_weighted_odd<=i_y[0];reg_weighted_column<=(i_x-wire_origin_x) >> 2;
            reg_weighted_row<=(i_y-wire_origin_y) >> 1;
            reg_weighted_left<={2'b0,i_rgb[95:88]}+{1'b0,i_rgb[87:80],1'b0}+{2'b0,i_rgb[79:72]};
            reg_weighted_middle_left<={2'b0,i_rgb[71:64]}+{1'b0,i_rgb[63:56],1'b0}+{2'b0,i_rgb[55:48]};
            reg_weighted_middle_right<={2'b0,i_rgb[47:40]}+{1'b0,i_rgb[39:32],1'b0}+{2'b0,i_rgb[31:24]};
            reg_weighted_right<={2'b0,i_rgb[23:16]}+{1'b0,i_rgb[15:8],1'b0}+{2'b0,i_rgb[7:0]};
            flag_pairs_valid<=flag_weighted_valid;flag_pairs_bank<=flag_weighted_bank;
            flag_pairs_odd<=flag_weighted_odd;reg_pairs_column<=reg_weighted_column;reg_pairs_row<=reg_weighted_row;
            reg_pairs[17:9]<={1'b0,reg_weighted_left[9:2]}+{1'b0,reg_weighted_middle_left[9:2]};
            reg_pairs[8:0]<={1'b0,reg_weighted_middle_right[9:2]}+{1'b0,reg_weighted_right[9:2]};
            flag_store_valid<=flag_pairs_valid && flag_pairs_odd;flag_store_bank<=flag_pairs_bank;
            reg_store_pairs<=reg_pairs;reg_store_address<={reg_pairs_row,reg_pairs_column};
        end
    end
    assign o_read_data=i_read_bank ? wire_bank_data[31:16] : wire_bank_data[15:0];
    assign o_busy=reg_busy_o;
    assign o_ready=reg_ready_o;
    assign o_frames=reg_frames_o;
    assign o_ticks=reg_ticks_o;
    assign o_epochs=reg_epochs_o;
    assign o_origins_x=reg_origins_x_o;
    assign o_origins_y=reg_origins_y_o;
    assign o_overrun=flag_overrun_o;

endmodule
