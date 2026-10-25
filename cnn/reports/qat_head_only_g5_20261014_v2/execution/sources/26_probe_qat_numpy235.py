"""One CPU-only NumPy 2.3.5 control using the reviewed frozen-Stem parent."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

import numpy as np
import torch

from cnn import disk_cache
from cnn.disk_cache import assert_item_equal
from cnn.model import RoadYOLOS4
from cnn.replay_sampling import ReplayWindow
from cnn.train import FullFrameDataset, load_dataset_snapshot, restore_rng, rng_state, sha256
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem as frozen
from cnn.hw_validation.production.run_trained_integer import centered, save
from cnn.hw_validation.production.trained_integer import load_package

PARENT = frozen.RUN / 'last.pt'
PARENT_SHA256 = 'f58ce4501104e818c8a6fb10e378d7e7668b937b1332f3530180d4806029d3dd'
PARENT_MANIFEST_SHA256 = '93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b'
RECEIPT = frozen.OUT / 'cache_receipt.json'
DEFAULT_OUTPUT = base.PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1/numpy235_control'


def array_hash(values):
    digest = hashlib.sha256()
    for name in sorted(values):
        value = np.asarray(values[name])
        digest.update(name.encode())
        digest.update(str(value.dtype).encode())
        digest.update(json.dumps(list(value.shape)).encode())
        digest.update(value.tobytes(order='C'))
    return digest.hexdigest()


def parameter_hash(parameters):
    return array_hash({f'{name}.{field}': value for name, row in parameters.items()
                       for field, value in row.items()})


def runtime_identity(runtime):
    package = Path(np.__file__).resolve().parent
    if np.__version__ != '2.3.5' or not package.is_relative_to(runtime.resolve()):
        raise ValueError(f'expected NumPy 2.3.5 below {runtime}, got {np.__version__} at {package}')
    binaries = sorted([*package.rglob('*.pyd'), *package.parent.glob('numpy.libs/*.dll')])
    generator = next((path for path in binaries if path.name.startswith('_generator.')), None)
    return dict(version=np.__version__, package=str(package), requested_runtime=str(runtime.resolve()),
        generator=str(generator) if generator else None,
        generator_sha256=sha256(generator) if generator else None,
        native_files=len(binaries),
        native_sha256={str(path.relative_to(runtime.resolve())).replace('\\', '/'): sha256(path)
                       for path in binaries}, python=sys.version, executable=sys.executable,
        base_executable=sys._base_executable, torch=torch.__version__)


def verify_cache(snapshot):
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    root = Path(receipt['cache_root'])
    encoded_index = (root / 'index.json').read_bytes()
    if hashlib.sha256(encoded_index).hexdigest() != receipt['cache_index_sha256']:
        raise ValueError('cache index receipt changed')
    metadata = json.loads(encoded_index)
    blob = root / 'rgb.bin'
    if (metadata.get('dataset_sha256') != snapshot.manifest_sha256
            or metadata.get('dataset_content_sha256') != snapshot.dataset_content_sha256
            or metadata.get('rgb_sha256') != receipt['rgb_sha256']
            or sha256(blob) != receipt['rgb_sha256']
            or len(metadata.get('entries', [])) != len(snapshot.rows)):
        raise ValueError('cache binding changed')
    datasets = {split: FullFrameDataset(snapshot.rows, split, mosaic=False)
                for split in ('train', 'val')}
    positions = dict(train=0, val=0)
    digest = hashlib.sha256()
    with blob.open('rb') as stream:
        for row, entry in zip(snapshot.rows, metadata['entries'], strict=True):
            index = positions[row['split']]
            positions[row['split']] += 1
            raw_pixels, _, _ = datasets[row['split']]._load(index)
            stream.seek(entry['offset'])
            encoded = stream.read(disk_cache.RECORD_BYTES)
            if (hashlib.sha256(encoded).hexdigest() != entry['rgb_sha256']
                    or raw_pixels.tobytes(order='C') != encoded
                    or entry['row_sha256'] != disk_cache.fingerprint(row)):
                raise ValueError('raw/cache byte or row mismatch')
            pixels = np.frombuffer(encoded, np.uint8).reshape(disk_cache.SHAPE).copy()
            cached = (torch.from_numpy(pixels.astype(np.float32)).permute(2, 0, 1) - 128,
                dict(boxes=torch.tensor(row['boxes'], dtype=torch.float32).reshape(-1, 4),
                     labels=torch.tensor(row['labels'], dtype=torch.long),
                     ignore_boxes=torch.tensor(row['ignore_boxes'], dtype=torch.float32).reshape(-1, 4)),
                row['teacher_key'])
            assert_item_equal(datasets[row['split']][index], cached)
            digest.update(encoded)
    if digest.hexdigest() != receipt['rgb_sha256'] or sum(positions.values()) != 103:
        raise ValueError('all-record cache digest mismatch')
    return dict(passed=True, records=103, split_counts=positions,
        raw_rgb_bytes_exact=True, centered_inputs_targets_keys_exact=True,
        cache_index_sha256=receipt['cache_index_sha256'], rgb_sha256=receipt['rgb_sha256'],
        cached_numpy_version=metadata['preprocessing']['libraries']['numpy'],
        diagnostic_numpy_version=np.__version__, cache_used_for_training=False)


def verify_parent(parent, snapshot, window):
    identity, protocol = parent.get('identity', {}), parent.get('training_protocol', {})
    if (sha256(PARENT) != PARENT_SHA256 or sha256(frozen.OUT / 'package/manifest.json') != PARENT_MANIFEST_SHA256
            or parent.get('format') != base.FORMAT or parent.get('candidate') is not True
            or parent.get('formal_acceptance') is not False or parent.get('trained_steps') != 10
            or parent.get('next_update') != 10 or parent.get('presentations') != 220
            or len(parent.get('sample_history', [])) != 10
            or identity.get('source_checkpoint_sha256') != base.CHECKPOINT_HASH
            or identity.get('dataset_sha256') != snapshot.manifest_sha256
            or identity.get('dataset_content_sha256') != snapshot.dataset_content_sha256
            or identity.get('sampling_sha256') != window.sampling_sha256
            or protocol.get('frozen_layers') != ['stem.conv']
            or len(parent.get('optimizer', {}).get('state', {})) != 132):
        raise ValueError('fixed frozen-Stem parent mismatch')
    for relative, digest in identity['source_sha256'].items():
        if sha256(base.PROJECT / relative) != digest:
            raise ValueError(f'parent source changed: {relative}')
    if any(not torch.isfinite(row['momentum_buffer']).all()
           for row in parent['optimizer']['state'].values()):
        raise ValueError('parent optimizer momentum invalid')


def trace(model, old_integer, sample, stage):
    current_parameters = model.integer_parameters()
    current_hash = parameter_hash(current_parameters)
    current_heads, _, current_captures = model.integer_forward(sample.unsqueeze(0), capture=True)
    current_values = current_captures[0]
    deployment_values = {name: value for name, value in current_values.items()
                         if not name.endswith(':acc')}
    accumulator_values = {name: value for name, value in current_values.items()
                          if name.endswith(':acc')}
    if len(deployment_values) != 181 or len(accumulator_values) != 67:
        raise ValueError('integer trace structure changed')
    result = dict(stage=stage, trace_tensors=181,
        trace_sha256=array_hash(deployment_values), accumulator_tensors=67,
        accumulator_trace_sha256=array_hash(accumulator_values),
        all_integer_capture_tensors=248, all_integer_capture_sha256=array_hash(current_values),
        parameter_codes_sha256=current_hash)
    if old_integer is not None:
        for name, expected in old_integer.parameters.items():
            for field, value in expected.items():
                np.testing.assert_array_equal(current_parameters[name][field], value)
        old_heads, _, old_values = old_integer.forward(centered(sample), capture=True)
        if len(current_values) != 248 or set(current_values) != set(old_values):
            raise ValueError('integer trace structure changed')
        for name in old_values:
            np.testing.assert_array_equal(current_values[name], old_values[name])
        for left, right in zip(current_heads, old_heads, strict=True):
            np.testing.assert_array_equal(left[0], right)
        result.update(parent_package_trace_sha256=array_hash(
                          {name: value for name, value in old_values.items() if not name.endswith(':acc')}),
                      parent_package_all_capture_sha256=array_hash(old_values),
                      parent_package_parameter_codes_sha256=parameter_hash(old_integer.parameters),
                      parent_package_exact=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numpy-expected', required=True, choices=('2.3.5',))
    parser.add_argument('--numpy-runtime', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.numpy_expected != np.__version__:
        raise ValueError(f'NumPy runtime mismatch: {np.__version__}')
    if torch.cuda.is_available() or torch.cuda.is_initialized():
        raise RuntimeError('diagnostic requires CUDA hidden')
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    args.output.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    shutil.copyfile(source, args.output / source.name)
    runtime = runtime_identity(args.numpy_runtime)
    payload, snapshot = load_dataset_snapshot(base.TRAIN)
    if sha256(base.TRAIN) != base.TRAIN_HASH:
        raise ValueError('training manifest changed')
    cache = verify_cache(snapshot)
    dataset = FullFrameDataset(snapshot.rows, 'train', mosaic=False)
    window = ReplayWindow(dataset, payload['replay_sampling'], 10)
    parent = torch.load(PARENT, map_location='cpu', weights_only=False)
    verify_parent(parent, snapshot, window)
    original = torch.load(base.CHECKPOINT, map_location='cpu', weights_only=False)
    source_model = RoadYOLOS4().eval()
    source_model.load_state_dict(original['model'], strict=True)
    model, optimizer = frozen.make_model(source_model.folded_conv_state(), torch.device('cpu'))
    model.load_state_dict(parent['model'], strict=True)
    optimizer.load_state_dict(parent['optimizer'])
    restore_rng(parent['rng_state'])
    old_integer, old_manifest = load_package(frozen.OUT / 'package')
    sample = dataset[0][0]
    traces = [trace(model, old_integer, sample, 'parent_pre_diagnostic')]
    source_sha256 = {str(path.relative_to(base.PROJECT)).replace('\\', '/'): sha256(path)
                     for path in (source, Path(base.__file__), Path(frozen.__file__),
                                  Path(__file__).with_name('qat_exact.py'),
                                  base.PROJECT / 'cnn/train.py', base.PROJECT / 'cnn/loss.py',
                                  base.PROJECT / 'cnn/model.py', base.PROJECT / 'cnn/dataset.py',
                                  base.PROJECT / 'cnn/disk_cache.py', base.PROJECT / 'cnn/replay_sampling.py')}
    receipt = dict(format='road-yolo-numpy235-runtime-receipt-v1', runtime=runtime,
        parent_checkpoint_sha256=PARENT_SHA256, parent_payload_sha256=old_manifest['payload_sha256'],
        source_checkpoint_sha256=base.CHECKPOINT_HASH, dataset_sha256=snapshot.manifest_sha256,
        dataset_content_sha256=snapshot.dataset_content_sha256, cache_compatibility=cache,
        source_sha256=source_sha256, no_gpu=True, diagnostic_only=True)
    save(args.output / 'runtime_receipt.json', receipt)
    receipt_sha256 = sha256(args.output / 'runtime_receipt.json')
    control_identity = dict(kind='numpy235_CPU_QAT_diagnostic_control', candidate=False,
        runtime_receipt_sha256=receipt_sha256, parent_checkpoint_sha256=PARENT_SHA256,
        dataset_sha256=snapshot.manifest_sha256,
        dataset_content_sha256=snapshot.dataset_content_sha256,
        sampling_sha256=window.sampling_sha256, numpy_version=np.__version__)
    preflight = dict(format='road-yolo-qat-numpy235-control-v1', diagnostic_only=True,
        candidate=False, optimizer_updates_published=0, no_gpu=True, runtime=runtime,
        runtime_receipt_sha256=receipt_sha256, control_identity=control_identity,
        parent_checkpoint_sha256=PARENT_SHA256, parent_payload_sha256=old_manifest['payload_sha256'],
        source_checkpoint_sha256=base.CHECKPOINT_HASH, dataset_sha256=snapshot.manifest_sha256,
        dataset_content_sha256=snapshot.dataset_content_sha256, cache_compatibility=cache,
        frozen_stem=True, convolution_layers=len(old_integer.parameters),
        source_sha256=source_sha256,
        trace=traces[0])
    save(args.output / 'preflight.json', preflight)
    history = []
    for local_update in range(2):
        print(json.dumps(dict(event='numpy235_diagnostic_update_start',
                              global_update=11 + local_update)), flush=True)
        record = frozen.update(model, optimizer, dataset, window, local_update,
                               torch.device('cpu'))
        record.update(global_update=11 + local_update, schedule_update=local_update + 1)
        history.append(record)
        traces.append(trace(model, None, sample, f'after_diagnostic_update_{11 + local_update}'))
        if local_update == 0:
            control_state = dict(format='road-yolo-numpy235-control-checkpoint-v1',
                checkpoint_kind='runtime_diagnostic_control', phase='qat', candidate=False,
                formal_acceptance=False, identity=control_identity,
                model=copy.deepcopy(model.state_dict()),
                optimizer=copy.deepcopy(optimizer.state_dict()),
                rng_state=copy.deepcopy(rng_state()), trained_steps=11, next_update=11,
                presentations=242, gradients_pending=False,
                sample_history=copy.deepcopy(parent['sample_history'] + history))
            checkpoint_path = args.output / 'control_update_0011.pt'
            checkpoint_sha256 = base.commit(checkpoint_path, control_state)
            reloaded = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
            if (reloaded.get('candidate') is not False or reloaded.get('identity') != control_identity
                    or reloaded.get('trained_steps') != 11 or reloaded.get('next_update') != 11
                    or len(reloaded.get('sample_history', [])) != 11
                    or len(reloaded.get('optimizer', {}).get('state', {})) != 132):
                raise ValueError('serialized NumPy 2.3.5 control checkpoint mismatch')
            print(json.dumps(dict(event='numpy235_control_checkpoint_verified',
                checkpoint=str(checkpoint_path.resolve()), checkpoint_sha256=checkpoint_sha256,
                candidate=False)), flush=True)
        print(json.dumps(dict(event='numpy235_diagnostic_update_complete',
                              global_update=11 + local_update)), flush=True)
    result = dict(preflight, passed=True, completed_diagnostic_updates=2,
        optimizer_updates_executed_in_memory=2, optimizer_updates_published=0,
        candidate_checkpoint_written=False, control_checkpoint_written=True,
        control_checkpoint_sha256=checkpoint_sha256,
        parent_checkpoint_unchanged=sha256(PARENT) == PARENT_SHA256,
        original_FP32_checkpoint_unchanged=sha256(base.CHECKPOINT) == base.CHECKPOINT_HASH,
        sample_history=history, traces=traces, formal_acceptance=False,
        conclusion_scope='runtime_diagnostic_only_not_training_or_accuracy_evidence')
    save(args.output / 'result.json', result)
    print(json.dumps(dict(event='numpy235_control_passed', updates=2,
                          output=str(args.output.resolve()))), flush=True)


if __name__ == '__main__':
    main()
