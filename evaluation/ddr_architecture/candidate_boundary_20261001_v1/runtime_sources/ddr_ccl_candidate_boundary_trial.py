#!/usr/bin/env python3
"""Formal candidate thresholds and CCL capacity/run boundary trial."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

import ddr_ccl_rtl_trial as prior
from candidate_chain_reference import digest, filter_short_runs
from ddr_ccl_scan_reference import scan_reference
from ddr_detection_capacity_probe import protected_hashes
from local_paired_diagnostic import dump


PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / 'evaluation/ddr_architecture/candidate_boundary_20261001_v1'
PRIOR = PROJECT / 'evaluation/ddr_architecture/rtl_ccl_trial_20261001_v1'
SCAN = PROJECT / 'evaluation/ddr_architecture/scan_limit_20261001_v2/frame_scan.csv'
FIXED = PROJECT / 'evaluation/ddr_architecture/fixed_mask_2415171_20261001_v2'

MIN_AREA = {'baseline256': 16, 'ddr640': 100}


def objects(rows: list[list[str]], frame: int = 0) -> list[dict]:
    return [
        {'index': int(row[2]), 'label': int(row[3]), 'area': int(row[4]),
         'xmin': int(row[5]), 'xmax': int(row[6]),
         'ymin': int(row[7]), 'ymax': int(row[8])}
        for row in rows if row[0] == 'OBJECT' and int(row[1]) == frame
    ]


def gold_candidates(mask: np.ndarray, minimum: int, capacity: int,
                    min_area: int) -> tuple[list[dict], dict]:
    filtered = filter_short_runs(mask, minimum)
    result = scan_reference(filtered, capacity, capacity.bit_length())
    if result['status'] != 'success':
        return [], result
    labels = result['partition']
    found = []
    for label in np.unique(labels):
        if label == 0:
            continue
        ys, xs = np.nonzero(labels == label)
        area = len(xs)
        if area >= min_area:
            found.append({'index': 0, 'label': int(label), 'area': area,
                          'xmin': int(xs.min()), 'xmax': int(xs.max()),
                          'ymin': int(ys.min()), 'ymax': int(ys.max())})
    found.sort(key=lambda item: (-item['area'], item['label']))
    for index, item in enumerate(found[:4]):
        item['index'] = index
    return found[:4], result


def compile_and_run(case_dir: Path, name: str, masks: list[np.ndarray],
                    minimum: int, min_area: int, capacity: int,
                    x_width: int, y_width: int, area_width: int,
                    optimized: bool, pixel_gap: int = 0) -> tuple[list[list[str]], list[dict], list[str]]:
    variant = 'optimized' if optimized else 'baseline'
    run_dir = case_dir / variant
    run_dir.mkdir(parents=True)
    mem, log = run_dir / 'mask.mem', run_dir / 'events.csv'
    image = run_dir / 'simulation.vvp'
    prior.write_mem(mem, masks)
    height, width = masks[0].shape
    params = {
        'FRAME_WIDTH': width, 'FRAME_HEIGHT': height, 'FRAME_COUNT': len(masks),
        'X_WIDTH': x_width, 'Y_WIDTH': y_width,
        'LABEL_WIDTH': capacity.bit_length(), 'AREA_WIDTH': area_width,
        'MAX_RUN': 64, 'MAX_LABEL': capacity, 'MIN_AREA': min_area,
        'MIN_RUN_LENGTH': minimum, 'PIXEL_GAP': pixel_gap, 'WAIT_FRAME_DONE': 1,
    }
    command = [str(prior.IVERILOG), '-g2012', '-Wall', '-s', 'tb_ddr_ccl_fixed_mask']
    command += [f'-Ptb_ddr_ccl_fixed_mask.{key}={value}' for key, value in params.items()]
    command += ['-o', str(image), str(prior.TB),
                str(prior.OPT_ROW if optimized else prior.BASE_ROW)]
    command += [str(path) for path in prior.COMMON_RTL]
    compiled = subprocess.run(command, cwd=PROJECT, text=True,
                              capture_output=True, timeout=120)
    (run_dir / 'compile.log').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
    if compiled.returncode:
        raise RuntimeError(f'{name}/{variant} compile failed')
    run_command = [str(prior.VVP), str(image), f'+MASK={mem}', f'+LOG={log}']
    ran = subprocess.run(run_command, cwd=PROJECT, text=True,
                         capture_output=True, timeout=900)
    (run_dir / 'simulation.log').write_text(ran.stdout + ran.stderr, encoding='utf-8')
    if ran.returncode:
        raise RuntimeError(f'{name}/{variant} run failed:\n{ran.stdout}{ran.stderr}')
    semantic, metrics = prior.parse_log(log)
    if len(metrics) != len(masks):
        raise AssertionError(f'{name}/{variant}: missing DONE record')
    return semantic, metrics, command + ['RUN:'] + run_command


def selected_real_cases() -> list[dict]:
    old = json.loads((PRIOR / 'cases.json').read_text(encoding='utf-8'))
    old = [case for case in old if not case.get('synthetic')]
    manifest = json.loads((FIXED / 'mask_manifest.json').read_text(encoding='utf-8'))['frames']
    paths = {(item['config'], int(item['frame_id'])): FIXED / item['path'] for item in manifest}
    result = []
    for case in old:
        path = paths[(case['config'], int(case['frame_id']))]
        if digest(path) != case['input_sha256']:
            raise AssertionError(f"prior mask changed: {case['name']}")
        result.append({
            'name': case['name'], 'config': case['config'], 'branch': case['branch'],
            'frame_id': int(case['frame_id']), 'path': path,
            'mask_sha256': case['input_sha256'], 'minimum': int(case['minimum']),
            'min_area': MIN_AREA[case['config']], 'capacity': int(case['capacity']),
            'x_width': int(case['x_width']), 'y_width': int(case['y_width']),
            'area_width': int(case['area_width']),
        })
    if len(result) != 8:
        raise AssertionError('expected the eight preserved real-mask cases')
    return result


def threshold_cases() -> list[dict]:
    small = np.zeros((1, 64), np.uint8)
    small[0, 0:15] = 1
    small[0, 16:32] = 1
    small[0, 33:50] = 1
    large = np.zeros((1, 320), np.uint8)
    large[0, 0:99] = 1
    large[0, 100:200] = 1
    large[0, 201:302] = 1
    return [
        {'name': 'threshold_256_area_15_16_17', 'mask': small, 'minimum': 2,
         'min_area': 16, 'capacity': 128, 'x_width': 8, 'y_width': 1,
         'area_width': 16, 'expected_areas': [17, 16]},
        {'name': 'threshold_640_area_99_100_101', 'mask': large, 'minimum': 5,
         'min_area': 100, 'capacity': 256, 'x_width': 9, 'y_width': 1,
         'area_width': 18, 'expected_areas': [101, 100]},
    ]


def separated_births(capacity: int, overflow: bool) -> np.ndarray:
    groups = capacity // 64 + (1 if capacity % 64 else 0)
    height = groups * 2 + 1
    mask = np.zeros((height, 127), np.uint8)
    remaining = capacity
    for group in range(groups):
        count = min(64, remaining)
        mask[group * 2, :count * 2:2] = 1
        remaining -= count
    if overflow:
        mask[groups * 2, 0] = 1
    return mask


def boundary_cases() -> list[dict]:
    cases = []
    for capacity in (128, 192):
        exact = separated_births(capacity, False)
        over = separated_births(capacity, True)
        empty, normal = np.zeros_like(exact), np.zeros_like(exact)
        normal[-1, 0:4] = 1
        cases.append({'name': f'label_{capacity}_and_{capacity + 1}_recovery',
                      'masks': [exact, over, empty, normal], 'minimum': 1,
                      'min_area': 1, 'capacity': capacity,
                      'x_width': 7, 'y_width': max(1, (exact.shape[0]-1).bit_length()),
                      'area_width': 16, 'kind': 'label'})
    run64 = np.zeros((1, 129), np.uint8)
    run64[0, 0:127:2] = 1
    run65 = run64.copy()
    run65[0, 128] = 1
    empty, normal = np.zeros_like(run64), np.zeros_like(run64)
    normal[0, 0:4] = 1
    cases.append({'name': 'run_64_and_65_recovery',
                  'masks': [run64, run65, empty, normal], 'minimum': 1,
                  'min_area': 1, 'capacity': 128, 'x_width': 8, 'y_width': 1,
                  'area_width': 16, 'kind': 'run'})
    return cases


@dataclass
class TwoLineBank:
    """Contract model only; it is not connected to production RTL."""

    slots: list[dict | None]
    write_bank: int = 0
    read_bank: int = 0
    canceling: bool = False

    @classmethod
    def create(cls) -> 'TwoLineBank':
        return cls([None, None])

    def accept(self, row_id: int, payload: tuple[int, ...], last: bool = False) -> bool:
        if self.canceling or self.slots[self.write_bank] is not None:
            return False
        self.slots[self.write_bank] = {'row_id': row_id, 'payload': payload, 'last': last}
        self.write_bank ^= 1
        return True

    def release(self, discard: bool = False) -> dict | None:
        item = self.slots[self.read_bank]
        if item is None:
            return None
        self.slots[self.read_bank] = None
        self.read_bank ^= 1
        return {'row_id': item['row_id'], 'last': item['last'],
                'discarded': bool(discard or self.canceling), 'payload': item['payload']}

    def cancel(self) -> None:
        self.canceling = True

    def finish_cancel(self) -> bool:
        if any(slot is not None for slot in self.slots):
            return False
        self.canceling = False
        self.write_bank = self.read_bank
        return True


def bank_model_check() -> dict:
    bank = TwoLineBank.create()
    events = []
    assert bank.accept(0, (1, 0))
    assert bank.accept(1, (0, 1))
    assert not bank.accept(2, (1, 1))
    events.append({'event': 'both_full_blocks_accept', 'accepted': False})
    first = bank.release()
    assert first and first['row_id'] == 0 and not first['discarded']
    assert bank.accept(2, (1, 1), last=True)
    second = bank.release()
    assert second and second['row_id'] == 1
    bank.cancel()
    assert not bank.accept(3, (0, 0))
    pending = bank.release()
    assert pending and pending['row_id'] == 2 and pending['last'] and pending['discarded']
    assert bank.finish_cancel() and not any(bank.slots)
    events += [first, second, pending, {'event': 'cancel_drained', 'accepted_after_drain': True}]

    mask = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 1]], np.uint8)
    def replay(gaps: set[int]) -> np.ndarray:
        model, rows = TwoLineBank.create(), []
        for y, row in enumerate(mask):
            if y in gaps:
                pass  # legal idle: no state transition
            if not model.accept(y, tuple(map(int, row)), y == len(mask)-1):
                released = model.release()
                if released and not released['discarded']:
                    rows.append(released['payload'])
                assert model.accept(y, tuple(map(int, row)), y == len(mask)-1)
        while any(model.slots):
            released = model.release()
            if released and not released['discarded']:
                rows.append(released['payload'])
        return np.asarray(rows, np.uint8)
    assert np.array_equal(replay(set()), replay({0, 2}))
    return {'status': 'PASS_python_contract_model', 'events': events,
            'same_mask_legal_gap_equal': True,
            'boundary': 'Python row-bank contract model; not production RTL integration evidence.'}


def run(output: Path) -> dict:
    root = (PROJECT / 'evaluation/ddr_architecture').resolve()
    if output.exists() or not output.resolve().is_relative_to(root):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    for path in [prior.IVERILOG, prior.VVP, prior.TB, prior.BASE_ROW, prior.OPT_ROW,
                 SCAN, FIXED, PRIOR / 'receipt.json', PRIOR / 'cases.json']:
        if not path.exists():
            raise FileNotFoundError(path)
    protected = protected_hashes()
    output.mkdir(parents=True)
    commands, records, alignment = [], [], []
    scan_rows = {(row['config'], row['branch'], int(row['frame_id'])): row
                 for row in csv.DictReader(SCAN.open(encoding='utf-8', newline=''))}

    for case in selected_real_cases():
        mask = np.load(case['path'], allow_pickle=False).astype(np.uint8)
        base, bm, bc = compile_and_run(output / case['name'], case['name'], [mask],
                                       case['minimum'], case['min_area'], case['capacity'],
                                       case['x_width'], case['y_width'], case['area_width'], False)
        opt, om, oc = compile_and_run(output / case['name'], case['name'], [mask],
                                      case['minimum'], case['min_area'], case['capacity'],
                                      case['x_width'], case['y_width'], case['area_width'], True)
        gold, reference = gold_candidates(mask, case['minimum'], case['capacity'], case['min_area'])
        actual_base, actual_opt = objects(base), objects(opt)
        key = (case['config'], case['branch'], case['frame_id'])
        saved = scan_rows[key]
        exact_scan = (bm[0]['scan_state_cycles'] == int(saved['full_scan_state_visits']) and
                      om[0]['scan_state_cycles'] == int(saved['limited_scan_state_visits']) and
                      reference['full_scan_state_visits'] == int(saved['full_scan_state_visits']) and
                      reference['limited_scan_state_visits'] == int(saved['limited_scan_state_visits']))
        if base != opt or actual_base != gold or actual_opt != gold or not exact_scan:
            raise AssertionError(f"candidate/scan mismatch: {case['name']}")
        if bm[0]['object_count'] != len(gold) or om[0]['object_count'] != len(gold):
            raise AssertionError(f"object count mismatch: {case['name']}")
        records.append({**{k: v for k, v in case.items() if k != 'path'},
                        'kind': 'real_formal_candidate', 'gold': gold,
                        'baseline_objects': actual_base, 'optimized_objects': actual_opt,
                        'baseline_metrics': bm, 'optimized_metrics': om})
        alignment.append({'config': case['config'], 'branch': case['branch'],
                          'frame_id': case['frame_id'], 'mask_sha256': case['mask_sha256'],
                          'capacity': case['capacity'], 'min_run': case['minimum'],
                          'min_area': case['min_area'], 'qualified_top4_count': len(gold),
                          'count_boundary': 'min(4, qualifying_components)',
                          'reference_full': reference['full_scan_state_visits'],
                          'rtl_baseline': bm[0]['scan_state_cycles'],
                          'reference_limited': reference['limited_scan_state_visits'],
                          'rtl_optimized': om[0]['scan_state_cycles'], 'exact': exact_scan})
        commands += [bc, oc]
        print(f"PASS candidate {case['name']}", flush=True)

    for case in threshold_cases():
        args = (output / case['name'], case['name'], [case['mask']], case['minimum'],
                case['min_area'], case['capacity'], case['x_width'], case['y_width'],
                case['area_width'])
        base, bm, bc = compile_and_run(*args, False)
        opt, om, oc = compile_and_run(*args, True)
        gold, _ = gold_candidates(case['mask'], case['minimum'], case['capacity'], case['min_area'])
        if base != opt or objects(base) != gold or [item['area'] for item in gold] != case['expected_areas']:
            raise AssertionError(f"threshold mismatch: {case['name']}")
        records.append({'name': case['name'], 'kind': 'threshold', 'min_area': case['min_area'],
                        'expected_areas': case['expected_areas'], 'gold': gold,
                        'baseline_metrics': bm, 'optimized_metrics': om})
        commands += [bc, oc]
        print(f"PASS threshold {case['name']}", flush=True)

    for case in boundary_cases():
        args = (output / case['name'], case['name'], case['masks'], case['minimum'],
                case['min_area'], case['capacity'], case['x_width'], case['y_width'],
                case['area_width'])
        base, bm, bc = compile_and_run(*args, False)
        opt, om, oc = compile_and_run(*args, True)
        if base != opt:
            raise AssertionError(f"boundary baseline/optimized mismatch: {case['name']}")
        expected_error = 'label_overflow' if case['kind'] == 'label' else 'run_overflow'
        if bm[0]['ccl_error'] or not bm[1][expected_error] or not bm[1]['ccl_error']:
            raise AssertionError(f"missing boundary transition: {case['name']}")
        if bm[2]['ccl_error'] or bm[2]['object_count'] or bm[3]['ccl_error'] or bm[3]['object_count'] != 1:
            raise AssertionError(f"overflow recovery failed: {case['name']}")
        records.append({'name': case['name'], 'kind': case['kind'],
                        'capacity': case['capacity'], 'label_width': case['capacity'].bit_length(),
                        'baseline_metrics': bm, 'optimized_metrics': om,
                        'failed_frame_object_events_are_diagnostic_only': bm[1]['object_events']})
        commands += [bc, oc]
        print(f"PASS boundary {case['name']}", flush=True)

    bank = bank_model_check()
    if protected_hashes() != protected:
        raise AssertionError('protected production source or frozen file changed')

    dump(output / 'cases.json', records)
    with (output / 'same_frame_alignment.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(alignment[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(alignment)
    dump(output / 'line_bank_model.json', bank)

    runtime = output / 'runtime_sources'
    runtime.mkdir()
    sources = [Path(__file__), prior.TB, prior.BASE_ROW, prior.OPT_ROW, *prior.COMMON_RTL]
    for source in sources:
        shutil.copy2(source, runtime / source.name)

    full_peak = max((row for row in scan_rows.values()
                     if row['config'] == 'ddr640' and row['branch'] == 'keep_all'),
                    key=lambda row: int(row['full_scan_state_visits']))
    measured_1040 = scan_rows[('ddr640', 'keep_all', 1040)]
    lines = [
        '# CCL 候选门槛与容量边界验证', '',
        '- 旧批 8 个 `MIN_AREA=1` 分区证据保持原样；本批引用其收据，不覆盖旧目录。',
        '- 同一 8 个 Mask 使用正式面积门槛（256 为16，640为100）时，基线/优化候选顺序、数量、面积和框逐项等于 Python 整数参考。',
        '- `area == MIN_AREA` 被接纳；低一面积被排除。对象计数按 `min(4, 合格组件数)`。',
        '- L=128/192 均验证恰好 L 成功、L+1 失败；MAX_RUN=64成功、65失败；失败后的空帧与正常帧恢复。',
        '- 失败帧的对象事件只作为局部诊断，不是成功结果。生产发布保护本批未实现。', '',
        '| 用例 | 帧号 | 容量/run/area | 候选数 | 扫描周期 基线→优化 |',
        '|---|---:|---|---:|---:|',
    ]
    for case, row in zip(selected_real_cases(), alignment):
        lines.append(f"| {case['name']} | {case['frame_id']} | {case['capacity']}/{case['minimum']}/{case['min_area']} | "
                     f"{row['qualified_top4_count']} | {row['rtl_baseline']}→{row['rtl_optimized']} |")
    lines += [
        '',
        f"640/keep_all 的全窗口 `full_scan_state_visits` 最大值属于 frame {full_peak['frame_id']}（{full_peak['full_scan_state_visits']}）；旧 RTL 有限批选择的 frame 1040 为累计标签峰值帧，其值是 {measured_1040['full_scan_state_visits']}。两者选择条件不同。",
        '',
        '双行银行仅完成 Python 合同行为检查：银行交替、双满拒绝、合法空拍、末行、取消后排空并丢弃残余均通过；这不是生产 RTL 行缓存已经接入的证据。',
        '',
        '边界：没有修改生产 RTL、隔离 row_matcher 或旧验证文件；没有验证 DDR、CDC、任务发布保护、综合、资源、时序或整机准确率。',
    ]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    receipt = {
        'status': 'PASS_bounded_candidate_and_capacity_trial',
        'case_count': len(records), 'real_formal_candidate_cases': len(alignment),
        'prior_min_area_1_receipt_sha256': digest(PRIOR / 'receipt.json'),
        'prior_min_area_1_cases_sha256': digest(PRIOR / 'cases.json'),
        'source_hashes': {str(path.relative_to(PROJECT)).replace('\\', '/'): digest(path)
                          for path in sources},
        'artifact_hashes': {name: digest(output / name) for name in
                            ('cases.json', 'same_frame_alignment.csv',
                             'line_bank_model.json', 'report.md')},
        'commands': commands, 'protected_sources_unchanged': protected,
        'boundaries': ['bounded saved masks and deterministic synthetic masks',
                       'failed frame object events are diagnostic only',
                       'Python bank model is not RTL integration',
                       'no DDR/CDC/publish guard/synthesis/timing/accuracy claim'],
    }
    dump(output / 'receipt.json', receipt)
    return {'status': receipt['status'], 'cases': len(records), 'output': str(output)}


def self_check() -> dict:
    mask = threshold_cases()[0]['mask']
    gold, result = gold_candidates(mask, 2, 128, 16)
    assert [item['area'] for item in gold] == [17, 16]
    assert result['status'] == 'success'
    for capacity in (128, 192):
        exact = scan_reference(separated_births(capacity, False), capacity,
                               capacity.bit_length())
        over = scan_reference(separated_births(capacity, True), capacity,
                              capacity.bit_length())
        assert exact['status'] == 'success' and exact['labels_allocated'] == capacity
        assert over['status'] == 'failure' and over['first_failure']['reason'] == 'label_capacity'
        assert over['labels_allocated'] == capacity + 1
    assert bank_model_check()['same_mask_legal_gap_equal']
    return {'status': 'PASS', 'python_boundaries': 'PASS'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),
                     ensure_ascii=False, indent=2))
