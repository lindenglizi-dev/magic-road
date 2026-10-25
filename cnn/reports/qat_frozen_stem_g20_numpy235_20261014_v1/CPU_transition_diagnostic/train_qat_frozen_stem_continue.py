"""Continue the reviewed frozen-Stem candidate from branch step 10 to 20."""
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import sys
import time
from types import SimpleNamespace

import numpy as np
import torch

from cnn.loss import YOLOXLoss
from cnn.train import protocol_hash, restore_rng, rng_state, sha256, _state_equal
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem as frozen
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import centered, save
from cnn.hw_validation.production.trained_integer import load_package, write_package

OUT = base.PROJECT / 'cnn/reports/qat_frozen_stem_g20_20261014_v4'
RUN = base.PROJECT / 'cnn/runs/qat_frozen_stem_g20_20261014_v4'
CHECK_DIR = OUT / 'integration_check_v1'
NUMPY_ROOT = base.PROJECT.parents[1] / '.tools/road_yolo_numpy_246_20261014/numpy'
PARENT_OUT = frozen.OUT
PARENT_RUN = frozen.RUN
PARENT = PARENT_RUN / 'last.pt'
PARENT_SHA256 = 'f58ce4501104e818c8a6fb10e378d7e7668b937b1332f3530180d4806029d3dd'
PARENT_ARTIFACTS = {
    'decision.json': '7653b98e64548a0bbf4792aa9f8b2b68e8354971226a1f7e1b10e368c89e3159',
    'control_comparison.json': 'd0ba22cf6352ee455ef0798e656ed63875025cc61efcf1430cb5973e3f826e09',
    'export_parity.json': 'b2ec6376b2b5a1a653c66564b4cddbd3e52b9f8f828a4800d0cfcd4b6aaebf61',
    'package/manifest.json': '93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b',
    'independent_completion_review.json': '7e01ff5e979c71d7afdbb278053957849eb47110f6ee66eab71aef883f97fc93',
}
FORMAT = 'road-qat-frozen-stem-continuation-v1'
START = 10
STOP = 20
SEGMENT_UPDATES = STOP - START
GLOBAL_QAT_UPDATES = 30  # preceding unfrozen 10 + this branch's cumulative 20
WORKER_MODULE = 'cnn.hw_validation.production.train_qat_frozen_stem_continue'


def native_runtime_identity():
    root = Path(np.__file__).resolve().parent
    if root != NUMPY_ROOT.resolve() or np.__version__ != '2.4.6':
        raise ValueError('project-isolated NumPy 2.4.6 is required')
    files = [root / 'random/_generator.cp313-win_amd64.pyd',
             root / '_core/_multiarray_umath.cp313-win_amd64.pyd',
             *sorted((root.parent / 'numpy.libs').glob('*.dll'))]
    hashes = {str(path): sha256(path) for path in files}
    if hashes[str(files[0])] != 'd7596499179429c584ae662296ef85738df3432c396f41f4ea5b1fe629b41f75':
        raise ValueError('isolated NumPy generator differs from verified official wheel')
    return dict(policy='project_isolated_numpy_246_v1', numpy_root=str(root),
                numpy_version=np.__version__, native_sha256=hashes,
                torch_root=str(Path(torch.__file__).resolve().parent))


def continued_record(dataset, window, global_update):
    schedule_update = global_update - START
    indices = list(window.orders[schedule_update])
    return dict(update=global_update + 1, schedule_update=schedule_update + 1,
        schedule_cycle=2, indices=indices,
        keys=[dataset.rows[index]['teacher_key'] for index in indices],
        groups=[dataset.rows[index]['sampling_group'] for index in indices])


def _optimizer_ok(state):
    groups, slots = state.get('param_groups'), state.get('state')
    if not isinstance(groups, list) or len(groups) != 1 or len(groups[0].get('params', [])) != 132:
        return False
    if set(slots or {}) != set(groups[0]['params']) or len(slots) != 132:
        return False
    return all(set(row) == {'momentum_buffer'} and torch.isfinite(row['momentum_buffer']).all()
               for row in slots.values())


