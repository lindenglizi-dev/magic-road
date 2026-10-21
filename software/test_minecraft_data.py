"""M0 format checks only: no Minecraft execution or physics validation."""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from minecraft_data import validate_episode, validate_file


def rejects(exception, callback):
    try:
        callback()
    except exception:
        return
    raise AssertionError(f'Expected {exception!r}')


def changed(item, path, value):
    result = copy.deepcopy(item)
    target = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return result


def main():
    root = Path(__file__).resolve().parents[1]
    sample = root / 'examples' / 'minecraft-offline.json'
    item = json.loads(sample.read_text(encoding='utf-8'))
    report = validate_file(sample)
    assert report['end_reason'] == 'goal'
    assert report['states'] == report['actions'] + 1 == 4
    assert report['duration_ticks'] == 12
    assert report['sha256'] == hashlib.sha256(sample.read_bytes()).hexdigest()
    assert report['source_kind'] == 'hand_authored'
    assert not report['game_captured'] and not report['physics_validated']

    timeout = changed(item, ('states', -1, 'value'), [2.5, 1, 0, 0])
    timeout['task']['max_actions'] = len(timeout['actions'])
    timeout['terminated'], timeout['truncated'] = False, True
    assert validate_episode(timeout)['end_reason'] == 'timeout'
    at_limit = copy.deepcopy(item)
    at_limit['task']['max_actions'] = len(at_limit['actions'])
    at_limit['states'][-1]['value'][0] = 2.75
    assert validate_episode(at_limit)['end_reason'] == 'goal', 'Goal wins at the action limit'

    contact = changed(item, ('states', 0, 'value'), [0, 0, 0, 0])
    contact['states'][1]['value'] = [2, 3.5, 0, 0]
    contact['actions'][0]['collision'] = True
    assert validate_episode(contact)['collision_segments'] == 1
    # M0 checks declared values; it deliberately does not infer velocity or collision physics.
    assert validate_episode(changed(item, ('states', 1, 'value', 2), 100))['source_kind'] == 'hand_authored'

    huge = copy.deepcopy(item)
    n = 10 ** 308
    huge['task'].update(center_bounds=[-n, -1, n, 1], center_obstacles=[],
                        goal=[n, 0], goal_radius=1, max_actions=1)
    huge['states'] = [{'tick': 0, 'value': [-n, 0, 0, 0]},
                      {'tick': 4, 'value': [n, 0, 0, 0]}]
    huge['actions'] = [copy.deepcopy(item['actions'][0])]
    assert validate_episode(huge)['end_reason'] == 'goal'
    beyond_float = changed(huge, ('states', 0, 'value', 0), -(10 ** 400))
    rejects(ValueError, lambda: validate_episode(beyond_float))

    invalid = [
        (('states',), item['states'][:-1]),
        (('actions',), []),
        (('states', 0, 'tick'), 1),
        (('states', 1, 'tick'), 8),
        (('states', 1, 'tick'), 3),
        (('states', 1, 'tick'), 0),
        (('states', 1, 'tick'), True),
        (('actions', 0, 'end_tick'), 0),
        (('actions', 0, 'start_tick'), False),
        (('actions', 1, 'start_tick'), 5),
        (('actions', 1, 'start_tick'), 3),
        (('actions', 1, 'end_tick'), 4),
        (('actions', 0, 'control'), 'jump'),
        (('actions', 0, 'control'), ['right']),
        (('actions', 0, 'collision'), 1),
        (('states', 0, 'value', 0), True),
        (('states', 0, 'value', 2), float('nan')),
        (('states', 0, 'value', 3), float('inf')),
        (('states', 0, 'value', 3), float('-inf')),
        (('states', 0, 'value', 0), -0.01),
        (('states', 0, 'value', 1), 8.01),
        (('states', 0, 'value'), [3, 3.5, 0, 0]),
        (('states', 0, 'value'), [3, 1, 0, 0]),
        (('states', 1, 'value'), [3, 1, 0, 0]),
        (('terminated',), False),
        (('terminated',), 1),
        (('truncated',), True),
        (('truncated',), 0),
        (('task', 'action_ticks'), True),
        (('task', 'max_actions'), True),
        (('task', 'max_actions'), 2),
        (('task', 'goal_radius'), True),
        (('task', 'goal_radius'), 0),
        (('task', 'goal'), [3, 3.5]),
        (('task', 'fixed_yaw_radians'), float('nan')),
        (('task', 'center_bounds'), [0, 0, 0, 8]),
        (('units', 'velocity'), 'unknown'),
        (('split',), 'train'),
        (('provenance', 'source_kind'), 'game_capture'),
        (('provenance', 'game_captured'), True),
        (('provenance', 'game_captured'), 0),
        (('provenance', 'physics_validated'), True),
        (('provenance', 'clock'), 'server_tick'),
        (('provenance', 'clock'), 'mineflayer.physicsTick'),
        (('provenance', 'server_tick'), 12),
        (('provenance', 'velocity_semantics'), 'server_authoritative'),
        (('provenance', 'image_source'), 'minecraft_client'),
    ]
    for path, value in invalid:
        rejects(ValueError, lambda path=path, value=value: validate_episode(changed(item, path, value)))
    incomplete = copy.deepcopy(timeout)
    incomplete['task']['max_actions'] += 1
    rejects(ValueError, lambda: validate_episode(incomplete))
    rejects(ValueError, lambda: validate_episode(changed(timeout, ('truncated',), False)))
    rejects(ValueError, lambda: validate_episode({**item, 'extra': None}))
    rejects(ValueError, lambda: validate_episode([]))

    runs = root / 'artifacts' / 'test-runs'
    runs.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='minecraft-m0-', dir=runs))
    document = json.dumps(item)
    failures = {
        'duplicate.json': document.replace('"schema_version":', '"schema_version": "duplicate", "schema_version":', 1).encode(),
        'nested-duplicate.json': document.replace('"collision": false', '"collision": false, "collision": true', 1).encode(),
        'nan.json': json.dumps(changed(item, ('states', 0, 'value', 2), float('nan'))).encode(),
        'infinity.json': json.dumps(changed(item, ('states', 0, 'value', 2), float('inf'))).encode(),
        'invalid-utf8.json': b'\xff',
        'malformed.json': b'{',
        'invalid-episode.json': json.dumps(changed(item, ('terminated',), False)).encode(),
        'beyond-float.json': json.dumps(beyond_float).encode(),
    }
    checker = root / 'software' / 'minecraft_data.py'
    huge_path = out / 'finite-huge.json'
    huge_path.write_text(json.dumps(huge), encoding='utf-8')
    surrogate_path = out / 'escaped-surrogate.json'
    surrogate_path.write_text(json.dumps(changed(item, ('episode_id',), '\ud800')), encoding='utf-8')
    for valid_path in (sample, huge_path, surrogate_path):
        success = subprocess.run([sys.executable, '-S', str(checker), str(valid_path)], capture_output=True, text=True, timeout=20)
        assert success.returncode == 0 and not success.stderr, success.stderr
        assert success.stdout.isascii(), 'JSON output must survive strict stdout encodings'
        assert json.loads(success.stdout) == validate_file(valid_path)
    for name, content in failures.items():
        path = out / name
        path.write_bytes(content)
        rejects((ValueError, UnicodeError), lambda path=path: validate_file(path))
        failure = subprocess.run([sys.executable, '-S', str(checker), str(path)], capture_output=True, text=True, timeout=20)
        assert failure.returncode == 1 and failure.stderr.startswith('INVALID '), failure
        assert not failure.stdout and 'Traceback' not in failure.stderr
    missing = subprocess.run([sys.executable, '-S', str(checker), str(out / 'missing.json')], capture_output=True, text=True, timeout=20)
    assert missing.returncode == 1 and missing.stderr.startswith('INVALID ')
    print('PASS: M0 goal/timeout, boundary contact, alignment, finite values, provenance, strict JSON/UTF-8 and real CLI exits; no game or physics evidence')


if __name__ == '__main__':
    main()
