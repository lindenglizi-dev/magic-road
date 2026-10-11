module array_range
(
output reg value
);
reg data [0:1];
always @(*) begin
    value = data[2];
end
endmodule
