import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_csp_tile_integrated.al -single_run
import_db source_gate.db
# Keep the clock constraints already stored in gate.db; do not redefine them.
update_timing
if {[llength [get_clocks probe_clk]] != 1} {error "Expected one100MHzprobe clock after timing update"}
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
route
export_db pr.db
write_verilog routed_netlist.v -implement -top road_csp_tile_integrated
report_area -verbose -io_info -file frontend_route.area
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file all_endpoints_include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file all_violations.timing
set all_regs [get_regs -hier *]
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_all_checks.timing
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $dsp_cells] == 0 || [llength $eram_cells] == 0} {error "Arithmetic or SiLU removed"}
set dsp_outputs [get_pins -of $dsp_cells -filter {DIRECTION == output} *]
set dsp_inputs [get_pins -of $dsp_cells -filter {DIRECTION == input} *]
set eram_outputs [get_pins -of $eram_cells -filter {DIRECTION == output} *]
set eram_inputs [get_pins -of $eram_cells -filter {DIRECTION == input} *]
report_timing_path -from $dsp_outputs -ep_num 100000 -path_num 1 -file dsp_outputs_all_checks.timing
report_timing_path -to $dsp_inputs -ep_num 100000 -path_num 1 -file dsp_inputs_all_checks.timing
report_timing_path -from $eram_outputs -ep_num 100000 -path_num 1 -file eram_outputs_all_checks.timing
report_timing_path -to $eram_inputs -ep_num 100000 -path_num 1 -file eram_inputs_all_checks.timing
report_timing_path -from [get_ports i_rstn] -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt

puts "CSP_TILE_PHYSICAL_REPORTS_COMPLETE"
close_project
exit
