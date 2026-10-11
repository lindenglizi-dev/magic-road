module parent
(
output [7:0] result
);

wire [7:0] bus;

 assign bus[3:0]=4'h5;
 assign result=bus;


endmodule
