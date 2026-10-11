"""One authorized batch: native epoch2 -> epoch7, then CPU val256 and stop."""
from datetime import datetime
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from . import run_road_epoch as segment
from .run_road_overnight import continuation, verify_evaluation

ROOT = segment.ROOT
RUN = segment.RECOVERY_REPORTS
OUTPUT = segment.RECOVERY_OUTPUT
SOURCE = segment.NATIVE2
SOURCE_SHA = segment.NATIVE2_SHA
BASELINE = ROOT / 'cnn/reports/person_ab_20261004/native_epoch_2_val256.json'
BASELINE_SHA = '62b71ab03e65f8d16ef9f5bf96aa487fe1a3ac4669e33498320b72da0ace0c90'


def validate_source(source, baseline):
    from . import train
    train.ensure_resume_eligible(source)
    protocol = source['training_protocol']
    if (source['format'] != 'road-yolo-checkpoint-v2' or source['epoch'] != 1
            or source['trained_steps'] != 596 or protocol['mosaic'] is not False
            or protocol['epochs'] != 40 or source['effective_batch'] != 64
            or baseline['checkpoint_sha256'] != SOURCE_SHA
            or baseline['checkpoint_epoch_number'] != 2
            or baseline['acceptance_eligible'] is not False
            or source['dataset_sha256'] != segment.DATASET_SHA
            or source['dataset_content_sha256'] != segment.CONTENT_SHA
            or source['architecture_hash'] != segment.ARCHITECTURE_SHA):
        raise ValueError('not the complete frozen native epoch2 state/baseline')
    for key in ('model', 'optimizer', 'scaler', 'rng_state'):
        if not isinstance(source.get(key), dict):
            raise ValueError('missing complete training state: ' + key)
    train._validate_v3_cursors(source, train_size=19050, val_size=5151,
                              batch_size=8, accum_steps=8, optimizer_steps_per_epoch=298, seed=42)


def comparison(result, baseline):
    from .metrics import evaluate
    classes = {}
    for label, name in enumerate(('person', 'vehicle')):
        current = result['diagnostic_metrics_at_0_5']['classes'][name]
        old = baseline['diagnostic_metrics_at_0_5']['classes'][name]
        low = evaluate(result['predictions'], result['truth'], result['ignores'],
                       label=label, threshold=.05)
        old_low = evaluate(baseline['predictions'], baseline['truth'], baseline['ignores'],
                           label=label, threshold=.05)
        classes[name] = dict(current=current, baseline=old, at_score_0_05=low,
            baseline_at_score_0_05=old_low,
            delta_percentage_points={key: 100 * (current[key] - old[key])
                for key in ('precision', 'recall', 'ap50', 'ap50_95')})
    delta = {name: value['delta_percentage_points']['ap50'] for name, value in classes.items()}
    return dict(classes=classes, p95_operating_points=result['p95_operating_points'],
                validation_thresholds=result['validation_thresholds'],
                candidate_diagnostics=dict(current=candidate_diagnostics(result),
                                           baseline=candidate_diagnostics(baseline)),
                development_observation_pass=delta['person'] >= 1 and delta['vehicle'] >= -1,
                formal_acceptance=False, next_training_requires_new_authorization=True)


def candidate_diagnostics(result):
    """Retained-box coverage, NOT one-to-one recall or proof of missing labels."""
    from .metrics import overlap
    predictions, counts = defaultdict(list), Counter()
    for row in result['predictions']:
        predictions[row['image_id']].append(row)
        counts[(row['image_id'], row['label'])] += 1
    groups = defaultdict(Counter)
    for truth in result['truth']:
        local = predictions[truth['image_id']]
        same = [row for row in local if row['label'] == truth['label']]
        correct = [row for row in same if overlap(row['box'], truth['box']) >= .5]
        if correct:
            reason = ('covered_score_ge_0_5' if max(row['score'] for row in correct) >= .5
                      else 'covered_only_below_score_0_5')
        elif any(overlap(row['box'], truth['box']) >= .5 for row in local):
            reason = 'wrong_class_overlap'
        elif any(overlap(row['box'], truth['box']) >= .25 for row in same):
            reason = 'localization_0_25_to_0_5'
        else:
            reason = 'no_retained_candidate_cause_unresolved'
        name = ('person', 'vehicle')[truth['label']]
        height = truth['box'][3] - truth['box'][1]
        size = 'h_le_8' if height <= 8 else 'h_8_to_16' if height <= 16 else 'h_gt_16'
        scene = Path(truth['image_id']).parent.as_posix()
        for key in (name, name + '/' + size, name + '/scene/' + scene):
            groups[key].update(total=1)
            groups[key][reason] += 1
    truth_counts = Counter((row['image_id'], row['label']) for row in result['truth'])
    ceiling = {name: sum(min(32, count) for (_, cls), count in truth_counts.items() if cls == label)
               / max(1, sum(count for (_, cls), count in truth_counts.items() if cls == label))
               for label, name in enumerate(('person', 'vehicle'))}
    return dict(groups={key: dict(value) for key, value in groups.items()},
                image_class_pairs_at_32_retained_boxes=sum(count == 32 for count in counts.values()),
                oracle_recall_ceiling_at_max32=ceiling,
                limitation='candidate coverage can double count; not detection recall; '
                           'no raw-head visibility to prove Top-K truncation; labels not auto-reviewed')


