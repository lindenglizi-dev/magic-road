#!/usr/bin/env python3
"""Per-target fixed-mask change ledger for the two DDR diagnostic configs."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference, components, digest, filter_short_runs
from ddr_detection_capacity_probe import (
    ANNOTATIONS, DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256, PROJECT,
    mean2x2, observe_rle, protected_hashes,
)
from local_paired_diagnostic import FRAME_IDS, PACKAGE, dump, iou, match, read_json, validate_annotations
from roi_dataset_tool import fpga_gray_bgr
from run_local_scene_pilot import guard_path

FIXED = PROJECT / 'evaluation/ddr_architecture/fixed_mask_2415171_20261001_v2'
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/target_change_20261001_v1'
CONFIGS = {
    'baseline256': {'stride': 5, 'current_min_run': 2, 'min_area': 16},
    'ddr640': {'stride': 2, 'current_min_run': 5, 'min_area': 100},
}
STAGES = ('before_area', 'area_all', 'top4', 'capacity_top4')


def j(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def source_box(candidate, stride):
    return [candidate.xmin * stride, candidate.ymin * stride,
            (candidate.xmax + 1) * stride - 1, (candidate.ymax + 1) * stride - 1]


def component_table(mask, stride, min_area):
    found = components(mask, 1, 1_000_000)
    table = []
    qualified_rank = 0
    for rank, candidate in enumerate(found, 1):
        qualified = candidate.area >= min_area
        if qualified:
            qualified_rank += 1
        table.append({
            'component_label': candidate.component_label,
            'pixel_area': candidate.area,
            'analysis_bbox': [candidate.xmin, candidate.ymin, candidate.xmax, candidate.ymax],
            'source_bbox': source_box(candidate, stride),
            'area_rank': rank,
            'qualified_rank': qualified_rank if qualified else None,
            'area_qualified': qualified,
            'is_top4': qualified and qualified_rank <= 4,
        })
    return table


def stage_pools(table, capacity_failed):
    qualified = [row for row in table if row['area_qualified']]
    return {
        'before_area': table,
        'area_all': qualified,
        'top4': qualified[:4],
        'capacity_top4': [] if capacity_failed else qualified[:4],
    }


def assignments(targets, pool):
    links = match(targets, [row['source_bbox'] for row in pool], .5)
    by_target = {targets[a]['track_id']: pool[b] for a, b in links.items()}
    by_component = {pool[b]['component_label']: targets[a]['track_id'] for a, b in links.items()}
    return by_target, by_component


def best_component(target, pool):
    if not pool:
        return None, 0.0
    scored = [(iou(target['box'], row['source_bbox']), row) for row in pool]
    value, row = max(scored, key=lambda item: (item[0], -item[1]['area_rank']))
    return row, value


def diagnostic(targets, mask, stride, min_area):
    table = component_table(mask, stride, min_area)
    linked, inverse = assignments(targets, table)
    return table, linked, inverse


def overlap_graph(current_mask, keep_mask, current, keep):
    _, current_labels = cv2.connectedComponents(current_mask, connectivity=8)
    _, keep_labels = cv2.connectedComponents(keep_mask, connectivity=8)
    current_by_id = {row['component_label']: row for row in current}
    keep_by_id = {row['component_label']: row for row in keep}
    nodes = []
    old_to_new = {}
    for new_id, new in keep_by_id.items():
        values, counts = np.unique(current_labels[keep_labels == new_id], return_counts=True)
        overlaps = [{'current_component_label': int(value), 'overlap_pixels': int(count)}
                    for value, count in zip(values, counts) if value]
        for edge in overlaps:
            old_to_new[edge['current_component_label']] = new_id
        old_area = sum(current_by_id[edge['current_component_label']]['pixel_area'] for edge in overlaps)
        if not overlaps:
            relation = 'new_from_restored_runs'
        elif len(overlaps) > 1:
            relation = 'merged_multiple_old_components'
        elif new['pixel_area'] > old_area:
            relation = 'extended_single_old_component'
        else:
            relation = 'unchanged'
        nodes.append({**new, 'relation_from_current': relation,
                      'current_components': overlaps,
                      'restored_run_pixels': new['pixel_area'] - sum(edge['overlap_pixels'] for edge in overlaps)})
    return {'current_components': current, 'keep_all_components': nodes}, old_to_new


def stage_row(frame_id, target, config, branch, minimum, min_area, stage,
              capacity_failed, pool, linked, inverse, raw_diag, clean_diag, run_diag):
    assigned = linked.get(target['track_id'])
    best, best_iou = best_component(target, pool)
    diag_values = {}
    last = None
    for name, diag in (('raw', raw_diag), ('clean', clean_diag), ('run', run_diag)):
        candidate, value = best_component(target, diag['table'])
        diag_values[f'{name}_best_iou'] = value
        diag_values[f'{name}_best_component_label'] = candidate['component_label'] if candidate else None
        diag_values[f'{name}_iou05_assigned'] = target['track_id'] in diag['linked']
        if target['track_id'] in diag['linked']:
            last = name
    return {
        'source_frame_id': frame_id,
        'target_id': target['track_id'],
        'observation_id': f"f{frame_id:06d}:{target['track_id']}",
        'label': target['label'],
        'target_source_bbox': j(target['box']),
        'config': config,
        'branch': branch,
        'min_run': minimum,
        'min_area': min_area,
        'stage': stage,
        'capacity_failed': capacity_failed,
        'matched': assigned is not None,
        'matched_object_id': target['track_id'] if assigned else '',
        'matched_component_label': assigned['component_label'] if assigned else None,
        'matched_component_pixel_area': assigned['pixel_area'] if assigned else None,
        'matched_component_analysis_bbox': j(assigned['analysis_bbox']) if assigned else '',
        'matched_component_source_bbox': j(assigned['source_bbox']) if assigned else '',
        'matched_component_iou': iou(target['box'], assigned['source_bbox']) if assigned else None,
        'matched_component_area_rank': assigned['area_rank'] if assigned else None,
        'matched_component_is_top4': assigned['is_top4'] if assigned else None,
        'best_component_label': best['component_label'] if best else None,
        'best_component_pixel_area': best['pixel_area'] if best else None,
        'best_component_source_bbox': j(best['source_bbox']) if best else '',
        'best_component_iou': best_iou,
        'best_component_area_rank': best['area_rank'] if best else None,
        'best_component_is_top4': best['is_top4'] if best else None,
        'best_component_matched_object_id': inverse.get(best['component_label'], '') if best else '',
        **diag_values,
        'last_raw_clean_run_iou05_assignment_stage': last or '',
    }


def transition_row(frame_id, target, config, stage, current, keep, graph, old_to_new):
    target_id = target['track_id']
    old = current['assignments'][stage][0].get(target_id)
    new = keep['assignments'][stage][0].get(target_id)
    status = ('gained' if old is None and new is not None else
              'lost' if old is not None and new is None else
              'stable_match' if old is not None else 'stable_miss')
    mapped_new_id = old_to_new.get(old['component_label']) if old else None
    relevant_new_id = new['component_label'] if new else mapped_new_id
    graph_by_id = {row['component_label']: row for row in graph['keep_all_components']}
    relation = graph_by_id.get(relevant_new_id, {}).get('relation_from_current', '')
    ancestors = graph_by_id.get(relevant_new_id, {}).get('current_components', [])
    ancestor_ids = [row['current_component_label'] for row in ancestors]
    current_labels = {row['component_label'] for row in current['pools'][stage]}
    keep_labels = {row['component_label'] for row in keep['pools'][stage]}
    old_member = bool(current_labels.intersection(ancestor_ids))
    new_member = relevant_new_id in keep_labels if relevant_new_id is not None else False
    rank_changed = old_member != new_member and stage in ('top4', 'capacity_top4')
    current_inverse = current['assignments'][stage][1]
    keep_inverse = keep['assignments'][stage][1]
    old_objects = {current_inverse[label] for label in ancestor_ids if label in current_inverse}
    new_object = keep_inverse.get(relevant_new_id)
    matching_changed = bool(old_member and new_member and old_objects != ({new_object} if new_object else set()))
    capacity_changed = (stage == 'capacity_top4' and
                        current['capacity_failed'] != keep['capacity_failed'])
    evidence = []
    if relation and relation != 'unchanged':
        evidence.append(relation)
    if rank_changed:
        evidence.append('ranking_reallocation')
    if matching_changed:
        evidence.append('matching_reallocation')
    if capacity_changed:
        evidence.append('capacity_gate_changed')
    if status in ('gained', 'lost') and not evidence:
        evidence.append('iou_geometry_or_assignment_change')
    return {
        'source_frame_id': frame_id,
        'target_id': target_id,
        'observation_id': f'f{frame_id:06d}:{target_id}',
        'label': target['label'],
        'config': config,
        'stage': stage,
        'change_current_to_keep_all': status,
        'current_component_label': old['component_label'] if old else None,
        'keep_all_component_label': new['component_label'] if new else None,
        'mapped_keep_all_component_label': mapped_new_id,
        'pixel_structural_relation': relation,
        'overlapping_current_component_labels': j(ancestor_ids),
        'ranking_membership_changed': rank_changed,
        'matching_assignment_changed': matching_changed,
        'capacity_gate_changed': capacity_changed,
        'evidence_tags': j(evidence),
    }


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def self_check():
    current = np.zeros((5, 9), np.uint8)
    current[2, 1:3] = current[2, 5:7] = 1
    keep = current.copy()
    keep[2, 3:5] = 1
    old = component_table(current, 1, 1)
    new = component_table(keep, 1, 1)
    graph, mapping = overlap_graph(current, keep, old, new)
    assert graph['keep_all_components'][0]['relation_from_current'] == 'merged_multiple_old_components'
    assert len(graph['keep_all_components'][0]['current_components']) == 2 and len(mapping) == 2
    extended = keep.copy()
    extended[1, 1] = 1
    graph, _ = overlap_graph(keep, extended, component_table(keep, 1, 1), component_table(extended, 1, 1))
    assert graph['keep_all_components'][0]['relation_from_current'] == 'extended_single_old_component'
    ranked = np.zeros((12, 24), np.uint8)
    for index, width in enumerate((8, 7, 6, 5, 4)):
        ranked[index * 2, :width] = 1
    table = component_table(ranked, 1, 1)
    assert [row['pixel_area'] for row in table[:4]] == [8, 7, 6, 5]
    gt = [{'track_id': 'a', 'box': [0, 0, 9, 9]}, {'track_id': 'b', 'box': [4, 0, 13, 9]}]
    before = match(gt, [[2, 0, 11, 9]], .5)
    after = match(gt, [[2, 0, 11, 9], [0, 0, 9, 9]], .5)
    assert before == {0: 0} and after == {0: 1, 1: 0}
    return {'status': 'PASS', 'checks': ['multi_component_merge', 'single_component_extension',
                                         'project_area_sort_top4', 'hungarian_reallocation']}


def run(output):
    for path in (output, FIXED, DEFAULT_VIDEO, ANNOTATIONS, PACKAGE):
        guard_path(path)
    if not output.resolve().is_relative_to((PROJECT / 'evaluation/ddr_architecture').resolve()) or output.exists():
        raise ValueError('Choose a new output inside evaluation/ddr_architecture')
    if digest(DEFAULT_VIDEO) != EXPECTED_VIDEO_SHA256:
        raise ValueError('Registered development video changed')

    fixed_receipt = read_json(FIXED / 'receipt.json')
    for name, expected in fixed_receipt['artifact_hashes'].items():
        if digest(FIXED / name) != expected:
            raise ValueError(f'Fixed-mask artifact changed: {name}')
    manifest = read_json(FIXED / 'mask_manifest.json')
    if manifest.get('stage') != 'after_cleanup_before_min_run' or len(manifest.get('frames', [])) != 1920:
        raise ValueError('Expected exactly 1920 saved clean masks')
    mask_lookup = {}
    mask_counts = Counter()
    for row in manifest['frames']:
        path = (FIXED / row['path']).resolve()
        if not path.is_relative_to(FIXED.resolve()) or digest(path) != row['sha256']:
            raise ValueError(f"Saved mask changed: {row['path']}")
        key = (row['config'], int(row['frame_id']))
        if key in mask_lookup:
            raise ValueError(f'Duplicate saved mask: {key}')
        mask_lookup[key] = path
        mask_counts[row['config']] += 1
    expected_keys = {(name, fid) for name in CONFIGS for fid in range(120, 1080)}
    if set(mask_lookup) != expected_keys or mask_counts != Counter({'baseline256': 960, 'ddr640': 960}):
        raise ValueError('Saved mask coverage is not config x frames120..1079')

    annotation = read_json(ANNOTATIONS)
    validate_annotations(annotation, read_json(PACKAGE / 'package.json'))
    confirmation_path = ANNOTATIONS.parent / 'confirmation_receipt.json'
    confirmation = read_json(confirmation_path)
    if (annotation.get('evaluation_scope') != 'moving_ped_vehicle_only' or
            digest(ANNOTATIONS) != confirmation['derived_sha256'] or
            digest(PROJECT / confirmation['original_path']) != confirmation['original_sha256']):
        raise ValueError('Annotation confirmation changed')
    truth = {row['frame_index']: [target for target in row['targets']
             if target['motion'] == 'moving' and target['label'] in ('ped', 'vehicle')]
             for row in annotation['frames']}
    if sum(map(len, truth.values())) != 57:
        raise ValueError('Expected 57 confirmed moving ped/vehicle observations')

    protected_before = protected_hashes()
    chains = {name: CandidateChainReference(sample_stride=cfg['stride'],
              min_run=cfg['current_min_run'], min_area=cfg['min_area'], top_k=1_000_000)
              for name, cfg in CONFIGS.items()}
    ledger, changes, graphs, states = [], [], [], {}
    replay_mask_checks = 0
    capture = cv2.VideoCapture(str(DEFAULT_VIDEO))
    if not capture.isOpened():
        raise ValueError('Cannot open registered development video')
    try:
        for frame_id in range(FRAME_IDS[-1] + 1):
            ok, image = capture.read()
            if not ok or image.shape != (720, 1280, 3):
                raise ValueError(f'Decode failure at frame {frame_id}')
            gray = fpga_gray_bgr(image)
            small = mean2x2(gray)
            for name, cfg in CONFIGS.items():
                result = chains[name].process_analysis(gray[::5, ::5] if cfg['stride'] == 5 else small,
                                                       frame_id)
                if frame_id >= 120:
                    saved = np.load(mask_lookup[(name, frame_id)], allow_pickle=False)
                    if not np.array_equal(result['clean_mask'], saved):
                        raise AssertionError(f'Clean-mask replay mismatch: {name} frame {frame_id}')
                    replay_mask_checks += 1
                if frame_id not in truth:
                    continue
                targets = truth[frame_id]
                raw_table, raw_linked, raw_inverse = diagnostic(targets, result['raw_mask'], cfg['stride'], cfg['min_area'])
                clean_table, clean_linked, clean_inverse = diagnostic(targets, result['clean_mask'], cfg['stride'], cfg['min_area'])
                branch_masks = {}
                for branch, minimum in (('current', cfg['current_min_run']), ('keep_all', 1)):
                    run_mask = filter_short_runs(result['clean_mask'], minimum)
                    if branch == 'current' and not np.array_equal(run_mask, result['run_filtered_mask']):
                        raise AssertionError('Project min-run helper differs from chain output')
                    profile = observe_rle(run_mask)
                    table, run_linked, run_inverse = diagnostic(targets, run_mask, cfg['stride'], cfg['min_area'])
                    pools = stage_pools(table, profile['capacity_failed'])
                    stage_assignments = {stage: assignments(targets, pool) for stage, pool in pools.items()}
                    state = {'table': table, 'pools': pools, 'assignments': stage_assignments,
                             'capacity_failed': profile['capacity_failed']}
                    states[(frame_id, name, branch)] = state
                    branch_masks[branch] = run_mask
                    raw_diag = {'table': raw_table, 'linked': raw_linked, 'inverse': raw_inverse}
                    clean_diag = {'table': clean_table, 'linked': clean_linked, 'inverse': clean_inverse}
                    run_diag = {'table': table, 'linked': run_linked, 'inverse': run_inverse}
                    for target in targets:
                        for stage in STAGES:
                            linked, inverse = stage_assignments[stage]
                            ledger.append(stage_row(frame_id, target, name, branch, minimum,
                                cfg['min_area'], stage, profile['capacity_failed'], pools[stage],
                                linked, inverse, raw_diag, clean_diag, run_diag))
                graph, old_to_new = overlap_graph(branch_masks['current'], branch_masks['keep_all'],
                    states[(frame_id, name, 'current')]['table'], states[(frame_id, name, 'keep_all')]['table'])
                graphs.append({'source_frame_id': frame_id, 'config': name, **graph})
                for target in targets:
                    for stage in STAGES:
                        changes.append(transition_row(frame_id, target, name, stage,
                            states[(frame_id, name, 'current')], states[(frame_id, name, 'keep_all')],
                            graph, old_to_new))
            if frame_id and frame_id % 120 == 0:
                print(f'processed through source frame {frame_id}', flush=True)
    finally:
        capture.release()

    if len(ledger) != 57 * 2 * 2 * 4 or len(changes) != 57 * 2 * 4:
        raise AssertionError('Ledger cardinality mismatch')
    summary = {}
    for config in CONFIGS:
        for stage in STAGES:
            selected = [row for row in changes if row['config'] == config and row['stage'] == stage]
            summary[f'{config}/{stage}'] = {
                'changes': dict(Counter(row['change_current_to_keep_all'] for row in selected)),
                'gained_target_observations': [row['observation_id'] for row in selected if row['change_current_to_keep_all'] == 'gained'],
                'lost_target_observations': [row['observation_id'] for row in selected if row['change_current_to_keep_all'] == 'lost'],
                'evidence_tags': dict(Counter(tag for row in selected for tag in json.loads(row['evidence_tags']))),
            }
    current_capacity_misses = [row for row in ledger if row['branch'] == 'current' and
                               row['stage'] == 'capacity_top4' and not row['matched']]
    miss_diagnostics = Counter(row['last_raw_clean_run_iou05_assignment_stage'] or 'none'
                               for row in current_capacity_misses)
    boundaries = [
        'Geometry proposal ledger only; no classifier or recognition-accuracy measurement.',
        'One development video, 32 confirmed frames, 57 moving ped/vehicle observations from four correlated tracks.',
        'Unmatched candidates and targets remain unknown/missed geometry observations, never automatic invalid labels.',
        'Pixel relations mean connected-component extension or merger only; they do not assert semantic target adhesion.',
        'Fixed min-run 2/5 versus1, fixed min-area16/100, project area ordering and Hungarian IoU>=0.5 matching; no sweep.',
        'Replay is causal from source frame0 through1050 with existing background/update/sampling settings.',
        'Capacity is the existing unlimited-reference demand proxy, not RTL overflow timing.',
        'No training, model/RTL/config modification, blind-reserve access, DDR/CDC/display or scheduler simulation.',
    ]
    report = {
        'status': 'target_change_geometry_diagnostic_not_acceptance',
        'target_observations': {'total': 57, 'ped': 46, 'vehicle': 11, 'tracks': ['p01', 'p02', 'v01', 'v02']},
        'ledger_rows': len(ledger),
        'change_rows': len(changes),
        'saved_clean_masks_verified': len(mask_lookup),
        'replayed_clean_masks_pixel_equal': replay_mask_checks,
        'replay_frame_range': [0, FRAME_IDS[-1]],
        'current_capacity_miss_last_iou05_stage': dict(miss_diagnostics),
        'summary': summary,
        'boundaries': boundaries,
        'self_check': self_check(),
    }
    output.mkdir(parents=True)
    write_csv(output / 'target_stage_ledger.csv', ledger)
    write_csv(output / 'target_change_ledger.csv', changes)
    dump(output / 'component_overlap_graph.json', {'relation_basis': 'exact run-mask pixel overlap', 'frames': graphs})
    dump(output / 'report.json', report)
    lines = ['# DDR 目标逐项变化账本', '',
             '仅报告候选几何与容量代理；以下“匹配”均为类别无关的一对一 IoU≥0.5 几何匹配。', '',
             '| 配置/阶段 | 新增 | 损失 | 持续匹配 | 持续漏检 |',
             '|---|---:|---:|---:|---:|']
    for key, value in summary.items():
        count = value['changes']
        lines.append(f"| {key} | {count.get('gained', 0)} | {count.get('lost', 0)} | "
                     f"{count.get('stable_match', 0)} | {count.get('stable_miss', 0)} |")
    lines += ['', '逐目标四阶段明细见 `target_stage_ledger.csv`；current→keep_all 新增/损失及像素证据见 '
              '`target_change_ledger.csv`；完整组件像素重叠图见 `component_overlap_graph.json`。', '',
              f"当前分支 capacity_top4 漏检的 raw/clean/run 最后 IoU≥0.5 匹配阶段：{dict(miss_diagnostics)}。", '',
              '证据边界：', ''] + ['- ' + text for text in boundaries]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    protected_after = protected_hashes()
    if protected_after != protected_before:
        raise AssertionError('Protected production sources/settings/documents changed')
    dependencies = [Path(__file__), PROJECT / 'tools/candidate_chain_reference.py',
                    PROJECT / 'tools/ddr_detection_capacity_probe.py',
                    PROJECT / 'tools/local_paired_diagnostic.py', PROJECT / 'tools/roi_dataset_tool.py']
    dump(output / 'receipt.json', {
        'command': [sys.executable, *sys.argv],
        'video_sha256': EXPECTED_VIDEO_SHA256,
        'annotation_sha256': digest(ANNOTATIONS),
        'confirmation_sha256': digest(confirmation_path),
        'fixed_mask_receipt_sha256': digest(FIXED / 'receipt.json'),
        'fixed_mask_manifest_sha256': digest(FIXED / 'mask_manifest.json'),
        'fixed_mask_artifact_hashes_verified': fixed_receipt['artifact_hashes'],
        'saved_mask_files_verified': len(mask_lookup),
        'replay_clean_mask_pixel_checks': replay_mask_checks,
        'source_hashes': {path.relative_to(PROJECT).as_posix(): digest(path) for path in dependencies},
        'protected_sources_before': protected_before,
        'protected_sources_after': protected_after,
        'protected_sources_unchanged': protected_before == protected_after,
        'runtime': {'python': sys.version, 'opencv': cv2.__version__, 'numpy': np.__version__},
        'artifact_hashes': {path.name: digest(path) for path in sorted(output.iterdir()) if path.is_file()},
    })
    return {'report': str(output / 'report.md'), 'ledger_rows': len(ledger),
            'change_rows': len(changes), 'clean_mask_checks': replay_mask_checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output), ensure_ascii=False, indent=2))

