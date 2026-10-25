"""Replay102-frame AI visual edits without changing source labels or human signatures."""
from collections import Counter
from copy import deepcopy
from html import escape
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw

from . import refine_virat_ac_expansion as edits_core
from .prepare_ground48 import read_json, sha256_file, write_json
from .prepare_virat_a_fill import OUT
from .import_verified_review import _validate_patch

EDITS = OUT/'assistant_visual_edits.json'
PATCH = OUT/'ai_visual_patch.json'
PAGE = OUT/'visual_index.html'
REPORT = OUT/'visual_status.json'


def record():
    m=read_json(OUT/'review_manifest_teacher.json');patch=read_json(OUT/'ai_draft_patch.json')
    edits={}
    # ponytail: these fixed-view rules only create review drafts, never automatic GT or training masks.
    cones=((440,435,510,525),(650,790,710,880),(825,565,900,655),
           (1070,270,1130,325),(1030,595,1115,650),(475,0,515,85),
           (530,90,585,160),(720,390,790,480),(525,130,580,190))
    for s,r in zip(m['samples'],patch['reviews'],strict=True):
        e=dict(note='AI联系表初查；不是逐目标完整GT。原始来源与教师缓存不变，待定不当背景。',remove={},delete_source={},uncertain=[],add=[],modify={})
        if s['split']=='train':
            for a in r['actions']:
                if a['action']=='N' and a['class']=='vehicle' and a['bbox'][3]<280:
                    e['remove'][a['target_id']]='远端细小车辆提示缺乏可确认车体，移入待定，不宣称误报或背景'
                    e['uncertain'].append(dict(bbox=a['bbox'],reason=e['remove'][a['target_id']]))
            e['uncertain'].append(dict(bbox=[90,215,360,290],reason='远端相邻人/重复来源轨迹及遗漏尚未逐目标核实；不能自动忽略小人'))
        else:
            e['note']+=' 独立直路迁移子组，含施工/公交，不冒充纯校园开发集。'
            later='_12_' in s['image_id']
            shift=0 if later else 10
            for a in r['actions']:
                x1,y1,x2,y2=a['bbox'];cx,cy=(x1+x2)/2,(y1+y2)/2
                if a['action']=='N':
                    if a['class']=='vehicle' and x2-x1<100 and y2-y1<110 and any(l<=cx<=rr and t<=cy<=b for l,t,rr,b in cones):
                        e['remove'][a['target_id']]='固定画面锥桶/信号灯/标牌，不是车体；AI原图和联系表初查清理'
                    if a['class']=='person' and ((535<=cx<=585 and 80<=cy<=165) or (620<=cx<=690 and 520<=cy<=625)):
                        e['remove'][a['target_id']]='施工锥桶/警示设施外形，不是可见人体；AI原图初查清理'
                if a['action']=='A' and a['class']=='vehicle' and x2<720 and y2<900:
                    known_truck=430<x1<510 and 100<y1<175 and x2>600
                    if not known_truck:
                        reason='树遮挡原轨迹框或非五类车辆的施工设备，可见范围/类别未核实，暂移待定；不当背景'
                        e['delete_source'][a['target_id']]=reason
                        e['uncertain'].append(dict(bbox=a['bbox'],reason=reason))
                if (a['class']=='ignore' or a['action']=='N') and 815<cx<950 and 145<cy<280:
                    if a['action']=='A': e['delete_source'][a['target_id']]='三辆停放摩托车，拆成独立vehicle草稿，原ignore不继承'
                    else: e['remove'][a['target_id']]='摩托车簇提示与独立补框重复，保留三个分离车体草稿'
                if a['class']=='ignore' and 1260<cx<1440 and 775<cy<875:
                    e['modify'][a['target_id']]=dict(**{'class':'vehicle'},bbox=[1290,798+shift,1415,850+shift],
                        reason='白色厢车旁停放摩托车，可见车体转为vehicle草稿，非确认GT')
            for box in ([836,165,914,220],[843,181,919,239],[867,186,934,275]):
                e['add'].append(dict(**{'class':'vehicle'},bbox=[box[0],box[1]+shift,box[2],box[3]+shift],
                    reason='AI原图放大后三辆停放摩托车分别补画；同机位静态传播草稿，精确边界仍待核'))
            e['uncertain'].append(dict(bbox=[0,0,720,1080],reason='树遮挡车的可见范围、施工机械/拖车类别未闭合，区域记录不是已批准ignore'))
        edits[s['legacy_id']]=e
    for key,targets in {'F012':['teacher_t3'],'F022':['teacher_t9'],'F036':['teacher_t16'],
                        'F038':['teacher_t2','teacher_t4','teacher_t14']}.items():
        for t in targets: edits[key]['remove'][t]='AI无框原图对照：同一人体局部重复或腿部误当车辆，保留独立人体草稿'
    edits['F038']['modify']['o9']=dict(**{'class':'person'},reason='来源ignore实际为独立行人，按原图改person草稿')
    for key,targets in {'F038':['o2'],'F040':['o3','o15','o9'],'F041':['o3']}.items():
        for t in targets: edits[key]['delete_source'][t]='AI原图可见同一人体的重复来源框，草稿只保留一框'
    for key,target in [('F040','o10'),('F041','o10')]:
        edits[key]['delete_source'][target]='来源整个人车混合ignore，草稿按骑行人体person和车体vehicle拆分'
    edits['F041']['modify']['teacher_t6']=dict(bbox=[915,505,1000,670],reason='骑行者人体与车体拆开，按无框原图修正人体范围')
    edits['F041']['modify']['teacher_t14']=dict(bbox=[895,601,1000,720],reason='骑行车体单独vehicle，裁到图边，不含整个骑行者')
    write_json(EDITS,dict(dataset_id=m['dataset_id'],images=edits,inspection=dict(
        contact_sheet_frames=[s['legacy_id'] for s in m['samples']],
        full_raw_frames=['F012','F022','F038','F040','F041','F056','F080'],
        raw_source_screen_frames=12,additional_raw_crop='motorcycle_raw_crop.png',
        method='AI contact-sheet first pass102, full raw7 plus12 source-screen frames; fixed-view draft propagation, not exhaustive truth verification',human_review=False)))


