// Isolated single-clock wiring experiment; production camera and DDR are absent.
module ccl_pipeline_trial_top #(
    parameter WIDTH = 129,
    parameter HEIGHT = 8,
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 4,
    parameter ID_WIDTH = 32,
    parameter LABEL_WIDTH = 8,
    parameter MAX_LABEL = 128,
    parameter MAX_RUN = 64,
    parameter AREA_WIDTH = 16,
    parameter MIN_RUN_LENGTH = 1,
    parameter MIN_AREA = 1
)(
    input wire clk,
    input wire rst_n,
    input wire task_valid,
    output wire task_ready,
    input wire [ID_WIDTH-1:0] task_id,
    input wire [ID_WIDTH-1:0] task_frame_id,
    input wire in_valid,
    output wire in_ready,
    input wire [ID_WIDTH-1:0] in_task_id,
    input wire [Y_WIDTH-1:0] in_y,
    input wire in_pixel,
    input wire in_last,
    input wire in_frame_last,
    input wire cancel,
    output wire rejected_input,
    output wire candidate_valid,
    output wire candidate_success,
    output wire [7:0] candidate_reason,
    output wire [2:0] candidate_count,
    output wire [ID_WIDTH-1:0] candidate_task_id,
    output wire [ID_WIDTH-1:0] candidate_frame_id,
    input wire candidate_release,
    output wire candidate_release_blocked,
    input wire read_valid,
    output wire read_ready,
    input wire [1:0] read_index,
    output reg response_valid,
    input wire response_ready,
    output reg [1:0] response_index,
    output reg [LABEL_WIDTH-1:0] response_label,
    output reg [X_WIDTH-1:0] response_xmin,
    output reg [X_WIDTH-1:0] response_xmax,
    output reg [Y_WIDTH-1:0] response_ymin,
    output reg [Y_WIDTH-1:0] response_ymax,
    output reg [AREA_WIDTH-1:0] response_area,
    output reg [ID_WIDTH-1:0] response_task_id,
    output reg [ID_WIDTH-1:0] response_frame_id,
    input wire processed_valid,
    output wire processed_ready,
    input wire [ID_WIDTH-1:0] processed_task_id,
    input wire [ID_WIDTH-1:0] processed_frame_id,
    input wire [2:0] processed_count,
    input wire [2:0] accepted_count,
    input wire processed_error,
    output wire final_valid,
    output reg final_success,
    output reg [7:0] final_reason,
    output reg [2:0] final_candidate_count,
    output reg [2:0] final_processed_count,
    output reg [2:0] final_accepted_count,
    output wire [ID_WIDTH-1:0] final_task_id,
    output wire [ID_WIDTH-1:0] final_frame_id,
    input wire display_commit_ack,
    input wire failure_ack,
    output wire algorithm_release,
    output wire banks_empty,
    output wire abort_active,
    output reg core_reset_active
);
    localparam IDLE = 3'd0, RUN = 3'd1, DRAIN = 3'd2,
               RESET_CORE = 3'd3, RECOVER = 3'd4, CANDIDATE = 3'd5,
               PROCESS = 3'd6, FINAL = 3'd7;
    localparam WAIT_ROW = 3'd0, PIXELS = 3'd1, EOL = 3'd2,
               ROW_COMMIT = 3'd3, LAST_ROW = 3'd4, EOF_EVENT = 3'd5,
               INPUT_DONE = 3'd6;
    reg [2:0] state, next_state, feed_state, next_feed_state;
    reg [ID_WIDTH-1:0] active_task, active_frame, line_task;
    reg line_frame_last, input_error, input_complete;
    reg [Y_WIDTH:0] committed_rows, completed_rows;
    reg [2:0] read_count;
    reg read_pending;
    reg [1:0] pending_index;
    wire accepted, guard_ready, guard_valid, guard_success, guard_cancelled;
    wire [7:0] guard_reason;
    wire [2:0] guard_count;
    wire guard_release, guard_clear, guard_stream_enable, guard_rejected;
    wire guard_abort, guard_rd_valid;
    wire [LABEL_WIDTH-1:0] guard_label;
    wire [X_WIDTH-1:0] guard_xmin, guard_xmax;
    wire [Y_WIDTH-1:0] guard_ymin, guard_ymax;
    wire [AREA_WIDTH-1:0] guard_area;
    wire bank_ready, bank_valid, bank_error, bank_cancel;
    wire [ID_WIDTH-1:0] bank_task;
    wire [X_WIDTH-1:0] bank_x;
    wire [Y_WIDTH-1:0] bank_y;
    wire bank_pixel, bank_last, bank_frame_last, bank_take;
    wire core_rst_n, core_ready, core_commit, core_idle, core_row_done;
    wire core_obj_valid, core_done, core_error, core_run_error, core_label_error;
    wire core_protocol_error, core_raw_error, core_labeled_error;
    wire [1:0] core_index;
    wire [LABEL_WIDTH-1:0] core_label;
    wire [X_WIDTH-1:0] core_xmin, core_xmax, core_center_x;
    wire [Y_WIDTH-1:0] core_ymin, core_ymax, core_center_y;
    wire [AREA_WIDTH-1:0] core_area;
    wire [2:0] core_count;
    wire abort_now, drain_done, event_valid, read_take, response_take, table_read_done;
    wire pixel_event, eol_event, eof_event, processed_identity_ok, processed_counts_ok;
    wire [7:0] error_reason;

    assign task_ready = (state == IDLE) && guard_ready && banks_empty;
    assign accepted = task_valid && task_ready;
    assign abort_now = (state == RUN) && (cancel || bank_error || input_error || core_error);
    assign bank_cancel = abort_now || (state == DRAIN) ||
                         (state == RESET_CORE) || (state == RECOVER);
    assign core_rst_n = rst_n && !core_reset_active;
    assign abort_active = bank_cancel;
    assign in_ready = (state == RUN) && !abort_now && !input_complete &&
                      (in_task_id == active_task) && bank_ready;
    assign rejected_input = in_valid && (in_task_id != active_task || state != RUN);
    assign pixel_event = (state == RUN) && (feed_state == PIXELS) && bank_valid;
    assign eol_event = (state == RUN) && (feed_state == EOL);
    assign eof_event = (state == RUN) && (feed_state == EOF_EVENT);
    assign event_valid = pixel_event || eol_event || eof_event;
    assign bank_take = pixel_event && guard_stream_enable && !abort_now;
    assign error_reason = {4'd0, (core_error || bank_error || input_error),
                           core_run_error, core_label_error, 1'b0};
    assign drain_done = (state == RECOVER) && banks_empty && core_idle && !core_error;
    assign candidate_valid = guard_valid && (state == CANDIDATE);
    assign candidate_success = guard_success;
    assign candidate_reason = guard_reason;
    assign candidate_count = guard_count;
    assign candidate_task_id = active_task;
    assign candidate_frame_id = active_frame;
    assign read_ready = candidate_valid && guard_success && !read_pending && !response_valid &&
                        (read_count < guard_count) && (read_index == read_count);
    assign read_take = read_valid && read_ready;
    assign response_take = response_valid && response_ready;
    assign table_read_done = !read_pending && !response_valid && (read_count == guard_count);
    assign guard_release = candidate_release && candidate_valid && table_read_done;
    assign candidate_release_blocked = candidate_release && candidate_valid && !table_read_done;
    assign processed_ready = (state == PROCESS);
    assign processed_identity_ok = (processed_task_id == active_task) &&
                                   (processed_frame_id == active_frame);
    assign processed_counts_ok = (processed_count == final_candidate_count) &&
                                 (accepted_count <= processed_count);
    assign final_valid = (state == FINAL);
    assign final_task_id = active_task;
    assign final_frame_id = active_frame;
    assign algorithm_release = final_valid &&
                               (final_success ? display_commit_ack : failure_ack);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin state <= IDLE; feed_state <= WAIT_ROW; end
        else begin state <= next_state; feed_state <= next_feed_state; end
    end
    always @(*) begin
        next_state = state;
        case (state)
            IDLE: if (accepted) next_state = RUN;
            RUN: begin
                if (abort_now) next_state = DRAIN;
                else if (guard_valid) next_state = CANDIDATE;
            end
            DRAIN: if (banks_empty) next_state = RESET_CORE;
            RESET_CORE: next_state = RECOVER;
            RECOVER: if (drain_done) next_state = CANDIDATE;
            CANDIDATE: if (guard_release) begin
                if (guard_success) next_state = PROCESS;
                else next_state = FINAL;
            end
            PROCESS: if (processed_valid) next_state = FINAL;
            FINAL: if (algorithm_release) next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end
    always @(*) begin
        next_feed_state = feed_state;
        if (accepted || bank_cancel) next_feed_state = WAIT_ROW;
        else if (state == RUN) begin
            case (feed_state)
                WAIT_ROW: if (core_ready) next_feed_state = PIXELS;
                PIXELS: if (bank_take && bank_last) next_feed_state = EOL;
                EOL: if (guard_stream_enable) next_feed_state = ROW_COMMIT;
                ROW_COMMIT: if (core_commit) begin
                    if (line_frame_last) next_feed_state = LAST_ROW;
                    else next_feed_state = WAIT_ROW;
                end
                LAST_ROW: if (completed_rows == HEIGHT) next_feed_state = EOF_EVENT;
                EOF_EVENT: if (guard_stream_enable) next_feed_state = INPUT_DONE;
                INPUT_DONE: next_feed_state = INPUT_DONE;
                default: next_feed_state = WAIT_ROW;
            endcase
        end
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            active_task <= 0; active_frame <= 0; line_task <= 0;
            line_frame_last <= 0; input_error <= 0;
            input_complete <= 0; core_reset_active <= 0;
            committed_rows <= 0; completed_rows <= 0;
            read_count <= 0; read_pending <= 0; pending_index <= 0;
            response_valid <= 0; response_index <= 0; response_label <= 0;
            response_xmin <= 0; response_xmax <= 0; response_ymin <= 0; response_ymax <= 0;
            response_area <= 0; response_task_id <= 0; response_frame_id <= 0;
            final_success <= 0; final_reason <= 0; final_candidate_count <= 0;
            final_processed_count <= 0; final_accepted_count <= 0;
        end else begin
            // Registered reset avoids combinational state-decode glitches on asynchronous resets.
            core_reset_active <= (next_state == RESET_CORE);
            if (accepted) begin
                active_task <= task_id; active_frame <= task_frame_id;
                input_error <= 0; committed_rows <= 0; completed_rows <= 0;
                input_complete <= 0;
                read_count <= 0; read_pending <= 0; response_valid <= 0;
                final_success <= 0; final_reason <= 0;
                final_candidate_count <= 0; final_processed_count <= 0; final_accepted_count <= 0;
            end
            if (in_valid && in_ready && in_frame_last) input_complete <= 1;
            if (bank_take && bank_last) begin
                line_task <= bank_task; line_frame_last <= bank_frame_last;
                if (bank_frame_last != (bank_y == HEIGHT-1) || bank_y != committed_rows)
                    input_error <= 1;
            end
            if ((state == RUN) && (feed_state == ROW_COMMIT) && core_commit)
                committed_rows <= committed_rows + 1'b1;
            if ((state == RUN) && core_row_done) completed_rows <= completed_rows + 1'b1;
            // Single outstanding synchronous table capture. Ownership survives response backpressure.
            if (read_take) begin read_pending <= 1; pending_index <= read_index; end
            if (read_pending) begin
                read_pending <= 0; response_valid <= 1;
                response_index <= pending_index; response_label <= guard_label;
                response_xmin <= guard_xmin; response_xmax <= guard_xmax;
                response_ymin <= guard_ymin; response_ymax <= guard_ymax;
                response_area <= guard_area; response_task_id <= active_task;
                response_frame_id <= active_frame;
            end
            if (response_take) begin response_valid <= 0; read_count <= read_count + 1'b1; end
            if (guard_release) begin
                final_candidate_count <= guard_count;
                final_success <= 0; final_reason <= guard_reason;
            end
            if ((state == PROCESS) && processed_valid) begin
                final_processed_count <= processed_count;
                final_accepted_count <= accepted_count;
                final_success <= !processed_error && processed_identity_ok && processed_counts_ok;
                if (processed_error || !processed_identity_ok || !processed_counts_ok)
                    final_reason <= 8'h40;
            end
        end
    end

    ccl_pixel_line_banks #(.WIDTH(WIDTH), .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ID_WIDTH(ID_WIDTH)) u_lines (
        .clk(clk), .rst_n(core_rst_n), .cancel(bank_cancel),
        .in_valid(in_valid && in_ready), .in_ready(bank_ready),
        .in_task_id(in_task_id), .in_y(in_y), .in_pixel(in_pixel),
        .in_last(in_last), .in_frame_last(in_frame_last),
        .out_valid(bank_valid), .out_ready(bank_take), .out_task_id(bank_task),
        .out_y(bank_y), .out_x(bank_x), .out_pixel(bank_pixel), .out_last(bank_last),
        .out_frame_last(bank_frame_last), .empty(banks_empty), .protocol_error(bank_error)
    );
    ccl_task_guard #(.ID_WIDTH(ID_WIDTH), .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH)) u_guard (
        .clk(clk), .rst_n(rst_n), .task_valid(accepted), .task_ready(guard_ready),
        .task_id(task_id), .task_frame_id(task_frame_id),
        .stream_event(event_valid), .stream_task_id(pixel_event ? bank_task : line_task),
        .stream_sof(1'b0), .core_stream_enable(guard_stream_enable),
        .core_frame_clear(guard_clear), .rejected_stream(guard_rejected),
        .core_obj_valid(core_obj_valid), .core_obj_index(core_index), .core_obj_label(core_label),
        .core_obj_xmin(core_xmin), .core_obj_xmax(core_xmax),
        .core_obj_ymin(core_ymin), .core_obj_ymax(core_ymax),
        .core_obj_center_x(core_center_x), .core_obj_center_y(core_center_y),
        .core_obj_area(core_area), .core_object_count(core_count), .core_done(core_done),
        .core_error_reason(error_reason), .cancel_valid(abort_now), .drain_done(drain_done),
        .abort_request(guard_abort), .result_valid(guard_valid), .result_ready(guard_release),
        .result_task_id(), .result_frame_id(), .result_success(guard_success),
        .result_cancelled(guard_cancelled), .result_reason(guard_reason), .result_object_count(guard_count),
        .rd_index(read_pending ? pending_index : read_index), .rd_valid(guard_rd_valid),
        .rd_label(guard_label), .rd_xmin(guard_xmin), .rd_xmax(guard_xmax),
        .rd_ymin(guard_ymin), .rd_ymax(guard_ymax), .rd_center_x(), .rd_center_y(), .rd_area(guard_area)
    );
    ccl_rle_stream_core #(.X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH), .LABEL_WIDTH(LABEL_WIDTH),
        .AREA_WIDTH(AREA_WIDTH), .LINE_WIDTH(WIDTH), .MAX_RUN(MAX_RUN), .MAX_LABEL(MAX_LABEL),
        .MIN_AREA(MIN_AREA), .MIN_RUN_LENGTH(MIN_RUN_LENGTH)) u_core (
        .clk(clk), .rst_n(core_rst_n), .analysis_valid(bank_take), .analysis_mask(bank_pixel),
        .analysis_x(bank_x), .analysis_y(bank_y), .analysis_sof(guard_clear),
        .analysis_eol(eol_event && guard_stream_enable && !abort_now),
        .analysis_eof(eof_event && guard_stream_enable && !abort_now),
        .row_input_ready(core_ready), .row_input_commit(core_commit), .core_idle(core_idle),
        .obj_valid(core_obj_valid), .obj_index(core_index), .obj_label(core_label),
        .obj_xmin(core_xmin), .obj_xmax(core_xmax), .obj_ymin(core_ymin), .obj_ymax(core_ymax),
        .obj_center_x(core_center_x), .obj_center_y(core_center_y), .obj_area(core_area),
        .object_count(core_count), .object_frame_done(core_done), .row_done_debug(core_row_done),
        .row_match_cycle_max(), .resolve_cycle_max(), .select_cycle_max(),
        .run_overflow(core_run_error), .label_overflow(core_label_error),
        .raw_overrun(core_raw_error), .labeled_overflow(core_labeled_error),
        .protocol_error(core_protocol_error), .ccl_error(core_error)
    );
endmodule
