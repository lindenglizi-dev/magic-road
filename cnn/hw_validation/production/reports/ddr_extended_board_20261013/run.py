"""Independent extended DDR experiment; immutable prior board baseline."""
import argparse
import ast
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET
import reference

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'ddr_display_cdc_20261013'
spec = importlib.util.spec_from_file_location('board_helpers', ROOT.parent / 'ddr_board_selftest_20261013/run.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ROOT = ROOT


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


base.sha = sha
save, check, fresh = base.save, base.check, base.fresh
original_command = base.command


def command(args, work, name, allowed=(0,)):
    if 'td_commands_prompt' in str(args[0]) and str(args[-1]) == 'build.tcl':
        shutil.copyfile(ROOT / 'vectors.hex', work / 'vectors.hex')
        # TD checks the RTL directory before the project directory.
        shutil.copyfile(ROOT / 'vectors.hex', ROOT / 'rtl/vectors.hex')
        inputs = json.loads((work / 'source_hashes.json').read_text(encoding='utf-8'))
        inputs[str(work / 'vectors.hex')] = sha(work / 'vectors.hex')
        inputs[str(ROOT / 'rtl/vectors.hex')] = sha(ROOT / 'rtl/vectors.hex')
        save(work / 'source_hashes.json', inputs)
    return original_command(args, work, name, allowed)


base.command = command


def timing(path):
    # Reuse the corrected parser: ignored paths must not overwrite scored ones.
    spec = importlib.util.spec_from_file_location('cdc_reports', BASE / 'run_cdc.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.timing(path)


def collect():
    check()
    work = max((p for p in ROOT.glob('physical*') if (p/'all_endpoints.timing').exists()), key=lambda p:p.stat().st_mtime)
    assert 'DDR_PHYSICAL_COMPLETE' in (work/'td.log').read_text(encoding='utf-8')
    paths = timing(work/'all_endpoints.timing')
    assert set(paths['worst']) == {'setup', 'hold', 'recovery', 'removal'}
    payload = timing(work/'bounded_payload.timing')
    rows = list(csv.DictReader((work/'display_cdc_mapping.tsv').open(encoding='utf-8'), delimiter='\t'))
    unique_payloads = {(r['source_q'], r['destination_d']) for r in rows if r['kind'] == 'payload'}
    assert payload['records'] == {'setup': len(unique_payloads)}
    sync = {name: timing(work/f'{name}.timing') for name in ('reg_request_meta', 'reg_ack_meta')}
    assert all(v['records'] == {'setup': 1, 'hold': 1} for v in sync.values())
    area = (work/'route.area').read_text(encoding='utf-8')
    resources = {name: int(re.search(r'^#'+name+r'\s+(\d+)', area, re.M)[1]) for name in ('slice','eram','dsp','pll','pad','IO')}
    with (work/'all_endpoints.timing').open(encoding='utf-8') as stream:
        header = ''.join(next(stream) for _ in range(35))
    coverage = float(re.search(r'STA coverage\s*:\s*([\d.]+)%', header)[1])
    checks = (work/'check_timing.rpt').read_text(encoding='utf-8')
    assert 'checking invalid constraint(0)' in checks and 'checking combinational loops(0)' in checks
    sources = json.loads((work/'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(p) == h for p,h in sources.items())
    rom = json.loads((work/'rom_audit.json').read_text(encoding='utf-8'))
    assert rom['passed'] and rom['netlist_sha256'] == sha(work/'routed_netlist.v')
    assert rom['vectors_sha256'] == sha(ROOT/'vectors.hex')
    tests = json.loads((ROOT/'simulation/receipt.json').read_text(encoding='utf-8'))
    assert len(tests['cases']) == 24 and all(c['passed'] for c in tests['cases'])
    display = json.loads((ROOT/'display_simulation/receipt.json').read_text(encoding='utf-8'))
    assert 'captures=60' in display['summary'][0]
    gate = max((p for p in ROOT.glob('gate*') if (p/'tests.json').exists()), key=lambda p:p.stat().st_mtime)
    hashes = json.loads((gate/'source_hashes.json').read_text(encoding='utf-8'))
    assert set(hashes) == {str(p) for folder in ('rtl','tests') for p in (ROOT/folder).glob('*.v')}
    assert all(sha(p) == h for p,h in hashes.items())
    strict = {}
    for name in ('rtl','tests'):
        result = json.loads((gate/f'{name}.json').read_text(encoding='utf-8'))
        strict[name] = {key: result[key] for key in ('errors','strict_warnings','checks','delivery_ready')}
    summary = {'physical_directory':str(work),'all_endpoints':paths,'bounded_payload':payload,
               'synchronizer_stages':sync,'resources_including_ddr_hdmi_test_rom_no_cnn':resources,
               'sta_coverage_percent':coverage,'source_hashes':sources,'strict':strict,
               'gate_directory':str(gate),'requester':tests,'display':display,
               'rom_initialization':rom,'board_readback':'NOT_RUN','bitstream':'NOT_GENERATED'}
    clean = not paths['violations'] and not payload['violations'] and all(not v['violations'] for v in sync.values())
    save(ROOT/'comparison.json',summary)
    save(ROOT/'status.json',{'status':'EXTENDED_DIAGNOSTIC_TIMING_PASS' if clean else 'PHYSICAL_TIMING_FAILED',
                            'whole_system_signoff':False,'strict_delivery':False,'board_readback':'NOT_RUN',
                            'physical_directory':str(work)})
    print(json.dumps({'worst':{k:v['slack_ns'] for k,v in paths['worst'].items()},
                      'violations':len(paths['violations']),'resources':resources,'coverage':coverage}))
    check()


def prepare():
    assert not (ROOT / 'frozen.json').exists()
    frozen = json.loads((BASE / 'frozen.json').read_text(encoding='utf-8'))
    for folder in (BASE, ROOT.parents[2] / 'board_test_20261013_ddr'):
        for path in folder.rglob('*'):
            if path.is_file():
                frozen[str(path)] = sha(path)
    for path in (ROOT.parent / 'ddr_offline_boundaries_20261013').glob('*'):
        if path.is_file():
            frozen[str(path)] = sha(path)
    save(ROOT / 'frozen.json', frozen)
    for folder in ('rtl', 'tests', 'build'):
        (ROOT / folder).mkdir(exist_ok=True)
    shutil.copyfile(BASE / 'rtl/road_ddr_selftest_top.v', ROOT / 'rtl/road_ddr_selftest_top.v')
    shutil.copyfile(BASE / 'tests/tb_ddr_display_cdc.v', ROOT / 'tests/tb_ddr_display_cdc.v')
    for path in (BASE / 'build').glob('*'):
        shutil.copyfile(path, ROOT / 'build' / path.name)
    shutil.copyfile(BASE / 'bitgen.tcl', ROOT / 'bitgen.tcl')
    check()
    base.dependencies()


def simulate():
    check()
    reference.generate(ROOT)
    work = fresh('simulation')
    for name in ('vectors.hex', 'board_vectors.txt'):
        shutil.copyfile(ROOT / name, work / name)
    command([base.MSIM/'vlib.exe', 'work'], work, 'vlib')
    command([base.MSIM/'vlog.exe', '-work', 'work', ROOT/'rtl/road_ddr_selftest.v', ROOT/'tests/tb_ddr_selftest.v'], work, 'vlog')
    cases = json.loads((ROOT / 'tests/cases.json').read_text(encoding='utf-8'))
    results = []
    for case in cases:
        number = case['case']
        output = command([base.MSIM/'vsim.exe', '-c', '-lib', 'work', 'tb_ddr_selftest', f'+CASE={number}',
                          '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],
                         work, f'case_{number:02d}', allowed=(0, 1, 2))
        passed = f'DDR_EXTENDED_PASS case={number} ' in output and '** Fatal:' not in output
        results.append({**case, 'passed': passed, 'summary': [line for line in output.splitlines() if 'DDR_EXTENDED_PASS' in line or '** Fatal:' in line]})
        save(work / 'receipt.json', {'scope': 'Controlled endpoint; not physical DDR simulation', 'cases': results})
        print(f'CASE {number}: {passed}', flush=True)
        assert passed, work
    check()


def bitgen():
    check()
    summary = json.loads((ROOT/'comparison.json').read_text(encoding='utf-8'))
    assert not summary['all_endpoints']['violations'] and not summary['bounded_payload']['violations']
    assert all(not v['violations'] for v in summary['synchronizer_stages'].values())
    physical = Path(summary['physical_directory'])
    assert all(sha(p) == h for p,h in summary['source_hashes'].items())
    assert summary['rom_initialization']['netlist_sha256'] == sha(physical/'routed_netlist.v')
    assert 'DDR_PHYSICAL_COMPLETE' in (physical/'td.log').read_text(encoding='utf-8')
    work = fresh('diagnostic_bitgen')
    tree = ET.fromstring((physical/'road_ddr_selftest_top.al').read_text(encoding='utf-8').replace('UsedInP&R','UsedInP&amp;R'))
    tree.set('Path', work.as_posix())
    (work/'road_ddr_selftest_top.al').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(tree,encoding='unicode').replace('UsedInP&amp;R','UsedInP&R'),encoding='utf-8')
    shutil.copyfile(physical/'pr.db', work/'pr.db')
    shutil.copyfile(ROOT/'bitgen.tcl', work/'bitgen.tcl')
    output = command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe','bitgen.tcl'],work,'td',allowed=(0,1,2))
    assert 'DDR_DIAGNOSTIC_BITGEN_COMPLETE' in output and 'DDR_PAXI_CONNECTIVITY_COMPLETE count=256' in output
    assert not timing(work/'imported.timing')['violations']
    bit = work/'HX1P35A_C7_DDR_EXTENDED.bit'
    assert bit.stat().st_size > 0
    receipt = {'bitstream':str(bit),'sha256':sha(bit),'bytes':bit.stat().st_size,
         'database_sha256':sha(physical/'pr.db'),'vectors_sha256':sha(ROOT/'vectors.hex'),
         'board_status':'NOT_RUN','scope':'Independent SRAM diagnostic; not CNN deployment'}
    save(work/'receipt.json', receipt)
    summary['bitstream'] = receipt
    save(ROOT/'comparison.json',summary)
    status = json.loads((ROOT/'status.json').read_text(encoding='utf-8'))
    status['bitstream'] = receipt
    save(ROOT/'status.json',status)
    print(json.dumps(receipt))
    check()


def finalize():
    check()
    summary = json.loads((ROOT/'comparison.json').read_text(encoding='utf-8'))
    state = json.loads((ROOT/'status.json').read_text(encoding='utf-8'))
    assert summary['bitstream'] == state['bitstream']
    assert sha(state['bitstream']['bitstream']) == state['bitstream']['sha256']
    physical = Path(summary['physical_directory'])
    assert 'HDL-5105' not in (physical/'td.log').read_text(encoding='utf-8')
    assert not summary['all_endpoints']['violations']
    for path in ROOT.glob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'))
    for name in ('DDR扩展验证报告.txt','DDR扩展上板操作.txt'):
        assert (ROOT/name).is_file()
    files = [p for p in ROOT.iterdir() if p.is_file() and p.name != 'artifact_hashes.json']
    for folder in ('rtl','tests','build','gate_attempt2','simulation','display_simulation',
                   physical.name,Path(state['bitstream']['bitstream']).parent.name):
        files += [p for p in (ROOT/folder).rglob('*') if p.is_file()]
    save(ROOT/'artifact_hashes.json',{str(p):sha(p) for p in files})
    print(json.dumps({'artifact_files':len(files),'board_status':'NOT_RUN','bitstream_verified':True}))


if __name__ == '__main__':
    ast.parse(Path(__file__).read_text(encoding='utf-8'))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','simulate','display','gate','physical','check','bitgen','collect','finalize'))
    action = parser.parse_args().action
    if action in ('prepare','simulate','bitgen','collect','finalize'):
        globals()[action]()
    else:
        getattr(base, action)()
