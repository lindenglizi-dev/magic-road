module width_parent ();
    reg [31:0] reg_values [0:7];
    width_child u_child (.i_value(reg_values[3:0]));
endmodule
