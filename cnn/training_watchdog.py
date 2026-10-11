"""Independent protection for one owned training segment; no RAM threshold."""
import ctypes
import json
import math
from pathlib import Path
import time

from .benchmark_cache_gpu import gpu_sample, system_available_ram

SOFT_SECONDS = 26 * 60
HARD_SECONDS = 30 * 60
POLL_SECONDS = 5
QUERY_SECONDS = 5
STALE_PAUSE_SECONDS = 20
STALE_KILL_SECONDS = 30
STOP_C = 75


def decision(sample, elapsed, stale, remaining=None):
    if remaining is not None and remaining <= 0:
        return 'kill', 'night_deadline'
    if elapsed >= HARD_SECONDS:
        return 'kill', 'hard_segment_deadline'
    if sample is not None:
        if sample['temperature_c'] >= STOP_C:
            return 'kill', 'temperature_stop'
        if sample['thermal_slowdown']:
            return 'kill', 'thermal_slowdown'
    if stale >= STALE_KILL_SECONDS:
        return 'kill', 'GPU_telemetry_stale_30s'
    if stale >= STALE_PAUSE_SECONDS:
        return 'pause', 'GPU_telemetry_stale_20s'
    if elapsed >= SOFT_SECONDS:
        return 'pause', 'segment_soft_limit'
    if remaining is not None and remaining <= 60:
        return 'pause', 'night_deadline'
    return None, None


def valid_sample(sample, uuid):
    if sample.get('uuid') != uuid or any(not math.isfinite(sample[key]) for key in
            ('temperature_c', 'power_w', 'memory_mib', 'total_memory_mib')):
        raise ValueError('invalid GPU identity or non-finite telemetry')
    return sample


def request_pause(path, reason):
    # One idempotent signal in the segment's exclusive directory.
    try:
        with path.open('x', encoding='utf-8') as stream:
            json.dump(dict(reason=reason), stream)
    except FileExistsError:
        pass


def watchdog(trainer_pid, owner_pid, uuid, failure, telemetry, pause, deadline=None,
             supervisor_pid=None):
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    kernel.TerminateProcess.argtypes = (ctypes.c_void_p, ctypes.c_uint)
    kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
    trainer = kernel.OpenProcess(0x00100000 | 0x0001 | 0x0400 | 0x0010, False, trainer_pid)
    owner = kernel.OpenProcess(0x00100000, False, owner_pid)
    supervisor = (kernel.OpenProcess(0x00100000, False, supervisor_pid)
                  if supervisor_pid is not None else None)
    if not trainer or not owner or (supervisor_pid is not None and not supervisor):
        for handle in (trainer, owner, supervisor):
            if handle:
                kernel.CloseHandle(handle)
        raise OSError(ctypes.get_last_error(), 'cannot pin owned training/controller process')

    class Memory(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in
            ('peak_working_set', 'working_set', 'peak_paged', 'paged',
             'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile', 'private')]

    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)
    started = None
    armed = False

    def terminate(reason, sample=None):
        if kernel.WaitForSingleObject(trainer, 0) == 258:
            if not kernel.TerminateProcess(trainer, 124):
                raise OSError(ctypes.get_last_error(), 'cannot stop owned trainer')
        with failure.open('x', encoding='utf-8') as stream:
            json.dump(dict(status='hard_stopped', reason=reason,
                           trigger_sample=sample,
                           segment_seconds=None if started is None else time.monotonic() - started,
                           recovery_checkpoint_verified=False), stream)

    try:
        # A real fresh reading is required before granting permission to use CUDA.
        initial = None
        for attempt in range(2):
            try:
                initial = valid_sample(gpu_sample(uuid, timeout=QUERY_SECONDS), uuid)
                break
            except Exception:
                if attempt:
                    raise
                time.sleep(1)
        action, reason = decision(initial, 0, 0, None if deadline is None else deadline - time.time())
        if action:
            raise RuntimeError(reason)
        with telemetry.open('x', encoding='utf-8') as stream:
            started = time.monotonic()
            last_good = started
            next_query = started + POLL_SECONDS
            armed = True
            print(json.dumps(dict(event='watchdog_ready', started_monotonic=started,
                                  trainer_pid=trainer_pid, owner_pid=owner_pid,
                                  initial=initial, memory_threshold_enabled=False)), flush=True)
            while kernel.WaitForSingleObject(trainer, 0) == 258:
                now = time.monotonic()
                if kernel.WaitForSingleObject(owner, 0) != 258:
                    terminate('controller_exited')
                    return
                if supervisor is not None and kernel.WaitForSingleObject(supervisor, 0) != 258:
                    terminate('night_controller_exited')
                    return
                sample = None
                error = None
                remaining = None if deadline is None else deadline - time.time()
                action, reason = decision(None, now - started, now - last_good, remaining)
                if action == 'kill':
                    terminate(reason, sample)
                    return
                if action == 'pause':
                    request_pause(pause, reason)
                if now >= next_query:
                    try:
                        sample = valid_sample(gpu_sample(uuid, timeout=min(
                            QUERY_SECONDS, max(0.01, HARD_SECONDS - (now - started)),
                            max(0.01, remaining) if remaining is not None else QUERY_SECONDS,
                            max(0.01, STALE_KILL_SECONDS - (now - last_good)))), uuid)
                        last_good = time.monotonic()
                    except Exception as exception:
                        error = repr(exception)
                    next_query = time.monotonic() + (1 if error else POLL_SECONDS)
                now = time.monotonic()
                action, reason = decision(sample, now - started, now - last_good,
                                          None if deadline is None else deadline - time.time())
                if action == 'kill':
                    terminate(reason, sample)
                    stream.write(json.dumps(dict(event='hard_stop', reason=reason,
                                                  elapsed_seconds=now - started,
                                                  trigger_sample=sample)) + '\n')
                    stream.flush()
                    return
                if action == 'pause':
                    request_pause(pause, reason)
                if sample is not None or error or action:
                    row = dict(elapsed_seconds=now - started,
                               last_valid_age_seconds=now - last_good,
                               warning=error, action=action, reason=reason, **(sample or {}))
                    try:
                        row['system_available_ram_bytes'] = system_available_ram()
                        memory = Memory()
                        memory.cb = ctypes.sizeof(memory)
                        if psapi.GetProcessMemoryInfo(trainer, ctypes.byref(memory), memory.cb):
                            row.update(process_ram_bytes=memory.working_set,
                                       process_peak_ram_bytes=memory.peak_working_set,
                                       process_private_bytes=memory.private)
                    except Exception as exception:
                        row['RAM_telemetry_warning'] = repr(exception)
                    stream.write(json.dumps(row) + '\n')
                    stream.flush()
                time.sleep(min(0.25, max(0, HARD_SECONDS - (time.monotonic() - started))))
    except BaseException as error:
        # Losing the independent protector must not leave our trainer running.
        try:
            terminate('watchdog_error:' + repr(error))
        finally:
            if not armed:
                print(json.dumps(dict(event='watchdog_failed', error=repr(error))), flush=True)
        raise
    finally:
        kernel.CloseHandle(trainer)
        kernel.CloseHandle(owner)
        if supervisor is not None:
            kernel.CloseHandle(supervisor)
