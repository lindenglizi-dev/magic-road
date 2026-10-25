import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
foreach signal {reg_request reg_request_meta reg_request_sync reg_acknowledge reg_ack_meta reg_ack_sync} {
    set pattern "road_selftest_display_Inst/$signal"
    set nets [get_nets -hier $pattern]
    puts "CDC_NET $signal count=[llength $nets] value=$nets"
    set pins [get_pins -of $nets *]
    puts "CDC_PINS $signal $pins"
    foreach pin $pins {report_property $pin}
}
puts "CDC_HOLD_NETS [get_nets -hier {road_selftest_display_Inst/reg_hold_payload*}]"
puts "CDC_ACTIVE_NETS [get_nets -hier {road_selftest_display_Inst/reg_active_payload*}]"
foreach bit {0 37 84 186 254 255 128 129} {
    foreach signal {reg_hold_payload o_active_payload} {
        set expression [format {^road_selftest_display_Inst/%s\[%d\]$} $signal $bit]
        set net [get_nets -hier -regexp $expression]
        puts "CDC_BIT $signal $bit net=$net"
        puts "CDC_BIT_PINS [get_pins -of $net *]"
    }
}
report_property [get_cells -hier {road_selftest_display_Inst/reg_active_payload_reg[186]_syn_2}]
puts "CDC_PROBE_COMPLETE"
