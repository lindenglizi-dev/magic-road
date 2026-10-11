# Read-only evidence export from the frozen routed database.  No constraints,
# synthesis, placement, routing, hold fixing, or bitstream commands are used.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../physical/td/pr.db
update_timing -mode final

set all_clocks [get_clocks -include_generated_clocks -verbose *]
puts "FOLLOWUP_CLOCK_COUNT=[llength $all_clocks]"
puts "FOLLOWUP_CLOCK_COLLECTION=$all_clocks"
foreach clock_object $all_clocks {
    puts "FOLLOWUP_CLOCK_OBJECT=$clock_object"
    list_property $clock_object
}

check_timing -verbose -file check_timing_verbose.rpt
report_clock_summary -clocks $all_clocks -expand_buckets -debug -file clock_summary_debug.rpt
report_clock_summary -clocks $all_clocks -endpoints_only -expand_buckets -debug -file clock_endpoints_debug.rpt
report_timing_summary -include_ignored -ep_num 10000 -path_num 1 -file all_paths_include_ignored.rpt
report_timing_ignored -ep_num 10000 -path_num 1 -file ignored_paths_detailed.rpt
report_timing_exception -ep_num 10000 -path_num 1 -file timing_exceptions_detailed.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
