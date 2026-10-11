# Isolated diagnostic bitstream only. No programmer or board command.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_board_selftest_top.al -single_run
import_db pr.db
read_sdc board.sdc
report_area -verbose -io_info -file imported.area
update_timing -mode final
report_timing_status -file imported.ts
report_timing_summary -file imported.timing
bitgen -bit RoadYOLO_HX1P35A_KEY4_SELFTEST.bit
export_bitgen_param -file bitgen_parameters.txt
close_project
