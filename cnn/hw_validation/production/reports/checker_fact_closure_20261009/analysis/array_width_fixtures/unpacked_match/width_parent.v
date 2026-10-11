module width_parent (
    input wire i_index
);
    reg [31:0] reg_values [0:1];
    width_child u_child (.i_value(reg_values[i_index]));
endmodule
