`timescale 1ns / 1ps
// ROI capture / 高位为第一个RGB像素；4x4块先累加，最后统一舍入。
module face_roi_capture(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_arm,
    input i_valid,
    input i_sof,
    input i_eof,
    input i_error,
    input [11:0] i_x,
    input [11:0] i_y,
    input [95:0] i_rgb,
    input [15:0] i_epoch,
    output o_write,
    output [11:0] o_address,
    output [7:0] o_gray,
    output o_done,
    output [31:0] o_sample,
    output [15:0] o_epoch,
    output o_fault
);
    reg flag_active,flag_bad;
    reg [14:0] cnt_groups;
    reg [31:0] cnt_sample;
    reg [15:0] reg_epoch_o;
    wire flag_select=i_valid && flag_active && i_x >= 512 && i_x < 768 && i_y >= 232 && i_y < 488;
    wire [5:0] wire_column=(i_x-12'd512) >> 2;
    wire [5:0] wire_row=(i_y-12'd232) >> 2;
    wire [19:0] wire_row_sum;
    reg [9:0] reg_red,reg_green,reg_blue;
    reg [17:0] reg_red_weight,reg_green_weight,reg_blue_weight;
    // 先以拼接扩展位宽，再平衡加法树；保留原有加权寄存级及唯一的最终舍入。
    wire [17:0] wire_red_high={2'd0,reg_red,6'd0}+{5'd0,reg_red,3'd0};
    wire [17:0] wire_red_low={6'd0,reg_red,2'd0}+{8'd0,reg_red};
    wire [17:0] wire_green_high={1'd0,reg_green,7'd0}+{4'd0,reg_green,4'd0};
    wire [17:0] wire_green_low={6'd0,reg_green,2'd0}+{7'd0,reg_green,1'd0};
    wire [17:0] wire_blue_high={4'd0,reg_blue,4'd0}+{5'd0,reg_blue,3'd0};
    wire [17:0] wire_blue_low={6'd0,reg_blue,2'd0}+{8'd0,reg_blue};
    reg [19:0] reg_weighted,reg_previous,reg_previous_delayed,reg_accumulated;
    reg [3:0] reg_valid,reg_first,reg_last,reg_final;
    reg [11:0] reg_address_first,reg_address_second,reg_address_third,reg_address_fourth;
    reg flag_done_o,flag_fault_o;
    wire [20:0] wire_rounded={1'b0,reg_accumulated}+21'd2048;
    // 行缓存仅64项；第一行覆盖旧值，故不复位阵列。
    ball_component_store #(.C_DEPTH(64),.C_ADDR_BITS(6),.C_DATA_BITS(20)) rows_Inst(
        .i_clk(i_clk),.i_read_enable(flag_select),.i_read_address(wire_column),
        .i_write_enable(reg_valid[3] && !i_clear),.i_write_address(reg_address_fourth[5:0]),
        .i_write_data(reg_accumulated),.o_read_data(wire_row_sum));
    assign o_write=reg_valid[3] && reg_last[3] && !flag_bad && !i_clear;
    assign o_address=reg_address_fourth;
    assign o_gray=wire_rounded[19:12];
    assign o_done=flag_done_o;
    assign o_fault=flag_fault_o;
    assign o_sample=cnt_sample;
    assign o_epoch=reg_epoch_o;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_active<=0;flag_bad<=0;cnt_groups<=0;cnt_sample<=0;reg_epoch_o<=0;
            reg_valid<=0;reg_first<=0;reg_last<=0;reg_final<=0;
            reg_red<=0;reg_green<=0;reg_blue<=0;reg_red_weight<=0;reg_green_weight<=0;reg_blue_weight<=0;
            reg_weighted<=0;reg_previous<=0;reg_previous_delayed<=0;reg_accumulated<=0;
            reg_address_first<=0;reg_address_second<=0;reg_address_third<=0;reg_address_fourth<=0;
            flag_done_o<=0;flag_fault_o<=0;
        end else if(i_clear)begin
            flag_active<=0;flag_bad<=0;cnt_groups<=0;reg_valid<=0;reg_final<=0;
            flag_done_o<=0;flag_fault_o<=0;
        end else begin
            flag_done_o<=0;flag_fault_o<=0;
            reg_valid<={reg_valid[2:0],flag_select};
            reg_first<={reg_first[2:0],i_y[1:0] == 0};
            reg_last<={reg_last[2:0],i_y[1:0] == 3};
            reg_final<={reg_final[2:0],flag_select && i_x == 764 && i_y == 487};
            if(i_sof && i_valid)begin
                flag_active<=i_arm;cnt_groups<=0;flag_bad<=0;reg_epoch_o<=i_epoch;
                if(flag_active)begin flag_fault_o<=1;flag_active<=0;cnt_sample<=cnt_sample+1'b1;end
            end
            if(i_error && flag_active)flag_bad<=1;
            if(flag_select)begin
                cnt_groups<=cnt_groups+1'b1;
                reg_red<={2'd0,i_rgb[95:88]}+i_rgb[71:64]+i_rgb[47:40]+i_rgb[23:16];
                reg_green<={2'd0,i_rgb[87:80]}+i_rgb[63:56]+i_rgb[39:32]+i_rgb[15:8];
                reg_blue<={2'd0,i_rgb[79:72]}+i_rgb[55:48]+i_rgb[31:24]+i_rgb[7:0];
                reg_address_first<={wire_row,wire_column};
            end
            if(reg_valid[0])begin
                reg_red_weight<=wire_red_high+wire_red_low;
                reg_green_weight<=wire_green_high+wire_green_low;
                reg_blue_weight<=wire_blue_high+wire_blue_low;
                reg_previous<=reg_first[0] ? 20'd0 : wire_row_sum;
                reg_address_second<=reg_address_first;
            end
            if(reg_valid[1])begin
                reg_weighted<={2'd0,reg_red_weight}+reg_green_weight+reg_blue_weight;
                reg_previous_delayed<=reg_previous;
                reg_address_third<=reg_address_second;
            end
            if(reg_valid[2])begin
                reg_accumulated<=reg_weighted+reg_previous_delayed;reg_address_fourth<=reg_address_third;
            end
            if(reg_valid[3] && reg_final[3])begin
                flag_active<=0;cnt_sample<=cnt_sample+1'b1;
                flag_done_o<=!flag_bad && cnt_groups == 16384;
                flag_fault_o<=flag_bad || cnt_groups != 16384;
            end
            if(i_eof && i_valid && flag_active)begin
                flag_active<=0;flag_fault_o<=1;cnt_sample<=cnt_sample+1'b1;
            end
        end
    end
endmodule