def validate_parent(state, parent_identity, parent_protocol, dataset, window):
    if (state.get('format') != base.FORMAT or state.get('candidate') is not True
            or state.get('formal_acceptance') is not False
            or state.get('identity') != parent_identity
            or state.get('training_protocol') != parent_protocol
            or state.get('trained_steps') != START or state.get('next_update') != START
            or state.get('presentations') != 220 or state.get('actual_samples_per_update') != 22
            or state.get('gradients_pending') is not False or len(state.get('sample_history', [])) != START
            or set(state.get('rng_state', {})) != {'python', 'numpy', 'torch', 'cuda'}
            or not _optimizer_ok(state.get('optimizer', {}))):
        raise ValueError('parent frozen-Stem checkpoint schema mismatch')
    for index, actual in enumerate(state['sample_history']):
        expected = base.sample_record(dataset, window, index)
        if (any(actual.get(key) != value for key, value in expected.items())
                or actual.get('actual_samples') != 22
                or actual.get('frozen_stem_unchanged') is not True):
            raise ValueError('parent sample history mismatch')


def prepare():
    native_runtime = native_runtime_identity()
    if sha256(PARENT) != PARENT_SHA256:
        raise ValueError('parent checkpoint changed')
    for relative, digest in PARENT_ARTIFACTS.items():
        if sha256(PARENT_OUT / relative) != digest:
            raise ValueError(f'parent artifact changed: {relative}')
    receipt = OUT / 'cache_receipt.json'
    if not receipt.exists() or sha256(receipt) != sha256(PARENT_OUT / 'cache_receipt.json'):
        raise ValueError('G20 cache receipt missing or differs from reviewed parent')
    previous_out = base.OUT
    base.OUT = OUT
    try:
        dataset, window, folded, parent_identity, parent_protocol = frozen.prepare()
    finally:
        base.OUT = previous_out
    parent = torch.load(PARENT, map_location='cpu', weights_only=False)
    validate_parent(parent, parent_identity, parent_protocol, dataset, window)
    decision = base.read(PARENT_OUT / 'decision.json')
    comparison = base.read(PARENT_OUT / 'control_comparison.json')
    review = base.read(PARENT_OUT / 'independent_completion_review.json')
    if (decision.get('status') != 'COMPLETED_FROZEN_STEM_QAT_G10_DEVELOPMENT_RECOVERY'
            or decision.get('selected_as_INT8_development_baseline') is not True
            or decision.get('candidate_checkpoint_sha256') != PARENT_SHA256
            or decision.get('cumulative_candidate_QAT_updates') != 20
            or comparison.get('bindings', {}).get('new_candidate_checkpoint_sha256') != PARENT_SHA256
            or review.get('verdict', {}).get('artifact_integrity') != 'PASS'):
        raise ValueError('parent evaluation/decision does not authorize bounded continuation')
    schedule = [list(order) for order in window.orders]
    protocol = dict(parent_protocol,
        name='deployment_exact_qat_frozen_stem_continuation_v1',
        prior_branch_updates=START, segment_updates=SEGMENT_UPDATES,
        total_updates=STOP, global_qat_updates_after_segment=GLOBAL_QAT_UPDATES,
        schedule_cycle=2, schedule_cycle_sha256=protocol_hash(schedule),
        cpu_resume_check_threads=1)
    identity = dict(parent_identity,
        protocol_sha256=protocol_hash(protocol), experiment_id='qat_frozen_stem_g20_20261014_v4',
        native_runtime=native_runtime,
        parent_checkpoint_sha256=PARENT_SHA256,
        parent_identity=parent_identity, parent_identity_sha256=protocol_hash(parent_identity),
        parent_training_protocol=parent_protocol,
        parent_training_protocol_sha256=protocol_hash(parent_protocol),
        parent_sample_history_sha256=protocol_hash(parent['sample_history']),
        parent_decision_sha256=PARENT_ARTIFACTS['decision.json'],
        parent_control_comparison_sha256=PARENT_ARTIFACTS['control_comparison.json'],
        parent_export_parity_sha256=PARENT_ARTIFACTS['export_parity.json'])
    identity['source_sha256'] = dict(parent_identity['source_sha256'])
    for path in (Path(__file__), Path(__file__).with_name('test_qat_frozen_stem_continue.py')):
        identity['source_sha256'][str(path.relative_to(base.PROJECT)).replace('\\', '/')] = sha256(path)
    ancestry = dict(parent_checkpoint=str(PARENT.relative_to(base.PROJECT)).replace('\\', '/'),
        parent_checkpoint_sha256=PARENT_SHA256, parent_trained_steps=START,
        parent_presentations=220, parent_identity=parent_identity,
        parent_identity_sha256=protocol_hash(parent_identity),
        parent_training_protocol=parent_protocol,
        parent_training_protocol_sha256=protocol_hash(parent_protocol),
        parent_sample_history_sha256=protocol_hash(parent['sample_history']))
    return dataset, window, folded, identity, protocol, ancestry, parent


