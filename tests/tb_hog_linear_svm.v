`timescale 1ns/1ps

module tb_hog_linear_svm;
    reg clk, rst_n, feature_valid, feature_object_done;
    reg [1:0] feature_object_index;
    reg [1:0] feature_cell_x, feature_cell_y, feature_bin;
    reg [17:0] feature_value;
    wire [5:0] weight_address;
    reg signed [11:0] weight_value;
    reg signed [39:0] bias_value;
    wire result_valid, busy, protocol_error;
    wire [1:0] result_object_index, result_class;
    wire signed [39:0] result_score;
    integer result_count, errors;

    hog_linear_svm u_dut (
        .clk(clk), .rst_n(rst_n),
        .feature_valid(feature_valid),
        .feature_object_index(feature_object_index),
        .feature_cell_x(feature_cell_x), .feature_cell_y(feature_cell_y),
        .feature_bin(feature_bin), .feature_value(feature_value),
        .feature_object_done(feature_object_done),
        .weight_address(weight_address), .weight_value(weight_value),
        .bias_value(bias_value),
        .result_valid(result_valid),
        .result_object_index(result_object_index),
        .result_class(result_class), .result_score(result_score),
        .busy(busy), .protocol_error(protocol_error)
    );

    always #5 clk = ~clk;

    always @* begin
        weight_value = weight_address[0] ? -12'sd2 : 12'sd3;
    end

    always @(posedge clk) begin
        if (result_valid) begin
            if (result_count == 0) begin
                if ((result_object_index != 0) ||
                    (result_class != 1) || (result_score != -40)) begin
                    $display("FAIL: object0 class=%0d score=%0d",
                             result_class, result_score);
                    errors = errors + 1;
                end
            end else if (result_count == 1) begin
                if ((result_object_index != 1) ||
                    (result_class != 2) || (result_score != 120)) begin
                    $display("FAIL: object1 class=%0d score=%0d",
                             result_class, result_score);
                    errors = errors + 1;
                end
            end else begin
                errors = errors + 1;
            end
            result_count = result_count + 1;
        end
    end

    task send_feature;
        input [1:0] object_index;
        input [5:0] index;
        input [17:0] value;
        begin
            @(negedge clk);
            feature_valid = 1'b1;
            feature_object_index = object_index;
            feature_cell_y = index[5:4];
            feature_cell_x = index[3:2];
            feature_bin = index[1:0];
            feature_value = value;
            feature_object_done = (index == 63);
        end
    endtask

    integer i;
    initial begin
        clk=0; rst_n=0; feature_valid=0; feature_object_done=0;
        feature_object_index=0; feature_cell_x=0; feature_cell_y=0;
        feature_bin=0; feature_value=0; bias_value=-40'sd1000;
        result_count=0; errors=0;
        repeat (5) @(posedge clk);
        rst_n=1;

        // Sum = -1000 + 3*(1+3+...+63) - 2*(2+4+...+64) = -40.
        for (i = 0; i < 64; i = i + 1)
            send_feature(0, i[5:0], i + 1);
        @(negedge clk); feature_valid=0; feature_object_done=0;
        repeat (2) @(posedge clk);

        // Reverse features: score = +120.
        for (i = 0; i < 64; i = i + 1)
            send_feature(1, i[5:0], 64 - i);
        @(negedge clk); feature_valid=0; feature_object_done=0;
        repeat (2) @(posedge clk);

        if (result_count != 2) begin
            $display("FAIL: result count=%0d", result_count);
            errors = errors + 1;
        end
        if (protocol_error) begin
            $display("FAIL: unexpected protocol error");
            errors = errors + 1;
        end

        // A stream that starts at index 1 must be rejected and diagnosed.
        send_feature(2, 6'd1, 18'd7);
        @(negedge clk); feature_valid=0; feature_object_done=0;
        repeat (2) @(posedge clk);
        if (!protocol_error) begin
            $display("FAIL: malformed feature order was not detected");
            errors = errors + 1;
        end

        if (errors == 0)
            $display("PASS: serial HOG linear SVM MAC and protocol guard");
        else
            $fatal(1, "HOG SVM errors=%0d", errors);
        $finish;
    end
endmodule
