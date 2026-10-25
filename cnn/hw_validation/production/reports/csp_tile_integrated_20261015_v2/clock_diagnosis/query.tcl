import_device ph1_35p.db -package PH1P35MDG324 -speed 3
import_db ../synthesis/gate.db
update_timing
puts "PROBE_CLOCK_COUNT=[llength [get_clocks *]]"
puts "PROBE_CLOCKS=[get_clocks *]"
puts "PROBE_PORTS=[llength [get_ports *]]"
puts "PROBE_REGS=[llength [get_regs -hier *]]"
report_timing_summary -file imported_gate.timing
check_timing -verbose -file imported_gate_check.rpt
export_sdc -file imported_gate.sdc
puts "CLOCK_DIAGNOSIS_COMPLETE"
exit
