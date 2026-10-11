import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
report_timing_path -from [get_regs -hier *] -to [get_pins -hier {u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.wea}] -ep_num 100 -path_num 1 -file reg_to_eram_wea.timing
report_timing_path -from [get_regs -hier *] -to [get_pins -hier {u_chain/u_dynamic_requant/mult0_syn_776.ce[0]}] -ep_num 100 -path_num 1 -file reg_to_dsp_ce.timing
report_timing_path -from [get_regs -hier *] -to [get_pins -hier {u_chain/u_dynamic_requant/mult0_syn_681.xa[0]}] -ep_num 100 -path_num 1 -file reg_to_dsp_xa.timing
report_timing_path -from [get_regs -hier *] -to [get_cells -hier {u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1}] -ep_num 10000 -path_num 1 -file reg_to_eram_cell.timing
report_timing_path -from [get_regs -hier *] -to [get_ports {o_tx_valid}] -ep_num 100 -path_num 1 -file reg_to_output.timing
report_timing_path -from [get_pins -hier {reg_release_done_reg_syn_3.oqa}] -to [get_regs -hier *] -ep_num 100000 -path_num 1 -file done_to_regs.timing
report_timing_path -from [get_pins -hier {reg_release_done_reg_syn_3.oqa}] -to [get_pins -hier {u_chain/u_dynamic_requant/mult0_syn_681.rst[0]}] -ep_num 100 -path_num 1 -file done_to_dsp_rst.timing
report_timing_path -from [get_ports {i_rx_data[7]}] -to [get_pins -hier {u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia[6]}] -ep_num 100 -path_num 1 -file input_to_eram_dia.timing
report_timing_path -to [get_pins -hier {u_chain/u_silu/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.wea}] -ep_num 100 -path_num 10 -file all_sources_eram_wea.timing
puts "A_PHASE_COMPLETE"
