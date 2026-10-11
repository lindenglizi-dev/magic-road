import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_overlap_low_io_top.al -single_run
elaborate -top road_dynamic_overlap_low_io_top
set dead [get_nets -filter {DRIVER_COUNT == 0} *]
foreach net $dead {
    puts "DEAD_RECORD [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}
puts "MODEL_QUERY_DONE"
close_project
