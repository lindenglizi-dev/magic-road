# Command discovery only: do not load, synthesize or change a design.
puts "DB_COMMANDS [info commands *db*]"
foreach name {import_db read_db get_pins get_regs get_cells get_nets get_ports report_timing_path get_property get_attribute} {
    puts "COMMAND $name [info commands $name]"
    if {[llength [info commands $name]] != 0} {
        catch {help $name} result
        puts "HELP_RESULT $name $result"
    }
}
puts "A_PHASE_COMPLETE"
