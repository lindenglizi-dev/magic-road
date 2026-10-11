# Supplement IR aliases with actual physical clock-to-output roots. DSP
# input-register Qs (mult_x/mult_y) are not the same as registered P output.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../snapshot/pr.db
update_timing -mode final
set slice_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_LSLICE} *]
set slice_q [get_pins -of $slice_cells {*.oqa *.oqb}]
set dsp_cells [get_cells -hier -filter {REF_NAME == PH1P_PHY_DSPSIOU_V2} *]
set dsp_q [get_pins -of $dsp_cells -filter {DIRECTION == output} *]
set eram_cells [get_cells -hier -filter {REF_NAME =~ *ERAM*} *]
set eram_q [get_pins -of $eram_cells -filter {DIRECTION == output} *]
foreach name {slice_q dsp_q eram_q} {
    set stream [open "$name.objects" {WRONLY CREAT EXCL}]
    foreach object [set $name] { puts $stream $object }
    close $stream
    puts "PHYSICAL_SOURCE_COUNT $name [llength [set $name]]"
}
report_timing_path -from $slice_q -ep_num 100000 -path_num 1 -file physical_slice_sources.timing
report_timing_path -from $dsp_q -ep_num 100000 -path_num 1 -file physical_dsp_sources.timing
report_timing_path -from $eram_q -ep_num 100000 -path_num 1 -file physical_eram_sources.timing
puts "A_PHASE_COMPLETE"
