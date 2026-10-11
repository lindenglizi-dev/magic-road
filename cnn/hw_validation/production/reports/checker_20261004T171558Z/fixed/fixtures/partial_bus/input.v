module parent(output [7:0] result); wire [7:0] bus; child u(.value(bus[3:0])); assign result=bus; endmodule
module child(output [3:0] value); assign value=4'h3; endmodule