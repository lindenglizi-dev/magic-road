# Resume only the reviewed candidate's gate database; no timing exceptions.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db gate.db
read_sdc joint.sdc
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
route
export_db pr.db
write_verilog routed_netlist.v -implement -top road_rom_down2_top
report_area -verbose -io_info -file joint_route.area
report_ram_utilization -file joint_route_ram.rpt
report_io -verbose -file joint_route_io.rpt
drc_check -all -verbose
update_timing -mode final
report_timing_status -file joint_route.ts
report_timing_summary -file final_timing.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_paths.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file violations.timing
set regs [get_regs -hier *]
set erams [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
set dsps [get_cells -hier -filter {REF_NAME =~ *DSP*} *]
puts "JOINT_OBJECTS regs=[llength $regs] erams=[llength $erams] dsps=[llength $dsps]"
report_timing_path -from $regs -to $regs -ep_num 100000 -path_num 1 -file internal.timing
report_timing_path -from [get_ports i_rstn] -to $regs -ep_num 100000 -path_num 1 -file external_reset.timing
report_timing_path -from [get_pins -of $erams -filter {DIRECTION == output} *] -ep_num 100000 -path_num 1 -file eram_outputs.timing
report_timing_path -to [get_pins -of $erams -filter {DIRECTION == input} *] -ep_num 100000 -path_num 1 -file eram_inputs.timing
report_timing_path -from [get_pins -of $dsps -filter {DIRECTION == output} *] -ep_num 100000 -path_num 1 -file dsp_outputs.timing
report_timing_path -to [get_pins -of $dsps -filter {DIRECTION == input} *] -ep_num 100000 -path_num 1 -file dsp_inputs.timing
check_timing -verbose -file check_timing.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
report_clock_summary -clocks [get_clocks *] -expand_buckets -debug -file clocks.rpt
puts "JOINT_PHYSICAL_DONE"
close_project
