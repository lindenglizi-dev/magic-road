"""Two-frame supervised state initialization and learned action-conditioned dynamics."""

import argparse
import json
import math
from pathlib import Path
import time

import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from tabletop import PHYSICS, file_hash, predict, write_json


HORIZON = 8
SCALE = torch.tensor([1.0, 1.0, 0.5, 0.5])


def dataset_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Dataset paths must stay inside the dataset directory.')
    return path


def load_data(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if (manifest['image_size'] != [64, 64, 3]
            or manifest['state_order'] != ['x', 'y', 'vx', 'vy']
            or manifest['action_order'] != ['normalized_acceleration_x', 'normalized_acceleration_y']
            or manifest['physics'] != json.loads(json.dumps(PHYSICS.__dict__))):
        raise ValueError('This pilot expects the original 64x64 tabletop physics and state/action convention.')
    splits = {name: [] for name in ('train', 'val', 'test')}
    identities, seeds, assets, digests = set(), set(), set(), set()
    for entry in manifest['episodes']:
        for value, seen in ((entry['episode_id'], identities), (entry['seed'], seeds),
                            (entry['asset_id'], assets), (entry['sha256'], digests)):
            if value in seen:
                raise ValueError('Repeated episode, seed, background or episode hash across dataset.')
            seen.add(value)
        path = dataset_path(root, entry['path'])
        if file_hash(path) != entry['sha256']:
            raise ValueError(f'Episode hash mismatch: {entry["episode_id"]}')
        item = json.loads(path.read_text(encoding='utf-8'))
        if (entry['split'] not in splits or item['split'] != entry['split']
                or item['episode_id'] != entry['episode_id'] or item['seed'] != entry['seed']
                or item['asset_id'] != entry['asset_id'] or item['dt'] != PHYSICS.dt):
            raise ValueError('Episode identity does not match manifest.')
        n = len(item['actions'])
        if not (len(item['states']) == len(item['frames']) == len(item['frame_sha256']) == n + 1
                and len(item['collisions']) == n):
            raise ValueError('Expected N actions and N+1 states/images.')
        states = np.asarray(item['states'], dtype=np.float32)
        actions = np.asarray(item['actions'], dtype=np.float32)
        if states.shape != (n + 1, 4) or actions.shape != (n, 2) or not np.isfinite(states).all() or not np.isfinite(actions).all() or np.max(np.abs(actions), initial=0) > 1:
            raise ValueError('Malformed or nonfinite states/actions.')
        images = []
        for relative, digest in zip(item['frames'], item['frame_sha256']):
            image_path = dataset_path(root, relative)
            if file_hash(image_path) != digest:
                raise ValueError(f'Frame hash mismatch: {relative}')
            with Image.open(image_path) as image:
                if image.size != (64, 64) or image.mode != 'RGB':
                    raise ValueError('Expected 64x64 RGB images.')
                images.append(np.asarray(image).copy())
        item['images'] = np.stack(images)
        item['states'] = states
        item['actions'] = actions
        splits[entry['split']].append(item)
    if any(not items for items in splits.values()):
        raise ValueError('Train, validation and test splits must all be nonempty.')
    return splits


class Windows(Dataset):
    def __init__(self, episodes):
        self.episodes = episodes
        self.origins = [(i, t) for i, item in enumerate(episodes) for t in range(1, len(item['actions']))]
        if not self.origins:
            raise ValueError('At least one two-frame prediction window is required.')

    def __len__(self):
        return len(self.origins)

    def __getitem__(self, index):
        episode_index, origin = self.origins[index]
        item = self.episodes[episode_index]
        length = min(HORIZON, len(item['actions']) - origin)
        images = item['images'][origin - 1:origin + 1].transpose(0, 3, 1, 2).reshape(6, 64, 64)
        actions = np.zeros((HORIZON, 2), dtype=np.float32)
        targets = np.zeros((HORIZON, 4), dtype=np.float32)
        mask = np.zeros(HORIZON, dtype=np.float32)
        actions[:length] = item['actions'][origin:origin + length]
        targets[:length] = item['states'][origin + 1:origin + length + 1]
        mask[:length] = 1
        return {'images': torch.from_numpy(images.copy()).float() / 255,
                'actions': torch.from_numpy(actions), 'targets': torch.from_numpy(targets),
                'mask': torch.from_numpy(mask), 'truth_initial': torch.from_numpy(item['states'][origin].copy()),
                'index': index}


class VisualPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(6, 8, 5, stride=2, padding=2), nn.ReLU(),
            nn.Conv2d(8, 16, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(16, 16, 3, stride=2, padding=1), nn.ReLU(), nn.Flatten(),
            nn.Linear(16 * 8 * 8, 64), nn.ReLU(), nn.Linear(64, 4))
        self.dynamics = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64),
                                      nn.ReLU(), nn.Linear(64, 4))
        nn.init.zeros_(self.dynamics[-1].weight)
        nn.init.zeros_(self.dynamics[-1].bias)

    def encode(self, images):
        if images.ndim != 4 or images.shape[1:] != (6, 64, 64):
            raise ValueError('Expected batch x 6 x 64 x 64 two-frame input.')
        raw = self.encoder(images)
        return torch.cat((raw[:, :2].sigmoid(), 0.5 * raw[:, 2:].tanh()), dim=1)

    def rollout(self, initial, actions):
        if initial.ndim != 2 or initial.shape[1] != 4 or actions.ndim != 3 or actions.shape[0] != initial.shape[0] or actions.shape[2] != 2 or not 1 <= actions.shape[1] <= HORIZON:
            raise ValueError('Expected initial [B,4] and actions [B,H,2], 1 <= H <= 8.')
        state, results = initial, []
        for action in actions.unbind(dim=1):
            # ponytail: supervised physical state; use latent representation learning for richer observations.
            state = state + 0.1 * self.dynamics(torch.cat((state, action), dim=1))
            results.append(state)
        return torch.stack(results, dim=1)

    def forward(self, images, actions):
        initial = self.encode(images)
        return initial, self.rollout(initial, actions)


