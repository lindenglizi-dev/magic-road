`timescale 1ns/1ps

module tb_ddr_ccl_fixed_mask;
    parameter integer FRAME_WIDTH    = 16;
    parameter integer FRAME_HEIGHT   = 8;
    parameter integer FRAME_COUNT    = 1;
    parameter integer X_WIDTH        = 8;
    parameter integer Y_WIDTH        = 8;
    parameter integer LABEL_WIDTH    = 6;
    parameter integer ADDR_WIDTH     = 6;
    parameter integer AREA_WIDTH     = 20;
    parameter integer MAX_RUN        = 64;
    parameter integer MAX_LABEL      = 32;
    parameter integer MIN_AREA       = 1;
    parameter integer MIN_RUN_LENGTH = 1;
    parameter integer PIXEL_GAP      = 0;
    parameter integer WAIT_FRAME_DONE = 1;

    localparam integer FRAME_PIXELS = FRAME_WIDTH * FRAME_HEIGHT;
    localparam integer TOTAL_PIXELS = FRAME_PIXELS * FRAME_COUNT;

    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg analysis_valid = 1'b0;
    reg analysis_mask = 1'b0;
    reg [X_WIDTH-1:0] analysis_x = {X_WIDTH{1'b0}};
    reg [Y_WIDTH-1:0] analysis_y = {Y_WIDTH{1'b0}};
    reg analysis_sof = 1'b0;
    reg analysis_eol = 1'b0;
    reg analysis_eof = 1'b0;
    reg mask_mem [0:TOTAL_PIXELS-1];
    reg [2047:0] mask_path;
    reg [2047:0] log_path;

    integer log_fd;
    integer frame_index;
    integer row;
    integer col;
    integer gap;
    integer flat_index;
    integer wait_cycles;
    integer dump_label;
    integer cycle_count = 0;
    integer frame_start_cycle = 0;
    integer scan_state_cycles = 0;
    integer feature_events = 0;
    integer union_events = 0;
    integer object_events = 0;
    integer active_frame = 0;
    reg done_seen = 1'b0;

    wire obj_valid;
    wire [1:0] obj_index;
    wire [LABEL_WIDTH-1:0] obj_label;
    wire [X_WIDTH-1:0] obj_xmin;
    wire [X_WIDTH-1:0] obj_xmax;
    wire [Y_WIDTH-1:0] obj_ymin;
    wire [Y_WIDTH-1:0] obj_ymax;
    wire [X_WIDTH-1:0] obj_center_x;
    wire [Y_WIDTH-1:0] obj_center_y;
    wire [AREA_WIDTH-1:0] obj_area;
    wire [2:0] object_count;
    wire object_frame_done;
    wire row_done_debug;
    wire [31:0] row_match_cycle_max;
    wire [31:0] resolve_cycle_max;
    wire [31:0] select_cycle_max;
    wire run_overflow;
    wire label_overflow;
    wire raw_overrun;
    wire labeled_overflow;
    wire protocol_error;
    wire ccl_error;

    always #5 clk = ~clk;

    rle_ccl_top #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .LABEL_WIDTH(LABEL_WIDTH), .ADDR_WIDTH(ADDR_WIDTH),
        .AREA_WIDTH(AREA_WIDTH), .LINE_WIDTH(FRAME_WIDTH),
        .MAX_RUN(MAX_RUN), .MAX_LABEL(MAX_LABEL),
        .MIN_AREA(MIN_AREA), .MIN_RUN_LENGTH(MIN_RUN_LENGTH)
    ) dut (
        .clk(clk), .rst_n(rst_n), .analysis_valid(analysis_valid),
        .analysis_mask(analysis_mask), .analysis_x(analysis_x),
        .analysis_y(analysis_y), .analysis_sof(analysis_sof),
        .analysis_eol(analysis_eol), .analysis_eof(analysis_eof),
        .obj_valid(obj_valid), .obj_index(obj_index), .obj_label(obj_label),
        .obj_xmin(obj_xmin), .obj_xmax(obj_xmax),
        .obj_ymin(obj_ymin), .obj_ymax(obj_ymax),
        .obj_center_x(obj_center_x), .obj_center_y(obj_center_y),
        .obj_area(obj_area), .object_count(object_count),
        .object_frame_done(object_frame_done),
        .row_done_debug(row_done_debug),
        .row_match_cycle_max(row_match_cycle_max),
        .resolve_cycle_max(resolve_cycle_max),
        .select_cycle_max(select_cycle_max),
        .run_overflow(run_overflow), .label_overflow(label_overflow),
        .raw_overrun(raw_overrun), .labeled_overflow(labeled_overflow),
        .protocol_error(protocol_error), .ccl_error(ccl_error)
    );

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (rst_n && (dut.u_row_matcher.state == 4'd4))
            scan_state_cycles <= scan_state_cycles + 1;
    end

    always @(negedge clk) begin
        if (rst_n && dut.feature_update_valid) begin
            feature_events = feature_events + 1;
            $fwrite(log_fd, "FEATURE,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    active_frame, dut.feature_update_label,
                    dut.feature_update_new_label, dut.feature_update_start,
                    dut.feature_update_end, dut.feature_update_y);
        end
        if (rst_n && dut.union_req) begin
            union_events = union_events + 1;
            $fwrite(log_fd, "UNION,%0d,%0d,%0d\n",
                    active_frame, dut.union_a, dut.union_b);
        end
        if (rst_n && obj_valid) begin
            object_events = object_events + 1;
            $fwrite(log_fd, "OBJECT,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    active_frame, obj_index, obj_label, obj_area,
                    obj_xmin, obj_xmax, obj_ymin, obj_ymax);
        end
        if (rst_n && object_frame_done) begin
            done_seen = 1'b1;
            for (dump_label = 1; dump_label < dut.u_label_manager.next_label;
                 dump_label = dump_label + 1) begin
                $fwrite(log_fd, "FINAL,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        active_frame, dump_label,
                        dut.u_label_manager.parent_mem[dump_label],
                        dut.u_feature_table.valid_mem[dump_label] &&
                        (dut.u_feature_table.epoch_mem[dump_label] ==
                         dut.u_feature_table.frame_epoch),
                        dut.u_feature_table.area_mem[dump_label],
                        dut.u_feature_table.xmin_mem[dump_label],
                        dut.u_feature_table.xmax_mem[dump_label],
                        dut.u_feature_table.ymin_mem[dump_label],
                        dut.u_feature_table.ymax_mem[dump_label]);
            end
            $fwrite(log_fd,
                    "DONE,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    active_frame, cycle_count-frame_start_cycle,
                    scan_state_cycles, row_match_cycle_max,
                    resolve_cycle_max, select_cycle_max,
                    feature_events, union_events, object_events,
                    object_count, run_overflow, label_overflow,
                    protocol_error, ccl_error);
            $fflush(log_fd);
        end
    end

    task send_frame;
        input integer number;
        begin
            active_frame = number;
            done_seen = 1'b0;
            scan_state_cycles = 0;
            feature_events = 0;
            union_events = 0;
            object_events = 0;
            frame_start_cycle = cycle_count;
            for (row = 0; row < FRAME_HEIGHT; row = row + 1) begin
                for (col = 0; col < FRAME_WIDTH; col = col + 1) begin
                    @(negedge clk);
                    flat_index = number*FRAME_PIXELS + row*FRAME_WIDTH + col;
                    analysis_valid = 1'b1;
                    analysis_mask = mask_mem[flat_index];
                    analysis_x = col;
                    analysis_y = row;
                    analysis_sof = (row == 0 && col == 0);
                    analysis_eol = 1'b0;
                    analysis_eof = 1'b0;
                    for (gap = 0; gap < PIXEL_GAP; gap = gap + 1) begin
                        @(negedge clk);
                        analysis_valid = 1'b0;
                        analysis_sof = 1'b0;
                    end
                end
                @(negedge clk);
                analysis_valid = 1'b0;
                analysis_sof = 1'b0;
                analysis_eol = 1'b1;
                analysis_eof = 1'b0;
                @(negedge clk);
                analysis_eol = 1'b0;
                analysis_eof = 1'b0;
                wait_cycles = 0;
                while (!row_done_debug && wait_cycles < 20000000) begin
                    @(posedge clk);
                    wait_cycles = wait_cycles + 1;
                end
                if (!row_done_debug)
                    $fatal(1, "row timeout frame=%0d row=%0d", number, row);
            end
            // EOL and EOF are separate protocol events.  Waiting for the
            // final row completion also guarantees that a trailing run has
            // reached the row matcher before frame resolution starts.
            @(negedge clk);
            analysis_eof = 1'b1;
            @(negedge clk);
            analysis_eof = 1'b0;
            if (WAIT_FRAME_DONE != 0) begin
                wait_cycles = 0;
                while (!done_seen && wait_cycles < 50000000) begin
                    @(posedge clk);
                    wait_cycles = wait_cycles + 1;
                end
                if (!done_seen)
                    $fatal(1, "frame timeout frame=%0d", number);
            end
        end
    endtask

    initial begin
        if (!$value$plusargs("MASK=%s", mask_path))
            $fatal(1, "missing +MASK=<readmemb file>");
        if (!$value$plusargs("LOG=%s", log_path))
            $fatal(1, "missing +LOG=<event log>");
        $readmemb(mask_path, mask_mem);
        log_fd = $fopen(log_path, "w");
        if (!log_fd)
            $fatal(1, "cannot open log %0s", log_path);
        $fwrite(log_fd, "META,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, MAX_LABEL,
                LABEL_WIDTH, MIN_RUN_LENGTH, PIXEL_GAP, WAIT_FRAME_DONE);
        repeat (5) @(posedge clk);
        @(negedge clk);
        rst_n = 1'b1;
        for (frame_index = 0; frame_index < FRAME_COUNT;
             frame_index = frame_index + 1)
            send_frame(frame_index);
        if (WAIT_FRAME_DONE == 0) begin
            wait_cycles = 0;
            while (!done_seen && wait_cycles < 50000000) begin
                @(posedge clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!done_seen)
                $fatal(1, "final frame timeout");
        end
        repeat (3) @(posedge clk);
        $fclose(log_fd);
        $display("PASS frames=%0d final_error=%0d", FRAME_COUNT, ccl_error);
        $finish;
    end
endmodule
