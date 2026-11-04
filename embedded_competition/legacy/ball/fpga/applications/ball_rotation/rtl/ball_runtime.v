`timescale 1ns / 1ps
// 安路摄像头应用插入层：保持early路径和原96/128视频接口。
module ball_runtime #(
    parameter C_WIDTH=1280, C_HEIGHT=720,
    parameter C_X_MIN=64, C_Y_MIN=160, C_X_END=1216, C_Y_END=640,
    parameter C_GATE_MIN=544, C_GATE_END=736, C_LINE=640, C_HYST=16,
    parameter C_MIN_AREA=128, C_MIN_SIZE=12, C_MAX_SIZE=384,
    parameter C_MAX_MOVE=64, C_DEBOUNCE=2100000, C_LONG_PRESS=103520000,
    parameter C_FACE_GATE=0,
    parameter C_ROTATION_ENABLE=1, C_ROTATION_CLOCK_HZ=103520000, // 追踪模式旋转支路及时间标定。
    parameter C_FACE_STUMPS="E:/project/ball/fpga/applications/ball_rotation/rtl/face_rom/stumps.mem",
    parameter C_FACE_STAGES="E:/project/ball/fpga/applications/ball_rotation/rtl/face_rom/stages.mem",
    parameter C_FACE_COORDINATES="E:/project/ball/fpga/applications/ball_rotation/rtl/face_rom/coordinates.mem"
)(
    input I_clk,
    input I_rst_n,
    input [3:0] I_keys_n,
    input [47:0] I_camera_status,
    input [95:0] I_rgb,
    input I_valid,
    input I_user,
    input I_last,
    output [127:0] O_data,
    output O_valid,
    output O_last,
    output O_done,
    output O_early,
    output O_error,
    output [31:0] O_red,
    output [31:0] O_green,
    output [31:0] O_yellow,
    output [33:0] O_total,
    output O_count_mode,
    output [2:0] O_gate_state,
    output [1:0] O_track_status,
    output [1:0] O_camera_step // 两键长按翻转事件，跨域由ae_set接收。
);
    wire mode,strict,mask,clear_history,key_clear,clear_counts;
    reg [47:0] reg_camera_status;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin reg_camera_status<=0;end
        else if(I_user)begin reg_camera_status<=I_camera_status;end
    end
    wire [15:0] epoch;
    wire [15:0] active_epoch;
    wire face_unlocked,face_restart,face_busy,face_done,face_positive,face_fault,face_pending;
    wire [1:0] face_confirmed;
    wire [31:0] face_sample,face_cycles;
    wire [15:0] face_epoch;
    wire [11:0] face_left,face_right,face_top,face_bottom;
    wire [7:0] face_raw_count;
    reg flag_face_box,flag_display_face_box,flag_display_unlocked,flag_display_face_busy,flag_display_face_fault;
    reg [1:0] reg_display_confirmed;
    reg [11:0] reg_face_left,reg_face_right,reg_face_top,reg_face_bottom;
    reg [11:0] reg_display_face_left,reg_display_face_right,reg_display_face_top,reg_display_face_bottom;
    wire ball_enabled=face_unlocked;
    // 锁定时统计已持续清零；解锁只提交epoch，无需再驱动统计清理扇出。
    wire stats_clear=key_clear || !ball_enabled;
    wire [95:0] front_rgb;
    wire front_valid,front_sof,front_eol,front_eof,front_error;
    wire [11:0] front_x,front_y;
    wire [7:0] front_labels;
    wire [2:0] front_hits;
    wire [15:0] front_epoch;
    wire scan_start,scan_valid,scan_done,scan_overflow,scan_fault,scan_error;
    wire [1:0] scan_color;
    wire [19:0] scan_area,scan_gate;
    wire scan_gate_occupied;
    wire [19:0] scan_effective_gate=scan_gate_occupied ? scan_gate : 20'd0;
    wire [11:0] scan_left,scan_right,scan_top,scan_bottom;
    wire [15:0] scan_epoch;
    wire [3:0] scan_diag_count,scan_diag_reject;
    wire [11:0] scan_diag_width,scan_diag_height;
    wire [19:0] scan_diag_area;
    wire [6:0] scan_diag_fill;
    reg [3:0] reg_pending_diag_count,reg_pending_diag_reject,reg_display_diag_count,reg_display_diag_reject;
    reg [11:0] reg_number_diag_width,reg_number_diag_height;
    reg [19:0] reg_number_diag_area;
    reg [6:0] reg_number_diag_fill;
    wire [15:0] bcd_diag_width,bcd_diag_height;
    wire [27:0] bcd_diag_area;
    wire [11:0] bcd_diag_fill;
    reg [15:0] reg_pending_diag_width_bcd,reg_pending_diag_height_bcd,reg_display_diag_width_bcd,reg_display_diag_height_bcd;
    reg [27:0] reg_pending_diag_area_bcd,reg_display_diag_area_bcd;
    reg [11:0] reg_pending_diag_fill_bcd,reg_display_diag_fill_bcd;
    // 退役任务只比较已提交epoch；新帧前端仍使用组合前视epoch。
    wire accept_frame=scan_epoch == active_epoch && !stats_clear;
    wire track_valid;
    wire [1:0] track_status,track_color;
    wire [11:0] track_left,track_right,track_top,track_bottom,track_x,track_y;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    wire [2:0] gate_state,reason;
    wire [1:0] gate_empty,count_event;
    wire [11:0] gate_x,gate_y;
    reg reg_early_o;
    reg [3:0] cnt_work;
    reg [7:0] reg_work_valid,reg_pending_valid,reg_display_valid;
    reg [15:0] reg_work_color,reg_pending_color,reg_display_color;
    reg [95:0] reg_work_left,reg_work_right,reg_work_top,reg_work_bottom;
    reg [95:0] reg_pending_left,reg_pending_right,reg_pending_top,reg_pending_bottom;
    reg [95:0] reg_display_left,reg_display_right,reg_display_top,reg_display_bottom;
    reg [15:0] reg_pending_epoch;
    reg [15:0] cnt_pending_job,reg_format_job,reg_format_epoch;
    reg [1:0] cnt_settle;
    reg flag_format_load,flag_pending_ready;
    reg [31:0] reg_number_red,reg_number_green,reg_number_yellow;
    reg [33:0] reg_number_total;
    reg [11:0] reg_number_x,reg_number_y;
    reg [1:0] reg_pending_track,reg_display_track;
    reg [2:0] reg_pending_gate,reg_pending_reason,reg_display_gate,reg_display_reason;
    wire [39:0] bcd_red,bcd_green,bcd_yellow;
    wire [43:0] bcd_total;
    wire [15:0] bcd_x,bcd_y;
    wire format_done;
    reg [39:0] reg_pending_red_bcd,reg_pending_green_bcd,reg_pending_yellow_bcd;
    reg [43:0] reg_pending_total_bcd;
    reg [15:0] reg_pending_x_bcd,reg_pending_y_bcd;
    reg [39:0] reg_display_red_bcd,reg_display_green_bcd,reg_display_yellow_bcd;
    reg [43:0] reg_display_total_bcd;
    reg [15:0] reg_display_x_bcd,reg_display_y_bcd;
    wire [95:0] overlay_rgb,osd_rgb;
    wire overlay_valid,overlay_sof,overlay_eol,overlay_eof;
    wire [11:0] overlay_x,overlay_y;
    wire osd_valid,osd_sof,osd_eol,osd_eof,pack_error;


    // 源帧身份在front SOF锁存；组件处理完成时刻不能代替采集时刻。
    localparam C_ROTATION_ACTIVE=C_ROTATION_ENABLE && C_WIDTH >= 256 && C_HEIGHT >= 256;
    reg [63:0] cnt_rotation_clock,reg_source_stamp,reg_observation_stamp;
    reg [31:0] cnt_source_frame,reg_source_frame,reg_observation_frame;
    reg [15:0] reg_observation_epoch;
    wire [31:0] source_frame=front_sof ? cnt_source_frame : reg_source_frame;
    wire [63:0] source_stamp=front_sof ? cnt_rotation_clock : reg_source_stamp;
    wire [31:0] scan_frame_id;
    wire [63:0] scan_stamp;
    wire observed_done,observed_valid,observed_new;
    wire [11:0] observed_left,observed_right,observed_top,observed_bottom;
    wire rotation_done,rotation_angle_valid,rotation_rpm_valid,rotation_partial,rotation_saturated,rotation_fault;
    wire [31:0] rotation_frame,rotation_cw,rotation_ccw;
    wire [15:0] rotation_epoch,rotation_phase;
    wire [23:0] rotation_rpm;
    wire [47:0] rotation_net;
    wire [2:0] rotation_status;
    wire [3:0] rotation_reason;
    reg flag_rotation_load,flag_rotation_pending,flag_rotation_format_valid;
    // 先冻结绝对累计相位，次拍缩位换算；新结果撤销旧的待转换事务。
    reg flag_rotation_scale,flag_rotation_input_saturated;
    reg [47:0] reg_rotation_abs_net;
    reg [15:0] reg_rotation_epoch;
    reg [23:0] reg_rotation_number_rpm;
    reg [11:0] reg_rotation_number_angle;
    reg [16:0] reg_rotation_number_net;
    reg [31:0] reg_rotation_number_cw,reg_rotation_number_ccw;
    wire [31:0] rotation_rpm_bcd;
    wire [15:0] rotation_angle_bcd;
    wire [19:0] rotation_net_bcd;
    wire [39:0] rotation_cw_bcd,rotation_ccw_bcd;
    wire rotation_format_done;
    wire [31:0] rotation_angle_scaled={16'd0,rotation_phase}*32'd3600;
    wire [47:0] rotation_abs_net=rotation_net[47] ? -rotation_net : rotation_net;
    // floor(abs*100/65536)>99999 当且仅当 abs>=65536000；非饱和值只需26位。
    wire flag_rotation_net_limit=|reg_rotation_abs_net[47:26] || reg_rotation_abs_net[25:0] >= 26'd65536000;
    // 三个操作数均先扩为33位，避免Verilog左移按窄操作数位宽截断。
    wire [32:0] rotation_net_scaled={1'b0,reg_rotation_abs_net[25:0],6'd0}+
        {2'b0,reg_rotation_abs_net[25:0],5'd0}+{5'b0,reg_rotation_abs_net[25:0],2'd0};
    reg [31:0] reg_rotation_pending_rpm_bcd,reg_rotation_display_rpm_bcd;
    reg [15:0] reg_rotation_pending_angle_bcd,reg_rotation_display_angle_bcd;
    reg [19:0] reg_rotation_pending_net_bcd,reg_rotation_display_net_bcd;
    reg [39:0] reg_rotation_pending_cw_bcd,reg_rotation_pending_ccw_bcd,reg_rotation_display_cw_bcd,reg_rotation_display_ccw_bcd;
    reg [2:0] reg_rotation_pending_status,reg_rotation_display_status;
    reg [3:0] reg_rotation_pending_reason,reg_rotation_display_reason;
    reg flag_rotation_pending_angle,flag_rotation_pending_rpm,flag_rotation_pending_partial,flag_rotation_pending_negative;
    reg flag_rotation_display_angle,flag_rotation_display_rpm,flag_rotation_display_partial,flag_rotation_display_negative;

    generate
        if(C_FACE_GATE)begin:gen_face_gate
            face_detector #(.C_STUMPS(C_FACE_STUMPS),.C_STAGES(C_FACE_STAGES),.C_COORDINATES(C_FACE_COORDINATES)) detector_Inst(
                .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(key_clear),.i_enable(!face_unlocked),
                .i_rgb(front_rgb),.i_valid(front_valid),.i_sof(front_sof),.i_eof(front_eof),.i_error(front_error),
                .i_x(front_x),.i_y(front_y),.i_epoch(front_epoch),.o_busy(face_busy),.o_done(face_done),
                .o_positive(face_positive),.o_fault(face_fault),.o_sample(face_sample),.o_epoch(face_epoch),.o_cycles(face_cycles),
                .o_left(face_left),.o_right(face_right),.o_top(face_top),.o_bottom(face_bottom),.o_raw_count(face_raw_count));
            face_gate_control gate_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_early(I_user),
                .i_session_clear(key_clear),.i_relock(1'b0),.i_result(face_done),.i_positive(face_positive),.i_fault(face_fault),
                .i_sample(face_sample),.i_result_epoch(face_epoch),.i_epoch(active_epoch),
                .o_unlocked(face_unlocked),.o_restart(face_restart),.o_confirmed(face_confirmed),.o_pending(face_pending));
        end else begin:gen_ball_regression
            // 仅供已有小球回归显式选择；上板工程默认始终启用门禁。
            assign face_unlocked=1'b1;assign face_restart=1'b0;assign face_busy=1'b0;assign face_done=1'b0;
            assign face_positive=1'b0;assign face_fault=1'b0;assign face_pending=1'b0;assign face_confirmed=2'd0;
            assign face_sample=32'd0;assign face_cycles=32'd0;assign face_epoch=16'd0;assign face_raw_count=8'd0;
            assign face_left=12'd0;assign face_right=12'd0;assign face_top=12'd0;assign face_bottom=12'd0;
        end
    endgenerate
    // 人脸状态与框也在CSI帧边界冻结，随后随RGB经DDR到HDMI，不裸跨多位总线。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            flag_face_box<=0;flag_display_face_box<=0;flag_display_unlocked<=!C_FACE_GATE;
            flag_display_face_busy<=0;flag_display_face_fault<=0;reg_display_confirmed<=0;
            reg_face_left<=0;reg_face_right<=0;reg_face_top<=0;reg_face_bottom<=0;
            reg_display_face_left<=0;reg_display_face_right<=0;reg_display_face_top<=0;reg_display_face_bottom<=0;
        end else begin
            if(key_clear)flag_face_box<=0;
            else if(face_done && face_epoch == active_epoch)begin
                flag_face_box<=face_positive && !face_fault;
                reg_face_left<=face_left;reg_face_right<=face_right;reg_face_top<=face_top;reg_face_bottom<=face_bottom;
            end
            if(I_user)begin
                flag_display_unlocked<=face_unlocked || face_restart;
                flag_display_face_box<=flag_face_box && !face_unlocked && !face_restart && !clear_history;
                flag_display_face_busy<=face_busy;flag_display_face_fault<=face_fault;reg_display_confirmed<=face_confirmed;
                reg_display_face_left<=reg_face_left;reg_display_face_right<=reg_face_right;
                reg_display_face_top<=reg_face_top;reg_display_face_bottom<=reg_face_bottom;
            end
        end
    end
    ball_key_control #(.C_DEBOUNCE(C_DEBOUNCE),.C_LONG_PRESS(C_LONG_PRESS)) keys_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_keys_n(I_keys_n),.i_early(I_user),
        .i_session_restart(face_restart),
        .o_count_mode(mode),.o_strict(strict),.o_mask(mask),.o_epoch(epoch),.o_active_epoch(active_epoch),
        .o_clear(clear_history),.o_key_clear(key_clear),.o_clear_counts(clear_counts),.o_camera_step(O_camera_step));
    ball_stream_front #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END)) front_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(I_rgb),.i_valid(I_valid),.i_early(I_user),.i_strict(strict),.i_epoch(epoch),
        .o_rgb(front_rgb),.o_valid(front_valid),.o_sof(front_sof),.o_eol(front_eol),.o_eof(front_eof),
        .o_x(front_x),.o_y(front_y),.o_labels(front_labels),.o_gate_hits(front_hits),.o_epoch(front_epoch),.o_error(front_error));
    ball_components #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_MIN_AREA(C_MIN_AREA),
        .C_MIN_SIZE(C_MIN_SIZE),.C_MAX_SIZE(C_MAX_SIZE)) components_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_session_clear(stats_clear),
        .i_valid(front_valid && ball_enabled),.i_sof(front_sof && ball_enabled),.i_eof(front_eof && ball_enabled),
        .i_x(front_x),.i_y(front_y),.i_labels(front_labels),.i_gate_hits(front_hits),.i_epoch(front_epoch),.i_frame_id(source_frame),.i_stamp(source_stamp),
        .o_frame_start(scan_start),.o_candidate_valid(scan_valid),.o_color(scan_color),.o_area(scan_area),
        .o_x_min(scan_left),.o_x_max(scan_right),.o_y_min(scan_top),.o_y_max(scan_bottom),
        .o_frame_done(scan_done),.o_gate_pixels(scan_gate),.o_gate_occupied(scan_gate_occupied),.o_epoch(scan_epoch),.o_frame_id(scan_frame_id),.o_stamp(scan_stamp),
        .o_overflow(scan_overflow),.o_fault(scan_fault),.o_error(scan_error),
        .o_diag_count(scan_diag_count),.o_diag_width(scan_diag_width),.o_diag_height(scan_diag_height),
        .o_diag_area(scan_diag_area),.o_diag_fill(scan_diag_fill),.o_diag_reject(scan_diag_reject));
    ball_target_tracker #(.C_MAX_MOVE(C_MAX_MOVE),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END)) tracker_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(stats_clear || (scan_fault && ball_enabled)),
        .i_frame_start(scan_start && accept_frame && !mode),.i_candidate_valid(scan_valid && accept_frame && !mode),
        .i_color(scan_color),.i_area(scan_area),.i_x_min(scan_left),.i_x_max(scan_right),.i_y_min(scan_top),.i_y_max(scan_bottom),
        .i_frame_done(scan_done && accept_frame && !mode),.i_overflow(scan_overflow),
        .o_valid(track_valid),.o_status(track_status),.o_color(track_color),
        .o_x_min(track_left),.o_x_max(track_right),.o_y_min(track_top),.o_y_max(track_bottom),.o_center_x(track_x),.o_center_y(track_y),
        .o_observation_done(observed_done),.o_observed_valid(observed_valid),.o_observed_new(observed_new),
        .o_observed_left(observed_left),.o_observed_right(observed_right),.o_observed_top(observed_top),.o_observed_bottom(observed_bottom));
    ball_gate_counter #(.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_GATE_TOP(C_Y_MIN),.C_GATE_BOTTOM(C_Y_END),
        .C_LINE(C_LINE),.C_HYST(C_HYST)) counter_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(stats_clear),
        .i_clear_counts(clear_counts || !ball_enabled),.i_fault(scan_fault && mode && !stats_clear),
        .i_frame_start(scan_start && accept_frame && mode),.i_candidate_valid(scan_valid && accept_frame && mode),
        .i_color(scan_color),.i_x_min(scan_left),.i_x_max(scan_right),.i_y_min(scan_top),.i_y_max(scan_bottom),
        .i_frame_done(scan_done && accept_frame && mode),.i_overflow(scan_overflow),.i_gate_pixels(scan_effective_gate),
        .o_red(red),.o_yellow(yellow),.o_green(green),.o_total(total),.o_state(gate_state),.o_empty(gate_empty),
        .o_event(count_event),.o_reason(reason),.o_center_x(gate_x),.o_center_y(gate_y));


    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            cnt_rotation_clock<=0;cnt_source_frame<=0;reg_source_frame<=0;reg_source_stamp<=0;
            reg_observation_frame<=0;reg_observation_stamp<=0;reg_observation_epoch<=0;
        end else begin
            cnt_rotation_clock<=cnt_rotation_clock+1'b1;
            if(front_valid && front_sof)begin
                reg_source_frame<=cnt_source_frame;cnt_source_frame<=cnt_source_frame+1'b1;
                reg_source_stamp<=cnt_rotation_clock;
            end
            if(scan_done && accept_frame && !mode)begin
                reg_observation_frame<=scan_frame_id;reg_observation_stamp<=scan_stamp;reg_observation_epoch<=scan_epoch;
            end
        end
    end
    generate
        if(C_ROTATION_ACTIVE)begin:gen_rotation
            ball_rotation #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_CLOCK_HZ(C_ROTATION_CLOCK_HZ)) rotation_Inst(
                .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(clear_history),.i_fault(scan_fault && ball_enabled && !mode),
                .i_enable(ball_enabled && !mode),.i_rgb(front_rgb),.i_valid(front_valid),.i_sof(front_sof),.i_x(front_x),.i_y(front_y),
                .i_frame(source_frame),.i_tick(source_stamp),.i_epoch(front_epoch),
                .i_observation_done(observed_done),.i_observation_valid(observed_valid),.i_observation_new(observed_new),
                .i_observation_frame(reg_observation_frame),.i_observation_tick(reg_observation_stamp),.i_observation_epoch(reg_observation_epoch),
                .i_left(observed_left),.i_right(observed_right),.i_top(observed_top),.i_bottom(observed_bottom),
                .i_predict_valid(track_valid),.i_predict_x(track_x),.i_predict_y(track_y),
                .o_done(rotation_done),.o_frame(rotation_frame),.o_epoch(rotation_epoch),.o_angle_valid(rotation_angle_valid),.o_phase(rotation_phase),
                .o_rpm_valid(rotation_rpm_valid),.o_rpm(rotation_rpm),.o_status(rotation_status),.o_net(rotation_net),.o_cw(rotation_cw),.o_ccw(rotation_ccw),
                .o_partial(rotation_partial),.o_saturated(rotation_saturated),.o_reason(rotation_reason),.o_fault(rotation_fault),
                .o_bank_busy(),.o_median(),.o_threshold());
        end else begin:gen_rotation_disabled
            assign rotation_done=0;assign rotation_frame=0;assign rotation_epoch=0;assign rotation_angle_valid=0;assign rotation_phase=0;
            assign rotation_rpm_valid=0;assign rotation_rpm=0;assign rotation_status=0;assign rotation_net=0;assign rotation_cw=0;assign rotation_ccw=0;
            assign rotation_partial=0;assign rotation_saturated=0;assign rotation_reason=0;assign rotation_fault=0;
        end
    endgenerate
    ball_decimal_format #(.C_BITS(24),.C_DIGITS(8)) rotation_rpm_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_rotation_load),.i_binary(reg_rotation_number_rpm),.o_bcd(rotation_rpm_bcd),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(12),.C_DIGITS(4)) rotation_angle_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_rotation_load),.i_binary(reg_rotation_number_angle),.o_bcd(rotation_angle_bcd),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(17),.C_DIGITS(5)) rotation_net_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_rotation_load),.i_binary(reg_rotation_number_net),.o_bcd(rotation_net_bcd),.o_done(),.o_busy());
    ball_decimal_format rotation_cw_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_rotation_load),.i_binary(reg_rotation_number_cw),.o_bcd(rotation_cw_bcd),.o_done(rotation_format_done),.o_busy());
    ball_decimal_format rotation_ccw_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_rotation_load),.i_binary(reg_rotation_number_ccw),.o_bcd(rotation_ccw_bcd),.o_done(),.o_busy());
    // 数值转换后在原视频帧边界整包发布；不向原像素通路插入时钟级。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            flag_rotation_load<=0;flag_rotation_pending<=0;flag_rotation_format_valid<=0;reg_rotation_epoch<=0;
            flag_rotation_scale<=0;flag_rotation_input_saturated<=0;reg_rotation_abs_net<=0;
            reg_rotation_number_rpm<=0;reg_rotation_number_angle<=0;reg_rotation_number_net<=0;reg_rotation_number_cw<=0;reg_rotation_number_ccw<=0;
            reg_rotation_pending_rpm_bcd<=0;reg_rotation_display_rpm_bcd<=0;reg_rotation_pending_angle_bcd<=0;reg_rotation_display_angle_bcd<=0;
            reg_rotation_pending_net_bcd<=0;reg_rotation_display_net_bcd<=0;
            reg_rotation_pending_cw_bcd<=0;reg_rotation_pending_ccw_bcd<=0;reg_rotation_display_cw_bcd<=0;reg_rotation_display_ccw_bcd<=0;
            reg_rotation_pending_status<=0;reg_rotation_display_status<=0;reg_rotation_pending_reason<=0;reg_rotation_display_reason<=0;
            flag_rotation_pending_angle<=0;flag_rotation_pending_rpm<=0;flag_rotation_pending_partial<=0;flag_rotation_pending_negative<=0;
            flag_rotation_display_angle<=0;flag_rotation_display_rpm<=0;flag_rotation_display_partial<=0;flag_rotation_display_negative<=0;
        end else if(clear_history || !ball_enabled || mode)begin
            flag_rotation_load<=0;flag_rotation_pending<=0;flag_rotation_format_valid<=0;flag_rotation_scale<=0;
            reg_rotation_display_rpm_bcd<=0;reg_rotation_display_angle_bcd<=0;reg_rotation_display_net_bcd<=0;
            reg_rotation_display_cw_bcd<=0;reg_rotation_display_ccw_bcd<=0;reg_rotation_display_status<=0;reg_rotation_display_reason<=0;
            flag_rotation_display_angle<=0;flag_rotation_display_rpm<=0;flag_rotation_display_partial<=0;flag_rotation_display_negative<=0;
        end else begin
            flag_rotation_load<=0;
            if(rotation_done && rotation_epoch == active_epoch)begin
                flag_rotation_scale<=1;flag_rotation_pending<=0;flag_rotation_format_valid<=0;reg_rotation_epoch<=rotation_epoch;
                reg_rotation_abs_net<=rotation_abs_net;flag_rotation_input_saturated<=rotation_saturated;
                reg_rotation_number_rpm<=rotation_rpm[23] ? -rotation_rpm : rotation_rpm;
                reg_rotation_number_angle<=rotation_angle_scaled[27:16];
                reg_rotation_number_cw<=rotation_cw;reg_rotation_number_ccw<=rotation_ccw;
                reg_rotation_pending_status<=rotation_status;
                reg_rotation_pending_reason<=rotation_saturated ? 4'd15 : rotation_reason;
                flag_rotation_pending_angle<=rotation_angle_valid;flag_rotation_pending_rpm<=rotation_rpm_valid;
                flag_rotation_pending_partial<=rotation_partial || rotation_saturated;flag_rotation_pending_negative<=rotation_net[47];
            end else if(flag_rotation_scale)begin
                flag_rotation_scale<=0;
                if(reg_rotation_epoch == active_epoch)begin
                    flag_rotation_load<=1;flag_rotation_format_valid<=1;
                    reg_rotation_number_net<=flag_rotation_net_limit ? 17'd99999 : rotation_net_scaled[32:16];
                    if(flag_rotation_net_limit && !flag_rotation_input_saturated)reg_rotation_pending_reason<=14;
                end
            end
            // 拒绝捕获、缩位和加载三处边界上的旧BCD完成脉冲。
            if(rotation_format_done && flag_rotation_format_valid && reg_rotation_epoch == active_epoch &&
               !rotation_done && !flag_rotation_scale && !flag_rotation_load)begin
                flag_rotation_pending<=1;
                reg_rotation_pending_rpm_bcd<=rotation_rpm_bcd;reg_rotation_pending_angle_bcd<=rotation_angle_bcd;
                reg_rotation_pending_net_bcd<=rotation_net_bcd;reg_rotation_pending_cw_bcd<=rotation_cw_bcd;reg_rotation_pending_ccw_bcd<=rotation_ccw_bcd;
            end
            if(I_user)begin
                if(rotation_fault)begin
                    reg_rotation_display_status<=7;reg_rotation_display_reason<=11;
                    flag_rotation_display_angle<=0;flag_rotation_display_rpm<=0;flag_rotation_display_partial<=1;
                end else if(flag_rotation_pending && reg_rotation_epoch == active_epoch)begin
                    reg_rotation_display_rpm_bcd<=reg_rotation_pending_rpm_bcd;reg_rotation_display_angle_bcd<=reg_rotation_pending_angle_bcd;
                    reg_rotation_display_net_bcd<=reg_rotation_pending_net_bcd;
                    reg_rotation_display_cw_bcd<=reg_rotation_pending_cw_bcd;reg_rotation_display_ccw_bcd<=reg_rotation_pending_ccw_bcd;
                    reg_rotation_display_status<=reg_rotation_pending_status;reg_rotation_display_reason<=reg_rotation_pending_reason;
                    flag_rotation_display_angle<=flag_rotation_pending_angle;flag_rotation_display_rpm<=flag_rotation_pending_rpm;
                    flag_rotation_display_partial<=flag_rotation_pending_partial;flag_rotation_display_negative<=flag_rotation_pending_negative;
                end
            end
        end
    end

    // start/done之间只写工作副本；帧显示使用另一份冻结副本。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            reg_early_o<=0; cnt_work<=0; cnt_settle<=0; flag_format_load<=0; flag_pending_ready<=0;
            cnt_pending_job<=0; reg_format_job<=0; reg_format_epoch<=0;
            reg_work_valid<=0; reg_work_color<=0; reg_work_left<=0; reg_work_right<=0; reg_work_top<=0; reg_work_bottom<=0;
            reg_pending_valid<=0; reg_pending_color<=0; reg_pending_left<=0; reg_pending_right<=0;
            reg_pending_top<=0; reg_pending_bottom<=0; reg_pending_epoch<=0;
            reg_display_valid<=0; reg_display_color<=0; reg_display_left<=0; reg_display_right<=0;
            reg_display_top<=0; reg_display_bottom<=0;
            reg_number_red<=0; reg_number_green<=0; reg_number_yellow<=0; reg_number_total<=0;
            reg_number_x<=0; reg_number_y<=0;
            reg_pending_track<=0; reg_pending_gate<=0; reg_pending_reason<=0;
            reg_display_track<=0; reg_display_gate<=0; reg_display_reason<=0;
            reg_pending_red_bcd<=0; reg_pending_green_bcd<=0; reg_pending_yellow_bcd<=0;
            reg_pending_total_bcd<=0; reg_pending_x_bcd<=0; reg_pending_y_bcd<=0;
            reg_display_red_bcd<=0; reg_display_green_bcd<=0; reg_display_yellow_bcd<=0;
            reg_display_total_bcd<=0; reg_display_x_bcd<=0; reg_display_y_bcd<=0;
            reg_pending_diag_count<=0;reg_pending_diag_reject<=0;reg_display_diag_count<=0;reg_display_diag_reject<=0;
            reg_number_diag_width<=0;reg_number_diag_height<=0;reg_number_diag_area<=0;reg_number_diag_fill<=0;
            reg_pending_diag_width_bcd<=0;reg_pending_diag_height_bcd<=0;reg_pending_diag_area_bcd<=0;reg_pending_diag_fill_bcd<=0;
            reg_display_diag_width_bcd<=0;reg_display_diag_height_bcd<=0;reg_display_diag_area_bcd<=0;reg_display_diag_fill_bcd<=0;
        end else begin
            reg_early_o<=I_user; flag_format_load<=0;
            if(flag_format_load)begin reg_format_job<=cnt_pending_job; reg_format_epoch<=reg_pending_epoch; end
            if(stats_clear)begin
                cnt_pending_job<=cnt_pending_job+1'b1;
                cnt_work<=0; cnt_settle<=0; flag_pending_ready<=0;
                reg_work_valid<=0; reg_pending_valid<=0; reg_display_valid<=0;
                reg_pending_epoch<=epoch; reg_display_track<=0; reg_display_gate<=0; reg_display_reason<=0;
                reg_display_x_bcd<=0; reg_display_y_bcd<=0;
                reg_pending_diag_count<=0;reg_pending_diag_reject<=0;reg_display_diag_count<=0;reg_display_diag_reject<=0;
                reg_display_diag_width_bcd<=0;reg_display_diag_height_bcd<=0;reg_display_diag_area_bcd<=0;reg_display_diag_fill_bcd<=0;
                if(clear_counts || !ball_enabled)begin
                    reg_display_red_bcd<=0; reg_display_green_bcd<=0;
                    reg_display_yellow_bcd<=0; reg_display_total_bcd<=0;
                end
            end else begin
                if(scan_start && accept_frame)begin cnt_work<=0; reg_work_valid<=0; end
                if(scan_valid && accept_frame && cnt_work < 8)begin
                    reg_work_valid[cnt_work]<=1; reg_work_color[cnt_work*2 +:2]<=scan_color;
                    reg_work_left[cnt_work*12 +:12]<=scan_left; reg_work_right[cnt_work*12 +:12]<=scan_right;
                    reg_work_top[cnt_work*12 +:12]<=scan_top; reg_work_bottom[cnt_work*12 +:12]<=scan_bottom;
                    cnt_work<=cnt_work+1'b1;
                end
                if(scan_done && accept_frame)begin
                    reg_pending_diag_count<=scan_diag_count;reg_pending_diag_reject<=scan_diag_reject;
                    reg_number_diag_width<=scan_diag_width;reg_number_diag_height<=scan_diag_height;
                    reg_number_diag_area<=scan_diag_area;reg_number_diag_fill<=scan_diag_fill;
                    cnt_pending_job<=cnt_pending_job+1'b1;
                    cnt_settle<=3; flag_pending_ready<=0; reg_pending_epoch<=scan_epoch;
                    reg_pending_valid<=scan_overflow ? 8'd0 : reg_work_valid;
                    reg_pending_color<=reg_work_color; reg_pending_left<=reg_work_left; reg_pending_right<=reg_work_right;
                    reg_pending_top<=reg_work_top; reg_pending_bottom<=reg_work_bottom;
                end else if(cnt_settle != 0)begin
                    cnt_settle<=cnt_settle-1'b1;
                    if(cnt_settle == 1)begin
                        flag_format_load<=1;
                        reg_number_red<=red; reg_number_green<=green; reg_number_yellow<=yellow; reg_number_total<=total;
                        reg_number_x<=mode ? gate_x : (track_valid ? track_x : 12'd0);
                        reg_number_y<=mode ? gate_y : (track_valid ? track_y : 12'd0);
                        reg_pending_gate<=gate_state; reg_pending_reason<=scan_overflow ? 3'd1 : reason;
                        reg_pending_track<=track_status;
                        if(!mode)begin
                            reg_pending_valid<={7'd0,track_valid};
                            reg_pending_color<={14'd0,(track_status == 3 ? 2'd0 : track_color)};
                            reg_pending_left<={84'd0,track_left}; reg_pending_right<={84'd0,track_right};
                            reg_pending_top<={84'd0,track_top}; reg_pending_bottom<={84'd0,track_bottom};
                        end
                    end
                end
                if(format_done && reg_format_epoch == active_epoch && reg_format_job == cnt_pending_job &&
                   !(scan_done && accept_frame))begin
                    flag_pending_ready<=1;
                    reg_pending_red_bcd<=bcd_red; reg_pending_green_bcd<=bcd_green; reg_pending_yellow_bcd<=bcd_yellow;
                    reg_pending_total_bcd<=bcd_total; reg_pending_x_bcd<=bcd_x; reg_pending_y_bcd<=bcd_y;
                    reg_pending_diag_width_bcd<=bcd_diag_width;reg_pending_diag_height_bcd<=bcd_diag_height;
                    reg_pending_diag_area_bcd<=bcd_diag_area;reg_pending_diag_fill_bcd<=bcd_diag_fill;
                end
                if(I_user && flag_pending_ready && reg_pending_epoch == active_epoch)begin
                    reg_display_valid<=reg_pending_valid; reg_display_color<=reg_pending_color;
                    reg_display_left<=reg_pending_left; reg_display_right<=reg_pending_right;
                    reg_display_top<=reg_pending_top; reg_display_bottom<=reg_pending_bottom;
                    reg_display_red_bcd<=reg_pending_red_bcd; reg_display_green_bcd<=reg_pending_green_bcd;
                    reg_display_yellow_bcd<=reg_pending_yellow_bcd; reg_display_total_bcd<=reg_pending_total_bcd;
                    reg_display_x_bcd<=reg_pending_x_bcd; reg_display_y_bcd<=reg_pending_y_bcd;
                    reg_display_track<=reg_pending_track; reg_display_gate<=reg_pending_gate; reg_display_reason<=reg_pending_reason;
                    reg_display_diag_count<=reg_pending_diag_count;reg_display_diag_reject<=reg_pending_diag_reject;
                    reg_display_diag_width_bcd<=reg_pending_diag_width_bcd;reg_display_diag_height_bcd<=reg_pending_diag_height_bcd;
                    reg_display_diag_area_bcd<=reg_pending_diag_area_bcd;reg_display_diag_fill_bcd<=reg_pending_diag_fill_bcd;
                end
            end
        end
    end
    ball_decimal_format red_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_red),.o_bcd(bcd_red),.o_done(),.o_busy());
    ball_decimal_format green_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_green),.o_bcd(bcd_green),.o_done(),.o_busy());
    ball_decimal_format yellow_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_yellow),.o_bcd(bcd_yellow),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(34),.C_DIGITS(11)) total_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_total),.o_bcd(bcd_total),.o_done(format_done),.o_busy());
    ball_decimal_format #(.C_BITS(12),.C_DIGITS(4)) x_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_x),.o_bcd(bcd_x),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(12),.C_DIGITS(4)) y_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_y),.o_bcd(bcd_y),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(12),.C_DIGITS(4)) diag_width_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_diag_width),.o_bcd(bcd_diag_width),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(12),.C_DIGITS(4)) diag_height_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_diag_height),.o_bcd(bcd_diag_height),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(20),.C_DIGITS(7)) diag_area_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_diag_area),.o_bcd(bcd_diag_area),.o_done(),.o_busy());
    ball_decimal_format #(.C_BITS(7),.C_DIGITS(3)) diag_fill_decimal_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_format_load),.i_binary(reg_number_diag_fill),.o_bcd(bcd_diag_fill),.o_done(),.o_busy());
    ball_overlay #(.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_X_END(C_X_END),.C_Y_END(C_Y_END),
        .C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_LINE(C_LINE),.C_HYST(C_HYST)) overlay_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(front_rgb),.i_valid(front_valid),.i_sof(front_sof),.i_eol(front_eol),.i_eof(front_eof),
        .i_x(front_x),.i_y(front_y),.i_labels(front_labels),.i_mask(mask),.i_count_mode(mode),
        .i_face_locked(!flag_display_unlocked),.i_face_valid(flag_display_face_box),
        .i_face_left(reg_display_face_left),.i_face_right(reg_display_face_right),
        .i_face_top(reg_display_face_top),.i_face_bottom(reg_display_face_bottom),
        .i_box_valid(reg_display_valid),.i_box_color(reg_display_color),.i_box_left(reg_display_left),.i_box_right(reg_display_right),
        .i_box_top(reg_display_top),.i_box_bottom(reg_display_bottom),.o_rgb(overlay_rgb),.o_valid(overlay_valid),
        .o_sof(overlay_sof),.o_eol(overlay_eol),.o_eof(overlay_eof),.o_x(overlay_x),.o_y(overlay_y));
    ball_status_osd #(.C_ROTATION(C_ROTATION_ACTIVE)) osd_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(overlay_rgb),.i_valid(overlay_valid),
        .i_sof(overlay_sof),.i_eol(overlay_eol),.i_eof(overlay_eof),.i_x(overlay_x),.i_y(overlay_y),.i_count_mode(mode),.i_strict(strict),
        .i_camera_status(reg_camera_status),
        .i_rotation_enable(flag_display_unlocked && !mode),.i_rotation_status(reg_rotation_display_status),
        .i_rotation_reason(reg_rotation_display_reason),.i_rotation_angle_valid(flag_rotation_display_angle),
        .i_rotation_rpm_valid(flag_rotation_display_rpm),.i_rotation_partial(flag_rotation_display_partial),
        .i_rotation_negative(flag_rotation_display_negative),.i_rotation_rpm_bcd(reg_rotation_display_rpm_bcd),
        .i_rotation_angle_bcd(reg_rotation_display_angle_bcd),.i_rotation_net_bcd(reg_rotation_display_net_bcd),
        .i_rotation_cw_bcd(reg_rotation_display_cw_bcd),.i_rotation_ccw_bcd(reg_rotation_display_ccw_bcd),
        .i_face_unlocked(flag_display_unlocked),.i_face_busy(flag_display_face_busy),
        .i_face_confirmed(reg_display_confirmed),.i_face_fault(flag_display_face_fault),
        .i_diag_count(reg_display_diag_count),.i_diag_reject(reg_display_diag_reject),
        .i_diag_width_bcd(reg_display_diag_width_bcd),.i_diag_height_bcd(reg_display_diag_height_bcd),
        .i_diag_area_bcd(reg_display_diag_area_bcd),.i_diag_fill_bcd(reg_display_diag_fill_bcd),
        .i_red_bcd(reg_display_red_bcd),.i_green_bcd(reg_display_green_bcd),.i_yellow_bcd(reg_display_yellow_bcd),
        .i_total_bcd(reg_display_total_bcd),.i_x_bcd(reg_display_x_bcd),.i_y_bcd(reg_display_y_bcd),
        .i_gate_state(reg_display_gate),.i_track_status(reg_display_track),.i_reason(O_error ? 3'd7 : reg_display_reason),
        .o_rgb(osd_rgb),.o_valid(osd_valid),.o_sof(osd_sof),.o_eol(osd_eol),.o_eof(osd_eof));
    rgb96_pack128_valid pack_Inst(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_rgb(osd_rgb),.I_valid(osd_valid),
        .I_user(osd_sof),.I_last(osd_eol),.I_done(osd_eof),.O_data(O_data),.O_valid(O_valid),.O_last(O_last),.O_done(O_done),.O_error(pack_error));
    assign O_early=reg_early_o;
    assign O_error=front_error || (scan_error && ball_enabled) || pack_error;
    assign O_red=red;
    assign O_green=green;
    assign O_yellow=yellow;
    assign O_total=total;
    assign O_count_mode=mode;
    assign O_gate_state=gate_state;
    assign O_track_status=track_status;
endmodule
