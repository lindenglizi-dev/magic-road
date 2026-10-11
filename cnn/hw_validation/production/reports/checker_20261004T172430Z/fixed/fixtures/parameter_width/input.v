module parent
(
output [7:0] result
);

wire [7:0] bus;

 child #(.WIDTH(7)) source_Inst(
.value(bus)
);
 assign result=bus;


endmodule
module child
#(
parameter WIDTH=8
)
(
output [WIDTH-1:0] value
);

assign value=0;


endmodule
