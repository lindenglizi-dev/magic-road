



set project_root [file normalize [file join [file dirname [info script]] ../..]]
set output_dir [file normalize [file dirname [info script]]]
set checked_db "$project_root/build/route/checked.db"
set run_dir "$project_root/build/route"
set primary_db "$run_dir/primary_checked.db"
set routed_db "$run_dir/routed.db"
set place_db [file join $project_root scripts placement seed0_auto place.db]
set gate_db "$project_root/build/gate/gate.db"
set qualification_marker "$run_dir/qualification.pass"
proc require_nonempty {path} {
 if {![file isfile $path] || [file size $path] <= 0} {error "Required completed evidence missing or empty: $path"}
}
foreach path [list $checked_db $primary_db $routed_db $place_db $gate_db $qualification_marker] {require_nonempty $path}
set guard_handle [open $qualification_marker rb]
set qualification_text [read $guard_handle]
close $guard_handle
set qualification_lines [split $qualification_text "\n"]
if {[string trim [lindex $qualification_lines 0]] ne "PASS FULL_APPLICATION_TWO_VIEW_TIMING_QUALIFIED"} {
 error "Exact completed two-view qualification marker required; INCOMPLETE is not approval"
}
foreach fact {
 primary=primary_checked.db checked=checked.db primary_hold=native_related_clock
 primary_extra_minimum_removed=1 secondary_original_data_maximum_ns=7.000
 primary_constraint_state_restored=1 independent_source_pad_coverage_audit_required=1
} {
 if {[lsearch -exact $qualification_lines $fact] < 0} {error "Missing qualification fact: $fact"}
}
foreach pair [list [list $gate_db $place_db] [list $place_db $routed_db] [list $routed_db $primary_db] [list $primary_db $checked_db] [list $checked_db $qualification_marker]] {
 lassign $pair earlier later
 if {[file mtime $later] < [file mtime $earlier]} {error "Stale checkpoint/qualification chronology: $later older than $earlier"}
}

foreach name {
 candidate_flow.status
 qualification_primary.timing qualification_primary.ts qualification_primary_exceptions.timing
 qualification_primary_init8.timing qualification_primary_sys50_usr.timing qualification_primary_usr_sys50.timing qualification_primary_applied.sdc
 qualification_pure_data7.sdc qualification_pure_data7.timing qualification_pure_data7.ts qualification_pure_data7_exceptions.timing
 qualification_pure_data7_init8.timing qualification_pure_data7_sys50_usr.timing qualification_pure_data7_usr_sys50.timing qualification_pure_data7_applied.sdc
 qualification_restored_primary.sdc qualification_restored_primary_exceptions.timing qualification_restored_primary.timing qualification_restored_primary_sys50_usr.timing
} {
 set path "$run_dir/$name"
 require_nonempty $path
 if {[file mtime $path] < [file mtime $routed_db] || [file mtime $path] > [file mtime $checked_db]} {
  error "Report is outside this route-to-checked qualification window: $path"
 }
}
set guard_handle [open "$run_dir/candidate_flow.status" rb]
set flow_text [read $guard_handle]
close $guard_handle
if {![regexp {Timing Mode\s*:\s*final} $flow_text]} {error "Final routed flow status required"}
foreach kind {Setup Hold} {
 set expression [format {%s\s*: WNS\s+(-?[0-9]+)ps\s+TNS\s+(-?[0-9]+)ps\s+NUM_FEPS\s+([0-9]+)} $kind]
 if {![regexp $expression $flow_text unused wns tns failures] || $wns < 0 || $tns != 0 || $failures != 0} {
  error "Route flow status is not qualified: $kind"
 }
}
puts "CHECKED_AUDIT_INPUT=$checked_db QUALIFICATION=$qualification_marker"
set hardware_freeze [file join $project_root scripts scalar_gate_source_before.json]
if {![file isfile $hardware_freeze] || [file size $hardware_freeze] <= 0} {error "Lean pre-synthesis source freeze manifest is required"}
puts "CLOCK_AUDIT_HARDWARE_FREEZE=$hardware_freeze"

