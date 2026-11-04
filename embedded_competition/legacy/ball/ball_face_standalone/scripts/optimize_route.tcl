set project_root [file normalize [file join [file dirname [info script]] ..]]
file mkdir "$project_root/build/default"
file mkdir "$project_root/build/optimized"
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db "$project_root/build/default/place.db"
read_sdc "$project_root/td_project/camera_to_dsi_display.sdc"
read_sdc -ip ddr2 "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc"
read_sdc -ip w128_d512_fifo "$project_root/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl"
cd "$project_root/build/optimized"
commit_param -step route
set_param route post_route_opt high
set_param route postrt_opt_extra_round 4
update_timing -mode manhattan
set_path_margin -group optimization_setup -global -setup 0.6
report_path_margin
update_timing -mode manhattan
report_timing_summary -file tightened_before.timing
route
update_timing -mode final
report_timing_summary -file tightened_after.timing
reset_path_margin -all
update_timing -mode final
report_timing_summary -file restored_original_constraints.timing
report_path_margin
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
puts OPTIMIZED_ROUTE_COMPLETE
exit