def masked_loss(predicted, target, mask):
    error = ((predicted - target) / SCALE).square().mean(dim=-1)
    return (error * mask).sum() / mask.sum().clamp_min(1)


@torch.no_grad()
def validation_score(model, data):
    model.eval()
    errors = []
    for batch in DataLoader(data, batch_size=128):
        _, future = model(batch['images'], batch['actions'])
        valid = batch['mask'][:, 7].bool()
        errors.extend((future[valid, 7, :2] - batch['targets'][valid, 7, :2]).square().sum(dim=1).tolist())
    if not errors:
        raise ValueError('Validation requires at least one complete 8-step window.')
    return math.sqrt(float(np.mean(errors))) * 63


@torch.no_grad()
def evaluate_model(model, data):
    model.eval()
    records, initial_errors = [], []
    for batch in DataLoader(data, batch_size=128):
        estimated, learned = model(batch['images'], batch['actions'])
        truth_learned = model.rollout(batch['truth_initial'], batch['actions'])
        for i, sample_index in enumerate(batch['index'].tolist()):
            episode_index, origin = data.origins[sample_index]
            item = data.episodes[episode_index]
            length = int(batch['mask'][i].sum())
            controls = batch['actions'][i, :length].tolist()
            initial_errors.append((estimated[i] - batch['truth_initial'][i]).numpy())
            methods = {'visual_learned': learned[i, :length].numpy(),
                       'truth_initial_learned': truth_learned[i, :length].numpy()}
            for source, initial in (('visual', estimated[i].tolist()), ('truth_initial', batch['truth_initial'][i].tolist())):
                for baseline in ('state_hold', 'constant_velocity', 'action_prior_no_collision'):
                    methods[f'{source}_{baseline}'] = np.asarray(predict(initial, controls, baseline))
            for horizon in (1, 4, 8):
                if horizon > length:
                    continue
                truth = item['states'][origin + horizon, :2]
                records.append({'window_id': f'{item["episode_id"]}:{origin}:H{horizon}',
                                'episode_id': item['episode_id'], 'origin': origin, 'horizon': horizon,
                                'collision': any(item['collisions'][origin:origin + horizon]),
                                'squared_position_error': {name: float(np.square(result[horizon - 1, :2] - truth).sum()) for name, result in methods.items()}})
    if not records:
        raise ValueError('No evaluation windows.')
    names = list(records[0]['squared_position_error'])
    metrics = {}
    for name in names:
        metrics[name] = {}
        for horizon in (1, 4, 8):
            selected = [r for r in records if r['horizon'] == horizon]
            collision = [r for r in selected if r['collision']]
            rmse = lambda rows: math.sqrt(float(np.mean([r['squared_position_error'][name] for r in rows]))) * 63 if rows else None
            metrics[name][str(horizon)] = {'windows': len(selected), 'endpoint_rmse_pixels': rmse(selected),
                                          'collision_windows': len(collision), 'collision_rmse_pixels': rmse(collision),
                                          'per_episode_rmse_pixels': {episode_id: rmse([r for r in selected if r['episode_id'] == episode_id]) for episode_id in sorted({r['episode_id'] for r in selected})}}
    initial_errors = np.stack(initial_errors)
    return {'metrics': metrics, 'initial_position_rmse_pixels': float(np.sqrt(np.mean(np.square(initial_errors[:, :2]).sum(axis=1))) * 63),
            'initial_velocity_rmse_world_units_per_second': float(np.sqrt(np.mean(np.square(initial_errors[:, 2:]).sum(axis=1)))),
            'window_records': records}


