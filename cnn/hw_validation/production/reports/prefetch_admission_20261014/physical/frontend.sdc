# Isolated 100MHz boundary. Zero IO delays are diagnostic only, not board signoff.
create_clock -name probe_clk -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]
set inputs [get_ports {i_rstn i_load_valid i_load_addr[*] i_load_data[*] i_start i_commit_ready i_export_start i_output_ready}]
set outputs [get_ports {o_load_ready o_parameters_ready o_busy o_done o_fault o_output_valid o_output_data[*] o_output_index[*] o_export_done}]
if {[llength $inputs] != 25} {error "Expected 25 nonclock input bits"}
if {[llength $outputs] != 24} {error "Expected 24 output bits"}
set_input_delay -clock [get_clocks probe_clk] -max 0.000 $inputs
set_input_delay -clock [get_clocks probe_clk] -min 0.000 $inputs
set_output_delay -clock [get_clocks probe_clk] -max 0.000 $outputs
set_output_delay -clock [get_clocks probe_clk] -min 0.000 $outputs
# No exceptions, board pin assignment or invented external timing.
