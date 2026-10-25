"""Apply recorded visual edits to an unsigned draft; preserve all source/cache files."""
from collections import Counter
from copy import deepcopy
from html import escape
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw

from .prepare_ground48 import ROOT, read_json, sha256_file, write_json
from .import_verified_review import _box, _validate_patch

OUT = ROOT / 'cnn/reports/virat_ac_expand_20261011_v1'
EDITS = OUT / 'assistant_visual_edits.json'
PATCH = OUT / 'ai_visual_patch.json'
PAGE = OUT / 'visual_index.html'
REPORT = OUT / 'visual_status.json'
INPUTS = ('manifest_original.json', 'review_manifest_teacher.json', 'ai_draft_patch.json',
          'teacher_receipt.json', 'draft_status.json', 'index.html', 'verification.json')


def corrected(manifest, patch, edits):
    result = deepcopy(patch)
    assert set(edits['images']) == {s['legacy_id'] for s in manifest['samples']}
    for sample, review in zip(manifest['samples'], result['reviews'], strict=True):
        assert sample['image_id'] == review['image_id']
        edit = edits['images'][sample['legacy_id']]
        actions = {a['target_id']: a for a in review['actions']}
        originals = {a['target_id'] for a in sample['original']}
        for target, reason in edit.get('remove', {}).items():
            assert reason and target in actions and target not in originals
            del actions[target]
        for target, reason in edit.get('delete_source', {}).items():
            assert reason and target in actions and target in originals
            actions[target].update(action='D', reason=reason)
        for target, change in edit.get('modify', {}).items():
            assert target in actions and change['reason']
            actions[target].update(change)
            actions[target]['action'] = 'M' if target in originals else 'N'
        for index, addition in enumerate(edit.get('add', []), 1):
            target = f'ai_visual_{index}'
            assert target not in actions and addition['reason']
            actions[target] = dict(addition, target_id=target, action='N', ai_assisted=True)
        for region in edit.get('uncertain', []):
            _box(region['bbox'], sample['width'], sample['height'], sample['legacy_id'])
            assert region['reason']
        review['actions'] = list(actions.values())
        review['notes'] = edit['note'] + ''.join('\n待定：'+u['reason'] for u in edit.get('uncertain', []))
        assert not review['complete'] and not review['raw_seen'] and not review['reviewer']
    result['provenance'] = dict(kind='AI_visual_unsigned_draft', edits_sha256=sha256_file(EDITS),
                               uncertain_regions_file=EDITS.name, human_signed_frames=0,
                               unresolved_regions_are_not_background=True)
    return result


