import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
source ../build/display_cdc.tcl
set fh [open resolved_display.sdc r]
set text [read $fh]
close $fh
set fh [open negative_display.sdc w]
puts $fh [string map {7.500 0.001} $text]
close $fh
read_sdc negative_display.sdc
update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file violations.timing
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
check_timing -verbose -file check_timing.rpt
foreach pair {{reg_request_meta reg_request_sync} {reg_ack_meta reg_ack_sync}} {
    lassign $pair source target
    set src [cdc_q $source]
    report_timing_path -from [cdc_clock $src] -through $src -to [cdc_d [cdc_q $target]] -ep_num 10 -path_num 10 -file "$source.timing"
}
puts "CDC_CONSTRAINT_PROBE_COMPLETE"
