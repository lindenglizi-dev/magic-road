`timescale 1ns/1ps

module tb_hog_svm_generated;
    reg clk, rst_n, feature_valid, feature_object_done;
    reg [1:0] feature_object_index;
    reg [1:0] feature_cell_x, feature_cell_y, feature_bin;
    reg [17:0] feature_value;
    wire [5:0] weight_address;
    wire signed [11:0] weight_value;
    wire signed [39:0] bias_value;
    wire result_valid, busy, protocol_error;
    wire [1:0] result_object_index, result_class;
    wire signed [39:0] result_score;

    reg [17:0] feature_memory [0:63];
    reg signed [39:0] expected_score_memory [0:0];
    reg [1:0] expected_class_memory [0:0];
    reg [1023:0] feature_file, score_file, class_file;
    integer i;

    hog_svm_weights u_weights (
        .weight_address(weight_address),
        .weight_value(weight_value), .bias_value(bias_value)
    );

    hog_linear_svm u_svm (
        .clk(clk), .rst_n(rst_n),
        .feature_valid(feature_valid),
        .feature_object_index(feature_object_index),
        .feature_cell_x(feature_cell_x), .feature_cell_y(feature_cell_y),
        .feature_bin(feature_bin), .feature_value(feature_value),
        .feature_object_done(feature_object_done),
        .weight_address(weight_address), .weight_value(weight_value),
        .bias_value(bias_value), .result_valid(result_valid),
        .result_object_index(result_object_index),
        .result_class(result_class), .result_score(result_score),
        .busy(busy), .protocol_error(protocol_error)
    );

    always #5 clk = ~clk;

    initial begin
        if (!$value$plusargs("FEATURE=%s", feature_file) ||
            !$value$plusargs("SCORE=%s", score_file) ||
            !$value$plusargs("CLASS=%s", class_file))
            $fatal(1, "missing generated-vector plusargs");
        $readmemh(feature_file, feature_memory);
        $readmemh(score_file, expected_score_memory);
        $readmemh(class_file, expected_class_memory);

        clk=0; rst_n=0; feature_valid=0; feature_object_done=0;
        feature_object_index=2; feature_cell_x=0; feature_cell_y=0;
        feature_bin=0; feature_value=0;
        repeat (5) @(posedge clk);
        rst_n=1;

        for (i = 0; i < 64; i = i + 1) begin
            @(negedge clk);
            feature_valid = 1'b1;
            feature_cell_y = i[5:4];
            feature_cell_x = i[3:2];
            feature_bin = i[1:0];
            feature_value = feature_memory[i];
            feature_object_done = (i == 63);
        end
        @(negedge clk); feature_valid=0; feature_object_done=0;

        wait (result_valid);
        #1;
        if (result_score !== expected_score_memory[0])
            $fatal(1, "score expected=%0d actual=%0d",
                   expected_score_memory[0], result_score);
        if (result_class !== expected_class_memory[0])
            $fatal(1, "class expected=%0d actual=%0d",
                   expected_class_memory[0], result_class);
        if (result_object_index != 2 || protocol_error)
            $fatal(1, "metadata/protocol failure");
        $display("PASS: generated SVM ROM score=%0d class=%0d",
                 result_score, result_class);
        $finish;
    end
endmodule
