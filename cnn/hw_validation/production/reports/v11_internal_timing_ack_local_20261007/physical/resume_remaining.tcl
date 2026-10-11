# Resume the remaining routed reports after the disk-full interruption.
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

set release_meta_regs [get_regs -hier {*reg_release_meta*}]
set release_done_regs [get_regs -hier {*reg_release_done*}]
if {[llength $release_meta_regs] == 0} { error "Missing reg_release_meta physical register" }
if {[llength $release_done_regs] == 0} { error "Missing reg_release_done physical register" }
report_timing_path -from $release_meta_regs -to $release_done_regs -ep_num 100 -path_num 10 -file reset_sync_interstage_resume.timing
report_timing_path -from $release_done_regs -to $all_regs -ep_num 100000 -path_num 1 -file functional_reset_distribution_resume.timing

set all_clocks [get_clocks -include_generated_clocks *]
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file clock_summary_debug_resume.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file clock_endpoints_debug_resume.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions_resume.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored_resume.rpt
check_timing -verbose -file check_timing_verbose_resume.rpt
report_abnormal_timing_target -file abnormal_targets_resume.rpt
close_project
