# Read-only physical objects from this candidate; no changed constraint or implementation command.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../physical/pr.db
foreach pattern {*flag_mac_input_accept* *Inst_mac*flag_input_accept*} {
    set selected [get_nets -hier $pattern]
    puts "QUERY_PATTERN $pattern NET_COUNT [llength $selected]"
    foreach net $selected {
        puts "ACCEPT_NET [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
    }
    if {[llength $selected] > 0} {
        report_nets $selected -connection -pin_display_limit 1000
    }
}
foreach pattern {*reg_mac_activation* *reg_mac_weight* *reg_mac_bias* *reg_halo* *reg_dw_weight* *reg_pw_weight*} {
    set selected [get_nets -hier $pattern]
    puts "OPERAND_PATTERN $pattern NET_COUNT [llength $selected]"
}
set all_clocks [get_clocks -include_generated_clocks *]
puts "CLOCK_OBJECTS $all_clocks"
report_clock_summary -clocks $all_clocks -expand_buckets -debug
puts "MAPPING_QUERY_DONE"
