"""Bounded disposable AMP/SGD cache benchmark; never save or resume training.

CPU identity validation precedes a ready-handshaken external watchdog. The
watchdog pins only this process handle: 75 C, thermal slowdown, telemetry loss,
or 295 seconds stops it. Driver protections and other processes stay untouched.
"""
import argparse
import copy
import ctypes
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time


FIELDS = ('uuid', 'temperature.gpu', 'power.draw', 'memory.used', 'memory.total',
          'clocks_throttle_reasons.hw_thermal_slowdown',
          'clocks_throttle_reasons.sw_thermal_slowdown')
HARD_SECONDS = 295
SOFT_SECONDS = 285
STOP_C = 75
RAM_RESERVE = 3 * (1 << 30)


def system_available_ram():
    class Status(ctypes.Structure):
        _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
            (name, ctypes.c_ulonglong) for name in
            ('total', 'available', 'total_pagefile', 'available_pagefile',
             'total_virtual', 'available_virtual', 'extended_virtual')]
    status = Status()
    status.length = ctypes.sizeof(status)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GlobalMemoryStatusEx.argtypes = (ctypes.POINTER(Status),)
    if not kernel.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError(ctypes.get_last_error(), 'system RAM telemetry unavailable')
    return status.available


def gpu_sample(uuid=None, timeout=2):
    command = ['nvidia-smi', '--query-gpu=' + ','.join(FIELDS),
               '--format=csv,noheader,nounits']
    if uuid:
        command += ['--id=' + uuid]
    result = subprocess.run(command, capture_output=True, text=True, check=True,
                            timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW)
    lines = result.stdout.strip().splitlines()
    if len(lines) != 1:
        raise ValueError('benchmark requires one unambiguous GPU')
    values = [value.strip() for value in lines[0].split(',')]
    if len(values) != len(FIELDS) or (uuid and values[0] != uuid):
        raise ValueError('GPU telemetry identity mismatch')
    if any(value not in ('Active', 'Not Active') for value in values[5:]):
        raise ValueError('thermal slowdown telemetry unavailable')
    return dict(uuid=values[0], temperature_c=float(values[1]), power_w=float(values[2]),
                memory_mib=float(values[3]), total_memory_mib=float(values[4]),
                thermal_slowdown=any(value == 'Active' for value in values[5:]))


def stop_reason(sample, elapsed):
    if elapsed >= HARD_SECONDS:
        return 'hard_GPU_window_deadline'
    if sample['temperature_c'] >= STOP_C:
        return 'conservative_temperature_stop'
    if sample['thermal_slowdown']:
        return 'device_thermal_slowdown'
    if sample.get('system_available_ram_bytes', RAM_RESERVE) < RAM_RESERVE:
        return 'system_available_RAM_below3_GiB'
    return None


def watchdog(pid, uuid, output, telemetry):
    # An open Windows process handle cannot be redirected by subsequent PID reuse.
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    kernel.TerminateProcess.argtypes = (ctypes.c_void_p, ctypes.c_uint)
    kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
    handle = kernel.OpenProcess(0x00100000 | 0x0001 | 0x0400 | 0x0010, False, pid)
    if not handle:
        raise OSError(ctypes.get_last_error(), 'cannot pin benchmark process')

    class Memory(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in
            ('peak_working_set', 'working_set', 'peak_paged', 'paged',
             'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile', 'private')]

    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)
    started = time.monotonic()
    ready = False
    try:
        with telemetry.open('x', encoding='utf-8') as stream:
            initial = gpu_sample(uuid)
            initial['system_available_ram_bytes'] = system_available_ram()
            if stop_reason(initial, 0):
                raise RuntimeError('GPU is not cool/observable enough to start')
            ready = True
            print(json.dumps(dict(event='watchdog_ready', started_monotonic=started)), flush=True)
            while kernel.WaitForSingleObject(handle, 0) == 258:  # WAIT_TIMEOUT: parent alive.
                elapsed = time.monotonic() - started
                reason = 'hard_GPU_window_deadline' if elapsed >= HARD_SECONDS else None
                sample = {}
                if reason is None:
                    try:
                        sample = gpu_sample(uuid, timeout=max(0.01, min(2, HARD_SECONDS - elapsed)))
                        sample['system_available_ram_bytes'] = system_available_ram()
                        elapsed = time.monotonic() - started
                        reason = stop_reason(sample, elapsed)
                    except Exception as error:
                        reason = 'telemetry_unavailable:' + str(error)
                if reason:
                    # Kill before potentially blocking report I/O, never after it.
                    if not kernel.TerminateProcess(handle, 124):
                        raise OSError(ctypes.get_last_error(), 'failed to stop benchmark')
                    with output.open('x', encoding='utf-8') as failure:
                        json.dump(dict(status='stopped_by_watchdog', reason=reason,
                                       gpu_window_seconds=elapsed, training_resumed=False), failure)
                    stream.write(json.dumps(dict(elapsed_seconds=elapsed, stopped=reason, **sample)) + '\n')
                    stream.flush()
                    return
                memory = Memory()
                memory.cb = ctypes.sizeof(memory)
                if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(memory), memory.cb):
                    kernel.TerminateProcess(handle, 124)
                    raise OSError(ctypes.get_last_error(), 'process memory telemetry unavailable')
                stream.write(json.dumps(dict(elapsed_seconds=elapsed,
                                             process_ram_bytes=memory.working_set,
                                             process_peak_ram_bytes=memory.peak_working_set,
                                             **sample)) + '\n')
                stream.flush()
                time.sleep(min(1, max(0, HARD_SECONDS - (time.monotonic() - started))))
    except Exception as error:
        # Once ready, losing the watchdog must never leave a live CUDA workload.
        if ready and kernel.WaitForSingleObject(handle, 0) != 0:
            kernel.TerminateProcess(handle, 124)
            try:
                with output.open('x', encoding='utf-8') as failure:
                    json.dump(dict(status='stopped_by_watchdog',
                                   reason='watchdog_exception:' + str(error),
                                   gpu_window_seconds=time.monotonic() - started,
                                   training_resumed=False), failure)
            except Exception:
                pass  # The process was stopped first, even if the disk cannot publish a receipt.
        raise
    finally:
        kernel.CloseHandle(handle)


