"""E01: reuse confirmed development frames/candidates; change only ROI source."""
import argparse
import csv
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from ddr_detection_capacity_probe import protected_hashes
from local_fourgrid_diagnostic import validated_package, validate_confirmation_chain
from local_paired_diagnostic import (PROJECT, PACKAGE, FRAME_IDS, candidates, digest,
                                     dump, match, read_json, validate_annotations)
from roi_dataset_tool import fpga_gray_bgr, fpga_resize_roi
from run_local_scene_pilot import (DEFAULT_OUTPUT, DEFAULT_VIDEO, EXPECTED_VIDEO_SHA256,
                                  MODEL_DIR, guard_path, load_models, make_hog324,
                                  quantization_contract, score_roi, write_csv)

ANNOTATIONS = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_confirmed_20260930/annotations.confirmed.json'
FOURGRID = PROJECT / 'evaluation/local_scene_pilots/intersection_2415171_fourgrid_v2'
CAPACITY = PROJECT / 'evaluation/ddr_architecture/capacity_2415171_20261001_v1'
SCORES = ('hog324_feature_sha256', 'hog324_float_score', 'hog324_float_prediction',
          'hog324_q_score_integer', 'hog324_q_score_normalized', 'hog324_q_prediction')
CLASSES = ('ped', 'vehicle')


def pixels(image):
    return hashlib.sha256(np.ascontiguousarray(image).tobytes()).hexdigest()


def joint_match(targets, boxes, predictions):
    """Reuse project cardinality/IoU matcher with class-correct eligible edges."""
    result = {}
    for label in CLASSES:
        ti = [i for i, t in enumerate(targets) if t['label'] == label]
        ci = [i for i, pred in enumerate(predictions) if pred == label]
        links = match([targets[i] for i in ti], [boxes[i] for i in ci])
        result.update({ti[a]: ci[b] for a, b in links.items()})
    return result


def summarize(rows, view):
    result = {}
    for label in CLASSES:
        selected = [r for r in rows if r['class'] == label and r['view'] == view]
        counts = Counter((r['A_correct'], r['B_correct']) for r in selected)
        n = len(selected)
        a = sum(r['A_correct'] for r in selected)
        b = sum(r['B_correct'] for r in selected)
        g = sum(r['geometric_match'] for r in selected)
        result[label] = {'N': n, 'geometry_A': g, 'geometry_B': g,
                         'geometry_recall': g/n if n else None,
                         'A_correct': a, 'B_correct': b,
                         'A_joint_recall': a/n if n else None,
                         'B_joint_recall': b/n if n else None,
                         'new_correct': counts[False, True],
                         'lost_correct': counts[True, False],
                         'both_correct': counts[True, True],
                         'neither_correct': counts[False, False],
                         'net_change': b-a, 'A_remaining': n-a, 'B_remaining': n-b,
                         'fixed_pair_A_correct': sum(r['fixed_A_correct'] for r in selected),
                         'fixed_pair_B_correct': sum(r['fixed_B_correct'] for r in selected),
                         'fixed_pair_denominator': g}
        assert sum(counts.values()) == n
        assert counts[False, True]-counts[True, False] == b-a
    return result


def decision(metrics):
    deltas = [metrics[k]['net_change'] for k in CLASSES]
    if any(x > 0 for x in deltas) and any(x < 0 for x in deltas):
        return 'mixed', '混合结果'
    if any(x < 0 for x in deltas):
        return 'degraded', '退化'
    if any(x > 0 for x in deltas):
        return 'positive_development_only', '本开发样本上的正向结果'
    return 'no_observed_gain', '未观察到收益'


def self_check():
    assert fpga_gray_bgr(np.full((1, 1, 3), 255, np.uint8)).item() == 253
    for h, w in ((1, 1), (3, 7), (24, 55), (720, 1280)):
        data = np.arange(h*w, dtype=np.int64).reshape(h, w)
        expected = np.array([[data[min((h*(4+8*v)) >> 8, h-1),
                                    min((w*(4+8*u)) >> 8, w-1)]
                              for u in range(32)] for v in range(32)])
        assert np.array_equal(fpga_resize_roi(data), expected)
    targets = [{'label': 'ped', 'box': [0, 0, 9, 9]},
               {'label': 'vehicle', 'box': [0, 0, 9, 9]}]
    boxes = [[0, 0, 9, 9], [0, 0, 9, 9]]
    assert len(match(targets, boxes)) == 2
    assert len(joint_match(targets, boxes, ['vehicle', 'ped'])) == 2
    assert len(joint_match(targets, boxes, [None, None])) == 0
    assert len(joint_match(targets, boxes[:1], ['ped'])) == 1
    return {'integer_sampling': 'PASS', 'white_gray_253': 'PASS',
            'one_to_one_class_correct_assignment': 'PASS'}


