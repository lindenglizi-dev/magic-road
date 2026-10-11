`timescale 1ns/1ps

module tb_ddr_line_banks;
    localparam WIDTH = 5;
    localparam X_WIDTH = 3;
    localparam Y_WIDTH = 4;
    localparam ID_WIDTH = 32;

    reg clk;
    reg rst_n;
    reg cancel;
    reg in_valid;
    wire in_ready;
    reg [ID_WIDTH-1:0] in_task_id;
    reg [Y_WIDTH-1:0] in_y;
    reg in_pixel;
    reg in_last;
    reg in_frame_last;
    wire out_valid;
    reg out_ready;
    wire [ID_WIDTH-1:0] out_task_id;
    wire [Y_WIDTH-1:0] out_y;
    wire [X_WIDTH-1:0] out_x;
    wire out_pixel;
    wire out_last;
    wire out_frame_last;
    wire empty;
    wire protocol_error;
    integer checks;

    ccl_pixel_line_banks #(
        .WIDTH(WIDTH), .X_WIDTH(X_WIDTH), .Y_WIDTH(Y_WIDTH),
        .ID_WIDTH(ID_WIDTH)
    ) dut (
        .clk(clk), .rst_n(rst_n), .cancel(cancel),
        .in_valid(in_valid), .in_ready(in_ready),
        .in_task_id(in_task_id), .in_y(in_y), .in_pixel(in_pixel),
        .in_last(in_last), .in_frame_last(in_frame_last),
        .out_valid(out_valid), .out_ready(out_ready),
        .out_task_id(out_task_id), .out_y(out_y), .out_x(out_x),
        .out_pixel(out_pixel), .out_last(out_last),
        .out_frame_last(out_frame_last), .empty(empty),
        .protocol_error(protocol_error)
    );

    always #5 clk = !clk;

    task fail;
        input [8*96-1:0] message;
        begin
            $display("FAIL: %0s", message);
            $finish(1);
        end
    endtask

    task reset_dut;
        begin
            @(negedge clk);
            rst_n = 1'b0;
            cancel = 1'b0;
            in_valid = 1'b0;
            out_ready = 1'b0;
            repeat (2) @(negedge clk);
            rst_n = 1'b1;
            @(negedge clk);
            if (!empty || protocol_error || out_valid)
                fail("reset state");
            checks = checks + 1;
        end
    endtask

    task send_pixel;
        input [ID_WIDTH-1:0] task_id;
        input [Y_WIDTH-1:0] y;
        input pixel;
        input last;
        input frame_last;
        begin
            @(negedge clk);
            in_task_id = task_id;
            in_y = y;
            in_pixel = pixel;
            in_last = last;
            in_frame_last = frame_last;
            in_valid = 1'b1;
            while (!in_ready) begin
                @(posedge clk);
                @(negedge clk);
            end
            @(posedge clk);
            checks = checks + 1;
            @(negedge clk);
            in_valid = 1'b0;
        end
    endtask

    task send_line;
        input [ID_WIDTH-1:0] task_id;
        input [Y_WIDTH-1:0] y;
        input [WIDTH-1:0] pixels;
        input frame_last;
        integer x;
        begin
            for (x = 0; x < WIDTH; x = x + 1)
                send_pixel(task_id, y, pixels[x], x == WIDTH - 1,
                           frame_last && (x == WIDTH - 1));
        end
    endtask

    task take_pixel;
        input [ID_WIDTH-1:0] task_id;
        input [Y_WIDTH-1:0] y;
        input [X_WIDTH-1:0] x;
        input pixel;
        input last;
        input frame_last;
        input stall_check;
        reg [ID_WIDTH+Y_WIDTH+X_WIDTH+2:0] snapshot;
        begin
            out_ready = 1'b0;
            wait (out_valid);
            @(negedge clk);
            if ({out_task_id, out_y, out_x, out_pixel, out_last, out_frame_last} !==
                {task_id, y, x, pixel, last, frame_last})
                fail("output payload or bank tag mismatch");
            if (stall_check) begin
                snapshot = {out_task_id, out_y, out_x, out_pixel,
                            out_last, out_frame_last};
                repeat (2) begin
                    @(posedge clk);
                    @(negedge clk);
                    if (!out_valid ||
                        {out_task_id, out_y, out_x, out_pixel,
                         out_last, out_frame_last} !== snapshot)
                        fail("output changed under backpressure");
                end
            end
            out_ready = 1'b1;
            @(posedge clk);
            checks = checks + 1;
            @(negedge clk);
            out_ready = 1'b0;
        end
    endtask

    task check_line;
        input [ID_WIDTH-1:0] task_id;
        input [Y_WIDTH-1:0] y;
        input [WIDTH-1:0] pixels;
        input frame_last;
        input stall_first;
        integer x;
        begin
            for (x = 0; x < WIDTH; x = x + 1)
                take_pixel(task_id, y, x[X_WIDTH-1:0], pixels[x],
                           x == WIDTH - 1,
                           frame_last && (x == WIDTH - 1),
                           stall_first && (x == 0));
        end
    endtask

    initial begin
        clk = 1'b0;
        rst_n = 1'b0;
        cancel = 1'b0;
        in_valid = 1'b0;
        in_task_id = 0;
        in_y = 0;
        in_pixel = 0;
        in_last = 0;
        in_frame_last = 0;
        out_ready = 1'b0;
        checks = 0;

        reset_dut();
        send_line(32'd11, 4'd3, 5'b10101, 1'b0);
        send_line(32'd12, 4'd4, 5'b01010, 1'b1);
        @(negedge clk);
        if (in_ready || empty)
            fail("two full banks did not stop input");
        checks = checks + 1;
        in_task_id = 32'hdeadbeef;
        in_y = 4'hf;
        check_line(32'd11, 4'd3, 5'b10101, 1'b0, 1'b1);
        check_line(32'd12, 4'd4, 5'b01010, 1'b1, 1'b0);
        @(negedge clk);
        if (!empty || protocol_error)
            fail("normal alternating-bank drain");
        checks = checks + 1;

        send_line(32'd21, 4'd6, 5'b11111, 1'b0);
        send_line(32'd22, 4'd7, 5'b00000, 1'b0);
        @(negedge clk);
        cancel = 1'b1;
        in_valid = 1'b1;
        out_ready = 1'b1;
        @(posedge clk);
        @(negedge clk);
        if (!empty || out_valid || in_ready || protocol_error)
            fail("dual-full cancel did not empty atomically");
        cancel = 1'b0;
        in_valid = 1'b0;
        repeat (4) begin
            @(posedge clk);
            @(negedge clk);
            if (out_valid)
                fail("late output after cancel");
        end
        checks = checks + 5;

        send_line(32'd31, 4'd8, 5'b10011, 1'b0);
        take_pixel(32'd31, 4'd8, 3'd0, 1'b1, 1'b0, 1'b0, 1'b0);
        take_pixel(32'd31, 4'd8, 3'd1, 1'b1, 1'b0, 1'b0, 1'b0);
        take_pixel(32'd31, 4'd8, 3'd2, 1'b0, 1'b0, 1'b0, 1'b0);
        take_pixel(32'd31, 4'd8, 3'd3, 1'b0, 1'b0, 1'b0, 1'b0);
        cancel = 1'b1;
        out_ready = 1'b1;
        @(posedge clk);
        @(negedge clk);
        if (!empty || out_valid)
            fail("cancel on last pending return leaked output");
        cancel = 1'b0;
        out_ready = 1'b0;
        repeat (3) @(posedge clk);
        if (out_valid)
            fail("last return appeared after cancel");
        checks = checks + 2;

        reset_dut();
        send_pixel(32'd41, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd42, 4'd1, 1'b1, 1'b0, 1'b0);
        @(negedge clk);
        if (!protocol_error)
            fail("task mismatch not detected");
        cancel = 1'b1;
        @(posedge clk);
        @(negedge clk);
        if (!protocol_error)
            fail("protocol error not sticky across cancel");
        checks = checks + 2;

        reset_dut();
        send_pixel(32'd51, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd51, 4'd2, 1'b1, 1'b0, 1'b0);
        @(negedge clk);
        if (!protocol_error)
            fail("y mismatch not detected");
        checks = checks + 1;

        reset_dut();
        send_pixel(32'd61, 4'd1, 1'b1, 1'b1, 1'b0);
        @(negedge clk);
        if (!protocol_error || !empty)
            fail("short line not rejected");
        checks = checks + 1;

        reset_dut();
        send_pixel(32'd71, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd71, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd71, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd71, 4'd1, 1'b0, 1'b0, 1'b0);
        send_pixel(32'd71, 4'd1, 1'b0, 1'b0, 1'b0);
        @(negedge clk);
        if (!protocol_error || !empty)
            fail("missing final last not rejected");
        checks = checks + 1;

        reset_dut();
        send_line(32'd77, 4'd9, 5'b00110, 1'b1);
        check_line(32'd77, 4'd9, 5'b00110, 1'b1, 1'b0);
        if (!empty || protocol_error)
            fail("normal recovery after reset");
        checks = checks + 1;

        $display("PASS line banks checks=%0d", checks);
        $finish;
    end
endmodule
