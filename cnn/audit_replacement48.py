"""Read-only Ground48 inventory; never exports GT, changes splits, or trains."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil

import cv2

from .import_verified_review import _validate_patch
from .prepare_ground48 import ROOT, OUTPUT, read_json, sha256_file, validate_ground_manifest, write_json


def effective_boxes(sample, review):
    actions = {item['target_id']: item for item in review.get('actions', [])}
    originals = {item['target_id'] for item in sample['original']}
    boxes = [actions.get(item['target_id'], item) for item in sample['original']]
    boxes += [item for key, item in actions.items() if key not in originals]
    return [item for item in boxes if item.get('action') != 'D']


def recommendation(complete, count):
    # These are proposals, not automatic replacement or a new human signature.
    if count >= 20:
        return 'REPLACE_CANDIDATE_DENSITY'
    return 'KEEP_CANDIDATE_SIGNED' if complete else 'UNRESOLVED_COMPLETENESS'


def audit(patch_path: Path, output: Path, source_probe: Path):
    if output.exists():
        raise FileExistsError(f'preserve existing report: {output}')
    manifest, samples = validate_ground_manifest(OUTPUT / 'review_manifest_teacher.json')
    probe = read_json(source_probe)
    if probe['stage'] not in {'BLOCKED_ACCESS', 'SOURCE_READY'}:
        raise ValueError('unrecognized source probe stage')
    patch, reviews, _ = _validate_patch(patch_path, manifest, samples)
    for review in reviews.values():
        if review['complete']:
            stamp = datetime.fromisoformat(review.get('reviewed_at_utc', '').replace('Z', '+00:00'))
            if stamp.tzinfo is None:
                raise ValueError('signed review timestamp needs timezone')
    protected = [OUTPUT / name for name in ('index.html', 'manifest_original.json',
                 'review_manifest_teacher.json', 'annotation_policy_v1.md')]
    protected += [ROOT / name for name in ('cnn/model.py', 'cnn/contract.json',
                   'cnn/template/design_top_wrapper.v', 'cnn/data/post_review_s_20261007_v1/dataset_train_val.json')]
    protected.append(patch_path)
    baseline = {str(path): sha256_file(path) for path in protected}
    rows = []
    for sample in samples.values():
        path = OUTPUT / sample['raw_file']
        rgb = cv2.imread(str(path))
        if rgb is None or rgb.shape[:2] != (sample['height'], sample['width']):
            raise ValueError(f'raw dimensions mismatch: {path}')
        baseline[str(path)] = sha256_file(path)
        review = reviews.get(sample['image_id'], {})
        boxes = effective_boxes(sample, review)
        counts = Counter(item['class'] for item in boxes)
        targets = counts['person'] + counts['vehicle']
        rows.append(dict(image_id=sample['image_id'], original_role=sample['bucket'],
            original_split=sample['split'], camera_id=sample['camera_id'],
            clip_id=sample['selection_clip_id'], frame_index=sample['frame_index'],
            raw_file=str(path), width=sample['width'], height=sample['height'],
            source_sha256=baseline[str(path)],
            pixel_sha256_rgb=hashlib.sha256(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB).tobytes()).hexdigest(),
            original_boxes=len(sample['original']), draft_person=counts['person'],
            draft_vehicle=counts['vehicle'], draft_ignore=counts['ignore'],
            human_complete=review.get('complete', False), reviewer=review.get('reviewer', ''),
            reviewed_at_utc=review.get('reviewed_at_utc', ''),
            draft_actions=len(review.get('actions', [])),
            recommendation=recommendation(review.get('complete', False), targets),
            source_label_status='official_original_or_human_derived_draft',
            original_label_reference=str(OUTPUT / 'manifest_original.json')))
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(patch_path, output / patch_path.name)
    with (output / 'old48_inventory.csv').open('x', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    unchanged = {path: sha256_file(Path(path)) == digest for path, digest in baseline.items()}
    write_json(output / 'protected_files_check.json', dict(baseline_sha256=baseline,
              unchanged=unchanged, all_unchanged=all(unchanged.values())))
    status = dict(stage=probe['stage'], created_at_utc=datetime.now(timezone.utc).isoformat(),
        dataset_id=manifest['dataset_id'], existing_count_observed=len(rows),
        cameras=dict(Counter(row['camera_id'] for row in rows)),
        patch_sha256=sha256_file(patch_path), human_complete_count=sum(row['human_complete'] for row in rows),
        recommendations=dict(Counter(row['recommendation'] for row in rows)),
        retained_verified=None, replacement_target=None, pilot_count=0,
        official_candidate_files_downloaded=probe['paired_candidate_count'], production_dataset_switch='NOT_AUTHORIZED',
        training='NOT_RUN', rtl_changes=False, all_protected_files_unchanged=all(unchanged.values()),
        source_probe=str(source_probe), source_probe_sha256=sha256_file(source_probe),
        blockers=probe['blockers'],
        limitations=['Signed counts are from the supplied exported patch; not a new visual certification.',
            'Unsigned action counts are draft counts, not confirmed total objects.',
            'KEEP_CANDIDATE is a recommendation only; no GT export or production selection changed.'])
    write_json(output / 'execution_status.json', status)
    return status


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--patch', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-probe', type=Path, required=True)
    args = parser.parse_args()
    print(audit(args.patch, args.output, args.source_probe))
