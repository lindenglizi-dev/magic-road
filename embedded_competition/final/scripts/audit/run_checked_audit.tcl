if {[catch {source [file join [file dirname [info script]] checked_clock_audit.tcl]} reason options]} {
 puts "FAIL_NATIVE_CURRENT_CHECKED_EXPORT: $reason"
 puts [dict get $options -errorinfo]
 exit
}
