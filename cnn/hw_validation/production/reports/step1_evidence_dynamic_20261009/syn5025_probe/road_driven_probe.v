`timescale 1ns / 1ps
// A fully driven one-register diagnostic: no floating wires or unused ports.
module road_driven_probe(
    input i_clk, // Clock of the only register.
    input i_rstn, // Asynchronous cancellation.
    input i_data, // Runtime operand, not a constant.
    output reg o_data // Registered observation of the runtime operand.
);
    // Explicit reset and both sequential branches drive the only output.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) o_data <= 1'b0;
        else o_data <= i_data;
    end
endmodule
