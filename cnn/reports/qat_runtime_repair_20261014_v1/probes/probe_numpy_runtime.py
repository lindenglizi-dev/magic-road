"""Small native subprocess probes for the Python/NumPy/Torch runtime crash."""
import argparse
import datetime as dt
import faulthandler
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

PROJECT = Path(__file__).resolve().parents[3]
PARENT = PROJECT / 'cnn/runs/qat_frozen_stem_g10_20261014_v1/last.pt'
PARENT_SHA256 = 'f58ce4501104e818c8a6fb10e378d7e7668b937b1332f3530180d4806029d3dd'
DEFAULT_OUTPUT = PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1/probes'


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def emit(event, **fields):
    print(json.dumps(dict(event=event, pid=os.getpid(), monotonic=time.monotonic(), **fields)), flush=True)


def check_parent():
    actual = sha256(PARENT)
    if actual != PARENT_SHA256:
        raise ValueError(f'parent checkpoint changed: {actual}')


def numpy_state_equal(left, right, np):
    return (left[0] == right[0] and np.array_equal(left[1], right[1])
            and left[2:] == right[2:])


def probe_rng(order):
    check_parent()
    emit('probe_start', probe='numpy_rng', order=order)
    if order == 'numpy_first':
        import numpy as np
        emit('numpy_imported', numpy_version=np.__version__)
        import torch
        state = torch.load(PARENT, map_location='cpu', weights_only=False)
    else:
        import torch
        emit('torch_imported', torch_version=torch.__version__)
        state = torch.load(PARENT, map_location='cpu', weights_only=False)
        import numpy as np
        emit('numpy_imported_after_torchload', numpy_version=np.__version__)
    before = np.random.get_state()
    np.random.set_state(state['rng_state']['numpy'])
    restored = np.random.get_state()
    if not numpy_state_equal(restored, state['rng_state']['numpy'], np):
        raise AssertionError('parent NumPy RNG did not restore exactly')
    np.random.set_state(before)
    emit('probe_passed', probe='numpy_rng', order=order,
         torch_version=torch.__version__, numpy_version=np.__version__)


def probe_bridge():
    check_parent()
    emit('probe_start', probe='torch_numpy_bridge')
    import gc
    import numpy as np
    import torch
    if torch.cuda.is_available():
        raise RuntimeError('CUDA must remain hidden')
    checksum = 0.0
    for index in range(2000):
        array = np.arange(256, dtype=np.float32) + index
        tensor = torch.from_numpy(array)
        tensor.add_(1)
        returned = tensor.numpy()
        checksum += float(returned[0] + returned[-1])
        del returned, tensor, array
        if index % 100 == 0:
            gc.collect()
            emit('bridge_progress', iteration=index)
    emit('probe_passed', probe='torch_numpy_bridge', iterations=2000,
         checksum=checksum, torch_version=torch.__version__, numpy_version=np.__version__)


def probe_parent_pickle():
    check_parent()
    emit('probe_start', probe='parent_rng_pickle_restore')
    import gc
    import pickle
    import random
    import numpy as np
    import torch
    if torch.cuda.is_available():
        raise RuntimeError('CUDA must remain hidden')
    state = torch.load(PARENT, map_location='cpu', weights_only=False)
    parent_rng = state['rng_state']
    numpy_rng = pickle.loads(pickle.dumps(parent_rng['numpy'], protocol=pickle.HIGHEST_PROTOCOL))
    torch_rng = pickle.loads(pickle.dumps(parent_rng['torch'], protocol=pickle.HIGHEST_PROTOCOL))
    python_rng = pickle.loads(pickle.dumps(parent_rng['python'], protocol=pickle.HIGHEST_PROTOCOL))
    np.random.set_state(numpy_rng)
    torch.set_rng_state(torch_rng)
    random.setstate(python_rng)
    if not numpy_state_equal(np.random.get_state(), parent_rng['numpy'], np):
        raise AssertionError('pickled NumPy RNG differs')
    if not torch.equal(torch.get_rng_state(), parent_rng['torch']):
        raise AssertionError('pickled Torch RNG differs')
    del state, parent_rng, numpy_rng, torch_rng, python_rng
    gc.collect()
    emit('probe_passed', probe='parent_rng_pickle_restore',
         torch_version=torch.__version__, numpy_version=np.__version__)


