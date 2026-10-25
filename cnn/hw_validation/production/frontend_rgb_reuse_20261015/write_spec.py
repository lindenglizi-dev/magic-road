"""Publish the unchanged ports and exact S1 channel/boundary behavior."""
import json
import sys
import run


def main():
    run.check()
    work = run.fresh('specifications')
    data = json.loads((run.BASE / 'specifications/road_stem_ddr_sequence.json').read_text(encoding='utf-8'))
    module = data['modules'][0]
    module['feature'] = 'frontend_rgb_reuse'
    module['description'] = '完整前三层RGB同像素缓存地址复用；核和DDR接口保持。'
    module['behavior'] += [
        'RGB非padding、channel<2、cache有效且tag匹配、lane<15时，core_load握手后lane+1并留HALO_BYTE。',
        'lane15、padding或cache无效回原MAP→ROW→ADDRESS→CACHE；末B通道换像素仍回原路径。',
        '反压不推进lane/channel/halo索引；整个DDR/CNN共同复位，重新装满1024项表。',
        'W响应只表示原mailbox接受AW/W，不是存储可见或提交保证。']
    module['verification_cases'] += ['原八例同向量，lane14/15跨词，RGB通道编号，真实子核装载长反压']
    module['timing_diagrams'] = [{'id': 'rgb_boundary', 'title': 'R14/G15直达与B跨词回退',
        'scenario': 'rgb_word_boundary', 'description': '例示响应延迟仅为图示；真实READ_RESPONSE等待valid。',
        'wavejson': {'signal': [{'name': 'clk', 'wave': 'p..........'},
            {'name': 'state', 'wave': '===========', 'data': ['HALO_R', 'HALO_G', 'MAP_B', 'ROW_B', 'ADDR_B', 'CACHE_B', 'READ_B', 'WAIT_B', 'HALO_B', 'MAP_R', 'ROW_R']},
            {'name': 'lane', 'wave': '===..=.....', 'data': ['14', '15', '15', '0']},
            {'name': 'load_accept', 'wave': '1.0.....10.'},
            {'name': 'read_request', 'wave': '0.....10...'}]}},
        {'id': 'rgb_stall', 'title': '装载反压保持游标', 'scenario': 'rgb_load_stall',
         'description': 'ready为零期间同一HALO字节保持，接受后才换下一通道。',
         'wavejson': {'signal': [{'name': 'clk', 'wave': 'p.......'},
             {'name': 'load_valid', 'wave': '01......'}, {'name': 'load_ready', 'wave': '10...1..'},
             {'name': 'channel', 'wave': '=.....=.', 'data': ['R', 'G']},
             {'name': 'lane', 'wave': '=.....=.', 'data': ['14', '15']},
             {'name': 'data', 'wave': '=.....=.', 'data': ['R[x,y]', 'G[x,y]']} ]}}]
    path = work / 'road_stem_ddr_sequence.json'
    run.save(path, data)
    entry = f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', path,
                 '--source', run.ROOT / 'rtl/road_stem_ddr_sequence.v', '--out-dir', run.ROOT / 'rtl', '--no-state'],
                run.ROOT, str(work.relative_to(run.ROOT) / 'write_spec'))
    run.save(run.ROOT / 'codegen_plan.json', {'task_classes': ['modify', 'validate'],
        'requirements': 'requirements.txt', 'reference': 'reference_s1.py',
        'core_modified': False, 'ports_modified': False, 'physical_started': False,
        'gates': ['compile', 'ast', 'readability', 'comment', 'naming', 'profile', 'testbench', 'toolchain']})
    run.check()


if __name__ == '__main__':
    main()
