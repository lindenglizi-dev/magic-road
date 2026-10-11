module param_constant_partial(
    input wire i_clk,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
localparam PARAM_ZERO = 0;
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[PARAM_ZERO] <= i_data;
end
assign o_data = memory[1];
endmodule
