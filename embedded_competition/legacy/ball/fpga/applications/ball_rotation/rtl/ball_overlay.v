`timescale 1ns / 1ps
// 框比较与颜色合成分两拍；数据、坐标和标记同步前进。
module ball_overlay #(
    parameter C_X_MIN=64, C_Y_MIN=160, C_X_END=1216, C_Y_END=640,
    parameter C_GATE_MIN=544, C_GATE_END=736, C_LINE=640, C_HYST=16
)(
    input i_clk,
    input i_rstn,
    input [95:0] i_rgb,
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
    input i_face_valid,
    input [11:0] i_face_left,
    input [11:0] i_face_right,
    input [11:0] i_face_top,
    input [11:0] i_face_bottom,
    input [7:0] i_box_valid,
    input [15:0] i_box_color,
    input [95:0] i_box_left,
    input [95:0] i_box_right,
    input [95:0] i_box_top,
    input [95:0] i_box_bottom,
    output [95:0] o_rgb,
    output o_valid,
    output o_sof,
    output o_eol,
    output o_eof,
    output [11:0] o_x,
    output [11:0] o_y
);
    wire [11:0] wire_center_x[0:7],wire_center_y[0:7];
    genvar box_index;
    generate
        for(box_index=0;box_index<8;box_index=box_index+1)begin:gen_box_center
            wire [12:0] wire_sum_x={1'b0,i_box_left[box_index*12 +: 12]}+{1'b0,i_box_right[box_index*12 +: 12]};
            wire [12:0] wire_sum_y={1'b0,i_box_top[box_index*12 +: 12]}+{1'b0,i_box_bottom[box_index*12 +: 12]};
            assign wire_center_x[box_index]=wire_sum_x[12:1];
            assign wire_center_y[box_index]=wire_sum_y[12:1];
        end
    endgenerate
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
    reg [95:0] reg_source;
    reg [3:0] reg_markers;
    reg [11:0] reg_x, reg_y;
    reg [15:0] reg_box_color;
    reg [31:0] reg_hit;
    reg [3:0] reg_roi,reg_gate,reg_line;
    reg [3:0] reg_face_guide,reg_face_hit;
    reg [95:0] reg_rgb_o;
    reg [3:0] reg_markers_o;
    reg [11:0] reg_x_o,reg_y_o;
    integer lane,slot,px,dx,dy;
    reg [23:0] pixel;
    // 第一级并行计算每个框的边界与中心十字。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_source<=0; reg_markers<=0; reg_x<=0; reg_y<=0; reg_hit<=0;
            reg_box_color<=0; reg_roi<=0; reg_gate<=0; reg_line<=0;reg_face_guide<=0;reg_face_hit<=0;
        end else begin
            reg_markers<={i_valid,i_sof,i_eol,i_eof}; reg_x<=i_x; reg_y<=i_y; reg_box_color<=i_box_color;
            for(lane=0;lane<4;lane=lane+1)begin
                px=i_x+lane;
                reg_source[95-lane*24 -:24]<=i_mask ? palette(i_labels[lane*2 +:2]) : i_rgb[95-lane*24 -:24];
                reg_roi[lane]<=px >= C_X_MIN && px < C_X_END && i_y >= C_Y_MIN && i_y < C_Y_END &&
                    (px == C_X_MIN || px == C_X_END-1 || i_y == C_Y_MIN || i_y == C_Y_END-1);
                reg_gate[lane]<=i_count_mode && i_y >= C_Y_MIN && i_y < C_Y_END &&
                    (px == C_GATE_MIN || px == C_GATE_END-1 || px == C_LINE-C_HYST || px == C_LINE+C_HYST);
                reg_line[lane]<=i_count_mode && i_y >= C_Y_MIN && i_y < C_Y_END && px == C_LINE;
                reg_face_guide[lane]<=i_face_locked && px >= 512 && px < 768 && i_y >= 232 && i_y < 488 &&
                    (px == 512 || px == 767 || i_y == 232 || i_y == 487);
                reg_face_hit[lane]<=i_face_locked && i_face_valid && px >= i_face_left && px <= i_face_right &&
                    i_y >= i_face_top && i_y <= i_face_bottom &&
                    (px == i_face_left || px == i_face_right || i_y == i_face_top || i_y == i_face_bottom);
                for(slot=0;slot<8;slot=slot+1)begin
                    dx=px >= wire_center_x[slot] ? px-wire_center_x[slot] : wire_center_x[slot]-px;
                    dy=i_y >= wire_center_y[slot] ? i_y-wire_center_y[slot] : wire_center_y[slot]-i_y;
                    reg_hit[lane*8+slot]<=i_box_valid[slot] &&
                        ((px >= i_box_left[slot*12 +:12] && px <= i_box_right[slot*12 +:12] &&
                          i_y >= i_box_top[slot*12 +:12] && i_y <= i_box_bottom[slot*12 +:12] &&
                          (px == i_box_left[slot*12 +:12] || px == i_box_right[slot*12 +:12] ||
                           i_y == i_box_top[slot*12 +:12] || i_y == i_box_bottom[slot*12 +:12])) ||
                         (dy == 0 && dx <= 5) || (dx == 0 && dy <= 5));
                end
            end
        end
    end
    // 第二级选择颜色；非有效周期只传递无效标记。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_rgb_o<=0; reg_markers_o<=0; reg_x_o<=0; reg_y_o<=0; end
        else begin
            reg_markers_o<=reg_markers; reg_x_o<=reg_x; reg_y_o<=reg_y;
            for(lane=0;lane<4;lane=lane+1)begin
                pixel=reg_source[95-lane*24 -:24];
                if(reg_roi[lane])begin pixel=24'h8090a0; end
                if(reg_gate[lane])begin pixel=24'h407090; end
                if(reg_line[lane])begin pixel=24'hffffff; end
                for(slot=0;slot<8;slot=slot+1)begin
                    if(reg_hit[lane*8+slot])begin
                        pixel=reg_box_color[slot*2 +:2] == 0 ? 24'h909090 : palette(reg_box_color[slot*2 +:2]);
                    end
                end
                if(reg_face_guide[lane])pixel=24'h307080;
                if(reg_face_hit[lane])pixel=24'h20e8ff;
                reg_rgb_o[95-lane*24 -:24]<=pixel;
            end
        end
    end
    assign o_rgb=reg_rgb_o;
    assign o_valid=reg_markers_o[3];
    assign o_sof=reg_markers_o[2];
    assign o_eol=reg_markers_o[1];
    assign o_eof=reg_markers_o[0];
    assign o_x=reg_x_o;
    assign o_y=reg_y_o;
endmodule
