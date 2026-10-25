"""Run one full continuity gate after the explicitly verified runtime transition."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import psutil
from cnn.hw_validation.production import train_qat_numpy235 as runner
from cnn.run_post_review_s import worker_environment
from cnn.train import sha256

def main():
    if os.environ.get('CUDA_VISIBLE_DEVICES') != '-1':
        raise RuntimeError('explicit CPU-only environment required')
    runner.OUT.mkdir(exist_ok=True)
    folder = runner.OUT / 'CPU_transition_diagnostic'
    folder.mkdir(exist_ok=False)
    sources = [Path(runner.__file__), Path(runner.__file__).with_name('test_qat_numpy235.py'),
               Path(runner.continuation.__file__), Path(__file__)]
    hashes = {str(path): sha256(path) for path in sources}
    for path, digest in hashes.items():
        target = folder / Path(path).name
        shutil.copyfile(path, target)
        if sha256(target) != digest:
            raise ValueError('pre-run source snapshot differs')
    command = [sys._base_executable, '-u', '-B', '-X', 'faulthandler', '-m',
               'cnn.hw_validation.production.train_qat_numpy235', 'check']
    receipt = dict(command=command, source_sha256=hashes, cpu_only=True,
                   runtime_transition='NumPy2.4.6_to_2.3.5', automatic_retry=False,
                   environment={name: os.environ.get(name) for name in
                       ('CUDA_VISIBLE_DEVICES','OMP_NUM_THREADS','MKL_NUM_THREADS','PYTHONPATH')})
    runner.save(folder / 'pre_run.json', receipt)
    started, peak_rss = time.perf_counter(), 0
    with (folder / 'stdout.log').open('x') as stdout, (folder / 'stderr.log').open('x') as stderr:
        child = subprocess.Popen(command, cwd=runner.base.PROJECT, env=worker_environment(),
            stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps(dict(event='CPU_transition_gate_started', pid=child.pid)), flush=True)
        while child.poll() is None:
            if time.perf_counter()-started > 300:
                child.terminate()
                child.wait(timeout=20)
                receipt['diagnostic_timeout'] = True
                break
            try:
                peak_rss = max(peak_rss, psutil.Process(child.pid).memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            time.sleep(1)
    receipt.update(pid=child.pid, exit_code=child.returncode,
        seconds=time.perf_counter()-started, peak_rss_bytes=peak_rss,
        sources_unchanged=all(sha256(Path(p))==h for p,h in hashes.items()),
        pass_receipt_exists=(runner.CHECK_DIR/'CPU_resume_check.json').is_file())
    runner.save(folder/'result.json', receipt)
    print(json.dumps(receipt), flush=True)
    if child.returncode != 0 or not receipt['pass_receipt_exists']:
        raise RuntimeError('runtime-transition gate failed; no GPU or retry')

if __name__ == '__main__':
    main()
