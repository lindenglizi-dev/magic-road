import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_stem_ddr_board_top.al -single_run
import_db pr.db
read_sdc {E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/frontend_ddr_full_20261015/physical/board.sdc}
read_sdc -ip ddr2 {E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/frontend_ddr_full_20261015/physical/ddr2/src/sdc/ddr2.sdc}
read_sdc {E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/frontend_ddr_full_20261015/physical/resolved_display.sdc}
update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 256 -path_num 1 -file include_ignored.timing
check_timing -verbose -file check_timing.rpt
report_timing_exception -ep_num 1000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 1000 -path_num 1 -file ignored.rpt
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clocks.rpt
puts "BANK_CONSTRAINT_RECHECK_COMPLETE"
close_project
