"""Run with python software/test_tabletop.py; no board or training required."""

import hashlib
import json
from contextlib import nullcontext
from pathlib import Path
import random
import tempfile

from PIL import Image

from tabletop import (PHYSICS, background, build_dataset, episode, file_hash,
                      predict, reached_goal, render, step, valid_state)


def rejects(exception, callback):
    try:
        callback()
    except exception:
        return
    raise AssertionError(f'Expected {exception.__name__}')


def main():
    rejects(ValueError, lambda: step((0.1, 0.1, 0, 0), (float('nan'), 0)))
    rejects(ValueError, lambda: step((0.1, 0.1, 0, 0), (1.01, 0)))
    rejects(ValueError, lambda: step((0.5, 0.5, 0, 0), (0, 0)))
    state, hit = step((0.395, 0.5, 0.5, 0), (1, 0))
    assert hit and abs(state[0] - 0.4) < 1e-12 and state[2] == 0
    state, hit = step((0.62, 0.5, -0.5, 0), (-1, 0))
    assert hit and abs(state[0] - 0.6) < 1e-12 and state[2] == 0
    state, hit = step((0.5, 0.27, 0, 0.5), (0, 1))
    assert hit and abs(state[1] - 0.28) < 1e-12 and state[3] == 0
    state, hit = step((0.5, 0.73, 0, -0.5), (0, -1))
    assert hit and abs(state[1] - 0.72) < 1e-12 and state[3] == 0
    state, hit = step((0.05, 0.05, -0.5, -0.5), (-1, -1))
    assert hit and state == (0.04, 0.04, 0.0, 0.0)
    for corner in ((0.39, 0.27, 0.5, 0.5), (0.61, 0.73, -0.5, -0.5)):
        result, _ = step(corner, (0, 0))
        assert valid_state(result)
    state, _ = step((0.76, 0.5, 0.2, 0), (1, 0))
    assert reached_goal(state)
    state, _ = step((0.1, 0.1, 0.2, 0), (0, 0))
    assert abs(state[2] - 0.18) < 1e-12, 'Zero action is not a brake'

    rng = random.Random(7)
    for seed in range(50):
        item = episode('test', seed, seed, 100)
        assert len(item['states']) == len(item['actions']) + 1
        assert len(item['actions']) == len(item['collisions'])
        assert all(valid_state(s) for s in item['states'])
        assert not any(reached_goal(s) for s in item['states'][:-1])
        for i, action in enumerate(item['actions']):
            result, hit = step(item['states'][i], action)
            assert list(result) == item['states'][i + 1] and hit == item['collisions'][i]
        assert item['terminated'] == reached_goal(item['states'][-1])
        assert item == episode('test', seed, seed, 100)
        assert item['states'] != episode('test', seed, seed + 1000, 100)['states']
    for _ in range(1000):
        state = (rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95),
                 rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5))
        if valid_state(state):
            result, _ = step(state, (rng.uniform(-1, 1), rng.uniform(-1, 1)))
            assert valid_state(result), (state, result)

    start = (0.1, 0.1, 0, 0)
    actions = [(1, 0)] * 3
    assert predict(start, actions, 'state_hold') == [start] * 3
    assert predict(start, actions, 'constant_velocity') == [start] * 3
    truth = start
    for action in actions:
        truth, _ = step(truth, action)
    assert predict(start, actions, 'action_prior_no_collision')[-1] == truth
    assert predict(start, [(-1, 0)] * 3, 'action_prior_no_collision')[-1][0] < start[0]
    rejects(ValueError, lambda: predict(start, actions, 'unknown'))

    test_root = Path(__file__).resolve().parents[1] / 'artifacts' / 'test-runs'
    test_root.mkdir(parents=True, exist_ok=True)
    # Keep run evidence in the ignored workspace directory; no recursive cleanup.
    with nullcontext(tempfile.mkdtemp(prefix='tabletop-', dir=test_root)) as temporary:
        out, again = Path(temporary) / 'run', Path(temporary) / 'again'
        manifest, report = build_dataset(out, seed=7, counts=(2, 2, 3), steps=12)
        repeated, repeated_report = build_dataset(again, seed=7, counts=(2, 2, 3), steps=12)
        assert manifest == repeated and report == repeated_report
        assert file_hash(out / 'preview.png') == file_hash(again / 'preview.png')
        seeds, assets, hashes = set(), set(), set()
        for entry in manifest['episodes']:
            assert entry['seed'] not in seeds and entry['asset_id'] not in assets
            assert entry['sha256'] not in hashes
            seeds.add(entry['seed']); assets.add(entry['asset_id']); hashes.add(entry['sha256'])
            path = out / entry['path']
            assert file_hash(path) == entry['sha256']
            item = json.loads(path.read_text(encoding='utf-8'))
            assert len(item['frames']) == len(item['states']) == len(item['frame_sha256'])
            for state, frame, digest in zip(item['states'], item['frames'], item['frame_sha256']):
                image_path = out / frame
                assert file_hash(image_path) == digest
                with Image.open(image_path) as image:
                    assert image.size == (64, 64) and image.mode == 'RGB'
                    expected = render(state, background(item['asset_seed']))
                    assert hashlib.sha256(image.tobytes()).digest() == hashlib.sha256(expected.tobytes()).digest()
        for method in report['metrics'].values():
            assert method['8']['windows'] > 0
        assert report['learned_model_status'] == 'not trained' and not report['nano_banana_used']
        assert report['hardware_workloads'][0]['macs_for_16_candidates_8_steps'] == 802816
        before = file_hash(out / 'manifest.json')
        rejects(FileExistsError, lambda: build_dataset(out))
        assert file_hash(out / 'manifest.json') == before, 'Refusing overwrite must preserve existing output'
        rejects(ValueError, lambda: build_dataset(Path(temporary) / 'bad', steps=7))
        rejects(ValueError, lambda: build_dataset(Path(temporary) / 'bad', counts=(0, 1, 1)))
    print('PASS: dynamics, collisions, termination, deterministic data/images, split isolation, open-loop baselines and overwrite protection')


if __name__ == '__main__':
    main()
