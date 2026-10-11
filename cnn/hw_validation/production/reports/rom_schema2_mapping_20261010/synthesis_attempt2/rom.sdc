# Isolated 100 MHz ROM probe. Zero IO delays are diagnostic, not board signoff.
create_clock -name probe_clk -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]
set_input_delay -clock [get_clocks {probe_clk}] -max 0.000 [get_ports {i_rstn}]
set_input_delay -clock [get_clocks {probe_clk}] -min 0.000 [get_ports {i_rstn}]
set_output_delay -clock [get_clocks {probe_clk}] -max 0.000 [get_ports {o_done o_checksum[*]}]
set_output_delay -clock [get_clocks {probe_clk}] -min 0.000 [get_ports {o_done o_checksum[*]}]
# No false path, multicycle, max/min-delay exception, or board pin assignment.
