# No invented board IO delays. Exact approved CDC SDC is generated after packing.
create_clock -name sys_clk_50m -period 20.000 -waveform {0.000 10.000} [get_ports i_sys_clk]
derive_clocks
# build.tcl explicitly reads the original DDR IP ADC/SDC with IP scope.
