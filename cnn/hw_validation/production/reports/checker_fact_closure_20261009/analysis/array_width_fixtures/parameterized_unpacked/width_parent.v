module width_parent #(
    parameter WIDTH = 6
) (
    input wire i_index
);
    reg [WIDTH-1:0] reg_values [0:1];
    width_child #(.WIDTH(WIDTH)) u_child (.i_value(reg_values[i_index]));
endmodule
