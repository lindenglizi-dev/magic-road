module parent
(
output [7:0] result
);

wire [7:0] bus;

 child source_Inst(
.value(bus)
);
 assign result=bus;


endmodule
module child
(
output [7:0] value
);

generate
if(1) begin : gen_data
assign value=8'h35;


end
endgenerate
endmodule
