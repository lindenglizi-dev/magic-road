"""Bounded CPU loader parity on full development metadata; never train or use CUDA."""
import argparse
import gc
import faulthandler
import json
import os
from pathlib import Path
import pickle
import threading
import time

import psutil

DATASET = Path('cnn/data/visdrone_vid_train/raw_manifest/dataset.json')
CACHE = Path('cnn/data/cache_road_full_development_20261003')
CHECKPOINT = Path('cnn/runs/coco_full_pretrain300/last.pt')
PINS = {
    DATASET: 'ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4',
    CACHE / 'index.json': '646db6bcd11ab8ff55b9fb024480ab0b015842f7a9495a890a9b947aa153e170',
    CHECKPOINT: '51da8c3289ef5ffa24fe9df01567657b8254a9ef982cdef379f12c3437b068d4',
    Path('cnn/reports/cache_gpu_benchmark_20261003.json'):
        'b96540b06f8fe4c9d870349cc6aa8d21846e86383a1e04acef5773dcdce69fdb',
    Path('cnn/reports/cache_gpu_benchmark_review_20261003.json'):
        'fdebceb04a6138554dd603d438758d9ae2fbb27b076ab85b10ea3b90ed939f50',
}
RESERVE = 3 * (1 << 30)


def memory_sample(root):
    children = root.children(recursive=True)
    processes = []
    for process in [root] + children:
        try:
            memory = process.memory_info()
            processes.append(dict(pid=process.pid, rss=memory.rss,
                                  private=getattr(memory, 'private', None)))
        except psutil.NoSuchProcess:
            continue
    return dict(available=psutil.virtual_memory().available,
                total=psutil.virtual_memory().total,
                tree_rss=sum(item['rss'] for item in processes), processes=processes)


def enforce_reserve(sample):
    if sample['available'] < RESERVE:
        raise MemoryError('CPU memory reserve below3 GiB; stop this diagnostic')


class MemoryMonitor:
    """Sample only this diagnostic's tree; never terminate an unrelated process."""
    def __init__(self):
        self.root = psutil.Process()
        self.done = threading.Event()
        self.error = None
        self.summary = dict(samples=0, peak_tree_rss=0, minimum_available=None,
                            peak_processes=[], observed_child_pids=[])
        self.thread = threading.Thread(target=self.watch, daemon=True)

    def watch(self):
        try:
            while not self.done.is_set():
                sample = memory_sample(self.root)
                self.summary['samples'] += 1
                minimum = self.summary['minimum_available']
                self.summary['minimum_available'] = min(sample['available'], minimum or sample['available'])
                self.summary['observed_child_pids'] = sorted(set(
                    self.summary['observed_child_pids']) | {
                        item['pid'] for item in sample['processes'] if item['pid'] != self.root.pid})
                if sample['tree_rss'] > self.summary['peak_tree_rss']:
                    self.summary.update(peak_tree_rss=sample['tree_rss'],
                                        peak_processes=sample['processes'])
                enforce_reserve(sample)
                self.done.wait(0.25)
        except Exception as error:
            self.error = str(error)
            print('CPU memory monitor stop: ' + type(error).__name__ + ': ' + self.error,
                  flush=True)
            # psutil retains creation identity and checks PID reuse on terminate.
            for process in self.root.children(recursive=True):
                try:
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass

    def __enter__(self):
        enforce_reserve(memory_sample(self.root))
        faulthandler.dump_traceback_later(60)
        self.thread.start()
        return self

    def __exit__(self, *_args):
        self.done.set()
        self.thread.join(timeout=3)
        faulthandler.cancel_dump_traceback_later()
        if self.thread.is_alive():
            raise RuntimeError('memory monitor failed to stop')

    def check(self):
        if self.error:
            raise RuntimeError('memory monitor: ' + self.error)


def check_loader(dataset, workers, batches, shuffle, baseline=None):
    import torch
    from torch.utils.data import DataLoader
    from .benchmark_cache_gpu import batch_digest
    from .train import collate
    options = dict(batch_size=8, num_workers=workers, collate_fn=collate,
                   shuffle=shuffle, pin_memory=False,
                   generator=torch.Generator().manual_seed(42 + dataset.epoch))
    if workers:
        options.update(timeout=120, multiprocessing_context='spawn')
    iterator = None
    records, times, keys = [], [], []
    started = time.perf_counter()
    with MemoryMonitor() as monitor:
        try:
            iterator = iter(DataLoader(dataset, **options))
            for index in range(batches):
                monitor.check()
                fetch = time.perf_counter()
                images, targets, batch_keys = next(iterator)
                times.append(time.perf_counter() - fetch)
                digest = batch_digest(images, targets, batch_keys)
                if baseline is not None and digest != baseline[index]:
                    raise AssertionError('pixels/targets/ignore/keys/order differ at batch' + str(index))
                records.append(digest)
                keys.extend(batch_keys)
                del images, targets, batch_keys
            monitor.check()
        except Exception:
            monitor.check()  # Prefer the actual reserve/telemetry cause over a later worker timeout.
            raise
        finally:
            # Torch's iterator has no public close; explicit shutdown prevents
            # overlapping Windows worker sets and queued prefetch after a test.
            if workers and iterator is not None:
                owned = list(iterator._workers)
                try:
                    iterator._shutdown_workers()
                finally:
                    for process in owned:
                        if process.is_alive():
                            process.terminate()
                        process.join(timeout=5)
                    if any(process.is_alive() for process in owned):
                        raise RuntimeError('loader workers did not stop')
            del iterator
            gc.collect()
    monitor.check()
    return dict(batch_sha256=records, keys=keys, consumed_samples=len(keys),
                iterator_and_consumption_seconds=time.perf_counter() - started,
                fetch_seconds=times, memory=monitor.summary,
                workers_stopped=True, prefetch_factor=2 if workers else None,
                pin_memory=False, persistent_workers=False)


