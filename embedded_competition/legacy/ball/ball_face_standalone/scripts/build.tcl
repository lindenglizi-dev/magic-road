set project_root [file normalize [file join [file dirname [info script]] ..]]
file mkdir "$project_root/build/default"
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
cd "$project_root/build/default"
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
commit_param -step place
place
update_timing -mode manhattan
report_timing_summary -file place.timing
report_area -io_info -file place.area
export_db place.db
puts BUILD_PLACE_COMPLETE
commit_param -step route
route
update_timing -mode final
report_area -io_info -file routed.area
report_timing_status -file routed.ts
report_timing_summary -file routed.timing
report_timing_exception -file exceptions.timing
report_timing_ignored -file ignored.timing
report_route_status -drc -file route_drc.txt
report_clock_utilization -file clocks.txt
flow_status -file route_flow.status
check_timing -verbose -file checks.timing
report_abnormal_timing_target -file abnormal.timing
export_sdc -file applied.sdc
export_db routed.db
puts BUILD_ROUTE_COMPLETE
exit


