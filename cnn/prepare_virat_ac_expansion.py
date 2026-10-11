"""Bounded 54-frame source/teacher draft, with no human assignment or training."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from html import escape
import io
from pathlib import Path
import time

import cv2
from PIL import Image, ImageDraw

from . import prepare_ac_next8 as assets
from .prepare_ac_correction import isolated
from .prepare_ground48 import ROOT, blank_patch, dataset_id, read_json, sha256_file, write_json

OUT = ROOT/'cnn/reports/virat_ac_expand_20261011_v1'
POOL = ROOT/'cnn/reports/ac_pool_inventory_20261011_v1/candidate_pool.json'
NEW = ROOT/'cnn/data/virat_ac_expand_source_20261011_v1'
PARK = ROOT/'cnn/data/virat_ai12_source_20261010_v1'
CLIPS = (
    ('VIRAT_S_010204_05_000856_000890', NEW, 'train', 'A', 24,
     'VIRAT-0102xx-train-only-provisional'),
    ('VIRAT_S_040000_00_000063_000085', PARK, 'train', 'C', 18,
     'VIRAT-0400xx-train-only-provisional'),
    ('VIRAT_S_000200_00_000100_000171', ROOT/'public_data/raw/virat_ground_v2/video_original',
     'dev', 'C', 12, 'virat-parking-lot-camera-a'),
)


def selected_frames(total, count, excluded):
    frames = [(i+1)*(total-1)//(count+1) for i in range(count)]
    assert len(set(frames)) == count and not set(frames) & excluded, 'Selection collision; stop, do not silently shift'
    return frames


def validate_samples(samples, previous):
    all_rows = samples + previous
    assert len(all_rows) == len({s['image_id'] for s in all_rows}), 'Duplicate image ID'
    assert len(all_rows) == len({s['source_sha256'] for s in all_rows}), 'Duplicate image pixels'
    isolated(all_rows)  # Reservations are not a claim of authoritative camera identity.


def build():
    assert not (OUT/'manifest_original.json').exists() and not (OUT/'images').exists()
    pool = read_json(POOL)
    previous_ids = {s['image_id'] for s in pool['images'] + pool['pending_unsigned']}
    catalog = read_json(ROOT/'evaluation/public_data/virat_ground_v2/catalog.json')
    protected = {str(POOL): sha256_file(POOL)}
    for name in ('model.py', 'annotation_policy_v1.md', 'teacher.py', 'build_verified_review.py', 'dataset.py'):
        p = ROOT/'cnn'/name
        protected[str(p)] = sha256_file(p)
    samples, source_receipts = [], []
    OUT.mkdir(exist_ok=True)
    assets.OUT = OUT
    for clip, directory, split, scene, count, family in CLIPS:
        video = directory/(clip+'.mp4')
        labels = directory/(clip+'.viratdata.objects.txt')
        if split == 'dev':
            row = next(c for c in catalog['clips'] if c['clip_id'] == clip)
            labels = Path(row['annotation_path'])
            assert sha256_file(video) == row['video_sha256']
            assert sha256_file(labels) == row['annotation_sha256']
        else:
            for p in (video, labels):
                receipt = p.with_suffix(p.suffix+'.receipt.json')
                assert sha256_file(p) == read_json(receipt)['sha256']
                protected[str(receipt)] = sha256_file(receipt)
        for p in (video, labels):
            protected[str(p)] = sha256_file(p)
        rows = [(i, list(map(int, line.split()))) for i, line in enumerate(labels.read_text().splitlines(), 1)]
        assert all(len(row) == 8 for _, row in rows)
        cap = cv2.VideoCapture(str(video))
        assert cap.isOpened()
        total, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
        assert fps > 0 and total > count
        excluded = {int(s.rsplit('_f', 1)[1]) for s in previous_ids if s.startswith(clip+'_f')}
        frames = selected_frames(total, count, excluded)
        source_receipts.append(dict(clip=clip, split=split, scene=scene, family=family, frame_count=total,
            fps=fps, selected_frames=frames, selected_unique_person_tracks=len({r[0] for _, r in rows if r[2] in frames and r[7] == 1}),
            annotation_outside_video_rows=[line for line, r in rows if not 0 <= r[2] < total],
            note='Timeline sampling before inference; repeated people/cars are not independent targets'))
        for frame in frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, bgr = cap.read()
            assert ok and abs(cap.get(cv2.CAP_PROP_POS_FRAMES)-(frame+1)) < .5
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            height, width = rgb.shape[:2]
            originals = []
            for line, row in rows:
                track, duration, f, x, y, w, h, kind = row
                if f != frame:
                    continue
                assert 0 <= x < x+w <= width and 0 <= y < y+h <= height, (clip, line)
                originals.append(dict(target_id=f'o{len(originals)+1}', source_target_id=f'{labels.name}:{line}',
                    source_category=kind, **{'class': 'person' if kind == 1 else 'vehicle' if kind in (2, 3) else 'ignore'},
                    bbox=[x, y, x+w, y+h], source_record=dict(line=line, row=row),
                    certified_project_ignore=False))
            buffer = io.BytesIO()
            Image.fromarray(rgb).save(buffer, format='PNG')
            buffer.seek(0)
            sample = assets.make_sample(f'{clip}_f{frame:07d}', buffer, originals, split, family, family,
                'https://viratdata.org/', dict(video=str(video), video_sha256=protected[str(video)],
                    annotations=str(labels), annotations_sha256=protected[str(labels)], frame_index=frame,
                    frame_origin='zero_based', fps=fps, full_static_GT_available=False))
            sample.update(scene=scene, legacy_id=f'X{len(samples)+1:02d}', training_eligible=False,
                human_complete=False, complete_GT_published=False,
                scene_basis='fixed oblique campus entrance/walkway' if scene == 'A' else 'parking/access lane',
                visual_review_status='not_individually_inspected', physical_camera_verified=False)
            samples.append(sample)
        cap.release()
    validate_samples(samples, pool['images'])
    m = dict(schema='cnn_review_workbench_v1', samples=samples, train_required_count=42,
        bucket_counts={'train_review': 42, 'road_development': 12},
        annotation_policy_sha256=sha256_file(ROOT/'cnn/annotation_policy_v1.md'),
        verified_gt=False, dataset_frozen=False, G_ready=False, training_started=False,
        human_signed_frames=0, new_human_assignments=0, source_receipts=source_receipts)
    m['dataset_id'] = dataset_id(m)
    write_json(OUT/'manifest_original.json', m)
    write_json(OUT/'source_bindings.json', protected)
    write_json(OUT/'source_investigation.json', dict(new_public_camera_families_investigated=2,
        usable_new_camera_family='0102xx', second_family='0502xx',
        second_family_status='stopped: both checked official objects.txt items returned empty file lists',
        empty_file_item_ids=['56f5819a8d777f753209c892', '56f5819b8d777f753209c8aa'],
        no_more_source_search_in_this_batch=True, additional_human_assignment=False))
    print('Built 54 new candidates: A-train24, C-train18, C-dev12; no verified GT', flush=True)


def teacher():
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads, json_hash, load_official_model, teacher_input, tree_hash
    m = read_json(OUT/'manifest_original.json')
    assert not (OUT/'teacher_receipt.json').exists()
    assets_dir = ROOT/'cnn/teacher_assets'
    receipt = read_json(assets_dir/'receipt.json')
    weights, source = assets_dir/'yolox_s.pth', assets_dir/'source/YOLOX-0.3.0'
    assert sha256_file(weights) == receipt['weights']['sha256']
    assert tree_hash(source/'yolox') == receipt['source_tree_sha256']
    config = dict(dataset_id=m['dataset_id'], device='cpu', input='1024x576_FP32_BGR', confidence=.1,
        nms_iou=.6, weights_sha256=sha256_file(weights), source_tree_sha256=receipt['source_tree_sha256'],
        code_sha256={str(p):sha256_file(p) for p in (Path(__file__), ROOT/'cnn/teacher.py', ROOT/'cnn/build_verified_review.py', ROOT/'cnn/dataset.py')})
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    device = torch.device('cpu')
    model = load_official_model(source, weights, device)
    start = time.perf_counter()
    for i, s in enumerate(m['samples'], 1):
        cache = OUT/'images'/s['image_id']/'teacher.json'
        if cache.exists():
            saved = read_json(cache)
            assert saved['config_sha256'] == json_hash(config) and saved['image_sha256'] == s['source_sha256']
            continue
        transform = _letterbox_transform(s['width'], s['height'])
        row = dict(image_path=OUT/s['raw_file'], preprocess=dict(raw_image=True, letterbox_1280x720=transform))
        assert sha256_file(row['image_path']) == s['source_sha256']
        predictions = decode_heads(capture_raw_heads(model, teacher_input(row, device)), transform)
        for j, p in enumerate(predictions):
            p.update(candidate_id=f't{j}', kind='AI_HINT_NOT_GT')
        write_json(cache, dict(config_sha256=json_hash(config), image_sha256=s['source_sha256'], predictions=predictions))
        print(i, '/', len(m['samples']), s['legacy_id'], len(predictions), 'CPU hints', flush=True)
    write_json(OUT/'teacher_receipt.json', dict(config=config, config_sha256=json_hash(config),
        seconds_this_invocation=time.perf_counter()-start, images=len(m['samples']), GPU_used=False, training_started=False))


def draw():
    from .build_verified_review import overlap
    from .dataset import _letterbox_720
    from .integer import resize_area
    import numpy as np
    m = read_json(OUT/'manifest_original.json')
    receipt = read_json(OUT/'teacher_receipt.json')
    patch = blank_patch(m)
    cards = []
    for s, review in zip(m['samples'], patch['reviews'], strict=True):
        cached = read_json(OUT/'images'/s['image_id']/'teacher.json')
        assert cached['config_sha256'] == receipt['config_sha256']
        assert cached['image_sha256'] == s['source_sha256']
        s['teacher'] = cached['predictions']
        for obj in s['original']:
            review['actions'].append(dict(target_id=obj['target_id'], action='A', **{'class':obj['class']},
                bbox=obj['bbox'], ai_assisted=True, reason='Source reference retained in unsigned draft; ignore semantics unverified'))
        for p in s['teacher']:
            if p['score'] >= .25 and not any(a['class'] == p['class'] and overlap(a['bbox'], p['bbox']) > .3 for a in review['actions']):
                review['actions'].append(dict(target_id='teacher_'+p['candidate_id'], action='N',
                    **{'class':p['class']}, bbox=p['bbox'], ai_assisted=True,
                    reason=f"Unmatched teacher {p['candidate_id']} score {p['score']:.4f}; proposal only, not GT"))
        raw = Image.open(OUT/s['raw_file']).convert('RGB')
        image = raw.copy()
        d = ImageDraw.Draw(image)
        for a in review['actions']:
            color = '#00c8ff' if a['action'] == 'N' else '#aaaaaa' if a['class'] == 'ignore' else '#00dd66'
            d.rectangle(a['bbox'], outline=color, width=2)
            d.text(a['bbox'][:2], a['target_id']+' '+a['class'], fill=color, stroke_width=1, stroke_fill='black')
        folder = OUT/'images'/s['image_id']
        image.save(folder/'ai_draft.png')
        canvas, transform = _letterbox_720(np.asarray(raw))
        Image.fromarray(resize_area(canvas)).save(folder/'network.png')
        s['preprocess_transform'] = transform
        cards.append(f'<article><h2>{escape(s["legacy_id"])} {escape(s["split"])} / {s["scene"]}</h2>'
            f'<p>{escape(s["image_id"])} — 未签署草稿</p><img src="images/{s["image_id"]}/ai_draft.png" alt="候选框">'
            f'<details><summary>无框原图</summary><img src="{s["raw_file"]}" alt="无框原图"></details>'
            f'<details><summary>实际512输入</summary><img src="images/{s["image_id"]}/network.png" alt="512输入"></details></article>')
    write_json(OUT/'review_manifest_teacher.json', m)
    write_json(OUT/'ai_draft_patch.json', patch)
    counts = {split: dict(images=sum(s['split'] == split for s in m['samples']),
        proposed_boxes=dict(Counter(a['class'] for s, r in zip(m['samples'], patch['reviews'], strict=True) if s['split'] == split for a in r['actions'])))
        for split in ('train', 'dev')}
    write_json(OUT/'draft_status.json', dict(status='automatic_source_plus_teacher_drafts_not_verified_GT', counts=counts,
        source_positive_boxes=sum(a['action'] == 'A' and a['class'] != 'ignore' for r in patch['reviews'] for a in r['actions']),
        teacher_added_proposals=sum(a['action'] == 'N' for r in patch['reviews'] for a in r['actions']),
        individually_visually_reviewed_frames=0, human_signed_new_frames=0, new_human_assignments=0,
        training_started=False, G_ready=False, dataset_frozen=False,
        note='Source/teacher disagreement is an audit hint, not measured student FP/FN. No background supervision inferred.'))
    with (OUT/'index.html').open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>A/C扩充54图：AI候选</title>'
            '<style>body{font-family:system-ui;max-width:1280px;margin:auto}article{border-bottom:2px solid #888;margin:30px 0}img{max-width:100%}summary{cursor:pointer}</style>'
            '<h1>A/C扩充54图：无需你现在审核</h1><p>绿框＝来源参考；青框＝教师新增候选；灰框＝来源未决区域。'
            '均非已确认GT。不要求签署，不启动训练。训练42张（A24/C18），开发候选12张（C）。同片邻帧有相关性。</p>'+''.join(cards)+'</html>')
    for start in range(0, len(m['samples']), 4):
        sheet = Image.new('RGB', (1536, 928), 'white')
        for j, s in enumerate(m['samples'][start:start+4]):
            image = Image.open(OUT/'images'/s['image_id']/'ai_draft.png')
            image.thumbnail((768, 432))
            x, y = j % 2 * 768, j // 2 * 464
            sheet.paste(image, (x, y+30))
            ImageDraw.Draw(sheet).text((x+5, y+5), s['legacy_id']+' '+s['split']+' '+s['scene'], fill='black')
        sheet.save(OUT/f'ai_{start+1:02d}_{min(start+4,len(m["samples"])):02d}.jpg', quality=95)
    print(counts, flush=True)


def check():
    from .import_verified_review import _validate_patch
    m = read_json(OUT/'review_manifest_teacher.json')
    assert dataset_id(m) == m['dataset_id']
    assert Counter((s['split'], s['scene']) for s in m['samples']) == {('train','A'):24, ('train','C'):18, ('dev','C'):12}
    validate_samples(m['samples'], read_json(POOL)['images'])
    for p, digest in read_json(OUT/'source_bindings.json').items():
        assert sha256_file(Path(p)) == digest, p
    for s in m['samples']:
        assert sha256_file(OUT/s['raw_file']) == s['source_sha256']
        assert not s['training_eligible'] and not s['human_complete']
    _, reviews, _ = _validate_patch(OUT/'ai_draft_patch.json', m, {s['image_id']:s for s in m['samples']})
    assert not any(r['complete'] or r['reviewed_at_utc'] for r in reviews.values())
    leaked = dict(m['samples'][0], image_id='negative_camera_leak', source_sha256='0'*64, split='dev')
    for bad in (m['samples'] + [m['samples'][0]], [leaked]):
        try:
            validate_samples(bad, [m['samples'][0]])
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError('Duplicate/cross-split input accepted')
    evidence = dict(status='passed_bounded_file_checks_not_visual_truth',
        command='python -B -m cnn.prepare_virat_ac_expansion check', script_sha256=sha256_file(Path(__file__)),
        files={name:sha256_file(OUT/name) for name in ('manifest_original.json','review_manifest_teacher.json','ai_draft_patch.json','teacher_receipt.json','draft_status.json','index.html')},
        training_started=False, new_human_assignments=0, complete_GT_published=False, browser_interaction_verified=False)
    if (OUT/'verification.json').exists():
        assert read_json(OUT/'verification.json') == evidence
    else:
        write_json(OUT/'verification.json', evidence)
    print('PASS: 54 unique raw frames, reserved splits, original inputs unchanged, valid unsigned draft; no GT or training')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build', 'teacher', 'draw', 'check'))
    globals()[parser.parse_args().action]()
