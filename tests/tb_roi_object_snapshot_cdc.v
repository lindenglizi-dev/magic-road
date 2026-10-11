`timescale 1ns/1ps

module tb_roi_object_snapshot_cdc;
    reg src_clk, dst_clk, src_rst_n, dst_rst_n;
    reg frame_clear, obj_valid, object_frame_done, discard_frame;
    reg [1:0] obj_index, obj_class;
    reg [7:0] obj_xmin, obj_xmax, obj_ymin, obj_ymax;
    reg [2:0] object_count;
    wire dst_update;
    wire [31:0] dst_frame_id;
    wire [2:0] dst_object_count;
    wire [159:0] dst_boxes;
    integer errors, updates;

    roi_object_snapshot_cdc dut (
        .src_clk(src_clk), .src_rst_n(src_rst_n),
        .frame_clear(frame_clear), .obj_valid(obj_valid),
        .obj_index(obj_index), .obj_class(obj_class),
        .obj_xmin(obj_xmin), .obj_xmax(obj_xmax),
        .obj_ymin(obj_ymin), .obj_ymax(obj_ymax),
        .object_count(object_count),
        .object_frame_done(object_frame_done),
        .discard_frame(discard_frame),
        .dst_clk(dst_clk), .dst_rst_n(dst_rst_n),
        .dst_update(dst_update), .dst_frame_id(dst_frame_id),
        .dst_object_count(dst_object_count), .dst_boxes(dst_boxes)
    );

    always #5 src_clk = ~src_clk;
    always #3.5 dst_clk = ~dst_clk;
    always @(posedge dst_clk) if (dst_update) updates = updates + 1;

    initial begin
        src_clk=0; dst_clk=0; src_rst_n=0; dst_rst_n=0;
        frame_clear=0; obj_valid=0; object_frame_done=0;
        discard_frame=0; obj_index=0; obj_class=0;
        obj_xmin=0; obj_xmax=0; obj_ymin=0; obj_ymax=0;
        object_count=0; errors=0; updates=0;
        repeat (5) @(posedge src_clk);
        src_rst_n=1; dst_rst_n=1;

        @(negedge src_clk); frame_clear=1;
        @(negedge src_clk); frame_clear=0;
        obj_valid=1; obj_index=2; obj_class=2;
        obj_xmin=11; obj_xmax=31; obj_ymin=7; obj_ymax=47;
        object_count=1; object_frame_done=1;
        @(negedge src_clk); obj_valid=0; object_frame_done=0;
        wait (updates == 1);
        #1;
        if ((dst_frame_id != 0) || (dst_object_count != 1) ||
            !dst_boxes[119] || (dst_boxes[116:109] != 11) ||
            (dst_boxes[108:101] != 31) ||
            (dst_boxes[100:93] != 7) ||
            (dst_boxes[92:85] != 47)) begin
            $display("FAIL: ROI object CDC payload"); errors=errors+1;
        end

        @(negedge src_clk); frame_clear=1;
        @(negedge src_clk); frame_clear=0; discard_frame=1;
        object_count=2; object_frame_done=1;
        @(negedge src_clk); object_frame_done=0; discard_frame=0;
        wait (updates == 2);
        #1;
        if ((dst_frame_id != 1) || (dst_object_count != 0) ||
            (dst_boxes != 0)) begin
            $display("FAIL: discarded snapshot was not empty"); errors=errors+1;
        end

        if (errors == 0)
            $display("PASS: candidate table snapshot CDC and discard handling");
        else
            $fatal(1, "ROI snapshot errors=%0d", errors);
        $finish;
    end
endmodule

