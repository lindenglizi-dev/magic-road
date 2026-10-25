"""One explicit CPU-only diagnostic retry; never starts GPU training."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import psutil

from cnn.hw_validation.production import train_qat_frozen_stem_continue as runner
from cnn.run_post_review_s import worker_environment
from cnn.train import sha256


def main():
    if os.environ.get('CUDA_VISIBLE_DEVICES') != '-1':
        raise RuntimeError('explicit CPU-only environment required')
    folder = runner.OUT / 'CPU_retry_diagnostic'
    folder.mkdir(exist_ok=False)
    source = Path(runner.__file__)
    test = source.with_name('test_qat_frozen_stem_continue.py')
    hashes = {str(path): sha256(path) for path in (source, test, Path(__file__))}
    for path, digest in hashes.items():
        target = folder / Path(path).name
        shutil.copyfile(path, target)
        if sha256(target) != digest:
            raise ValueError('pre-run source snapshot differs')
    command = [sys._base_executable, '-u', '-B', '-X', 'faulthandler', '-m',
               'cnn.hw_validation.production.train_qat_frozen_stem_continue', 'check']
    receipt = dict(command=command, source_sha256=hashes,
                   cpu_only=True, explicit_retry=True, automatic_retry=False,
                   diagnostic_timeout_seconds=300,
                   failure_scope='prior native crash is time-correlated, PID not bound')
    runner.save(folder / 'pre_run.json', receipt)
    started = time.perf_counter()
    peak_rss = 0
    with (folder / 'stdout.log').open('x', encoding='utf-8') as stdout, \
            (folder / 'stderr.log').open('x', encoding='utf-8') as stderr:
        process = subprocess.Popen(command, cwd=runner.base.PROJECT,
            env=worker_environment(), stdout=stdout, stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW)
        print(json.dumps(dict(event='CPU_diagnostic_started', pid=process.pid)), flush=True)
        while process.poll() is None:
            if time.perf_counter() - started > 300:
                process.terminate()
                process.wait(timeout=20)
                receipt['diagnostic_timeout'] = True
                break
            try:
                peak_rss = max(peak_rss, psutil.Process(process.pid).memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            time.sleep(1)
    receipt.update(pid=process.pid, exit_code=process.returncode,
                   seconds=time.perf_counter() - started, peak_rss_bytes=peak_rss,
                   sources_unchanged=all(sha256(Path(p)) == h for p, h in hashes.items()),
                   pass_receipt_exists=(runner.CHECK_DIR / 'CPU_resume_check.json').is_file())
    runner.save(folder / 'result.json', receipt)
    print(json.dumps(receipt), flush=True)
    if process.returncode != 0 or not receipt['pass_receipt_exists']:
        raise RuntimeError('CPU gate still incomplete; no further retry')


if __name__ == '__main__':
    main()
