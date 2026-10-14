import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_pr.db
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
export_db before_replication.db
update_timing
update_timing
set target_net [get_nets -hier {u_compute/u_pp/u_pre/u_round/i_advance_dup_2}]
if {[llength $target_net] != 1} {error "Expected exactly one target net"}
puts "TARGET_BEFORE_BEGIN"
report_nets $target_net -connection -pin_display_limit 2000
puts "TARGET_BEFORE_END"
puts "REPLICATION_BEGIN"
phys_opt -force_replication_on_nets {u_compute/u_pp/u_pre/u_round/i_advance_dup_2} -fanout_threshold 128
route
puts "REPLICATION_DONE"
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_current_down2_top
update_timing -mode final
puts "TARGET_AFTER_BEGIN"
report_nets [get_nets -hier {*u_pre/u_round/i_advance*}] -connection -pin_display_limit 2000
puts "TARGET_AFTER_END"
report_area -verbose -io_info -file frontend_route.area
report_ram_utilization -file frontend_route_ram.rpt
report_io -verbose -file frontend_route_io.rpt
report_route_status -drc -file frontend_route_status.rpt
drc_check -all -verbose
report_design_cell_num -hier -top 300
report_hierarchy_stats [get_cells -hier *] -list

update_timing -mode final
report_timing_status -file frontend_route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file all_endpoints_include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file all_violations.timing

set all_regs [get_regs -hier *]
set reset_port [get_ports {i_rstn}]
set data_inputs [get_ports {i_load_valid i_load_addr[*] i_load_data[*] i_start i_commit_ready i_export_start i_output_ready}]
set data_outputs [get_ports {o_load_ready o_parameters_ready o_busy o_done o_fault o_output_valid o_output_data[*] o_output_index[*] o_export_done}]
if {[llength $all_regs] == 0} { error "No registers: refuse empty timing evidence" }
if {[llength $reset_port] != 1} { error "Expected one i_rstn bit" }
if {[llength $data_inputs] != 24} { error "Expected 24 non-reset data input bits" }
if {[llength $data_outputs] != 24} { error "Expected 24 output bits" }

# This report contains every register endpoint (up to the explicit 100000 cap)
# with applicable register-to-register setup/hold; reset checks are separate.
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_all_checks.timing
report_timing_path -from $data_inputs -to $all_regs -ep_num 100000 -path_num 1 -file diagnostic_inputs_to_regs.timing
report_timing_path -from $all_regs -to $data_outputs -ep_num 100000 -path_num 1 -file regs_to_diagnostic_outputs.timing
report_timing_path -from $reset_port -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing

set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $dsp_cells] == 0} { error "No physical DSP cells: arithmetic chain was not retained" }
if {[llength $eram_cells] < 1} { error "No retained ERAM" }
set silu_count 0
foreach cell $eram_cells {
    puts "ERAM_RECORD [get_property NAME $cell]"
    if {[string match {*u_silu*} [get_property NAME $cell]]} { incr silu_count }
}
if {$silu_count != 1} { error "Shared SiLU table was duplicated or removed" }
set dsp_outputs [get_pins -of $dsp_cells -filter {DIRECTION == output} *]
set dsp_inputs [get_pins -of $dsp_cells -filter {DIRECTION == input} *]
set eram_outputs [get_pins -of $eram_cells -filter {DIRECTION == output} *]
set eram_inputs [get_pins -of $eram_cells -filter {DIRECTION == input} *]
report_timing_path -from $dsp_outputs -ep_num 100000 -path_num 1 -file dsp_outputs_all_checks.timing
report_timing_path -to $dsp_inputs -ep_num 100000 -path_num 1 -file dsp_inputs_all_checks.timing
report_timing_path -from $eram_outputs -ep_num 100000 -path_num 1 -file all_eram_outputs_all_checks.timing
report_timing_path -to $eram_inputs -ep_num 100000 -path_num 1 -file all_eram_inputs_all_checks.timing
puts "FRONTEND_OBJECT_COUNT all_regs=[llength $all_regs] dsp_cells=[llength $dsp_cells] eram_cells=[llength $eram_cells]"

report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clock_summary_debug.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
set ram_names {}
set ram_file [open frontend_route_ram.rpt r]
while {[gets $ram_file ram_line] >= 0} {
 if {[regexp {^\s*(\S+)\s*\|[^|]*\|[^|]*\([0-9]+\)\s*\|} $ram_line unused ram_name]} {lappend ram_names $ram_name}
}
close $ram_file
set memory_cells [get_cells -hier $ram_names]
if {[llength $memory_cells] != [llength $ram_names]} {error {Memory object resolution incomplete}}
set memory_inputs [get_pins -of $memory_cells -filter {DIRECTION == input} *]
set memory_outputs [get_pins -of $memory_cells -filter {DIRECTION == output} *]
set internal_sources [concat $all_regs $dsp_outputs $memory_outputs]
report_timing_path -from $internal_sources -to $memory_inputs -ep_num 100000 -path_num 1 -file internal_to_memory.timing
report_timing_path -from $internal_sources -to $dsp_inputs -ep_num 100000 -path_num 1 -file internal_to_dsp.timing
report_timing_path -from $memory_outputs -to $all_regs -ep_num 100000 -path_num 1 -file memory_to_registers.timing
report_timing_path -from $dsp_outputs -to $all_regs -ep_num 100000 -path_num 1 -file dsp_to_registers.timing
puts "ROM_CURRENT_MEMORY_OBJECTS [llength $memory_cells]"
puts "REPORT_COMPLETION_DONE"
close_project
exit
