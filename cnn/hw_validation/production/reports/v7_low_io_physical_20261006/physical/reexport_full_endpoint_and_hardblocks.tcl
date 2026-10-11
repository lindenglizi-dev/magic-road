# Read-only full-endpoint and hard-block timing export from the frozen routed DB.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set ep_limit 20000
set all_regs [get_regs -hier *]
set reset_port [get_ports {i_rstn}]
set data_inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set data_outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $all_regs] == 0} { error "No registers in routed database" }
if {[llength $reset_port] != 1} { error "Expected one reset port" }
if {[llength $data_inputs] != 18} { error "Expected 18 non-reset data input bits" }
if {[llength $data_outputs] != 18} { error "Expected 18 data output bits" }

# Full design reports. ep_limit exceeds the 10109 endpoints in the baseline.
report_timing_summary -ep_num $ep_limit -path_num 1 -file full_20000_all_paths.timing
report_timing_summary -include_ignored -ep_num $ep_limit -path_num 1 -file full_20000_include_ignored.timing
report_timing_summary -viol_only -ep_num $ep_limit -path_num 1 -file full_20000_violations.timing
report_timing_path -from $all_regs -to $all_regs -ep_num $ep_limit -path_num 1 -file full_internal_reg_to_reg.timing
report_timing_path -from $data_inputs -to $all_regs -ep_num $ep_limit -path_num 1 -file diagnostic_inputs_to_regs.timing
report_timing_path -from $all_regs -to $data_outputs -ep_num $ep_limit -path_num 1 -file regs_to_diagnostic_outputs.timing
report_timing_path -from $reset_port -to $all_regs -ep_num $ep_limit -path_num 1 -file reset_recovery_removal.timing

# The physical DSP implementation is 26 DSPSIOU sites and 26 paired DSPMULT
# sub-cells: two sites for the fixed-coefficient 32x32 rescale multiply and
# twenty-four sites for the dynamic 8x8 MAC lanes.
set dsp_siou_cells [get_cells -hier -full_hier {
    road_onchip_chain_Inst_shell/mult0_syn_168
    road_onchip_chain_Inst_shell/mult0_syn_263
    road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult*_syn_57
}]
set dsp_mult_cells [get_cells -hier -full_hier {
    road_onchip_chain_Inst_shell/mult0_syn_169
    road_onchip_chain_Inst_shell/mult0_syn_264
    road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult*_syn_58
}]
if {[llength $dsp_siou_cells] != 26} { error "Expected 26 physical DSPSIOU cells" }
if {[llength $dsp_mult_cells] != 26} { error "Expected 26 physical DSPMULT cells" }

set dsp_operand_pins [get_pins -hier -full_hier {
    road_onchip_chain_Inst_shell/mult0_syn_168.xa[*]
    road_onchip_chain_Inst_shell/mult0_syn_168.y[*]
    road_onchip_chain_Inst_shell/mult0_syn_263.xa[*]
    road_onchip_chain_Inst_shell/mult0_syn_263.y[*]
    road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult*_syn_57.xa[*]
    road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult*_syn_57.y[*]
}]
set dsp_result_pins [get_pins -hier -full_hier {
    road_onchip_chain_Inst_shell/mult0_syn_168.p[*]
    road_onchip_chain_Inst_shell/mult0_syn_263.p[*]
    road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult*_syn_57.p[*]
}]
set dsp_mult_internal_pins [get_pins -of $dsp_mult_cells]
if {[llength $dsp_operand_pins] == 0 || [llength $dsp_result_pins] == 0 || [llength $dsp_mult_internal_pins] == 0} {
    error "DSP timing pin selection is empty"
}
report_timing_path -through $dsp_operand_pins -ep_num $ep_limit -path_num 1 -file dsp_operand_paths.timing
report_timing_path -through $dsp_mult_internal_pins -ep_num $ep_limit -path_num 1 -file dsp_mult_internal_paths.timing
report_timing_path -through $dsp_result_pins -ep_num $ep_limit -path_num 1 -file dsp_result_paths.timing

# The only ERAM is the runtime-loaded SiLU table. Select only active A-port
# address/data/control and output pins, not unused primitive pins.
set eram_cells [get_cells -hier -full_hier {*PH1P_LOGIC_ERAM_Inst_silu_table_syn_1}]
if {[llength $eram_cells] != 1} { error "Expected exactly one physical SiLU ERAM" }
set eram_input_pins [get_pins -hier -full_hier {
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.addra[*]
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia[*]
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia_extra[*]
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.csa[*]
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.wea
}]
set eram_output_pins [get_pins -hier -full_hier {
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.doa[*]
    *PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.doa_extra[*]
}]
if {[llength $eram_input_pins] == 0 || [llength $eram_output_pins] == 0} {
    error "ERAM timing pin selection is empty"
}
report_timing_path -through $eram_input_pins -ep_num $ep_limit -path_num 1 -file eram_input_paths.timing
report_timing_path -through $eram_output_pins -ep_num $ep_limit -path_num 1 -file eram_output_paths.timing

puts "OBJECT_COUNT all_regs=[llength $all_regs]"
puts "OBJECT_COUNT dsp_siou_cells=[llength $dsp_siou_cells]"
puts "OBJECT_COUNT dsp_mult_cells=[llength $dsp_mult_cells]"
puts "OBJECT_COUNT dsp_operand_pins=[llength $dsp_operand_pins]"
puts "OBJECT_COUNT dsp_result_pins=[llength $dsp_result_pins]"
puts "OBJECT_COUNT dsp_mult_internal_pins=[llength $dsp_mult_internal_pins]"
puts "OBJECT_COUNT eram_cells=[llength $eram_cells]"
puts "OBJECT_COUNT eram_input_pins=[llength $eram_input_pins]"
puts "OBJECT_COUNT eram_output_pins=[llength $eram_output_pins]"
report_timing_exception -ep_num $ep_limit -path_num 1 -file full_timing_exceptions.rpt
report_timing_ignored -ep_num $ep_limit -path_num 1 -file full_timing_ignored.rpt
check_timing -verbose -file full_check_timing_verbose.rpt
report_abnormal_timing_target -file full_abnormal_targets.rpt
