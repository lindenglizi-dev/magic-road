"""One train-only aligned-scale MSE calibration experiment; no weight updates."""
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
from cnn.hw_validation.production.run_trained_integer import (
    PROJECT, CHECKPOINT, CHECKPOINT_HASH, TRAIN, TRAIN_HASH, VALIDATION, VAL_HASH, BASELINE, save, centered)
from cnn.hw_validation.production.trained_integer import (
    load_package, float_forward, encode_parameters, write_package)
from cnn.hw_validation.production.diagnose_trained_integer import error

PREVIOUS = PROJECT / 'cnn/reports/replay_g10_integer_20261013_v2'
PREVIOUS_MANIFEST_HASH = '64ad4e3284c4fdf90fa9f9ddc468db00159c46b152a13d440753030a979624f9'
BINS = 16384
RATIOS = np.geomspace(1 / 16, 1, 65)
POSTPROCESS = {'top_k_per_class': 128, 'max_boxes_per_class': 32, 'nms_iou': .5,
               'score_floor_uint16': 3276}


def validate_baseline(baseline):
    if (baseline.get('checkpoint_sha256') != CHECKPOINT_HASH
            or baseline.get('image_count') != 17
            or baseline.get('diagnostic_metrics_at_0_5', {}).get('protocol') != 'road_greedy_101point_ap_v1'
            or baseline.get('postprocess_contract') != POSTPROCESS):
        raise ValueError('baseline checkpoint or evaluation protocol differs')


def add_histogram(histogram, values, maximum):
    flat = values.astype(np.float64, copy=False).reshape(-1)
    if not np.isfinite(flat).all() or np.any(np.abs(flat) > maximum * (1 + 1e-6)):
        raise ValueError('new observations outside pinned calibration range')
    index = np.clip(((flat + maximum) * (BINS / (2 * maximum))).astype(np.int64), 0, BINS - 1)
    histogram[0] += np.bincount(index, minlength=BINS)
    histogram[1] += np.bincount(index, weights=flat, minlength=BINS)
    histogram[2] += np.bincount(index, weights=flat * flat, minlength=BINS)


