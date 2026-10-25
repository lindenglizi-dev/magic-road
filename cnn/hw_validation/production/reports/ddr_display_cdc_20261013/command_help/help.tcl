# Read-only command semantics; no project or constraints changed.
foreach cmd {set_max_delay set_min_delay set_false_path set_multicycle_path get_regs get_pins get_nets get_property get_cells import_db report_timing_path} {
    puts "CDC_HELP $cmd"
    catch {help $cmd} result
    puts $result
}
puts "CDC_HELP_COMPLETE"
