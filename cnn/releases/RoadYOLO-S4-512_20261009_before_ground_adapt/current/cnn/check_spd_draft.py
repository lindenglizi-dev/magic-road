"""Read-only label diagnostics and overlays, never GT sign-off or auto correction."""
import argparse
from collections import Counter
import html
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess

import cv2

from .prepare_ground48 import ROOT, read_json, sha256_file, write_json
from .prepare_spd_pilot import RIDERS


def intersection(a, b):
    return max(0, min(a[2], b[2])-max(a[0], b[0])) * max(0, min(a[3], b[3])-max(a[1], b[1]))


def area(a):
    return (a[2]-a[0])*(a[3]-a[1])


def iou(a, b):
    common = intersection(a, b)
    return common/(area(a)+area(b)-common)


def associate(riders, boxes, label):
    # ponytail: at most three riders here; greedy overlap is a diagnostic proposal,
    # not a semantic assignment or proof of completeness. Human review resolves ambiguity.
    edges = []
    for rider in riders:
        for box in boxes:
            if box['class'] == label:
                fraction = intersection(rider['bbox_xyxy'], box['bbox']) / area(box['bbox'])
                if fraction >= .5:
                    edges.append((fraction, iou(rider['bbox_xyxy'], box['bbox']), rider['source_id'], box['id']))
    result, used = {}, set()
    for fraction, overlap, source, target in sorted(edges, reverse=True):
        if source not in result and target not in used:
            result[source] = dict(draft_id=target, containment=round(fraction,4), iou=round(overlap,4))
            used.add(target)
    return result


def diagnose(sample, review):
    boxes = review['boxes']
    duplicates = [dict(first=a['id'], second=b['id'], iou=round(iou(a['bbox'],b['bbox']),4))
        for a,b in itertools.combinations(boxes,2)
        if a['class']==b['class'] and iou(a['bbox'],b['bbox']) >= .85]
    riders = [obj for obj in sample['objects'] if obj['source_type'] in RIDERS]
    person, vehicle = associate(riders,boxes,'person'), associate(riders,boxes,'vehicle')
    rider_checks = [dict(source_id=obj['source_id'], source_type=obj['source_type'],
                        source_bbox=obj['bbox_xyxy'], person=person.get(obj['source_id']),
                        vehicle=vehicle.get(obj['source_id'])) for obj in riders]
    missing = []
    for obj in sample['objects']:
        if obj['proposed_class'] and not any(b['class']==obj['proposed_class']
                and iou(b['bbox'],obj['bbox_xyxy']) >= .5 for b in boxes):
            missing.append(obj['source_id'])
    conflicts = []
    for box in boxes:
        source = next((obj for obj in sample['objects'] if obj['source_id']==box['source_id']),None)
        if source is not None and iou(source['bbox_xyxy'],box['bbox']) < .1:
            conflicts.append(dict(draft_id=box['id'], source_id=source['source_id'],
                                  reason='tagged source and draft spatially inconsistent; not automatic deletion'))
    return dict(sample_id=sample['sample_id'], boxes=len(boxes), counts=dict(Counter(b['class'] for b in boxes)),
                duplicates=duplicates, rider_checks=rider_checks, missing_source_support=missing,
                binding_conflicts=conflicts, empty_draft=not boxes, complete_gt=False)


def draw(canvas, box, label, color, offset=(0,0)):
    x0,y0,x1,y1 = [round(value-offset[i%2]) for i,value in enumerate(box)]
    cv2.rectangle(canvas,(x0,y0),(x1,y1),color,2)
    text_size = cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,.55,1)[0]
    x=max(0,min(x0,canvas.shape[1]-text_size[0]-4)); y=max(18,min(y0-4,canvas.shape[0]-4))
    cv2.rectangle(canvas,(x,y-17),(x+text_size[0]+4,y+4),(0,0,0),-1)
    cv2.putText(canvas,label,(x+2,y),cv2.FONT_HERSHEY_SIMPLEX,.55,color,1)


