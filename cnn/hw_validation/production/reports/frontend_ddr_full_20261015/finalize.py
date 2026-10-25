"""Bind complete frontend evidence; optionally export the approved SRAM diagnostic."""
import argparse
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
import run

ROOT = run.ROOT
BIN_NAMES = ('initialization', 'input_fill', 'table_parameters', 'rgb_halo',
             'stem_compute', 'stem_export_write', 'dw_halo', 'down_compute',
             'pw_export_write', 'control')


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def collect():
    run.check()
    closure = load('physical/source_hashes.json')
    assert all(run.sha(path) == value for path, value in closure.items())
    constraint = load('constraint_recheck/receipt.json')
    assert constraint['passed'] and constraint['database_sha256'] == run.sha(ROOT / 'physical/pr.db')
    paths = run.timing(ROOT / 'physical/all_endpoints.timing')
    assert paths == constraint['timing'] and not paths['violations']
    assert set(paths['worst']) == {'setup', 'hold', 'recovery', 'removal'}
    cases = {}
    for path in sorted((ROOT / 'verification').glob('*/receipt.json')):
        item = json.loads(path.read_text(encoding='utf-8'))
        if 'compiled_source_sha256' in item:
            cases[item['case']] = (path, item)
    assert set(cases) == set(range(8)), 'All eight final test cases required'
    for _, item in cases.values():
        assert item['result'].startswith('PASS_')
        assert all(run.sha(ROOT / p) == h for p, h in item['compiled_source_sha256'].items())
        assert all(run.sha(ROOT / 'vectors' / p) == h for p, h in item['input_vector_sha256'].items())
        if item['case'] < 4:
            assert (item['writes'], item['reads'], item['output_bytes'], item['halo_accepts']) == (78336, 97564, 221184, 1306368)
            assert item['acc_pre_silu_post'] == [958464] * 4
            assert sum(item['cycle_bins']) == item['cycles']
    normal = cases[0][1]
    assert normal['cycles'] == 17252079
    reports = {name: run.timing(ROOT / 'physical' / (name + '.timing')) for name in
               ('bounded_payload', 'reg_request_meta', 'reg_ack_meta', 'arithmetic_all',
                'eram_inputs', 'eram_outputs', 'mailbox_all', 'user_reset_sync', 'user_reset_distribution')}
    assert all(not item['violations'] for item in reports.values())
    area = (ROOT / 'physical/route.area').read_text(encoding='utf-8')
    resources = {name: int(re.search(r'^#' + name + r'\s+(\d+)', area, re.M)[1])
                 for name in ('slice', 'dsp', 'eram', 'plb', 'pll', 'IO')}
    assert resources['slice'] <= 21216 and resources['dsp'] <= 40 and resources['eram'] <= 108
    coverage = float(re.search(r'STA coverage\s*:\s*([\d.]+)',
                     (ROOT / 'physical/final_timing.rpt').read_text(encoding='utf-8'))[1])
    gates = {name: {key: load(path)[key] for key in ('errors', 'strict_warnings', 'delivery_ready')}
             for name, path in (('rtl', 'rtl_gate/rtl.json'), ('testbench', 'verification/tb_gate.json'))}
    summary = {'stage': 'COMPLETE_FRONTEND_FUNCTIONAL_PHYSICAL_PASS', 'whole_system_signoff': False,
        'parameters': 'FROZEN_TEST_ONLY_NOT_QAT_MODEL', 'board_status': 'NOT_RUN',
        'layers': ['Stem 3->16', 'down2 DW 16', 'down2 PW 16->24'],
        'tiles': {'stem': 2304, 'down2': 576},
        'reference': 'reference/contract.json', 'physical_directory': str(ROOT / 'physical'),
        'physical_flow': load('physical/td.command.json'), 'source_hashes': closure,
        'constraint_check': constraint, 'all_endpoints': paths, 'selected_paths': reports,
        'resources_including_ddr_hdmi_diagnostic_shell': resources, 'sta_coverage_percent': coverage,
        'strict': gates, 'strict_gate_pass': False,
        'functional': [{'directory': str(path.parent), **item} for path, item in cases.values()],
        'normal_cycles': normal['cycles'], 'exclusive_cycle_bins': dict(zip(BIN_NAMES, normal['cycle_bins'])),
        'normal_compute_window_cycles': normal['cycle_bins'][4] + normal['cycle_bins'][7],
        'bitstream': 'NOT_GENERATED',
        'limits': ['Only first three layers; not full 67-layer CNN', 'Not camera/video concurrent',
                   'Controlled memory endpoint simulation, not manufacturer full DRAM simulation',
                   'Whole DDR/CNN reset only; no independent cancellation with late DDR returns',
                   'External IO timing not signed off; 23 input/49 output delay objects absent',
                   'Strict gates and SYN-5025 diagnostics retained; no production delivery pass',
                   'Thin timing margins and 93.21 percent PLB use',
                   'Periodic test RGB and fixed test coefficients; all four PW class goldens coincide',
                   'Quantization may mask small read-data corruption; board compare not exhaustive memory test',
                   '17.25 million cycles is first-three-layer controlled-endpoint cost, not full-network FPS']}
    run.save(ROOT / 'comparison.json', summary)
    run.save(ROOT / 'status.json', {'stage': summary['stage'], 'board_status': 'NOT_RUN',
        'comparison': str(ROOT / 'comparison.json'), 'strict_gate_pass': False, 'bitstream': 'NOT_GENERATED'})
    run.check()
    print(json.dumps({'resources': resources, 'worst_ns': {k: v['slack_ns'] for k, v in paths['worst'].items()},
                      'normal_cycles': normal['cycles'], 'tests': len(cases)}), flush=True)


