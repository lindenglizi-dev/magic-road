# Isolated ROM probe: no board pins, timing exceptions, or bitstream commands.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db gate.db
read_sdc rom.sdc
update_timing
set_param place effort high
set_param place opt_timing high
set_param place logic_level_opt on
set_param place timing_driven_mode on
set_param place post_place_opt high
set_param place hfn_opt_effort high
set_param route post_route_opt high
set_param route postrt_opt_extra_round 4
report_param
place
report_qor -step place -file place.qor
route
report_qor -step route -file route.qor
export_db pr.db
write_verilog routed_netlist.v -implement -top road_yolo_numeric_rom_probe
report_area -verbose -io_info -file rom_route.area
report_ram_utilization -file rom_route_ram.rpt
report_io -verbose -file rom_route_io.rpt
report_route_status -drc -file rom_route_status.rpt
drc_check -all -verbose
update_timing -mode final
report_timing_status -file rom_route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file coverage_100000_all_paths.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file coverage_100000_include_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file coverage_100000_violations.timing
set all_regs [get_regs -hier *]
set reset_port [get_ports i_rstn]
set outputs [get_ports {o_done o_checksum[*]}]
set erams [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
set dsp [get_cells -hier -filter {REF_NAME =~ *DSP*} *]
set eram_q [get_pins -of $erams -filter {DIRECTION == output} *]
set eram_d [get_pins -of $erams -filter {DIRECTION == input} *]
if {[llength $erams] != 56} { error "Expected 56 physical ERAMs" }
if {[llength $dsp] != 0} { error "ROM probe must not use DSP" }
if {[llength $outputs] != 33} { error "Expected 33 output bits" }
if {[llength $all_regs] == 0} { error "Empty register timing scope" }
puts "ROM_OBJECT_COUNT regs=[llength $all_regs] erams=[llength $erams] dsp=[llength $dsp] outputs=[llength $outputs]"
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file internal_reg_to_reg.timing
report_timing_path -from $reset_port -to $all_regs -ep_num 100000 -path_num 1 -file external_reset_entry.timing
report_timing_path -from $all_regs -to $outputs -ep_num 100000 -path_num 1 -file regs_to_diagnostic_outputs.timing
report_timing_path -from $eram_q -ep_num 100000 -path_num 1 -file eram_outputs_all.timing
report_timing_path -to $eram_d -ep_num 100000 -path_num 1 -file eram_inputs_all.timing
set clocks [get_clocks -include_generated_clocks *]
report_clock_summary -clocks $clocks -expand_buckets -debug -file clock_summary_debug.rpt
report_clock_summary -clocks $clocks -endpoints_only -expand_buckets -debug -file clock_endpoints_debug.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
puts "ROM_PHYSICAL_DONE"
