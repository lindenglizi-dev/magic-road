"""Bounded display CDC diagnostic; reuse frozen tests/build without editing baseline."""
import argparse
import ast
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'ddr_board_selftest_20261013'
sys.path.insert(0, str(BASE))
spec = importlib.util.spec_from_file_location('frozen_ddr_run', BASE / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
run.ROOT = ROOT


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


run.sha = sha


def prepare():
    assert not (ROOT / 'frozen.json').exists()
    frozen = json.loads((BASE / 'frozen.json').read_text(encoding='utf-8'))
    for path in BASE.rglob('*'):
        if path.is_file():
            frozen[str(path)] = sha(path)
    run.save(ROOT / 'frozen.json', frozen)
    for folder in ('rtl', 'tests', 'build'):
        shutil.copytree(BASE / folder, ROOT / folder)
    run.check()
    run.dependencies()


def help_commands():
    run.check()
    work = run.fresh('command_help')
    shutil.copyfile(ROOT / 'help.tcl', work / 'help.tcl')
    output = run.command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe',
                          'help.tcl'], work, 'td', allowed=(0, 1, 2))
    print('\n'.join(line for line in output.splitlines() if 'set_max_delay -help' in line)[:1000])
    run.check()


def probe(constraints=False, negative=False, logical=False):
    run.check()
    work = run.fresh('probe')
    shutil.copyfile(BASE / ('physical_attempt2/gate.db' if logical else 'physical_attempt2/pr.db'), work / 'pr.db')
    script = 'constraint_probe.tcl' if constraints else 'probe.tcl'
    shutil.copyfile(ROOT / script, work / 'probe.tcl')
    if negative:
        # Generated negative test, never the implementation constraint file.
        text = (work / 'probe.tcl').read_text(encoding='utf-8')
        text = text.replace('read_sdc resolved_display.sdc',
            'set fh [open resolved_display.sdc r]\nset text [read $fh]\nclose $fh\n'
            'set fh [open negative_display.sdc w]\nputs $fh [string map {7.500 0.001} $text]\nclose $fh\n'
            'read_sdc negative_display.sdc')
        (work / 'probe.tcl').write_text(text, encoding='utf-8')
    output = run.command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe',
                          'probe.tcl'], work, 'td', allowed=(0, 1, 2))
    print('\n'.join(line for line in output.splitlines() if 'CDC_' in line))
    assert ('CDC_CONSTRAINT_PROBE_COMPLETE' if constraints else 'CDC_PROBE_COMPLETE') in output
    if negative:
        status = (work / 'route.ts').read_text(encoding='utf-8')
        assert 'SWNS: -' in status, 'Negative bound failed to detect unsafe delay'
        run.save(work / 'negative_receipt.json', {'passed': True, 'expected': '0.001ns bound rejected', 'actual': status})
    run.check()


def timing(path):
    records = []
    current, group = {}, ''
    labels = {'Begin Point': 'begin', 'End Point': 'end', 'Check Type': 'type',
              'Process': 'process', 'Data Path Delay': 'data_delay', 'Budget': 'budget'}
    for line in path.open(encoding='utf-8'):
        match = re.match(r'Path Group\s*:\s*(.+)', line)
        if match:
            group = match[1]
        match = re.match(r'Slack\s*:\s*([-\d.]+)ns', line)
        if match:
            if 'type' in current:
                records.append(current)
            current = {'slack_ns': float(match[1]), 'group': group}
        for label, key in labels.items():
            match = re.match(label + r'\s*:\s*(.+)', line)
            if match and current:
                # Ignored paths have Begin/End/Type but no Slack. Do not let
                # their fields overwrite the preceding scored path.
                if key == 'begin' and 'begin' in current:
                    if 'type' in current:
                        records.append(current)
                    current = {}
                    continue
                current[key] = match[1]
    if 'type' in current:
        records.append(current)
    assert records, path
    kinds = Counter(item['type'] for item in records)
    return {'records': kinds,
            'worst': {kind: min((item for item in records if item['type'] == kind), key=lambda x: x['slack_ns']) for kind in kinds},
            'violations': [item for item in records if item['slack_ns'] < 0]}


