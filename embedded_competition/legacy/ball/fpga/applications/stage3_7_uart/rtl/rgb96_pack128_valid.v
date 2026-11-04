`timescale 1ns/1ps
// 连续字节打包：四个96bit有效组转换成三个128bit字；valid空拍保持相位和余数。
// 每行宽度须为16像素倍数，使行末无残留字节。字节顺序与原打包器一致。
module rgb96_pack128_valid(
    input wire I_clk,I_rst_n,
    input wire [95:0] I_rgb,
    input wire I_valid,I_user,I_last,I_done,
    output reg [127:0] O_data,
    output reg O_valid,O_last,O_done,O_error
);
    reg [95:0] S_prev; // 上一个有效96bit组，空拍保持，供下一字补齐。
    reg [1:0] S_phase; // 当前组在四有效组中的编号，不按墙上时钟计数。
    wire [1:0] S_phase_now=I_user?2'd0:S_phase; // 帧首可与首组同拍。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n)begin
            S_prev<=0;S_phase<=0;O_data<=0;O_valid<=0;O_last<=0;O_done<=0;O_error<=0;
        end else begin
            O_data<=0;O_valid<=0;O_last<=0;O_done<=0;
            if(I_user)begin S_phase<=0;S_prev<=0;end
            if(I_valid)begin
                S_prev<=I_rgb;
                S_phase<=S_phase_now+2'd1;
                case(S_phase_now)
                    2'd0:begin end // 只有12字节，先存住，不输出16字节。
                    2'd1:begin O_data<={S_prev,I_rgb[95:64]};O_valid<=1;end
                    2'd2:begin O_data<={S_prev[63:0],I_rgb[95:32]};O_valid<=1;end
                    2'd3:begin O_data<={S_prev[31:0],I_rgb};O_valid<=1;end
                endcase
                if(I_last || I_done)begin
                    if(S_phase_now!=2'd3)O_error<=1; // 本配置的行/帧末必须正好填完打包组。
                    else begin O_last<=I_last;O_done<=I_done;end
                end
            end
        end
    end
endmodule
