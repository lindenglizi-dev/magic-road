"""Bounded deployment-exact QAT, using existing cache, replay and watchdog."""
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

from cnn.disk_cache import open_validated_cache
from cnn.loss import YOLOXLoss
from cnn.model import RoadYOLOS4
from cnn.replay_sampling import ReplayWindow
from cnn.run_post_review_s import run_protected
from cnn.train import (load_dataset_snapshot, make_frame_dataset, protocol_hash,
                       rng_state, restore_rng, set_seed, sha256, _state_equal)
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import (
    PROJECT, CHECKPOINT, CHECKPOINT_HASH, TRAIN, TRAIN_HASH, centered, save)
from cnn.hw_validation.production.trained_integer import load_package, write_package

OUT = PROJECT / 'cnn/reports/qat_g10_20261013_v1'
CHECK_DIR = OUT / 'integration_check_v2'
RUN = PROJECT / 'cnn/runs/qat_g10_20261013_v1'
BASE = PROJECT / 'cnn/reports/replay_g10_integer_20261013_v2'
MANIFEST_HASH = '64ad4e3284c4fdf90fa9f9ddc468db00159c46b152a13d440753030a979624f9'
GPU = 'GPU-a85887e6-358e-1ebb-cf09-81b558fa321a'
FORMAT = 'road-qat-resume-v1'
UPDATES = 10
MICROBATCH = 2


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepare():
    """CPU-only identities and dataset binding, before the GO/CUDA boundary."""
    for path, expected in ((CHECKPOINT, CHECKPOINT_HASH), (TRAIN, TRAIN_HASH),
                           (BASE / 'package/manifest.json', MANIFEST_HASH)):
        if sha256(path) != expected:
            raise ValueError(f'frozen input changed: {path}')
    receipt = read(OUT / 'cache_receipt.json')
    if receipt.get('passed') is not True:
        raise ValueError('cache equivalence has not passed')
    payload, snapshot = load_dataset_snapshot(TRAIN)
    binding = open_validated_cache(snapshot, Path(receipt['cache_root']), receipt['cache_index_sha256'])
    dataset = make_frame_dataset(snapshot.rows, 'train', TRAIN, mosaic=False,
        cache_root=binding.root, cache_index_sha256=binding.index_sha256, cache_binding=binding)
    window = ReplayWindow(dataset, payload['replay_sampling'], UPDATES)
    original = torch.load(CHECKPOINT, map_location='cpu', weights_only=False)
    source = RoadYOLOS4().eval()
    source.load_state_dict(original['model'], strict=True)
    if original['dataset_content_sha256'] != snapshot.dataset_content_sha256:
        raise ValueError('source training content differs')
    integer, manifest = load_package(BASE / 'package')
    quantization = BASE / 'quantization.json'
    if sha256(quantization) != manifest['provenance']['quantization_sha256']:
        raise ValueError('weight scales differ from frozen package')
    sources = [Path(__file__), *[PROJECT / 'cnn' / name for name in (
        'train.py', 'loss.py', 'model.py', 'integer.py', 'dataset.py', 'disk_cache.py',
        'replay_sampling.py', 'run_post_review_s.py', 'training_watchdog.py', 'benchmark_cache_gpu.py')],
        *[Path(__file__).with_name(name) for name in (
            'qat_exact.py', 'trained_integer.py', 'graph.py', 'numeric_package.py',
            'requant_product.py', 'run_trained_integer.py', 'test_train_qat.py')], PROJECT / 'cnn/contract.json',
            Path(__file__).with_name('deployment_contract.json')]
    protocol = dict(name='deployment_exact_qat_sgd_replay_v1', optimizer='SGD', lr=1e-4,
        momentum=.9, weight_decay=5e-4, clip_grad=10., seed=42, microbatch=MICROBATCH,
        actual_samples_per_update=22, new_samples=11, replay_samples=11,
        accumulation_normalization='sum_loss_numerators_then_divide_total_foreground',
        amp=False, tf32=False, deterministic_algorithms=True, mosaic=False,
        activation_scales='frozen_maxabs', weight_scales='frozen_per_output_channel',
        cpu_integer_forward_correction=True, total_updates=UPDATES, overall_budget_cap=100)
    identity = dict(source_checkpoint_sha256=CHECKPOINT_HASH, architecture_hash=source.architecture_hash(),
        dataset_sha256=snapshot.manifest_sha256, dataset_content_sha256=snapshot.dataset_content_sha256,
        graph_sha256=protocol_hash(integer.graph), scales_sha256=protocol_hash(integer.scales),
        source_package_manifest_sha256=MANIFEST_HASH, source_payload_sha256=manifest['payload_sha256'],
        quantization_sha256=sha256(quantization), sampling_sha256=window.sampling_sha256,
        cache_index_sha256=binding.index_sha256, cache_rgb_sha256=binding.metadata['rgb_sha256'],
        protocol_sha256=protocol_hash(protocol),
        source_sha256={str(path.relative_to(PROJECT)).replace('\\', '/'): sha256(path) for path in sources},
        torch_version=torch.__version__, numpy_version=np.__version__,
        python_executable_sha256=sha256(Path(sys._base_executable)))
    return dataset, window, source.folded_conv_state(), identity, protocol


