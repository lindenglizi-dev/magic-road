module rle_ccl_top #(
    parameter X_WIDTH     = 8,
    parameter Y_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter ADDR_WIDTH  = 6,
    parameter AREA_WIDTH  = 16,
    parameter LINE_WIDTH  = 256,
    parameter MAX_RUN     = 64,
    parameter MAX_LABEL   = 32,
    parameter MIN_AREA    = 4,
    parameter MIN_RUN_LENGTH = 2
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     analysis_valid,
    input  wire                     analysis_mask,
    input  wire [X_WIDTH-1:0]       analysis_x,
    input  wire [Y_WIDTH-1:0]       analysis_y,
    input  wire                     analysis_sof,
    input  wire                     analysis_eol,
    input  wire                     analysis_eof,

    output wire                     obj_valid,
    output wire [1:0]               obj_index,
    output wire [LABEL_WIDTH-1:0]   obj_label,
    output wire [X_WIDTH-1:0]       obj_xmin,
    output wire [X_WIDTH-1:0]       obj_xmax,
    output wire [Y_WIDTH-1:0]       obj_ymin,
    output wire [Y_WIDTH-1:0]       obj_ymax,
    output wire [X_WIDTH-1:0]       obj_center_x,
    output wire [Y_WIDTH-1:0]       obj_center_y,
    output wire [AREA_WIDTH-1:0]    obj_area,
    output wire [2:0]               object_count,
    output wire                     object_frame_done,

    output wire                     row_done_debug,
    output wire [31:0]              row_match_cycle_max,
    output wire [31:0]              resolve_cycle_max,
    output wire [31:0]              select_cycle_max,
    output wire                     run_overflow,
    output wire                     label_overflow,
    output wire                     raw_overrun,
    output wire                     labeled_overflow,
    output wire                     protocol_error,
    output wire                     ccl_error
);

    localparam P_SCAN    = 2'd0;
    localparam P_RESOLVE = 2'd1;
    localparam P_SELECT  = 2'd2;

    wire frame_clear;
    assign frame_clear = analysis_sof;

    wire run_valid;
    wire [X_WIDTH-1:0] run_x_start;
    wire [X_WIDTH-1:0] run_x_end;
    wire [Y_WIDTH-1:0] run_y;
    wire detector_row_end;
    wire [Y_WIDTH-1:0] detector_row_end_y;
    wire detector_frame_end;
    wire run_detector_error;

    wire raw_locked;
    wire [Y_WIDTH-1:0] raw_row_y;
    wire [ADDR_WIDTH:0] raw_run_count;
    wire raw_run_overflow;
    wire raw_table_error;
    wire raw_rd_req;
    wire [ADDR_WIDTH-1:0] raw_rd_idx;
    wire raw_rd_valid;
    wire [X_WIDTH-1:0] raw_rd_start;
    wire [X_WIDTH-1:0] raw_rd_end;
    wire raw_release;

    wire [ADDR_WIDTH:0] prev_count;
    wire [ADDR_WIDTH:0] curr_count;
    wire prev_rd_req;
    wire [ADDR_WIDTH-1:0] prev_rd_idx;
    wire prev_rd_valid;
    wire [X_WIDTH-1:0] prev_rd_start;
    wire [X_WIDTH-1:0] prev_rd_end;
    wire [LABEL_WIDTH-1:0] prev_rd_label;
    wire curr_wr_en;
    wire [X_WIDTH-1:0] curr_wr_start;
    wire [X_WIDTH-1:0] curr_wr_end;
    wire [LABEL_WIDTH-1:0] curr_wr_label;
    wire row_commit;
    wire labeled_table_error;

    wire alloc_req;
    wire alloc_done;
    wire [LABEL_WIDTH-1:0] alloc_label;
    wire union_req;
    wire [LABEL_WIDTH-1:0] union_a;
    wire [LABEL_WIDTH-1:0] union_b;
    wire union_done;
    wire [LABEL_WIDTH-1:0] union_root;
    wire find_req;
    wire [LABEL_WIDTH-1:0] find_label;
    wire find_done;
    wire [LABEL_WIDTH-1:0] find_root;
    wire label_busy;
    wire [LABEL_WIDTH:0] next_label;
    wire parent_chain_error;
    wire label_manager_error;

    wire feature_update_valid;
    wire feature_update_new_label;
    wire [LABEL_WIDTH-1:0] feature_update_label;
    wire [X_WIDTH-1:0] feature_update_start;
    wire [X_WIDTH-1:0] feature_update_end;
    wire [Y_WIDTH-1:0] feature_update_y;
    wire feature_update_done;
    wire feature_merge_req;
    wire [LABEL_WIDTH-1:0] feature_merge_src;
    wire [LABEL_WIDTH-1:0] feature_merge_dst;
    wire feature_merge_done;
    wire feature_rd_req;
    wire [LABEL_WIDTH-1:0] feature_rd_label;
    wire feature_rd_valid;
    wire feature_valid;
    wire [AREA_WIDTH-1:0] feature_area;
    wire [X_WIDTH-1:0] feature_xmin;
    wire [X_WIDTH-1:0] feature_xmax;
    wire [Y_WIDTH-1:0] feature_ymin;
    wire [Y_WIDTH-1:0] feature_ymax;
    wire feature_area_overflow;
    wire feature_table_error;

    wire matcher_start;
    wire matcher_busy;
    wire matcher_row_done;
    wire [31:0] row_match_cycle_count;
    wire matcher_error;

    reg resolver_start;
    wire resolver_busy;
    wire resolver_done;
    wire [31:0] resolve_cycle_count;
    wire resolver_error;
    wire resolver_protocol_error;

    reg selector_start;
    wire selector_busy;
    wire [31:0] select_cycle_count;
    wire selector_error;
    wire selector_protocol_error;

    reg [1:0] phase;
    reg frame_end_pending;
    reg last_row_done_seen;
    reg top_protocol_error;
    reg run_overflow_sticky;

    assign matcher_start = raw_locked && !matcher_busy && (phase == P_SCAN);
    assign row_done_debug = matcher_row_done;
    assign run_overflow = raw_run_overflow || run_overflow_sticky;

    assign protocol_error = run_detector_error || raw_table_error ||
                            labeled_table_error || label_manager_error ||
                            feature_table_error || resolver_protocol_error ||
                            selector_protocol_error || top_protocol_error;

    assign ccl_error = protocol_error || run_overflow || label_overflow ||
                       raw_overrun || labeled_overflow ||
                       parent_chain_error || feature_area_overflow ||
                       matcher_error || resolver_error || selector_error;

    run_detector #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH), .LINE_WIDTH(LINE_WIDTH),
        .MIN_RUN_LENGTH(MIN_RUN_LENGTH)
    ) u_run_detector (
        .clk(clk), .rst_n(rst_n), .valid(analysis_valid),
        .mask(analysis_mask), .x(analysis_x), .y(analysis_y),
        .sof(analysis_sof), .eol(analysis_eol), .eof(analysis_eof),
        .run_valid(run_valid), .run_x_start(run_x_start),
        .run_x_end(run_x_end), .run_y(run_y), .row_end(detector_row_end),
        .row_end_y(detector_row_end_y), .line_end(),
        .frame_end(detector_frame_end), .protocol_error(run_detector_error)
    );

    raw_run_table #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ADDR_WIDTH(ADDR_WIDTH), .MAX_RUN(MAX_RUN)
    ) u_raw_run_table (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .run_valid(run_valid), .run_start(run_x_start), .run_end(run_x_end),
        .row_end(detector_row_end), .row_end_y(detector_row_end_y),
        .row_release(raw_release), .rd_req(raw_rd_req), .rd_idx(raw_rd_idx),
        .rd_valid(raw_rd_valid), .rd_start(raw_rd_start), .rd_end(raw_rd_end),
        .raw_locked(raw_locked), .raw_row_y(raw_row_y),
        .raw_run_count(raw_run_count), .run_overflow(raw_run_overflow),
        .raw_overrun(raw_overrun), .protocol_error(raw_table_error)
    );

    labeled_run_table #(
        .X_WIDTH(X_WIDTH), .LABEL_WIDTH(LABEL_WIDTH),
        .ADDR_WIDTH(ADDR_WIDTH), .MAX_RUN(MAX_RUN)
    ) u_labeled_run_table (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .row_commit(row_commit), .curr_wr_en(curr_wr_en),
        .curr_wr_start(curr_wr_start), .curr_wr_end(curr_wr_end),
        .curr_wr_label(curr_wr_label), .prev_rd_req(prev_rd_req),
        .prev_rd_idx(prev_rd_idx), .prev_rd_valid(prev_rd_valid),
        .prev_rd_start(prev_rd_start), .prev_rd_end(prev_rd_end),
        .prev_rd_label(prev_rd_label), .prev_count(prev_count),
        .curr_count(curr_count), .prev_bank_sel(), .curr_bank_sel(),
        .labeled_overflow(labeled_overflow),
        .protocol_error(labeled_table_error)
    );

    label_manager #(
        .LABEL_WIDTH(LABEL_WIDTH), .MAX_LABEL(MAX_LABEL)
    ) u_label_manager (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .alloc_req(alloc_req), .alloc_done(alloc_done),
        .alloc_label(alloc_label), .union_req(union_req),
        .union_a(union_a), .union_b(union_b), .union_done(union_done),
        .union_root(union_root), .find_req(find_req),
        .find_label(find_label), .find_done(find_done), .find_root(find_root),
        .busy(label_busy), .next_label(next_label),
        .label_overflow(label_overflow),
        .parent_chain_error(parent_chain_error),
        .protocol_error(label_manager_error)
    );

    feature_table #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH),
        .MAX_LABEL(MAX_LABEL)
    ) u_feature_table (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .update_valid(feature_update_valid),
        .update_new_label(feature_update_new_label),
        .update_label(feature_update_label),
        .update_start(feature_update_start),
        .update_end(feature_update_end), .update_y(feature_update_y),
        .update_done(feature_update_done), .merge_req(feature_merge_req),
        .merge_src_label(feature_merge_src),
        .merge_dst_label(feature_merge_dst), .merge_done(feature_merge_done),
        .rd_req(feature_rd_req), .rd_label(feature_rd_label),
        .rd_valid(feature_rd_valid), .rd_feature_valid(feature_valid),
        .rd_area(feature_area), .rd_xmin(feature_xmin),
        .rd_xmax(feature_xmax), .rd_ymin(feature_ymin),
        .rd_ymax(feature_ymax), .area_overflow(feature_area_overflow),
        .protocol_error(feature_table_error)
    );

    row_matcher #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .ADDR_WIDTH(ADDR_WIDTH),
        .MAX_RUN(MAX_RUN), .MAX_LABEL(MAX_LABEL)
    ) u_row_matcher (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .start(matcher_start), .raw_locked(raw_locked),
        .raw_row_y(raw_row_y), .raw_run_count(raw_run_count),
        .raw_rd_req(raw_rd_req), .raw_rd_idx(raw_rd_idx),
        .raw_rd_valid(raw_rd_valid), .raw_rd_start(raw_rd_start),
        .raw_rd_end(raw_rd_end), .raw_release(raw_release),
        .prev_count(prev_count), .prev_rd_req(prev_rd_req),
        .prev_rd_idx(prev_rd_idx), .prev_rd_valid(prev_rd_valid),
        .prev_rd_start(prev_rd_start), .prev_rd_end(prev_rd_end),
        .prev_rd_label(prev_rd_label), .curr_wr_en(curr_wr_en),
        .curr_wr_start(curr_wr_start), .curr_wr_end(curr_wr_end),
        .curr_wr_label(curr_wr_label), .row_commit(row_commit),
        .alloc_req(alloc_req), .alloc_done(alloc_done),
        .alloc_label(alloc_label), .union_req(union_req),
        .union_a(union_a), .union_b(union_b), .union_done(union_done),
        .union_root(union_root), .feature_update_valid(feature_update_valid),
        .feature_update_new_label(feature_update_new_label),
        .feature_update_label(feature_update_label),
        .feature_update_start(feature_update_start),
        .feature_update_end(feature_update_end),
        .feature_update_y(feature_update_y), .busy(matcher_busy),
        .row_done(matcher_row_done),
        .row_match_cycle_count(row_match_cycle_count),
        .row_match_cycle_max(row_match_cycle_max),
        .matcher_error(matcher_error)
    );

    frame_resolver #(
        .LABEL_WIDTH(LABEL_WIDTH), .MAX_LABEL(MAX_LABEL)
    ) u_frame_resolver (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .start(resolver_start), .label_limit(next_label),
        .find_req(find_req), .find_label(find_label),
        .find_done(find_done), .find_root(find_root),
        .merge_req(feature_merge_req),
        .merge_src_label(feature_merge_src),
        .merge_dst_label(feature_merge_dst),
        .merge_done(feature_merge_done), .busy(resolver_busy),
        .done(resolver_done), .resolve_cycle_count(resolve_cycle_count),
        .resolve_cycle_max(resolve_cycle_max),
        .resolver_error(resolver_error),
        .protocol_error(resolver_protocol_error)
    );

    top4_selector #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH),
        .MAX_LABEL(MAX_LABEL), .MIN_AREA(MIN_AREA)
    ) u_top4_selector (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .start(selector_start), .label_limit(next_label),
        .feature_rd_req(feature_rd_req),
        .feature_rd_label(feature_rd_label),
        .feature_rd_valid(feature_rd_valid), .feature_valid(feature_valid),
        .feature_area(feature_area), .feature_xmin(feature_xmin),
        .feature_xmax(feature_xmax), .feature_ymin(feature_ymin),
        .feature_ymax(feature_ymax), .obj_valid(obj_valid),
        .obj_index(obj_index), .obj_label(obj_label),
        .obj_xmin(obj_xmin), .obj_xmax(obj_xmax),
        .obj_ymin(obj_ymin), .obj_ymax(obj_ymax),
        .obj_center_x(obj_center_x), .obj_center_y(obj_center_y),
        .obj_area(obj_area), .object_count(object_count),
        .object_frame_done(object_frame_done), .busy(selector_busy),
        .select_cycle_count(select_cycle_count),
        .select_cycle_max(select_cycle_max),
        .selector_error(selector_error),
        .protocol_error(selector_protocol_error)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase                <= P_SCAN;
            frame_end_pending    <= 1'b0;
            last_row_done_seen   <= 1'b0;
            resolver_start       <= 1'b0;
            selector_start       <= 1'b0;
            top_protocol_error   <= 1'b0;
            run_overflow_sticky  <= 1'b0;
        end else if (frame_clear) begin
            phase                <= P_SCAN;
            frame_end_pending    <= 1'b0;
            last_row_done_seen   <= 1'b0;
            resolver_start       <= 1'b0;
            selector_start       <= 1'b0;
            top_protocol_error   <= 1'b0;
            run_overflow_sticky  <= 1'b0;
        end else begin
            resolver_start <= 1'b0;
            selector_start <= 1'b0;

            if (raw_run_overflow)
                run_overflow_sticky <= 1'b1;

            if (detector_row_end)
                last_row_done_seen <= 1'b0;
            if (matcher_row_done)
                last_row_done_seen <= 1'b1;
            if (detector_frame_end)
                frame_end_pending <= 1'b1;

            case (phase)
                P_SCAN: begin
                    if ((frame_end_pending || detector_frame_end) &&
                        (last_row_done_seen || matcher_row_done)) begin
                        resolver_start    <= 1'b1;
                        frame_end_pending <= 1'b0;
                        phase             <= P_RESOLVE;
                    end
                end

                P_RESOLVE: begin
                    if (detector_row_end || detector_frame_end)
                        top_protocol_error <= 1'b1;
                    if (resolver_done) begin
                        selector_start <= 1'b1;
                        phase          <= P_SELECT;
                    end
                end

                P_SELECT: begin
                    if (detector_row_end || detector_frame_end)
                        top_protocol_error <= 1'b1;
                    if (object_frame_done)
                        phase <= P_SCAN;
                end

                default: begin
                    phase              <= P_SCAN;
                    top_protocol_error <= 1'b1;
                end
            endcase
        end
    end

endmodule