def build():
    assert not any(p.exists() for p in (PATCH, PAGE, REPORT)), 'Existing revision must be preserved'
    manifest = read_json(OUT / 'review_manifest_teacher.json')
    edits = read_json(EDITS)
    assert edits['dataset_id'] == manifest['dataset_id']
    hashes = {name: sha256_file(OUT / name) for name in INPUTS}
    revised = corrected(manifest, read_json(OUT / 'ai_draft_patch.json'), edits)
    write_json(PATCH, revised)
    _validate_patch(PATCH, manifest, {s['image_id']: s for s in manifest['samples']})
    cards, counts = [], Counter()
    for sample, review in zip(manifest['samples'], revised['reviews'], strict=True):
        edit = edits['images'][sample['legacy_id']]
        with Image.open(OUT / sample['raw_file']) as original:
            image = original.convert('RGB')
        draw = ImageDraw.Draw(image)
        for action in review['actions']:
            if action['action'] == 'D':
                continue
            counts[action['class']] += 1
            color = '#00dd66' if action['action'] == 'A' else '#00c8ff'
            if action['class'] == 'ignore':
                color = '#aaaaaa'
            draw.rectangle(action['bbox'], outline=color, width=2)
            draw.text(action['bbox'][:2], action['target_id']+' '+action['class'],
                      fill=color, stroke_width=1, stroke_fill='black')
        for index, region in enumerate(edit.get('uncertain', []), 1):
            draw.rectangle(region['bbox'], outline='#ffaa00', width=2)
            draw.text(region['bbox'][:2], f'uncertain{index}', fill='#ffaa00', stroke_width=1, stroke_fill='black')
        relative = f'images/{sample["image_id"]}/ai_visual.png'
        assert not (OUT / relative).exists()
        image.save(OUT / relative)
        cards.append(f'<article><h2>{sample["legacy_id"]} {sample["split"]} / {sample["scene"]}</h2>'
                     f'<p>{escape(edit["note"])}</p><img src="{relative}" alt="AI修订候选框">'
                     f'<details><summary>无框原图</summary><img src="{sample["raw_file"]}" alt="原图"></details>'
                     f'<details><summary>实际512输入</summary><img src="images/{sample["image_id"]}/network.png" alt="网络输入"></details></article>')
    with PAGE.open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>A/C 54图：AI初查修订</title>'
                     '<style>body{font-family:system-ui;max-width:1280px;margin:auto}article{border-bottom:2px solid #888;margin:30px 0}img{max-width:100%}summary{cursor:pointer}</style>'
                     '<h1>A/C 54图：AI初查修订预览</h1><p>绿色＝来源参考；青色＝AI补充/修订；橙色＝待定区域；灰色＝尚未核实的来源ignore。'
                     '保留编号和类别。全部仍是未签署草稿，待定区域不是背景或已确认ignore。本页不分配新增人工审核任务。</p>'
                     '<p>候选用途：A训练24图、C训练18图、C开发12图。同片帧有相关性；尚未冻结训练集、未启动训练。</p>'
                     + ''.join(cards) + '</html>')
    write_json(REPORT, dict(status='AI_visual_first_pass_unsigned', images=54, proposed_boxes=dict(counts),
                           script_sha256=sha256_file(Path(__file__)),
                           input_sha256=hashes, edits_sha256=sha256_file(EDITS),
                           patch_sha256=sha256_file(PATCH), page_sha256=sha256_file(PAGE),
                           inspection=edits['inspection'],
                           removed_teacher_proposals=sum(len(e.get('remove', {})) for e in edits['images'].values()),
                           deleted_source_proposals=sum(len(e.get('delete_source', {})) for e in edits['images'].values()),
                           modified_boxes=sum(len(e.get('modify', {})) for e in edits['images'].values()),
                           added_boxes=sum(len(e.get('add', [])) for e in edits['images'].values()),
                           uncertain_regions=sum(len(e.get('uncertain', [])) for e in edits['images'].values()),
                           human_signed_new_frames=0, new_human_assignments=0,
                           dataset_frozen=False, G_ready=False, training_started=False))


def check():
    manifest, edits, report = (read_json(p) for p in (OUT / 'review_manifest_teacher.json', EDITS, REPORT))
    assert sha256_file(Path(__file__)) == report['script_sha256']
    for name, digest in report['input_sha256'].items():
        assert sha256_file(OUT / name) == digest, name
    assert read_json(PATCH) == corrected(manifest, read_json(OUT / 'ai_draft_patch.json'), edits)
    _validate_patch(PATCH, manifest, {s['image_id']: s for s in manifest['samples']})
    for field, path in [('edits_sha256', EDITS), ('patch_sha256', PATCH), ('page_sha256', PAGE)]:
        assert report[field] == sha256_file(path)
    links = re.findall(r'<img src="([^"]+)"', PAGE.read_text(encoding='utf-8'))
    assert len(links) == 162 and all((OUT / p).is_file() for p in links)
    bad = deepcopy(edits)
    bad['images']['X01']['remove'] = {'missing_target': 'negative check'}
    try:
        corrected(manifest, read_json(OUT / 'ai_draft_patch.json'), bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Unknown target accepted')
    print('PASS: unsigned edits, coordinates, immutable sources, 162 preview links, invalid-target rejection')


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['check'])
    if sys.argv[1] == 'build':
        build()
    check()