proc read_bytes {path} {
 set handle [open $path rb]
 set value [read $handle]
 close $handle
 return $value
}
proc require_one {objects label} {
 if {[llength $objects] != 1} {error "Expected exactly one $label, found: $objects"}
 return $objects
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


proc require_constraint_coverage {path} {
 set handle [open $path rb]; set text [read $handle]; close $handle
 if {![regexp {STA coverage\s*:\s*([0-9.]+)%} $text unused coverage] || $coverage < 98.66} {
  error "Timing coverage dropped below measured 98.66%: $path"
 }
 foreach {name expected} {
  {ETH_RX_CLK} 125.000
  {ETH_RX_FABRIC} 125.000
  {ETH_TX_CLK} 125.000
  {HDMI_PIXEL_CLK} 75.002
  {HDMI_SERIAL_CLK} 375.094
  {MIPI_RX_BYTE_CLK} 103.520
  {PHY_TX_CAPTURE} 125.000
  {mipi_rx_ck_pad} 414.079
  {pll_clk_100m} 100.000
  {pll_clk_24m} 23.810
  {sys_clk_50m} 50.000
  {u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.io_clk_pad_p} 414.079
  {u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.tif_c16_in} 103.520
  {u_ph1p35_324_ddr_wrapper/u_ddr2/ctl_clk} 133.333
  {u_ph1p35_324_ddr_wrapper/u_ddr2/ddr_clk} 533.333
  {u_ph1p35_324_ddr_wrapper/u_ddr2/mcu_clk} 50.795
  {u_ph1p35_324_ddr_wrapper/u_ddr2/ref_clk} 133.333
  {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk} 133.333
 } {
  set found 0
  foreach line [split $text "\n"] {
   if {[regexp {^\s*clk[0-9]+:\s+([0-9.]+)\s+[0-9]+\s+(\S+)\s*$} $line unused freq actual] && $actual eq $name} {
    if {abs($freq-$expected) > 0.001} {error "Clock frequency changed: $name=$freq, expected $expected"}
    incr found
   }
  }
  if {$found != 1} {error "Missing actual clock frequency: $name"}
 }
}

proc require_active_exceptions {path pure_data {reference {}}} {
 set handle [open $path rb]; set text [read $handle]; close $handle


 set summary [string range $text 0 [string first "Status of timing exceptions" $text]]
 if {[string first "set_min_delay" $summary] >= 0} {error "Unexpected minimum-delay override: $path"}
 set expected {
  {set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks {sys_clk_50m pll_clk_24m}] 9.000}
  {set_max_delay -datapath_only -from [get_clocks {sys_clk_50m pll_clk_24m}] -to [get_clocks MIPI_RX_BYTE_CLK] 9.000}
  {set_max_delay -datapath_only -from [get_clocks {MIPI_RX_BYTE_CLK pll_clk_24m HDMI_PIXEL_CLK}] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 7.000}
  {set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks {MIPI_RX_BYTE_CLK pll_clk_24m HDMI_PIXEL_CLK}] 7.000}
  {set_max_delay -datapath_only -from [get_clocks sys_clk_50m] -to [get_clocks ETH_TX_CLK] 6.000}
  {set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks sys_clk_50m] 6.000}
  {set_max_delay -datapath_only -from [get_clocks HDMI_PIXEL_CLK] -to [get_clocks ETH_TX_CLK] 7.000}
  {set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks HDMI_PIXEL_CLK] 7.000}
  {set_max_delay -datapath_only -from [get_clocks ETH_RX_FABRIC] -to [get_clocks ETH_TX_CLK] 7.000}
  {set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_RX_FABRIC] 7.000}
  {set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_RX_CLK] 7.000}
  {set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000}
  {set_max_delay -from [get_regs -nowarn {*/primary_addr_gray_reg[*]}] -to [get_regs -nowarn {*/sync_r1[*]}] -datapath_only 7.200}
  {set_max_delay -from [get_regs -nowarn {*/primary_addr_gray_reg[*]}] -to [get_regs -nowarn {*/sync_r1[*]}] -datapath_only 7.200}
 }
 if {$pure_data} {
  lappend expected {set_max_delay -datapath_only -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 7.000}
  lappend expected {set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks sys_clk_50m] 7.000}
 }
 set actual {}; set actual_commands {}
 foreach line [split $summary "\n"] {
  if {[regexp {^\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+(set_max_delay[^\r\n]*)} $line unused total dominated shadowed ignored command]} {
   set command [string trim $command]
   if {$command eq {set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000}} {
    if {$total != 0 || $dominated != 0 || $shadowed != 0 || $ignored != 0} {error "Byte RAM direct crossing unexpectedly returned: $line"}
   } elseif {$total <= 0 || $dominated <= 0 || $ignored != 0 || $total != $dominated+$shadowed} {error "Empty or ignored active exception: $line"}
   lappend actual [list $total $dominated $shadowed $ignored $command]
   lappend actual_commands $command
  }
 }
 if {[lsort $actual_commands] ne [lsort $expected]} {error "Active exception command set changed: $actual_commands"}
 if {$reference ne {} && [lsort $actual] ne [lsort $reference]} {error "Active exception counts changed from this physical checkpoint's frozen baseline: $actual"}
 puts "VERIFIED_ACTIVE_MAXIMUM_EXCEPTIONS=[llength $actual] COUNTS=$actual"
 return $actual
}

