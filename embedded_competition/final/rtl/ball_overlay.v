`timescale 1ns / 1ps
// 框比较与颜色合成分两拍；数据、坐标和标记同步前进。
module ball_overlay #(
    parameter C_X_MIN=64, C_Y_MIN=160, C_X_END=1216, C_Y_END=640,
    parameter C_GATE_MIN=544, C_GATE_END=736, C_LINE=640, C_HYST=16,
    parameter C_PANEL_CONFIG=0, C_VIEW_SWITCH=0
)(
    input i_clk,
    input i_rstn,
    input [95:0] i_rgb,
    input i_view_ball,
    input i_valid,
    input i_sof,
    input i_eol,
    input i_eof,
    input [11:0] i_x,
    input [11:0] i_y,
    input [7:0] i_labels,
    input i_mask,
    input i_count_mode,
    input i_face_locked,
    input [11:0] i_face_guide_left,
    input [11:0] i_face_guide_right,
    input i_face_valid,
    input [11:0] i_face_left,
    input [11:0] i_face_right,
    input [11:0] i_face_top,
    input [11:0] i_face_bottom,
    input [17:0] i_gain_red,
    input [17:0] i_gain_blue,
    input [191:0] i_settings,
    input [3:0] i_box_good,
    input [3:0] i_box_predicted,
    input [7:0] i_box_valid,
    input [15:0] i_box_color,
    input [95:0] i_box_left,
    input [95:0] i_box_right,
    input [95:0] i_box_top,
    input [95:0] i_box_bottom,
    output [95:0] o_rgb,
    output o_view_ball,
    output o_valid,
    output o_sof,
    output o_eol,
    output o_eof,
    output [11:0] o_x,
    output [11:0] o_y
);
    wire effective_view=!C_VIEW_SWITCH || i_view_ball;
    reg reg_view,reg_view_o;
    localparam C_BOX_SLOTS=C_PANEL_CONFIG ? 4 : 8;
    wire flag_show=!C_PANEL_CONFIG || i_settings[25];
    wire [11:0] wire_roi_left=C_PANEL_CONFIG ? i_settings[43:32] : C_X_MIN;
    wire [11:0] wire_roi_right=C_PANEL_CONFIG ? i_settings[75:64] : C_X_END;
    wire [11:0] wire_roi_top=C_PANEL_CONFIG ? i_settings[59:48] : C_Y_MIN;
    wire [11:0] wire_roi_bottom=C_PANEL_CONFIG ? i_settings[91:80] : C_Y_END;
    wire [11:0] wire_roi_last_x=wire_roi_right-12'd1,wire_roi_last_y=wire_roi_bottom-12'd1;
    wire [11:0] wire_count_line=C_PANEL_CONFIG ? i_settings[171:160] : C_LINE;
    function [23:0] palette;
        input [1:0] color;
        begin
            case(color)
                1:begin palette=24'hff4050; end
                2:begin palette=24'hffdf20; end
                3:begin palette=24'h20ef70; end
                default:begin palette=24'h000000; end
            endcase
        end
    endfunction
    // Q16显示增益最大2倍，乘积加半LSB后截位，超过255时饱和。
    function [7:0] display_balance;
        input [7:0] value;
        input [17:0] gain;
        reg [25:0] product;
        begin
            product=value*gain+26'd32768;
            display_balance=(|product[25:24]) ? 8'd255 : product[23:16];
        end
    endfunction
    reg [95:0] reg_source;
    reg [3:0] reg_markers;
    reg [11:0] reg_x, reg_y;
    reg [15:0] reg_box_color;
    reg [C_BOX_SLOTS*4-1:0] reg_hit;
    reg [3:0] reg_box_good,reg_box_predicted;
    reg [3:0] reg_roi,reg_gate,reg_line;
    reg [3:0] reg_face_guide,reg_face_hit;
    reg [95:0] reg_rgb_o;
    reg [3:0] reg_markers_o;
    reg [11:0] reg_x_o,reg_y_o;
    integer lane,slot;
    reg [12:0] px;
    reg [23:0] pixel;
    // 第一级只登记框边界；目标槽位仍由检测结果表提供。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_source<=0; reg_view<=0; reg_markers<=0; reg_x<=0; reg_y<=0; reg_hit<=0;
            reg_box_color<=0; reg_roi<=0; reg_gate<=0; reg_line<=0;reg_face_guide<=0;reg_face_hit<=0;
            reg_box_good<=0;reg_box_predicted<=0;
        end else begin
            reg_view<=effective_view;reg_markers<={i_valid,i_sof,i_eol,i_eof}; reg_x<=i_x; reg_y<=i_y; reg_box_color<=i_box_color;
            reg_box_good<=i_box_good;reg_box_predicted<=i_box_predicted;
            for(lane=0;lane<4;lane=lane+1)begin
                px={1'b0,i_x}+lane[12:0];
                reg_source[95-lane*24 -:24]<=!effective_view ? i_rgb[95-lane*24 -:24] : i_mask ? palette(i_labels[lane*2 +:2]) :
                    {display_balance(i_rgb[95-lane*24 -:8],i_gain_red),
                     i_rgb[87-lane*24 -:8],
                     display_balance(i_rgb[79-lane*24 -:8],i_gain_blue)};
                reg_roi[lane]<=flag_show && px >= wire_roi_left && px < wire_roi_right && i_y >= wire_roi_top && i_y < wire_roi_bottom &&
                    (px == wire_roi_left || px == wire_roi_last_x || i_y == wire_roi_top || i_y == wire_roi_last_y);
                reg_gate[lane]<=!C_PANEL_CONFIG && i_count_mode && i_y >= C_Y_MIN && i_y < C_Y_END &&
                    (px == C_GATE_MIN || px == C_GATE_END-1 || px == C_LINE-C_HYST || px == C_LINE+C_HYST);
                reg_line[lane]<=flag_show && i_count_mode && i_y >= wire_roi_top && i_y < wire_roi_bottom && px == wire_count_line;
                reg_face_guide[lane]<=i_face_locked && px >= i_face_guide_left && px <= i_face_guide_right && i_y >= 232 && i_y < 488 &&
                    (px == i_face_guide_left || px == i_face_guide_right || i_y == 232 || i_y == 487);
                reg_face_hit[lane]<=i_face_locked && i_face_valid && px >= i_face_left && px <= i_face_right &&
                    i_y >= i_face_top && i_y <= i_face_bottom &&
                    (px == i_face_left || px == i_face_right || i_y == i_face_top || i_y == i_face_bottom);
                for(slot=0;slot<C_BOX_SLOTS;slot=slot+1)begin
                    reg_hit[lane*C_BOX_SLOTS+slot]<=flag_show && i_box_valid[slot] &&
                        px >= i_box_left[slot*12 +:12] && px <= i_box_right[slot*12 +:12] &&
                        i_y >= i_box_top[slot*12 +:12] && i_y <= i_box_bottom[slot*12 +:12] &&
                        (px == i_box_left[slot*12 +:12] || px == i_box_right[slot*12 +:12] ||
                         i_y == i_box_top[slot*12 +:12] || i_y == i_box_bottom[slot*12 +:12]);
                end
            end
        end
    end
    // 第二级选择颜色；非有效周期只传递无效标记。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_view_o<=0;reg_rgb_o<=0; reg_markers_o<=0; reg_x_o<=0; reg_y_o<=0; end
        else begin
            reg_view_o<=reg_view;reg_markers_o<=reg_markers; reg_x_o<=reg_x; reg_y_o<=reg_y;
            for(lane=0;lane<4;lane=lane+1)begin
                pixel=reg_source[95-lane*24 -:24];
                if(reg_view)begin
                if(reg_roi[lane])begin pixel=24'h8090a0; end
                if(reg_gate[lane])begin pixel=24'h407090; end
                if(reg_line[lane])begin pixel=24'hffffff; end
                for(slot=0;slot<C_BOX_SLOTS;slot=slot+1)begin
                    if(reg_hit[lane*C_BOX_SLOTS+slot])begin
                        if(C_PANEL_CONFIG)pixel=(reg_box_predicted[slot] || reg_box_color[slot*2+:2]==0) ? 24'h909090 : reg_box_good[slot] ? 24'h20ef70 : 24'hff4050;
                        else pixel=reg_box_color[slot*2 +:2] == 0 ? 24'h909090 : palette(reg_box_color[slot*2 +:2]);
                    end
                end
                if(reg_face_guide[lane])pixel=24'h307080;
                if(reg_face_hit[lane])pixel=24'h20e8ff;
                end
                reg_rgb_o[95-lane*24 -:24]<=pixel;
            end
        end
    end
    assign o_rgb=reg_rgb_o;
    assign o_view_ball=reg_view_o;
    assign o_valid=reg_markers_o[3];
    assign o_sof=reg_markers_o[2];
    assign o_eol=reg_markers_o[1];
    assign o_eof=reg_markers_o[0];
    assign o_x=reg_x_o;
    assign o_y=reg_y_o;
endmodule
