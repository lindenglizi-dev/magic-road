module parent(output [7:0] result); wire [7:0] bus; unknown u(.value(bus)); assign result=bus; endmodule
