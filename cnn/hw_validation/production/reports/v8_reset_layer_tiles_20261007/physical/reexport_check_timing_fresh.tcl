# Fresh-process timing-integrity export from the frozen routed database.
# Existing reports are intentionally not overwritten.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set all_clocks [get_clocks -include_generated_clocks *]
puts "FRESH_OBJECT_COUNT clocks=[llength $all_clocks]"
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file fresh_clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file fresh_clock_endpoints_debug.rpt
report_timing_exception -ep_num 20000 -path_num 1 -file fresh_timing_exceptions.rpt
report_timing_ignored -ep_num 20000 -path_num 1 -file fresh_timing_ignored.rpt
check_timing -verbose -file fresh_check_timing_verbose.rpt
report_abnormal_timing_target -file fresh_abnormal_targets.rpt
