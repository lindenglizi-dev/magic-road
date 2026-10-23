#!/usr/bin/env python3
"""Run standalone IP checks; a Croc-type stub is not a full-SoC validation."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'


def run_step(name, command, timeout, marker=None):
    status, code = 'FAIL', None
    env = os.environ.copy()
    for key in ('TMPDIR', 'TMP', 'TEMP'):
        env[key] = str(REPORTS / 'tmp')
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                text=True, encoding='utf-8', errors='replace',
                                timeout=timeout, env=env)
        output, code = result.stdout + result.stderr, result.returncode
        if code == 0 and (marker is None or marker in output):
            status = 'PASS'
        elif code == 0:
            output += '\nFAIL: expected success marker was not emitted\n'
    except subprocess.TimeoutExpired:
        status, output = 'TIMEOUT', f'Exceeded {timeout} seconds\n'
    except OSError as exc:
        output = f'{exc}\n'
    log = REPORTS / f'{name}.log'
    log.write_text(f'COMMAND: {json.dumps(command)}\nEXIT: {code}\n{output}',
                   encoding='utf-8')
    print(f'{name}: {status} exit={code} ({log.relative_to(ROOT)})')
    return {'name': name, 'status': status, 'returncode': code,
            'command': command, 'log': str(log.relative_to(ROOT))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict', action='store_true',
                        help='Compatibility flag; unavailable tools always fail the gate')
    parser.parse_args()
    (REPORTS / 'tmp').mkdir(parents=True, exist_ok=True)
    steps = [run_step('static', [sys.executable, 'scripts/check_structure.py'], 120),
             run_step('protocol_model', [sys.executable, 'reference/obi_reference.py'],
                      30, 'PASS OBI cycle model:')]
    missing = [name for name in ('iverilog', 'vvp') if not shutil.which(name)]
    if missing:
        steps.append({'name': 'rtl_toolchain', 'status': 'UNAVAILABLE',
                      'missing': missing})
    else:
        sources = ['tb/croc_pkg_stub.sv', 'rtl/mac_array_4x4.sv',
                   'rtl/gemm_mmio_4x4.sv', 'rtl/croc_gemm_obi.sv']
        for top, stem, marker in [
            ('tb_croc_gemm_obi', 'obi_gemm', 'PASS OBI GEMM'),
            ('tb_croc_gemm_obi_stress', 'stress', 'PASS STRESS:')
        ]:
            binary = f'reports/{stem}.vvp'
            compiled = run_step(f'{stem}_compile',
                                [shutil.which('iverilog'), '-g2012', '-s', top,
                                 '-o', binary, *sources, f'tb/{top}.sv'], 120)
            steps.append(compiled)
            if compiled['status'] == 'PASS':
                steps.append(run_step(stem, [shutil.which('vvp'), binary], 30, marker))
            else:
                steps.append({'name': stem, 'status': 'SKIP',
                              'reason': 'Compilation did not pass'})
    failed = any(step['status'] in ('FAIL', 'TIMEOUT') for step in steps)
    passed = all(step['status'] == 'PASS' for step in steps)
    gate = 'RTL_PASS' if passed else ('FAIL' if failed else 'RTL_UNVERIFIED')
    summary = {'gate': gate, 'generated_utc': datetime.now(timezone.utc).isoformat(),
               'scope': 'Standalone IP with Croc-compatible type stub; no CPU/SoC/PPA proof',
               'steps': steps}
    (REPORTS / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n',
                                          encoding='utf-8')
    print(f'{gate}: {summary["scope"]}')
    return 0 if passed else (1 if failed else 2)


if __name__ == '__main__':
    sys.exit(main())
