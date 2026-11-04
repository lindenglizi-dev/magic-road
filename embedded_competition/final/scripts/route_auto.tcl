set script_root [file normalize [file dirname [info script]]]
source [file join $script_root placement current_binding.tcl]
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
set project_root [file normalize [file join [file dirname [info script]] ..]]
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db "$project_root/scripts/placement/seed0_auto/place.db"


clear_sdc -user
read_sdc "$project_root/td_project/camera_to_dsi_display.sdc"
read_sdc -ip ddr2 "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc"
read_sdc -ip w128_d512_fifo "$project_root/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl"
reset_path_margin -all


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
  sys_clk_50m 50.000 pll_clk_100m 100.000 pll_clk_24m 23.810
  MIPI_RX_BYTE_CLK 103.520 ETH_TX_CLK 125.000 ETH_RX_CLK 125.000
  ETH_RX_FABRIC 125.000 PHY_TX_CAPTURE 125.000 HDMI_PIXEL_CLK 75.002
  HDMI_SERIAL_CLK 375.094 u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk 133.333
  u_ph1p35_324_ddr_wrapper/u_ddr2/ctl_clk 133.333
  u_ph1p35_324_ddr_wrapper/u_ddr2/ddr_clk 533.333
  u_ph1p35_324_ddr_wrapper/u_ddr2/mcu_clk 50.795
  u_ph1p35_324_ddr_wrapper/u_ddr2/ref_clk 133.333
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
  if {$reference ne {}} {
   lappend reference [list 116 116 0 0 [lindex $expected end-1]]
   lappend reference [list 1 1 0 0 [lindex $expected end]]
  }
 }
 set actual {}; set actual_commands {}
 foreach line [split $summary "\n"] {
  if {[regexp {^\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+(set_max_delay[^\r\n]*)} $line unused total dominated shadowed ignored command]} {
   set command [string trim $command]


   if {$command eq {set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000}} {
    if {$total != 0 || $dominated != 0 || $shadowed != 0 || $ignored != 0} {error "Byte RAM direct crossing unexpectedly returned: $line"}
    puts "VERIFIED_BYTE_RAM_REMOVED_DIRECT_MIPI_ETH_PATH=0"
   } elseif {$total <= 0 || $dominated <= 0 || $ignored != 0 || $total != $dominated+$shadowed} {error "Empty or ignored active exception: $line"}
   if {[string first "primary_addr_gray_reg" $command] >= 0 && ($total != 18 || $dominated != 18 || $shadowed != 0)} {error "Vendor Gray exception endpoint coverage changed: $line"}
   lappend actual [list $total $dominated $shadowed $ignored $command]
   lappend actual_commands $command
  }
 }
 if {[lsort $actual_commands] ne [lsort $expected]} {error "Active exception command set changed: $actual_commands"}
 if {$reference ne {} && [lsort $actual] ne [lsort $reference]} {error "Active exception counts changed from this physical checkpoint's frozen baseline: $actual"}
 puts "VERIFIED_ACTIVE_MAXIMUM_EXCEPTIONS=[llength $actual] COUNTS=$actual"
 return $actual
}

update_timing -mode manhattan
require_active_clocks
file mkdir "$project_root/build/route"
cd "$project_root/build/route"
report_timing_exception -file frozen_placed_exceptions.timing
set constraint_counts [require_active_exceptions frozen_placed_exceptions.timing 0]
commit_param -step route
set_param flow thread 8
puts "Vendor-default route timing=[get_param route timing]"
set_param route effort normal
set_param route timing on
report_param -detail -stage route -file applied_route_params.rpt
set parameter_handle [open applied_route_params.rpt r]
set parameter_text [read $parameter_handle]
close $parameter_handle
if {![regexp {effort[ \t]*\|[ \t]*normal[ \t]*\|} $parameter_text]} {error "Live DB normal effort not applied"}
set_param route fix_hold on
set_param route post_route_opt on
set_param route postrt_opt_extra_round 4

report_param -detail -stage route -file final_applied_route_params.rpt
set route_error [catch {route} route_message]
if {$route_error} {
 export_db diagnostic_partial.db
 catch {update_timing -mode final}
 catch {report_timing_summary -file partial_original.timing}
 catch {report_timing_path -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks MIPI_RX_BYTE_CLK] -ep_num 50 -path_num 1 -file partial_mipi.timing}
 catch {report_timing_path -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_TX_CLK] -ep_num 50 -path_num 1 -file partial_eth.timing}
 puts "SAVED_PARTIAL_DIAGNOSTIC_NOT_SIGNOFF: $route_message"
 exit 2
}

export_db routed.db
update_timing -mode final


require_active_clocks
report_path_margin
report_timing_summary -file candidate_final.timing
report_timing_path -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks MIPI_RX_BYTE_CLK] -ep_num 50 -path_num 1 -file worst_mipi.timing
report_timing_path -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_TX_CLK] -ep_num 50 -path_num 1 -file worst_eth.timing
report_timing_path -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 50 -path_num 1 -file worst_ddr.timing

report_timing_status -file candidate_final.ts
report_timing_exception -file candidate_exception.timing
require_active_exceptions candidate_exception.timing 0 $constraint_counts
report_timing_ignored -file candidate_ignored.timing
report_area -io_info -file candidate_final.area
check_timing -verbose -file candidate_coverage.rpt
report_clock_summary -file candidate_clocks.rpt
report_clock_utilization -file candidate_clock_utilization.rpt
report_route_status -drc -file candidate_drc.rpt
report_abnormal_timing_target -file candidate_abnormal.rpt
flow_status -file candidate_flow.status
analyze_clock -detail
export_sdc -file candidate_applied.sdc
require_constraint_coverage candidate_final.timing
set handle [open candidate_final.timing r]
set timing_text [read $handle]
close $handle
foreach kind {SWNS HWNS STNS HTNS} {
    if {![regexp [format {%s:\s*(-?[0-9.]+)ns} $kind] $timing_text unused slack] || $slack < 0} {
        error "Full application original-constraint $kind failed; no checked DB or bit generated"
    }
}
export_db primary_checked.db
puts "PASS FULL_APPLICATION_PRIMARY_SDC_SIGNOFF; same physical DB pure-data7ns audit and independent source/pad/coverage audit required before final qualification"
exit





