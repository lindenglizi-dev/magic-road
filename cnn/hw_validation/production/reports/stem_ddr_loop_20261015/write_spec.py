"""生成真实端口规格和取数周期图，保留独立原接口契约。"""
import copy
import json
import sys
import run


def main():
    run.check()
    work = run.fresh('specifications')
    entry = f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
    original = json.loads((run.BASE.parent / 'stem_ddr_down2_four_20261014/specifications/road_stem_ddr_sequence.json').read_text(encoding='utf-8'))
    wave = [{'id': 'fetch_hold', 'title': '同步取数与命令完成推进', 'scenario': 'advance_hold',
        'description': 'FETCH沿返回当前命令；等待期间保持；ADVANCE只推进游标，下一FETCH才换返回。',
        'wavejson': {'signal': [{'name': 'clk', 'wave': 'p.......'}, {'name': 'fetch', 'wave': '010...10'},
            {'name': 'advance', 'wave': '0...10..'}, {'name': 'command', 'wave': 'x=....=.', 'data': ['wordN', 'wordN+1']},
            {'name': 'cursor', 'wave': '=....=..', 'data': ['N', 'N+1']}]}}]
    sequence = copy.deepcopy(original)
    sequence['modules'][0]['feature'] = 'frontend_loop'
    sequence['modules'][0]['behavior'].append('64位命令由有界循环加载器返回；与冻结6092条逐位一致，原FSM和所有案例周期保持。')
    sequence['modules'][0]['timing_diagrams'] = wave
    loader = copy.deepcopy(original)
    module = loader['modules'][0]
    module.update({'name': 'road_frontend_load_sequence', 'feature': 'frontend_loop',
        'rtl_path': 'road_frontend_load_sequence.v', 'description': '固定阶段与计数器产生原命令头，窄ROM保存数值。',
        'clock': {'domains': 'CNN100MHz'},
        'reset': {'assertion': '异步低有效复位清零阶段、计数和命令输出', 'release': '上游同步释放；重新从1024项装表开始'},
        'behavior': ['i_fetch上升沿锁存当前命令；i_advance上升沿推进一项；两者不得同拍。',
                     '输出在非FETCH期间保持，推进阶段不修改已经返回的命令。',
                     '固定十六个Stem tile和四个down2 tile；6092条命令顺序与原程序逐位一致。',
                     'RGB零扩展，参数32位原样；SiLU符号扩展；像素第九位保留padding kind。'],
        'corner_cases': ['阶段边界、ROM首末项、512拍停顿、参数中途复位、最终END保持'],
        'verification_cases': ['原程序逐字比较17704次、13例数值及故障周期一致、双时钟集成一致'],
        'timing_diagrams': wave})
    module['interfaces'] = {'ports': [{'name': name, 'direction': direction, 'width': width, 'role': desc, 'description': desc}
        for name, direction, width, desc in [('i_clk', 'input', 1, '100MHz计算时钟'), ('i_rstn', 'input', 1, '低有效异步复位'),
        ('i_fetch', 'input', 1, '锁存当前命令'), ('i_advance', 'input', 1, '已完成命令推进'), ('o_command', 'output', 64, '稳定命令返回')]]}
    for contract in (sequence, loader):
        name = contract['modules'][0]['name']
        path = work / f'{name}.json'
        run.save(path, contract)
        run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', path,
                     '--source', run.ROOT / 'rtl' / f'{name}.v', '--out-dir', run.ROOT / 'rtl', '--no-state'],
                    run.ROOT, str(work.relative_to(run.ROOT) / name))
    run.save(run.ROOT / 'codegen_plan.json', {'task_classes': ['modify', 'generate', 'validate'],
        'requirements': 'requirements.txt', 'python_model': 'reference.py', 'arithmetic_modified': False,
        'source_targets': ['rtl/road_frontend_load_sequence.v', 'rtl/road_stem_ddr_sequence.v'],
        'latency_change': 0, 'gates': ['compile', 'ast', 'readability', 'comment', 'naming', 'profile', 'testbench', 'toolchain'],
        'diagnostic_only_until_strict_closure': True})
    run.check()


if __name__ == '__main__':
    main()
