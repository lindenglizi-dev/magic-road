"""Bounded native/Mosaic experiment: two complete epochs per arm, then CPU evaluation."""
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from .run_road_epoch import (DATASET, ROAD_OUTPUT, ROAD20_SHA, ROOT, sha256,
                             worker_environment)
from .run_road_overnight import continuation, verify_evaluation

RUN = ROOT / 'cnn/reports/person_ab_20261004'
BASELINE = ROOT / 'cnn/reports/road_segmented_20261003/overnight_20261004/epoch_20_val256.json'


def main():
    if sha256(ROAD_OUTPUT / 'epoch_0019.pt') != ROAD20_SHA:
        raise ValueError('epoch20 source changed')
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    if baseline['checkpoint_sha256'] != ROAD20_SHA:
        raise ValueError('baseline differs from initial weights')
    if any((ROOT / f'cnn/runs/person_ab_20261004_{arm}').exists() for arm in ('native', 'mosaic')):
        raise FileExistsError('first A/B launch requires two fresh output directories')
    sources = {path.name: sha256(path) for path in (ROOT / 'cnn').glob('*.py')}

    def verify_sources():
        current = {path.name: sha256(path) for path in (ROOT / 'cnn').glob('*.py')}
        if current != sources:
            raise ValueError('Python sources changed during the A/B experiment')

    RUN.mkdir()  # Exclusive parent directory prevents duplicate experiment launch.
    deadline = time.time() + 6 * 3600
    state = dict(status='starting', owner_pid=os.getpid(), controller_pid=None,
                 deadline_unix=deadline, arms={}, target_epochs_per_arm=2,
                 source_checkpoint_sha256=ROAD20_SHA, baseline_sha256=sha256(BASELINE),
                 source_sha256=sources,
                 initialization='weights_only_fresh_optimizer_RNG_and_40_epoch_schedule',
                 differences=['mosaic_enabled'], order=['native', 'mosaic'],
                 limitation='Mosaic changes image/object exposure too; fixed arm order can have thermal bias',
                 formal_acceptance=False)

    def publish():
        state['updated_at'] = datetime.now().astimezone().isoformat()
        temporary = RUN / 'status.tmp'
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(RUN / 'status.json')

    child = None
    try:
        publish()
        for arm in state['order']:
            state['current_arm'] = arm
            arm_state = state['arms'][arm] = dict(status='starting', segments=[], evaluations=[])
            output = ROOT / f'cnn/runs/person_ab_20261004_{arm}'
            for iteration in range(1, 13):
                verify_sources()
                if time.time() >= deadline - 120:
                    state['status'] = 'paused_deadline'
                    break
                log = RUN / f'{arm}_segment_{iteration:02d}.log'
                errors = RUN / f'{arm}_segment_{iteration:02d}.stderr.log'
                command = [sys._base_executable, '-u', '-B', '-m', 'cnn.run_road_epoch',
                           '--person-ab-arm', arm, '--stop-after-epoch', '2',
                           '--deadline-unix', str(deadline), '--supervisor-pid', str(os.getpid())]
                with log.open('x', encoding='utf-8') as out, errors.open('x', encoding='utf-8') as err:
                    child = subprocess.Popen(command, cwd=ROOT, env=worker_environment(),
                        stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
                    state.update(status='training', controller_pid=child.pid, controller_log=str(log))
                    arm_state['status'] = 'training'
                    publish()
                    code = child.wait(timeout=max(1, deadline - time.time() + 65))
                final = json.loads(log.read_text(encoding='utf-8').splitlines()[-1])
                path = Path(final['report'])
                if path.parent.parent.resolve() != (RUN / arm).resolve():
                    raise ValueError('segment report outside its experiment arm')
                report = json.loads(path.read_text(encoding='utf-8'))
                arm_state['segments'].append(dict(report=str(path), status=report['status'],
                                                   sha256=sha256(path)))
                pause = path.parent / 'pause.json'
                reason = json.loads(pause.read_text())['reason'] if pause.exists() else None
                action = continuation(report, code, reason)
                if action == 'stop_deadline':
                    state['status'] = 'paused_deadline'
                    break
                if action == 'resume_same_epoch':
                    publish()
                    continue
                arm_state['status'] = 'trained_two_epochs'
                state.update(status='evaluating', controller_pid=None)
                publish()
                for epoch in (1, 2):
                    verify_sources()
                    checkpoint = output / f'epoch_{epoch - 1:04d}.pt'
                    metrics = RUN / f'{arm}_epoch_{epoch}_val256.json'
                    with (RUN / f'{arm}_epoch_{epoch}_evaluation.log').open('x', encoding='utf-8') as out:
                        subprocess.run([sys._base_executable, '-u', '-B', '-m', 'cnn.evaluate',
                            '--checkpoint', str(checkpoint), '--dataset', str(DATASET),
                            '--output', str(metrics), '--device', 'cpu', '--threads', '2',
                            '--max-images', '256'], cwd=ROOT, env=worker_environment(),
                            stdout=out, stderr=subprocess.STDOUT, check=True,
                            timeout=min(300, max(1, deadline - time.time())),
                            creationflags=subprocess.CREATE_NO_WINDOW)
                    result = json.loads(metrics.read_text(encoding='utf-8'))
                    verify_evaluation(result, baseline, epoch, checkpoint)
                    arm_state['evaluations'].append(dict(epoch=epoch, report=str(metrics),
                        sha256=sha256(metrics), metrics=result['diagnostic_metrics_at_0_5'],
                        p95_operating_points=result['p95_operating_points']))
                    publish()
                arm_state['status'] = 'completed_and_evaluated'
                break
            else:
                raise ValueError('segment cap reached; no unlimited retries')
            if state['status'] == 'paused_deadline':
                break
        else:
            state['status'] = 'completed_both_arms'
    except BaseException as error:
        state.update(status='stopped_error_no_retry', error=repr(error))
    finally:
        # If wait failed, an exited supervisor makes the existing watchdog stop its owned trainer.
        state['controller_pid'] = child.pid if child is not None and child.poll() is None else None
        state['source_checkpoint_sha256_after'] = sha256(ROAD_OUTPUT / 'epoch_0019.pt')
        if state['source_checkpoint_sha256_after'] != ROAD20_SHA:
            state.update(status='stopped_error_no_retry', error='source weights changed')
        try:
            verify_sources()
            state['source_freeze_verified'] = True
        except Exception as error:
            state.update(status='stopped_error_no_retry', error=repr(error), source_freeze_verified=False)
        publish()
    print(json.dumps(dict(status=state['status'], report=str(RUN / 'status.json'))), flush=True)
    return 1 if state['status'] == 'stopped_error_no_retry' else 0


if __name__ == '__main__':
    raise SystemExit(main())
