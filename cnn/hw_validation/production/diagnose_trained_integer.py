"""Train-only PTQ diagnosis; FP64 convolution used solely as independent oracle."""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from cnn.hw_validation.production.trained_integer import load_package, float_forward
from cnn.hw_validation.production.run_trained_integer import CHECKPOINT, TRAIN, centered, save
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset, sha256


def error(reference, actual):
    reference, actual = reference.astype(np.float64), actual.astype(np.float64)
    mse = float(np.mean((reference - actual) ** 2))
    power = float(np.mean(reference ** 2))
    return {'rmse': mse ** 0.5, 'normalized_rmse': (mse / max(power, 1e-30)) ** 0.5,
            'max_abs_error': float(np.max(np.abs(reference - actual)))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    torch.set_num_threads(2)
    started = time.perf_counter()
    integer, manifest = load_package(args.run / 'package')
    if sha256(CHECKPOINT) != manifest['provenance']['checkpoint_sha256']:
        raise ValueError('checkpoint changed')
    _, snapshot = load_dataset_snapshot(TRAIN)
    if snapshot.dataset_content_sha256 != manifest['provenance']['calibration_content_sha256']:
        raise ValueError('training data changed')
    dataset = make_frame_dataset(snapshot.rows, 'train', TRAIN, mosaic=False)
    model = RoadYOLOS4().eval()
    model.load_state_dict(torch.load(CHECKPOINT, map_location='cpu', weights_only=False)['model'])
    folded = model.folded_conv_state()
    quantization = json.loads((args.run / 'quantization.json').read_text(encoding='utf-8'))
    weight_only = {}
    for name, (weight, bias) in folded.items():
        scale = np.array(quantization[name]['weight_scale'])[:, None, None, None]
        weight_only[name] = (torch.from_numpy((integer.parameters[name]['weights'] * scale).astype(np.float32)), bias)
    cases, oracle_layers = [], []
    with torch.inference_mode():
        for index in range(4):
            image, _, key = dataset[index]
            data = centered(image)
            _, _, values = integer.forward(data, capture=True)
            reference = float_forward(integer.graph, folded, data.astype(np.float32))
            weight_quantized = float_forward(integer.graph, weight_only, data.astype(np.float32))
            layers = {}
            for node in integer.graph['nodes']:
                if node['op'] != 'conv':
                    continue
                name = node['name']
                layers[name] = error(reference[name], values[name].astype(np.float64) * integer.scales[name])
                layers[name]['weight_only'] = error(reference[name], weight_quantized[name])
                if index != 0:
                    continue
                p = integer.parameters[name]
                bound = np.abs(p['bias'].astype(np.int64)) + 128 * np.abs(p['weights'].astype(np.int64)).sum((1, 2, 3))
                # Products, partial sums and bias are exact integers below 2**32;
                # binary64 represents all exactly (<2**53). Not the inference path.
                if np.any(bound >= 2**32):
                    raise ValueError('independent FP64 exactness proof bound failed')
                source = torch.from_numpy(values[node['inputs'][0]].astype(np.float64).transpose(2, 0, 1)).unsqueeze(0)
                oracle = F.conv2d(source, torch.from_numpy(p['weights'].astype(np.float64)),
                                  torch.from_numpy(p['bias'].astype(np.float64)), stride=node['stride'],
                                  padding=node['padding'], groups=node['groups'])
                np.testing.assert_array_equal(oracle[0].permute(1, 2, 0).numpy(), values[name + ':acc'])
                oracle_layers.append({'name': name, 'values': values[name + ':acc'].size,
                                      'absolute_bound': int(bound.max()), 'bit_exact': True})
            cases.append({'train_index': index, 'key': key, 'layers': layers,
                          'heads': {name: {'integer': error(reference[name], values[name].astype(np.float64) / 256),
                                           'weights_only': error(reference[name], weight_quantized[name])}
                                    for name in integer.graph['outputs']}})
            print(f'train-only quantization diagnosis {index + 1}/4', flush=True)
    save(args.run / 'layer_diagnosis.json', {'scope': 'first four training frames; no validation tuning',
         'package_sha256': manifest['payload_sha256'], 'oracle': 'independent torch FP64 integer conv; all absolute bounds <2^32',
         'oracle_layers': oracle_layers, 'oracle_accumulators_bit_exact': len(oracle_layers) == 67,
         'cases': cases, 'seconds': time.perf_counter() - started,
         'limitation': 'weights_only ablation holds FP32 bias/activations; not a deployment model; no QAT or RTL evidence'})


if __name__ == '__main__':
    main()
