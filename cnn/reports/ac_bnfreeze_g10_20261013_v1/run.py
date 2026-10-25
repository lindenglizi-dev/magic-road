"""One user-approved E7 -> frozen-BN G10 trial, with the existing owned watchdog."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

import torch

from cnn.model import RoadYOLOS4
from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.reports.ac_g10_20261013_v1.run_g10 import E7, E7_SHA, GPU, inspect as original_inspect
from cnn.run_post_review_s import run_protected, run_validate_only
from cnn.train import build_parser, protocol_for, protocol_hash

OUT = Path(__file__).resolve().parent
BASE = OUT.parent/'ac_g10_20261013_v1'
RUN = ROOT/'cnn/runs/ac_bnfreeze_g10_20261013_v1'
OLD_G10 = ROOT/'cnn/runs/ac_g10_20261013_v1/last.pt'
OLD_G10_SHA = '978c330f74095a8b18c060bc75901f19f3c60c126103447eb9f2cad32f12fc5d'


def inspect():
    contract = original_inspect()
    original = read_json(BASE/'training_contract_v3.json')
    for key in ('dataset_sha256', 'dataset_content_sha256', 'initializer_sha256',
                'baseline_sha256', 'protocol', 'protocol_sha256'):
        assert contract[key] == original[key], key
    assert sha256_file(OLD_G10) == OLD_G10_SHA
    command = contract['command']
    command[command.index('--output')+1] = str(RUN)
    command[command.index('--lr')+1] = '0.0001'
    command.append('--freeze-bn')
    options = build_parser().parse_args(command[command.index('--dataset'):])
    protocol = protocol_for(options, 1, None)
    assert protocol['batch_norm_policy'] == 'frozen_running_stats_and_affine_v1'
    assert protocol['base_lr'] == .0001 and protocol['epochs'] == 10
    for path in (Path(__file__), OUT/'evaluate_trial.py', *[ROOT/'cnn'/name for name in
                 ('test_frozen_bn.py', 'test_training.py', 'test_finetune_schedule.py', 'test_segment_resume.py')]):
        contract['source_hashes'][str(path)] = sha256_file(path)
    contract.update(protocol=protocol, protocol_sha256=protocol_hash(protocol),
        original_G10_sha256=OLD_G10_SHA, user_request='好，下一步',
        approved_scope='E7 new optimizer, freeze BN stats and affine, LR0.0001, at most10 updates',
        evaluation='same17 development plus old256 regression; no threshold/data changes',
        development_gates=dict(person_ap50_gain_pp=1, person_recall_drop_pp=0,
                               vehicle_ap50_max_drop_pp=1, old256_each_ap50_max_drop_pp=1,
                               per_camera_review_required=True),
        deployment_authorized=False)
    return contract


def verify_checkpoint(contract):
    reference = torch.load(E7, map_location='cpu', weights_only=False)['model']
    model = RoadYOLOS4()
    bn_keys = {f'{name}.{key}' for name, module in model.named_modules()
               if isinstance(module, torch.nn.BatchNorm2d) for key in module.state_dict()}
    assert len(bn_keys) == 61*5
    paths = [RUN/f'epoch_{i:04d}.pt' for i in range(10)] + [RUN/'last.pt', RUN/'last_resume.pt']
    for index, path in enumerate(paths):
        saved = torch.load(path, map_location='cpu', weights_only=False)
        assert saved['training_protocol'] == contract['protocol']
        assert saved['training_protocol_sha256'] == contract['protocol_sha256']
        assert saved['dataset_sha256'] == contract['dataset_sha256']
        assert saved['trained_steps'] == min(index+1, 10)
        assert saved['last_optimizer_effective_batch'] == 22
        assert saved['architecture_hash'] == model.architecture_hash()
        for key in bn_keys:
            assert torch.equal(saved['model'][key], reference[key]), (path.name, key)
        assert all(torch.isfinite(value).all() for value in saved['model'].values())
        assert len(saved['optimizer']['param_groups']) == 1
        assert len(saved['optimizer']['param_groups'][0]['params']) == 73
        assert all(torch.isfinite(state['momentum_buffer']).all()
                   for state in saved['optimizer']['state'].values())
    return dict(BN_modules=61, frozen_BN_tensors=len(bn_keys), checked_checkpoints=len(paths),
                all_BN_equal_E7=True, all_model_and_optimizer_tensors_finite=True,
                optimizer_parameter_tensors=73)


def completion(event, contract):
    if event.get('event') == 'paused_segment':
        assert 0 <= event['trained_steps'] <= 10
        return dict(status='paused_no_auto_resume', completed_updates=event['trained_steps'],
                    checkpoint=event.get('checkpoint'))
    assert event.get('event') == 'paused_complete_epoch', event
    assert event['epoch_number'] == event['trained_steps'] == 10
    assert Path(event['checkpoint']).resolve() == RUN/'last.pt'
    frozen = verify_checkpoint(contract)
    return dict(status='completed_frozen_BN_G10', completed_updates=10, completed_epochs=10,
                checkpoint=str(RUN/'last.pt'), checkpoint_sha256=sha256_file(RUN/'last.pt'),
                frozen_BN_verification=frozen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'prepare', 'execute'])
    action = parser.parse_args().action
    contract = inspect()
    assert not RUN.exists(), 'Never restart or overwrite an existing run'
    if action == 'check':
        assert not (OUT/'CPU_tests.json').exists()
        checks = []
        temporary = OUT/'cpu_test_temp'
        temporary.mkdir(exist_ok=True)
        env = dict(os.environ, CUDA_VISIBLE_DEVICES='', TEMP=str(temporary), TMP=str(temporary))
        for module in ('test_frozen_bn', 'test_training', 'test_finetune_schedule', 'test_segment_resume'):
            command = [sys.executable, '-B', '-m', 'cnn.'+module]
            completed = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                text=True, encoding='utf-8', errors='replace', timeout=120)
            checks.append(dict(command=command, exit_code=completed.returncode,
                               stdout_tail=completed.stdout[-4000:], stderr_tail=completed.stderr[-1000:]))
            print(module, completed.returncode, flush=True)
            if completed.returncode:
                break
        passed = len(checks)==4 and all(row['exit_code']==0 for row in checks)
        write_json(OUT/'CPU_tests.json', dict(status='passed' if passed else 'failed', checks=checks,
                   source_hashes=contract['source_hashes'], real_data_training=False))
        if not passed:
            raise SystemExit(1)
        return
    if action == 'prepare':
        validation = run_validate_only(contract['command'])
        write_json(OUT/'CPU_preflight.json', validation)
        assert validation['exit_code'] == 0, validation
        write_json(OUT/'training_contract.json', contract)
        print('PASS CPU preflight; frozen BN, LR0.0001, cap10; no GPU work started', flush=True)
        return
    assert read_json(OUT/'training_contract.json') == contract
    assert read_json(OUT/'CPU_preflight.json')['exit_code'] == 0
    tests = read_json(OUT/'CPU_tests.json')
    assert tests['status'] == 'passed' and tests['source_hashes'] == contract['source_hashes']
    exposure = read_json(BASE/'historical_exposure.json')
    assert exposure['final_dataset']['sha256'] == contract['dataset_sha256']
    assert exposure['checks']['raw_source_sha256_intersection']['union_matches'] == 0
    assert exposure['checks']['declared_source_text']['passed'] is True
    execution = OUT/'execution'
    execution.mkdir(exist_ok=False)
    source_dir = execution/'sources'
    source_dir.mkdir()
    for ordinal, (path, digest) in enumerate(contract['source_hashes'].items()):
        target = source_dir/(str(ordinal)+'_'+Path(path).name)
        shutil.copy2(path, target)
        assert sha256_file(target) == digest
    write_json(execution/'authorization.json', dict(user_request='好，下一步', owner_pid=os.getpid(),
        gpu_uuid=GPU, contract=contract, CPU_tests_sha256=sha256_file(OUT/'CPU_tests.json'),
        available_disk_bytes=shutil.disk_usage(ROOT).free,
        historical_exposure_sha256=sha256_file(BASE/'historical_exposure.json')))
    print(json.dumps(dict(event='frozen_BN_G10_started', owner_pid=os.getpid(), cap=10)), flush=True)
    options = SimpleNamespace(receipt=execution/'segment.json', output=RUN, gpu_uuid=GPU,
                              preflight_timeout_seconds=120)
    result = run_protected(contract['command'], options, expected_ready=dict(
        dataset_sha256=contract['dataset_sha256'],
        dataset_content_sha256=contract['dataset_content_sha256'], resume=None),
        completion_validator=lambda event: completion(event, contract))
    result.update(frozen_E7_unchanged=sha256_file(E7)==E7_SHA,
        original_G10_unchanged=sha256_file(OLD_G10)==OLD_G10_SHA,
        source_unchanged=all(sha256_file(Path(p))==h for p,h in contract['source_hashes'].items()),
        formal_acceptance=False)
    write_json(execution/'report.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    if result['status'] != 'completed_frozen_BN_G10':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
