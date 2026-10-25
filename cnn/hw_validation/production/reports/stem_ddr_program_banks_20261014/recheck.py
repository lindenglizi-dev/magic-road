"""Re-export routed timing with the unchanged original constraint sources."""
import json
import shutil
import xml.etree.ElementTree as ET
from run import ROOT, check, command, fresh, save, sha, timing


def main():
    check()
    original = ROOT / 'physical'
    work = fresh('constraint_recheck')
    project = 'road_stem_ddr_board_top.al'
    tree = ET.fromstring((original / project).read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    (work / project).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R'), encoding='utf-8')
    shutil.copyfile(original / 'pr.db', work / 'pr.db')
    constraints = [original / 'board.sdc', original / 'ddr2/src/sdc/ddr2.sdc', original / 'resolved_display.sdc']
    hashes = {str(p): sha(p) for p in constraints}
    database_hash = sha(original / 'pr.db')
    script = '''import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_stem_ddr_board_top.al -single_run
import_db pr.db
'''
    script += f'read_sdc {{{constraints[0].as_posix()}}}\nread_sdc -ip ddr2 {{{constraints[1].as_posix()}}}\nread_sdc {{{constraints[2].as_posix()}}}\n'
    script += '''update_timing -mode final
report_timing_status -file route.ts
report_timing_summary -ep_num 100000 -path_num 1 -file all_endpoints.timing
report_timing_summary -include_ignored -ep_num 256 -path_num 1 -file include_ignored.timing
check_timing -verbose -file check_timing.rpt
report_timing_exception -ep_num 1000 -path_num 1 -file exceptions.rpt
report_timing_ignored -ep_num 1000 -path_num 1 -file ignored.rpt
report_clock_summary -clocks [get_clocks -include_generated_clocks *] -expand_buckets -debug -file clocks.rpt
puts "BANK_CONSTRAINT_RECHECK_COMPLETE"
close_project
'''
    (work / 'check.tcl').write_text(script, encoding='utf-8')
    output = command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe', 'check.tcl'], work, 'td', allowed=(0, 1, 2))
    assert 'BANK_CONSTRAINT_RECHECK_COMPLETE' in output
    assert sha(work / 'pr.db') == database_hash == sha(original / 'pr.db')
    assert all(sha(p) == h for p, h in hashes.items())
    paths = timing(work / 'all_endpoints.timing')
    checks = (work / 'check_timing.rpt').read_text(encoding='utf-8')
    clean = all(f'checking {name}(0)' in checks for name in ('clock definition', 'invalid constraint', 'combinational loops', 'no clock'))
    save(work / 'receipt.json', {'passed': clean and not paths['violations'], 'database_sha256': database_hash,
         'constraints': hashes, 'timing': paths, 'clock_definition_clean': clean,
         'scope': 'Same routed database and original SDC sources; no implementation rerun or new exception'})
    print(json.dumps({'clock_definition_clean': clean, 'worst': paths['worst'], 'violations': len(paths['violations'])}), flush=True)
    check()


if __name__ == '__main__':
    main()