def model_and_optimizer(folded, device):
    model = QATExactModel.from_package(BASE / 'package', folded, BASE / 'quantization.json').to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
    return model, optimizer


def sample_record(dataset, window, update):
    indices = list(window.orders[update])
    return dict(update=update + 1, indices=indices,
        keys=[dataset.rows[index]['teacher_key'] for index in indices],
        groups=[dataset.rows[index]['sampling_group'] for index in indices])


def update_once(model, optimizer, dataset, window, update, device, pause=None):
    window.set_epoch(update, mosaic=False)
    optimizer.zero_grad(set_to_none=True)
    criterion = YOLOXLoss()
    started = time.perf_counter()
    loss_sum = 0.
    total_foreground = 0
    record = sample_record(dataset, window, update)
    actual_keys = []
    for offset in range(0, 22, MICROBATCH):
        if pause is not None and pause.exists():
            optimizer.zero_grad(set_to_none=True)
            return None  # Current partial gradients are deliberately never published.
        samples = [window[index] for index in range(offset, min(offset + MICROBATCH, 22))]
        actual_keys.extend(sample[2] for sample in samples)
        images = torch.stack([sample[0] for sample in samples]).to(device)
        targets = [{name: value.to(device) for name, value in sample[1].items()} for sample in samples]
        losses = criterion(model(images), targets)
        if any(not torch.isfinite(value).all() for value in losses.values()):
            raise FloatingPointError('nonfinite detection loss')
        foreground = int(losses['num_foreground'].detach())
        contribution = losses['loss'] * max(foreground, 1)
        contribution.backward()
        loss_sum += float(contribution.detach())
        total_foreground += foreground
        print(json.dumps(dict(event='microbatch', update=update + 1,
            samples_consumed=offset + len(samples), actual_update_samples=22)), flush=True)
    if actual_keys != record['keys']:
        raise ValueError('actual input sample keys disagree with frozen replay order')
    gradients = [parameter.grad for parameter in model.parameters()]
    if any(value is None or not torch.isfinite(value).all() for value in gradients):
        raise FloatingPointError('missing or nonfinite gradient')
    for gradient in gradients:
        gradient.div_(max(total_foreground, 1))
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
    model.integer_parameters()  # Reject unexportable bias/accumulator bounds before committing.
    if device.type == 'cuda':
        torch.cuda.synchronize()
    record.update(loss=loss_sum / max(total_foreground, 1), foreground=total_foreground,
                  gradient_norm_before_clip=float(norm),
                  seconds=time.perf_counter() - started, actual_samples=22)
    return record


def checkpoint(model, optimizer, identity, protocol, history, *, candidate):
    return dict(format=FORMAT, checkpoint_kind='training', phase='qat', candidate=candidate,
        identity=identity, training_protocol=protocol, model=model.state_dict(),
        optimizer=optimizer.state_dict(), rng_state=rng_state(), trained_steps=len(history),
        next_update=len(history), presentations=len(history) * 22,
        sample_history=copy.deepcopy(history), actual_samples_per_update=22,
        gradients_pending=False, formal_acceptance=False)


def commit(path, state):
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.pt.tmp')
    with temporary.open('xb') as stream:
        torch.save(state, stream)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    return sha256(path)


def validate_state(state, identity, protocol, dataset, window, *, expected_candidate):
    count = state.get('trained_steps')
    if (state.get('format') != FORMAT or state.get('checkpoint_kind') != 'training'
            or state.get('phase') != 'qat' or state.get('actual_samples_per_update') != 22
            or state.get('candidate') is not expected_candidate or state.get('formal_acceptance') is not False
            or state.get('identity') != identity
            or state.get('training_protocol') != protocol
            or type(count) is not int or not 0 <= count <= UPDATES
            or state.get('next_update') != count or state.get('presentations') != count * 22
            or state.get('gradients_pending') is not False
            or len(state.get('sample_history', [])) != count):
        raise ValueError('QAT resume identity or cursor mismatch')
    for index, actual in enumerate(state['sample_history']):
        expected = sample_record(dataset, window, index)
        if any(actual.get(key) != value for key, value in expected.items()) or actual.get('actual_samples') != 22:
            raise ValueError('QAT resume sample history mismatch')


