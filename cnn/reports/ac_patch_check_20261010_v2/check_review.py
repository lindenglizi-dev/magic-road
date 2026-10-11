"""Validate this exact signed AC8 patch; no training/dataset publication."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import html
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw
from cnn.import_verified_review import _validate_patch
from cnn.prepare_ground48 import read_json, write_json, sha256_file, dataset_id, _parse_signed_time
from cnn.prepare_ac_correction import isolated

OUT = Path(__file__).resolve().parent
PILOT = ROOT / 'cnn/reports/ac_correction_pilot8_20261009_v2'
PATCH = Path('C:/Users/lenovo/Downloads/review_patch_4e7300bec9a0_2026-10-10T01-17-00-432Z.json')
OLD = Path('C:/Users/lenovo/Downloads/review_patch_4e7300bec9a0_2026-10-10T00-33-19-779Z.json')


def check():
    assert sha256_file(PATCH) == 'e10101088ed9955d47cf3a9cd204659a0e678405cfbeddb875e452ef2b5cb5c3'
    manifest = read_json(PILOT / 'review_manifest_teacher.json')
    samples = {s['image_id']: s for s in manifest['samples']}
    patch, reviews, raw = _validate_patch(PATCH, manifest, samples)
    assert dataset_id(manifest) == manifest['dataset_id']
    assert set(reviews) == set(samples) and len(reviews) == 8
    assert all(r['complete'] for r in reviews.values())
    for image_id, review in reviews.items():
        _parse_signed_time(review['reviewed_at_utc'], image_id)
        assert sha256_file(PILOT / samples[image_id]['raw_file']) == samples[image_id]['source_sha256']
    isolated(manifest['samples'])
    for path, digest in read_json(PILOT / 'source_bindings.json').items():
        assert sha256_file(Path(path)) == digest, path
    old = read_json(OLD)
    for previous in old['reviews']:
        current = {a['target_id']: a for a in reviews[previous['image_id']]['actions']}
        assert all(current[a['target_id']] == a for a in previous['actions'])
    wrong = deepcopy(manifest)
    wrong['dataset_id'] = 'wrong'
    try:
        _validate_patch(PATCH, wrong, samples)
    except ValueError:
        pass
    else:
        raise AssertionError('Wrong dataset accepted')
    labels = Counter(a['class'] for r in reviews.values() for a in r['actions'])
    actions = Counter(a['action'] for r in reviews.values() for a in r['actions'])
    assert labels == {'person': 11, 'vehicle': 61, 'ignore': 1}
    assert actions == {'A': 51, 'N': 22}
    return manifest, reviews, raw, labels, actions


if __name__ == '__main__':
    manifest, reviews, raw, labels, actions = check()
    digest = sha256_file(PATCH)
    # Hash is bound below after read-only validation; never overwrite an existing report.
    print('PASS signatures8, labels', dict(labels), 'actions', dict(actions), 'SHA', digest)
    if '--check-only' in sys.argv:
        assert (OUT / PATCH.name).read_bytes() == raw
        assert read_json(OUT / 'patch_validation.json')['patch_sha256'] == digest
        print('PASS saved patch bytes and report binding')
        raise SystemExit(0)
    assert not (OUT / 'patch_validation.json').exists(), 'Preserve existing report'
    with (OUT / PATCH.name).open('xb') as stream:
        stream.write(raw)
    frames, cards = [], []
    sheet = Image.new('RGB', (1440, 8 * 310), 'white')
    for n, sample in enumerate(manifest['samples'], 1):
        review = reviews[sample['image_id']]
        with Image.open(PILOT / sample['raw_file']) as source:
            image = source.convert('RGB')
        image.thumbnail((700, 280))
        scale = image.width / sample['width']
        overlay = image.copy()
        draw = ImageDraw.Draw(overlay)
        for action in review['actions']:
            color = {'person': '#00ff80', 'vehicle': '#ffb000', 'ignore': '#ff40ff'}[action['class']]
            box = [v * scale for v in action['bbox']]
            draw.rectangle(box, outline=color, width=2)
            draw.text((box[0], max(0, box[1]-11)), action['target_id'], fill=color, stroke_width=1, stroke_fill='black')
        filename = f'frame{n}_signed.png'
        overlay.save(OUT / filename)
        y = (n-1)*310
        sheet.paste(image, (0, y+25))
        sheet.paste(overlay, (720, y+25))
        ImageDraw.Draw(sheet).text((4, y+4), f'{n}: {sample["image_id"]} | raw / signed labels', fill='black')
        counts = dict(Counter(a['class'] for a in review['actions']))
        frames.append(dict(image_number=n, image_id=sample['image_id'], scene=sample['scene'], candidate_split=sample['split'], family_id=sample['family_id'], complete=True, signed_at=review['reviewed_at_utc'], labels=counts))
        raw_path = (PILOT / sample['raw_file']).as_uri()
        cards.append(f'<h2>{n}. {html.escape(sample["image_id"])}</h2><p>{html.escape(str(counts))}</p><a href="{raw_path}">完整无框原图</a><br><img src="{filename}">')
    sheet.save(OUT / 'contact_sheet.jpg', quality=95)
    teacher_new = sum(a['action']=='N' and a['target_id'].startswith('teacher_') for r in reviews.values() for a in r['actions'])
    write_json(OUT / 'patch_validation.json', dict(status='signed_patch_valid_pending_visual_coverage_check', dataset_id=manifest['dataset_id'], patch_sha256=digest, complete_frames=8, label_counts=dict(labels), action_counts=dict(actions), new_teacher_id_boxes=teacher_new, new_other_id_boxes=22-teacher_new, previous_actions_preserved=True, additional_records=27, old_inputs_unchanged=True, dataset_frozen=False, G_ready=False, training_started=False, frames=frames, boundary='Human signed pilot annotations; no accuracy measurement or complete training/dev dataset freeze.'))
    with (OUT / 'index.html').open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><meta charset="utf-8"><title>AC8 本次签署补丁核对</title><style>body{font:18px sans-serif;background:#202020;color:white;padding:24px}img{max-width:100%}a{color:cyan}</style><h1>AC8：8张已签署，73条标注</h1><p>绿色person，橙色vehicle，紫色ignore。签署状态与覆盖质量分开；不是准确率报告，不启动训练。原始文件及旧标签不变。</p>'+''.join(cards))
