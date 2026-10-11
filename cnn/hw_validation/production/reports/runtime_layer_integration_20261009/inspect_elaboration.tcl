# Inspect the original runtime chain before uniform-instance zero substitution.
# All exports are local to this independent diagnostic directory; no bit generation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project PROJECT_FILE -single_run
elaborate -top road_dynamic_chain_low_io_top
export_db elaborated.db
write_verilog elaborated_netlist.v -top road_dynamic_chain_low_io_top
import_db elaborated.db -flatten
set nets [get_nets -hier -full_hier *]
puts "ELAB_NET_COUNT=[llength $nets]"
set sample [lindex $nets 0]
puts "NET_PROPERTY_NAMES=[list_property $sample]"
report_property $sample
set undriven [get_nets -hier -full_hier -filter {DRIVER_COUNT == 0} *]
puts "UNDRIVEN_RAW_COUNT=[llength $undriven]"
report_nets {u_chain/check_lane[0] u_chain/reg_pre_mul_b6[31] u_chain/reg_post_mul_b6[0] u_chain/reg_post_shift_b6[0] u_chain/wire_emit_lane_b1[0] u_chain/select_lane_b1[0] u_chain/u_pre/u_round/reg_half_b2[0] u_chain/u_post/u_round/reg_half_b2[0]} -connection -pin_display_limit 100
optimize_rtl
set undriven_after [get_nets -hier -full_hier -filter {DRIVER_COUNT == 0} *]
puts "UNDRIVEN_AFTER_COUNT=[llength $undriven_after]"
puts "ELAB_QUERY_LIMITATION: post-optimization names may be removed aliases, not load-bearing undriven objects."
puts "ELABORATION_INSPECT_DONE"
close_project
