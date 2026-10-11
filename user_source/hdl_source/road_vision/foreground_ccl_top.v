module foreground_ccl_top #(
    parameter X_WIDTH       = 8,
    parameter Y_WIDTH       = 8,
    parameter BG_ADDR_WIDTH = 16,
    parameter FRAME_WIDTH   = 256,
    parameter FRAME_HEIGHT  = 150,
    parameter LEARN_FRAMES  = 4,
    parameter LEARN_SHIFT   = 2,
    parameter UPDATE_SHIFT  = 4,
    parameter LABEL_WIDTH   = 6,
    parameter RUN_ADDR_WIDTH = 6,
    parameter AREA_WIDTH    = 16,
    parameter MAX_RUN       = 64,
    parameter MAX_LABEL     = 32,
    parameter MIN_AREA      = 16,
    parameter MIN_RUN_LENGTH = 2,
    parameter CLEANUP_ENABLE = 1,
    parameter CLEANUP_MIN_NEIGHBORS = 3,
    parameter CLASS_MIN_AREA = 16,
    parameter PED_MIN_HEIGHT = 8,
    parameter VEH_MIN_WIDTH  = 8,
    parameter MIN_FILL_QUARTERS = 1,
    parameter ZONE_X_MIN = 80,
    parameter ZONE_X_MAX = 175,
    parameter ZONE_Y_MIN = 50,
    parameter ZONE_Y_MAX = 149,
    parameter LINE_X = 128,
    parameter DWELL_FRAMES = 30
)(
    input  wire                    clk,
    input  wire                    rst_n,

    input  wire                    analysis_valid,
    input  wire [7:0]              analysis_gray,
    input  wire [X_WIDTH-1:0]      analysis_x,
    input  wire [Y_WIDTH-1:0]      analysis_y,
    input  wire                    analysis_sof,
    input  wire                    analysis_eol,
    input  wire                    analysis_eof,

    input  wire [7:0]              diff_threshold,
    input  wire                    background_update_enable,
    input  wire                    freeze_foreground,
    input  wire                    background_relearn,
    input  wire [1:0]              object_rd_index,
    input  wire [1:0]              track_rd_index,

    output wire                    mask_valid,
    output wire                    foreground_mask,
    output wire [7:0]              foreground_diff,
    output wire [7:0]              background_gray,
    output wire [X_WIDTH-1:0]      mask_x,
    output wire [Y_WIDTH-1:0]      mask_y,
    output wire                    mask_sof,
    output wire                    mask_eol,
    output wire                    mask_eof,
    output wire                    background_learning,
    output wire                    background_ready,
    output wire [7:0]              learned_frame_count,

    output wire                    obj_valid,
    output wire [1:0]              obj_index,
    output wire [LABEL_WIDTH-1:0]  obj_label,
    output wire [X_WIDTH-1:0]      obj_xmin,
    output wire [X_WIDTH-1:0]      obj_xmax,
    output wire [Y_WIDTH-1:0]      obj_ymin,
    output wire [Y_WIDTH-1:0]      obj_ymax,
    output wire [X_WIDTH-1:0]      obj_center_x,
    output wire [Y_WIDTH-1:0]      obj_center_y,
    output wire [AREA_WIDTH-1:0]   obj_area,
    output wire [X_WIDTH:0]        obj_width,
    output wire [Y_WIDTH:0]        obj_height,
    output wire [X_WIDTH+Y_WIDTH+1:0] obj_bbox_area,
    output wire [1:0]              obj_fill_level,
    output wire [1:0]              obj_class,
    output wire [2:0]              object_count,
    output wire                    object_frame_done,

    output wire                    object_table_valid,
    output wire [LABEL_WIDTH-1:0]  object_table_label,
    output wire [X_WIDTH-1:0]      object_table_xmin,
    output wire [X_WIDTH-1:0]      object_table_xmax,
    output wire [Y_WIDTH-1:0]      object_table_ymin,
    output wire [Y_WIDTH-1:0]      object_table_ymax,
    output wire [X_WIDTH-1:0]      object_table_center_x,
    output wire [Y_WIDTH-1:0]      object_table_center_y,
    output wire [AREA_WIDTH-1:0]   object_table_area,
    output wire [X_WIDTH:0]        object_table_width,
    output wire [Y_WIDTH:0]        object_table_height,
    output wire [1:0]              object_table_fill_level,
    output wire [1:0]              object_table_class,
    output wire [2:0]              stored_object_count,
    output wire [31:0]             object_frame_sequence,
    output wire                    object_table_commit,

    output wire                    track_valid,
    output wire                    track_visible,
    output wire                    track_confirmed,
    output wire [15:0]             track_id,
    output wire [X_WIDTH-1:0]      track_center_x,
    output wire [Y_WIDTH-1:0]      track_center_y,
    output wire [X_WIDTH-1:0]      track_xmin,
    output wire [X_WIDTH-1:0]      track_xmax,
    output wire [Y_WIDTH-1:0]      track_ymin,
    output wire [Y_WIDTH-1:0]      track_ymax,
    output wire signed [X_WIDTH:0] track_vx,
    output wire signed [Y_WIDTH:0] track_vy,
    output wire [1:0]              track_class,
    output wire [2:0]              track_miss_count,
    output wire                    track_table_ready,
    output wire                    track_frame_done,
    output wire                    track_overflow,
    output wire                    tracker_protocol_error,

    output wire                    event_valid,
    output wire [2:0]              event_type,
    output wire [15:0]             event_track_id,
    output wire [1:0]              event_track_class,
    output wire [15:0]             line_cross_count,
    output wire                    event_frame_done,
    output wire                    event_protocol_error,

    output wire                    run_overflow,
    output wire                    label_overflow,
    output wire                    raw_overrun,
    output wire                    labeled_overflow,
    output wire                    background_protocol_error,
    output wire                    cleanup_protocol_error,
    output wire                    ccl_protocol_error,
    output wire                    classifier_protocol_error,
    output wire                    object_store_protocol_error,
    output wire                    core_error
);

    wire [7:0] mask_gray;
    wire raw_mask_valid, raw_foreground_mask;
    wire [X_WIDTH-1:0] raw_mask_x;
    wire [Y_WIDTH-1:0] raw_mask_y;
    wire raw_mask_sof, raw_mask_eol, raw_mask_eof;
    wire row_done_debug;
    wire [31:0] row_match_cycle_max;
    wire [31:0] resolve_cycle_max;
    wire [31:0] select_cycle_max;
    wire ccl_error;
    wire raw_obj_valid;
    wire [1:0] raw_obj_index;
    wire [LABEL_WIDTH-1:0] raw_obj_label;
    wire [X_WIDTH-1:0] raw_obj_xmin;
    wire [X_WIDTH-1:0] raw_obj_xmax;
    wire [Y_WIDTH-1:0] raw_obj_ymin;
    wire [Y_WIDTH-1:0] raw_obj_ymax;
    wire [X_WIDTH-1:0] raw_obj_center_x;
    wire [Y_WIDTH-1:0] raw_obj_center_y;
    wire [AREA_WIDTH-1:0] raw_obj_area;
    wire raw_object_frame_done;
    wire [1:0] tracker_object_rd_index;
    wire tracker_object_valid;
    wire [X_WIDTH-1:0] tracker_object_xmin;
    wire [X_WIDTH-1:0] tracker_object_xmax;
    wire [Y_WIDTH-1:0] tracker_object_ymin;
    wire [Y_WIDTH-1:0] tracker_object_ymax;
    wire [X_WIDTH-1:0] tracker_object_center_x;
    wire [Y_WIDTH-1:0] tracker_object_center_y;
    wire [1:0] tracker_object_class;
    wire [1:0] event_rd_index;
    wire event_track_valid, event_track_visible, event_track_confirmed;
    wire [15:0] event_read_id;
    wire [X_WIDTH-1:0] event_center_x;
    wire [Y_WIDTH-1:0] event_center_y;
    wire [1:0] event_read_class;

    background_model #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ADDR_WIDTH(BG_ADDR_WIDTH),
        .FRAME_WIDTH(FRAME_WIDTH), .FRAME_HEIGHT(FRAME_HEIGHT),
        .LEARN_FRAMES(LEARN_FRAMES), .LEARN_SHIFT(LEARN_SHIFT),
        .UPDATE_SHIFT(UPDATE_SHIFT)
    ) u_background_model (
        .clk(clk), .rst_n(rst_n),
        .in_valid(analysis_valid), .in_gray(analysis_gray),
        .in_x(analysis_x), .in_y(analysis_y),
        .in_sof(analysis_sof), .in_eol(analysis_eol),
        .in_eof(analysis_eof), .diff_threshold(diff_threshold),
        .update_enable(background_update_enable),
        .freeze_foreground(freeze_foreground),
        .relearn(background_relearn), .out_valid(raw_mask_valid),
        .out_gray(mask_gray), .out_mask(raw_foreground_mask),
        .out_diff(foreground_diff), .out_background(background_gray),
        .out_x(raw_mask_x), .out_y(raw_mask_y), .out_sof(raw_mask_sof),
        .out_eol(raw_mask_eol), .out_eof(raw_mask_eof),
        .learning(background_learning),
        .background_ready(background_ready),
        .learned_frame_count(learned_frame_count),
        .protocol_error(background_protocol_error)
    );

    binary_cleanup_3x3 #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .FRAME_WIDTH(FRAME_WIDTH), .FRAME_HEIGHT(FRAME_HEIGHT),
        .ENABLE(CLEANUP_ENABLE),
        .MIN_NEIGHBORS(CLEANUP_MIN_NEIGHBORS)
    ) u_binary_cleanup_3x3 (
        .clk(clk), .rst_n(rst_n),
        .in_valid(raw_mask_valid), .in_mask(raw_foreground_mask),
        .in_x(raw_mask_x), .in_y(raw_mask_y),
        .in_sof(raw_mask_sof), .in_eol(raw_mask_eol),
        .in_eof(raw_mask_eof),
        .out_valid(mask_valid), .out_mask(foreground_mask),
        .out_x(mask_x), .out_y(mask_y), .out_sof(mask_sof),
        .out_eol(mask_eol), .out_eof(mask_eof),
        .protocol_error(cleanup_protocol_error)
    );

    rle_ccl_top #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .ADDR_WIDTH(RUN_ADDR_WIDTH),
        .AREA_WIDTH(AREA_WIDTH), .LINE_WIDTH(FRAME_WIDTH),
        .MAX_RUN(MAX_RUN), .MAX_LABEL(MAX_LABEL), .MIN_AREA(MIN_AREA),
        .MIN_RUN_LENGTH(MIN_RUN_LENGTH)
    ) u_rle_ccl_top (
        .clk(clk), .rst_n(rst_n),
        .analysis_valid(mask_valid), .analysis_mask(foreground_mask),
        .analysis_x(mask_x), .analysis_y(mask_y),
        .analysis_sof(mask_sof), .analysis_eol(mask_eol),
        .analysis_eof(mask_eof), .obj_valid(raw_obj_valid),
        .obj_index(raw_obj_index), .obj_label(raw_obj_label),
        .obj_xmin(raw_obj_xmin), .obj_xmax(raw_obj_xmax),
        .obj_ymin(raw_obj_ymin), .obj_ymax(raw_obj_ymax),
        .obj_center_x(raw_obj_center_x),
        .obj_center_y(raw_obj_center_y), .obj_area(raw_obj_area),
        .object_count(object_count),
        .object_frame_done(raw_object_frame_done),
        .row_done_debug(row_done_debug),
        .row_match_cycle_max(row_match_cycle_max),
        .resolve_cycle_max(resolve_cycle_max),
        .select_cycle_max(select_cycle_max),
        .run_overflow(run_overflow), .label_overflow(label_overflow),
        .raw_overrun(raw_overrun), .labeled_overflow(labeled_overflow),
        .protocol_error(ccl_protocol_error), .ccl_error(ccl_error)
    );

    object_geometry_classifier #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH),
        .CLASS_MIN_AREA(CLASS_MIN_AREA),
        .PED_MIN_HEIGHT(PED_MIN_HEIGHT),
        .VEH_MIN_WIDTH(VEH_MIN_WIDTH),
        .MIN_FILL_QUARTERS(MIN_FILL_QUARTERS)
    ) u_object_geometry_classifier (
        .clk(clk), .rst_n(rst_n), .frame_clear(mask_sof),
        .in_obj_valid(raw_obj_valid), .in_obj_index(raw_obj_index),
        .in_obj_label(raw_obj_label), .in_obj_xmin(raw_obj_xmin),
        .in_obj_xmax(raw_obj_xmax), .in_obj_ymin(raw_obj_ymin),
        .in_obj_ymax(raw_obj_ymax),
        .in_obj_center_x(raw_obj_center_x),
        .in_obj_center_y(raw_obj_center_y), .in_obj_area(raw_obj_area),
        .in_object_frame_done(raw_object_frame_done),
        .obj_valid(obj_valid), .obj_index(obj_index), .obj_label(obj_label),
        .obj_xmin(obj_xmin), .obj_xmax(obj_xmax),
        .obj_ymin(obj_ymin), .obj_ymax(obj_ymax),
        .obj_center_x(obj_center_x), .obj_center_y(obj_center_y),
        .obj_area(obj_area), .obj_width(obj_width),
        .obj_height(obj_height), .obj_bbox_area(obj_bbox_area),
        .obj_fill_level(obj_fill_level), .obj_class(obj_class),
        .object_frame_done(object_frame_done),
        .protocol_error(classifier_protocol_error)
    );

    object_frame_store #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH)
    ) u_object_frame_store (
        .clk(clk), .rst_n(rst_n), .frame_clear(mask_sof),
        .in_obj_valid(obj_valid), .in_obj_index(obj_index),
        .in_obj_label(obj_label), .in_obj_xmin(obj_xmin),
        .in_obj_xmax(obj_xmax), .in_obj_ymin(obj_ymin),
        .in_obj_ymax(obj_ymax), .in_obj_center_x(obj_center_x),
        .in_obj_center_y(obj_center_y), .in_obj_area(obj_area),
        .in_obj_width(obj_width), .in_obj_height(obj_height),
        .in_obj_fill_level(obj_fill_level), .in_obj_class(obj_class),
        .in_object_count(object_count),
        .in_object_frame_done(object_frame_done),
        .discard_frame(background_protocol_error || cleanup_protocol_error || ccl_error ||
                       classifier_protocol_error),
        .rd_index(object_rd_index), .rd_valid(object_table_valid),
        .rd_label(object_table_label), .rd_xmin(object_table_xmin),
        .rd_xmax(object_table_xmax), .rd_ymin(object_table_ymin),
        .rd_ymax(object_table_ymax),
        .rd_center_x(object_table_center_x),
        .rd_center_y(object_table_center_y), .rd_area(object_table_area),
        .rd_width(object_table_width), .rd_height(object_table_height),
        .rd_fill_level(object_table_fill_level),
        .rd_class(object_table_class),
        .track_rd_index(tracker_object_rd_index),
        .track_obj_valid(tracker_object_valid),
        .track_obj_xmin(tracker_object_xmin),
        .track_obj_xmax(tracker_object_xmax),
        .track_obj_ymin(tracker_object_ymin),
        .track_obj_ymax(tracker_object_ymax),
        .track_obj_center_x(tracker_object_center_x),
        .track_obj_center_y(tracker_object_center_y),
        .track_obj_class(tracker_object_class),
        .stored_object_count(stored_object_count),
        .frame_sequence(object_frame_sequence),
        .object_table_commit(object_table_commit),
        .protocol_error(object_store_protocol_error)
    );

    object_tracker #(.X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH))
    u_object_tracker (
        .clk(clk), .rst_n(rst_n),
        .object_table_commit(object_table_commit),
        .object_rd_index(tracker_object_rd_index),
        .object_valid(tracker_object_valid),
        .object_center_x(tracker_object_center_x),
        .object_center_y(tracker_object_center_y),
        .object_xmin(tracker_object_xmin),
        .object_xmax(tracker_object_xmax),
        .object_ymin(tracker_object_ymin),
        .object_ymax(tracker_object_ymax),
        .object_class(tracker_object_class),
        .object_count(stored_object_count),
        .track_rd_index(track_rd_index),
        .event_rd_index(event_rd_index),
        .event_track_valid(event_track_valid),
        .event_track_visible(event_track_visible),
        .event_track_confirmed(event_track_confirmed),
        .event_track_id(event_read_id),
        .event_track_center_x(event_center_x),
        .event_track_center_y(event_center_y),
        .event_track_class(event_read_class),
        .track_valid(track_valid),
        .track_visible(track_visible),
        .track_confirmed(track_confirmed),
        .track_id(track_id),
        .track_center_x(track_center_x),
        .track_center_y(track_center_y),
        .track_xmin(track_xmin), .track_xmax(track_xmax),
        .track_ymin(track_ymin), .track_ymax(track_ymax),
        .track_vx(track_vx), .track_vy(track_vy),
        .track_class(track_class),
        .track_miss_count(track_miss_count),
        .track_table_ready(track_table_ready),
        .track_frame_done(track_frame_done),
        .track_overflow(track_overflow),
        .protocol_error(tracker_protocol_error)
    );

    track_event_detector #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ZONE_X_MIN(ZONE_X_MIN), .ZONE_X_MAX(ZONE_X_MAX),
        .ZONE_Y_MIN(ZONE_Y_MIN), .ZONE_Y_MAX(ZONE_Y_MAX),
        .LINE_X(LINE_X), .DWELL_FRAMES(DWELL_FRAMES)
    ) u_track_event_detector (
        .clk(clk), .rst_n(rst_n),
        .track_frame_done(track_frame_done),
        .track_rd_index(event_rd_index),
        .track_valid(event_track_valid),
        .track_visible(event_track_visible),
        .track_confirmed(event_track_confirmed),
        .track_id(event_read_id),
        .track_center_x(event_center_x),
        .track_center_y(event_center_y),
        .track_class(event_read_class),
        .event_valid(event_valid), .event_type(event_type),
        .event_track_id(event_track_id),
        .event_track_class(event_track_class),
        .line_cross_count(line_cross_count),
        .event_frame_done(event_frame_done),
        .protocol_error(event_protocol_error)
    );

    assign core_error = background_protocol_error || cleanup_protocol_error || ccl_error ||
                        classifier_protocol_error ||
                        object_store_protocol_error ||
                        tracker_protocol_error || track_overflow ||
                        event_protocol_error;

endmodule
