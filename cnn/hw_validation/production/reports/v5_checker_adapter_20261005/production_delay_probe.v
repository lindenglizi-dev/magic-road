module production_delay_probe();
reg i_clk;
always #5 i_clk = ~i_clk;
endmodule
