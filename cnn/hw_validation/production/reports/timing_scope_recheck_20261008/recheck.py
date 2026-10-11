"""Isolated read-back of frozen TD evidence; no RTL or constraint changes."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'dynamic_control_timing_20261008'
TD = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe')
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def publish(path, data):
    path = path.resolve()
    if not path.is_relative_to(HERE) or path.parent == HERE.parent:
        raise ValueError('Output outside new validation directory')
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)


def verify(manifest):
    bad = [name for name, value in manifest.items()
           if not Path(name).is_file() or digest(Path(name)) != value]
    if bad:
        raise RuntimeError(f'Frozen input changed: {bad}')
    return len(manifest)


def phase_dir(label):
    if label not in ('probe', 'inventory', 'restore', 'restore_check', 'reports', 'closure', 'endpoint_probe', 'precise', 'precise_fixed', 'complete_sources', 'physical_sources'):
        raise ValueError('Phase not in explicit whitelist')
    target = (HERE / label).resolve()
    if target.parent != HERE or target.exists():
        raise ValueError('Phase output outside root or already exists')
    return target


def initialize():
    if (HERE / 'frozen_inputs.json').exists():
        raise ValueError('Refuse to replace freeze')
    receipt = json.loads((OLD / 'execution_receipt.json').read_text(encoding='utf-8'))
    frozen = {str((OLD / name).resolve()): value for name, value in receipt['hashes'].items()}
    for name, value in json.loads((OLD / 'frozen.json').read_text(encoding='utf-8')).items():
        frozen[str((OLD.parent / name).resolve())] = value
    frozen[str(OLD / 'execution_receipt.json')] = digest(OLD / 'execution_receipt.json')
    count = verify(frozen)
    publish(HERE / 'frozen_inputs.json', frozen)
    snapshot = HERE / 'snapshot'
    snapshot.mkdir()
    for name in ('pr.db', 'shell.sdc', 'shell.adc', 'routed_netlist.v', 'build.tcl'):
        shutil.copy2(OLD / 'candidate/physical' / name, snapshot / name)
    rtl = snapshot / 'rtl'
    rtl.mkdir()
    for source in (OLD / 'candidate/rtl').glob('*.v'):
        shutil.copy2(source, rtl / source.name)
    shutil.copy2(OLD / 'road_dynamic_low_io_top.v', rtl / 'road_dynamic_low_io_top.v')
    publish(HERE / 'snapshot_hashes.json', {str(p): digest(p) for p in snapshot.rglob('*') if p.is_file()})
    publish(HERE / 'initial_receipt.json', {
        'checked_original_files': count, 'td_path': str(TD), 'td_sha256': digest(TD),
        'device': 'PH1P35MDG324', 'speed': '-3', 'clock_ns': 10,
        'action': 'existing routed database timing read-back only',
        'no_rtl_sdc_synthesis_place_route_bitstream_training': True})
    print('INITIAL_FREEZE_PASS', count)


def run_phase(label):
    frozen = json.loads((HERE / 'frozen_inputs.json').read_text(encoding='utf-8'))
    snapshot = json.loads((HERE / 'snapshot_hashes.json').read_text(encoding='utf-8'))
    verify(frozen)
    verify(snapshot)
    destination = phase_dir(label)
    source = HERE / (label + '.tcl')
    if not source.is_file():
        raise ValueError('Missing reviewed Tcl source')
    destination.mkdir()
    shutil.copy2(source, destination / 'run.tcl')
    with (destination / 'td.log').open('x', encoding='utf-8') as log:
        process = subprocess.run([str(TD)], cwd=destination,
                                 input='source run.tcl\nexit\n', text=True,
                                 stdout=log, stderr=subprocess.STDOUT)
    original_count = verify(frozen)
    verify(snapshot)
    log_text = (destination / 'td.log').read_text(encoding='utf-8', errors='replace')
    completed = 'A_PHASE_COMPLETE' in log_text
    publish(destination / 'receipt.json', {
        'phase': label, 'returncode': process.returncode, 'completion_marker': completed,
        'original_files_unchanged': original_count, 'snapshot_unchanged': len(snapshot),
        'script_sha256': digest(source), 'log_sha256': digest(destination / 'td.log')})
    if process.returncode != 0 or not completed:
        raise RuntimeError(f'TD phase failed; preserve {destination}/td.log')
    print('PHASE_EXECUTED_NOT_SIGNOFF', label, 'ORIGINAL_UNCHANGED', original_count)


def guard_test():
    for label in ('../candidate', str(OLD), '', 'reports/../probe'):
        try:
            phase_dir(label)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsafe phase accepted')
    try:
        publish(OLD / 'forbidden_test.json', {})
    except ValueError:
        pass
    else:
        raise AssertionError('Unsafe output accepted')
    for label in ('probe', 'inventory', 'restore', 'restore_check', 'reports', 'closure', 'endpoint_probe', 'precise', 'precise_fixed', 'complete_sources', 'physical_sources'):
        if (HERE / label).exists():
            try:
                phase_dir(label)
            except ValueError:
                pass
            else:
                raise AssertionError('Existing output accepted')
    print('GUARD_TEST_PASS traversal absolute existing output rejected')


def static_gate():
    frozen = json.loads((HERE / 'frozen_inputs.json').read_text(encoding='utf-8'))
    verify(frozen)
    destination = HERE / 'static_gate'
    destination.mkdir()
    with (destination / 'gate.log').open('x', encoding='utf-8') as log:
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-m',
            'scripts.python.validation.generated_deliverable_gate', str(HERE / 'snapshot/rtl'),
            '--json', str(destination / 'gate.json'), '--markdown', str(destination / 'gate.md')],
            cwd=HERE, env={**os.environ, 'PYTHONPATH': str(SKILL)},
            stdout=log, stderr=subprocess.STDOUT)
    verify(frozen)
    if result.returncode not in (0, 1):
        raise RuntimeError('Static gate invocation failed; keep log')
    gate = json.loads((destination / 'gate.json').read_text(encoding='utf-8'))
    publish(destination / 'receipt.json', {'returncode': result.returncode,
        'errors': gate['errors'], 'strict_warnings': gate['strict_warnings'],
        'checks': {key: value['status'] for key, value in gate['checks'].items()},
        'source_hashes': {str(p): digest(p) for p in (HERE / 'snapshot/rtl').glob('*.v')}})
    print('STRICT_GATE', gate['errors'], gate['strict_warnings'])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: recheck.py init|check|selftest|probe|inventory|restore|reports')
    action = sys.argv[1]
    if action == 'init':
        initialize()
    elif action == 'check':
        print('FREEZE_CHECK_PASS', verify(json.loads((HERE / 'frozen_inputs.json').read_text(encoding='utf-8'))))
        print('SNAPSHOT_CHECK_PASS', verify(json.loads((HERE / 'snapshot_hashes.json').read_text(encoding='utf-8'))))
    elif action == 'selftest':
        guard_test()
    elif action == 'gate':
        static_gate()
    else:
        run_phase(action)
