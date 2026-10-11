# Isolated low-I/O diagnostic implementation. Intentionally no bitgen.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_low_io_physical_shell.al -single_run
elaborate -top road_low_io_physical_shell
read_adc shell.adc
optimize_rtl
report_area -verbose -file shell_rtl.area
read_sdc shell.sdc
optimize_gate
legalize_phy_inst
read_sdc shell.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_low_io_physical_shell
report_qor -step gate -file gate.qor
update_timing
place
report_qor -step place -file place.qor
route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_low_io_physical_shell
report_area -verbose -io_info -file shell_route.area
report_ram_utilization -file shell_route_ram.rpt
report_io -verbose -file shell_route_io.rpt
report_route_status -drc -file shell_route_status.rpt
drc_check -all -verbose
report_design_cell_num -hier -top 200
report_hierarchy_stats [get_cells -hier *] -list
update_timing -mode final
report_timing_status -file shell_route.ts
report_timing_summary -ep_num 10000 -path_num 1 -file shell_route.timing
report_timing_summary -include_ignored -ep_num 10000 -path_num 1 -file all_paths_include_ignored.timing
report_timing_summary -viol_only -ep_num 10000 -path_num 1 -file all_violations.timing
set all_regs [get_regs -hier *]
if {[llength $all_regs] == 0} { error "No registers: refuse empty timing evidence" }
report_timing_path -from $all_regs -to $all_regs -ep_num 10000 -path_num 1 -file internal_reg_to_reg.timing
set reset_port [get_ports {i_rstn}]
if {[llength $reset_port] != 1} { error "Missing i_rstn for recovery/removal export" }
report_timing_path -from $reset_port -to $all_regs -ep_num 10000 -path_num 1 -file reset_to_regs.timing
set all_clocks [get_clocks -include_generated_clocks *]
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file clock_endpoints_debug.rpt
report_timing_exception -ep_num 10000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 10000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
close_project
