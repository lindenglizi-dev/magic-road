# Read-only clock metadata query against the completed new candidate.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db continuous_physical/pr.db
help get_property
help get_clocks
set clocks [get_clocks -include_generated_clocks *]
puts "CLOCK_QUERY_COUNT [llength $clocks]"
foreach clock $clocks {
    foreach property {NAME TYPE IS_GENERATED MASTER_CLOCK PERIOD WAVEFORM SOURCE} {
        if {[catch {get_property $property $clock} value]} {
            puts "CLOCK_QUERY_PROPERTY_UNAVAILABLE $property $value"
        } else {
            puts "CLOCK_QUERY_PROPERTY $property $value"
        }
    }
}
puts "CLOCK_QUERY_DONE"
