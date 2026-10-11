module indexed_read(
    input wire i_clk,
    input wire [1:0] i_write_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [1:0] read_index;
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_write_index] <= i_data;
end
assign o_data = memory[read_index];
endmodule
