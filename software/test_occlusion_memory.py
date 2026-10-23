"""Run with python software/test_occlusion_memory.py; retain local evidence."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

from occlusion_memory import COLORS, METHODS, load_frames, observe, predict, run, summarize
from tabletop import file_hash


def rejects(exception, callback):
    try:
        callback()
    except exception:
        return
    raise AssertionError(f'Expected {exception.__name__}')


def main():
    root = Path(__file__).resolve().parents[1]
    test_root = root / 'artifacts' / 'test-runs'
    test_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='occlusion-', dir=test_root))
    out = temporary / 'first'
    manifest, report = run(out, seed=11, pairs=6)
    repeated, repeated_report = run(temporary / 'repeat', seed=11, pairs=6)
    assert manifest == repeated and report == repeated_report
    assert file_hash(out / 'preview.png') == file_hash(temporary / 'repeat' / 'preview.png')
    rows = json.loads((out / 'predictions.json').read_text(encoding='utf-8'))
    assert summarize(rows) == summarize(list(reversed(rows)))
    assert report['acceptance']['passed']
    assert report['stimulus_checks']['passed']
    assert report['stimulus_checks']['first_frames_correct'] == 18
    assert report['stimulus_checks']['paired_hidden_segments_identical'] == 6
    assert report['metrics']['last_frame']['seen_accuracy'] == 0
    assert report['metrics']['last_frame']['unknown_accuracy'] == 1
    assert report['metrics']['always_red']['seen_accuracy'] == 0.5
    assert report['metrics']['always_red']['unknown_accuracy'] == 0
    assert report['metrics']['always_red']['pair_accuracy'] == 0
    for pair in range(6):
        trials = {item['target']: item for item in manifest['trials'] if item['pair'] == pair}
        assert set(trials) == {'red', 'blue', 'unknown'}
        frames = {target: load_frames(out, trial) for target, trial in trials.items()}
        assert len({len(sequence) for sequence in frames.values()}) == 1
        for target, sequence in frames.items():
            assert observe(sequence[0]) == target
            assert all(observe(image) == 'unknown' for image in sequence[1:])
            for name, digest in zip(trials[target]['frames'], trials[target]['frame_sha256']):
                assert file_hash(out / name) == digest
        assert frames['red'][0].tobytes() != frames['blue'][0].tobytes()
        for red, blue, unknown in zip(frames['red'][1:], frames['blue'][1:], frames['unknown'][1:]):
            assert red.tobytes() == blue.tobytes() == unknown.tobytes(), 'Hidden pixels leak color'
        for target in ('red', 'unknown', 'blue', 'unknown'):
            assert predict(frames[target], 'last_seen') == target, 'Memory leaked between sequences'
        assert predict(frames['red'][1:], 'last_seen') == 'unknown', 'Past-frame removal must remove evidence'
        assert predict([frames['red'][0], frames['blue'][0], frames['red'][-1]], 'last_seen') == 'blue'
    ambiguous = Image.new('RGB', (64, 64), (230, 230, 230))
    draw = ImageDraw.Draw(ambiguous)
    draw.rectangle((5, 5, 10, 10), fill=COLORS['red'])
    draw.rectangle((20, 20, 25, 25), fill=COLORS['blue'])
    assert observe(ambiguous) == 'unknown'
    rejects(ValueError, lambda: observe(ambiguous.convert('L')))
    rejects(ValueError, lambda: predict([], METHODS[0]))
    rejects(ValueError, lambda: predict([ambiguous], 'invalid'))
    rejects(ValueError, lambda: run(temporary / 'invalid', pairs=True))
    rejects(ValueError, lambda: run(temporary / 'invalid', seed=-1))
    before = file_hash(out / 'manifest.json')
    rejects(FileExistsError, lambda: run(out))
    assert before == file_hash(out / 'manifest.json')
    command = [sys.executable, str(root / 'software' / 'occlusion_memory.py')]
    success = subprocess.run(command + ['--out', str(temporary / 'cli'), '--pairs', '2'],
                             capture_output=True, text=True)
    assert success.returncode == 0, success.stderr
    failure = subprocess.run(command + ['--out', str(out)], capture_output=True, text=True)
    assert failure.returncode == 1 and 'never overwritten' in failure.stderr
    assert before == file_hash(out / 'manifest.json')
    print('PASS: paired pixels, perception, memory reset/removal/update, unknown cases, scoring, reproducibility and CLI overwrite protection')


if __name__ == '__main__':
    main()
