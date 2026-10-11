# Read-only evidence export from the frozen routed database.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../../../td/round_internal_baseline_20261005/pr.db
update_timing -mode final

# SWUG105-documented report/export commands.
write_verilog routed_netlist.v
check_timing -file check_timing_default.rpt
check_timing -verbose -file check_timing_verbose.rpt
report_clock_summary -file clock_summary.rpt
report_timing_summary -file timing_summary.rpt
report_timing_exception -file timing_exceptions.rpt
report_timing_ignored -file timing_ignored.rpt

# Installed-version object queries, emitted as readable names for netlist mapping.
set object_report [open object_queries.txt w]
puts $object_report "dummy cells: [get_cells -hier {*_al_n1_syn_76*}]"
puts $object_report "dummy nets: [get_nets -hier {*_al_n1_syn_76*}]"
puts $object_report "dummy pins: [get_pins -hier {*_al_n1_syn_76*}]"
puts $object_report "reset regs: [get_regs -hier {*reset_release*}]"
puts $object_report "reset cells: [get_cells -hier {*reset_release*}]"
puts $object_report "reset nets: [get_nets -hier {*reset_release*}]"
puts $object_report "reset pins: [get_pins -hier {*reset_release*}]"
close $object_report

report_timing_path -from [get_ports {i_rstn}] -to [get_pins -hier {road_round_reset_gen_Inst_release/reg_reset_release_reg_syn_3.asr}] -ep_num 10 -path_num 10 -file reset_entry_paths.rpt
report_timing_path -from [get_regs -hier {road_round_reset_gen_Inst_release/reg_reset_meta}] -to [get_regs -hier {road_round_internal_probe_core_Inst_datapath/i_rstn}] -ep_num 10 -path_num 10 -file reset_stage_to_stage.rpt
report_timing_path -from [get_regs -hier {road_round_internal_probe_core_Inst_datapath/i_rstn}] -to [get_regs -hier {*}] -ep_num 10000 -path_num 1 -file reset_release_to_function.rpt
