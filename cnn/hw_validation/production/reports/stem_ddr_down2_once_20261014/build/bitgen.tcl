# Temporary SRAM/JTAG diagnostic only. No programming/download command.
import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_stem_ddr_board_top.al -single_run
import_db pr.db
update_timing -mode final
report_timing_status -file imported.ts
report_timing_summary -ep_num 100000 -path_num 1 -file imported.timing
check_timing -verbose -file check_timing.rpt
set fh [open imported.ts r]
set status [read $fh]
close $fh
if {[regexp {(SWNS|HWNS): -[0-9]} $status]} {error "Imported database has timing violation"}
set fh [open check_timing.rpt r]
set checks [read $fh]
close $fh
if {![string match {*checking invalid constraint(0)*} $checks]} {error "Imported constraints invalid"}
set fh [open paxi_connectivity.tsv w]
puts $fh "logical\tcanonical_net\tdriver\tsinks"
set signals {}
foreach name {wdata rdata} {
    for {set bit 0} {$bit < 128} {incr bit} {lappend signals [format {%s[%d]} $name $bit]}
}
foreach name $signals {
    # Synthesis folds control expressions across hierarchy; top wire aliases
    # are not guaranteed objects. These retained full data buses are explicit
    # in routed_netlist.v. Control semantics remain bound to frozen RTL/tests.
    if {[string match {rdata*} $name]} {
        set logical "u_mailbox/i_$name"
    } else {
        set logical "u_ddr2/ph1p_ddrmc_wrapper/ph1p_ddrmc_top/u_alc_mc_top/dhi_$name"
    }
    set net [get_nets -hier $logical]
    if {[llength $net] != 1} {error "PAXI missing net $name"}
    set drivers [get_pins -of $net -filter {DIRECTION == output} *]
    set sinks [get_pins -of $net -filter {DIRECTION == input} *]
    if {[llength $drivers] != 1 || [llength $sinks] == 0} {error "PAXI missing driver/consumer $name"}
    if {[string match {rdata*} $name] && ![string match {u_ddr2/*} [lindex $drivers 0]]} {error "PAXI read data not from DDR $name $drivers"}
    puts $fh "$name\t$net\t$drivers\t$sinks"
}
close $fh
puts "DDR_PAXI_CONNECTIVITY_COMPLETE count=[llength $signals]"
bitgen -bit HX1P35A_C7_STEM_DDR_DOWN2.bit
export_bitgen_param -file bitgen_parameters.txt
puts "DDR_DIAGNOSTIC_BITGEN_COMPLETE"
close_project
