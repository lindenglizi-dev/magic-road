`timescale 1ns / 1ps
// 摄像头应用顶层：人脸门禁、小球检测、计数和显示，视频数据宽度96/128位。
module ball_runtime #(
    parameter C_WIDTH=1280, C_HEIGHT=720,
    parameter C_X_MIN=64, C_Y_MIN=160, C_X_END=1216, C_Y_END=640,
    parameter C_GATE_MIN=544, C_GATE_END=736, C_LINE=640, C_HYST=16,
    parameter C_MIN_AREA=128, C_MIN_SIZE=12, C_MAX_SIZE=384,
    parameter C_MAX_MOVE=64, C_DEBOUNCE=2100000, C_LONG_PRESS=103520000,
    parameter C_COUNT_MIN_SIZE=24,C_COUNT_MAX_SIZE=384,parameter [6:0] C_COUNT_COMPACT=27,
    parameter C_PREDECODE_MODE_CHANGE=0,
    parameter C_FACE_GATE=1, C_PANEL_CONFIG=0, C_COMBINED=0, C_VIEW_SWITCH=0, C_SHARED_INSPECTION_GAMMA=0, C_SERIAL_RENDER=0,
    parameter C_FACE_STUMPS="../rtl/face_rom/stumps.mem",
    parameter C_FACE_STAGES="../rtl/face_rom/stages.mem",
    parameter C_FACE_COORDINATES="../rtl/face_rom/coordinates.mem"
)(
    input [3:0] I_application_mode,
    input I_clk,
    input I_rst_n,
    input [3:0] I_keys_n,
    input [47:0] I_camera_status,
    input [191:0] I_settings,
    input I_panel_clear,
    output [31:0] O_good,
    output [31:0] O_bad,
    input [95:0] I_rgb,
    input [95:0] I_raw_rgb,
    input I_view_target,I_application_commit,
    input I_application_mode_change,
    output O_view_actual,O_view_commit,
    output [13:0] O_view_revision,
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
    output [7:0] O_seg_select_n,
    output [7:0] O_seg_segments_n,
    output [1535:0] O_status_snapshot,
    output O_status_valid,
    output [1:0] O_camera_step                                                                   
);
    wire mode,count_enable,strict,mask,clear_history,key_clear,clear_counts,face_relock;
    wire key_strict,key_clear_event,key_count_clear;
    wire panel_clear=C_PANEL_CONFIG && I_panel_clear;
    assign strict=C_PANEL_CONFIG ? I_settings[24] : key_strict;
    assign key_clear=key_clear_event || panel_clear;
    assign clear_counts=key_count_clear || panel_clear;
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
    wire [2:0] face_request_roi,face_result_roi;
    wire [11:0] face_request_x;
    wire face_capture_accept,face_result_accepted;
    reg [11:0] reg_guide_left,reg_guide_right;
    wire [11:0] face_left,face_right,face_top,face_bottom;
    wire [7:0] face_raw_count;
    reg flag_face_box,flag_display_face_box,flag_display_unlocked,flag_display_face_busy,flag_display_face_fault;
    reg [1:0] reg_display_confirmed;
    reg flag_display_face_pending;
    reg [31:0] reg_display_face_sample,reg_display_face_cycles;
    reg [15:0] reg_display_face_epoch;
    reg [7:0] reg_display_face_raw_count;
    reg [2:0] reg_display_face_roi;
    reg [11:0] reg_face_left,reg_face_right,reg_face_top,reg_face_bottom;
    reg [11:0] reg_display_face_left,reg_display_face_right,reg_display_face_top,reg_display_face_bottom;
    wire ball_enabled=face_unlocked && (!C_PANEL_CONFIG || I_settings[0]);
    // 锁定时统计已持续清零；解锁只提交epoch，无需再驱动统计清理扇出。
    wire detection_active=!C_COMBINED || I_application_mode==10;
    reg [3:0] previous_application_mode;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)previous_application_mode<=10;
        else if(I_user)previous_application_mode<=I_application_mode;
    end
                                                                                    
    wire mode_switch=C_COMBINED && I_user && (C_PREDECODE_MODE_CHANGE ?
        I_application_mode_change : previous_application_mode!=I_application_mode);
    // 仅复制已测得的高扇出清理驱动，逻辑值、优先级和生效时钟保持不变。
    (* max_fanout = 32 *) wire stats_clear=key_clear || !ball_enabled || mode_switch;
                                                                           
                                                                            
                                                                                
    reg reg_components_clear,reg_components_enable;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin reg_components_clear<=1;reg_components_enable<=0;end
        else begin reg_components_clear<=stats_clear;reg_components_enable<=ball_enabled && detection_active;end
    end
    wire components_clear=C_COMBINED ? reg_components_clear : stats_clear;
    wire components_enable=C_COMBINED ? reg_components_enable : ball_enabled && detection_active;
    wire [95:0] front_rgb;
                                                                                
    reg flag_view_active,flag_view_commit;
    reg [13:0] cnt_view_revision;
    reg view_front_first,view_front_second;
    wire view_target=(!C_VIEW_SWITCH || !detection_active) ? 1'b1 : I_view_target;
    wire view_for_input=I_user ? view_target : flag_view_active;
    wire [95:0] front_display_rgb=(C_VIEW_SWITCH && !view_for_input) ? I_raw_rgb : I_rgb;
    wire overlay_view;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            flag_view_active<=!C_VIEW_SWITCH;flag_view_commit<=0;cnt_view_revision<=0;
            view_front_first<=!C_VIEW_SWITCH;view_front_second<=!C_VIEW_SWITCH;
        end else begin
            flag_view_commit<=I_user;
            if(I_user)begin
                flag_view_active<=view_target;
                if(C_VIEW_SWITCH && (I_application_commit || view_target!=flag_view_active))
                    cnt_view_revision<=cnt_view_revision+1'b1;
            end
            view_front_first<=view_for_input;view_front_second<=view_front_first;
        end
    end
    assign O_view_actual=flag_view_active;
    assign O_view_commit=flag_view_commit;
    assign O_view_revision=cnt_view_revision;

    wire front_valid,front_sof,front_eol,front_eof,front_error,front_capture_fault;
    wire [11:0] front_x,front_y;
    wire [7:0] front_labels;
    wire [7:0] front_geometry_labels;
    wire [2:0] front_hits;
    wire [3:0] front_highlight;
    wire [15:0] front_epoch;
    wire scan_start,scan_valid,scan_done,scan_overflow,scan_fault,scan_error,scan_reject;
    wire [1:0] scan_color;
    wire [1:0] scan_shapes;
    wire [3:0] scan_shape_reject;
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
    // 退役任务只比较已提交epoch；新帧前端仍使用组合前视epoch。
    wire accept_frame=scan_epoch == active_epoch && !stats_clear;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    wire [2:0] gate_state,reason;
    wire [11:0] gate_x,gate_y;
    wire multi_done;
    wire [3:0] multi_valid;
    wire [7:0] multi_color;
    wire [7:0] multi_identity_color;
    wire [3:0] multi_predicted;
    wire [3:0] multi_quality_pending;
    wire [3:0] multi_good;
    wire [31:0] multi_reject_reason;
    wire [3:0] multi_raw_good;
    reg [31:0] reg_pending_reject_reason,reg_display_reject_reason;
    reg [3:0] reg_pending_raw_good,reg_display_raw_good;
    reg [31:0] reg_pending_good_count,reg_pending_bad_count,reg_display_good_count,reg_display_bad_count;
    reg [15:0] reg_display_result_epoch,reg_display_result_job;
    reg [31:0] cnt_processed_jobs,cnt_capture_faults;
    reg [3:0] reg_pending_good,reg_display_good;
    reg [3:0] reg_pending_quality_pending,reg_display_quality_pending;
    wire [47:0] multi_left,multi_right,multi_top,multi_bottom;
    wire [2:0] multi_live;
    reg [2:0] reg_pending_live,reg_display_live;
    reg [15:0] reg_count_epoch;
    wire result_done=multi_done && reg_count_epoch==active_epoch && !stats_clear;
    reg [3:0] reg_count_diag_count,reg_count_diag_reject;
    reg [11:0] reg_count_diag_width,reg_count_diag_height;
    reg [19:0] reg_count_diag_area;
    reg [6:0] reg_count_diag_fill;
    // 延后的COUNT结果使用本任务冻结诊断，不能读取下一帧的统计字段。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            reg_count_epoch<=0;reg_count_diag_count<=0;reg_count_diag_reject<=0;
            reg_count_diag_width<=0;reg_count_diag_height<=0;reg_count_diag_area<=0;reg_count_diag_fill<=0;
        end else if(stats_clear)begin reg_count_epoch<=epoch;end
        else begin
            if(scan_start && accept_frame)reg_count_epoch<=scan_epoch;
            if(scan_done && accept_frame)begin
                reg_count_diag_count<=scan_diag_count;reg_count_diag_reject<=scan_diag_reject;
                reg_count_diag_width<=scan_diag_width;reg_count_diag_height<=scan_diag_height;
                reg_count_diag_area<=scan_diag_area;reg_count_diag_fill<=scan_diag_fill;
            end
        end
    end
    reg reg_early_o;
    reg [7:0] reg_pending_valid,reg_display_valid;
    reg [15:0] reg_pending_color,reg_display_color;
    reg [95:0] reg_pending_left,reg_pending_right,reg_pending_top,reg_pending_bottom;
    reg [95:0] reg_display_left,reg_display_right,reg_display_top,reg_display_bottom;
    reg [15:0] reg_pending_epoch;
    reg [15:0] cnt_pending_job,reg_format_job,reg_format_epoch;
    reg [2:0] cnt_settle;
    reg flag_format_load,flag_pending_ready;
    reg [31:0] reg_number_red,reg_number_green,reg_number_yellow;
    reg [33:0] reg_number_total;
    reg [3:0] reg_pending_predicted,reg_display_predicted;
    reg [7:0] reg_pending_identity,reg_display_identity;
    
    wire [31:0] reg_pending_red_raw=reg_number_red;
    wire [31:0] reg_pending_green_raw=reg_number_green;
    wire [31:0] reg_pending_yellow_raw=reg_number_yellow;
    reg [31:0] reg_display_red_raw,reg_display_green_raw,reg_display_yellow_raw;
    reg [33:0] reg_display_total_raw;
    wire [33:0] reg_pending_total_raw=reg_number_total;
    reg [11:0] reg_display_diag_width_raw,reg_display_diag_height_raw;
    wire [11:0] reg_pending_diag_width_raw=reg_number_diag_width;
    wire [11:0] reg_pending_diag_height_raw=reg_number_diag_height;
    reg [19:0] reg_display_diag_area_raw;
    wire [19:0] reg_pending_diag_area_raw=reg_number_diag_area;
    reg [6:0] reg_display_diag_fill_raw;
    wire [6:0] reg_pending_diag_fill_raw=reg_number_diag_fill;
    reg [2:0] reg_pending_gate,reg_pending_reason,reg_display_gate,reg_display_reason;
    reg [39:0] bcd_red,bcd_green,bcd_yellow;
    reg [43:0] bcd_total;
    wire format_done;
    
    wire [39:0] reg_pending_red_bcd=bcd_red;
    wire [39:0] reg_pending_green_bcd=bcd_green;
    wire [39:0] reg_pending_yellow_bcd=bcd_yellow;
    
    wire [43:0] reg_pending_total_bcd=bcd_total;
    
    reg [39:0] reg_display_red_bcd,reg_display_green_bcd,reg_display_yellow_bcd;
    reg [43:0] reg_display_total_bcd;
    wire [95:0] overlay_rgb,osd_rgb;
    wire overlay_valid,overlay_sof,overlay_eol,overlay_eof;
    wire [11:0] overlay_x,overlay_y;
    wire osd_valid,osd_sof,osd_eol,osd_eof,pack_error;
                                                                              
                                                                               
    reg [1:0] cnt_render_lane,cnt_render_output_lane;
    reg [4:0] reg_render_flush;
    reg flag_render_active,flag_render_fault,reg_render_first;
    reg reg_render_input_eol,reg_render_input_eof;
    reg [71:0] reg_render_gather;
    reg [95:0] reg_render_rgb;
    reg reg_render_valid,reg_render_sof,reg_render_eol,reg_render_eof;
    wire [1:0] wire_render_lane=front_valid ? 2'd0 : cnt_render_lane;
    wire wire_render_scalar_valid=!I_user && (front_valid || cnt_render_lane!=0);
    wire [95:0] wire_render_rgb=C_SERIAL_RENDER ? {front_rgb[95-wire_render_lane*24-:24],72'd0} : front_rgb;
    wire [7:0] wire_render_labels=C_SERIAL_RENDER ? {6'd0,front_labels[wire_render_lane*2+:2]} : front_labels;
    wire [11:0] wire_render_x=C_SERIAL_RENDER ? front_x+{10'd0,wire_render_lane} : front_x;
    wire wire_render_valid=C_SERIAL_RENDER ? wire_render_scalar_valid : front_valid;
    wire wire_render_sof=C_SERIAL_RENDER ? wire_render_scalar_valid && wire_render_lane==0 && front_sof : front_sof;
    wire wire_render_eol=C_SERIAL_RENDER ? wire_render_scalar_valid && wire_render_lane==3 && reg_render_input_eol : front_eol;
    wire wire_render_eof=C_SERIAL_RENDER ? wire_render_scalar_valid && wire_render_lane==3 && reg_render_input_eof : front_eof;
    wire [1:0] wire_render_output_lane=osd_sof ? 2'd0 : cnt_render_output_lane;
    wire [95:0] wire_pack_rgb=C_SERIAL_RENDER ? reg_render_rgb : osd_rgb;
    wire wire_pack_valid=C_SERIAL_RENDER ? reg_render_valid : osd_valid;
    wire wire_pack_sof=C_SERIAL_RENDER ? reg_render_sof : osd_sof;
    wire wire_pack_eol=C_SERIAL_RENDER ? reg_render_eol : osd_eol;
    wire wire_pack_eof=C_SERIAL_RENDER ? reg_render_eof : osd_eof;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            cnt_render_lane<=0;cnt_render_output_lane<=0;reg_render_flush<=0;
            flag_render_active<=0;flag_render_fault<=0;reg_render_first<=0;
            reg_render_input_eol<=0;reg_render_input_eof<=0;
            reg_render_gather<=0;reg_render_rgb<=0;
            reg_render_valid<=0;reg_render_sof<=0;reg_render_eol<=0;reg_render_eof<=0;
        end else if(I_user)begin
            cnt_render_lane<=0;cnt_render_output_lane<=0;reg_render_flush<=5'b11111;
            flag_render_active<=0;flag_render_fault<=0;reg_render_first<=0;
            reg_render_input_eol<=0;reg_render_input_eof<=0;
            reg_render_valid<=0;reg_render_sof<=0;reg_render_eol<=0;reg_render_eof<=0;
        end else begin
            reg_render_flush<={reg_render_flush[3:0],1'b0};
            reg_render_valid<=0;reg_render_sof<=0;reg_render_eol<=0;reg_render_eof<=0;
            if(front_valid)begin
                if(cnt_render_lane!=0)flag_render_fault<=1;
                reg_render_input_eol<=front_eol;reg_render_input_eof<=front_eof;
                cnt_render_lane<=1;
            end else if(cnt_render_lane!=0)cnt_render_lane<=cnt_render_lane+1'b1;
                                                                             
                                                                     
            if(osd_valid && reg_render_flush==0 && (flag_render_active || osd_sof))begin
                if(osd_sof && flag_render_active)flag_render_fault<=1;
                if((osd_eol || osd_eof) && wire_render_output_lane!=3)begin
                    flag_render_fault<=1;flag_render_active<=0;cnt_render_output_lane<=0;
                end else begin
                    if(osd_sof)flag_render_active<=1;
                    reg_render_gather<={reg_render_gather[47:0],osd_rgb[95:72]};
                    if(wire_render_output_lane==0)reg_render_first<=osd_sof;
                    if(wire_render_output_lane==3)begin
                        cnt_render_output_lane<=0;reg_render_rgb<={reg_render_gather,osd_rgb[95:72]};
                        reg_render_valid<=1;reg_render_sof<=reg_render_first;
                        reg_render_eol<=osd_eol;reg_render_eof<=osd_eof;
                        if(osd_eof)flag_render_active<=0;
                    end else cnt_render_output_lane<=wire_render_output_lane+1'b1;
                end
            end
        end
    end


    generate
        if(C_FACE_GATE)begin:gen_face_gate
            face_detector #(.C_STUMPS(C_FACE_STUMPS),.C_STAGES(C_FACE_STAGES),.C_COORDINATES(C_FACE_COORDINATES)) detector_Inst(
                .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(key_clear),.i_enable(!face_unlocked),
                .i_request_roi(face_request_roi),.i_request_x(face_request_x),
                .i_rgb(front_rgb),.i_valid(front_valid),.i_sof(front_sof),.i_eof(front_eof),.i_error(front_error),
                .i_x(front_x),.i_y(front_y),.i_epoch(front_epoch),.o_busy(face_busy),.o_done(face_done),
                .o_positive(face_positive),.o_fault(face_fault),.o_sample(face_sample),.o_epoch(face_epoch),.o_cycles(face_cycles),
                .o_left(face_left),.o_right(face_right),.o_top(face_top),.o_bottom(face_bottom),.o_raw_count(face_raw_count),
                .o_roi_id(face_result_roi),.o_capture_accept(face_capture_accept));
            face_gate_control gate_Inst(.i_clk(I_clk),.i_rstn(I_rst_n),.i_early(I_user),
                .i_session_clear(key_clear),.i_relock(face_relock),.i_result(face_done),.i_positive(face_positive),.i_fault(face_fault),
                .i_sample(face_sample),.i_result_epoch(face_epoch),.i_epoch(active_epoch),.i_result_roi(face_result_roi),
                .o_unlocked(face_unlocked),.o_restart(face_restart),.o_confirmed(face_confirmed),.o_pending(face_pending),
                .o_request_roi(face_request_roi),.o_request_x(face_request_x),.o_result_accepted(face_result_accepted));
        end else begin:gen_ball_regression
            // 无人脸构建直接启用小球；检测器与模型ROM在编译时移除。
            assign face_unlocked=1'b1;assign face_restart=1'b0;assign face_busy=1'b0;assign face_done=1'b0;
            assign face_positive=1'b0;assign face_fault=1'b0;assign face_pending=1'b0;assign face_confirmed=2'd0;
            assign face_sample=32'd0;assign face_cycles=32'd0;assign face_epoch=16'd0;assign face_raw_count=8'd0;
            assign face_request_roi=3'd0;assign face_result_roi=3'd0;assign face_request_x=12'd512;
            assign face_capture_accept=1'b0;assign face_result_accepted=1'b0;
            assign face_left=12'd0;assign face_right=12'd0;assign face_top=12'd0;assign face_bottom=12'd0;
        end
    endgenerate
    // 人脸状态与框也在CSI帧边界冻结，随后随RGB经DDR到HDMI，不裸跨多位总线。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            flag_face_box<=0;flag_display_face_box<=0;flag_display_unlocked<=!C_FACE_GATE;
            flag_display_face_busy<=0;flag_display_face_fault<=0;reg_display_confirmed<=0;
            flag_display_face_pending<=0;reg_display_face_sample<=0;reg_display_face_cycles<=0;
            reg_display_face_epoch<=0;reg_display_face_raw_count<=0;reg_display_face_roi<=0;
            reg_guide_left<=512;reg_guide_right<=767;
            reg_face_left<=0;reg_face_right<=0;reg_face_top<=0;reg_face_bottom<=0;
            reg_display_face_left<=0;reg_display_face_right<=0;reg_display_face_top<=0;reg_display_face_bottom<=0;
        end else begin
            // 与真实采集接受同拍冻结引导区，不能在更早的I_user取未来轮询索引。
            if(face_capture_accept)begin
                reg_guide_left<=face_request_x;reg_guide_right<=face_request_x+12'd255;
            end
            if(key_clear)flag_face_box<=0;
            else if(face_result_accepted)begin
                flag_face_box<=face_positive && !face_fault;
                reg_face_left<=face_left;reg_face_right<=face_right;reg_face_top<=face_top;reg_face_bottom<=face_bottom;
            end
            if(I_user)begin
                flag_display_unlocked<=!C_FACE_GATE || (!face_relock && (face_unlocked || face_restart));
                flag_display_face_box<=flag_face_box && !face_unlocked && !face_restart && !clear_history;
                flag_display_face_busy<=face_busy;flag_display_face_fault<=face_fault;reg_display_confirmed<=face_confirmed;
                flag_display_face_pending<=face_pending && !face_restart && !face_relock;
                reg_display_face_sample<=face_sample;reg_display_face_cycles<=face_cycles;
                reg_display_face_epoch<=face_epoch;reg_display_face_raw_count<=face_raw_count;reg_display_face_roi<=face_result_roi;
                reg_display_face_left<=reg_face_left;reg_display_face_right<=reg_face_right;
                reg_display_face_top<=reg_face_top;reg_display_face_bottom<=reg_face_bottom;
            end
        end
    end
    ball_key_control #(.C_DEBOUNCE(C_DEBOUNCE),.C_LONG_PRESS(C_LONG_PRESS)) keys_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_keys_n(I_keys_n),.i_early(I_user),
        .i_session_restart(face_restart || panel_clear || mode_switch),
        .o_count_mode(mode),.o_count_enable(count_enable),.o_strict(key_strict),.o_mask(mask),.o_epoch(epoch),.o_active_epoch(active_epoch),
        .o_clear(clear_history),.o_key_clear(key_clear_event),.o_clear_counts(key_count_clear),.o_face_relock(face_relock),.o_camera_step(O_camera_step),.o_white_calibrate());
    ball_stream_front #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_CHECK_LAST(1),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_PANEL_CONFIG(C_PANEL_CONFIG),.C_DISPLAY_SOURCE(C_VIEW_SWITCH),.C_SERIAL_CLASSIFY(1),.C_SHARED_GAMMA(C_SHARED_INSPECTION_GAMMA)) front_Inst(
        .i_apply_gamma(C_SHARED_INSPECTION_GAMMA && detection_active),
        .i_display_source_gamma(C_SHARED_INSPECTION_GAMMA && detection_active && (!C_VIEW_SWITCH || view_for_input)),
        .i_settings(I_settings),
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(I_rgb),.i_display_rgb(front_display_rgb),.i_valid(I_valid),.i_early(I_user),.i_last(I_last),.i_strict(strict),.i_epoch(epoch),
        .o_rgb(front_rgb),.o_valid(front_valid),.o_sof(front_sof),.o_eol(front_eol),.o_eof(front_eof),
        .o_x(front_x),.o_y(front_y),.o_labels(front_labels),.o_geometry_labels(front_geometry_labels),.o_gate_hits(front_hits),.o_epoch(front_epoch),.o_error(front_error),.o_highlight(front_highlight),
        .o_capture_fault(front_capture_fault));
    ball_components #(.C_WIDTH(C_WIDTH),.C_HEIGHT(C_HEIGHT),.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),
        .C_X_END(C_X_END),.C_Y_END(C_Y_END),.C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_MIN_AREA(C_MIN_AREA),
        .C_MIN_SIZE(C_MIN_SIZE),.C_MAX_SIZE(C_MAX_SIZE),.C_ROUND_MIN_SIZE(C_COUNT_MIN_SIZE),
        .C_ROUND_MAX_SIZE(C_COUNT_MAX_SIZE),.C_ROUND_COMPACT(C_COUNT_COMPACT),.C_HIGHLIGHT_REPAIR(1),.C_PANEL_CONFIG(C_PANEL_CONFIG),.C_FRAME_CHECK(1)) components_Inst(
        .i_settings(I_settings),.o_shape_flags(scan_shapes),.o_shape_reject(scan_shape_reject),.i_capture_fault(front_capture_fault),
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_session_clear(components_clear),
        .i_valid(front_valid && components_enable),.i_sof(front_sof && components_enable),.i_eof(front_eof && components_enable),
        .i_x(front_x),.i_y(front_y),.i_labels(front_geometry_labels),.i_highlight(front_highlight),.i_gate_hits(front_hits),.i_epoch(front_epoch),.i_shape_enable(1'b1),
        .o_frame_start(scan_start),.o_candidate_valid(scan_valid),.o_reject_valid(scan_reject),.o_color(scan_color),.o_area(scan_area),
        .o_x_min(scan_left),.o_x_max(scan_right),.o_y_min(scan_top),.o_y_max(scan_bottom),
        .o_frame_done(scan_done),.o_gate_pixels(scan_gate),.o_gate_occupied(scan_gate_occupied),.o_epoch(scan_epoch),
        .o_overflow(scan_overflow),.o_fault(scan_fault),.o_error(scan_error),
        .o_diag_count(scan_diag_count),.o_diag_width(scan_diag_width),.o_diag_height(scan_diag_height),
        .o_diag_area(scan_diag_area),.o_diag_fill(scan_diag_fill),.o_diag_reject(scan_diag_reject));
                                                                                 
    reg [49:0] reg_candidate_measure,reg_candidate_ready;
    reg [12:0] reg_candidate_width,reg_candidate_height;
    reg [19:0] reg_candidate_area,reg_ready_area;
    reg [1:0] reg_candidate_shapes;
    reg [3:0] reg_candidate_shape_reject;
    reg [7:0] reg_ready_reject_reason;
    reg reg_measure_start,reg_measure_valid,reg_measure_done;
    reg reg_ready_start,reg_ready_valid,reg_ready_done,reg_ready_good,reg_ready_considered;
    reg [11:0] reg_line_low,reg_line_high;
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            reg_candidate_measure<=0;reg_candidate_ready<=0;
            reg_candidate_width<=0;reg_candidate_height<=0;reg_candidate_area<=0;reg_ready_area<=0;reg_candidate_shapes<=0;
            reg_candidate_shape_reject<=0;reg_ready_reject_reason<=0;
            reg_measure_start<=0;reg_measure_valid<=0;reg_measure_done<=0;
            reg_ready_start<=0;reg_ready_valid<=0;reg_ready_done<=0;reg_ready_good<=0;reg_ready_considered<=0;
            reg_line_low<=C_LINE-C_HYST;reg_line_high<=C_LINE+C_HYST;
        end else begin
            if(I_user && C_PANEL_CONFIG)begin
                reg_line_low<=I_settings[171:160]-C_HYST;
                reg_line_high<=I_settings[171:160]+C_HYST;
            end
            if(stats_clear)begin
                reg_measure_start<=0;reg_measure_valid<=0;reg_measure_done<=0;
                reg_ready_start<=0;reg_ready_valid<=0;reg_ready_done<=0;
            end else begin
                reg_measure_start<=scan_start && accept_frame;
                reg_measure_valid<=scan_valid && accept_frame && scan_color!=0 &&
                    (I_settings[9:8]==0 || scan_color==I_settings[9:8]);
                reg_measure_done<=scan_done && accept_frame;
                reg_candidate_measure<={scan_color,scan_left,scan_right,scan_top,scan_bottom};
                reg_candidate_width<={1'b0,scan_right}-{1'b0,scan_left}+13'd1;
                reg_candidate_height<={1'b0,scan_bottom}-{1'b0,scan_top}+13'd1;
                reg_candidate_area<=scan_area;reg_candidate_shapes<=scan_shapes;reg_candidate_shape_reject<=scan_shape_reject;
                reg_ready_start<=reg_measure_start;reg_ready_valid<=reg_measure_valid;reg_ready_done<=reg_measure_done;
                reg_candidate_ready<=reg_candidate_measure;
                reg_ready_area<=reg_candidate_area;
                reg_ready_considered<=reg_candidate_measure[49:48]!=0 &&
                    (I_settings[9:8]==0 || reg_candidate_measure[49:48]==I_settings[9:8]);
                reg_ready_reject_reason[0]<=reg_candidate_width<I_settings[111:96] || reg_candidate_width>I_settings[127:112];
                reg_ready_reject_reason[1]<=reg_candidate_height<I_settings[143:128] || reg_candidate_height>I_settings[159:144];
                reg_ready_reject_reason[2]<=reg_candidate_area<{4'd0,I_settings[191:176]};
                reg_ready_reject_reason[3]<=!((I_settings[23:16]==0) ||
                    (I_settings[23:16]==1 && reg_candidate_shapes[0]) || (I_settings[23:16]==2 && reg_candidate_shapes[1]));
                reg_ready_reject_reason[4]<=reg_candidate_measure[49:48]==0 ||
                    (I_settings[9:8]!=0 && reg_candidate_measure[49:48]!=I_settings[9:8]);
                reg_ready_reject_reason[5]<=I_settings[23:16]==1 && reg_candidate_shape_reject[0];
                reg_ready_reject_reason[6]<=I_settings[23:16]==1 && reg_candidate_shape_reject[1];
                reg_ready_reject_reason[7]<=I_settings[23:16]==1 && (reg_candidate_shape_reject[2] || reg_candidate_shape_reject[3]);
                reg_ready_good<=reg_candidate_measure[49:48]!=0 &&
                    (I_settings[9:8]==0 || reg_candidate_measure[49:48]==I_settings[9:8]) &&
                    reg_candidate_width>=I_settings[111:96] && reg_candidate_width<=I_settings[127:112] &&
                    reg_candidate_height>=I_settings[143:128] && reg_candidate_height<=I_settings[159:144] &&
                    reg_candidate_area>={4'd0,I_settings[191:176]} &&
                    (I_settings[23:16]==0 || (I_settings[23:16]==1 && reg_candidate_shapes[0]) ||
                     (I_settings[23:16]==2 && reg_candidate_shapes[1]));
            end
        end
    end
    ball_multi_counter #(.C_MAX_MOVE(C_MAX_MOVE),.C_LINE(C_LINE),.C_HYST(C_HYST),.C_PANEL_CONFIG(C_PANEL_CONFIG),
        .C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_X_END(C_X_END),.C_Y_END(C_Y_END)) counter_Inst(
        .i_settings(I_settings),.i_line_low(reg_line_low),.i_line_high(reg_line_high),
        .i_good(reg_ready_good),.i_considered(reg_ready_considered),.o_good(O_good),.o_bad(O_bad),.o_box_good(multi_good),
        .i_reject_reason(reg_ready_reject_reason),.o_box_reject_reason(multi_reject_reason),.o_box_raw_good(multi_raw_good),
        .o_box_quality_pending(multi_quality_pending),
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(stats_clear),.i_clear_counts(clear_counts || !ball_enabled),.i_fault(scan_fault && !stats_clear),
        .i_count_enable(count_enable && detection_active),.i_frame_start(C_PANEL_CONFIG ? reg_ready_start : scan_start && accept_frame),
        .i_candidate_valid(C_PANEL_CONFIG ? reg_ready_valid : scan_valid && accept_frame),
        .i_color(C_PANEL_CONFIG ? reg_candidate_ready[49:48] : scan_color),
        .i_area(C_PANEL_CONFIG ? reg_ready_area : scan_area),
        .i_x_min(C_PANEL_CONFIG ? reg_candidate_ready[47:36] : scan_left),.i_x_max(C_PANEL_CONFIG ? reg_candidate_ready[35:24] : scan_right),
        .i_y_min(C_PANEL_CONFIG ? reg_candidate_ready[23:12] : scan_top),.i_y_max(C_PANEL_CONFIG ? reg_candidate_ready[11:0] : scan_bottom),
        .i_frame_done(C_PANEL_CONFIG ? reg_ready_done : scan_done && accept_frame),.i_overflow(scan_overflow),
        .o_red(red),.o_yellow(yellow),.o_green(green),.o_total(total),.o_state(gate_state),
        .o_reason(reason),.o_center_x(gate_x),.o_center_y(gate_y),.o_done(multi_done),.o_busy(),
        .o_active_count(multi_live),.o_box_valid(multi_valid),.o_box_color(multi_color),
        .o_box_predicted(multi_predicted),.o_identity_color(multi_identity_color),
        .o_box_left(multi_left),.o_box_right(multi_right),.o_box_top(multi_top),.o_box_bottom(multi_bottom));

    // start/done之间只写工作副本；帧显示使用另一份冻结副本。
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            reg_early_o<=0; cnt_settle<=0; flag_format_load<=0; flag_pending_ready<=0;
            cnt_pending_job<=0; reg_format_job<=0; reg_format_epoch<=0;
            reg_pending_valid<=0; reg_pending_color<=0; reg_pending_left<=0; reg_pending_right<=0;
            reg_pending_top<=0; reg_pending_bottom<=0; reg_pending_epoch<=0;
            reg_display_valid<=0; reg_display_color<=0; reg_display_left<=0; reg_display_right<=0;
            reg_display_top<=0; reg_display_bottom<=0;
            reg_number_red<=0; reg_number_green<=0; reg_number_yellow<=0; reg_number_total<=0;
            reg_pending_predicted<=0;reg_display_predicted<=0;reg_pending_identity<=0;reg_display_identity<=0;
            reg_pending_good<=0;reg_display_good<=0;
            reg_pending_quality_pending<=0;reg_display_quality_pending<=0;
            reg_pending_reject_reason<=0;reg_display_reject_reason<=0;
            reg_pending_raw_good<=0;reg_display_raw_good<=0;
            reg_pending_good_count<=0;reg_pending_bad_count<=0;reg_display_good_count<=0;reg_display_bad_count<=0;
            reg_display_result_epoch<=0;reg_display_result_job<=0;
            
            reg_display_red_raw<=0;reg_display_green_raw<=0;reg_display_yellow_raw<=0;reg_display_total_raw<=0;
            
            reg_display_diag_width_raw<=0;reg_display_diag_height_raw<=0;reg_display_diag_area_raw<=0;reg_display_diag_fill_raw<=0;
            reg_pending_gate<=0; reg_pending_reason<=0;
            reg_pending_live<=0;reg_display_live<=0;
            reg_display_gate<=0; reg_display_reason<=0;
              
              
            reg_display_red_bcd<=0; reg_display_green_bcd<=0; reg_display_yellow_bcd<=0;
            reg_display_total_bcd<=0;
            reg_pending_diag_count<=0;reg_pending_diag_reject<=0;reg_display_diag_count<=0;reg_display_diag_reject<=0;
            reg_number_diag_width<=0;reg_number_diag_height<=0;reg_number_diag_area<=0;reg_number_diag_fill<=0;
        end else begin
            reg_early_o<=I_user; flag_format_load<=0;
            if(flag_format_load)begin reg_format_job<=cnt_pending_job; reg_format_epoch<=reg_pending_epoch; end
            if(stats_clear)begin
                cnt_pending_job<=cnt_pending_job+1'b1;
                cnt_settle<=0; flag_pending_ready<=0;
                reg_pending_valid<=0; reg_display_valid<=0;
                reg_pending_predicted<=0;reg_display_predicted<=0;reg_pending_good<=0;reg_display_good<=0;
                reg_pending_quality_pending<=0;reg_display_quality_pending<=0;
                reg_pending_reject_reason<=0;reg_display_reject_reason<=0;
                reg_pending_raw_good<=0;reg_display_raw_good<=0;
                reg_display_result_epoch<=epoch;reg_display_result_job<=cnt_pending_job+1'b1;
                reg_pending_epoch<=epoch; reg_display_gate<=0; reg_display_reason<=0;
                reg_pending_live<=0;reg_display_live<=0;
                reg_pending_diag_count<=0;reg_pending_diag_reject<=0;reg_display_diag_count<=0;reg_display_diag_reject<=0;
                reg_display_diag_width_raw<=0;reg_display_diag_height_raw<=0;reg_display_diag_area_raw<=0;reg_display_diag_fill_raw<=0;
                if(clear_counts || !ball_enabled)begin
                    reg_pending_good_count<=0;reg_pending_bad_count<=0;reg_display_good_count<=0;reg_display_bad_count<=0;
                    reg_display_red_raw<=0;reg_display_green_raw<=0;reg_display_yellow_raw<=0;reg_display_total_raw<=0;
                    reg_display_red_bcd<=0; reg_display_green_bcd<=0;
                    reg_display_yellow_bcd<=0; reg_display_total_bcd<=0;
                end
            end else begin
                if(result_done)begin
                    reg_pending_diag_count<=reg_count_diag_count;reg_pending_diag_reject<=reg_count_diag_reject;
                    reg_number_diag_width<=reg_count_diag_width;reg_number_diag_height<=reg_count_diag_height;
                    reg_number_diag_area<=reg_count_diag_area;reg_number_diag_fill<=reg_count_diag_fill;
                    cnt_pending_job<=cnt_pending_job+1'b1;
                    cnt_settle<=4; flag_pending_ready<=0; reg_pending_epoch<=reg_count_epoch;
                    reg_pending_valid<={4'd0,multi_valid};reg_pending_color<={8'd0,multi_color};
                    reg_pending_identity<=multi_identity_color;reg_pending_predicted<=multi_predicted;reg_pending_good<=multi_good;
                    reg_pending_quality_pending<=multi_quality_pending;
                    reg_pending_reject_reason<=multi_reject_reason;reg_pending_raw_good<=multi_raw_good;
                    reg_pending_good_count<=O_good;reg_pending_bad_count<=O_bad;
                    reg_pending_left<={48'd0,multi_left};reg_pending_right<={48'd0,multi_right};
                    reg_pending_top<={48'd0,multi_top};reg_pending_bottom<={48'd0,multi_bottom};
                    reg_pending_live<=multi_live;
                end else if(cnt_settle != 0)begin
                    cnt_settle<=cnt_settle-1'b1;
                    if(cnt_settle == 1)begin
                        flag_format_load<=1;
                        reg_number_red<=red; reg_number_green<=green; reg_number_yellow<=yellow; reg_number_total<=total;
                        reg_pending_gate<=gate_state; reg_pending_reason<=scan_overflow ? 3'd1 : reason;
                    end
                end
                if(format_done && reg_format_epoch == active_epoch && reg_format_job == cnt_pending_job &&
                   !result_done)begin
                    flag_pending_ready<=1;
                      
                      
                    
                    
                    
                    
                    
                    
                end
                // 无脸会话由stats_clear优先取消ready；格式完成时已校验epoch/job。
                if(I_user && flag_pending_ready && (C_FACE_GATE ? reg_pending_epoch == active_epoch : 1'b1))begin
                    reg_display_valid<=reg_pending_valid; reg_display_color<=reg_pending_color;
                    reg_display_left<=reg_pending_left; reg_display_right<=reg_pending_right;
                    reg_display_top<=reg_pending_top; reg_display_bottom<=reg_pending_bottom;
                    reg_display_red_bcd<=reg_pending_red_bcd; reg_display_green_bcd<=reg_pending_green_bcd;
                    reg_display_yellow_bcd<=reg_pending_yellow_bcd; reg_display_total_bcd<=reg_pending_total_bcd;
                    reg_display_gate<=reg_pending_gate; reg_display_reason<=reg_pending_reason;
                    reg_display_identity<=reg_pending_identity;reg_display_predicted<=reg_pending_predicted;reg_display_good<=reg_pending_good;
                    reg_display_quality_pending<=reg_pending_quality_pending;
                    reg_display_reject_reason<=reg_pending_reject_reason;reg_display_raw_good<=reg_pending_raw_good;
                    reg_display_good_count<=reg_pending_good_count;reg_display_bad_count<=reg_pending_bad_count;
                    reg_display_result_epoch<=reg_pending_epoch;reg_display_result_job<=cnt_pending_job;
                    reg_display_red_raw<=reg_pending_red_raw;reg_display_green_raw<=reg_pending_green_raw;
                    reg_display_yellow_raw<=reg_pending_yellow_raw;reg_display_total_raw<=reg_pending_total_raw;
                    reg_display_diag_width_raw<=reg_pending_diag_width_raw;reg_display_diag_height_raw<=reg_pending_diag_height_raw;
                    reg_display_diag_area_raw<=reg_pending_diag_area_raw;reg_display_diag_fill_raw<=reg_pending_diag_fill_raw;
                    reg_display_live<=reg_pending_live;
                    reg_display_diag_count<=reg_pending_diag_count;reg_display_diag_reject<=reg_pending_diag_reject;
                end
            end
        end
    end
    // 一份34位转换器顺序处理三色和总计四个冻结字段，完成后原epoch/job检查一次提交。
    reg [1:0] cnt_format_field;
    reg flag_format_active,reg_format_done;
    reg [33:0] dec_format_binary;
    wire [43:0] wire_format_bcd;
    wire flag_decimal_done;
    wire flag_decimal_load=!stats_clear && (flag_format_load ||
        (flag_format_active && flag_decimal_done && cnt_format_field < 3));
    wire [1:0] wire_format_field=flag_format_load ? 2'd0 : cnt_format_field+1'b1;
    assign format_done=reg_format_done;
    always @(*)begin
        dec_format_binary=0;
        case(wire_format_field)
            0:dec_format_binary={2'd0,reg_number_red};
            1:dec_format_binary={2'd0,reg_number_green};
            2:dec_format_binary={2'd0,reg_number_yellow};
            3:dec_format_binary=reg_number_total;
            default:begin end
        endcase
    end
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            cnt_format_field<=0;flag_format_active<=0;reg_format_done<=0;
            bcd_red<=0;bcd_green<=0;bcd_yellow<=0;bcd_total<=0;
        end else begin
            reg_format_done<=0;
            if(stats_clear)begin flag_format_active<=0;end
            else if(flag_format_load)begin cnt_format_field<=0;flag_format_active<=1;end
            else if(flag_decimal_done && flag_format_active)begin
                case(cnt_format_field)
                    0:bcd_red<=wire_format_bcd[39:0];
                    1:bcd_green<=wire_format_bcd[39:0];
                    2:bcd_yellow<=wire_format_bcd[39:0];
                    3:bcd_total<=wire_format_bcd;
                    default:begin end
                endcase
                if(cnt_format_field == 3)begin flag_format_active<=0;reg_format_done<=1;end
                else cnt_format_field<=cnt_format_field+1'b1;
            end
        end
    end
    ball_decimal_format #(.C_BITS(34),.C_DIGITS(11)) shared_decimal_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_load(flag_decimal_load),.i_binary(dec_format_binary),
        .o_bcd(wire_format_bcd),.o_done(flag_decimal_done),.o_busy());
    ball_overlay #(.C_X_MIN(C_X_MIN),.C_Y_MIN(C_Y_MIN),.C_X_END(C_X_END),.C_Y_END(C_Y_END),
        .C_GATE_MIN(C_GATE_MIN),.C_GATE_END(C_GATE_END),.C_LINE(C_LINE),.C_HYST(C_HYST),.C_PANEL_CONFIG(C_PANEL_CONFIG),.C_VIEW_SWITCH(C_VIEW_SWITCH)) overlay_Inst(
        .i_settings(detection_active?I_settings:(I_settings & ~(192'd1<<25))),.i_box_good(reg_display_good),.i_box_predicted(reg_display_predicted),
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_view_ball(view_front_second),.o_view_ball(overlay_view),.i_rgb(wire_render_rgb),.i_valid(wire_render_valid),.i_sof(wire_render_sof),.i_eol(wire_render_eol),.i_eof(wire_render_eof),
        .i_x(wire_render_x),.i_y(front_y),.i_labels(wire_render_labels),.i_mask(mask && detection_active),.i_count_mode(mode),
        .i_gain_red(18'd65536),.i_gain_blue(18'd65536),
        .i_face_locked(!flag_display_unlocked),.i_face_guide_left(reg_guide_left),.i_face_guide_right(reg_guide_right),.i_face_valid(flag_display_face_box),
        .i_face_left(reg_display_face_left),.i_face_right(reg_display_face_right),
        .i_face_top(reg_display_face_top),.i_face_bottom(reg_display_face_bottom),
        .i_box_valid(detection_active?reg_display_valid:8'd0),.i_box_color(reg_display_color),.i_box_left(reg_display_left),.i_box_right(reg_display_right),
        .i_box_top(reg_display_top),.i_box_bottom(reg_display_bottom),.o_rgb(overlay_rgb),.o_valid(overlay_valid),
        .o_sof(overlay_sof),.o_eol(overlay_eol),.o_eof(overlay_eof),.o_x(overlay_x),.o_y(overlay_y));
    ball_status_osd #(.C_FACE_GATE(C_FACE_GATE),.C_COMBINED(C_COMBINED),.C_VIEW_SWITCH(C_VIEW_SWITCH),.C_SCALAR_RENDER(C_SERIAL_RENDER),.C_PREDECODE(C_SERIAL_RENDER)) osd_Inst(.i_view_ball(overlay_view),.i_application_mode(I_application_mode),.i_clk(I_clk),.i_rstn(I_rst_n),.i_rgb(overlay_rgb),.i_valid(overlay_valid),
        .i_sof(overlay_sof),.i_eol(overlay_eol),.i_eof(overlay_eof),.i_x(overlay_x),.i_y(overlay_y),.i_count_mode(1'b1),.i_count_enable(count_enable),.i_strict(1'b0),
        .i_camera_status(reg_camera_status),
        .i_face_unlocked(1'b0),.i_face_busy(1'b0),
        .i_live_count(reg_display_live),.i_display_white_busy(1'b0),
        .i_display_white_ready(1'b0),.i_display_white_error(1'b0),
        .i_face_confirmed(2'd0),.i_face_fault(1'b0),
        .i_diag_count(4'd0),.i_diag_reject(4'd0),
        .i_diag_width_bcd(16'd0),.i_diag_height_bcd(16'd0),
        .i_diag_area_bcd(28'd0),.i_diag_fill_bcd(12'd0),
        .i_red_bcd(reg_display_red_bcd),.i_green_bcd(reg_display_green_bcd),.i_yellow_bcd(reg_display_yellow_bcd),
        .i_total_bcd(reg_display_total_bcd),.i_x_bcd(16'd0),.i_y_bcd(16'd0),
        .i_gate_state(3'd0),.i_track_status(2'd0),.i_reason(O_error ? 3'd7 : reg_display_reason),
        .o_rgb(osd_rgb),.o_valid(osd_valid),.o_sof(osd_sof),.o_eol(osd_eol),.o_eof(osd_eof));
    rgb96_pack128_valid pack_Inst(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_rgb(wire_pack_rgb),.I_valid(wire_pack_valid),
        .I_user(wire_pack_sof),.I_last(wire_pack_eol),.I_done(wire_pack_eof),.O_data(O_data),.O_valid(O_valid),.O_last(O_last),.O_done(O_done),.O_error(pack_error));
    assign O_early=reg_early_o;
    // E页按形状/尺寸筛除候选累计；同一候选命中多条规则仍只产生一拍。
    // 采用同一CSI时钟和已提交epoch门控，清零/重锁取消旧会话事件。
    wire [27:0] reject_bcd;
    ball_segment_display segment_Inst(
        .i_clk(I_clk),.i_rstn(I_rst_n),.i_clear(clear_counts || !ball_enabled),
        .i_red_bcd(reg_display_red_bcd),.i_green_bcd(reg_display_green_bcd),
        .i_yellow_bcd(reg_display_yellow_bcd),.i_reject_valid(scan_reject && accept_frame),
        .o_select_n(O_seg_select_n),.o_segments_n(O_seg_segments_n),.o_reject_bcd(reject_bcd));

                                                                                   
                                                                                     
                                                                                    
    reg [31:0] input_frame_seq;
    reg [1535:0] status_data;
    reg [12:0] status_center_x,status_center_y;
    integer status_slot,status_offset;
    always @(*)begin
        status_data=0;status_center_x=0;status_center_y=0;status_offset=0;
        status_data[0*8+:8]=8'd1;
        status_data[1*8+:8]={flag_display_face_box,flag_display_face_pending,
            flag_display_face_fault,flag_display_face_busy,flag_display_unlocked,mask,strict,!count_enable};
        status_data[2*8+:8]={6'd0,reg_display_confirmed};
        status_data[3*8+:8]={5'd0,reg_display_face_roi};
        status_data[4*8+:16]=active_epoch;
        status_data[6*8+:16]=reg_display_face_epoch;
        status_data[8*8+:32]=input_frame_seq;
        status_data[12*8+:32]=reg_display_face_sample;status_data[16*8+:32]=reg_display_face_cycles;
        status_data[20*8+:32]=reg_display_red_raw;
        status_data[24*8+:32]=reg_display_green_raw;
        status_data[28*8+:32]=reg_display_yellow_raw;
        status_data[32*8+:64]={30'd0,reg_display_total_raw};
        status_data[40*8+:32]={4'd0,reject_bcd};
        status_data[44*8+:8]={4'd0,reg_display_diag_count};
        status_data[45*8+:8]={4'd0,reg_display_diag_reject};
        status_data[46*8+:16]={4'd0,reg_display_diag_width_raw};
        status_data[48*8+:16]={4'd0,reg_display_diag_height_raw};
        status_data[50*8+:8]={1'b0,reg_display_diag_fill_raw};
        status_data[51*8+:8]={5'd0,reg_display_gate};
        status_data[52*8+:8]={5'd0,(O_error ? 3'd7 : reg_display_reason)};
        status_data[53*8+:8]={5'd0,reg_display_live};
        status_data[54*8+:8]=reg_display_face_raw_count;
        // 保留字节标记能力：bit7有效，bit0表示本构建是否启用人脸。
        status_data[55*8+:8]=C_COMBINED ? 8'h82 : (C_FACE_GATE ? 8'h81 : 8'h80);
        status_data[56*8+:16]={4'd0,reg_display_face_left};status_data[58*8+:16]={4'd0,reg_display_face_top};
        status_data[60*8+:16]={4'd0,reg_display_face_right};status_data[62*8+:16]={4'd0,reg_display_face_bottom};
        status_data[64*8+:48]=reg_camera_status;
        status_data[70*8+:8]=8'd0;
        status_data[71*8+:8]=C_COMBINED?{4'd0,I_application_mode}:8'd10;
        status_data[72*8+:32]=32'h00010000;status_data[76*8+:32]=32'h00010000;
        status_data[144*8+:32]={12'd0,reg_display_diag_area_raw};
                                                                                                
        status_data[148*8+:8]=8'hd1;status_data[149*8+:8]=8'd1;
        status_data[150*8+:16]=reg_display_result_epoch;status_data[152*8+:16]=reg_display_result_job;
        status_data[154*8+:8]={4'd0,reg_display_raw_good};status_data[155*8+:8]={4'd0,reg_display_good};
        status_data[156*8+:32]=reg_display_reject_reason;
        status_data[160*8+:32]=reg_display_good_count;status_data[164*8+:32]=reg_display_bad_count;
        status_data[168*8+:32]=cnt_processed_jobs;status_data[172*8+:32]=cnt_capture_faults;
        for(status_slot=0;status_slot<4;status_slot=status_slot+1)begin
            status_offset=(80+16*status_slot)*8;
            if(reg_display_valid[status_slot])begin
                status_center_x={1'b0,reg_display_left[status_slot*12+:12]}+{1'b0,reg_display_right[status_slot*12+:12]};
                status_center_y={1'b0,reg_display_top[status_slot*12+:12]}+{1'b0,reg_display_bottom[status_slot*12+:12]};
                status_data[status_offset+:8]=8'd1;
                status_data[status_offset+8+:8]={6'd0,reg_display_identity[status_slot*2+:2]};
                status_data[status_offset+16+:8]=reg_display_predicted[status_slot] ? 8'd2 : 8'd1;
                status_data[status_offset+24+:8]={6'd0,reg_display_quality_pending[status_slot],reg_display_good[status_slot]};
                status_data[status_offset+32+:16]={4'd0,status_center_x[12:1]};
                status_data[status_offset+48+:16]={4'd0,status_center_y[12:1]};
                status_data[status_offset+64+:16]={4'd0,reg_display_left[status_slot*12+:12]};
                status_data[status_offset+80+:16]={4'd0,reg_display_top[status_slot*12+:12]};
                status_data[status_offset+96+:16]={4'd0,reg_display_right[status_slot*12+:12]};
                status_data[status_offset+112+:16]={4'd0,reg_display_bottom[status_slot*12+:12]};
            end
        end
    end
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin input_frame_seq<=0;end
        else if(I_user)input_frame_seq<=input_frame_seq+1'b1;
    end
                                                                                            
    always @(posedge I_clk or negedge I_rst_n)begin
        if(!I_rst_n)begin cnt_processed_jobs<=0;cnt_capture_faults<=0;end
        else begin
            if(result_done)cnt_processed_jobs<=cnt_processed_jobs+1'b1;
            if(front_capture_fault)cnt_capture_faults<=cnt_capture_faults+1'b1;
        end
    end
    assign O_status_snapshot=status_data;
    assign O_status_valid=reg_early_o;

    assign O_error=front_error || (scan_error && ball_enabled) || pack_error || (C_SERIAL_RENDER && flag_render_fault);
    assign O_red=red;
    assign O_green=green;
    assign O_yellow=yellow;
    assign O_total=total;
    assign O_count_mode=mode;
    assign O_gate_state=gate_state;
    assign O_track_status=2'd0;
endmodule
