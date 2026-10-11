"""Bounded AC expansion: EPFL train candidates and independent PETS dev candidates."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request
import zipfile

from PIL import Image, ImageDraw

from . import prepare_ac_correction as pilot
from .prepare_ground48 import ROOT, blank_patch, dataset_id, read_json, sha256_file, write_json

OUT = ROOT / 'cnn/reports/ac_expansion8_20261010_v1'
DATA = ROOT / 'cnn/data/pets_ac_pilot_20261010'
URL = 'https://motchallenge.net/data/MOT15.zip'
SIZE = 1310994213
PETS_FRAMES = (100, 550)


class SourceRanges(io.RawIOBase):
    # ponytail: read-only HTTP seek adapter for stdlib ZIP; 8 MiB/request-budget ceiling, no full-archive fallback.
    def __init__(self):
        self.position, self.total, self.etag = 0, 0, None
        self.receipts = []

    def seek(self, offset, whence=0):
        self.position = offset if whence == 0 else self.position+offset if whence == 1 else SIZE+offset
        if not 0 <= self.position <= SIZE:
            raise ValueError('ZIP seek outside source')
        return self.position

    def tell(self):
        return self.position

    def seekable(self):
        return True

    def read(self, count=-1):
        count = SIZE-self.position if count < 0 else min(count, SIZE-self.position)
        if not count:
            return b''
        if self.total+count > 8*1024**2 or len(self.receipts) >= 40:
            raise ValueError('Bounded sample budget exceeded')
        start, end = self.position, self.position+count-1
        headers = {'Range': f'bytes={start}-{end}', 'User-Agent': 'RoadYOLO-research/1'}
        if self.etag:
            headers['If-Range'] = self.etag
        with urllib.request.urlopen(urllib.request.Request(URL, headers=headers), timeout=20) as response:
            if response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{SIZE}':
                raise ValueError('Range not honored; refuse full download')
            etag = response.headers.get('ETag')
            if not etag or (self.etag and self.etag != etag):
                raise ValueError('Source version changed')
            self.etag = etag
            raw = response.read(count+1)
            if len(raw) != count:
                raise ValueError('Incomplete source range')
        self.position += count
        self.total += count
        self.receipts.append(dict(start=start, end=end, bytes=count, sha256=hashlib.sha256(raw).hexdigest()))
        return raw


def fetch():
    if DATA.exists():
        raise FileExistsError('Preserve prior download/partial evidence')
    DATA.mkdir(parents=True)
    remote = SourceRanges()
    selected = []
    with zipfile.ZipFile(remote) as archive:
        wanted = ['gt/gt.txt'] + [f'img1/{frame:06d}.jpg' for frame in PETS_FRAMES]
        for suffix in wanted:
            matches = [n for n in archive.namelist() if n.endswith('train/PETS09-S2L1/'+suffix)]
            if len(matches) != 1:
                raise ValueError(f'Expected exactly one train PETS member: {suffix}')
            name = matches[0]
            info = archive.getinfo(name)
            if info.file_size > 2*1024**2:
                raise ValueError('Unexpected member size')
            raw = archive.read(info)  # stdlib verifies the original member CRC.
            destination = DATA / ('gt.txt' if suffix.startswith('gt/') else Path(suffix).name)
            with destination.open('xb') as stream:
                stream.write(raw)
            selected.append(dict(member=name, bytes=len(raw), crc32=info.CRC, sha256=sha256_file(destination), path=str(destination)))
    write_json(DATA / 'receipt.json', dict(url=URL, etag=remote.etag, archive_bytes=SIZE,
               archive_fully_downloaded=False, archive_sha256=None, downloaded_payload_bytes=remote.total,
               ranges=remote.receipts, members=selected, accessed_pixels_and_labels='train/PETS09-S2L1 only',
               source_page='https://motchallenge.net/data/MOT15/', license_page='https://motchallenge.net/',
               license_note='MOTChallenge states CC BY-NC-SA3.0; retain PETS attribution. Local research pilot only; public competition/republication not certified.',
               formal_test=False, training_started=False))
    print('PETS original JPEG2 + GT: downloaded', remote.total, 'bytes; full archive not downloaded', flush=True)


def build():
    if OUT.exists():
        raise FileExistsError('Preserve existing package')
    receipt = read_json(DATA / 'receipt.json')
    for item in receipt['members']:
        assert sha256_file(Path(item['path'])) == item['sha256']
    previous = pilot.OUT
    protected = {str(p): sha256_file(p) for p in pilot.protected_files()}
    protected.update({str(previous/'index.html'):sha256_file(previous/'index.html'),
                      str(previous/'review_manifest_teacher.json'):sha256_file(previous/'review_manifest_teacher.json')})
    latest = ROOT/'cnn/reports/ac_patch_check_20261010_v3/patch_validation.json'
    protected[str(latest)] = sha256_file(latest)
    OUT.mkdir()
    shutil.copy2(ROOT/'cnn/annotation_policy_v1.md', OUT/'annotation_policy_v1.md')
    samples = []
    # Put the new independent dev family in the first batch, not behind six training frames.
    for frame in PETS_FRAMES:
        originals = []
        for line_number, line in enumerate((DATA/'gt.txt').read_text(encoding='utf-8').splitlines(), 1):
            values = list(map(float, line.split(',')))
            if int(values[0]) != frame:
                continue
            if len(values) != 10 or values[6] != 1:
                raise ValueError('Unexpected PETS GT layout/confidence; manual mapping required')
            x, y, w, h = values[2:6]
            # MOT explicitly uses1-based image boxes; preview converts to native half-open0-based.
            box = [x-1, y-1, x-1+w, y-1+h]
            if not (0 <= box[0] < box[2] <= 768 and 0 <= box[1] < box[3] <= 576):
                raise ValueError('PETS box needs explicit edge policy, no silent clamp')
            originals.append(dict(target_id=f'o{len(originals)+1}', source_target_id=f'gt.txt:{line_number}',
                                 source_category='person', **{'class':'person'}, bbox=box,
                                 source_record=dict(row=line_number, values=values, track_id=int(values[1]))))
        samples.append(make_sample(f'pets09_s2l1_f{frame:06d}', DATA/f'{frame:06d}.jpg', originals,
                       'dev', 'PETS09-S2L1-all-views', 'PETS09-S2L1-view1',
                       'https://motchallenge.net/data/MOT15/', dict(frame_1based=frame, frame_0based=frame-1,
                       source_receipt_sha256=sha256_file(DATA/'receipt.json'), GT_sha256=sha256_file(DATA/'gt.txt'))))
    # Reuse the existing EPFL parser, never propagate the signed boxes to other frames.
    sys_path = str(ROOT/'cnn')
    import sys
    sys.path.insert(0, sys_path)
    from .prepare_ac_pilot import DATA as EPFL, epfl_boxes, FAMILY
    epfl_receipt = read_json(pilot.SCREEN/'epfl_download_receipt.json')
    for entry in epfl_receipt['downloads']:
        assert sha256_file(Path(entry['path'])) == entry['sha256']
    with zipfile.ZipFile(EPFL/'multiclass_ground_truth.zip') as labels, zipfile.ZipFile(EPFL/'multiclass_ground_truth_images.zip') as images:
        for camera, ordinal in ((0,80),(5,80),(4,80),(0,220),(5,220),(4,220)):
            member = f'c{camera}/{ordinal:08d}.jpg'
            raw = images.read(member)
            boxes, missing = epfl_boxes(labels, camera, ordinal)
            originals = [dict(target_id=f'o{i}', source_target_id=f'{b["member"]}:{b["row"]}',
                         source_category=b['source_class'], **{'class':'person' if b['source_class']=='person' else 'vehicle'},
                         bbox=b['xyxy_raw'], source_record=b) for i,b in enumerate(boxes,1)]
            samples.append(make_sample(f'epfl_c{camera}_o{ordinal:03d}', io.BytesIO(raw), originals,
                           'train', FAMILY, f'EPFL:c{camera}', 'https://www.epfl.ch/labs/cvlab/data/data-multiclass/',
                           dict(member=member, member_sha256=hashlib.sha256(raw).hexdigest(), archive_sha256=sha256_file(EPFL/'multiclass_ground_truth_images.zip'), annotation_ordinal=ordinal, original_video_frame=None, missing_class_files=missing)))
    for n,s in enumerate(samples):
        s.update(legacy_id=f'next{n+1:02d}', review_batch=1 if n<4 else 2, review_batch_ordinal=n%4+1)
    pilot.isolated(samples)
    manifest = dict(schema='cnn_review_workbench_v1', samples=samples, train_required_count=6,
                    bucket_counts={'train_review':6,'road_development':2},
                    annotation_policy_sha256=sha256_file(OUT/'annotation_policy_v1.md'),
                    teacher_status='pending CPU hints; source boxes not complete GT', verified_gt=False,
                    dataset_frozen=False, G_ready=False, training_started=False, formal_acceptance=False,
                    split_note='All EPFL synchronized views train candidates; entire PETS camera/original family dev only. Source train PETS used as local dev, not formal test.')
    manifest['dataset_id'] = dataset_id(manifest)
    write_json(OUT/'manifest_original.json', manifest)
    write_json(OUT/'review_patch_template.json', blank_patch(manifest))
    write_json(OUT/'source_bindings.json', protected)
    print('Built8 independent candidates, unsigned; no dataset freeze', flush=True)


def make_sample(image_id, source, originals, split, family, camera, url, source_record):
    directory = OUT/'images'/image_id
    directory.mkdir(parents=True)
    with Image.open(source) as image:
        image = image.convert('RGB')
    image.save(directory/'raw.png')
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for obj in originals:
        draw.rectangle(obj['bbox'], outline='#10c14a' if obj['class']=='person' else '#168aff', width=2)
        draw.text(obj['bbox'][:2], obj['target_id'], fill='white', stroke_width=1, stroke_fill='black')
    overlay.save(directory/'source_overlay.png')
    return dict(image_id=image_id, bucket='train_review' if split=='train' else 'road_development', split=split,
                split_status='proposed_family_reservation_not_dataset_freeze', scene='A', family_id=family, camera_id=camera,
                source_url=url, source_record=source_record, width=image.width, height=image.height,
                raw_file=f'images/{image_id}/raw.png', gt_overlay_file=f'images/{image_id}/source_overlay.png',
                source_sha256=sha256_file(directory/'raw.png'), original=originals, teacher=[],
                teacher_status='pending_CPU_hints', warnings=['来源参考非完整GT；检查停放车辆、骑行者和可见框范围。'], review_score=0)


def teacher():
    import time
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads, json_hash, load_official_model, teacher_input, tree_hash
    assert not (OUT/'review_manifest_teacher.json').exists(), 'Preserve hints'
    manifest = read_json(OUT/'manifest_original.json')
    assets = ROOT/'cnn/teacher_assets'
    receipt = read_json(assets/'receipt.json')
    source, weights = assets/'source/YOLOX-0.3.0', assets/'yolox_s.pth'
    assert sha256_file(weights) == receipt['weights']['sha256']
    assert tree_hash(source/'yolox') == receipt['source_tree_sha256']
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    device = torch.device('cpu')
    config = dict(device='cpu', threads=2, input='1024x576 FP32 official BGR', confidence=.1, nms_iou=.6,
                  dataset_id=manifest['dataset_id'], weights=receipt['weights']['sha256'], source_tree=receipt['source_tree_sha256'],
                  code={str(p.relative_to(ROOT)):sha256_file(p) for p in [Path(__file__), ROOT/'cnn/teacher.py',ROOT/'cnn/dataset.py',ROOT/'cnn/build_verified_review.py']},
                  torch_version=torch.__version__, kind='review_hints_not_GT_or_accuracy')
    model = load_official_model(source, weights, device)
    start = time.perf_counter()
    for sample in manifest['samples']:
        path = OUT/sample['raw_file']
        assert sha256_file(path) == sample['source_sha256']
        transform = _letterbox_transform(sample['width'],sample['height'])
        row = dict(image_path=path,preprocess=dict(raw_image=True,letterbox_1280x720=transform))
        predictions = decode_heads(capture_raw_heads(model, teacher_input(row,device)),transform)
        for n,p in enumerate(predictions):
            p.update(candidate_id=f't{n}',kind='REVIEW_HINT_NOT_ERROR_OR_GT')
        sample.update(teacher=predictions,teacher_status='CPU_hints_only_not_truth')
        print(sample['image_id'],len(predictions),'CPU hints',flush=True)
    assert dataset_id(manifest) == manifest['dataset_id']
    manifest['teacher_status'] = 'CPU hints all8; no GPU/training; not GT'
    write_json(OUT/'review_manifest_teacher.json',manifest)
    write_json(OUT/'teacher_receipt.json',dict(config=config,config_sha256=json_hash(config),seconds=time.perf_counter()-start,
               GPU_used=False,training_started=False,per_image={s['image_id']:len(s['teacher']) for s in manifest['samples']}))
    # Reuse the existing8-frame UI without modifying its source or the previous page.
    pilot.OUT = OUT
    pilot.render(manifest)


def check():
    from .import_verified_review import _validate_patch
    m = read_json(OUT/'review_manifest_teacher.json')
    assert dataset_id(m) == m['dataset_id'] and len(m['samples'])==8
    assert Counter(s['split'] for s in m['samples'])=={'dev':2,'train':6}
    pilot.isolated(m['samples'])
    bad = [dict(s) for s in m['samples']]
    bad[3]['split']='dev'
    try:
        pilot.isolated(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('EPFL family leakage accepted')
    for name,digest in read_json(OUT/'source_bindings.json').items():
        assert sha256_file(Path(name))==digest, name
    for s in m['samples']:
        assert sha256_file(OUT/s['raw_file'])==s['source_sha256']
    _,reviews,_ = _validate_patch(OUT/'review_patch_template.json',m,{s['image_id']:s for s in m['samples']})
    assert not any(r['complete'] for r in reviews.values())
    page = (OUT/'index.html').read_text(encoding='utf-8')
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>',page,re.S))
    assert read_json(OUT/'review_manifest_teacher.json') == __import__('json').loads(scripts['review-manifest'])
    assert 'id="rawSeen"' not in page and 'id="checks"' not in page and 'toggleDraftBoxes' in page
    js = scripts['core']+'\nconst assert=require("node:assert/strict"),m='+scripts['review-manifest']+';assert.deepEqual(WorkbenchCore.validateManifest(m),[]);assert.ok(WorkbenchCore.completionErrors(m.samples[0],{reviewer:"1",raw_seen:false,checks:{},actions:[]}).length);'
    result = subprocess.run(['node','-'],input=js,text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    result = subprocess.run(['node','--check','-'],input=scripts['core']+'\n'+scripts['app-script'],text=True,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    print('PASS8 original identities; split family leakage rejected; unsigned rejected; UI JS; old assets unchanged',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['fetch','build','teacher','check'])
    args=parser.parse_args()
    {'fetch':fetch,'build':build,'teacher':teacher,'check':check}[args.action]()
