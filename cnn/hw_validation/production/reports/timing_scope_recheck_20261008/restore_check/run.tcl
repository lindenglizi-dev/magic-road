import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
puts "CLOCK_QUERY [get_clocks -include_generated_clocks *]"
puts "CLOCK_QUERY_COUNT [llength [get_clocks -include_generated_clocks *]]"
report_analysis_corner -active
report_timing_summary -ep_num 25 -path_num 1 -file restored_sanity.timing
report_timing_status -file restored_status.rpt
foreach pin [get_pins -hier {reg_release_done_reg_syn_3.oqa reg_release_done_reg_syn_3.oqb}] { report_property $pin }
set dsp_cells [get_cells -hier -filter {REF_NAME =~ *DSP*} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
puts "DSP_CELLS $dsp_cells"
puts "ERAM_CELLS $eram_cells"
foreach cell [concat $dsp_cells $eram_cells] {
    set pins [get_pins -of [list $cell] *]
    puts "HARD_PINS $pins"
    foreach pin [lrange $pins 0 2] { report_property $pin }
}
puts "A_PHASE_COMPLETE"
