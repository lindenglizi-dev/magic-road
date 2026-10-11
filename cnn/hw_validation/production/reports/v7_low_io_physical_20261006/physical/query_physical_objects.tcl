# Read-only object inventory from the frozen routed database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db pr.db
update_timing -mode final

set all_mult_cells [get_cells -hier -full_hier {*mult*_syn_*}]
set eram_cells [get_cells -hier -full_hier {*PH1P_LOGIC_ERAM_Inst_silu_table_syn_1}]
set mult_pins [get_pins -of $all_mult_cells]
set eram_pins [get_pins -of $eram_cells]

puts "OBJECT_COUNT all_mult_cells=[llength $all_mult_cells]"
puts "OBJECT_COUNT all_mult_pins=[llength $mult_pins]"
puts "OBJECT_COUNT eram_cells=[llength $eram_cells]"
puts "OBJECT_COUNT eram_pins=[llength $eram_pins]"
puts "OBJECT_LIST_BEGIN all_mult_cells"
puts [join $all_mult_cells "\n"]
puts "OBJECT_LIST_END all_mult_cells"
puts "OBJECT_LIST_BEGIN eram_cells"
puts [join $eram_cells "\n"]
puts "OBJECT_LIST_END eram_cells"
puts "OBJECT_LIST_BEGIN eram_pins"
puts [join $eram_pins "\n"]
puts "OBJECT_LIST_END eram_pins"
