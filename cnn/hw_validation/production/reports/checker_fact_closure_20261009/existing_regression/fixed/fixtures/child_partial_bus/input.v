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

assign value[3:0]=4'h5;


endmodule
