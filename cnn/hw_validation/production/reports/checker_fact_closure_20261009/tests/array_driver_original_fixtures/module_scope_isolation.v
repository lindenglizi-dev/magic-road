module array_writer(
    input wire i_clk,
    input wire [1:0] i_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_index] <= i_data;
end
assign o_data = memory[i_index];
endmodule

module array_reader(
    input wire [1:0] i_index,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
assign o_data = memory[i_index];
endmodule
