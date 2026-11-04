import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd {E:/project/ball/fpga/applications/ball_rotation/td_project}
if {[catch {
open_project {E:/project/ball/fpga/applications/ball_rotation/td_project/ball_rotation.al} -noanalyze
import_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/gate.db}
commit_param -step place
insert_debugger
place
update_timing -mode manhattan
report_timing_summary -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/place.timing}
report_area -io_info -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/place.area}
export_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/place.db}
puts ROTATION_OPTIMIZED_PLACEMENT_COMPLETE
commit_param -step route
route
update_timing -mode final
report_timing_status -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.ts}
report_timing_summary -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.timing}
report_timing_exception -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/exception.timing}
report_area -io_info -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.area}
report_clock_utilization -file {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route_clocks.txt}
export_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.db}
puts ROTATION_OPTIMIZED_ROUTE_COMPLETE
} error_message]} {puts stderr $error_message; exit 1}
exit