import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db $checked_db

clear_sdc -user
read_sdc "$project_root/td_project/camera_to_dsi_display.sdc"
read_sdc -ip ddr2 "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc"
read_sdc -ip w128_d512_fifo "$project_root/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl"
cd $output_dir
reset_path_margin -all
update_timing -mode final
require_active_clocks
foreach clock_object [get_clocks *] {report_property $clock_object}

report_path_margin
report_timing_status -file checked_clock_status.timing
report_timing_summary -file checked_clock_summary.timing
set summary [read_bytes checked_clock_summary.timing]
if {[string first {Confidence          : Routed} $summary] < 0} {error "Clock audit requires Routed timing confidence"}
require_constraint_coverage checked_clock_summary.timing
set checkpoint_exception_report "$project_root/build/route/frozen_placed_exceptions.timing"
if {![file isfile $checkpoint_exception_report]} {error "Current checkpoint native exception-count baseline is required"}
set checkpoint_counts [require_active_exceptions $checkpoint_exception_report 0]



check_timing -verbose -file checked_clock_checks.rpt
report_clock_utilization -file checked_clock_utilization.rpt
report_clock_summary -file checked_clock_groups.rpt -levels 20 -expand_buckets

set pll_rows [list \
 [list main pll_clk_100m \
  {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL} \
  {u_PLL/bufg_feedback}] \
 [list ethernet ETH_TX_CLK \
  {u_ethernet/u_eth_pll/ph1p_phy_pll_wrapper_d2616deaaa79_Inst/u_PH1P_PHY_PLL} \
  {u_ethernet/u_eth_pll/bufg_feedback}] \
 [list ddr_user {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk} \
  {u_ph1p35_324_ddr_wrapper/u_ddr2/ph1p_ddrmc_wrapper/ph1p_ddrmc_top/u_ddr_phy/u_ddrphy_top/u_ddrphy_clk/u_pll1/u_pll_inst} \
  {u_ph1p35_324_ddr_wrapper/u_ddr2/ph1p_ddrmc_wrapper/ph1p_ddrmc_top/u_ddr_phy/u_ddrphy_top/u_ddrphy_clk/u_pll1/u_bufg_fbclk}]]
foreach row $pll_rows {
 lassign $row label clock_name pll_name bufg_name
 puts "BEGIN_CHECKED_PLL_FEEDBACK $label"
 set target_clock [require_one [get_clocks $clock_name] "$label clock"]
 set target_pll [require_one [get_cells $pll_name] "$label PLL"]
 set target_bufg [require_one [get_cells $bufg_name] "$label BUFG"]
 set feedback_pin [require_one [get_pins "$pll_name.fbclk"] "$label feedback pin"]
 set buffer_pin [require_one [get_pins "$bufg_name.clkout"] "$label BUFG output"]
 set feedback_net [require_one [get_nets -of $feedback_pin] "$label feedback net"]
 set buffer_net [require_one [get_nets -of $buffer_pin] "$label BUFG output net"]
 puts "READBACK_FEEDBACK_BRANCH label=$label feedback_net=$feedback_net buffer_net=$buffer_net; graph review required"
 report_nets $buffer_net -connection -pin_display_limit 16 -mode final -timing -hold
 puts "PLL_FEEDBACK_CONNECTION label=$label clock=$target_clock sink=$feedback_pin bufg=$target_bufg net=$feedback_net"
 report_property $feedback_pin
 report_property $feedback_net

 report_nets $feedback_net
 report_nets $feedback_net -connection -pin_display_limit 12 -mode final -timing -hold
 report_cells $target_pll -connection -pin_loc -mode final -timing -hold
 report_cells $target_bufg -connection -pin_loc -mode final -timing -hold

 report_clock_summary -file "checked_clock_${label}_tree.rpt" -clocks $target_clock -levels 20 -expand_buckets
 puts "END_CHECKED_PLL_FEEDBACK $label"
}



