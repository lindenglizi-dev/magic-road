"""One bounded, audited replay experiment; reuse trainer, watchdog and evaluator."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
from types import SimpleNamespace

import torch

from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.model import RoadYOLOS4
from cnn.replay_sampling import ReplayWindow
from cnn.train import build_parser, load_dataset_snapshot, make_frame_dataset, protocol_for, protocol_hash
from cnn.run_post_review_s import run_protected, run_validate_only
from cnn.reports.ac_g10_20261013_v1.run_g10 import E7, E7_SHA, GPU
from cnn.reports.ac_bnfreeze_g10_20261013_v1.evaluate_trial import compare, OLD_BASELINE, OLD_DATASET
from cnn.reports.ac_bnfreeze_g10_20261013_v1.early_checkpoints.evaluate_early import gates
from cnn.metrics import report

OUT = Path(__file__).resolve().parent
PARENT = OUT.parent
BASE = ROOT/'cnn/reports/ac_g10_20261013_v1'
BN = ROOT/'cnn/reports/ac_bnfreeze_g10_20261013_v1'
RUN = ROOT/'cnn/runs/ac_replay_g10_20261013_v1'
POOL = PARENT/'replay/replay64_manifest.json'
RECEIPT = PARENT/'replay/selection_receipt.json'
DATA = OUT/'dataset.json'
TESTS = ('test_replay_sampling', 'test_frozen_bn', 'test_training',
         'test_finetune_schedule', 'test_segment_resume')


def prepare():
    assert not DATA.exists() and not RUN.exists()
    pool, receipt = read_json(POOL), read_json(RECEIPT)
    assert receipt['status'] == 'fixed_replay_pool_ready' and receipt['selected_size'] == 64
    assert receipt['outputs']['manifest_sha256'] == sha256_file(POOL)
    checks = receipt['checks']
    assert any('old256' in key for key in checks), 'old256 isolation evidence required'
    for key, value in checks.items():
        if 'overlap' in key:
            assert (type(value) is int and value == 0) or value == [], key
        else:
            assert value is True, key
    base = read_json(BASE/'dataset.json')
    assert sha256_file(BASE/'dataset.json') == read_json(BN/'training_contract.json')['dataset_sha256']
    new = [dict(r, sampling_group='new') for r in base['images'] if r['split'] == 'train']
    old = [dict(r, sampling_group='replay') for r in pool['images']]
    val = [r for r in base['images'] if r['split'] == 'val']
    assert len(new) == 22 and len(old) == 64 and len(val) == 17
    assert all(r['split'] == 'train' for r in old)
    rows = new + old + val
    assert len({r['image'] for r in rows}) == len(rows)
    assert len({r['source_sha256'] for r in rows}) == len(rows)
    new_indices, old_indices = list(range(22)), list(range(22, 86))
    generator = random.Random(42)
    generator.shuffle(new_indices)
    generator.shuffle(old_indices)
    orders = []
    for step in range(10):
        orders.append([pool_indices[(step*11+j) % len(pool_indices)]
                       for j in range(11) for pool_indices in (new_indices, old_indices)])
    sampling = dict(kind='balanced_replay_11_plus_11_v1', orders=orders)
    payload = {**base, 'images': rows, 'dataset_id': 'ac_replay_g10_20261013_v1',
               'manifest_status': 'development_replay_G10', 'replay_sampling': sampling,
               'purpose': '22 reviewed AC + 64 previously signed train replay; 10 updates; not acceptance',
               'input_bindings': {str(p): sha256_file(p) for p in (POOL, RECEIPT, BASE/'dataset.json')}}
    write_json(DATA, payload)
    _, snapshot = load_dataset_snapshot(DATA)
    window = ReplayWindow(make_frame_dataset(snapshot.rows, 'train', DATA), sampling, 10)
    exposure = Counter(i for order in window.orders for i in order)
    assert sum(exposure.values()) == 220 and all(exposure[i] == 5 for i in range(22))
    assert set(exposure) == set(range(86))
    write_json(OUT/'sampling_receipt.json', dict(
        dataset_sha256=snapshot.manifest_sha256, sampling_sha256=window.sampling_sha256,
        new_pool_images=22, replay_pool_images=64, unchanged_val_images=17,
        new_presentations=110, replay_presentations=110, actual_batch=22,
        optimizer_updates=10, primary_decision_update=10,
        per_image_presentations=[dict(image=rows[i]['image'], domain=rows[i]['sampling_group'], count=exposure[i])
                                 for i in range(86)],
        exposure_boundary='same total budget as old G10, half new-image exposure; not an isolated causal test'))
    print('Prepared 22+64 pool; ten fixed windows, each 11 new + 11 replay; 17 val unchanged', flush=True)


def contract():
    manifest, snapshot = load_dataset_snapshot(DATA)
    window = ReplayWindow(make_frame_dataset(snapshot.rows, 'train', DATA), manifest['replay_sampling'], 10)
    for path, digest in manifest['input_bindings'].items():
        assert sha256_file(Path(path)) == digest, path
    old_contract = read_json(BN/'training_contract.json')
    arguments = old_contract['command'][old_contract['command'].index('--dataset'):].copy()
    arguments[arguments.index('--dataset')+1] = str(DATA)
    arguments[arguments.index('--output')+1] = str(RUN)
    options = build_parser().parse_args(arguments)
    protocol = protocol_for(options, 1, None, replay_sampling_sha256=window.sampling_sha256)
    assert protocol == dict(old_contract['protocol'], replay_sampling_sha256=window.sampling_sha256)
    assert sha256_file(E7) == E7_SHA
    sources = [Path(__file__), BASE/'run_g10.py', BN/'run.py', BN/'evaluate_trial.py',
               BN/'early_checkpoints/evaluate_early.py', *[ROOT/'cnn'/name for name in (
        'train.py', 'replay_sampling.py', 'model.py', 'loss.py', 'integer.py', 'dataset.py',
        'metrics.py', 'resume_state.py', 'run_post_review_s.py', 'training_watchdog.py',
        'benchmark_cache_gpu.py', 'evaluate.py', 'prepare_ground48.py',
        *[name+'.py' for name in TESTS])]]
    return dict(command=[sys._base_executable, '-u', '-B', '-m', 'cnn.train', *arguments],
        dataset_sha256=snapshot.manifest_sha256, dataset_content_sha256=snapshot.dataset_content_sha256,
        initializer_sha256=E7_SHA, protocol=protocol, protocol_sha256=protocol_hash(protocol),
        source_hashes={str(p): sha256_file(p) for p in sources},
        input_bindings=manifest['input_bindings'], actual_batch=22, parameter_update_cap=10,
        new_presentations=110, replay_presentations=110,
        primary_decision_update=10, development_gates=old_contract['development_gates'],
        temperature_stop_c=75, hard_seconds=1800, memory_threshold_enabled=False,
        automatic_retry=False, automatic_continuation=False, formal_acceptance=False)


def check():
    assert not RUN.exists() and not (OUT/'CPU_tests.json').exists()
    current = contract()
    temporary = OUT/'cpu_test_temp'
    temporary.mkdir(exist_ok=True)
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
               TEMP=str(temporary), TMP=str(temporary))
    results = []
    for module in TESTS:
        command = [sys.executable, '-u', '-B', '-m', 'cnn.'+module]
        done = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=180)
        results.append(dict(command=command, exit_code=done.returncode,
                            stdout=done.stdout, stderr=done.stderr))
        print(module, done.returncode, flush=True)
        if done.returncode:
            break
    passed = len(results) == len(TESTS) and all(r['exit_code'] == 0 for r in results)
    write_json(OUT/'CPU_tests.json', dict(passed=passed, checks=results, source_hashes=current['source_hashes'],
        prior_attempt='Initial direct test failed due sandbox default TEMP write denial; project-local TEMP passed'))
    assert passed
    validation = run_validate_only(current['command'])
    write_json(OUT/'CPU_preflight.json', validation)
    assert validation['exit_code'] == 0
    write_json(OUT/'training_contract.json', current)
    print('CPU tests and validate-only passed; no real-data training started', flush=True)


def completion(event, current):
    if event.get('event') == 'paused_segment':
        assert 0 <= event['trained_steps'] <= 10
        return dict(status='paused_no_retry', completed_updates=event['trained_steps'])
    assert event['event'] == 'paused_complete_epoch' and event['trained_steps'] == event['epoch_number'] == 10
    assert Path(event['checkpoint']).resolve() == RUN/'last.pt'
    reference = torch.load(E7, map_location='cpu', weights_only=False)['model']
    model = RoadYOLOS4()
    bn_keys = {f'{name}.{key}' for name, module in model.named_modules()
               if isinstance(module, torch.nn.BatchNorm2d) for key in module.state_dict()}
    assert len(bn_keys) == 305
    for step in range(1, 11):
        saved = torch.load(RUN/f'epoch_{step-1:04d}.pt', map_location='cpu', weights_only=False)
        assert saved['trained_steps'] == step and saved['last_optimizer_effective_batch'] == 22
        assert saved['training_protocol_sha256'] == current['protocol_sha256']
        assert saved['dataset_sha256'] == current['dataset_sha256']
        assert all(torch.equal(saved['model'][k], reference[k]) for k in bn_keys)
        assert all(torch.isfinite(v).all() for v in saved['model'].values())
        assert all(torch.isfinite(state['momentum_buffer']).all() for state in saved['optimizer']['state'].values())
    final = torch.load(RUN/'last.pt', map_location='cpu', weights_only=False)
    assert final['trained_steps'] == 10 and final['epoch'] == 9
    assert all(torch.equal(final['model'][k], saved['model'][k]) for k in saved['model'])
    return dict(status='completed_replay_G10', completed_updates=10,
                checkpoint_sha256=sha256_file(RUN/'last.pt'), all_saved_BN_equal_E7=True,
                all_saved_tensors_finite=True)


def execute():
    assert not RUN.exists()
    current = contract()
    assert current == read_json(OUT/'training_contract.json')
    assert read_json(OUT/'CPU_tests.json')['passed'] is True
    assert read_json(OUT/'CPU_tests.json')['source_hashes'] == current['source_hashes']
    assert read_json(OUT/'CPU_preflight.json')['exit_code'] == 0
    folder = OUT/'execution'
    folder.mkdir(exist_ok=False)
    (folder/'sources').mkdir()
    for i, (path, digest) in enumerate(current['source_hashes'].items()):
        target = folder/'sources'/f'{i}_{Path(path).name}'
        shutil.copy2(path, target)
        assert sha256_file(target) == digest
    write_json(folder/'authorization.json', dict(user_request='好的，推进吧',
        scope='Approved mixed replay plan: E7, frozen BN, LR0.0001, ten updates, no auto continuation',
        owner_pid=os.getpid(), gpu_uuid=GPU, contract=current,
        receipt_sha256=sha256_file(RECEIPT), available_disk_bytes=shutil.disk_usage(ROOT).free))
    options = SimpleNamespace(receipt=folder/'segment.json', output=RUN,
                              gpu_uuid=GPU, preflight_timeout_seconds=120)
    print('Starting one protected replay G10 segment', flush=True)
    result = run_protected(current['command'], options, expected_ready=dict(
        dataset_sha256=current['dataset_sha256'], dataset_content_sha256=current['dataset_content_sha256'],
        resume=None), completion_validator=lambda e: completion(e, current))
    result.update(E7_unchanged=sha256_file(E7) == E7_SHA,
                  sources_unchanged=all(sha256_file(Path(p)) == h for p, h in current['source_hashes'].items()),
                  formal_acceptance=False)
    write_json(folder/'report.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    assert result['status'] == 'completed_replay_G10'


def evaluate():
    current = read_json(OUT/'training_contract.json')
    assert all(sha256_file(Path(p)) == h for p, h in current['source_hashes'].items())
    execution = read_json(OUT/'execution/report.json')
    assert execution['status'] == 'completed_replay_G10' and execution['E7_unchanged'] and execution['sources_unchanged']
    assert execution['checkpoint_sha256'] == sha256_file(RUN/'last.pt')
    baselines = dict(development17=read_json(BN/'e7_control17.json'), old256=read_json(OLD_BASELINE))
    assert sha256_file(OLD_BASELINE) == '501282373e41cdc3a26a3b66f61097c95562878bab8012a0fa588eee18ec1ec8'
    assert sha256_file(BN/'e7_control17.json') == '88aec5cc0fab8211493b9537b2734f162e7c5111948abd36821501e4baedb0a7'
    evaluations, comparisons = {}, {}
    for name, dataset, count in (('development17', BASE/'dataset.json', 17), ('old256', OLD_DATASET, 256)):
        output = OUT/(name+'.json')
        command = [sys.executable, '-u', '-B', '-m', 'cnn.evaluate', '--checkpoint', str(RUN/'last.pt'),
                   '--dataset', str(dataset), '--output', str(output), '--device', 'cpu', '--threads', '2',
                   '--max-images', str(count), '--development-domain']
        with output.with_suffix('.log').open('x', encoding='utf-8') as log:
            subprocess.run(command, cwd=ROOT, env=dict(os.environ, CUDA_VISIBLE_DEVICES=''),
                           stdout=log, stderr=subprocess.STDOUT, check=True, timeout=600)
        result = evaluations[name] = read_json(output)
        assert result['checkpoint_sha256'] == execution['checkpoint_sha256']
        assert result['checkpoint_optimizer_steps'] == 10
        assert result['device'] == 'cpu' and result['image_count'] == count
        values = comparisons[name] = compare(baselines[name], result)
        for row in values.values():
            row['replay_G10'] = row.pop('frozen_BN_G10')
        print(name, json.dumps(values, ensure_ascii=False), flush=True)
    decisions = gates(comparisons['development17'], comparisons['old256'])
    cameras = {}
    rows = [r for r in read_json(BASE/'dataset.json')['images'] if r['split'] == 'val']
    for camera in sorted({r['camera_id'] for r in rows}):
        images = {r['image'] for r in rows if r['camera_id'] == camera}
        cameras[camera] = {}
        for name, result in (('E7', baselines['development17']), ('replay_G10', evaluations['development17'])):
            parts = [[r for r in result[k] if r['image_id'] in images] for k in ('predictions', 'truth', 'ignores')]
            cameras[camera][name] = report(*parts, thresholds=(.5, .5))
    summary = dict(status='completed_and_evaluated', comparisons=comparisons, gates=decisions,
                   numeric_gates_pass=all(decisions.values()), per_camera=cameras,
                   camera_review_required=True, automatic_continuation=False, formal_acceptance=False,
                   evidence_sha256={name: sha256_file(OUT/(name+'.json')) for name in evaluations})
    write_json(OUT/'comparison.json', summary)
    print(json.dumps(dict(gates=decisions, numeric_pass=all(decisions.values())), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'check', 'execute', 'evaluate'))
    globals()[parser.parse_args().action]()
