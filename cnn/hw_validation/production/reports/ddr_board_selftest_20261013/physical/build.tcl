# Independent native DDR requester plus frozen HDMI. No bitgen here.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_ddr_selftest_top.al -single_run
elaborate -top road_ddr_selftest_top
read_adc board.adc
optimize_rtl
report_area -verbose -file rtl.area
read_sdc board.sdc
optimize_gate
legalize_phy_inst
read_sdc board.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_ddr_selftest_top
report_qor -step gate -file gate.qor
update_timing
set_param place effort high
set_param place opt_timing high
set_param place timing_driven_mode on
set_param place post_place_opt high
set_param route post_route_opt high
place
report_qor -step place -file place.qor
route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_ddr_selftest_top
report_area -verbose -io_info -file route.area
report_ram_utilization -file route_ram.rpt
report_io -verbose -file route_io.rpt
report_route_status -drc -file route_status.rpt
drc_check -all -verbose
update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file violations.timing
set all_regs [get_regs -hier *]
if {[llength $all_regs] == 0} {error "Empty DDR implementation"}
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_reg_to_reg.timing
report_timing_path -from [get_ports i_rstn] -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing
set user_meta [get_regs -hier {*reg_user_meta*}]
set user_release [get_regs -hier {*reg_user_release*}]
report_timing_path -from $user_meta -to $user_release -ep_num 100 -path_num 10 -file user_reset_sync.timing
report_timing_path -from $user_release -to $all_regs -ep_num 100000 -path_num 1 -file user_reset_distribution.timing
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $eram_cells] > 0} {
    report_timing_path -from [get_pins -of $eram_cells -filter {DIRECTION == output} *] -ep_num 100000 -path_num 1 -file eram_outputs.timing
    report_timing_path -to [get_pins -of $eram_cells -filter {DIRECTION == input} *] -ep_num 100000 -path_num 1 -file eram_inputs.timing
}
puts "DDR_OBJECT_COUNT regs=[llength $all_regs] eram=[llength $eram_cells]"
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clocks.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
check_timing -verbose -file check_timing.rpt
report_abnormal_timing_target -file abnormal.rpt
puts "DDR_PHYSICAL_COMPLETE"
close_project
