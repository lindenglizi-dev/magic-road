"""One bounded G10 experiment using the existing trainer and owned watchdog."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace

import torch

from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.reports.ac_replacement_review_20261013_v1.export_approved import check as check_labels
from cnn.run_post_review_s import run_protected, run_validate_only
from cnn.train import build_parser, load_dataset_snapshot, protocol_for, protocol_hash
from cnn import training_watchdog

OUT = Path(__file__).resolve().parent
RUN = ROOT/'cnn/runs/ac_g10_20261013_v1'
E7 = ROOT/'cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5/cnn/runs/person_native_recovery_20261004/epoch_0006.pt'
E7_SHA = '17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42'
GPU = 'GPU-a85887e6-358e-1ebb-cf09-81b558fa321a'


def inspect():
    check_labels()
    assert sha256_file(E7) == E7_SHA
    _, snapshot = load_dataset_snapshot(OUT/'dataset.json')
    assert sum(s['split']=='train' for s in snapshot.rows) == 22
    assert sum(s['split']=='val' for s in snapshot.rows) == 17
    assert (training_watchdog.STOP_C,training_watchdog.SOFT_SECONDS,
            training_watchdog.HARD_SECONDS,training_watchdog.STALE_PAUSE_SECONDS,
            training_watchdog.STALE_KILL_SECONDS) == (75,1560,1800,20,30)
    baseline = read_json(OUT/'e7_baseline.json')
    assert baseline['checkpoint_sha256'] == E7_SHA
    assert baseline['dataset_sha256'] == snapshot.manifest_sha256 and baseline['image_count'] == 17
    arguments = ['--dataset',str(OUT/'dataset.json'),'--output',str(RUN),
        '--phase','supervised','--epochs','10','--stop-after-epoch','10',
        '--batch-size','8','--accum-steps','8','--lr','0.001',
        '--lr-schedule','finetune_constant','--momentum','0.9','--weight-decay','0.0005',
        '--clip-grad','10','--seed','42','--workers','0','--device','cuda','--amp',
        '--no-mosaic','--checkpoint-kind','training','--checkpoint-every-steps','1',
        '--checkpoint-every-seconds','120','--init-checkpoint',str(E7)]
    options = build_parser().parse_args(arguments)
    updates_per_epoch = math.ceil(math.ceil(22/options.batch_size)/options.accum_steps)
    assert updates_per_epoch == 1 and updates_per_epoch*options.epochs == 10
    protocol = protocol_for(options,updates_per_epoch,None)
    sources = [Path(__file__), *[ROOT/'cnn'/name for name in (
        'train.py','model.py','loss.py','integer.py','dataset.py','metrics.py',
        'resume_state.py','run_post_review_s.py','training_watchdog.py','benchmark_cache_gpu.py')]]
    return dict(command=[sys.executable,'-u','-B','-m','cnn.train',*arguments],
        dataset_sha256=snapshot.manifest_sha256, dataset_content_sha256=snapshot.dataset_content_sha256,
        initializer_sha256=E7_SHA, baseline_sha256=sha256_file(OUT/'e7_baseline.json'),
        protocol=protocol, protocol_sha256=protocol_hash(protocol),
        source_hashes={str(p):sha256_file(p) for p in sources},
        nominal_batch=64, actual_batch=22, parameter_update_cap=10,
        planned_training_image_presentations=220,
        cache='Existing raw loader; no new cache, existing 20GiB cache reserve unchanged',
        temperature_stop_c=75, hard_seconds=1800, memory_threshold_enabled=False,
        automatic_retry=False, formal_acceptance=False)


def completion(event, contract):
    if event.get('event') == 'paused_segment':
        assert 0 <= event['trained_steps'] <= 10
        return dict(status='paused_no_auto_resume',completed_updates=event['trained_steps'],
                    checkpoint=event.get('checkpoint'))
    assert event.get('event') == 'paused_complete_epoch',event
    assert event['epoch_number'] == event['trained_steps'] == 10
    assert Path(event['checkpoint']).resolve() == RUN/'last.pt'
    saved = torch.load(RUN/'last.pt',map_location='cpu',weights_only=False)
    assert saved['trained_steps'] == 10 and saved['epoch'] == 9
    assert saved['last_optimizer_effective_batch'] == 22
    assert saved['training_protocol_sha256'] == contract['protocol_sha256']
    assert saved['dataset_sha256'] == contract['dataset_sha256']
    return dict(status='completed_G10', completed_updates=10, completed_epochs=10,
                checkpoint=str(RUN/'last.pt'),checkpoint_sha256=sha256_file(RUN/'last.pt'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','execute'])
    action=parser.parse_args().action
    contract=inspect()
    assert not RUN.exists(),'Never restart or overwrite an existing run'
    if action == 'prepare':
        validation=run_validate_only(contract['command'])
        write_json(OUT/'CPU_preflight_v2.json',validation)
        assert validation['exit_code']==0,validation
        write_json(OUT/'training_contract_v2.json',contract)
        print('PASS CPU trainer preflight; G10 cap10; no GPU work started',flush=True)
        return
    assert read_json(OUT/'training_contract_v2.json') == contract
    assert read_json(OUT/'CPU_preflight_v2.json')['exit_code']==0
    exposure=read_json(OUT/'historical_exposure.json')
    assert exposure['final_dataset']['sha256']==contract['dataset_sha256']
    assert exposure['checks']['raw_source_sha256_intersection']['union_matches']==0
    assert exposure['checks']['declared_source_text']['passed'] is True
    execution=OUT/'execution'
    execution.mkdir(exist_ok=False)
    source_dir=execution/'sources'; source_dir.mkdir()
    for ordinal,(path,digest) in enumerate(contract['source_hashes'].items()):
        target=source_dir/(str(ordinal)+'_'+Path(path).name)
        shutil.copy2(path,target)
        assert sha256_file(target)==digest
    write_json(execution/'authorization.json',dict(user_request='直接将所有标为正确自己导出json进行下一步',
        approved_plan='24 review images then frozen E7 baseline and G10 only',
        owner_pid=os.getpid(),gpu_uuid=GPU,contract=contract,
        historical_exposure_sha256=sha256_file(OUT/'historical_exposure.json')))
    print(json.dumps(dict(event='G10_controller_started',owner_pid=os.getpid(),cap=10)),flush=True)
    options=SimpleNamespace(receipt=execution/'segment.json',output=RUN,gpu_uuid=GPU,
                            preflight_timeout_seconds=120)
    result=run_protected(contract['command'],options,expected_ready=dict(
        dataset_sha256=contract['dataset_sha256'],
        dataset_content_sha256=contract['dataset_content_sha256'],resume=None),
        completion_validator=lambda event:completion(event,contract))
    result['frozen_E7_unchanged']=sha256_file(E7)==E7_SHA
    result['source_unchanged']=all(sha256_file(Path(p))==h for p,h in contract['source_hashes'].items())
    result['formal_acceptance']=False
    write_json(execution/'report.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)
    if result['status']!='completed_G10':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
