# Actual ROM + shared Stem/down2 top; stop before placement and bitstream.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_rom_current_down2_top.al -single_run
elaborate -top road_rom_current_down2_top
read_adc frontend.adc
optimize_rtl
report_area -verbose -file frontend_rtl.area
read_sdc frontend.sdc
optimize_gate
legalize_phy_inst
read_sdc frontend.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_rom_current_down2_top
report_qor -step gate -file gate.qor
puts "SINGLE_BANK_SYNTHESIS_DONE_NOT_PLACED"
close_project
exit
