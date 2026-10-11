module packed_partial(
    input wire i_clk,
    input wire [3:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] packed_data;
always @(posedge i_clk) begin
    packed_data[3:0] <= i_data;
end
assign o_data = packed_data;
endmodule