def collect():
    run.check()
    work = max((path for path in ROOT.glob('physical*') if (path / 'all_endpoints.timing').exists()), key=lambda p: p.stat().st_mtime)
    log = (work / 'td.log').read_text(encoding='utf-8')
    assert 'DDR_PHYSICAL_COMPLETE' in log
    all_paths = timing(work / 'all_endpoints.timing')
    payload = timing(work / 'bounded_payload.timing')
    sync = {name: timing(work / f'{name}.timing') for name in ('reg_request_meta', 'reg_ack_meta')}
    assert not payload['violations'] and payload['records'] == {'setup': 182}
    assert all(not result['violations'] and result['records'] == {'setup': 1, 'hold': 1} for result in sync.values())
    rows = list(csv.DictReader((work / 'display_cdc_mapping.tsv').open(encoding='utf-8'), delimiter='\t'))
    mapped = {row['destination_d'].strip('{}'): row['kind'] for row in rows if row['kind'] in ('payload', 'first_stage')}
    old_paths = json.loads((BASE / 'violating_paths.json').read_text(encoding='utf-8'))
    old_mapping = list(csv.DictReader((ROOT / 'probe_attempt6/display_cdc_mapping.tsv').open(encoding='utf-8'), delimiter='\t'))
    old_mapped = {row['destination_d'].strip('{}'): row['kind'] for row in old_mapping if row['kind'] in ('payload', 'first_stage')}
    classified = Counter(f"{item['type']}:{old_mapped.get(item['end'].split(' (')[0], 'UNMAPPED')}" for item in old_paths)
    assert classified == {'setup:payload': 182, 'setup:first_stage': 1, 'hold:first_stage': 1}
    assert Counter(row['kind'] for row in rows) == {'payload': 199, 'first_stage': 2, 'absent_constant_bits': 1}
    assert len(mapped) == 184
    area = (work / 'route.area').read_text(encoding='utf-8')
    resources = {name: int(re.search(r'^#' + name + r'\s+(\d+)', area, re.M)[1]) for name in ('slice', 'eram', 'dsp', 'pll', 'pad', 'IO')}
    report = (work / 'all_endpoints.timing').open(encoding='utf-8')
    header = ''.join(next(report) for _ in range(35))
    report.close()
    coverage = float(re.search(r'STA coverage\s*:\s*([\d.]+)%', header)[1])
    checks = (work / 'check_timing.rpt').read_text(encoding='utf-8')
    assert 'checking invalid constraint(0)' in checks and 'checking combinational loops(0)' in checks
    source_hashes = json.loads((work / 'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(path) == digest for path, digest in source_hashes.items())
    for name in ('road_ddr_selftest.v', 'road_ddr_selftest_top.v'):
        assert sha(ROOT / 'rtl' / name) == sha(BASE / 'rtl' / name)
    tests = json.loads((ROOT / 'simulation/receipt.json').read_text(encoding='utf-8'))
    assert len(tests['cases']) == 17 and all(item['passed'] for item in tests['cases'])
    display = json.loads((ROOT / 'display_simulation/receipt.json').read_text(encoding='utf-8'))
    assert 'captures=60' in display['summary'][0]
    strict = {}
    for name in ('rtl', 'tests'):
        result = json.loads((ROOT / 'gate' / f'{name}.json').read_text(encoding='utf-8'))
        strict[name] = {key: result[key] for key in ('errors', 'strict_warnings', 'checks', 'delivery_ready')}
    bitstream = 'NOT_GENERATED'
    for receipt_path in sorted(ROOT.glob('diagnostic_bitgen*/receipt.json'), key=lambda p: p.stat().st_mtime):
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        if receipt['database_sha256'] == sha(work / 'pr.db') and sha(receipt['path']) == receipt['sha256']:
            bitstream = receipt
    summary = {'physical_directory': str(work), 'all_endpoints': all_paths, 'bounded_payload': payload,
               'synchronizer_stages': sync, 'old_failure_corrected_classification': classified,
               'resources_including_ddr_and_hdmi_no_cnn': resources, 'sta_coverage_percent': coverage,
               'source_hashes': source_hashes, 'strict': strict,
               'requester': tests, 'display': display, 'board_readback': 'NOT_RUN', 'bitstream': bitstream}
    run.save(ROOT / 'comparison.json', summary)
    run.save(ROOT / 'status.json', {'status': 'BOUNDED_CDC_DIAGNOSTIC_PASS' if not all_paths['violations'] else 'PHYSICAL_TIMING_FAILED',
             'whole_system_signoff': False, 'strict_delivery': False, 'board_readback': 'NOT_RUN',
             'bitstream': bitstream, 'physical_directory': str(work)})
    run.check()
    print(json.dumps({'worst': {kind: value['slack_ns'] for kind, value in all_paths['worst'].items()},
                      'violations': len(all_paths['violations']), 'resources': resources, 'coverage': coverage}, ensure_ascii=False))


def bitgen():
    run.check()
    summary = json.loads((ROOT / 'comparison.json').read_text(encoding='utf-8'))
    assert not summary['all_endpoints']['violations']
    physical = Path(summary['physical_directory'])
    work = run.fresh('diagnostic_bitgen')
    tree = ET.fromstring((physical / 'road_ddr_selftest_top.al').read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    (work / 'road_ddr_selftest_top.al').write_text('<?xml version="1.0" encoding="UTF-8"?>\n' +
         ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R'), encoding='utf-8')
    shutil.copyfile(physical / 'pr.db', work / 'pr.db')
    shutil.copyfile(ROOT / 'bitgen.tcl', work / 'bitgen.tcl')
    run.save(work / 'input_hashes.json', {str(path): sha(path) for path in
             (physical / 'pr.db', work / 'pr.db', work / 'bitgen.tcl', work / 'road_ddr_selftest_top.al')})
    output = run.command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe',
                         'bitgen.tcl'], work, 'td', allowed=(0, 1, 2))
    assert 'DDR_DIAGNOSTIC_BITGEN_COMPLETE' in output
    assert 'DDR_PAXI_CONNECTIVITY_COMPLETE count=256' in output
    assert not timing(work / 'imported.timing')['violations']
    path = work / 'HX1P35A_C7_DDR_DIAG.bit'
    assert path.stat().st_size > 0
    receipt = {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size,
               'scope': 'Temporary diagnostic SRAM/JTAG; NOT deployment or board PASS',
               'database_sha256': sha(physical / 'pr.db'), 'hardware_not_accessed': True}
    run.save(work / 'receipt.json', receipt)
    state = json.loads((ROOT / 'status.json').read_text(encoding='utf-8'))
    state['bitstream'] = receipt
    run.save(ROOT / 'status.json', state)
    summary['bitstream'] = receipt
    run.save(ROOT / 'comparison.json', summary)
    run.check()
    print(json.dumps(receipt, ensure_ascii=False))


def finalize():
    run.check()
    ast.parse((ROOT / 'run_cdc.py').read_text(encoding='utf-8'))
    summary = json.loads((ROOT / 'comparison.json').read_text(encoding='utf-8'))
    state = json.loads((ROOT / 'status.json').read_text(encoding='utf-8'))
    assert summary['bitstream'] == state['bitstream']
    assert sha(state['bitstream']['path']) == state['bitstream']['sha256']
    physical = Path(summary['physical_directory'])
    generated = Path(state['bitstream']['path']).parent
    files = [*ROOT.glob('*.py'), *ROOT.glob('*.tcl'), *ROOT.glob('*.md')]
    files += [ROOT / name for name in ('comparison.json', 'status.json', 'frozen.json', 'frozen_check.json')]
    files += [path for folder in ('rtl', 'tests', 'build', 'gate', 'simulation', 'display_simulation')
              for path in (ROOT / folder).glob('*') if path.is_file()]
    files += [path for folder in (physical, generated) for path in folder.glob('*') if path.is_file()]
    assert len(list(ROOT.glob('*.md'))) >= 2
    run.save(ROOT / 'artifact_hashes.json', {str(path): sha(path) for path in files})
    print(json.dumps({'artifact_files': len(files), 'board_readback': state['board_readback'], 'bitstream_verified': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'help', 'probe', 'logical', 'constraints', 'negative', 'check', 'simulate', 'display', 'physical', 'gate', 'collect', 'bitgen', 'finalize'))
    action = parser.parse_args().action
    if action == 'prepare':
        prepare()
    elif action == 'help':
        help_commands()
    elif action == 'probe':
        probe()
    elif action == 'logical':
        probe(logical=True)
    elif action == 'constraints':
        probe(constraints=True)
    elif action == 'negative':
        probe(constraints=True, negative=True)
    elif action == 'collect':
        collect()
    elif action == 'bitgen':
        bitgen()
    elif action == 'finalize':
        finalize()
    else:
        getattr(run, action)()