def bitgen():
    run.check()
    summary = load('comparison.json')
    assert summary['stage'] == 'COMPLETE_FRONTEND_FUNCTIONAL_PHYSICAL_PASS'
    assert not summary['all_endpoints']['violations']
    assert all(run.sha(p) == h for p, h in summary['source_hashes'].items())
    for item in summary['functional']:
        assert all(run.sha(ROOT / p) == h for p, h in item['compiled_source_sha256'].items())
    assert not list(ROOT.glob('diagnostic_bitgen*/*.bit')), 'Do not repeat successful bit generation'
    work = run.fresh('diagnostic_bitgen')
    physical = ROOT / 'physical'
    name = 'road_stem_ddr_board_top.al'
    tree = ET.fromstring((physical / name).read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    for node in tree.findall('.//File'):
        node.set('Path', (physical / node.attrib['Path']).resolve().as_posix())
    (work / name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R'), encoding='utf-8')
    shutil.copyfile(physical / 'pr.db', work / 'pr.db')
    constraints = summary['constraint_check']['constraints']
    assert all(run.sha(p) == h for p, h in constraints.items())
    paths = [Path(p).as_posix() for p in constraints]
    reads = f'read_sdc {{{paths[0]}}}\nread_sdc -ip ddr2 {{{paths[1]}}}\nread_sdc {{{paths[2]}}}\n'
    script = (ROOT / 'build/bitgen.tcl').read_text(encoding='utf-8')
    script = script.replace('import_db pr.db\n', 'import_db pr.db\n' + reads)
    script = script.replace('report_timing_summary -ep_num 100000', 'report_timing_summary -ep_num 100')
    script = script.replace('HX1P35A_C7_STEM_DDR_DOWN2_FOUR.bit', 'HX1P35A_C7_FRONTEND_DDR_FULL.bit')
    script = script.replace('set fh [open paxi_connectivity.tsv w]',
        'if {![string match {*checking clock definition(0)*} $checks]} {error "Clock definitions unresolved"}\nset fh [open paxi_connectivity.tsv w]')
    (work / 'bitgen.tcl').write_text(script, encoding='utf-8')
    output = run.command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe', 'bitgen.tcl'], work, 'td', allowed=(0, 1, 2))
    assert 'DDR_DIAGNOSTIC_BITGEN_COMPLETE' in output and 'DDR_PAXI_CONNECTIVITY_COMPLETE count=256' in output
    assert run.sha(work / 'pr.db') == summary['constraint_check']['database_sha256']
    imported = run.timing(work / 'imported.timing')
    assert not imported['violations'] and set(imported['worst']) == set(summary['all_endpoints']['worst'])
    bit = work / 'HX1P35A_C7_FRONTEND_DDR_FULL.bit'
    assert bit.stat().st_size > 0
    receipt = {'path': str(bit), 'sha256': run.sha(bit), 'bytes': bit.stat().st_size,
               'database_sha256': run.sha(work / 'pr.db'), 'board_status': 'NOT_RUN',
               'scope': 'Temporary SRAM/JTAG frontend diagnostic only; no camera, deployment or Flash image'}
    run.save(work / 'receipt.json', receipt)
    summary['bitstream'] = receipt
    run.save(ROOT / 'comparison.json', summary)
    run.save(ROOT / 'status.json', {'stage': 'AWAITING_USER_FRONTEND_BOARD_TEST', 'board_status': 'NOT_RUN',
        'comparison': str(ROOT / 'comparison.json'), 'bitstream': receipt,
        'strict_gate_pass': False, 'whole_system_signoff': False})
    assert all(run.sha(p) == h for p, h in summary['source_hashes'].items())
    run.check()
    print(json.dumps(receipt), flush=True)


def freeze():
    run.check()
    summary = load('comparison.json')
    bit = summary['bitstream']
    assert isinstance(bit, dict) and run.sha(bit['path']) == bit['sha256']
    assert all(run.sha(p) == h for p, h in summary['source_hashes'].items())
    paths = [p for p in ROOT.iterdir() if p.is_file() and p.suffix in ('.py', '.json', '.txt', '.v')
             and p.name != 'artifact_hashes.json']
    for folder in ('rtl', 'reused', 'build', 'vectors', 'tests', 'reference', 'specifications'):
        paths.extend(p for p in (ROOT / folder).rglob('*') if p.is_file())
    paths += [ROOT / 'verification/suite_manifest.json', ROOT / 'verification/TEST_REPORT.md',
              ROOT / 'verification/tb_gate.json', ROOT / 'netlist_check.json',
              ROOT / 'constraint_recheck/receipt.json', ROOT / 'diagnostic_bitgen/receipt.json',
              ROOT / 'physical/pr.db', ROOT / 'physical/route.area', ROOT / 'physical/all_endpoints.timing',
              ROOT / 'physical/source_hashes.json', Path(bit['path'])]
    run.save(ROOT / 'artifact_hashes.json', {str(path): run.sha(path) for path in paths})
    print('FRONTEND_CLOSURE_FROZEN; awaiting user SRAM board test', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('collect', 'bitgen', 'freeze'))
    globals()[parser.parse_args().action]()
