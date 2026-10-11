# Read-only re-export from THIS run's immutable routed database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final
set regs [get_regs -hier *]
if {[llength $regs] == 0} { error "No register objects: refuse empty-filter timing evidence" }
report_timing_path -from $regs -to $regs -ep_num 10000 -path_num 1 -file internal_reg_to_reg_full.timing
report_timing_path -from [get_ports {i_rstn}] -to $regs -ep_num 10000 -path_num 1 -file reset_to_regs_full.timing
report_timing_summary -ep_num 10000 -path_num 1 -file all_paths_full.timing
report_abnormal_timing_target -file abnormal_targets.timing
