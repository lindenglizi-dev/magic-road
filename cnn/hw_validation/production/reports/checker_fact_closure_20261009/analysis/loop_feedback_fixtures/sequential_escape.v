module sequential_escape
(
input i_clk,
output reg [3:0] value,
output reg escaped
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = 1'b1;
end
always @(posedge i_clk) begin
    escaped <= index[0];
end

endmodule
