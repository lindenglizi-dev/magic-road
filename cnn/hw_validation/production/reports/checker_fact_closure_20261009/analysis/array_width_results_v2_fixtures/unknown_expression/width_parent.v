module width_parent (
    input wire [31:0] i_value
);
    width_child u_child (.i_value(i_value + 1'b1));
endmodule
