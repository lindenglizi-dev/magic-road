`timescale 1ns/1ps

module tb_ddr_raw_handoff;
    localparam X_WIDTH = 8;
    localparam Y_WIDTH = 8;
    localparam ADDR_WIDTH = 6;
    localparam MAX_RUN = 64;

    reg clk;
    reg rst_n;
    reg frame_clear;
    reg run_valid;
    reg [X_WIDTH-1:0] run_start;
    reg [X_WIDTH-1:0] run_end;
    reg row_end;
    reg [Y_WIDTH-1:0] row_end_y;
    reg row_release;
    reg rd_req;
    reg [ADDR_WIDTH-1:0] rd_idx;
    wire rd_valid;
    wire [X_WIDTH-1:0] rd_start;
    wire [X_WIDTH-1:0] rd_end;
    wire row_write_ready;
    wire raw_locked;
    wire [Y_WIDTH-1:0] raw_row_y;
    wire [ADDR_WIDTH:0] raw_run_count;
    wire run_overflow;
    wire raw_overrun;
    wire protocol_error;
    integer checks;
    integer handoffs;
    integer illegal_events;
    integer reads;

    ccl_raw_run_table #(
        .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ADDR_WIDTH(ADDR_WIDTH), .MAX_RUN(MAX_RUN)
    ) dut (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .run_valid(run_valid), .run_start(run_start), .run_end(run_end),
        .row_end(row_end), .row_end_y(row_end_y),
        .row_release(row_release), .rd_req(rd_req), .rd_idx(rd_idx),
        .rd_valid(rd_valid), .rd_start(rd_start), .rd_end(rd_end),
        .row_write_ready(row_write_ready), .raw_locked(raw_locked),
        .raw_row_y(raw_row_y), .raw_run_count(raw_run_count),
        .run_overflow(run_overflow), .raw_overrun(raw_overrun),
        .protocol_error(protocol_error)
    );

    always #5 clk = !clk;

    task fail;
        input [8*112-1:0] message;
        begin
            $display("FAIL: %0s", message);
            $finish(1);
        end
    endtask

    task reset_dut;
        begin
            @(negedge clk);
            rst_n = 1'b0;
            frame_clear = 1'b0;
            run_valid = 1'b0;
            row_end = 1'b0;
            row_release = 1'b0;
            rd_req = 1'b0;
            repeat (2) @(negedge clk);
            rst_n = 1'b1;
            @(negedge clk);
            if (!row_write_ready || raw_locked || rd_valid ||
                run_overflow || raw_overrun || protocol_error)
                fail("reset state");
            checks = checks + 1;
        end
    endtask

    task clear_frame;
        begin
            @(negedge clk);
            frame_clear = 1'b1;
            @(posedge clk);
            @(negedge clk);
            frame_clear = 1'b0;
            if (!row_write_ready || raw_locked || rd_valid ||
                run_overflow || raw_overrun || protocol_error)
                fail("frame_clear recovery");
            checks = checks + 1;
        end
    endtask

    task push_run;
        input [X_WIDTH-1:0] first_x;
        input [X_WIDTH-1:0] last_x;
        begin
            @(negedge clk);
            if (!row_write_ready)
                fail("legal run offered without row admission");
            run_start = first_x;
            run_end = last_x;
            run_valid = 1'b1;
            @(posedge clk);
            @(negedge clk);
            run_valid = 1'b0;
            checks = checks + 1;
        end
    endtask

    task finish_row;
        input [Y_WIDTH-1:0] y;
        input release_old;
        begin
            @(negedge clk);
            if (!row_write_ready)
                fail("legal row_end offered without row admission");
            row_end_y = y;
            row_end = 1'b1;
            row_release = release_old;
            @(posedge clk);
            @(negedge clk);
            row_end = 1'b0;
            row_release = 1'b0;
            if (protocol_error || raw_overrun || run_overflow)
                fail("legal row handoff raised error");
            if (release_old)
                handoffs = handoffs + 1;
            checks = checks + 1;
        end
    endtask

    task release_row;
        begin
            @(negedge clk);
            if (!raw_locked)
                fail("release requested without locked row");
            row_release = 1'b1;
            @(posedge clk);
            @(negedge clk);
            row_release = 1'b0;
            checks = checks + 1;
        end
    endtask

    task expect_row;
        input [Y_WIDTH-1:0] y;
        input [ADDR_WIDTH:0] count;
        begin
            if (!raw_locked || raw_row_y !== y || raw_run_count !== count)
                fail("published row identity or count mismatch");
            checks = checks + 1;
        end
    endtask

    task read_run;
        input [ADDR_WIDTH-1:0] index;
        input [X_WIDTH-1:0] first_x;
        input [X_WIDTH-1:0] last_x;
        begin
            @(negedge clk);
            rd_idx = index;
            rd_req = 1'b1;
            @(posedge clk);
            @(negedge clk);
            rd_req = 1'b0;
            if (!rd_valid || rd_start !== first_x || rd_end !== last_x)
                fail("synchronous run read mismatch");
            reads = reads + 1;
            checks = checks + 1;
            @(posedge clk);
            @(negedge clk);
            if (rd_valid || rd_start !== first_x || rd_end !== last_x)
                fail("read valid pulse or held payload mismatch");
            checks = checks + 1;
        end
    endtask

    task illegal_full_run;
        begin
            @(negedge clk);
            if (row_write_ready)
                fail("full-bank precondition missing");
            run_start = 8'd40;
            run_end = 8'd43;
            run_valid = 1'b1;
            @(posedge clk);
            @(negedge clk);
            run_valid = 1'b0;
            if (!protocol_error || !raw_overrun)
                fail("full-bank run was not rejected");
            illegal_events = illegal_events + 1;
            checks = checks + 1;
        end
    endtask

    task illegal_run_with_row_end;
        begin
            @(negedge clk);
            if (!row_write_ready)
                fail("combined-invalid precondition missing");
            run_start = 8'd5;
            run_end = 8'd9;
            run_valid = 1'b1;
            row_end_y = 8'd20;
            row_end = 1'b1;
            @(posedge clk);
            @(negedge clk);
            run_valid = 1'b0;
            row_end = 1'b0;
            if (!protocol_error)
                fail("run_valid plus row_end was not marked invalid");
            illegal_events = illegal_events + 1;
            checks = checks + 1;
        end
    endtask

    initial begin
        clk = 1'b0;
        rst_n = 1'b0;
        frame_clear = 1'b0;
        run_valid = 1'b0;
        run_start = 0;
        run_end = 0;
        row_end = 1'b0;
        row_end_y = 0;
        row_release = 1'b0;
        rd_req = 1'b0;
        rd_idx = 0;
        checks = 0;
        handoffs = 0;
        illegal_events = 0;
        reads = 0;

        reset_dut();

        // Bank A becomes the old read bank.
        push_run(8'd1, 8'd3);
        push_run(8'd10, 8'd15);
        finish_row(8'd10, 1'b0);
        expect_row(8'd10, 7'd2);
        read_run(6'd0, 8'd1, 8'd3);
        read_run(6'd1, 8'd10, 8'd15);

        // Finish bank B while releasing A on the same edge.
        push_run(8'd2, 8'd4);
        push_run(8'd20, 8'd22);
        push_run(8'd30, 8'd35);
        finish_row(8'd11, 1'b1);
        if (dut.full_a || !dut.full_b || dut.count_a != 0 || dut.count_b != 3 ||
            dut.read_bank != 1'b1 || dut.write_bank != 1'b0)
            fail("A-to-B same-cycle ownership exchange");
        expect_row(8'd11, 7'd3);
        read_run(6'd0, 8'd2, 8'd4);
        read_run(6'd1, 8'd20, 8'd22);
        read_run(6'd2, 8'd30, 8'd35);

        // Finish bank A while releasing B on the same edge.
        push_run(8'd7, 8'd12);
        finish_row(8'd12, 1'b1);
        if (!dut.full_a || dut.full_b || dut.count_a != 1 || dut.count_b != 0 ||
            dut.read_bank != 1'b0 || dut.write_bank != 1'b1)
            fail("B-to-A same-cycle ownership exchange");
        expect_row(8'd12, 7'd1);
        read_run(6'd0, 8'd7, 8'd12);
        checks = checks + 2;

        // Fill B without releasing A, then prove a full-bank request cannot corrupt A.
        push_run(8'd16, 8'd18);
        push_run(8'd24, 8'd29);
        finish_row(8'd13, 1'b0);
        if (row_write_ready || !dut.full_a || !dut.full_b)
            fail("two-full-bank state missing");
        illegal_full_run();
        expect_row(8'd12, 7'd1);
        read_run(6'd0, 8'd7, 8'd12);
        release_row();
        if (!row_write_ready || !protocol_error || !raw_overrun)
            fail("full-bank error did not preserve recovery path");
        expect_row(8'd13, 7'd2);
        read_run(6'd0, 8'd16, 8'd18);
        read_run(6'd1, 8'd24, 8'd29);
        clear_frame();

        // This edge is invalid even though the table records temporary state.
        illegal_run_with_row_end();
        if (!raw_locked || raw_run_count != 1 || handoffs != 2)
            fail("combined-invalid event accounting changed");
        clear_frame();

        // Clean input after explicit recovery must work normally.
        push_run(8'd9, 8'd14);
        finish_row(8'd21, 1'b0);
        expect_row(8'd21, 7'd1);
        read_run(6'd0, 8'd9, 8'd14);
        release_row();
        if (raw_locked || !row_write_ready || protocol_error || raw_overrun)
            fail("normal operation did not recover");
        checks = checks + 1;

        if (handoffs != 2 || illegal_events != 2 || reads != 10)
            fail("final accounting mismatch");
        $display("PASS raw handoff checks=%0d handoffs=%0d illegal=%0d reads=%0d",
                 checks, handoffs, illegal_events, reads);
        $finish;
    end
endmodule