def tree_cpu(value):
    import torch
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().clone()
    if isinstance(value, dict):
        return {key: tree_cpu(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [tree_cpu(item) for item in value]
    return value


def assert_tree_equal(left, right):
    import torch
    if isinstance(left, torch.Tensor):
        torch.testing.assert_close(left, right, rtol=0, atol=0)
    elif isinstance(left, dict):
        assert left.keys() == right.keys(), 'state keys differ'
        for key in left:
            assert_tree_equal(left[key], right[key])
    elif isinstance(left, list):
        assert len(left) == len(right), 'state lengths differ'
        for a, b in zip(left, right, strict=True):
            assert_tree_equal(a, b)
    else:
        assert left == right, 'scalar state differs'


def batch_digest(images, targets, keys):
    digest = hashlib.sha256(images.numpy().tobytes())
    for target in targets:
        for name in ('boxes', 'labels', 'ignore_boxes'):
            value = target[name]
            digest.update(str((name, value.dtype, tuple(value.shape))).encode())
            digest.update(value.numpy().tobytes())
    digest.update(json.dumps(keys).encode())
    return digest.hexdigest()


def run(args):
    if os.name != 'nt' or os.environ.get('CUDA_VISIBLE_DEVICES') not in (None, '0'):
        raise ValueError('this watchdog requires Windows and unambiguous CUDA device0')
    if args.output.exists() or args.output.with_suffix('.telemetry.jsonl').exists():
        raise FileExistsError(args.output)
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
    import torch
    from torch.utils.data import DataLoader
    from .loss import YOLOXLoss
    from .model import RoadYOLOS4
    from .train import (CLASS_CONTRACT, collate, ensure_resume_eligible, load_dataset_manifest,
                        make_frame_dataset, protocol_hash, restore_rng, scheduled_lr, sha256)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    began = time.perf_counter()
    checkpoint_hash = sha256(args.checkpoint)
    if checkpoint_hash != args.checkpoint_sha256:
        raise ValueError('paused checkpoint receipt mismatch')
    checkpoint = torch.load(args.checkpoint, map_location='cpu', weights_only=False)
    ensure_resume_eligible(checkpoint)
    protocol = checkpoint['training_protocol']
    if (protocol_hash(protocol) != args.protocol_sha256 or protocol['microbatch'] != 8
            or protocol['accum_steps'] != 8 or checkpoint['effective_batch'] != 64
            or not protocol['amp'] or protocol['phase'] != 'supervised'
            or checkpoint['dataset_sha256'] != sha256(args.checkpoint_training_dataset)):
        raise ValueError('original checkpoint data/protocol binding mismatch')
    if sha256(args.dataset) != args.dataset_sha256:
        raise ValueError('road manifest receipt mismatch')
    receipt = json.loads(args.cache_report.read_text())
    review = json.loads(args.cache_review.read_text())
    if (receipt['status'] != 'passed_full_development_cache_CPU_equivalence_not_training_speed'
            or receipt['dataset_sha256'] != args.dataset_sha256
            or receipt['cache_index_sha256'] != args.cache_index_sha256
            or review['verdict']['blocking_defects']
            or review['source_and_artifact_snapshots']['builder_report_sha256'] != sha256(args.cache_report)
            or review['source_and_artifact_snapshots']['cache_index_sha256'] != args.cache_index_sha256):
        raise ValueError('final cache equivalence/review receipts do not match')
    print('CPU startup: validate complete road manifest', flush=True)
    started = time.perf_counter()
    declared = json.loads(args.dataset.read_text())
    if any(row['split'] not in ('train', 'val') for row in declared['images']):
        raise ValueError('development rows only; no newtest access')
    del declared
    _, rows = load_dataset_manifest(args.dataset)
    manifest_seconds = time.perf_counter() - started
    datasets, startup = {}, {}
    for name in ('raw', 'cache'):
        print('CPU startup: construct ' + name + ' loader', flush=True)
        started = time.perf_counter()
        options = dict(cache_root=args.cache_dir, cache_index_sha256=args.cache_index_sha256) if name == 'cache' else {}
        datasets[name] = make_frame_dataset(rows, 'train', args.dataset, mosaic=True,
                                           seed=protocol['seed'], **options)
        datasets[name].set_epoch(6, True)
        startup[name] = time.perf_counter() - started
    model_probe = RoadYOLOS4()
    if (checkpoint['architecture_hash'] != model_probe.architecture_hash()
            or checkpoint['class_contract'] != CLASS_CONTRACT):
        raise ValueError('checkpoint topology/class mismatch')
    del model_probe
    initial = gpu_sample()
    initial['system_available_ram_bytes'] = system_available_ram()
    if stop_reason(initial, 0):
        raise RuntimeError('GPU not cool enough or already thermally throttled')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    telemetry = args.output.with_suffix('.telemetry.jsonl')
    # Base Python avoids Windows venv launcher indirection when terminating the helper.
    monitor = subprocess.Popen([sys._base_executable, '-B', str(Path(__file__).resolve()),
                               '--watchdog', str(os.getpid()), initial['uuid'],
                               str(args.output.resolve()), str(telemetry.resolve())],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW)
    ready = json.loads(monitor.stdout.readline())
    if ready.get('event') != 'watchdog_ready':
        monitor.terminate()
        raise RuntimeError('watchdog not ready; no CUDA operations permitted')
    gpu_started = ready['started_monotonic']
    steps_per_trial = 3 if args.continuous else 1
    result = dict(status='failed_or_partial', checkpoint_sha256=checkpoint_hash,
                  checkpoint_epoch=checkpoint['epoch'] + 1, original_protocol_sha256=protocol_hash(protocol),
                  checkpoint_training_dataset_sha256=checkpoint['dataset_sha256'],
                  benchmark_dataset_sha256=args.dataset_sha256,
                  cache_index_sha256=args.cache_index_sha256, initial_gpu=initial,
                  manifest_validation_seconds=manifest_seconds, constructor_seconds=startup,
                  workers=0, microbatch=8, accum_steps=8, effective_batch=64,
                  amp=True, mosaic_epoch=6, steps_per_trial=steps_per_trial,
                  order=['raw', 'cache', 'cache', 'raw'], trials=[], training_resumed=False,
                  checkpoints_written=0, hard_seconds=HARD_SECONDS, soft_seconds=SOFT_SECONDS,
                  stop_temperature_c=STOP_C, system_RAM_reserve_bytes=RAM_RESERVE,
                  source_sha256=sha256(Path(__file__)))
    model = optimizer = scaler = group = norm = None
    baseline = None
    try:
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise RuntimeError('CUDA device mapping unavailable')
        for trial, name in enumerate(result['order']):
            if monitor.poll() is not None:
                raise RuntimeError('watchdog unexpectedly exited')
            model = RoadYOLOS4()
            model.load_state_dict(checkpoint['model'], strict=True)
            model.to('cuda').train()
            optimizer = torch.optim.SGD(model.parameters(), lr=protocol['base_lr'],
                                        momentum=protocol['momentum'], weight_decay=protocol['weight_decay'])
            optimizer.load_state_dict(copy.deepcopy(checkpoint['optimizer']))
            scaler = torch.amp.GradScaler('cuda', enabled=True)
            scaler.load_state_dict(copy.deepcopy(checkpoint['scaler']))
            restore_rng(checkpoint['rng_state'])
            loader = iter(DataLoader(datasets[name], batch_size=8, shuffle=True, num_workers=0,
                                    pin_memory=True, collate_fn=collate,
                                    generator=torch.Generator().manual_seed(protocol['seed'] + 6)))
            criterion = YOLOXLoss()
            records, snapshots = [], []
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
            for step in range(steps_per_trial):
                optimizer.zero_grad(set_to_none=True)
                inputs, heads, losses, sample_keys = [], [], [], []
                fetch_seconds = compute_seconds = qa_seconds = 0.0
                group_started = time.perf_counter()
                for micro in range(8):
                    if time.monotonic() - gpu_started >= SOFT_SECONDS or monitor.poll() is not None:
                        raise RuntimeError('soft GPU budget or watchdog failure')
                    started = time.perf_counter()
                    images, targets, keys = next(loader)
                    fetch_seconds += time.perf_counter() - started
                    started = time.perf_counter()
                    inputs.append(batch_digest(images, targets, keys))
                    sample_keys.extend(keys)
                    qa_seconds += time.perf_counter() - started
                    started = time.perf_counter()
                    gpu_images = images.to('cuda', non_blocking=True)
                    with torch.amp.autocast(device_type='cuda', enabled=True):
                        outputs = model(gpu_images)
                        values = criterion(outputs, targets)
                        total_loss = values['loss']
                        scaled_loss = total_loss * 8 / 64
                    if not all(torch.isfinite(value).all().item() for value in values.values()):
                        raise FloatingPointError('non-finite AMP loss')
                    scaler.scale(scaled_loss).backward()
                    torch.cuda.synchronize()
                    compute_seconds += time.perf_counter() - started
                    started = time.perf_counter()
                    heads.append(tree_cpu(outputs))
                    losses.append(tree_cpu(values))
                    qa_seconds += time.perf_counter() - started
                    del outputs, values, total_loss, scaled_loss, gpu_images, images, targets
                started = time.perf_counter()
                scaler.unscale_(optimizer)
                torch.cuda.synchronize()
                compute_seconds += time.perf_counter() - started
                started = time.perf_counter()
                gradients = {key: tree_cpu(value.grad) for key, value in model.named_parameters()
                             if value.grad is not None}
                if gradients.keys() != {
                        key for key, value in model.named_parameters() if value.requires_grad}:
                    raise AssertionError('trainable parameter is missing its gradient')
                if gradients and not all(torch.isfinite(value).all() for value in gradients.values()):
                    raise FloatingPointError('non-finite unscaled gradients')
                qa_seconds += time.perf_counter() - started
                started = time.perf_counter()
                norm = torch.nn.utils.clip_grad_norm_(model.parameters(), protocol['clip_grad'],
                                                     error_if_nonfinite=True)
                lr = scheduled_lr(checkpoint['trained_steps'] + step,
                                  protocol['optimizer_steps_per_epoch'] * protocol['epochs'],
                                  protocol['optimizer_steps_per_epoch'] * protocol['warmup_epochs'],
                                  protocol['base_lr'])
                for group in optimizer.param_groups:
                    group['lr'] = lr
                scale_before = scaler.get_scale()
                scaler.step(optimizer)
                scaler.update()
                torch.cuda.synchronize()
                if scaler.get_scale() < scale_before:
                    raise FloatingPointError('AMP optimizer step skipped')
                compute_seconds += time.perf_counter() - started
                started = time.perf_counter()
                snapshot = dict(inputs=inputs, losses=losses, scaler=scaler.state_dict(),
                                state=tree_cpu(model.state_dict()),
                                optimizer=tree_cpu(optimizer.state_dict()))
                snapshot.update(heads=heads, gradients=gradients)
                snapshots.append(snapshot)
                qa_seconds += time.perf_counter() - started
                records.append(dict(step=step, samples=64, fetch_seconds=fetch_seconds,
                                    compute_seconds=compute_seconds, qa_seconds=qa_seconds,
                                    work_seconds=fetch_seconds + compute_seconds,
                                    diagnostic_group_wall_seconds=time.perf_counter() - group_started,
                                    mean_loss=statistics.mean(float(item['loss']) for item in losses),
                                    gradient_norm=float(norm), lr=lr,
                                    input_batch_sha256=inputs, sample_keys=sample_keys,
                                    compared_gradient_tensors=len(gradients),
                                    scaler_scale_after=scaler.get_scale()))
                print(f'GPU trial{trial} {name} step{step}: '
                      f'fetch={fetch_seconds:.3f}s compute={compute_seconds:.3f}s', flush=True)
            if baseline is None:
                baseline = snapshots
            else:
                assert_tree_equal(baseline, snapshots)
            result['trials'].append(dict(path=name, steps=records,
                                        peak_torch_cuda_bytes=torch.cuda.max_memory_allocated(),
                                        peak_torch_reserved_bytes=torch.cuda.max_memory_reserved(),
                                        compared_first_group_gradient_tensors=len(snapshots[0]['gradients'])))
            del loader, criterion, snapshots
            model = optimizer = scaler = group = norm = None
            torch.cuda.empty_cache()
        result.update(status=('passed_bounded_GPU_continuous_cache_equivalence_not_epoch_speed'
                              if args.continuous else
                              'passed_bounded_GPU_cache_AMP_SGD_equivalence_not_epoch_speed'),
                      max_input_head_loss_gradient_BN_optimizer_parameter_difference=0,
                      disposable_optimizer_steps=4 * steps_per_trial, persistent_optimizer_updates=0)
    except Exception as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        model = optimizer = scaler = group = norm = None
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        try:
            final_sample = gpu_sample(initial['uuid'])
            final_sample['system_available_ram_bytes'] = system_available_ram()
            result['final_gpu'] = final_sample
            if stop_reason(final_sample, time.monotonic() - gpu_started):
                result.update(status='failed_or_partial', error='final thermal/deadline check failed')
        except Exception as error:
            result.update(status='failed_or_partial', error='final telemetry unavailable:' + str(error))
        result['gpu_window_seconds'] = time.monotonic() - gpu_started
        if result['gpu_window_seconds'] >= HARD_SECONDS:
            result.update(status='failed_or_partial', error='GPU window exceeded publication budget')
        monitor.terminate()
        monitor.wait(timeout=3)
    result['checkpoint_sha256_after'] = sha256(args.checkpoint)
    if result['checkpoint_sha256_after'] != checkpoint_hash:
        result.update(status='failed_or_partial', error='paused checkpoint changed')
    samples = [json.loads(line) for line in telemetry.read_text().splitlines()]
    gpu_samples = [initial] + samples + ([result['final_gpu']] if 'final_gpu' in result else [])
    result['telemetry_samples'] = len(samples)
    result['peak_temperature_c'] = max(sample['temperature_c'] for sample in gpu_samples)
    result['peak_power_w'] = max(sample['power_w'] for sample in gpu_samples)
    result['peak_process_RAM_bytes'] = max((sample['process_peak_ram_bytes'] for sample in samples), default=None)
    result['peak_device_used_mib'] = max(sample['memory_mib'] for sample in gpu_samples)
    result['thermal_slowdown_observed'] = any(sample['thermal_slowdown'] for sample in gpu_samples)
    result['minimum_system_available_ram_bytes'] = min(
        sample['system_available_ram_bytes'] for sample in gpu_samples)
    if result['status'].startswith('passed'):
        medians = {name: statistics.median(step['work_seconds']
                                        for trial in result['trials'] if trial['path'] == name
                                        for step in trial['steps']) for name in ('raw', 'cache')}
        result.update(all_group_work_median_seconds=medians,
                      bounded_work_speed_ratio=medians['raw'] / medians['cache'])
    result['total_session_seconds'] = time.perf_counter() - began
    result['limitation'] = (f'Two AB/BA trials per path, {steps_per_trial} consecutive groups each, '
                            f'workers0, same{64 * steps_per_trial} development Mosaic samples per trial. '
                            'Model/SGD/scaler/RNG restored only between trials, never between consecutive groups. '
                            'Every microbatch head/loss and every group gradient/state compared. '
                            'Excludes diagnostic QA from work timing; includes fetch, '
                            'transfer, synchronized forward/backward/unscale/clip/SGD. Startup separately measured. '
                            'Few bounded timings; first CUDA run is cold, not a robust steady-state speedup. '
                            'No full epoch, workers4 RAM/order, accuracy, QAT, RTL or formal training resume.')
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result['status'].startswith('passed') else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--watchdog':
        watchdog(int(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5]))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--continuous', action='store_true',
                        help='fixed three consecutive disposable optimizer groups per ABBA trial')
    for name in ('dataset', 'checkpoint', 'checkpoint-training-dataset', 'cache-dir',
                 'cache-report', 'cache-review', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    for name in ('dataset-sha256', 'checkpoint-sha256', 'protocol-sha256', 'cache-index-sha256'):
        parser.add_argument('--' + name, required=True)
    return run(parser.parse_args())


if __name__ == '__main__':
    sys.exit(main())