def run(output):
    output = output.resolve()
    allowed = (PROJECT/'evaluation/ddr_architecture').resolve()
    if not output.is_relative_to(allowed) or output.exists():
        raise ValueError('use a fresh isolated directory within evaluation/ddr_architecture')
    for path in (output, DEFAULT_VIDEO, ANNOTATIONS, PACKAGE, FOURGRID, CAPACITY, MODEL_DIR):
        guard_path(path)
    start = time.perf_counter()
    before = protected_hashes()
    checks = self_check()
    inputs = {}

    def bind(path):
        inputs[path.relative_to(PROJECT).as_posix()] = digest(path)

    def artifact(directory, name):
        receipt = read_json(directory/'receipt.json')
        path = directory/name
        assert digest(path) == receipt['artifact_hashes'][name], path
        bind(directory/'receipt.json'); bind(path)
        return path

    assert digest(DEFAULT_VIDEO) == EXPECTED_VIDEO_SHA256
    bind(DEFAULT_VIDEO)
    package, _ = validated_package(PACKAGE)
    annotation = read_json(ANNOTATIONS)
    validate_annotations(annotation, package)
    chain = validate_confirmation_chain(ANNOTATIONS, annotation)
    for path in (ANNOTATIONS, chain['path'], chain['original_path'], PACKAGE/'package.json', PACKAGE/'receipt.json'):
        bind(path)
    table, candidate_hash = candidates()
    artifact(DEFAULT_OUTPUT, 'candidates.csv')
    parameters, _, model_receipt = load_models(MODEL_DIR)
    for path in MODEL_DIR.iterdir():
        if path.is_file(): bind(path)
    model_before = {path: digest(PROJECT/path) for path in inputs if path.startswith(MODEL_DIR.relative_to(PROJECT).as_posix())}
    historical = read_json(artifact(FOURGRID, 'fourgrid_rows.json'))
    old_receipt = read_json(FOURGRID/'receipt.json')
    assert old_receipt['candidate_csv_sha256'] == candidate_hash
    assert old_receipt['annotation_sha256'] == digest(ANNOTATIONS)
    assert old_receipt['model_input_sha256'] == {k: v for k, v in model_receipt.items() if k.endswith('sha256')}
    old_dense = {r['candidate_id']: r['D'] for r in historical if r['matched']}
    capacity_rows = list(csv.DictReader(artifact(CAPACITY, 'frame_capacity.csv').open(encoding='utf-8-sig')))
    capacity = {int(r['frame_index']): r for r in capacity_rows if r['variant'] == 'baseline256'}
    assert set(capacity) == set(range(120, 1080))
    reviewed = read_json(artifact(CAPACITY, 'reviewed_frames.json'))
    for row in reviewed:
        if row['variant'] == 'baseline256':
            assert row['source_boxes_top4'] == [json.loads(c['selected_source_box']) for c in table[row['frame_index']]]
    output.mkdir(parents=True)
    config = {'schema': 'E01_same_candidate_roi_source_v1', 'sole_variable': 'ROI image source',
              'source': str(DEFAULT_VIDEO), 'source_sha256': EXPECTED_VIDEO_SHA256,
              'frames': FRAME_IDS, 'capacity_window': [120, 1079],
              'candidate_contract': {'resolution': [256, 144], 'min_run': 2, 'min_area': 16,
                                     'selection': 'original area Top4', 'background': 'reuse frame0 causal frozen candidate history'},
              'A': 'gray[::5,::5], inclusive analysis bbox',
              'B': 'same-frame720p gray, half-open [5*xmin,5*(xmax+1)) and y equivalent',
              'resize': 'min((W*(4+8*u))>>8,W-1), u=0..31; same for y',
              'gray': '(R>>2)+(G>>1)+(B>>2)', 'primary_prediction': 'hog324_q_prediction',
              'model': model_receipt, 'threshold': 'score >= 0 -> vehicle, else ped; unchanged',
              'matching': 'project match: maximum cardinality then total IoU>=0.5; class-correct edges for joint result',
              'processing_failure': 'any candidate error makes its branch frame unusable; targets remain in denominator',
              'capacity_views': ['pre_capacity', 'proxy_L32_R64', 'proxy_L128_R64'],
              'truth_scope': 'confirmed moving ped/vehicle only, correlated development tracks',
              'complete_existing_E01': False,
              'existing_gap': 'fourgrid computed all candidates but retained only matched C/D records, no full predictions or class-correct reassignment',
              'new_annotation_budget': 0, 'retraining': False, 'threshold_scan': False,
              'full_integer_HOG_or_RTL': False, 'inputs_at_start': dict(inputs)}
    dump(output/'experiment.json', config)  # Record contract before inference.
    predictions, target_rows, usage, vectors, failures = [], [], [], {}, []
    hog = make_hog324(); quant = quantization_contract(parameters['opencv_hog324'])
    counts = Counter()
    for ann, saved_frame in zip(annotation['frames'], package['frames']):
        frame_id = ann['frame_index']; assert frame_id == saved_frame['frame_index']
        path = PACKAGE/saved_frame['path']; bind(path)
        assert digest(path) == saved_frame['sha256']
        frame = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if frame is None or frame.shape != (720, 1280, 3):
            dump(output/'blocked.json', {'reason': 'full batch source frame missing or unreadable', 'path': str(path), 'frame_id': frame_id})
            raise ValueError(f'full batch blocked at {path}')
        full = fpga_gray_bgr(frame); analysis = full[::5, ::5]
        cands = table[frame_id]; boxes = [json.loads(c['selected_source_box']) for c in cands]
        targets = [t for t in ann['targets'] if t['label'] in CLASSES and t['motion'] == 'moving']
        geometry = match(targets, boxes)
        branch_records = {'A': [], 'B': []}
        for index, c in enumerate(cands):
            x0,y0,x1,y1 = json.loads(c['selected_analysis_box'])
            assert boxes[index] == [x0*5,y0*5,(x1+1)*5-1,(y1+1)*5-1]
            for branch, crop in [('A', analysis[y0:y1+1,x0:x1+1]),
                                 ('B', full[y0*5:(y1+1)*5,x0*5:(x1+1)*5])]:
                record = {'branch': branch, 'source_frame_id': frame_id, 'candidate_index': index,
                          'candidate_id': c['candidate_id'], 'analysis_bbox': json.dumps([x0,y0,x1,y1]),
                          'source_bbox': json.dumps(boxes[index]), 'roi_source': str(path),
                          'roi_pixel_sha256': '', 'reuse_source': '', 'processing_error': '',
                          'geometrically_unmatched_unknown': index not in geometry.values(),
                          **{k: '' for k in SCORES}}
                try:
                    roi = fpga_resize_roi(crop); record['roi_pixel_sha256'] = pixels(roi)
                    vectors[f'{branch}_f{frame_id:06d}_c{index}'] = roi
                    if branch == 'A':
                        assert pixels(roi) == c['roi_pixel_sha256'], 'historical A crop differs from E01'
                        score = c; record['reuse_source'] = 'frozen_baseline_candidate_csv'
                    elif c['candidate_id'] in old_dense:
                        score = old_dense[c['candidate_id']]
                        assert pixels(roi) == score['roi_pixel_sha256'], 'historical dense crop differs'
                        record['reuse_source'] = 'fourgrid_v2_D'
                    else:
                        score = score_roi(roi, parameters, hog, quant)
                        record['reuse_source'] = 'new_E01_inference'
                    record.update({k: str(score[k]) for k in SCORES})
                    counts[record['reuse_source']] += 1
                except AssertionError:
                    # Contract mismatch invalidates the experiment, never an ordinary missing prediction.
                    dump(output/'blocked.json', {'reason': 'single-variable contract mismatch', 'candidate': c['candidate_id'], 'branch': branch})
                    raise
                except Exception as error:
                    record['processing_error'] = f'{type(error).__name__}: {error}'
                    failures.append(record.copy())
                predictions.append(record); branch_records[branch].append(record)
        for target in ann['targets']:
            eligible = target in targets
            usage.append({'video': str(DEFAULT_VIDEO), 'source_sha256': EXPECTED_VIDEO_SHA256,
                          'frame_id': frame_id, 'target_id': target['track_id'], 'class': target['label'],
                          'bbox_source_inclusive': json.dumps(target['box']), 'motion': target['motion'],
                          'human_confirmed': True, 'original_record': str(chain['original_path']),
                          'imported_record': str(ANNOTATIONS), 'found': True, 'imported': True,
                          'used_E01': eligible, 'purpose': 'evaluation' if eligible else 'excluded_scope',
                          'training': False, 'reserved': False, 'conflict': '',
                          'unused_reason': '' if eligible else 'outside confirmed moving ped/vehicle scope'})
        for view, limit in [('pre_capacity', None), ('proxy_L32_R64', 32), ('proxy_L128_R64', 128)]:
            fail_capacity = limit is not None and (int(capacity[frame_id]['labels_allocated']) > limit or int(capacity[frame_id]['max_runs_per_row']) > 64)
            available_geometry = {} if fail_capacity else geometry
            joint, fixed = {}, {}
            for branch in ('A', 'B'):
                records = branch_records[branch]
                frame_error = any(r['processing_error'] for r in records)
                preds = [r['hog324_q_prediction'] for r in records]
                joint[branch] = {} if fail_capacity or frame_error else joint_match(targets, boxes, preds)
                fixed[branch] = {} if fail_capacity or frame_error else {ti: ci for ti,ci in geometry.items() if preds[ci] == targets[ti]['label']}
            for ti, target in enumerate(targets):
                row = {'view': view, 'source_frame_id': frame_id, 'target_id': target['track_id'],
                       'class': target['label'], 'source_bbox': json.dumps(target['box']),
                       'geometric_match': ti in available_geometry,
                       'geometry_candidate_id': cands[geometry[ti]]['candidate_id'] if ti in geometry else '',
                       'capacity_failed': fail_capacity}
                for branch in ('A','B'):
                    row[f'{branch}_correct'] = ti in joint[branch]
                    row[f'{branch}_candidate_id'] = cands[joint[branch][ti]]['candidate_id'] if ti in joint[branch] else ''
                    row[f'fixed_{branch}_correct'] = ti in fixed[branch]
                    row[f'{branch}_remaining_reason'] = ('correct' if ti in joint[branch] else
                        'capacity_proxy_failure' if fail_capacity else
                        'processing_failure' if any(r['processing_error'] for r in branch_records[branch]) else
                        'no_geometric_candidate' if ti not in geometry else
                        'class_error_or_joint_assignment')
                row['transition'] = ('both_correct' if row['A_correct'] and row['B_correct'] else
                                     'new_correct' if row['B_correct'] else 'lost_correct' if row['A_correct'] else 'neither_correct')
                target_rows.append(row)
        print(f'E01 source frame {frame_id}: {len(cands)} unchanged candidates', flush=True)
    metrics = {v: summarize(target_rows, v) for v in ('pre_capacity','proxy_L32_R64','proxy_L128_R64')}
    verdict, verdict_zh = decision(metrics['pre_capacity'])
    metrics.update({'decision': verdict, 'decision_zh': verdict_zh, 'actual_frames_used': len(FRAME_IDS),
                    'target_observations': len(usage), 'unique_tracks': len({r['target_id'] for r in usage}),
                    'candidates_each_branch': sum(map(len,table.values())), 'reuse_counts': dict(counts),
                    'unknown_each_branch': sum(r['geometrically_unmatched_unknown'] for r in predictions if r['branch']=='A'),
                    'processing_errors': len(failures), 'new_truth_boxes': 0,
                    'precision': None, 'F1': None, 'invalid_FAR': None,
                    'NA_reason': 'no complete negative candidate truth; unknown is not invalid',
                    'capacity_window_failures': {f'L{l}_R64': sum(int(r['labels_allocated'])>l or int(r['max_runs_per_row'])>64 for r in capacity.values()) for l in (32,128)},
                    'capacity_reviewed_frame_failures': {f'L{l}_R64': sum(int(capacity[f]['labels_allocated'])>l or int(capacity[f]['max_runs_per_row'])>64 for f in FRAME_IDS) for l in (32,128)},
                    'elapsed_software_seconds': time.perf_counter()-start})
    write_csv(output/'predictions.csv', predictions); write_csv(output/'target_pairs.csv', target_rows)
    write_csv(output/'annotation_usage.csv', usage); dump(output/'metrics.json', metrics)
    dump(output/'processing_failures.json', failures); dump(output/'inputs_read.json', inputs)
    np.savez_compressed(output/'roi_pixels.npz', **vectors)
    lines = ['# E01 同候选ROI来源对照：实际结果', '',
             '| 类别 | 几何匹配A/B | A定位且类别正确 | B定位且类别正确 | 新增 | 损失 | A仍未正确 | B仍未正确 |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for label, m in metrics['pre_capacity'].items():
        lines.append(f"| {label} | {m['geometry_A']}/{m['N']}（两组相同） | {m['A_correct']}/{m['N']} | {m['B_correct']}/{m['N']} | {m['new_correct']} | {m['lost_correct']} | {m['A_remaining']} | {m['B_remaining']} |")
    lines += ['', f'**决定：{verdict_zh}。** 仅本开发窗口同候选比较；不据此部署或外推其它场景。',
              '', f"实际复用32帧、{len(usage)}个确认目标观测、118自动候选；4条相关轨迹。A复用118原预测，B复用14历史同框高清预测并新推理104个其余候选。无新增画框或训练。",
              f"处理错误：{len(failures)}；unknown候选每组{metrics['unknown_each_branch']}，保留推理、不当invalid。precision/F1/FAR=NA：缺完整负候选真值。",
              '', '## 容量代理后（固定背景事后过滤；不代表RTL或背景回滚状态机）', '']
    for view in ('proxy_L32_R64','proxy_L128_R64'):
        lines += [f'### {view}', '', '| 类别 | 分母 | 几何匹配A/B | A联合正确 | B联合正确 | 新增 | 损失 | A/B仍未正确 |', '|---|---:|---:|---:|---:|---:|---:|---|']
        for label,m in metrics[view].items():
            lines.append(f"| {label} | {m['N']} | {m['geometry_A']}/{m['N']} | {m['A_correct']}/{m['N']} | {m['B_correct']}/{m['N']} | {m['new_correct']} | {m['lost_correct']} | {m['A_remaining']}/{m['B_remaining']} |")
        lines.append('')
    lines += ['## 评价与复用边界', '',
              '几何配对调用项目match：先最大匹配数、再最大总IoU；主联合指标在类别正确边上重新一对一匹配。固定几何配对分类正确数另见metrics.json；逐目标对应候选及原因见target_pairs.csv。',
              'A/B只差ROI图像来源。两组沿用同一Q8中心采样、HOG324浮点特征＋既有量化线性层、零阈值；不是全整数HOG/RTL。冻结候选由frame0因果历史生成，本次无需重建背景或候选。',
              '同批旧fourgrid已有部分结果，只有14个匹配候选双路评分被保存；未对未保存的104个结果冒充历史预测。本轮补全所有候选并记录新推理身份。',
              '已存源帧为同开发视频的哈希校验无损PNG，不重新解码视频。首次A像素哈希逐项复核原候选CSV；历史B14像素哈希复核fourgrid，模型与标注身份也核对。',
              '32帧确认范围是移动人车，存在相关观测、截断目标和未标负区域；不能作为独立验证、停车事件、事故预警或硬件FPS。',
              '27项背景子类仍是独立诊断支线，不影响本次E01。无收益或退化时停止仅替换ROI的改法，不扫描参数，不追加画框。',
              '', '可复现命令：`python -B tools/ddr_metrics_roi_ab.py --output evaluation/ddr_architecture/<新的运行目录>`。',
              '最小检查：`python -B tools/ddr_metrics_roi_ab.py --self-check`。']
    (output/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    assert protected_hashes() == before
    assert all(digest(PROJECT/path) == h for path,h in inputs.items())
    assert all(digest(PROJECT/path) == h for path,h in model_before.items())
    sources = [Path(__file__), PROJECT/'tools/local_paired_diagnostic.py', PROJECT/'tools/local_fourgrid_diagnostic.py',
               PROJECT/'tools/roi_dataset_tool.py', PROJECT/'tools/run_local_scene_pilot.py',
               PROJECT/'external_reference_exploration/opencv_hog_candidate_diagnostic.py']
    (output/'runtime_sources').mkdir()
    for source in sources: (output/'runtime_sources'/source.name).write_bytes(source.read_bytes())
    dump(output/'receipt.json', {'status': 'PASS_completed_E01', 'command': ['python','-B','tools/ddr_metrics_roi_ab.py','--output',str(output)],
          'runtime': {'python':platform.python_version(),'opencv':cv2.__version__,'numpy':np.__version__},
          'source_hashes': {s.relative_to(PROJECT).as_posix():digest(s) for s in sources},
          'inputs_read': inputs, 'protected_sources_unchanged': before, 'self_check': checks,
          'artifact_hashes': {x.relative_to(output).as_posix():digest(x) for x in output.rglob('*') if x.is_file()}})
    return {k:metrics[k] for k in ('decision','pre_capacity','reuse_counts','unknown_each_branch','processing_errors')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'evaluation/ddr_architecture/metrics_roi_ab_20261002_v1')
    parser.add_argument('--self-check',action='store_true')
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),ensure_ascii=False,indent=2))
