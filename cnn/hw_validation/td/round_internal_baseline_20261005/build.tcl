# SWUG105 single-run flow. Isolated registered fixture; never bitgen.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project round_internal_probe.al -single_run
elaborate -top road_round_internal_probe
read_adc probe.adc
optimize_rtl
report_area -file probe_rtl.area
read_sdc probe.sdc
optimize_gate
legalize_phy_inst
read_sdc probe.sdc
export_db gate.db
update_timing
place
route
export_db pr.db
report_area -io_info -file probe_route.area
update_timing -mode final
report_timing_status -file probe_route.ts
report_timing_summary -file probe_route.timing
report_timing_summary -viol_only -ep_num 10000 -path_num 1 -file all_violations.timing
report_timing_path -from [get_regs *] -to [get_regs *] -ep_num 10 -path_num 1 -file internal_reg_to_reg.timing
report_clock_summary -file clocks.timing
report_timing_exception -file exceptions.timing
report_timing_ignored -file ignored.timing
check_timing -file check.timing
close_project