def child(name):
    faulthandler.enable(all_threads=True)
    emit('child_ready', probe=name, executable=sys.executable, base_executable=sys._base_executable,
         python=sys.version, cuda_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'))
    if name == 'rng_numpy_first':
        probe_rng('numpy_first')
    elif name == 'rng_torchload_first':
        probe_rng('torchload_first')
    elif name == 'bridge':
        probe_bridge()
    elif name == 'parent_pickle':
        probe_parent_pickle()
    else:
        raise ValueError(name)


def run_one(output, sequence, family, name, repeat, timeout):
    stem = f'{sequence:02d}_{name}_r{repeat}'
    stdout_path, stderr_path = output / f'{stem}.stdout.log', output / f'{stem}.stderr.log'
    command = [sys._base_executable, '-u', '-B', '-X', 'faulthandler', str(Path(__file__).resolve()),
               'child', '--probe', name]
    environment = os.environ.copy()
    python_path = [str(Path(sys.prefix) / 'Lib/site-packages'), str(PROJECT)]
    if environment.get('PYTHONPATH'):
        python_path.append(environment['PYTHONPATH'])
    environment.update(CUDA_VISIBLE_DEVICES='-1', PYTHONDONTWRITEBYTECODE='1',
                       PYTHONFAULTHANDLER='1', OMP_NUM_THREADS='2', MKL_NUM_THREADS='2',
                       PYTHONPATH=os.pathsep.join(python_path))
    started = dt.datetime.now(dt.timezone.utc).astimezone().isoformat()
    with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
        process = subprocess.Popen(command, cwd=PROJECT, env=environment, stdout=stdout, stderr=stderr)
        timed_out = False
        try:
            exit_code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            exit_code = process.wait(timeout=10)
    result = dict(sequence=sequence, family=family, probe=name, repeat=repeat,
        pid=process.pid, command=command, started_at=started,
        finished_at=dt.datetime.now(dt.timezone.utc).astimezone().isoformat(),
        timeout_seconds=timeout, timed_out=timed_out, exit_code=exit_code,
        exit_code_windows_hex=f'0x{exit_code & 0xffffffff:08x}',
        stdout=str(stdout_path.relative_to(PROJECT)).replace('\\', '/'),
        stderr=str(stderr_path.relative_to(PROJECT)).replace('\\', '/'),
        stdout_sha256=sha256(stdout_path), stderr_sha256=sha256(stderr_path))
    (output / f'{stem}.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def matrix(output, repeats, timeout):
    check_parent()
    if not 1 <= repeats <= 2 or not 1 <= timeout <= 45:
        raise ValueError('repeats and timeout exceed bounded probe contract')
    output.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    snapshot = output / 'probe_numpy_runtime.py'
    shutil.copyfile(source, snapshot)
    plan = [('numpy_rng', 'rng_numpy_first'), ('numpy_rng', 'rng_torchload_first'),
            *[('torch_numpy_bridge', 'bridge')] * repeats,
            *[('parent_rng_pickle_restore', 'parent_pickle')] * repeats]
    results = [run_one(output, index, family, name, occurrence, timeout)
               for index, (family, name) in enumerate(plan, 1)
               for occurrence in [sum(1 for prior_family, prior_name in plan[:index]
                                  if (prior_family, prior_name) == (family, name))]]
    summary = dict(format='road-yolo-numpy-runtime-probes-v1', passed=all(
        row['exit_code'] == 0 and not row['timed_out'] for row in results),
        parent_checkpoint=str(PARENT.relative_to(PROJECT)).replace('\\', '/'),
        parent_checkpoint_sha256=PARENT_SHA256, source_sha256=sha256(source),
        source_snapshot_sha256=sha256(snapshot), python_executable=sys.executable,
        python_base_executable=sys._base_executable, repeats=repeats, timeout_seconds=timeout,
        cuda_visible_devices_children='-1', no_gpu=True, no_training=True,
        results=results)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('matrix', 'child'))
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--probe', choices=('rng_numpy_first', 'rng_torchload_first', 'bridge', 'parent_pickle'))
    parser.add_argument('--repeats', type=int, default=2)
    parser.add_argument('--timeout-seconds', type=int, default=45)
    args = parser.parse_args()
    if args.action == 'child':
        if args.probe is None:
            parser.error('--probe is required for child')
        child(args.probe)
    else:
        matrix(args.output, args.repeats, args.timeout_seconds)


if __name__ == '__main__':
    main()
