import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd {E:/project/ball/fpga/applications/ball_rotation/td_project}
if {[catch {
open_project {E:/project/ball/fpga/applications/ball_rotation/td_project/ball_rotation.al} -noanalyze
import_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.db}
update_timing -mode final
analyze_clock -detail
puts ROTATION_CLOCK_DETAIL_COMPLETE
} message]} {puts stderr $message; exit 1}
exit

