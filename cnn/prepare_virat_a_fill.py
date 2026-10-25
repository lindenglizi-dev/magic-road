"""Fill only the A-scene candidate gap; never publish GT or start training."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import urllib.request

import cv2
from PIL import Image, ImageDraw

from . import prepare_virat_ac_expansion as base
from .prepare_ground48 import ROOT, dataset_id, read_json, sha256_file, write_json

OUT = ROOT/'cnn/reports/virat_a_fill_20261012_v1'
DATA = ROOT/'cnn/data/virat_a_fill_source_20261012_v1'
PREVIOUS = ROOT/'cnn/reports/virat_ac_expand_20261011_v1'
API = 'https://data.kitware.com/api/v1'
CLIPS = (
    ('VIRAT_S_010204_01_000072_000225', '56f588038d777f753209cc75', '56f57f4d8d777f753209c4de',
     'train', 55, 'VIRAT-0102xx-train-only-provisional'),
    ('VIRAT_S_050000_12_001591_001619', '56f58e7c8d777f753209cd93', '56f581958d777f753209c851',
     'dev', 24, 'VIRAT-0500xx-dev-only-provisional'),
    ('VIRAT_S_050000_10_001462_001491', '56f58e738d777f753209cd8d', '56f581938d777f753209c83f',
     'dev', 23, 'VIRAT-0500xx-dev-only-provisional'),
)


def fetch():
    DATA.mkdir(exist_ok=True)
    for clip, video_id, label_id, *_ in CLIPS:
        for item_id, suffix in ((video_id, '.mp4'), (label_id, '.viratdata.objects.txt')):
            path = DATA/(clip+suffix)
            receipt = path.with_suffix(path.suffix+'.receipt.json')
            if receipt.exists():
                assert sha256_file(path) == read_json(receipt)['sha256']
                continue
            assert not path.exists(), f'Preserve incomplete download: {path}'
            with urllib.request.urlopen(f'{API}/item/{item_id}/files', timeout=30) as response:
                files = json.load(response)
            assert len(files) == 1 and files[0]['name'] == path.name
            file = files[0]
            assert 0 < file['size'] < 100*1024**2
            url = f'{API}/file/{file["_id"]}/download'
            digest, count = hashlib.sha512(), 0
            with urllib.request.urlopen(url, timeout=45) as response, path.open('xb') as target:
                while chunk := response.read(1024**2):
                    count += len(chunk)
                    assert count <= file['size']
                    target.write(chunk)
                    digest.update(chunk)
            assert count == file['size'] and digest.hexdigest() == file['sha512']
            write_json(receipt, dict(url=url, item_id=item_id, official_file=file, bytes=count,
                sha256=sha256_file(path), sha512_verified=True,
                purpose='public A candidate screening, not blind test or certified GT'))
            print('Verified:', path.name, count, flush=True)


def screen():
    for clip, *_ in CLIPS:
        cap = cv2.VideoCapture(str(DATA/(clip+'.mp4')))
        assert cap.isOpened()
        total, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
        sheet = Image.new('RGB', (1536, 912), 'white')
        for j, frame in enumerate(base.selected_frames(total, 4, set())):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, image = cap.read()
            assert ok
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            image.thumbnail((768, 432))
            x, y = j % 2 * 768, j // 2 * 456
            sheet.paste(image, (x, y+24))
            ImageDraw.Draw(sheet).text((x+4, y+4), f'{clip} frame {frame}', fill='black')
        path = OUT/(clip+'_screen.jpg')
        assert not path.exists()
        sheet.save(path, quality=96)
        cap.release()
        print(clip, total, fps, flush=True)


def build():
    decision = read_json(OUT/'scene_decision.json')
    assert set(decision['accepted_clips']) == {r[0] for r in CLIPS}
    assert not (OUT/'manifest_original.json').exists()
    pool = read_json(base.POOL)
    previous = pool['images']+read_json(PREVIOUS/'manifest_original.json')['samples']
    protected = {str(p):sha256_file(p) for p in (base.POOL, PREVIOUS/'manifest_original.json',
        PREVIOUS/'ai_visual_patch.json', OUT/'scene_decision.json', Path(__file__), Path(base.__file__),
        ROOT/'cnn/model.py', ROOT/'cnn/annotation_policy_v1.md', ROOT/'cnn/teacher.py',
        ROOT/'cnn/build_verified_review.py', ROOT/'cnn/dataset.py')}
    base.assets.OUT = OUT
    samples, receipts = [], []
    for clip, _, _, split, count, family in CLIPS:
        video, labels = DATA/(clip+'.mp4'), DATA/(clip+'.viratdata.objects.txt')
        for p in (video, labels):
            assert sha256_file(p) == read_json(p.with_suffix(p.suffix+'.receipt.json'))['sha256']
            protected[str(p)] = sha256_file(p)
        rows = [(i,list(map(int,line.split()))) for i,line in enumerate(labels.read_text().splitlines(),1)]
        assert all(len(r)==8 for _,r in rows)
        cap = cv2.VideoCapture(str(video))
        assert cap.isOpened()
        total, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
        frames = base.selected_frames(total, count, set())
        assert min(b-a for a,b in zip(frames,frames[1:])) >= fps
        receipts.append(dict(clip=clip, split=split, scene='A', family=family, frame_count=total,
            fps=fps, selected_frames=frames, unique_source_person_tracks=len({r[0] for _,r in rows if r[2] in frames and r[7]==1}),
            annotation_outside_video_rows=[i for i,r in rows if not 0<=r[2]<total],
            note='Pre-inference uniform temporal anchors; correlated frames, not independent targets'))
        for frame in frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
            ok,bgr=cap.read()
            assert ok and abs(cap.get(cv2.CAP_PROP_POS_FRAMES)-(frame+1))<.5
            rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
            h,w=rgb.shape[:2]
            originals=[]
            for line,r in rows:
                track,duration,f,x,y,bw,bh,kind=r
                if f!=frame: continue
                assert 0<=x<x+bw<=w and 0<=y<y+bh<=h,(clip,line)
                originals.append(dict(target_id=f'o{len(originals)+1}',source_target_id=f'{labels.name}:{line}',
                    source_category=kind, **{'class':'person' if kind==1 else 'vehicle' if kind in (2,3) else 'ignore'},
                    bbox=[x,y,x+bw,y+bh],source_record=dict(line=line,row=r),certified_project_ignore=False))
            buf=io.BytesIO()
            Image.fromarray(rgb).save(buf,format='PNG');buf.seek(0)
            s=base.assets.make_sample(f'{clip}_f{frame:07d}',buf,originals,split,family,family,
                'https://viratdata.org/',dict(video=str(video),video_sha256=protected[str(video)],
                    annotations=str(labels),annotations_sha256=protected[str(labels)],frame_index=frame,
                    frame_origin='zero_based',fps=fps,full_static_GT_available=False))
            s.update(scene='A',legacy_id=f'F{len(samples)+1:03d}',training_eligible=False,human_complete=False,
                complete_GT_published=False,physical_camera_verified=False,
                scene_basis=decision['scene_basis'][clip],visual_review_status='not_individually_inspected')
            samples.append(s)
        cap.release()
    base.validate_samples(samples,previous)
    m=dict(schema='cnn_review_workbench_v1',samples=samples,train_required_count=55,
        bucket_counts={'train_review':55,'road_development':47},source_receipts=receipts,
        annotation_policy_sha256=sha256_file(ROOT/'cnn/annotation_policy_v1.md'),
        verified_gt=False,dataset_frozen=False,G_ready=False,training_started=False,human_signed_frames=0,new_human_assignments=0)
    m['dataset_id']=dataset_id(m)
    write_json(OUT/'manifest_original.json',m)
    write_json(OUT/'source_bindings.json',protected)
    print('Built102 A candidates; not GT, not training-ready',flush=True)


def draw():
    base.OUT=OUT
    base.draw()
    # Only generated presentation text changes; frozen helpers and previous outputs stay untouched.
    page=OUT/'index.html'
    text=page.read_text(encoding='utf-8').replace('A/C扩充54图','A场景补齐102图')
    text=text.replace('训练42张（A24/C18），开发候选12张（C）','训练候选55张（A），开发候选47张（A）')
    page.write_text(text,encoding='utf-8')


def check():
    from .import_verified_review import _validate_patch
    m=read_json(OUT/'review_manifest_teacher.json')
    previous=read_json(base.POOL)['images']+read_json(PREVIOUS/'manifest_original.json')['samples']
    assert dataset_id(m)==m['dataset_id']
    assert Counter((s['split'],s['scene']) for s in m['samples'])=={('train','A'):55,('dev','A'):47}
    base.validate_samples(m['samples'],previous)
    for p,digest in read_json(OUT/'source_bindings.json').items(): assert sha256_file(Path(p))==digest,p
    for s in m['samples']: assert sha256_file(OUT/s['raw_file'])==s['source_sha256']
    _,reviews,_=_validate_patch(OUT/'ai_draft_patch.json',m,{s['image_id']:s for s in m['samples']})
    assert not any(r['complete'] or r['reviewed_at_utc'] for r in reviews.values())
    bad=dict(m['samples'][0],image_id='negative_split_leak',source_sha256='0'*64,split='dev')
    for rows in ([m['samples'][0]],[bad]):
        try: base.validate_samples(rows,[m['samples'][0]])
        except (AssertionError,ValueError): pass
        else: raise AssertionError('Duplicate or cross-split leak accepted')
    write_json(OUT/'verification.json',dict(status='passed_file_checks_not_GT',images=102,
        merged_candidate_counts={'train':128,'dev':64},physical_camera_authoritative_id_verified=False,
        correlated_frame_warning=True,training_started=False,dataset_frozen=False,
        script_sha256=sha256_file(Path(__file__))))
    print('PASS102 unique frames, source hashes, split reservations, unsigned patch and negative regressions')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('fetch','screen','build','teacher','draw','check'))
    action=p.parse_args().action
    if action=='teacher':
        base.OUT=OUT
        base.teacher()
    else: globals()[action]()
