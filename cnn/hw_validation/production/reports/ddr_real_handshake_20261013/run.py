"""Observe the unchanged vendor PAXI interface without a DRAM data model."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
BASE = ROOT.parent / 'ddr_board_selftest_20261013'
PREVIOUS = ROOT.parent / 'ddr_offline_boundaries_20261013'
STARTUP = ROOT.parent / 'ddr_vendor_startup_20261011'
SOURCE = PROJECT / 'user_source/hdl_source/ph1p35_ddr'
sys.path.insert(0, str(BASE))
definition = importlib.util.spec_from_file_location('local_ddr_helpers', BASE / 'run.py')
helper = importlib.util.module_from_spec(definition)
definition.loader.exec_module(helper)
helper.ROOT = ROOT


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


helper.sha = sha


def prepare():
    assert not (ROOT / 'frozen.json').exists()
    frozen = json.loads((PREVIOUS / 'frozen.json').read_text(encoding='utf-8'))
    for parent in (PREVIOUS, STARTUP):
        for path in parent.rglob('*'):
            if path.is_file() and 'work' not in path.relative_to(parent).parts and path.suffix not in ('.wlf', '.pyc'):
                frozen[str(path)] = sha(path)
    frozen[str(BASE / 'run.py')] = sha(BASE / 'run.py')
    helper.save(ROOT / 'frozen.json', frozen)
    helper.check()
    helper.dependencies()
    # This reference defines stimulus/checks, not undocumented vendor ordering.
    cases = [{'case': index, 'native_address': index * 8,
              'w_presentation': 'with_aw' if index == 0 else f'{index}_cycles_after_aw_accept'}
             for index in range(3)]
    assert len({item['native_address'] for item in cases}) == 3
    assert all(item['native_address'] % 8 == 0 for item in cases)
    helper.save(ROOT / 'reference.json', {
        'clock_period_ps': 10000, 'reset_low_ps': 2000000,
        'cases': cases, 'memory_pass_allowed': False,
        'forbidden': ['force', 'fake read data', 'vendor parameter or port changes', 'fixed-delay commit'],
        'observation': 'AW/W acceptance, internal B and DDR WRITE, AR/R handshake and unknown data',
        'timeout': 'Stop issuing on accepted request timeout; never release or restart an owner',
        'public_gates': ['compile', 'ast', 'readability', 'comment', 'naming', 'profile', 'testbench', 'toolchain']})
    print(f'FROZEN files={len(frozen)}; stimulus reference PASS')


def gate():
    helper.check()
    work = helper.fresh('gate')
    source = ROOT / 'tests/tb_ddr_real_handshake.v'
    helper.save(work / 'source_hashes.json', {str(source): sha(source)})
    entry = (f'import sys;sys.path.insert(0,{str(helper.SKILL)!r});'
             'from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())')
    helper.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, ROOT / 'tests',
        '--include-testbench', '--external-interface-source', SOURCE / 'ddr2/ddr2.v',
        '--json', work / 'tests.json', '--markdown', work / 'tests.md'], work, 'strict', allowed=(0, 1, 2))
    assert (work / 'tests.json').exists()
    helper.check()
    print(f'Strict diagnostic receipt: {work}')


def simulate():
    helper.check()
    work = helper.fresh('simulation')
    fileset = SOURCE / 'ddr2/sim/fileset/fileset_mis.f'
    args = [line.strip().replace('<mis_path>', SOURCE.as_posix())
            for line in fileset.read_text().splitlines()
            if line.strip() and not line.lstrip().startswith(('#', '+define+DDRPHY_ROM_INIT='))]
    cfg = SOURCE / 'ddr2/src/rtl/include/ph1p_mis_define.vh'
    rom = SOURCE / 'ddr2/src/rtl/phy/ddrphy_cfg_rom.txt'
    shutil.copyfile(rom, work / rom.name)
    tb = ROOT / 'tests/tb_ddr_real_handshake.v'
    shutil.copyfile(tb, work / tb.name)
    models = json.loads((ROOT.parent / 'stem_down2_handoff_20261011/simulation_attempt3/receipt.json')
                        .read_text(encoding='utf-8'))['vendor_models']
    sources = [tb, Path(__file__), ROOT / 'reference.json', fileset, cfg, rom]
    sources += [Path(path) for path in args + models if not path.startswith('+')]
    sources += list((SOURCE / 'ddr2/src').rglob('*.vh'))
    source_hashes = {str(path): sha(path) for path in sources}
    helper.save(work / 'source_hashes.json', source_hashes)
    helper.save(work / 'tool_hashes.json', {str(helper.MSIM / f'{name}.exe'):
                sha(helper.MSIM / f'{name}.exe') for name in ('vlib', 'vlog', 'vsim')})
    helper.command([helper.MSIM / 'vlib.exe', 'work'], work, 'vlib')
    helper.command([helper.MSIM / 'vlog.exe', '-work', 'work', *models], work, 'primitives')
    helper.command([helper.MSIM / 'vlog.exe', '-work', 'work', '-sv', '-mfcu', cfg,
                    *args, work / tb.name], work, 'vlog')
    output = helper.command([helper.MSIM / 'vsim.exe', '-c', '-voptargs=+acc', '-lib', 'work',
        'PH1P_PHY_GSR', 'tb_ddr_real_handshake', '-wlf', work / 'handshake.wlf',
        '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; '
               'log /tb_ddr_real_handshake/*; run -all; quit -code 0'],
        work, 'handshake', allowed=(0, 1, 2))
    lines = [line for line in output.splitlines() if 'REAL_' in line]
    changed = [name for name, digest in source_hashes.items() if sha(name) != digest]
    helper.save(work / 'receipt.json', {'scope': 'Unmodified vendor interface observation, no DRAM model',
        'memory_pass': False, 'changed_during_run': changed, 'lines': lines,
        'completed': all(marker in output for marker in ('REAL_SUMMARY', 'REAL_OBSERVATION_COMPLETE'))
                     and not changed and '** Fatal:' not in output and 'REAL_ERROR' not in output})
    print('\n'.join(lines), flush=True)
    helper.check()
    assert not changed, changed


def finish():
    helper.check()
    work = max(ROOT.glob('simulation*'), key=lambda path: path.stat().st_mtime)
    receipt = json.loads((work / 'receipt.json').read_text(encoding='utf-8'))
    execution = json.loads((work / 'handshake.command.json').read_text(encoding='utf-8'))
    gate_dir = max(ROOT.glob('gate*'), key=lambda path: path.stat().st_mtime)
    strict = json.loads((gate_dir / 'tests.json').read_text(encoding='utf-8'))
    assert receipt['completed'] and execution['returncode'] == 0, receipt
    status = {'status': 'REAL_VENDOR_HANDSHAKE_OBSERVED_NOT_MEMORY_PASS',
        'memory_pass': False, 'production_modified': False, 'board_accessed': False,
        'bitstream_generated': False, 'flash_written': False,
        'simulation': str(work), 'observations': receipt['lines'],
        'strict_errors': strict['errors'], 'strict_checks': strict['checks'],
        'strict_delivery': False, 'frozen': json.loads((ROOT / 'frozen_check.json').read_text()),
        'run_seconds': execution['seconds'],
        'limits': ['No DRAM model or read-data truth', 'Internal B is observed, not assigned commit semantics',
                   'Sampled latency is not an all-conditions guarantee', 'No bridge interface changed']}
    helper.save(ROOT / 'status.json', status)
    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ast.parse(Path(__file__).read_text(encoding='utf-8'))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'gate', 'simulate', 'finish', 'check'])
    stage = parser.parse_args().stage
    helper.check() if stage == 'check' else globals()[stage]()
