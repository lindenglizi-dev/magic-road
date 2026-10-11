#!/usr/bin/env python3
"""Run the isolated raw-run bank handoff Icarus trial."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from ddr_detection_capacity_probe import protected_hashes


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/raw_handoff_20261002_v1'
IVERILOG = PROJECT.parents[1] / '.tools/iverilog/bin/iverilog.exe'
VVP = PROJECT.parents[1] / '.tools/iverilog/bin/vvp.exe'
TB = PROJECT / 'tests/tb_ddr_raw_handoff.v'
TB_SPEC = PROJECT / 'tests/tb_ddr_raw_handoff_spec.md'
RAW = PROJECT / 'tests/experimental_ddr_ccl/ccl_raw_run_table.v'
RAW_SPEC = PROJECT / 'tests/experimental_ddr_ccl/ccl_raw_run_table_spec.md'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8')


def run(output: Path) -> dict:
    allowed = (PROJECT / 'evaluation/ddr_architecture').resolve()
    if output.exists() or not output.resolve().is_relative_to(allowed):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    sources = [Path(__file__), TB, TB_SPEC, RAW, RAW_SPEC]
    for path in [IVERILOG, VVP, *sources]:
        if not path.exists():
            raise FileNotFoundError(path)

    protected_before = protected_hashes()
    raw_before = digest(RAW)
    output.mkdir(parents=True)
    image = output / 'simulation.vvp'
    compile_command = [str(IVERILOG), '-g2012', '-Wall', '-s',
                       'tb_ddr_raw_handoff', '-o', str(image), str(TB), str(RAW)]
    compiled = subprocess.run(compile_command, cwd=PROJECT, text=True,
                              capture_output=True, timeout=120)
    compile_log = compiled.stdout + compiled.stderr
    (output / 'compile.log').write_text(compile_log, encoding='utf-8')
    if compiled.returncode:
        raise RuntimeError(f'Icarus compile failed:\n{compile_log}')

    run_command = [str(VVP), str(image)]
    simulated = subprocess.run(run_command, cwd=PROJECT, text=True,
                               capture_output=True, timeout=120)
    simulation_log = simulated.stdout + simulated.stderr
    (output / 'simulation.log').write_text(simulation_log, encoding='utf-8')
    if simulated.returncode:
        raise RuntimeError(f'Icarus simulation failed:\n{simulation_log}')
    match = re.search(
        r'PASS raw handoff checks=(\d+) handoffs=(\d+) illegal=(\d+) reads=(\d+)',
        simulation_log,
    )
    if not match or tuple(map(int, match.groups())) != (50, 2, 2, 10):
        raise AssertionError('raw handoff accounting changed')

    protected_after = protected_hashes()
    if protected_after != protected_before:
        raise AssertionError('protected production source or frozen file changed')
    if digest(RAW) != raw_before:
        raise AssertionError('ccl_raw_run_table changed during read-only trial')

    runtime = output / 'runtime_sources'
    runtime.mkdir()
    for path in sources:
        shutil.copy2(path, runtime / path.name)

    boundaries = [
        'Isolated ccl_raw_run_table with MAX_RUN=64; no functional RTL edit.',
        'Single clock and synthetic run coordinates; no DDR or CDC model.',
        'run_valid plus row_end is flagged but temporarily stored by existing RTL; supervisory error discard is required.',
        'No synthesis, RAM inference, timing, complete CCL throughput or production integration evidence.',
    ]
    result = {
        'status': 'PASS_bounded_local_simulation',
        'checks': int(match.group(1)),
        'same_cycle_handoffs': int(match.group(2)),
        'illegal_events': int(match.group(3)),
        'synchronous_reads': int(match.group(4)),
        'compile_warnings': compile_log.lower().count('warning:'),
        'raw_source_unchanged': raw_before,
        'protected_sources_unchanged': True,
        'boundaries': boundaries,
    }
    dump(output / 'report.json', result)
    lines = [
        '# 原始 run 银行同拍交接验证', '',
        '- A 释放、B 完成与 B 释放、A 完成两种同拍交换均通过。',
        '- 10 次同步读取逐项匹配独立的 y、run 数量、坐标和顺序。',
        '- 双银行 full 后的额外 run 置位 raw_overrun/protocol_error，未破坏已提交银行；释放和 frame_clear 后恢复。',
        '- run_valid 与 row_end 同拍被判非法；该暂存行未计入正常交接并由 frame_clear 丢弃。',
        f"- Icarus 检查 {result['checks']} 项，编译警告 {result['compile_warnings']} 条。",
        '- 隔离 raw 表源码与生产保护文件在试验前后哈希一致。', '',
        '证据边界：', '',
        *[f'- {text}' for text in boundaries],
    ]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    receipt = {
        'command': [sys.executable, *sys.argv],
        'python': sys.version,
        'tools': {'iverilog_sha256': digest(IVERILOG), 'vvp_sha256': digest(VVP)},
        'compile_command': compile_command,
        'run_command': run_command,
        'source_hashes': {path.relative_to(PROJECT).as_posix(): digest(path)
                          for path in sources},
        'protected_source_hashes': protected_after,
        'raw_source_unchanged': raw_before,
    }
    receipt['artifact_hashes'] = {
        path.relative_to(output).as_posix(): digest(path)
        for path in sorted(output.rglob('*')) if path.is_file() and path.name != 'receipt.json'
    }
    dump(output / 'receipt.json', receipt)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
