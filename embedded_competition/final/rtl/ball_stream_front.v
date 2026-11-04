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
    parameter C_GATE_END = 736,
    parameter C_PANEL_CONFIG = 0,
    parameter C_DISPLAY_SOURCE = 0,
    parameter C_SERIAL_CLASSIFY = 0,
    parameter C_SHARED_GAMMA = 0,
    parameter C_CHECK_LAST = 0
)(
    input i_apply_gamma,
    input i_display_source_gamma,
    input i_clk,
    input i_rstn,
    input [95:0] i_rgb,
    input [95:0] i_display_rgb,
    input i_valid,
    input i_early,
    input i_last,
    input i_strict,
    input [15:0] i_epoch,
    input [191:0] i_settings,
    output [95:0] o_rgb,
    output o_valid,
    output o_sof,
    output o_eol,
    output o_eof,
    output [11:0] o_x,
    output [11:0] o_y,
    output [7:0] o_labels,
    output [7:0] o_geometry_labels,
    output [2:0] o_gate_hits,
    output [15:0] o_epoch,
    output o_error,
    output [3:0] o_highlight,
    output o_capture_fault
);
    wire [95:0] source_rgb,source_display_rgb;
    wire source_valid,source_early,source_last,source_strict;
    wire [15:0] source_epoch;
    wire [191:0] source_settings;
    wire [7:0] serial_strong,serial_weak;
    wire [3:0] serial_inside,serial_highlight;
    wire serial_error,serial_capture_fault;
    generate if(C_SERIAL_CLASSIFY)begin:gen_serial_classify
        wire [51:0] control;
        ball_color_group_serial #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
            .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_PANEL_CONFIG(C_PANEL_CONFIG),.C_CHECK_LAST(C_CHECK_LAST),.C_SHARED_GAMMA(C_SHARED_GAMMA)) color_lane(
            .i_apply_gamma(i_apply_gamma),.i_display_source_gamma(i_display_source_gamma),
            .i_clk(i_clk),.i_rstn(i_rstn),.i_rgb(i_rgb),.i_display_rgb(C_DISPLAY_SOURCE?i_display_rgb:i_rgb),
            .i_valid(i_valid),.i_early(i_early),.i_last(i_last),.i_strict(i_strict),.i_epoch(i_epoch),.i_settings(i_settings),
            .o_display_rgb(source_display_rgb),.o_valid(source_valid),.o_sof(source_early),.o_eol(source_last),.o_eof(),
            .o_epoch(source_epoch),.o_control(control),.o_strong(serial_strong),.o_weak(serial_weak),
            .o_inside(serial_inside),.o_highlight(serial_highlight),.o_error(serial_error),.o_capture_fault(serial_capture_fault),
            .o_busy(),.o_level());
        assign source_rgb=source_display_rgb;
        assign source_strict=control[1];
        assign source_settings={100'd0,control[51:40],4'd0,control[39:28],4'd0,control[27:16],4'd0,control[15:4],
            7'd0,control[1],14'd0,control[3:2],7'd0,control[0]};
    end else begin:gen_parallel_classify
        assign source_rgb=i_rgb;assign source_display_rgb=i_display_rgb;
        assign source_valid=i_valid;assign source_early=i_early;assign source_last=i_last;assign source_strict=i_strict;
        assign source_epoch=i_epoch;assign source_settings=i_settings;
        assign serial_strong=0;assign serial_weak=0;assign serial_inside=0;assign serial_highlight=0;
        assign serial_error=0;assign serial_capture_fault=0;
    end endgenerate
    reg [3:0] reg_serial_highlight;

    reg [11:0] reg_x, reg_y; // 当前输入组左端坐标。
    reg flag_active, flag_pending; // 已开帧及待提交的像素SOF。
    reg [63:0] reg_highlight_bounds;
    reg [3:0] reg_highlight_o;
    wire [63:0] wire_highlight_bounds;
    wire [3:0] wire_highlight;
    wire flag_settings_strict=C_PANEL_CONFIG ? source_settings[24] : source_strict;
    reg [3:0] dec_inside,reg_inside;
    function [15:0] highlight_bounds;
        input [23:0] pixel;
        reg [7:0] minimum,maximum;
        begin
            minimum=pixel[23:16];maximum=minimum;
            if(pixel[15:8]<minimum)minimum=pixel[15:8];
            if(pixel[7:0]<minimum)minimum=pixel[7:0];
            if(pixel[15:8]>maximum)maximum=pixel[15:8];
            if(pixel[7:0]>maximum)maximum=pixel[7:0];
            highlight_bounds={maximum,minimum};
        end
    endfunction
    genvar highlight_lane;
    generate if(!C_SERIAL_CLASSIFY)begin:gen_parallel_highlight
    for(highlight_lane=0;highlight_lane<4;highlight_lane=highlight_lane+1)begin:gen_highlight
        assign wire_highlight_bounds[highlight_lane*16+:16]=highlight_bounds(source_rgb[95-highlight_lane*24-:24]);
        assign wire_highlight[highlight_lane]=reg_highlight_bounds[highlight_lane*16+:8]>=160 &&
            {1'b0,reg_highlight_bounds[highlight_lane*16+8+:8]}<=
            {1'b0,reg_highlight_bounds[highlight_lane*16+:8]}+9'd24;
    end
    end else begin:gen_serial_highlight
        assign wire_highlight_bounds=0;
        assign wire_highlight=reg_serial_highlight;
    end endgenerate
    assign o_highlight=reg_highlight_o;
    reg [95:0] reg_rgb_o;
    reg reg_valid_o, reg_sof_o, reg_eol_o, reg_eof_o;
    reg [11:0] reg_x_o, reg_y_o;
    reg [7:0] reg_labels_o;
    reg [15:0] reg_epoch_o;
    reg flag_error_o;
    reg flag_capture_bad,reg_capture_fault,reg_capture_fault_o;
    wire [11:0] wire_x = source_early ? 12'd0 : reg_x;
    wire [11:0] wire_y = source_early ? 12'd0 : reg_y;
    wire flag_line_fault=C_CHECK_LAST && source_valid && (flag_active || source_early) &&
        (source_last!=(wire_x==C_WIDTH-4));
    reg [7:0] dec_labels;
    reg [7:0] dec_weak_labels,reg_weak_labels;
    reg reg_strict;
    reg [95:0] reg_filtered_rgb;
    reg reg_filtered_valid,reg_filtered_sof,reg_filtered_eol,reg_filtered_eof;
    reg [11:0] reg_filtered_x,reg_filtered_y;
    reg [15:0] reg_filtered_epoch;
    reg [7:0] dec_supported_labels,reg_supported_labels;
    reg [7:0] dec_geometry_labels,reg_geometry_labels;
    reg [2:0] cnt_gate,reg_supported_gate;
    reg [2:0] cnt_strong_red,cnt_strong_yellow,cnt_strong_green;
    reg [2:0] cnt_weak_red,cnt_weak_yellow,cnt_weak_green;
    reg [1:0] reg_target_color;
    reg [1:0] strong_color,weak_color,supported_color;
    reg [1:0] dec_color;
    integer lane,vote_lane;
    reg [12:0] pixel_x,vote_x;

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
        dec_inside = C_PANEL_CONFIG ? 4'd0 : 4'hf;
        dec_color = 0;
        pixel_x = 0;
        if(C_SERIAL_CLASSIFY)begin
            dec_labels=serial_strong;dec_weak_labels=serial_weak;dec_inside=serial_inside;
        end else begin
        for(lane=0; lane<4; lane=lane+1)begin
            pixel_x = {1'b0,wire_x}+lane[12:0];
            dec_color = 0;
            if(pixel_x >= C_X_MIN && pixel_x < C_X_END &&
               wire_y >= C_Y_MIN && wire_y < C_Y_END &&
               (!C_PANEL_CONFIG || (source_settings[0] && pixel_x >= {1'b0,source_settings[43:32]} &&
                pixel_x < {1'b0,source_settings[75:64]} && wire_y >= source_settings[59:48] && wire_y < source_settings[91:80])))begin
                dec_color = classify(source_rgb[95-lane*24 -: 24],flag_settings_strict);
                dec_inside[lane]=1'b1;
                dec_weak_labels[lane*2 +:2]=classify_weak(source_rgb[95-lane*24 -:24]);
            end
            dec_labels[lane*2 +: 2] = dec_color;
        end
        end
    end

    // 组内滤波仅处理四个相邻像素，二维目标分离由连通域模块完成。
    always @(*)begin
        cnt_strong_red=0;cnt_strong_yellow=0;cnt_strong_green=0;
        cnt_weak_red=0;cnt_weak_yellow=0;cnt_weak_green=0;
        dec_supported_labels=0;dec_geometry_labels=0;cnt_gate=0;
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
                                                                                                         
            dec_geometry_labels[vote_lane*2 +:2]=supported_color;
            if(C_PANEL_CONFIG && reg_target_color!=0 && supported_color!=reg_target_color)begin
                supported_color=0;
            end
            dec_supported_labels[vote_lane*2 +:2]=supported_color;
            vote_x={1'b0,reg_x_o}+vote_lane[12:0];
            if(supported_color!=0 && vote_x>=C_GATE_MIN && vote_x<C_GATE_END)begin cnt_gate=cnt_gate+1'b1;end
        end
    end

    // 输出寄存一级，RGB与分类、坐标及行帧标记同时交给后级。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_x <= 0; reg_y <= 0; flag_active <= 0; flag_pending <= 0;
            reg_highlight_bounds<=0;reg_serial_highlight<=0;
            reg_inside<=0;
            reg_rgb_o <= 0; reg_valid_o <= 0; reg_sof_o <= 0; reg_eol_o <= 0; reg_eof_o <= 0;
            reg_x_o <= 0; reg_y_o <= 0; reg_labels_o <= 0;reg_weak_labels<=0;reg_strict<=0;
            reg_epoch_o <= 0; flag_error_o <= 0;
            flag_capture_bad<=0;reg_capture_fault<=0;
            reg_target_color<=0;
        end else begin
            reg_valid_o <= 0; reg_sof_o <= 0; reg_eol_o <= 0; reg_eof_o <= 0;
            reg_capture_fault<=0;
            if(source_early)begin
                flag_error_o<=0;
                if(flag_active && !flag_capture_bad)begin flag_error_o <= 1;reg_capture_fault<=1;end
                flag_capture_bad<=0;
                reg_x <= 0; reg_y <= 0; flag_active <= 1; flag_pending <= 1;
            end
            if(flag_line_fault && (source_early || !flag_capture_bad))begin
                flag_error_o<=1;flag_capture_bad<=1;reg_capture_fault<=1;
            end
            if(source_valid && (flag_active || source_early))begin
                reg_highlight_bounds<=wire_highlight_bounds;reg_serial_highlight<=serial_highlight;
                reg_inside<=dec_inside;
                reg_rgb_o <= C_DISPLAY_SOURCE ? source_display_rgb : source_rgb; reg_valid_o <= 1;
                reg_sof_o <= flag_pending || source_early; flag_pending <= 0;
                reg_x_o <= wire_x; reg_y_o <= wire_y;
                reg_labels_o <= dec_labels;reg_weak_labels<=dec_weak_labels;reg_strict<=flag_settings_strict;reg_epoch_o <= source_epoch;
                reg_target_color<=source_settings[9:8];
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
            reg_highlight_o<=0;
            reg_filtered_rgb<=0;reg_filtered_valid<=0;reg_filtered_sof<=0;reg_filtered_eol<=0;reg_filtered_eof<=0;
            reg_filtered_x<=0;reg_filtered_y<=0;reg_filtered_epoch<=0;reg_supported_labels<=0;reg_geometry_labels<=0;reg_supported_gate<=0;
            reg_capture_fault_o<=0;
        end else begin
            reg_capture_fault_o<=reg_capture_fault;
            reg_highlight_o<=wire_highlight & reg_inside;
            reg_filtered_rgb<=reg_rgb_o;reg_filtered_valid<=reg_valid_o;
            reg_filtered_sof<=reg_sof_o;reg_filtered_eol<=reg_eol_o;reg_filtered_eof<=reg_eof_o;
            reg_filtered_x<=reg_x_o;reg_filtered_y<=reg_y_o;reg_filtered_epoch<=reg_epoch_o;
            reg_supported_labels<=dec_supported_labels;reg_geometry_labels<=dec_geometry_labels;reg_supported_gate<=cnt_gate;
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
    assign o_geometry_labels = reg_geometry_labels;
    assign o_gate_hits = reg_supported_gate;
    assign o_epoch = reg_filtered_epoch;
    assign o_error = C_SERIAL_CLASSIFY ? serial_error : flag_error_o;
    assign o_capture_fault = C_SERIAL_CLASSIFY ? serial_capture_fault : reg_capture_fault_o;
endmodule