def revised(manifest, edits):
    assert edits['dataset_id']==manifest['dataset_id']
    edits_core.EDITS=EDITS
    return edits_core.corrected(manifest,read_json(OUT/'ai_draft_patch.json'),edits)


def build():
    assert not any(p.exists() for p in (PATCH,PAGE,REPORT))
    m,edits=read_json(OUT/'review_manifest_teacher.json'),read_json(EDITS)
    patch=revised(m,edits)
    write_json(PATCH,patch)
    _validate_patch(PATCH,m,{s['image_id']:s for s in m['samples']})
    counts,cards=Counter(),[]
    for s,r in zip(m['samples'],patch['reviews'],strict=True):
        edit=edits['images'][s['legacy_id']]
        image=Image.open(OUT/s['raw_file']).convert('RGB');d=ImageDraw.Draw(image)
        for a in r['actions']:
            if a['action']=='D': continue
            counts[(s['split'],a['class'])]+=1
            color='#aaaaaa' if a['class']=='ignore' else '#00dd66' if a['action']=='A' else '#00c8ff'
            d.rectangle(a['bbox'],outline=color,width=2)
            d.text(a['bbox'][:2],a['target_id']+' '+a['class'],fill=color,stroke_width=1,stroke_fill='black')
        for i,u in enumerate(edit.get('uncertain',[]),1):
            d.rectangle(u['bbox'],outline='#ffaa00',width=2)
            d.text(u['bbox'][:2],f'uncertain{i}',fill='#ffaa00',stroke_width=1,stroke_fill='black')
        path=f'images/{s["image_id"]}/ai_visual.png'
        assert not (OUT/path).exists()
        image.save(OUT/path)
        cards.append(f'<article><h2>{s["legacy_id"]} {s["split"]} / A</h2><p>{escape(edit["note"])}</p>'
            f'<img src="{path}" alt="AI修订草稿"><details><summary>无框原图</summary><img src="{s["raw_file"]}" alt="无框原图"></details>'
            f'<details><summary>512输入</summary><img src="images/{s["image_id"]}/network.png" alt="512输入"></details></article>')
    with PAGE.open('x',encoding='utf-8') as f:
        f.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>A补齐102图</title>'
            '<style>body{font-family:system-ui;max-width:1280px;margin:auto}img{max-width:100%}article{border-bottom:2px solid #888;margin:30px 0}summary{cursor:pointer}</style>'
            '<h1>A场景补齐102张：AI草稿</h1><p>训练55张校园入口；开发47张独立直路机位，含施工和公交，单独作为A迁移子组。'
            '绿＝来源，青＝补充/修订，橙＝待定，灰＝未核实来源ignore。均非人工GT，不要求现在逐张签署，未启动训练。</p>'
            '<p>同视频帧有关联，数量不代表独立目标/机位数；待定区域不能作为背景或自动ignore。</p>'+''.join(cards)+'</html>')
    report=dict(status='AI_visual_first_pass_unsigned',images=len(m['samples']),
        proposed_boxes={split:{label:counts[(split,label)] for label in ('person','vehicle','ignore')} for split in ('train','dev')},
        inspection=edits['inspection'],edits_sha256=sha256_file(EDITS),patch_sha256=sha256_file(PATCH),
        page_sha256=sha256_file(PAGE),script_sha256=sha256_file(Path(__file__)),core_sha256=sha256_file(Path(edits_core.__file__)),
        input_sha256={name:sha256_file(OUT/name) for name in ('manifest_original.json','review_manifest_teacher.json','ai_draft_patch.json','teacher_receipt.json','verification.json')},
        removed_teacher_proposals=sum(len(e.get('remove',{})) for e in edits['images'].values()),
        deleted_source_proposals=sum(len(e.get('delete_source',{})) for e in edits['images'].values()),
        modified_boxes=sum(len(e.get('modify',{})) for e in edits['images'].values()),
        added_boxes=sum(len(e.get('add',[])) for e in edits['images'].values()),
        uncertain_regions=sum(len(e.get('uncertain',[])) for e in edits['images'].values()),
        human_signed_new_frames=0,new_human_assignments=0,dataset_frozen=False,G_ready=False,training_started=False)
    write_json(REPORT,report)


