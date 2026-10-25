"""Launch exactly one version-control diagnostic with permanent native logs."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

PROJECT = Path(__file__).resolve().parents[3]
ROOT = PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1'
RUNTIME = PROJECT.parents[1] / '.tools/road_yolo_numpy_235_20261014'
SOURCE = PROJECT / 'cnn/hw_validation/production/probe_qat_numpy235.py'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    folder = ROOT / 'numpy235_launch'
    folder.mkdir(exist_ok=False)
    source_hash = digest(SOURCE)
    shutil.copyfile(SOURCE, folder / SOURCE.name)
    command = [sys._base_executable, '-u', '-B', '-X', 'faulthandler', str(SOURCE),
               '--numpy-expected', '2.3.5', '--numpy-runtime', str(RUNTIME)]
    site = Path(sys.executable).parent.parent / 'Lib/site-packages'
    environment = dict(os.environ, CUDA_VISIBLE_DEVICES='-1',
        PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='2', MKL_NUM_THREADS='2',
        PYTHONPATH=os.pathsep.join(map(str, (RUNTIME, site, PROJECT))))
    started = time.perf_counter()
    with (folder / 'stdout.log').open('x') as stdout, (folder / 'stderr.log').open('x') as stderr:
        child = subprocess.Popen(command, cwd=PROJECT, env=environment,
            stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps(dict(event='numpy235_control_started', pid=child.pid)), flush=True)
        try:
            code = child.wait(timeout=300)
        except subprocess.TimeoutExpired:
            child.terminate()
            code = child.wait(timeout=20)
    receipt = dict(command=command, pid=child.pid, exit_code=code,
        seconds=time.perf_counter()-started, source_sha256=source_hash,
        sources_unchanged=digest(SOURCE)==source_hash, CPU_only=True,
        candidate_training=False, automatic_retry=False)
    (folder / 'result.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt), flush=True)
    if code != 0:
        raise RuntimeError('version control failed; do not start GPU training')

if __name__ == '__main__':
    main()
