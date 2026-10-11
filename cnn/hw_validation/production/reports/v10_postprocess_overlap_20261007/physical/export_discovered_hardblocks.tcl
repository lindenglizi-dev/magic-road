# Generated from this run's routed netlist; do not hand-edit names.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set dsp_cells [get_cells -hier -full_hier {
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult0_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult10_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult11_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult12_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult13_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult14_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult15_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult16_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult17_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult18_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult19_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult1_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult20_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult21_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult22_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult23_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult2_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult3_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult4_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult5_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult6_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult7_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult8_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult9_syn_57
    down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_170
    down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/mult0_syn_265
}]
set mac_dsp_cells [get_cells -hier -full_hier {
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult0_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult10_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult11_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult12_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult13_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult14_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult15_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult16_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult17_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult18_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult19_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult1_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult20_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult21_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult22_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult23_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult2_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult3_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult4_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult5_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult6_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult7_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult8_syn_57
    down2_overlap_tile_runner_Inst_shell/road_mac_probe_Inst_tile/mult9_syn_57
}]
set eram_cells [get_cells -hier -full_hier {
    down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/silu_shared_unit_Inst_shared/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1
}]
set dram_cells [get_cells -hier -full_hier {
    down2_overlap_tile_runner_Inst_shell/ramread0_syn_26
    down2_overlap_tile_runner_Inst_shell/ramread0_syn_46
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1004
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1024
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1044
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1064
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1084
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1104
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1124
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1144
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1164
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1184
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1204
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1224
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1244
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1264
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1284
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1304
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1324
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_1344
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_884
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_904
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_924
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_944
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_964
    down2_overlap_tile_runner_Inst_shell/ramread10_syn_984
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_114
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_134
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_34
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_54
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_74
    down2_overlap_tile_runner_Inst_shell/ramread36_syn_94
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10010
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10030
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10050
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10070
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10090
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10110
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10130
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10150
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10170
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10190
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10210
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10230
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10250
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10270
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10290
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10310
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_10330
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8750
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8770
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8790
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8810
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8830
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8850
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8870
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8890
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8910
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8930
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8950
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8970
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_8990
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9010
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9030
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9050
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9070
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9090
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9110
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9130
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9150
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9170
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9190
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9210
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9230
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9250
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9270
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9290
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9310
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9330
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9350
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9370
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9390
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9410
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9430
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9450
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9470
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9490
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9510
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9530
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9550
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9570
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9590
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9610
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9630
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9650
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9670
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9690
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9710
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9730
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9750
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9770
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9790
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9810
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9830
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9850
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9870
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9890
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9910
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9930
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9950
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9970
    down2_overlap_tile_runner_Inst_shell/ramread39_syn_9990
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1166
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1186
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1206
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1226
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1246
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1266
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1286
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1306
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1326
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1346
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1366
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1386
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1406
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1426
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1446
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1466
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1486
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1506
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1526
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1546
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1566
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1586
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1606
    down2_overlap_tile_runner_Inst_shell/ramread40_syn_1626
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_177
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_197
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_217
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_237
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_257
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_277
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_297
    down2_overlap_tile_runner_Inst_shell/ramread5_syn_317
    down2_overlap_tile_runner_Inst_shell/road_postprocess_stream_Inst_tile/ramread0_syn_26
}]
set all_regs [get_regs -hier *]

foreach {name objects minimum} [list     dsp_cells $dsp_cells 24     mac_dsp_cells $mac_dsp_cells 24     eram_cells $eram_cells 1     dram_cells $dram_cells 1     all_regs $all_regs 1] {
    if {[llength $objects] < $minimum} { error "$name minimum=$minimum actual=[llength $objects]" }
}

set dsp_pins [get_pins -of $dsp_cells]
set mac_dsp_pins [get_pins -of $mac_dsp_cells]
set eram_pins [get_pins -of $eram_cells]
set dram_pins [get_pins -of $dram_cells]
foreach {name objects} [list dsp_pins $dsp_pins mac_dsp_pins $mac_dsp_pins eram_pins $eram_pins dram_pins $dram_pins] {
    if {[llength $objects] == 0} { error "$name is empty" }
}

report_timing_path -through $dsp_pins -ep_num 100000 -path_num 1 -file discovered_dsp_paths.timing
report_timing_path -through $mac_dsp_pins -ep_num 100000 -path_num 1 -file discovered_mac_dsp_paths.timing
report_timing_path -through $eram_pins -ep_num 100000 -path_num 1 -file discovered_eram_paths.timing
report_timing_path -through $dram_pins -ep_num 100000 -path_num 1 -file discovered_dram_paths.timing
report_timing_path -from $all_regs -to $all_regs -ep_num 100000 -path_num 1 -file discovered_all_reg_paths.timing

set object_count_file [open discovered_object_counts.txt w]
foreach {name objects} [list dsp_cells $dsp_cells mac_dsp_cells $mac_dsp_cells eram_cells $eram_cells dram_cells $dram_cells all_regs $all_regs dsp_pins $dsp_pins mac_dsp_pins $mac_dsp_pins eram_pins $eram_pins dram_pins $dram_pins] {
    set line "OBJECT_COUNT $name=[llength $objects]"
    puts $line
    puts $object_count_file $line
}
close $object_count_file

report_timing_summary -ep_num 100000 -path_num 1 -file discovered_coverage_100000_summary.rpt
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file discovered_coverage_100000_violations.timing
report_timing_exception -ep_num 100000 -path_num 1 -file discovered_timing_exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file discovered_timing_ignored.rpt
check_timing -verbose -file discovered_check_timing_verbose.rpt
report_abnormal_timing_target -file discovered_abnormal_targets.rpt