def load_state(model, optimizer, state):
    model.load_state_dict(state['model'], strict=True)
    optimizer.load_state_dict(state['optimizer'])
    restore_rng(state['rng_state'])
    stem = model.layers[model._layer_index['stem.conv']]
    if stem.weight.requires_grad or stem.bias.requires_grad or stem.weight in optimizer.state or stem.bias in optimizer.state:
        raise AssertionError('frozen Stem entered optimizer')


def update_once(model, optimizer, dataset, window, global_update, device, pause=None):
    schedule_update = global_update - START
    if not 0 <= schedule_update < SEGMENT_UPDATES:
        raise ValueError('continuation cursor outside fixed 11..20 segment')
    expected = continued_record(dataset, window, global_update)
    result = frozen.update(model, optimizer, dataset, window, schedule_update, device, pause)
    if result is None:
        return None
    result.update(update=expected['update'], schedule_update=expected['schedule_update'],
                  schedule_cycle=expected['schedule_cycle'])
    return result


def checkpoint(model, optimizer, identity, protocol, ancestry, history, *, candidate):
    count = len(history)
    return dict(format=FORMAT, checkpoint_kind='training', phase='qat', candidate=candidate,
        identity=identity, training_protocol=protocol, ancestry=ancestry,
        model=model.state_dict(), optimizer=optimizer.state_dict(), rng_state=rng_state(),
        trained_steps=count, next_update=count, presentations=count * 22,
        segment_start_update=START, segment_trained_steps=count - START,
        segment_presentations=(count - START) * 22, global_qat_updates=10 + count,
        sample_history=copy.deepcopy(history), actual_samples_per_update=22,
        gradients_pending=False, formal_acceptance=False)


def validate_state(state, identity, protocol, ancestry, parent, dataset, window, *, candidate):
    count = state.get('trained_steps')
    if (state.get('format') != FORMAT or state.get('checkpoint_kind') != 'training'
            or state.get('phase') != 'qat' or state.get('candidate') is not candidate
            or state.get('formal_acceptance') is not False or state.get('identity') != identity
            or state.get('training_protocol') != protocol or state.get('ancestry') != ancestry
            or type(count) is not int or not START <= count <= STOP
            or state.get('next_update') != count or state.get('presentations') != count * 22
            or state.get('segment_start_update') != START
            or state.get('segment_trained_steps') != count - START
            or state.get('segment_presentations') != (count - START) * 22
            or state.get('global_qat_updates') != 10 + count
            or state.get('actual_samples_per_update') != 22
            or state.get('gradients_pending') is not False
            or len(state.get('sample_history', [])) != count
            or state['sample_history'][:START] != parent['sample_history']
            or not _optimizer_ok(state.get('optimizer', {}))
            or set(state.get('rng_state', {})) != {'python', 'numpy', 'torch', 'cuda'}):
        raise ValueError('G20 continuation identity, ancestry or cursor mismatch')
    for global_update in range(START, count):
        actual = state['sample_history'][global_update]
        expected = continued_record(dataset, window, global_update)
        if (any(actual.get(key) != value for key, value in expected.items())
                or actual.get('actual_samples') != 22
                or actual.get('frozen_stem_unchanged') is not True):
            raise ValueError('G20 continuation sample history mismatch')
    for field in ('layers.0.weight', 'layers.0.bias'):
        torch.testing.assert_close(state['model'][field], parent['model'][field], atol=0, rtol=0)
    if count == START:
        if not _state_equal(state['model'], parent['model']) or not _state_equal(state['optimizer'], parent['optimizer']):
            raise ValueError('G20 start does not exactly inherit parent model/optimizer')
        streams = ('python', 'numpy', 'torch', 'cuda') if candidate else ('python', 'numpy', 'torch')
        if any(not _state_equal(state['rng_state'][name], parent['rng_state'][name]) for name in streams):
            raise ValueError('G20 start does not exactly inherit parent RNG')
    if candidate and not state['rng_state']['cuda']:
        raise ValueError('candidate continuation lost parent CUDA RNG stream')


