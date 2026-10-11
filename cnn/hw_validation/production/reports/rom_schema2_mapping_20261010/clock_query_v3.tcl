import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db continuous_physical/pr.db
update_timing -mode final
set clocks [get_clocks *]
set included [get_clocks -include_generated_clocks *]
puts "CLOCK_QUERY_PRIMARY_COUNT [llength $clocks] INCLUDED_COUNT [llength $included]"
if {[llength $clocks] != 1} { error "Expected one primary clock" }
puts "CLOCK_QUERY_PROPERTIES [list_property $clocks]"
report_property $clocks
puts "CLOCK_QUERY_DONE"