def check():
    m,edits,report=read_json(OUT/'review_manifest_teacher.json'),read_json(EDITS),read_json(REPORT)
    assert len(m['samples'])==102 and report['images']==102
    assert read_json(PATCH)==revised(m,edits)
    _validate_patch(PATCH,m,{s['image_id']:s for s in m['samples']})
    for name,digest in report['input_sha256'].items(): assert sha256_file(OUT/name)==digest,name
    for field,p in (('edits_sha256',EDITS),('patch_sha256',PATCH),('page_sha256',PAGE),('script_sha256',Path(__file__)),('core_sha256',Path(edits_core.__file__))):
        assert sha256_file(p)==report[field],p
    links=re.findall(r'<img src="([^"]+)"',PAGE.read_text(encoding='utf-8'))
    assert len(links)==306 and all((OUT/p).is_file() for p in links)
    bad=deepcopy(edits);bad['images']['F001']['remove']={'missing_target':'negative regression'}
    try: revised(m,bad)
    except AssertionError: pass
    else: raise AssertionError('Unknown target accepted')
    print('PASS102 unsigned visual edits, coordinates, hashes,306 links, invalid-target rejection')


if __name__=='__main__':
    assert sys.argv[1:] in (['record'],['build'],['check'])
    if sys.argv[1]=='record': record()
    else:
        if sys.argv[1]=='build': build()
        check()