def restore(path, model, optimizer, identity, protocol, ancestry, parent, dataset, window, *, candidate):
    state = torch.load(path, map_location='cpu', weights_only=False)
    validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=candidate)
    load_state(model, optimizer, state)
    return state


def cpu_check():
    OUT.mkdir(exist_ok=True)
    CHECK_DIR.mkdir(exist_ok=False)
    if torch.cuda.is_initialized() or torch.cuda.is_available():
        raise RuntimeError('CPU gate requires CUDA hidden')
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    dataset, window, folded, identity, protocol, ancestry, parent = prepare()
    device = torch.device('cpu')
    model, optimizer = frozen.make_model(folded, device)
    load_state(model, optimizer, parent)
    parent_cpu_rng = copy.deepcopy(rng_state())
    parent_cpu_rng_matches = all(_state_equal(parent_cpu_rng[name], parent['rng_state'][name])
                                 for name in ('python', 'numpy', 'torch'))
    if not parent_cpu_rng_matches:
        raise AssertionError('parent CPU RNG streams were not restored')
    history = copy.deepcopy(parent['sample_history'])
    history.append(update_once(model, optimizer, dataset, window, START, device))
    saved = copy.deepcopy(checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=False))
    base.commit(CHECK_DIR / 'resume_check/update_0011.pt', saved)
    history.append(update_once(model, optimizer, dataset, window, START + 1, device))
    continuous = copy.deepcopy(checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=False))
    restored_model, restored_optimizer = frozen.make_model(folded, device)
    resumed_state = restore(CHECK_DIR / 'resume_check/update_0011.pt', restored_model, restored_optimizer,
        identity, protocol, ancestry, parent, dataset, window, candidate=False)
    resumed_history = copy.deepcopy(resumed_state['sample_history'])
    resumed_history.append(update_once(restored_model, restored_optimizer, dataset, window, START + 1, device))
    resumed = checkpoint(restored_model, restored_optimizer, identity, protocol, ancestry,
                         resumed_history, candidate=False)
    for field in ('model', 'optimizer', 'rng_state', 'trained_steps', 'next_update', 'presentations'):
        if not _state_equal(continuous[field], resumed[field]):
            raise AssertionError(f'continuous versus resumed mismatch: {field}')
    for left, right in zip(continuous['sample_history'], resumed['sample_history'], strict=True):
        if ({k: v for k, v in left.items() if k != 'seconds'}
                != {k: v for k, v in right.items() if k != 'seconds'}):
            raise AssertionError('resumed continuation differs')
    for name, bad in (
            ('ancestry', dict(saved, ancestry={})),
            ('cursor', dict(saved, next_update=10)),
            ('history', dict(saved, sample_history=saved['sample_history'][:10])),
            ('global', dict(saved, global_qat_updates=20))):
        path = CHECK_DIR / f'resume_check/negative_{name}.pt'
        base.commit(path, bad)
        try:
            restore(path, restored_model, restored_optimizer, identity, protocol, ancestry,
                    parent, dataset, window, candidate=False)
        except (ValueError, AssertionError):
            pass
        else:
            raise AssertionError(f'negative continuation accepted: {name}')
    save(CHECK_DIR / 'CPU_resume_check.json', dict(passed=True, identity=identity, protocol=protocol,
        ancestry=ancestry, parent_checkpoint_sha256=PARENT_SHA256,
        parent_optimizer_momentum_states=132, parent_history_rows=10,
        continuous_global_updates=[11, 12], resumed_global_update=12,
        resumed_second_update_exact=True, cumulative_presentations=264,
        schedule_cycle=2, schedule_cycle_sha256=protocol['schedule_cycle_sha256'],
        cpu_rng_streams_compared=['python', 'numpy', 'torch'],
        cpu_threads=torch.get_num_threads(),
        parent_cpu_rng_restored=parent_cpu_rng_matches, negative_cases=4,
        optimizer_updates_published=0,
        candidate_training_started=False, cuda_initialized=torch.cuda.is_initialized()))
    print(json.dumps(dict(event='CPU_G20_resume_check_passed', parent_checkpoint_sha256=PARENT_SHA256)), flush=True)


