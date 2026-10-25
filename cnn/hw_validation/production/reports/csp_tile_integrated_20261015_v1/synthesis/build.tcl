import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_csp_tile_integrated.al -single_run
elaborate -top road_csp_tile_integrated
optimize_rtl
report_area -verbose -file rtl.area
read_sdc frontend.sdc
optimize_gate
legalize_phy_inst
export_db gate.db
write_verilog gate_netlist.v -top road_csp_tile_integrated
report_area -verbose -io_info -file gate.area
report_qor -step gate -file gate.qor
puts "CSP_TILE_SYNTHESIS_COMPLETE"
close_project
exit
