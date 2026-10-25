"""完整层的真实接口、宏命令顺序和DDR握手规格。"""
import json
import sys
import run


def main():
    root = run.ROOT
    work = run.fresh('specifications')
    entry = f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
    for source, name in [('road_stem_ddr_sequence', 'road_stem_ddr_sequence'),
                         ('road_frontend_load_sequence', 'road_frontend_layer_sequence'),
                         ('road_stem_ddr_sequence', 'road_stem_ddr_board_top')]:
        data = json.loads((run.BASE / 'specifications' / f'{source}.json').read_text(encoding='utf-8'))
        module = data['modules'][0]
        module.update({'name': name, 'feature': 'frontend_ddr_tensor', 'rtl_path': f'{name}.v',
            'description': '固定完整前三层宏调度与真实DDR读写，TEST_ONLY参数。',
            'behavior': ['10800个宏命令；2304 Stem块和576下采样块，真实输出写DDR再作为下一层输入。',
                '图像从48词周期图案写满DDR；算术激活必须来自DDR实读或定义的padding。',
                '单16B缓存每tile失效，命中省读；完整写/读/导出计数必须一致才PASS。',
                '计算与DDR共同复位；所有旧计数、缓存和valid取消，重新写输入并装满1024表。'],
            'corner_cases': ['顶左padding、右下末tile、行列进位、cache跨字节边界、请求背压、读延迟、复位与故障'],
            'verification_cases': ['全帧逐项数值与地址、真实中间值、正常及随机背压、共同复位、实际TD资源时序']})
        for port in module['interfaces']['ports']:
            if port['name'] in ('o_writes', 'o_reads', 'o_output_bytes'):
                port['width'] = 32
        if name == 'road_frontend_layer_sequence':
            module['behavior'] = ['FETCH沿返回稳定64位宏命令，ADVANCE沿才推进；停顿期间保持。',
                '1024表项、482首层参数、2304次HALO/START/EXPORT、选择、652下采样参数、576次HALO/START/EXPORT及END，共10800条。',
                'RGB宏命令opcode8，由外层执行完整halo读取；本模块只保存参数和SiLU表。',
                '复位清零阶段与局部计数，下一轮重新从表项零开始。']
        if name == 'road_stem_ddr_board_top':
            module['interfaces'] = {'ports': [{'name': n, 'direction': d, 'width': w, 'role': desc, 'description': desc}
                for n, d, w, desc in [('i_sys_clk', 'input', 1, 'C4板载50MHz'), ('i_rstn', 'input', 1, 'C7共同复位'),
                *[(f'o_tmds_{c}_p', 'output', 1, '原HDMI差分正端') for c in ('blue', 'green', 'red', 'clock')],
                *[(f'ddr_{n}', 'output', 1, '原厂DDR专用命令端') for n in ('ck_p', 'ck_n', 'cke', 'odt', 'cs_n', 'ras_n', 'cas_n', 'we_n')],
                ('ddr_ba', 'output', 2, 'DDR bank地址'), ('ddr_addr', 'output', 13, 'DDR行列地址'),
                ('ddr_dqs_p', 'inout', 2, 'DDR差分选通正端'), ('ddr_dqs_n', 'inout', 2, 'DDR差分选通负端'),
                ('ddr_dq', 'inout', 16, 'DDR数据'), ('ddr_dm', 'inout', 2, 'DDR掩码')]]}
            module['behavior'] = ['原PLL/DDR IP/HDMI和mailbox连接完整前三层序列器。',
                '诊断计数加宽32位；原状态字段显示低位，第二数据页显示完整写/读/输出/周期计数。',
                '各域异步断言、同步释放；加载器和DDR共同复位；不增加时序例外或真实外设协议。',
                '顶层物理I/O沿原约束，51位外部I/O，不增加UART/AXI控制端口。']
        module['timing_diagrams'] = [{'id': 'full_traversal', 'title': '完整张量交接', 'scenario': 'tensor_handoff',
            'description': '阶段顺序图；每个真实DDR请求均等待接受和响应，不规定返回固定拍数。',
            'wavejson': {'signal': [{'name': 'clk', 'wave': 'p.......'},
                {'name': 'stage', 'wave': '========', 'data': ['INPUT_WRITE', 'TABLE_PARAM', 'RGB_READ', 'STEM', 'STEM_WRITE', 'HALO_READ', 'DW_PW', 'PW_WRITE']},
                {'name': 'source', 'wave': '=.=..=..', 'data': ['pattern ROM', 'DDR RGB', 'DDR Stem']},
                {'name': 'result', 'wave': 'x...=..=', 'data': ['589824B Stem', '221184B PW']} ]}}]
        path = work / f'{name}.json'
        run.save(path, data)
        run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', path,
                     '--source', root / 'rtl' / f'{name}.v', '--out-dir', root / 'rtl', '--no-state'], root,
                    str(work.relative_to(root) / name))
    run.save(root / 'codegen_plan.json', {'task_classes': ['generate', 'modify', 'validate'], 'requirements': 'requirements.txt',
        'python_reference': 'reference/generate.py', 'arithmetic_modified': False, 'internal_interfaces_modified': False,
        'diagnostic_counter_ports_widened_to': 32, 'macro_commands': 10800,
        'gates': ['compile', 'ast', 'readability', 'comment', 'naming', 'profile', 'testbench', 'toolchain']})
    run.check()


if __name__ == '__main__':
    main()
