# Resume diagnostic I/O reports from the retained routed database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final
set all_regs [get_regs -hier *]
set reset_port [get_ports {i_rstn}]
set data_inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set data_outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $all_regs] == 0} { error "No registers: refuse empty timing evidence" }
if {[llength $reset_port] != 1} { error "Expected one i_rstn port" }
if {[llength $data_inputs] != 18} { error "Expected 18 non-reset data input bits" }
if {[llength $data_outputs] != 18} { error "Expected 18 data output bits" }
report_timing_path -from $data_inputs -to $all_regs -ep_num 100000 -path_num 1 -file diagnostic_inputs_to_regs_resume.timing
report_timing_path -from $all_regs -to $data_outputs -ep_num 100000 -path_num 1 -file regs_to_diagnostic_outputs_resume.timing
report_timing_path -from $reset_port -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry_resume.timing
close_project
