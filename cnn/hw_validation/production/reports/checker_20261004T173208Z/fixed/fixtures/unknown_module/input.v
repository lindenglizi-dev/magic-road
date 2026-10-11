module parent
(
output [7:0] result
);

wire [7:0] bus;

 unknown source_Inst(
.value(bus)
);
 assign result=bus;


endmodule
