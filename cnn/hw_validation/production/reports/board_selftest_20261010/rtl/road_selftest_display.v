`timescale 1ns / 1ps

// 自检诊断快照在VS消隐边界切换；固定TEST标志不属于识别画面。
module road_selftest_display (
    input i_clk,                          // 快照源计算时钟
    input i_rstn,                         // 源域同步释放复位
    input [255:0] i_payload,              // 运行进度或持续终态
    input i_pixel_clk,                    // 官方75MHz像素时钟
    input i_pixel_rstn,                   // 像素域同步释放复位
    input i_vsync,                        // 官方VTC垂直同步
    input i_de,                           // 官方VTC有效像素
    output [23:0] o_rgb,                  // 与输出VS/DE等延迟色块
    output o_vsync,                       // 延迟一拍垂直同步
    output o_de,                          // 延迟一拍有效像素
    output [255:0] o_active_payload       // 整帧冻结快照观察口
);
    //---------------寄存器信号-----------------//
    reg [255:0] reg_hold_payload;         // 源端冻结，ack前不覆盖
    reg reg_request;                     // 源端翻转发布请求
    reg reg_ack_meta;                    // 返回确认第一级
    reg reg_ack_sync;                    // 返回确认第二级
    reg reg_request_meta;                // 目标请求第一级
    reg reg_request_sync;                // 目标请求第二级
    reg reg_acknowledge;                 // VS采样后的确认
    reg [255:0] reg_active_payload;       // 像素整帧使用的诊断表
    reg reg_vsync_previous;              // 检测消隐区VS上升沿
    reg reg_de_previous;                 // 检测有效行结束
    reg [10:0] cnt_x;                     // 有效像素横向坐标
    reg [9:0] cnt_y;                      // 有效行纵向坐标
    reg [5:0] cnt_frames;                // 显示本地心跳，不是检测FPS
    reg [19:0] dec_test_row;              // 固定TEST字符的一行点阵
    reg [23:0] dec_rgb;                  // 当前输入像素的状态颜色
    reg [23:0] rgb_o;                    // RGB输出寄存器
    reg vsync_o;                         // VS输出寄存器
    reg de_o;                            // DE输出寄存器

    //---------------输出信号连线---------------//
    assign o_rgb = rgb_o;
    assign o_vsync = vsync_o;
    assign o_de = de_o;
    assign o_active_payload = reg_active_payload;

    //---------------主要任务处理区域---------------//
    // 源端仅在上次确认返回后改写冻结载荷并发布下一请求。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_hold_payload <= 256'd0;
            reg_request <= 1'b0;
            reg_ack_meta <= 1'b0;
            reg_ack_sync <= 1'b0;
        end else begin
            reg_ack_meta <= reg_acknowledge;
            reg_ack_sync <= reg_ack_meta;
            if (reg_request == reg_ack_sync) begin
                reg_hold_payload <= i_payload;
                reg_request <= ~reg_request;
            end
        end
    end

    // 两级同步只用于请求；载荷保持到VS实际采样后才确认。
    always @(posedge i_pixel_clk or negedge i_pixel_rstn) begin
        if (!i_pixel_rstn) begin
            reg_request_meta <= 1'b0;
            reg_request_sync <= 1'b0;
            reg_acknowledge <= 1'b0;
            reg_active_payload <= 256'd0;
            reg_vsync_previous <= 1'b0;
            reg_de_previous <= 1'b0;
            cnt_x <= 11'd0;
            cnt_y <= 10'd0;
            cnt_frames <= 6'd0;
        end else begin
            reg_request_meta <= reg_request;
            reg_request_sync <= reg_request_meta;
            reg_vsync_previous <= i_vsync;
            reg_de_previous <= i_de;
            if (i_vsync && !reg_vsync_previous) begin
                cnt_x <= 11'd0;
                cnt_y <= 10'd0;
                cnt_frames <= cnt_frames + 6'd1;
                if (reg_request_sync != reg_acknowledge) begin
                    reg_active_payload <= reg_hold_payload;
                    reg_acknowledge <= reg_request_sync;
                end
            end else if (i_de) begin
                cnt_x <= cnt_x + 11'd1;
            end else begin
                cnt_x <= 11'd0;
                if (reg_de_previous) cnt_y <= cnt_y + 10'd1;
            end
        end
    end

    // 只包含固定TEST四字母，不建立通用字库或字符控制接口。
    always @(*) begin
        case (cnt_y[5:3])
            3'd0: dec_test_row = 20'b11110111100111011110;
            3'd1: dec_test_row = 20'b00100100001000000100;
            3'd2: dec_test_row = 20'b00100100001000000100;
            3'd3: dec_test_row = 20'b00100111000110000100;
            3'd4: dec_test_row = 20'b00100100000001000100;
            3'd5: dec_test_row = 20'b00100100000001000100;
            3'd6: dec_test_row = 20'b00100111101110000100;
            default: dec_test_row = 20'd0;
        endcase
    end

    // 黄色运行、绿色通过、红色失败；诊断带从最高位向右逐位显示。
    always @(*) begin
        case (reg_active_payload[255:254])
            2'd1: dec_rgb = 24'h00c040;
            2'd2: dec_rgb = 24'hd02020;
            default: dec_rgb = 24'hd0a000;
        endcase
        if ((cnt_y < 10'd56) && (cnt_x < 11'd160)) begin
            dec_rgb = dec_test_row[5'd19 - cnt_x[7:3]] ? 24'hffffff : 24'h502080;
        end
        if ((cnt_y >= 10'd80) && (cnt_y < 10'd112) && (cnt_x < 11'd1024)) begin
            dec_rgb = reg_active_payload[8'd255 - cnt_x[9:2]] ? 24'hffffff : 24'h000000;
        end
        if ((cnt_y < 10'd64) && (cnt_x >= 11'd1152)) begin
            dec_rgb = cnt_frames[4] ? 24'h4080ff : 24'h102040;
        end
        if (!i_de) dec_rgb = 24'd0;
    end

    // 颜色与时序共同延迟一拍再送原HDMI发送器。
    always @(posedge i_pixel_clk or negedge i_pixel_rstn) begin
        if (!i_pixel_rstn) begin
            rgb_o <= 24'd0;
            vsync_o <= 1'b0;
            de_o <= 1'b0;
        end else begin
            rgb_o <= dec_rgb;
            vsync_o <= i_vsync;
            de_o <= i_de;
        end
    end
endmodule
