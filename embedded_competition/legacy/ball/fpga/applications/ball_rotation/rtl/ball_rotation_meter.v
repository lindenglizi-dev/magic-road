`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_rotation_meter
// Description: Frame-timestamped integer least-squares RPM and directional turns
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
// 模块名称: ball_rotation_meter
// 模块说明: Frame-timestamped integer least-squares RPM and directional turns
// 仿真工程: sim/tb_ball_rotation_numeric.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_rotation_meter #(
    parameter C_CLOCK_HZ=103520000, C_MAX_RPM=120 // 时钟标定与已知转速上界。
)(
    input i_clk, // 串行统计时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 清除旋转参考及圈数
    input i_fault, // 失效闭锁并冻结已有圈数
    input i_start, // 空闲时提交一帧观测
    input i_valid, // 本帧相位有效
    input i_new_target, // 该事务建立新的目标参考
    input [16-1:0] i_phase, // 图像内顺时针圈相位
    input [64-1:0] i_tick, // 源帧SOF时间戳
    output o_busy, // 统计事务尚未完成
    output o_done, // 整包统计结果完成
    output o_angle_valid, // 本帧角度有效
    output [16-1:0] o_phase, // 本帧冻结相位
    output o_rpm_valid, // 历史窗口足以测量转速
    output [24-1:0] o_rpm, // 有符号转速，单位零点一RPM
    output [3-1:0] o_status, // 等待采集预热顺转逆转停止丢失故障
    output [48-1:0] o_net, // 有符号累计相位
    output [32-1:0] o_cw, // 连续顺转段完成整圈数
    output [32-1:0] o_ccw, // 连续逆转段完成整圈数
    output o_partial, // 观测曾经不连续
    output o_saturated, // 整圈计数达到上限
    output o_fault // 时间或数值合同失效
);
    localparam ST_IDLE=0;
    localparam ST_PREPARE=1;
    localparam ST_TIME=2;
    localparam ST_DELTA=3;
    localparam ST_CLASSIFY=4;
    localparam ST_GUARD_LEFT=5;
    localparam ST_GUARD_LEFT_WAIT=6;
    localparam ST_GUARD_RIGHT=7;
    localparam ST_GUARD_RIGHT_WAIT=8;
    localparam ST_MISSING=9;
    localparam ST_REBASE=10;
    localparam ST_ACCUMULATE=11;
    localparam ST_DIRECTION=12;
    localparam ST_EXTREME=13;
    localparam ST_TURNS=14;
    localparam ST_COUNT=15;
    localparam ST_REVERSE=16;
    localparam ST_SAVE=17;
    localparam ST_OLDEST_READ=18;
    localparam ST_OLDEST_TEST=19;
    localparam ST_APPEND=20;
    localparam ST_BASE_READ=21;
    localparam ST_BASE_TEST=22;
    localparam ST_HISTORY_READ=23;
    localparam ST_HISTORY_LOAD=24;
    localparam ST_HISTORY_CHECK=25;
    localparam ST_SQUARE=26;
    localparam ST_SQUARE_WAIT=27;
    localparam ST_CROSS=28;
    localparam ST_CROSS_WAIT=29;
    localparam ST_NUM_FIRST=30;
    localparam ST_NUM_FIRST_WAIT=31;
    localparam ST_NUM_SECOND=32;
    localparam ST_NUM_SECOND_WAIT=33;
    localparam ST_DEN_FIRST=34;
    localparam ST_DEN_FIRST_WAIT=35;
    localparam ST_DEN_SECOND=36;
    localparam ST_DEN_SECOND_WAIT=37;
    localparam ST_SCALE=38;
    localparam ST_SCALE_WAIT=39;
    localparam ST_DIVIDE=40;
    localparam ST_DIVIDE_WAIT=41;
    localparam ST_BAD=42;
    localparam ST_DONE=43;

    localparam [63:0] C_GAP_LIMIT=(64'd25*C_CLOCK_HZ+C_MAX_RPM-1)/C_MAX_RPM;
    localparam [63:0] C_WINDOW_TICKS=64'd3*C_CLOCK_HZ/10;
    reg [5:0] state_current,state_next;
    reg [15:0] reg_input_phase,reg_previous_phase,reg_phase_o;
    reg [63:0] reg_input_tick,reg_previous_tick,reg_last_tick,reg_delta_tick;
    reg signed [15:0] reg_delta_phase;
    reg [16:0] reg_absolute_delta;
    reg flag_input_valid,flag_new_target,flag_previous,flag_last,flag_restart;
    reg signed [47:0] reg_net_o,reg_anchor,reg_extreme;
    reg signed [1:0] reg_direction;
    reg [31:0] reg_segment_turns,reg_turns,reg_cw_o,reg_ccw_o;
    reg [2:0] reg_status_o;
    reg [23:0] reg_rpm_o;
    reg flag_done_o,flag_angle_valid_o,flag_rpm_valid_o,flag_partial_o,flag_saturated_o,flag_fault_o;
    reg [63:0] mem_ticks[0:31];
    reg signed [47:0] mem_phases[0:31];
    reg [4:0] cnt_head,cnt_tail,cnt_index;
    reg [5:0] cnt_history,cnt_processed;
    reg [63:0] reg_history_tick,reg_base_tick,reg_relative_tick;
    reg signed [47:0] reg_history_phase,reg_base_phase,reg_relative_phase;
    reg [63:0] reg_sum_time,reg_sum_square,reg_denominator;
    reg signed [63:0] reg_sum_phase,reg_sum_cross,reg_product,reg_numerator;
    reg [95:0] reg_math_left,reg_math_right,reg_guard_left,reg_scaled;
    reg flag_math_start,reg_math_divide,reg_math_round;
    wire flag_math_done,flag_math_error;
    wire [95:0] wire_math_result;
    wire [63:0] wire_relative_tick=reg_history_tick-reg_base_tick;
    wire [47:0] reg_anchor_distance=reg_net_o >= reg_anchor ? reg_net_o-reg_anchor : reg_anchor-reg_net_o;
    wire [47:0] wire_segment_distance=reg_extreme >= reg_anchor ? reg_extreme-reg_anchor : reg_anchor-reg_extreme;
    wire [31:0] wire_increment=reg_turns-reg_segment_turns;
    wire [32:0] wire_cw_sum={1'b0,reg_cw_o}+{1'b0,wire_increment};
    wire [32:0] wire_ccw_sum={1'b0,reg_ccw_o}+{1'b0,wire_increment};
    ball_rotation_arithmetic #(.C_BITS(96)) arithmetic_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear || i_fault),.i_start(flag_math_start),
        .i_divide(reg_math_divide),.i_round(reg_math_round),.i_left(reg_math_left),.i_right(reg_math_right),
        .o_busy(),.o_done(flag_math_done),.o_error(flag_math_error),.o_result(wire_math_result));

    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear || i_fault)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin if(i_start)begin state_next=ST_PREPARE;end end
            ST_PREPARE:begin state_next=ST_TIME; end
            ST_TIME:begin if(flag_last && reg_input_tick <= reg_last_tick)begin state_next=ST_BAD;end else begin state_next=ST_DELTA;end end
            ST_DELTA:begin state_next=ST_CLASSIFY; end
            ST_CLASSIFY:begin if(!flag_input_valid)begin state_next=ST_MISSING;end
else if(!flag_previous)begin state_next=ST_SAVE;end
else if(reg_delta_tick > C_CLOCK_HZ/4 || reg_delta_tick >= C_GAP_LIMIT)begin state_next=ST_REBASE;end
else if(reg_absolute_delta <= 729)begin state_next=ST_ACCUMULATE;end
else begin state_next=ST_GUARD_LEFT;end end
            ST_GUARD_LEFT:begin state_next=ST_GUARD_LEFT_WAIT; end
            ST_GUARD_LEFT_WAIT:begin if(flag_math_done)begin state_next=ST_GUARD_RIGHT;end end
            ST_GUARD_RIGHT:begin state_next=ST_GUARD_RIGHT_WAIT; end
            ST_GUARD_RIGHT_WAIT:begin if(flag_math_done)begin
    if(reg_guard_left > wire_math_result)begin state_next=ST_REBASE;end
    else begin state_next=ST_ACCUMULATE;end
end end
            ST_MISSING:begin state_next=ST_DONE; end
            ST_REBASE:begin state_next=ST_SAVE; end
            ST_ACCUMULATE:begin state_next=ST_DIRECTION; end
            ST_DIRECTION:begin if(reg_direction == 0 && reg_anchor_distance < 48'd1456)begin state_next=ST_SAVE;end
else begin state_next=ST_EXTREME;end end
            ST_EXTREME:begin state_next=ST_TURNS; end
            ST_TURNS:begin state_next=ST_COUNT; end
            ST_COUNT:begin state_next=ST_REVERSE; end
            ST_REVERSE:begin state_next=ST_SAVE; end
            ST_SAVE:begin if(cnt_history == 0)begin state_next=ST_APPEND;end else begin state_next=ST_OLDEST_READ;end end
            ST_OLDEST_READ:begin state_next=ST_OLDEST_TEST; end
            ST_OLDEST_TEST:begin if((cnt_history >= 4 && reg_input_tick-reg_history_tick > C_WINDOW_TICKS) || cnt_history == 32)begin
    state_next=ST_OLDEST_READ;
end else begin state_next=ST_APPEND;end end
            ST_APPEND:begin state_next=ST_BASE_READ; end
            ST_BASE_READ:begin state_next=ST_BASE_TEST; end
            ST_BASE_TEST:begin if(cnt_history >= 4 && reg_input_tick-reg_history_tick >= C_CLOCK_HZ/10)begin state_next=ST_HISTORY_READ;end
else begin state_next=ST_DONE;end end
            ST_HISTORY_READ:begin state_next=ST_HISTORY_LOAD; end
            ST_HISTORY_LOAD:begin state_next=ST_HISTORY_CHECK; end
            ST_HISTORY_CHECK:begin if(|reg_relative_tick[63:18] || reg_relative_phase[47:19] != {29{reg_relative_phase[19]}})begin
    state_next=ST_BAD;
end else begin state_next=ST_SQUARE;end end
            ST_SQUARE:begin state_next=ST_SQUARE_WAIT; end
            ST_SQUARE_WAIT:begin if(flag_math_done)begin state_next=ST_CROSS;end end
            ST_CROSS:begin state_next=ST_CROSS_WAIT; end
            ST_CROSS_WAIT:begin if(flag_math_done)begin
    if(cnt_processed+1 == cnt_history)begin state_next=ST_NUM_FIRST;end
    else begin state_next=ST_HISTORY_READ;end
end end
            ST_NUM_FIRST:begin state_next=ST_NUM_FIRST_WAIT; end
            ST_NUM_FIRST_WAIT:begin if(flag_math_done)begin state_next=ST_NUM_SECOND;end end
            ST_NUM_SECOND:begin state_next=ST_NUM_SECOND_WAIT; end
            ST_NUM_SECOND_WAIT:begin if(flag_math_done)begin state_next=ST_DEN_FIRST;end end
            ST_DEN_FIRST:begin state_next=ST_DEN_FIRST_WAIT; end
            ST_DEN_FIRST_WAIT:begin if(flag_math_done)begin state_next=ST_DEN_SECOND;end end
            ST_DEN_SECOND:begin state_next=ST_DEN_SECOND_WAIT; end
            ST_DEN_SECOND_WAIT:begin if(flag_math_done)begin state_next=ST_SCALE;end end
            ST_SCALE:begin if(reg_denominator == 0)begin state_next=ST_BAD;end else begin state_next=ST_SCALE_WAIT;end end
            ST_SCALE_WAIT:begin if(flag_math_done)begin state_next=ST_DIVIDE;end end
            ST_DIVIDE:begin state_next=ST_DIVIDE_WAIT; end
            ST_DIVIDE_WAIT:begin if(flag_math_done)begin
    if(flag_math_error || |wire_math_result[95:23])begin state_next=ST_BAD;end
    else begin state_next=ST_DONE;end
end end
            ST_BAD:begin state_next=ST_DONE; end
            ST_DONE:begin state_next=ST_IDLE; end
            default:begin state_next=ST_IDLE;end
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_input_phase<=0;reg_previous_phase<=0;reg_phase_o<=0;reg_input_tick<=0;reg_previous_tick<=0;
            reg_last_tick<=0;reg_delta_tick<=0;reg_delta_phase<=0;reg_absolute_delta<=0;
            flag_input_valid<=0;flag_new_target<=0;flag_previous<=0;flag_last<=0;flag_restart<=0;
            reg_net_o<=0;reg_anchor<=0;reg_extreme<=0;reg_direction<=0;reg_segment_turns<=0;reg_turns<=0;
            reg_cw_o<=0;reg_ccw_o<=0;reg_status_o<=0;reg_rpm_o<=0;
            flag_done_o<=0;flag_angle_valid_o<=0;flag_rpm_valid_o<=0;flag_partial_o<=0;flag_saturated_o<=0;flag_fault_o<=0;
            cnt_head<=0;cnt_tail<=0;cnt_index<=0;cnt_history<=0;cnt_processed<=0;
            reg_history_tick<=0;reg_base_tick<=0;reg_relative_tick<=0;reg_history_phase<=0;reg_base_phase<=0;reg_relative_phase<=0;
            reg_sum_time<=0;reg_sum_square<=0;reg_denominator<=0;reg_sum_phase<=0;reg_sum_cross<=0;reg_product<=0;reg_numerator<=0;
            reg_math_left<=0;reg_math_right<=0;reg_guard_left<=0;reg_scaled<=0;
            flag_math_start<=0;reg_math_divide<=0;reg_math_round<=0;
        end else if(i_clear)begin
            flag_previous<=0;flag_last<=0;reg_net_o<=0;reg_anchor<=0;reg_extreme<=0;reg_direction<=0;
            reg_segment_turns<=0;reg_cw_o<=0;reg_ccw_o<=0;reg_status_o<=0;reg_rpm_o<=0;
            flag_done_o<=0;flag_angle_valid_o<=0;flag_rpm_valid_o<=0;flag_partial_o<=0;flag_saturated_o<=0;flag_fault_o<=0;
            cnt_head<=0;cnt_tail<=0;cnt_history<=0;flag_math_start<=0;
        end else if(i_fault)begin
            flag_previous<=0;cnt_history<=0;cnt_head<=0;cnt_tail<=0;flag_math_start<=0;
            flag_rpm_valid_o<=0;flag_angle_valid_o<=0;flag_partial_o<=1;flag_fault_o<=1;flag_done_o<=0;reg_status_o<=7;
        end else begin
            flag_done_o<=0;flag_math_start<=0;
            case(state_current)
                ST_IDLE:begin
if(i_start)begin
    reg_input_phase<=i_phase;reg_input_tick<=i_tick;
    flag_input_valid<=i_valid;flag_new_target<=i_new_target;
end
                end
                ST_PREPARE:begin
flag_rpm_valid_o<=0;flag_angle_valid_o<=flag_input_valid;
flag_restart<=!flag_previous || flag_new_target;
flag_fault_o<=0;
if(flag_new_target)begin
    flag_previous<=0;flag_last<=0;reg_net_o<=0;reg_anchor<=0;reg_extreme<=0;
    reg_direction<=0;reg_segment_turns<=0;reg_cw_o<=0;reg_ccw_o<=0;
    flag_partial_o<=0;flag_saturated_o<=0;cnt_history<=0;cnt_head<=0;cnt_tail<=0;
end
                end
                ST_TIME:begin
reg_delta_tick<=reg_input_tick-reg_previous_tick;
reg_delta_phase<=$signed(reg_input_phase-reg_previous_phase);
reg_last_tick<=reg_input_tick;flag_last<=1;reg_phase_o<=reg_input_phase;
                end
                ST_DELTA:begin
reg_absolute_delta<=reg_delta_phase < 0 ? -{reg_delta_phase[15],reg_delta_phase} : {1'b0,reg_delta_phase};
                end
                ST_GUARD_LEFT:begin
reg_math_left<=reg_absolute_delta-17'd729;
reg_math_right<=64'd60*C_CLOCK_HZ;reg_math_divide<=0;reg_math_round<=0;flag_math_start<=1;
                end
                ST_GUARD_LEFT_WAIT:begin
if(flag_math_done)begin reg_guard_left<=wire_math_result;end
                end
                ST_GUARD_RIGHT:begin
reg_math_left<=reg_delta_tick;
reg_math_right<=64'd65536*C_MAX_RPM;flag_math_start<=1;
                end
                ST_MISSING:begin
reg_status_o<=3'd6;
if(flag_previous && (reg_delta_tick > C_CLOCK_HZ/4 || reg_delta_tick >= C_GAP_LIMIT))begin flag_partial_o<=1;end
                end
                ST_REBASE:begin
flag_partial_o<=1;flag_restart<=1;cnt_history<=0;cnt_head<=0;cnt_tail<=0;
reg_direction<=0;reg_segment_turns<=0;reg_anchor<=reg_net_o;reg_extreme<=reg_net_o;
                end
                ST_ACCUMULATE:begin
reg_net_o<=reg_net_o+{{32{reg_delta_phase[15]}},reg_delta_phase};
                end
                ST_DIRECTION:begin
if(reg_direction == 0 && reg_anchor_distance >= 48'd1456)begin reg_direction<=reg_net_o >= reg_anchor ? 2'sd1 : -2'sd1;end
                end
                ST_EXTREME:begin
if(reg_direction > 0 && reg_net_o > reg_extreme)begin reg_extreme<=reg_net_o;end
else if(reg_direction < 0 && reg_net_o < reg_extreme)begin reg_extreme<=reg_net_o;end
                end
                ST_TURNS:begin
reg_turns<=wire_segment_distance[47:16];
                end
                ST_COUNT:begin
reg_segment_turns<=reg_turns;
if(reg_direction > 0)begin
    if(wire_cw_sum[32])begin reg_cw_o<=32'hffffffff;flag_saturated_o<=1;flag_partial_o<=1;end
    else begin reg_cw_o<=wire_cw_sum[31:0];end
end else begin
    if(wire_ccw_sum[32])begin reg_ccw_o<=32'hffffffff;flag_saturated_o<=1;flag_partial_o<=1;end
    else begin reg_ccw_o<=wire_ccw_sum[31:0];end
end
                end
                ST_REVERSE:begin
if((reg_direction > 0 && reg_extreme-reg_net_o > 48'sd1456) ||
   (reg_direction < 0 && reg_net_o-reg_extreme > 48'sd1456))begin
    reg_anchor<=reg_extreme;reg_extreme<=reg_net_o;reg_direction<=-reg_direction;reg_segment_turns<=0;
end
                end
                ST_SAVE:begin
reg_previous_phase<=reg_input_phase;reg_previous_tick<=reg_input_tick;flag_previous<=1;
reg_status_o<=flag_restart ? 3'd1 : 3'd2;
                end
                ST_OLDEST_READ:begin
reg_history_tick<=mem_ticks[cnt_head];reg_history_phase<=mem_phases[cnt_head];
                end
                ST_OLDEST_TEST:begin
if((cnt_history >= 4 && reg_input_tick-reg_history_tick > C_WINDOW_TICKS) || cnt_history == 32)begin
    cnt_head<=cnt_head+1'b1;cnt_history<=cnt_history-1'b1;
end
                end
                ST_APPEND:begin
mem_ticks[cnt_tail]<=reg_input_tick;mem_phases[cnt_tail]<=reg_net_o;
cnt_tail<=cnt_tail+1'b1;cnt_history<=cnt_history+1'b1;
                end
                ST_BASE_READ:begin
reg_history_tick<=mem_ticks[cnt_head];reg_history_phase<=mem_phases[cnt_head];
                end
                ST_BASE_TEST:begin
reg_base_tick<=reg_history_tick;reg_base_phase<=reg_history_phase;
cnt_index<=cnt_head;cnt_processed<=0;reg_sum_time<=0;reg_sum_phase<=0;reg_sum_square<=0;reg_sum_cross<=0;
                end
                ST_HISTORY_READ:begin
reg_history_tick<=mem_ticks[cnt_index];reg_history_phase<=mem_phases[cnt_index];
                end
                ST_HISTORY_LOAD:begin
reg_relative_tick<=wire_relative_tick >> 10;
reg_relative_phase<=reg_history_phase-reg_base_phase;
                end
                ST_HISTORY_CHECK:begin
reg_sum_time<=reg_sum_time+reg_relative_tick;
reg_sum_phase<=reg_sum_phase+reg_relative_phase;
                end
                ST_SQUARE:begin
reg_math_left<=reg_relative_tick;reg_math_right<=reg_relative_tick;
reg_math_divide<=0;flag_math_start<=1;
                end
                ST_SQUARE_WAIT:begin
if(flag_math_done)begin reg_sum_square<=reg_sum_square+wire_math_result[63:0];end
                end
                ST_CROSS:begin
reg_math_left<=reg_relative_tick;reg_math_right<={{48{reg_relative_phase[47]}},reg_relative_phase};flag_math_start<=1;
                end
                ST_CROSS_WAIT:begin
if(flag_math_done)begin
    reg_sum_cross<=reg_sum_cross+$signed(wire_math_result[63:0]);
    cnt_processed<=cnt_processed+1'b1;cnt_index<=cnt_index+1'b1;
end
                end
                ST_NUM_FIRST:begin
reg_math_left<=cnt_history;
reg_math_right<={{32{reg_sum_cross[63]}},reg_sum_cross};flag_math_start<=1;
                end
                ST_NUM_FIRST_WAIT:begin
if(flag_math_done)begin reg_product<=wire_math_result[63:0];end
                end
                ST_NUM_SECOND:begin
reg_math_left<=reg_sum_time;
reg_math_right<={{32{reg_sum_phase[63]}},reg_sum_phase};flag_math_start<=1;
                end
                ST_NUM_SECOND_WAIT:begin
if(flag_math_done)begin reg_numerator<=reg_product-$signed(wire_math_result[63:0]);end
                end
                ST_DEN_FIRST:begin
reg_math_left<=cnt_history;reg_math_right<=reg_sum_square;flag_math_start<=1;
                end
                ST_DEN_FIRST_WAIT:begin
if(flag_math_done)begin reg_product<=wire_math_result[63:0];end
                end
                ST_DEN_SECOND:begin
reg_math_left<=reg_sum_time;reg_math_right<=reg_sum_time;flag_math_start<=1;
                end
                ST_DEN_SECOND_WAIT:begin
if(flag_math_done)begin reg_denominator<=reg_product-wire_math_result[63:0];end
                end
                ST_SCALE:begin
reg_math_left<=reg_numerator < 0 ? -reg_numerator : reg_numerator;
reg_math_right<=64'd600*C_CLOCK_HZ;flag_math_start<=1;
                end
                ST_SCALE_WAIT:begin
if(flag_math_done)begin reg_scaled<=wire_math_result;end
                end
                ST_DIVIDE:begin
reg_math_left<=reg_scaled;reg_math_right<={reg_denominator,26'd0};
reg_math_divide<=1;reg_math_round<=1;flag_math_start<=1;
                end
                ST_DIVIDE_WAIT:begin
if(flag_math_done)begin
    reg_rpm_o<=reg_numerator < 0 ? -wire_math_result[23:0] : wire_math_result[23:0];
    flag_rpm_valid_o<=1;
    if(wire_math_result < 20)begin reg_status_o<=3'd5;end
    else begin reg_status_o<=reg_numerator < 0 ? 3'd4 : 3'd3;end
end
                end
                ST_BAD:begin
flag_partial_o<=1;flag_fault_o<=1;flag_rpm_valid_o<=0;flag_angle_valid_o<=0;
flag_previous<=0;cnt_history<=0;cnt_head<=0;cnt_tail<=0;reg_status_o<=3'd7;
                end
                ST_DONE:begin
flag_done_o<=1;
                end
                default:begin end
            endcase
        end
    end
    assign o_busy=state_current != ST_IDLE;
    assign o_done=flag_done_o;
    assign o_angle_valid=flag_angle_valid_o;
    assign o_phase=reg_phase_o;
    assign o_rpm_valid=flag_rpm_valid_o;
    assign o_rpm=reg_rpm_o;
    assign o_status=reg_status_o;
    assign o_net=reg_net_o;
    assign o_cw=reg_cw_o;
    assign o_ccw=reg_ccw_o;
    assign o_partial=flag_partial_o;
    assign o_saturated=flag_saturated_o;
    assign o_fault=flag_fault_o;

endmodule
