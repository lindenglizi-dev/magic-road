# Same device, clock constraints and gate optimization as the frozen joint top.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_overlap_low_io_top.al -single_run
elaborate -top road_rom_down2_top
optimize_rtl
report_area -verbose -file joint_rtl.area
read_sdc joint.sdc
optimize_gate
legalize_phy_inst
read_sdc joint.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_rom_down2_top
report_area -verbose -file joint_gate.area
report_ram_utilization -file joint_gate_ram.rpt
puts "INGRESS_SYNTHESIS_DONE"
close_project
