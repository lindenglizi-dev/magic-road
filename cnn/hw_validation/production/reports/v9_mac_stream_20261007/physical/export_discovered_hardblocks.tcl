# Generated from this run's routed_netlist.v; do not hand-edit instance names.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set dsp_siou_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57
}]
set dsp_mult_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_169
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_264
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_58
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_58
}]
set mac_dsp_siou_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57
}]
set dsp_reset_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.rst[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.rst[*]
}]
set dsp_operand_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.y[*]
}]
set dsp_result_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.p[*]
}]
set dsp_control_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_168.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/mult0_syn_263.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.opctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.ce[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.inctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.muxctrl[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.opctrl[*]
}]
set mac_dsp_operand_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.y[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.xa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.y[*]
}]
set mac_dsp_result_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult0_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult10_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult11_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult12_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult13_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult14_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult15_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult16_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult17_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult18_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult19_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult1_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult20_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult21_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult22_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult23_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult2_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult3_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult4_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult5_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult6_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult7_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult8_syn_57.p[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/mult9_syn_57.p[*]
}]
set dsp_mult_internal_pins [get_pins -of $dsp_mult_cells]

set eram_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1
}]
set eram_input_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.addra[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.dia_extra[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.csa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.wea
}]
set eram_output_pins [get_pins -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.doa[*]
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/silu_shared_unit_Inst_chain/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.doa_extra[*]
}]

set feature_cache_dram_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_187
}]
set feature_cache_mslice_cells [get_cells -hier -full_hier {
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_179
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_180
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_181
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_182
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_183
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_184
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_185
    road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/ramread0_syn_186
}]
set feature_cache_dram_pins [get_pins -of $feature_cache_dram_cells]
set feature_cache_mslice_pins [get_pins -of $feature_cache_mslice_cells]

set mac_regs [get_regs -hier {*road_mac_probe_Inst_chain/*}]
set mac_bias_regs [get_regs -hier {*road_mac_probe_Inst_chain/reg_bias*}]
set mac_valid_regs [get_regs -hier {*road_mac_probe_Inst_chain/*valid*}]
set mac_dot_regs [get_regs -hier {*road_mac_probe_Inst_chain/reg_dot*}]
set mac_accumulator_regs [get_regs -hier {*road_mac_probe_Inst_chain/reg_accumulator*}]

foreach {name objects expected} [list     dsp_siou_cells $dsp_siou_cells 26     dsp_mult_cells $dsp_mult_cells 26     mac_dsp_siou_cells $mac_dsp_siou_cells 24     eram_cells $eram_cells 1     feature_cache_dram_cells $feature_cache_dram_cells 1     feature_cache_mslice_cells $feature_cache_mslice_cells 8] {
    if {[llength $objects] != $expected} { error "$name expected=$expected actual=[llength $objects]" }
}
set object_count_lines {}
foreach {name objects} [list     dsp_reset_pins $dsp_reset_pins     dsp_operand_pins $dsp_operand_pins     dsp_result_pins $dsp_result_pins     dsp_control_pins $dsp_control_pins     mac_dsp_operand_pins $mac_dsp_operand_pins     mac_dsp_result_pins $mac_dsp_result_pins     dsp_mult_internal_pins $dsp_mult_internal_pins     eram_input_pins $eram_input_pins     eram_output_pins $eram_output_pins     feature_cache_dram_pins $feature_cache_dram_pins     feature_cache_mslice_pins $feature_cache_mslice_pins     mac_regs $mac_regs     mac_bias_regs $mac_bias_regs     mac_valid_regs $mac_valid_regs     mac_dot_regs $mac_dot_regs     mac_accumulator_regs $mac_accumulator_regs] {
    if {[llength $objects] == 0} { error "$name is empty" }
}

report_timing_path -through $dsp_reset_pins -ep_num 20000 -path_num 1 -file dsp_reset_paths.timing
report_timing_path -through $dsp_operand_pins -ep_num 20000 -path_num 1 -file dsp_operand_paths.timing
report_timing_path -through $dsp_mult_internal_pins -ep_num 20000 -path_num 1 -file dsp_mult_internal_paths.timing
report_timing_path -through $dsp_result_pins -ep_num 20000 -path_num 1 -file dsp_result_paths.timing
report_timing_path -through $dsp_control_pins -ep_num 20000 -path_num 1 -file dsp_control_paths.timing
report_timing_path -through $mac_dsp_operand_pins -ep_num 20000 -path_num 1 -file mac_dsp_operand_paths.timing
report_timing_path -through $mac_dsp_result_pins -ep_num 20000 -path_num 1 -file mac_dsp_result_paths.timing
report_timing_path -from $mac_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_internal_reg_to_reg.timing
report_timing_path -from $mac_bias_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_bias_paths.timing
report_timing_path -from $mac_valid_regs -to $mac_regs -ep_num 20000 -path_num 1 -file mac_valid_control_paths.timing
report_timing_path -from $mac_accumulator_regs -to $mac_accumulator_regs -ep_num 1000 -path_num 10 -file mac_a5_feedback_paths.timing
report_timing_path -from $mac_dot_regs -to $mac_accumulator_regs -ep_num 1000 -path_num 10 -file mac_dot_to_accumulator_paths.timing
report_timing_path -through $eram_input_pins -ep_num 20000 -path_num 1 -file eram_input_paths.timing
report_timing_path -through $eram_output_pins -ep_num 20000 -path_num 1 -file eram_output_paths.timing
report_timing_path -through $feature_cache_dram_pins -ep_num 20000 -path_num 1 -file feature_cache_dram_paths.timing
report_timing_path -through $feature_cache_mslice_pins -ep_num 20000 -path_num 1 -file feature_cache_data_paths.timing

foreach {name objects} [list     dsp_siou_cells $dsp_siou_cells     dsp_mult_cells $dsp_mult_cells     mac_dsp_siou_cells $mac_dsp_siou_cells     dsp_reset_pins $dsp_reset_pins     dsp_operand_pins $dsp_operand_pins     dsp_result_pins $dsp_result_pins     dsp_control_pins $dsp_control_pins     mac_dsp_operand_pins $mac_dsp_operand_pins     mac_dsp_result_pins $mac_dsp_result_pins     dsp_mult_internal_pins $dsp_mult_internal_pins     eram_cells $eram_cells     eram_input_pins $eram_input_pins     eram_output_pins $eram_output_pins     feature_cache_dram_cells $feature_cache_dram_cells     feature_cache_mslice_cells $feature_cache_mslice_cells     feature_cache_dram_pins $feature_cache_dram_pins     feature_cache_mslice_pins $feature_cache_mslice_pins     mac_regs $mac_regs     mac_bias_regs $mac_bias_regs     mac_valid_regs $mac_valid_regs     mac_dot_regs $mac_dot_regs     mac_accumulator_regs $mac_accumulator_regs] {
    set line "OBJECT_COUNT $name=[llength $objects]"
    puts $line
    lappend object_count_lines $line
}
set object_count_file [open discovered_object_counts.txt w]
foreach line $object_count_lines { puts $object_count_file $line }
close $object_count_file

report_timing_summary -ep_num 20000 -path_num 1 -file discovered_full_timing_summary.rpt
report_timing_summary -viol_only -ep_num 20000 -path_num 1 -file discovered_full_violations.timing
report_timing_exception -ep_num 20000 -path_num 1 -file discovered_timing_exceptions.rpt
report_timing_ignored -ep_num 20000 -path_num 1 -file discovered_timing_ignored.rpt
check_timing -verbose -file discovered_check_timing_verbose.rpt
report_abnormal_timing_target -file discovered_abnormal_targets.rpt
