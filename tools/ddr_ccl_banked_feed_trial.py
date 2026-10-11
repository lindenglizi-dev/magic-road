#!/usr/bin/env python3
"""Bounded two-line-bank feeder trial against the real CCL core."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import ddr_ccl_rtl_trial as prior
from candidate_chain_reference import digest
from ddr_ccl_candidate_boundary_trial import gold_candidates, objects
from ddr_detection_capacity_probe import protected_hashes
from local_paired_diagnostic import dump


PROJECT = Path(__file__).resolve().parents[1]
TB = PROJECT / 'tests/tb_ddr_ccl_banked_feed.v'
SPEC = PROJECT / 'tests/tb_ddr_ccl_banked_feed_spec.md'
OUTPUT = PROJECT / 'evaluation/ddr_architecture/banked_feed_20261001_v1'


def stress_mask(height: int = 8) -> np.ndarray:
    mask = np.zeros((height, 129), np.uint8)
    mask[:, 0:127:2] = 1
    return mask


def parse_bank(path: Path) -> dict:
    rows = list(csv.reader(path.open(encoding='utf-8', newline='')))
    summary = next(row for row in rows if row[0] == 'BANK_SUMMARY')
    fills = [(int(row[1]), int(row[2])) for row in rows if row[0] == 'BANK_FILL']
    sends = [(int(row[1]), int(row[2])) for row in rows if row[0] == 'BANK_SEND_START']
    full, stall_starts_both_full = set(), True
    for row in rows:
        if row[0] == 'BANK_FILL':
            full.add(int(row[2]))
        elif row[0] == 'BANK_SEND_END':
            full.remove(int(row[2]))
        elif row[0] == 'PRODUCER_STALL_START':
            stall_starts_both_full &= full == {0, 1}
    values = list(map(int, summary[1:]))
    return {
        'fill_count': values[0], 'send_count': values[1],
        'producer_stall_cycles': values[2], 'producer_stall_episodes': values[3],
        'core_wait_cycles': values[4], 'row_done_count': values[5],
        'fill_alternation_errors': values[6], 'send_alternation_errors': values[7],
        'fills': fills, 'sends': sends,
        'stall_starts_both_full': stall_starts_both_full,
    }


def compile_and_run(run_dir: Path, mask: np.ndarray, optimized: bool,
                    pixel_gap: int) -> tuple[list[list[str]], list[dict], dict, list[str]]:
    run_dir.mkdir(parents=True)
    mem, log, image = run_dir / 'mask.mem', run_dir / 'events.csv', run_dir / 'simulation.vvp'
    prior.write_mem(mem, [mask])
    height, width = mask.shape
    params = {
        'FRAME_WIDTH': width, 'FRAME_HEIGHT': height,
        'X_WIDTH': (width-1).bit_length(), 'Y_WIDTH': max(1, (height-1).bit_length()),
        'LABEL_WIDTH': 8, 'AREA_WIDTH': 16,
        'MAX_RUN': 64, 'MAX_LABEL': 128, 'MIN_AREA': 1,
        'MIN_RUN_LENGTH': 1, 'PIXEL_GAP': pixel_gap, 'EOL_FLUSH_CYCLES': 4,
    }
    command = [str(prior.IVERILOG), '-g2012', '-Wall', '-s', 'tb_ddr_ccl_banked_feed']
    command += [f'-Ptb_ddr_ccl_banked_feed.{key}={value}' for key, value in params.items()]
    command += ['-o', str(image), str(TB),
                str(prior.OPT_ROW if optimized else prior.BASE_ROW)]
    command += [str(path) for path in prior.COMMON_RTL]
    compiled = subprocess.run(command, cwd=PROJECT, text=True,
                              capture_output=True, timeout=120)
    (run_dir / 'compile.log').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
    if compiled.returncode:
        raise RuntimeError(f'compile failed:\n{compiled.stdout}{compiled.stderr}')
    run_command = [str(prior.VVP), str(image), f'+MASK={mem}', f'+LOG={log}']
    ran = subprocess.run(run_command, cwd=PROJECT, text=True,
                         capture_output=True, timeout=600)
    (run_dir / 'simulation.log').write_text(ran.stdout + ran.stderr, encoding='utf-8')
    if ran.returncode:
        raise RuntimeError(f'run failed:\n{ran.stdout}{ran.stderr}')
    semantic, metrics = prior.parse_log(log)
    if len(metrics) != 1:
        raise AssertionError('missing DONE record')
    return semantic, metrics, parse_bank(log), command + ['RUN:'] + run_command


def validate_run(name: str, semantic: list[list[str]], metrics: list[dict],
                 bank: dict, mask: np.ndarray, gold: list[dict]) -> dict:
    height = mask.shape[0]
    metric = metrics[0]
    if metric['ccl_error'] or metric['run_overflow'] or metric['label_overflow']:
        raise AssertionError(f'{name}: unexpected CCL error')
    if objects(semantic) != gold:
        raise AssertionError(f'{name}: candidate mismatch')
    if prior.log_features(semantic, 0) != prior.gold_features(mask, 128, 8):
        raise AssertionError(f'{name}: final partition/features mismatch')
    event_rows = [row for row in semantic if row[0] in ('FEATURE', 'UNION')]
    if event_rows != prior.gold_events(mask, 128, 8):
        raise AssertionError(f'{name}: event order mismatch')
    expected = [(row, row & 1) for row in range(height)]
    if bank['fills'] != expected or bank['sends'] != expected:
        raise AssertionError(f'{name}: bank order/alternation mismatch')
    if (bank['fill_count'] != height or bank['send_count'] != height or
            bank['row_done_count'] != height or
            bank['fill_alternation_errors'] or bank['send_alternation_errors']):
        raise AssertionError(f'{name}: bank summary mismatch')
    if bank['producer_stall_cycles'] <= 0 or bank['producer_stall_episodes'] <= 0:
        raise AssertionError(f'{name}: pressure did not stop producer')
    if not bank['stall_starts_both_full']:
        raise AssertionError(f'{name}: producer stalled without both banks full')
    return {'name': name, 'metrics': metric, 'bank': bank,
            'objects': objects(semantic)}


def run(output: Path) -> dict:
    root = (PROJECT / 'evaluation/ddr_architecture').resolve()
    if output.exists() or not output.resolve().is_relative_to(root):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    for path in [TB, SPEC, prior.IVERILOG, prior.VVP, prior.BASE_ROW,
                 prior.OPT_ROW, *prior.COMMON_RTL]:
        if not path.exists():
            raise FileNotFoundError(path)
    protected = protected_hashes()
    output.mkdir(parents=True)
    mask = stress_mask()
    gold, reference = gold_candidates(mask, 1, 128, 1)
    if reference['status'] != 'success' or len(gold) != 4:
        raise AssertionError('invalid pressure reference')

    records, commands, semantic_by_name = [], [], {}
    for optimized in (False, True):
        variant = 'optimized' if optimized else 'baseline'
        for gap in (0, 1):
            name = f'{variant}_gap{gap}'
            semantic, metrics, bank, command = compile_and_run(
                output / name, mask, optimized, gap)
            records.append(validate_run(name, semantic, metrics, bank, mask, gold))
            semantic_by_name[name] = semantic
            commands.append(command)
            print(f"PASS {name} stalls={bank['producer_stall_cycles']} "
                  f"core_wait={bank['core_wait_cycles']}", flush=True)

    reference_semantic = semantic_by_name['baseline_gap0']
    if any(rows != reference_semantic for rows in semantic_by_name.values()):
        raise AssertionError('gap or scan optimization changed CCL semantics')
    if protected_hashes() != protected:
        raise AssertionError('protected production source or frozen file changed')

    dump(output / 'cases.json', records)
    runtime = output / 'runtime_sources'
    runtime.mkdir()
    sources = [Path(__file__), TB, SPEC, prior.BASE_ROW, prior.OPT_ROW, *prior.COMMON_RTL]
    for source in sources:
        name = ('row_matcher_optimized.v' if source == prior.OPT_ROW else
                'row_matcher_baseline.v' if source == prior.BASE_ROW else source.name)
        shutil.copy2(source, runtime / name)
    lines = [
        '# CCL 双行银行供数行为验证', '',
        '- 一个确定性压力 Mask：129×8，每行64个 run；不构成完整真实视频批次。',
        '- 测试台生产者使用两个像素行银行。两银行满时停止接受新行；消费者仅在 CCL 原始 run 写银行空闲时启动下一行。',
        '- 基线/扫描优化与 `PIXEL_GAP=0/1` 四组逐事件日志、最终 feature 分区和正式候选均相同并等于 Python 整数参考。', '',
        '| 运行 | 生产停顿周期/次数 | 等待CCL写银行周期 | 总周期 | 扫描周期 |',
        '|---|---:|---:|---:|---:|',
    ]
    for record in records:
        bank, metric = record['bank'], record['metrics']
        lines.append(f"| {record['name']} | {bank['producer_stall_cycles']}/{bank['producer_stall_episodes']} | "
                     f"{bank['core_wait_cycles']} | {metric['total_cycles']} | {metric['scan_state_cycles']} |")
    lines += [
        '',
        '证据边界：这是测试台行银行喂入真实 CCL 的行为仿真，不是已综合行缓存或真实 DDR/CDC 供数。取消缓冲残余仍只有 Python 合同证据，本批没有构造新的 RTL 取消管线。',
    ]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    receipt = {
        'status': 'PASS_bounded_banked_feed_simulation',
        'input': {'shape': list(mask.shape), 'sha256': digest_bytes(mask.tobytes()),
                  'runs_per_row': 64, 'capacity': 128, 'min_run': 1, 'min_area': 1},
        'case_count': len(records),
        'source_hashes': {str(path.relative_to(PROJECT)).replace('\\', '/'): digest(path)
                          for path in sources},
        'artifact_hashes': {'cases.json': digest(output / 'cases.json'),
                            'report.md': digest(output / 'report.md')},
        'commands': commands, 'protected_sources_unchanged': protected,
        'boundaries': ['one deterministic pressure mask',
                       'testbench two-line bank, not synthesized input cache',
                       'no real DDR/CDC', 'RTL cancellation path not implemented',
                       'no synthesis/resource/timing/accuracy claim'],
    }
    dump(output / 'receipt.json', receipt)
    return {'status': receipt['status'], 'cases': len(records), 'output': str(output)}


def digest_bytes(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def self_check() -> dict:
    mask = stress_mask(3)
    assert mask.shape == (3, 129)
    assert all(sum(1 for x in range(129) if mask[y, x] and
                   (x == 0 or not mask[y, x-1])) == 64 for y in range(3))
    root = Path(tempfile.mkdtemp(prefix='ddr_ccl_banked_feed_'))
    semantic, metrics, bank, _ = compile_and_run(root / 'case', mask, False, 0)
    gold, _ = gold_candidates(mask, 1, 128, 1)
    validate_run('self_check', semantic, metrics, bank, mask, gold)
    return {'status': 'PASS', 'preserved_run_directory': str(root)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else run(args.output),
                     ensure_ascii=False, indent=2))
