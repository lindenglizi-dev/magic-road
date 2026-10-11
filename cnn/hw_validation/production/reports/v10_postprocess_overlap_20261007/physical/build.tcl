# V10 overlap-runner physical validation. Intentionally no bit generation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_postprocess_low_io_top.al -single_run
elaborate -top road_postprocess_low_io_top
read_adc shell.adc
optimize_rtl
report_area -verbose -file shell_rtl.area
read_sdc shell.sdc
optimize_gate
legalize_phy_inst
read_sdc shell.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_postprocess_low_io_top
report_qor -step gate -file gate.qor
update_timing
place
report_qor -step place -file place.qor
route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_postprocess_low_io_top
report_area -verbose -io_info -file shell_route.area
report_ram_utilization -file shell_route_ram.rpt
report_io -verbose -file shell_route_io.rpt
report_route_status -drc -file shell_route_status.rpt
drc_check -all -verbose
report_design_cell_num -hier -top 300
report_hierarchy_stats [get_cells -hier *] -list
update_timing -mode final
report_timing_status -file shell_route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file coverage_100000_all_paths.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file coverage_100000_include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file coverage_100000_violations.timing

set all_regs [get_regs -hier *]
set reset_port [get_ports {i_rstn}]
set data_inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set data_outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $all_regs] == 0} { error "No registers: refuse empty timing evidence" }
if {[llength $reset_port] != 1} { error "Expected one i_rstn port" }
if {[llength $data_inputs] != 18} { error "Expected 18 non-reset data input bits" }
if {[llength $data_outputs] != 18} { error "Expected 18 data output bits" }

report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_reg_to_reg.timing
report_timing_path -from $data_inputs -to $all_regs -ep_num 100000 -path_num 1 -file diagnostic_inputs_to_regs.timing
report_timing_path -from $all_regs -to $data_outputs -ep_num 100000 -path_num 1 -file regs_to_diagnostic_outputs.timing
report_timing_path -from $reset_port -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing

set release_meta_regs [get_regs -hier {*reg_release_meta*}]
set release_done_regs [get_regs -hier {*reg_release_done*}]
if {[llength $release_meta_regs] == 0} { error "Missing reg_release_meta physical register" }
if {[llength $release_done_regs] == 0} { error "Missing reg_release_done physical register" }
report_timing_path -from $release_meta_regs -to $release_done_regs -ep_num 100 -path_num 10 -file reset_sync_interstage.timing
report_timing_path -from $release_done_regs -to $all_regs -ep_num 100000 -path_num 1 -file functional_reset_distribution.timing

puts "OBJECT_COUNT all_regs=[llength $all_regs]"
puts "OBJECT_COUNT release_meta_regs=[llength $release_meta_regs]"
puts "OBJECT_COUNT release_done_regs=[llength $release_done_regs]"

set all_clocks [get_clocks -include_generated_clocks *]
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file clock_endpoints_debug.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
close_project