def train(data_root, out, epochs=80, seed=20261022):
    if not isinstance(epochs, int) or not 1 <= epochs <= 200 or not isinstance(seed, int) or not 0 <= seed < 2**32:
        raise ValueError('Use 1..200 epochs and a seed in [0, 2**32).')
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise FileExistsError('Output must be new or empty; checkpoints are not overwritten across runs.')
    splits = load_data(data_root)
    datasets = {name: Windows(items) for name, items in splits.items()}
    if any(not any(len(item['actions']) > HORIZON for item in items) for items in splits.values()):
        raise ValueError('Every split requires at least one complete two-frame 8-step prediction window.')
    torch.set_num_threads(2)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    model = VisualPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loader = DataLoader(datasets['train'], batch_size=64, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    best, best_epoch, history = math.inf, 0, []
    for epoch in range(1, epochs + 1):
        model.train()
        total, count = 0.0, 0
        for batch in loader:
            optimizer.zero_grad()
            estimated, future = model(batch['images'], batch['actions'])
            teacher_initial_future = model.rollout(batch['truth_initial'], batch['actions'])
            initial_loss = ((estimated - batch['truth_initial']) / SCALE).square().mean()
            loss = 4 * initial_loss + masked_loss(future, batch['targets'], batch['mask']) + masked_loss(teacher_initial_future, batch['targets'], batch['mask'])
            if not torch.isfinite(loss):
                raise FloatingPointError('Nonfinite training loss.')
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            optimizer.step()
            total += loss.item() * len(estimated); count += len(estimated)
        score = validation_score(model, datasets['val'])
        if not math.isfinite(score):
            raise FloatingPointError('Nonfinite validation score.')
        history.append({'epoch': epoch, 'train_loss': total / count, 'validation_h8_rmse_pixels': score})
        if score < best:
            best, best_epoch = score, epoch
            torch.save({'state_dict': model.state_dict(), 'epoch': epoch, 'seed': seed}, out / 'checkpoint.pt')
        if epoch == 1 or epoch % 10 == 0 or epoch == epochs:
            print(f'Epoch {epoch}/{epochs}: loss={total/count:.5f}, validation H8={score:.3f}px', flush=True)
    checkpoint = torch.load(out / 'checkpoint.pt', map_location='cpu', weights_only=True)
    model.load_state_dict(checkpoint['state_dict'])
    report = evaluate_model(model, datasets['test'])
    report.update({'model': 'two-frame CNN initializer + supervised residual state MLP',
                   'device': 'cpu', 'epochs': epochs, 'best_epoch': best_epoch,
                   'selection': 'minimum validation H8 position RMSE; test evaluated only after selection',
                   'best_validation_h8_rmse_pixels': best, 'seed': seed,
                   'dataset_manifest_sha256': file_hash(Path(data_root) / 'manifest.json'),
                   'source_sha256': file_hash(Path(__file__)),
                   'checkpoint_sha256': file_hash(out / 'checkpoint.pt'),
                   'training_seconds': time.perf_counter() - started,
                   'train_windows': len(datasets['train']), 'val_windows': len(datasets['val']),
                   'test_episodes': len(splits['test']), 'test_origin_windows': len(datasets['test']),
                   'torch_version': str(torch.__version__), 'cpu_threads': torch.get_num_threads(),
                   'prediction_contract': 'Only image[t-1], image[t] and candidate future actions are inputs; no future image/state feedback.',
                   'training_supervision': 'Initial physical state and future states; additional rollouts initialized from training truth states.',
                   'baseline_contract': 'All methods use the same t>=1 windows; truth_initial methods have stronger inputs and are diagnostic references.',
                   'limitations': ['Fixed geometry and procedural textures; Nano Banana not used.',
                                   'Only prediction tested; no planning success, quantization, FPGA timing or energy results.',
                                   'One seed and six held-out episodes; overlapping windows are not independent experiments.'],
                   'parameter_counts': {'encoder': sum(p.numel() for p in model.encoder.parameters()),
                                        'dynamics': sum(p.numel() for p in model.dynamics.parameters())},
                   'dynamics_macs_per_step_excluding_activations_residual': 6 * 64 + 64 * 64 + 64 * 4})
    write_json(out / 'history.json', history)
    write_json(out / 'report.json', report)
    for name, result in report['metrics'].items():
        print(f'{name}: H8={result["8"]["endpoint_rmse_pixels"]:.3f}px', flush=True)
    return model, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('artifacts/tabletop-baseline'))
    parser.add_argument('--out', type=Path, default=Path('artifacts/visual-pilot'))
    parser.add_argument('--epochs', type=int, default=80)
    parser.add_argument('--seed', type=int, default=20261022)
    args = parser.parse_args()
    train(args.data, args.out, epochs=args.epochs, seed=args.seed)


if __name__ == '__main__':
    main()
