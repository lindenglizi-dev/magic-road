"""Archive the supplied VIRAT review without changing signatures or publishing GT."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import shutil

from PIL import Image

from .collect_ac_signed import signed_sample
from .import_verified_review import _validate_patch, _validate_action, ReviewError
from .prepare_ac_correction import isolated
from .prepare_ground48 import ROOT, dataset_id, read_json, sha256_file, write_json

SOURCE = Path('C:/Users/lenovo/Downloads/review_patch_b6741c9a883e_2026-10-10T14-04-53-924Z.json')
BASE = ROOT/'cnn/reports/virat_ai12_20261010_v2'
OUT = ROOT/'cnn/reports/virat_review_received_20261010_v1'


def inspect(patch_path):
    manifest=read_json(BASE/'review_manifest_ai_draft.json')
    assert dataset_id(manifest)==manifest['dataset_id']
    samples={s['image_id']:s for s in manifest['samples']}
    patch,reviews,_=_validate_patch(patch_path,manifest,samples)
    assert len(samples)==len(reviews)==12 and set(samples)==set(reviews)
    assert sha256_file(BASE/'annotation_policy_v1.md')==manifest['annotation_policy_sha256']
    protected=read_json(BASE/'source_bindings.json')
    for path,digest in protected.items():assert sha256_file(Path(path))==digest,path
    previous=read_json(ROOT/'cnn/reports/ac_signed_progress_20261010_v1/reviewed_partial_labels.json')
    assert not set(samples)&{s['image_id'] for s in previous['images']}
    isolated(manifest['samples']+previous['images'])
    initial={r['image_id']:r for r in read_json(BASE/'ai_draft_patch.json')['reviews']}
    completed,pending,changes=[],[],[]
    for sample in manifest['samples']:
        raw=BASE/sample['raw_file'];review=reviews[sample['image_id']]
        assert sha256_file(raw)==sample['source_sha256']
        with Image.open(raw) as image:assert image.size==(sample['width'],sample['height'])
        row=signed_sample(sample,review,raw)
        before={a['target_id']:a for a in initial[sample['image_id']]['actions']}
        after={a['target_id']:a for a in review['actions']}
        removed=[deepcopy(a) for key,a in before.items() if a['action']!='D' and
                 (key not in after or after[key]['action']=='D')]
        changes.append(dict(image_id=sample['image_id'],ordinal=sample['review_batch_ordinal'],
            removed_positive_drafts=removed,
            altered_actions=[deepcopy(a) for key,a in after.items() if before.get(key)!=a],
            inherited_notes_unchanged=review['notes']==initial[sample['image_id']]['notes'],
            source_uncertain_regions=sample['ai_visual_review']['uncertain_regions']))
        if row is None:
            pending.append(dict(image_id=sample['image_id'],ordinal=sample['review_batch_ordinal'],
                review=deepcopy(review),reason='export still incomplete; never fabricate confirmation'))
        else:
            row.update(training_eligible=False,complete_GT_published=False,
                eligibility_reason='received signature only; auxiliary/source/removed-positive and unresolved-region decisions not closed')
            completed.append(row)
    counts=Counter(a['class'] for r in reviews.values() for a in r['actions'] if a['action']!='D')
    signed_counts=Counter(a['class'] for s in completed for a in s['labels'])
    return dict(schema='cnn_virat_received_review_archive_v1',dataset_id=manifest['dataset_id'],
        status='received_partial_human_review_not_training_GT',patch_sha256=sha256_file(patch_path),
        manifest_sha256=sha256_file(BASE/'review_manifest_ai_draft.json'),
        reviews_received=len(reviews),completed_records=len(completed),pending=pending,
        current_draft_boxes=dict(counts),completed_record_boxes=dict(signed_counts),
        completed_splits=dict(Counter(s['split'] for s in completed)),
        removed_positive_drafts=sum(len(c['removed_positive_drafts']) for c in changes),
        images=completed,changes=changes,
        original_review_flags_preserved=True,original_patch_modified=False,
        previous_archive_sha256=sha256_file(ROOT/'cnn/reports/ac_signed_progress_20261010_v1/reviewed_partial_labels.json'),
        protected_files=protected,physical_camera_mapping_fully_verified=False,
        training_started=False,dataset_frozen=False,G_ready=False,complete_GT_published=False,
        cautions=['A deletion is not proof of background; no automatic negative-mask generation.',
                  'Unchanged AI uncertainty notes remain traceable; human region dispositions not inferred.',
                  'Courtyard stress/auxiliary frames are not silently promoted into main A/C training.',
                  'Receipt proves file/signature consistency, not pixel-level truth or acceptance accuracy.'])


def check():
    snapshot=OUT/SOURCE.name
    result=inspect(snapshot if snapshot.exists() else SOURCE)
    if (OUT/'review_archive.json').exists():assert read_json(OUT/'review_archive.json')==result
    # Runnable negative checks: an unsigned record stays unsigned; invalid boxes and identity fail.
    assert signed_sample({},dict(complete=False),Path('unused')) is None
    manifest=read_json(BASE/'review_manifest_ai_draft.json');sample=manifest['samples'][0]
    invalid=dict(target_id='new',action='N',**{'class':'person'},bbox=[0,0,sample['width']+1,10],
        reason='negative check',ai_assisted=False)
    try:_validate_action(invalid,sample,{a['target_id']:a for a in sample['original']},set(),'negative')
    except ReviewError:pass
    else:raise AssertionError('Out-of-range box accepted')
    wrong=deepcopy(manifest);wrong['dataset_id']='0'*64
    try:_validate_patch(snapshot if snapshot.exists() else SOURCE,wrong,{s['image_id']:s for s in manifest['samples']})
    except ReviewError:pass
    else:raise AssertionError('Wrong dataset identity accepted')
    print('PASS: identities, coordinates, signatures, source hashes, prior archive preserved, negative regressions')
    print(result['completed_records'],'complete;',len(result['pending']),'pending;',result['current_draft_boxes'])
    return result


def build():
    assert not OUT.exists(),'Preserve earlier archive'
    result=check()
    OUT.mkdir()
    shutil.copy2(SOURCE,OUT/SOURCE.name)
    assert sha256_file(OUT/SOURCE.name)==result['patch_sha256']
    write_json(OUT/'review_archive.json',result)
    write_json(OUT/'receipt.json',{key:result[key] for key in
        ('status','dataset_id','patch_sha256','manifest_sha256','reviews_received','completed_records',
         'current_draft_boxes','completed_record_boxes','completed_splits','removed_positive_drafts',
         'training_started','dataset_frozen','G_ready','complete_GT_published')})
    check()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['build','check'])
    globals()[parser.parse_args().action]()
