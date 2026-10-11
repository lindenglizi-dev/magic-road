#!/usr/bin/env python3
"""Bounded DDR detection capacity diagnostic; no RTL or classifier changes.

Replay the registered development video causally, with native frame cadence.
The unbounded RLE observer measures storage demand, not actual overflow timing.
Background rollback is a capacity-only counterfactual, not a DDR simulation.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference, digest
from local_paired_diagnostic import (
    FRAME_IDS, PACKAGE, PROJECT, candidates, dump, match, read_json,
    validate_annotations,
)
from roi_dataset_tool import fpga_gray_bgr
from run_local_scene_pilot import (
    DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256, guard_path,
)

ANNOTATIONS = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930/annotations.confirmed.json'
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/capacity_2415171_20261001_v1'
VARIANTS = (
    ('baseline256', 5, 2, 16, False),
    ('ddr640_capacity_observer', 2, 5, 100, False),
    ('ddr640_rollback_on_capacity_failure', 2, 5, 100, True),
)


def mean2x2(gray):
    if gray.dtype != np.uint8 or gray.ndim != 2 or any(n % 2 for n in gray.shape):
        raise ValueError('2x2 mean requires even-sized uint8 grayscale')
    values = gray.astype(np.uint16)
    return ((values[::2, ::2] + values[::2, 1::2] +
             values[1::2, ::2] + values[1::2, 1::2]) >> 2).astype(np.uint8)


def observe_rle(mask, capture_pixels=False):
    """Mirror label selection/union ordering with unlimited storage.

    A label is allocated only for a run touching no previous-row run. Union
    follows the smallest root, without compression or label reuse. Raw labels
    in the previous row are deduplicated before the ascending bitmap scan.
    Counts after a capacity breach describe demand, not actual RTL execution.
    """
    if mask.ndim != 2 or not mask.size or not np.all((mask == 0) | (mask == 1)):
        raise ValueError('RLE input must be a nonempty binary 2D mask')
    parents, previous, run_counts = [0], [], []
    comparisons = label_scan_runs = unions = links = max_walk = 0
    first_run_excess = first_label_excess = None
    pixels = np.zeros(mask.shape, np.int32) if capture_pixels else None

    def root(label):
        nonlocal max_walk
        steps = 1
        while parents[label] != label:
            label = parents[label]
            steps += 1
        max_walk = max(max_walk, steps)
        return label

    for y, row in enumerate(mask):
        transitions = np.diff(np.pad(row.astype(np.int8), (1, 1)))
        starts = np.flatnonzero(transitions == 1)
        ends = np.flatnonzero(transitions == -1) - 1
        run_counts.append(len(starts))
        if len(starts) > 64 and first_run_excess is None:
            first_run_excess = y
        comparisons += len(starts) * len(previous)
        label_scan_runs += len(starts)
        current = []
        # ponytail: scan all previous runs like current RTL; not a fast CCL engine.
        for start, end in zip(starts.tolist(), ends.tolist()):
            matched = sorted({label for a, b, label in previous
                              if start <= b + 1 and a <= end + 1})
            if not matched:
                label = len(parents)
                parents.append(label)
                if label > 32 and first_label_excess is None:
                    first_label_excess = y
            else:
                label = matched[0]
                for other in matched[1:]:
                    unions += 1
                    a, b = root(label), root(other)
                    if a != b:
                        parents[max(a, b)] = min(a, b)
                        links += 1
                    label = min(a, b)
            current.append((start, end, label))
            if pixels is not None:
                pixels[y, start:end + 1] = label
        previous = current
    roots = {root(label) for label in range(1, len(parents))}
    result = {
        'max_runs_per_row': max(run_counts),
        'runs_total': sum(run_counts),
        'rows_runs_gt64': sum(n > 64 for n in run_counts),
        'labels_allocated': len(parents) - 1,
        'components_after_run': len(roots),
        'union_requests': unions,
        'union_links': links,
        'max_parent_nodes_observed': max_walk,
        'previous_run_comparisons': comparisons,
        'label_scan_runs': label_scan_runs,
        'first_run_excess_y': first_run_excess,
        'first_label_excess_y': first_label_excess,
        'capacity_failed': first_run_excess is not None or first_label_excess is not None,
    }
    if pixels is not None:
        lookup = np.array([0] + [root(i) for i in range(1, len(parents))])
        resolved = lookup[pixels]
        result['pixel_sets'] = sorted(tuple(np.flatnonzero(resolved.ravel() == r)) for r in roots)
    return result


def self_check():
    assert mean2x2(np.full((2, 2), 253, np.uint8)).item() == 253
    assert mean2x2(np.array([[1, 2], [3, 5]], np.uint8)).item() == 2
    try:
        mean2x2(np.zeros((3, 2), np.uint8))
    except ValueError:
        pass
    else:
        raise AssertionError('Odd shape was accepted')
    comb = np.zeros((2, 264), np.uint8)
    for x in range(0, 264, 8):
        comb[0, x:x + 5] = 1
    comb[1] = 1
    profile = observe_rle(comb)
    assert profile['max_runs_per_row'] == 33 and profile['labels_allocated'] == 33
    assert profile['components_after_run'] == 1 and profile['union_requests'] == 32
    assert profile['capacity_failed'] and profile['first_label_excess_y'] == 0
    assert profile['rows_runs_gt64'] == 0
    assert profile['label_scan_runs'] == 34
    dense = np.tile(np.array([1] * 5 + [0] * 3, np.uint8), (2, 80))
    assert observe_rle(dense)['max_runs_per_row'] == 80
    aliases = np.zeros((3, 9), np.uint8)
    aliases[0, 0] = aliases[0, 4:] = 1
    aliases[1, :5] = aliases[1, 7:] = 1
    aliases[2] = 1
    profile = observe_rle(aliases)
    assert profile['union_requests'] == 2 and profile['union_links'] == 1
    rng = np.random.default_rng(1300)
    masks = [np.zeros((4, 5), np.uint8), np.ones((4, 5), np.uint8),
             np.eye(5, dtype=np.uint8), comb, dense, aliases]
    masks += [(rng.random((9, 13)) < .35).astype(np.uint8) for _ in range(60)]
    for mask in masks:
        n, labels = cv2.connectedComponents(mask, connectivity=8)
        expected = sorted(tuple(np.flatnonzero(labels.ravel() == i)) for i in range(1, n))
        profile = observe_rle(mask, capture_pixels=True)
        assert profile['components_after_run'] == n - 1
        assert profile['pixel_sets'] == expected
    return {'self_check': 'PASS', 'independent_component_checks': len(masks)}


def protected_hashes():
    files = [PROJECT / name for name in (
        'CURRENT_ARCHITECTURE.md', 'REAL_DATA_WORKFLOW.md',
        'DDR_ROAD_VISION_ARCHITECTURE_PLAN.md',
        'evaluation/status.json', 'evaluation/criteria.pending.json')]
    files += sorted((PROJECT / 'user_source').rglob('*.v'))
    return {p.relative_to(PROJECT).as_posix(): digest(p) for p in files}


def run(output):
    for path in (output, DEFAULT_VIDEO, ANNOTATIONS, PACKAGE):
        guard_path(path)
    if not output.resolve().is_relative_to((PROJECT / 'evaluation/ddr_architecture').resolve()):
        raise ValueError('Output must stay inside evaluation/ddr_architecture')
    if output.exists():
        raise ValueError('Use a new output directory; previous results are immutable')
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError('Development video hash changed')
    annotations = read_json(ANNOTATIONS)
    validate_annotations(annotations, read_json(PACKAGE / 'package.json'))
    confirmation_path = ANNOTATIONS.parent / 'confirmation_receipt.json'
    confirmation = read_json(confirmation_path)
    if (annotations.get('evaluation_scope') != 'moving_ped_vehicle_only' or
            digest(ANNOTATIONS) != confirmation['derived_sha256'] or
            digest(PROJECT / confirmation['original_path']) != confirmation['original_sha256']):
        raise ValueError('Human confirmation provenance mismatch')
    frozen, frozen_hash = candidates()
    reference = read_json(PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_stage_diagnostic_v1/report.json')
    protected = protected_hashes()
    truth = {r['frame_index']: [t for t in r['targets'] if t['motion'] == 'moving'
                              and t['label'] in ('ped', 'vehicle')] for r in annotations['frames']}
    totals = {label: sum(t['label'] == label for ts in truth.values() for t in ts)
              for label in ('ped', 'vehicle')}
    output.mkdir(parents=True)
    variants = {name: {'chain': CandidateChainReference(sample_stride=stride, min_run=min_run,
                min_area=min_area, top_k=1000000), 'stride': stride, 'rollback': rollback,
                'matches': {stage: Counter() for stage in ('area_all', 'top4', 'capacity_gated_top4')}}
                for name, stride, min_run, min_area, rollback in VARIANTS}
    rows, reviewed, capture = [], [], cv2.VideoCapture(str(DEFAULT_VIDEO))
    if not capture.isOpened():
        raise ValueError('Cannot open registered development video')
    metadata = {key: capture.get(prop) for key, prop in (
        ('fps', cv2.CAP_PROP_FPS), ('frames', cv2.CAP_PROP_FRAME_COUNT),
        ('width', cv2.CAP_PROP_FRAME_WIDTH), ('height', cv2.CAP_PROP_FRAME_HEIGHT))}
    try:
        for frame_index in range(1080):
            ok, image = capture.read()
            if not ok or image.shape != (720, 1280, 3):
                raise ValueError(f'Decode failed at source frame {frame_index}')
            gray = fpga_gray_bgr(image)
            small = mean2x2(gray)
            for name, variant in variants.items():
                chain = variant['chain']
                result = chain.process_analysis(gray[::5, ::5] if variant['stride'] == 5 else small,
                                                frame_index)
                profile = observe_rle(result['run_filtered_mask'])
                if variant['rollback'] and not result['learning'] and profile['capacity_failed']:
                    chain.background = result['background'].copy()
                if frame_index < 120:
                    continue
                found = result['candidates']
                row = {'variant': name, 'frame_index': frame_index, **profile,
                       'area_qualified_components': len(found),
                       'foreground_pixels': result['foreground_pixels_after_min_run']}
                rows.append(row)
                if frame_index not in truth:
                    continue
                if name == 'baseline256':
                    actual = [([c[k] for k in ('xmin', 'ymin', 'xmax', 'ymax')], c['area']) for c in found[:4]]
                    expected = [(json.loads(c['selected_analysis_box']), int(c['component_area']))
                                for c in frozen[frame_index]]
                    if actual != expected:
                        raise AssertionError(f'Frozen baseline mismatch at frame {frame_index}')
                stride = variant['stride']
                boxes = [[c['xmin']*stride, c['ymin']*stride,
                          (c['xmax']+1)*stride-1, (c['ymax']+1)*stride-1] for c in found]
                pools = {'area_all': boxes, 'top4': boxes[:4],
                         'capacity_gated_top4': [] if profile['capacity_failed'] else boxes[:4]}
                matches = {}
                for stage, pool in pools.items():
                    pairs = match(truth[frame_index], pool, .5)
                    by_class = Counter(truth[frame_index][i]['label'] for i in pairs)
                    variant['matches'][stage].update(by_class)
                    matches[stage] = dict(by_class)
                reviewed.append({'variant': name, 'frame_index': frame_index,
                                 'capacity_failed': profile['capacity_failed'],
                                 'targets': truth[frame_index], 'matched_by_class': matches,
                                 'source_boxes_top4': boxes[:4]})
            if frame_index % 120 == 119:
                print(f'processed {frame_index + 1}/1080 source frames', flush=True)
    finally:
        capture.release()
    summary = {}
    for name, variant in variants.items():
        selected = [r for r in rows if r['variant'] == name]
        streak = longest = 0
        for row in selected:
            streak = streak + 1 if row['capacity_failed'] else 0
            longest = max(longest, streak)
        peaks = {key: max(r[key] for r in selected) for key in (
            'max_runs_per_row', 'labels_allocated', 'components_after_run', 'union_requests',
            'max_parent_nodes_observed', 'previous_run_comparisons', 'label_scan_runs')}
        summary[name] = {'frames': len(selected), 'peaks': peaks,
            'capacity_failed_frames': sum(r['capacity_failed'] for r in selected),
            'run_failed_frames': sum(r['rows_runs_gt64'] > 0 for r in selected),
            'label_failed_frames': sum(r['labels_allocated'] > 32 for r in selected),
            'longest_failure_streak_frames': longest,
            'proposal_recall_iou05': {stage: {label: {'matched': counts[label], 'targets': totals[label],
                    'recall': counts[label]/totals[label] if totals[label] else None}
                    for label in totals} for stage, counts in variant['matches'].items()}}
    for label in totals:
        expected = reference['primary_iou05']['top4']['by_class'][label]['matched']
        if summary['baseline256']['proposal_recall_iou05']['top4'][label]['matched'] != expected:
            raise AssertionError('Historical baseline matching changed')
    if protected_hashes() != protected:
        raise AssertionError('Protected production sources, settings or documents changed')
    boundaries = [
        'One registered development video; 960 workload frames and 32 reviewed frames, four correlated tracks.',
        'Native video cadence, causal updates from frame zero; not the final 15/20 Hz hardware scheduler.',
        'Unlimited storage observer; failure is a capacity-demand proxy, not RTL overflow/cycle equivalence.',
        'Counts include tiny components before area filtering; merged labels are not recycled.',
        'Rollback variant models capacity-only background cancellation; no DDR, CDC, display or recovery simulation.',
        'Class-blind proposal recall only; no classifier, FAR, precision or final recognition accuracy claim.',
        'No parameter sweep, training, blind-reserve access, production RTL or model modification.',
    ]
    report = {'status': 'diagnostic_only_not_acceptance', 'source': str(DEFAULT_VIDEO),
              'source_metadata': metadata, 'workload_window': [120, 1079],
              'reviewed_frame_ids': FRAME_IDS, 'target_observations': totals,
              'variants': summary, 'boundaries': boundaries, 'self_check': self_check()}
    with (output / 'frame_capacity.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    dump(output / 'reviewed_frames.json', reviewed)
    dump(output / 'report.json', report)
    lines = ['# DDR 检测容量首轮诊断', '',
             '仅软件诊断。固定开发视频从第 0 帧因果回放，统计第 120～1079 帧；不代表硬件时序或识别验收。', '',
             '| 配置 | 行 run 峰值 | 累计标签峰值 | 容量失败帧/960 | 最长连续失败帧 |',
             '|---|---:|---:|---:|---:|']
    for name, data in summary.items():
        p = data['peaks']
        lines.append(f"| {name} | {p['max_runs_per_row']} | {p['labels_allocated']} | "
                     f"{data['capacity_failed_frames']} | {data['longest_failure_streak_frames']} |")
    lines += ['', '32 张人工确认帧的候选召回，IoU≥0.5，一对一、类别无关匹配；尚未经过分类器。', '',
              '| 配置 | 全部面积合格候选：行人/机动车 | top4：行人/机动车 | 容量失败计漏检后的 top4：行人/机动车 |',
              '|---|---|---|---|']
    for name, data in summary.items():
        columns = []
        for stage in ('area_all', 'top4', 'capacity_gated_top4'):
            values = data['proposal_recall_iou05'][stage]
            columns.append(' / '.join(f"{values[label]['matched']}/{values[label]['targets']}" for label in totals))
        lines.append('| ' + name + ' | ' + ' | '.join(columns) + ' |')
    lines += ['', '背景回滚配置只模拟容量失败时撤销背景更新；没有自动重建背景，也不能作为正式部署方案。', '',
              '证据边界：', ''] + ['- ' + text for text in boundaries]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    dependencies = [Path(__file__), PROJECT / 'tools/candidate_chain_reference.py',
                    PROJECT / 'tools/roi_dataset_tool.py', PROJECT / 'tools/local_paired_diagnostic.py',
                    PROJECT / 'tools/run_local_scene_pilot.py']
    dump(output / 'receipt.json', {
        'command': [sys.executable, *sys.argv], 'video_sha256': EXPECTED_VIDEO_SHA256,
        'annotation_sha256': digest(ANNOTATIONS), 'confirmation_sha256': digest(confirmation_path),
        'frozen_candidate_sha256': frozen_hash,
        'runtime': {'python': sys.version, 'opencv': cv2.__version__, 'numpy': np.__version__},
        'source_hashes': {p.relative_to(PROJECT).as_posix(): digest(p) for p in dependencies},
        'protected_sources_unchanged': protected,
        'artifact_hashes': {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
    })
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = self_check() if args.self_check else run(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
