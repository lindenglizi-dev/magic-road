# Source-constrained reports deliberately leave destinations open. This keeps
# library timing arc endpoints which do not expand from a get_regs -to alias.
# Output-port endpoints are classified separately, not called internal.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
set regs [get_regs -hier *]
set dsp_q [get_pins -hier -regexp {^u_chain/u_dynamic_requant/mult0_syn_(776|1200)\.p\[[0-9]+\]$}]
set eram_q [get_pins -hier -regexp {^u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1\.(doa|doa_extra)\[[0-9]+\]$}]
set memory_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_MSLICE || REF_NAME == PH1P_PHY_SHIFTERHARDCON} *]
set memory_q [get_pins -of $memory_cells -filter {DIRECTION == output} *]
set done_q [get_pins -hier {reg_release_done_reg_syn_3.oqa}]
set inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
foreach name {regs dsp_q eram_q memory_q done_q inputs} {
    set stream [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object [set $name] { puts $stream $object }
    close $stream
    puts "COMPLETE_SOURCE_COUNT $name [llength [set $name]]"
}
report_timing_path -from $regs -ep_num 100000 -path_num 1 -file reg_all_destinations.timing
report_timing_path -from $dsp_q -ep_num 100000 -path_num 1 -file dsp_all_destinations.timing
report_timing_path -from $eram_q -ep_num 100000 -path_num 1 -file eram_all_destinations.timing
report_timing_path -from $memory_q -ep_num 100000 -path_num 1 -file distributed_memory_all_destinations.timing
report_timing_path -from $done_q -ep_num 100000 -path_num 1 -file done_all_destinations.timing
report_timing_path -from $inputs -ep_num 100000 -path_num 1 -file input_all_destinations.timing
puts "A_PHASE_COMPLETE"
