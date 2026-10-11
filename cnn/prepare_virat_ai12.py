"""Bounded VIRAT source/AI draft; no human signature, dataset publication or training."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request

import cv2
from PIL import Image, ImageDraw

from . import prepare_ac_correction as pilot, prepare_ac_next8 as expansion
from .prepare_ground48 import ROOT, blank_patch, dataset_id, read_json, sha256_file, write_json

OUT = ROOT / 'cnn/reports/virat_ai12_20261010_v1'
DATA = ROOT / 'cnn/data/virat_ai12_source_20261010_v1'
API = 'https://data.kitware.com/api/v1'
# Ordinary public development sources only, not any existing blind/reserve family.
CLIPS = (
    ('VIRAT_S_010000_02_000388_000421', '56f5877b8d777f753209cad4', '56f57ebb8d777f753209c05b'),
    ('VIRAT_S_040000_00_000063_000085', '56f5882c8d777f753209cced', '56f57f618d777f753209c636'),
)


def fetch():
    DATA.mkdir(parents=True, exist_ok=True)
    for clip, video_id, label_id in CLIPS:
        for item_id, suffix in ((video_id, '.mp4'), (label_id, '.viratdata.objects.txt')):
            path = DATA / (clip + suffix)
            receipt = path.with_suffix(path.suffix + '.receipt.json')
            if receipt.exists():
                assert sha256_file(path) == read_json(receipt)['sha256']
                continue
            if path.exists():
                raise FileExistsError(f'Preserve incomplete download: {path}')
            with urllib.request.urlopen(f'{API}/item/{item_id}/files', timeout=30) as response:
                files = json.load(response)
            assert len(files) == 1 and files[0]['name'] == path.name
            file = files[0]
            assert 0 < file['size'] < 60 * 1024**2
            url = f'{API}/file/{file["_id"]}/download'
            digest = hashlib.sha512()
            count = 0
            with urllib.request.urlopen(url, timeout=45) as response, path.open('xb') as target:
                while chunk := response.read(1024**2):
                    count += len(chunk)
                    assert count <= file['size'], 'Oversized response'
                    target.write(chunk)
                    digest.update(chunk)
            assert count == file['size'] and digest.hexdigest() == file['sha512']
            write_json(receipt, dict(url=url, item_id=item_id, official_file=file,
                bytes=count, sha256=sha256_file(path), sha512_verified=True,
                purpose='public training-candidate screening, not blind test'))
            print('Verified official download:', path.name, count, flush=True)


def panels(manifest, kind):
    for start in range(0, len(manifest['samples']), 4):
        sheet = Image.new('RGB', (1536, 928), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for j, sample in enumerate(manifest['samples'][start:start+4]):
            image = Image.open(OUT / sample['raw_file']).convert('RGB')
            if kind == 'teacher':
                d = ImageDraw.Draw(image)
                for item in sample['teacher']:
                    d.rectangle(item['bbox'], outline='#ff8700', width=2)
                    d.text(item['bbox'][:2], f'{item["candidate_id"]} {item["class"]} {item["score"]:.2f}',
                           fill='white', stroke_width=1, stroke_fill='black')
            elif kind == 'drawn':
                image = Image.open(OUT / sample['ai_draft_file']).convert('RGB')
            image.thumbnail((768, 432))
            x, y = j % 2 * 768, j // 2 * 464
            sheet.paste(image, (x, y+32))
            draw.text((x+8, y+8), f'{start+j+1:02d} {sample["image_id"]}', fill='black')
        sheet.save(OUT / f'{kind}_{start+1:02d}_{min(start+4,len(manifest["samples"])):02d}.jpg', quality=96)


def build():
    assert not OUT.exists(), 'Preserve earlier artifacts'
    OUT.mkdir()
    shutil.copy2(ROOT/'cnn/annotation_policy_v1.md', OUT/'annotation_policy_v1.md')
    protected = pilot.protected_files() + [ROOT/'cnn/reports/ac_signed_progress_20261010_v1/reviewed_partial_labels.json']
    write_json(OUT/'source_bindings.json', {str(p):sha256_file(p) for p in protected})
    expansion.OUT = OUT
    samples = []
    for clip, _, _ in CLIPS:
        video, labels = DATA/(clip+'.mp4'), DATA/(clip+'.viratdata.objects.txt')
        for path in (video, labels):
            assert sha256_file(path) == read_json(path.with_suffix(path.suffix+'.receipt.json'))['sha256']
        cap = cv2.VideoCapture(str(video))
        assert cap.isOpened()
        frames, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
        rows = [(i,list(map(int,line.split()))) for i,line in enumerate(labels.read_text().splitlines(),1)]
        assert all(len(row)==8 for _,row in rows)
        # Six temporal anchors picked before model inference; all stay in one train-only family.
        selected = [(i+1)*(frames-1)//7 for i in range(6)]
        for frame in selected:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, bgr = cap.read()
            assert ok and abs(cap.get(cv2.CAP_PROP_POS_FRAMES)-(frame+1)) < .5
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            height,width = rgb.shape[:2]
            originals = []
            for line,row in rows:
                track,duration,f,x,y,w,h,kind = row
                if f != frame:
                    continue
                assert 0 <= x < x+w <= width and 0 <= y < y+h <= height
                originals.append(dict(target_id=f'o{len(originals)+1}', source_target_id=f'{labels.name}:{line}',
                    source_category=kind, **{'class':'person' if kind==1 else 'vehicle' if kind in (2,3) else 'ignore'},
                    bbox=[x,y,x+w,y+h], source_record=dict(line=line,row=row,
                    note='type0/4/5 pending visual decision; source ignore is NOT certified ignore')))
            family = 'VIRAT-'+clip.split('_')[2][:4]+'xx-train-only-provisional'
            import io
            buffer = io.BytesIO()
            Image.fromarray(rgb).save(buffer, format='PNG');buffer.seek(0)
            sample = expansion.make_sample(f'{clip}_f{frame:07d}', buffer, originals, 'train', family,
                family, 'https://viratdata.org/', dict(video=str(video),video_sha256=sha256_file(video),
                    annotations=str(labels),annotations_sha256=sha256_file(labels),frame_index=frame,
                    frame_origin='zero_based',fps=fps,frame_count=frames,full_static_GT_available=False))
            sample.update(scene='C',legacy_id=f'V{len(samples)+1:02d}', review_batch=1,
                review_batch_ordinal=len(samples)+1,split_status='train_only_candidate_pending_physical_camera_check',
                warnings=['AI预画待审核，非完整GT；来源轨迹框不覆盖全部静止车。'])
            samples.append(sample)
        cap.release()
    manifest = dict(schema='cnn_review_workbench_v1',samples=samples,train_required_count=12,
        bucket_counts={'train_review':12,'road_development':0},
        annotation_policy_sha256=sha256_file(OUT/'annotation_policy_v1.md'),
        verified_gt=False,dataset_frozen=False,G_ready=False,training_started=False,human_signed_frames=0,
        manual_assignment_authorized=False,formal_acceptance=False,
        purpose='12 AI draft previews; additional human review allowance not yet confirmed')
    manifest['dataset_id']=dataset_id(manifest)
    write_json(OUT/'manifest_original.json',manifest)
    panels(manifest,'raw')
    print('Built 12 unsigned raw candidates; not a training dataset',flush=True)


def teacher():
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads, load_official_model, teacher_input, tree_hash
    manifest=read_json(OUT/'manifest_original.json')
    assets=ROOT/'cnn/teacher_assets'; receipt=read_json(assets/'receipt.json')
    weights=assets/'yolox_s.pth'; source=assets/'source/YOLOX-0.3.0'
    assert sha256_file(weights)==receipt['weights']['sha256']
    assert tree_hash(source/'yolox')==receipt['source_tree_sha256']
    torch.set_num_threads(2);torch.set_num_interop_threads(1)
    device=torch.device('cpu');model=load_official_model(source,weights,device)
    for sample in manifest['samples']:
        transform=_letterbox_transform(sample['width'],sample['height'])
        row=dict(image_path=OUT/sample['raw_file'],preprocess=dict(raw_image=True,letterbox_1280x720=transform))
        predictions=decode_heads(capture_raw_heads(model,teacher_input(row,device)),transform)
        for i,item in enumerate(predictions):item.update(candidate_id=f't{i}',kind='AI_HINT_NOT_GT')
        sample.update(teacher=predictions,teacher_status='CPU_hints_not_GT')
        print(sample['legacy_id'],len(predictions),'CPU hints',flush=True)
    manifest['teacher_status']='CPU YOLOX-S hints, assistant visual corrections recorded separately'
    write_json(OUT/'review_manifest_teacher.json',manifest)
    write_json(OUT/'teacher_receipt.json',dict(device='cpu',GPU_used=False,training_started=False,
        weights_sha256=sha256_file(weights),source_tree_sha256=receipt['source_tree_sha256'],
        input='1024x576',confidence=.1,nms_iou=.6,images=12))
    panels(manifest,'teacher')


def inspect():
    manifest=read_json(OUT/'review_manifest_teacher.json')
    for sample in manifest['samples'][:6]:
        image=Image.open(OUT/sample['raw_file'])
        sheet=Image.new('RGB',(1280,500),'#eeeeee')
        sheet.paste(image.crop((0,175,1280,390)),(0,25))
        sheet.paste(image.crop((0,630,160,720)).resize((400,225)),(0,270))
        ImageDraw.Draw(sheet).text((8,5),sample['legacy_id']+' RAW crops; top origin=(0,175), bottom=(0,630) at2.5x',fill='black')
        sheet.save(OUT/(sample['legacy_id']+'_raw_crops.png'))


def draft():
    from .import_verified_review import _validate_patch
    manifest=read_json(OUT/'review_manifest_teacher.json')
    edits=read_json(OUT/'assistant_edits.json')['images']
    assert set(edits)=={s['legacy_id'] for s in manifest['samples']}
    for sample in manifest['samples'][:6]:
        sample.update(scene='person_aux_courtyard',bucket='person_background_aux',split='stress',
            split_status='auxiliary_preview_not_main_AC_training; family_reserved_out_of_dev')
    manifest.update(train_required_count=6,bucket_counts={'train_review':6,'road_development':0,'person_background_aux':6},
        source_dataset_id=manifest['dataset_id'],
        purpose='6 C vehicle/background candidates plus6 courtyard person auxiliary previews; no new human assignment')
    manifest['dataset_id']=dataset_id(manifest)
    patch=blank_patch(manifest)
    for sample,review in zip(manifest['samples'],patch['reviews'],strict=True):
        edit=edits[sample['legacy_id']]
        sample['ai_visual_review']=dict(status='assistant_inspected_raw_and_hints',note=edit['note'],
            uncertain_regions=edit['uncertain'],human_verified=False)
        originals={o['target_id']:o for o in sample['original']}
        assert set(edit.get('original',{}))<=set(originals)
        for item in sample['original']:
            action=dict(target_id=item['target_id'],action='A',**{'class':item['class']},bbox=item['bbox'],
                reason='AI原图检查暂保留来源框，待人工确认',ai_assisted=True)
            if item['target_id'] in edit.get('original',{}):
                action.update(edit['original'][item['target_id']])
            review['actions'].append(action)
        hints={t['candidate_id']:t for t in sample['teacher']}
        assert len(edit['keep_teacher'])==len(set(edit['keep_teacher']))
        for name in edit['keep_teacher']:
            item=hints[name]
            review['actions'].append(dict(target_id='teacher_'+name,action='N',**{'class':item['class']},
                bbox=item['bbox'],reason=f'AI原图复核后保留教师{name}，非人工GT',ai_assisted=True))
        for i,(label,box) in enumerate(edit['add'],1):
            review['actions'].append(dict(target_id=f'ai_{i:03d}',action='N',**{'class':label},bbox=box,
                reason='AI按可见范围补画/拆分，待人工确认',ai_assisted=True))
        review['notes']=edit['note']+'\n'+('\n'.join('待核：'+u[4] for u in edit['uncertain']) or 'AI初查无特别疑点，仍非人工确认。')
        image=Image.open(OUT/sample['raw_file']).convert('RGB');draw=ImageDraw.Draw(image)
        for action in review['actions']:
            if action['action']=='D':continue
            color='#00c8ff'
            draw.rectangle(action['bbox'],outline=color,width=2)
            draw.text(action['bbox'][:2],action['target_id']+' '+action['class'],fill=color,
                stroke_width=1,stroke_fill='black')
        sample['ai_draft_file']=f'images/{sample["image_id"]}/ai_draft.png'
        image.save(OUT/sample['ai_draft_file'])
    patch['provenance']=dict(kind='AI_assisted_unsigned_draft',edits_sha256=sha256_file(OUT/'assistant_edits.json'),
        assistant_inspected_images=12,human_signed_frames=0,training_started=False)
    write_json(OUT/'ai_draft_patch.json',patch)
    write_json(OUT/'review_manifest_ai_draft.json',manifest)
    _validate_patch(OUT/'ai_draft_patch.json',manifest,{s['image_id']:s for s in manifest['samples']})
    # ponytail: adapt the existing working24-frame page, preserving all drawing/edit/export controls.
    page=(ROOT/'cnn/reports/ac_ai_drawn24_20261010_v1/index.html').read_text(encoding='utf-8')
    replace=pilot.replace_once
    for script,value in (('review-manifest',manifest),('ai-draft',patch)):
        pattern=rf'(<script id="{script}"(?: type="[^"]+")?>)(.*?)(</script>)'
        assert len(re.findall(pattern,page,re.S))==1
        encoded=json.dumps(value,ensure_ascii=False,allow_nan=False).replace('<','\\u003c')
        page=re.sub(pattern,lambda m:m[1]+encoded+m[3],page,flags=re.S)
    page=page.replace('RoadYOLO A/C 24张 AI已画草稿','VIRAT 12张 AI补画预览')
    page=replace(page,'全部24张（不滚动追加）','全部12张（预览，不自动追加审核任务）')
    page=replace(page,'manifest.train_required_count !== 20','manifest.train_required_count !== 6')
    page=replace(page,'AI24 train count must be20','VIRAT train candidates must be6')
    page=replace(page,'manifest.samples.length !== 24','manifest.samples.length !== 12')
    page=replace(page,'AI24 samples must be24','VIRAT samples must be12')
    page=replace(page,'counts.train_review !== 20 || counts.road_development !== 4 || counts.person_background_aux !== 0',
        'counts.train_review !== 6 || counts.road_development !== 0 || counts.person_background_aux !== 6')
    page=replace(page,'AI24 buckets must be20/4/0','VIRAT buckets must be6/0/6')
    page=replace(page,'${item.review_batch_ordinal}/24','${item.review_batch_ordinal}/12')
    page=replace(page,'我已按原图预画24张，已自动载入草稿，不需要逐个重新采用。绿色为暂保留来源框，青色为AI修订/新增，橙色为可选教师提示；均不是已确认GT。可切换RAW原图；决策列表可定位、编辑或撤销。备注“待核”是尚不能可靠确认的区域，不是ignore，也不代表背景；未处理不要签署。此包只有候选24张，192张来源门槛尚未通过，不要求现在强行签完。',
        '12张均已载入AI草稿，无需重新逐框采用。第1–6张为庭院行人辅助预览，不冒充A/C主道路；第7–12张为C道路/停车场车辆候选。绿色为暂留来源框，青色为AI修订/补画，橙色为未采用教师提示。先看RAW，对错框用定位/编辑；骑行者人车分开。待核区域不是背景或已确认ignore，不确定就保留草稿。本包尚未增加人工任务配额、未发布训练集、未训练；不要求现在签完12张。')
    (OUT/'index.html').write_text(page,encoding='utf-8')
    (OUT/'操作说明.txt').write_text('默认已载入AI补画。无需逐个采用教师。RAW看原图；来源参考框看有效草稿；来源参考+Teacher仅作可选提示。\n决策列表“定位/编辑”修改框；不需要的AI新增框点撤销；不要因教师漏检删除真实目标。\n第1–6张仅行人辅助预览，第7–12张为C车辆候选。尚未确认新增审核配额，不要求全部签署。\n待核未解决就留草稿。刷新/关闭前导出JSON，再将下载文件发给我。\n',encoding='utf-8')
    panels(manifest,'drawn')
    counts=Counter(a['class'] for r in patch['reviews'] for a in r['actions'] if a['action']!='D')
    write_json(OUT/'draft_status.json',dict(status='AI_drawn_unsigned_preview',images=12,
        proposed_boxes=dict(counts),human_signed_new_frames=0,manual_assignment_authorized=False,
        main_C_vehicle_candidates=6,person_auxiliary_previews=6,
        dataset_frozen=False,G_ready=False,training_started=False,
        modified_originals=sum(a['action']=='M' for r in patch['reviews'] for a in r['actions']),
        removed_originals=sum(a['action']=='D' for r in patch['reviews'] for a in r['actions']),
        new_draft_boxes=sum(a['action']=='N' for r in patch['reviews'] for a in r['actions'])))
    print('Drawn unsigned previews:',dict(counts),flush=True)


def check():
    from .import_verified_review import _validate_patch
    manifest=read_json(OUT/'review_manifest_ai_draft.json');patch=read_json(OUT/'ai_draft_patch.json')
    assert dataset_id(manifest)==manifest['dataset_id']
    assert len(manifest['samples'])==len(patch['reviews'])==12
    assert Counter(s['split'] for s in manifest['samples'])=={'train':6,'stress':6}
    pilot.isolated(manifest['samples'])
    for path,digest in read_json(OUT/'source_bindings.json').items():assert sha256_file(Path(path))==digest,path
    for sample in manifest['samples']:assert sha256_file(OUT/sample['raw_file'])==sample['source_sha256']
    _validate_patch(OUT/'ai_draft_patch.json',manifest,{s['image_id']:s for s in manifest['samples']})
    assert not any(r['complete'] or r['raw_seen'] or r['reviewed_at_utc'] or any(r['checks'].values()) for r in patch['reviews'])
    page=(OUT/'index.html').read_text(encoding='utf-8')
    scripts=dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>',page,re.S))
    assert json.loads(scripts['review-manifest'])==manifest and json.loads(scripts['ai-draft'])==patch
    assert 'toggleDraftBoxes' in page and 'id="rawSeen"' not in page and 'id="checks"' not in page
    syntax=subprocess.run(['node','--check','-'],input=scripts['core']+'\n'+scripts['app-script'],
        text=True,encoding='utf-8',capture_output=True)
    assert syntax.returncode==0,syntax.stderr
    test=scripts['core']+'\nconst assert=require("node:assert/strict"),m='+scripts['review-manifest']+',p='+scripts['ai-draft']+';'+r'''
assert.deepEqual(WorkbenchCore.validateManifest(m),[]);
for(let i=0;i<m.samples.length;i++) {
  for(const a of p.reviews[i].actions) assert.deepEqual(WorkbenchCore.actionErrors(m.samples[i],a),[]);
  assert.ok(WorkbenchCore.completionErrors(m.samples[i],p.reviews[i]).length);
}
const bad=structuredClone(m);bad.samples.pop();assert.ok(WorkbenchCore.validateManifest(bad).length);
const a=structuredClone(p.reviews[0].actions[0]);a.bbox=[0,0,m.samples[0].width+1,10];
assert.ok(WorkbenchCore.actionErrors(m.samples[0],a).length);
console.log('PASS: manifest, draft coordinates, unsigned and invalid-input regressions');
'''
    result=subprocess.run(['node','-'],input=test,text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    evidence=dict(status='passed_bounded_file_and_core_checks',
        command='python -m cnn.prepare_virat_ai12 check',
        script_sha256=sha256_file(Path(__file__)),
        files_sha256={name:sha256_file(OUT/name) for name in
            ('index.html','review_manifest_ai_draft.json','ai_draft_patch.json','assistant_edits.json')},
        checks=['raw hashes','previous protected files unchanged','family split isolation',
                'manifest and embedded patch binding','unsigned signature rejection',
                'out-of-range and wrong-count rejection','JavaScript syntax'],
        browser_interaction_verified=False,
        browser_limitation='Automation rejected local file protocol; no workaround attempted',
        training_started=False,verified_GT=False)
    if not (OUT/'verification.json').exists():write_json(OUT/'verification.json',evidence)
    else:assert read_json(OUT/'verification.json')==evidence
    print(result.stdout.strip());print('PASS: previous inputs unchanged; no train/dev leakage or GT publication')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['fetch','build','teacher','inspect','draft','check'])
    args=parser.parse_args()
    globals()[args.action]()
