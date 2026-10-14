import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
# Routed reference is read-only. The separate pre-route DB is the only candidate input.
import_db reference_pr.db
foreach name {
 u_compute/u_stem/reg_weight_n1_syn_817
 u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg[130]_syn_2
 u_compute/u_stem/cnt_channel_reg[1]_syn_54
 u_compute/u_stem/ramread11_syn_7458
 u_compute/u_stem/ramread11_syn_7858
 u_compute/u_down2/flag_halo_load_write_syn_1117
} {
    set object [get_cells -hier $name]
    if {[llength $object] != 1} {error "Reference locality object missing: $name"}
    puts "REFERENCE_CELL_BEGIN $name"
    report_cells $object -attributes -connection -pin_loc
    puts "REFERENCE_CELL_END $name"
}
foreach net_name {u_compute/u_stem/i_load_valid u_compute/u_stem/reg_weight_n1_dup_810 u_compute/u_stem/reg_weight_n1_syn_dup_702 u_compute/u_stem/reg_weight_n1_syn_dup_716} {
    set net [get_nets -hier $net_name]
    if {[llength $net] != 1} {error "Reference locality net missing: $net_name"}
    report_nets $net -connection -pin_display_limit 100
}
foreach grid {x35y23 x35y24 x35y25 x34y24 x36y24} {
    puts "REFERENCE_GRID_BEGIN $grid"
    report_cells -grid $grid
    puts "REFERENCE_GRID_END $grid"
}
close_project
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
foreach name {
 u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg[130]_syn_2
 u_compute/u_stem/cnt_channel_reg[1]_syn_54
} {
    set object [get_cells -hier $name]
    if {[llength $object] != 1} {error "Placed locality object missing: $name"}
    puts "PLACED_CELL_BEGIN $name"
    report_cells $object -attributes -connection -pin_loc
    puts "PLACED_CELL_END $name"
}
puts "LOCALITY_INSPECTION_DONE"
close_project
exit
