module loop_variable_escape
(
input [3:0] data,
output reg [3:0] value,
output reg escaped
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = data[index];
    escaped = index[0];
end

endmodule
