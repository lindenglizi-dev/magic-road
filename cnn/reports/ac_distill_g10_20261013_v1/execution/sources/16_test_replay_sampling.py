"""CPU-only replay coverage, rejection, gradient exposure and exact-resume checks."""
import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import torch

from . import train
from .replay_sampling import ReplayWindow
from .test_finetune_schedule import _TinyModel, _TinyLoss, _same, _fails


class Pool(torch.utils.data.Dataset):
    def __init__(self, split):
        self.rows = [dict(sampling_group='new' if i < 22 else 'replay')
                     for i in range(44 if split == 'train' else 2)]

    def __len__(self):
        return len(self.rows)

    def set_epoch(self, epoch, mosaic=None):
        assert mosaic is False

    def __getitem__(self, index):
        return torch.full((1, 2, 2), (index + 1) / 50.), {}, str(index)


def schedule():
    return dict(kind='balanced_replay_11_plus_11_v1',
                orders=[list(range(11)) + list(range(22, 33)),
                        list(range(11, 22)) + list(range(33, 44))])


def args(manifest, output, stop=0):
    return train.build_parser().parse_args([
        '--dataset', str(manifest), '--output', str(output), '--device', 'cpu',
        '--workers', '0', '--epochs', '2', '--batch-size', '8', '--accum-steps', '8',
        '--lr', '0.0001', '--lr-schedule', 'finetune_constant', '--freeze-bn',
        '--no-mosaic', '--no-amp', '--stop-after-epoch', str(stop),
        '--checkpoint-every-seconds', '0'])


def main():
    torch.set_num_threads(1)
    frozen = schedule()
    wrapped = ReplayWindow(Pool('train'), frozen, 2)
    exposed = []
    for epoch, order in enumerate(frozen['orders']):
        wrapped.set_epoch(epoch, mosaic=False)
        actual = [int(wrapped[i][2]) for i in range(len(wrapped))]
        assert actual == order and sum(i < 22 for i in actual) == 11
        exposed.extend(actual)
    assert sorted(exposed) == list(range(44))
    # Caller mutation cannot change an already validated window.
    frozen['orders'][0][0] = 43
    assert wrapped.orders[0][0] == 0
    _fails(lambda: wrapped.set_epoch(2))
    _fails(lambda: wrapped.set_epoch(0, mosaic=True))
    for kind in ('duplicate', 'range', 'domain', 'length', 'boolean', 'coverage'):
        bad = schedule()
        if kind == 'duplicate': bad['orders'][0][0] = 1
        if kind == 'range': bad['orders'][0][0] = 44
        if kind == 'domain': bad['orders'][0][0] = 43
        if kind == 'length': bad['orders'].pop()
        if kind == 'boolean': bad['orders'][0][0] = False
        if kind == 'coverage': bad['orders'][1] = bad['orders'][0].copy()
        _fails(lambda: ReplayWindow(Pool('train'), bad, 2))
    assert [train.accumulation_group_samples(i, 3, 8, 8, 22) for i in range(3)] == [22]*3
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root/'dataset.json'
        manifest.write_text('{}', encoding='utf-8')
        payload = dict(replay_sampling=schedule())
        rows = [dict(image='tiny', image_sha256='0'*64)]
        with (patch.object(train, 'load_dataset_manifest', return_value=(payload, rows)),
              patch.object(train, 'make_frame_dataset',
                           side_effect=lambda _rows, split, *_a, **_kw: Pool(split)),
              patch.object(train, 'RoadYOLOS4', _TinyModel),
              patch.object(train, 'YOLOXLoss', _TinyLoss),
              patch.object(torch.cuda, 'is_available', return_value=False),
              redirect_stdout(io.StringIO())):
            continuous = args(manifest, root/'continuous')
            assert train.train(continuous) == 0
            segmented = args(manifest, root/'segmented', 1)
            assert train.train(segmented) == 0
            segmented.resume = segmented.output/'last_resume.pt'
            segmented.stop_after_epoch = 0
            swapped = copy.deepcopy(payload)
            swapped['replay_sampling']['orders'].reverse()
            with patch.object(train, 'load_dataset_manifest', return_value=(swapped, rows)):
                _fails(lambda: train.train(segmented))
            assert train.train(segmented) == 0
        first = torch.load(continuous.output/'last.pt', map_location='cpu', weights_only=False)
        second = torch.load(segmented.output/'last.pt', map_location='cpu', weights_only=False)
        for field in ('model', 'optimizer', 'scaler', 'rng_state'):
            _same(first[field], second[field])
        assert first['trained_steps'] == second['trained_steps'] == 2
        assert first['last_optimizer_effective_batch'] == 22
        assert first['training_protocol']['replay_sampling_sha256'] == wrapped.sampling_sha256
        for output in (continuous.output, segmented.output):
            events = [json.loads(line) for line in (output/'train_log.jsonl').read_text().splitlines()]
            assert len([e for e in events if e['event'] == 'step']) == 2
    print('PASS replay11+11 coverage/rejections, true batch22, protocol binding and exact CPU resume')


if __name__ == '__main__':
    main()
