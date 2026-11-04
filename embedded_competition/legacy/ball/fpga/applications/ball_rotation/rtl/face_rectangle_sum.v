`timescale 1ns / 1ps
// Integral rectangle reader / 积分图四角串行读取；坐标为半开区间。
module face_rectangle_sum(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [6:0] i_left,
    input [6:0] i_top,
    input [6:0] i_right,
    input [6:0] i_bottom,
    output o_read,
    output [11:0] o_address,
    input [19:0] i_data,
    output o_done,
    output [19:0] o_sum
);
    localparam ST_IDLE=0,ST_ADDRESS=1,ST_READ=2,ST_LOAD=3,ST_ADD=4,ST_DONE=5;
    reg [2:0] state_current,state_next;
    reg [6:0] reg_left,reg_top,reg_right,reg_bottom,reg_x,reg_y;
    reg [1:0] cnt_corner;
    reg signed [22:0] reg_sum;
    reg [19:0] reg_corner;
    reg flag_zero;
    wire [5:0] wire_x=reg_x-1'b1,wire_y=reg_y-1'b1;
    assign o_read=state_current == ST_READ && !flag_zero;
    assign o_address={wire_y,wire_x};
    assign o_sum=reg_sum[19:0];
    assign o_done=state_current == ST_DONE;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_ADDRESS;
            ST_ADDRESS:state_next=ST_READ;
            ST_READ:state_next=ST_LOAD;
            ST_LOAD:state_next=ST_ADD;
            ST_ADD:state_next=cnt_corner == 3 ? ST_DONE : ST_ADDRESS;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_left<=0;reg_top<=0;reg_right<=0;reg_bottom<=0;reg_x<=0;reg_y<=0;
            cnt_corner<=0;reg_sum<=0;reg_corner<=0;flag_zero<=0;
        end else if(!i_clear)begin
            case(state_current)
                ST_IDLE:if(i_start)begin
                    reg_left<=i_left;reg_top<=i_top;reg_right<=i_right;reg_bottom<=i_bottom;
                    cnt_corner<=0;reg_sum<=0;
                end
                ST_ADDRESS:begin
                    reg_x<=cnt_corner[0] ? reg_right : reg_left;
                    reg_y<=cnt_corner[1] ? reg_bottom : reg_top;
                    flag_zero<=(cnt_corner[0] ? reg_right : reg_left) == 0 ||
                        (cnt_corner[1] ? reg_bottom : reg_top) == 0;
                end
                ST_LOAD:reg_corner<=flag_zero ? 20'd0 : i_data;
                ST_ADD:begin
                    if(cnt_corner == 0 || cnt_corner == 3)reg_sum<=reg_sum+$signed({3'b0,reg_corner});
                    else reg_sum<=reg_sum-$signed({3'b0,reg_corner});
                    cnt_corner<=cnt_corner+1'b1;
                end
                default:begin end
            endcase
        end
    end
endmodule
