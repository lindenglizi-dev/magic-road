`timescale 1ns / 1ps
// 中央256x256解锁区；三个新样本通过后在early提交。
module face_gate_control(
    input i_clk,
    input i_rstn,
    input i_early,
    input i_session_clear,
    input i_relock,
    input i_result,
    input i_positive,
    input i_fault,
    input [31:0] i_sample,
    input [15:0] i_result_epoch,
    input [15:0] i_epoch,
    input [2:0] i_result_roi,
    output o_unlocked,
    output o_restart,
    output [1:0] o_confirmed,
    output o_pending,
    output [2:0] o_request_roi,
    output [11:0] o_request_x,
    output o_result_accepted
);
    reg flag_unlocked,flag_pending,flag_seen;
    reg [1:0] cnt_confirmed;
    reg [31:0] reg_last_sample;
    wire signed [31:0] wire_difference=i_sample-reg_last_sample;
    wire flag_fresh=!flag_seen || wire_difference > 0;
    wire flag_result=i_result && !flag_unlocked && i_result_epoch == i_epoch && i_result_roi == 3'd0 && flag_fresh;
    wire flag_cancel=flag_result && (i_fault || !i_positive);
    assign o_request_roi=3'd0;
    assign o_request_x=12'd512;
    assign o_result_accepted=flag_result && !i_relock && !i_session_clear;
    assign o_restart=i_early && flag_pending && !flag_unlocked && !i_relock && !flag_cancel && !i_session_clear;
    assign o_unlocked=flag_unlocked;
    assign o_confirmed=cnt_confirmed;
    assign o_pending=flag_pending;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_unlocked<=0;flag_pending<=0;flag_seen<=0;cnt_confirmed<=0;reg_last_sample<=0;
        end else if(i_relock)begin
            flag_unlocked<=0;flag_pending<=0;flag_seen<=0;cnt_confirmed<=0;
        end else if(o_restart)begin flag_unlocked<=1;flag_pending<=0;end
        else if(i_session_clear && !flag_unlocked)begin flag_pending<=0;cnt_confirmed<=0;end
        else if(flag_result)begin
            flag_seen<=1;reg_last_sample<=i_sample;
            if(i_fault || !i_positive)begin
                cnt_confirmed<=0;flag_pending<=0;
            end
            else if(cnt_confirmed == 2)begin cnt_confirmed<=3;flag_pending<=1;end
            else if(!flag_pending)cnt_confirmed<=cnt_confirmed+1'b1;
        end
    end
endmodule
