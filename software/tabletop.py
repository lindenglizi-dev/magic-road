"""Reproducible tabletop data and analytic baselines; no learned model yet."""

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageDraw


@dataclass(frozen=True)
class Physics:
    dt: float = 0.1
    acceleration: float = 2.0
    drag: float = 0.9
    max_speed: float = 0.5
    half_size: float = 0.04
    obstacle: tuple = (0.44, 0.32, 0.56, 0.68)
    goal: tuple = (0.84, 0.5)
    goal_radius: float = 0.07


PHYSICS = Physics()
IMAGE_SIZE = 64


def valid_state(state, physics=PHYSICS):
    x, y, vx, vy = state
    half = physics.half_size
    left, top, right, bottom = physics.obstacle
    return (all(math.isfinite(v) for v in state)
            and half <= x <= 1 - half and half <= y <= 1 - half
            and abs(vx) <= physics.max_speed and abs(vy) <= physics.max_speed
            and not (left - half < x < right + half
                     and top - half < y < bottom + half))


def reached_goal(state, physics=PHYSICS):
    return math.hypot(state[0] - physics.goal[0], state[1] - physics.goal[1]) <= physics.goal_radius


def free_step(state, action, physics=PHYSICS):
    """Known-parameter motion prior, without walls or obstacle collisions."""
    x, y, vx, vy = state
    ax, ay = action
    vx = max(-physics.max_speed, min(physics.max_speed, physics.drag * vx + physics.acceleration * ax * physics.dt))
    vy = max(-physics.max_speed, min(physics.max_speed, physics.drag * vy + physics.acceleration * ay * physics.dt))
    return (x + vx * physics.dt, y + vy * physics.dt, vx, vy)


def step(state, action, physics=PHYSICS):
    if len(state) != 4 or not valid_state(state, physics):
        raise ValueError('State must be finite, collision-free and within supported bounds.')
    if len(action) != 2 or not all(math.isfinite(v) and -1 <= v <= 1 for v in action):
        raise ValueError('Action must have two finite acceleration controls in [-1, 1].')
    x, y, _, _ = state
    nx, ny, vx, vy = free_step(state, action, physics)
    half = physics.half_size
    left, top, right, bottom = physics.obstacle
    left, top, right, bottom = left - half, top - half, right + half, bottom + half
    collision = False
    if nx < half or nx > 1 - half:
        nx = max(half, min(1 - half, nx)); vx = 0.0; collision = True
    # ponytail: axis-separated square collision; use a continuous rigid-body solver for rotation or contact forces.
    if top < y < bottom:
        if x <= left < nx:
            nx = left; vx = 0.0; collision = True
        elif nx < right <= x:
            nx = right; vx = 0.0; collision = True
    if ny < half or ny > 1 - half:
        ny = max(half, min(1 - half, ny)); vy = 0.0; collision = True
    if left < nx < right:
        if y <= top < ny:
            ny = top; vy = 0.0; collision = True
        elif ny < bottom <= y:
            ny = bottom; vy = 0.0; collision = True
    return (nx, ny, vx, vy), collision


def initial_state(rng):
    for _ in range(10000):
        state = (rng.uniform(0.08, 0.92), rng.uniform(0.08, 0.92),
                 rng.uniform(-0.15, 0.15), rng.uniform(-0.15, 0.15))
        if valid_state(state) and not reached_goal(state):
            return state
    raise RuntimeError('Could not sample a free initial state.')


def background(seed):
    rng = random.Random(seed)
    color = tuple(rng.randrange(205, 246) for _ in range(3))
    image = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color)
    draw = ImageDraw.Draw(image)
    for _ in range(16):
        x, y = rng.randrange(IMAGE_SIZE), rng.randrange(IMAGE_SIZE)
        draw.line((x, y, min(x + rng.randrange(2, 12), IMAGE_SIZE - 1), y),
                  fill=tuple(max(0, c - 15) for c in color))
    return image


def render(state, backdrop, physics=PHYSICS):
    image = backdrop.copy()
    draw = ImageDraw.Draw(image)
    scale = IMAGE_SIZE - 1
    gx, gy = physics.goal
    radius = physics.goal_radius
    draw.ellipse(tuple(v * scale for v in (gx - radius, gy - radius, gx + radius, gy + radius)),
                 outline=(30, 120, 65), width=2)
    draw.rectangle(tuple(v * scale for v in physics.obstacle), fill=(65, 70, 85))
    x, y = state[:2]
    half = physics.half_size
    draw.rectangle(tuple(v * scale for v in (x - half, y - half, x + half, y + half)),
                   fill=(200, 45, 50))
    return image


