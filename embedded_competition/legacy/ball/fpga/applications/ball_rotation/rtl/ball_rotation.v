`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_rotation
// Description: Frame-ordered dual-bank marker and rotation transaction controller
// Simulations: sim/tb_ball_rotation_runtime.v
// Referrences: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// Dependencies: same-clock synchronous memories
// Version: V1.0
// Revision Date: 2026-10-20
// History: V1.0 Create file
// 版权归属: 用户工程
// 开发人员: Codex
// 创建日期: 2026-10-20
// 设计名称: 带标记小球旋转
// 模块名称: ball_rotation
// 模块说明: Frame-ordered dual-bank marker and rotation transaction controller
// 仿真工程: sim/tb_ball_rotation_runtime.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_rotation #(
    parameter C_WIDTH=1280,C_HEIGHT=720,
    parameter C_X_MIN=64,C_Y_MIN=160,C_X_END=1216,C_Y_END=640,
    parameter C_CLOCK_HZ=103520000,C_MAX_RPM=120 // 保留源时钟与先验上界。
)(
    input i_clk, // 像素组与统计共用时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 清除旋转会话
    input i_fault, // 颜色支路故障闭锁
    input i_enable, // 追踪模式且门禁已解锁
    input [96-1:0] i_rgb, // 原始四像素RGB旁路
    input i_valid, // 有效像素组
    input i_sof, // 首个有效像素组
    input [12-1:0] i_x, // 当前横坐标
    input [12-1:0] i_y, // 当前纵坐标
    input [32-1:0] i_frame, // 源帧编号
    input [64-1:0] i_tick, // 该源帧采集时刻
    input [16-1:0] i_epoch, // 当前配置代次
    input i_observation_done, // 当前组件帧已完成目标选择
    input i_observation_valid, // 本帧有实测球而非漏检保留
    input i_observation_new, // 新目标首帧
    input [32-1:0] i_observation_frame, // 实测球所属源帧
    input [64-1:0] i_observation_tick, // 实测源帧采集时间
    input [16-1:0] i_observation_epoch, // 实测帧配置代次
    input [12-1:0] i_left, // 实测左边界
    input [12-1:0] i_right, // 实测右边界
    input [12-1:0] i_top, // 实测上边界
    input [12-1:0] i_bottom, // 实测下边界
    input i_predict_valid, // 预测框仍有效
    input [12-1:0] i_predict_x, // 用于未来采集窗的预测中心
    input [12-1:0] i_predict_y, // 用于未来采集窗的预测纵坐标
    output o_done, // 带源帧号的结果完成脉冲
    output [32-1:0] o_frame, // 统计结果源帧号
    output [16-1:0] o_epoch, // 统计结果配置代次
    output o_angle_valid, // 相位有效
    output [16-1:0] o_phase, // 65536一圈的冻结相位
    output o_rpm_valid, // 转速窗口有效
    output [24-1:0] o_rpm, // 有符号零点一RPM
    output [3-1:0] o_status, // 旋转统计状态
    output [48-1:0] o_net, // 有符号累计圈相位
    output [32-1:0] o_cw, // 顺转整圈累计
    output [32-1:0] o_ccw, // 逆转整圈累计
    output o_partial, // 存在未能观测的时段
    output o_saturated, // 整圈计数已饱和
    output [4-1:0] o_reason, // 本次测量拒绝原因
    output o_fault, // 旋转支路失效闭锁
    output [2-1:0] o_bank_busy, // 缓存所有权诊断
    output [8-1:0] o_median, // 当前实测球内中位亮度
    output [8-1:0] o_threshold // 当前黑点阈值
);

    localparam ST_IDLE=0,ST_FETCH=1,ST_SELECT=2,ST_MARKER_START=3,ST_MARKER_WAIT=4,
        ST_ANGLE_START=5,ST_ANGLE_WAIT=6,ST_METER_START=7,ST_METER_WAIT=8,ST_COMMIT=9;
    reg [3:0] state_current,state_next;
    reg [161:0] mem_jobs[0:3];
    reg [161:0] reg_job;
    reg [1:0] cnt_head,cnt_tail;
    reg [2:0] cnt_jobs;
    reg flag_fault_o,flag_window_valid,flag_marker_start,flag_angle_start,flag_meter_start;
    reg [11:0] reg_window_x,reg_window_y;
    reg [1:0] reg_release;
    reg [15:0] reg_phase,reg_dx,reg_dy;
    reg flag_phase_valid,flag_done_o;
    reg [3:0] reg_reason_o;
    reg [31:0] reg_frame_o;
    reg [15:0] reg_epoch_o;
    wire [15:0] wire_job_epoch;
    wire [31:0] wire_job_frame;
    wire [63:0] wire_job_tick;
    wire flag_job_new,flag_job_valid;
    wire [11:0] wire_job_left,wire_job_right,wire_job_top,wire_job_bottom;
    wire flag_enqueue=i_observation_done && i_enable && !flag_fault_o;
    wire flag_dequeue=state_current == ST_FETCH;
    wire [1:0] wire_bank_busy,wire_bank_ready;
    wire [63:0] wire_frames;
    wire [127:0] wire_ticks;
    wire [31:0] wire_epochs;
    wire [23:0] wire_origins_x,wire_origins_y;
    wire flag_bank=wire_job_frame[0];
    wire flag_match=wire_bank_busy[flag_bank] && wire_frames[flag_bank*32 +:32] == wire_job_frame &&
        wire_ticks[flag_bank*64 +:64] == wire_job_tick && wire_epochs[flag_bank*16 +:16] == wire_job_epoch;
    wire flag_complete=wire_bank_ready[flag_bank];
    wire flag_gray_read,flag_marker_done,flag_marker_valid,flag_angle_done,flag_angle_valid,flag_meter_done;
    wire flag_meter_rpm_valid,flag_meter_angle_valid,flag_meter_partial,flag_meter_saturated,flag_meter_fault;
    wire [12:0] wire_gray_address;
    wire [15:0] wire_gray_data,wire_center_x,wire_center_y,wire_marker_x,wire_marker_y,wire_angle,wire_meter_phase;
    wire [3:0] wire_marker_reason;
    wire [23:0] wire_meter_rpm;
    wire [2:0] wire_meter_status;
    wire [47:0] wire_meter_net;
    wire [31:0] wire_meter_cw,wire_meter_ccw;
    wire flag_abort=i_clear || !i_enable || flag_fault_o;
    assign {wire_job_epoch,wire_job_frame,wire_job_tick,flag_job_new,flag_job_valid,
            wire_job_left,wire_job_right,wire_job_top,wire_job_bottom}=reg_job;
    ball_rotation_capture capture_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),.i_enable(i_enable),
        .i_rgb(i_rgb),.i_valid(i_valid),.i_sof(i_sof),.i_x(i_x),.i_y(i_y),.i_frame(i_frame),.i_tick(i_tick),.i_epoch(i_epoch),
        .i_window_valid(flag_window_valid),.i_window_x(reg_window_x),.i_window_y(reg_window_y),.i_release(reg_release),
        .i_read(flag_gray_read),.i_read_bank(flag_bank),.i_read_address(wire_gray_address),.o_read_data(wire_gray_data),
        .o_busy(wire_bank_busy),.o_ready(wire_bank_ready),.o_frames(wire_frames),.o_ticks(wire_ticks),.o_epochs(wire_epochs),
        .o_origins_x(wire_origins_x),.o_origins_y(wire_origins_y),.o_overrun());
    ball_marker_extract #(.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_X_END(C_X_END),.C_Y_END(C_Y_END)) marker_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),.i_start(flag_marker_start),
        .i_origin_x(wire_origins_x[flag_bank*12 +:12]),.i_origin_y(wire_origins_y[flag_bank*12 +:12]),
        .i_left(wire_job_left),.i_right(wire_job_right),.i_top(wire_job_top),.i_bottom(wire_job_bottom),
        .i_read_data(wire_gray_data),.o_read(flag_gray_read),.o_read_address(wire_gray_address),.o_busy(),
        .o_done(flag_marker_done),.o_valid(flag_marker_valid),.o_reason(wire_marker_reason),
        .o_center_x(wire_center_x),.o_center_y(wire_center_y),.o_marker_x(wire_marker_x),.o_marker_y(wire_marker_y),
        .o_median(o_median),.o_threshold(o_threshold));
    ball_rotation_angle angle_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),.i_start(flag_angle_start),
        .i_dx(reg_dx),.i_dy(reg_dy),.o_busy(),.o_done(flag_angle_done),.o_valid(flag_angle_valid),.o_phase(wire_angle));
    ball_rotation_meter #(.C_CLOCK_HZ(C_CLOCK_HZ),.C_MAX_RPM(C_MAX_RPM)) meter_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear || !i_enable),.i_fault(flag_fault_o),.i_start(flag_meter_start),
        .i_valid(flag_phase_valid),.i_new_target(flag_job_new),.i_phase(reg_phase),.i_tick(wire_job_tick),
        .o_busy(),.o_done(flag_meter_done),.o_angle_valid(flag_meter_angle_valid),.o_phase(wire_meter_phase),
        .o_rpm_valid(flag_meter_rpm_valid),.o_rpm(wire_meter_rpm),.o_status(wire_meter_status),.o_net(wire_meter_net),
        .o_cw(wire_meter_cw),.o_ccw(wire_meter_ccw),.o_partial(flag_meter_partial),.o_saturated(flag_meter_saturated),.o_fault(flag_meter_fault));
    // 有界事务FIFO保持源帧顺序；溢出闭锁并保留已有转数，等待用户清零。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_head<=0;cnt_tail<=0;cnt_jobs<=0;flag_fault_o<=0;flag_window_valid<=0;reg_window_x<=0;reg_window_y<=0;
        end else if(i_clear || !i_enable)begin
            cnt_head<=0;cnt_tail<=0;cnt_jobs<=0;flag_fault_o<=0;flag_window_valid<=0;
        end else begin
            if(i_fault || flag_meter_fault || (flag_enqueue && cnt_jobs == 4))begin flag_fault_o<=1;end
            if(flag_fault_o)begin cnt_head<=0;cnt_tail<=0;cnt_jobs<=0;flag_window_valid<=0;end
            else begin
                if(flag_enqueue && cnt_jobs < 4)begin
                    mem_jobs[cnt_tail]<={i_observation_epoch,i_observation_frame,i_observation_tick,
                        i_observation_new,i_observation_valid,i_left,i_right,i_top,i_bottom};
                    cnt_tail<=cnt_tail+1'b1;
                end
                if(flag_dequeue)begin cnt_head<=cnt_head+1'b1;end
                case({flag_enqueue,flag_dequeue})
                    2'b10:if(cnt_jobs < 4)begin cnt_jobs<=cnt_jobs+1'b1;end
                    2'b01:begin cnt_jobs<=cnt_jobs-1'b1;end
                    default:begin end
                endcase
                if(!i_predict_valid)begin flag_window_valid<=0;end
                else if(i_observation_done && i_observation_valid)begin
                    flag_window_valid<=1;
                    if(i_predict_x < 128)begin reg_window_x<=0;end
                    else if(i_predict_x-128 > C_WIDTH-256)begin reg_window_x<=(C_WIDTH-256) & 4092;end
                    else begin reg_window_x<=(i_predict_x-12'd128) & 12'hffc;end
                    if(i_predict_y < 128)begin reg_window_y<=0;end
                    else if(i_predict_y-128 > C_HEIGHT-256)begin reg_window_y<=(C_HEIGHT-256) & 4094;end
                    else begin reg_window_y<=(i_predict_y-12'd128) & 12'hffe;end
                end
            end
        end
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(flag_abort)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin if(cnt_jobs != 0)begin state_next=ST_FETCH;end end
            ST_FETCH:begin state_next=ST_SELECT;end
            ST_SELECT:begin
                if(wire_job_epoch != i_epoch || !flag_match)begin state_next=ST_METER_START;end
                else if(flag_complete)begin
                    if(flag_job_valid)begin state_next=ST_MARKER_START;end
                    else begin state_next=ST_METER_START;end
                end
            end
            ST_MARKER_START:begin state_next=ST_MARKER_WAIT;end
            ST_MARKER_WAIT:begin if(flag_marker_done)begin
                if(flag_marker_valid)begin state_next=ST_ANGLE_START;end else begin state_next=ST_METER_START;end
            end end
            ST_ANGLE_START:begin state_next=ST_ANGLE_WAIT;end
            ST_ANGLE_WAIT:begin if(flag_angle_done)begin state_next=ST_METER_START;end end
            ST_METER_START:begin state_next=ST_METER_WAIT;end
            ST_METER_WAIT:begin if(flag_meter_done)begin state_next=ST_COMMIT;end end
            ST_COMMIT:begin state_next=ST_IDLE;end
            default:begin state_next=ST_IDLE;end
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_job<=0;reg_release<=0;reg_phase<=0;reg_dx<=0;reg_dy<=0;flag_phase_valid<=0;
            flag_done_o<=0;reg_reason_o<=0;reg_frame_o<=0;reg_epoch_o<=0;
            flag_marker_start<=0;flag_angle_start<=0;flag_meter_start<=0;
        end else if(flag_abort)begin
            reg_release<=0;flag_phase_valid<=0;flag_done_o<=0;
            flag_marker_start<=0;flag_angle_start<=0;flag_meter_start<=0;
        end else begin
            reg_release<=0;flag_done_o<=0;flag_marker_start<=0;flag_angle_start<=0;flag_meter_start<=0;
            case(state_current)
                ST_FETCH:begin reg_job<=mem_jobs[cnt_head];flag_phase_valid<=0;end
                ST_SELECT:begin
                    if(wire_job_epoch != i_epoch)begin reg_reason_o<=4;end
                    else if(!flag_match)begin reg_reason_o<=2;end
                    else if(flag_complete && !flag_job_valid)begin reg_reason_o<=3;reg_release[flag_bank]<=1;end
                end
                ST_MARKER_START:begin flag_marker_start<=1;end
                ST_MARKER_WAIT:begin if(flag_marker_done)begin
                    reg_release[flag_bank]<=1;reg_reason_o<=wire_marker_reason;
                    reg_dx<=wire_marker_x-wire_center_x;reg_dy<=wire_marker_y-wire_center_y;
                end end
                ST_ANGLE_START:begin flag_angle_start<=1;end
                ST_ANGLE_WAIT:begin if(flag_angle_done)begin reg_phase<=wire_angle;flag_phase_valid<=flag_angle_valid;end end
                ST_METER_START:begin flag_meter_start<=1;end
                ST_COMMIT:begin
                    flag_done_o<=1;reg_frame_o<=wire_job_frame;reg_epoch_o<=wire_job_epoch;
                end
                default:begin end
            endcase
        end
    end
    assign o_done=flag_done_o;
    assign o_frame=reg_frame_o;
    assign o_epoch=reg_epoch_o;
    assign o_angle_valid=flag_meter_angle_valid;
    assign o_phase=wire_meter_phase;
    assign o_rpm_valid=flag_meter_rpm_valid;
    assign o_rpm=wire_meter_rpm;
    assign o_status=flag_fault_o ? 3'd7 : wire_meter_status;
    assign o_net=wire_meter_net;
    assign o_cw=wire_meter_cw;
    assign o_ccw=wire_meter_ccw;
    assign o_partial=flag_fault_o || flag_meter_partial;
    assign o_saturated=flag_meter_saturated;
    assign o_reason=flag_fault_o ? 4'd11 : reg_reason_o;
    assign o_fault=flag_fault_o;
    assign o_bank_busy=wire_bank_busy;

endmodule
