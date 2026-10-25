"""Export the user's explicit chat approval without altering the unsigned draft."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

from PIL import Image

from cnn.collect_ac_signed import signed_sample
from cnn.dataset import _letterbox_transform, _letterboxed_box, audit
from cnn.import_verified_review import _validate_patch, _validate_action, ReviewError
from cnn.prepare_ac_correction import isolated
from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from cnn.reports.ac_replacement_review_20261013_v1.build_review import check as check_draft

BASE = Path(__file__).resolve().parent
OUT = ROOT/'cnn/reports/ac_g10_20261013_v1'
PROPOSAL = ROOT/'cnn/reports/ac_replacement_scope_20261013_v1/proposal.json'
CLOSURE = ROOT/'cnn/reports/ac_label_closure_20261013_v1/closure_manifest_v2.json'
QUOTE = '我看完了，觉得你的来源参考框应该都是正确的，你直接将所有标为正确自己导出json进行下一步'


def documents(stamp):
    manifest = read_json(BASE/'review_manifest.json')
    draft = read_json(BASE/'ai_draft_patch.json')
    patch = deepcopy(draft)
    approval = dict(kind='user_chat_approval_transcribed_by_assistant', user_quote=QUOTE,
        recorded_at_utc=stamp, reviewer='1',
        scope='Current displayed 24-frame preloaded draft accepted unchanged; A/M/N geometry preserved',
        checks_basis='User overall approval mapped to workbench complete fields; not browser click telemetry',
        prior_uncertainty='AI uncertainty notes retained as provenance; user accepted existing draft',
        draft_sha256=sha256_file(BASE/'ai_draft_patch.json'),
        manifest_sha256=sha256_file(BASE/'review_manifest.json'))
    for review in patch['reviews']:
        review.update(reviewer='1', reviewed_at_utc=stamp, raw_seen=True, complete=True,
                      checks={key:True for key in review['checks']})
        review['notes'] += '\n用户在聊天中确认本批通过并授权代导出；坐标和动作未改变。'
        review['confirmation_method'] = 'explicit_user_chat_approval_not_UI_click'
    patch['user_authorization'] = approval
    proposal = read_json(PROPOSAL)
    retained = {s['image_id']:s for s in read_json(CLOSURE)['images']}
    native = [deepcopy(retained[key]) for key in proposal['retained_reviewed_ids']]
    assert len(native) == 15
    assert all(s['human_signature_valid'] and s['review_unchanged'] and not s['holds'] for s in native)
    for sample, review in zip(manifest['samples'],patch['reviews'],strict=True):
        assert sample['image_id'] == review['image_id']
        row = signed_sample(sample,review,BASE/sample['raw_file'])
        row['approval_provenance'] = approval
        row['prior_AI_uncertainty'] = sample['ai_visual_review']['uncertain']
        native.append(row)
    isolated(native)
    assert len(native) == len({s['image_id'] for s in native}) == len({s['source_sha256'] for s in native}) == 39
    rows = []
    for sample in native:
        raw = Path(sample['raw_file_absolute'])
        assert sha256_file(raw) == sample['source_sha256']
        with Image.open(raw) as image:
            assert image.size == (sample['width'],sample['height'])
        transform = _letterbox_transform(sample['width'],sample['height'])
        boxes, labels, ignores = [], [], []
        for action in sample['labels']:
            x1,y1,x2,y2 = action['bbox']
            box = _letterboxed_box([x1,y1,x2-x1,y2-y1],transform)
            if action['class'] == 'ignore':
                ignores.append(box)
            else:
                boxes.append(box)
                labels.append({'person':0,'vehicle':1}[action['class']])
        rows.append(dict(image=str(raw), source_sha256=sample['source_sha256'],
            scene_id=sample['family_id'], camera_id=sample['camera_id'],
            source_frame=int(re.search(r'(\d+)$',sample['image_id'])[1]),
            split='train' if sample['split']=='train' else 'val', incomplete_frame=False,
            boxes=boxes, labels=labels, ignore_boxes=ignores,
            preprocess=dict(raw_image=True,letterbox_1280x720=transform),
            teacher_key=sample['image_id'], manual_review_image_id=sample['image_id'],
            native_labels=sample['labels']))
    dataset = dict(schema_version=1, task='detection', input_size=[512,288],
        classes=['person','vehicle'], manifest_status='development_AC_G10',
        purpose='User-approved tiny supervised diagnostic; not formal acceptance',
        training_eligible=True, formal_acceptance=False, max_optimizer_updates=10,
        dataset_id=manifest['dataset_id'], images=rows)
    result = audit(dataset)
    assert result['images_by_split'] == {'train':22,'val':17}
    assert result['incomplete_frames'] == 0 and not result['formal_training_eligible']
    return patch, native, dataset, result


def check():
    saved = read_json(OUT/'review_patch_user_authorized.json')
    patch,native,dataset,result = documents(saved['user_authorization']['recorded_at_utc'])
    assert saved == patch
    assert read_json(OUT/'verified_native_labels.json') == {'images':native,'formal_acceptance':False}
    assert read_json(OUT/'dataset.json') == dataset
    manifest = read_json(BASE/'review_manifest.json')
    _,reviews,_ = _validate_patch(OUT/'review_patch_user_authorized.json',manifest,
                                 {s['image_id']:s for s in manifest['samples']})
    assert len(reviews) == 24 and all(r['complete'] for r in reviews.values())
    draft = read_json(BASE/'ai_draft_patch.json')
    assert all(a['actions']==b['actions'] and not a['complete']
               for a,b in zip(draft['reviews'],patch['reviews'],strict=True))
    bad = deepcopy(native); bad[0]['split']='dev'
    try:
        isolated(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Family leakage not rejected')
    sample=manifest['samples'][0]
    invalid=deepcopy(patch['reviews'][0]['actions'][0]); invalid['bbox'][2]=sample['width']+1
    try:
        _validate_action(invalid,sample,{o['target_id']:o for o in sample['original']},set(),'negative')
    except ReviewError:
        pass
    else:
        raise AssertionError('Invalid box not rejected')
    for path,digest in read_json(OUT/'freeze_receipt.json')['source_bindings'].items():
        assert sha256_file(Path(path)) == digest,path
    print('PASS: 24 authorized records; A/M/N unchanged; 39 raw hashes; 22/17 family isolation; negative regressions')
    print(result['class_box_counts'])


def build():
    assert not OUT.exists(), 'Preserve existing experiment'
    check_draft()
    stamp = datetime.now(timezone.utc).isoformat()
    patch,native,dataset,result = documents(stamp)
    OUT.mkdir()
    write_json(OUT/'review_patch_user_authorized.json',patch)
    write_json(OUT/'verified_native_labels.json',dict(images=native,formal_acceptance=False))
    write_json(OUT/'dataset.json',dataset)
    sources = [BASE/'review_manifest.json',BASE/'ai_draft_patch.json',BASE/'index.html',
               BASE/'scope_approval.json',PROPOSAL,CLOSURE,Path(__file__)]
    write_json(OUT/'freeze_receipt.json',dict(status='tiny_diagnostic_data_frozen',
        recorded_at_utc=stamp, new_approved_images=24, prior_reviewed_images=15,
        dataset_sha256=sha256_file(OUT/'dataset.json'),
        authorized_patch_sha256=sha256_file(OUT/'review_patch_user_authorized.json'),
        source_bindings={str(p):sha256_file(p) for p in sources}, audit=result,
        historical_E7_exposure='pending comparison before launch',
        formal_acceptance=False, training_started=False,
        caveats=['Correlated frames, not 39 independent scenes.',
                 'Prior AI uncertainty retained; approval is user chat attestation, not objective pixel proof.',
                 'Non-16:9 source uses existing letterbox adapter; not native 720p camera evidence.']))
    check()


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'],['check'])
    globals()[sys.argv[1]]()
