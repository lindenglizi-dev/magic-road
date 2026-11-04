set project_root [file normalize [file join [file dirname [info script]] ..]]
set status_file "$project_root/build/optimized/route_flow.status"
if {![file exists $status_file]} {error "Run build.tcl and optimize_route.tcl first"}
set handle [open $status_file r]
set status_text [read $handle]
close $handle
foreach check_type {Setup Hold} {
    set expression [format {%s\s*: WNS\s+(-?[0-9]+)ps\s+TNS\s+(-?[0-9]+)ps\s+NUM_FEPS\s+([0-9]+)} $check_type]
    if {![regexp $expression $status_text all wns tns failures] || $wns < 0 || $tns != 0 || $failures != 0} {
        error "Timing qualification failed: $check_type"
    }
}
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db "$project_root/build/optimized/routed.db"
cd "$project_root/build/optimized"
commit_param -step bitgen
bitgen -bit "$project_root/build/ball_face.bit"
export_bitgen_param -file "$project_root/build/bitgen_parameters.txt"
puts BITSTREAM_COMPLETE
exit

