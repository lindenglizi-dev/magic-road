`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_rotation_angle
// Description: Sixteen-iteration image-coordinate CORDIC phase
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
// 模块名称: ball_rotation_angle
// 模块说明: Sixteen-iteration image-coordinate CORDIC phase
// 仿真工程: sim/tb_ball_rotation_numeric.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_rotation_angle (
    input i_clk, // 向量计算时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 撤销尚未完成的角度
    input i_start, // 空闲时提交相对向量
    input [16-1:0] i_dx, // 有符号Q4水平位移
    input [16-1:0] i_dy, // 有符号Q4垂直位移
    output o_busy, // CORDIC正在迭代
    output o_done, // 本次向量处理结束
    output o_valid, // 非零向量角度有效
    output [16-1:0] o_phase // 65536表示一圈的相位
);

    localparam ST_IDLE=0, ST_ROTATE=1, ST_DONE=2;
    reg [1:0] state_current,state_next;
    reg signed [25:0] reg_vector_x,reg_vector_y;
    reg [15:0] reg_angle,reg_phase_o;
    reg [3:0] cnt_iteration;
    reg [15:0] dec_increment;
    reg flag_valid_o,flag_done_o;
    wire signed [25:0] wire_input_x=$signed({{10{i_dx[15]}},i_dx}) <<< 8;
    wire signed [25:0] wire_input_y=$signed({{10{i_dy[15]}},i_dy}) <<< 8;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin if(i_start)begin state_next=ST_ROTATE;end end
            ST_ROTATE:begin if(cnt_iteration == 15 || !flag_valid_o)begin state_next=ST_DONE;end end
            ST_DONE:begin state_next=ST_IDLE;end
            default:begin state_next=ST_IDLE;end
        endcase
    end
    always @(*)begin
        case(cnt_iteration)
            0:dec_increment=8192;1:dec_increment=4836;2:dec_increment=2555;3:dec_increment=1297;
            4:dec_increment=651;5:dec_increment=326;6:dec_increment=163;7:dec_increment=81;
            8:dec_increment=41;9:dec_increment=20;10:dec_increment=10;11:dec_increment=5;
            12:dec_increment=3;13:dec_increment=1;14:dec_increment=1;default:dec_increment=0;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_vector_x<=0;reg_vector_y<=0;reg_angle<=0;cnt_iteration<=0;
            reg_phase_o<=0;flag_valid_o<=0;flag_done_o<=0;
        end else if(i_clear)begin flag_valid_o<=0;flag_done_o<=0;end
        else begin
            flag_done_o<=0;
            case(state_current)
                ST_IDLE:begin if(i_start)begin
                    reg_vector_x<=i_dx[15] ? -wire_input_x : wire_input_x;
                    reg_vector_y<=i_dx[15] ? -wire_input_y : wire_input_y;
                    reg_angle<=i_dx[15] ? 16'd32768 : 16'd0;cnt_iteration<=0;
                    flag_valid_o<=i_dx != 0 || i_dy != 0;
                end end
                ST_ROTATE:begin
                    cnt_iteration<=cnt_iteration+1'b1;
                    if(reg_vector_y > 0)begin
                        reg_vector_x<=reg_vector_x+(reg_vector_y >>> cnt_iteration);
                        reg_vector_y<=reg_vector_y-(reg_vector_x >>> cnt_iteration);
                        reg_angle<=reg_angle+dec_increment;
                    end else if(reg_vector_y < 0)begin
                        reg_vector_x<=reg_vector_x-(reg_vector_y >>> cnt_iteration);
                        reg_vector_y<=reg_vector_y+(reg_vector_x >>> cnt_iteration);
                        reg_angle<=reg_angle-dec_increment;
                    end
                end
                ST_DONE:begin reg_phase_o<=reg_angle;flag_done_o<=1;end
                default:begin end
            endcase
        end
    end
    assign o_busy=state_current != ST_IDLE;
    assign o_done=flag_done_o;
    assign o_valid=flag_valid_o;
    assign o_phase=reg_phase_o;

endmodule
