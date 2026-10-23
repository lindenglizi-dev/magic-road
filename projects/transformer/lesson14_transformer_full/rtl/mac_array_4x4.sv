`timescale 1ns/1ps
// 16 independent signed INT8 MAC lanes, output-stationary within one C tile.
// a_vec[8*r +: 8] is A[row r,k]; b_vec[8*c +:8] is B[k,col c].
// Deliberately NOT a spatial systolic array: the operand feeder broadcasts
// a 4-row column slice and a 4-column row slice each compute cycle.
module mac_array_4x4 (
    input  logic               clk,
    input  logic               rst_n,
    input  logic               clear,
    input  logic               mac_en,
    input  logic [31:0]        a_vec,
    input  logic [31:0]        b_vec,
    output logic [511:0]       acc_bus
);
    genvar r, c;
    generate
        for (r = 0; r < 4; r = r + 1) begin : g_row
            for (c = 0; c < 4; c = c + 1) begin : g_col
                wire signed [7:0]  a_val = $signed(a_vec[8*r +: 8]);
                wire signed [7:0]  b_val = $signed(b_vec[8*c +: 8]);
                wire signed [15:0] prod = a_val * b_val;
                logic signed [31:0] acc_q;
                assign acc_bus[32*(4*r+c) +: 32] = acc_q;
                always_ff @(posedge clk or negedge rst_n) begin
                    if (!rst_n)
                        acc_q <= 32'sd0;
                    else if (clear)
                        acc_q <= 32'sd0;
                    else if (mac_en)
                        acc_q <= acc_q + {{16{prod[15]}}, prod};
                end
            end
        end
    endgenerate
endmodule
