import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
import_db pr.db
set target {u_rom/road_yolo_numeric_rom_group_Inst_xi/word_data_o_reg[130]_syn_2}
set object [get_cells -hier $target]
if {[llength $object] != 1} {error "Final target missing or ambiguous"}
puts "FINAL_LOCATION_BEGIN"
report_cells $object -attributes -connection -pin_loc
puts "FINAL_LOCATION_END"
puts "FINAL_LOCATION_INSPECTION_DONE"
close_project
exit
