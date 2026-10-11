"""Eight-frame A/C annotation-cost pilot; never exports a training dataset."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

import numpy as np
from PIL import Image

from .prepare_ground48 import (ROOT, blank_patch, dataset_id, read_json,
                               render_workbench, sha256_file, write_json)


SCREEN = ROOT / 'cnn/reports/ac_source_screen_20261009_v1'
GROUND = ROOT / 'cnn/reports/post_review_s_20261007_v1/ground48'
OUT = ROOT / 'cnn/reports/ac_correction_pilot8_20261009_v2'
IDS = (
    'epfl_c5_o040', 'epfl_c2_o160',
    'VIRAT_S_000200_00_000100_000171_f0001376',
    'VIRAT_S_010107_02_000282_000312_f0000249',
    'epfl_c0_o040', 'epfl_c0_o160', 'epfl_c5_o160', 'epfl_c2_o040',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def isolated(samples):
    for field in ('family_id', 'camera_id'):
        groups = defaultdict(set)
        for sample in samples:
            require(bool(sample.get(field)), f'missing {field}')
            groups[sample[field]].add(sample['split'])
        require(all(len(splits) == 1 for splits in groups.values()), f'{field} crosses splits')


def protected_files():
    return [SCREEN / 'screening_manifest.json', SCREEN / 'index.html',
            SCREEN / 'pilot_freeze_status.json', GROUND / 'review_manifest_teacher.json',
            GROUND / 'index.html', ROOT / 'cnn/annotation_policy_v1.md',
            ROOT / 'cnn/review_workbench.html', ROOT / 'cnn/prepare_ground48.py',
            ROOT / 'cnn/ground48_teacher_batch.js',
            ROOT / 'cnn/reports/scene_view_choice_20261009_v1/confirmed_preferences.json',
            ROOT / 'cnn/releases/RoadYOLO-S4-512_20261009_before_ground_adapt/ancestral_e7/cnn/runs/person_native_recovery_20261004/epoch_0006.pt']


def build():
    require(not OUT.exists(), 'Preserve existing correction package; no overwrite')
    screened = read_json(SCREEN / 'screening_manifest.json')
    require(not screened['dataset_frozen'], 'Unexpected source freeze state')
    source = {row['candidate_id']: row for row in screened['frames']}
    old_ground = read_json(GROUND / 'review_manifest_teacher.json')
    ground = {row['image_id']: row for row in old_ground['samples']}
    hashes = {str(path): sha256_file(path) for path in protected_files()}
    OUT.mkdir()
    shutil.copy2(ROOT / 'cnn/annotation_policy_v1.md', OUT / 'annotation_policy_v1.md')
    samples = []
    for index, image_id in enumerate(IDS):
        row = source[image_id]
        directory = OUT / 'images' / image_id
        directory.mkdir(parents=True)
        for key, filename in (('raw', 'raw.png'), ('source_boxes', 'source_overlay.png')):
            asset = row['assets'][key]
            require(sha256_file(Path(asset['path'])) == asset['sha256'], 'Screen asset changed')
            shutil.copy2(asset['path'], directory / filename)
        width, height = row['size']
        is_epfl = image_id.startswith('epfl_')
        if is_epfl:
            originals = [dict(target_id=f'o{n}', source_target_id=f"{box['member']}:{box['row']}",
                              source_category=box['source_class'],
                              **{'class': 'person' if box['source_class'] == 'person' else 'vehicle'},
                              bbox=box['xyxy_raw'], source_record=box)
                         for n, box in enumerate(row['boxes'], 1)]
            teachers = []
            coordinate_note = 'EPFL原值仅作参考；尚无官方坐标原点约定。请核对/重画，不能自动视为真值。'
        else:
            original = ground[image_id]
            old_raw = GROUND / original['raw_file']
            require(sha256_file(old_raw) == original['source_sha256'] == row['source_sha256'], 'VIRAT identity mismatch')
            # Screening PNG was re-encoded; cached hints require identical decoded pixels, not an invented equal byte hash.
            with Image.open(old_raw) as old_image, Image.open(directory / 'raw.png') as new_image:
                require(np.array_equal(np.asarray(old_image.convert('RGB')), np.asarray(new_image.convert('RGB'))),
                        'VIRAT cached teacher pixels differ')
            originals, teachers = deepcopy(original['original']), deepcopy(original['teacher'])
            coordinate_note = '沿用已核对VIRAT坐标转换；仍需检查全帧漏标、停放车辆和重复框。'
        sample = dict(image_id=image_id, legacy_id=f'ac{index+1:02d}',
                      bucket='train_review' if is_epfl else 'road_development',
                      split='train' if is_epfl else 'dev',
                      split_status='proposed_family_reservation_not_dataset_freeze',
                      scene=row['scene'], family_id=row['family_id'], camera_id=row['camera_id'],
                      source_url=row['source_url'], source_record=row,
                      width=width, height=height,
                      raw_file=f'images/{image_id}/raw.png',
                      gt_overlay_file=f'images/{image_id}/source_overlay.png',
                      source_sha256=row['assets']['raw']['sha256'],
                      original=originals, teacher=teachers,
                      teacher_status='pending_CPU_hints' if is_epfl else 'reused_existing_hints_not_truth',
                      teacher_source_manifest_sha256=None if is_epfl else hashes[str(GROUND / 'review_manifest_teacher.json')],
                      warnings=[coordinate_note, '骑行者分别标人体和车体；可辨认小目标/静止车不能自动忽略。'],
                      review_score=0, review_batch=1 if index < 4 else 2,
                      review_batch_ordinal=index % 4 + 1)
        samples.append(sample)
    isolated(samples)
    manifest = dict(schema='cnn_review_workbench_v1', annotation_policy_sha256=sha256_file(OUT / 'annotation_policy_v1.md'),
                    samples=samples, train_required_count=6,
                    bucket_counts={'train_review': 6, 'road_development': 2},
                    teacher_status='EPFL待CPU预画；VIRAT复用已有候选；均非GT',
                    verified_gt=False, dataset_frozen=False, G_ready=False,
                    training_started=False, human_signed_frames=0, formal_acceptance=False,
                    purpose='annotation workload/coverage pilot, not an accuracy dataset',
                    split_note='EPFL synchronized family reserved train only; existing VIRAT cameras remain dev. No qualified A dev yet.')
    manifest['dataset_id'] = dataset_id(manifest)
    write_json(OUT / 'review_manifest_cached.json', manifest)
    frozen = deepcopy(manifest)
    for sample in frozen['samples']:
        sample['teacher'] = []
    write_json(OUT / 'manifest_original.json', frozen)
    write_json(OUT / 'review_patch_template.json', blank_patch(manifest))
    write_json(OUT / 'source_bindings.json', hashes)
    render(manifest)
    print('Built 8-frame draft, first batch4; no training data published', flush=True)


def teacher():
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads, json_hash, load_official_model, teacher_input, tree_hash
    require(not (OUT / 'review_manifest_teacher.json').exists(), 'Teacher manifest already exists')
    manifest = read_json(OUT / 'review_manifest_cached.json')
    assets = ROOT / 'cnn/teacher_assets'
    receipt = read_json(assets / 'receipt.json')
    source, weights = assets / 'source/YOLOX-0.3.0', assets / 'yolox_s.pth'
    require(sha256_file(weights) == receipt['weights']['sha256'], 'Teacher weight changed')
    require(tree_hash(source / 'yolox') == receipt['source_tree_sha256'], 'Teacher source changed')
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    device = torch.device('cpu')
    config = dict(device='cpu', threads=2, input='1024x576 FP32 official BGR',
                  confidence=.1, nms_iou=.6, candidate_cap=None,
                  coordinate='native half-open XYXY, hints only', dataset_id=manifest['dataset_id'],
                  weight_sha256=receipt['weights']['sha256'], tree_sha256=receipt['source_tree_sha256'],
                  decoder_sha256=sha256_file(ROOT / 'cnn/build_verified_review.py'),
                  teacher_sha256=sha256_file(ROOT / 'cnn/teacher.py'),
                  dataset_source_sha256=sha256_file(ROOT / 'cnn/dataset.py'),
                  tool_sha256=sha256_file(Path(__file__)), torch_version=torch.__version__)
    model = load_official_model(source, weights, device)
    destination = OUT / 'teacher_predictions'
    destination.mkdir(exist_ok=True)
    start = time.perf_counter()
    for sample in manifest['samples']:
        if not sample['image_id'].startswith('epfl_'):
            continue
        path = OUT / sample['raw_file']
        require(sha256_file(path) == sample['source_sha256'], 'Raw image changed')
        target = destination / (sample['image_id'] + '.json')
        if target.exists():
            saved = read_json(target)
            require(saved['config_sha256'] == json_hash(config) and saved['source_sha256'] == sample['source_sha256'],
                    'Existing partial teacher hints have different bindings')
            predictions = saved['predictions']
        else:
            transform = _letterbox_transform(sample['width'], sample['height'])
            row = dict(image_path=path, preprocess=dict(raw_image=True, letterbox_1280x720=transform))
            predictions = decode_heads(capture_raw_heads(model, teacher_input(row, device)), transform)
            for n, prediction in enumerate(predictions):
                prediction.update(candidate_id=f't{n}', kind='REVIEW_HINT_NOT_ERROR_OR_GT')
            write_json(target, dict(image_id=sample['image_id'], source_sha256=sample['source_sha256'],
                                    config_sha256=json_hash(config), predictions=predictions))
        sample.update(teacher=predictions, teacher_status='CPU_hints_only_not_truth')
        print(f"CPU teacher {sample['image_id']}: {len(predictions)} hints, elapsed {time.perf_counter()-start:.1f}s", flush=True)
    manifest['teacher_status'] = 'EPFL六张CPU预画＋VIRAT两张历史缓存；候选非GT，不能当真实误报'
    require(dataset_id(manifest) == manifest['dataset_id'], 'Hints altered source binding')
    write_json(OUT / 'review_manifest_teacher.json', manifest)
    write_json(OUT / 'teacher_receipt.json', dict(config=config, new_CPU_images=6, reused_VIRAT_images=2,
                elapsed_seconds=time.perf_counter()-start, GPU_used=False, training_started=False,
                original_labels_changed=False, human_signed_frames=0,
                per_image_hint_counts={s['image_id']: len(s['teacher']) for s in manifest['samples']},
                prediction_sha256={p.name: sha256_file(p) for p in sorted(destination.glob('*.json'))}))
    render(manifest)


def replace_once(text, old, new):
    require(text.count(old) == 1, f'UI anchor missing/duplicated: {old[:80]}')
    return text.replace(old, new, 1)


def render(manifest):
    # ponytail: reuse the existing signed-review UI; this adapter is intentionally fixed at8, not a generic review builder.
    page = render_workbench((ROOT / 'cnn/review_workbench.html').read_text(encoding='utf-8'), manifest)
    page = page.replace('RoadYOLO Ground48 分批人工审核台', 'RoadYOLO A/C 8张补标试点')
    page = replace_once(page, '<label>批次 <select id="bucket">\n    <option value="1">第 1 批（12 张）</option>\n    <option value="2">第 2 批（12 张）</option>\n    <option value="3">第 3 批（12 张）</option>\n    <option value="4">第 4 批（12 张）</option>\n    <option value="all">全部 48 张</option>\n  </select></label>',
                        '<label>批次 <select id="bucket"><option value="1">先做这4张</option><option value="2">第二批4张（可暂缓）</option><option value="all">全部8张</option></select></label>')
    page = replace_once(page, 'if (manifest.train_required_count !== 0) errors.push("ground48 train_required_count 必须为 0");',
                        'if (manifest.train_required_count !== 6) errors.push("AC8 candidate train count must be6");')
    page = replace_once(page, 'if (manifest.samples.length !== 48) errors.push("ground48 samples 必须固定为 48 张");',
                        'if (manifest.samples.length !== 8) errors.push("AC8 samples must be8");')
    page = replace_once(page, 'if (counts.train_review !== 0 || counts.road_development !== 48 || counts.person_background_aux !== 0) errors.push("ground48 桶数量必须为 0/48/0");',
                        'if (counts.train_review !== 6 || counts.road_development !== 2 || counts.person_background_aux !== 0) errors.push("AC8 candidate buckets must be6/2/0");')
    page = replace_once(page, '${item.review_batch_ordinal}/12', '${item.review_batch_ordinal}/4')
    page = replace_once(page, 'GT 来源框</button>', '来源参考框（未核实GT）</button>')
    page = replace_once(page, '<main id="app" hidden>',
                        '<p style="max-width:1400px;margin:12px auto;padding:0 18px">只做第一批4张即可导出，未完成图保持草稿。绿色是来源参考、橙色是教师候选、青色是你的修订。EPFL来源坐标约定未确认，请按原图核对或重画；不得因教师没框就删掉目标。<a href="操作说明.txt">具体操作与本图要补什么</a>。刷新/关闭前请导出JSON；本页不自动保存，不启动训练，也不冻结数据。</p><main id="app" hidden>')
    page = replace_once(page, 'const item = sample(), record = review();',
                        'const item = sample(), record = review(); $("zoom").value = item.width < 512 ? "1.5" : "0.5";')
    # A new manual target must not accidentally replace the selected source target.
    page = replace_once(page, '<button data-action="N">N 新增人工框</button>',
                        '<button id="startNewBox">开始补一个新框</button><button data-action="N">N 保存新增框</button>')
    page = replace_once(page, '  document.querySelectorAll("[data-action]").forEach(button => button.addEventListener("click", () => applyAction(button.dataset.action)));',
                        '  $("startNewBox").addEventListener("click", () => { $("original").value = ""; $("teacher").value = ""; $("aiAssisted").checked = false; $("reason").value = "人工补漏"; setBox(null); setView("gt"); });\n  document.querySelectorAll("[data-action]").forEach(button => button.addEventListener("click", () => applyAction(button.dataset.action)));')
    (OUT / 'index.html').write_text(page, encoding='utf-8')


def check():
    manifest_path = OUT / 'review_manifest_teacher.json'
    if not manifest_path.exists():
        manifest_path = OUT / 'review_manifest_cached.json'
    manifest = read_json(manifest_path)
    require([s['image_id'] for s in manifest['samples']] == list(IDS), 'Wrong8 source images')
    require(dataset_id(manifest) == manifest['dataset_id'], 'Dataset binding changed')
    require(not manifest['dataset_frozen'] and not manifest['G_ready'] and not manifest['verified_gt'], 'False freeze')
    require(Counter(s['scene'] for s in manifest['samples']) == {'A': 4, 'C': 4}, 'Scene composition changed')
    isolated(manifest['samples'])
    require(sha256_file(OUT / 'annotation_policy_v1.md') == manifest['annotation_policy_sha256'], 'Policy changed')
    for path, digest in read_json(OUT / 'source_bindings.json').items():
        require(sha256_file(Path(path)) == digest, f'Protected file changed: {path}')
    for sample in manifest['samples']:
        require(sha256_file(OUT / sample['raw_file']) == sample['source_sha256'], 'Raw binding changed')
        with Image.open(OUT / sample['raw_file']) as image:
            require(image.size == (sample['width'], sample['height']), 'Raw dimensions changed')
        asset = sample['source_record']['assets']['source_boxes']
        require(sha256_file(OUT / sample['gt_overlay_file']) == asset['sha256'], 'Overlay changed')
    html = (OUT / 'index.html').read_text(encoding='utf-8')
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>', html, re.S))
    require(json.loads(scripts['review-manifest']) == manifest, 'Embedded manifest changed')
    require('id="rawSeen"' not in html and 'id="checks"' not in html and 'toggleDraftBoxes' in html, 'UI regression')
    syntax = subprocess.run(['node', '--check', '-'], input=scripts['core']+'\n'+scripts['app-script'],
                            text=True, encoding='utf-8', capture_output=True)
    require(syntax.returncode == 0, syntax.stderr)
    js = scripts['core'] + '\nconst m=' + scripts['review-manifest'] + ';\n' + r'''
const assert=require('node:assert/strict'), C=WorkbenchCore;
assert.deepEqual(C.validateManifest(m), []);
const s=m.samples[0], r={reviewer:'1',raw_seen:false,checks:{},actions:[]};
assert.ok(C.completionErrors(s,r).length);
assert.ok(C.actionErrors(s,{target_id:'new',action:'N',class:'person',bbox:[0,0,s.width+1,10],reason:'manual',ai_assisted:false}).length);
const bad=JSON.parse(JSON.stringify(m)); bad.samples.pop(); assert.ok(C.validateManifest(bad).length);
console.log('PASS JS: actual manifest valid; unsigned, out-of-range and wrong-count rejected');
'''
    result = subprocess.run(['node', '-'], input=js, text=True, encoding='utf-8', capture_output=True)
    require(result.returncode == 0, result.stderr)
    print(result.stdout.strip())
    print('PASS:8 bound A/C drafts; family/camera isolation; old inputs unchanged; no training freeze')


def self_test():
    samples = [dict(family_id='sync_epfl', camera_id='c0', split='train'),
               dict(family_id='sync_epfl', camera_id='c2', split='train')]
    isolated(samples)
    bad = deepcopy(samples)
    bad[1]['split'] = 'dev'
    try:
        isolated(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Synchronized family leakage not rejected')
    assert replace_once('abcd', 'bc', 'X') == 'aXd'
    for text in ('none', 'bcbc'):
        try:
            replace_once(text, 'bc', 'X')
        except ValueError:
            pass
        else:
            raise AssertionError('Missing/duplicate UI anchor not rejected')
    print('PASS: family leakage and ambiguous UI anchors rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'teacher', 'check', 'self-test'])
    args = parser.parse_args()
    {'build': build, 'teacher': teacher, 'check': check, 'self-test': self_test}[args.action]()
