

set project_root [file normalize [file join [file dirname [info script]] ../..]]
set screen_root [file normalize [file dirname [info script]]]
set candidate_settings [dict create \
 seed0_macro_congestion {0 macro_congestion} \
 seed1_macro_congestion {1 macro_congestion} \
 seed0_auto {0 auto}]
if {![info exists candidate] || ![dict exists $candidate_settings $candidate]} {
 error "Unknown placement screening candidate"
}
lassign [dict get $candidate_settings $candidate] candidate_seed candidate_macro
set output_dir [file join $screen_root $candidate]
set gate_db "$project_root/build/gate/gate.db"
if {![file isfile $gate_db] || [file size $gate_db] <= 0} {error "New routelean gate.db is not ready: $gate_db"}
if {[file exists "$output_dir/place.db"] || [file exists "$output_dir/screen.pass"]} {
 error "Candidate already has a result; preserve it and use a separate explicitly reviewed rerun directory"
}

proc screen_file_binding {path} {
 set fh [open $path rb]
 set checksum 0
 while {![eof $fh]} {set checksum [zlib crc32 [read $fh 1048576] $checksum]}
 close $fh
 return [dict create path [file normalize $path] size [file size $path] crc32 [format %08x $checksum]]
}
proc require_active_clocks {} {
 set expected {
  ETH_RX_CLK ETH_RX_FABRIC ETH_TX_CLK HDMI_PIXEL_CLK HDMI_SERIAL_CLK
  MIPI_RX_BYTE_CLK PHY_TX_CAPTURE mipi_rx_ck_pad pll_clk_100m pll_clk_24m sys_clk_50m
  u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.io_clk_pad_p
  u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.tif_c16_in
  u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.tif_c20_in
  u_ph1p35_324_ddr_wrapper/u_ddr2/ctl_clk
  u_ph1p35_324_ddr_wrapper/u_ddr2/ddr_clk
  u_ph1p35_324_ddr_wrapper/u_ddr2/mcu_clk
  u_ph1p35_324_ddr_wrapper/u_ddr2/ref_clk
  u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk
 }
 set actual [lsort [get_clocks *]]
 if {$actual ne [lsort $expected]} {error "Active clock set changed: $actual"}
 puts "VERIFIED_ACTUAL_CLOCK_SET=[llength $actual]"
}

set initial_gate_binding [screen_file_binding $gate_db]
file mkdir $output_dir
set fh [open "$output_dir/input_binding.tcl" w]
puts $fh [dict create candidate $candidate seed $candidate_seed macro_performance $candidate_macro \
 source_root $project_root gate_db $initial_gate_binding constraints inherited_from_same_new_gate_db \
 started_epoch [clock seconds]]
close $fh
puts "SCREEN_CANDIDATE=$candidate SOURCE_ROOT=$project_root INPUT=$initial_gate_binding"

import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db $gate_db

read_adc "$project_root/scripts/reference_slots.adc"
set_param flow thread 8
set_param flow enable_seed on
set_param place seed $candidate_seed
set_param place opt_timing high
set_param place ofv 70
set_param place opt_max_density 50
set_param place target_density 0.6
set_param place target_density_pp 0.7
set_param place aggressive_opt 20
set_param place enhanced_beeline_opt 2
set_param place enhanced_gp on
set_param place non_crit_opt on
set_param place post_place_opt high
set_param place macro_performance $candidate_macro
set_param place enable_congestion_recovery on
cd $output_dir
set members [list {u_power_on_reset/ref_startup_complete_reg} {S_ref_reset_release_reg[0]} {S_ref_reset_release_reg[1]}]
foreach member $members {
 if {[llength [get_cells $member]] != 1} {error "Missing exact reference cell: $member"}
}

