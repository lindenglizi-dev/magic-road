"""Bounded CPU PTQ export/calibration/evaluation for the selected replay-G10."""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from cnn.evaluate import load_validation_subset
from cnn.integer import postprocess
from cnn.metrics import report
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset, FullFrameDataset, dataset_content_hash, sha256
from cnn.hw_validation.production.trained_integer import (
    build_graph, float_forward, aligned_scales, encode_parameters, IntegerModel, write_package, load_package)

PROJECT = Path(__file__).resolve().parents[3]
CHECKPOINT = PROJECT / 'cnn/runs/ac_replay_g10_20261013_v1/last.pt'
TRAIN = PROJECT / 'cnn/reports/ac_optimization_20261013_v1/trial/dataset.json'
VALIDATION = PROJECT / 'cnn/reports/ac_g10_20261013_v1/dataset.json'
BASELINE = PROJECT / 'cnn/reports/ac_optimization_20261013_v1/trial/development17.json'
CHECKPOINT_HASH = 'e7e6a0f514b39417451ff90cec32e7f5adc862136bdf3adeac988c4d454fa262'
TRAIN_HASH = '5b25180c25d1f3835ea5248b107f19d2fc39cfac166500c45c87c2dfde08fd59'
VAL_HASH = '6af48b5ec8da6550a5d0af31db8b8f58d1fc8c9960df0eda9a66ad7c94f5f5e1'


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def centered(image):
    value = image.permute(1, 2, 0).numpy()
    if not np.isfinite(value).all() or np.any(value != np.rint(value)) or np.any(value < -128) or np.any(value > 127):
        raise ValueError('preprocessing not exact pixel-minus128 INT8')
    return value.astype(np.int8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    started = time.perf_counter()
    for path, expected in [(CHECKPOINT, CHECKPOINT_HASH), (TRAIN, TRAIN_HASH), (VALIDATION, VAL_HASH)]:
        if sha256(path) != expected:
            raise ValueError(f'input changed: {path}')
    graph = build_graph()
    state = torch.load(CHECKPOINT, weights_only=False, map_location='cpu')
    model = RoadYOLOS4().eval()
    if state['architecture_hash'] != model.architecture_hash():
        raise ValueError('checkpoint architecture differs')
    model.load_state_dict(state['model'], strict=True)
    folded = model.folded_conv_state()
    _, snapshot = load_dataset_snapshot(TRAIN)
    if snapshot.dataset_content_sha256 != state['dataset_content_sha256']:
        raise ValueError('training image content changed')
    dataset = make_frame_dataset(snapshot.rows, 'train', TRAIN, mosaic=False)
    if len(dataset) != 86:
        raise ValueError('expected 86 training calibration images')
    ranges, parity = {}, []
    with torch.inference_mode():
        for index in range(len(dataset)):
            image, _, key = dataset[index]
            values = float_forward(graph, folded, centered(image).astype(np.float32))
            if index < 4:
                expected = model(image.unsqueeze(0))
                errors = []
                for output, name in zip(expected, graph['outputs'], strict=True):
                    actual = torch.from_numpy(values[name].transpose(2, 0, 1)).unsqueeze(0)
                    torch.testing.assert_close(actual, output, atol=1e-3, rtol=1e-5)
                    errors.append(float((actual - output).abs().max()))
                parity.append({'train_key': key, 'max_abs_by_head': errors})
            for name, value in values.items():
                if not np.isfinite(value).all():
                    raise FloatingPointError(name)
                item = ranges.setdefault(name, {'min': float('inf'), 'max': float('-inf'), 'max_abs': 0., 'images': 0})
                item['min'] = min(item['min'], float(value.min()))
                item['max'] = max(item['max'], float(value.max()))
                item['max_abs'] = max(abs(item['min']), abs(item['max']))
                item['images'] += 1
            if index == 0 or (index + 1) % 16 == 0 or index == len(dataset) - 1:
                print(f'train-only calibration {index + 1}/{len(dataset)}', flush=True)
    scales, groups = aligned_scales(graph, ranges)
    save(args.output / 'calibration.json', {'split': 'train', 'images': 86, 'ranges': ranges,
         'scale_groups': groups, 'method': 'max_abs/127 per aligned component; input scale 1; raw heads 1/256',
         'float_graph_parity': parity, 'parity_atol': 1e-3, 'parity_rtol': 1e-5,
         'train_images': [{'image': row['image'], 'sha256': row['image_sha256']} for row in dataset.rows]})
    parameters, quantization = encode_parameters(graph, folded, scales)
    save(args.output / 'quantization.json', quantization)
    sources = ['cnn/hw_validation/production/trained_integer.py',
               'cnn/hw_validation/production/run_trained_integer.py',
               'cnn/hw_validation/production/test_trained_integer.py', 'cnn/train.py', 'cnn/evaluate.py',
               'cnn/hw_validation/production/diagnose_trained_integer.py',
               'cnn/metrics.py', 'cnn/model.py', 'cnn/integer.py', 'cnn/contract.json',
               'cnn/hw_validation/production/graph.py', 'cnn/hw_validation/production/deployment_contract.json']
    provenance = {'checkpoint': str(CHECKPOINT), 'checkpoint_sha256': CHECKPOINT_HASH,
                  'calibration_dataset_sha256': TRAIN_HASH, 'calibration_content_sha256': snapshot.dataset_content_sha256,
                  'calibration_sha256': sha256(args.output / 'calibration.json'),
                  'quantization_sha256': sha256(args.output / 'quantization.json'),
                  'source_sha256': {name: sha256(PROJECT / name) for name in sources}}
    write_package(args.output / 'package', graph, parameters, scales, provenance)
    integer, manifest = load_package(args.output / 'package')
    package_identity = {'payload_sha256': manifest['payload_sha256'], 'physical_sha256': manifest['physical_sha256'],
                        'manifest_sha256': sha256(args.output / 'package/manifest.json')}
    original = IntegerModel(graph, parameters, scales)
    sample, _, _ = dataset[0]
    first_heads, _, _ = original.forward(centered(sample))
    saved_heads, _, saved_values = integer.forward(centered(sample), capture=True)
    for left, right in zip(first_heads, saved_heads, strict=True):
        np.testing.assert_array_equal(left, right)
    np.savez_compressed(args.output / 'golden_train0.npz', **saved_values)
    save(args.output / 'golden_train0.json', {'image': dataset.rows[0]['image'],
         'image_sha256': dataset.rows[0]['image_sha256'], 'package_sha256': manifest['payload_sha256'],
         'package_identity': package_identity,
         'npz_sha256': sha256(args.output / 'golden_train0.npz'),
         'meaning': 'logical HWC tensors; :acc INT32 and :pre Q7.8 before SiLU; not DDR tile bytes',
         'tensors': {name: {'shape': list(array.shape), 'dtype': str(array.dtype)} for name, array in saved_values.items()},
         'package_reload_heads_bit_exact': True})
    print('67-convolution integer forward and package reload PASS', flush=True)
    del saved_values
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    rows, total = load_validation_subset(VALIDATION, None, 17)
    val = FullFrameDataset(rows, 'val')
    if (total != 17 or dataset_content_hash(val.rows) != baseline['evaluated_image_content_sha256'] or
            baseline['checkpoint_sha256'] != CHECKPOINT_HASH):
        raise ValueError('baseline validation identity mismatch')
    predictions, truth, ignores, timings, statistics = [], [], [], [], []
    for index, row in enumerate(val.rows):
        image, _, _ = val[index]
        before = time.perf_counter()
        heads, stats, _ = integer.forward(centered(image))
        timings.append(time.perf_counter() - before)
        statistics.append({'image': row['image'], 'nodes': stats})
        detections = postprocess(heads, (3276, 3276))
        predictions.extend(dict(image_id=row['image'], label=det['label'],
                                box=[v / 256 for v in det['box_q8']], score=det['score_uint16'] / 65536)
                           for det in detections)
        truth.extend(dict(image_id=row['image'], label=label, box=box)
                     for label, box in zip(row['labels'], row['boxes'], strict=True))
        metadata = row.get('ignore_metadata', [{'label': -1, 'crowd': False}] * len(row['ignore_boxes']))
        ignores.extend(dict(image_id=row['image'], label=region['label'], box=box, crowd=region['crowd'])
                       for box, region in zip(row['ignore_boxes'], metadata, strict=True))
        print(f'INT8 development validation {index + 1}/17 ({timings[-1]:.2f}s CPU forward)', flush=True)
    if truth != baseline['truth'] or ignores != baseline['ignores']:
        raise ValueError('baseline GT or ignores differ')
    metrics = report(predictions, truth, ignores, thresholds=(.5, .5))
    delta = {name: {field: (metrics['classes'][name][field] - baseline['diagnostic_metrics_at_0_5']['classes'][name][field]) * 100
                    for field in ('precision', 'recall', 'ap50', 'ap50_95')} for name in ('person', 'vehicle')}
    mean_drop = -sum(delta[name]['ap50'] for name in delta) / 2
    save(args.output / 'development17.json', {'status': 'PTQ_diagnostic_not_formal_acceptance',
         'inference': 'INT8_CNN_INT32_bias_acc_INT16_Q7.8_heads_fixed_postprocess',
         'checkpoint_sha256': CHECKPOINT_HASH, 'package_sha256': manifest['payload_sha256'],
         'package_identity': package_identity,
         'dataset_sha256': VAL_HASH, 'evaluated_image_content_sha256': dataset_content_hash(val.rows),
         'image_count': 17, 'predictions': predictions, 'truth': truth, 'ignores': ignores,
         'postprocess_contract': baseline['postprocess_contract'], 'diagnostic_metrics_at_0_5': metrics,
         'delta_pp_vs_FP32': delta, 'map50_drop_pp': mean_drop, 'quantization_drop_at_most_1pp': mean_drop <= 1.,
         'cpu_forward_seconds': timings, 'baseline_sha256': sha256(BASELINE), 'acceptance_eligible': False,
         'limitation': baseline['limitation'] + '; only 17 development frames, PTQ not QAT'})
    save(args.output / 'saturation_diagnostics.json', statistics)
    save(args.output / 'status.json', {'status': 'completed_PTQ_export_and_17_image_integer_validation',
         'package_identity': package_identity,
         'cpu_only': True, 'cuda_initialized': torch.cuda.is_initialized(), 'training_started': False,
         'package_bytes': manifest['payload_bytes'], 'physical_bytes': manifest['physical_bytes'],
         'conv_layers': 67, 'full_integer_forward': True, 'float_graph_parity': True,
         'package_reload_bit_exact': True, 'map50_drop_pp': mean_drop,
         'quantization_drop_at_most_1pp': mean_drop <= 1., 'seconds': time.perf_counter() - started,
         'production_release': False, 'RTL_compared': False, 'formal_acceptance': False})
    print(json.dumps({'metrics': metrics, 'delta_pp': delta, 'map50_drop_pp': mean_drop}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
