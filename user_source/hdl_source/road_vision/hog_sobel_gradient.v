// Streaming 3x3 Sobel front-end for one 32x32 grayscale ROI.
// Outputs the 30x30 valid interior gradients with center coordinates 1..30.
// Direction is quantized to four unsigned bins: 0, 45, 90 and 135 degrees.
module hog_sobel_gradient #(
    parameter ROI_SIZE = 32
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        roi_valid,
    input  wire [1:0]  roi_object_index,
    input  wire [4:0]  roi_x,
    input  wire [4:0]  roi_y,
    input  wire [7:0]  roi_gray,
    output reg         grad_valid,
    output reg  [1:0]  grad_object_index,
    output reg  [4:0]  grad_x,
    output reg  [4:0]  grad_y,
    output reg  [10:0] grad_magnitude,
    output reg  [1:0]  grad_bin,
    output reg         grad_object_done,
    output reg         protocol_error
);
    reg [7:0] line_prev [0:ROI_SIZE-1];
    reg [7:0] line_top  [0:ROI_SIZE-1];
    reg [7:0] top_l2, top_l1;
    reg [7:0] mid_l2, mid_l1;
    reg [7:0] bot_l2, bot_l1;
    reg [1:0] active_object;
    reg [4:0] expected_x, expected_y;
    integer i;

    wire [10:0] left_sum = {3'd0, top_l2} +
                            ({3'd0, mid_l2} << 1) +
                            {3'd0, bot_l2};
    wire [10:0] right_sum = {3'd0, line_top[roi_x]} +
                             ({3'd0, line_prev[roi_x]} << 1) +
                             {3'd0, roi_gray};
    wire [10:0] upper_sum = {3'd0, top_l2} +
                             ({3'd0, top_l1} << 1) +
                             {3'd0, line_top[roi_x]};
    wire [10:0] lower_sum = {3'd0, bot_l2} +
                             ({3'd0, bot_l1} << 1) +
                             {3'd0, roi_gray};
    wire signed [11:0] gx_signed = $signed({1'b0, right_sum}) -
                                    $signed({1'b0, left_sum});
    wire signed [11:0] gy_signed = $signed({1'b0, lower_sum}) -
                                    $signed({1'b0, upper_sum});
    wire [10:0] abs_gx = gx_signed[11] ? (~gx_signed[10:0] + 1'b1) :
                                        gx_signed[10:0];
    wire [10:0] abs_gy = gy_signed[11] ? (~gy_signed[10:0] + 1'b1) :
                                        gy_signed[10:0];
    wire [11:0] magnitude_sum = {1'b0, abs_gx} + {1'b0, abs_gy};
    wire [11:0] twice_gx = {1'b0, abs_gx} << 1;
    wire [11:0] twice_gy = {1'b0, abs_gy} << 1;
    wire [1:0] direction_bin =
        (twice_gy <= {1'b0, abs_gx}) ? 2'd0 :
        (twice_gx <= {1'b0, abs_gy}) ? 2'd2 :
        (gx_signed[11] == gy_signed[11]) ? 2'd1 : 2'd3;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            grad_valid <= 1'b0;
            grad_object_index <= 0;
            grad_x <= 0; grad_y <= 0;
            grad_magnitude <= 0;
            grad_bin <= 0;
            grad_object_done <= 1'b0;
            protocol_error <= 1'b0;
            top_l2 <= 0; top_l1 <= 0;
            mid_l2 <= 0; mid_l1 <= 0;
            bot_l2 <= 0; bot_l1 <= 0;
            active_object <= 0;
            expected_x <= 0; expected_y <= 0;
            for (i = 0; i < ROI_SIZE; i = i + 1) begin
                line_prev[i] <= 0;
                line_top[i] <= 0;
            end
        end else begin
            grad_valid <= 1'b0;
            grad_object_done <= 1'b0;
            if (roi_valid) begin
                if ((roi_x != expected_x) || (roi_y != expected_y) ||
                    ((roi_x == 0) && (roi_y == 0) &&
                     (expected_x != 0 || expected_y != 0)))
                    protocol_error <= 1'b1;

                if ((roi_x == 0) && (roi_y == 0)) begin
                    active_object <= roi_object_index;
                    top_l2 <= 0; top_l1 <= 0;
                    mid_l2 <= 0; mid_l1 <= 0;
                    bot_l2 <= 0; bot_l1 <= 0;
                end else if (roi_object_index != active_object) begin
                    protocol_error <= 1'b1;
                end

                if ((roi_x >= 2) && (roi_y >= 2)) begin
                    grad_valid <= 1'b1;
                    grad_object_index <= roi_object_index;
                    grad_x <= roi_x - 1'b1;
                    grad_y <= roi_y - 1'b1;
                    grad_magnitude <= magnitude_sum[11] ? 11'h7ff :
                                                         magnitude_sum[10:0];
                    grad_bin <= direction_bin;
                    grad_object_done <= (roi_x == ROI_SIZE-1) &&
                                        (roi_y == ROI_SIZE-1);
                end

                line_top[roi_x] <= line_prev[roi_x];
                line_prev[roi_x] <= roi_gray;
                top_l2 <= top_l1;
                top_l1 <= line_top[roi_x];
                mid_l2 <= mid_l1;
                mid_l1 <= line_prev[roi_x];
                bot_l2 <= bot_l1;
                bot_l1 <= roi_gray;

                if (roi_x == ROI_SIZE-1) begin
                    expected_x <= 0;
                    if (roi_y == ROI_SIZE-1)
                        expected_y <= 0;
                    else
                        expected_y <= roi_y + 1'b1;
                end else begin
                    expected_x <= roi_x + 1'b1;
                end
            end
        end
    end
endmodule

