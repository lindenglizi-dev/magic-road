"""Pixel-only rule baselines for a controlled occlusion memory experiment."""

import argparse
import hashlib
from pathlib import Path
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tabletop import IMAGE_SIZE, background, file_hash, write_json


COLORS = {'red': (200, 45, 50), 'blue': (40, 75, 210)}
METHODS = ('last_frame', 'last_seen', 'always_red')


def observe(image):
    """Recognize one dominant red/blue patch; ambiguous or absent means unknown."""
    if image.mode != 'RGB' or image.size != (IMAGE_SIZE, IMAGE_SIZE):
        raise ValueError('Expected a 64x64 RGB image.')
    pixels = np.asarray(image).astype(np.int16)
    red, green, blue = (pixels[:, :, channel] for channel in range(3))
    masks = ((red > 150) & (red - green > 60) & (red - blue > 60),
             (blue > 150) & (blue - green > 60) & (blue - red > 60))
    found = [color for color, mask in zip(COLORS, masks) if np.count_nonzero(mask) >= 4]
    # ponytail: fixed palette/neutral backgrounds only; compare learned perception on richer scenes later.
    return found[0] if len(found) == 1 else 'unknown'


def predict(frames, method):
    """Only decoded pixels enter here. Memory is local to this sequence."""
    if not frames or method not in METHODS:
        raise ValueError('Provide a nonempty sequence and a supported method.')
    if method == 'always_red':
        return 'red'
    if method == 'last_frame':
        return observe(frames[-1])
    remembered = 'unknown'
    for image in frames:
        observed = observe(image)
        if observed != 'unknown':
            remembered = observed
    return remembered


def make_cases(seed, pairs):
    rng = random.Random(seed)
    cases = []
    for pair in range(pairs):
        backdrop = background(seed + pair)
        side = rng.randint(8, 14)
        x, y = rng.randint(8, 42), rng.randint(8, 42)
        hidden = backdrop.copy()
        ImageDraw.Draw(hidden).rectangle((x - 3, y - 3, x + side + 3, y + side + 3),
                                        fill=(65, 70, 85))
        delay = rng.randint(2, 6)
        for color, rgb in COLORS.items():
            visible = backdrop.copy()
            ImageDraw.Draw(visible).rectangle((x, y, x + side, y + side), fill=rgb)
            cases.append((pair, color, [visible] + [hidden.copy() for _ in range(delay)]))
        # The question is what was observed, not the generator's hidden physical state.
        cases.append((pair, 'unknown', [hidden.copy() for _ in range(delay + 1)]))
    rng.shuffle(cases)
    return cases


def load_frames(out, trial):
    frames = []
    for name in trial['frames']:
        with Image.open(out / name) as image:
            frames.append(image.convert('RGB'))
    return frames


def summarize(rows):
    seen = [row for row in rows if row['target'] != 'unknown']
    unseen = [row for row in rows if row['target'] == 'unknown']
    pairs = sorted({row['pair'] for row in seen})
    metrics = {}
    for method in METHODS:
        correct_seen = sum(row['predictions'][method] == row['target'] for row in seen)
        correct_unknown = sum(row['predictions'][method] == 'unknown' for row in unseen)
        both = sum(all(row['predictions'][method] == row['target']
                       for row in seen if row['pair'] == pair) for pair in pairs)
        metrics[method] = {
            'seen_correct': correct_seen, 'seen_total': len(seen),
            'seen_accuracy': correct_seen / len(seen),
            'unknown_correct': correct_unknown, 'unknown_total': len(unseen),
            'unknown_accuracy': correct_unknown / len(unseen),
            'pairs_both_correct': both, 'pairs_total': len(pairs),
            'pair_accuracy': both / len(pairs),
            'errors': len(rows) - correct_seen - correct_unknown}
    return metrics


def preview(out, trials, rows):
    selected = sorted((trial for trial in trials if trial['pair'] == 0),
                      key=lambda trial: ('red', 'blue', 'unknown').index(trial['target']))
    predictions = {row['id']: row['predictions'] for row in rows}
    sheet = Image.new('RGB', (1040, 580), (246, 247, 250))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    small = ImageFont.load_default(size=16)
    draw.text((20, 12), 'Occlusion memory | same final pixels, different histories',
              fill=(25, 35, 50), font=font)
    for row, trial in enumerate(selected):
        y = 60 + row * 170
        frames = load_frames(out, trial)
        for col, index in enumerate((0, 1, len(frames) - 1)):
            x = 20 + col * 160
            draw.text((x, y), f'Frame {index}', fill=(55, 60, 75), font=small)
            sheet.paste(frames[index].resize((128, 128), Image.Resampling.NEAREST), (x, y + 25))
        draw.text((510, y + 15), f'Previously observed: {trial["target"]}',
                  fill=(25, 35, 50), font=font)
        for line, method in enumerate(METHODS):
            answer = predictions[trial['id']][method]
            color = (25, 110, 65) if answer == trial['target'] else (180, 55, 40)
            draw.text((510, y + 47 + line * 28), f'{method}: {answer}', fill=color, font=small)
    sheet.save(out / 'preview.png')


