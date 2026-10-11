module known_child(
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
assign o_data = i_data;
endmodule

module multiple_instance_outputs(
    input wire [7:0] i_first,
    input wire [7:0] i_second,
    output wire [7:0] o_data
);
wire [7:0] shared_data;
known_child u_first(.i_data(i_first), .o_data(shared_data));
known_child u_second(.i_data(i_second), .o_data(shared_data));
assign o_data = shared_data;
endmodule
