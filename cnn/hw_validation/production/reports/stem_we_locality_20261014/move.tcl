import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
update_timing
# Replay only the two already proven repairs; do not add WE replication.
phys_opt -force_replication_on_nets {u_compute/u_pp/u_pre/u_round/i_advance_dup_2} -fanout_threshold 128
phys_opt -force_replication_on_nets {u_rom/cnt_wait_b_n_dup_4} -fanout_threshold 16
set target {u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg[130]_syn_2}
set object [get_cells -hier $target]
if {[llength $object] != 1} {error "Exactly one locality target required"}
puts "LOCALITY_BEFORE_BEGIN"
report_cells $object -attributes -connection -pin_loc
report_cells -grid x36y24
puts "LOCALITY_BEFORE_END"
write_verilog before_move.v -implement -top road_rom_current_down2_top
# Nonforce: never evict neighbours or broaden the search to other clusters.
set target_pattern {u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg*130*_syn_2}
set matched [get_cells -hier $target_pattern]
if {[llength $matched] != 1 || [get_property NAME $matched] ne $target} {error "Move pattern must resolve only the frozen target"}
puts "MOVE_ARGUMENT_NAME [get_property NAME $matched] COLLECTION=$matched"
# Quote the literal name for TD's second argument parser; do not escape the stored name.
set literal_name [format {"%s"} $target]
move_cells -inst $literal_name -location {x36y24} -mode nonforce -step place
puts "LOCALITY_AFTER_BEGIN"
report_cells $object -attributes -connection -pin_loc
report_cells -grid x36y24
puts "LOCALITY_AFTER_END"
report_placement_status
write_verilog after_move.v -implement -top road_rom_current_down2_top
export_db local_placed.db
puts "LOCALITY_MOVE_DONE_NOT_ROUTED"
close_project
exit
