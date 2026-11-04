


set project_root [file normalize [file join [file dirname [info script]] ..]]
set run_dir "$project_root/build/route"
set primary_sdc "$project_root/td_project/camera_to_dsi_display.sdc"
set primary_db "$run_dir/primary_checked.db"
if {![file isfile $primary_db]} {error "Missing completed primary_checked.db"}

proc read_bytes {path} {
 set handle [open $path rb]
 set value [read $handle]
 close $handle
 return $value
}
proc save_bytes {path value} {
 set handle [open $path wb]
 puts -nonewline $handle $value
 close $handle
}
proc require {condition message} {
 if {![uplevel 1 [list expr $condition]]} {error $message}
}
proc cold_import_constraints {path} {
 global project_root primary_db

 import_db $primary_db
 clear_sdc -user
 read_sdc $path
 read_sdc -ip ddr2 "$project_root/user_source/hdl_source/ph1p35_ddr/ddr2/src/sdc/ddr2.sdc"
 read_sdc -ip w128_d512_fifo "$project_root/user_source/ip_source/w128_d512_fifo/w128_d512_fifo.tcl"
 reset_path_margin -all
 update_timing -mode final
 report_path_margin
 require_active_clocks
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

proc require_global {path check_hold} {
 require_constraint_coverage $path
 set text [read_bytes $path]
 require {[string first "Confidence          : Routed" $text] >= 0} "STA is not Routed"
 require {[string first "Both (Slow and Fast)" $text] >= 0} "Both timing corners required"
 set kinds {SWNS STNS}
 if {$check_hold} {set kinds {SWNS STNS HWNS HTNS}}
 foreach kind $kinds {
  if {![regexp [format {%s:\s*(-?[0-9.]+)ns} $kind] $text unused value]} {error "Missing global $kind"}
  require {$value >= 0} "Global $kind failed"
  if {$kind == "STNS" || $kind == "HTNS"} {require {$value == 0} "Global total negative slack is not zero"}
 }
 set kinds {Max}
 if {$check_hold} {lappend kinds Min}
 foreach kind $kinds {
  set matches [regexp -all -inline [format {(?m)^%s\s*:[^\n]*?([0-9]+) Viol Endpoints} $kind] $text]
  require {[llength $matches] > 0} "No $kind endpoint statistics"
  foreach {whole count} $matches {require {$count == 0} "STA has failing endpoints"}
 }
}
proc require_pair {path max_count min_count pure_data {minimum_budget 0.000}} {
 set text [read_bytes $path]
 set actual_counts {}
 set statistics_groups -1
 foreach {kind expected} [list Max $max_count Min $min_count] {
  set pattern [format {(?m)^%s\s*:[^\n]*?([0-9]+) Viol Endpoints,\s*([0-9]+) Total Endpoints,\s*([0-9]+) Paths Analyzed} $kind]
  set matches [regexp -all -inline $pattern $text]
  require {[llength $matches] > 0} "Missing $kind path statistics: $path"
  set group_count [expr {[llength $matches]/4}]
  if {$statistics_groups < 0} {set statistics_groups $group_count}
  require {$group_count == $statistics_groups} "Mismatched maximum/minimum statistics groups: $path"
  set count 0
  foreach {whole violations endpoints paths} $matches {
   require {$violations == 0 && $endpoints == $paths} "Incomplete or failing $kind endpoint/path count: $path"
   incr count $paths
  }
  if {$expected >= 0} {
   require {$count == $expected} "Unexpected exact $kind endpoint count: $path"
  } else {
   require {$count > 0} "Empty whole-pair $kind endpoint set: $path"
  }
  dict set actual_counts $kind $count
 }
 set max_budgets {}; set min_budgets {}; set max_skews {}; set max_endpoints {}; set min_endpoints {}
 set section {}; set max_sections 0; set min_sections 0
 foreach line [split $text "\n"] {
  set line [string trimright $line "\r"]
  if {[regexp {^Path Group\s*:} $line]} {set section {}}
  if {$line == "Max Paths"} {set section Max; incr max_sections}
  if {$line == "Min Paths"} {set section Min; incr min_sections}
  if {[regexp {^Budget\s*:\s*(-?[0-9.]+)ns} $line unused value]} {
   if {$section == "Max"} {lappend max_budgets $value}
   if {$section == "Min"} {lappend min_budgets $value}
  }
  if {$section == "Max" && [regexp {^Clock Skew\s*:\s*(-?[0-9.]+)ns} $line unused value]} {lappend max_skews $value}
  if {$section == "Max" && [regexp {^End Point\s*:\s*(\S+)} $line unused endpoint]} {lappend max_endpoints $endpoint}
  if {$section == "Min" && [regexp {^End Point\s*:\s*(\S+)} $line unused endpoint]} {lappend min_endpoints $endpoint}
 }
 set max_actual [dict get $actual_counts Max]
 set min_actual [dict get $actual_counts Min]
 require {$max_sections == $statistics_groups && $min_sections == $statistics_groups} "Incomplete maximum/minimum path sections: $path"
 require {[llength $max_budgets] == $max_actual && [llength $min_budgets] == $min_actual} "Incomplete maximum/minimum path budgets: $path"
 set max_endpoints [lsort -unique $max_endpoints]
 set min_endpoints [lsort -unique $min_endpoints]
 require {[llength $max_endpoints] == $max_actual} "Incomplete maximum endpoint identities: $path"
 require {[llength $min_endpoints] == $min_actual} "Incomplete minimum endpoint identities: $path"
 if {$min_count < 0} {require {$min_actual == $max_actual} "Whole-pair minimum/maximum endpoint counts differ: $path"}
 dict set actual_counts MaxEndpoints $max_endpoints
 dict set actual_counts MinEndpoints $min_endpoints
 if {$pure_data} {
  foreach value $max_budgets {require {$value == 7.000} "Maximum budget changed from 7ns: $path"}
  require {[llength $max_skews] == $max_actual} "Incomplete pure-data skew evidence: $path"
  foreach value $max_skews {require {$value == 0} "Pure-data view includes clock skew: $path"}
 } else {
  require {$min_endpoints == $max_endpoints} "Primary minimum/maximum endpoint identities differ: $path"
  require {[string first "set_max_delay" $text] < 0} "Primary related setup is overridden by a maximum exception: $path"
  foreach value $max_budgets {require {$value > 0} "Primary related setup has no positive edge budget: $path"}
  if {$minimum_budget != ""} {
   foreach value $min_budgets {require {$value == $minimum_budget} "Minimum budget changed from $minimum_budget ns: $path"}
  }
 }
 puts "QUALIFIED_PATH_COUNTS file=$path max_paths=$max_actual min_paths=$min_actual groups=$statistics_groups"
 return $actual_counts
}

cd $run_dir

save_bytes qualification.pass "INCOMPLETE\n"
foreach path {qualification_primary.timing qualification_primary.ts qualification_primary_exceptions.timing qualification_primary_init8.timing qualification_primary_sys50_usr.timing qualification_primary_usr_sys50.timing qualification_pure_data7.timing qualification_pure_data7.ts qualification_pure_data7_exceptions.timing qualification_pure_data7_init8.timing qualification_pure_data7_sys50_usr.timing qualification_pure_data7_usr_sys50.timing} {
 save_bytes $path ""
}
set original_sdc [read_bytes $primary_sdc]
set normal_max {set_max_delay -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 7.000}
require {[string first $normal_max $original_sdc] < 0} "Primary related setup must not be widened to ordinary max7"
require {![regexp -line {^[ \t]*set_min_delay} $original_sdc]} "Primary SDC must retain native hold without a minimum-delay override"
set pure_max {set_max_delay -datapath_only -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 7.000}
set reverse_pure_max {set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks sys_clk_50m] 7.000}
set secondary_sdc "$run_dir/qualification_pure_data7.sdc"
save_bytes $secondary_sdc "$original_sdc\n$pure_max\n$reverse_pure_max\n"

