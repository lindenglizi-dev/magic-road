module width_child(input wire i_value); endmodule
module width_parent(input wire i_index, input wire [31:0] i_value);
    width_child u_child (.i_value(i_value[i_index]));
endmodule
