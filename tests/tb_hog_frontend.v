`timescale 1ns/1ps

module tb_hog_frontend;
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
    integer x, y, errors, grad_count, feature_count;
    integer cell_width, cell_height, expected_value;

    hog_sobel_gradient u_grad (
        .clk(clk), .rst_n(rst_n),
        .roi_valid(roi_valid), .roi_object_index(roi_object_index),
        .roi_x(roi_x), .roi_y(roi_y), .roi_gray(roi_gray),
        .grad_valid(grad_valid), .grad_object_index(grad_object_index),
        .grad_x(grad_x), .grad_y(grad_y),
        .grad_magnitude(grad_magnitude), .grad_bin(grad_bin),
        .grad_object_done(grad_object_done),
        .protocol_error(grad_error)
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
        if (grad_valid) begin
            grad_count = grad_count + 1;
            if ((grad_magnitude != 8) || (grad_bin != 0) ||
                (grad_x < 1) || (grad_x > 30) ||
                (grad_y < 1) || (grad_y > 30)) begin
                $display("FAIL: gradient x=%0d y=%0d mag=%0d bin=%0d",
                         grad_x, grad_y, grad_magnitude, grad_bin);
                errors = errors + 1;
            end
        end
        if (feature_valid) begin
            feature_count = feature_count + 1;
            cell_width = ((feature_cell_x == 0) ||
                          (feature_cell_x == 3)) ? 7 : 8;
            cell_height = ((feature_cell_y == 0) ||
                           (feature_cell_y == 3)) ? 7 : 8;
            expected_value = (feature_bin == 0) ?
                             (cell_width * cell_height * 8) : 0;
            if ((feature_object_index != 1) ||
                (feature_value != expected_value)) begin
                $display("FAIL: feature cy=%0d cx=%0d bin=%0d value=%0d expected=%0d",
                         feature_cell_y, feature_cell_x, feature_bin,
                         feature_value, expected_value);
                errors = errors + 1;
            end
        end
    end

    initial begin
        clk=0; rst_n=0; roi_valid=0; roi_object_index=1;
        roi_x=0; roi_y=0; roi_gray=0;
        errors=0; grad_count=0; feature_count=0;
        repeat (5) @(posedge clk);
        rst_n=1;

        // Horizontal ramp: exact Sobel result is |Gx|=8, Gy=0.
        for (y = 0; y < 32; y = y + 1)
            for (x = 0; x < 32; x = x + 1) begin
                @(negedge clk);
                roi_valid = 1;
                roi_x = x; roi_y = y; roi_gray = x;
            end
        @(negedge clk); roi_valid=0;

        wait (feature_object_done);
        repeat (3) @(posedge clk);
        if (grad_count != 900) begin
            $display("FAIL: gradient count=%0d", grad_count); errors=errors+1;
        end
        if (feature_count != 64) begin
            $display("FAIL: feature count=%0d", feature_count); errors=errors+1;
        end
        if (grad_error || hist_error) begin
            $display("FAIL: HOG protocol error grad=%0d hist=%0d",
                     grad_error, hist_error); errors=errors+1;
        end
        if (errors == 0)
            $display("PASS: Sobel gradient and 4x4x4 HOG cell histogram");
        else
            $fatal(1, "HOG frontend errors=%0d", errors);
        $finish;
    end
endmodule

