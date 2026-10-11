# Second fresh-process audit: materialize a routed timing summary before
# check_timing, matching the proven baseline re-export ordering.
# First-session and first-fresh reports remain preserved.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final
report_timing_summary -ep_num 20000 -path_num 1 -file fresh2_timing_summary.rpt

set all_clocks [get_clocks -include_generated_clocks *]
puts "FRESH2_OBJECT_COUNT clocks=[llength $all_clocks]"
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file fresh2_clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file fresh2_clock_endpoints_debug.rpt
report_timing_exception -ep_num 20000 -path_num 1 -file fresh2_timing_exceptions.rpt
report_timing_ignored -ep_num 20000 -path_num 1 -file fresh2_timing_ignored.rpt
check_timing -verbose -file fresh2_check_timing_verbose.rpt
report_abnormal_timing_target -file fresh2_abnormal_targets.rpt
