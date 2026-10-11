import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_dynamic_low_io_top.al -single_run
elaborate -top road_dynamic_low_io_top
read_adc shell.adc
optimize_rtl
report_area -verbose -file rtl.area
read_sdc shell.sdc
optimize_gate
legalize_phy_inst
read_sdc shell.sdc
export_db gate.db
write_verilog gate_netlist.v -top road_dynamic_low_io_top
update_timing
place
route
export_db pr.db
write_verilog routed_netlist.v -implement -top road_dynamic_low_io_top
report_area -verbose -io_info -file route.area
report_ram_utilization -file ram.rpt
report_io -verbose -file io.rpt
report_route_status -drc -file route_status.rpt
drc_check -all -verbose
update_timing -mode final
report_analysis_corner -all
report_analysis_corner -active
report_timing_summary -file timing_summary.rpt
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 100000 -path_num 1 -file with_ignored.timing
report_timing_summary -viol_only -ep_num 100000 -path_num 1 -file violations.timing
report_timing_exception -ep_num 100000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 100000 -path_num 1 -file ignored.rpt
check_timing -verbose -file check_timing.rpt

# 新实现不继承旧物理引脚编号；原生对象按角色分别查询。
set regs [get_regs -hier *]
set raw [get_ports {i_rstn}]
set meta [get_regs -hier -filter {NAME == reg_release_meta} *]
set done [get_regs -hier -filter {NAME == reg_release_done} *]
set functional [get_regs -hier -filter {NAME != reg_release_meta && NAME != reg_release_done} *]
if {[llength $meta] != 1 || [llength $done] != 1} { error "Reset alias count incorrect" }
report_timing_path -from $raw -to $regs -ep_num 100000 -path_num 1 -file raw_regs.timing
report_timing_path -from $meta -to $done -ep_num 100000 -path_num 1 -file sync_stages.timing
report_timing_path -from $done -to $functional -ep_num 100000 -path_num 1 -file functional_reset.timing
report_timing_path -from $regs -ep_num 100000 -path_num 1 -file reg_destinations.timing
set inputs [get_ports {i_rx_valid i_rx_data[*] i_tx_ready}]
set outputs [get_ports {o_rx_ready o_tx_valid o_tx_data[*]}]
report_timing_path -from $inputs -ep_num 100000 -path_num 1 -file input_destinations.timing
report_timing_path -to $outputs -ep_num 100000 -path_num 1 -file output_paths.timing
set dsp_cells [get_cells -hier -filter {REF_NAME =~ *DSP*} *]
set dsp_pins [get_pins -of $dsp_cells *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
set eram_pins [get_pins -of $eram_cells *]
report_timing_path -through $dsp_pins -ep_num 100000 -path_num 1 -file dsp_paths.timing
report_timing_path -through $eram_pins -ep_num 100000 -path_num 1 -file eram_paths.timing
puts "DIAGNOSTIC_PHYSICAL_COMPLETE"
close_project
