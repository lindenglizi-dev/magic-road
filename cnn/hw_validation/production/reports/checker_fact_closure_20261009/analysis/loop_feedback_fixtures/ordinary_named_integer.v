module ordinary_named_integer
(

);

integer lane_index;
always @(*) begin
    lane_index = lane_index + 1;
end

endmodule
