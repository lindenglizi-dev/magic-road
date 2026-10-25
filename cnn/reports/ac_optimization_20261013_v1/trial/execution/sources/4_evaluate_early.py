"""CPU-only comparison of saved updates 1/3/5; no training or promotion."""
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import torch

from cnn.metrics import report
from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.reports.ac_bnfreeze_g10_20261013_v1.evaluate_trial import (
    OUT as PARENT, BASE, RUN, E7, E7_SHA, OLD_BASELINE, OLD_DATASET, compare)
from cnn.reports.ac_bnfreeze_g10_20261013_v1.run import verify_checkpoint

OUT = Path(__file__).resolve().parent
STEPS = (1, 3, 5)


def gates(main, old):
    return dict(person_AP50_gain_at_least_1pp=main['person']['delta_pp']['ap50'] >= 1,
                person_recall_nondecreasing=main['person']['delta_pp']['recall'] >= 0,
                vehicle_AP50_drop_at_most_1pp=main['vehicle']['delta_pp']['ap50'] >= -1,
                old256_AP50_drop_at_most_1pp_each=all(
                    old[c]['delta_pp']['ap50'] >= -1 for c in ('person', 'vehicle')))


def self_check():
    main = dict(person=dict(delta_pp=dict(ap50=1, recall=0)),
                vehicle=dict(delta_pp=dict(ap50=-1)))
    old = {c: dict(delta_pp=dict(ap50=-1)) for c in ('person', 'vehicle')}
    assert all(gates(main, old).values())
    old['person']['delta_pp']['ap50'] = -1.0001
    assert not gates(main, old)['old256_AP50_drop_at_most_1pp_each']
    main['person']['delta_pp']['recall'] = -.0001
    assert not gates(main, old)['person_recall_nondecreasing']


