import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd {E:/project/ball/fpga/applications/ball_rotation/td_project}
if {[catch {
open_project {E:/project/ball/fpga/applications/ball_rotation/td_project/ball_rotation.al} -noanalyze
import_db {E:/project/ball/fpga/applications/ball_rotation/reports/optimized_build/route.db}
update_timing -mode final
report_timing_status -file {E:/project/ball/fpga/applications/ball_rotation/release/route.ts}
report_timing_summary -file {E:/project/ball/fpga/applications/ball_rotation/release/route.timing}
report_area -io_info -file {E:/project/ball/fpga/applications/ball_rotation/release/route.area}
# Recompute and gate the imported database before producing any bitstream.
set status_fd [open {E:/project/ball/fpga/applications/ball_rotation/release/route.ts} r]
set status_text [read $status_fd]
close $status_fd
foreach metric {SWNS STNS HWNS HTNS} {
 set pattern [format {%s: (-?[0-9]+[.][0-9]+)ns} $metric]
 if {![regexp $pattern $status_text unused value]} {error "MISSING_TIMING_METRIC: $metric"}
 if {$value < 0.0 || (($metric eq "STNS" || $metric eq "HTNS") && $value != 0.0)} {error "FAILED_TIMING: $metric $value"}
 puts "RELEASE_TIMING $metric $value ns"
}
puts ROTATION_RELEASE_TIMING_PASSED
commit_param -step bitgen
bitgen -bit {E:/project/ball/fpga/applications/ball_rotation/release/ball_rotation.bit} -compress -g {mclk_freq:33MHz boot_mode:mspix4}
export_bitgen_param -file {E:/project/ball/fpga/applications/ball_rotation/release/bitgen_param.f}
puts ROTATION_RELEASE_BITGEN_COMPLETE
} message]} {puts stderr $message; exit 1}
exit
