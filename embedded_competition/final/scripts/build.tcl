set project_root [file normalize [file join [file dirname [info script]] ..]]
file mkdir "$project_root/build/gate"
file mkdir "$project_root/build/optimized"
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al"
commit_param -step design
elaborate -top design_top_wrapper
read_adc "$project_root/user_source/constraints_source/pin.adc"
read_ip_adc -ip ddr2 -file "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/adc/ddr2.adc"
read_sdc "$project_root/td_project/camera_to_dsi_display.sdc"
read_sdc -ip ddr2 "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc"
read_sdc -ip w128_d512_fifo "$project_root/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl"
cd "$project_root/build/gate"
export_db elaborate.db
commit_param -step rtl
insert_debugger
optimize_rtl
report_area -file rtl.area
export_db rtl.db
commit_param -step gate
optimize_gate -packarea gate.area
legalize_phy_inst
update_timing
report_timing_status -file gate.ts
report_timing_summary -file gate.timing
export_db gate.db
puts BUILD_GATE_COMPLETE
puts "PASS COMBINED_FIRST_GATE; gate resources only, no placement/routing or bitstream qualification"
exit



