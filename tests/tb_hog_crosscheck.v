`timescale 1ns/1ps

module tb_hog_crosscheck;
    reg clk, rst_n, roi_valid;
    reg [1:0] roi_object_index;
    reg [4:0] roi_x, roi_y;
    reg [7:0] roi_gray;
    wire grad_valid, grad_object_done, grad_error;
    wire [1:0] grad_object_index, grad_bin;
    wire [4:0] grad_x, grad_y;
    wire [10:0] grad_magnitude;
    wire feature_valid, feature_object_done, hist_busy, hist_error;
    wire [1:0] feature_object_index, feature_cell_x;
    wire [1:0] feature_cell_y, feature_bin;
    wire [17:0] feature_value;

    reg [7:0] roi_memory [0:1023];
    reg [1023:0] roi_file;
    reg [1023:0] output_file;
    integer output_handle;
    integer x, y, feature_count;

    hog_sobel_gradient u_grad (
        .clk(clk), .rst_n(rst_n),
        .roi_valid(roi_valid), .roi_object_index(roi_object_index),
        .roi_x(roi_x), .roi_y(roi_y), .roi_gray(roi_gray),
        .grad_valid(grad_valid), .grad_object_index(grad_object_index),
        .grad_x(grad_x), .grad_y(grad_y),
        .grad_magnitude(grad_magnitude), .grad_bin(grad_bin),
        .grad_object_done(grad_object_done), .protocol_error(grad_error)
    );

    hog_cell_histogram u_hist (
        .clk(clk), .rst_n(rst_n),
        .grad_valid(grad_valid), .grad_object_index(grad_object_index),
        .grad_x(grad_x), .grad_y(grad_y),
        .grad_magnitude(grad_magnitude), .grad_bin(grad_bin),
        .grad_object_done(grad_object_done),
        .feature_valid(feature_valid),
        .feature_object_index(feature_object_index),
        .feature_cell_x(feature_cell_x), .feature_cell_y(feature_cell_y),
        .feature_bin(feature_bin), .feature_value(feature_value),
        .feature_object_done(feature_object_done),
        .busy(hist_busy), .protocol_error(hist_error)
    );

    always #5 clk = ~clk;

    always @(posedge clk) begin
        if (feature_valid) begin
            $fdisplay(output_handle, "%05x", feature_value);
            feature_count = feature_count + 1;
            if ({feature_cell_y, feature_cell_x, feature_bin} != feature_count - 1)
                $fatal(1, "feature order mismatch at %0d", feature_count - 1);
        end
    end

    initial begin
        if (!$value$plusargs("ROI=%s", roi_file))
            $fatal(1, "missing +ROI=<hex file>");
        if (!$value$plusargs("OUT=%s", output_file))
            $fatal(1, "missing +OUT=<hex file>");
        $readmemh(roi_file, roi_memory);
        output_handle = $fopen(output_file, "w");
        if (output_handle == 0)
            $fatal(1, "cannot open output feature file");

        clk = 0; rst_n = 0; roi_valid = 0;
        roi_object_index = 2; roi_x = 0; roi_y = 0; roi_gray = 0;
        feature_count = 0;
        repeat (5) @(posedge clk);
        rst_n = 1;

        for (y = 0; y < 32; y = y + 1)
            for (x = 0; x < 32; x = x + 1) begin
                @(negedge clk);
                roi_valid = 1;
                roi_x = x;
                roi_y = y;
                roi_gray = roi_memory[y * 32 + x];
            end
        @(negedge clk);
        roi_valid = 0;

        wait (feature_object_done);
        repeat (2) @(posedge clk);
        $fclose(output_handle);
        if (feature_count != 64)
            $fatal(1, "feature count=%0d", feature_count);
        if (grad_error || hist_error)
            $fatal(1, "protocol error grad=%0d hist=%0d", grad_error, hist_error);
        $display("PASS: exported 64 RTL HOG features");
        $finish;
    end
endmodule
