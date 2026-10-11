# Independent legacy 720p template build. All reports stay under this directory.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project hw_video_baseline.al -single_run
elaborate -top design_top_wrapper
read_adc E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/user_source/constraints_source/pin.adc
read_ip_adc -ip ddr2 -file E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/user_source/hdl_source/ph1p35_ddr/ddr2/src/adc/ddr2.adc
read_sdc E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/td_project/camera_to_dsi_display.sdc
read_sdc -ip ddr2 E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc
read_sdc -ip w128_d512_fifo E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl
optimize_rtl
report_area -file template_rtl.area
optimize_gate -packarea template_gate.area
legalize_phy_inst
update_timing
report_timing_summary -file template_gate.timing
place
update_timing -mode manhattan
report_area -io_info -file template_place.area
report_timing_summary -file template_place.timing
route
report_area -io_info -file template_route.area
update_timing -mode final
report_timing_status -file template_route.ts
report_timing_summary -file template_route.timing

# JTAG recovery artifact only; no programmer or Flash operation here.
bitgen -bit hw_video_baseline.bit