import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
cd $run_dir
set constraint_counts [require_active_exceptions candidate_exception.timing 0]
cold_import_constraints $primary_sdc
report_timing_summary -file qualification_primary.timing
report_timing_status -file qualification_primary.ts
report_timing_exception -file qualification_primary_exceptions.timing
require_active_exceptions qualification_primary_exceptions.timing 0 $constraint_counts
report_timing_path -from [get_regs {*u_ddrphy_fiu_wrapper/init_wsl[*]}] -to [get_regs {*u_ddrphy_fiu_wrapper/init_wsl_r[*]}] -ep_num 32 -path_num 1 -file qualification_primary_init8.timing
report_timing_path -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 512 -path_num 1 -file qualification_primary_sys50_usr.timing
report_timing_path -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks sys_clk_50m] -ep_num 512 -path_num 1 -file qualification_primary_usr_sys50.timing
export_sdc -file qualification_primary_applied.sdc
require_global qualification_primary.timing 1
set exceptions [read_bytes qualification_primary_exceptions.timing]
require {[string first "set_min_delay" $exceptions] < 0} "Unexpected minimum-delay exception; real hold must remain active"
require_pair qualification_primary_init8.timing 8 8 0
set primary_counts [require_pair qualification_primary_sys50_usr.timing 116 116 0]

