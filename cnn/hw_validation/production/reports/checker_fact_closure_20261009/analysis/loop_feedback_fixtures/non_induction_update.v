module non_induction_update
(
output reg [3:0] value
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 1; index < 4; index = index * 2)
        value[index] = 1'b1;
end

endmodule
