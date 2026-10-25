"""Close candidate dispositions, not human signatures or a training manifest."""
from collections import Counter
from copy import deepcopy
from html import escape
from pathlib import Path
import sys

from PIL import Image, ImageDraw

from cnn.import_verified_review import _box
from cnn.prepare_ac_correction import isolated
from cnn.prepare_ground48 import ROOT, read_json, sha256_file, write_json

OUT = Path(__file__).resolve().parent
POOL = ROOT / 'cnn/reports/virat_a_fill_20261012_v1/candidate_pool_128_64.json'
OLD = ROOT / 'cnn/reports/ac_pool_inventory_20261011_v1/candidate_pool.json'
EXPAND = ROOT / 'cnn/reports/virat_ac_expand_20261011_v1'
REPORT = OUT / 'closure_manifest_v2.json'


def screen():
    manifest = read_json(EXPAND / 'review_manifest_teacher.json')
    sources = []
    for start in range(0, 24, 4):
        page = Image.new('RGB', (1200, 4 * 280), 'white')
        d = ImageDraw.Draw(page)
        for row, sample in enumerate(manifest['samples'][start:start + 4]):
            for column, name in enumerate(('raw.png', 'ai_visual.png')):
                path = EXPAND / 'images' / sample['image_id'] / name
                with Image.open(path) as image:
                    crop = image.crop((160, 205, 360, 290)).resize((600, 255))
                page.paste(crop, (column * 600, row * 280 + 25))
                sources.append(dict(path=str(path), sha256=sha256_file(path)))
            d.text((5, row * 280 + 5), sample['legacy_id'] + ' RAW | AI DRAFT', fill='black')
        path = OUT / f'far_X{start+1:02d}_{start+4:02d}.png'
        assert not path.exists(), 'Preserve screening outputs'
        page.save(path)
    for key, sample, region in (
        ('parking_far', manifest['samples'][24], (1450, 210, 1920, 340)),
        ('X01_ignore', manifest['samples'][0], (760, 410, 1000, 720)),
    ):
        path = EXPAND / sample['raw_file']
        with Image.open(path) as image:
            crop = image.crop(region).resize(((region[2]-region[0])*2, (region[3]-region[1])*2))
        destination = OUT / (key + '.png')
        assert not destination.exists()
        crop.save(destination)
        sources.append(dict(path=str(path), sha256=sha256_file(path)))
    write_json(OUT / 'screen_inputs.json', sources)


def validate(rows):
    assert len(rows) == len({s['image_id'] for s in rows})
    assert len(rows) == len({s['source_sha256'] for s in rows})
    isolated(rows)
    for sample in rows:
        assert sha256_file(Path(sample['raw_file_absolute'])) == sample['source_sha256']
        for a in sample['labels']:
            assert a['class'] in ('person', 'vehicle', 'ignore')
            _box(a['bbox'], sample['width'], sample['height'], sample['image_id'])


def freeze_guard(rows):
    """No unsigned edits, unresolved regions or unknown isolation in an export."""
    validate(rows)
    assert rows and all(s['human_signature_valid'] and s.get('review_unchanged', False)
                        and not s.get('holds') and s.get('camera_evidence_verified', False)
                        for s in rows), 'Incomplete GT/isolation; freeze and training denied'


