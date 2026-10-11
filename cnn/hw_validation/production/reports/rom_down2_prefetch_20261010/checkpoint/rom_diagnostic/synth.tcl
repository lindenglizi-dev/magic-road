# Frozen original ROM logic, new schema2 file binding. No bitstream command.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_overlap_low_io_top.al -single_run
elaborate -top road_yolo_numeric_rom_probe
optimize_rtl
report_area -verbose -file rom_rtl.area
read_sdc rom.sdc
optimize_gate
legalize_phy_inst
read_sdc rom.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_yolo_numeric_rom_probe
report_area -verbose -file rom_gate.area
report_ram_utilization -file rom_gate_ram.rpt
set erams [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
puts "ROM_ERAM_COUNT [llength $erams]"
report_design_cell_num -hier -top 100
set undriven [get_nets -hier -filter {DRIVER_COUNT == 0} *]
foreach net $undriven {
    puts "UNDRIVEN_RECORD [get_property NAME $net] PINS [get_property PIN_COUNT $net] DRIVER [get_property DRIVER_COUNT $net]"
}
report_nets $undriven -connection -pin_display_limit 100
puts "ROM_SYNTH_DONE"
close_project