set primary_reverse_text [read_bytes qualification_primary_usr_sys50.timing]
set primary_reverse_counts [require_pair qualification_primary_usr_sys50.timing -1 -1 0 ""]
set primary_reverse_endpoints [dict get $primary_reverse_counts MaxEndpoints]
puts "QUALIFIED_REVERSE_PRIMARY_COUNTS max_paths=[dict get $primary_reverse_counts Max] min_paths=[dict get $primary_reverse_counts Min]"
puts PASS_PRIMARY_TIMING_WINDOW_QUALIFIED



cold_import_constraints $secondary_sdc
report_timing_summary -file qualification_pure_data7.timing
report_timing_status -file qualification_pure_data7.ts
report_timing_exception -file qualification_pure_data7_exceptions.timing
require_active_exceptions qualification_pure_data7_exceptions.timing 1 $constraint_counts
report_timing_path -from [get_regs {*u_ddrphy_fiu_wrapper/init_wsl[*]}] -to [get_regs {*u_ddrphy_fiu_wrapper/init_wsl_r[*]}] -ep_num 32 -path_num 1 -file qualification_pure_data7_init8.timing
report_timing_path -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 512 -path_num 1 -file qualification_pure_data7_sys50_usr.timing
report_timing_path -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks sys_clk_50m] -ep_num 512 -path_num 1 -file qualification_pure_data7_usr_sys50.timing
export_sdc -file qualification_pure_data7_applied.sdc
require_global qualification_pure_data7.timing 0
require_pair qualification_pure_data7_init8.timing 8 0 1
set secondary_counts [require_pair qualification_pure_data7_sys50_usr.timing -1 0 1]
require {[dict get $secondary_counts Max] == [dict get $primary_counts Max]} "Whole-pair maximum endpoint coverage changed between views"
require {[dict get $secondary_counts MaxEndpoints] == [dict get $primary_counts MaxEndpoints]} "Whole-pair maximum endpoint identities changed between views"
set secondary_reverse_counts [require_pair qualification_pure_data7_usr_sys50.timing -1 0 1]
require {[dict get $secondary_reverse_counts Max] == [dict get $primary_reverse_counts Max]} "Reverse maximum endpoint coverage changed between views"
set secondary_reverse_endpoints [dict get $secondary_reverse_counts MaxEndpoints]
require {$secondary_reverse_endpoints == $primary_reverse_endpoints} "Reverse maximum endpoint identities changed between views"
puts PASS_ORIGINAL_PURE_DATA7_BOUND_QUALIFIED

require {[read_bytes $primary_sdc] == $original_sdc} "Production SDC changed during qualification"
cold_import_constraints $primary_sdc
export_sdc -file qualification_restored_primary.sdc
report_timing_exception -file qualification_restored_primary_exceptions.timing
require_active_exceptions qualification_restored_primary_exceptions.timing 0 $constraint_counts
report_timing_summary -file qualification_restored_primary.timing
require_global qualification_restored_primary.timing 1
report_timing_path -from [get_clocks sys_clk_50m] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -ep_num 512 -path_num 1 -file qualification_restored_primary_sys50_usr.timing
require_pair qualification_restored_primary_sys50_usr.timing 116 116 0
set pending_db "$run_dir/checked.pending_[pid]_[clock microseconds].db"
export_db $pending_db
require {[file isfile $pending_db] && [file size $pending_db] > 0} "Native export did not produce a new database"
file rename -force $pending_db "$run_dir/checked.db"
save_bytes qualification.pass "PASS FULL_APPLICATION_TWO_VIEW_TIMING_QUALIFIED\nprimary=primary_checked.db\nchecked=checked.db\nprimary_hold=native_related_clock\nprimary_extra_minimum_removed=1\nsecondary_original_data_maximum_ns=7.000\nprimary_constraint_state_restored=1\nindependent_source_pad_coverage_audit_required=1\n"
puts PASS_DUAL_VIEW_TIMING_QUALIFIED_NO_BITGEN
exit


