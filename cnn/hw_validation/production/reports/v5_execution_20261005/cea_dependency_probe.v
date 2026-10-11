module cea_dependency_probe(
    input wire i_left,
    input wire i_right,
    output wire o_data
);
    wire flag_enable;
    wire wire_data;
    assign flag_enable = i_left | i_right;
    opaque_ram u_ram(.cea(flag_enable), .doa(wire_data));
    assign o_data = wire_data;
endmodule
