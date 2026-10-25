# Read-only tool option discovery. No project or design mutation.
foreach command {{report_param -all -detail -file td_parameters.rpt}} {
    puts "QUERY $command"
    if {[catch {eval $command} result]} {puts "QUERY_ERROR $result"} else {puts $result}
}
