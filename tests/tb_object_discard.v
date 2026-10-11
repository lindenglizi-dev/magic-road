`timescale 1ns/1ps

module tb_object_discard;
    reg clk = 0;
    reg rst_n = 0;
    always #5 clk = ~clk;
    reg frame_clear = 0;
    reg in_obj_valid = 0;
    reg [1:0] in_obj_index = 0;
    reg [2:0] in_object_count = 0;
    reg in_object_frame_done = 0;
    reg discard_frame = 0;
    reg [1:0] rd_index = 0;
    wire rd_valid;
    wire [2:0] stored_object_count;
    wire object_table_commit;
    wire protocol_error;

    object_frame_store dut (
        .clk(clk), .rst_n(rst_n), .frame_clear(frame_clear),
        .in_obj_valid(in_obj_valid), .in_obj_index(in_obj_index),
        .in_obj_label(6'd3), .in_obj_xmin(8'd10),
        .in_obj_xmax(8'd20), .in_obj_ymin(8'd5), .in_obj_ymax(8'd15),
        .in_obj_center_x(8'd15), .in_obj_center_y(8'd10),
        .in_obj_area(16'd100), .in_obj_width(9'd11),
        .in_obj_height(9'd11), .in_obj_fill_level(2'd3),
        .in_obj_class(2'd1), .in_object_count(in_object_count),
        .in_object_frame_done(in_object_frame_done),
        .discard_frame(discard_frame),
        .rd_index(rd_index), .rd_valid(rd_valid),
        .track_rd_index(2'd0),
        .stored_object_count(stored_object_count),
        .object_table_commit(object_table_commit),
        .protocol_error(protocol_error)
    );

    task pulse_object;
        begin
            @(negedge clk); in_obj_valid = 1'b1;
            @(negedge clk); in_obj_valid = 1'b0;
        end
    endtask

    task finish_frame;
        input discard;
        begin
            @(negedge clk);
            discard_frame = discard;
            in_object_count = 3'd1;
            in_object_frame_done = 1'b1;
            @(negedge clk);
            in_object_frame_done = 1'b0;
            discard_frame = 1'b0;
            #1;
        end
    endtask

    initial begin
        repeat (3) @(posedge clk);
        @(negedge clk); rst_n = 1'b1;

        pulse_object();
        finish_frame(1'b1);
        if (stored_object_count != 0 || rd_valid)
            $fatal(1, "discarded frame leaked partial object");

        @(negedge clk); frame_clear = 1'b1;
        @(negedge clk); frame_clear = 1'b0;
        pulse_object();
        finish_frame(1'b0);
        if (stored_object_count != 1 || !rd_valid || protocol_error)
            $fatal(1, "clean object frame failed after discard recovery");

        $display("PASS: invalid CCL frame commits empty object table");
        $finish;
    end
endmodule
