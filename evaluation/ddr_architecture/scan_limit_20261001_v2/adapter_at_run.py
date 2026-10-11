#!/usr/bin/env python3
"""扫描上界优化的整数参考与固定 Mask 实验；不修改生产 RTL。

仍按重叠旧 run 的原始标签升序 union，不压缩或回收编号。
只将 bitmap 扫描终点由 MAX_LABEL 缩到本 run 最大重叠标签。
扫描状态次数由源码控制规则推导，不是实测 RTL 总周期。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import digest, filter_short_runs
from ddr_detection_capacity_probe import PROJECT, observe_rle, protected_hashes
from ddr_fixed_mask_trial import load_audit
from local_paired_diagnostic import dump, read_json

PRIOR = PROJECT / 'evaluation/ddr_architecture/fixed_mask_2415171_20261001_v2'
OUTPUT = PROJECT / 'evaluation/ddr_architecture/scan_limit_20261001_v2'
EXPERIMENTS = (
    ('baseline256', 'current', 2, 128, 8, 8, 16),
    ('baseline256', 'keep_all', 1, 192, 8, 8, 16),
    ('ddr640', 'current', 5, 256, 10, 9, 18),
    ('ddr640', 'keep_all', 1, 1024, 10, 9, 18),
)


def storage_bits(capacity, x_width, y_width, area_width, runs=64):
    """计数数组有效位；不推断器件 RAM 块、LUT、DSP 或时序。"""
    width = capacity.bit_length()
    parts = {
        'parent_table': (capacity + 1) * width,
        'feature_table': (capacity + 1) * (area_width + 2*x_width + 2*y_width + 2),
        'raw_run_double_bank': 4*runs*x_width,
        'labeled_run_double_bank': 2*runs*(2*x_width + width),
        'match_bitmap': capacity,
        'extra_scan_limit_register': width,
    }
    return {'label_width': width, 'parts': parts, 'total_bits': sum(parts.values())}


def scan_reference(mask, capacity, label_width=None):
    """独立记录原始标签和合并顺序，并计算两种扫描的状态访问次数。

    超限后只计算无界需求，禁止发布其分区为正常结果；它不模拟 RTL
    超限后的局部执行或具体取消延迟。bitmap 空位没有状态副作用。
    """
    if capacity < 1 or (label_width is not None and capacity >= 1 << label_width):
        raise ValueError('label width must represent 0 through capacity inclusive')
    if mask.ndim != 2 or not mask.size or not np.isin(mask, (0, 1)).all():
        raise ValueError('nonempty binary mask required')
    parents, previous, trace = [0], [], []
    labels = np.zeros(mask.shape, np.int32)
    full_scan = short_scan = union_requests = union_links = comparisons = 0
    find_nodes = find_calls = max_find_nodes = run_total = run_peak = 0
    first_failure = None

    def root(label):
        nonlocal find_nodes, find_calls, max_find_nodes
        nodes = 1
        while parents[label] != label:
            label = parents[label]
            nodes += 1
        find_nodes += nodes
        find_calls += 1
        max_find_nodes = max(max_find_nodes, nodes)
        return label

    for y, row in enumerate(mask):
        delta = np.diff(np.pad(row.astype(np.int8), (1, 1)))
        starts = np.flatnonzero(delta == 1)
        ends = np.flatnonzero(delta == -1) - 1
        run_peak = max(run_peak, len(starts))
        if len(starts) > 64 and first_failure is None:
            first_failure = {'reason': 'run_capacity', 'row': y}
        current = []
        for start, end in zip(starts.tolist(), ends.tolist()):
            run_total += 1
            comparisons += len(previous)
            matched = sorted({label for a, b, label in previous
                              if start <= b+1 and a <= end+1})
            limit = matched[-1] if matched else 0
            # 加一计入扫描结束判定；等待、RAM、union 和其它 FSM 不在此计数。
            full_scan += capacity + 1
            short_scan += limit + 1
            events = []
            if not matched:
                label = len(parents)
                parents.append(label)
                if label > capacity and first_failure is None:
                    first_failure = {'reason': 'label_capacity', 'row': y, 'label': label}
            else:
                label = matched[0]
                for other in matched[1:]:
                    union_requests += 1
                    a, b = root(label), root(other)
                    events.append((label, other, a, b))
                    if a != b:
                        parents[max(a, b)] = min(a, b)
                        union_links += 1
                    label = min(a, b)
            current.append((start, end, label))
            labels[y, start:end+1] = label
            trace.append((y, start, end, tuple(matched), label, tuple(events)))
        previous = current
    union_find = {'calls': find_calls, 'nodes': find_nodes, 'max_nodes': max_find_nodes,
                  'mean_nodes': find_nodes/find_calls if find_calls else 0.0}
    # 此处的帧末根查找另行累计，避免掩盖 union 的 find 压力。
    union_nodes = find_nodes
    lookup = np.array([0] + [root(i) for i in range(1, len(parents))], np.int32)
    resolved = lookup[labels]
    return {
        'status': 'failure' if first_failure else 'success', 'first_failure': first_failure,
        'labels_allocated': len(parents)-1, 'runs_total': run_total, 'row_run_peak': run_peak,
        'union_requests': union_requests, 'union_links': union_links,
        'previous_run_comparisons': comparisons, 'union_find': union_find,
        'frame_end_find_nodes': find_nodes-union_nodes,
        'full_scan_state_visits': full_scan, 'limited_scan_state_visits': short_scan,
        'partition': resolved if first_failure is None else None,
        'unbounded_partition_for_demand_only': resolved, 'trace': trace,
    }


def self_check():
    audit = load_audit()
    rng = np.random.default_rng(2415171)
    masks = [np.zeros((5, 9), np.uint8), np.ones((5, 9), np.uint8),
             np.eye(9, dtype=np.uint8)]
    bridge = np.zeros((3, 9), np.uint8)
    bridge[0, 0] = bridge[0, 4:] = 1
    bridge[1, :5] = bridge[1, 7:] = 1
    bridge[2] = 1
    masks.append(bridge)
    masks += [(rng.random((9, 13)) < .35).astype(np.uint8) for _ in range(40)]
    for mask in masks:
        result = scan_reference(mask, 128)
        profile = observe_rle(mask, capture_pixels=True)
        _, cv_labels = cv2.connectedComponents(mask, connectivity=8)
        assert np.array_equal(audit.canonical(result['partition']), audit.canonical(cv_labels))
        assert result['labels_allocated'] == profile['labels_allocated']
        assert result['union_requests'] == profile['union_requests']
        assert result['union_links'] == profile['union_links']
        assert result['previous_run_comparisons'] == profile['previous_run_comparisons']
        for _, _, _, matched, _, _ in result['trace']:
            bitmap = set(matched)
            full = [label for label in range(1, 129) if label in bitmap]
            limited = [label for label in range(1, max(bitmap, default=0)+1) if label in bitmap]
            assert full == limited == list(matched)
    exact = np.tile([1, 0], 32).astype(np.uint8)[None, :]
    assert scan_reference(exact, 32, 6)['status'] == 'success'
    assert scan_reference(np.pad(exact, ((0, 0), (0, 2)), constant_values=1), 32, 6)['status'] == 'failure'
    assert scan_reference(np.zeros((2, 3), np.uint8), 32)['status'] == 'success'
    try:
        scan_reference(exact, 512, 9)
    except ValueError:
        pass
    else:
        raise AssertionError('0..512 cannot fit 9 bits')
    assert storage_bits(1024, 10, 9, 18)['label_width'] == 11
    return {'status': 'PASS', 'partition_order_checks': len(masks),
            'overflow_empty_next_frame_and_width_checks': 'PASS_reference_only'}


def run(output):
    if output.exists() or not output.resolve().is_relative_to((PROJECT/'evaluation/ddr_architecture').resolve()):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    audit = load_audit()
    receipt = read_json(PRIOR/'receipt.json')
    for name, expected in receipt['artifact_hashes'].items():
        if digest(PRIOR/name) != expected:
            raise ValueError('fixed-mask evidence changed')
    manifest = read_json(PRIOR/'mask_manifest.json')['frames']
    expected_rows = {(r['config'], r['branch'], int(r['frame_id'])): r
                     for r in csv.DictReader((PRIOR/'frame_audit.csv').open(encoding='utf-8', newline=''))}
    protected = protected_hashes()
    rows = []
    output.mkdir(parents=True)
    for index, entry in enumerate(manifest):
        path = (PRIOR/entry['path']).resolve()
        if not path.is_relative_to(PRIOR.resolve()) or digest(path) != entry['sha256']:
            raise ValueError('fixed clean mask changed or escaped input directory')
        clean = np.load(path, allow_pickle=False)
        for config, branch, minimum, capacity, xw, yw, aw in EXPERIMENTS:
            if config != entry['config']:
                continue
            mask = filter_short_runs(clean, minimum)
            data = scan_reference(mask, capacity, capacity.bit_length())
            _, cv_labels = cv2.connectedComponents(mask, connectivity=8)
            if not np.array_equal(audit.canonical(data['unbounded_partition_for_demand_only']), audit.canonical(cv_labels)):
                raise AssertionError('proposed scan-limit reference partition differs from OpenCV')
            old = expected_rows[(config, branch, entry['frame_id'])]
            assert data['labels_allocated'] == int(old['reference_labels_allocated'])
            assert data['runs_total'] == int(old['total_runs_after_filter'])
            rows.append({'config': config, 'branch': branch, 'frame_id': entry['frame_id'],
                         'experimental_capacity': capacity, 'experimental_label_width': capacity.bit_length(),
                         **{k: data[k] for k in ('status', 'labels_allocated', 'runs_total', 'row_run_peak',
                            'union_requests', 'union_links', 'previous_run_comparisons',
                            'full_scan_state_visits', 'limited_scan_state_visits', 'frame_end_find_nodes')},
                         **{'union_find_'+k: v for k, v in data['union_find'].items()}})
        if index % 240 == 239:
            print(f'profiled {index+1}/{len(manifest)} clean masks', flush=True)
    if protected_hashes() != protected:
        raise AssertionError('production sources/configuration or plan changed during reference trial')
    summary = {}
    for config, branch, minimum, capacity, xw, yw, aw in EXPERIMENTS:
        selected = [r for r in rows if r['config']==config and r['branch']==branch]
        full = sum(r['full_scan_state_visits'] for r in selected)
        limited = sum(r['limited_scan_state_visits'] for r in selected)
        summary[f'{config}/{branch}'] = {
            'capacity': capacity, 'storage': storage_bits(capacity, xw, yw, aw),
            'frames': len(selected), 'capacity_proxy_failure_frames': sum(r['status']=='failure' for r in selected),
            'peak_labels': max(r['labels_allocated'] for r in selected),
            'scan_visits_total_full': full, 'scan_visits_total_limited': limited,
            'scan_visits_saved_fraction': 1-limited/full if full else 0,
            'peak_scan_visits_full': max(r['full_scan_state_visits'] for r in selected),
            'peak_scan_visits_limited': max(r['limited_scan_state_visits'] for r in selected),
            'peak_union_requests': max(r['union_requests'] for r in selected),
            'peak_union_links': max(r['union_links'] for r in selected),
            'peak_previous_run_comparisons': max(r['previous_run_comparisons'] for r in selected),
            'peak_union_find_nodes': max(r['union_find_max_nodes'] for r in selected),
        }
    report = {'status':'software_reference_not_rtl_ready', 'summary':summary,
              'partition_checks':len(rows), 'self_check':self_check(),
              'contract':'raw-label ascending union, no compression/reuse; scan limit=max matched raw label, zero if empty; wait for all previous returns first',
              'boundaries':['Scan-state visits are derived counts, not measured RTL cycles or full task latency.',
                            'Logical array bits exclude control/pipeline registers, RAM mapping/granularity, routing, LUT/DSP and other vision modules.',
                            'Experiment capacities are controls for this fixed-mask workload, not deployment capacities.',
                            'Only empty bitmap suffix visits are removed; mask, partition, bbox/area and candidate geometry remain unchanged.',
                            'No new classifier, invalid truth, background policy, scheduler history, RTL simulation, synthesis or blind test.']}
    with (output/'frame_scan.csv').open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    dump(output/'report.json',report)
    lines=['# CCL 扫描上界优化与容量预算','',
           '软件参考保留每条 run 的原始标签升序合并，只去掉最高匹配标签之后的空 bitmap 扫描。未修改生产 RTL。','',
           '| 配置/分支 | 实验容量/位宽 | 超限帧 | 逻辑数组位数（含新增上界寄存器） | 扫描访问总量减少 | 峰值：全容量扫描/上界扫描 |',
           '|---|---|---:|---:|---:|---|']
    for key, data in summary.items():
        lines.append(f"| {key} | {data['capacity']}/{data['storage']['label_width']} | {data['capacity_proxy_failure_frames']}/{data['frames']} | {data['storage']['total_bits']} | {data['scan_visits_saved_fraction']:.1%} | {data['peak_scan_visits_full']}/{data['peak_scan_visits_limited']} |")
    lines+=['', '扫描访问不是 RTL 总周期，逻辑位数不是综合资源。容量扩大没有改变候选几何或分类效果。',
            '', '实现约束：最大重叠原始标签必须随 run 清零；收齐全部 previous-row 返回后才开始扫描，最后一次返回的上界更新须在下一拍可见；union 的根变化不能重排原始标签；超限输出不得作为成功发布。',
            '', '正式验证仍须覆盖最后返回拍、不同合法间隙、满表、union 链、溢出取消和随后空帧/正常帧，比较逐 run 最终根分区与面积框。',
            '', f"本批 {len(rows)} 个过滤 Mask 与 OpenCV 分区一致；自检 {report['self_check']['partition_order_checks']} 个用例通过。"]
    (output/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    sources=[Path(__file__), PROJECT/'tools/ddr_detection_capacity_probe.py',
             PROJECT/'tools/ddr_fixed_mask_trial.py', PROJECT/'tools/candidate_chain_reference.py',
             PROJECT/'user_source/hdl_source/road_vision/row_matcher.v',
             PROJECT/'user_source/hdl_source/road_vision/feature_table.v',
             PROJECT/'user_source/hdl_source/road_vision/raw_run_table.v',
             PROJECT/'user_source/hdl_source/road_vision/labeled_run_table.v']
    dump(output/'receipt.json',{'command':[sys.executable,*sys.argv],
        'prior_receipt_sha256':digest(PRIOR/'receipt.json'),
        'source_hashes':{p.relative_to(PROJECT).as_posix():digest(p) for p in sources},
        'protected_sources_unchanged':protected,
        'artifacts':{p.name:digest(p) for p in output.iterdir() if p.is_file()},
        'runtime':{'python':sys.version,'opencv':cv2.__version__,'numpy':np.__version__}})
    return {'summary':summary,'partition_checks':len(rows),'report':str(output/'report.md')}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check',action='store_true')
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),ensure_ascii=False,indent=2))
