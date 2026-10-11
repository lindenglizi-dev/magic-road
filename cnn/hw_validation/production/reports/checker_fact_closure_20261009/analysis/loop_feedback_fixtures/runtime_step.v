module runtime_step
(
input [2:0] step,
output reg [3:0] value
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + step)
        value[index] = 1'b1;
end

endmodule
