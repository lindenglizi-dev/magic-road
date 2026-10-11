"""Publish the explicitly human-approved SPD eight-frame development set only."""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import shutil

from .check_spd_draft import check
from .dataset import _letterbox_transform, _letterboxed_box, audit
from .evaluate import load_validation_subset
from .prepare_ground48 import read_json, sha256_file, write_json


DRAFT_SHA = '96e2913a471bcde353893ef29c5ac92e6938e80e3493ff8221ce3947c98ecd24'
CHECKPOINT_SHA = '17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42'


def convert(sample, review):
    transform = _letterbox_transform(sample['width'], sample['height'])
    boxes, labels, ignores = [], [], []
    for item in review['boxes']:
        x0, y0, x1, y1 = item['bbox']
        box = _letterboxed_box([x0, y0, x1-x0, y1-y0], transform)
        if item['class'] == 'ignore':
            ignores.append(box)
        else:
            boxes.append(box)
            labels.append({'person': 0, 'vehicle': 1}[item['class']])
    return dict(image=f'raw/{sample["sample_id"]}.jpg',
        source_sha256=sample['image_sha256'], scene_id=sample['source_group'],
        source_frame=int(sample['frame_id']), split='val', incomplete_frame=False,
        boxes=boxes, labels=labels, ignore_boxes=ignores,
        preprocess=dict(raw_image=True, letterbox_1280x720=transform),
        teacher_key=sample['sample_id'], native_labels=deepcopy(review['boxes']),
        source_association_policy='original source_id retained as provenance only; not used to score',
        camera_id=sample['camera_id'], clip_id=sample['sequence_id'])


def publish(draft_path, package, checkpoint, output, approved):
    if not approved or sha256_file(draft_path) != DRAFT_SHA:
        raise ValueError('requires explicit human confirmation bound to the reviewed draft hash')
    if sha256_file(checkpoint) != CHECKPOINT_SHA:
        raise ValueError('frozen E7 checkpoint hash mismatch')
    if output.exists():
        raise FileExistsError(output)
    manifest, draft = read_json(package/'draft_manifest.json'), read_json(draft_path)
    if len(manifest['samples']) != 8:
        raise ValueError('exactly eight reviewed frames required')
    # Reuse actual UI validation, source byte checks and diagnostic overlays.
    status = check(draft_path, package, output/'label_check')
    if status['nonempty_images'] != 8 or status['near_duplicate_pairs']:
        raise ValueError('empty frame or unresolved duplicate review')
    diagnostics = json.loads((output/'label_check/diagnostics.json').read_text(encoding='utf-8'))
    unresolved = [(row['sample_id'], rider['source_id']) for row in diagnostics
        for rider in row['rider_checks'] if not rider['person'] or not rider['vehicle']]
    if unresolved != [('spd_inf_010881', 'o11')]:
        raise ValueError('unexpected unresolved rider; do not silently exclude')
    unsupported = [(row['sample_id'], source) for row in diagnostics
                   for source in row['missing_source_support']]
    if unsupported != [('spd_inf_010907', 'o12')]:
        raise ValueError('unexpected unsupported official source')
    (output/'raw').mkdir()
    rows = []
    for sample in manifest['samples']:
        for ext in ('.jpg', '.json'):
            shutil.copy2(package/'raw'/(sample['sample_id']+ext), output/'raw'/(sample['sample_id']+ext))
        review = next(r for r in draft['reviews'] if r['sample_id'] == sample['sample_id'])
        rows.append(convert(sample, review))
    dataset = dict(schema_version=1, task='detection', input_size=[512, 288],
        classes=['person', 'vehicle'], manifest_status='development_spd_val8',
        purpose='human-confirmed full-frame development evaluation only',
        # Existing ground48/evaluation schema uses this compatibility flag.
        # All rows are val; the training loader rejects a manifest without train.
        training_eligible=True, evaluation_only=True, formal_acceptance=False,
        images=rows)
    write_json(output/'spd_val8.json', dataset)
    selected, count = load_validation_subset(output/'spd_val8.json', None, 8)
    assert len(selected) == count == 8
    counts = Counter(item['class'] for review in draft['reviews'] for item in review['boxes'])
    assert counts == {'person': 25, 'vehicle': 120}
    receipt = dict(status='published_human_confirmed_development_only',
        review_confirmation='无修改，已复核无问题', reviewer=draft['reviewer'],
        confirmation_source='direct user message in this chat, not draft complete_gt flag',
        draft_complete_gt_preserved=draft['complete_gt'], image_count=8,
        labels=dict(counts), scene_count=len({s['source_group'] for s in manifest['samples']}),
        draft_sha256=DRAFT_SHA, dataset_sha256=sha256_file(output/'spd_val8.json'),
        checkpoint=str(checkpoint.resolve()), checkpoint_sha256=CHECKPOINT_SHA,
        fully_occluded_source_exclusions=[dict(sample_id='spd_inf_010881', source_id='o11',
            reason='user confirmed fully occluded and not visually identifiable',
            scoring='not positive GT; no ignore region or prediction suppression introduced')],
        user_directed_source_exclusions=[dict(sample_id='spd_inf_010907', source_id='o12',
            reason='user explicitly instructed not to add o12 and to proceed with reviewed image',
            visibility='not asserted fully occluded',
            scoring='no positive GT and no ignore region; unmatched predictions remain false positives')],
        association_conflicts_preserved=status['binding_conflict_count'],
        association_effect_on_scoring='none; class and coordinates determine matching',
        audit=audit(dataset), formal_acceptance=False, training_started=False,
        limitations=['8 correlated frames from one scene, not Ground48 or independent test',
            'Completeness human-confirmed, not machine-proven; raw sources and draft unchanged',
            'Official Car o12 in 010907 excluded by direct user instruction; metrics use exactly this label version',
            'False positives in unannotated areas are not automatically ignored'])
    write_json(output/'publication_receipt.json', receipt)
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('draft', 'package', 'checkpoint', 'output'):
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--human-approved', action='store_true')
    a = p.parse_args()
    result = publish(a.draft, a.package, a.checkpoint, a.output, a.human_approved)
    print(result['status'], result['labels'])
