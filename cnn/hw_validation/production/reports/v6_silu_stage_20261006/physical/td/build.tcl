# SWUG105 single-run flow. Isolated registered fixture; never bitgen.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project silu_internal_probe.al -single_run
elaborate -top silu_internal_probe
read_adc probe.adc
optimize_rtl
report_area -file probe_rtl.area
read_sdc probe.sdc
optimize_gate
legalize_phy_inst
read_sdc probe.sdc
export_db gate.db
write_verilog gate_netlist.v -top silu_internal_probe
update_timing
place
route
export_db pr.db
write_verilog routed_netlist.v -implement -top silu_internal_probe
report_area -io_info -file probe_route.area
update_timing -mode final
report_timing_status -file probe_route.ts
report_timing_summary -file probe_route.timing
report_timing_summary -viol_only -ep_num 10000 -path_num 1 -file all_violations.timing
report_timing_path -from [get_regs -hier *] -to [get_regs -hier *] -ep_num 10000 -path_num 1 -file internal_reg_to_reg.timing
report_clock_summary -file clocks.timing
report_timing_exception -file exceptions.timing
report_timing_ignored -file ignored.timing
check_timing -file check.timing
close_project
