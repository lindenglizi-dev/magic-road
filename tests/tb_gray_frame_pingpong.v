`timescale 1ns/1ps

module tb_gray_frame_pingpong;
    reg wr_clk, rd_clk, wr_rst_n, rd_rst_n;
    reg wr_valid, wr_sof, wr_eol, wr_eof;
    reg [7:0] wr_gray;
    reg [2:0] wr_x, wr_y;
    wire wr_protocol_error, wr_frame_drop;
    wire [31:0] wr_captured_count;
    wire rd_frame_ready, rd_frame_bank, rd_owned;
    wire [31:0] rd_frame_id;
    reg rd_release, rd_req_valid;
    reg [15:0] rd_req_addr;
    wire rd_rsp_valid;
    wire [7:0] rd_rsp_gray;
    wire rd_protocol_error;
    integer x, y, errors, ready_count, drop_count;

    gray_frame_pingpong #(
        .X_WIDTH(3), .Y_WIDTH(3), .ADDR_WIDTH(16),
        .FRAME_WIDTH(8), .FRAME_HEIGHT(4)
    ) dut (
        .wr_clk(wr_clk), .wr_rst_n(wr_rst_n),
        .wr_valid(wr_valid), .wr_gray(wr_gray),
        .wr_x(wr_x), .wr_y(wr_y), .wr_sof(wr_sof),
        .wr_eol(wr_eol), .wr_eof(wr_eof),
        .wr_protocol_error(wr_protocol_error),
        .wr_frame_drop(wr_frame_drop),
        .wr_captured_count(wr_captured_count),
        .rd_clk(rd_clk), .rd_rst_n(rd_rst_n),
        .rd_frame_ready(rd_frame_ready), .rd_frame_id(rd_frame_id),
        .rd_frame_bank(rd_frame_bank), .rd_owned(rd_owned),
        .rd_release(rd_release), .rd_req_valid(rd_req_valid),
        .rd_req_addr(rd_req_addr), .rd_rsp_valid(rd_rsp_valid),
        .rd_rsp_gray(rd_rsp_gray),
        .rd_protocol_error(rd_protocol_error)
    );

    always #5 wr_clk = ~wr_clk;
    always #3.5 rd_clk = ~rd_clk;

    always @(posedge rd_clk)
        if (rd_frame_ready)
            ready_count = ready_count + 1;
    always @(posedge wr_clk)
        if (wr_frame_drop)
            drop_count = drop_count + 1;

    task send_frame;
        input [7:0] base;
        begin
            for (y = 0; y < 4; y = y + 1) begin
                for (x = 0; x < 8; x = x + 1) begin
                    @(negedge wr_clk);
                    wr_valid = 1'b1;
                    wr_sof = (x == 0) && (y == 0);
                    wr_x = x; wr_y = y;
                    wr_gray = base + y*8 + x;
                end
                @(negedge wr_clk);
                wr_valid = 0; wr_sof = 0; wr_eol = 1;
                @(negedge wr_clk); wr_eol = 0;
            end
            repeat (2) @(negedge wr_clk);
            wr_eof = 1;
            @(negedge wr_clk); wr_eof = 0;
            repeat (5) @(negedge wr_clk);
        end
    endtask

    task send_bad_frame;
        input [7:0] base;
        begin
            for (y = 0; y < 4; y = y + 1) begin
                for (x = 0; x < 8; x = x + 1) begin
                    @(negedge wr_clk);
                    wr_valid = 1'b1;
                    wr_sof = (x == 0) && (y == 0);
                    // Duplicate one coordinate without changing pixel count.
                    wr_x = ((x == 3) && (y == 1)) ? 2 : x;
                    wr_y = y;
                    wr_gray = base + y*8 + x;
                end
                @(negedge wr_clk);
                wr_valid = 0; wr_sof = 0; wr_eol = 1;
                @(negedge wr_clk); wr_eol = 0;
            end
            repeat (2) @(negedge wr_clk);
            wr_eof = 1;
            @(negedge wr_clk); wr_eof = 0;
            repeat (5) @(negedge wr_clk);
        end
    endtask

    task read_check;
        input [15:0] addr;
        input [7:0] expected;
        begin
            @(negedge rd_clk); rd_req_valid = 1; rd_req_addr = addr;
            @(negedge rd_clk); rd_req_valid = 0;
            wait (rd_rsp_valid);
            #1;
            if (rd_rsp_gray !== expected) begin
                $display("FAIL: address=%0d expected=%0d actual=%0d",
                         addr, expected, rd_rsp_gray);
                errors = errors + 1;
            end
        end
    endtask

    initial begin
        wr_clk=0; rd_clk=0; wr_rst_n=0; rd_rst_n=0;
        wr_valid=0; wr_sof=0; wr_eol=0; wr_eof=0; wr_gray=0;
        wr_x=0; wr_y=0; rd_release=0; rd_req_valid=0; rd_req_addr=0;
        errors=0; ready_count=0; drop_count=0;
        repeat (5) @(posedge wr_clk);
        wr_rst_n=1; rd_rst_n=1;

        send_bad_frame(8'h01);             // malformed frame is not published
        repeat (8) @(posedge rd_clk);
        if ((ready_count != 0) || (wr_captured_count != 0)) begin
            $display("FAIL: malformed frame was published"); errors=errors+1;
        end

        send_frame(8'h10);                 // bank 0, reader owns it
        wait (ready_count == 1);
        repeat (2) @(posedge rd_clk);
        read_check(16'd0, 8'h10);
        read_check(16'd31, 8'h2f);

        send_frame(8'h40);                 // bank 1 completes; notification dropped
        send_frame(8'h70);                 // bank 0 protected; capture dropped

        @(negedge rd_clk); rd_release=1;
        @(negedge rd_clk); rd_release=0;
        repeat (6) @(posedge wr_clk);
        send_frame(8'ha0);                 // bank 0 is free and reusable
        wait (ready_count == 2);
        repeat (2) @(posedge rd_clk);
        read_check(16'd0, 8'ha0);
        read_check(16'd31, 8'hbf);

        if (!wr_protocol_error) begin
            $display("FAIL: malformed frame was not reported"); errors=errors+1;
        end
        // A dropped notification is intentionally reported in the read domain.
        if (!rd_protocol_error) begin
            $display("FAIL: missed-frame notification was not reported");
            errors=errors+1;
        end
        if ((drop_count != 1) || (wr_captured_count != 3)) begin
            $display("FAIL: drop_count=%0d captured=%0d", drop_count,
                     wr_captured_count);
            errors=errors+1;
        end
        if (errors == 0)
            $display("PASS: ping-pong ownership, invalid-frame discard and conflict containment");
        else
            $fatal(1, "ping-pong errors=%0d", errors);
        $finish;
    end
endmodule
