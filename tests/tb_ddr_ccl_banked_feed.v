`timescale 1ns/1ps

module tb_ddr_ccl_banked_feed;
    parameter integer FRAME_WIDTH     = 129;
    parameter integer FRAME_HEIGHT    = 8;
    parameter integer X_WIDTH         = 8;
    parameter integer Y_WIDTH         = 4;
    parameter integer LABEL_WIDTH     = 8;
    parameter integer AREA_WIDTH      = 16;
    parameter integer MAX_RUN         = 64;
    parameter integer MAX_LABEL       = 128;
    parameter integer MIN_AREA        = 1;
    parameter integer MIN_RUN_LENGTH  = 1;
    parameter integer PIXEL_GAP       = 0;
    parameter integer EOL_FLUSH_CYCLES = 4;

    localparam integer FRAME_PIXELS = FRAME_WIDTH * FRAME_HEIGHT;

    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg analysis_valid = 1'b0;
    reg analysis_mask = 1'b0;
    reg [X_WIDTH-1:0] analysis_x = {X_WIDTH{1'b0}};
    reg [Y_WIDTH-1:0] analysis_y = {Y_WIDTH{1'b0}};
    reg analysis_sof = 1'b0;
    reg analysis_eol = 1'b0;
    reg analysis_eof = 1'b0;

    reg mask_mem [0:FRAME_PIXELS-1];
    reg line_bank0 [0:FRAME_WIDTH-1];
    reg line_bank1 [0:FRAME_WIDTH-1];
    reg bank0_full = 1'b0;
    reg bank1_full = 1'b0;
    reg producer_bank = 1'b0;
    reg consumer_bank = 1'b0;
    integer bank0_row = -1;
    integer bank1_row = -1;

    reg [2047:0] mask_path;
    reg [2047:0] log_path;
    integer log_fd;
    integer producer_row = 0;
    integer consumer_row = 0;
    integer col;
    integer gap;
    integer copy_col;
    integer wait_cycles;
    integer dump_label;
    integer cycle_count = 0;
    integer frame_start_cycle = 0;
    integer scan_state_cycles = 0;
    integer feature_events = 0;
    integer union_events = 0;
    integer object_events = 0;
    integer row_done_count = 0;
    integer producer_stall_cycles = 0;
    integer producer_stall_episodes = 0;
    integer core_wait_cycles = 0;
    integer fill_count = 0;
    integer send_count = 0;
    integer fill_alternation_errors = 0;
    integer send_alternation_errors = 0;
    reg stall_active = 1'b0;
    reg last_fill_bank = 1'b1;
    reg last_send_bank = 1'b1;
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
        .LABEL_WIDTH(LABEL_WIDTH), .ADDR_WIDTH(6),
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
        if (rst_n && row_done_debug)
            row_done_count <= row_done_count + 1;
    end

    // The producer fills complete rows. It cannot overwrite either full bank.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bank0_full <= 1'b0;
            bank1_full <= 1'b0;
            producer_bank <= 1'b0;
            producer_row <= 0;
            stall_active <= 1'b0;
        end else if (producer_row < FRAME_HEIGHT) begin
            if ((producer_bank && !bank1_full) ||
                (!producer_bank && !bank0_full)) begin
                for (copy_col = 0; copy_col < FRAME_WIDTH;
                     copy_col = copy_col + 1) begin
                    if (producer_bank)
                        line_bank1[copy_col] =
                            mask_mem[producer_row*FRAME_WIDTH + copy_col];
                    else
                        line_bank0[copy_col] =
                            mask_mem[producer_row*FRAME_WIDTH + copy_col];
                end
                if (producer_bank) begin
                    bank1_row <= producer_row;
                    bank1_full <= 1'b1;
                end else begin
                    bank0_row <= producer_row;
                    bank0_full <= 1'b1;
                end
                if ((fill_count != 0) && (last_fill_bank == producer_bank))
                    fill_alternation_errors <= fill_alternation_errors + 1;
                last_fill_bank <= producer_bank;
                fill_count <= fill_count + 1;
                $fwrite(log_fd, "BANK_FILL,%0d,%0d,%0d\n",
                        producer_row, producer_bank, cycle_count);
                producer_bank <= ~producer_bank;
                producer_row <= producer_row + 1;
                if (stall_active) begin
                    $fwrite(log_fd, "PRODUCER_STALL_END,%0d,%0d\n",
                            producer_row, cycle_count);
                    stall_active <= 1'b0;
                end
            end else begin
                producer_stall_cycles <= producer_stall_cycles + 1;
                if (!stall_active) begin
                    producer_stall_episodes <= producer_stall_episodes + 1;
                    stall_active <= 1'b1;
                    $fwrite(log_fd, "PRODUCER_STALL_START,%0d,%0d,%0d\n",
                            producer_row, producer_bank, cycle_count);
                end
            end
        end
    end

    always @(negedge clk) begin
        if (rst_n && dut.feature_update_valid) begin
            feature_events = feature_events + 1;
            $fwrite(log_fd, "FEATURE,0,%0d,%0d,%0d,%0d,%0d\n",
                    dut.feature_update_label, dut.feature_update_new_label,
                    dut.feature_update_start, dut.feature_update_end,
                    dut.feature_update_y);
        end
        if (rst_n && dut.union_req) begin
            union_events = union_events + 1;
            $fwrite(log_fd, "UNION,0,%0d,%0d\n", dut.union_a, dut.union_b);
        end
        if (rst_n && obj_valid) begin
            object_events = object_events + 1;
            $fwrite(log_fd, "OBJECT,0,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    obj_index, obj_label, obj_area, obj_xmin, obj_xmax,
                    obj_ymin, obj_ymax);
        end
        if (rst_n && object_frame_done) begin
            done_seen = 1'b1;
            for (dump_label = 1; dump_label < dut.u_label_manager.next_label;
                 dump_label = dump_label + 1) begin
                $fwrite(log_fd, "FINAL,0,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                        dump_label, dut.u_label_manager.parent_mem[dump_label],
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
                    "DONE,0,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    cycle_count-frame_start_cycle, scan_state_cycles,
                    row_match_cycle_max, resolve_cycle_max, select_cycle_max,
                    feature_events, union_events, object_events, object_count,
                    run_overflow, label_overflow, protocol_error, ccl_error);
        end
    end

    task send_buffered_row;
        input integer row_number;
        integer stored_row;
        begin
            wait ((consumer_bank && bank1_full) ||
                  (!consumer_bank && bank0_full));
            stored_row = consumer_bank ? bank1_row : bank0_row;
            if (stored_row != row_number)
                $fatal(1, "bank order mismatch expected=%0d got=%0d",
                       row_number, stored_row);

            while (dut.u_raw_run_table.write_bank_full) begin
                @(posedge clk);
                core_wait_cycles = core_wait_cycles + 1;
            end
            if ((send_count != 0) && (last_send_bank == consumer_bank))
                send_alternation_errors = send_alternation_errors + 1;
            last_send_bank = consumer_bank;
            send_count = send_count + 1;
            $fwrite(log_fd, "BANK_SEND_START,%0d,%0d,%0d\n",
                    row_number, consumer_bank, cycle_count);

            for (col = 0; col < FRAME_WIDTH; col = col + 1) begin
                @(negedge clk);
                analysis_valid = 1'b1;
                analysis_mask = consumer_bank ? line_bank1[col] : line_bank0[col];
                analysis_x = col;
                analysis_y = row_number;
                analysis_sof = (row_number == 0 && col == 0);
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
            @(negedge clk);
            analysis_eol = 1'b0;
            repeat (EOL_FLUSH_CYCLES) @(posedge clk);

            if (consumer_bank)
                bank1_full = 1'b0;
            else
                bank0_full = 1'b0;
            $fwrite(log_fd, "BANK_SEND_END,%0d,%0d,%0d\n",
                    row_number, consumer_bank, cycle_count);
            consumer_bank = ~consumer_bank;
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
        $fwrite(log_fd, "META,%0d,%0d,%0d,%0d,%0d,%0d\n",
                FRAME_WIDTH, FRAME_HEIGHT, MAX_LABEL, MIN_RUN_LENGTH,
                PIXEL_GAP, EOL_FLUSH_CYCLES);
        repeat (5) @(posedge clk);
        @(negedge clk);
        rst_n = 1'b1;
        frame_start_cycle = cycle_count;

        for (consumer_row = 0; consumer_row < FRAME_HEIGHT;
             consumer_row = consumer_row + 1)
            send_buffered_row(consumer_row);

        wait_cycles = 0;
        while ((row_done_count < FRAME_HEIGHT) && (wait_cycles < 20000000)) begin
            @(posedge clk);
            wait_cycles = wait_cycles + 1;
        end
        if (row_done_count != FRAME_HEIGHT)
            $fatal(1, "final row did not complete count=%0d", row_done_count);
        @(negedge clk);
        analysis_eof = 1'b1;
        @(negedge clk);
        analysis_eof = 1'b0;

        wait_cycles = 0;
        while (!done_seen && (wait_cycles < 50000000)) begin
            @(posedge clk);
            wait_cycles = wait_cycles + 1;
        end
        if (!done_seen)
            $fatal(1, "frame timeout");
        if (fill_count != FRAME_HEIGHT || send_count != FRAME_HEIGHT)
            $fatal(1, "bank count mismatch fill=%0d send=%0d", fill_count, send_count);
        $fwrite(log_fd, "BANK_SUMMARY,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                fill_count, send_count, producer_stall_cycles,
                producer_stall_episodes, core_wait_cycles, row_done_count,
                fill_alternation_errors, send_alternation_errors);
        $fflush(log_fd);
        repeat (3) @(posedge clk);
        $fclose(log_fd);
        $display("PASS rows=%0d producer_stall=%0d core_wait=%0d error=%0d",
                 FRAME_HEIGHT, producer_stall_cycles, core_wait_cycles, ccl_error);
        $finish;
    end
endmodule
