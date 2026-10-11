# pr.db stores constraints. Initialize timing before querying clocks; do not
# read the SDC again or add a clock/exception to the frozen constraint graph.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
set clocks [get_clocks -include_generated_clocks *]
if {[llength $clocks] != 1} { error "Expected original single clock after timing initialization" }
puts "RESTORED_CLOCKS $clocks"
report_analysis_corner -all
report_analysis_corner -active
report_timing_summary -ep_num 25 -path_num 1 -file restored_sanity.timing
report_timing_status -file restored_status.rpt
set reset_q [get_pins -hier {reg_release_done_reg_syn_3.oqa reg_release_done_reg_syn_3.oqb}]
foreach pin $reset_q { report_property $pin }
foreach cell [get_cells -hier *] {
    set type [get_property REF_NAME $cell]
    if {[string match {*DSP*} $type] || [string match {*ERAM*} $type]} {
        puts "HARD_CELL $type $cell"
        report_property $cell
        set pins [get_pins -of [list $cell] *]
        puts "HARD_PINS $pins"
        foreach pin [lrange $pins 0 2] { report_property $pin }
    }
}
puts "A_PHASE_COMPLETE"
