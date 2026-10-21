"""Small P2 checks; no formal training run, board or file deletion."""

import copy
import json
from pathlib import Path
import shutil
import tempfile

import numpy as np
import torch
from torch import nn

from tabletop import build_dataset, file_hash, write_json
from visual_predictor import (HORIZON, VisualPredictor, Windows, dataset_path,
                              evaluate_model, load_data, masked_loss, train)


def rejects(exception, callback, text=''):
    try:
        callback()
    except exception as error:
        assert text in str(error), str(error)
        return
    raise AssertionError(f'Expected {exception.__name__}')


def main():
    torch.set_num_threads(1)
    torch.manual_seed(7)
    n = 10
    item = {
        'episode_id': 'test-indexed',
        'images': np.stack([np.full((64, 64, 3), i, dtype=np.uint8) for i in range(n + 1)]),
        'states': np.asarray([[i / 20, i / 30, i / 100, -i / 100] for i in range(n + 1)], dtype=np.float32),
        'actions': np.asarray([[i / 20, -i / 20] for i in range(n)], dtype=np.float32),
        'collisions': [i == 4 for i in range(n)],
    }
    windows = Windows([item])
    assert windows.origins == [(0, i) for i in range(1, n)]
    first, last = windows[0], windows[len(windows) - 1]
    assert first['images'].shape == (6, 64, 64)
    assert torch.all(first['images'][:3] == 0)
    torch.testing.assert_close(first['images'][3:], torch.full((3, 64, 64), 1 / 255))
    np.testing.assert_array_equal(first['actions'].numpy(), item['actions'][1:9])
    np.testing.assert_array_equal(first['targets'].numpy(), item['states'][2:10])
    np.testing.assert_array_equal(first['truth_initial'].numpy(), item['states'][1])
    assert first['mask'].sum() == HORIZON and last['mask'].sum() == 1
    np.testing.assert_array_equal(last['targets'][0].numpy(), item['states'][n])
    assert torch.count_nonzero(last['actions'][1:]) == 0
    assert torch.count_nonzero(last['targets'][1:]) == 0
    rejects(ValueError, lambda: Windows([]))

    model = VisualPredictor()
    images, actions = first['images'][None], first['actions'][None]
    initial, future = model(images, actions)
    assert initial.shape == (1, 4) and future.shape == (1, HORIZON, 4)
    assert torch.isfinite(initial).all() and torch.isfinite(future).all()
    loss = ((initial - first['truth_initial'][None]) ** 2).mean()
    loss += masked_loss(future, first['targets'][None], first['mask'][None])
    loss.backward()
    assert any(p.grad is not None and torch.count_nonzero(p.grad) for p in model.encoder.parameters())
    assert any(p.grad is not None and torch.count_nonzero(p.grad) for p in model.dynamics.parameters())
    model.eval()
    with torch.no_grad():
        expected = model(images, actions)
        repeated = model(images, actions)
    for a, b in zip(expected, repeated):
        torch.testing.assert_close(a, b, rtol=0, atol=0)
    changed = copy.deepcopy(item)
    changed['states'][2:] += 100
    altered = Windows([changed])[0]
    assert not torch.equal(altered['targets'], first['targets'])
    with torch.no_grad():
        actual = model(altered['images'][None], altered['actions'][None])
    for a, b in zip(expected, actual):
        torch.testing.assert_close(a, b, rtol=0, atol=0)
    rejects(ValueError, lambda: model.encode(torch.zeros(1, 3, 64, 64)))
    rejects(ValueError, lambda: model.rollout(initial, torch.zeros(1, 0, 2)))

    report = evaluate_model(model, windows)
    names = {'visual_learned', 'truth_initial_learned'} | {
        f'{source}_{method}' for source in ('visual', 'truth_initial')
        for method in ('state_hold', 'constant_velocity', 'action_prior_no_collision')}
    assert set(report['metrics']) == names and len(names) == 8
    expected_ids = {f'test-indexed:{t}:H{h}' for t in range(1, n) for h in (1, 4, 8) if t + h <= n}
    assert {r['window_id'] for r in report['window_records']} == expected_ids
    assert len(report['window_records']) == len(expected_ids)
    assert all(set(r['squared_position_error']) == names for r in report['window_records'])
    for h in (1, 4, 8):
        assert {report['metrics'][name][str(h)]['windows'] for name in names} == {n - h}

    # Replace dynamics with a known recurrence: each prediction must feed the next.
    recurrence = VisualPredictor()
    recurrence.dynamics = nn.Linear(6, 4, bias=False)
    with torch.no_grad():
        recurrence.dynamics.weight.zero_()
        recurrence.dynamics.weight[:, :4].copy_(torch.eye(4) * 0.5)
        recurrence.dynamics.weight[0, 4] = 1
        recurrence.dynamics.weight[1, 5] = 1
        state = torch.tensor([[0.2, 0.3, 0.1, -0.1]])
        controls = torch.tensor([[[1., 0.], [0., -1.], [-1., 1.]]])
        result = recurrence.rollout(state, controls)
        for i, action in enumerate(controls.unbind(1)):
            state = state * 1.05 + torch.cat((action * 0.1, torch.zeros(1, 2)), dim=1)
            torch.testing.assert_close(result[:, i], state)

    runs = Path(__file__).resolve().parents[1] / 'artifacts' / 'test-runs'
    runs.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='visual-', dir=runs))
    checkpoint = temporary / 'checkpoint.pt'
    torch.save({'state_dict': model.state_dict()}, checkpoint)
    restored = VisualPredictor().eval()
    restored.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True)['state_dict'])
    with torch.no_grad():
        actual = restored(images, actions)
    for a, b in zip(expected, actual):
        torch.testing.assert_close(a, b, rtol=0, atol=0)

    data = temporary / 'data'
    build_dataset(data, seed=19, counts=(1, 1, 1), steps=12)
    loaded = load_data(data)
    assert set(loaded) == {'train', 'val', 'test'} and all(len(items) == 1 for items in loaded.values())
    rejects(ValueError, lambda: dataset_path(data, '../escape.json'), 'inside')

    for case in ('escape', 'missing_frame', 'frame_hash', 'episode_hash'):
        bad = temporary / case
        shutil.copytree(data, bad)
        manifest = json.loads((bad / 'manifest.json').read_text(encoding='utf-8'))
        entry = manifest['episodes'][0]
        if case == 'escape':
            entry['path'] = '../escape.json'
        elif case == 'episode_hash':
            entry['sha256'] = '0' * 64
        else:
            episode_path = bad / entry['path']
            episode = json.loads(episode_path.read_text(encoding='utf-8'))
            if case == 'missing_frame':
                episode['frames'][0] = 'frames/not-present.png'
            else:
                episode['frame_sha256'][0] = '0' * 64
            write_json(episode_path, episode)
            entry['sha256'] = file_hash(episode_path)
        write_json(bad / 'manifest.json', manifest)
        rejects(FileNotFoundError if case == 'missing_frame' else ValueError, lambda: load_data(bad))

    occupied = temporary / 'occupied'
    occupied.mkdir()
    sentinel = occupied / 'keep.txt'
    sentinel.write_text('preserve me', encoding='utf-8')
    rejects(FileExistsError, lambda: train(data, occupied, epochs=1))
    assert sentinel.read_text(encoding='utf-8') == 'preserve me'
    rejects(ValueError, lambda: train(data, temporary / 'invalid', epochs=0))
    print('PASS: window alignment, gradients, checkpoint, deterministic eval, identical comparison windows, no future-state feedback, recurrent rollout and dataset/output validation')


if __name__ == '__main__':
    main()
