# Inspect the original runtime chain before uniform-instance zero substitution.
# All exports are local to this independent diagnostic directory; no bit generation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_chain_low_io_top.al -single_run
elaborate -top road_dynamic_chain_low_io_top
export_db elaborated.db
write_verilog elaborated_netlist.v -top road_dynamic_chain_low_io_top
set nets [get_nets -hier *]
puts "ELAB_NET_COUNT=[llength $nets]"
set sample [lindex $nets 0]
puts "NET_PROPERTY_NAMES=[list_property $sample]"
report_property $sample
set undriven [get_nets -hier -filter {DRIVER_COUNT == 0} *]
puts "UNDRIVEN_RAW_COUNT=[llength $undriven]"
report_nets $undriven -connection -pin_display_limit 100
optimize_rtl
set undriven_after [get_nets -hier -filter {DRIVER_COUNT == 0} *]
puts "UNDRIVEN_AFTER_COUNT=[llength $undriven_after]"
report_nets $undriven_after -connection -pin_display_limit 100
puts "ELABORATION_INSPECT_DONE"
close_project
