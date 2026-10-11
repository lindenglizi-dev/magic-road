module multidimensional_partial(
    input wire i_clk,
    input wire [1:0] i_first_index,
    input wire i_second_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3][0:1];
always @(posedge i_clk) begin
    memory[i_first_index][i_second_index] <= i_data;
end
assign o_data = memory[i_first_index][i_second_index];
endmodule
