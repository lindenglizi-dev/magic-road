"""Reuse the signed-review UI for the approved, bounded 12+12 AI draft."""
from collections import Counter
import ast
from copy import deepcopy
from pathlib import Path
import json
import math
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

from cnn.prepare_ground48 import ROOT, blank_patch, dataset_id, read_json, sha256_file, write_json
from cnn.prepare_ac_correction import isolated, replace_once
from cnn.import_verified_review import _box, _validate_patch, _validate_action, ReviewError

OUT = Path(__file__).resolve().parent
PROPOSAL = ROOT/'cnn/reports/ac_replacement_scope_20261013_v1/proposal.json'
TEMPLATE = ROOT/'cnn/reports/ac_ai_drawn24_20261010_v1/index.html'
HINTS = ROOT/'cnn/reports/virat_ac_expand_20261011_v1/review_manifest_teacher.json'


def build():
    assert not (OUT/'review_manifest.json').exists(), 'Preserve any existing review'
    proposal = read_json(PROPOSAL)
    edits = {}
    for name in ('virat_edits.json', 'pets_edits.json'):
        part = read_json(OUT/name)['images']
        assert not set(edits) & set(part)
        edits.update(part)
    assert set(edits) == {s['image_id'] for s in proposal['images']}
    hints = {s['image_id']:s for s in read_json(HINTS)['samples']}
    policy = ROOT/'cnn/annotation_policy_v1.md'
    bindings = {str(p):sha256_file(p) for p in (PROPOSAL, TEMPLATE, HINTS, policy,
                OUT/'virat_edits.json', OUT/'pets_edits.json', OUT/'scope_approval.json')}
    shutil.copy2(policy, OUT/policy.name)
    samples = []
    for i, row in enumerate(proposal['images'], 1):
        edit = edits[row['image_id']]
        assert edit['inspected_raw'] is True
        image_dir = OUT/'images'/row['image_id']
        image_dir.mkdir(parents=True, exist_ok=False)
        source = Path(row['raw_file_absolute'])
        assert sha256_file(source) == row['source_sha256']
        relative = f'images/{row["image_id"]}/raw{source.suffix}'
        shutil.copy2(source, OUT/relative)
        originals = []
        for label in row['labels']:
            original = dict(target_id=label['target_id'], **{'class':label['class']}, bbox=label['bbox'],
                source_category=label['class'], source_target_id=label['target_id'],
                source_record=deepcopy(label), provenance_kind=row['provenance_kind'])
            originals.append(original)
        teacher = []
        if row['image_id'] in hints:
            old = hints[row['image_id']]
            assert old['source_sha256'] == row['source_sha256']
            teacher = deepcopy(old['teacher'])
        samples.append(dict(image_id=row['image_id'], legacy_id=f'{i:02d} '+row['split'],
            bucket='train_review' if row['split']=='train' else 'road_development',
            split=row['split'], scene=row['scene'], family_id=row['family_id'], camera_id=row['camera_id'],
            width=row['width'], height=row['height'], source_sha256=row['source_sha256'], raw_file=relative,
            gt_overlay_file=f'images/{row["image_id"]}/source.png', original=originals, teacher=teacher,
            teacher_status='复用既有CPU教师提示，不是真值' if teacher else '本图无新增教师推理；AI按原图补画',
            warnings=[u['reason'] for u in edit['uncertain']], review_score=len(edit['uncertain']),
            review_batch=1, review_batch_ordinal=i,
            ai_visual_review=dict(inspected_raw=True, note=edit['note'], uncertain=edit['uncertain'], human_verified=False),
            source_record=deepcopy(row)))
    isolated(samples)
    manifest = dict(schema='cnn_review_workbench_v1', samples=samples, train_required_count=12,
        bucket_counts={'train_review':12, 'road_development':12, 'person_background_aux':0},
        annotation_policy_sha256=sha256_file(policy),
        teacher_status='VIRAT复用已保存提示；PETS未新跑教师。AI逐图修订，不是教师或人工真值。',
        human_review_cap=24, proposed_updates=10, dataset_frozen=False, G_ready=False, training_started=False)
    manifest['dataset_id'] = dataset_id(manifest)
    patch = blank_patch(manifest)
    for sample, review in zip(samples, patch['reviews'], strict=True):
        edit = edits[sample['image_id']]
        originals = {o['target_id']:o for o in sample['original']}
        assert set(edit['modify_original']) <= set(originals)
        assert set(edit['drop_original']) <= set(originals)
        assert not set(edit['modify_original']) & set(edit['drop_original'])
        for original in sample['original']:
            target = original['target_id']
            action = dict(target_id=target, action='A', **{'class':original['class']}, bbox=original['bbox'],
                reason='AI逐图检查后暂保留参考；待人工确认', ai_assisted=True)
            if target in edit['modify_original']:
                action.update(action='M', bbox=edit['modify_original'][target], reason='AI依原图修订可见范围；'+edit['note'])
            if target in edit['drop_original']:
                action.update(action='D', reason=edit['drop_original'][target])
            review['actions'].append(action)
        for i, extra in enumerate(edit['add'], 1):
            assert extra['class'] in ('person','vehicle') and extra['reason']
            review['actions'].append(dict(target_id=f'ai_{i:03d}', action='N', ai_assisted=True, **extra))
        review['notes'] = edit['note'] + ''.join('\n待核：'+u['reason'] for u in edit['uncertain'])
        for filename, objects in (('source.png', sample['original']),
                ('ai_draft.png', [a for a in review['actions'] if a['action'] != 'D'])):
            with Image.open(OUT/sample['raw_file']) as raw:
                image = raw.convert('RGB')
            draw = ImageDraw.Draw(image)
            for obj in objects:
                _box(obj['bbox'], sample['width'], sample['height'], sample['image_id'])
                color = '#00c8ff' if filename=='ai_draft.png' else '#00e676'
                draw.rectangle(obj['bbox'], outline=color, width=2)
                draw.text(obj['bbox'][:2], obj['target_id']+' '+obj['class'], fill=color, stroke_width=1, stroke_fill='black')
            image.save(OUT/'images'/sample['image_id']/filename)
    patch['provenance'] = dict(kind='AI_assisted_unsigned_draft', human_signed_frames=0,
        edit_hashes={name:sha256_file(OUT/name) for name in ('virat_edits.json','pets_edits.json')})
    write_json(OUT/'review_manifest.json', manifest)
    write_json(OUT/'ai_draft_patch.json', patch)
    write_json(OUT/'source_bindings.json', bindings)
    _validate_patch(OUT/'ai_draft_patch.json', manifest, {s['image_id']:s for s in samples})
    render(manifest, patch)
    counts = Counter(a['class'] for r in patch['reviews'] for a in r['actions'] if a['action']!='D')
    write_json(OUT/'status.json', dict(status='AI_draft_ready_for_human_review', images=24,
        proposed_boxes=dict(counts), actions=dict(Counter(a['action'] for r in patch['reviews'] for a in r['actions'])),
        uncertain_images=[key for key,e in edits.items() if e['uncertain']],
        human_signed_frames=0, dataset_frozen=False, E7_baseline_started=False, training_started=False,
        page_sha256=sha256_file(OUT/'index.html'), script_sha256=sha256_file(Path(__file__))))
    check()