def restore(path, model, optimizer, identity, protocol, dataset, window, *, expected_candidate=False):
    state = torch.load(path, map_location='cpu', weights_only=False)
    validate_state(state, identity, protocol, dataset, window, expected_candidate=expected_candidate)
    model.load_state_dict(state['model'], strict=True)
    optimizer.load_state_dict(state['optimizer'])
    restore_rng(state['rng_state'])
    return state


def cpu_check():
    OUT.mkdir(exist_ok=True)
    CHECK_DIR.mkdir(exist_ok=False)
    if torch.cuda.is_initialized():
        raise RuntimeError('CPU gate requires CUDA hidden')
    torch.set_num_threads(2)
    dataset, window, folded, identity, protocol = prepare()
    set_seed(42)
    device = torch.device('cpu')
    model, optimizer = model_and_optimizer(folded, device)
    history = [update_once(model, optimizer, dataset, window, 0, device)]
    saved = checkpoint(model, optimizer, identity, protocol, history, candidate=False)
    commit(CHECK_DIR / 'resume_check/update_0001.pt', saved)
    history.append(update_once(model, optimizer, dataset, window, 1, device))
    continuous = copy.deepcopy(checkpoint(model, optimizer, identity, protocol, history, candidate=False))
    restored, other_optimizer = model_and_optimizer(folded, device)
    state = restore(CHECK_DIR / 'resume_check/update_0001.pt', restored, other_optimizer,
                    identity, protocol, dataset, window)
    resumed_record = update_once(restored, other_optimizer, dataset, window, state['next_update'], device)
    resumed = checkpoint(restored, other_optimizer, identity, protocol,
        state['sample_history'] + [resumed_record], candidate=False)
    for field in ('model', 'optimizer', 'rng_state', 'trained_steps', 'next_update', 'presentations'):
        if not _state_equal(continuous[field], resumed[field]):
            raise AssertionError(f'continuous versus resumed mismatch: {field}')
    for left, right in zip(continuous['sample_history'], resumed['sample_history'], strict=True):
        if {k: v for k, v in left.items() if k != 'seconds'} != {k: v for k, v in right.items() if k != 'seconds'}:
            raise AssertionError('resumed samples, losses or gradients differ')
    # Real negative cursor/history cases must fail before loading model/optimizer state.
    for name, bad in (('cursor', dict(saved, next_update=0)),
                      ('presentations', dict(saved, presentations=44)),
                      ('identity', dict(saved, identity={})),
                      ('sample_history', dict(saved, sample_history=[]))):
        path = CHECK_DIR / f'resume_check/negative_{name}.pt'
        commit(path, bad)
        try:
            restore(path, restored, other_optimizer, identity, protocol, dataset, window)
        except ValueError:
            pass
        else:
            raise AssertionError(f'resume negative case accepted: {name}')
    save(CHECK_DIR / 'CPU_resume_check.json', dict(passed=True, identity=identity, protocol=protocol,
        continuous_updates=2, resumed_second_update_exact=True, presentations=44,
        microbatch=MICROBATCH, actual_update_samples=22, negative_cases=4,
        candidate_training_started=False, cuda_initialized=torch.cuda.is_initialized(),
        first_two_orders=[sample_record(dataset, window, index) for index in range(2)]))
    print(json.dumps(dict(event='CPU_resume_check_passed', source_checkpoint_sha256=CHECKPOINT_HASH)), flush=True)


