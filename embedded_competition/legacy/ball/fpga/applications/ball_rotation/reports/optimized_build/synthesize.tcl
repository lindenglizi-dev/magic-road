import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd {E:/project/ball/fpga/applications/ball_rotation/td_project}
if {[catch {
open_project {E:/project/ball/fpga/applications/ball_rotation/td_project/ball_rotation.al}
commit_param -step design
elaborate -top design_top_wrapper
read_adc {E:/project/ball/fpga/applications/ball_rotation/user_source/constraints_source/pin.adc}
read_ip_adc -ip ddr2 -file {E:/project/ball/fpga/applications/ball_rotation/user_source/hdl_source/ph1p35_ddr/ddr2/src/adc/ddr2.adc}
read_sdc {E:/project/ball/fpga/applications/ball_rotation/td_project/camera_to_dsi_display.sdc}
read_sdc -ip ddr2 {E:/project/ball/fpga/applications/ball_rotation/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc}
read_sdc -ip w128_d512_fifo {E:/project/ball/fpga/applications/ball_rotation/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl}
commit_param -step rtl
optimize_rtl
report_area -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/rtl.area}
commit_param -step gate
optimize_gate -packarea {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate.area}
legalize_phy_inst
update_timing
foreach {clock_name expected} {
 sys_clk_50m 20.0
 pll_clk_24m 42.0
 MIPI_RX_BYTE_CLK 9.660
 u_ph1p35_324_ddr_wrapper/u_ddr2/ref_clk 15.0
 u_ph1p35_324_ddr_wrapper/u_ddr2/ctl_clk 15.0
 u_ph1p35_324_ddr_wrapper/u_ddr2/ddr_clk 3.75
 u_ph1p35_324_ddr_wrapper/u_ddr2/mcu_clk 39.375
 u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk 15.0
} {
 set actual [get_property -max PERIOD [get_clocks $clock_name]]
 if {$actual eq "" || abs($actual-$expected)>0.002} {error "CLOCK_PERIOD_MISMATCH: $clock_name $actual vs $expected"}
 puts "VERIFIED_CLOCK $clock_name $actual ns"
}
puts ROTATION_PLL_CLOCKS_VERIFIED
report_timing_status -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate.ts}
report_timing_summary -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate.timing}
check_timing -verbose -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate_constraint_check.txt}
export_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate.db}
puts ROTATION_OPTIMIZED_SYNTHESIS_COMPLETE
} error_message]} {puts stderr $error_message; exit 1}
exit