def episode(split, index, seed, steps):
    rng = random.Random(seed)
    state = initial_state(rng)
    states, actions, collisions = [list(state)], [], []
    for _ in range(steps):
        # Some goal-directed pushes provide useful trajectories, mixed with random exploration.
        if rng.random() < 0.4:
            action = [max(-1.0, min(1.0, (g - p) * 4)) for g, p in zip(PHYSICS.goal, state[:2])]
        else:
            action = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        state, collision = step(state, action)
        actions.append(action); states.append(list(state)); collisions.append(collision)
        if reached_goal(state):
            break
    return {'episode_id': f'{split}-{index:04d}', 'split': split, 'seed': seed,
            'asset_seed': seed + 100_000_000, 'dt': PHYSICS.dt,
            'scene_id': 'tabletop-square-fixed', 'states': states, 'actions': actions,
            'collisions': collisions, 'terminated': reached_goal(state),
            'truncated': not reached_goal(state), 'frames': []}


def predict(state, actions, method):
    """Open-loop analytic baselines: initial truth state, future controls, no future truth."""
    if method not in ('state_hold', 'constant_velocity', 'action_prior_no_collision'):
        raise ValueError('Unknown baseline method.')
    current = tuple(state)
    predicted = []
    for action in actions:
        if method == 'constant_velocity':
            x, y, vx, vy = current
            current = (x + vx * PHYSICS.dt, y + vy * PHYSICS.dt, vx, vy)
        elif method == 'action_prior_no_collision':
            current = free_step(current, action)
        predicted.append(current)
    return predicted


def hardware_workload(latent, hidden):
    weights = (2 * latent + 2) * hidden + hidden * latent
    return {'assumed_network': f'{2 * latent + 2}->{hidden}->{latent}',
            'macs_per_step': weights, 'weight_bytes_int8_excluding_bias_scales': weights,
            'macs_for_16_candidates_8_steps': weights * 16 * 8,
            'two_state_buffers_bytes_int16': 16 * 2 * latent * 2,
            'all_future_states_bytes_int16': 16 * 8 * latent * 2}


