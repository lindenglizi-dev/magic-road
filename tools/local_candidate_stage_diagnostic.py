#!/usr/bin/env python3
"""Bounded, moving-target-only stage coverage; no training or RTL claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference
from local_paired_diagnostic import (
    PROJECT, PACKAGE, FRAME_IDS, candidates, digest, dump, iou, match,
    read_json, validate_annotations,
)
from run_local_scene_pilot import DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256, guard_path

ANNOTATIONS = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930/annotations.confirmed.json'
OUTPUT = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_stage_diagnostic_v1'


def cell_box(box):
    x0, y0, x1, y1 = box
    return [5*x0, 5*y0, 5*(x1+1)-1, 5*(y1+1)-1]


def independent_components(mask):
    """Eight-connected DFS without OpenCV; exact pixel-set fingerprints."""
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    result = []
    for index in np.flatnonzero(mask):
        y, x = divmod(int(index), w)
        if seen[y, x]:
            continue
        seen[y, x] = True
        stack, pixels = [(y, x)], []
        while stack:
            cy, cx = stack.pop()
            pixels.append(cy*w+cx)
            for ny in range(max(0, cy-1), min(h, cy+2)):
                for nx in range(max(0, cx-1), min(w, cx+2)):
                    if mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        indices = np.array(sorted(pixels), dtype='<i4')
        yy, xx = indices // w, indices % w
        result.append((len(pixels), int(xx.min()), int(yy.min()),
                       int(xx.max()), int(yy.max()), int(xx.sum()), int(yy.sum()),
                       hashlib.sha256(indices.tobytes()).hexdigest()))
    return sorted(result)


def checked_components(mask):
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    signatures, rows = [], []
    for label in range(1, n):
        x, y, w, h, area = map(int, stats[label])
        indices = np.flatnonzero(labels.ravel() == label).astype('<i4')
        yy, xx = indices // mask.shape[1], indices % mask.shape[1]
        signature = (area, x, y, x+w-1, y+h-1, int(xx.sum()), int(yy.sum()),
                     hashlib.sha256(indices.tobytes()).hexdigest())
        signatures.append(signature)
        rows.append({'label': label, 'area': area, 'analysis_box': [x, y, x+w-1, y+h-1],
                     'source_box': cell_box([x, y, x+w-1, y+h-1]), 'pixel_set_sha256': signature[-1]})
    if sorted(signatures) != independent_components(mask):
        raise AssertionError('Independent CCL pixel membership / geometry mismatch')
    return sorted(rows, key=lambda r: (-r['area'], r['label']))


def summarize(rows, threshold):
    totals = {}
    for stage in rows[0]['stages']:
        stats = {label: {'targets': 0, 'matched': 0} for label in ('ped', 'vehicle')}
        unrestricted = capped = 0
        for frame in rows:
            result = frame['stages'][stage]['matching'][str(threshold)]
            for label in stats:
                stats[label]['targets'] += sum(t['label'] == label for t in frame['targets'])
                stats[label]['matched'] += result['matched_by_class'].get(label, 0)
            unrestricted += result['matched_total']
            capped += min(4, result['matched_total'])
        for entry in stats.values():
            entry['recall'] = entry['matched']/entry['targets'] if entry['targets'] else None
        totals[stage] = {'by_class': stats, 'matched_total': unrestricted,
                         'final_four_oracle_total': capped,
                         'note': 'Oracle only; per-class allocation is maximum-cardinality then maximum-IoU matching, not class-specific maximization.'}
    return totals


def run(annotation_path, output):
    for path in (annotation_path, output, PACKAGE, DEFAULT_VIDEO):
        guard_path(path)
    if output.exists():
        raise ValueError('Output must be new')
    annotation, package = read_json(annotation_path), read_json(PACKAGE/'package.json')
    validate_annotations(annotation, package)
    if annotation.get('evaluation_scope') != 'moving_ped_vehicle_only':
        raise ValueError('Explicit moving-only evaluation scope required')
    confirmation_path = annotation_path.parent/'confirmation_receipt.json'
    confirmation = read_json(confirmation_path)
    if confirmation['derived_sha256'] != digest(annotation_path):
        raise ValueError('Confirmation hash mismatch')
    if digest(PROJECT/confirmation['original_path']) != confirmation['original_sha256']:
        raise ValueError('Original annotation changed')
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError('Video changed')
    receipt = read_json(PACKAGE/'receipt.json')
    for name, expected in receipt['artifact_hashes'].items():
        path = (PACKAGE/name).resolve()
        if not path.is_relative_to(PACKAGE.resolve()) or digest(path) != expected:
            raise ValueError('Package hash mismatch')
    frozen, candidate_hash = candidates()
    ann_by_frame = {r['frame_index']: r for r in annotation['frames']}
    package_frames = {r['frame_index']: r for r in package['frames']}
    output.mkdir(parents=True)
    (output/'masks').mkdir()
    chain, frame_rows = CandidateChainReference(), []
    cap = cv2.VideoCapture(str(DEFAULT_VIDEO))
    try:
        for frame_index in range(max(FRAME_IDS)+1):
            ok, image = cap.read()
            if not ok or image.shape[:2] != (720, 1280):
                raise ValueError(f'Decode failure {frame_index}')
            result = chain.process_bgr(image, frame_index)
            if frame_index not in ann_by_frame:
                continue
            cached = cv2.imread(str(PACKAGE/package_frames[frame_index]['path']))
            if not np.array_equal(image, cached):
                raise AssertionError('Causal replay frame differs from reviewed package frame')
            targets = [t for t in ann_by_frame[frame_index]['targets']
                       if t['motion'] == 'moving' and t['label'] in ('ped', 'vehicle')]
            stage_pools = {}
            for key, mask_key in [('raw_all', 'raw_mask'), ('clean_all', 'clean_mask'), ('run_all', 'run_filtered_mask')]:
                stage_pools[key] = checked_components(result[mask_key])
                if not cv2.imwrite(str(output/'masks'/f'f{frame_index:06d}_{key}.png'), result[mask_key]*255):
                    raise OSError('Cannot save mask')
            stage_pools['area16_all'] = [r for r in stage_pools['run_all'] if r['area'] >= 16]
            for count in (4, 8, 16):
                stage_pools[f'top{count}'] = stage_pools['area16_all'][:count]
            actual = [(r['analysis_box'], r['area']) for r in stage_pools['top4']]
            cached_rows = [(json.loads(r['selected_analysis_box']), int(r['component_area'])) for r in frozen[frame_index]]
            if actual != cached_rows:
                raise AssertionError(f'Baseline replay mismatch frame {frame_index}')
            for a, b in zip(stage_pools['top4'], frozen[frame_index]):
                if a['source_box'] != json.loads(b['selected_source_box']):
                    raise AssertionError('Source cell mapping mismatch')
            stages = {}
            for key, pool in stage_pools.items():
                boxes = [r['source_box'] for r in pool]
                matches = {}
                for threshold in (.5, .25):
                    links = match(targets, boxes, threshold)
                    matches[str(threshold)] = {
                        'matched_total': len(links),
                        'matched_by_class': dict(Counter(targets[i]['label'] for i in links)),
                        'pairs': [{'track_id': targets[i]['track_id'], 'label': targets[i]['label'],
                                   'component_label': pool[j]['label'], 'iou': iou(targets[i]['box'], boxes[j])}
                                  for i, j in links.items()]}
                stages[key] = {'candidate_count': len(pool), 'components': pool, 'matching': matches,
                               'best_iou_per_target_not_one_to_one': [
                                   {'track_id': t['track_id'], 'best_iou': max((iou(t['box'], b) for b in boxes), default=0)}
                                   for t in targets]}
            run_mask = result['run_filtered_mask']
            starts = (run_mask != 0) & (np.pad(run_mask[:, :-1], ((0, 0), (1, 0))) == 0)
            run_counts = starts.sum(axis=1)
            frame_rows.append({'frame_index': frame_index, 'targets': targets, 'stages': stages,
                               'max_runs_per_row': int(run_counts.max()),
                               'rows_runs_gt64': int((run_counts > 64).sum()),
                               'foreground_pixels': {k: int(result[k].sum()) for k in ('raw_mask', 'clean_mask', 'run_filtered_mask')}})
    finally:
        cap.release()
    if len(frame_rows) != 32:
        raise AssertionError('Incomplete frame set')
    report = {'scope': 'moving_ped_vehicle_only', 'human_confirmed': True,
              'frames': len(frame_rows), 'target_observations': sum(len(f['targets']) for f in frame_rows),
              'unique_tracks': len({t['track_id'] for f in frame_rows for t in f['targets']}),
              'primary_iou05': summarize(frame_rows, .5), 'sensitivity_iou025': summarize(frame_rows, .25),
              'independent_ccl': {'method': 'OpenCV versus standalone 8-neighbor DFS, exact pixel sets, bbox, area, coordinate sums',
                                  'mask_comparisons': 96, 'mismatches': 0},
              'frozen_top4_replay_frames_verified': 32,
              'capacity_proxies': {'max_runs_per_row': max(f['max_runs_per_row'] for f in frame_rows),
                                   'rows_runs_gt64': sum(f['rows_runs_gt64'] for f in frame_rows),
                                   'max_components_after_run': max(f['stages']['run_all']['candidate_count'] for f in frame_rows)},
              'boundaries': ['Python reference only; no RTL capacity, active-label, overflow, CDC or cycle validation.',
                             'Oracle localization upper bounds, not achieved detector recall or classifier performance.',
                             'No background truth: unmatched candidates are NOT automatically invalid; FAR and precision unavailable.',
                             'Only 32 sampled frames and four correlated tracks; not cross-scene acceptance.',
                             'Stage changes are diagnostic associations, not proof of foreground semantic ownership.',
                             'No new windows, no changed candidate rules, no threshold tuning.']}
    dump(output/'frame_stages.json', frame_rows)
    dump(output/'report.json', report)
    dependencies = ['local_candidate_stage_diagnostic.py', 'candidate_chain_reference.py',
                    'local_paired_diagnostic.py', 'run_local_scene_pilot.py', 'roi_dataset_tool.py']
    dump(output/'receipt.json', {'annotation_sha256': digest(annotation_path),
         'confirmation_receipt_sha256': digest(confirmation_path), 'source_sha256': EXPECTED_VIDEO_SHA256,
         'frozen_candidate_sha256': candidate_hash, 'package_receipt_sha256': digest(PACKAGE/'receipt.json'),
         'script_sha256': {name: digest(PROJECT/'tools'/name) for name in dependencies},
         'runtime': {'opencv': cv2.__version__, 'numpy': np.__version__},
         'replay': 'frame0..1050 continuous, default CandidateChainReference; score only fixed32 reviewed frames',
         'artifact_hashes': {p.relative_to(output).as_posix(): digest(p) for p in sorted(output.rglob('*')) if p.is_file()}})
    return report


def self_check():
    masks = [np.zeros((4, 5), np.uint8), np.ones((4, 5), np.uint8), np.eye(5, dtype=np.uint8),
             np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]], np.uint8)]
    assert [len(checked_components(m)) for m in masks] == [0, 1, 1, 4]
    rng = np.random.default_rng(2309)
    for _ in range(30):
        checked_components((rng.random((13, 17)) < .25).astype(np.uint8))
    assert cell_box([0, 0, 255, 143]) == [0, 0, 1279, 719]
    assert len(match([{'box': [0, 0, 9, 9]}]*2, [[0, 0, 9, 9]])) == 1
    return {'self_check': 'PASS', 'independent_ccl_masks': 34}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--annotations', type=Path, default=ANNOTATIONS)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.annotations, args.output), indent=2))
