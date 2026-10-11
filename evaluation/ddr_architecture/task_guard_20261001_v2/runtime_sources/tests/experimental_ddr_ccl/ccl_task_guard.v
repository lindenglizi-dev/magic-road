// Single-clock experiment: accept one task, then publish one qualified table.
module ccl_task_guard #(
    parameter ID_WIDTH = 32,
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter LABEL_WIDTH = 6,
    parameter AREA_WIDTH = 16
)(
    input wire clk,
    input wire rst_n,
    input wire task_valid,
    output wire task_ready,
    input wire [ID_WIDTH-1:0] task_id,
    input wire [ID_WIDTH-1:0] task_frame_id,
    input wire stream_event,
    input wire [ID_WIDTH-1:0] stream_task_id,
    input wire stream_sof,
    output wire core_stream_enable,
    output wire core_frame_clear,
    output wire rejected_stream,
    input wire core_obj_valid,
    input wire [1:0] core_obj_index,
    input wire [LABEL_WIDTH-1:0] core_obj_label,
    input wire [X_WIDTH-1:0] core_obj_xmin,
    input wire [X_WIDTH-1:0] core_obj_xmax,
    input wire [Y_WIDTH-1:0] core_obj_ymin,
    input wire [Y_WIDTH-1:0] core_obj_ymax,
    input wire [X_WIDTH-1:0] core_obj_center_x,
    input wire [Y_WIDTH-1:0] core_obj_center_y,
    input wire [AREA_WIDTH-1:0] core_obj_area,
    input wire [2:0] core_object_count,
    input wire core_done,
    input wire [7:0] core_error_reason,
    input wire cancel_valid,
    input wire drain_done,
    output wire abort_request,
    output wire result_valid,
    input wire result_ready,
    output wire [ID_WIDTH-1:0] result_task_id,
    output wire [ID_WIDTH-1:0] result_frame_id,
    output wire result_success,
    output reg result_cancelled,
    output wire [7:0] result_reason,
    output wire [2:0] result_object_count,
    input wire [1:0] rd_index,
    output wire rd_valid,
    output wire [LABEL_WIDTH-1:0] rd_label,
    output wire [X_WIDTH-1:0] rd_xmin,
    output wire [X_WIDTH-1:0] rd_xmax,
    output wire [Y_WIDTH-1:0] rd_ymin,
    output wire [Y_WIDTH-1:0] rd_ymax,
    output wire [X_WIDTH-1:0] rd_center_x,
    output wire [Y_WIDTH-1:0] rd_center_y,
    output wire [AREA_WIDTH-1:0] rd_area
);
    localparam IDLE = 3'd0, RUN = 3'd1, FLUSH = 3'd2,
               HOLD = 3'd3, CANCEL_DRAIN = 3'd4;
    reg [2:0] state, next_state;
    reg [ID_WIDTH-1:0] active_id, active_frame_id;
    reg [7:0] error_latched;
    reg stream_started;
    reg [3:0] seen_objects;
    reg [2:0] declared_count;
    wire accepted, matching_stream, repeated_sof, cancel_complete;
    wire store_error, stored_valid;
    wire [7:0] live_error, terminal_reason;
    wire bad_count, bad_object;
    wire [3:0] expected_objects;

    assign task_ready = rst_n && (state == IDLE);
    assign accepted = task_valid && task_ready;
    assign matching_stream = (state == RUN) && stream_event &&
                             (stream_task_id == active_id);
    assign repeated_sof = matching_stream && stream_sof && stream_started;
    assign core_stream_enable = matching_stream && !repeated_sof && !cancel_valid;
    assign rejected_stream = rst_n && stream_event && !core_stream_enable;
    assign cancel_complete = (state == CANCEL_DRAIN) && drain_done;
    assign core_frame_clear = accepted || cancel_complete;
    assign abort_request = (state == CANCEL_DRAIN);
    assign result_valid = rst_n && (state == HOLD);
    // These registers cannot change while HOLD owns the result, so reuse
    // them instead of allocating a second descriptor and error snapshot.
    assign result_task_id = active_id;
    assign result_frame_id = active_frame_id;
    assign result_reason = error_latched;
    assign result_success = result_valid && (error_latched == 8'd0) && !result_cancelled;
    assign result_object_count = result_success ? declared_count : 3'd0;
    assign rd_valid = result_valid && result_success && stored_valid;
    // Width-four wrap gives 1111 for count four; counts above four fail.
    assign expected_objects = (4'b0001 << declared_count) - 4'b0001;
    assign bad_count = (state == FLUSH) &&
                       ((declared_count > 4) || (seen_objects != expected_objects));
    assign bad_object = ((state == RUN) && core_obj_valid && seen_objects[core_obj_index]) ||
                        ((state == FLUSH) && core_obj_valid);
    assign live_error = core_error_reason | (repeated_sof ? 8'h01 : 8'h00) |
                        ((bad_count || bad_object || store_error) ? 8'h10 : 8'h00);
    assign terminal_reason = error_latched | live_error;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    always @(*) begin
        next_state = state;
        case (state)
            IDLE: if (accepted) next_state = RUN;
            RUN: begin
                if (cancel_valid) next_state = CANCEL_DRAIN;
                else if (core_done) next_state = FLUSH;
            end
            FLUSH: next_state = HOLD;
            HOLD: if (result_ready) next_state = IDLE;
            CANCEL_DRAIN: if (drain_done) next_state = HOLD;
            default: next_state = IDLE;
        endcase
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            active_id <= {ID_WIDTH{1'b0}};
            active_frame_id <= {ID_WIDTH{1'b0}};
            error_latched <= 8'd0;
            stream_started <= 1'b0;
            seen_objects <= 4'd0;
            declared_count <= 3'd0;
            result_cancelled <= 1'b0;
        end else begin
            if (accepted) begin
                active_id <= task_id;
                active_frame_id <= task_frame_id;
                error_latched <= 8'd0;
                stream_started <= 1'b0;
                seen_objects <= 4'd0;
                declared_count <= 3'd0;
                result_cancelled <= 1'b0;
            end else if (state == RUN) begin
                error_latched <= terminal_reason | (cancel_valid ? 8'h20 : 8'h00);
                if (core_stream_enable) stream_started <= 1'b1;
                if (core_obj_valid) begin
                    seen_objects[core_obj_index] <= 1'b1;
                end
                if (core_done) declared_count <= core_object_count;
            end
            // FLUSH gives the existing store one full clock to retain a
            // last object arriving with DONE. Current errors still win.
            if (state == FLUSH) begin
                error_latched <= terminal_reason;
                result_cancelled <= 1'b0;
            end else if (cancel_complete) begin
                error_latched <= error_latched | 8'h20;
                result_cancelled <= 1'b1;
            end
        end
    end

    // Reuse the production staging/front table; only this guard qualifies it.
    object_frame_store #(.X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH)) u_store (
        .clk(clk), .rst_n(rst_n), .frame_clear(core_frame_clear),
        .in_obj_valid((state == RUN) && core_obj_valid),
        .in_obj_index(core_obj_index), .in_obj_label(core_obj_label),
        .in_obj_xmin(core_obj_xmin), .in_obj_xmax(core_obj_xmax),
        .in_obj_ymin(core_obj_ymin), .in_obj_ymax(core_obj_ymax),
        .in_obj_center_x(core_obj_center_x), .in_obj_center_y(core_obj_center_y),
        .in_obj_area(core_obj_area), .in_obj_width({(X_WIDTH+1){1'b0}}),
        .in_obj_height({(Y_WIDTH+1){1'b0}}), .in_obj_fill_level(2'd0), .in_obj_class(2'd0),
        .in_object_count(declared_count), .in_object_frame_done(state == FLUSH),
        .discard_frame(terminal_reason != 8'd0), .rd_index(rd_index),
        .rd_valid(stored_valid), .rd_label(rd_label), .rd_xmin(rd_xmin), .rd_xmax(rd_xmax),
        .rd_ymin(rd_ymin), .rd_ymax(rd_ymax), .rd_center_x(rd_center_x),
        .rd_center_y(rd_center_y), .rd_area(rd_area), .rd_width(), .rd_height(),
        .rd_fill_level(), .rd_class(), .track_rd_index(2'd0), .track_obj_valid(),
        .track_obj_xmin(), .track_obj_xmax(), .track_obj_ymin(), .track_obj_ymax(),
        .track_obj_center_x(), .track_obj_center_y(), .track_obj_class(),
        .stored_object_count(), .frame_sequence(), .object_table_commit(),
        .protocol_error(store_error)
    );
endmodule
