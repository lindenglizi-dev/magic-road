"""CPU-only 2x2 parameter/BN-buffer ablation; never trains or replaces originals."""
import json
import os
from pathlib import Path
import subprocess
import sys

import torch

from cnn.model import RoadYOLOS4
from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
E7 = ROOT/'cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5/cnn/runs/person_native_recovery_20261004/epoch_0006.pt'
G10 = ROOT/'cnn/runs/ac_g10_20261013_v1/last.pt'
EXPECTED = {
    E7: '17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42',
    G10: '978c330f74095a8b18c060bc75901f19f3c60c126103447eb9f2cad32f12fc5d',
    BASE/'dataset.json': '6af48b5ec8da6550a5d0af31db8b8f58d1fc8c9960df0eda9a66ad7c94f5f5e1',
}
FIELDS = ('precision', 'recall', 'ap50', 'ap50_95')


def main():
    torch.set_num_threads(4)
    for path, digest in EXPECTED.items():
        assert sha256_file(path) == digest, path
    cases = {'E7': E7, 'G10': G10,
             'G10_parameters_E7_BN': OUT/'G10_parameters_E7_BN.pt',
             'E7_parameters_G10_BN': OUT/'E7_parameters_G10_BN.pt'}
    targets = [OUT/'comparison.json', OUT/'contract.json',
               *[OUT/f'{name}.json' for name in cases], *list(cases.values())[2:]]
    assert not any(path.exists() for path in targets), 'Existing evidence: do not overwrite/retry'
    saved = {name: torch.load(path, map_location='cpu', weights_only=False)
             for name, path in list(cases.items())[:2]}
    model = RoadYOLOS4()
    bn = {name: module for name, module in model.named_modules()
          if isinstance(module, torch.nn.BatchNorm2d)}
    buffers = {f'{name}.{key}' for name in bn
               for key in ('running_mean', 'running_var', 'num_batches_tracked')}
    template = model.state_dict()
    assert buffers == set(dict(model.named_buffers()))
    for checkpoint in saved.values():
        assert checkpoint['architecture_hash'] == model.architecture_hash()
        assert checkpoint['model'].keys() == template.keys()
        for key, value in checkpoint['model'].items():
            assert value.shape == template[key].shape and value.dtype == template[key].dtype, key
            assert torch.isfinite(value).all(), key
        model.load_state_dict(checkpoint['model'], strict=True)
    count_deltas = {name: int(saved['G10']['model'][f'{name}.num_batches_tracked'] -
                             saved['E7']['model'][f'{name}.num_batches_tracked']) for name in bn}
    assert set(count_deltas.values()) == {30}, count_deltas
    sources = [Path(__file__), *[ROOT/'cnn'/f'{name}.py' for name in
               ('evaluate', 'model', 'train', 'dataset', 'integer', 'metrics')]]
    source_hashes = {str(path): sha256_file(path) for path in sources}
    contract = dict(device='cpu', training=False, original_hashes={str(p): h for p,h in EXPECTED.items()},
        source_hashes=source_hashes, BN_modules=len(bn), swapped_keys=sorted(buffers),
        BN_forward_count_deltas=count_deltas, BN_momentum=sorted({m.momentum for m in bn.values()}),
        BN_eps=sorted({m.eps for m in bn.values()}), affine_parameters_follow_parameter_donor=True,
        confidence_threshold=.5, match_iou=.5, development_images=17,
        formal_acceptance=False, checkpoint_export='inference-only ablations, no optimizer/resume state')
    write_json(OUT/'contract.json', contract)
    for name, parameter_donor, buffer_donor in (
            ('G10_parameters_E7_BN', 'G10', 'E7'), ('E7_parameters_G10_BN', 'E7', 'G10')):
        state = {key: saved[buffer_donor if key in buffers else parameter_donor]['model'][key].clone()
                 for key in template}
        model.load_state_dict(state, strict=True)
        for key, value in model.state_dict().items():
            assert torch.equal(value, saved[buffer_donor if key in buffers else parameter_donor]['model'][key])
        payload = dict(format='road-yolo-inference-ablation-not-training-v1', checkpoint_kind='diagnostic',
            resume_eligible=False, model=state, architecture_hash=model.architecture_hash(),
            dataset_sha256=saved[parameter_donor]['dataset_sha256'],
            dataset_content_sha256=saved[parameter_donor]['dataset_content_sha256'],
            epoch=-1, trained_steps=0, ablation=dict(parameters=parameter_donor, BN_buffers=buffer_donor,
                                                  contract_sha256=sha256_file(OUT/'contract.json')))
        with cases[name].open('xb') as stream:
            torch.save(payload, stream)
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='')
    results = {}
    for name, checkpoint in cases.items():
        command = [sys.executable, '-B', '-m', 'cnn.evaluate', '--checkpoint', str(checkpoint),
                   '--dataset', str(BASE/'dataset.json'), '--output', str(OUT/f'{name}.json'),
                   '--device', 'cpu', '--threads', '4', '--max-images', '17', '--development-domain']
        completed = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True,
                                   encoding='utf-8', errors='replace', timeout=120)
        assert completed.returncode == 0, (completed.stdout, completed.stderr)
        result = results[name] = read_json(OUT/f'{name}.json')
        assert result['device'] == 'cpu' and result['image_count'] == 17
        assert result['checkpoint_sha256'] == sha256_file(checkpoint)
        print(name, json.dumps(result['diagnostic_metrics_at_0_5']['classes']), flush=True)
    for name, previous in (('E7', 'e7_baseline.json'), ('G10', 'g10_development_matched_order.json')):
        old = read_json(BASE/previous)
        for key in ('predictions', 'truth', 'ignores', 'diagnostic_metrics_at_0_5',
                    'dataset_sha256', 'evaluated_image_content_sha256', 'postprocess_contract'):
            assert results[name][key] == old[key], (name, 'control did not reproduce', key)
    for result in results.values():
        for key in ('truth', 'ignores', 'dataset_sha256', 'evaluated_image_content_sha256', 'postprocess_contract'):
            assert result[key] == results['E7'][key], key
    metrics = {name: {label: {key: result['diagnostic_metrics_at_0_5']['classes'][label][key] for key in FIELDS}
                     for label in ('person', 'vehicle')} for name, result in results.items()}
    effects = {}
    for label in ('person', 'vehicle'):
        effects[label] = {}
        for key in FIELDS:
            a, b, c, d = [metrics[name][label][key] for name in cases]
            effects[label][key] = dict(parameters_at_E7_BN_pp=100*(c-a),
                BN_at_E7_parameters_pp=100*(d-a), interaction_pp=100*(b-c-d+a), total_pp=100*(b-a))
    for path, digest in {**{str(p): h for p,h in EXPECTED.items()}, **source_hashes}.items():
        assert sha256_file(Path(path)) == digest, path
    write_json(OUT/'comparison.json', dict(status='CPU_ablation_complete', metrics=metrics,
        factorial_effects=effects, controls_reproduced_exactly=True, original_files_unchanged=True,
        formal_acceptance=False, new_training=False, automatic_continuation=False,
        caveat='17 correlated development frames; BN/parameters interact; swaps are not a retraining trial',
        evidence_sha256={name: sha256_file(OUT/f'{name}.json') for name in cases}))
    print('PASS: controls reproduced; donor tensors exact; originals unchanged; no training.', flush=True)


if __name__ == '__main__':
    main()
