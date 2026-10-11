import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_overlap_low_io_top.al -single_run
elaborate -top road_yolo_numeric_rom_group
set dead [get_nets -hier -full_hier -filter {DRIVER_COUNT == 0} *]
puts "PREZERO_MODULE road_yolo_numeric_rom_group COUNT [llength $dead]"
foreach net $dead {
    puts "PREZERO_NET [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}
report_nets $dead -connection -pin_display_limit 100
puts "PREZERO_QUERY_DONE"
close_project