def build():
    decisions = read_json(OUT / 'decisions.json')
    pool, old = read_json(POOL), read_json(OLD)
    holds = {}
    for h in old['region_holds']:
        holds.setdefault(h['image_id'], []).append(h)
    rows = deepcopy(pool['images'])
    for s in rows:
        s['review_unchanged'] = True
        s['camera_evidence_verified'] = False  # No official/historical camera proof invented.
        s['holds'] = deepcopy(s.get('uncertain_regions', [])) + holds.get(s['image_id'], [])
        s['holds'].extend(deepcopy(decisions.get('additional_holds', {}).get(s['image_id'], [])))
        s['training_eligible'] = False
        if s['image_id'].startswith('VIRAT_S_050000_'):
            s['disposition'] = 'excluded_construction_dev_source'
        elif s['holds']:
            s['disposition'] = 'excluded_unresolved_supervision'
        elif not s['human_signature_valid']:
            s['disposition'] = 'unsigned_draft_not_GT'
        elif s['image_id'].startswith('mio_'):
            s['disposition'] = 'review_preserved_camera_metadata_pending'
        else:
            s['disposition'] = 'review_preserved_candidate_not_G_ready'
        s['label_changes'] = []
        for change in decisions.get('label_changes', {}).get(s['image_id'], []):
            assert not s['human_signature_valid'], 'Never modify a signed review in place'
            if change['action'] == 'N':
                assert change['reason'] and not any(a['target_id']==change['target_id'] for a in s['labels'])
                s['labels'].append(dict(change, ai_assisted=True))
            elif change['action'] == 'D':
                target = next(a for a in s['labels'] if a['target_id'] == change['target_id'])
                s['labels'].remove(target)
            else:
                assert change['action'] == 'M'
                target = next(a for a in s['labels'] if a['target_id'] == change['target_id'])
                target.update(change)
            s['label_changes'].append(change)
        # These are explicit AI resolutions, not inferred from a missing teacher box.
        resolved = decisions.get('resolved_regions', {}).get(s['image_id'], [])
        s['resolved_region_indices'] = resolved
        if resolved:
            assert len(resolved) == len(set(resolved))
            assert all(0 <= i < len(s['holds']) for i in resolved)
            s['holds'] = [h for i, h in enumerate(s['holds']) if i not in resolved]
        if not s['holds'] and s['disposition'] == 'excluded_unresolved_supervision':
            s['disposition'] = 'unsigned_draft_not_GT'
        s['review_unchanged'] = not s['label_changes']
    validate(rows)
    statistics = {}
    for split in ('train', 'dev'):
        local = [s for s in rows if s['split'] == split]
        statistics[split] = dict(images=len(local), dispositions=dict(Counter(s['disposition'] for s in local)))
    summary = dict(schema='ac_label_closure_v1', date_local='2026-10-13', images=rows,
        counts=statistics, decision_sha256=sha256_file(OUT/'decisions.json'),
        input_sha256={str(p):sha256_file(p) for p in (POOL, OLD, Path(__file__))},
        dataset_frozen=False, complete_GT_published=False, G_ready=False,
        E7_baseline_started=False, training_started=False,
        new_human_assignments=0,
        blockers=decisions['blockers'])
    summary['resolved_region_records'] = sum(len(s['resolved_region_indices']) for s in rows)
    summary['new_hold_records'] = sum(len(v) for v in decisions.get('additional_holds', {}).values())
    summary['modified_draft_boxes'] = sum(len(s['label_changes']) for s in rows)
    summary['preserved_review_counts'] = {
        split: dict(images=sum(s['split']==split and s['disposition']=='review_preserved_candidate_not_G_ready' for s in rows),
                    labels=dict(Counter(a['class'] for s in rows if s['split']==split and
                        s['disposition']=='review_preserved_candidate_not_G_ready' for a in s['labels'])))
        for split in ('train', 'dev')}
    assert not REPORT.exists(), 'Preserve prior closure'
    write_json(REPORT, summary)
    cards = []
    for case in decisions['visual_cases']:
        s = next(s for s in rows if s['image_id'] == case['image_id'])
        image = Image.open(s['raw_file_absolute']).convert('RGB')
        d = ImageDraw.Draw(image)
        for a in s['labels']:
            color = '#aaaaaa' if a['class'] == 'ignore' else '#00dd66' if a['class'] == 'person' else '#00ccff'
            d.rectangle(a['bbox'], outline=color, width=2)
            d.text(a['bbox'][:2], a['target_id']+' '+a['class'], fill=color, stroke_width=1, stroke_fill='black')
        path = OUT/('v2_'+case['key']+'.png')
        assert not path.exists()
        image.save(path)
        cards.append(f'<article><h2>{escape(case["key"])}</h2><p>{escape(case["finding"])}</p>'
            f'<p>{escape(s["disposition"])}</p><img src="{path.name}" alt="AI修订参考，不是GT">'
            f'<details><summary>无框原图</summary><img src="{Path(s["raw_file_absolute"]).as_uri()}" alt="无框原图"></details></article>')
    with (OUT/'index_v2.html').open('x', encoding='utf-8') as f:
        f.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>标签收口与排除依据</title>'
            '<style>body{font-family:system-ui;max-width:1280px;margin:auto}img{max-width:100%}article{border-bottom:2px solid #888;margin:24px 0}</style>'
            '<h1>标签收口与排除依据</h1><p>本页为AI判断记录，不是新增逐张人工审核任务。未冻结完整GT、未测E7、未启动训练。原图及历史审核文件不变。</p>'
            + ''.join(cards) + '</html>')
    check()


def check():
    report = read_json(REPORT)
    for path, digest in report['input_sha256'].items():
        assert sha256_file(Path(path)) == digest, path
    assert sha256_file(OUT/'decisions.json') == report['decision_sha256']
    validate(report['images'])
    assert len(report['images']) == 192 and not report['G_ready']
    # Negative regression: the complete candidate pool may never pass the export gate.
    try:
        freeze_guard(report['images'])
    except AssertionError:
        pass
    else:
        raise AssertionError('Draft pool passed freeze guard')
    # Isolate the unsigned-label failure, rather than relying on another failed field.
    unsigned = deepcopy(next(s for s in report['images'] if not s['human_signature_valid']))
    unsigned.update(holds=[], camera_evidence_verified=True, review_unchanged=True)
    try:
        freeze_guard([unsigned])
    except AssertionError:
        pass
    else:
        raise AssertionError('Unsigned image passed freeze guard')
    print('PASS192 hashes/coordinates/reservations; draft freeze rejected; no training')
    print(report['counts'])


if __name__ == '__main__':
    assert sys.argv[1:] in (['screen'], ['build'], ['check'])
    globals()[sys.argv[1]]()
