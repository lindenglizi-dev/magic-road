module parent(output [7:0] result); wire [7:0] bus; child u(.value(bus)); assign result=bus; endmodule
module child(input [7:0] value); endmodule