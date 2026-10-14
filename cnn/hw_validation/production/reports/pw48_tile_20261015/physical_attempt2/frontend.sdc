create_clock -name probe_clk -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]
set inputs [get_ports {i_rstn i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*] o_busy o_done o_fault o_parameters_ready}]
if {[llength $inputs] != 19 || [llength $outputs] != 22} {error "PW diagnostic IO count changed"}
set_input_delay -clock [get_clocks probe_clk] -max 0.000 $inputs
set_input_delay -clock [get_clocks probe_clk] -min 0.000 $inputs
set_output_delay -clock [get_clocks probe_clk] -max 0.000 $outputs
set_output_delay -clock [get_clocks probe_clk] -min 0.000 $outputs