def run(out, seed=20261024, pairs=100):
    if type(seed) is not int or not 0 <= seed < 100_000_000:
        raise ValueError('Seed must be an integer in [0, 100000000).')
    if type(pairs) is not int or not 1 <= pairs <= 1000:
        raise ValueError('Pairs must be an integer in [1, 1000].')
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise FileExistsError('Output must be new or empty; existing results are never overwritten.')
    out.mkdir(parents=True, exist_ok=True)
    trials, rows = [], []
    hidden_signatures = {}
    checks = {'first_frames_correct': 0, 'hidden_frames_without_color': 0, 'hidden_frames_total': 0}
    for index, (pair, target, frames) in enumerate(make_cases(seed, pairs)):
        trial = {'id': f'{index:04d}', 'pair': pair, 'target': target, 'frames': [], 'frame_sha256': []}
        directory = out / 'frames' / trial['id']
        directory.mkdir(parents=True)
        for step, image in enumerate(frames):
            path = directory / f'{step:02d}.png'
            image.save(path)
            trial['frames'].append(path.relative_to(out).as_posix())
            trial['frame_sha256'].append(file_hash(path))
        trials.append(trial)
        # Read exported pixels back. Neither filenames nor target/pair metadata reach predict().
        decoded = load_frames(out, trial)
        observations = [observe(image) for image in decoded]
        checks['first_frames_correct'] += observations[0] == target
        checks['hidden_frames_without_color'] += observations[1:].count('unknown')
        checks['hidden_frames_total'] += len(decoded) - 1
        signature = tuple(hashlib.sha256(image.tobytes()).hexdigest() for image in decoded[1:])
        hidden_signatures.setdefault(pair, set()).add(signature)
        answers = {method: predict(decoded, method) for method in METHODS}
        rows.append({'id': trial['id'], 'pair': pair, 'target': target,
                     'predictions': answers,
                     'failed_methods': [method for method in METHODS if answers[method] != target]})

    manifest = {
        'schema_version': 'occlusion-memory-v1', 'seed': seed, 'pairs': pairs,
        'question': 'Which color did you observe before the occlusion? Answer unknown if never observed.',
        'image_size': [IMAGE_SIZE, IMAGE_SIZE, 3],
        'sequence': 'one visible frame then 2-6 hidden frames; unknown cases are hidden throughout',
        'scope': 'one static object, fixed palette, neutral backgrounds, no changes while hidden',
        'split': 'controlled diagnostic only; no training, validation or held-out generalization claim',
        'model_input': 'decoded RGB images only; labels and pairing are evaluator metadata',
        'trials': trials}
    write_json(out / 'manifest.json', manifest)
    write_json(out / 'predictions.json', rows)
    metrics = summarize(rows)
    checks['paired_hidden_segments_identical'] = sum(len(signatures) == 1
                                                    for signatures in hidden_signatures.values())
    checks['passed'] = (checks['first_frames_correct'] == len(trials)
                        and checks['hidden_frames_without_color'] == checks['hidden_frames_total']
                        and checks['paired_hidden_segments_identical'] == pairs)
    report = {
        'schema_version': 'occlusion-memory-v1', 'seed': seed, 'pairs': pairs, 'sequences': len(trials),
        'methods': {
            'last_frame': 'fixed color detector on the final image; absent color yields unknown',
            'last_seen': 'same detector, remembers the most recent visible color; reset per sequence',
            'always_red': 'constant guess; 50% on balanced seen cases, 0% on unknown cases'},
        'metrics': metrics, 'stimulus_checks': checks,
        'acceptance': {
            'criterion': 'stimulus checks pass; last_seen gets all seen, unknown and paired cases correct',
            'passed': checks['passed'] and metrics['last_seen']['seen_accuracy'] == 1
                      and metrics['last_seen']['unknown_accuracy'] == 1
                      and metrics['last_seen']['pair_accuracy'] == 1},
        'scope': 'hand-written rule baselines; no training, Nano Banana, learned memory or hardware measurement',
        'manifest_sha256': file_hash(out / 'manifest.json'),
        'predictions_sha256': file_hash(out / 'predictions.json'),
        'source_sha256': {name: file_hash(Path(__file__).with_name(name))
                          for name in ('occlusion_memory.py', 'tabletop.py')},
        'versions': {'python': sys.version.split()[0], 'numpy': np.__version__, 'pillow': Image.__version__}}
    write_json(out / 'report.json', report)
    preview(out, trials, rows)
    return manifest, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('artifacts/occlusion-memory'))
    parser.add_argument('--seed', type=int, default=20261024)
    parser.add_argument('--pairs', type=int, default=100)
    args = parser.parse_args()
    try:
        _, report = run(args.out, args.seed, args.pairs)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Generated {report["sequences"]} sequences / {report["pairs"]} pairs in {args.out}')
    for method, metrics in report['metrics'].items():
        print(f'{method}: seen={metrics["seen_accuracy"]:.1%}, '
              f'unknown={metrics["unknown_accuracy"]:.1%}, pairs={metrics["pair_accuracy"]:.1%}')
    print('Rule baselines only. See preview.png and predictions.json for individual results.')
    return 0 if report['acceptance']['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
