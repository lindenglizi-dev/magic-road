"""Reproduce the actual device-check failure and verify the repaired full validator.

No model construction, forward, backward, optimizer or training update.
"""
import copy
import json
import os
from pathlib import Path
import time

import torch

from cnn.benchmark_cache_gpu import gpu_sample
from cnn.hw_validation.production import train_qat_head_only as runner
from cnn.hw_validation.production import train_qat_numpy235 as runtime
from cnn.train import sha256


def main():
    if (os.environ.get('CUDA_VISIBLE_DEVICES') != '0'
            or os.environ.get('PYTORCH_NVML_BASED_CUDA_CHECK') != '1'):
        raise RuntimeError('Explicit selected GPU test environment required')
    output = runner.OUT / 'checker_device_regression.json'
    if output.exists():
        raise FileExistsError(output)
    torch.set_num_threads(2)
    initial = gpu_sample(runner.base.GPU)
    if initial['temperature_c'] >= 75 or initial['thermal_slowdown']:
        raise RuntimeError('GPU thermal protection: no diagnostic copy')
    dataset, window, _, _, _, ancestry, parent = runtime.prepare()
    path = runner.CHECK_DIR / 'resume_check/update_H1.pt'
    state = torch.load(path, map_location='cpu', weights_only=False)
    identity, protocol, ancestry = state['identity'], state['training_protocol'], state['ancestry']
    before = {str(path): sha256(path), str(runner.PARENT): sha256(runner.PARENT)}
    started = time.perf_counter()
    actual_uuid = str(torch.cuda.get_device_properties(0).uuid).removeprefix('GPU-')
    if actual_uuid.lower() != runner.base.GPU.removeprefix('GPU-').lower():
        raise RuntimeError('Unexpected GPU UUID')
    gpu_state = copy.deepcopy(state)
    gpu_state['model'] = {name: value.to('cuda') for name, value in state['model'].items()}
    name = identity['frozen_parameter_names'][0]
    try:
        torch.testing.assert_close(gpu_state['model'][name], parent['model'][name], atol=0, rtol=0)
    except AssertionError as error:
        if 'device' not in str(error):
            raise
        original_device_failure_reproduced = True
    else:
        raise AssertionError('Original cross-device failure was not reproduced')
    runner.validate_state(gpu_state, identity, protocol, ancestry, parent,
                          dataset, window, candidate=False)
    rejected = []
    for label in ('wrong_value', 'wrong_dtype'):
        bad = copy.deepcopy(gpu_state)
        if label == 'wrong_value':
            bad['model'][name].flatten()[0].add_(1)
        else:
            bad['model'][name] = bad['model'][name].double()
        try:
            runner.validate_state(bad, identity, protocol, ancestry, parent,
                                  dataset, window, candidate=False)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError(f'Fixed validator accepted {label}')
    torch.cuda.synchronize()
    if any(sha256(Path(path)) != digest for path, digest in before.items()):
        raise AssertionError('Regression test changed a checkpoint')
    result = dict(status='PASS_REAL_CUDA_CPU_FROZEN_VALIDATOR_REGRESSION',
        original_device_failure_reproduced=original_device_failure_reproduced,
        repaired_full_state_validator_passed=True, frozen_tensor_count=92,
        negative_cases_rejected=rejected, source_sha256=sha256(Path(runner.__file__)),
        test_source_sha256=sha256(Path(__file__)), checkpoint_input_sha256=before,
        initial_gpu=initial, final_gpu=gpu_sample(runner.base.GPU),
        model_forward=False, backward=False, optimizer_created=False,
        training_updates=0, seconds=time.perf_counter() - started,
        limitation='Uses the saved CPU H1 diagnostic state moved to CUDA. Validates the actual checkpoint checker, not a restarted training segment.')
    runner.base.save(output, result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
