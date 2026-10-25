"""Bounded local digital verification; retain every attempt and its source/tool closure."""
import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import run

ROOT = Path(__file__).resolve().parent
FROZEN_TIME = ROOT.parent / 'detection_table_cdc_20261015/rtl/road_time_snapshot.v'


def execute(case):
    run.check()
    (ROOT / 'verification').mkdir(exist_ok=True)
    work = run.fresh('verification/' + case)
    top = {'identity': 'tb_road_source_sof_identity', 'overlay': 'tb_road_age_overlay'}[case]
    rtl = [ROOT / 'rtl' / (top.removeprefix('tb_') + '.v')]
    if case == 'identity':
        rtl.append(FROZEN_TIME)
    tb = ROOT / 'tests' / (top + '.v')
    tools = [run.MSIM / (name + '.exe') for name in ('vlib', 'vlog', 'vsim')]
    inputs = [*rtl, tb, ROOT / 'interfaces.json', ROOT / 'verify.py', ROOT / 'run.py',
              Path(run.command.__globals__['__file__']),
              *sorted((ROOT / 'reference').glob('*.*'))]
    closure = {str(path): run.sha(path) for path in inputs if path.is_file()}
    snapshot = work / 'inputs'
    snapshot.mkdir()
    for index, path in enumerate(inputs):
        if path.is_file():
            shutil.copy2(path, snapshot / (str(index) + '_' + path.name))
    tool_hashes = {str(path): run.sha(path) for path in [Path(sys.executable), *tools]}
    receipt = {'case': case, 'sources': closure, 'tools': tool_hashes,
               'boundary': 'digital local ModelSim, no physical CDC or production integration',
               'status': 'RUNNING'}
    run.save(work / 'receipt.json', receipt)
    try:
        reference_output = run.command([sys.executable, '-B', '-X', 'utf8', ROOT / 'reference/reference.py'],
                                       work, 'reference')
        assert 'SOURCE_SOF_REFERENCE_PASS' in reference_output
        if case == 'overlay':
            spec = importlib.util.spec_from_file_location('age_golden', ROOT / 'reference/reference.py')
            reference = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = reference
            spec.loader.exec_module(reference)
            ages = [0, 1996, 1997, 2000, 2001, 9999, 10000, reference.U64,
                    1, 10, 99, 100, 999, 1000, 2345, 6789]
            (work / 'overlay_ages.hex').write_text(''.join(f'{age:016x}\n' for age in ages), encoding='ascii')
            pixels = [str(int(reference.text_pixel(reference.age_label(age), x, y)))
                      for age in ages for y in range(34) for x in range(160)]
            (work / 'overlay_pixels.hex').write_text('\n'.join(pixels) + '\n', encoding='ascii')
            receipt['vectors'] = {name: run.sha(work / name) for name in ('overlay_ages.hex', 'overlay_pixels.hex')}
        run.command([tools[0], 'work'], work, 'vlib')
        run.command([tools[1], '-work', 'work', '-l', 'compile.log', *rtl, tb], work, 'vlog')
        compile_text = (work / 'compile.log').read_text(encoding='utf-8', errors='replace')
        summaries = re.findall(r'Errors:\s*(\d+),\s*Warnings:\s*(\d+)', compile_text)
        assert summaries and all(tuple(map(int, item)) == (0, 0) for item in summaries), compile_text
        output = run.command([tools[2], '-c', '-t', '1ps', '-voptargs=+acc', '-lib', 'work', top,
                              '-l', 'simulation.log', '-do', 'onbreak {quit -code 1}; run -all; quit -code 0'],
                             work, 'vsim')
        marker = 'TB_PASS_' + case.upper()
        assert marker in output and '** Fatal:' not in output and '** Error:' not in output, output[-4000:]
        assert all(run.sha(path) == value for path, value in closure.items()), 'inputs changed during simulation'
        receipt.update(status='PASS', marker=next(line for line in output.splitlines() if marker in line),
                       metrics=[line for line in output.splitlines() if 'TB_METRICS_' in line])
    except BaseException as exc:
        receipt.update(status='FAIL', error=repr(exc))
        raise
    finally:
        run.save(work / 'receipt.json', receipt)
        run.check()
    print(json.dumps({'directory': str(work), 'status': receipt['status'], 'marker': receipt['marker']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('identity', 'overlay', 'all'))
    choice = parser.parse_args().case
    for item in ('identity', 'overlay') if choice == 'all' else (choice,):
        execute(item)
