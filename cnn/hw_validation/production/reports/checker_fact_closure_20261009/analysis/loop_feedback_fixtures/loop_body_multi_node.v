module loop_body_multi_node
(
output reg [3:0] value
);

integer index;
integer mirror;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1) begin
        mirror = index;
        index = mirror;
        value[index] = 1'b1;
    end
end

endmodule
