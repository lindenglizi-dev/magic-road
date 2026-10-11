"""Bounded real-cache/guard/CCL/consumer integration; preserve every run."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from ddr_detection_capacity_probe import protected_hashes
from ddr_pipeline_reference import self_check

PROJECT = Path(__file__).resolve().parents[1]
EXPERIMENT = PROJECT / 'tests/experimental_ddr_ccl'
RTL = PROJECT / 'user_source/hdl_source/road_vision'
IVERILOG = PROJECT.parents[1] / '.tools/iverilog/bin/iverilog.exe'
VVP = IVERILOG.with_name('vvp.exe')
COMMON = [RTL / n for n in ('run_detector.v', 'labeled_run_table.v', 'label_manager.v',
                            'feature_table.v', 'frame_resolver.v', 'top4_selector.v',
                            'object_frame_store.v')]
NEW = [EXPERIMENT / n for n in ('ccl_pixel_line_banks.v', 'ccl_task_guard.v',
                               'ccl_raw_run_table.v', 'ccl_rle_stream_core.v',
                               'ccl_pipeline_trial_top.v')]
EXPECTED = {p.stem for p in COMMON + NEW} | {'row_matcher'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(paths, expected):
    if not paths:
        raise ValueError('empty input is not a passed check')
    names = set()
    for path in paths:
        names.update(re.findall(r'^\s*module\s+(\w+)', path.read_text(encoding='utf-8'), re.M))
    if not expected <= names:
        raise ValueError(f'missing expected modules: {sorted(expected - names)}')
    return sorted(names)


def command(arguments, directory, name):
    result = subprocess.run([str(a) for a in arguments], cwd=PROJECT,
                            capture_output=True, text=True, timeout=60)
    (directory / (name + '.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'{name} failed: {result.stdout}{result.stderr}')
    return {'argv': [str(a) for a in arguments], 'exit_code': result.returncode}


def run(output):
    allowed = PROJECT / 'evaluation/ddr_architecture'
    output = output.resolve()
    if output.exists() or not output.is_relative_to(allowed.resolve()):
        raise ValueError('use a fresh directory within evaluation/ddr_architecture')
    output.mkdir(parents=True)
    before = protected_hashes()
    reference = self_check()
    try:
        inventory([], EXPECTED)
    except ValueError:
        pass
    else:
        raise AssertionError('empty inventory passed')
    try:
        inventory(NEW, {'missing_module'})
    except ValueError:
        pass
    else:
        raise AssertionError('missing module passed')
    records = []
    all_sources = set(COMMON + NEW + [Path(__file__).resolve(), PROJECT / 'tools/ddr_pipeline_reference.py',
                                    PROJECT / 'tests/tb_ddr_pipeline.v'])
    for variant in ('baseline', 'optimized'):
        row = (RTL if variant == 'baseline' else EXPERIMENT) / 'row_matcher.v'
        sources = COMMON + NEW + [row]
        all_sources.add(row)
        directory = output / variant
        directory.mkdir()
        modules = inventory(sources, EXPECTED)
        design = directory / 'design.vvp'
        commands = [command([IVERILOG, '-g2001', '-Wall', '-s', 'ccl_pipeline_trial_top',
                             '-o', design, *sources], directory, 'design_compile')]
        actual = set(re.findall(r'\.scope module, "[^"]+" "([^"]+)"',
                                design.read_text(encoding='utf-8')))
        if not EXPECTED <= actual:
            raise AssertionError(f'elaborated modules absent: {EXPECTED - actual}')
        simulation = directory / 'simulation.vvp'
        commands.append(command([IVERILOG, '-g2012', '-Wall', '-s', 'tb_ddr_pipeline',
                                 '-o', simulation, PROJECT / 'tests/tb_ddr_pipeline.v', *sources],
                                directory, 'test_compile'))
        commands.append(command([VVP, simulation], directory, 'simulation'))
        log = (directory / 'simulation.log').read_text(encoding='utf-8')
        match = re.search(r'PASS pipeline checks=(\d+) tasks=(\d+) terminals=(\d+) resets=(\d+) eof=(\d+)', log)
        if not match:
            raise AssertionError('no integration PASS record')
        checks, tasks, terminals, resets, eof = map(int, match.groups())
        assert tasks == terminals == 11 and resets == 3 and eof == 8
        records.append({'variant': variant, 'checks': checks, 'tasks': tasks,
                        'terminals': terminals, 'controlled_resets': resets, 'eof': eof,
                        'input_modules': modules, 'elaborated_modules': sorted(actual),
                        'top': 'tb_ddr_pipeline', 'parameters': {'WIDTH':17,'HEIGHT':4,'MAX_LABEL':32},
                        'commands': commands})
    assert protected_hashes() == before
    all_sources.update(path.with_name(path.stem + '_spec.md') for path in NEW
                       if path.with_name(path.stem + '_spec.md').exists())
    all_sources.add(PROJECT / 'tests/tb_ddr_pipeline_spec.md')
    for path in all_sources:
        target = output / 'runtime_sources' / path.relative_to(PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    report = ['# 真实行缓存、guard、CCL与表读取组合验证', '',
              '输入为确定性17×4二值帧，结果消费者使用同步请求、返回背压及释放握手。', '',
              '| 核心 | 检查次数 | 接受任务 | 终态ACK | 受控核心复位 | EOF |',
              '|---|---:|---:|---:|---:|---:|']
    for r in records:
        report.append(f"| {r['variant']} | {r['checks']} | {r['tasks']} | {r['terminals']} | {r['controlled_resets']} | {r['eof']} |")
    report += ['', '覆盖：延迟读表、最后返回背压与提前释放拒绝、全部候选正常拒识、部分后级失败、双银行占用取消、半行协议错误受控复位、最后RAM返回与取消同拍、旧任务事件隔离和恢复。',
               '', '硬件行交接使用显式ready/commit和完成行计数，没有固定EOL等待拍数或功能层级访问。',
               '', '未接DDR、摄像头、分类器或显示；processed输入与显示ACK由受控消费者模拟，不是完整识别或显示实现。输入握手无DDR在途读取，预留预算仍待DDR适配。',
               'Icarus真实解析/展开为非空；完整技能静态门禁独立报告，未以此功能通过替代。']
    (output/'report.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    receipt = {'status':'PASS_bounded_isolated_pipeline','reference':reference,'runs':records,
               'source_hashes':{p.relative_to(PROJECT).as_posix():digest(p) for p in sorted(all_sources)},
               'protected_sources_unchanged':before,'tools':{'iverilog':digest(IVERILOG),'vvp':digest(VVP)},
               'strict_static_gate':'not_passed_by_this_functional_runner'}
    (output/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':receipt['status'],'runs':[{k:r[k] for k in ('variant','checks','tasks','terminals')} for r in records]},indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'evaluation/ddr_architecture/pipeline_20261002_v1')
    run(parser.parse_args().output)
