`timescale 1ns/1ps
// Measurement-only fixture: actual ROI/HOG/SVM, synthetic synchronous RAM.
// Not included in the Tang project; weights of one are not a trained model.
module tb_roi_hog_svm_measure;
    reg clk = 0;
    reg rst_n = 0;
    always #5 clk = ~clk;
    reg frame_ready = 0;
    reg boxes_update = 0;
    reg [159:0] boxes = 0;
    wire release_frame, rd_req_valid, roi_valid, busy, frame_done;
    wire [15:0] rd_req_addr;
    reg rd_rsp_valid = 0;
    reg [7:0] rd_rsp_gray = 0;
    wire [1:0] roi_object_index;
    wire [4:0] roi_x, roi_y;
    wire [7:0] roi_gray, roi_checksum;
    wire [31:0] completed_frame_id;
    wire pair_miss, reader_error;
    wire grad_valid, grad_done, grad_error;
    wire [1:0] grad_object, grad_bin;
    wire [4:0] grad_x, grad_y;
    wire [10:0] magnitude;
    wire feature_valid, feature_done, hist_busy, hist_error;
    wire [1:0] feature_object, cell_x, cell_y, feature_bin;
    wire [17:0] feature_value;
    wire [5:0] weight_address;
    wire result_valid, svm_busy, svm_error;
    wire [1:0] result_object, result_class;
    wire signed [39:0] result_score;
    integer pixels = 0;
    integer features = 0;
    integer results = 0;
    integer releases = 0;
    integer index;

    roi_frame_reader u_reader (
        .clk(clk), .rst_n(rst_n), .frame_ready(frame_ready), .frame_id(32'd7),
        .boxes_update(boxes_update), .boxes_frame_id(32'd7), .object_count(3'd4),
        .boxes(boxes), .release_frame(release_frame), .rd_req_valid(rd_req_valid),
        .rd_req_addr(rd_req_addr), .rd_rsp_valid(rd_rsp_valid), .rd_rsp_gray(rd_rsp_gray),
        .roi_valid(roi_valid), .roi_object_index(roi_object_index), .roi_x(roi_x),
        .roi_y(roi_y), .roi_gray(roi_gray), .busy(busy), .frame_done(frame_done),
        .completed_frame_id(completed_frame_id), .roi_checksum(roi_checksum),
        .pair_miss(pair_miss), .protocol_error(reader_error)
    );
    hog_sobel_gradient u_grad (
        .clk(clk), .rst_n(rst_n), .roi_valid(roi_valid), .roi_object_index(roi_object_index),
        .roi_x(roi_x), .roi_y(roi_y), .roi_gray(roi_gray), .grad_valid(grad_valid),
        .grad_object_index(grad_object), .grad_x(grad_x), .grad_y(grad_y),
        .grad_magnitude(magnitude), .grad_bin(grad_bin), .grad_object_done(grad_done),
        .protocol_error(grad_error)
    );
    hog_cell_histogram u_hist (
        .clk(clk), .rst_n(rst_n), .grad_valid(grad_valid), .grad_object_index(grad_object),
        .grad_x(grad_x), .grad_y(grad_y), .grad_magnitude(magnitude), .grad_bin(grad_bin),
        .grad_object_done(grad_done), .feature_valid(feature_valid),
        .feature_object_index(feature_object), .feature_cell_x(cell_x), .feature_cell_y(cell_y),
        .feature_bin(feature_bin), .feature_value(feature_value), .feature_object_done(feature_done),
        .busy(hist_busy), .protocol_error(hist_error)
    );
    hog_linear_svm u_svm (
        .clk(clk), .rst_n(rst_n), .feature_valid(feature_valid), .feature_object_index(feature_object),
        .feature_cell_x(cell_x), .feature_cell_y(cell_y), .feature_bin(feature_bin),
        .feature_value(feature_value), .feature_object_done(feature_done), .weight_address(weight_address),
        .weight_value(12'sd1), .bias_value(40'sd0), .result_valid(result_valid),
        .result_object_index(result_object), .result_class(result_class), .result_score(result_score),
        .busy(svm_busy), .protocol_error(svm_error)
    );
    always @(posedge clk) begin
        rd_rsp_valid <= rd_req_valid;
        if (rd_req_valid) rd_rsp_gray <= rd_req_addr[7:0] ^ rd_req_addr[15:8];
        if (rst_n) begin
            if (roi_valid) pixels = pixels + 1;
            if (feature_valid) features = features + 1;
            if (release_frame) releases = releases + 1;
            if (result_valid) begin
                if (result_object != results || result_score != 14176 || result_class != 2)
                    $fatal(1, "score/object differs from Python fixture reference");
                results = results + 1;
            end
            if (reader_error || grad_error || hist_error || svm_error || pair_miss)
                $fatal(1, "pipeline protocol error");
        end
    end
    initial begin
        repeat (5) @(negedge clk);
        rst_n = 1;
        for (index = 0; index < 4; index = index + 1)
            boxes[index*40 +: 40] = {1'b1, 2'd1, 8'd10, 8'd25, 8'd20, 8'd27, 5'd0};
        @(negedge clk); frame_ready = 1; boxes_update = 1;
        @(negedge clk); frame_ready = 0; boxes_update = 0;
        wait(results == 4);
        @(negedge clk);
        if (pixels != 4096 || features != 256 || releases != 1)
            $fatal(1, "unexpected transaction counts");
        $display("PASS: four ROI/HOG/SVM measurement fixture, 4096 pixels, 256 features, 4 results");
        $finish;
    end
    initial begin
        #1000000;
        $fatal(1, "measurement timeout");
    end
endmodule
