"""Independent DDR board experiment; no writes outside this directory."""
import argparse
import ast
from collections import Counter
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import time
import shutil
import xml.etree.ElementTree as ET

import reference

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
MSIM = Path('D:/modeltech64_2020.4/win64')
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def fresh(name):
    path = ROOT / name
    index = 1
    while path.exists():
        index += 1
        path = ROOT / f'{name}_attempt{index}'
    path.mkdir()
    return path


def command(args, work, name, allowed=(0,)):
    assert work.resolve().is_relative_to(ROOT)
    start = time.monotonic()
    result = subprocess.run([str(x) for x in args], cwd=work, capture_output=True)
    output = (result.stdout + result.stderr).decode('utf-8', errors='replace')
    (work / f'{name}.log').write_text(output, encoding='utf-8')
    save(work / f'{name}.command.json', {'argv': [str(x) for x in args],
         'cwd': str(work), 'returncode': result.returncode, 'seconds': time.monotonic()-start})
    assert result.returncode in allowed, f'{name}: exit {result.returncode}; see {work / (name+".log")}'
    return output


def check():
    frozen = json.loads((ROOT / 'frozen.json').read_text(encoding='utf-8'))
    changed = [name for name, digest in frozen.items() if sha(name) != digest]
    save(ROOT / 'frozen_check.json', {'checked': len(frozen), 'changed': changed})
    assert not changed, changed


def prepare():
    assert not (ROOT / 'frozen.json').exists()
    frozen = {}
    for relative in ('ddr_vendor_startup_20261011/frozen.json',
                     'board_selftest_20261010/evidence_attempt4/candidate_final_freeze.json'):
        manifest = ROOT.parent / relative
        content = json.loads(manifest.read_text(encoding='utf-8'))
        assert isinstance(content, dict)
        # These historical manifests map absolute paths directly to SHA256.
        assert all(isinstance(value, str) and len(value) == 64 for value in content.values())
        frozen.update(content)
        frozen[str(manifest)] = sha(manifest)
    for path in (PROJECT / 'cnn/hw_validation/board_test_20261010').iterdir():
        if path.is_file():
            frozen[str(path)] = sha(path)
    save(ROOT / 'frozen.json', frozen)
    check()
    dependencies()