def run(output):
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    import torch
    from .train import load_dataset_manifest, make_frame_dataset, sha256
    if output.exists():
        raise FileExistsError(output)
    result = dict(status='failed_or_partial', device='cpu', gpu_used=False,
                  optimizer_updates=0, training_resumed=False, checkpoints_written=0,
                  memory_reserve_bytes=RESERVE, trials=[], admission_skips=[],
                  source_sha256=sha256(Path(__file__)))
    started = time.perf_counter()
    try:
        initial_memory = memory_sample(psutil.Process())
        result['initial_memory'] = initial_memory
        # Previous full-manifest startup exceeded1 GiB in this process. Leave
        #1.5 GiB for validation in addition to the live3 GiB system reserve.
        if initial_memory['available'] < RESERVE + (1536 << 20):
            raise MemoryError('full-manifest admission requires4.5 GiB available before loading')
        for path, expected in PINS.items():
            if sha256(path) != expected:
                raise ValueError('pinned artifact changed: ' + str(path))
        result['artifact_sha256'] = {str(path): value for path, value in PINS.items()}
        declared = json.loads(DATASET.read_text(encoding='utf-8'))
        if any(row['split'] not in ('train', 'val') for row in declared['images']):
            raise ValueError('development only; no newtest access')
        del declared
        torch.set_num_threads(2)
        print('CPU: full manifest integrity validation', flush=True)
        began = time.perf_counter()
        _, rows = load_dataset_manifest(DATASET)
        result['manifest_validation_seconds'] = time.perf_counter() - began
        datasets, constructors = {}, {}
        for split in ('train', 'val'):
            for path in ('raw', 'cache'):
                print('CPU: construct ' + split + '/' + path, flush=True)
                began = time.perf_counter()
                options = dict(cache_root=CACHE, cache_index_sha256=PINS[CACHE / 'index.json']) if path == 'cache' else {}
                datasets[split, path] = make_frame_dataset(rows, split, DATASET, **options)
                constructors[split + '/' + path] = time.perf_counter() - began
        result.update(constructor_seconds=constructors,
                      full_metadata_sizes={split: len(datasets[split, 'raw']) for split in ('train', 'val')},
                      memory_after_both_split_constructors=memory_sample(psutil.Process()))
        # Metadata remains complete in every spawned worker. Bounded reads are QA,
        # not a filtered training dataset or an accuracy/epoch-speed measurement.
        for split, epoch, mosaic, batches in (('train', 6, True, 8),
                                               ('train', 7, True, 2),
                                               ('train', 285, False, 2),
                                               ('val', 6, False, 2)):
            baseline = None
            for workers in (0, 2, 4):
                for path in ('raw', 'cache'):
                    data = datasets[split, path]
                    data.set_epoch(epoch, mosaic)
                    encoded_bytes = len(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
                    gc.collect()
                    # Conservative admission estimate, followed by live monitoring;
                    # it is not a proof of peak memory for an entire training epoch.
                    required = RESERVE + workers * (encoded_bytes * 3 + (512 << 20))
                    available = psutil.virtual_memory().available
                    if available < required:
                        result['admission_skips'].append(dict(
                            split=split, path=path, epoch=epoch, workers=workers,
                            required_bytes=required, available_bytes=available))
                        print(f'not admitted {split}/{path} epoch{epoch} workers{workers}: '
                              f'requires{required} bytes; available{available}', flush=True)
                        continue  # Preserve lower-worker evidence; never call a skipped trial passed.
                    print(f'CPU trial {split}/{path} epoch{epoch} workers{workers}', flush=True)
                    trial = check_loader(data, workers, batches, split == 'train', baseline)
                    if baseline is None:
                        baseline = trial['batch_sha256']
                    trial.update(split=split, path=path, epoch=epoch, mosaic=mosaic,
                                 workers=workers, full_dataset_rows=len(data),
                                 dataset_pickle_bytes=encoded_bytes)
                    result['trials'].append(trial)
                    print(f"passed {trial['consumed_samples']} samples; tree RAM "
                          f"{trial['memory']['peak_tree_rss'] / (1 << 30):.2f} GiB", flush=True)
        if torch.cuda.is_initialized():
            raise AssertionError('CUDA initialized in CPU-only diagnostic')
        result.update(status=('partial_CPU_parity_with_memory_admission_skips'
                              if result['admission_skips'] else
                              'passed_bounded_CPU_workers_parity_not_training_speed'),
                      maximum_compared_difference=0)
    except Exception as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    result['checkpoint_sha256_after'] = sha256(CHECKPOINT)
    if result['checkpoint_sha256_after'] != PINS[CHECKPOINT]:
        result.update(status='failed_or_partial', error='paused checkpoint changed')
    result.update(total_seconds=time.perf_counter() - started,
                  limitation='Full train/val metadata and default prefetch2, CPU pin_memory=False, '
                             'bounded consumed batches only; prefetched extra samples may be read. '
                             'Tree RSS can double-count shared mappings.0.25s memory sampling is not '
                             'an exhaustive peak. No CUDA, pin-memory/GPU overlap, continuous optimizer '
                             'trajectory, full epoch, accuracy, QAT, RTL or training adoption proof.')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(result['status'], flush=True)
    return 0 if result['status'].startswith('passed') else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path('cnn/reports/cache_workers_cpu_20261003.json'))
    raise SystemExit(run(parser.parse_args().output))