def gpu_check(model, dataset, folded, parent, identity):
    sample, target, key = dataset[0]
    cpu = QATExactModel.from_package(base.BASE / 'package', folded, base.BASE / 'quantization.json')
    cpu.load_state_dict(parent['model'], strict=True)
    with torch.no_grad():
        cpu_heads, cpu_trace = cpu(sample.unsqueeze(0), capture=True)
    gpu_heads, gpu_trace = model(sample.unsqueeze(0).cuda(), capture=True)
    for name in cpu_trace:
        torch.testing.assert_close(cpu_trace[name], gpu_trace[name].cpu(), rtol=0, atol=0)
    for left, right in zip(cpu_heads, gpu_heads, strict=True):
        torch.testing.assert_close(left, right.cpu(), rtol=0, atol=0)
    losses = YOLOXLoss()(gpu_heads, [{name: value.cuda() for name, value in target.items()}])
    losses['loss'].backward()
    gradients = [parameter.grad for parameter in model.parameters()]
    if any(value is None or not torch.isfinite(value).all() for value in gradients):
        raise FloatingPointError('parent GPU gradient invalid')
    nonzero = sum(int(torch.count_nonzero(value)) for value in gradients)
    if not nonzero:
        raise AssertionError('parent GPU check has no detection gradients')
    model.zero_grad(set_to_none=True)
    torch.cuda.synchronize()
    save(OUT / 'GPU_check.json', dict(passed=True, identity=identity, image=key,
        parent_checkpoint_sha256=PARENT_SHA256, parent_model_used=True,
        trace_tensors=len(cpu_trace), cpu_gpu_forward_bit_exact=True,
        finite_gradient_tensors=len(gradients), nonzero_gradient_elements=nonzero,
        amp=False, tf32=False, optimizer_updates=0, gpu_name=torch.cuda.get_device_name()))


