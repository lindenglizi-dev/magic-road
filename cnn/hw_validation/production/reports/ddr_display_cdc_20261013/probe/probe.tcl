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
puts "CDC_PROBE_COMPLETE"
