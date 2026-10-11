// One-feature-per-cycle binary linear SVM for the 64-entry HOG stream.
// The weight ROM is deliberately external: training exports the 64 signed
// weights and bias without changing this arithmetic/control module.
module hog_linear_svm #(
    parameter WEIGHT_WIDTH = 12,
    parameter ACC_WIDTH = 40,
    parameter [1:0] NEGATIVE_CLASS = 2'd1,
    parameter [1:0] POSITIVE_CLASS = 2'd2
)(
    input  wire                         clk,
    input  wire                         rst_n,
    input  wire                         feature_valid,
    input  wire [1:0]                   feature_object_index,
    input  wire [1:0]                   feature_cell_x,
    input  wire [1:0]                   feature_cell_y,
    input  wire [1:0]                   feature_bin,
    input  wire [17:0]                  feature_value,
    input  wire                         feature_object_done,
    output wire [5:0]                   weight_address,
    input  wire signed [WEIGHT_WIDTH-1:0] weight_value,
    input  wire signed [ACC_WIDTH-1:0]  bias_value,
    output reg                          result_valid,
    output reg  [1:0]                   result_object_index,
    output reg  [1:0]                   result_class,
    output reg signed [ACC_WIDTH-1:0]   result_score,
    output reg                          busy,
    output reg                          protocol_error
);
    localparam FEATURE_SIGNED_WIDTH = 19;
    localparam PRODUCT_WIDTH = FEATURE_SIGNED_WIDTH + WEIGHT_WIDTH;

    wire [5:0] feature_index = {feature_cell_y, feature_cell_x, feature_bin};
    assign weight_address = feature_index;

    wire signed [FEATURE_SIGNED_WIDTH-1:0] signed_feature =
        $signed({1'b0, feature_value});
    wire signed [PRODUCT_WIDTH-1:0] product = signed_feature * weight_value;
    wire signed [ACC_WIDTH-1:0] product_extended =
        {{(ACC_WIDTH-PRODUCT_WIDTH){product[PRODUCT_WIDTH-1]}}, product};

    reg [5:0] expected_index;
    reg [1:0] active_object_index;
    reg signed [ACC_WIDTH-1:0] accumulator;
    wire signed [ACC_WIDTH-1:0] final_sum = accumulator + product_extended;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result_valid <= 1'b0;
            result_object_index <= 2'd0;
            result_class <= 2'd0;
            result_score <= {ACC_WIDTH{1'b0}};
            busy <= 1'b0;
            protocol_error <= 1'b0;
            expected_index <= 6'd0;
            active_object_index <= 2'd0;
            accumulator <= {ACC_WIDTH{1'b0}};
        end else begin
            result_valid <= 1'b0;

            if (feature_valid) begin
                if (feature_index == 0) begin
                    if (busy || feature_object_done)
                        protocol_error <= 1'b1;
                    busy <= 1'b1;
                    active_object_index <= feature_object_index;
                    expected_index <= 6'd1;
                    accumulator <= bias_value + product_extended;
                end else if (!busy ||
                             (feature_object_index != active_object_index) ||
                             (feature_index != expected_index) ||
                             (feature_object_done != (feature_index == 63))) begin
                    protocol_error <= 1'b1;
                    busy <= 1'b0;
                    expected_index <= 6'd0;
                    accumulator <= {ACC_WIDTH{1'b0}};
                end else if (feature_index == 63) begin
                    result_valid <= 1'b1;
                    result_object_index <= active_object_index;
                    result_score <= final_sum;
                    result_class <= final_sum[ACC_WIDTH-1] ?
                                    NEGATIVE_CLASS : POSITIVE_CLASS;
                    busy <= 1'b0;
                    expected_index <= 6'd0;
                    accumulator <= {ACC_WIDTH{1'b0}};
                end else begin
                    accumulator <= final_sum;
                    expected_index <= expected_index + 1'b1;
                end
            end
        end
    end
endmodule
