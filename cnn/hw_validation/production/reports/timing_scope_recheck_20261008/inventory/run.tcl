# Read an immutable routed snapshot; no synthesis, placement or routing.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
puts "LOADED_CLOCKS [get_clocks -include_generated_clocks *]"
if {[llength [get_clocks -include_generated_clocks *]] == 0} {
    read_sdc ../snapshot/shell.sdc
}
update_timing -mode final
report_analysis_corner -all
report_analysis_corner -active

proc save_objects {name objects} {
    set stream [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object $objects { puts $stream $object }
    close $stream
    puts "OBJECT_COUNT $name [llength $objects]"
}
save_objects all_cells [get_cells -hier *]
save_objects all_regs [get_regs -hier *]
save_objects all_pins [get_pins -hier *]
save_objects reset_named_cells [get_cells -hier {*reg_release*}]
save_objects reset_named_regs [get_regs -hier {*reg_release*}]
save_objects reset_named_pins [get_pins -hier {*reg_release*}]
save_objects exact_meta_q [get_pins -hier {reg_release_done_reg_syn_3.oqb}]
save_objects exact_done_q [get_pins -hier {reg_release_done_reg_syn_3.oqa}]
save_objects exact_meta_q_slash [get_pins -hier {reg_release_done_reg_syn_3/oqb}]
save_objects exact_done_q_slash [get_pins -hier {reg_release_done_reg_syn_3/oqa}]
save_objects reset_nets [get_nets -hier {*reg_release_meta* *reg_release_done*}]
foreach object [get_cells -hier {*reg_release*}] { report_property $object }
foreach object [get_nets -hier {*reg_release_meta* *reg_release_done*}] {
    puts "RESET_NET $object"
    report_nets [list $object] -connection -pin_display_limit 10000
}
report_timing_status -file loaded_status.rpt
report_timing_summary -ep_num 20 -path_num 1 -file loaded_sanity.timing
puts "A_PHASE_COMPLETE"
