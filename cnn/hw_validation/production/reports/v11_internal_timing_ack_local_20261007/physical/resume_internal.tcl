# Resume only the failed routed internal-path export from the retained database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final
set all_regs [get_regs -hier *]
if {[llength $all_regs] == 0} { error "No registers: refuse empty timing evidence" }
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_reg_to_reg_resume.timing
close_project
