"""Test the unchanged conditional bridge; all writes stay in this experiment."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'ddr_board_selftest_20261013'
CDC = ROOT.parent / 'ddr_display_cdc_20261013'
PROJECT = ROOT.parents[4]
DDR = PROJECT / 'cnn/hw_validation/ddr'

# Reuse the previous local-only command/receipt helpers, not its build flow.
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('frozen_ddr_helpers', BASE / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
run.ROOT = ROOT


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


run.sha = sha


def prepare():
    assert not (ROOT / 'frozen.json').exists(), 'Use check after initial freeze'
    frozen = {}
    for name in ('frozen.json', 'artifact_hashes.json'):
        path = CDC / name
        frozen.update(json.loads(path.read_text(encoding='utf-8')))
        frozen[str(path)] = sha(path)
    paths = list(DDR.glob('*')) + [BASE / 'run.py',
        PROJECT / 'cnn/hw_validation/production/graph_artifacts/graph.json']
    # Only production source inputs, not another chat's active report directory.
    paths += list((PROJECT / 'user_source').rglob('*'))
    for path in paths:
        if path.is_file():
            frozen[str(path)] = sha(path)
    run.save(ROOT / 'frozen.json', frozen)
    run.check()
    run.dependencies()
    print(f'FROZEN {len(frozen)} files; production/old evidence unchanged')


def reference():
    run.check()
    result = run.reference.generate(ROOT)
    # Existing cancellation reference has its own executable assertions.
    text = run.command([sys.executable, '-B', '-X', 'utf8',
                        DDR / 'paxi_single_outstanding_model.py'], ROOT, 'legacy_reference')
    assert 'Python behavior reference: PASS' in text
    for path in (ROOT / 'reference.py', ROOT / 'run.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    print(json.dumps(result, ensure_ascii=False))
    run.check()


def gate():
    run.check()
    work = run.fresh('gate')
    paths = list((ROOT / 'tests').glob('*.v'))
    assert paths
    run.save(work / 'source_hashes.json', {str(path): sha(path) for path in paths})
    entry = (f'import sys;sys.path.insert(0,{str(run.SKILL)!r});'
             'from scripts.python.validation.generated_deliverable_gate import main;'
             'raise SystemExit(main())')
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry,
        ROOT / 'tests', '--include-testbench', '--external-interface-source',
        DDR / 'paxi_single_outstanding_bridge.v', '--json', work / 'tests.json',
        '--markdown', work / 'tests.md'], work, 'tests', allowed=(0, 1, 2))
    assert (work / 'tests.json').exists(), 'Checker failed to write a receipt'
    run.check()
    print(f'Strict diagnostics preserved: {work}')


def simulate():
    run.check()
    work = run.fresh('simulation')
    inputs = [ROOT / name for name in ('reference.py', 'run.py', 'reference.json',
              'vectors.txt', 'addresses.hex', 'address_audit.json')]
    inputs += [ROOT / 'tests/tb_paxi_boundary_mask.v',
               DDR / 'paxi_single_outstanding_bridge.v',
               DDR / 'tb_paxi_single_outstanding_bridge.v']
    run.save(work / 'source_hashes.json', {str(path): sha(path) for path in inputs})
    for path in inputs:
        shutil.copyfile(path, work / path.name)
    tools = [run.MSIM / f'{name}.exe' for name in ('vlib', 'vlog', 'vsim')]
    run.save(work / 'tool_hashes.json', {str(path): sha(path) for path in tools})
    run.command([tools[0], 'work'], work, 'vlib')
    run.command([tools[1], '-work', 'work', 'paxi_single_outstanding_bridge.v',
        'tb_paxi_boundary_mask.v', 'tb_paxi_single_outstanding_bridge.v'], work, 'vlog')
    counts = json.loads((work / 'reference.json').read_text(encoding='utf-8'))['counts']
    results = []
    cases = [('legacy', 'tb_paxi_single_outstanding_bridge', [],
              'H1-B isolated PAXI bridge PASS')]
    cases += [(f'mode_{mode}', 'tb_paxi_boundary_mask',
               [f'+MODE={mode}', f'+COUNT={counts["vectors"]}',
                f'+SLOTS={counts["address_slots_total_including_invalid"]}'], 'PAXI_BOUNDARY_PASS')
              for mode in range(3)]
    for name, top, plusargs, marker in cases:
        output = run.command([tools[2], '-c', '-lib', 'work', top, *plusargs,
            '-do', 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],
            work, name, allowed=(0, 1, 2))
        passed = marker in output and not re.search(r'\*\* (?:Fatal|Error):|PAXI_BOUNDARY_FAIL| > ERR:', output)
        results.append({'name': name, 'passed': passed,
            'summary': [line for line in output.splitlines()
                        if marker in line or 'SUMMARY' in line or '** Fatal:' in line]})
        run.save(work / 'receipt.json', {'scope': 'Conditional endpoint only, not actual DDR',
            'cases': results, 'all_passed': len(results) == len(cases) and all(x['passed'] for x in results)})
        print(f'{name}: {"PASS" if passed else "FAIL"}', flush=True)
        assert passed, f'Retained failure: {work / (name + ".log")}'
    assert all(sha(name) == digest for name, digest in
               json.loads((work / 'source_hashes.json').read_text(encoding='utf-8')).items())
    run.check()


def finish():
    run.check()
    sims = sorted(ROOT.glob('simulation*'), key=lambda path: path.stat().st_mtime)
    assert sims
    work = sims[-1]
    receipt = json.loads((work / 'receipt.json').read_text(encoding='utf-8'))
    assert receipt['all_passed'], 'Newest simulation did not pass'
    gates = sorted(ROOT.glob('gate*'), key=lambda path: path.stat().st_mtime)
    assert gates and (gates[-1] / 'tests.json').exists()
    result = {'status': 'OFFLINE_CONDITIONAL_PASS_BOARD_PENDING',
        'simulation': str(work), 'simulation_cases': receipt['cases'],
        'reference': json.loads((ROOT / 'reference.json').read_text(encoding='utf-8'))['counts'],
        'strict_report': str(gates[-1] / 'tests.json'),
        'strict_delivery': False, 'hardware_modified': False, 'new_physical_run': False,
        'production_modified': False, 'training_started': False,
        'board_accessed': False, 'bitstream_generated': False, 'flash_written': False,
        'real_ddr_visibility': 'UNPROVEN; i_commit_confirmed is endpoint-test-only',
        'real_memory_capacity_and_video_concurrency': 'NOT_TESTED',
        'frozen': json.loads((ROOT / 'frozen_check.json').read_text(encoding='utf-8'))}
    run.save(ROOT / 'status.json', result)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('simulation_cases', 'frozen')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'reference', 'gate', 'simulate', 'check', 'finish'])
    args = parser.parse_args()
    if args.stage == 'check':
        run.check()
    else:
        globals()[args.stage]()
