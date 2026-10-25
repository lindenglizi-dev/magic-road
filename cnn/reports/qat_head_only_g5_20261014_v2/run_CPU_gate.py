"""One owned CPU restore gate; capture native failures without automatic retries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import psutil

from cnn.hw_validation.production import train_qat_head_only as runner
from cnn.run_post_review_s import worker_environment
from cnn.train import sha256


def main():
    if (os.environ.get('CUDA_VISIBLE_DEVICES') != '-1'
            or os.environ.get('PYTORCH_NVML_BASED_CUDA_CHECK') != '1'):
        raise RuntimeError('Explicit hidden-CPU/NVML-check environment required')
    folder = runner.OUT / 'CPU_launch_v1'
    folder.mkdir(exist_ok=False)
    sources = [Path(runner.__file__), Path(runner.__file__).with_name('test_train_qat_head_only.py'),
               Path(__file__)]
    hashes = {str(path): sha256(path) for path in sources}
    for path, digest in hashes.items():
        target = folder / Path(path).name
        shutil.copyfile(path, target)
        if sha256(target) != digest:
            raise ValueError('Launcher source snapshot mismatch')
    command = [sys._base_executable, '-u', '-B', '-X', 'faulthandler', '-m',
               'cnn.hw_validation.production.train_qat_head_only', 'check']
    receipt = dict(command=command, source_sha256=hashes, cpu_only=True, automatic_retry=False,
        environment={name: os.environ.get(name) for name in ('CUDA_VISIBLE_DEVICES',
            'PYTORCH_NVML_BASED_CUDA_CHECK', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'PYTHONPATH')})
    runner.base.save(folder / 'pre_run.json', receipt)
    started, peak_rss = time.perf_counter(), 0
    minimum_available_ram = psutil.virtual_memory().available
    with (folder / 'stdout.log').open('x') as stdout, (folder / 'stderr.log').open('x') as stderr:
        child = subprocess.Popen(command, cwd=runner.base.PROJECT, env=worker_environment(),
            stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps(dict(event='head_only_CPU_gate_started', pid=child.pid)), flush=True)
        while child.poll() is None:
            if time.perf_counter() - started > 300:
                child.terminate()
                child.wait(timeout=20)
                receipt['diagnostic_timeout'] = True
                break
            try:
                peak_rss = max(peak_rss, psutil.Process(child.pid).memory_info().rss)
                minimum_available_ram = min(minimum_available_ram, psutil.virtual_memory().available)
            except psutil.NoSuchProcess:
                pass
            time.sleep(1)
    receipt.update(pid=child.pid, exit_code=child.returncode, seconds=time.perf_counter() - started,
        peak_rss_bytes=peak_rss, minimum_sampled_available_RAM_bytes=minimum_available_ram,
        sources_unchanged=all(sha256(Path(path)) == digest for path, digest in hashes.items()),
        pass_receipt_exists=(runner.CHECK_DIR / 'CPU_resume_check.json').is_file())
    runner.base.save(folder / 'result.json', receipt)
    print(json.dumps(receipt), flush=True)
    if child.returncode != 0 or not receipt['pass_receipt_exists'] or not receipt['sources_unchanged']:
        raise RuntimeError('CPU head-only gate failed; do not start GPU or automatically retry')


if __name__ == '__main__':
    main()
