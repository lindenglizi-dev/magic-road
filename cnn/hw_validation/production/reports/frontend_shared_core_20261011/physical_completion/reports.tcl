# Read-only report completion from the same routed database. No reimplementation.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../physical_attempt2/pr.db
read_sdc ../physical_attempt2/frontend.sdc
update_timing -mode final
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $dsp_cells] != 32} { error "Unexpected DSP count in this frozen implementation" }
if {[llength $eram_cells] != 4} { error "Expected routed SiLU plus inferred tile memories" }
foreach cell $eram_cells { puts "ERAM_RECORD [get_property NAME $cell]" }
set silu_count 0
foreach cell $eram_cells {
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
set all_regs [get_regs -hier *]
puts "FRONTEND_OBJECT_COUNT all_regs=[llength $all_regs] dsp_cells=[llength $dsp_cells] eram_cells=[llength $eram_cells]"
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clock_summary_debug.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file timing_ignored.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
puts "REPORT_COMPLETION_DONE"
