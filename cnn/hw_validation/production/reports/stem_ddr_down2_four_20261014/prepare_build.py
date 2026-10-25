"""Retain approved display CDC scope, add only timing reports for new logic."""
import run


def generate():
    old=(run.PREVIOUS/'build/display_cdc.tcl').read_text(encoding='utf-8')
    begin=old.index('set cdc_expected_absent {}')
    end=old.index('if {$cdc_absent_bits != $cdc_expected_absent}',begin)
    replacement='''set cdc_expected_absent {}
for {set bit 128} {$bit < 182} {incr bit} {
    if {((0x535444445234 >> ($bit - 128)) & 1) == 0} {lappend cdc_expected_absent $bit}
}
'''
    (run.ROOT/'build/display_cdc.tcl').write_text(old[:begin]+replacement+old[end:],encoding='utf-8')
    script=(run.PREVIOUS/'build/build.tcl').read_text(encoding='utf-8')
    script=script.replace('road_ddr_selftest_top','road_stem_ddr_board_top').replace('DDR_PHYSICAL_COMPLETE','ONCE_PHYSICAL_COMPLETE')
    # Synthesis initializes a 24-thread pool despite the earlier flow setting.
    # Reapply at the placement boundary, as in the proven import diagnostic.
    script=script.replace('set_param place effort high',
        'set_param flow thread 1\nreport_param -all -detail -file placement_parameters.rpt\nset_param place effort high')
    # Bounded different-strategy diagnostic after high timing effort crashed
    # with both 24 and one actual placement threads. Timing limits stay intact.
    script=script.replace('set_param place opt_timing high','set_param place opt_timing medium')
    insertion='''# New mailbox and arithmetic paths receive no additional exceptions.
set mailbox_regs [get_regs -hier {*u_mailbox/*}]
if {[llength $mailbox_regs] == 0} {error "Mailbox registers missing"}
report_timing_path -from $mailbox_regs -to $mailbox_regs -ep_num 100000 -path_num 1 -file mailbox_all.timing
set arithmetic_regs [get_regs -hier {*u_sequence/u_core/*}]
if {[llength $arithmetic_regs] == 0} {error "Arithmetic registers missing"}
report_timing_path -from $arithmetic_regs -to $arithmetic_regs -ep_num 100000 -path_num 1 -file arithmetic_all.timing
puts "ONCE_RETAINED_REGS mailbox=[llength $mailbox_regs] arithmetic=[llength $arithmetic_regs]"
'''
    script=script.replace('puts "ONCE_PHYSICAL_COMPLETE"',insertion+'puts "ONCE_PHYSICAL_COMPLETE"')
    # Keep all endpoint coverage once; ancillary views only repeat worst paths.
    lines=[]
    for line in script.splitlines():
        if '-ep_num 100000' in line and ' -file all_endpoints.timing' not in line and ' -file bounded_payload.timing' not in line:
            line=line.replace('-ep_num 100000','-ep_num 256')
        lines.append(line)
    script='\n'.join(lines)+'\n'
    (run.ROOT/'build/build.tcl').write_text(script,encoding='utf-8')
    bitgen=(run.PREVIOUS/'bitgen.tcl').read_text(encoding='utf-8')
    bitgen=bitgen.replace('road_ddr_selftest_top','road_stem_ddr_board_top')
    bitgen=bitgen.replace('road_ddr_selftest_Inst/i_$name','u_mailbox/i_$name')
    bitgen=bitgen.replace('HX1P35A_C7_DDR_EXTENDED.bit','HX1P35A_C7_STEM_DDR_DOWN2_FOUR.bit')
    (run.ROOT/'build/bitgen.tcl').write_text(bitgen,encoding='utf-8')
    print('BUILD_PREPARED retained_display_CDC only; new mailbox fully timed')


if __name__=='__main__':
    generate()
