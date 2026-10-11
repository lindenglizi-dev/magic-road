# Warning-origin diagnosis only: no placement, routing, timing exceptions or bitgen.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_driven_probe.al -single_run
elaborate -top road_driven_probe
optimize_rtl
report_area -verbose -file driven.area
export_db driven.db
write_verilog driven_netlist.v -top road_driven_probe
puts "PROBE_SYNTHESIS_DONE"
close_project
