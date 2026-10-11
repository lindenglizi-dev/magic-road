# import_db restores frozen timing constraints. Do not read the same SDC twice.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_board_selftest_top.al -single_run
import_db pr.db
report_area -verbose -io_info -file imported.area
update_timing -mode final
report_timing_status -file imported.ts
report_timing_summary -ep_num 100000 -path_num 1 -file imported.timing
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -file clocks.rpt
check_timing -verbose -file check_timing.rpt
bitgen -bit RoadYOLO_HX1P35A_KEY4_SELFTEST.bit
export_bitgen_param -file bitgen_parameters.txt
close_project