def budget():
    """Exercise the current sample-count helper without importing torch or starting training."""
    path = ROOT/'cnn/train.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    helper = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='accumulation_group_samples')
    namespace = {}
    exec(compile(ast.Module(body=[helper],type_ignores=[]),str(path),'exec'),namespace)
    actual = namespace['accumulation_group_samples'](0,3,8,8,22)
    assert actual == 22
    for size in range(1,23):
        steps = math.ceil(size/8)
        assert namespace['accumulation_group_samples'](0,steps,8,8,size) == size
    write_json(OUT/'training_budget_check.json',dict(train_source_sha256=sha256_file(path),
        inspected_rule='due at accumulation boundary OR epoch end; gradients cleared after step',
        nominal_batch=64, proposed_train_images=22, microbatches_per_epoch=3,
        actual_samples_per_update=actual, G10_epoch_passes=10, G10_image_presentations=220,
        earlier_640_presentations_29_passes='hypothetical full64 groups, NOT current trainer behavior',
        training_started=False, trainer_modified=False))
    print('PASS1..22 sample counts;22 images -> actual batch22, G10=10passes/220presentations, not640')


def render(manifest, patch):
    # ponytail: reuse the frozen24-image workbench, adapting only this batch's binding and counts.
    page = TEMPLATE.read_text(encoding='utf-8')
    for name, payload in (('review-manifest',manifest), ('ai-draft',patch)):
        pattern = rf'(<script id="{name}" type="application/json">).*?(</script>)'
        encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).replace('<','\\u003c')
        page, count = re.subn(pattern, lambda m:m[1]+encoded+m[2], page, flags=re.S)
        assert count == 1
    page = page.replace('RoadYOLO A/C 24张 AI已画草稿','RoadYOLO A/C 固定24张复核')
    page = replace_once(page, 'manifest.train_required_count !== 20', 'manifest.train_required_count !== 12')
    page = replace_once(page, 'counts.train_review !== 20 || counts.road_development !== 4',
                        'counts.train_review !== 12 || counts.road_development !== 12')
    page = page.replace('AI24 train count must be20','AC24 train count must be12').replace('AI24 buckets must be20/4/0','AC24 buckets must be12/12/0')
    old = '此包只有候选24张，192张来源门槛尚未通过，不要求现在强行签完。'
    page = replace_once(page, old, '本轮范围已获确认：新增审核最多24张（训练12/开发12），剔除也计上限，不追加。完成后仅做G10小样本诊断。待核未解决请保持未签署并在备注说明；不要为了凑数签完。')
    page = page.replace('绿色为暂保留来源框', '绿色为暂保留来源/既有AI参考框')
    with (OUT/'index.html').open('x', encoding='utf-8') as stream:
        stream.write(page)