set rx_ports [get_ports {I_a_rgmii_rxd[*] I_a_rgmii_rx_ctl}]
set tx_ports [get_ports {O_a_rgmii_txd[*] O_a_rgmii_tx_ctl}]
if {[llength $rx_ports] != 5 || [llength $tx_ports] != 5} {error "RGMII requires five RX and five TX data/control pads"}
foreach corner {slow fast} {
 update_timing -mode final -check_corner $corner
 report_timing_path -from $rx_ports -to [get_clocks ETH_RX_CLK] -ep_num 64 -path_num 4 -file "checked_rgmii_rx_${corner}.timing"
 report_timing_path -from [get_clocks ETH_TX_CLK] -to $tx_ports -ep_num 64 -path_num 4 -file "checked_rgmii_tx_${corner}.timing"
}
update_timing -mode final
report_timing_status -file checked_restored_both_status.timing


write_verilog -implement "$output_dir/actual_checked.v"

report_timing_exception -ep_num 512 -path_num 1 -file checked_exceptions.timing
require_active_exceptions checked_exceptions.timing 0 $checkpoint_counts

report_timing_path -from [get_clocks sys_clk_50m] -to [get_clocks pll_clk_24m] -ep_num 512 -path_num 1 -file checked_sys50_ref24.timing
report_timing_path -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 512 -path_num 1 -file checked_sys50_usr.timing
report_timing_path -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks sys_clk_50m] -ep_num 512 -path_num 1 -file checked_usr_sys50.timing

set private_completion_regs [get_regs {u_power_on_reset/O_ref_startup_complete}]
if {[llength $private_completion_regs] == 0} {
 set private_completion_regs [get_regs {u_power_on_reset/ref_startup_complete}]
}
set private_completion_regs [require_one $private_completion_regs {private reference completion register}]
set completion_regs [require_one [get_regs {u_power_on_reset/startup_complete}] {original completion register}]
set ref_release_regs [get_regs {*S_ref_reset_release*}]
set ddr_release_regs [get_regs {*S_ddr_reset_release*}]
if {[llength $ref_release_regs] == 0 || [llength $ddr_release_regs] == 0} {error "Actual reset release registers are required"}
puts "REF_LOCAL_PATH_OBJECTS original=$completion_regs private=$private_completion_regs ref=$ref_release_regs ddr=$ddr_release_regs"
report_timing_path -from $private_completion_regs -to $ref_release_regs -ep_num 32 -path_num 1 -file checked_completion_ref.timing
report_timing_path -from $completion_regs -to $ddr_release_regs -ep_num 32 -path_num 1 -file checked_completion_ddr.timing
report_timing_path -from [get_regs {*u_ddrphy_fiu_wrapper/init_wsl[*]}] -to [get_regs {*u_ddrphy_fiu_wrapper/init_wsl_r[*]}] -ep_num 32 -path_num 1 -file checked_init8.timing
report_timing_path -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks MIPI_RX_BYTE_CLK] -ep_num 50 -path_num 1 -file checked_internal_mipi.timing
report_timing_path -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 50 -path_num 1 -file checked_internal_ddr.timing
report_timing_path -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_TX_CLK] -ep_num 50 -path_num 1 -file checked_internal_eth.timing
report_route_status -drc -file checked_drc.rpt
export_sdc -file actual_checked.sdc
export_adc -file actual_checked.adc
require_active_clocks
puts CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED
puts {REVIEW_REQUIRED: all three actual .fbclk branches GLOBAL_NETWORK; zero PLL frequency mismatch; zero USR-6135 in the full CLI log; actual private-reference/original-DDR setup/hold and four release FF initialization mapping.}
puts {Inspect the native expanded clock topology and available skew evidence; this export is not timing qualification.}
exit


