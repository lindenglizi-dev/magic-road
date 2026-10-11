"""One bounded AI-drawn A/C review draft; never signs or publishes training GT."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

from PIL import Image, ImageDraw

from . import prepare_ac_correction as pilot, prepare_ac_next8 as expansion
from .prepare_ground48 import ROOT, blank_patch, dataset_id, read_json, sha256_file, write_json

OUT = ROOT / 'cnn/reports/ac_ai_drawn24_20261010_v1'
MIO = ROOT / 'cnn/data/mio_ac_screen_20261010_v2'
# Selected from raw scenes, before inference; not selected by student/teacher performance.
MIO_IDS = ('00093389','00055961','00021031','00101156','00071079','00065563',
           '00097475','00066766','00098678','00087785','00026320','00101068',
           '00079251','00016630','00048542','00105154')


def build():
    if OUT.exists():
        raise FileExistsError('Preserve prior draft; do not overwrite')
    protected = {str(p): sha256_file(p) for p in pilot.protected_files()}
    for p in (ROOT/'cnn/reports/ac_scope_fixed_20261010_v1/scope_decision.json',
              ROOT/'cnn/reports/ac_patch_check_20261010_v3/patch_validation.json'):
        protected[str(p)] = sha256_file(p)
    OUT.mkdir()
    shutil.copy2(ROOT/'cnn/annotation_policy_v1.md', OUT/'annotation_policy_v1.md')
    expansion.OUT = OUT
    receipt = read_json(MIO/'receipt.json')
    members = {Path(r['path']).stem:r for r in receipt['members']}
    samples = []
    for name in MIO_IDS:
        r = members[name]
        assert '/train/' in r['name'] and sha256_file(Path(r['path'])) == r['sha256']
        s = expansion.make_sample('mio_'+name, r['path'], [], 'train',
            'MIO-entire-source-train-only-camera-IDs-unresolved', 'MIO-camera-unknown-'+name,
            receipt['source_page'], dict(member=r, receipt_sha256=sha256_file(MIO/'receipt.json'),
            official_boxes_available=False, camera_id_verified=False, license=receipt['license']))
        s['scene'] = 'C' if name in {'00098678','00016630'} else 'A'
        samples.append(s)
    sys.path.insert(0, str(ROOT/'cnn'))
    from .prepare_ac_pilot import DATA as EPFL, epfl_boxes, FAMILY
    with zipfile.ZipFile(EPFL/'multiclass_ground_truth.zip') as labels, zipfile.ZipFile(EPFL/'multiclass_ground_truth_images.zip') as images:
        for camera, ordinal in ((2,80),(3,80),(2,220),(3,220)):
            member = f'c{camera}/{ordinal:08d}.jpg'
            boxes, missing = epfl_boxes(labels,camera,ordinal)
            originals = [dict(target_id=f'o{i}',source_target_id=f'{b["member"]}:{b["row"]}',
                source_category=b['source_class'], **{'class':'person' if b['source_class']=='person' else 'vehicle'},
                bbox=b['xyxy_raw'],source_record=b) for i,b in enumerate(boxes,1)]
            s = expansion.make_sample(f'epfl_c{camera}_o{ordinal:03d}', io.BytesIO(images.read(member)), originals,
                'train',FAMILY,f'EPFL:c{camera}','https://www.epfl.ch/labs/cvlab/data/data-multiclass/',
                dict(member=member,archive_sha256=sha256_file(EPFL/'multiclass_ground_truth_images.zip'),
                     ordinal=ordinal,missing_class_files=missing))
            s['scene']='C'
            samples.append(s)
    previous = read_json(ROOT/'cnn/reports/ac_expansion8_20261010_v1/review_manifest_teacher.json')
    ground = read_json(pilot.GROUND/'review_manifest_teacher.json')
    wanted = [(ROOT/'cnn/reports/ac_expansion8_20261010_v1',s) for s in previous['samples'] if s['image_id'].startswith('pets')]
    for image_id in ('VIRAT_S_000200_00_000100_000171_f0000637','VIRAT_S_010107_02_000282_000312_f0000104'):
        wanted.append((pilot.GROUND,next(s for s in ground['samples'] if s['image_id']==image_id)))
    for directory, old in wanted:
        s = expansion.make_sample(old['image_id'],directory/old['raw_file'],deepcopy(old['original']),
            'dev',old.get('family_id',old['camera_id']),old['camera_id'],
            old.get('source_url','https://viratdata.org/'),dict(reused_manifest=str(directory/'review_manifest_teacher.json'),
            reused_manifest_sha256=sha256_file(directory/'review_manifest_teacher.json')))
        s.update(scene='A' if s['image_id'].startswith('pets') else 'C',teacher=deepcopy(old['teacher']))
        samples.append(s)
    assert len(samples)==24 and len({s['image_id'] for s in samples})==24
    signed = read_json(pilot.OUT/'review_manifest_teacher.json')
    assert not ({s['image_id'] for s in samples}&{s['image_id'] for s in signed['samples']})
    for i,s in enumerate(samples,1):
        s.update(legacy_id=f'AI{i:02d}',review_batch=1,review_batch_ordinal=i,
                 warnings=['AI草稿待人工确认，不是完整GT；静止车/骑行者需核对。'])
    pilot.isolated(samples)
    m = dict(schema='cnn_review_workbench_v1',samples=samples,train_required_count=20,
        bucket_counts={'train_review':20,'road_development':4},
        annotation_policy_sha256=sha256_file(OUT/'annotation_policy_v1.md'),
        teacher_status='CPU hints pending; not GT',verified_gt=False,dataset_frozen=False,G_ready=False,
        training_started=False,human_signed_frames=0,formal_acceptance=False,
        purpose='24 AI-drawn candidates; not the complete192 manifest; no additional manual assignment before source gate',
        split_note='All MIO source reserved train, unknown camera grouping; EPFL synchronized family train; PETS/VIRAT dev only.')
    m['dataset_id']=dataset_id(m)
    write_json(OUT/'manifest_original.json',m)
    write_json(OUT/'source_bindings.json',protected)
    panels(m,False)
    print('Built24 raw candidates:20 train/4 dev, unsigned',flush=True)


def teacher():
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads,load_official_model,teacher_input,tree_hash
    assert not (OUT/'review_manifest_teacher.json').exists()
    m=read_json(OUT/'manifest_original.json')
    assets=ROOT/'cnn/teacher_assets'; r=read_json(assets/'receipt.json')
    weights=assets/'yolox_s.pth'; source=assets/'source/YOLOX-0.3.0'
    assert sha256_file(weights)==r['weights']['sha256'] and tree_hash(source/'yolox')==r['source_tree_sha256']
    torch.set_num_threads(2); torch.set_num_interop_threads(1)
    device=torch.device('cpu'); model=load_official_model(source,weights,device)
    for s in m['samples']:
        if s['teacher']:
            continue
        transform=_letterbox_transform(s['width'],s['height'])
        row=dict(image_path=OUT/s['raw_file'],preprocess=dict(raw_image=True,letterbox_1280x720=transform))
        preds=decode_heads(capture_raw_heads(model,teacher_input(row,device)),transform)
        for i,p in enumerate(preds): p.update(candidate_id=f't{i}',kind='AI_HINT_NOT_GT')
        s['teacher']=preds
        print(s['image_id'],len(preds),'CPU hints',flush=True)
    m['teacher_status']='CPU YOLOX-S hints; assistant drawing separately recorded; not GT'
    write_json(OUT/'review_manifest_teacher.json',m)
    write_json(OUT/'teacher_receipt.json',dict(device='cpu',GPU_used=False,training_started=False,
        weights_sha256=sha256_file(weights),source_tree_sha256=r['source_tree_sha256'],
        inference=dict(input='1024x576',confidence=.1,nms_iou=.6),
        cached_dev_hints=4,new_CPU_images=20,script_sha256=sha256_file(Path(__file__))))
    panels(m,True)


def panels(m, predictions):
    # ponytail: fixed4-frame sheets for visual inspection; no general image viewer.
    for start in range(0,24,4):
        panel=Image.new('RGB',(1536,1216),'#eeeeee'); draw=ImageDraw.Draw(panel)
        for offset,s in enumerate(m['samples'][start:start+4]):
            image=Image.open(OUT/s['raw_file']).convert('RGB')
            if predictions:
                d=ImageDraw.Draw(image)
                for p in s['teacher']:
                    d.rectangle(p['bbox'],outline='#ff8700',width=2)
                    d.text(p['bbox'][:2],p['candidate_id']+' '+p['class'][0]+f' {p["score"]:.2f}',fill='white',stroke_width=1,stroke_fill='black')
            image.thumbnail((768,576))
            x,y=(offset%2)*768,(offset//2)*608
            panel.paste(image,(x,y+32));draw.text((x+8,y+7),f'{start+offset+1:02d} {s["image_id"]} {s["width"]}x{s["height"]}',fill='black')
        panel.save(OUT/f'{"teacher" if predictions else "raw"}_{start+1:02d}_{start+4:02d}.jpg',quality=95)


def draw_drafts():
    from .import_verified_review import _validate_patch
    m=read_json(OUT/'review_manifest_teacher.json')
    edits=read_json(OUT/'assistant_edits.json')['images']
    assert set(edits)=={s['image_id'] for s in m['samples']}
    patch=blank_patch(m)
    for s,review in zip(m['samples'],patch['reviews'],strict=True):
        e=edits[s['image_id']]
        s['scene']='A' if s['image_id']=='mio_00098678' else s['scene']
        s['ai_visual_review']=dict(status='assistant_inspected_raw_and_teacher_overlay',
            note=e['note'],uncertain_regions=e['uncertain'],human_verified=False)
        # Explicit user authority permits AI drafts, never fabricated human sign-off.
        s['ai_draft_authorization']='用户要求：找到合适训练集图片视频后进行画框，最后由用户审核。'
        originals={o['target_id']:o for o in s['original']}
        assert set(e.get('modify_original',{}))<=set(originals)
        assert set(e.get('drop_original',[]))<=set(originals)
        for o in s['original']:
            action=dict(target_id=o['target_id'],action='A',**{'class':o['class']},bbox=o['bbox'],
                reason='AI检查后暂保留来源框；待人工确认',ai_assisted=True)
            if o['target_id'] in e.get('modify_original',{}):
                action.update(action='M',bbox=e['modify_original'][o['target_id']],reason='AI按可见车体/人体修订；待人工确认')
            if o['target_id'] in e.get('drop_original',[]):
                action.update(action='D',reason='AI原图检查：重复框或该位置未见可辨目标；待人工确认')
            review['actions'].append(action)
        teachers={t['candidate_id']:t for t in s['teacher']}
        assert len(set(e['keep_teacher']))==len(e['keep_teacher']) and set(e['keep_teacher'])<=set(teachers)
        for target in e['keep_teacher']:
            t=teachers[target]
            review['actions'].append(dict(target_id='teacher_'+target,action='N',**{'class':t['class']},
                bbox=t['bbox'],reason=f'AI逐图检查后暂保留教师{target}；非人工确认',ai_assisted=True))
        for i,(label,box) in enumerate(e['add'],1):
            review['actions'].append(dict(target_id=f'ai_{i:03d}',action='N',**{'class':label},bbox=box,
                reason='AI按无框原图补画教师/来源漏标目标；待人工确认',ai_assisted=True))
        review['notes']=e['note']+'\n'+('\n'.join('待核：'+region[4] for region in e['uncertain']) or 'AI初查无特别疑点；仍须人工确认。')
        image=Image.open(OUT/s['raw_file']).convert('RGB');d=ImageDraw.Draw(image)
        for a in review['actions']:
            if a['action']=='D': continue
            color='#00c8ff' if a['class']!='ignore' else '#da69f0'
            d.rectangle(a['bbox'],outline=color,width=2)
            d.text(a['bbox'][:2],a['target_id']+' '+a['class'],fill=color,stroke_width=1,stroke_fill='black')
        image.save(OUT/'images'/s['image_id']/'ai_draft.png')
        s['ai_draft_file']=f'images/{s["image_id"]}/ai_draft.png'
    assert dataset_id(m)==m['dataset_id']
    patch['provenance']=dict(kind='AI_assisted_unsigned_draft',edits_sha256=sha256_file(OUT/'assistant_edits.json'),
        assistant_inspected_images=24,human_signed_frames=0,training_started=False)
    write_json(OUT/'ai_draft_patch.json',patch)
    write_json(OUT/'review_manifest_ai_draft.json',m)
    _validate_patch(OUT/'ai_draft_patch.json',m,{s['image_id']:s for s in m['samples']})
    for start in range(0,24,4):
        panel=Image.new('RGB',(1536,1216),'#eeeeee');d=ImageDraw.Draw(panel)
        for j,s in enumerate(m['samples'][start:start+4]):
            im=Image.open(OUT/s['ai_draft_file']);im.thumbnail((768,576))
            x,y=j%2*768,j//2*608;panel.paste(im,(x,y+32))
            d.text((x+8,y+7),f'{start+j+1:02d} {s["image_id"]} AI DRAFT NOT GT',fill='black')
        panel.save(OUT/f'drawn_{start+1:02d}_{start+4:02d}.jpg',quality=95)
    pilot.OUT=OUT;pilot.render(m)
    page=(OUT/'index.html').read_text(encoding='utf-8')
    replace=pilot.replace_once
    page=page.replace('RoadYOLO A/C 8张补标试点','RoadYOLO A/C 24张 AI已画草稿')
    page=replace(page,'<label>批次 <select id="bucket"><option value="1">先做这4张</option><option value="2">第二批4张（可暂缓）</option><option value="all">全部8张</option></select></label>',
        '<label>固定清单 <select id="bucket"><option value="all">全部24张（不滚动追加）</option></select></label>')
    page=page.replace('manifest.train_required_count !== 6','manifest.train_required_count !== 20').replace('AC8 candidate train count must be6','AI24 train count must be20')
    page=page.replace('manifest.samples.length !== 8','manifest.samples.length !== 24').replace('AC8 samples must be8','AI24 samples must be24')
    page=page.replace('counts.train_review !== 6 || counts.road_development !== 2','counts.train_review !== 20 || counts.road_development !== 4').replace('AC8 candidate buckets must be6/2/0','AI24 buckets must be20/4/0')
    page=replace(page,'${item.review_batch_ordinal}/4','${item.review_batch_ordinal}/24')
    page=replace(page,'只做第一批4张即可导出，未完成图保持草稿。绿色是来源参考、橙色是教师候选、青色是你的修订。EPFL来源坐标约定未确认，请按原图核对或重画；不得因教师没框就删掉目标。',
        '我已按原图预画24张，已自动载入草稿，不需要逐个重新采用。绿色为暂保留来源框，青色为AI修订/新增，橙色为可选教师提示；均不是已确认GT。可切换RAW原图；决策列表可定位、编辑或撤销。备注“待核”是尚不能可靠确认的区域，不是ignore，也不代表背景；未处理不要签署。此包只有候选24张，192张来源门槛尚未通过，不要求现在强行签完。')
    encoded=json.dumps(patch,ensure_ascii=False,allow_nan=False).replace('<','\\u003c')
    page=replace(page,'<script id="core">','<script id="ai-draft" type="application/json">'+encoded+'</script>\n<script id="core">')
    page=replace(page,'const reviews = manifest.samples.map(blankReview);',
        'const initial = JSON.parse($("ai-draft").textContent);\n  if (initial.dataset_id !== manifest.dataset_id || initial.annotation_policy_sha256 !== manifest.annotation_policy_sha256) throw new Error("AI草稿绑定不匹配");\n  const reviews = manifest.samples.map(item => validateImportedReview(initial.reviews.find(r => r.image_id === item.image_id), item));')
    page=replace(page,'renderProgress(); setView("raw");','renderProgress(); setView("gt");')
    # Draw effective labels, not stale deleted/replaced source boxes underneath the draft.
    page=replace(page,'if (view !== "raw") sample().original.forEach(item => drawBox(item.bbox, "#00e676", ""));',
        'if (view !== "raw" && showDraftBoxes) sample().original.filter(item => { const a=review().actions.find(a=>a.target_id===item.target_id); return !a || a.action === "A"; }).forEach(item => drawBox(item.bbox, "#00e676", `${item.target_id} ${item.class}`));')
    page=replace(page,'teacher ? `${teacher.candidate_id} ${item.class} 已采用` : ""',
        'teacher ? `${teacher.candidate_id} ${item.class} AI草稿` : `${item.target_id} ${item.class}`')
    page=replace(page,'      row.append(remove, document.createTextNode(',
        '      const locate=document.createElement("button"); locate.textContent="定位/编辑"; locate.addEventListener("click",()=>{ $("original").value=sample().original.some(o=>o.target_id===action.target_id)?action.target_id:""; $("teacher").value=""; $("className").value=action.class; $("reason").value=action.reason; $("aiAssisted").checked=action.ai_assisted; teacherEditId=action.action==="N"?action.target_id:null; $("teacherSaveEdit").hidden=!teacherEditId; setView("gt"); setBox(action.bbox); }); row.append(locate);\n      row.append(remove, document.createTextNode(')
    page=page.replace('保存已采用框的修改（使用坐标/类别/原因栏）','保存已添加草稿框的修改（使用坐标/类别/原因栏）')
    (OUT/'index.html').write_text(page,encoding='utf-8')
    counts=Counter(a['class'] for r in patch['reviews'] for a in r['actions'] if a['action']!='D')
    write_json(OUT/'draft_status.json',dict(status='AI_drawn_drafts_not_dataset_ready',images=24,
        split_counts=dict(Counter(s['split'] for s in m['samples'])),scene_counts=dict(Counter(s['scene'] for s in m['samples'])),
        proposed_boxes=dict(counts),added_by_assistant=sum(len(e['add']) for e in edits.values()),
        modified_source_boxes=sum(len(e.get('modify_original',{})) for e in edits.values()),
        uncertain_images=sum(bool(e['uncertain']) for e in edits.values()),
        human_signed_new_frames=0,previous_signed_frames=8,remaining_manual_cap=24,
        dataset_frozen=False,G_ready=False,training_started=False,
        source_gate='failed_to_establish_complete192: static/rider coverage and MIO camera IDs not closed; no third source investigation'))
    print('AI drafts drawn:',dict(counts),'unsigned; dataset not ready',flush=True)


def check():
    from .import_verified_review import _validate_patch
    m=read_json(OUT/'review_manifest_ai_draft.json');p=read_json(OUT/'ai_draft_patch.json')
    assert dataset_id(m)==m['dataset_id'] and len(m['samples'])==len(p['reviews'])==24
    assert Counter(s['split'] for s in m['samples'])=={'train':20,'dev':4}
    pilot.isolated(m['samples'])
    for path,digest in read_json(OUT/'source_bindings.json').items(): assert sha256_file(Path(path))==digest,path
    for s in m['samples']: assert sha256_file(OUT/s['raw_file'])==s['source_sha256']
    _validate_patch(OUT/'ai_draft_patch.json',m,{s['image_id']:s for s in m['samples']})
    assert not any(r['complete'] or r['raw_seen'] or r['reviewed_at_utc'] or any(r['checks'].values()) for r in p['reviews'])
    page=(OUT/'index.html').read_text(encoding='utf-8')
    scripts=dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>',page,re.S))
    assert json.loads(scripts['ai-draft'])==p and json.loads(scripts['review-manifest'])==m
    assert 'toggleDraftBoxes' in page and 'id="rawSeen"' not in page and 'id="checks"' not in page
    result=subprocess.run(['node','--check','-'],input=scripts['core']+'\n'+scripts['app-script'],text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    test=scripts['core']+'\nconst assert=require("node:assert/strict"),m='+scripts['review-manifest']+',p='+scripts['ai-draft']+';'+r'''
assert.deepEqual(WorkbenchCore.validateManifest(m),[]);
for(let i=0;i<m.samples.length;i++) {
  const s=m.samples[i],r=p.reviews[i]; assert.ok(!r.complete);
  for(const a of r.actions) assert.deepEqual(WorkbenchCore.actionErrors(s,a),[]);
  assert.ok(WorkbenchCore.completionErrors(s,r).length);
}
const a=structuredClone(p.reviews[0].actions[0]); a.bbox=[0,0,m.samples[0].width+1,10];
assert.ok(WorkbenchCore.actionErrors(m.samples[0],a).length);
const bad=structuredClone(m);bad.samples.pop();assert.ok(WorkbenchCore.validateManifest(bad).length);
console.log('PASS:24 drafts, bound coordinates, unsigned completion rejected, wrong count rejected');
'''
    result=subprocess.run(['node','-'],input=test,text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    print(result.stdout.strip());print('PASS: old inputs unchanged; family isolation; CPU only; no GT publication')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['build','teacher','draw','check'])
    args=parser.parse_args()
    {'build':build,'teacher':teacher,'draw':draw_drafts,'check':check}[args.action]()
