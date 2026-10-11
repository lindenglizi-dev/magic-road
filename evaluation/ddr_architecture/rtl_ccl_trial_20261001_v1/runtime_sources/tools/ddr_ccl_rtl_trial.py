#!/usr/bin/env python3
"""Bounded Icarus trial for production CCL versus isolated scan-limit RTL."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

from candidate_chain_reference import digest, filter_short_runs
from ddr_ccl_scan_reference import scan_reference
from ddr_detection_capacity_probe import protected_hashes
from local_paired_diagnostic import dump

PROJECT = Path(__file__).resolve().parents[1]
FIXED = PROJECT / 'evaluation/ddr_architecture/fixed_mask_2415171_20261001_v2'
SCAN = PROJECT / 'evaluation/ddr_architecture/scan_limit_20261001_v2/frame_scan.csv'
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/rtl_ccl_trial_20261001_v1'
IVERILOG = PROJECT.parents[1] / '.tools/iverilog/bin/iverilog.exe'
VVP = PROJECT.parents[1] / '.tools/iverilog/bin/vvp.exe'
TB = PROJECT / 'tests/tb_ddr_ccl_fixed_mask.v'
BASE_ROW = PROJECT / 'user_source/hdl_source/road_vision/row_matcher.v'
OPT_ROW = PROJECT / 'tests/experimental_ddr_ccl/row_matcher.v'
RTL = PROJECT / 'user_source/hdl_source/road_vision'
COMMON_RTL = [RTL / name for name in (
    'rle_ccl_top.v', 'run_detector.v', 'raw_run_table.v',
    'labeled_run_table.v', 'label_manager.v', 'feature_table.v',
    'frame_resolver.v', 'top4_selector.v')]
CONFIGS = {
    ('baseline256', 'current'): (2, 128, 8, 8, 16),
    ('baseline256', 'keep_all'): (1, 192, 8, 8, 16),
    ('ddr640', 'current'): (5, 256, 10, 9, 18),
    ('ddr640', 'keep_all'): (1, 1024, 10, 9, 18),
}


def write_mem(path: Path, masks: list[np.ndarray]) -> None:
    shape = masks[0].shape
    if any(mask.shape != shape for mask in masks):
        raise ValueError('all masks in one simulation must have the same shape')
    with path.open('w', encoding='ascii', newline='\n') as stream:
        for mask in masks:
            stream.writelines('1\n' if value else '0\n' for value in mask.ravel())


def parse_log(path: Path) -> tuple[list[list[str]], list[dict]]:
    rows = list(csv.reader(path.open(encoding='utf-8', newline='')))
    semantic, metrics = [], []
    for row in rows:
        if row[0] in ('FEATURE', 'UNION', 'OBJECT', 'FINAL'):
            semantic.append(row)
        elif row[0] == 'DONE':
            semantic.append(row[:2] + row[7:])
            metrics.append({
                'frame': int(row[1]), 'total_cycles': int(row[2]),
                'scan_state_cycles': int(row[3]), 'row_match_cycle_max': int(row[4]),
                'resolve_cycle_max': int(row[5]), 'select_cycle_max': int(row[6]),
                'feature_events': int(row[7]), 'union_events': int(row[8]),
                'object_events': int(row[9]), 'object_count': int(row[10]),
                'run_overflow': int(row[11]), 'label_overflow': int(row[12]),
                'protocol_error': int(row[13]), 'ccl_error': int(row[14]),
            })
    return semantic, metrics


def gold_features(mask: np.ndarray, capacity: int, width: int) -> dict[int, tuple[int, ...]]:
    result = scan_reference(mask, capacity, width)
    if result['status'] != 'success':
        return {}
    labels = result['partition']
    features = {}
    for label in np.unique(labels):
        if label == 0:
            continue
        ys, xs = np.nonzero(labels == label)
        features[int(label)] = (len(xs), int(xs.min()), int(xs.max()),
                                int(ys.min()), int(ys.max()))
    return features


def gold_events(mask: np.ndarray, capacity: int, width: int, frame: int = 0):
    result = scan_reference(mask, capacity, width)
    if result['status'] != 'success':
        return None
    expected = []
    for y, start, end, matched, label, events in result['trace']:
        expected.extend([['UNION', str(frame), str(event[0]), str(event[1])]
                         for event in events])
        expected.append(['FEATURE', str(frame), str(label), str(int(not matched)),
                         str(start), str(end), str(y)])
    return expected


def log_features(rows: list[list[str]], frame: int) -> dict[int, tuple[int, ...]]:
    return {int(row[2]): tuple(map(int, row[5:10]))
            for row in rows if row[0] == 'FINAL' and int(row[1]) == frame and int(row[4])}


def compile_and_run(case_dir: Path, name: str, masks: list[np.ndarray], minimum: int,
                    capacity: int, x_width: int, y_width: int, area_width: int,
                    optimized: bool, pixel_gap: int = 0,
                    wait_frame_done: int = 1) -> tuple[list[list[str]], list[dict], list[str]]:
    variant = 'optimized' if optimized else 'baseline'
    run_dir = case_dir / variant
    run_dir.mkdir(parents=True)
    mem = run_dir / 'mask.mem'
    log = run_dir / 'events.csv'
    image = run_dir / 'simulation.vvp'
    write_mem(mem, masks)
    height, width = masks[0].shape
    params = {
        'FRAME_WIDTH': width, 'FRAME_HEIGHT': height, 'FRAME_COUNT': len(masks),
        'X_WIDTH': x_width, 'Y_WIDTH': y_width,
        'LABEL_WIDTH': capacity.bit_length(), 'AREA_WIDTH': area_width,
        'MAX_RUN': 64, 'MAX_LABEL': capacity, 'MIN_AREA': 1,
        'MIN_RUN_LENGTH': minimum, 'PIXEL_GAP': pixel_gap,
        'WAIT_FRAME_DONE': wait_frame_done,
    }
    command = [str(IVERILOG), '-g2012', '-Wall', '-s', 'tb_ddr_ccl_fixed_mask']
    command += [f'-Ptb_ddr_ccl_fixed_mask.{key}={value}' for key, value in params.items()]
    command += ['-o', str(image), str(TB), str(OPT_ROW if optimized else BASE_ROW)]
    command += [str(path) for path in COMMON_RTL]
    compiled = subprocess.run(command, cwd=PROJECT, text=True, capture_output=True, timeout=120)
    if compiled.returncode:
        raise RuntimeError(f'{name}/{variant} compile failed:\n{compiled.stdout}{compiled.stderr}')
    run_command = [str(VVP), str(image), f'+MASK={mem}', f'+LOG={log}']
    ran = subprocess.run(run_command, cwd=PROJECT, text=True, capture_output=True, timeout=600)
    (run_dir / 'compile.log').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
    (run_dir / 'simulation.log').write_text(ran.stdout + ran.stderr, encoding='utf-8')
    if ran.returncode:
        raise RuntimeError(f'{name}/{variant} run failed:\n{ran.stdout}{ran.stderr}')
    semantic, metrics = parse_log(log)
    if wait_frame_done and len(metrics) != len(masks):
        raise AssertionError(f'{name}/{variant}: missing DONE records')
    return semantic, metrics, command + ['RUN:'] + run_command


def selected_real_cases() -> list[dict]:
    rows = list(csv.DictReader(SCAN.open(encoding='utf-8', newline='')))
    manifest = json.loads((FIXED / 'mask_manifest.json').read_text(encoding='utf-8'))['frames']
    paths = {(entry['config'], int(entry['frame_id'])): FIXED / entry['path']
             for entry in manifest}
    selected = []
    for key, params in CONFIGS.items():
        candidates = [row for row in rows if (row['config'], row['branch']) == key]
        peak = max(candidates, key=lambda row: (int(row['labels_allocated']),
                                                 int(row['row_run_peak']),
                                                 int(row['union_requests'])))
        frame_ids = {int(peak['frame_id'])}
        if key[0] == 'baseline256':
            frame_ids.update((300, 450))
        for frame_id in sorted(frame_ids):
            minimum, capacity, xw, yw, aw = params
            selected.append({
                'name': f'{key[0]}_{key[1]}_f{frame_id}', 'config': key[0],
                'branch': key[1], 'frame_id': frame_id, 'minimum': minimum,
                'capacity': capacity, 'x_width': xw, 'y_width': yw,
                'area_width': aw,
                'path': paths[(key[0], frame_id)],
            })
    return selected


def synthetic_cases() -> list[dict]:
    bridge = np.zeros((3, 9), np.uint8)
    bridge[0, 0] = bridge[0, 4:] = 1
    bridge[1, :5] = bridge[1, 7:] = 1
    bridge[2] = 1
    boundary = []
    exact = np.zeros((2, 264), np.uint8)
    for x in range(0, 256, 8):
        exact[0, x:x+5] = 1
    exact[1] = 1
    overflow = exact.copy()
    overflow[0, 256:261] = 1
    empty = np.zeros_like(exact)
    normal = np.zeros_like(exact)
    normal[:, 260:264] = 1
    boundary.extend((exact, overflow, empty, normal))
    return [
        {'name': 'synthetic_merge_right_edge_valid_gap', 'masks': [bridge],
         'minimum': 1, 'capacity': 32, 'x_width': 4, 'y_width': 2,
         'area_width': 16, 'pixel_gap': 1, 'wait': 1},
        {'name': 'synthetic_exact32_overflow_empty_normal', 'masks': boundary,
         'minimum': 1, 'capacity': 32, 'x_width': 9, 'y_width': 1,
         'area_width': 16, 'pixel_gap': 0, 'wait': 1},
        {'name': 'synthetic_sof_while_busy_probe', 'masks': [bridge, bridge],
         'minimum': 1, 'capacity': 32, 'x_width': 4, 'y_width': 2,
         'area_width': 16, 'pixel_gap': 0, 'wait': 0},
    ]


def run(output: Path) -> dict:
    if output.exists() or not output.resolve().is_relative_to(
            (PROJECT / 'evaluation/ddr_architecture').resolve()):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    for path in [IVERILOG, VVP, TB, BASE_ROW, OPT_ROW, SCAN, FIXED]:
        if not path.exists():
            raise FileNotFoundError(path)
    protected = protected_hashes()
    output.mkdir(parents=True)
    results, commands = [], []
    cases = selected_real_cases()
    for item in cases:
        clean = np.load(item['path'], allow_pickle=False).astype(np.uint8)
        masks = [clean]
        case_dir = output / item['name']
        base, base_metrics, base_cmd = compile_and_run(
            case_dir, item['name'], masks, item['minimum'], item['capacity'],
            item['x_width'], item['y_width'], item['area_width'], False)
        opt, opt_metrics, opt_cmd = compile_and_run(
            case_dir, item['name'], masks, item['minimum'], item['capacity'],
            item['x_width'], item['y_width'], item['area_width'], True)
        semantic_equal = base == opt
        filtered = filter_short_runs(clean, item['minimum'])
        gold = gold_features(filtered, item['capacity'], item['capacity'].bit_length())
        gold_equal = log_features(base, 0) == gold if not base_metrics[0]['ccl_error'] else None
        observed_events = [row for row in base if row[0] in ('FEATURE', 'UNION')]
        event_gold_equal = observed_events == gold_events(
            filtered, item['capacity'], item['capacity'].bit_length())
        results.append({**{k: v for k, v in item.items() if k != 'path'},
                        'input_sha256': digest(item['path']),
                        'semantic_equal': semantic_equal, 'gold_features_equal': gold_equal,
                        'gold_events_equal': event_gold_equal,
                        'baseline': base_metrics, 'optimized': opt_metrics})
        if not semantic_equal or gold_equal is False or not event_gold_equal:
            raise AssertionError(f"semantic/gold mismatch: {item['name']}")
        commands += [base_cmd, opt_cmd]
        print(f"PASS {item['name']} cycles {base_metrics[0]['total_cycles']} -> "
              f"{opt_metrics[0]['total_cycles']}", flush=True)
    for item in synthetic_cases():
        case_dir = output / item['name']
        args = (case_dir, item['name'], item['masks'], item['minimum'], item['capacity'],
                item['x_width'], item['y_width'], item['area_width'])
        base, bm, bc = compile_and_run(*args, False, item['pixel_gap'], item['wait'])
        opt, om, oc = compile_and_run(*args, True, item['pixel_gap'], item['wait'])
        equal = base == opt
        results.append({'name': item['name'], 'synthetic': True,
                        'semantic_equal': equal, 'baseline': bm, 'optimized': om})
        if not equal and item['wait']:
            raise AssertionError(f"baseline/optimized mismatch: {item['name']}")
        commands += [bc, oc]
        print(f"PASS {item['name']}", flush=True)
    if protected_hashes() != protected:
        raise AssertionError('protected production source or frozen file changed')
    rows = []
    for result in results:
        for variant in ('baseline', 'optimized'):
            for metric in result[variant]:
                rows.append({'case': result['name'], 'variant': variant, **metric})
    with (output / 'cycles.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    dump(output / 'cases.json', results)
    real = [r for r in results if not r.get('synthetic')]
    lines = ['# CCL 本地 Icarus 固定 Mask 验证', '',
             f'- 有限真实 Mask：{len(real)} 个；每组取累计标签峰值帧，256 组另含人工帧 300/450。',
             '- 合法输入下基线与隔离优化版逐事件语义日志一致；周期字段不参与语义相等判定。',
             '- MIN_AREA=1，用于检查全部最终组件 feature，不是正式 16/100 面积候选评价。',
             '- 输入逐行等待 row_done，不是连续相机、DDR 或最终调度链。', '',
             '| 用例 | 基线总周期 | 优化总周期 | 扫描状态周期 基线→优化 | CCL错误 |',
             '|---|---:|---:|---:|---:|']
    for result in real:
        b, o = result['baseline'][0], result['optimized'][0]
        lines.append(f"| {result['name']} | {b['total_cycles']} | {o['total_cycles']} | "
                     f"{b['scan_state_cycles']}→{o['scan_state_cycles']} | {b['ccl_error']} |")
    lines += ['', '边界：没有重跑视频、没有综合/布局布线、没有测 DDR/CDC/显示，也不证明识别准确率或 15/20 Hz。SOF-busy 是故障探针，不计入合法输入性能。']
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    sources = [Path(__file__), TB, PROJECT/'tests/tb_ddr_ccl_fixed_mask_spec.md',
               BASE_ROW, OPT_ROW, *COMMON_RTL]
    receipt = {
        'status': 'PASS_bounded_local_simulation',
        'python': sys.version, 'numpy': np.__version__,
        'tools': {'iverilog_sha256': digest(IVERILOG), 'vvp_sha256': digest(VVP)},
        'source_hashes': {p.relative_to(PROJECT).as_posix(): digest(p) for p in sources},
        'commands': commands, 'case_count': len(results),
        'real_mask_count': len(real), 'protected_sources_unchanged': protected,
        'boundaries': ['bounded saved masks only', 'row-paced input',
                       'no DDR/CDC/display', 'no synthesis or timing closure',
                       'no accuracy claim'],
    }
    dump(output / 'receipt.json', receipt)
    return {'status': receipt['status'], 'cases': len(results), 'output': str(output)}


def self_check() -> dict:
    mask = np.array([[1, 0, 1], [1, 1, 1]], np.uint8)
    assert filter_short_runs(mask, 2).tolist() == [[0, 0, 0], [1, 1, 1]]
    root = Path(tempfile.mkdtemp(prefix='ddr_ccl_rtl_'))
    base, bm, _ = compile_and_run(root, 'self_check', [mask], 1, 32, 2, 1, 8, False)
    opt, om, _ = compile_and_run(root, 'self_check', [mask], 1, 32, 2, 1, 8, True)
    assert base == opt and bm[0]['ccl_error'] == 0 and om[0]['ccl_error'] == 0
    assert log_features(base, 0) == gold_features(mask, 32, 6)
    assert [row for row in base if row[0] in ('FEATURE', 'UNION')] == gold_events(mask, 32, 6)
    return {'status': 'PASS', 'compile_run_and_gold': 'PASS',
            'preserved_run_directory': str(root)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),
                     ensure_ascii=False, indent=2))
