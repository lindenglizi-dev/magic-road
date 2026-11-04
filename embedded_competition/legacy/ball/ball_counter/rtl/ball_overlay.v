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
    input [17:0] i_gain_red,
    input [17:0] i_gain_blue,
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
    // 行号和列号均限制为三位，避免通用整数字模索引引入乘法长路径。
    function [4:0] track_row;
        input [1:0] index;
        input [2:0] row;
        reg [34:0] glyph;
        begin
            glyph=track_glyph(index);
            case(row)
                0:track_row=glyph[34:30];1:track_row=glyph[29:25];
                2:track_row=glyph[24:20];3:track_row=glyph[19:15];
                4:track_row=glyph[14:10];5:track_row=glyph[9:5];
                6:track_row=glyph[4:0];default:track_row=0;
            endcase
        end
    endfunction
    // COUNT框内数字对应四个固定轨迹槽，失联保留期间编号不换。
    function [34:0] track_glyph;
        input [1:0] index;
        begin
            case(index)
                0:track_glyph=35'b00100_01100_00100_00100_00100_00100_01110;
                1:track_glyph=35'b01110_10001_00001_00010_00100_01000_11111;
                2:track_glyph=35'b11110_00001_00001_01110_00001_00001_11110;
                3:track_glyph=35'b00010_00110_01010_10010_11111_00010_00010;
                default:track_glyph=0;
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
    // 显示专用S曲线：压低暗部、拉开中间调，保留黑白端点与灰阶中性。
    // 位宽覆盖5*255；本函数只进入原图支路，颜色标签和掩膜不变。
    function [7:0] display_tone;
        input [7:0] value;
        reg [10:0] scaled;
        begin
            if(value < 8'd64)begin
                scaled=({3'd0,value} << 1)+{3'd0,value}+11'd2;
            end else if(value <= 8'd192)begin
                scaled=({3'd0,value} << 2)+{3'd0,value}-11'd128+11'd2;
            end else begin
                scaled=({3'd0,value} << 1)+{3'd0,value}+11'd257;
            end
            display_tone=scaled[9:2];
        end
    endfunction
    reg [95:0] reg_source;
    reg flag_source_mask;
    reg [3:0] reg_markers;
    reg [11:0] reg_x, reg_y;
    reg [15:0] reg_box_color;
    reg [31:0] reg_hit;
    reg [3:0] reg_roi,reg_gate,reg_line;
    reg [95:0] reg_rgb_o;
    reg [3:0] reg_markers_o;
    reg [11:0] reg_x_o,reg_y_o;
    integer lane,slot,px,dx,dy;
    reg signed [13:0] tag_offset_x,tag_offset_y;
    reg [4:0] tag_row_bits;
    reg [23:0] pixel;
    // 第一级并行计算每个框的边界与中心十字。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_source<=0;flag_source_mask<=0; reg_markers<=0; reg_x<=0; reg_y<=0; reg_hit<=0;
            reg_box_color<=0; reg_roi<=0; reg_gate<=0; reg_line<=0;
        end else begin
            reg_markers<={i_valid,i_sof,i_eol,i_eof};flag_source_mask<=i_mask; reg_x<=i_x; reg_y<=i_y; reg_box_color<=i_box_color;
            for(lane=0;lane<4;lane=lane+1)begin
                px=i_x+lane;
                reg_source[95-lane*24 -:24]<=i_mask ? palette(i_labels[lane*2 +:2]) :
                    {display_balance(i_rgb[95-lane*24 -:8],i_gain_red),i_rgb[87-lane*24 -:8],display_balance(i_rgb[79-lane*24 -:8],i_gain_blue)};
                reg_roi[lane]<=px >= C_X_MIN && px < C_X_END && i_y >= C_Y_MIN && i_y < C_Y_END &&
                    (px == C_X_MIN || px == C_X_END-1 || i_y == C_Y_MIN || i_y == C_Y_END-1);
                reg_gate[lane]<=i_count_mode && i_y >= C_Y_MIN && i_y < C_Y_END &&
                    (px == C_GATE_MIN || px == C_GATE_END-1 || px == C_LINE-C_HYST || px == C_LINE+C_HYST);
                reg_line[lane]<=i_count_mode && i_y >= C_Y_MIN && i_y < C_Y_END && px == C_LINE;
                for(slot=0;slot<8;slot=slot+1)begin
                    tag_offset_x=$signed({2'd0,px[11:0]})-$signed({2'd0,i_box_left[slot*12 +:12]})-14'sd4;
                    tag_offset_y=$signed({2'd0,i_y})-$signed({2'd0,i_box_top[slot*12 +:12]})-14'sd4;
                    tag_row_bits=track_row(slot,tag_offset_y[3:1]);
                    dx=px >= wire_center_x[slot] ? px-wire_center_x[slot] : wire_center_x[slot]-px;
                    dy=i_y >= wire_center_y[slot] ? i_y-wire_center_y[slot] : wire_center_y[slot]-i_y;
                    reg_hit[lane*8+slot]<=i_box_valid[slot] &&
                        ((px >= i_box_left[slot*12 +:12] && px <= i_box_right[slot*12 +:12] &&
                          i_y >= i_box_top[slot*12 +:12] && i_y <= i_box_bottom[slot*12 +:12] &&
                          (px == i_box_left[slot*12 +:12] || px == i_box_right[slot*12 +:12] ||
                           i_y == i_box_top[slot*12 +:12] || i_y == i_box_bottom[slot*12 +:12])) ||
                         (dy == 0 && dx <= 5) || (dx == 0 && dy <= 5) ||
                         (i_count_mode && slot<4 && tag_offset_x>=0 && tag_offset_x<10 && tag_offset_y>=0 && tag_offset_y<14 &&
                          tag_row_bits[3'd4-tag_offset_x[3:1]]));
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
                if(!flag_source_mask)begin
                    pixel={display_tone(reg_source[95-lane*24 -:8]),display_tone(reg_source[87-lane*24 -:8]),display_tone(reg_source[79-lane*24 -:8])};
                end
                if(reg_roi[lane])begin pixel=24'h8090a0; end
                if(reg_gate[lane])begin pixel=24'h407090; end
                if(reg_line[lane])begin pixel=24'hffffff; end
                for(slot=0;slot<8;slot=slot+1)begin
                    if(reg_hit[lane*8+slot])begin
                        pixel=reg_box_color[slot*2 +:2] == 0 ? 24'h909090 : palette(reg_box_color[slot*2 +:2]);
                    end
                end
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
