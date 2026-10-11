# Never concat native TD collections of different object classes. Query and
# report each source/destination class independently; combine evidence later.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
report_analysis_corner -all
report_analysis_corner -active
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing

set regs [get_regs -hier *]
set function_regs [get_regs -hier -filter {NAME != reg_release_meta && NAME != reg_release_done} *]
set dsp_in [get_pins -hier -regexp {^u_chain/u_dynamic_requant/mult0_syn_(681|776|1105|1200)\.(xa|y|ce|rst)\[[0-9]+\]$} *]
set dsp_q [get_pins -hier -regexp {^u_chain/u_dynamic_requant/mult0_syn_(776|1200)\.p\[[0-9]+\]$} *]
set eram_in [get_pins -hier -regexp {^u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1\.(addra|dia|dia_extra|csa)\[[0-9]+\]$|^u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1\.wea$} *]
set eram_q [get_pins -hier -regexp {^u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1\.(doa|doa_extra)\[[0-9]+\]$} *]
set dsp_reset [get_pins -hier -regexp {^u_chain/u_dynamic_requant/mult0_syn_(681|776|1105|1200)\.rst\[0\]$} *]
set memory_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_MSLICE || REF_NAME == PH1P_PHY_SHIFTERHARDCON} *]
set memory_pins [get_pins -of $memory_cells *]
set meta_q [get_pins -hier {reg_release_done_reg_syn_3.oqb}]
set done_q [get_pins -hier {reg_release_done_reg_syn_3.oqa}]
set done_d [get_pins -hier {reg_release_done_reg_syn_3.ima}]
set raw [get_ports {i_rstn}]
set shared_asr [get_pins -hier {reg_release_done_reg_syn_3.asr}]
set inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
set hard_cells [get_cells -hier -filter {REF_NAME =~ *DSP*} *]
set hard_pins [get_pins -of $hard_cells *]

foreach name {regs function_regs dsp_in dsp_q eram_in eram_q dsp_reset memory_cells memory_pins meta_q done_q done_d raw shared_asr inputs outputs} {
    set objects [set $name]
    puts "PRECISE_COUNT $name [llength $objects]"
    set stream [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object $objects { puts $stream $object }
    close $stream
}
foreach {name count} {regs 1941 function_regs 1939 dsp_in 212 dsp_q 108 eram_in 38 eram_q 20 dsp_reset 4 memory_cells 9 meta_q 1 done_q 1 done_d 1 raw 1 shared_asr 1 inputs 18 outputs 18} {
    if {[llength [set $name]] != $count} { error "Incorrect native collection: $name" }
}
report_timing_path -from $raw -to $shared_asr -ep_num 100 -path_num 1 -file raw_sync_asr.timing
report_timing_path -from $meta_q -to $done_d -ep_num 100 -path_num 1 -file meta_done.timing
report_timing_path -from $done_q -to $function_regs -ep_num 100000 -path_num 1 -file done_function_regs.timing
report_timing_path -from $done_q -to $dsp_reset -ep_num 1000 -path_num 1 -file done_dsp_reset.timing
report_timing_path -from $regs -to $regs -ep_num 100000 -path_num 1 -file reg_reg.timing
report_timing_path -from $regs -to $dsp_in -ep_num 100000 -path_num 1 -file reg_dsp.timing
report_timing_path -from $regs -to $eram_in -ep_num 100000 -path_num 1 -file reg_eram.timing
report_timing_path -from $dsp_q -to $regs -ep_num 100000 -path_num 1 -file dsp_reg.timing
report_timing_path -from $eram_q -to $regs -ep_num 100000 -path_num 1 -file eram_reg.timing
report_timing_path -from $dsp_q -to $dsp_in -ep_num 100000 -path_num 1 -file dsp_dsp.timing
report_timing_path -from $eram_q -to $dsp_in -ep_num 100000 -path_num 1 -file eram_dsp.timing
report_timing_path -from $inputs -to $regs -ep_num 100000 -path_num 1 -file input_reg.timing
report_timing_path -from $inputs -to $eram_in -ep_num 100000 -path_num 1 -file input_eram.timing
report_timing_path -from $inputs -to $dsp_in -ep_num 100000 -path_num 1 -file input_dsp.timing
report_timing_path -from $regs -to $outputs -ep_num 100000 -path_num 1 -file reg_output.timing
report_timing_path -from $dsp_q -to $outputs -ep_num 100000 -path_num 1 -file dsp_output.timing
report_timing_path -from $eram_q -to $outputs -ep_num 100000 -path_num 1 -file eram_output.timing
report_timing_path -through $hard_pins -ep_num 100000 -path_num 1 -file dsp_through.timing
report_timing_path -through $memory_pins -ep_num 100000 -path_num 1 -file distributed_memory_through.timing
report_timing_path -from $regs -to $memory_pins -ep_num 100000 -path_num 1 -file reg_distributed_memory.timing
report_timing_path -from $raw -to $regs -ep_num 100000 -path_num 1 -file raw_regs.timing
report_timing_path -from $raw -to $dsp_reset -ep_num 1000 -path_num 1 -file raw_dsp.timing
report_timing_path -from $done_q -to $outputs -ep_num 1000 -path_num 1 -file done_output.timing
check_timing -verbose -file check_timing.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
puts "A_PHASE_COMPLETE"