def worker(args):
    torch.set_num_threads(2)
    dataset, window, folded, identity, protocol, ancestry, parent = prepare()
    gate = base.read(CHECK_DIR / 'CPU_resume_check.json')
    if not gate.get('passed') or gate.get('identity') != identity or gate.get('protocol') != protocol:
        raise ValueError('G20 CPU resume gate stale')
    print(json.dumps(dict(event='preflight_ready', trainer_pid=os.getpid(),
        dataset_sha256=identity['dataset_sha256'], dataset_content_sha256=identity['dataset_content_sha256'],
        identity_sha256=protocol_hash(identity), resume=str(args.resume.resolve()) if args.resume else None)), flush=True)
    if not args.supervised_start or input().strip() != 'GO':
        raise RuntimeError('owned watchdog GO required')
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = torch.device('cuda')
    actual_uuid = str(getattr(torch.cuda.get_device_properties(device), 'uuid', '')).removeprefix('GPU-')
    if actual_uuid.lower() != base.GPU.removeprefix('GPU-').lower():
        raise ValueError('CUDA GPU UUID unavailable or differs from watchdog')
    model, optimizer = frozen.make_model(folded, device)
    if args.resume:
        if args.resume.resolve().parent != RUN.resolve():
            raise ValueError('resume must belong to this fixed G20 run')
        state = restore(args.resume, model, optimizer, identity, protocol, ancestry,
                        parent, dataset, window, candidate=True)
        history = copy.deepcopy(state['sample_history'])
    else:
        load_state(model, optimizer, parent)
        parent_rng = copy.deepcopy(parent['rng_state'])
        gpu_check(model, dataset, folded, parent, identity)
        restore_rng(parent_rng)
        RUN.mkdir(exist_ok=False)
        history = copy.deepcopy(parent['sample_history'])
        base.commit(RUN / 'update_0010.pt', checkpoint(
            model, optimizer, identity, protocol, ancestry, history, candidate=True))
    for global_update in range(len(history), STOP):
        record = update_once(model, optimizer, dataset, window, global_update, device, args.pause_request)
        if record is None:
            last = RUN / f'update_{len(history):04d}.pt'
            print(json.dumps(dict(event='paused_qat', trained_steps=len(history),
                checkpoint=str(last), partial_update_discarded=True)), flush=True)
            return
        history.append(record)
        state = checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=True)
        path = RUN / f'update_{len(history):04d}.pt'
        digest = base.commit(path, state)
        temporary = RUN / 'last.pt.tmp'
        shutil.copyfile(path, temporary)
        with temporary.open('rb+') as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, RUN / 'last.pt')
        print(json.dumps(dict(event='qat_update_saved', trained_steps=len(history),
            checkpoint=str(path), checkpoint_sha256=digest, **record)), flush=True)
    cpu = QATExactModel.from_package(base.BASE / 'package', folded, base.BASE / 'quantization.json')
    cpu.load_state_dict({name: value.cpu() for name, value in model.state_dict().items()}, strict=True)
    exported = write_package(OUT / 'package', cpu.graph, cpu.integer_parameters(), cpu.scales,
        dict(purpose='QAT_G20_CONTINUATION_DEVELOPMENT_CANDIDATE',
             checkpoint_sha256=sha256(RUN / 'last.pt'), source_checkpoint_sha256=base.CHECKPOINT_HASH,
             trained_steps=STOP, cumulative_qat_updates=STOP, global_qat_updates=GLOBAL_QAT_UPDATES,
             segment_qat_updates=SEGMENT_UPDATES, identity=identity,
             parent_checkpoint_sha256=PARENT_SHA256, parent_identity=ancestry['parent_identity'],
             qat_exact_fixed_weight_scales=True))
    integer, _ = load_package(OUT / 'package')
    sample = dataset[0][0]
    with torch.no_grad():
        _, trace = cpu(sample.unsqueeze(0), capture=True)
    if len(trace) != 181:
        raise AssertionError('deployment trace count changed')
    _, _, exact = integer.forward(centered(sample), capture=True)
    count = 0
    for name, value in trace.items():
        scale = 1 / 256 if name.endswith(':pre') else cpu.scales[name]
        recovered = torch.round(value / scale)[0].permute(1, 2, 0).numpy()
        np.testing.assert_array_equal(recovered, exact[name])
        count += recovered.size
    save(OUT / 'export_parity.json', dict(passed=True, trace_tensors=181, values=count,
        payload_sha256=exported['payload_sha256'], checkpoint_sha256=sha256(RUN / 'last.pt'),
        trained_steps=STOP, global_qat_updates=GLOBAL_QAT_UPDATES,
        parent_checkpoint_sha256=PARENT_SHA256, identity=identity,
        image=dataset[0][2], formal_acceptance=False))
    print(json.dumps(dict(event='completed_qat_G20', trained_steps=STOP,
        global_qat_updates=GLOBAL_QAT_UPDATES, checkpoint=str(RUN / 'last.pt'),
        checkpoint_sha256=sha256(RUN / 'last.pt'))), flush=True)


