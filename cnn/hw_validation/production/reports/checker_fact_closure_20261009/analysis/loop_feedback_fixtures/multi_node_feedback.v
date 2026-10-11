module multi_node_feedback
(
output reg first,
output reg second
);

always @(*) begin
    first = second;
    second = first;
end

endmodule
