"""Record the portless-TB spec limitation and render its two timing diagrams."""
import json
import os
import sys

import run

ROOT = run.ROOT
os.chdir(ROOT)
run.run.check()
work = run.run.fresh('specification')
sys.path.insert(0, str(run.run.SKILL))
from scripts.python.toolchain.wavedrom_runtime import render_waveform

waves = {
    'write': {'signal': [
        {'name': 'clk', 'wave': 'p.......'},
        {'name': 'req_valid', 'wave': '010.....'},
        {'name': 'req_ready', 'wave': '1.0.....'},
        {'name': 'awvalid', 'wave': '0.1.0...'},
        {'name': 'awready', 'wave': '0..10...'},
        {'name': 'wvalid', 'wave': '0...1.0.'},
        {'name': 'wready', 'wave': '0....10.'}],
        'head': {'text': 'Schematic: W presented after AW acceptance; independent stalls'}},
    'read': {'signal': [
        {'name': 'clk', 'wave': 'p.........'},
        {'name': 'arvalid', 'wave': '01.0......'},
        {'name': 'arready', 'wave': '0.10......'},
        {'name': 'rvalid', 'wave': '0..10.....'},
        {'name': 'result_valid', 'wave': '0....1..0.'},
        {'name': 'result_ready', 'wave': '0......10.'}],
        'head': {'text': 'Schematic: delayed return and held result; not fixed DDR latency'}},
}
module = {
    'name': 'tb_paxi_boundary_mask', 'feature': 'ddr_offline',
    'rtl_path': 'tb_paxi_boundary_mask.v', 'description': __doc__,
    'interfaces': {'ports': []},
    'clock': {'domains': 'Single 100 MHz simulated user clock'},
    'reset': {'assertion': 'Coordinated asynchronous reset of bridge and endpoint',
              'release': 'Three held clock edges, released at falling edge'},
    'behavior': ['Load six-field vectors; compare independent sparse memory.',
                 'Three stall modes, invalid rejection, six long cancellation cases.'],
    'constraints': ['This top is a portless non-synthesizable testbench.',
                    'Commit is conditional endpoint evidence, not vendor completion.'],
    'corner_cases': ['High-bit aliases, byte masks, stalled requests, late returns.'],
    'verification_cases': ['1102 vectors per mode and original bridge regression.'],
    'timing_diagrams': [dict(id=name, title=name, scenario=name,
                           description='Protocol schematic, not a measured trace', wavejson=wave)
                       for name, wave in waves.items()],
}
run.run.save(work / 'contract.json', {'modules': [module]})
entry = (f'import sys;sys.path.insert(0,{str(run.run.SKILL)!r});'
         'from scripts.python.workflow.cli import main;raise SystemExit(main())')
output = run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry,
    'write-spec', '--spec', work / 'contract.json', '--source',
    ROOT / 'tests/tb_paxi_boundary_mask.v', '--out-dir', work, '--no-state'],
    ROOT, str(work.relative_to(ROOT) / 'canonical'), allowed=(0, 1, 2))
receipt = {'canonical_log': str(work / 'canonical.log'),
    'manual_companion': str(ROOT / 'tests/tb_paxi_boundary_mask_spec.md'), 'rendered': []}
command = json.loads((work / 'canonical.command.json').read_text(encoding='utf-8'))
receipt['canonical_passed'] = command['returncode'] == 0
if not receipt['canonical_passed']:
    assert 'ports must be non-empty' in output, output
    receipt['limitation'] = 'Canonical schema rejects portless TB; no fake ports added.'
for name, wave in waves.items():
    path = work / f'{name}.json5'
    run.run.save(path, wave)
    receipt['rendered'].append(render_waveform(path, work / f'{name}.svg'))
run.run.save(work / 'receipt.json', receipt)
run.run.check()
print(json.dumps(receipt, ensure_ascii=False, indent=2))
