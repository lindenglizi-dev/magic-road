`timescale 1ns / 1ps
// 顺序double-dabble：每拍处理一个二进制位，像素链不使用除法器。
module ball_decimal_format #(
    parameter C_BITS=32,
    parameter C_DIGITS=10
)(
    input i_clk,
    input i_rstn,
    input i_load,
    input [C_BITS-1:0] i_binary,
    output [C_DIGITS*4-1:0] o_bcd,
    output o_done,
    output o_busy
);
    reg [C_BITS-1:0] reg_binary;
    reg [C_DIGITS*4-1:0] reg_work, reg_adjust;
    reg [C_DIGITS*4-1:0] reg_bcd_o;
    reg [6:0] cnt_bits;
    reg flag_busy_o, flag_done_o;
    integer digit;
    // 各十进制半字节并行加三，移位在时序过程完成。
    always @(*)begin
        reg_adjust=reg_work;
        for(digit=0; digit<C_DIGITS; digit=digit+1)begin
            if(reg_work[digit*4 +: 4] >= 5)begin
                reg_adjust[digit*4 +: 4]=reg_work[digit*4 +: 4]+4'd3;
            end
        end
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_binary<=0; reg_work<=0; reg_bcd_o<=0; cnt_bits<=0; flag_busy_o<=0; flag_done_o<=0;
        end else begin
            flag_done_o<=0;
            if(i_load)begin
                reg_binary<=i_binary; reg_work<=0; cnt_bits<=C_BITS; flag_busy_o<=1;
            end else if(flag_busy_o)begin
                reg_work<={reg_adjust[C_DIGITS*4-2:0],reg_binary[C_BITS-1]};
                reg_binary<=reg_binary << 1;
                cnt_bits<=cnt_bits-1'b1;
                if(cnt_bits == 1)begin
                    reg_bcd_o<={reg_adjust[C_DIGITS*4-2:0],reg_binary[C_BITS-1]};
                    flag_busy_o<=0; flag_done_o<=1;
                end
            end
        end
    end
    assign o_bcd=reg_bcd_o;
    assign o_done=flag_done_o;
    assign o_busy=flag_busy_o;
endmodule
