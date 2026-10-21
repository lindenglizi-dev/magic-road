"""Validate M0 hand-authored trajectory fixtures; no game or physics execution."""

import argparse
import hashlib
import json
import math
from pathlib import Path


SCHEMA = 'minecraft-m0-v1'
STATE_ORDER = ['x', 'z', 'vx', 'vz']
ACTION_ORDER = ['forward', 'back', 'left', 'right', 'idle']
PROVENANCE = {
    'source_kind': 'hand_authored',
    'game_captured': False,
    'physics_validated': False,
    'clock': 'synthetic_tick',
    'server_tick': None,
    'velocity_semantics': 'hand_authored_boundary_value',
    'image_source': 'none',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, names, label):
    require(type(value) is dict, f'{label}: expected an object')
    require(set(value) == set(names), f'{label}: expected fields {", ".join(names)}')


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def vector(value, size, label):
    require(type(value) is list and len(value) == size,
            f'{label}: expected {size} values')
    require(all(finite_number(v) for v in value), f'{label}: expected finite numbers')


def rectangle(value, label):
    vector(value, 4, label)
    require(value[0] < value[2] and value[1] < value[3],
            f'{label}: expected xmin < xmax and zmin < zmax')


def legal_position(position, task):
    x, z = position
    xmin, zmin, xmax, zmax = task['center_bounds']
    return (xmin <= x <= xmax and zmin <= z <= zmax
            and not any(left < x < right and top < z < bottom
                        for left, top, right, bottom in task['center_obstacles']))


def validate_episode(item):
    fields(item, ('schema_version', 'episode_id', 'split', 'provenance', 'units',
                  'state_order', 'action_order', 'task', 'states', 'actions',
                  'terminated', 'truncated'), 'episode')
    require(item['schema_version'] == SCHEMA, 'schema_version: unsupported schema')
    require(type(item['episode_id']) is str and bool(item['episode_id'].strip()),
            'episode_id: expected nonempty text')
    require(item['split'] == 'example', 'split: M0 fixtures must be example, not training data')
    fields(item['provenance'], PROVENANCE, 'provenance')
    for name, expected in PROVENANCE.items():
        value = item['provenance'][name]
        require(type(value) is type(expected) and value == expected,
                f'provenance.{name}: M0 requires {expected!r}')
    require(item['units'] == {'position': 'block', 'velocity': 'block_per_recorded_tick',
                              'normalization': 'none'}, 'units: unsupported or missing units')
    require(item['state_order'] == STATE_ORDER, 'state_order: expected x,z,vx,vz')
    require(item['action_order'] == ACTION_ORDER, 'action_order: unsupported action encoding')

    task = item['task']
    fields(task, ('scene_id', 'center_bounds', 'center_obstacles', 'goal', 'goal_radius',
                  'fixed_yaw_radians', 'ground', 'action_ticks', 'max_actions'), 'task')
    require(type(task['scene_id']) is str and bool(task['scene_id'].strip()),
            'task.scene_id: expected nonempty text')
    rectangle(task['center_bounds'], 'task.center_bounds')
    require(type(task['center_obstacles']) is list, 'task.center_obstacles: expected a list')
    for index, obstacle in enumerate(task['center_obstacles']):
        rectangle(obstacle, f'task.center_obstacles[{index}]')
        require(all(legal_position(point, {**task, 'center_obstacles': []})
                    for point in (obstacle[:2], obstacle[2:])),
                f'task.center_obstacles[{index}]: outside center bounds')
    vector(task['goal'], 2, 'task.goal')
    require(legal_position(task['goal'], task), 'task.goal: outside allowed center region')
    require(finite_number(task['goal_radius']) and task['goal_radius'] > 0,
            'task.goal_radius: expected a positive finite number')
    require(finite_number(task['fixed_yaw_radians']), 'task.fixed_yaw_radians: expected a finite number')
    require(task['ground'] == 'uniform_dry_flat', 'task.ground: unsupported scene condition')
    for name in ('action_ticks', 'max_actions'):
        require(type(task[name]) is int and task[name] > 0, f'task.{name}: expected a positive integer')

    states, actions = item['states'], item['actions']
    require(type(states) is list and type(actions) is list, 'states/actions: expected lists')
    count = len(actions)
    require(1 <= count <= task['max_actions'], 'actions: expected 1..max_actions segments')
    require(len(states) == count + 1, 'states/actions: N actions require N+1 states')
    reached = []
    for index, state in enumerate(states):
        label = f'states[{index}]'
        fields(state, ('tick', 'value'), label)
        require(type(state['tick']) is int and state['tick'] >= 0,
                f'{label}.tick: expected a nonnegative integer')
        require(state['tick'] == index * task['action_ticks'],
                f'{label}.tick: expected contiguous fixed intervals starting at zero')
        vector(state['value'], 4, f'{label}.value')
        require(legal_position(state['value'][:2], task), f'{label}: outside allowed center region')
        distance = math.dist(state['value'][:2], task['goal'])
        reached.append(distance <= task['goal_radius'])
    require(not any(reached[:-1]), 'goal: initial success or actions after first arrival are unsupported')

    for index, action in enumerate(actions):
        label = f'actions[{index}]'
        fields(action, ('start_tick', 'end_tick', 'control', 'collision'), label)
        require(type(action['start_tick']) is int and type(action['end_tick']) is int,
                f'{label}: start/end tick must be integers')
        require(action['start_tick'] == states[index]['tick']
                and action['end_tick'] == states[index + 1]['tick'],
                f'{label}: interval must match states[i] and states[i+1]')
        require(action['control'] in ACTION_ORDER, f'{label}.control: unsupported action')
        # ponytail: collision is a declared interval label; validate contact using game evidence in M1.
        require(type(action['collision']) is bool, f'{label}.collision: expected a boolean')

    require(type(item['terminated']) is bool and type(item['truncated']) is bool,
            'termination: expected boolean flags')
    require(item['terminated'] == reached[-1], 'terminated: must match final goal arrival')
    require(reached[-1] or count == task['max_actions'], 'termination: incomplete episode before timeout')
    require(item['truncated'] == (not reached[-1]), 'truncated: true only for timeout without goal')
    return {'episode_id': item['episode_id'], 'schema_version': SCHEMA,
            'source_kind': 'hand_authored', 'game_captured': False, 'physics_validated': False,
            'states': len(states), 'actions': count, 'duration_ticks': states[-1]['tick'],
            'collision_segments': sum(action['collision'] for action in actions),
            'end_reason': 'goal' if reached[-1] else 'timeout'}


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        require(name not in result, f'JSON: duplicate field {name!r}')
        result[name] = value
    return result


def reject_constant(value):
    raise ValueError(f'JSON: non-finite literal {value}')


def validate_file(path):
    content = Path(path).read_bytes()
    item = json.loads(content.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)
    return {**validate_episode(item), 'sha256': hashlib.sha256(content).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='M0 hand-authored episode JSON')
    args = parser.parse_args()
    try:
        result = validate_file(args.path)
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        parser.exit(1, f'INVALID {args.path}: {error}\n')
    print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
