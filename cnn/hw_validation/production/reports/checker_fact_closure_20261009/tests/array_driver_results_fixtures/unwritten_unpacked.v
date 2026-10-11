module unwritten_unpacked(
    input wire [1:0] i_read_index,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
assign o_data = memory[i_read_index];
endmodule
