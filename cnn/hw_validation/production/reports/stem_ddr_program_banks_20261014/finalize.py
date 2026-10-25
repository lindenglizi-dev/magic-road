"""Bind the measured candidate evidence and generate only a temporary diagnostic."""
import json
import re
import shutil
import xml.etree.ElementTree as ET
import run

ROOT = run.ROOT


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    run.check()
    physical = ROOT / 'physical'
    closure = load('physical/source_hashes.json')
    assert all(run.sha(p) == h for p, h in closure.items())
    constraint = load('constraint_recheck/receipt.json')
    assert constraint['passed'] and constraint['database_sha256'] == run.sha(physical / 'pr.db')
    before = run.timing(physical / 'all_endpoints.timing')
    assert before == constraint['timing']
    assert set(before['worst']) == {'setup', 'hold', 'recovery', 'removal'} and not before['violations']
    rom = load('netlist_rom_attempt3/receipt.json')
    assert rom['passed'] and rom['original_netlist_sha256'] == run.sha(physical / 'gate_netlist.v')
    assert all(run.sha(p) == h for p, h in rom['source_hashes'].items())
    functional = load('functional_comparison.json')
    assert functional['passed'] and functional['all_13_case_cycles_identical']
    integrated = load('integrated_simulation/receipt.json')
    assert all(item['passed'] for item in integrated['results'])
    assert all(run.sha(p) == h for p, h in integrated['source_hashes'].items())
    area = (physical / 'route.area').read_text(encoding='utf-8')
    resources = {key: int(re.search(r'^#' + key + r'\s+(\d+)', area, re.M)[1]) for key in ('slice', 'dsp', 'eram', 'pll', 'IO', 'plb')}
    assert resources['slice'] <= 21216 and resources['dsp'] <= 40 and resources['eram'] <= 108
    summary = {'started': '2026-10-14', 'completed': '2026-10-15', 'physical_directory': str(physical),
        'physical_flow': load('physical/td.command.json'), 'constraint_check': constraint,
        'all_endpoints': before, 'resources_including_diagnostic_shell': resources,
        'sta_coverage_percent': 98.41, 'program_mapping': 'LUT logic plus registered bank outputs; not the old 20-ERAM program layout',
        'program_netlist_test': rom, 'functional': functional, 'integrated': integrated,
        'strict_rtl': {'errors': 782, 'strict_warnings': 20, 'directory': 'gate_attempt2'},
        'strict_tests': {'errors': 723, 'strict_warnings': 0, 'directory': 'gate_attempt2'},
        'source_hashes': closure, 'board_status': 'NOT_RUN', 'whole_system_signoff': False,
        'limitations': ['TEST_ONLY coefficients', 'Four down2 tiles, not complete CNN', 'External IO/reset timing not signed off',
                       'Three dummy-node categories and SYN-5025 records retained', 'Thin timing margins and 93.59 percent PLB use',
                       'Strict delivery gates remain failed; portless TB canonical specification unsupported']}
    run.save(ROOT / 'comparison.json', summary)
    work = run.fresh('diagnostic_bitgen')
    name = 'road_stem_ddr_board_top.al'
    tree = ET.fromstring((physical / name).read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    for node in tree.findall('.//File'):
        node.set('Path', (physical / node.attrib['Path']).resolve().as_posix())
    (work / name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R'), encoding='utf-8')
    shutil.copyfile(physical / 'pr.db', work / 'pr.db')
    paths = list(constraint['constraints'])
    assert all(run.sha(p) == h for p, h in constraint['constraints'].items())
    reads = f'read_sdc {{{paths[0]}}}\nread_sdc -ip ddr2 {{{paths[1]}}}\nread_sdc {{{paths[2]}}}\n'.replace('\\', '/')
    script = (ROOT / 'build/bitgen.tcl').read_text(encoding='utf-8')
    script = script.replace('import_db pr.db\n', 'import_db pr.db\n' + reads)
    script = script.replace('report_timing_summary -ep_num 100000', 'report_timing_summary -ep_num 100')
    script = script.replace('HX1P35A_C7_STEM_DDR_DOWN2_FOUR.bit', 'HX1P35A_C7_STEM_DDR_DOWN2_BANKS.bit')
    script = script.replace('set fh [open paxi_connectivity.tsv w]', 'if {![string match {*checking clock definition(0)*} $checks]} {error "Clock definitions unresolved"}\nset fh [open paxi_connectivity.tsv w]')
    (work / 'bitgen.tcl').write_text(script, encoding='utf-8')
    output = run.command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe', 'bitgen.tcl'], work, 'td', allowed=(0, 1, 2))
    assert 'DDR_DIAGNOSTIC_BITGEN_COMPLETE' in output and 'DDR_PAXI_CONNECTIVITY_COMPLETE count=256' in output
    assert run.sha(work / 'pr.db') == constraint['database_sha256']
    imported = run.timing(work / 'imported.timing')
    assert not imported['violations'] and set(imported['worst']) == set(before['worst'])
    bit = work / 'HX1P35A_C7_STEM_DDR_DOWN2_BANKS.bit'
    assert bit.stat().st_size > 0
    receipt = {'path': str(bit), 'sha256': run.sha(bit), 'bytes': bit.stat().st_size,
               'database_sha256': run.sha(work / 'pr.db'), 'board_status': 'NOT_RUN',
               'scope': 'Temporary SRAM/JTAG diagnostic only; not deployment or Flash image', 'timing': imported}
    run.save(work / 'receipt.json', receipt)
    summary['bitstream'] = receipt
    run.save(ROOT / 'comparison.json', summary)
    run.save(ROOT / 'status.json', {'stage': 'DIAGNOSTIC_BIT_READY_BOARD_NOT_RUN', 'comparison': str(ROOT / 'comparison.json'),
             'bitstream': receipt, 'strict_gate_pass': False, 'whole_system_signoff': False})
    assert all(run.sha(p) == h for p, h in closure.items())
    run.check()
    print(json.dumps({'bitstream': str(bit), 'sha256': receipt['sha256'], 'resources': resources}), flush=True)


if __name__ == '__main__':
    main()