def execute():
    if RUN.exists() or (OUT / 'execution').exists():
        raise FileExistsError('G20 segment already exists; no automatic retry')
    dataset, window, _, identity, protocol, ancestry, parent = prepare()
    gate = base.read(CHECK_DIR / 'CPU_resume_check.json')
    if not gate.get('passed') or gate.get('identity') != identity or gate.get('protocol') != protocol:
        raise ValueError('G20 CPU gate missing or stale')
    folder = OUT / 'execution'
    folder.mkdir()
    (folder / 'sources').mkdir()
    for index, (relative, digest) in enumerate(identity['source_sha256'].items()):
        target = folder / 'sources' / f'{index}_{Path(relative).name}'
        shutil.copyfile(base.PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError('source snapshot differs')
    command = [sys._base_executable, '-u', '-B', '-m', WORKER_MODULE, 'worker']
    save(OUT / 'training_contract.json', dict(command=command, identity=identity, protocol=protocol,
        ancestry=ancestry, source_checkpoint=str(PARENT), parent_checkpoint_sha256=PARENT_SHA256,
        segment_start_update=START, planned_segment_updates=SEGMENT_UPDATES,
        cumulative_branch_updates=STOP, global_qat_updates_after_segment=GLOBAL_QAT_UPDATES,
        overall_qat_budget_cap=100, actual_samples_per_update=22,
        temperature_stop_c=75, hard_segment_seconds=1800,
        automatic_retry=False, automatic_continuation=False, formal_acceptance=False))

    def complete(event):
        if event.get('event') == 'paused_qat':
            state = torch.load(event['checkpoint'], map_location='cpu', weights_only=False)
            validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=True)
            return dict(status='paused_no_auto_resume', saved_updates=state['trained_steps'])
        if event.get('event') != 'completed_qat_G20' or event.get('trained_steps') != STOP:
            raise ValueError('missing complete G20 event')
        for count in range(START, STOP + 1):
            state = torch.load(RUN / f'update_{count:04d}.pt', map_location='cpu', weights_only=False)
            validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=True)
        parity = base.read(OUT / 'export_parity.json')
        final_digest = sha256(RUN / f'update_{STOP:04d}.pt')
        if (sha256(RUN / 'last.pt') != final_digest or final_digest != event['checkpoint_sha256']
                or not parity.get('passed')
                or parity.get('trace_tensors') != 181 or parity.get('trained_steps') != STOP):
            raise ValueError('final G20 export/commit differs')
        return dict(status='completed_frozen_stem_qat_G20', checkpoint_sha256=event['checkpoint_sha256'],
                    saved_updates=STOP, global_qat_updates=GLOBAL_QAT_UPDATES,
                    all_saved_Stem_states_unchanged=True)

    options = SimpleNamespace(receipt=folder / 'segment.json', output=RUN,
                              gpu_uuid=base.GPU, preflight_timeout_seconds=180)
    started = time.perf_counter()
    result = base.run_protected(command, options, expected_ready=dict(
        dataset_sha256=identity['dataset_sha256'], dataset_content_sha256=identity['dataset_content_sha256'],
        identity_sha256=protocol_hash(identity), resume=None), completion_validator=complete)
    result.update(seconds=time.perf_counter() - started, formal_acceptance=False,
        parent_checkpoint_unchanged=sha256(PARENT) == PARENT_SHA256,
        sources_unchanged=all(sha256(base.PROJECT / name) == digest
                              for name, digest in identity['source_sha256'].items()))
    save(folder / 'report.json', result)
    print(json.dumps(result), flush=True)
    if result['status'] != 'completed_frozen_stem_qat_G20':
        raise RuntimeError('G20 stopped; no automatic retry')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'execute', 'worker'))
    parser.add_argument('--pause-request', type=Path)
    parser.add_argument('--supervised-start', action='store_true')
    parser.add_argument('--resume', type=Path)
    args = parser.parse_args()
    if args.action == 'check':
        receipt = OUT / 'cache_receipt.json'
        OUT.mkdir(exist_ok=True)
        if not receipt.exists():
            shutil.copyfile(PARENT_OUT / 'cache_receipt.json', receipt)
        if sha256(receipt) != sha256(PARENT_OUT / 'cache_receipt.json'):
            raise ValueError('shared cache receipt changed')
        cpu_check()
    elif args.action == 'execute':
        execute()
    else:
        worker(args)


if __name__ == '__main__':
    main()