def main():
    import torch
    if OUTPUT.exists() or RUN.exists():
        raise FileExistsError('five-epoch batch already reserved; do not duplicate/restart it')
    if segment.sha256(SOURCE) != SOURCE_SHA or segment.sha256(BASELINE) != BASELINE_SHA:
        raise ValueError('frozen native epoch2 weights/evaluation changed')
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    source = torch.load(SOURCE, map_location='cpu', weights_only=False)
    validate_source(source, baseline)
    del source
    sources = {path.name: segment.sha256(path) for path in (ROOT / 'cnn').glob('*.py')}

    def verify_sources():
        if {path.name: segment.sha256(path) for path in (ROOT / 'cnn').glob('*.py')} != sources:
            raise ValueError('Python sources changed during the batch')
        if segment.sha256(SOURCE) != SOURCE_SHA or segment.sha256(BASELINE) != BASELINE_SHA:
            raise ValueError('original A/B artifacts changed')

    RUN.mkdir()  # Exclusive directory is the duplicate-launch lock; never clear it automatically.
    deadline = time.time() + 2 * 3600
    state = dict(status='starting', owner_pid=os.getpid(), controller_pid=None,
        started_at=datetime.now().astimezone().isoformat(), deadline_unix=deadline,
        target_epoch=7, start_epoch=2, additional_epochs=5, last_completed_epoch=2,
        source_checkpoint=str(SOURCE), source_checkpoint_sha256=SOURCE_SHA,
        baseline_report=str(BASELINE), baseline_report_sha256=BASELINE_SHA,
        initialization='full_model_optimizer_scaler_RNG_continuation_no_warmup_reset',
        source_sha256=sources, segments=[], acceptance_eligible=False)

    def publish():
        state['updated_at'] = datetime.now().astimezone().isoformat()
        temporary = RUN / 'status.tmp'
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(RUN / 'status.json')

    child = None
    try:
        publish()
        OUTPUT.mkdir()
        shutil.copyfile(SOURCE, OUTPUT / 'last.pt')
        if segment.sha256(OUTPUT / 'last.pt') != SOURCE_SHA:
            raise ValueError('full-state copy differs from source')
        for iteration in range(1, 7):
            verify_sources()
            if time.time() >= deadline - 120:
                state['status'] = 'paused_deadline'
                break
            log = RUN / f'segment_{iteration:02d}.log'
            command = [sys._base_executable, '-u', '-B', '-m', 'cnn.run_road_epoch',
                '--person-recovery-five', '--stop-after-epoch', '7',
                '--deadline-unix', str(deadline), '--supervisor-pid', str(os.getpid())]
            with log.open('x', encoding='utf-8') as out, (RUN / f'segment_{iteration:02d}.stderr.log').open(
                    'x', encoding='utf-8') as err:
                child = subprocess.Popen(command, cwd=ROOT, env=segment.worker_environment(),
                    stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
                state.update(status='training', controller_pid=child.pid, controller_log=str(log))
                publish()
                code = child.wait(timeout=max(1, deadline - time.time() + 65))
            final = json.loads(log.read_text(encoding='utf-8').splitlines()[-1])
            report_path = Path(final['report'])
            if report_path.parent.parent.resolve() != (RUN / 'segments').resolve():
                raise ValueError('segment report outside the batch')
            report = json.loads(report_path.read_text(encoding='utf-8'))
            state['segments'].append(dict(report=str(report_path), status=report['status'],
                sha256=segment.sha256(report_path), peak_temperature_c=report.get('peak_temperature_c')))
            complete = report.get('checkpoints', {}).get('last.pt', {})
            if complete.get('valid'):
                state['last_completed_epoch'] = complete['epoch'] + 1
            pause = report_path.parent / 'pause.json'
            action = continuation(report, code, json.loads(pause.read_text())['reason'] if pause.exists() else None)
            if action == 'stop_deadline':
                state['status'] = 'paused_deadline'
                break
            if action == 'resume_same_epoch':
                publish()
                continue
            if state['last_completed_epoch'] != 7:
                raise ValueError('batch did not finish exactly at epoch7')
            state.update(status='evaluating', controller_pid=None)
            publish()
            verify_sources()
            checkpoint = OUTPUT / 'epoch_0006.pt'
            metrics = RUN / 'epoch_7_val256.json'
            with (RUN / 'evaluation.log').open('x', encoding='utf-8') as out:
                subprocess.run([sys._base_executable, '-u', '-B', '-m', 'cnn.evaluate',
                    '--checkpoint', str(checkpoint), '--dataset', str(segment.DATASET),
                    '--output', str(metrics), '--device', 'cpu', '--threads', '2', '--max-images', '256'],
                    cwd=ROOT, env=segment.worker_environment(), stdout=out, stderr=subprocess.STDOUT,
                    check=True, timeout=min(300, max(1, deadline - time.time())),
                    creationflags=subprocess.CREATE_NO_WINDOW)
            result = json.loads(metrics.read_text(encoding='utf-8'))
            verify_evaluation(result, baseline, 7, checkpoint)
            state.update(status='completed_epoch7_evaluated', evaluation_report=str(metrics),
                evaluation_sha256=segment.sha256(metrics), comparison=comparison(result, baseline))
            break
        else:
            raise ValueError('segment cap reached; no unlimited retries')
    except BaseException as error:
        state.update(status='stopped_error_no_retry', error=repr(error))
    finally:
        state['controller_pid'] = child.pid if child is not None and child.poll() is None else None
        # Losing this supervisor stops the owned trainer via the existing independent watchdog.
        try:
            verify_sources()
            state['source_freeze_verified'] = True
        except Exception as error:
            state.update(status='stopped_error_no_retry', error=repr(error), source_freeze_verified=False)
        state['total_seconds'] = time.time() - (deadline - 2 * 3600)
        publish()
    print(json.dumps(dict(status=state['status'], report=str(RUN / 'status.json'))), flush=True)
    return int(state['status'] == 'stopped_error_no_retry')


if __name__ == '__main__':
    raise SystemExit(main())
