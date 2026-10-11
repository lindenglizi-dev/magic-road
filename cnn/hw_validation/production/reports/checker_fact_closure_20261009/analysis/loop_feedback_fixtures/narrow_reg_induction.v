module narrow_reg_induction
(
output reg [15:0] value
);

reg [3:0] index;
always @(*) begin
    value = 16'd0;
    for (index = 0; index < 16; index = index + 1)
        value[index] = 1'b1;
end

endmodule
