# Read the routed candidate; preserve its constraints and failed first query.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../physical/pr.db
update_timing -mode final
report_analysis_corner -all
report_analysis_corner -active
set regs [get_regs -hier *]
set raw [get_ports i_rstn]
set meta_q [get_pins -hier {reg_release_done_reg_syn_3.oqb}]
set done_d [get_pins -hier {reg_release_done_reg_syn_4.ima reg_release_done_reg_syn_5.ima}]
set done_q [get_pins -hier {reg_release_done_reg_syn_4.oqa reg_release_done_reg_syn_5.oqa}]
set raw_asr [get_pins -hier {reg_release_done_reg_syn_3.asr reg_release_done_reg_syn_4.asr reg_release_done_reg_syn_5.asr}]
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set dsp_q [get_pins -of $dsp_cells -filter {DIRECTION == output} *]
set dsp_reset [get_pins -of $dsp_cells {*rst*}]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
set eram_q [get_pins -of $eram_cells -filter {DIRECTION == output} *]
set slice_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_LSLICE} *]
set slice_q [get_pins -of $slice_cells {*.oqa *.oqb}]
set mem_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_MSLICE || REF_NAME == PH1P_PHY_SHIFTERHARDCON} *]
set mem_q [get_pins -of $mem_cells -filter {DIRECTION == output} *]
set inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
foreach name {regs raw meta_q done_d done_q raw_asr dsp_cells dsp_q dsp_reset eram_cells eram_q slice_q mem_q inputs outputs} {
    puts "OBJECT_COUNT $name [llength [set $name]]"
    set f [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object [set $name] {puts $f $object}
    close $f
}
foreach {name count} {meta_q 1 done_d 2 done_q 2 raw_asr 3 dsp_cells 4 eram_cells 1} {
    if {[llength [set $name]] != $count} {error "Incorrect physical collection $name"}
}
report_timing_path -from $raw -to $raw_asr -ep_num 10000 -path_num 1 -file raw_sync_asr.timing
report_timing_path -from $meta_q -to $done_d -ep_num 10000 -path_num 1 -file meta_done.timing
report_timing_path -from $done_q -ep_num 100000 -path_num 1 -file done_all.timing
report_timing_path -from $done_q -to $dsp_reset -ep_num 100000 -path_num 1 -file done_dsp.timing
report_timing_path -from $regs -ep_num 100000 -path_num 1 -file reg_all.timing
report_timing_path -from $slice_q -ep_num 100000 -path_num 1 -file slice_all.timing
report_timing_path -from $dsp_q -ep_num 100000 -path_num 1 -file dsp_all.timing
report_timing_path -from $eram_q -ep_num 100000 -path_num 1 -file eram_all.timing
report_timing_path -from $mem_q -ep_num 100000 -path_num 1 -file memory_all.timing
report_timing_path -from $inputs -ep_num 100000 -path_num 1 -file input_all.timing
report_timing_path -to $outputs -ep_num 100000 -path_num 1 -file output_all.timing
puts "CANDIDATE_READBACK_COMPLETE"
