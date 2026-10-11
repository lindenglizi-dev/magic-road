#!/usr/bin/env python3
"""Project adapter for the user-supplied fixed-mask audit; diagnostic only.

Preserves native-cadence background history and project matching/top4 rules.
Only current min-run versus min-run=1 is compared, with fixed area thresholds.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference, components, digest
from ddr_detection_capacity_probe import (
    ANNOTATIONS, DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256, PROJECT,
    mean2x2, observe_rle, protected_hashes,
)
from local_paired_diagnostic import FRAME_IDS, PACKAGE, candidates, dump, iou, match, read_json, validate_annotations
from roi_dataset_tool import fpga_gray_bgr
from run_local_scene_pilot import guard_path

VENDOR = PROJECT / 'external_reference_exploration/ddr_candidate_audit_20261001'
OUTPUT = PROJECT / 'evaluation/ddr_architecture/fixed_mask_2415171_20261001_v1'
PRIOR = PROJECT / 'evaluation/ddr_architecture/capacity_2415171_20261001_v1'
CONFIGS = (('baseline256', 5, 2, 16), ('ddr640', 2, 5, 100))


def load_audit():
    receipt = read_json(VENDOR / 'IMPORT_RECEIPT.json')
    for row in receipt['Files']:
        path = (VENDOR / row['Name']).resolve()
        if not path.is_relative_to(VENDOR.resolve()) or digest(path).upper() != row['SHA256']:
            raise ValueError('Imported audit reference changed')
    spec = importlib.util.spec_from_file_location('ddr_mask_audit_reference', VENDOR / 'ddr_mask_audit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_box(candidate, stride):
    return [candidate.xmin * stride, candidate.ymin * stride,
            (candidate.xmax + 1) * stride - 1, (candidate.ymax + 1) * stride - 1]


def project_partition_check(filtered, audit):
    profile = observe_rle(filtered, capture_pixels=True)
    independent, demand = audit.rle_partition(filtered)
    reconstructed = np.zeros(filtered.size, np.int32)
    for label, indices in enumerate(profile.pop('pixel_sets'), 1):
        reconstructed[np.asarray(indices, np.intp)] = label
    if not np.array_equal(reconstructed.reshape(filtered.shape), audit.canonical(independent)):
        raise AssertionError('Project Python RLE and independent RLE partitions differ')
    if profile['labels_allocated'] != demand['reference_labels_allocated']:
        raise AssertionError('Allocation demand differs between references')
    return profile


def self_check():
    audit = load_audit()
    image = np.random.default_rng(1301).integers(0, 256, (8, 10, 3), dtype=np.uint8)
    expected = np.array([[(int(r) >> 2) + (int(g) >> 1) + (int(b) >> 2)
                         for b, g, r in row] for row in image], np.uint8)
    assert np.array_equal(fpga_gray_bgr(image), expected)
    averaged = np.array([[sum(int(expected[y + dy, x + dx]) for dy in (0, 1) for dx in (0, 1)) // 4
                         for x in range(0, 10, 2)] for y in range(0, 8, 2)], np.uint8)
    assert np.array_equal(mean2x2(expected), averaged)
    assert mean2x2(fpga_gray_bgr(np.full((2, 2, 3), 255, np.uint8))).item() == 253
    for stride in (2, 5):
        target = [7, 9, 37, 48]
        mask_target = [target[0]/stride, target[1]/stride, (target[2]+1)/stride, (target[3]+1)/stride]
        candidate = [4, 5, 18, 24]
        source = [candidate[0]*stride, candidate[1]*stride, candidate[2]*stride-1, candidate[3]*stride-1]
        assert abs(iou(target, source) - audit.iou(mask_target, candidate)) < 1e-12
    masks = [np.zeros((6, 9), np.uint8), np.ones((6, 9), np.uint8), np.eye(9, dtype=np.uint8)]
    rng = np.random.default_rng(20261001)
    masks += [(rng.random((9, 13)) < .35).astype(np.uint8) for _ in range(20)]
    for mask in masks:
        project_partition_check(mask, audit)
    return {'status': 'PASS', 'project_independent_partition_checks': len(masks),
            'gray_mean_and_coordinate_checks': 'PASS'}


def run(output):
    for path in (output, DEFAULT_VIDEO, ANNOTATIONS, PACKAGE):
        guard_path(path)
    if not output.resolve().is_relative_to((PROJECT / 'evaluation/ddr_architecture').resolve()) or output.exists():
        raise ValueError('Choose a new output inside evaluation/ddr_architecture')
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError('Registered development video changed')
    audit = load_audit()
    annotation = read_json(ANNOTATIONS)
    validate_annotations(annotation, read_json(PACKAGE / 'package.json'))
    confirmation_path = ANNOTATIONS.parent / 'confirmation_receipt.json'
    confirmation = read_json(confirmation_path)
    if (annotation.get('evaluation_scope') != 'moving_ped_vehicle_only' or
            digest(ANNOTATIONS) != confirmation['derived_sha256'] or
            digest(PROJECT / confirmation['original_path']) != confirmation['original_sha256']):
        raise ValueError('Annotation confirmation changed')
    frozen, frozen_hash = candidates()
    prior_report = read_json(PRIOR / 'report.json')
    prior_receipt = read_json(PRIOR / 'receipt.json')
    for name, expected in prior_receipt['artifact_hashes'].items():
        if digest(PRIOR / name) != expected:
            raise ValueError('Previous result artifact changed')
    truth = {r['frame_index']: [t for t in r['targets'] if t['motion'] == 'moving'
                              and t['label'] in ('ped', 'vehicle')] for r in annotation['frames']}
    totals = {label: sum(t['label'] == label for ts in truth.values() for t in ts) for label in ('ped', 'vehicle')}
    protected = protected_hashes()
    output.mkdir(parents=True)
    for name, *_ in CONFIGS:
        (output / 'masks' / name).mkdir(parents=True)
    variants = {name: {'chain': CandidateChainReference(sample_stride=stride, min_run=minimum,
                                     min_area=area, top_k=1000000),
                       'stride': stride, 'minimum': minimum, 'area': area}
                for name, stride, minimum, area in CONFIGS}
    rows, reviewed, masks = [], [], []
    partition_checks = 0
    counters = {f'{name}/{branch}': {stage: Counter() for stage in ('before_area', 'area_all', 'top4', 'capacity_top4')}
                for name in variants for branch in ('current', 'keep_all')}
    cap = cv2.VideoCapture(str(DEFAULT_VIDEO))
    if not cap.isOpened():
        raise ValueError('Cannot open video')
    try:
        for fid in range(1080):
            ok, image = cap.read()
            if not ok or image.shape != (720, 1280, 3):
                raise ValueError(f'Decode failure at frame {fid}')
            gray = fpga_gray_bgr(image)
            small = mean2x2(gray)
            for name, config in variants.items():
                result = config['chain'].process_analysis(gray[::5, ::5] if config['stride'] == 5 else small, fid)
                if fid < 120:
                    continue
                clean = result['clean_mask']
                path = output / 'masks' / name / f'frame_{fid:06d}.npy'
                np.save(path, clean, allow_pickle=False)
                masks.append({'config': name, 'frame_id': fid, 'path': path.relative_to(output).as_posix(),
                              'sha256': digest(path), 'stage': 'after_cleanup_before_min_run',
                              'background_before_update_sha256': hashlib.sha256(result['background'].tobytes()).hexdigest()})
                background = config['chain'].background.copy()
                for branch, minimum in (('current', config['minimum']), ('keep_all', 1)):
                    data = audit.audit_mask(clean, minimum, config['area'], 4, 32, 64, None)
                    filtered, _, _ = audit.keep_runs(clean, minimum)
                    if branch == 'current' and not np.array_equal(filtered, result['run_filtered_mask']):
                        raise AssertionError('Imported and project min-run filters differ')
                    qualified = components(filtered, config['area'], 1000000)
                    expected_geometry = sorted((c.area, c.xmin, c.ymin, c.xmax+1, c.ymax+1) for c in qualified)
                    actual_geometry = sorted((c['area'], *c['bbox_xyxy']) for c in data['area_qualified_candidates'])
                    if expected_geometry != actual_geometry:
                        raise AssertionError('Imported and project component geometry differ')
                    row = {'config': name, 'branch': branch, 'frame_id': fid, 'minimum_run': minimum,
                           **{key: data[key] for key in (
                               'foreground_pixels_before_run_filter', 'foreground_pixels_after_run_filter',
                               'row_run_peak_after_filter', 'total_runs_after_filter',
                               'reference_labels_allocated', 'reference_union_operations',
                               'reference_component_count', 'area_qualified_candidate_count',
                               'capacity_proxy_failure', 'reference_rle_opencv_partition_equal')}}
                    rows.append(row)
                    if fid not in truth:
                        continue
                    project_partition_check(filtered, audit)
                    partition_checks += 1
                    if name == 'baseline256' and branch == 'current':
                        actual = [([c.xmin, c.ymin, c.xmax, c.ymax], c.area) for c in qualified[:4]]
                        expected = [(json.loads(c['selected_analysis_box']), int(c['component_area'])) for c in frozen[fid]]
                        if actual != expected:
                            raise AssertionError('Frozen top4 baseline changed')
                    stride = config['stride']
                    all_boxes = [[x*stride, y*stride, right*stride-1, bottom*stride-1]
                                 for x, y, right, bottom in (c['bbox_xyxy'] for c in data['components_before_area_filter'])]
                    boxes = [source_box(c, stride) for c in qualified]
                    pools = {'before_area': all_boxes, 'area_all': boxes, 'top4': boxes[:4],
                             'capacity_top4': [] if data['capacity_proxy_failure'] else boxes[:4]}
                    matches, target_ids = {}, {}
                    for stage, pool in pools.items():
                        pairs = match(truth[fid], pool, .5)
                        counts = Counter(truth[fid][i]['label'] for i in pairs)
                        counters[f'{name}/{branch}'][stage].update(counts)
                        matches[stage] = dict(counts)
                        target_ids[stage] = [truth[fid][i]['track_id'] for i in sorted(pairs)]
                        half_open_boxes = [[a, b, c+1, d+1] for a, b, c, d in pool]
                        objects = [{'id': t['track_id'], 'class': t['label'],
                                    'bbox_xyxy': [t['box'][0], t['box'][1], t['box'][2]+1, t['box'][3]+1]} for t in truth[fid]]
                        if audit.match_report(half_open_boxes, objects)['matched'] != len(pairs):
                            raise AssertionError('Independent maximum-cardinality match differs')
                    reviewed.append({'config': name, 'branch': branch, 'frame_id': fid,
                                     'matches_by_class': matches, 'matched_target_ids': target_ids,
                                     'source_boxes_top4': boxes[:4],
                                     'unmatched_top4_unknown': len(boxes[:4])-sum(matches['top4'].values()),
                                     'capacity_failed': data['capacity_proxy_failure']})
                if not np.array_equal(background, config['chain'].background):
                    raise AssertionError('Fixed-mask branches mutated background state')
            if fid % 120 == 119:
                print(f'processed {fid+1}/1080 source frames', flush=True)
    finally:
        cap.release()
    summary = {}
    for name in variants:
        for branch in ('current', 'keep_all'):
            key = f'{name}/{branch}'
            selected = [r for r in rows if r['config'] == name and r['branch'] == branch]
            demand = [r['reference_labels_allocated'] for r in selected]
            summary[key] = {'frames': len(selected),
                'row_run_peak': max(r['row_run_peak_after_filter'] for r in selected),
                'labels': {q: int(np.percentile(demand, p, method='higher')) for q, p in (('p50',50), ('p95',95), ('max',100))},
                'capacity_failed_frames': sum(r['capacity_proxy_failure'] for r in selected),
                'proposal_matches': {stage: {label: {'matched': counts[label], 'targets': totals[label]}
                                             for label in totals} for stage, counts in counters[key].items()}}
            if branch == 'current':
                prior_name = 'baseline256' if name == 'baseline256' else 'ddr640_capacity_observer'
                previous = prior_report['variants'][prior_name]
                if (summary[key]['labels']['max'] != previous['peaks']['labels_allocated'] or
                        summary[key]['capacity_failed_frames'] != previous['capacity_failed_frames']):
                    raise AssertionError('Current branch does not reproduce prior capacity report')
                for label in totals:
                    if counters[key]['top4'][label] != previous['proposal_recall_iou05']['top4'][label]['matched']:
                        raise AssertionError('Current branch does not reproduce prior matching')
    paired = {}
    for name in variants:
        pairs = {fid: [r for r in reviewed if r['config'] == name and r['frame_id'] == fid] for fid in FRAME_IDS}
        paired[name] = {stage: {'gained': sum(len(set(b['matched_target_ids'][stage])-set(a['matched_target_ids'][stage]))
                                            for a,b in pairs.values()),
                                'lost': sum(len(set(a['matched_target_ids'][stage])-set(b['matched_target_ids'][stage]))
                                            for a,b in pairs.values())} for stage in ('before_area','area_all','top4')}
    if protected_hashes() != protected:
        raise AssertionError('Protected production sources/settings/documents changed during trial')
    boundaries = [
        'One development video, native cadence, replay from frame0; stats120..1079. Not 960 independent samples.',
        '32 confirmed frames, 46 ped and 11 vehicle observations from four correlated tracks; moving-only scope.',
        'Fixed clean masks compare current min-run versus1; area/top4/background history remain fixed.',
        'Unmatched candidates are UNKNOWN, not invalid. New candidate semantics, FAR/precision and classification are unavailable.',
        'Independent RLE union_links differ from project union_requests; top4/matching use project rules.',
        '3840 external RLE/OpenCV partition checks and128 project Python RLE partition checks do NOT prove production RTL partitions.',
        'Capacity is unlimited-reference demand, not RTL overflow timing. No deployment capacity is selected from this video.',
        'No DDR/CDC/display/scheduler, no rollback/recovery experiment, no classifier training and no blind-reserve access.',
    ]
    report = {'status':'fixed_mask_diagnostic_not_deployment', 'settings':{
        'source_sha256':EXPECTED_VIDEO_SHA256, 'gray':'(R>>2)+(G>>1)+(B>>2)',
        'sampling':{'baseline256':'stride5 point sampling','ddr640':'uint16 four-gray sum >>2'},
        'background':'learn4; toward shift2 learning, shift4 update with minstep1; freeze raw foreground',
        'threshold':'abs difference >=20','cleanup':'zero-padded3x3 sum>=3; center must be1',
        'min_run':{'baseline256':2,'ddr640':5,'single_factor_control':1},
        'min_area':{'baseline256':16,'ddr640':100},'top4':'area desc then OpenCV component label',
        'foreground_label_ids':'1..32 inclusive;0 reserved; frame clear resets allocation; union does not recycle',
        'run_capacity':64, 'matching':'project maximum-cardinality then maximum-total-IoU; source inclusive IoU>=0.5'},
        'summary':summary,'paired_observations':paired,'target_denominators':totals,
        'external_partition_checks':len(rows),'project_python_partition_checks':partition_checks,
        'invalid_false_accept_rate':None,'boundaries':boundaries,'self_check':self_check()}
    with (output/'frame_audit.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    dump(output/'reviewed_frames.json',reviewed)
    dump(output/'mask_manifest.json',{'stage':'after_cleanup_before_min_run','frames':masks})
    dump(output/'report.json',report)
    lines=['# DDR 固定 Mask 单因素审计','',
           '当前 min-run 与保留全部 run；背景历史、面积门槛及项目 Top4/匹配规则保持不变。','',
           '| 配置/分支 | 行 run 峰值 | 标签 p50 / p95 / max | 容量超限帧/960 | Top4 行人/机动车匹配 |',
           '|---|---:|---|---:|---|']
    for key,data in summary.items():
        values=data['proposal_matches']['top4']
        matched=' / '.join(f"{values[label]['matched']}/{values[label]['targets']}" for label in totals)
        labels=' / '.join(str(data['labels'][q]) for q in ('p50','p95','max'))
        lines.append(f"| {key} | {data['row_run_peak']} | {labels} | {data['capacity_failed_frames']} | {matched} |")
    lines+=['','全量去噪后、min-run前 Mask 已保存，帧号对应原视频。容量与几何不是分类准确率；未匹配候选不能标为 invalid。',
            '', '项目 Python observer 的分区检查不是生产 RTL 分区证明；RTL 分区仍列为接入前门禁。','', '证据边界：','']
    lines+=['- '+text for text in boundaries]
    (output/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    dependencies=[Path(__file__), VENDOR/'ddr_mask_audit.py',PROJECT/'tools/ddr_detection_capacity_probe.py',
                  PROJECT/'tools/candidate_chain_reference.py',PROJECT/'tools/local_paired_diagnostic.py',
                  PROJECT/'tools/roi_dataset_tool.py']
    dump(output/'receipt.json',{'command':[sys.executable,*sys.argv],
        'import_receipt_sha256':digest(VENDOR/'IMPORT_RECEIPT.json'),
        'annotation_sha256':digest(ANNOTATIONS),'confirmation_sha256':digest(confirmation_path),
        'frozen_candidate_sha256':frozen_hash,'prior_receipt_sha256':digest(PRIOR/'receipt.json'),
        'source_hashes':{p.relative_to(PROJECT).as_posix():digest(p) for p in dependencies},
        'protected_sources_unchanged':protected,
        'runtime':{'python':sys.version,'opencv':cv2.__version__,'numpy':np.__version__},
        'artifact_hashes':{p.name:digest(p) for p in sorted(output.iterdir()) if p.is_file()}})
    return {'summary':summary,'partition_checks':[len(rows),partition_checks],'report':str(output/'report.md')}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check',action='store_true')
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),ensure_ascii=False,indent=2))
