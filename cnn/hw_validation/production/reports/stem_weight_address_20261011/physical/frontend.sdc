# Isolated 100 MHz diagnostic boundary for the functional integration top.
set frontend_clock_port [get_ports {i_clk}]
if {[llength $frontend_clock_port] != 1} { error "Expected exactly one i_clk bit" }
create_clock -name {frontend_clk} -period 10.000 -waveform {0.000 5.000} $frontend_clock_port

# No external device or board delay is modeled. These zero delays are diagnostic
# assumptions only and must remain separate from internal endpoint timing.
set frontend_input_ports [get_ports {i_rstn i_select_valid i_select_down2 i_table_valid i_table_addr[*] i_table_data[*] i_load_valid i_load_kind[*] i_load_addr[*] i_load_data[*] i_start i_commit_ready i_export_start i_output_ready}]
if {[llength $frontend_input_ports] != 81} { error "Expected 81 non-clock input bits" }
set_input_delay -clock [get_clocks {frontend_clk}] -max 0.000 $frontend_input_ports
set_input_delay -clock [get_clocks {frontend_clk}] -min 0.000 $frontend_input_ports

set frontend_output_ports [get_ports {o_select_ready o_selected_down2 o_table_ready o_table_loaded o_table_fault o_load_ready o_busy o_done o_fault o_core_cycles[*] o_output_valid o_output_data[*] o_output_index[*] o_export_done}]
if {[llength $frontend_output_ports] != 60} { error "Expected 60 output bits" }
set_output_delay -clock [get_clocks {frontend_clk}] -max 0.000 $frontend_output_ports
set_output_delay -clock [get_clocks {frontend_clk}] -min 0.000 $frontend_output_ports

# Raw reset remains timed. No false, multicycle, max-delay, or min-delay
# exception is present.