def main():
    self_check()
    contract = read_json(PARENT/'training_contract.json')
    pins = dict(contract['source_hashes'])
    for name in ('evaluate.py', 'prepare_ground48.py', 'import_verified_review.py'):
        path = ROOT/'cnn'/name
        pins[str(path)] = sha256_file(path)
    baseline_paths = dict(development17=PARENT/'e7_control17.json', old256=OLD_BASELINE)
    expected = dict(development17='88aec5cc0fab8211493b9537b2734f162e7c5111948abd36821501e4baedb0a7',
                    old256='501282373e41cdc3a26a3b66f61097c95562878bab8012a0fa588eee18ec1ec8')
    baselines = {name: read_json(path) for name, path in baseline_paths.items()}
    for name, path in baseline_paths.items():
        assert sha256_file(path) == expected[name]
        pins[str(path)] = expected[name]
        assert baselines[name]['checkpoint_sha256'] == E7_SHA
    for dataset, expected_sha in ((BASE/'dataset.json', contract['dataset_sha256']),
                                  (OLD_DATASET, baselines['old256']['dataset_sha256'])):
        pins[str(dataset)] = expected_sha
    pins[str(E7)] = E7_SHA
    pins[str(Path(__file__))] = sha256_file(Path(__file__))
    for path, expected_sha in pins.items():
        assert sha256_file(Path(path)) == expected_sha, path
    frozen = verify_checkpoint(contract)
    checkpoints = {}
    for step in STEPS:
        path = RUN/f'epoch_{step-1:04d}.pt'
        saved = torch.load(path, map_location='cpu', weights_only=False)
        assert saved['trained_steps'] == step and saved['epoch'] == step-1
        checkpoints[str(step)] = dict(path=str(path), sha256=sha256_file(path))
        pins[str(path)] = checkpoints[str(step)]['sha256']
    jobs = []
    for step in STEPS:
        for name, dataset, count, threads in (
                ('development17', BASE/'dataset.json', 17, 4), ('old256', OLD_DATASET, 256, 2)):
            output = OUT/f'update_{step}_{name}.json'
            assert not output.exists()
            command = [sys.executable, '-u', '-B', '-m', 'cnn.evaluate', '--checkpoint',
                       checkpoints[str(step)]['path'], '--dataset', str(dataset), '--output',
                       str(output), '--device', 'cpu', '--threads', str(threads),
                       '--max-images', str(count), '--development-domain']
            jobs.append((step, name, output, count, command))
    write_json(OUT/'evaluation_contract.json', dict(
        scope='CPU evaluation of existing checkpoints only', updates=STEPS, inputs_sha256=pins,
        checkpoints=checkpoints, frozen_BN_verification=frozen, commands=[j[-1] for j in jobs],
        development_gates=contract['development_gates'], fixed_PR_threshold=.5, match_iou=.5,
        gate_self_check_passed=True, python=sys.version, python_executable_sha256=sha256_file(Path(sys.executable)),
        packages={p: importlib.metadata.version(p) for p in ('torch', 'numpy', 'Pillow', 'opencv-python')},
        automatic_training=False, automatic_promotion=False, formal_acceptance=False))
    results = {str(step): {} for step in STEPS}
    receipts = []
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1')
    for step, name, output, count, command in jobs:
        print(f'CPU evaluation update {step}: {name}', flush=True)
        started = time.perf_counter()
        log_path = output.with_suffix('.log')
        try:
            with log_path.open('x', encoding='utf-8') as stream:
                subprocess.run(command, cwd=ROOT, env=env, stdout=stream,
                               stderr=subprocess.STDOUT, check=True, timeout=600)
            result = read_json(output)
            assert result['device'] == 'cpu' and result['image_count'] == count
            assert result['checkpoint_optimizer_steps'] == step
            assert result['checkpoint_sha256'] == checkpoints[str(step)]['sha256']
            values = compare(baselines[name], result)
            for value in values.values():
                value['candidate'] = value.pop('frozen_BN_G10')
            results[str(step)][name] = values
            receipts.append(dict(step=step, dataset=name, seconds=time.perf_counter()-started,
                                 report_sha256=sha256_file(output), log_sha256=sha256_file(log_path)))
            print(json.dumps(dict(step=step, dataset=name, metrics=values), ensure_ascii=False), flush=True)
        except Exception as error:
            write_json(OUT/'failure.json', dict(step=step, dataset=name, error=repr(error),
                       completed=receipts, automatic_retry=False))
            raise
    rows = [r for r in read_json(BASE/'dataset.json')['images'] if r['split'] == 'val']
    cameras = {}
    main_reports = {'E7': baselines['development17'],
                    **{f'update_{s}': read_json(OUT/f'update_{s}_development17.json') for s in STEPS}}
    for camera in sorted({r['camera_id'] for r in rows}):
        images = {r['image'] for r in rows if r['camera_id'] == camera}
        cameras[camera] = dict(image_count=len(images), metrics={})
        for name, result in main_reports.items():
            parts = [[r for r in result[k] if r['image_id'] in images]
                     for k in ('predictions', 'truth', 'ignores')]
            cameras[camera]['metrics'][name] = report(*parts, thresholds=(.5, .5))
    passing = []
    for step, values in results.items():
        values['gates'] = gates(values['development17'], values['old256'])
        values['numeric_gates_pass'] = all(values['gates'].values())
        if values['numeric_gates_pass']:
            passing.append(int(step))
    for path, expected_sha in pins.items():
        assert sha256_file(Path(path)) == expected_sha, ('changed during evaluation', path)
    summary = dict(status='completed_cpu_evaluation', results=results, per_camera=cameras,
                   passing_numeric_updates=passing, per_camera_review_required=True,
                   receipts=receipts, inputs_unchanged=True, training_started=False,
                   baseline_replaced=False, formal_acceptance=False,
                   limitations='17 correlated development frames and fixed old256 subset; '
                   'FP32 CNN + fixed-point postprocess; no formal test/QAT/board run')
    write_json(OUT/'comparison.json', summary)
    print(json.dumps(dict(passing_numeric_updates=passing, results=results), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
