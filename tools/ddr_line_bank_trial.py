#!/usr/bin/env python3
"""Run the bounded Python and Icarus checks for the isolated line banks."""
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
from ddr_line_bank_reference import self_check


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT / 'evaluation/ddr_architecture/line_banks_20261001_v1'
IVERILOG = PROJECT.parents[1] / '.tools/iverilog/bin/iverilog.exe'
VVP = PROJECT.parents[1] / '.tools/iverilog/bin/vvp.exe'
RTL = PROJECT / 'tests/experimental_ddr_ccl/ccl_pixel_line_banks.v'
RTL_SPEC = PROJECT / 'tests/experimental_ddr_ccl/ccl_pixel_line_banks_spec.md'
TB = PROJECT / 'tests/tb_ddr_line_banks.v'
TB_SPEC = PROJECT / 'tests/tb_ddr_line_banks_spec.md'
REFERENCE = PROJECT / 'tools/ddr_line_bank_reference.py'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8')


def run(output: Path) -> dict:
    allowed = (PROJECT / 'evaluation/ddr_architecture').resolve()
    if output.exists() or not output.resolve().is_relative_to(allowed):
        raise ValueError('choose a fresh output inside evaluation/ddr_architecture')
    sources = [Path(__file__), REFERENCE, RTL, RTL_SPEC, TB, TB_SPEC]
    for path in [IVERILOG, VVP, *sources]:
        if not path.exists():
            raise FileNotFoundError(path)

    protected_before = protected_hashes()
    reference = self_check()
    output.mkdir(parents=True)
    image = output / 'simulation.vvp'
    compile_command = [str(IVERILOG), '-g2012', '-Wall', '-s',
                       'tb_ddr_line_banks', '-o', str(image), str(TB), str(RTL)]
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
    match = re.search(r'PASS line banks checks=(\d+)', simulation_log)
    if not match or int(match.group(1)) != 80:
        raise AssertionError('expected 80 line-bank checks')

    protected_after = protected_hashes()
    if protected_after != protected_before:
        raise AssertionError('protected production source or frozen file changed')

    runtime = output / 'runtime_sources'
    runtime.mkdir()
    for path in sources:
        shutil.copy2(path, runtime / path.name)

    boundaries = [
        'Single clock and two 129-pixel banks; testbench uses WIDTH=5.',
        'One-cycle synchronous read request plus held output register.',
        'No DDR controller, CDC, production top, CCL result, synthesis or timing evidence.',
        'Cancel is sampled as a level and new-task ownership remains a top-level duty.',
    ]
    report = {
        'status': 'PASS_bounded_local_simulation',
        'reference': reference,
        'icarus_checks': int(match.group(1)),
        'compile_warnings': compile_log.lower().count('warning:'),
        'protected_sources_unchanged': protected_after,
        'boundaries': boundaries,
    }
    dump(output / 'report.json', report)
    lines = [
        '# 双银行像素行缓存本地验证', '',
        '- Python 周期模型自检通过。',
        '- Icarus 共 80 项检查通过：背压、银行交替、双满停供、取消、错误和 tag 保留。',
        f"- 编译警告：{report['compile_warnings']}。",
        '- 生产 RTL、冻结配置和架构文档在试验前后哈希一致。', '',
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
        'protected_sources_unchanged': protected_after,
    }
    receipt['artifact_hashes'] = {
        path.relative_to(output).as_posix(): digest(path)
        for path in sorted(output.rglob('*')) if path.is_file() and path.name != 'receipt.json'
    }
    dump(output / 'receipt.json', receipt)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--self-check', action='store_true')
    args = parser.parse_args()
    result = self_check() if args.self_check else run(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
