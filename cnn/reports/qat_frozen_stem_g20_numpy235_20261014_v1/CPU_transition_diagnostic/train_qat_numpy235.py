"""Run the fixed G10-to-G20 continuation under the verified NumPy 2.3.5 runtime."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import torch

from cnn import disk_cache
from cnn.disk_cache import ValidatedCacheBinding, preprocessing_identity
from cnn.model import RoadYOLOS4
from cnn.replay_sampling import ReplayWindow
from cnn.train import load_dataset_snapshot, make_frame_dataset, protocol_hash, sha256
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem as frozen
from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production.run_trained_integer import save
from cnn.hw_validation.production.trained_integer import load_package

OUT = base.PROJECT / 'cnn/reports/qat_frozen_stem_g20_numpy235_20261014_v1'
RUN = base.PROJECT / 'cnn/runs/qat_frozen_stem_g20_numpy235_20261014_v1'
CHECK_DIR = OUT / 'integration_check_v1'
NUMPY_ROOT = base.PROJECT.parents[1] / '.tools/road_yolo_numpy_235_20261014/numpy'
CONTROL = base.PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1/numpy235_control'
CONTROL_RESULT_SHA256 = 'd5275e4f6e6798586caf01d0ee02d38e1a69fa573c3d30f295c32cb83d80ae4a'
RUNTIME_RECEIPT_SHA256 = '1d98574cc13f576c11ed0f5ae96e7a339046e43b45cf9f41fb384d6ed285becb'
CROSS_RUNTIME = base.PROJECT / 'cnn/reports/qat_runtime_repair_20261014_v1/cross_runtime_parent_integer.json'
CROSS_RUNTIME_SHA256 = '82e0fa11a059b351ccf159c6963e4afeb4199782dccd9c5c91d7880c168bb328'
WORKER_MODULE = 'cnn.hw_validation.production.train_qat_numpy235'
_INSTALLED = False


def _read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def control_evidence():
    result_path, runtime_path = CONTROL / 'result.json', CONTROL / 'runtime_receipt.json'
    if sha256(result_path) != CONTROL_RESULT_SHA256 or sha256(runtime_path) != RUNTIME_RECEIPT_SHA256:
        raise ValueError('NumPy 2.3.5 control evidence changed')
    if sha256(CROSS_RUNTIME) != CROSS_RUNTIME_SHA256:
        raise ValueError('cross-runtime parent integer receipt changed')
    result, receipt, cross = _read(result_path), _read(runtime_path), _read(CROSS_RUNTIME)
    cache = result.get('cache_compatibility', {})
    if (result.get('passed') is not True or result.get('candidate') is not False
            or result.get('no_gpu') is not True or result.get('completed_diagnostic_updates') != 2
            or result.get('candidate_checkpoint_written') is not False
            or result.get('parent_checkpoint_sha256') != continuation.PARENT_SHA256
            or result.get('runtime_receipt_sha256') != RUNTIME_RECEIPT_SHA256
            or result.get('trace', {}).get('trace_tensors') != 181
            or result.get('trace', {}).get('accumulator_tensors') != 67
            or result.get('trace', {}).get('all_integer_capture_tensors') != 248
            or result.get('trace', {}).get('parent_package_exact') is not True
            or cache.get('passed') is not True or cache.get('records') != 103
            or cache.get('raw_rgb_bytes_exact') is not True
            or cache.get('centered_inputs_targets_keys_exact') is not True
            or cache.get('cached_numpy_version') != '2.4.6'
            or cache.get('diagnostic_numpy_version') != '2.3.5'
            or receipt.get('diagnostic_only') is not True or receipt.get('no_gpu') is not True
            or cross.get('passed') is not True or cross.get('captures') != 248
            or cross.get('reference_numpy_version') != '2.4.6'
            or cross.get('comparison_numpy_version') != '2.3.5'
            or cross.get('parent_payload_sha256') != result.get('parent_payload_sha256')
            or cross.get('control_preflight_sha256') != sha256(CONTROL / 'preflight.json')
            or cross.get('trace_hashes', {}).get('all_integer_capture_sha256')
                != result.get('trace', {}).get('all_integer_capture_sha256')
            or cross.get('trace_hashes', {}).get('parameter_codes_sha256')
                != result.get('trace', {}).get('parameter_codes_sha256')):
        raise ValueError('NumPy 2.3.5 control did not pass the declared transition gates')
    return result, receipt, cross


def native_runtime_identity():
    _result, receipt, _cross = control_evidence()
    expected = receipt['runtime']
    root = Path(np.__file__).resolve().parent
    if (root != NUMPY_ROOT.resolve() or np.__version__ != '2.3.5'
            or torch.__version__ != expected['torch'] or sys.version != expected['python']):
        raise ValueError('project-isolated NumPy 2.3.5 is required')
    actual = {relative: sha256(NUMPY_ROOT.parent / relative)
              for relative in expected['native_sha256']}
    if actual != expected['native_sha256']:
        raise ValueError('NumPy 2.3.5 native files differ from the passed control')
    return dict(policy='explicit_numpy_246_to_235_runtime_transition_v1',
        numpy_root=str(root), numpy_version=np.__version__, native_sha256=actual,
        generator_sha256=actual['numpy/random/_generator.cp313-win_amd64.pyd'],
        torch_root=str(Path(torch.__file__).resolve().parent), torch_version=torch.__version__,
        control_result_sha256=CONTROL_RESULT_SHA256,
        runtime_receipt_sha256=RUNTIME_RECEIPT_SHA256,
        cross_runtime_parent_integer_sha256=CROSS_RUNTIME_SHA256)


def expected_cache_receipt():
    result, _receipt, _cross = control_evidence()
    cache = result['cache_compatibility']
    return dict(schema_version=1, passed=True,
        status='passed_exact_cache_compatibility_with_explicit_runtime_transition',
        dataset_sha256=result['dataset_sha256'],
        dataset_content_sha256=result['dataset_content_sha256'], records=cache['records'],
        split_counts=cache['split_counts'], cache_root=_read(frozen.OUT / 'cache_receipt.json')['cache_root'],
        cache_index_sha256=cache['cache_index_sha256'], rgb_sha256=cache['rgb_sha256'],
        raw_rgb_bytes_exact=cache['raw_rgb_bytes_exact'],
        centered_inputs_targets_keys_exact=cache['centered_inputs_targets_keys_exact'],
        runtime_transition=dict(source_numpy='2.4.6', current_numpy='2.3.5',
            source_cache_preprocessing_retained=True,
            numeric_and_preprocessing_sources_unchanged=True,
            control_result_sha256=CONTROL_RESULT_SHA256,
            runtime_receipt_sha256=RUNTIME_RECEIPT_SHA256,
            cross_runtime_parent_integer_sha256=CROSS_RUNTIME_SHA256),
        cache_used_for_training=True, gpu_used=False, candidate_training_started=False)


def transition_cache_binding(snapshot, receipt):
    root = Path(receipt['cache_root']).resolve()
    encoded = (root / 'index.json').read_bytes()
    index_sha256 = __import__('hashlib').sha256(encoded).hexdigest()
    metadata = json.loads(encoded)
    entries = metadata.get('entries', [])
    blob = root / 'rgb.bin'
    if (index_sha256 != receipt['cache_index_sha256']
            or metadata.get('dataset_sha256') != snapshot.manifest_sha256
            or metadata.get('dataset_content_sha256') != snapshot.dataset_content_sha256
            or metadata.get('rgb_sha256') != receipt['rgb_sha256']
            or sha256(blob) != receipt['rgb_sha256']
            or len(entries) != len(snapshot.rows) or len(snapshot.rows) != 103):
        raise ValueError('transition cache bytes or dataset binding changed')
    recorded, current = copy.deepcopy(metadata['preprocessing']), preprocessing_identity()
    recorded_numpy = recorded['libraries'].pop('numpy')
    current_numpy = current['libraries'].pop('numpy')
    if recorded_numpy != '2.4.6' or current_numpy != '2.3.5' or recorded != current:
        raise ValueError('cache preprocessing differs beyond explicit NumPy runtime transition')
    for index, (row, entry) in enumerate(zip(snapshot.rows, entries, strict=True)):
        if (entry.get('offset') != index * disk_cache.RECORD_BYTES
                or entry.get('image') != row['image']
                or entry.get('source_sha256') != row['image_sha256']
                or entry.get('row_sha256') != disk_cache.fingerprint(row)):
            raise ValueError('transition cache row binding changed')
    return ValidatedCacheBinding(snapshot, root, metadata, tuple(entries), index_sha256)


def prepare():
    native_runtime = native_runtime_identity()
    for path, digest in ((base.CHECKPOINT, base.CHECKPOINT_HASH),
                         (base.BASE / 'package/manifest.json', base.MANIFEST_HASH)):
        if sha256(path) != digest:
            raise ValueError(f'frozen source input changed: {path}')
    source_integer, source_manifest = load_package(base.BASE / 'package')
    if sha256(base.BASE / 'quantization.json') != source_manifest['provenance']['quantization_sha256']:
        raise ValueError('frozen quantization metadata changed')
    receipt_path = OUT / 'cache_receipt.json'
    expected_receipt = expected_cache_receipt()
    if not receipt_path.exists() or _read(receipt_path) != expected_receipt:
        raise ValueError('NumPy 2.3.5 transition cache receipt missing or stale')
    if sha256(continuation.PARENT) != continuation.PARENT_SHA256:
        raise ValueError('parent checkpoint changed')
    for relative, digest in continuation.PARENT_ARTIFACTS.items():
        if sha256(continuation.PARENT_OUT / relative) != digest:
            raise ValueError(f'parent artifact changed: {relative}')
    payload, snapshot = load_dataset_snapshot(base.TRAIN)
    if sha256(base.TRAIN) != base.TRAIN_HASH:
        raise ValueError('fixed training manifest changed')
    binding = transition_cache_binding(snapshot, expected_receipt)
    dataset = make_frame_dataset(snapshot.rows, 'train', base.TRAIN, mosaic=False,
        cache_root=binding.root, cache_index_sha256=binding.index_sha256, cache_binding=binding)
    window = ReplayWindow(dataset, payload['replay_sampling'], 10)
    parent = torch.load(continuation.PARENT, map_location='cpu', weights_only=False)
    parent_identity, parent_protocol = parent['identity'], parent['training_protocol']
    continuation.validate_parent(parent, parent_identity, parent_protocol, dataset, window)
    for relative, digest in parent_identity['source_sha256'].items():
        if sha256(base.PROJECT / relative) != digest:
            raise ValueError(f'parent source changed: {relative}')
    decision = base.read(continuation.PARENT_OUT / 'decision.json')
    comparison = base.read(continuation.PARENT_OUT / 'control_comparison.json')
    review = base.read(continuation.PARENT_OUT / 'independent_completion_review.json')
    if (decision.get('status') != 'COMPLETED_FROZEN_STEM_QAT_G10_DEVELOPMENT_RECOVERY'
            or decision.get('candidate_checkpoint_sha256') != continuation.PARENT_SHA256
            or comparison.get('bindings', {}).get('new_candidate_checkpoint_sha256') != continuation.PARENT_SHA256
            or review.get('verdict', {}).get('artifact_integrity') != 'PASS'):
        raise ValueError('reviewed parent decision changed')
    original = torch.load(base.CHECKPOINT, map_location='cpu', weights_only=False)
    source = RoadYOLOS4().eval()
    source.load_state_dict(original['model'], strict=True)
    if (original['dataset_content_sha256'] != snapshot.dataset_content_sha256
            or source.architecture_hash() != parent_identity['architecture_hash']
            or protocol_hash(source_integer.graph) != parent_identity['graph_sha256']
            or protocol_hash(source_integer.scales) != parent_identity['scales_sha256']
            or parent_identity['source_package_manifest_sha256'] != base.MANIFEST_HASH):
        raise ValueError('source FP32 dataset content changed')
    runtime_transition = dict(source_numpy_version=parent_identity['numpy_version'],
        current_numpy_version=np.__version__, intentional=True,
        control_result_sha256=CONTROL_RESULT_SHA256,
        runtime_receipt_sha256=RUNTIME_RECEIPT_SHA256,
        cross_runtime_parent_integer_sha256=CROSS_RUNTIME_SHA256,
        cache_receipt_sha256=sha256(receipt_path))
    schedule = [list(order) for order in window.orders]
    protocol = dict(parent_protocol,
        name='deployment_exact_qat_frozen_stem_continuation_numpy235_v1',
        prior_branch_updates=10, segment_updates=10, total_updates=20,
        global_qat_updates_after_segment=30, schedule_cycle=2,
        schedule_cycle_sha256=protocol_hash(schedule), cpu_resume_check_threads=1,
        gpu_worker_threads=2, runtime_transition=runtime_transition)
    identity = dict(parent_identity, numpy_version=np.__version__,
        protocol_sha256=protocol_hash(protocol),
        experiment_id='qat_frozen_stem_g20_numpy235_20261014_v1',
        native_runtime=native_runtime, runtime_transition=runtime_transition,
        parent_checkpoint_sha256=continuation.PARENT_SHA256,
        parent_identity=parent_identity, parent_identity_sha256=protocol_hash(parent_identity),
        parent_training_protocol=parent_protocol,
        parent_training_protocol_sha256=protocol_hash(parent_protocol),
        parent_sample_history_sha256=protocol_hash(parent['sample_history']),
        parent_decision_sha256=continuation.PARENT_ARTIFACTS['decision.json'],
        parent_control_comparison_sha256=continuation.PARENT_ARTIFACTS['control_comparison.json'],
        parent_export_parity_sha256=continuation.PARENT_ARTIFACTS['export_parity.json'])
    identity['source_sha256'] = dict(parent_identity['source_sha256'])
    for path in (Path(continuation.__file__), Path(__file__),
                 Path(__file__).with_name('test_qat_numpy235.py'),
                 Path(__file__).with_name('probe_qat_numpy235.py')):
        identity['source_sha256'][str(path.relative_to(base.PROJECT)).replace('\\', '/')] = sha256(path)
    ancestry = dict(parent_checkpoint=str(continuation.PARENT.relative_to(base.PROJECT)).replace('\\', '/'),
        parent_checkpoint_sha256=continuation.PARENT_SHA256, parent_trained_steps=10,
        parent_presentations=220, parent_identity=parent_identity,
        parent_identity_sha256=protocol_hash(parent_identity),
        parent_training_protocol=parent_protocol,
        parent_training_protocol_sha256=protocol_hash(parent_protocol),
        parent_sample_history_sha256=protocol_hash(parent['sample_history']))
    return dataset, window, source.folded_conv_state(), identity, protocol, ancestry, parent


def install():
    global _INSTALLED
    values = dict(OUT=OUT, RUN=RUN, CHECK_DIR=CHECK_DIR, WORKER_MODULE=WORKER_MODULE,
                  prepare=prepare, native_runtime_identity=native_runtime_identity)
    if _INSTALLED:
        if any(getattr(continuation, name) is not value and getattr(continuation, name) != value
               for name, value in values.items()):
            raise RuntimeError('NumPy 2.3.5 adapter installation was altered')
        return
    for name, value in values.items():
        setattr(continuation, name, value)
    _INSTALLED = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'execute', 'worker'))
    parser.add_argument('--pause-request', type=Path)
    parser.add_argument('--supervised-start', action='store_true')
    parser.add_argument('--resume', type=Path)
    args = parser.parse_args()
    install()
    if args.action == 'check':
        OUT.mkdir(exist_ok=True)
        receipt = expected_cache_receipt()
        path = OUT / 'cache_receipt.json'
        if not path.exists():
            save(path, receipt)
        if _read(path) != receipt:
            raise ValueError('NumPy 2.3.5 transition receipt changed')
        continuation.cpu_check()
    elif args.action == 'execute':
        continuation.execute()
    else:
        continuation.worker(args)


if __name__ == '__main__':
    main()
