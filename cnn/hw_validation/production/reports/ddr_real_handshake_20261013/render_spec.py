"""Render protocol sketches; retain the canonical portless-TB limitation."""
import json
import os
import sys

import run

ROOT = run.ROOT
os.chdir(ROOT)
run.helper.check()
work = run.helper.fresh('specification')
sys.path.insert(0, str(run.helper.SKILL))
from scripts.python.toolchain.wavedrom_runtime import render_waveform

waves = {}
for gap in range(3):
    waves[f'gap{gap}'] = {'signal': [
        {'name': 'dhi_clk', 'wave': 'p.......'},
        {'name': 'AWVALID', 'wave': '010.....'},
        {'name': 'AWREADY', 'wave': '1.......'},
        {'name': 'WVALID', 'wave': ('010.....', '0.10....', '0..10...')[gap]},
        {'name': 'WREADY', 'wave': '1.......'}],
        'head': {'text': f'AW/W gap {gap}; illustrative ready-high case, not measured latency'}}
module = {
    'name': 'tb_ddr_real_handshake', 'feature': 'vendor_paxi_observation',
    'rtl_path': 'tb_ddr_real_handshake.v', 'description': __doc__,
    'interfaces': {'ports': []},
    'clock': {'domains': '100 MHz reference; vendor-generated DHI and DDR clocks'},
    'reset': {'assertion': 'Hold sys_rst_n low for 2 us',
              'release': 'Release on falling ref_clk edge, wait for real PHY ready'},
    'behavior': ['Three single-beat writes, one read, no memory data oracle.'],
    'constraints': ['Portless simulation top; vendor sources and parameters unchanged.',
                    'B and command pins are observations, not commit guarantees.'],
    'corner_cases': ['Separate AW/W acceptance; W gap 0/1/2; unknown read data.'],
    'verification_cases': ['Request hold, owner conservation, bounded observation.'],
    'timing_diagrams': [dict(id=name, title=name, scenario=name,
                           description='Schematic, not a measured trace', wavejson=wave)
                       for name, wave in waves.items()]}
run.helper.save(work / 'contract.json', {'modules': [module]})
entry = (f'import sys;sys.path.insert(0,{str(run.helper.SKILL)!r});'
         'from scripts.python.workflow.cli import main;raise SystemExit(main())')
output = run.helper.command([sys.executable, '-B', '-X', 'utf8', '-c', entry,
    'write-spec', '--spec', work / 'contract.json', '--source',
    ROOT / 'tests/tb_ddr_real_handshake.v', '--out-dir', work, '--no-state'],
    ROOT, str(work.relative_to(ROOT) / 'canonical'), allowed=(0, 1, 2))
result = json.loads((work / 'canonical.command.json').read_text(encoding='utf-8'))
receipt = {'canonical_passed': result['returncode'] == 0, 'rendered': []}
if not receipt['canonical_passed']:
    assert 'ports must be non-empty' in output, output
    receipt['limitation'] = 'Canonical schema rejects portless TB; no fake ports added.'
for name, wave in waves.items():
    path = work / f'{name}.json5'
    run.helper.save(path, wave)
    receipt['rendered'].append(render_waveform(path, work / f'{name}.svg'))
run.helper.save(work / 'receipt.json', receipt)
run.helper.check()
print(json.dumps(receipt, ensure_ascii=False, indent=2))
