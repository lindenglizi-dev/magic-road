import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db source_placed.db
update_timing
# Keep the two proven baseline control repairs, no new replication.
phys_opt -force_replication_on_nets {u_compute/u_pp/u_pre/u_round/i_advance_dup_2} -fanout_threshold 128
phys_opt -force_replication_on_nets {u_rom/cnt_wait_b_n_dup_4} -fanout_threshold 16
set target {u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg[130]_syn_2}
set object [get_cells -hier $target]
if {[llength $object] != 1} {error "Require exactly one frozen physical target"}
puts "LOCATION_BEFORE_BEGIN"
report_cells $object -attributes -connection -pin_loc
puts "LOCATION_BEFORE_END"
write_verilog before_place.v -implement -top road_rom_current_down2_top
read_adc locality.adc
place
set object [get_cells -hier $target]
if {[llength $object] != 1} {error "Target disappeared during placement"}
puts "LOCATION_AFTER_BEGIN"
report_cells $object -attributes -connection -pin_loc
report_cells -grid x36y24
puts "LOCATION_AFTER_END"
write_verilog after_place.v -implement -top road_rom_current_down2_top
export_db local_placed.db
puts "LOCATION_PLACED_NOT_ROUTED"
close_project
exit
