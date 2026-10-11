import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db continuous_physical/pr.db
update_timing -mode final
set clocks [get_clocks -include_generated_clocks *]
puts "CLOCK_QUERY_COUNT [llength $clocks]"
puts "CLOCK_QUERY_PROPERTIES [list_property $clocks]"
report_property $clocks
puts "CLOCK_QUERY_DONE"
