`timescale 1ns/1ps

module tb_binary_cleanup_3x3;
    reg clk, rst_n;
    reg in_valid, in_mask, in_sof, in_eol, in_eof;
    reg [2:0] in_x, in_y;
    wire out_valid, out_mask, out_sof, out_eol, out_eof;
    wire [2:0] out_x, out_y;
    wire protocol_error;
    integer x, y, output_count, one_count, errors;
    reg phase;

    binary_cleanup_3x3 #(
        .X_WIDTH(3), .Y_WIDTH(3), .FRAME_WIDTH(5), .FRAME_HEIGHT(5),
        .ENABLE(1), .MIN_NEIGHBORS(3), .REQUIRE_CENTER(1)
    ) dut (
        .clk(clk), .rst_n(rst_n), .in_valid(in_valid),
        .in_mask(in_mask), .in_x(in_x), .in_y(in_y),
        .in_sof(in_sof), .in_eol(in_eol), .in_eof(in_eof),
        .out_valid(out_valid), .out_mask(out_mask),
        .out_x(out_x), .out_y(out_y), .out_sof(out_sof),
        .out_eol(out_eol), .out_eof(out_eof),
        .protocol_error(protocol_error)
    );

    always #5 clk = ~clk;

    always @(posedge clk) begin
        #1;
        if (out_valid) begin
            if ((out_x !== (output_count % 5)) ||
                (out_y !== (output_count / 5))) begin
                $display("FAIL: phase=%0d output=%0d coordinate=(%0d,%0d)",
                         phase, output_count, out_x, out_y);
                errors = errors + 1;
            end
            if (out_sof !== (output_count == 0)) begin
                $display("FAIL: SOF position phase=%0d output=%0d", phase,
                         output_count);
                errors = errors + 1;
            end
            if (out_mask)
                one_count = one_count + 1;
            output_count = output_count + 1;
        end
    end

    task send_frame;
        input dense_block;
        begin
            output_count = 0;
            one_count = 0;
            for (y = 0; y < 5; y = y + 1) begin
                for (x = 0; x < 5; x = x + 1) begin
                    @(negedge clk);
                    in_valid = 1'b1;
                    in_x = x;
                    in_y = y;
                    in_sof = (x == 0) && (y == 0);
                    if (dense_block)
                        in_mask = (x >= 1) && (x <= 3) &&
                                  (y >= 1) && (y <= 3);
                    else
                        in_mask = (x == 2) && (y == 2);
                end
                @(negedge clk);
                in_valid = 1'b0; in_sof = 1'b0; in_mask = 1'b0;
                in_eol = 1'b1;
                @(negedge clk); in_eol = 1'b0;
                repeat (2) @(negedge clk);
            end
            in_eof = 1'b1;
            @(negedge clk); in_eof = 1'b0;
            wait (out_eof);
            @(posedge clk); #2;
            if (output_count != 25) begin
                $display("FAIL: phase=%0d output count=%0d", phase,
                         output_count);
                errors = errors + 1;
            end
            if (!dense_block && one_count != 0) begin
                $display("FAIL: isolated pixel survived, ones=%0d", one_count);
                errors = errors + 1;
            end
            if (dense_block && one_count != 9) begin
                $display("FAIL: dense 3x3 block changed, ones=%0d", one_count);
                errors = errors + 1;
            end
        end
    endtask

    initial begin
        clk = 0; rst_n = 0;
        in_valid = 0; in_mask = 0; in_sof = 0; in_eol = 0; in_eof = 0;
        in_x = 0; in_y = 0; output_count = 0; one_count = 0; errors = 0;
        phase = 0;
        repeat (4) @(posedge clk);
        rst_n = 1;
        send_frame(1'b0);
        phase = 1;
        repeat (4) @(negedge clk);
        send_frame(1'b1);
        if (protocol_error) begin
            $display("FAIL: cleanup protocol_error asserted");
            errors = errors + 1;
        end
        if (errors == 0)
            $display("PASS: 3x3 cleanup removes isolated noise and preserves dense foreground");
        else
            $fatal(1, "3x3 cleanup errors=%0d", errors);
        $finish;
    end
endmodule
