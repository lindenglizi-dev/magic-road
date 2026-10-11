`timescale 1ns/1ps

// Fault injection for the spatial background RAM. The second frame swaps two
// coordinates while keeping the total pixel count correct. A pure +1 address
// counter cannot detect this; coordinate checking must flag it and block all
// writes from the first bad pixel onward.
module tb_background_address_guard;
    localparam W = 8;
    localparam H = 2;
    reg clk = 0;
    reg rst_n = 0;
    always #5 clk = ~clk;

    reg in_valid = 0;
    reg [7:0] in_gray = 0;
    reg [7:0] in_x = 0;
    reg [7:0] in_y = 0;
    reg in_sof = 0;
    reg in_eol = 0;
    reg in_eof = 0;
    wire background_ready;
    wire [7:0] learned_frame_count;
    wire protocol_error;
    integer row, col, linear;
    reg [7:0] old5, old6, old12;

    background_model #(
        .X_WIDTH(8), .Y_WIDTH(8), .ADDR_WIDTH(4),
        .FRAME_WIDTH(W), .FRAME_HEIGHT(H),
        .LEARN_FRAMES(1), .LEARN_SHIFT(1), .UPDATE_SHIFT(2)
    ) dut (
        .clk(clk), .rst_n(rst_n),
        .in_valid(in_valid), .in_gray(in_gray),
        .in_x(in_x), .in_y(in_y),
        .in_sof(in_sof), .in_eol(in_eol), .in_eof(in_eof),
        .diff_threshold(8'd10), .update_enable(1'b1),
        .freeze_foreground(1'b0), .relearn(1'b0),
        .background_ready(background_ready),
        .learned_frame_count(learned_frame_count),
        .protocol_error(protocol_error)
    );

    task send_frame;
        input integer corrupt_coordinates;
        input integer base_value;
        begin
            linear = 0;
            for (row = 0; row < H; row = row + 1) begin
                for (col = 0; col < W; col = col + 1) begin
                    @(negedge clk);
                    in_valid = 1'b1;
                    in_gray = base_value + linear;
                    in_x = col;
                    in_y = row;
                    in_sof = (linear == 0);
                    if (corrupt_coordinates && linear == 5)
                        in_x = 8'd6;
                    else if (corrupt_coordinates && linear == 6)
                        in_x = 8'd5;
                    linear = linear + 1;
                end
                @(negedge clk);
                in_valid = 1'b0;
                in_sof = 1'b0;
                in_eol = 1'b1;
                @(negedge clk);
                in_eol = 1'b0;
            end
            @(negedge clk); in_eof = 1'b1;
            @(negedge clk); in_eof = 1'b0;
            repeat (8) @(posedge clk);
        end
    endtask

    initial begin
        repeat (3) @(posedge clk);
        @(negedge clk); rst_n = 1'b1;

        send_frame(0, 20);
        if (protocol_error || !background_ready || learned_frame_count != 1)
            $fatal(1, "clean learning frame failed");
        old5 = dut.background_mem[5];
        old6 = dut.background_mem[6];
        old12 = dut.background_mem[12];

        // Same number of pixels, but x=5 and x=6 are exchanged.
        send_frame(1, 200);
        if (!protocol_error)
            $fatal(1, "coordinate corruption was not detected");
        if (dut.background_mem[5] !== old5 ||
            dut.background_mem[6] !== old6 ||
            dut.background_mem[12] !== old12)
            $fatal(1, "bad frame modified protected background addresses");

        // A clean SOF must re-arm the checker and recover without reset.
        send_frame(0, 20);
        if (protocol_error)
            $fatal(1, "address guard did not recover on next clean frame");
        $display("PASS: coordinate address guard detects and contains bad frame");
        $finish;
    end
endmodule
