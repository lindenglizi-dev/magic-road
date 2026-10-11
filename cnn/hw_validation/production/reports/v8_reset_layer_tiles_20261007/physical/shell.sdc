# Isolated 100 MHz diagnostic boundary. Values are ns in TD SDC.
set shell_clock_port [get_ports {i_clk}]
if {[llength $shell_clock_port] != 1} { error "Expected exactly one i_clk port" }
create_clock -name {probe_clk} -period 10.000 -waveform {0.000 5.000} $shell_clock_port

# No external device or board delay is modeled. Keep both values at zero;
# these diagnostic assumptions must not be tuned to make timing pass.
set shell_input_ports [get_ports {i_rstn i_rx_valid i_rx_data[*] i_tx_ready}]
if {[llength $shell_input_ports] != 19} { error "Expected 19 non-clock input bits" }
set_input_delay -clock [get_clocks {probe_clk}] -max 0.000 $shell_input_ports
set_input_delay -clock [get_clocks {probe_clk}] -min 0.000 $shell_input_ports

set shell_output_ports [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $shell_output_ports] != 18} { error "Expected 18 output bits" }
set_output_delay -clock [get_clocks {probe_clk}] -max 0.000 $shell_output_ports
set_output_delay -clock [get_clocks {probe_clk}] -min 0.000 $shell_output_ports

# i_rstn remains timed. No false/multicycle/min/max-delay exception is added.