def choose_scale(histogram, maximum):
    count, sums, squares = histogram
    if not count.sum() or maximum <= 0:
        raise ValueError('empty calibration component')
    centres = np.linspace(-maximum, maximum, BINS, endpoint=False) + maximum / BINS
    candidates = []
    for ratio in RATIOS:
        scale = maximum / 127 * ratio
        rounded = np.rint(centres / scale)
        reconstructed = np.clip(rounded, -128, 127) * scale
        # Exact first/second moments; only quantizer-bin boundary assignment is approximate.
        mse = float(np.maximum(squares - 2 * reconstructed * sums + reconstructed**2 * count, 0).sum() / count.sum())
        clipped = float(count[(rounded < -128) | (rounded > 127)].sum() / count.sum())
        candidates.append({'scale': float(scale), 'ratio_to_max_abs': float(ratio), 'mse': mse,
                           'histogram_clipped_fraction': clipped})
    best = min(candidates, key=lambda row: (row['mse'], -row['scale']))
    return best, candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(2)
    started = time.perf_counter()
    for path, expected in [(CHECKPOINT, CHECKPOINT_HASH), (TRAIN, TRAIN_HASH),
                           (PREVIOUS / 'package/manifest.json', PREVIOUS_MANIFEST_HASH)]:
        if sha256(path) != expected:
            raise ValueError(f'input identity changed: {path}')
    previous, manifest = load_package(PREVIOUS / 'package')
    old_calibration = json.loads((PREVIOUS / 'calibration.json').read_text(encoding='utf-8'))
    if sha256(PREVIOUS / 'calibration.json') != manifest['provenance']['calibration_sha256']:
        raise ValueError('previous calibration identity changed')
    _, snapshot = load_dataset_snapshot(TRAIN)
    if snapshot.dataset_content_sha256 != manifest['provenance']['calibration_content_sha256']:
        raise ValueError('training content differs')
    dataset = make_frame_dataset(snapshot.rows, 'train', TRAIN, mosaic=False)
    train_images = [{'image': row['image'], 'sha256': row['image_sha256']} for row in dataset.rows]
    if len(dataset) != 86 or train_images != old_calibration['train_images']:
        raise ValueError('calibration training selection changed')
    model = RoadYOLOS4().eval()
    model.load_state_dict(torch.load(CHECKPOINT, weights_only=False, map_location='cpu')['model'])
    folded = model.folded_conv_state()
    graph = previous.graph
    groups = old_calibration['scale_groups']
    # Views alias existing values: observe material convolution/pool/residual outputs
    # once, not their duplicated concat/split/nearest representations.
    material = {node['output'] for node in graph['nodes'] if node['op'] in ('conv', 'maxpool', 'residual_view')
                and node['dtype'] == 'int8'}
    histograms, owners, maxima = {}, {}, {}
    for index, group in enumerate(groups):
        contributors = sorted(material.intersection(group['members']))
        if not contributors:
            continue
        histograms[index] = np.zeros((3, BINS), dtype=np.float64)
        maxima[index] = group['scale'] * 127
        owners.update({name: index for name in contributors})
    with torch.inference_mode():
        for index in range(len(dataset)):
            image, _, _ = dataset[index]
            values = float_forward(graph, folded, centered(image).astype(np.float32))
            for name, group in owners.items():
                add_histogram(histograms[group], values[name], maxima[group])
            if index == 0 or (index + 1) % 16 == 0 or index == len(dataset) - 1:
                print(f'train-only MSE histograms {index + 1}/86', flush=True)
    scales = dict(previous.scales)
    choices = []
    for index, histogram in histograms.items():
        best, candidates = choose_scale(histogram, maxima[index])
        members = groups[index]['members']
        for name in members:
            scales[name] = best['scale']
        choices.append({'members': members, 'contributors': [name for name, owner in owners.items() if owner == index],
                        'observations': int(histogram[0].sum()), 'selected': best, 'candidates': candidates})
    save(args.output / 'calibration.json', {'split': 'train', 'images': 86, 'train_images': train_images,
         'method': 'aligned-component histogram MSE; 16384 signed bins; fixed 65 scale ratios [1/16,1]',
         'views_not_double_counted': True, 'choices': choices, 'scales': scales,
         'selection_uses_validation': False, 'previous_manifest_sha256': PREVIOUS_MANIFEST_HASH})
    parameters, quantization = encode_parameters(graph, folded, scales)
    save(args.output / 'quantization.json', quantization)
    provenance = dict(manifest['provenance'])
    provenance.update(calibration_sha256=sha256(args.output / 'calibration.json'),
                      quantization_sha256=sha256(args.output / 'quantization.json'),
                      previous_manifest_sha256=PREVIOUS_MANIFEST_HASH)
    provenance['source_sha256'] = dict(provenance['source_sha256'])
    for path in (Path(__file__), Path(__file__).with_name('test_calibrate_mse.py')):
        provenance['source_sha256'][str(path.relative_to(PROJECT)).replace('\\', '/')] = sha256(path)
    write_package(args.output / 'package', graph, parameters, scales, provenance)
    integer, current = load_package(args.output / 'package')
    identity = {'payload_sha256': current['payload_sha256'], 'physical_sha256': current['physical_sha256'],
                'manifest_sha256': sha256(args.output / 'package/manifest.json')}
    comparisons = []
    with torch.inference_mode():
        for index in range(4):
            image, _, key = dataset[index]
            data = centered(image)
            reference = float_forward(graph, folded, data.astype(np.float32))
            _, _, old_values = previous.forward(data, capture=True)
            _, _, new_values = integer.forward(data, capture=True)
            names = ['stem.conv', 'down2.dw.conv', 'down2.pw.conv'] + graph['outputs']
            comparisons.append({'train_key': key, 'nodes': {name: {
                'max_abs': error(reference[name], old_values[name].astype(np.float64) * previous.scales[name]),
                'mse_calibration': error(reference[name], new_values[name].astype(np.float64) * scales[name])}
                for name in names}})
            print(f'train-only full-network comparison {index + 1}/4', flush=True)
    save(args.output / 'train_error_comparison.json', comparisons)
    # Calibration is now frozen. Exactly one same-protocol validation, no scale retuning.
    if sha256(VALIDATION) != VAL_HASH:
        raise ValueError('validation manifest changed')
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    validate_baseline(baseline)
    rows, total = load_validation_subset(VALIDATION, None, 17)
    val = FullFrameDataset(rows, 'val')
    if total != 17 or dataset_content_hash(val.rows) != baseline['evaluated_image_content_sha256']:
        raise ValueError('validation image identity differs')
    predictions, truth, ignores = [], [], []
    for index, row in enumerate(val.rows):
        image, _, _ = val[index]
        heads, _, _ = integer.forward(centered(image))
        detections = postprocess(heads, (3276, 3276))
        predictions.extend(dict(image_id=row['image'], label=d['label'], box=[v / 256 for v in d['box_q8']],
                                score=d['score_uint16'] / 65536) for d in detections)
        truth.extend(dict(image_id=row['image'], label=label, box=box)
                     for label, box in zip(row['labels'], row['boxes'], strict=True))
        metadata = row.get('ignore_metadata', [{'label': -1, 'crowd': False}] * len(row['ignore_boxes']))
        ignores.extend(dict(image_id=row['image'], label=region['label'], box=box, crowd=region['crowd'])
                       for box, region in zip(row['ignore_boxes'], metadata, strict=True))
        print(f'frozen-calibration validation {index + 1}/17', flush=True)
    if truth != baseline['truth'] or ignores != baseline['ignores']:
        raise ValueError('evaluation GT/ignore changed')
    metrics = report(predictions, truth, ignores, thresholds=(.5, .5))
    delta = {name: (metrics['classes'][name]['ap50'] - baseline['diagnostic_metrics_at_0_5']['classes'][name]['ap50']) * 100
             for name in ('person', 'vehicle')}
    save(args.output / 'development17.json', {'status': 'MSE_PTQ_diagnostic_not_formal_acceptance',
         'package_identity': identity, 'checkpoint_sha256': CHECKPOINT_HASH,
         'dataset_sha256': VAL_HASH, 'evaluated_image_content_sha256': dataset_content_hash(val.rows),
         'image_count': 17, 'truth': truth, 'ignores': ignores, 'predictions': predictions,
         'diagnostic_metrics_at_0_5': metrics, 'AP50_delta_pp_vs_FP32': delta,
         'postprocess_contract': baseline['postprocess_contract'], 'baseline_sha256': sha256(BASELINE),
         'map50_drop_pp': -sum(delta.values()) / 2, 'acceptance_eligible': False})
    save(args.output / 'status.json', {'status': 'calibration_and_evaluation_completed',
         'training_started': False, 'cuda_initialized': torch.cuda.is_initialized(), 'package_identity': identity,
         'seconds': time.perf_counter() - started, 'map50_drop_pp': -sum(delta.values()) / 2,
         'formal_acceptance': False, 'production_release': False})
    print(json.dumps({'metrics': metrics, 'AP50_delta_pp': delta}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