def gpu_check(model, dataset, folded, identity):
    sample, target, key = dataset[0]
    cpu = QATExactModel.from_package(BASE / 'package', folded, BASE / 'quantization.json')
    with torch.no_grad():
        cpu_heads, cpu_trace = cpu(sample.unsqueeze(0), capture=True)
    gpu_heads, gpu_trace = model(sample.unsqueeze(0).cuda(), capture=True)
    for name in cpu_trace:
        torch.testing.assert_close(cpu_trace[name], gpu_trace[name].detach().cpu(), rtol=0, atol=0)
    for left, right in zip(cpu_heads, gpu_heads, strict=True):
        torch.testing.assert_close(left, right.detach().cpu(), rtol=0, atol=0)
    losses = YOLOXLoss()(gpu_heads, [{name: value.cuda() for name, value in target.items()}])
    losses['loss'].backward()
    gradients = [parameter.grad for parameter in model.parameters()]
    if any(value is None or not torch.isfinite(value).all() for value in gradients):
        raise FloatingPointError('GPU check gradient invalid')
    nonzero = sum(int(torch.count_nonzero(value)) for value in gradients)
    if not nonzero:
        raise AssertionError('GPU check has no detection gradients')
    model.zero_grad(set_to_none=True)
    torch.cuda.synchronize()
    save(OUT / 'GPU_check.json', dict(passed=True, identity=identity, image=key,
        trace_tensors=len(cpu_trace), cpu_gpu_forward_bit_exact=True,
        finite_gradient_tensors=len(gradients), nonzero_gradient_elements=nonzero,
        amp=False, tf32=False, optimizer_updates=0, gpu_name=torch.cuda.get_device_name()))


def worker(args):
    torch.set_num_threads(2)
    dataset, window, folded, identity, protocol = prepare()
    gate = read(CHECK_DIR / 'CPU_resume_check.json')
    if not gate['passed'] or gate['identity'] != identity or gate['protocol'] != protocol:
        raise ValueError('CPU resume gate stale')
    ready = dict(event='preflight_ready', trainer_pid=os.getpid(),
        dataset_sha256=identity['dataset_sha256'], dataset_content_sha256=identity['dataset_content_sha256'],
        identity_sha256=protocol_hash(identity), resume=str(args.resume.resolve()) if args.resume else None)
    print(json.dumps(ready), flush=True)
    if not args.supervised_start or input().strip() != 'GO':
        raise RuntimeError('owned watchdog GO required')
    set_seed(42)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = torch.device('cuda')
    actual_uuid = str(getattr(torch.cuda.get_device_properties(device), 'uuid', '')).removeprefix('GPU-')
    if actual_uuid.lower() != GPU.removeprefix('GPU-').lower():
        raise ValueError('CUDA GPU UUID unavailable or differs from watchdog')
    model, optimizer = model_and_optimizer(folded, device)
    history = []
    if args.resume:
        if args.resume.resolve().parent != RUN.resolve():
            raise ValueError('QAT resume must belong to the candidate run directory')
        restored = restore(args.resume, model, optimizer, identity, protocol, dataset, window,
                           expected_candidate=True)
        history = restored['sample_history']
    else:
        gpu_check(model, dataset, folded, identity)
        RUN.mkdir(exist_ok=False)
        commit(RUN / 'update_0000.pt', checkpoint(model, optimizer, identity, protocol, [], candidate=True))
    for update in range(len(history), UPDATES):
        record = update_once(model, optimizer, dataset, window, update, device, args.pause_request)
        if record is None:
            last = RUN / f'update_{len(history):04d}.pt'
            print(json.dumps(dict(event='paused_qat', trained_steps=len(history),
                checkpoint=str(last), partial_update_discarded=True)), flush=True)
            return
        history.append(record)
        state = checkpoint(model, optimizer, identity, protocol, history, candidate=True)
        path = RUN / f'update_{len(history):04d}.pt'
        digest = commit(path, state)
        temporary = RUN / 'last.pt.tmp'
        shutil.copyfile(path, temporary)
        with temporary.open('rb+') as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, RUN / 'last.pt')
        print(json.dumps(dict(event='qat_update_saved', trained_steps=len(history), checkpoint=str(path),
            checkpoint_sha256=digest, **record)), flush=True)
    cpu = QATExactModel.from_package(BASE / 'package', folded, BASE / 'quantization.json')
    cpu.load_state_dict({name: value.cpu() for name, value in model.state_dict().items()}, strict=True)
    exported = write_package(OUT / 'package', cpu.graph, cpu.integer_parameters(), cpu.scales,
        dict(purpose='QAT_G10_DEVELOPMENT_CANDIDATE', checkpoint_sha256=sha256(RUN / 'last.pt'),
             source_checkpoint_sha256=CHECKPOINT_HASH, trained_steps=UPDATES, identity=identity,
             qat_exact_fixed_weight_scales=True))
    integer, _ = load_package(OUT / 'package')
    sample = dataset[0][0]
    with torch.no_grad():
        _, trace = cpu(sample.unsqueeze(0), capture=True)
    _, _, exact = integer.forward(centered(sample), capture=True)
    count = 0
    for name, value in trace.items():
        scale = 1 / 256 if name.endswith(':pre') else cpu.scales[name]
        recovered = torch.round(value / scale)[0].permute(1, 2, 0).numpy()
        np.testing.assert_array_equal(recovered, exact[name])
        count += recovered.size
    save(OUT / 'export_parity.json', dict(passed=True, trace_tensors=len(trace), values=count,
        payload_sha256=exported['payload_sha256'], checkpoint_sha256=sha256(RUN / 'last.pt'),
        identity=identity, image=dataset[0][2], formal_acceptance=False))
    print(json.dumps(dict(event='completed_qat_G10', trained_steps=UPDATES,
        checkpoint=str(RUN / 'last.pt'), checkpoint_sha256=sha256(RUN / 'last.pt'))), flush=True)


