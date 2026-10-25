"""One ten-update distillation comparison, reusing the owned watchdog and evaluator."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

import torch

from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.replay_sampling import ReplayWindow
from cnn.train import build_parser, load_dataset_snapshot, make_frame_dataset, protocol_for, protocol_hash
from cnn.run_post_review_s import run_protected, run_validate_only, worker_environment
from cnn.reports.ac_g10_20261013_v1.run_g10 import E7, E7_SHA, GPU
from cnn.reports.ac_optimization_20261013_v1.trial.run import completion as verify_saved_updates
from cnn.reports.ac_bnfreeze_g10_20261013_v1.evaluate_trial import compare, OLD_DATASET
from cnn.metrics import report

OUT = Path(__file__).resolve().parent
CONTROL = ROOT/'cnn/reports/ac_optimization_20261013_v1/trial'
DATA = CONTROL/'dataset.json'
CACHE = ROOT/'cnn/reports/completion_route_20261013_v1/teacher/teacher_train86.pt'
RUN = ROOT/'cnn/runs/ac_distill_g10_20261013_v1'
DATA_SHA = '5b25180c25d1f3835ea5248b107f19d2fc39cfac166500c45c87c2dfde08fd59'
CACHE_SHA = '37c2edfcf416167c3c230a079aa7c4ff33e067fe0a37bcff15ee4ea318595927'
TESTS = ('test_distill_replay', 'test_replay_sampling', 'test_distillation_safety',
         'test_finetune_schedule', 'test_frozen_bn')


def contract():
    previous = read_json(CONTROL/'training_contract.json')
    assert sha256_file(DATA) == DATA_SHA and sha256_file(CACHE) == CACHE_SHA
    assert sha256_file(E7) == E7_SHA
    manifest, snapshot = load_dataset_snapshot(DATA)
    window = ReplayWindow(make_frame_dataset(snapshot.rows, 'train', DATA), manifest['replay_sampling'], 10)
    arguments = previous['command'][previous['command'].index('--dataset'):].copy()
    arguments[arguments.index('--output')+1] = str(RUN)
    arguments[arguments.index('--phase')+1] = 'distill'
    arguments += ['--teacher-cache', str(CACHE), '--distill-weight', '1.0']
    options = build_parser().parse_args(arguments)
    protocol = protocol_for(options, 1, CACHE_SHA, replay_sampling_sha256=window.sampling_sha256)
    expected = dict(previous['protocol'], phase='distill', teacher_cache_sha256=CACHE_SHA)
    from cnn.loss import DISTILL_CONTRACT
    expected['distillation_contract'] = DISTILL_CONTRACT
    assert protocol == expected
    # All numerical helpers remain byte-identical to the completed supervision control.
    for name in ('model.py', 'loss.py', 'integer.py', 'dataset.py', 'metrics.py', 'evaluate.py'):
        path = ROOT/'cnn'/name
        assert sha256_file(path) == previous['source_hashes'][str(path)], name
    paths = [Path(__file__), *[ROOT/'cnn'/name for name in (
        'train.py', 'model.py', 'loss.py', 'integer.py', 'dataset.py', 'metrics.py',
        'teacher.py', 'evaluate.py', 'resume_state.py', 'replay_sampling.py', 'prepare_ground48.py',
        'run_post_review_s.py', 'training_watchdog.py', 'benchmark_cache_gpu.py',
        *[test+'.py' for test in TESTS])], CONTROL/'run.py',
        ROOT/'cnn/reports/ac_g10_20261013_v1/run_g10.py',
        ROOT/'cnn/reports/ac_bnfreeze_g10_20261013_v1/evaluate_trial.py']
    return dict(command=[sys._base_executable, '-u', '-B', '-m', 'cnn.train', *arguments],
        dataset_sha256=snapshot.manifest_sha256, dataset_content_sha256=snapshot.dataset_content_sha256,
        initializer_sha256=E7_SHA, teacher_cache_sha256=CACHE_SHA,
        protocol=protocol, protocol_sha256=protocol_hash(protocol),
        source_hashes={str(path): sha256_file(path) for path in paths},
        actual_batch=22, parameter_update_cap=10, new_presentations=110, replay_presentations=110,
        control_checkpoint_sha256='e7e6a0f514b39417451ff90cec32e7f5adc862136bdf3adeac988c4d454fa262',
        temperature_stop_c=75, hard_seconds=1800, memory_threshold_enabled=False,
        automatic_retry=False, automatic_continuation=False, formal_acceptance=False)


def check():
    assert not RUN.exists() and not (OUT/'training_contract.json').exists()
    current = contract()
    temporary = OUT/'cpu_temp'
    temporary.mkdir(exist_ok=True)
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
               TEMP=str(temporary), TMP=str(temporary))
    checks = []
    for test in TESTS:
        command = [sys.executable, '-u', '-B', '-m', 'cnn.'+test]
        done = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                              text=True, encoding='utf-8', errors='replace', timeout=180)
        checks.append(dict(command=command, exit_code=done.returncode,
                           stdout=done.stdout, stderr=done.stderr))
        print(test, done.returncode, flush=True)
        if done.returncode:
            break
    passed = len(checks) == len(TESTS) and all(item['exit_code'] == 0 for item in checks)
    write_json(OUT/'CPU_tests.json', dict(passed=passed, checks=checks, source_hashes=current['source_hashes']))
    assert passed
    probe = subprocess.Popen([current['command'][0], '-B', '-c',
        'import os, torch, json; print(json.dumps(dict(pid=os.getpid(), torch=torch.__version__)))'],
        cwd=ROOT, env=worker_environment(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    stdout, stderr = probe.communicate(timeout=30)
    assert probe.returncode == 0 and json.loads(stdout)['pid'] == probe.pid
    write_json(OUT/'launcher_PID_check.json', dict(passed=True, popen_pid=probe.pid,
        child=json.loads(stdout), stderr=stderr, command_python=current['command'][0]))
    validation = run_validate_only(current['command'])
    write_json(OUT/'CPU_preflight.json', validation)
    assert validation['exit_code'] == 0
    write_json(OUT/'training_contract.json', current)


def completion(event, current):
    # Reuse the existing checks for all ten saved checkpoints, frozen BN and finite momentum.
    from cnn.reports.ac_optimization_20261013_v1.trial import run as replay
    previous_run = replay.RUN
    try:
        replay.RUN = RUN
        result = verify_saved_updates(event, current)
    finally:
        replay.RUN = previous_run
    if result['status'] == 'completed_replay_G10':
        result['status'] = 'completed_distill_G10'
    return result


def execute():
    assert not RUN.exists()
    current = contract()
    assert current == read_json(OUT/'training_contract.json')
    assert read_json(OUT/'CPU_tests.json')['passed']
    assert read_json(OUT/'CPU_tests.json')['source_hashes'] == current['source_hashes']
    assert read_json(OUT/'CPU_preflight.json')['exit_code'] == 0
    folder = OUT/'execution_attempt2'
    folder.mkdir(exist_ok=False)
    (folder/'sources').mkdir()
    for index, (path, digest) in enumerate(current['source_hashes'].items()):
        target = folder/'sources'/f'{index}_{Path(path).name}'
        shutil.copy2(path, target)
        assert sha256_file(target) == digest
    write_json(folder/'authorization.json', dict(
        user_request='好的，进行下一步，是蒸馏是吗', owner_pid=os.getpid(),
        scope='One independent E7 distillation comparison, ten updates, unchanged replay order and supervision',
        gpu_uuid=GPU, contract=current, available_disk_bytes=shutil.disk_usage(ROOT).free))
    options = SimpleNamespace(receipt=folder/'segment.json', output=RUN,
                              gpu_uuid=GPU, preflight_timeout_seconds=120)
    print('Starting protected distillation: ten updates', flush=True)
    result = run_protected(current['command'], options, expected_ready=dict(
        dataset_sha256=current['dataset_sha256'], dataset_content_sha256=current['dataset_content_sha256'],
        resume=None), completion_validator=lambda event: completion(event, current))
    result.update(E7_unchanged=sha256_file(E7) == E7_SHA,
        sources_unchanged=all(sha256_file(Path(path)) == digest for path, digest in current['source_hashes'].items()),
        teacher_cache_unchanged=sha256_file(CACHE) == CACHE_SHA, formal_acceptance=False)
    write_json(folder/'report.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    assert (result['status'] == 'completed_distill_G10' and result['E7_unchanged']
            and result['sources_unchanged'] and result['teacher_cache_unchanged'])


def evaluate():
    current = read_json(OUT/'training_contract.json')
    execution = read_json(OUT/'execution_attempt2/report.json')
    assert (execution['status'] == 'completed_distill_G10' and execution['E7_unchanged']
            and execution['sources_unchanged'] and execution['teacher_cache_unchanged'])
    assert all(sha256_file(Path(path)) == digest for path, digest in current['source_hashes'].items())
    assert sha256_file(CACHE) == current['teacher_cache_sha256'] and sha256_file(E7) == E7_SHA
    assert execution['checkpoint_sha256'] == sha256_file(RUN/'last.pt')
    comparisons, evaluations = {}, {}
    for name, dataset, count in (
            ('development17', ROOT/'cnn/reports/ac_g10_20261013_v1/dataset.json', 17),
            ('old256', OLD_DATASET, 256)):
        output = OUT/(name+'.json')
        assert not output.exists()
        command = [sys.executable, '-u', '-B', '-m', 'cnn.evaluate', '--checkpoint', str(RUN/'last.pt'),
                   '--dataset', str(dataset), '--output', str(output), '--device', 'cpu', '--threads', '2',
                   '--max-images', str(count), '--development-domain']
        with output.with_suffix('.log').open('x', encoding='utf-8') as log:
            subprocess.run(command, cwd=ROOT, env=dict(os.environ, CUDA_VISIBLE_DEVICES=''),
                           stdout=log, stderr=subprocess.STDOUT, check=True, timeout=600)
        candidate, control = read_json(output), read_json(CONTROL/(name+'.json'))
        assert candidate['checkpoint_sha256'] == execution['checkpoint_sha256']
        assert candidate['checkpoint_optimizer_steps'] == 10
        assert control['checkpoint_sha256'] == current['control_checkpoint_sha256']
        values = compare(control, candidate)
        for row in values.values():
            row['supervised_replay_G10'] = row.pop('E7')
            row['distill_G10'] = row.pop('frozen_BN_G10')
        comparisons[name], evaluations[name] = values, candidate
        print(name, json.dumps(values, ensure_ascii=False), flush=True)
    dev, old = comparisons['development17'], comparisons['old256']
    gates = dict(person_AP50_gain_at_least_1pp=dev['person']['delta_pp']['ap50'] >= 1,
        person_recall_nondecreasing=dev['person']['delta_pp']['recall'] >= 0,
        vehicle_AP50_drop_at_most_1pp=dev['vehicle']['delta_pp']['ap50'] >= -1,
        old256_AP50_drop_at_most_1pp_each=all(old[label]['delta_pp']['ap50'] >= -1
                                             for label in ('person', 'vehicle')))
    rows = [row for row in read_json(DATA)['images'] if row['split'] == 'val']
    cameras = {}
    for camera in sorted({row['camera_id'] for row in rows}):
        images = {row['image'] for row in rows if row['camera_id'] == camera}
        cameras[camera] = {}
        for name, result in (('supervised_replay_G10', read_json(CONTROL/'development17.json')),
                             ('distill_G10', evaluations['development17'])):
            parts = [[row for row in result[key] if row['image_id'] in images]
                     for key in ('predictions', 'truth', 'ignores')]
            cameras[camera][name] = report(*parts, thresholds=(.5, .5))
    summary = dict(status='completed_and_evaluated', comparisons=comparisons, gates=gates,
        numeric_development_gates_pass=all(gates.values()), per_camera=cameras,
        automatic_continuation=False, formal_acceptance=False,
        checkpoint_sha256=execution['checkpoint_sha256'],
        evidence_sha256={name: sha256_file(OUT/(name+'.json')) for name in evaluations})
    write_json(OUT/'comparison.json', summary)
    print(json.dumps(dict(gates=gates, numeric_pass=all(gates.values())), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'execute', 'evaluate'))
    globals()[parser.parse_args().action]()