def evaluate(episodes):
    metrics = {}
    for method in ('state_hold', 'constant_velocity', 'action_prior_no_collision'):
        metrics[method] = {}
        for horizon in (1, 4, 8):
            errors, collision_errors = [], []
            for item in episodes:
                for origin in range(len(item['actions']) - horizon + 1):
                    result = predict(item['states'][origin], item['actions'][origin:origin + horizon], method)[-1]
                    truth = item['states'][origin + horizon]
                    squared_error = sum((result[k] - truth[k]) ** 2 for k in (0, 1))
                    errors.append(squared_error)
                    if any(item['collisions'][origin:origin + horizon]):
                        collision_errors.append(squared_error)
            rmse = math.sqrt(float(np.mean(errors))) if errors else None
            metrics[method][str(horizon)] = {
                'windows': len(errors), 'endpoint_rmse_world_units': rmse,
                'endpoint_rmse_pixels': rmse * (IMAGE_SIZE - 1) if rmse is not None else None,
                'collision_windows': len(collision_errors),
                'collision_endpoint_rmse_world_units': math.sqrt(float(np.mean(collision_errors))) if collision_errors else None}
    return {'data_source': 'procedural simulation and rendering', 'nano_banana_used': False,
            'learned_model_status': 'not trained',
            'evaluation': 'test split, open-loop endpoint position RMSE, overlapping windows',
            'baseline_input': 'ground-truth initial x,y,vx,vy; action prior also knows simulator coefficients',
            'scope': 'state-level analytic baselines; no visual encoder, learned dynamics or hardware result',
            'position_units': 'world width = 1.0; pixel conversion uses image size minus one',
            'metrics': metrics,
            'hardware_estimate_status': 'illustrative workload only; no quantization validation, synthesis or timing',
            'hardware_workloads': [hardware_workload(32, 64), hardware_workload(64, 128)]}


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preview(episodes, out):
    # Diagnostic contact sheet: observed frames from three held-out trajectories.
    sheet = Image.new('RGB', (IMAGE_SIZE * 4, (IMAGE_SIZE + 20) * 3), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    for row, item in enumerate(episodes[:3]):
        last = len(item['frames']) - 1
        for col, index in enumerate((0, last // 3, 2 * last // 3, last)):
            x, y = col * IMAGE_SIZE, row * (IMAGE_SIZE + 20)
            with Image.open(out / item['frames'][index]) as image:
                sheet.paste(image, (x, y + 20))
            draw.text((x + 2, y + 3), f'e{row} t{index}', fill=(30, 30, 30))
    sheet.resize((768, 756), Image.Resampling.NEAREST).save(out / 'preview.png')


def build_dataset(out, seed=20261021, counts=(24, 6, 6), steps=48):
    if not isinstance(seed, int) or not 0 <= seed < 100_000_000:
        raise ValueError('Seed must be an integer in [0, 100000000).')
    if len(counts) != 3 or not all(isinstance(n, int) and 1 <= n <= 10000 for n in counts):
        raise ValueError('Provide positive train/val/test episode counts, at most 10000 each.')
    if not isinstance(steps, int) or not 8 <= steps <= 10000:
        raise ValueError('Steps must be an integer in [8, 10000].')
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise FileExistsError('Output must be a new or empty directory; existing results are never overwritten.')
    out.mkdir(parents=True, exist_ok=True)
    entries, test_episodes = [], []
    for split_index, (split, count) in enumerate(zip(('train', 'val', 'test'), counts)):
        (out / 'episodes' / split).mkdir(parents=True, exist_ok=True)
        for index in range(count):
            item = episode(split, index, seed + split_index * 1_000_000 + index, steps)
            frame_dir = out / 'frames' / item['episode_id']
            frame_dir.mkdir(parents=True)
            backdrop = background(item['asset_seed'])
            item['asset_id'] = hashlib.sha256(backdrop.tobytes()).hexdigest()
            frame_hashes = []
            for frame_index, state in enumerate(item['states']):
                path = frame_dir / f'{frame_index:03d}.png'
                render(state, backdrop).save(path)
                item['frames'].append(path.relative_to(out).as_posix())
                frame_hashes.append(file_hash(path))
            item['frame_sha256'] = frame_hashes
            path = out / 'episodes' / split / f'{item["episode_id"]}.json'
            write_json(path, item)
            entries.append({'episode_id': item['episode_id'], 'split': split, 'seed': item['seed'],
                            'asset_id': item['asset_id'], 'path': path.relative_to(out).as_posix(),
                            'sha256': file_hash(path), 'transitions': len(item['actions'])})
            if split == 'test':
                test_episodes.append(item)
    manifest = {'schema_version': 1, 'seed': seed, 'physics': asdict(PHYSICS),
                'image_size': [IMAGE_SIZE, IMAGE_SIZE, 3], 'state_order': ['x', 'y', 'vx', 'vy'],
                'action_order': ['normalized_acceleration_x', 'normalized_acceleration_y'],
                'action_interval': '[state[t], state[t+1]); dt seconds',
                'action_zero': 'no push; drag still slows existing velocity',
                'goal_rule': 'center distance <= goal_radius, tested after each step; first hit terminates',
                'collision_rule': 'non-elastic axis-separated square/AABB, zero normal velocity',
                'source': 'procedural only; no Nano Banana assets or API calls',
                'split_policy': 'whole episodes with disjoint RNG seeds and background instances; fixed scene geometry',
                'generalization_scope': 'unseen trajectories and procedural background instances, not new physics or scene geometry',
                'tool_versions': {'numpy': np.__version__, 'pillow': Image.__version__}, 'episodes': entries}
    write_json(out / 'manifest.json', manifest)
    report = evaluate(test_episodes)
    write_json(out / 'baseline_report.json', report)
    preview(test_episodes, out)
    return manifest, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('artifacts/tabletop-baseline'))
    parser.add_argument('--seed', type=int, default=20261021)
    parser.add_argument('--steps', type=int, default=48)
    args = parser.parse_args()
    manifest, report = build_dataset(args.out, seed=args.seed, steps=args.steps)
    print(f'Generated {len(manifest["episodes"])} episodes / {sum(e["transitions"] for e in manifest["episodes"])} transitions in {args.out}')
    for method, horizons in report['metrics'].items():
        result = horizons['8']
        error = result['endpoint_rmse_pixels']
        formatted = f'{error:.3f}' if error is not None else 'N/A'
        print(f'{method}: H8 endpoint RMSE = {formatted} pixels ({result["windows"]} windows)')
    print('Analytic baselines only. No learned model, Nano Banana call or FPGA measurement.')


if __name__ == '__main__':
    main()
