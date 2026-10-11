// Accumulate four direction bins for sixteen 8x8 cells. After each ROI, emit
// 64 features in {cell_y, cell_x, bin} order and clear entries as they leave.
module hog_cell_histogram (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        grad_valid,
    input  wire [1:0]  grad_object_index,
    input  wire [4:0]  grad_x,
    input  wire [4:0]  grad_y,
    input  wire [10:0] grad_magnitude,
    input  wire [1:0]  grad_bin,
    input  wire        grad_object_done,
    output reg         feature_valid,
    output reg  [1:0]  feature_object_index,
    output reg  [1:0]  feature_cell_x,
    output reg  [1:0]  feature_cell_y,
    output reg  [1:0]  feature_bin,
    output reg  [17:0] feature_value,
    output reg         feature_object_done,
    output reg         busy,
    output reg         protocol_error
);
    (* ram_style = "distributed" *) reg [17:0] histogram [0:63];
    wire [5:0] write_index = {grad_y[4:3], grad_x[4:3], grad_bin};
    reg [5:0] emit_index;
    reg [1:0] emit_object_index;
    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            feature_valid <= 1'b0;
            feature_object_index <= 0;
            feature_cell_x <= 0; feature_cell_y <= 0;
            feature_bin <= 0; feature_value <= 0;
            feature_object_done <= 1'b0;
            busy <= 1'b0;
            protocol_error <= 1'b0;
            emit_index <= 0;
            emit_object_index <= 0;
            for (i = 0; i < 64; i = i + 1)
                histogram[i] <= 0;
        end else begin
            feature_valid <= 1'b0;
            feature_object_done <= 1'b0;

            if (grad_valid) begin
                if (busy) begin
                    protocol_error <= 1'b1;
                end else begin
                    histogram[write_index] <= histogram[write_index] +
                                              grad_magnitude;
                    if (grad_object_done) begin
                        busy <= 1'b1;
                        emit_index <= 0;
                        emit_object_index <= grad_object_index;
                    end
                end
            end

            if (busy) begin
                feature_valid <= 1'b1;
                feature_object_index <= emit_object_index;
                feature_cell_y <= emit_index[5:4];
                feature_cell_x <= emit_index[3:2];
                feature_bin <= emit_index[1:0];
                feature_value <= histogram[emit_index];
                histogram[emit_index] <= 0;
                if (emit_index == 63) begin
                    feature_object_done <= 1'b1;
                    busy <= 1'b0;
                end else begin
                    emit_index <= emit_index + 1'b1;
                end
            end
        end
    end
endmodule

