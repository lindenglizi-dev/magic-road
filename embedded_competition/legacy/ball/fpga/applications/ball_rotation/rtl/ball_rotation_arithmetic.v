`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_rotation_arithmetic
// Description: Unsigned serial multiply and rounded restoring divide
// Simulations: sim/tb_ball_rotation_numeric.v
// Referrences: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// Dependencies: same-clock synchronous memories
// Version: V1.0
// Revision Date: 2026-10-20
// History: V1.0 Create file
// 版权归属: 用户工程
// 开发人员: Codex
// 创建日期: 2026-10-20
// 设计名称: 带标记小球旋转
// 模块名称: ball_rotation_arithmetic
// 模块说明: Unsigned serial multiply and rounded restoring divide
// 仿真工程: sim/tb_ball_rotation_numeric.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_rotation_arithmetic #(
    parameter C_BITS=96 // 串行寄存器宽度，必须至少为二。
)(
    input i_clk, // 统计运算时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 撤销正在执行的运算
    input i_start, // 空闲时提交运算
    input i_divide, // 为高执行除法，为低执行截断乘法
    input i_round, // 除法按最近整数舍入
    input [C_BITS-1:0] i_left, // 被除数或第一乘数
    input [C_BITS-1:0] i_right, // 除数或第二乘数
    output o_busy, // 正在占用串行运算器
    output o_done, // 结果完成脉冲
    output o_error, // 本次除数为零
    output [C_BITS-1:0] o_result // 无符号结果或低位乘积
);

    localparam ST_IDLE=0, ST_EXECUTE=1, ST_ROUND=2, ST_DONE=3;
    reg [1:0] state_current,state_next;
    reg [C_BITS-1:0] reg_left,reg_right,reg_result_o,reg_product;
    reg [C_BITS:0] reg_remainder;
    reg [$clog2(C_BITS+1)-1:0] cnt_remaining;
    reg flag_divide,flag_round,flag_error_o,flag_done_o;
    wire [C_BITS:0] wire_trial={reg_remainder[C_BITS-1:0],reg_left[C_BITS-1]};
    wire flag_subtract=wire_trial >= {1'b0,reg_right};
    wire [C_BITS:0] wire_difference=wire_trial-{1'b0,reg_right};
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin if(i_start)begin state_next=ST_EXECUTE;end end
            ST_EXECUTE:begin if(cnt_remaining == 1 || flag_error_o)begin state_next=ST_ROUND;end end
            ST_ROUND:begin state_next=ST_DONE;end
            ST_DONE:begin state_next=ST_IDLE;end
            default:begin state_next=ST_IDLE;end
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_left<=0;reg_right<=0;reg_product<=0;reg_remainder<=0;cnt_remaining<=0;
            flag_divide<=0;flag_round<=0;flag_error_o<=0;flag_done_o<=0;reg_result_o<=0;
        end else if(i_clear)begin
            cnt_remaining<=0;flag_done_o<=0;flag_error_o<=0;
        end else begin
            flag_done_o<=0;
            case(state_current)
                ST_IDLE:begin if(i_start)begin
                    reg_left<=i_left;reg_right<=i_right;reg_product<=0;reg_remainder<=0;
                    cnt_remaining<=C_BITS;flag_divide<=i_divide;flag_round<=i_round;
                    flag_error_o<=i_divide && i_right == 0;
                end end
                ST_EXECUTE:begin
                    cnt_remaining<=cnt_remaining-1'b1;
                    if(flag_divide)begin
                        reg_left<={reg_left[C_BITS-2:0],flag_subtract};
                        reg_remainder<=flag_subtract ? wire_difference : wire_trial;
                    end else begin
                        if(reg_right[0])begin reg_product<=reg_product+reg_left;end
                        reg_left<=reg_left << 1;reg_right<=reg_right >> 1;
                    end
                end
                ST_ROUND:begin
                    if(flag_error_o)begin reg_result_o<=0;end
                    else if(flag_divide)begin
                        reg_result_o<=reg_left+((flag_round && (reg_remainder << 1) >= {1'b0,reg_right}) ? 1'b1 : 1'b0);
                    end else begin reg_result_o<=reg_product;end
                end
                ST_DONE:begin flag_done_o<=1;end
                default:begin end
            endcase
        end
    end
    assign o_busy=state_current != ST_IDLE;
    assign o_done=flag_done_o;
    assign o_error=flag_error_o;
    assign o_result=reg_result_o;

endmodule
