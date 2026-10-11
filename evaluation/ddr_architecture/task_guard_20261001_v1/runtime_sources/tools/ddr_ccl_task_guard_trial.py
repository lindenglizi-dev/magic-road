#!/usr/bin/env python3
"""Run the bounded task-guard mock and production-CCL Icarus checks."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from ddr_ccl_task_guard_reference import self_check as reference_self_check
from ddr_detection_capacity_probe import protected_hashes


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/task_guard_20261001_v1'
IVERILOG = PROJECT.parents[1] / '.tools/iverilog/bin/iverilog.exe'
VVP = PROJECT.parents[1] / '.tools/iverilog/bin/vvp.exe'
TB = PROJECT / 'tests/tb_ddr_ccl_task_guard.v'
GUARD = PROJECT / 'tests/experimental_ddr_ccl/ccl_task_guard.v'
STORE = PROJECT / 'user_source/hdl_source/road_vision/object_frame_store.v'
BASE_ROW = PROJECT / 'user_source/hdl_source/road_vision/row_matcher.v'
OPT_ROW = PROJECT / 'tests/experimental_ddr_ccl/row_matcher.v'
RTL = PROJECT / 'user_source/hdl_source/road_vision'
COMMON_CCL = [RTL / name for name in (
    'rle_ccl_top.v', 'run_detector.v', 'raw_run_table.v',
    'labeled_run_table.v', 'label_manager.v', 'feature_table.v',
    'frame_resolver.v', 'top4_selector.v')]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(name: str, top: str, sources: list[Path], output: Path) -> dict:
    run_dir = output / name
    run_dir.mkdir(parents=True)
    image = run_dir / 'simulation.vvp'
    compile_command = [str(IVERILOG), '-g2012', '-Wall', '-s', top,
                       '-o', str(image), *(str(path) for path in sources)]
    compiled = subprocess.run(compile_command, cwd=PROJECT, text=True,
                              capture_output=True, timeout=120)
    compile_log = compiled.stdout + compiled.stderr
    (run_dir / 'compile.log').write_text(compile_log, encoding='utf-8')
    if compiled.returncode:
        raise RuntimeError(f'{name} compile failed:\n{compile_log}')
    run_command = [str(VVP), str(image)]
    ran = subprocess.run(run_command, cwd=PROJECT, text=True,
                         capture_output=True, timeout=120)
    simulation_log = ran.stdout + ran.stderr
    (run_dir / 'simulation.log').write_text(simulation_log, encoding='utf-8')
    if ran.returncode:
        raise RuntimeError(f'{name} simulation failed:\n{simulation_log}')
    match = re.search(
        r'PASS (?:mock|real) guard checks=(\d+) accepted=(\d+) terminal=(\d+)'
        r'(?: rejected=(\d+))?', simulation_log)
    if not match:
        raise AssertionError(f'{name}: missing PASS/accounting record')
    checks, accepted, terminal = (int(value) for value in match.groups()[:3])
    rejected = int(match.group(4) or 0)
    return {
        'name': name, 'checks': checks, 'accepted': accepted,
        'terminal': terminal, 'rejected': rejected,
        'compile_command': compile_command, 'run_command': run_command,
        'compile_warnings': compile_log.count('warning:'),
    }


def run(output: Path) -> dict:
    allowed = (PROJECT / 'evaluation/ddr_architecture').resolve()
    if output.exists() or not output.resolve().is_relative_to(allowed):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    sources = [Path(__file__), PROJECT / 'tools/ddr_ccl_task_guard_reference.py',
               TB, PROJECT / 'tests/tb_ddr_ccl_task_guard_spec.md', GUARD,
               PROJECT / 'tests/experimental_ddr_ccl/ccl_task_guard_spec.md',
               STORE, BASE_ROW, OPT_ROW, *COMMON_CCL]
    for path in [IVERILOG, VVP, *sources]:
        if not path.exists():
            raise FileNotFoundError(path)
    protected_before = protected_hashes()
    output.mkdir(parents=True)

    reference = reference_self_check()
    if reference['accepted'] != reference['terminal']:
        raise AssertionError('Python guard reference lost a terminal')
    mock = execute('mock', 'tb_ddr_ccl_task_guard', [TB, GUARD, STORE], output)
    baseline = execute('real_baseline', 'tb_ddr_ccl_task_guard_real',
                       [TB, GUARD, STORE, BASE_ROW, *COMMON_CCL], output)
    optimized = execute('real_optimized', 'tb_ddr_ccl_task_guard_real',
                        [TB, GUARD, STORE, OPT_ROW, *COMMON_CCL], output)
    if (mock['accepted'], mock['terminal']) != (13, 12):
        raise AssertionError('mock reset-boundary accounting changed')
    for result in (baseline, optimized):
        if (result['accepted'], result['terminal'], result['rejected']) != (4, 4, 4):
            raise AssertionError(f"{result['name']}: task conservation failed")
    if baseline['checks'] != optimized['checks']:
        raise AssertionError('baseline/optimized guard checks diverged')
    protected_after = protected_hashes()
    if protected_after != protected_before:
        raise AssertionError('protected production source or frozen file changed')

    results = [mock, baseline, optimized]
    report = [
        '# CCL 任务入口与发布保护本地验证', '',
        '- Python 合同自检：已接受任务与终态数量相等。',
        '- mock core：同拍错误、四对象、非法流、背压、取消排空及复位边界通过。',
        '- 生产 CCL：基线与扫描优化版均通过 exact32、exact33 溢出、空帧、正常恢复及忙时 B 隔离。',
        '- 失败任务发布明确失败终态，正式对象读取保持关闭；成功空任务与失败任务可区分。', '',
        '| 运行 | 检查数 | 已接受 | 已握手终态 | 被拒流事件 |',
        '|---|---:|---:|---:|---:|',
    ]
    for result in results:
        report.append(f"| {result['name']} | {result['checks']} | "
                      f"{result['accepted']} | {result['terminal']} | "
                      f"{result['rejected']} |")
    report += ['',
        'mock 的最后一个任务由复位划断，因此 13 次接受对应 12 次握手终态；复位前守恒断言已通过。',
        '',
        '边界：单时钟、单任务、外部 drain_done 被视为可信排空确认；未连接 DDR/CDC/显示，未综合、未布局布线，也不证明识别准确率或整机帧率。']
    (output / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    receipt = {
        'status': 'PASS_bounded_local_simulation',
        'python': sys.version,
        'reference': reference,
        'runs': results,
        'tools': {'iverilog_sha256': digest(IVERILOG), 'vvp_sha256': digest(VVP)},
        'source_hashes': {path.relative_to(PROJECT).as_posix(): digest(path)
                          for path in sources},
        'protected_sources_unchanged': protected_after,
        'boundaries': ['single clock and one task in flight',
                       'drain_done is an external trusted acknowledgement',
                       'synthetic masks only', 'no DDR/CDC/display',
                       'no synthesis, timing closure, or accuracy claim'],
    }
    (output / 'receipt.json').write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'status': receipt['status'], 'output': str(output),
            'mock_checks': mock['checks'], 'real_checks_each': baseline['checks']}


def self_check() -> dict:
    root = Path(tempfile.mkdtemp(prefix='ddr_guard_trial_'))
    reference = reference_self_check()
    mock = execute('mock', 'tb_ddr_ccl_task_guard', [TB, GUARD, STORE], root)
    assert reference['accepted'] == reference['terminal']
    assert mock['checks'] >= 140 and mock['accepted'] == mock['terminal'] + 1
    return {'status': 'PASS', 'reference': reference, 'mock': mock,
            'preserved_run_directory': str(root)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    print(json.dumps(self_check() if arguments.self_check else run(arguments.output),
                     ensure_ascii=False, indent=2))
