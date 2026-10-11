module instance_escape
(
output reg [3:0] value
);

integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = 1'b1;
end
escape_sink escape_sink_Inst(
    .value(index)
);

endmodule
module escape_sink
(
input [31:0] value
);

endmodule
