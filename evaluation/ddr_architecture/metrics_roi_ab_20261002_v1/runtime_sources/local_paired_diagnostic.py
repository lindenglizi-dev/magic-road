#!/usr/bin/env python3
"""Bounded local full-frame annotation package and paired ROI diagnosis.

Uses only one explicitly allowed development video and its frozen candidates.
AI labels and incomplete annotation exports are never accepted as human truth.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from run_local_scene_pilot import (
    DEFAULT_VIDEO, DEFAULT_OUTPUT, EXPECTED_VIDEO_SHA256, MODEL_DIR,
    guard_path, load_models, make_hog324, quantization_contract, score_roi,
)
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi

PROJECT = Path(__file__).resolve().parents[1]
PACKAGE = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_target32_v2'
FRAME_IDS = list(range(120, 1080, 30))
CONTRACT = 'local2415171_target32_source_inclusive_v1'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def candidates():
    path = DEFAULT_OUTPUT / 'candidates.csv'
    receipt = read_json(DEFAULT_OUTPUT / 'receipt.json')
    if digest(path) != receipt['artifact_hashes']['candidates.csv']:
        raise ValueError('Frozen candidate CSV changed')
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    selected = {f: [] for f in FRAME_IDS}
    for row in rows:
        f = int(row['frame_index'])
        if f in selected:
            selected[f].append(row)
    if any(len(v) > 4 for v in selected.values()):
        raise ValueError('Candidate budget exceeded')
    return selected, digest(path)


def build(output):
    guard_path(output)
    if output.exists():
        raise ValueError('Use a new output directory; existing packages are immutable')
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError('Video hash changed')
    table, candidate_hash = candidates()
    output.mkdir(parents=True)
    (output / 'frames').mkdir()
    capture = cv2.VideoCapture(str(DEFAULT_VIDEO))
    frames = []
    try:
        for f in range(FRAME_IDS[-1] + 1):
            ok, frame = capture.read()
            if not ok or frame.shape[:2] != (720, 1280):
                raise ValueError(f'Decode failure at frame {f}')
            if f not in table:
                continue
            path = output / 'frames' / f'f{f:06d}.png'
            if not cv2.imwrite(str(path), frame):
                raise OSError(path)
            frames.append({'frame_index': f, 'path': path.relative_to(output).as_posix(),
                           'sha256': digest(path), 'completed': False, 'targets': [],
                           'candidate_boxes': [json.loads(r['selected_source_box']) for r in table[f]]})
    finally:
        capture.release()
    package = {'contract_id': CONTRACT, 'source_sha256': EXPECTED_VIDEO_SHA256,
               'candidate_sha256': candidate_hash, 'source_size': [1280, 720],
               'review_basis': 'human_full_frame_review', 'reviewer': '',
               'reviewed_at': '', 'frames': frames,
               'truth_status': 'pending_human_annotation',
               'sampling': 'f120..1050 every30 source frames, irrespective of candidates or scores',
               'source_to_analysis': 'inclusive floor(x/5), floor(y/5), explicit five-pixel cell mapping',
               'primary_matching': 'class-blind maximum-cardinality one-to-one source IoU >= 0.5',
               'metrics': 'moving-only and all visible separately; unknown motion excluded only from moving stratum'}
    dump(output / 'package.json', package)
    template = Path(__file__).with_name('local_paired_annotation.html').read_text(encoding='utf-8')
    (output / 'annotate.html').write_text(template.replace('__PACKAGE_JSON__', json.dumps(package, ensure_ascii=False)), encoding='utf-8')
    canvas = np.full((4 * 205, 8 * 320, 3), 245, dtype=np.uint8)
    for index, row in enumerate(frames):
        frame = cv2.imread(str(output / row['path']))
        thumb = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
        y, x = divmod(index, 8)
        canvas[y*205:y*205+180, x*320:x*320+320] = thumb
        cv2.putText(canvas, f"frame {row['frame_index']}", (x*320+8, y*205+199),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1)
    if not cv2.imwrite(str(output / 'contact32.jpg'), canvas):
        raise OSError('Cannot write contact sheet')
    dump(output / 'receipt.json', {'schema': 'paired_package_receipt_v1',
         'source_sha256': EXPECTED_VIDEO_SHA256, 'candidate_sha256': candidate_hash,
         'script_sha256': digest(__file__),
         'artifact_hashes': {p.relative_to(output).as_posix(): digest(p)
                             for p in sorted(output.rglob('*')) if p.is_file()}})
    return {'package': str(output), 'frames': len(frames), 'truth_status': 'pending_human_annotation'}


def iou(a, b):
    overlap = max(0, min(a[2], b[2]) - max(a[0], b[0]) + 1) * max(0, min(a[3], b[3]) - max(a[1], b[1]) + 1)
    aa = (a[2]-a[0]+1)*(a[3]-a[1]+1)
    bb = (b[2]-b[0]+1)*(b[3]-b[1]+1)
    return overlap / (aa + bb - overlap)


def match(gt, boxes, threshold=.5):
    # Maximum cardinality then maximum total IoU; no labels or model scores.
    from scipy.optimize import linear_sum_assignment
    if not gt or not boxes:
        return {}
    n, m = len(gt), len(boxes)
    costs = np.zeros((n + m, n + m))
    costs[:n, :m] = 1.0
    for a, g in enumerate(gt):
        for b, box in enumerate(boxes):
            value = iou(g['box'], box)
            if value >= threshold:
                costs[a, b] = -(min(n, m) + 1 + value)
    rr, cc = linear_sum_assignment(costs)
    return {int(a): int(b) for a, b in zip(rr, cc) if a < n and b < m and costs[a, b] < 0}


def validate_annotations(annotation, package):
    if annotation.get('contract_id') != CONTRACT or annotation.get('source_sha256') != EXPECTED_VIDEO_SHA256:
        raise ValueError('Annotation contract or video mismatch')
    if annotation.get('review_basis') != 'human_full_frame_review' or not annotation.get('reviewer', '').strip():
        raise ValueError('Human reviewer confirmation is required; AI prelabels are not truth')
    import datetime
    datetime.date.fromisoformat(annotation.get('reviewed_at', ''))
    if annotation.get('human_confirmed') is not True:
        raise ValueError('Explicit human confirmation required')
    rows = annotation.get('frames', [])
    if [r.get('frame_index') for r in rows] != FRAME_IDS:
        raise ValueError('Missing, duplicated or reordered fixed frames')
    for row in rows:
        if row.get('completed') is not True:
            raise ValueError(f"Frame {row['frame_index']} not marked complete")
        ids = set()
        for target in row.get('targets', []):
            box = target.get('box', [])
            if len(box) != 4 or any(type(v) is not int for v in box):
                raise ValueError('Box requires four integer source coordinates')
            if not (0 <= box[0] <= box[2] < 1280 and 0 <= box[1] <= box[3] < 720):
                raise ValueError('Box out of source bounds')
            if target.get('label') not in {'ped', 'vehicle', 'ignore'}:
                raise ValueError('Unknown target class')
            if target.get('motion') not in {'moving', 'stationary', 'uncertain'}:
                raise ValueError('Motion must be explicit')
            if target.get('visibility') not in {'full', 'occluded', 'frame_truncated'}:
                raise ValueError('Visibility must be explicit')
            if not target.get('track_id', '').strip() or target['track_id'] in ids:
                raise ValueError('Unique per-frame track ID required')
            if target.get('label') == 'ignore' and not target.get('subtype', '').strip():
                raise ValueError('Ignored target needs subtype, e.g. rider_bicycle')
            ids.add(target['track_id'])
    if package['candidate_sha256'] != candidates()[1]:
        raise ValueError('Candidate source changed')


def evaluate(annotation_path, package_dir, output):
    for path in (annotation_path, package_dir, output):
        guard_path(path)
    if output.exists():
        raise ValueError('Evaluation output must be new')
    package = read_json(package_dir / 'package.json')
    receipt = read_json(package_dir / 'receipt.json')
    for name, expected in receipt['artifact_hashes'].items():
        path = (package_dir / name).resolve()
        if not path.is_relative_to(package_dir.resolve()) or digest(path) != expected:
            raise ValueError(f'Package artifact mismatch: {name}')
    annotations = read_json(annotation_path)
    validate_annotations(annotations, package)
    table, _ = candidates()
    parameters, _, model_receipt = load_models(MODEL_DIR)
    hog, quant = make_hog324(), quantization_contract(parameters['opencv_hog324'])
    output.mkdir(parents=True)
    pairs = []
    frame_rows = []
    for ann, frame_row in zip(annotations['frames'], package['frames']):
        f = ann['frame_index']
        gray = fpga_analysis_frame(cv2.imread(str(package_dir / frame_row['path'])))
        active = [t for t in ann['targets'] if t['label'] != 'ignore']
        ignored = [t for t in ann['targets'] if t['label'] == 'ignore']
        ccl = table[f]
        boxes = [json.loads(r['selected_source_box']) for r in ccl]
        links = match(active, boxes)
        # Verify cached candidate ROI and predictions directly from lossless frames.
        for candidate in ccl:
            x0, y0, x1, y1 = json.loads(candidate['selected_analysis_box'])
            roi = fpga_resize_roi(gray[y0:y1+1, x0:x1+1])
            if hashlib.sha256(roi.tobytes()).hexdigest() != candidate['roi_pixel_sha256']:
                raise ValueError('Stored candidate pixel identity mismatch')
            score = score_roi(roi, parameters, hog, quant)
            if any(str(score[k]) != candidate[k] for k in ('hog64_prediction', 'hog324_q_prediction', 'hog324_q_score_integer')):
                raise ValueError('Stored candidate model score mismatch')
        for index, target in enumerate(active):
            x0, y0, x1, y1 = [v // 5 for v in target['box']]
            roi = fpga_resize_roi(gray[y0:y1+1, x0:x1+1])
            score = score_roi(roi, parameters, hog, quant)
            candidate = ccl[links[index]] if index in links else None
            pairs.append({'frame_index': f, **target, 'analysis_box': [x0,y0,x1,y1],
                          'gt_roi_score': score, 'candidate_id': candidate['candidate_id'] if candidate else None,
                          'candidate_iou': iou(target['box'], boxes[links[index]]) if candidate else None,
                          'candidate_score': {k: candidate[k] for k in ('hog64_prediction','hog324_q_prediction')} if candidate else None,
                          'gt_roi_sha256': hashlib.sha256(roi.tobytes()).hexdigest()})
        unmatched = [b for b in range(len(boxes)) if b not in links.values()]
        ignored_overlap = [b for b in unmatched if any(iou(boxes[b], t['box']) >= .5 for t in ignored)]
        frame_rows.append({'frame_index': f, 'gt_count': len(active), 'ignored_count': len(ignored),
                           'candidate_count': len(ccl), 'matched_count': len(links),
                           'unmatched_candidates': len(unmatched), 'ignored_overlap_unmatched': len(ignored_overlap),
                           'sensitivity_matches_iou025': len(match(active, boxes, .25))})
    metrics = {}
    for stratum in ('all_visible', 'moving_only'):
        rows = [r for r in pairs if stratum == 'all_visible' or r['motion'] == 'moving']
        metrics[stratum] = {}
        for label in ('ped', 'vehicle'):
            subset = [r for r in rows if r['label'] == label]
            matched = [r for r in subset if r['candidate_score'] is not None]
            metrics[stratum][label] = {'targets': len(subset), 'unique_tracks': len({r['track_id'] for r in subset}),
                'covered': len(matched), 'coverage': len(matched)/len(subset) if subset else None,
                'models': {key: {'gt_correct_all': sum(r['gt_roi_score'][key] == label for r in subset),
                                'gt_correct_matched': sum(r['gt_roi_score'][key] == label for r in matched),
                                'ccl_correct_matched': sum(r['candidate_score'][key] == label for r in matched),
                                'end_to_end_recall': sum(r['candidate_score'][key] == label for r in matched)/len(subset) if subset else None}
                           for key in ('hog64_prediction', 'hog324_q_prediction')}}
    dump(output / 'pairs.json', pairs)
    dump(output / 'report.json', {'metrics': metrics, 'frames': frame_rows,
         'annotation_sha256': digest(annotation_path), 'package_receipt_sha256': digest(package_dir / 'receipt.json'),
         'models': model_receipt, 'script_sha256': digest(__file__),
         'boundary': '32 sampled frames only; GT box diagnostic not deployed detection; unmatched boxes are not automatically invalid labels; repeated tracks correlated; no RTL performance claim'})
    return {'output': str(output), 'paired_targets': len(pairs), 'metrics': metrics}


def self_test():
    assert iou([0,0,9,9], [0,0,9,9]) == 1
    assert iou([0,0,9,9], [10,0,19,9]) == 0
    gt = [{'box':[0,0,9,9]}, {'box':[0,0,9,9]}]
    assert len(match(gt, [[0,0,9,9]])) == 1
    assert len(match(gt, [[0,0,9,9], [0,0,9,9]])) == 2
    assert not match(gt, [[100,100,110,110]])
    for bad in ({}, {'contract_id': CONTRACT, 'source_sha256': EXPECTED_VIDEO_SHA256,
                      'review_basis':'ai_visual_prelabel', 'reviewer':'agent'}):
        try:
            validate_annotations(bad, {})
        except ValueError:
            pass
        else:
            raise AssertionError('Unconfirmed truth accepted')
    return {'self_test': 'PASS', 'frames': len(FRAME_IDS)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['build','evaluate','self-test'])
    parser.add_argument('--package', type=Path, default=PACKAGE)
    parser.add_argument('--annotations', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.mode == 'build':
        result = build(args.output or args.package)
    elif args.mode == 'evaluate':
        if args.annotations is None or args.output is None:
            parser.error('evaluate requires --annotations and --output')
        result = evaluate(args.annotations, args.package, args.output)
    else:
        result = self_test()
    print(json.dumps(result, ensure_ascii=False, indent=2))
