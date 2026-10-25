import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_feature_workstore_top.al -single_run
elaborate -top road_feature_workstore_top
optimize_rtl
report_area -verbose -file rtl.area
read_sdc frontend.sdc
optimize_gate
legalize_phy_inst
export_db gate.db
write_verilog gate_netlist.v -top road_feature_workstore_top
report_area -verbose -io_info -file gate.area
report_qor -step gate -file gate.qor
puts "FEATURE_WORKSTORE_DIAGNOSTIC_SYNTHESIS_COMPLETE"
close_project
exit
