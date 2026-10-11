`timescale 1ns / 1ps
module tb_always_delay_parser_min();
	reg i_clk = 1'b0;
	always #5 i_clk = ~i_clk;
endmodule
