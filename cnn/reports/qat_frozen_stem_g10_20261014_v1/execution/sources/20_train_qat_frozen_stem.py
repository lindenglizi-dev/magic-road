"""One frozen-Stem control; retain the preceding runner and artifacts unchanged."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import time
from types import SimpleNamespace

import numpy as np
import torch

from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.train import protocol_hash, sha256

PREVIOUS = base.OUT
OUT = base.PROJECT / 'cnn/reports/qat_frozen_stem_g10_20261014_v1'
RUN = base.PROJECT / 'cnn/runs/qat_frozen_stem_g10_20261014_v1'
_prepare = base.prepare
_update = base.update_once
BASE_SOURCE_HASH = '33086b5725c84ce687b91e869ee954befd4bb910d8a50101a3012d334921ae35'


class FrozenStemQAT(QATExactModel):
    def parameters(self, recurse=True):
        # The reused runner clips/checks every yielded parameter. Exclude frozen
        # Stem here; named_parameters/state_dict still retain its complete state.
        return (parameter for parameter in super().parameters(recurse=recurse) if parameter.requires_grad)


def make_model(folded, device):
    model = FrozenStemQAT.from_package(base.BASE / 'package', folded, base.BASE / 'quantization.json')
    stem = model.layers[model._layer_index['stem.conv']]
    stem.weight.requires_grad_(False)
    stem.bias.requires_grad_(False)
    model.to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
    return model, optimizer


def prepare():
    if sha256(Path(base.__file__)) != BASE_SOURCE_HASH:
        raise ValueError('preceding runner source changed')
    dataset, window, folded, identity, protocol = _prepare()
    prior = base.read(PREVIOUS / 'decision.json')
    if (prior['updates_completed'] != 10 or prior['continue_training']
            or prior.get('experiment_id') != 'qat_g10_20261013_v1'
            or prior.get('status') != 'COMPLETED_QAT_G10_REJECTED_AFTER_DEVELOPMENT17'
            or prior.get('selected_FP32_source_checkpoint_sha256') != base.CHECKPOINT_HASH):
        raise ValueError('previous comparison is not frozen/stopped')
    inspection = base.read(OUT / 'gradient_inspection.json')
    expected_sources = dict(identity['source_sha256'])
    script = Path(__file__).with_name('inspect_qat_gradients.py')
    expected_sources[str(script.relative_to(base.PROJECT)).replace('\\', '/')] = sha256(script)
    if (inspection.get('optimizer_updates') != 0 or inspection.get('finite_gradients') is not True
            or inspection.get('identity') != identity or inspection.get('protocol') != protocol
            or inspection.get('source_closure') != expected_sources):
        raise ValueError('train-only finite gradient inspection missing')
    protocol = dict(protocol, name='deployment_exact_qat_frozen_stem_control_v1',
                    frozen_layers=['stem.conv'], frozen_fields=['weight', 'bias'], prior_qat_updates=10)
    identity = dict(identity, protocol_sha256=protocol_hash(protocol),
                    previous_decision_sha256=sha256(PREVIOUS / 'decision.json'),
                    gradient_inspection_sha256=sha256(OUT / 'gradient_inspection.json'),
                    experiment_id='qat_frozen_stem_g10_20261014_v1')
    identity['source_sha256'] = dict(identity['source_sha256'])
    for path in (Path(__file__), Path(__file__).with_name('test_qat_frozen_stem.py'),
                 Path(__file__).with_name('inspect_qat_gradients.py')):
        identity['source_sha256'][str(path.relative_to(base.PROJECT)).replace('\\', '/')] = sha256(path)
    return dataset, window, folded, identity, protocol


def update(model, optimizer, dataset, window, index, device, pause=None):
    stem = model.layers[model._layer_index['stem.conv']]
    before = (stem.weight.detach().clone(), stem.bias.detach().clone())
    result = _update(model, optimizer, dataset, window, index, device, pause)
    for actual, expected in zip((stem.weight, stem.bias), before, strict=True):
        torch.testing.assert_close(actual, expected, atol=0, rtol=0)
        if actual.requires_grad or actual.grad is not None or actual in optimizer.state:
            raise AssertionError('frozen Stem acquired gradient/optimizer state')
    if result is not None:
        result['frozen_stem_unchanged'] = True
    return result


def install():
    # Process-local adapter: no edits to the source closure of the prior run.
    base.OUT, base.RUN, base.CHECK_DIR = OUT, RUN, OUT / 'integration_check_v2'
    base.prepare, base.model_and_optimizer, base.update_once = prepare, make_model, update


def execute():
    if RUN.exists() or (OUT / 'execution').exists():
        raise FileExistsError('independent trial already exists; no automatic retry')
    dataset, window, folded, identity, protocol = prepare()
    gate = base.read(base.CHECK_DIR / 'CPU_resume_check.json')
    if not gate['passed'] or gate['identity'] != identity or gate['protocol'] != protocol:
        raise ValueError('frozen-Stem CPU restore gate stale')
    folder = OUT / 'execution'
    folder.mkdir()
    (folder / 'sources').mkdir()
    for index, (relative, digest) in enumerate(identity['source_sha256'].items()):
        target = folder / 'sources' / f'{index}_{Path(relative).name}'
        shutil.copyfile(base.PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError('source snapshot mismatch')
    command = [sys._base_executable, '-u', '-B', '-m',
               'cnn.hw_validation.production.train_qat_frozen_stem', 'worker']
    base.save(OUT / 'training_contract.json', dict(command=command, identity=identity, protocol=protocol,
        planned_updates=10, actual_samples_per_update=22, cumulative_qat_updates_after_trial=20,
        overall_qat_budget_cap=100, temperature_stop_c=75, hard_segment_seconds=1800,
        automatic_retry=False, automatic_continuation=False, formal_acceptance=False))

    def complete(event):
        if event.get('event') == 'paused_qat':
            state = torch.load(event['checkpoint'], map_location='cpu', weights_only=False)
            base.validate_state(state, identity, protocol, dataset, window, expected_candidate=True)
            return dict(status='paused_no_auto_resume', saved_updates=state['trained_steps'])
        if event.get('event') != 'completed_qat_G10' or event.get('trained_steps') != 10:
            raise ValueError('missing completed frozen-Stem event')
        initial = torch.load(RUN / 'update_0000.pt', map_location='cpu', weights_only=False)
        fields = ('layers.0.weight', 'layers.0.bias')
        for index in range(1, 11):
            state = torch.load(RUN / f'update_{index:04d}.pt', map_location='cpu', weights_only=False)
            base.validate_state(state, identity, protocol, dataset, window, expected_candidate=True)
            if state['trained_steps'] != index:
                raise ValueError('saved update cursor mismatch')
            for field in fields:
                torch.testing.assert_close(state['model'][field], initial['model'][field], atol=0, rtol=0)
            if not all(row['frozen_stem_unchanged'] for row in state['sample_history']):
                raise ValueError('missing per-update Stem freeze evidence')
        if sha256(RUN / 'last.pt') != event['checkpoint_sha256']:
            raise ValueError('final checkpoint mismatch')
        parity = base.read(OUT / 'export_parity.json')
        if not parity['passed'] or parity['checkpoint_sha256'] != event['checkpoint_sha256']:
            raise ValueError('export parity failed')
        integer, _ = base.load_package(OUT / 'package')
        original, _ = base.load_package(base.BASE / 'package')
        for field in original.parameters['stem.conv']:
            np.testing.assert_array_equal(integer.parameters['stem.conv'][field], original.parameters['stem.conv'][field])
        return dict(status='completed_frozen_stem_qat_G10', saved_updates=10,
                    checkpoint_sha256=event['checkpoint_sha256'], all_saved_Stem_states_and_codes_unchanged=True)

    options = SimpleNamespace(receipt=folder / 'segment.json', output=RUN,
                              gpu_uuid=base.GPU, preflight_timeout_seconds=180)
    started = time.perf_counter()
    result = base.run_protected(command, options, expected_ready=dict(
        dataset_sha256=identity['dataset_sha256'], dataset_content_sha256=identity['dataset_content_sha256'],
        identity_sha256=protocol_hash(identity), resume=None), completion_validator=complete)
    result.update(seconds=time.perf_counter() - started, formal_acceptance=False,
        original_checkpoint_unchanged=sha256(base.CHECKPOINT) == base.CHECKPOINT_HASH,
        sources_unchanged=all(sha256(base.PROJECT / name) == digest for name, digest in identity['source_sha256'].items()))
    base.save(folder / 'report.json', result)
    print(json.dumps(result), flush=True)
    if result['status'] != 'completed_frozen_stem_qat_G10':
        raise RuntimeError('control stopped; no automatic retry')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'execute', 'worker'))
    parser.add_argument('--pause-request', type=Path)
    parser.add_argument('--supervised-start', action='store_true')
    parser.add_argument('--resume', type=Path)
    args = parser.parse_args()
    install()
    if args.action == 'check':
        OUT.mkdir(exist_ok=True)
        receipt = OUT / 'cache_receipt.json'
        if not receipt.exists():
            shutil.copyfile(PREVIOUS / 'cache_receipt.json', receipt)
        if sha256(receipt) != sha256(PREVIOUS / 'cache_receipt.json'):
            raise ValueError('shared cache receipt changed')
        base.cpu_check()
    elif args.action == 'execute':
        execute()
    else:
        base.worker(args)


if __name__ == '__main__':
    main()