def execute():
    if RUN.exists():
        raise FileExistsError('new run already exists; no automatic restart')
    dataset, window, folded, identity, protocol = prepare()
    gate = read(CHECK_DIR / 'CPU_resume_check.json')
    if not gate['passed'] or gate['identity'] != identity:
        raise ValueError('CPU gate missing or stale')
    folder = OUT / 'execution'
    folder.mkdir(exist_ok=False)
    (folder / 'sources').mkdir()
    for index, (relative, digest) in enumerate(identity['source_sha256'].items()):
        target = folder / 'sources' / f'{index}_{Path(relative).name}'
        shutil.copyfile(PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError('source snapshot differs')
    command = [sys._base_executable, '-u', '-B', '-m', 'cnn.hw_validation.production.train_qat', 'worker']
    save(OUT / 'training_contract.json', dict(command=command, identity=identity, protocol=protocol,
        temperature_stop_c=75, hard_segment_seconds=1800, automatic_retry=False,
        automatic_continuation=False, source_checkpoint= str(CHECKPOINT),
        actual_samples_per_update=22, planned_updates=10, formal_acceptance=False))

    def complete(event):
        if event.get('event') == 'paused_qat':
            path = Path(event['checkpoint'])
            state = torch.load(path, map_location='cpu', weights_only=False)
            if state['identity'] != identity or state['trained_steps'] != event['trained_steps']:
                raise ValueError('pause checkpoint mismatch')
            return dict(status='paused_no_auto_resume', saved_updates=state['trained_steps'])
        if event.get('event') != 'completed_qat_G10' or event.get('trained_steps') != UPDATES:
            raise ValueError('missing complete QAT event')
        for index in range(1, UPDATES + 1):
            state = torch.load(RUN / f'update_{index:04d}.pt', map_location='cpu', weights_only=False)
            validate_state(state, identity, protocol, dataset, window, expected_candidate=True)
            if state['identity'] != identity or state['trained_steps'] != index or state['presentations'] != 22 * index:
                raise ValueError('saved checkpoint identity/count mismatch')
        if sha256(RUN / 'last.pt') != event['checkpoint_sha256'] or not read(OUT / 'export_parity.json')['passed']:
            raise ValueError('final export/commit differs')
        return dict(status='completed_qat_G10', checkpoint_sha256=event['checkpoint_sha256'], saved_updates=10)

    options = SimpleNamespace(receipt=folder / 'segment.json', output=RUN,
                              gpu_uuid=GPU, preflight_timeout_seconds=180)
    started = time.perf_counter()
    result = run_protected(command, options, expected_ready=dict(
        dataset_sha256=identity['dataset_sha256'], dataset_content_sha256=identity['dataset_content_sha256'],
        identity_sha256=protocol_hash(identity), resume=None), completion_validator=complete)
    result.update(seconds=time.perf_counter() - started, formal_acceptance=False,
        original_checkpoint_unchanged=sha256(CHECKPOINT) == CHECKPOINT_HASH,
        sources_unchanged=all(sha256(PROJECT / name) == digest for name, digest in identity['source_sha256'].items()))
    save(folder / 'report.json', result)
    print(json.dumps(result), flush=True)
    if result['status'] != 'completed_qat_G10':
        raise RuntimeError('QAT stopped; no automatic retry')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'execute', 'worker'))
    parser.add_argument('--pause-request', type=Path)
    parser.add_argument('--supervised-start', action='store_true')
    parser.add_argument('--resume', type=Path)
    args = parser.parse_args()
    if args.action == 'check':
        cpu_check()
    elif args.action == 'execute':
        execute()
    else:
        worker(args)


if __name__ == '__main__':
    main()
