# PH1P-only native hold-fix candidate from the frozen baseline gate database.
# No RTL, numerical contract, SDC exception, clock, or I/O delay is changed.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../gate.db
clear_sdc -user
read_sdc ../shell.sdc

# SWUG105 documents route fix_hold=on for all supported device families.
# The stronger High value is PH2-only and is intentionally not used on PH1P.
set_param route fix_hold on
report_param

place
report_qor -step place -file hold_fix_place.qor
route
report_qor -step route -file hold_fix_route.qor
export_db hold_fix_pr.db
write_verilog hold_fix_routed_netlist.v -implement -top road_low_io_physical_shell
report_area -verbose -io_info -file hold_fix_route.area
report_ram_utilization -file hold_fix_route_ram.rpt
report_io -verbose -file hold_fix_route_io.rpt
report_route_status -drc -file hold_fix_route_status.rpt
drc_check -all -verbose

update_timing -mode final
report_timing_status -file hold_fix_route.ts
report_timing_summary -ep_num 20000 -path_num 1 -file hold_fix_all_paths.timing
report_timing_summary -include_ignored -ep_num 20000 -path_num 1 -file hold_fix_include_ignored.timing
report_timing_summary -viol_only -ep_num 20000 -path_num 1 -file hold_fix_violations.timing

set all_regs [get_regs -hier *]
set reset_port [get_ports {i_rstn}]
set data_inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set data_outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
if {[llength $all_regs] == 0} { error "No registers in hold-fix routed database" }
if {[llength $reset_port] != 1} { error "Expected one reset port" }
if {[llength $data_inputs] != 18 || [llength $data_outputs] != 18} {
    error "Diagnostic I/O selection mismatch"
}
report_timing_path -from $all_regs -to $all_regs -ep_num 20000 -path_num 1 -file hold_fix_internal_reg_to_reg.timing
report_timing_path -from $data_inputs -to $all_regs -ep_num 20000 -path_num 1 -file hold_fix_diagnostic_inputs_to_regs.timing
report_timing_path -from $all_regs -to $data_outputs -ep_num 20000 -path_num 1 -file hold_fix_regs_to_outputs.timing
report_timing_path -from $reset_port -to $all_regs -ep_num 20000 -path_num 1 -file hold_fix_reset_recovery_removal.timing

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
set eram_cells [get_cells -hier -full_hier {*PH1P_LOGIC_ERAM_Inst_silu_table_syn_1}]
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
if {[llength $dsp_operand_pins] == 0 || [llength $dsp_result_pins] == 0} {
    error "DSP timing selection is empty"
}
if {[llength $eram_cells] != 1 || [llength $eram_input_pins] == 0 || [llength $eram_output_pins] == 0} {
    error "ERAM timing selection mismatch"
}
report_timing_path -through $dsp_operand_pins -ep_num 20000 -path_num 1 -file hold_fix_dsp_operand_paths.timing
report_timing_path -through $dsp_result_pins -ep_num 20000 -path_num 1 -file hold_fix_dsp_result_paths.timing
report_timing_path -through $eram_input_pins -ep_num 20000 -path_num 1 -file hold_fix_eram_input_paths.timing
report_timing_path -through $eram_output_pins -ep_num 20000 -path_num 1 -file hold_fix_eram_output_paths.timing

report_timing_exception -ep_num 20000 -path_num 1 -file hold_fix_timing_exceptions.rpt
report_timing_ignored -ep_num 20000 -path_num 1 -file hold_fix_timing_ignored.rpt
check_timing -verbose -file hold_fix_check_timing_verbose.rpt
report_abnormal_timing_target -file hold_fix_abnormal_targets.rpt
