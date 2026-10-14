# Actual shared Stem/down2 arithmetic top. Intentionally no bitstream operation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
elaborate -top road_rom_current_down2_top
read_adc frontend.adc
optimize_rtl
report_area -verbose -file frontend_rtl.area
read_sdc frontend.sdc
optimize_gate
legalize_phy_inst
read_sdc frontend.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_rom_current_down2_top
report_qor -step gate -file gate.qor
update_timing

set_param place effort high
set_param place opt_timing high
set_param place logic_level_opt on
set_param place aggressive_opt 21
set_param place aggr_neighbor_dist 5
set_param place enhanced_beeline_opt 3
set_param place timing_driven_mode on
set_param place shifter_opt on
set_param place crit_path_opt on
set_param place post_place_opt high
set_param place hfn_opt_effort high
set_param place split_data_from_clock on
set_param route post_route_opt off
report_param
place
report_qor -step place -file place.qor
export_db before_replication.db
write_verilog placed_netlist.v -implement -top road_rom_current_down2_top
puts "CONTROL_QUERY_BEGIN"
foreach pattern {u_compute/u_pp/u_pre/u_round/i_advance* u_rom/cnt_wait_b_n*} {
 set family [get_nets -hier $pattern]
 if {[llength $family] == 0} {error "Missing control family $pattern"}
 foreach net $family {report_nets $net -connection -pin_display_limit 2000}
}
puts "CONTROL_QUERY_END"
puts "SOURCE_PLACEMENT_DONE"
close_project
exit
