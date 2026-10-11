# Read-only report re-export from this run's routed database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final
set all_regs [get_regs -hier *]
if {[llength $all_regs] == 0} { error "No registers in routed database" }
report_timing_summary -ep_num 10000 -path_num 1 -file reexport_all_paths.timing
report_timing_summary -include_ignored -ep_num 10000 -path_num 1 -file reexport_all_paths_include_ignored.timing
report_timing_summary -viol_only -ep_num 10000 -path_num 1 -file reexport_violations.timing
report_timing_path -from $all_regs -to $all_regs -ep_num 10000 -path_num 1 -file reexport_internal_reg_to_reg.timing
report_timing_path -from [get_ports {i_rstn}] -to $all_regs -ep_num 10000 -path_num 1 -file reexport_reset_to_regs.timing
set all_clocks [get_clocks -include_generated_clocks *]
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file reexport_clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file reexport_clock_endpoints_debug.rpt
report_timing_exception -ep_num 10000 -path_num 1 -file reexport_timing_exceptions.rpt
report_timing_ignored -ep_num 10000 -path_num 1 -file reexport_timing_ignored.rpt
check_timing -verbose -file reexport_check_timing_verbose.rpt
report_abnormal_timing_target -file reexport_abnormal_targets.rpt
