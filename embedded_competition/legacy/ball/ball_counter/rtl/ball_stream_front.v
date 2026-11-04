`timescale 1ns / 1ps
// 两拍前端：判色后检查四像素支持，RGB/坐标/标记同步延迟。
module ball_stream_front #(
    parameter C_WIDTH = 1280,
    parameter C_HEIGHT = 720,
    parameter C_X_MIN = 64,
    parameter C_Y_MIN = 160,
    parameter C_X_END = 1216,
    parameter C_Y_END = 640,
    parameter C_GATE_MIN = 544,
    parameter C_GATE_END = 736
)(
    input i_clk,
    input i_rstn,
    input [95:0] i_rgb,
    input i_valid,
    input i_early,
    input i_strict,
    input [15:0] i_epoch,
    output [95:0] o_rgb,
    output o_valid,
    output o_sof,
    output o_eol,
    output o_eof,
    output [11:0] o_x,
    output [11:0] o_y,
    output [7:0] o_labels,
    output [2:0] o_gate_hits,
    output [15:0] o_epoch,
    output o_error
);
    reg [11:0] reg_x, reg_y; // 当前输入组左端坐标。
    reg flag_active, flag_pending; // 已开帧及待提交的像素SOF。
    reg [95:0] reg_rgb_o;
    reg reg_valid_o, reg_sof_o, reg_eol_o, reg_eof_o;
    reg [11:0] reg_x_o, reg_y_o;
    reg [7:0] reg_labels_o;
    reg [15:0] reg_epoch_o;
    reg flag_error_o;
    wire [11:0] wire_x = i_early ? 12'd0 : reg_x;
    wire [11:0] wire_y = i_early ? 12'd0 : reg_y;
    reg [7:0] dec_labels;
    reg [7:0] dec_weak_labels,reg_weak_labels;
    reg reg_strict;
    reg [95:0] reg_filtered_rgb;
    reg reg_filtered_valid,reg_filtered_sof,reg_filtered_eol,reg_filtered_eof;
    reg [11:0] reg_filtered_x,reg_filtered_y;
    reg [15:0] reg_filtered_epoch;
    reg [7:0] dec_supported_labels,reg_supported_labels;
    reg [2:0] cnt_gate,reg_supported_gate;
    reg [2:0] cnt_strong_red,cnt_strong_yellow,cnt_strong_green;
    reg [2:0] cnt_weak_red,cnt_weak_yellow,cnt_weak_green;
    reg [1:0] strong_color,weak_color,supported_color;
    reg [1:0] dec_color;
    integer lane,pixel_x,vote_lane,vote_x;

    // 普通档用相对通道优势识别暗球；严格档保留高亮度门槛。
    function [1:0] classify;
        input [23:0] pixel;
        input tight;
        reg [8:0] red, green, blue, floor_value, margin;
        reg [10:0] red_four, green_four, blue_five, red_five, green_five;
        begin
            red = {1'b0,pixel[23:16]};
            green = {1'b0,pixel[15:8]};
            blue = {1'b0,pixel[7:0]};
            floor_value = tight ? 9'd150 : 9'd100;
            margin = tight ? 9'd50 : 9'd30;
            red_four = {2'd0,red} << 2;
            green_four = {2'd0,green} << 2;
            blue_five = ({2'd0,blue} << 2)+blue;
            red_five = red_four+red;
            green_five = green_four+green;
            classify = 0;
            if(!tight)begin
                // 五比四的颜色优势及12级色差拒绝灰白与青色背景。
                // 黄与红绿使用互补边界，避免暗红被黄优先规则吞掉。
                if(red >= 64 && green >= 64 && red > blue+9'd12 && green > blue+9'd12 &&
                   red_four > blue_five && green_four > blue_five &&
                   red_four <= green_five && green_four <= red_five)begin
                    classify = 2;
                end else if(red >= 64 && red > green+9'd12 && red > blue+9'd12 &&
                            red_four > green_five && red_four > blue_five)begin
                    classify = 1;
                end else if(green >= 64 && green > red+9'd12 && green > blue+9'd12 &&
                            green_four > red_five && green_four > blue_five)begin
                    classify = 3;
                end
            end else if(red >= floor_value && green >= floor_value && red > blue+margin &&
               green > blue+margin && red+9'd60 >= green && green+9'd60 >= red)begin
                classify = 2;
            end else if(red >= floor_value && red > green+margin && red > blue+margin)begin
                classify = 1;
            end else if(green >= floor_value && green > red+margin && green > blue+margin)begin
                classify = 3;
            end
        end
    endfunction

    // 暗部只产生候选；是否接受由下一拍的同组支持决定。
    function [1:0] classify_weak;
        input [23:0] pixel;
        reg [8:0] red,green,blue;
        reg [11:0] red_eight,green_eight,red_nine,green_nine,blue_nine;
        reg [10:0] red_four,green_four,red_five,green_five;
        begin
            red={1'b0,pixel[23:16]};green={1'b0,pixel[15:8]};blue={1'b0,pixel[7:0]};
            red_eight={3'd0,red} << 3;green_eight={3'd0,green} << 3;
            red_nine=red_eight+red;green_nine=green_eight+green;
            blue_nine=({3'd0,blue} << 3)+blue;
            red_four={2'd0,red} << 2;green_four={2'd0,green} << 2;
            red_five=red_four+red;green_five=green_four+green;
            classify_weak=0;
            if(red>=32 && green>=32 && red>blue+9'd6 && green>blue+9'd6 &&
               red_eight>blue_nine && green_eight>blue_nine &&
               red_four<=green_five && green_four<=red_five)begin classify_weak=2;end
            else if(red>=32 && red>green+9'd6 && red>blue+9'd6 &&
                    red_eight>green_nine && red_eight>blue_nine)begin classify_weak=1;end
            else if(green>=32 && green>red+9'd6 && green>blue+9'd6 &&
                    green_eight>red_nine && green_eight>blue_nine)begin classify_weak=3;end
        end
    endfunction

    // ROI逐像素判断，未命中也输出零标签以初始化完整首行列统计。
    always @(*)begin
        dec_labels = 0;
        dec_weak_labels = 0;
        dec_color = 0;
        pixel_x = 0;
        for(lane=0; lane<4; lane=lane+1)begin
            pixel_x = wire_x+lane;
            dec_color = 0;
            if(pixel_x >= C_X_MIN && pixel_x < C_X_END &&
               wire_y >= C_Y_MIN && wire_y < C_Y_END)begin
                dec_color = classify(i_rgb[95-lane*24 -: 24],i_strict);
                dec_weak_labels[lane*2 +:2]=classify_weak(i_rgb[95-lane*24 -:24]);
            end
            dec_labels[lane*2 +: 2] = dec_color;
        end
    end

    // 只检查同一四像素组，密集背景仍需后续二维目标分离。
    always @(*)begin
        cnt_strong_red=0;cnt_strong_yellow=0;cnt_strong_green=0;
        cnt_weak_red=0;cnt_weak_yellow=0;cnt_weak_green=0;
        dec_supported_labels=0;cnt_gate=0;
        strong_color=0;weak_color=0;supported_color=0;vote_x=0;
        for(vote_lane=0;vote_lane<4;vote_lane=vote_lane+1)begin
            case(reg_labels_o[vote_lane*2 +:2])
                1:cnt_strong_red=cnt_strong_red+1'b1;
                2:cnt_strong_yellow=cnt_strong_yellow+1'b1;
                3:cnt_strong_green=cnt_strong_green+1'b1;
                default:begin end
            endcase
            case(reg_weak_labels[vote_lane*2 +:2])
                1:cnt_weak_red=cnt_weak_red+1'b1;
                2:cnt_weak_yellow=cnt_weak_yellow+1'b1;
                3:cnt_weak_green=cnt_weak_green+1'b1;
                default:begin end
            endcase
        end
        for(vote_lane=0;vote_lane<4;vote_lane=vote_lane+1)begin
            strong_color=reg_labels_o[vote_lane*2 +:2];weak_color=reg_weak_labels[vote_lane*2 +:2];
            supported_color=0;
            if(reg_strict)begin supported_color=strong_color;end
            else if((strong_color==1 && cnt_strong_red>=2) ||
                    (strong_color==2 && cnt_strong_yellow>=2) ||
                    (strong_color==3 && cnt_strong_green>=2))begin supported_color=strong_color;end
            else if((weak_color==1 && cnt_weak_red>=3) ||
                    (weak_color==2 && cnt_weak_yellow>=3) ||
                    (weak_color==3 && cnt_weak_green>=3))begin supported_color=weak_color;end
            dec_supported_labels[vote_lane*2 +:2]=supported_color;
            vote_x=reg_x_o+vote_lane;
            if(supported_color!=0 && vote_x>=C_GATE_MIN && vote_x<C_GATE_END)begin cnt_gate=cnt_gate+1'b1;end
        end
    end

    // 输出寄存一级，RGB与分类、坐标及行帧标记同时交给后级。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_x <= 0; reg_y <= 0; flag_active <= 0; flag_pending <= 0;
            reg_rgb_o <= 0; reg_valid_o <= 0; reg_sof_o <= 0; reg_eol_o <= 0; reg_eof_o <= 0;
            reg_x_o <= 0; reg_y_o <= 0; reg_labels_o <= 0;reg_weak_labels<=0;reg_strict<=0;
            reg_epoch_o <= 0; flag_error_o <= 0;
        end else begin
            reg_valid_o <= 0; reg_sof_o <= 0; reg_eol_o <= 0; reg_eof_o <= 0;
            if(i_early)begin
                if(flag_active)begin flag_error_o <= 1; end
                reg_x <= 0; reg_y <= 0; flag_active <= 1; flag_pending <= 1;
            end
            if(i_valid && (flag_active || i_early))begin
                reg_rgb_o <= i_rgb; reg_valid_o <= 1;
                reg_sof_o <= flag_pending || i_early; flag_pending <= 0;
                reg_x_o <= wire_x; reg_y_o <= wire_y;
                reg_labels_o <= dec_labels;reg_weak_labels<=dec_weak_labels;reg_strict<=i_strict;reg_epoch_o <= i_epoch;
                if(wire_x == C_WIDTH-4)begin
                    reg_x <= 0; reg_eol_o <= 1;
                    if(wire_y == C_HEIGHT-1)begin
                        reg_y <= 0; flag_active <= 0; reg_eof_o <= 1;
                    end else begin reg_y <= wire_y+1'b1; end
                end else begin reg_x <= wire_x+12'd4; end
            end
        end
    end
    // 第二拍保留完整元数据；invalid空拍不推进输入坐标。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_filtered_rgb<=0;reg_filtered_valid<=0;reg_filtered_sof<=0;reg_filtered_eol<=0;reg_filtered_eof<=0;
            reg_filtered_x<=0;reg_filtered_y<=0;reg_filtered_epoch<=0;reg_supported_labels<=0;reg_supported_gate<=0;
        end else begin
            reg_filtered_rgb<=reg_rgb_o;reg_filtered_valid<=reg_valid_o;
            reg_filtered_sof<=reg_sof_o;reg_filtered_eol<=reg_eol_o;reg_filtered_eof<=reg_eof_o;
            reg_filtered_x<=reg_x_o;reg_filtered_y<=reg_y_o;reg_filtered_epoch<=reg_epoch_o;
            reg_supported_labels<=dec_supported_labels;reg_supported_gate<=cnt_gate;
        end
    end
    assign o_rgb = reg_filtered_rgb;
    assign o_valid = reg_filtered_valid;
    assign o_sof = reg_filtered_sof;
    assign o_eol = reg_filtered_eol;
    assign o_eof = reg_filtered_eof;
    assign o_x = reg_filtered_x;
    assign o_y = reg_filtered_y;
    assign o_labels = reg_supported_labels;
    assign o_gate_hits = reg_supported_gate;
    assign o_epoch = reg_filtered_epoch;
    assign o_error = flag_error_o;
endmodule
