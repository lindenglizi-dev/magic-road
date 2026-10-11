"""Check the five added AC8 vehicle labels, without altering source labels."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw
from cnn.import_verified_review import _validate_patch
from cnn.prepare_ac_correction import isolated
from cnn.prepare_ground48 import read_json, write_json, sha256_file, dataset_id, _parse_signed_time

OUT = Path(__file__).resolve().parent
PILOT = ROOT / 'cnn/reports/ac_correction_pilot8_20261009_v2'
PATCH = Path('C:/Users/lenovo/Downloads/review_patch_4e7300bec9a0_2026-10-10T01-58-35-215Z.json')
OLD = ROOT / 'cnn/reports/ac_patch_check_20261010_v2/review_patch_4e7300bec9a0_2026-10-10T01-17-00-432Z.json'
DIGEST = '883c57e4f174399485ba29696562f0a791c8b0321e93660d4d22fa6bbc9a160e'


def check():
    assert sha256_file(PATCH) == DIGEST
    assert sha256_file(OLD) == 'e10101088ed9955d47cf3a9cd204659a0e678405cfbeddb875e452ef2b5cb5c3'
    manifest = read_json(PILOT / 'review_manifest_teacher.json')
    samples = {s['image_id']: s for s in manifest['samples']}
    _, reviews, raw = _validate_patch(PATCH, manifest, samples)
    assert dataset_id(manifest) == manifest['dataset_id']
    assert set(reviews) == set(samples) and len(reviews) == 8
    isolated(manifest['samples'])
    for image_id, r in reviews.items():
        assert r['complete']
        _parse_signed_time(r['reviewed_at_utc'], image_id)
        assert sha256_file(PILOT / samples[image_id]['raw_file']) == samples[image_id]['source_sha256']
    for name, digest in read_json(PILOT / 'source_bindings.json').items():
        assert sha256_file(Path(name)) == digest, name
    additions = {}
    for previous in read_json(OLD)['reviews']:
        before = {a['target_id']: a for a in previous['actions']}
        after = {a['target_id']: a for a in reviews[previous['image_id']]['actions']}
        assert all(after.get(k) == a for k, a in before.items()), 'Prior label lost/changed'
        additions[previous['image_id']] = [a for k, a in after.items() if k not in before]
    assert sum(map(len, additions.values())) == 5
    assert all(a['action'] == 'N' and a['class'] == 'vehicle' for group in additions.values() for a in group)
    assert Counter(a['class'] for r in reviews.values() for a in r['actions']) == {'person': 11, 'vehicle': 66, 'ignore': 1}
    wrong = deepcopy(manifest)
    wrong['dataset_id'] = 'wrong'
    try:
        _validate_patch(PATCH, wrong, samples)
    except ValueError:
        pass
    else:
        raise AssertionError('Wrong dataset accepted')
    return samples, reviews, raw, additions


if __name__ == '__main__':
    samples, reviews, raw, additions = check()
    if '--check-only' in sys.argv:
        assert (OUT / PATCH.name).read_bytes() == raw
        assert read_json(OUT / 'patch_validation.json')['patch_sha256'] == DIGEST
        print('PASS current patch, prior preservation, source hashes, signatures, counts, negative regression, saved report')
        raise SystemExit(0)
    with (OUT / PATCH.name).open('xb') as stream:
        stream.write(raw)
    for image_id, added in additions.items():
        if not added:
            continue
        with Image.open(PILOT / samples[image_id]['raw_file']) as source:
            image = source.convert('RGB').resize((1080, 864), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(image)
        added_ids = {a['target_id'] for a in added}
        for a in reviews[image_id]['actions']:
            fresh = a['target_id'] in added_ids
            color = '#00ffff' if fresh else '#ffb000' if a['class']=='vehicle' else '#00ff80'
            box = [v*3 for v in a['bbox']]
            draw.rectangle(box, outline=color, width=4 if fresh else 2)
            if fresh:
                draw.text((box[0], max(0, box[1]-14)), a['target_id'], fill=color, stroke_width=2, stroke_fill='black')
        image.save(OUT / f'{image_id}_additions.png')
    write_json(OUT / 'patch_validation.json', dict(status='signed_patch_valid_not_full_dataset_freeze', patch_sha256=DIGEST, previous_patch_sha256=sha256_file(OLD), complete_frames=8, labels={'person':11,'vehicle':66,'ignore':1}, added_vehicle_boxes=5, additions=additions, prior_73_actions_unchanged=True, protected_inputs_unchanged=True, dataset_frozen=False, G_ready=False, training_started=False))
    print('PASS: +5 vehicles; all73 prior records retained;78 total;8 signatures; no training')
