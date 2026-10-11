`timescale 1ns/1ps

module tb_roi_frame_reader;
    reg clk, rst_n;
    reg frame_ready, boxes_update;
    reg [31:0] frame_id, boxes_frame_id;
    reg [2:0] object_count;
    reg [159:0] boxes;
    wire release_frame, rd_req_valid;
    wire [15:0] rd_req_addr;
    reg rd_rsp_valid;
    reg [7:0] rd_rsp_gray;
    wire roi_valid, busy, frame_done, pair_miss, protocol_error;
    wire [1:0] roi_object_index;
    wire [4:0] roi_x, roi_y;
    wire [7:0] roi_gray, roi_checksum;
    wire [31:0] completed_frame_id;
    integer errors, pixel_count, done_count, miss_count;
    integer expected_x, expected_y, expected_addr;

    roi_frame_reader dut (
        .clk(clk), .rst_n(rst_n),
        .frame_ready(frame_ready), .frame_id(frame_id),
        .boxes_update(boxes_update), .boxes_frame_id(boxes_frame_id),
        .object_count(object_count), .boxes(boxes),
        .release_frame(release_frame),
        .rd_req_valid(rd_req_valid), .rd_req_addr(rd_req_addr),
        .rd_rsp_valid(rd_rsp_valid), .rd_rsp_gray(rd_rsp_gray),
        .roi_valid(roi_valid), .roi_object_index(roi_object_index),
        .roi_x(roi_x), .roi_y(roi_y), .roi_gray(roi_gray),
        .busy(busy), .frame_done(frame_done),
        .completed_frame_id(completed_frame_id),
        .roi_checksum(roi_checksum), .pair_miss(pair_miss),
        .protocol_error(protocol_error)
    );

    always #5 clk = ~clk;

    // One-cycle synchronous memory response.
    always @(posedge clk) begin
        rd_rsp_valid <= rd_req_valid;
        if (rd_req_valid)
            rd_rsp_gray <= rd_req_addr[7:0] ^ rd_req_addr[15:8];
    end

    always @(posedge clk) begin
        if (roi_valid) begin
            expected_x = 10 + ((roi_x * 16 + 8) >> 5);
            expected_y = 20 + ((roi_y * 8 + 4) >> 5);
            expected_addr = expected_y * 256 + expected_x;
            if (roi_object_index != 0 ||
                roi_gray !== (expected_addr[7:0] ^ expected_addr[15:8])) begin
                $display("FAIL: ROI (%0d,%0d) gray=%0d expected_addr=%0d",
                         roi_x, roi_y, roi_gray, expected_addr);
                errors = errors + 1;
            end
            pixel_count = pixel_count + 1;
        end
        if (frame_done) done_count = done_count + 1;
        if (pair_miss) miss_count = miss_count + 1;
    end

    task pulse_pair;
        input [31:0] f_id;
        input [31:0] b_id;
        begin
            @(negedge clk);
            frame_id = f_id; frame_ready = 1;
            boxes_frame_id = b_id; boxes_update = 1;
            @(negedge clk);
            frame_ready = 0; boxes_update = 0;
        end
    endtask

    initial begin
        clk=0; rst_n=0; frame_ready=0; boxes_update=0;
        frame_id=0; boxes_frame_id=0; object_count=0; boxes=0;
        rd_rsp_valid=0; rd_rsp_gray=0;
        errors=0; pixel_count=0; done_count=0; miss_count=0;
        repeat (5) @(posedge clk);
        rst_n=1;

        // One 16x8 candidate normalized to 32x32.
        boxes[39:0] = {1'b1, 2'd1, 8'd10, 8'd25,
                       8'd20, 8'd27, 5'd0};
        object_count = 1;
        pulse_pair(32'd3, 32'd3);
        wait (done_count == 1);
        repeat (4) @(posedge clk);
        if (pixel_count != 1024) begin
            $display("FAIL: ROI pixel_count=%0d", pixel_count);
            errors = errors + 1;
        end
        if (completed_frame_id != 3) begin
            $display("FAIL: completed frame id=%0d", completed_frame_id);
            errors = errors + 1;
        end

        // A newer box snapshot makes the older buffered frame stale.
        pulse_pair(32'd5, 32'd6);
        repeat (8) @(posedge clk);
        if (miss_count != 1) begin
            $display("FAIL: pair miss count=%0d", miss_count);
            errors = errors + 1;
        end
        if (protocol_error) begin
            $display("FAIL: unexpected ROI protocol error");
            errors = errors + 1;
        end

        if (errors == 0)
            $display("PASS: CCL box is normalized into a 32x32 ROI stream");
        else
            $fatal(1, "ROI reader errors=%0d", errors);
        $finish;
    end
endmodule

