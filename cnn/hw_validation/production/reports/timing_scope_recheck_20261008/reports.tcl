# Timing-only read-back: original DB/SDC graph, no placement/route/exception.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
report_timing_summary -ep_num 30 -path_num 1 -file sanity.timing
set stream [open sanity.timing r]
set sanity [read $stream]
close $stream
if {![regexp {STA coverage *: 100\.00%} $sanity]} { error "Restored timing coverage is not 100%" }
if {![regexp {Confidence *: Routed} $sanity]} { error "Not a routed timing database" }
report_analysis_corner -all
report_analysis_corner -active

proc save_objects {name objects} {
    set stream [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object $objects { puts $stream $object }
    close $stream
    puts "OBJECT_COUNT $name [llength $objects]"
}
proc exact_one {pattern} {
    set pins [get_pins -hier [list $pattern]]
    if {[llength $pins] != 1} { error "Expected exactly one physical pin: $pattern" }
    return $pins
}
proc report_scope {name from to} {
    if {[llength $from] == 0 || [llength $to] == 0} { error "Empty scope: $name" }
    save_objects "${name}_from" $from
    save_objects "${name}_to" $to
    report_timing_path -from $from -to $to -ep_num 100000 -path_num 1 -file "$name.timing"
}

set meta_q [exact_one reg_release_done_reg_syn_3.oqb]
set done_q [exact_one reg_release_done_reg_syn_3.oqa]
set done_d [exact_one reg_release_done_reg_syn_3.ima]
set shared_asr [exact_one reg_release_done_reg_syn_3.asr]
set sync_cell [get_cells -hier {reg_release_done_reg_syn_3}]
if {[llength $sync_cell] != 1} { error "Unexpected synchronizer physical cell" }
set all_regs [get_regs -hier *]
set meta_reg [get_regs -hier {reg_release_meta}]
set done_reg [get_regs -hier {reg_release_done}]
if {[llength $meta_reg] != 1 || [llength $done_reg] != 1} { error "Ambiguous exact logical alias" }
set function_regs {}
foreach reg $all_regs {
    if {$reg ni $meta_reg && $reg ni $done_reg} { lappend function_regs $reg }
}
save_objects all_regs $all_regs
save_objects functional_regs $function_regs
save_objects exact_meta_alias $meta_reg
save_objects exact_done_alias $done_reg

set slice_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_LSLICE} *]
set hard_cells [get_cells -hier -filter {REF_NAME =~ *DSP* || REF_NAME =~ *ERAM*} *]
set memory_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_MSLICE || REF_NAME == PH1P_PHY_SHIFTERHARDCON} *]
set sequential_cells [concat $slice_cells $hard_cells $memory_cells]
set sequential_pins [concat $all_regs [get_pins -of $sequential_cells *]]
set function_cells {}
foreach cell $sequential_cells {
    if {$cell ni $sync_cell} { lappend function_cells $cell }
}
set function_pins [concat $function_regs [get_pins -of $function_cells *]]

set siou [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set mul [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPMULT_V2} *]
set tadd [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPTADD} *]
set eram [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
if {[llength $siou] != 4 || [llength $mul] != 4 || [llength $tadd] != 2 || [llength $eram] != 1} {
    error "Unexpected DSP/ERAM structural identity"
}
save_objects dsp_siou_cells $siou
save_objects dsp_mult_cells $mul
save_objects dsp_tadd_cells $tadd
save_objects eram_cells $eram
save_objects distributed_memory_cells $memory_cells
save_objects broad_sequential_pins $sequential_pins

# Exact-cell port families cover active timing arcs; unused/mode pins stay in
# the separate broad safety-net report, not the claimed register count.
set dsp_targets [get_pins -of $siou {*.xa* *.y* *.ce* *.rst*}]
set hard_detail_pins [get_pins -of [concat $siou $mul $tadd] *]
set eram_targets [get_pins -of $eram {*.addra* *.dia* *.csa* *.wea}]
set hard_outputs [concat [get_pins -of [concat $siou $mul $tadd] {*.p* *.sum* *.cout*}] [get_pins -of $eram {*.doa*}]]
set memory_outputs [get_pins -of $memory_cells {*.oqa *.oqb *.of* *.do* *.q*}]
set internal_sources [concat $all_regs $hard_outputs $memory_outputs]
save_objects hard_outputs $hard_outputs
save_objects dsp_exact_family_targets $dsp_targets
save_objects eram_a_targets $eram_targets

set raw [get_ports {i_rstn}]
set inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $raw] != 1 || [llength $inputs] != 18 || [llength $outputs] != 18} {
    error "Unexpected top boundary bits"
}

report_scope reset_raw_sync_asr $raw $shared_asr
report_scope reset_meta_done $meta_q $done_d
report_scope reset_done_function $done_q $function_pins
report_scope reset_raw_all $raw $sequential_pins
report_scope internal_alias_reg $all_regs $all_regs
report_scope internal_sequential_hard $internal_sources $sequential_pins
report_scope internal_dsp_family $internal_sources $dsp_targets
report_scope internal_eram_a $internal_sources $eram_targets
report_scope internal_distributed_memory $internal_sources [get_pins -of $memory_cells *]
report_scope input_sequential_hard $inputs $sequential_pins
report_scope output_sequential_hard $internal_sources $outputs

save_objects hard_detail_through $hard_detail_pins
report_timing_path -from $internal_sources -to $sequential_pins -through $hard_detail_pins -ep_num 100000 -path_num 1 -file internal_dsp_through.timing
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoint_safety_net.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file all_endpoint_include_ignored.timing
check_timing -verbose -file check_timing_verbose.rpt
report_abnormal_timing_target -file abnormal_targets.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_status -file timing_status.rpt
report_area -verbose -file area.rpt
report_ram_utilization -file ram.rpt
puts "A_PHASE_COMPLETE"