def dependencies():
    os.chdir(ROOT)
    sys.path.insert(0, str(SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    settings = json.loads((SKILL / 'config/defaults.json').read_text(encoding='utf-8'))
    result = check_dependencies(settings, state_path=ROOT / 'dependency_state.json')
    save(ROOT / 'dependency_preflight.json', result)
    assert result['required_ok']


def simulate():
    check()
    reference.self_check()
    work = fresh('simulation')
    (work / 'patterns.hex').write_text(''.join(f'{reference.pattern(r, i):032x}\n'
         for r in range(2) for i in range(4)), encoding='ascii')
    command([MSIM/'vlib.exe', 'work'], work, 'vlib')
    command([MSIM/'vlog.exe', '-work', 'work', ROOT/'rtl/road_ddr_selftest.v',
             ROOT/'tests/tb_ddr_selftest.v'], work, 'vlog')
    results = []
    for case in range(17):
        output = command([MSIM/'vsim.exe', '-c', '-lib', 'work', 'tb_ddr_selftest',
            f'+CASE={case}', '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],
            work, f'case_{case:02d}', allowed=(0, 1, 2))
        passed = f'DDR_REQUESTER_PASS case={case} ' in output and '** Fatal:' not in output
        results.append({'case': case, 'passed': passed,
                        'summary': [line for line in output.splitlines() if 'DDR_REQUESTER_PASS' in line or '** Fatal:' in line]})
        save(work/'receipt.json', {'scope': 'Controlled endpoint, NOT DDR device simulation', 'cases': results})
        print(f'CASE {case}: {"PASS" if passed else "FAIL"}', flush=True)
        if not passed:
            break
    check()
    assert len(results) == 17 and all(item['passed'] for item in results), str(work)


def gate():
    check()
    work = fresh('gate')
    source_hashes = {str(path): sha(path) for folder in (ROOT/'rtl', ROOT/'tests') for path in folder.glob('*.v')}
    save(work/'source_hashes.json', source_hashes)
    entry = f'import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())'
    for name, source, extra in [('rtl', ROOT/'rtl', []), ('tests', ROOT/'tests', ['--include-testbench'])]:
        external = []
        # Legacy official HDMI cannot be parsed by this strict formatter.
        # Preserve unresolved-IP diagnostics here; actual TD elaborates the real sources.
        for path in [ROOT/'rtl/road_ddr_selftest.v', PROJECT/'user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v',
                     ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v']:
            external += ['--external-interface-source', path]
        command([sys.executable, '-B', '-X', 'utf8', '-c', entry, source, *extra,
                 *external,
                 '--json', work/f'{name}.json', '--markdown', work/f'{name}.md'],
                ROOT, str(work.relative_to(ROOT)/name), allowed=(0, 1, 2))
        assert (work/f'{name}.json').exists(), f'Checker execution failed; see {work}/{name}.log'
    assert all(sha(name) == digest for name, digest in source_hashes.items()), 'Gate sources changed during execution'
    check()


def display():
    check()
    work = fresh('display_simulation')
    command([MSIM/'vlib.exe', 'work'], work, 'vlib')
    command([MSIM/'vlog.exe', '-work', 'work', ROOT/'tests/tb_ddr_display_cdc.v',
             ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v'], work, 'vlog')
    output = command([MSIM/'vsim.exe', '-c', '-lib', 'work', 'tb_ddr_display_cdc',
            '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],
            work, 'display', allowed=(0, 1, 2))
    assert 'DDR_DISPLAY_CDC_PASS' in output and '** Fatal:' not in output, work
    save(work/'receipt.json', {'scope': 'Handshake and reset simulation, NOT metastability or STA proof',
                             'summary': [line for line in output.splitlines() if 'DDR_DISPLAY_CDC_PASS' in line]})
    check()


def specifications():
    check()
    work = fresh('specifications')
    entry = f'import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
    for path in sorted((ROOT/'rtl').glob('*.v')):
        ports = []
        for direction, high, low, name, description in re.findall(
                r'^\s*(input|output|inout)\s*(?:\[(\d+):(\d+)\])?\s*(\w+),?\s*//\s*(.+)$',
                path.read_text(encoding='utf-8'), re.M):
            ports.append({'name': name, 'direction': direction, 'width': abs(int(high)-int(low))+1 if high else 1,
                          'role': description, 'description': description})
        assert ports
        wave = {'signal': [{'name': 'clk', 'wave': 'p.........'}, {'name': 'rstn', 'wave': '01........'},
                           {'name': 'phy_ready', 'wave': '0..1......'}, {'name': 'AWVALID/WVALID', 'wave': '0....1.0..'},
                           {'name': 'AWREADY', 'wave': '0.....10..'}, {'name': 'WREADY', 'wave': '0......10.'}],
                'head': {'text': 'Schematic: AW/W offered together, accepted independently; no fixed DDR latency'}}
        module = {'name': path.stem, 'feature': 'ddr_board_selftest', 'rtl_path': path.name,
                  'description': 'Exclusive native PAXI DDR diagnostic, not full CNN or memory capacity proof.',
                  'interfaces': {'ports': ports},
                  'clock': {'domains': 'DDR user ~133.33MHz; top additionally 100MHz ref,75MHz pixel,375MHz serial'},
                  'reset': {'assertion': 'Asynchronous, full DDR IP and requester reset together',
                            'release': 'Top two-flop release per domain; PHY reset also gates requester'},
                  'behavior': ['Wait PHY ready; write four native addresses 0/8/16/24, read reverse, repeat with complement.',
                               'Keep AW/W payload stable until own acceptance; present W with AW (zero launch delay).',
                               'One read outstanding; compare all 128 bits and RLAST; latch first failure, no retry.',
                               'PAXI mask=0; byte address=native*2 for current 16-bit DDR, not full-capacity validation.',
                               'HDMI frozen snapshots contain error/address/counts and alternate full expected/actual pages.'],
                  'constraints': ['No write completion fabricated from AW/W acceptance. No production Tensor READY claim.',
                                  'C_TIMEOUT=27h7ffffff per waiting stage; immediate fault cancellation requires full IP reset before retry.'],
                  'corner_cases': ['Independent AW/W backpressure, missing response, mismatch, unsolicited R, PHY lost, partial reset.'],
                  'verification_cases': ['17 controlled-endpoint cases; separate actual-IP implementation; real DDR readback requires board.'],
                  'timing_diagrams': [{'id': 'split_acceptance', 'title': 'Split AW/W acceptance', 'scenario': 'backpressure',
                                       'description': 'Compressed schematic only; maximum W generation delay is zero in requester.', 'wavejson': wave}]}
        contract = work/f'{path.stem}.json'
        save(contract, {'modules': [module]})
        command([sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', contract,
                 '--source', path, '--out-dir', ROOT/'rtl', '--no-state'], ROOT,
                str(work.relative_to(ROOT)/path.stem))
    check()


def physical():
    check()
    work = fresh('physical')
    old = ROOT.parent/'board_key4_c7_20261010/physical/road_board_selftest_top.al'
    tree = ET.fromstring(old.read_text(encoding='utf-8').replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    tree.find('Name').text = 'road_ddr_selftest_top'
    sources = tree.find('Source_Files')
    sources.clear()
    verilog = ET.SubElement(sources, 'Verilog')
    ips = ET.SubElement(sources, 'IP_FILE')
    official = ROOT.parent/'board_selftest_20261010/official'
    shutil.copytree(official, work/'official')
    vendor = PROJECT/'user_source/hdl_source/ph1p35_ddr/ddr2'
    shutil.copytree(vendor, work/'ddr2')
    inputs = {str(path): sha(path) for folder in (official, vendor) for path in folder.rglob('*') if path.is_file()}
    save(work/'original_ip_hashes.json', inputs)
    paths = [ROOT/'rtl/road_ddr_selftest.v', ROOT/'rtl/road_ddr_selftest_top.v',
             ROOT.parent/'board_selftest_20261010/rtl/road_selftest_display.v']
    paths += sorted((work/'official').glob('*.v'))
    paths += [work/'official/PLL/PLL.xml', work/'ddr2/ddr2.xml']
    for order, path in enumerate(paths, 1):
        section = ips if path.suffix == '.xml' else verilog
        node = ET.SubElement(section, 'File', {'Path': path.as_posix()})
        info = ET.SubElement(node, 'FileInfo')
        for key, value in [('UsedInSyn', 'true'), ('UsedInP&R', 'true'), ('BelongTo', 'design_1'), ('CompileOrder', str(order))]:
            ET.SubElement(info, 'Attr', {'Name': key, 'Val': value})
    for label in ('LABEL', 'MODULE'):
        tree.find(f'TOP_MODULE/{label}').text = 'road_ddr_selftest_top'
    data = ET.tostring(tree, encoding='unicode').replace('UsedInP&amp;R', 'UsedInP&R')
    (work/'road_ddr_selftest_top.al').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+data, encoding='utf-8')
    for name in ('build.tcl', 'board.sdc'):
        shutil.copyfile(ROOT/'build'/name, work/name)
    shutil.copyfile(ROOT.parent/'board_key4_c7_20261010/board.adc', work/'board.adc')
    save(work/'source_hashes.json', {str(path): sha(path) for path in paths})
    output = command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe', 'build.tcl'],
                     work, 'td', allowed=(0, 1, 2))
    original_changed = [name for name, digest in inputs.items() if sha(name) != digest]
    save(work/'original_ip_check.json', {'checked': len(inputs), 'changed': original_changed})
    assert not original_changed, original_changed
    check()
    assert 'DDR_PHYSICAL_COMPLETE' in output, f'Physical incomplete: {work}'


def collect():
    """Keep measured implementation and checker failures, not a board PASS."""
    check()
    physical_work = ROOT/'physical_attempt2'
    assert 'DDR_PHYSICAL_COMPLETE' in (physical_work/'td.log').read_text(encoding='utf-8')
    inputs = json.loads((physical_work/'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(name) == digest for name, digest in inputs.items())
    stats, worst, violations = Counter(), {}, []
    current, group = {}, ''
    for line in (physical_work/'all_endpoints.timing').open(encoding='utf-8'):
        match = re.match(r'Path Group\s*:\s*(.+)', line)
        if match:
            group = match[1]
        match = re.match(r'Slack\s*:\s*([-\d.]+)ns', line)
        if match:
            current = {'slack_ns': float(match[1]), 'group': group}
        for label, key in [('Begin Point', 'begin'), ('End Point', 'end'), ('Check Type', 'type'), ('Process', 'process')]:
            match = re.match(label + r'\s*:\s*(.+)', line)
            if match and current:
                current[key] = match[1]
                if key == 'process':
                    kind = current['type']
                    stats[kind] += 1
                    if kind not in worst or current['slack_ns'] < worst[kind]['slack_ns']:
                        worst[kind] = dict(current)
                    if current['slack_ns'] < 0:
                        violations.append(dict(current))
                    current = {}
    assert len(violations) == 184, len(violations)
    assert Counter(item['type'] for item in violations) == {'setup': 183, 'hold': 1}
    save(ROOT/'violating_paths.json', violations)
    assert all(('u_ddr2/usr_clk' in item['group']) and ('clkc[4]' in item['group']) for item in violations)
    save(ROOT/'physical_summary.json', {'physical_complete': True, 'timing_pass': False,
         'resources_including_ip_hdmi': {'slice': 3922, 'eram': 5, 'dsp': 0, 'pll': 3,
                                       'logical_io_bits': 51, 'package_pad_count': 10},
         'sta_coverage_percent': 92.69, 'corners': 'Slow/Fast Max/Min enabled',
         'path_records_by_check': stats, 'worst': worst, 'violating_paths': violations,
         'source_hashes': inputs, 'no_bitstream_generated': True})
    gate_work = max((path for path in ROOT.glob('gate*') if (path/'source_hashes.json').exists() and
                    (path/'tests.json').exists()), key=lambda path: path.stat().st_mtime)
    strict = {}
    for name in ('rtl', 'tests'):
        result = json.loads((gate_work/f'{name}.json').read_text(encoding='utf-8'))
        findings = result['findings']
        strict[name] = {'errors': result['errors'], 'warnings': result['strict_warnings'],
                        'checks': result['checks'], 'rules': Counter(item.get('rule', '') for item in findings)}
        save(ROOT/f'strict_{name}_semantic_review.json', [item for item in findings if any(word in item.get('rule', '')
             for word in ('width', 'driver', 'overflow', 'fsm', 'reset', 'rst_', 'loop', 'latch'))])
    strict['report_directory'] = str(gate_work)
    save(ROOT/'strict_summary.json', strict)
    receipt = json.loads((ROOT/'simulation_attempt3/receipt.json').read_text(encoding='utf-8'))
    assert len(receipt['cases']) == 17 and all(item['passed'] for item in receipt['cases'])
    save(ROOT/'status.json', {'status': 'PHYSICAL_COMPLETE_DISPLAY_CDC_TIMING_NOT_CLOSED',
         'requester_tests': '17/17 controlled endpoint; not DDR model',
         'display_cdc': json.loads((ROOT/'display_simulation/receipt.json').read_text(encoding='utf-8')),
         'board_readback': 'NOT_RUN', 'full_device_simulation': 'MODEL_MISSING',
         'bitstream': 'NOT_GENERATED', 'strict_delivery': False,
         'next_decision': 'Bounded display CDC timing treatment; no timing exception applied yet',
         'old_files': json.loads((ROOT/'frozen_check.json').read_text(encoding='utf-8'))})
    manifest_paths = list((ROOT/'rtl').rglob('*')) + list((ROOT/'tests').glob('*')) + list((ROOT/'build').glob('*'))
    manifest_paths += [ROOT/'run.py', ROOT/'reference.py', ROOT/'requirements.json', ROOT/'status.json',
                       ROOT/'physical_summary.json', ROOT/'strict_summary.json',
                       ROOT/'DDR板上自检_执行报告与下一步.md']
    save(ROOT/'artifact_manifest.json', {str(path): sha(path) for path in manifest_paths if path.is_file()})
    print(json.dumps({'worst': {kind: item['slack_ns'] for kind, item in worst.items()},
                      'violation_types': Counter(item['type'] for item in violations),
                      'strict_errors': {name: strict[name]['errors'] for name in ('rtl', 'tests')}}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    ast.parse(Path(__file__).read_text(encoding='utf-8'))
    parser = argparse.ArgumentParser(description=__doc__)
    os.chdir(ROOT)
    parser.add_argument('action', choices=('prepare', 'dependencies', 'simulate', 'gate', 'specifications', 'display', 'physical', 'collect', 'check'))
    globals()[parser.parse_args().action]()
