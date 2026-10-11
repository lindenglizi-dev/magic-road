module unknown_module_output(
    output wire [7:0] o_data
);
wire [7:0] unknown_data;
unknown_child u_unknown(.o_data(unknown_data));
assign o_data = unknown_data;
endmodule
