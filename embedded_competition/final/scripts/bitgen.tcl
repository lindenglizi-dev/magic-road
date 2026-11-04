source [file join [file dirname [info script]] source_counts.tcl]

set project_root [file normalize [file join [file dirname [info script]] ..]]
set execution_root [file normalize [file dirname [info script]]]
set run_dir "$project_root/build/route"
set checked_db "$run_dir/checked.db"
if {![file isfile $checked_db] || [file size $checked_db] == 0} {
 error "Missing qualified checked.db; complete route and qualify_timing.tcl first"
}
foreach name {qualification.pass candidate_flow.status} {
 set path "$run_dir/$name"
 if {![file isfile $path]} {error "Missing $name"}
 set handle [open $path r]
 set reports($name) [read $handle]
 close $handle
}
set marker [string trim [lindex [split $reports(qualification.pass) "\n"] 0]]
if {$marker ne "PASS FULL_APPLICATION_TWO_VIEW_TIMING_QUALIFIED"} {
 error "Both timing views have not qualified"
}
if {[file mtime "$run_dir/qualification.pass"] < [file mtime $checked_db]} {
 error "Qualification marker is older than checked.db"
}
set status $reports(candidate_flow.status)
if {![regexp {Timing Mode\s*:\s*final} $status]} {error "Final routed timing mode required"}
foreach kind {Setup Hold} {
 set expression [format {%s\s*: WNS\s+(-?[0-9]+)ps\s+TNS\s+(-?[0-9]+)ps\s+NUM_FEPS\s+([0-9]+)} $kind]
 if {![regexp $expression $status unused wns tns failures] || $wns < 0 || $tns != 0 || $failures != 0} {
  error "Timing qualification failed: $kind"
 }
}

proc audit_file_binding {path} {
 if {![file isfile $path]} {error "Audit bound file missing: $path"}
 set handle [open $path rb]
 set checksum 0
 while {![eof $handle]} {set checksum [zlib crc32 [read $handle 1048576] $checksum]}
 close $handle
 return [list size [file size $path] crc32 [format %08x $checksum]]
}
proc audit_check_binding {binding expected_path label} {
 foreach key {path size crc32} {
  if {![dict exists $binding $key]} {error "Incomplete audit binding: $label/$key"}
 }
 set path [dict get $binding path]
 if {$expected_path ne "" && [file normalize $path] ne [file normalize $expected_path]} {error "Wrong audit bound path: $label"}
 set actual [audit_file_binding $path]
 if {[dict get $binding size] ne [dict get $actual size] || [dict get $binding crc32] ne [dict get $actual crc32]} {error "Audit bound file changed: $label"}
}
proc require_independent_audit {receipt checked_db primary_sdc} {
 global project_root execution_root
 if {![file isfile $receipt]} {error "Missing independent audit receipt"}
 set handle [open $receipt rb];set text [read $handle];close $handle
 set first_newline [string first "\n" $text]
 if {$first_newline < 0 || [string trim [string range $text 0 [expr {$first_newline-1}]]] ne "PASS FULL_APPLICATION_INDEPENDENT_AUDIT"} {error "Independent audit success marker missing"}
 set audit [string trim [string range $text [expr {$first_newline+1}] end]]
 if {[catch {dict size $audit}]} {error "Malformed independent audit dictionary"}
 foreach key {version reviewer result unresolved_findings checks checked_db primary_sdc reports input_bindings script_bindings flow_bindings} {
  if {![dict exists $audit $key]} {error "Missing independent audit field: $key"}
 }
 if {[dict get $audit version] ne "1" || [dict get $audit result] ne "PASS" || [string trim [dict get $audit reviewer]] eq "" || [dict get $audit unresolved_findings] ne "0"} {error "Independent audit is not explicitly approved without unresolved findings"}
 foreach kind {source_freeze drc pad clock coverage} {
  if {![dict exists $audit checks $kind] || [dict get $audit checks $kind] ne "PASS"} {error "Independent audit did not pass: $kind"}
  if {![dict exists $audit reports $kind]} {error "Missing independent audit report: $kind"}
  set report [dict get $audit reports $kind]
  if {![dict exists $report size] || [dict get $report size] <= 0} {error "Audit report missing or empty: $kind"}
  audit_check_binding $report "" "report/$kind"
 }
 audit_check_binding [dict get $audit checked_db] $checked_db checked_db
 audit_check_binding [dict get $audit primary_sdc] $primary_sdc primary_sdc
 set bound_paths {}
 foreach {kind count} [list input_bindings $release_input_count script_bindings $release_script_count] {
  set bindings [dict get $audit $kind]
  if {[dict size $bindings] != $count} {error "Incomplete reviewed source coverage: $kind"}
  dict for {relative binding} $bindings {
   if {[file pathtype $relative] ne "relative"} {error "Audit source key is not relative: $relative"}
   set expected [file normalize [file join $project_root $relative]]
   if {[string first "[file normalize $project_root]/" $expected] != 0 || [lsearch -exact $bound_paths $expected] >= 0} {error "Audit source path escapes ROOT or is duplicated: $relative"}
   audit_check_binding $binding $expected "$kind/$relative"
   lappend bound_paths $expected
  }
 }


 set expected_flow_files $release_flow_files
 set flow_bindings [dict get $audit flow_bindings]
 if {[lsort [dict keys $flow_bindings]] ne [lsort $expected_flow_files]} {error "Incomplete actual execution-flow binding set"}
 dict for {relative binding} $flow_bindings {
  set expected [file normalize [file join $execution_root $relative]]
  if {[file pathtype $relative] ne "relative" || [string first "[file normalize $execution_root]/" $expected] != 0} {error "Flow binding path escapes execution root"}
  audit_check_binding $binding $expected "flow/$relative"
 }
 puts "PASS_INDEPENDENT_AUDIT_RECEIPT_BOUND_TO_CHECKED_DB_SDC_AND_REPORTS"
}

require_independent_audit "$run_dir/independent_audit.receipt" $checked_db "$project_root/td_project/camera_to_dsi_display.sdc"
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
cd "$project_root/td_project"
open_project "$project_root/td_project/ball_face.al" -noanalyze
import_db $checked_db
cd $run_dir
file mkdir "$project_root/output/rebuilt"
commit_param -step bitgen
set pending_bit "$project_root/output/rebuilt/ball_face_ethernet.pending_[pid]_[clock microseconds].bit"
bitgen -bit $pending_bit
export_bitgen_param -file bitgen_parameters.txt
if {![file isfile $pending_bit] || [file size $pending_bit] == 0} {
 error "Native bitgen did not produce a new bitstream"
}
set output_bit "$project_root/output/rebuilt/ball_algorithm_rebuilt.bit"
if {[file exists $output_bit]} {error "输出已存在，请使用新的构建副本"}
file rename $pending_bit $output_bit
puts PASS_FULL_APPLICATION_ETHERNET_BITSTREAM_GENERATED
exit