def check(draft_path, package, output):
    if output.exists():
        raise FileExistsError(output)
    manifest, draft = read_json(package/'draft_manifest.json'),read_json(draft_path)
    page = (package/'index.html').read_text(encoding='utf-8')
    scripts = '\n'.join(re.search(r'<script id="'+key+r'">(.*?)</script>',page,re.S).group(1)
                        for key in ('core','draft-core'))
    validation = subprocess.run(['node','-'],input=scripts+'\nSpDraftCore.validateDraft('
        +json.dumps(draft,ensure_ascii=True)+','+json.dumps(manifest,ensure_ascii=True)+');',
        text=True,capture_output=True)
    if validation.returncode:
        raise ValueError(validation.stderr)
    protected = [draft_path,package/'draft_manifest.json',package/'index.html']
    protected += [package/'raw'/(s['sample_id']+ext) for s in manifest['samples'] for ext in ('.jpg','.json')]
    before = {str(p):sha256_file(p) for p in protected}
    for sample in manifest['samples']:
        for key, ext in (('image_sha256','.jpg'),('label_sha256','.json')):
            if sha256_file(package/'raw'/(sample['sample_id']+ext)) != sample[key]:
                raise ValueError('actual raw source hash mismatch')
    output.mkdir(parents=True,exist_ok=False)
    (output/'views').mkdir()
    shutil.copy2(draft_path,output/draft_path.name)
    reports, cards, tiles = [], [], []
    for sample in manifest['samples']:
        review = next(r for r in draft['reviews'] if r['sample_id']==sample['sample_id'])
        report = diagnose(sample,review);reports.append(report)
        if not review['boxes']:
            continue
        raw=cv2.imread(str(package/'raw'/(sample['sample_id']+'.jpg')))
        if raw is None:
            raise ValueError('image decode failed')
        canvas=raw.copy()
        for box in review['boxes']:
            draw(canvas,box['bbox'],box['id']+' '+box['class'],(0,255,0) if box['class']=='person' else (255,200,0))
        filename=f'views/{sample["sample_id"]}_draft.jpg'
        if not cv2.imwrite(str(output/filename),canvas):
            raise OSError(filename)
        tile=cv2.resize(canvas,(960,540));cv2.putText(tile,sample['sample_id'],(10,30),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,0,255),2);tiles.append(tile)
        crops=[]
        for rider in report['rider_checks']:
            x0,y0,x1,y1=rider['source_bbox'];pad=max(30,round(max(x1-x0,y1-y0)*.3))
            x0,y0,x1,y1=max(0,int(x0)-pad),max(0,int(y0)-pad),min(sample['width'],int(x1)+pad),min(sample['height'],int(y1)+pad)
            crop=raw[y0:y1,x0:x1].copy();region=[x0,y0,x1,y1]
            draw(crop,rider['source_bbox'],rider['source_id']+' official rider',(0,150,255),(x0,y0))
            for box in review['boxes']:
                if intersection(box['bbox'],region)>0:
                    draw(crop,box['bbox'],box['id']+' '+box['class'],(0,255,0) if box['class']=='person' else (255,200,0),(x0,y0))
            cropfile=f'views/{sample["sample_id"]}_{rider["source_id"]}.jpg'
            if not cv2.imwrite(str(output/cropfile),crop):
                raise OSError(cropfile)
            text=f'{rider["source_id"]}: person={rider["person"]}, vehicle={rider["vehicle"]}'
            crops.append(f'<figure><figcaption>{html.escape(text)}</figcaption><img src="{cropfile}"></figure>')
        details=html.escape(json.dumps(report,ensure_ascii=False,indent=2))
        cards.append(f'<section><h2>{sample["sample_id"]} · {report["counts"]}</h2><details open><summary>人工草稿叠框</summary><img src="{filename}"></details><details><summary>骑行者局部核对（橙色是官方整体框）</summary>{"".join(crops)}</details><details><summary>自动几何提示（不是漏检结论）</summary><pre>{details}</pre></details></section>')
    if tiles:
        import numpy as np
        if len(tiles)%2:
            tiles.append(np.zeros_like(tiles[0]))
        montage=np.concatenate([np.concatenate(tiles[i:i+2],axis=1) for i in range(0,len(tiles),2)],axis=0)
        cv2.imwrite(str(output/'views/montage.jpg'),montage)
    write_json(output/'diagnostics.json',reports)
    summary=dict(stage='WAIT_TARGETED_REVIEW',nonempty_images=sum(not r['empty_draft'] for r in reports),
        excluded_empty=[r['sample_id'] for r in reports if r['empty_draft']],
        draft_boxes=sum(r['boxes'] for r in reports),near_duplicate_pairs=sum(len(r['duplicates']) for r in reports),
        rider_pairs_without_geometric_support=[dict(sample=r['sample_id'],source=x['source_id'],person=x['person'],vehicle=x['vehicle'])
            for r in reports if not r['empty_draft'] for x in r['rider_checks'] if not x['person'] or not x['vehicle']],
        binding_conflict_count=sum(len(r['binding_conflicts']) for r in reports),
        input_draft_sha256=sha256_file(draft_path),complete_gt=False,training='NOT_RUN',
        limitations=['Geometry cannot prove no unlabeled targets; missing support is a review prompt, not confirmed missed person.',
                     'No boxes changed, re-linked, accepted or deleted. Eighth empty draft not treated as a negative image.'])
    write_json(output/'execution_status.json',summary)
    write_json(output/'protected_files_check.json',dict(baseline_sha256=before,
        all_unchanged=all(sha256_file(Path(p))==h for p,h in before.items())))
    with (output/'index.html').open('x',encoding='utf-8') as handle:
        handle.write('<!doctype html><html lang="zh"><meta charset="utf-8"><title>SPD草稿复核</title><style>body{font-family:sans-serif;max-width:1300px;margin:24px auto}img{max-width:100%}section{border:1px solid #aaa;padding:16px;margin:20px 0}summary{padding:10px;cursor:pointer}pre{white-space:pre-wrap}figure img{max-width:600px}</style><h1>前7图人工草稿复核：不是完整GT</h1><p>绿色person，蓝色vehicle；骑行者局部橙框是官方整体来源，不是教师框。自动匹配仅提示，不修改标签；第8图空草稿暂排除。</p>'+''.join(cards)+'</html>')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--draft',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(check(a.draft,a.package,a.output),ensure_ascii=False,indent=2))
