module concat_body_write
(
output reg [3:0] value
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1) begin
        {index, value[index]} = {index + 1, 1'b1};
    end
end

endmodule