create_bound ref_completion_source -mode fixed -width 1 -height 1 -origin {22 19}
add_cells_to_bound -bound ref_completion_source -cells [list [lindex $members 0]]
create_bound ref_completion_release -mode fixed -width 1 -height 1 -origin {22 20}
add_cells_to_bound -bound ref_completion_release -cells [lrange $members 1 2]
export_adc -file applied_ref_completion_bound.adc
set fh [open applied_ref_completion_bound.adc r]; set adc [read $fh]; close $fh
foreach {name row} {ref_completion_source 19 ref_completion_release 20} {
 set pat [format {create_bound\s*\{\s*%s\s*\}\s*-mode fixed -width 1 -height 1 -origin\s*\{\s*22 %s\s*\}} $name $row]
 if {![regexp $pat $adc]} {error "Missing exact fixed reference bound $name"}
}
foreach member $members bound {ref_completion_source ref_completion_release ref_completion_release} {
 if {[string first "add_cells_to_bound -bound \{ $bound \} -cells \{ $member \}" $adc] < 0} {
  error "Missing exported bound member $member"
 }
}
puts "APPLIED_ORDERED_REF_COMPLETION_MEMBERS=$members"
report_param -detail -stage place -file applied_place_params.rpt
puts "SCREEN_ACTUAL_SEED=[get_param place seed] SCREEN_ACTUAL_MACRO=[get_param place macro_performance]"
place

export_db place.db
update_timing -mode manhattan
require_active_clocks
report_area -io_info -file place.area
report_timing_summary -file place.timing
report_qor -step place -file screen.qor
report_clock_summary -file place_clocks.rpt
report_timing_exception -file place_exceptions.timing
export_sdc -file place_applied.sdc
report_param -detail -stage place -file final_place_params.rpt

puts "BEGIN_NATIVE_PLACE_CONGESTION candidate=$candidate"
report_congestion -step place
puts "END_NATIVE_PLACE_CONGESTION candidate=$candidate"
if {[screen_file_binding $gate_db] ne $initial_gate_binding} {error "New gate.db changed during placement screening"}
foreach name {place.db place.area place.timing screen.qor place_clocks.rpt place_exceptions.timing place_applied.sdc} {
 if {![file isfile $name] || [file size $name] <= 0} {error "Missing placement screening output: $name"}
}
set fh [open screen.pass w]
puts $fh "PASS_PLACE_SCREEN_ONLY_NOT_ROUTED candidate=$candidate seed=$candidate_seed macro=$candidate_macro"
puts $fh "gate_binding=$initial_gate_binding"
close $fh
puts "BEGIN_LOCAL_POR_SCOPE"
foreach pattern {*S_rst_n* *S_power_ready* *startup_complete*} {
 foreach net [get_nets -hier -nowarn $pattern] {
  catch {report_property $net}
  catch {report_nets $net -connection -pin_display_limit 5}
 }
}
puts "END_LOCAL_POR_SCOPE"
puts "BEGIN_NATIVE_PREDECODE_SCOPE"
puts "LEGACY_MODE_COMPARATOR_CELLS=[get_cells -hier -nowarn *previous_application_mode*]"
puts "PREDECODE_SOURCE_NETS=[get_nets -hier -nowarn *flag_application_mode_changed*]"
puts "MODE_FRAME_FENCE_NETS=[get_nets -hier -nowarn *fence_mode_change*]"
foreach net [get_nets -hier -nowarn *fence_mode_change*] {
 catch {report_property $net}
 catch {report_nets $net -connection -pin_display_limit 4}
}
puts "END_NATIVE_PREDECODE_SCOPE"
puts "BEGIN_LOCAL_CLEAR_NATIVE_NETS"
set clear_nets [get_nets -hier -nowarn *stats_clear*]
puts "LOCAL_CLEAR_NETS=$clear_nets"
foreach net $clear_nets {
 if {[catch {report_property $net} diagnostic]} {puts "LOCAL_CLEAR_PROPERTY_UNAVAILABLE: $diagnostic"}
 if {[catch {report_nets $net -connection -pin_display_limit 4} diagnostic]} {puts "LOCAL_CLEAR_NET_REPORT_UNAVAILABLE: $diagnostic"}
}
puts "END_LOCAL_CLEAR_NATIVE_NETS"
puts "PASS_PLACE_SCREEN_ONLY_NOT_ROUTED candidate=$candidate seed=$candidate_seed macro=$candidate_macro"
exit


