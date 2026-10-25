import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
source ../build/display_cdc.tcl
update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file violations.timing
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
check_timing -verbose -file check_timing.rpt
foreach pair {{reg_request_meta reg_request_sync} {reg_ack_meta reg_ack_sync}} {
    lassign $pair source target
    report_timing_path -from [cdc_q $source] -through [cdc_q $source] -to [cdc_d [cdc_q $target]] -ep_num 10 -path_num 10 -file "$source.timing"
}
puts "CDC_CONSTRAINT_PROBE_COMPLETE"
