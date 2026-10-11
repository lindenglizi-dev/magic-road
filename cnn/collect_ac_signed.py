"""Archive the two user-reviewed A/C batches; never publish a ready training set."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import shutil

from PIL import Image

from .import_verified_review import _raw_path, _validate_patch
from .prepare_ac_correction import isolated
from .prepare_ground48 import ROOT, dataset_id, read_json, sha256_file, write_json, _parse_signed_time

OUT = ROOT / 'cnn/reports/ac_signed_progress_20261010_v1'
INPUTS = (
    (ROOT / 'cnn/reports/ac_correction_pilot8_20261009_v2',
     ROOT / 'cnn/reports/ac_patch_check_20261010_v3/review_patch_4e7300bec9a0_2026-10-10T01-58-35-215Z.json',
     '883c57e4f174399485ba29696562f0a791c8b0321e93660d4d22fa6bbc9a160e'),
    (ROOT / 'cnn/reports/ac_ai_drawn24_20261010_v1',
     ROOT / 'cnn/reports/person_local_screen_20261010_v2/review_patch_snapshot.json',
     'a730c086a89ae50fdce02602a5340f8a08fd31614ec371f2db93a4e4fb922f2c'),
)


def signed_sample(sample, review, raw_path):
    if not review or not review['complete']:
        return None
    _parse_signed_time(review.get('reviewed_at_utc'), sample['image_id'])
    return dict(image_id=sample['image_id'], split=sample['split'], scene=sample['scene'],
        family_id=sample['family_id'], camera_id=sample['camera_id'],
        width=sample['width'], height=sample['height'], raw_file_absolute=str(raw_path),
        source_sha256=sample['source_sha256'], source_url=sample.get('source_url'),
        labels=[deepcopy(a) for a in review['actions'] if a['action'] != 'D'],
        manual_review=deepcopy(review), human_signature_valid=True,
        training_eligible=False, eligibility_reason='partial pilot; source/count/main-dev gate not closed')


def collect():
    images, pending, protected, sources, all_samples = [], [], {}, [], []
    for ordinal, (directory, patch_path, expected_hash) in enumerate(INPUTS, 1):
        assert sha256_file(patch_path) == expected_hash
        manifest_path = directory / 'review_manifest_teacher.json'
        original_path = directory / 'manifest_original.json'
        manifest, original = read_json(manifest_path), read_json(original_path)
        assert dataset_id(manifest) == manifest['dataset_id'] == dataset_id(original) == original['dataset_id']
        assert len(manifest['samples']) == len(original['samples'])
        assert sha256_file(directory / 'annotation_policy_v1.md') == manifest['annotation_policy_sha256']
        for sample, frozen in zip(manifest['samples'], original['samples'], strict=True):
            for key in ('image_id', 'family_id', 'camera_id', 'scene', 'split', 'raw_file'):
                assert sample[key] == frozen[key], (sample['image_id'], key)
        for path, digest in read_json(directory / 'source_bindings.json').items():
            assert sha256_file(Path(path)) == digest, path
            protected[path] = digest
        _, reviews, _ = _validate_patch(patch_path, manifest,
                                       {s['image_id']: s for s in manifest['samples']})
        protected.update({str(p): sha256_file(p) for p in (patch_path, manifest_path, original_path,
                          directory / 'annotation_policy_v1.md', directory / 'source_bindings.json')})
        sources.append(dict(batch=ordinal, manifest=str(manifest_path), patch=str(patch_path),
                            patch_sha256=expected_hash, dataset_id=manifest['dataset_id']))
        for sample in manifest['samples']:
            raw = _raw_path(directory, sample['raw_file'], sample['image_id'])
            assert sha256_file(raw) == sample['source_sha256']
            with Image.open(raw) as image:
                assert image.size == (sample['width'], sample['height'])
            protected[str(raw)] = sample['source_sha256']
            all_samples.append(sample)
            row = signed_sample(sample, reviews.get(sample['image_id']), raw)
            if row is None:
                pending.append(dict(image_id=sample['image_id'], split=sample['split'],
                                    reason='unsigned draft excluded; no new review assignment'))
            else:
                row['batch'] = ordinal
                images.append(row)
    assert len(all_samples) == len({s['image_id'] for s in all_samples}) == 32
    isolated(all_samples)  # Conservative reservations, not proof of MIO physical camera identities.
    assert len({s['source_sha256'] for s in all_samples}) == 32
    assert len(images) == 30 and len(pending) == 2
    counts = {}
    for split in ('train', 'dev'):
        subset = [s for s in images if s['split'] == split]
        counts[split] = dict(images=len(subset), scenes=dict(Counter(s['scene'] for s in subset)),
            labels=dict(Counter(a['class'] for s in subset for a in s['labels'])),
            person_bearing_images=sum(any(a['class'] == 'person' for a in s['labels']) for s in subset))
    scope_path = ROOT / 'cnn/reports/ac_scope_fixed_20261010_v1/scope_decision.json'
    scope = read_json(scope_path)
    protected[str(scope_path)] = sha256_file(scope_path)
    gaps = {split: scope['current_round']['train' if split == 'train' else 'development']-counts[split]['images']
            for split in ('train', 'dev')}
    return dict(schema='cnn_ac_signed_partial_archive_v1', status='blocked_data_not_training_ready',
        sources=sources, images=images, pending=pending, counts=counts, minimum_pilot_gaps=gaps,
        human_workload=dict(assigned_distinct_images=32, signed=30, pending=2,
                            maximum_distinct_images=32, new_assignments=0),
        family_reservations_pass=True, physical_camera_mapping_fully_verified=False,
        dataset_frozen=False, G_ready=False, training_started=False, inference_run=False,
        steps={'1': 'candidate_views_delivered_source_gate_not_closed',
               '2': '30_signed_frames_archived_128_64_pilot_not_ready',
               '3': 'new_main_dev_E7_baseline_not_started', '4': 'G100_not_started'},
        MOT17_disposition='auxiliary candidate only; no adopted labels, no A/C replacement or new A/B experiment',
        protected_files=protected)


def check():
    assert signed_sample({}, {'complete': False}, Path('unused')) is None
    try:
        isolated([{'family_id': 'same', 'camera_id': 'a', 'split': 'train'},
                  {'family_id': 'same', 'camera_id': 'b', 'split': 'dev'}])
    except ValueError:
        pass
    else:
        raise AssertionError('Cross-split original family accepted')
    result = collect()
    assert result['counts']['train']['images'] == 25 and result['counts']['dev']['images'] == 5
    assert result['counts']['train']['labels'] == {'person': 11, 'vehicle': 111}
    assert result['counts']['dev']['labels'] == {'person': 14, 'vehicle': 63, 'ignore': 2}
    if (OUT / 'reviewed_partial_labels.json').exists():
        assert read_json(OUT / 'reviewed_partial_labels.json') == result
    print('PASS: signed-only labels, hashes/coordinates, family reservations, partial-not-ready state')
    return result


def build():
    if OUT.exists():
        raise FileExistsError('Preserve previous output; use check')
    result = check()
    OUT.mkdir(parents=True)
    for ordinal, (_, source, _) in enumerate(INPUTS, 1):
        shutil.copy2(source, OUT / f'batch{ordinal}_user_patch_snapshot.json')
    write_json(OUT / 'reviewed_partial_labels.json', result)
    receipt = dict(status=result['status'], counts=result['counts'],
                   minimum_pilot_gaps=result['minimum_pilot_gaps'], steps=result['steps'],
                   partial_labels_sha256=sha256_file(OUT / 'reviewed_partial_labels.json'),
                   dataset_frozen=False, G_ready=False, training_started=False, inference_run=False)
    write_json(OUT / 'progress_receipt.json', receipt)
    check()
    print('Archived 30 signed frames; no ready dataset, baseline inference or training:', OUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build', 'check'))
    {'build': build, 'check': check}[parser.parse_args().action]()
