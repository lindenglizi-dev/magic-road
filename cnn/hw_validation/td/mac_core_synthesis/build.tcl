import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project mac_core_synthesis.al -single_run
elaborate -top road_mac_probe
optimize_rtl
report_area -file mac_core_rtl.area
optimize_gate
report_area -file mac_core_gate.area