def check():
    manifest, patch = read_json(OUT/'review_manifest.json'), read_json(OUT/'ai_draft_patch.json')
    assert len(manifest['samples']) == len(patch['reviews']) == 24
    assert dataset_id(manifest) == manifest['dataset_id']
    assert Counter(s['split'] for s in manifest['samples']) == {'train':12,'dev':12}
    isolated(manifest['samples'])
    for path,digest in read_json(OUT/'source_bindings.json').items():
        assert sha256_file(Path(path)) == digest, path
    for sample in manifest['samples']:
        assert sha256_file(OUT/sample['raw_file']) == sample['source_sha256']
        assert (OUT/sample['gt_overlay_file']).is_file()
    _validate_patch(OUT/'ai_draft_patch.json',manifest,{s['image_id']:s for s in manifest['samples']})
    assert not any(r['complete'] or r['raw_seen'] or r['reviewed_at_utc'] or any(r['checks'].values()) for r in patch['reviews'])
    page = (OUT/'index.html').read_text(encoding='utf-8')
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>',page,re.S))
    assert json.loads(scripts['review-manifest']) == manifest and json.loads(scripts['ai-draft']) == patch
    assert 'toggleDraftBoxes' in page and 'id="rawSeen"' not in page and 'id="checks"' not in page
    result = subprocess.run(['node','--check','-'], input=scripts['core']+'\n'+scripts['app-script'], text=True, encoding='utf-8',capture_output=True)
    assert result.returncode == 0, result.stderr
    test = scripts['core']+'\nconst assert=require("node:assert/strict"),m='+scripts['review-manifest']+',p='+scripts['ai-draft']+r''';
assert.deepEqual(WorkbenchCore.validateManifest(m),[]);
for(let i=0;i<24;i++) {
  const s=m.samples[i],r=p.reviews[i];
  assert.ok(WorkbenchCore.completionErrors(s,r).length);
  for(const a of r.actions) assert.deepEqual(WorkbenchCore.actionErrors(s,a),[]);
}
const bad=structuredClone(m);bad.samples.pop();assert.ok(WorkbenchCore.validateManifest(bad).length);
const a=structuredClone(p.reviews[0].actions[0]);a.bbox=[0,0,m.samples[0].width+1,10];
assert.ok(WorkbenchCore.actionErrors(m.samples[0],a).length);
'''
    result = subprocess.run(['node','-'],input=test,text=True,encoding='utf-8',capture_output=True)
    assert result.returncode == 0, result.stderr
    sample = manifest['samples'][0]
    invalid = deepcopy(patch['reviews'][0]['actions'][0]); invalid['target_id']='missing'
    try:
        _validate_action(invalid,sample,{o['target_id']:o for o in sample['original']},set(),'negative_test')
    except ReviewError:
        pass
    else:
        raise AssertionError('Unknown original target accepted')
    assert (OUT/'操作说明.txt').is_file()
    status = read_json(OUT/'status.json')
    assert status['page_sha256'] == sha256_file(OUT/'index.html')
    assert status['script_sha256'] == sha256_file(Path(__file__))
    print('PASS24 source hashes/coordinates/12+12 split; UI JS; bad-count/box/target rejected; unsigned drafts only')


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'],['check'],['budget'])
    globals()[sys.argv[1]]()
