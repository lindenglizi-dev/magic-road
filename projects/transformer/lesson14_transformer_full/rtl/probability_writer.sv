module probability_writer #(
    parameter integer ADDR_W=16
)(
    input  logic clk, rst_n,
    input  logic [6:0] seq_len,
    input  logic [6:0] row_idx,
    input  logic [7:0] in_data,
    input  logic [6:0] in_index,
    input  logic in_valid, in_last,
    output logic in_ready,
    output logic wr_en,
    output logic [1:0] wr_bank,
    output logic [ADDR_W-1:0] wr_addr,
    output logic signed [7:0] wr_data,
    output logic row_done
);
    // The receiver has no backpressure in this teaching version.
    // For P(LxL) as GEMM A, bank by row, local address by row/4 and column.
    assign in_ready = 1'b1;
    assign wr_en = in_valid && in_ready;
    assign wr_bank = row_idx[1:0];
    assign wr_addr = (row_idx >> 2) * seq_len + in_index;
    wire [7:0] rounded = (in_data >> 1) + {7'b0,in_data[0]};
    assign wr_data = (rounded > 8'd127) ? 8'sd127 : $signed(rounded[7:0]);
    always_ff @(posedge clk or negedge rst_n)
        if (!rst_n) row_done <= 1'b0;
        else row_done <= wr_en && in_last;
endmodule
