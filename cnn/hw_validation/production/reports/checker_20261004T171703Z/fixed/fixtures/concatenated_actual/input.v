module parent(output [7:0] result); wire [7:0] bus; child u(.value({bus[7:4],bus[3:0]})); assign result=bus; endmodule
module child(output [7:0] value); assign value=8'h35; endmodule
