`timescale 1ns / 1ps
// 安路摄像头应用插入层：保持early路径和原96/128视频接口。
module ball_runtime #(
    parameter C_WIDTH=1280, C_HEIGHT=720,
    parameter C_X_MIN=64, C_Y_MIN=160, C_X_END=1216, C_Y_END=640,
    parameter C_GATE_MIN=544, C_GATE_END=736, C_LINE=640, C_HYST=16,
    parameter C_MIN_AREA=128, C_MIN_SIZE=12, C_MAX_SIZE=384,
    parameter C_MAX_MOVE=64, C_DEBOUNCE=2100000, C_LONG_PRESS=103520000,
    parameter C_COUNT_MIN_SIZE=24,C_COUNT_MAX_SIZE=384,parameter [6:0] C_COUNT_COMPACT=27
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
    wire mode,strict,mask,clear_history,clear_counts;
    reg [47:0] reg_camera_status;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin reg_camera_status<=0;end
        else if(I_user)begin reg_camera_status<=I_camera_status;end
    end
    wire [15:0] epoch;
    wire [95:0] front_rgb;
    wire front_valid,front_sof,front_eol,front_eof,front_error;
    wire [11:0] front_x,front_y;
    wire [7:0] front_labels;
    wire [2:0] front_hits;
    wire [15:0] front_epoch;
    wire white_request,white_ready;
    wire [19:0] white_gain_red,white_gain_blue;
    reg flag_white_busy,flag_white_collect,flag_white_ready,flag_white_error;
    reg [2:0] cnt_white_frames;
    reg [17:0] reg_white_red,reg_white_blue;
    reg [2:0] reg_white_status;
    localparam C_WHITE_HALF_X=C_WIDTH>=128 ? 64 : C_WIDTH/4;
    localparam C_WHITE_HALF_Y=C_HEIGHT>=128 ? 64 : C_HEIGHT/4;
    wire white_sample=front_valid && flag_white_collect &&
        front_x>=C_WIDTH/2-C_WHITE_HALF_X && front_x<C_WIDTH/2+C_WHITE_HALF_X &&
        front_y>=C_HEIGHT/2-C_WHITE_HALF_Y && front_y<C_HEIGHT/2+C_WHITE_HALF_Y;
    // 校准在Gamma后、显示增强前取样，永不回送分割或原相机AWB。
    ball_white_balance #(.C_WHITE_CARD(1)) display_balance_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n && flag_white_busy),.i_rgb(front_rgb),
        .i_valid(white_sample),.i_early(front_sof),
        .o_gain_red(white_gain_red),.o_gain_blue(white_gain_blue),.o_ready(white_ready));
    // 只采一完整帧；成功/失败都在提前帧边界退役，首组像素之前增益已稳定。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            flag_white_busy<=0;flag_white_collect<=0;flag_white_ready<=0;flag_white_error<=0;
            cnt_white_frames<=0;reg_white_red<=18'd65536;reg_white_blue<=18'd65536;
            reg_white_status<=0;
        end else begin
            if(I_user)begin reg_white_status<={flag_white_busy,flag_white_ready,flag_white_error};end
            if(white_request && !flag_white_busy)begin
                flag_white_busy<=1;flag_white_collect<=0;cnt_white_frames<=0;flag_white_error<=0;
            end else if(flag_white_busy)begin
                if(I_user && white_ready)begin
                    reg_white_red<=white_gain_red[17:0];reg_white_blue<=white_gain_blue[17:0];
                    flag_white_ready<=1;flag_white_busy<=0;flag_white_collect<=0;
                end else if(I_user && (cnt_white_frames>=5 || front_error))begin
                    // 无足够白纸样本时保留上一次增益；不把失败当成已校准。
                    flag_white_error<=1;flag_white_busy<=0;flag_white_collect<=0;
                end else if(front_sof)begin
                    cnt_white_frames<=cnt_white_frames+1'b1;
                    flag_white_collect<=cnt_white_frames==0;
                end
            end
        end
    end
    wire scan_start,scan_valid,scan_done,scan_overflow,scan_fault,scan_error;
    wire [1:0] scan_color;
    wire [19:0] scan_area,scan_gate;
    wire scan_gate_occupied;
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
    wire accept_frame=scan_epoch == epoch && !clear_history;
    wire track_valid;
    wire [1:0] track_status,track_color;
    wire [11:0] track_left,track_right,track_top,track_bottom,track_x,track_y;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    wire [2:0] gate_state,reason;
    wire [11:0] gate_x,gate_y;
    wire multi_done;
    wire [3:0] multi_valid;
    wire [7:0] multi_color;
    wire [47:0] multi_left,multi_right,multi_top,multi_bottom;
    wire [2:0] multi_live;
    reg [2:0] reg_pending_live,reg_display_live;
    wire result_done=mode ? multi_done : (scan_done && accept_frame);
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

    ball_key_control #(.C_DEBOUNCE(C_DEBOUNCE),.C_LONG_PRESS(C_LONG_PRESS)) keys_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_keys_n(I_keys_n),.i_early(I_user),
        .o_count_mode(mode),.o_strict(strict),.o_mask(mask),.o_epoch(epoch),
        .o_clear(clear_history),.o_clear_counts(clear_counts),.o_camera_step(O_camera_step),.o_white_calibrate(white_request));
    ball_stream_front #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END)) front_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(I_rgb),.i_valid(I_valid),.i_early(I_user),.i_strict(strict),.i_epoch(epoch),
        .o_rgb(front_rgb),.o_valid(front_valid),.o_sof(front_sof),.o_eol(front_eol),.o_eof(front_eof),
        .o_x(front_x),.o_y(front_y),.o_labels(front_labels),.o_gate_hits(front_hits),.o_epoch(front_epoch),.o_error(front_error));
    ball_components #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_MIN_AREA(C_MIN_AREA),
        .C_MIN_SIZE(C_MIN_SIZE),.C_MAX_SIZE(C_MAX_SIZE),.C_ROUND_MIN_SIZE(C_COUNT_MIN_SIZE),.C_ROUND_MAX_SIZE(C_COUNT_MAX_SIZE),.C_ROUND_COMPACT(C_COUNT_COMPACT)) components_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_valid(front_valid),.i_sof(front_sof),.i_eof(front_eof),
        .i_x(front_x),.i_y(front_y),.i_labels(front_labels),.i_gate_hits(front_hits),.i_epoch(front_epoch),.i_shape_enable(mode),
        .o_frame_start(scan_start),.o_candidate_valid(scan_valid),.o_color(scan_color),.o_area(scan_area),
        .o_x_min(scan_left),.o_x_max(scan_right),.o_y_min(scan_top),.o_y_max(scan_bottom),
        .o_frame_done(scan_done),.o_gate_pixels(scan_gate),.o_gate_occupied(scan_gate_occupied),.o_epoch(scan_epoch),
        .o_overflow(scan_overflow),.o_fault(scan_fault),.o_error(scan_error),
        .o_diag_count(scan_diag_count),.o_diag_width(scan_diag_width),.o_diag_height(scan_diag_height),
        .o_diag_area(scan_diag_area),.o_diag_fill(scan_diag_fill),.o_diag_reject(scan_diag_reject));
    ball_target_tracker #(.C_MAX_MOVE(C_MAX_MOVE),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END)) tracker_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(clear_history || scan_fault),
        .i_frame_start(scan_start && accept_frame && !mode),.i_candidate_valid(scan_valid && accept_frame && !mode),
        .i_color(scan_color),.i_area(scan_area),.i_x_min(scan_left),.i_x_max(scan_right),.i_y_min(scan_top),.i_y_max(scan_bottom),
        .i_frame_done(scan_done && accept_frame && !mode),.i_overflow(scan_overflow),
        .o_valid(track_valid),.o_status(track_status),.o_color(track_color),
        .o_x_min(track_left),.o_x_max(track_right),.o_y_min(track_top),.o_y_max(track_bottom),.o_center_x(track_x),.o_center_y(track_y));
    ball_multi_counter #(.C_MAX_MOVE(C_MAX_MOVE),.C_LINE(C_LINE),.C_HYST(C_HYST)) counter_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(clear_history),.i_clear_counts(clear_counts),.i_fault(scan_fault && mode),
        .i_frame_start(scan_start && accept_frame && mode),.i_candidate_valid(scan_valid && accept_frame && mode),
        .i_color(scan_color),.i_x_min(scan_left),.i_x_max(scan_right),.i_y_min(scan_top),.i_y_max(scan_bottom),
        .i_frame_done(scan_done && accept_frame && mode),.i_overflow(scan_overflow),
        .o_red(red),.o_yellow(yellow),.o_green(green),.o_total(total),.o_state(gate_state),
        .o_reason(reason),.o_center_x(gate_x),.o_center_y(gate_y),.o_done(multi_done),.o_busy(),
        .o_active_count(multi_live),.o_box_valid(multi_valid),.o_box_color(multi_color),
        .o_box_left(multi_left),.o_box_right(multi_right),.o_box_top(multi_top),.o_box_bottom(multi_bottom));

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
            reg_pending_live<=0;reg_display_live<=0;
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
            if(clear_history)begin
                cnt_pending_job<=cnt_pending_job+1'b1;
                cnt_work<=0; cnt_settle<=0; flag_pending_ready<=0;
                reg_work_valid<=0; reg_pending_valid<=0; reg_display_valid<=0;
                reg_pending_epoch<=epoch; reg_display_track<=0; reg_display_gate<=0; reg_display_reason<=0;
                reg_pending_live<=0;reg_display_live<=0;
                reg_display_x_bcd<=0; reg_display_y_bcd<=0;
                reg_pending_diag_count<=0;reg_pending_diag_reject<=0;reg_display_diag_count<=0;reg_display_diag_reject<=0;
                reg_display_diag_width_bcd<=0;reg_display_diag_height_bcd<=0;reg_display_diag_area_bcd<=0;reg_display_diag_fill_bcd<=0;
                if(clear_counts)begin
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
                // COUNT的关联为帧间任务，等原子提交后再排BCD；不能沿用scan_done后三拍。
                if(result_done)begin
                    reg_pending_diag_count<=scan_diag_count;reg_pending_diag_reject<=scan_diag_reject;
                    reg_number_diag_width<=scan_diag_width;reg_number_diag_height<=scan_diag_height;
                    reg_number_diag_area<=scan_diag_area;reg_number_diag_fill<=scan_diag_fill;
                    cnt_pending_job<=cnt_pending_job+1'b1;
                    cnt_settle<=3; flag_pending_ready<=0; reg_pending_epoch<=scan_epoch;
                    reg_pending_valid<=mode ? {4'd0,multi_valid} : (scan_overflow ? 8'd0 : reg_work_valid);
                    reg_pending_color<=mode ? {8'd0,multi_color} : reg_work_color;
                    reg_pending_left<=mode ? {48'd0,multi_left} : reg_work_left;
                    reg_pending_right<=mode ? {48'd0,multi_right} : reg_work_right;
                    reg_pending_top<=mode ? {48'd0,multi_top} : reg_work_top;
                    reg_pending_bottom<=mode ? {48'd0,multi_bottom} : reg_work_bottom;
                    reg_pending_live<=multi_live;
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
                if(format_done && reg_format_epoch == epoch && reg_format_job == cnt_pending_job &&
                   !result_done)begin
                    flag_pending_ready<=1;
                    reg_pending_red_bcd<=bcd_red; reg_pending_green_bcd<=bcd_green; reg_pending_yellow_bcd<=bcd_yellow;
                    reg_pending_total_bcd<=bcd_total; reg_pending_x_bcd<=bcd_x; reg_pending_y_bcd<=bcd_y;
                    reg_pending_diag_width_bcd<=bcd_diag_width;reg_pending_diag_height_bcd<=bcd_diag_height;
                    reg_pending_diag_area_bcd<=bcd_diag_area;reg_pending_diag_fill_bcd<=bcd_diag_fill;
                end
                if(I_user && flag_pending_ready && reg_pending_epoch == epoch)begin
                    reg_display_valid<=reg_pending_valid; reg_display_color<=reg_pending_color;
                    reg_display_left<=reg_pending_left; reg_display_right<=reg_pending_right;
                    reg_display_top<=reg_pending_top; reg_display_bottom<=reg_pending_bottom;
                    reg_display_red_bcd<=reg_pending_red_bcd; reg_display_green_bcd<=reg_pending_green_bcd;
                    reg_display_yellow_bcd<=reg_pending_yellow_bcd; reg_display_total_bcd<=reg_pending_total_bcd;
                    reg_display_x_bcd<=reg_pending_x_bcd; reg_display_y_bcd<=reg_pending_y_bcd;
                    reg_display_track<=reg_pending_track; reg_display_gate<=reg_pending_gate; reg_display_reason<=reg_pending_reason;
                    reg_display_live<=reg_pending_live;
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
        .i_gain_red(reg_white_red),.i_gain_blue(reg_white_blue),
        .i_box_valid(reg_display_valid),.i_box_color(reg_display_color),.i_box_left(reg_display_left),.i_box_right(reg_display_right),
        .i_box_top(reg_display_top),.i_box_bottom(reg_display_bottom),.o_rgb(overlay_rgb),.o_valid(overlay_valid),
        .o_sof(overlay_sof),.o_eol(overlay_eol),.o_eof(overlay_eof),.o_x(overlay_x),.o_y(overlay_y));
    ball_status_osd osd_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(overlay_rgb),.i_valid(overlay_valid),
        .i_sof(overlay_sof),.i_eol(overlay_eol),.i_eof(overlay_eof),.i_x(overlay_x),.i_y(overlay_y),.i_count_mode(mode),.i_strict(strict),.i_live_count(reg_display_live),
        .i_camera_status(reg_camera_status),.i_display_white_busy(reg_white_status[2]),
        .i_display_white_ready(reg_white_status[1]),.i_display_white_error(reg_white_status[0]),
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
    assign O_error=front_error || scan_error || pack_error;
    assign O_red=red;
    assign O_green=green;
    assign O_yellow=yellow;
    assign O_total=total;
    assign O_count_mode=mode;
    assign O_gate_state=gate_state;
    assign O_track_status=track_status;
endmodule
