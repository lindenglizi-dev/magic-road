# Board oscillator from existing project, not yet checked against physical board.
create_clock -name sys_clk_50m -period 20.000 -waveform {0.000 10.000} [get_ports i_sys_clk]
derive_clocks
# Related PLL clocks remain related. No invented input/output delay or timing exception.
