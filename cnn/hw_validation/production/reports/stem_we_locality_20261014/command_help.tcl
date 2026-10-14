# Read-only command inventory. Do not open or mutate a database in this probe.
foreach pattern {*place* *move* *loc* *eco* *route* *cell*} {
    puts "COMMAND_INVENTORY $pattern [info commands $pattern]"
}
foreach name {move_cells mpnr_move_inst set_inst_init_loc dr_move set_cell_location report_cells get_property place route report_placement_status} {
    puts "USAGE_BEGIN $name"
    if {[catch {$name -help} detail]} {puts "USAGE_ERROR $detail"}
    puts "USAGE_END $name"
}
puts "LOCALITY_COMMAND_HELP_DONE"
exit
