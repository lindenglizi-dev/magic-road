# Read-only elaboration audit of the current candidate, not another implementation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_frontend_shared_core.al -single_run
elaborate -top road_frontend_shared_core
set dead [get_nets -hier -filter {DRIVER_COUNT == 0} *]
foreach net $dead {
    puts "DEAD_RECORD [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}
puts "MODEL_QUERY_DONE count=[llength $dead]"
close_project
