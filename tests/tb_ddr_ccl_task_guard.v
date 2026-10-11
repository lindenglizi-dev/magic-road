`timescale 1ns/1ps

module tb_ddr_ccl_task_guard;
    localparam ID_WIDTH = 32;
    localparam X_WIDTH = 9;
    localparam Y_WIDTH = 2;
    localparam LABEL_WIDTH = 6;
    localparam AREA_WIDTH = 16;

    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg task_valid = 1'b0;
    reg [ID_WIDTH-1:0] task_id = 0;
    reg [ID_WIDTH-1:0] task_frame_id = 0;
    reg stream_event = 1'b0;
    reg [ID_WIDTH-1:0] stream_task_id = 0;
    reg stream_sof = 1'b0;
    reg core_obj_valid = 1'b0;
    reg [1:0] core_obj_index = 0;
    reg [LABEL_WIDTH-1:0] core_obj_label = 0;
    reg [X_WIDTH-1:0] core_obj_xmin = 0;
    reg [X_WIDTH-1:0] core_obj_xmax = 0;
    reg [Y_WIDTH-1:0] core_obj_ymin = 0;
    reg [Y_WIDTH-1:0] core_obj_ymax = 0;
    reg [X_WIDTH-1:0] core_obj_center_x = 0;
    reg [Y_WIDTH-1:0] core_obj_center_y = 0;
    reg [AREA_WIDTH-1:0] core_obj_area = 0;
    reg [2:0] core_object_count = 0;
    reg core_done = 1'b0;
    reg [7:0] core_error_reason = 0;
    reg cancel_valid = 1'b0;
    reg drain_done = 1'b0;
    reg result_ready = 1'b0;
    reg [1:0] rd_index = 0;

    wire task_ready;
    wire core_stream_enable;
    wire core_frame_clear;
    wire rejected_stream;
    wire abort_request;
    wire result_valid;
    wire [ID_WIDTH-1:0] result_task_id;
    wire [ID_WIDTH-1:0] result_frame_id;
    wire result_success;
    wire result_cancelled;
    wire [7:0] result_reason;
    wire [2:0] result_object_count;
    wire rd_valid;
    wire [LABEL_WIDTH-1:0] rd_label;
    wire [X_WIDTH-1:0] rd_xmin;
    wire [X_WIDTH-1:0] rd_xmax;
    wire [Y_WIDTH-1:0] rd_ymin;
    wire [Y_WIDTH-1:0] rd_ymax;
    wire [X_WIDTH-1:0] rd_center_x;
    wire [Y_WIDTH-1:0] rd_center_y;
    wire [AREA_WIDTH-1:0] rd_area;

    integer accepted_count = 0;
    integer terminal_count = 0;
    integer checks = 0;
    integer read_slot;

    always #5 clk = ~clk;

    ccl_task_guard #(
        .ID_WIDTH(ID_WIDTH), .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH)
    ) dut (
        .clk(clk), .rst_n(rst_n), .task_valid(task_valid),
        .task_ready(task_ready), .task_id(task_id),
        .task_frame_id(task_frame_id), .stream_event(stream_event),
        .stream_task_id(stream_task_id), .stream_sof(stream_sof),
        .core_stream_enable(core_stream_enable),
        .core_frame_clear(core_frame_clear), .rejected_stream(rejected_stream),
        .core_obj_valid(core_obj_valid), .core_obj_index(core_obj_index),
        .core_obj_label(core_obj_label), .core_obj_xmin(core_obj_xmin),
        .core_obj_xmax(core_obj_xmax), .core_obj_ymin(core_obj_ymin),
        .core_obj_ymax(core_obj_ymax),
        .core_obj_center_x(core_obj_center_x),
        .core_obj_center_y(core_obj_center_y), .core_obj_area(core_obj_area),
        .core_object_count(core_object_count), .core_done(core_done),
        .core_error_reason(core_error_reason), .cancel_valid(cancel_valid),
        .drain_done(drain_done), .abort_request(abort_request),
        .result_valid(result_valid), .result_ready(result_ready),
        .result_task_id(result_task_id), .result_frame_id(result_frame_id),
        .result_success(result_success), .result_cancelled(result_cancelled),
        .result_reason(result_reason), .result_object_count(result_object_count),
        .rd_index(rd_index), .rd_valid(rd_valid), .rd_label(rd_label),
        .rd_xmin(rd_xmin), .rd_xmax(rd_xmax), .rd_ymin(rd_ymin),
        .rd_ymax(rd_ymax), .rd_center_x(rd_center_x),
        .rd_center_y(rd_center_y), .rd_area(rd_area)
    );

    always @(posedge clk) begin
        if (rst_n && task_valid && task_ready)
            accepted_count <= accepted_count + 1;
        if (rst_n && result_valid && result_ready)
            terminal_count <= terminal_count + 1;
    end

    task check_value;
        input condition;
        input [8*96-1:0] message;
        begin
            checks = checks + 1;
            if (!condition)
                $fatal(1, "check %0d failed: %0s", checks, message);
        end
    endtask

    task clear_inputs;
        begin
            task_valid = 0;
            stream_event = 0;
            stream_sof = 0;
            core_obj_valid = 0;
            core_done = 0;
            core_error_reason = 0;
            cancel_valid = 0;
            drain_done = 0;
            result_ready = 0;
        end
    endtask

    task accept_task;
        input [31:0] id;
        input [31:0] frame_id;
        begin
            @(negedge clk);
            check_value(task_ready, "task_ready before accept");
            task_id = id;
            task_frame_id = frame_id;
            task_valid = 1;
            #1 check_value(core_frame_clear, "accept produces core clear");
            @(negedge clk);
            task_valid = 0;
            check_value(!task_ready, "accepted task owns guard");
        end
    endtask

    task pulse_object;
        input [1:0] index;
        input [5:0] label_value;
        input [15:0] area_value;
        begin
            @(negedge clk);
            core_obj_index = index;
            core_obj_label = label_value;
            core_obj_xmin = index * 10;
            core_obj_xmax = index * 10 + 7;
            core_obj_ymin = index;
            core_obj_ymax = index + 1;
            core_obj_center_x = index * 10 + 3;
            core_obj_center_y = index;
            core_obj_area = area_value;
            core_obj_valid = 1;
            @(negedge clk);
            core_obj_valid = 0;
        end
    endtask

    task finish_task;
        input [2:0] count;
        input [7:0] reason;
        begin
            @(negedge clk);
            core_object_count = count;
            core_error_reason = reason;
            core_done = 1;
            @(negedge clk);
            core_done = 0;
            core_error_reason = 0;
            @(negedge clk);
            check_value(result_valid, "terminal enters HOLD after FLUSH");
        end
    endtask

    task consume_result;
        begin
            @(negedge clk);
            result_ready = 1;
            @(negedge clk);
            result_ready = 0;
            check_value(task_ready, "guard returns idle after result handshake");
        end
    endtask

    task expect_result;
        input [31:0] id;
        input success;
        input cancelled;
        input [7:0] reason;
        input [2:0] count;
        begin
            check_value(result_valid, "result valid");
            check_value(result_task_id == id, "result task identity");
            check_value(result_success == success, "result success");
            check_value(result_cancelled == cancelled, "result cancelled");
            check_value(result_reason == reason, "result reason");
            check_value(result_object_count == count, "result count");
            check_value(!success || count != 0 || !rd_valid,
                   "success empty exposes no object");
            check_value(success || !rd_valid, "failed result exposes no object");
        end
    endtask

    initial begin
        repeat (3) @(posedge clk);
        @(negedge clk);
        rst_n = 1;

        // A pulsed error remains sticky until the task terminal.
        accept_task(1, 101);
        @(negedge clk); core_error_reason = 8'h04;
        @(negedge clk); core_error_reason = 0;
        finish_task(0, 0);
        expect_result(1, 0, 0, 8'h04, 0);
        consume_result();

        // Last object, done, and error on one edge: error wins and no object leaks.
        accept_task(2, 102);
        @(negedge clk);
        core_obj_valid = 1;
        core_obj_index = 0;
        core_obj_label = 6'd12;
        core_obj_area = 16'd77;
        core_object_count = 1;
        core_done = 1;
        core_error_reason = 8'h02;
        @(negedge clk);
        core_obj_valid = 0;
        core_done = 0;
        core_error_reason = 0;
        @(negedge clk);
        expect_result(2, 0, 0, 8'h02, 0);
        consume_result();

        // Last object and done on one edge are retained by the delayed store commit.
        accept_task(3, 103);
        @(negedge clk);
        core_obj_valid = 1;
        core_obj_index = 0;
        core_obj_label = 6'd13;
        core_obj_xmin = 9'd20;
        core_obj_xmax = 9'd27;
        core_obj_area = 16'd88;
        core_object_count = 1;
        core_done = 1;
        @(negedge clk);
        core_obj_valid = 0;
        core_done = 0;
        @(negedge clk);
        expect_result(3, 1, 0, 0, 1);
        check_value(rd_valid && rd_label == 13 && rd_area == 88,
               "last object is visible only with successful held result");

        // While HOLD is backpressured, identity and table remain stable; B waits.
        task_id = 32'd99;
        task_frame_id = 32'd199;
        task_valid = 1;
        repeat (3) begin
            @(negedge clk);
            check_value(!task_ready && result_task_id == 3 && result_object_count == 1,
                   "held result is stable and new task waits");
            check_value(rd_valid && rd_label == 13 && rd_area == 88,
                   "held object table is stable");
        end
        task_valid = 0;
        consume_result();

        // Count-four boundary: all indices exist and the last shares DONE.
        accept_task(30, 130);
        pulse_object(0, 30, 200);
        pulse_object(1, 31, 201);
        pulse_object(2, 32, 202);
        @(negedge clk);
        core_obj_valid = 1;
        core_obj_index = 3;
        core_obj_label = 33;
        core_obj_area = 203;
        core_object_count = 4;
        core_done = 1;
        @(negedge clk);
        core_obj_valid = 0;
        core_done = 0;
        @(negedge clk);
        expect_result(30, 1, 0, 0, 4);
        for (read_slot = 0; read_slot < 4; read_slot = read_slot + 1) begin
            rd_index = read_slot;
            #1;
            check_value(rd_valid && rd_label == (30 + read_slot) &&
                        rd_area == (200 + read_slot),
                        "all four held objects remain readable");
            @(negedge clk);
        end
        consume_result();

        // An unaccepted B stream is rejected as a whole and cannot damage A.
        accept_task(4, 104);
        repeat (4) begin
            @(negedge clk);
            stream_event = 1;
            stream_task_id = 32'd55;
            stream_sof = (checks[0] == 1'b0);
            #1 check_value(rejected_stream && !core_stream_enable,
                      "unaccepted task stream is isolated");
        end
        @(negedge clk);
        stream_event = 0;
        stream_sof = 0;
        finish_task(0, 0);
        expect_result(4, 1, 0, 0, 0);
        consume_result();

        // Count mismatch and duplicate object index are task failures.
        accept_task(5, 105);
        pulse_object(0, 20, 100);
        finish_task(2, 0);
        check_value(result_reason[4] && !result_success,
               "declared/received count mismatch fails");
        consume_result();

        accept_task(6, 106);
        pulse_object(1, 21, 101);
        pulse_object(1, 22, 102);
        finish_task(1, 0);
        check_value(result_reason[4] && !result_success,
               "duplicate object index fails");
        consume_result();

        accept_task(61, 161);
        pulse_object(1, 23, 103);
        finish_task(1, 0);
        check_value(result_reason[4] && !result_success,
                    "noncontiguous object index fails");
        consume_result();

        // An object arriving after done is outside the snapshot and fails.
        accept_task(62, 162);
        @(negedge clk);
        core_object_count = 0;
        core_done = 1;
        @(negedge clk);
        core_done = 0;
        core_obj_valid = 1;
        core_obj_index = 0;
        @(negedge clk);
        core_obj_valid = 0;
        check_value(result_valid && result_reason[4] && !result_success,
                    "object in FLUSH fails the task");
        consume_result();

        // A repeated SOF for the accepted ID is an input error, not a clear.
        accept_task(7, 107);
        @(negedge clk);
        stream_event = 1; stream_task_id = 7; stream_sof = 1;
        #1 check_value(core_stream_enable, "first accepted SOF event passes");
        @(negedge clk);
        #1 check_value(rejected_stream && !core_stream_enable,
                  "repeated accepted SOF is blocked");
        @(negedge clk);
        stream_event = 0; stream_sof = 0;
        finish_task(0, 0);
        check_value(result_reason[0] && !result_success,
               "repeated SOF becomes sticky input error");
        consume_result();

        // A legal empty task is a successful zero-object result.
        accept_task(8, 108);
        finish_task(0, 0);
        expect_result(8, 1, 0, 0, 0);
        consume_result();

        // Cancellation waits for explicit drain completion and then publishes once.
        accept_task(9, 109);
        @(negedge clk); cancel_valid = 1;
        @(negedge clk); cancel_valid = 0;
        repeat (3) begin
            @(negedge clk);
            check_value(abort_request && !result_valid && !task_ready,
                   "cancel waits in drain state");
        end
        stream_event = 1; stream_task_id = 9;
        #1 check_value(rejected_stream && !core_stream_enable,
                  "cancel drain blocks remaining stream");
        @(negedge clk);
        stream_event = 0;
        drain_done = 1;
        #1 check_value(core_frame_clear, "drain acknowledgement clears core");
        @(negedge clk);
        drain_done = 0;
        expect_result(9, 0, 1, 8'h20, 0);
        consume_result();

        check_value(accepted_count == terminal_count,
               "every accepted task has exactly one consumed terminal");

        // Cancellation wins even when completion shares the same clock.
        accept_task(11, 111);
        @(negedge clk);
        cancel_valid = 1; core_done = 1; core_object_count = 0;
        @(negedge clk);
        cancel_valid = 0; core_done = 0;
        check_value(abort_request && !result_valid, "cancel wins over done");
        drain_done = 1;
        @(negedge clk); drain_done = 0;
        expect_result(11, 0, 1, 8'h20, 0);
        consume_result();

        // A preasserted consumer READY still consumes exactly one terminal.
        accept_task(12, 112);
        result_ready = 1;
        finish_task(0, 0);
        expect_result(12, 1, 0, 0, 0);
        @(negedge clk); result_ready = 0;
        check_value(task_ready && accepted_count == terminal_count,
                    "preasserted ready consumes once");

        // Reset boundaries abort local ownership; they are not normal terminals.
        accept_task(13, 113);
        finish_task(0, 0);
        @(negedge clk); rst_n = 0; clear_inputs();
        @(negedge clk); rst_n = 1;
        #1 check_value(task_ready && !result_valid && !rd_valid,
                        "reset during HOLD suppresses stale result");
        accept_task(14, 114);
        @(negedge clk); cancel_valid = 1;
        @(negedge clk); cancel_valid = 0;
        check_value(abort_request, "cancel state before reset");
        @(negedge clk); rst_n = 0; clear_inputs();
        @(negedge clk); rst_n = 1;
        #1 check_value(task_ready && !result_valid && !abort_request,
                        "reset during cancel suppresses stale ownership");

        // Reset establishes a new conservation interval and suppresses ghost results.
        accept_task(10, 110);
        @(negedge clk); rst_n = 0;
        @(negedge clk); clear_inputs();
        repeat (2) @(posedge clk);
        @(negedge clk); rst_n = 1;
        #1;
        check_value(task_ready && !result_valid && !rd_valid,
               "reset returns idle without a ghost terminal");

        $display("PASS mock guard checks=%0d accepted=%0d terminal=%0d",
                 checks, accepted_count, terminal_count);
        $finish;
    end
endmodule

module tb_ddr_ccl_task_guard_real;
    localparam FRAME_WIDTH = 264;
    localparam FRAME_HEIGHT = 2;
    localparam X_WIDTH = 9;
    localparam Y_WIDTH = 1;
    localparam LABEL_WIDTH = 6;
    localparam AREA_WIDTH = 16;

    reg clk = 0;
    reg rst_n = 0;
    reg task_valid = 0;
    reg [31:0] task_id = 0;
    reg [31:0] task_frame_id = 0;
    reg stream_event = 0;
    reg [31:0] stream_task_id = 0;
    reg stream_sof = 0;
    reg pixel_valid = 0;
    reg pixel_mask = 0;
    reg [X_WIDTH-1:0] pixel_x = 0;
    reg [Y_WIDTH-1:0] pixel_y = 0;
    reg event_eol = 0;
    reg event_eof = 0;
    reg cancel_valid = 0;
    reg drain_done = 0;
    reg result_ready = 0;
    reg [1:0] rd_index = 0;

    wire task_ready;
    wire core_stream_enable;
    wire core_frame_clear;
    wire rejected_stream;
    wire abort_request;
    wire result_valid;
    wire [31:0] result_task_id;
    wire [31:0] result_frame_id;
    wire result_success;
    wire result_cancelled;
    wire [7:0] result_reason;
    wire [2:0] result_object_count;
    wire rd_valid;
    wire [LABEL_WIDTH-1:0] rd_label;
    wire [X_WIDTH-1:0] rd_xmin;
    wire [X_WIDTH-1:0] rd_xmax;
    wire [Y_WIDTH-1:0] rd_ymin;
    wire [Y_WIDTH-1:0] rd_ymax;
    wire [X_WIDTH-1:0] rd_center_x;
    wire [Y_WIDTH-1:0] rd_center_y;
    wire [AREA_WIDTH-1:0] rd_area;

    wire core_obj_valid;
    wire [1:0] core_obj_index;
    wire [LABEL_WIDTH-1:0] core_obj_label;
    wire [X_WIDTH-1:0] core_obj_xmin;
    wire [X_WIDTH-1:0] core_obj_xmax;
    wire [Y_WIDTH-1:0] core_obj_ymin;
    wire [Y_WIDTH-1:0] core_obj_ymax;
    wire [X_WIDTH-1:0] core_obj_center_x;
    wire [Y_WIDTH-1:0] core_obj_center_y;
    wire [AREA_WIDTH-1:0] core_obj_area;
    wire [2:0] core_object_count;
    wire core_done;
    wire row_done_debug;
    wire run_overflow;
    wire label_overflow;
    wire raw_overrun;
    wire labeled_overflow;
    wire protocol_error;
    wire ccl_error;
    wire [7:0] core_error_reason;

    integer row;
    integer col;
    integer wait_cycles;
    integer checks = 0;
    integer accepted_count = 0;
    integer terminal_count = 0;
    integer rejected_count = 0;

    always #5 clk = ~clk;

    assign core_error_reason = (label_overflow ? 8'h02 : 8'h00) |
                               (run_overflow ? 8'h04 : 8'h00) |
                               ((ccl_error && !label_overflow && !run_overflow) ?
                                8'h08 : 8'h00);

    always @(posedge clk) begin
        if (rst_n && task_valid && task_ready)
            accepted_count <= accepted_count + 1;
        if (rst_n && result_valid && result_ready)
            terminal_count <= terminal_count + 1;
        if (rst_n && rejected_stream)
            rejected_count <= rejected_count + 1;
    end

    ccl_task_guard #(
        .ID_WIDTH(32), .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .AREA_WIDTH(AREA_WIDTH)
    ) guard (
        .clk(clk), .rst_n(rst_n), .task_valid(task_valid),
        .task_ready(task_ready), .task_id(task_id),
        .task_frame_id(task_frame_id), .stream_event(stream_event),
        .stream_task_id(stream_task_id), .stream_sof(stream_sof),
        .core_stream_enable(core_stream_enable),
        .core_frame_clear(core_frame_clear), .rejected_stream(rejected_stream),
        .core_obj_valid(core_obj_valid), .core_obj_index(core_obj_index),
        .core_obj_label(core_obj_label), .core_obj_xmin(core_obj_xmin),
        .core_obj_xmax(core_obj_xmax), .core_obj_ymin(core_obj_ymin),
        .core_obj_ymax(core_obj_ymax),
        .core_obj_center_x(core_obj_center_x),
        .core_obj_center_y(core_obj_center_y), .core_obj_area(core_obj_area),
        .core_object_count(core_object_count), .core_done(core_done),
        .core_error_reason(core_error_reason), .cancel_valid(cancel_valid),
        .drain_done(drain_done), .abort_request(abort_request),
        .result_valid(result_valid), .result_ready(result_ready),
        .result_task_id(result_task_id), .result_frame_id(result_frame_id),
        .result_success(result_success), .result_cancelled(result_cancelled),
        .result_reason(result_reason), .result_object_count(result_object_count),
        .rd_index(rd_index), .rd_valid(rd_valid), .rd_label(rd_label),
        .rd_xmin(rd_xmin), .rd_xmax(rd_xmax), .rd_ymin(rd_ymin),
        .rd_ymax(rd_ymax), .rd_center_x(rd_center_x),
        .rd_center_y(rd_center_y), .rd_area(rd_area)
    );

    rle_ccl_top #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH), .LABEL_WIDTH(LABEL_WIDTH),
        .ADDR_WIDTH(6), .AREA_WIDTH(AREA_WIDTH), .LINE_WIDTH(FRAME_WIDTH),
        .MAX_RUN(64), .MAX_LABEL(32), .MIN_AREA(1), .MIN_RUN_LENGTH(1)
    ) core (
        .clk(clk), .rst_n(rst_n),
        .analysis_valid(core_stream_enable && pixel_valid),
        .analysis_mask(pixel_mask), .analysis_x(pixel_x), .analysis_y(pixel_y),
        .analysis_sof(core_frame_clear),
        .analysis_eol(core_stream_enable && event_eol),
        .analysis_eof(core_stream_enable && event_eof),
        .obj_valid(core_obj_valid), .obj_index(core_obj_index),
        .obj_label(core_obj_label), .obj_xmin(core_obj_xmin),
        .obj_xmax(core_obj_xmax), .obj_ymin(core_obj_ymin),
        .obj_ymax(core_obj_ymax), .obj_center_x(core_obj_center_x),
        .obj_center_y(core_obj_center_y), .obj_area(core_obj_area),
        .object_count(core_object_count), .object_frame_done(core_done),
        .row_done_debug(row_done_debug), .row_match_cycle_max(),
        .resolve_cycle_max(), .select_cycle_max(),
        .run_overflow(run_overflow), .label_overflow(label_overflow),
        .raw_overrun(raw_overrun), .labeled_overflow(labeled_overflow),
        .protocol_error(protocol_error), .ccl_error(ccl_error)
    );

    task real_check;
        input condition;
        input [8*96-1:0] message;
        begin
            checks = checks + 1;
            if (!condition)
                $fatal(1, "real check %0d failed: %0s", checks, message);
        end
    endtask

    task accept_real;
        input [31:0] id;
        begin
            @(negedge clk);
            real_check(task_ready, "ready before real task");
            task_id = id;
            task_frame_id = id + 1000;
            task_valid = 1;
            #1 real_check(core_frame_clear, "real accept clears core");
            @(negedge clk);
            task_valid = 0;
        end
    endtask

    task drive_pixel;
        input [31:0] id;
        input integer x_value;
        input integer y_value;
        input mask_value;
        begin
            @(negedge clk);
            stream_event = 1;
            stream_task_id = id;
            stream_sof = (x_value == 0 && y_value == 0);
            pixel_valid = 1;
            pixel_mask = mask_value;
            pixel_x = x_value;
            pixel_y = y_value;
            #1 real_check(core_stream_enable, "accepted pixel enabled");
        end
    endtask

    task finish_row;
        input [31:0] id;
        begin
            @(negedge clk);
            stream_event = 1;
            stream_task_id = id;
            stream_sof = 0;
            pixel_valid = 0;
            event_eol = 1;
            #1 real_check(core_stream_enable, "accepted EOL enabled");
            @(negedge clk);
            stream_event = 0;
            event_eol = 0;
            wait_cycles = 0;
            while (!row_done_debug && wait_cycles < 200000) begin
                @(posedge clk);
                wait_cycles = wait_cycles + 1;
            end
            real_check(row_done_debug, "real row completes");
        end
    endtask

    task finish_frame_input;
        input [31:0] id;
        begin
            @(negedge clk);
            stream_event = 1;
            stream_task_id = id;
            stream_sof = 0;
            pixel_valid = 0;
            event_eof = 1;
            #1 real_check(core_stream_enable, "accepted EOF enabled");
            @(negedge clk);
            stream_event = 0;
            event_eof = 0;
        end
    endtask

    task send_pattern;
        input [31:0] id;
        input integer pattern;
        begin
            for (row = 0; row < FRAME_HEIGHT; row = row + 1) begin
                for (col = 0; col < FRAME_WIDTH; col = col + 1) begin
                    case (pattern)
                        0: drive_pixel(id, col, row,
                            (row == 0) ? ((col < 256) && ((col % 8) < 5)) : 1'b1);
                        1: drive_pixel(id, col, row,
                            (row == 0) ? (((col < 256) && ((col % 8) < 5)) ||
                                          ((col >= 256) && (col < 261))) : 1'b1);
                        2: drive_pixel(id, col, row, 1'b0);
                        default: drive_pixel(id, col, row, col >= 260);
                    endcase
                end
                @(negedge clk);
                pixel_valid = 0;
                stream_event = 0;
                stream_sof = 0;
                finish_row(id);
            end
            finish_frame_input(id);
        end
    endtask

    task inject_unaccepted_b;
        integer event_number;
        begin
            wait_cycles = 0;
            while ((core.phase == 0) && wait_cycles < 200000) begin
                @(posedge clk);
                wait_cycles = wait_cycles + 1;
            end
            real_check(core.phase != 0, "A entered resolve/select before B probe");
            for (event_number = 0; event_number < 4;
                 event_number = event_number + 1) begin
                @(negedge clk);
                task_valid = 1;
                task_id = 999;
                task_frame_id = 1999;
                stream_event = 1;
                stream_task_id = 999;
                stream_sof = (event_number == 0);
                pixel_valid = (event_number == 1);
                event_eol = (event_number == 2);
                event_eof = (event_number == 3);
                #1 real_check(!task_ready && rejected_stream &&
                              !core_stream_enable,
                              "busy A rejects unaccepted B event");
            end
            @(negedge clk);
            task_valid = 0;
            stream_event = 0;
            stream_sof = 0;
            pixel_valid = 0;
            event_eol = 0;
            event_eof = 0;
        end
    endtask

    task wait_real_result;
        input [31:0] id;
        input expected_success;
        input [7:0] required_reason;
        input [2:0] expected_count;
        begin
            wait_cycles = 0;
            while (!result_valid && wait_cycles < 2000000) begin
                @(posedge clk);
                wait_cycles = wait_cycles + 1;
            end
            @(negedge clk);
            real_check(result_valid, "real task has terminal");
            real_check(result_task_id == id, "real terminal identity");
            real_check(result_success == expected_success,
                       "real terminal success state");
            real_check((result_reason & required_reason) == required_reason,
                       "real terminal reason");
            real_check(result_object_count == expected_count,
                       "real terminal object count");
            real_check(expected_success || !rd_valid,
                       "failed real task exposes no object");
        end
    endtask

    task consume_real;
        begin
            @(negedge clk);
            result_ready = 1;
            @(negedge clk);
            result_ready = 0;
        end
    endtask

    initial begin
        repeat (4) @(posedge clk);
        @(negedge clk); rst_n = 1;

        accept_real(101);
        send_pattern(101, 0);
        inject_unaccepted_b();
        wait_real_result(101, 1, 0, 1);
        real_check(rd_valid, "exact32 publishes its complete object");
        consume_real();

        accept_real(102);
        send_pattern(102, 1);
        wait_real_result(102, 0, 8'h02, 0);
        consume_real();

        accept_real(103);
        send_pattern(103, 2);
        wait_real_result(103, 1, 0, 0);
        real_check(!rd_valid, "successful empty frame has no object");
        consume_real();

        accept_real(104);
        send_pattern(104, 3);
        wait_real_result(104, 1, 0, 1);
        real_check(rd_valid && rd_area == 8,
                   "normal frame recovers after overflow and empty frame");
        consume_real();

        @(negedge clk);
        real_check(accepted_count == 4 && terminal_count == 4,
                   "real accepted tasks conserve terminals");
        real_check(rejected_count >= 4,
                   "unaccepted B stream produced diagnostics");
        $display("PASS real guard checks=%0d accepted=%0d terminal=%0d rejected=%0d",
                 checks, accepted_count, terminal_count, rejected_count);
        $finish;
    end
endmodule
