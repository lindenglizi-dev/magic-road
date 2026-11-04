`timescale 1ns / 1ps
// Bounded divider / 20拍无符号恢复除法，调用方保证分母非零。
module face_unsigned_divide(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [19:0] i_numerator,
    input [8:0] i_denominator,
    output o_done,
    output [19:0] o_quotient
);
    localparam ST_IDLE=0,ST_DIVIDE=1,ST_DONE=2;
    reg [1:0] state_current,state_next;
    reg [19:0] reg_quotient;
    reg [9:0] reg_remainder;
    reg [8:0] reg_denominator;
    reg [4:0] cnt_bit;
    wire [9:0] wire_shifted={reg_remainder[8:0],reg_quotient[19]};
    wire flag_subtract=wire_shifted >= {1'b0,reg_denominator};
    assign o_done=state_current == ST_DONE;
    assign o_quotient=reg_quotient;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_DIVIDE;
            ST_DIVIDE:if(cnt_bit == 19)state_next=ST_DONE;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_quotient<=0;reg_remainder<=0;reg_denominator<=1;cnt_bit<=0;end
        else if(!i_clear)begin
            if(state_current == ST_IDLE && i_start)begin
                reg_quotient<=i_numerator;reg_remainder<=0;reg_denominator<=i_denominator;cnt_bit<=0;
            end else if(state_current == ST_DIVIDE)begin
                reg_remainder<=flag_subtract ? wire_shifted-reg_denominator : wire_shifted;
                reg_quotient<={reg_quotient[18:0],flag_subtract};cnt_bit<=cnt_bit+1'b1;
            end
        end
    end
endmodule
