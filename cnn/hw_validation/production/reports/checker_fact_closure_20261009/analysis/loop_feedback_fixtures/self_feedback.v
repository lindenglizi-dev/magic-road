module self_feedback
(
input source,
output reg value
);

always @(*) begin
    value = value | source;
end

endmodule
