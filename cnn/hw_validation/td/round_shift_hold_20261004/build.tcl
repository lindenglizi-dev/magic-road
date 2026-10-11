import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project round_shift_probe.al -single_run
elaborate -top road_round_shift
read_adc probe.adc
read_sdc probe.sdc
optimize_rtl
report_area -file probe_rtl.area
optimize_gate
legalize_phy_inst
update_timing
place
route
fix_hold
report_area -io_info -file probe_route.area
update_timing -mode final
report_timing_status -file probe_route.ts
report_timing_summary -file probe_route.timing
