"""冻结本批真实证据，输出逐项诊断清单与最终收据。"""
import ast
import csv
import json
import re
from pathlib import Path
from execute import HERE, A, CORE, MSIM, TD, check, sha, write


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_hashes(values, root):
    for name, value in values.items():
        path = Path(name)
        if not path.is_absolute():
            path = root / path
        assert path.is_file() and sha(path) == value, path


def main():
    assert not (HERE / 'delivery_receipt.json').exists(), 'Refuse to overwrite final receipt'
    check()
    for path in HERE.glob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    check_hashes(load(HERE / 'layer_inputs.json'), HERE)
    check_hashes(load(HERE / 'candidate/physical/input_hashes.json'), HERE)
    for name in CORE:
        assert sha(HERE / 'candidate/rtl' / name) == sha(HERE / 'hardware' / name)
    for folder in ('layer', 'layer/phases', 'layer/stress_bias_host',
                   'layer/stress_bias_contract_host', 'layer/declared_validation'):
        receipt = load(HERE / folder / 'receipt.json')
        check_hashes(receipt['sources'], HERE)
    for folder in ('layer/vectors', 'layer/stress_bias_host/vectors',
                   'layer/stress_bias_contract_host/vectors', 'layer/declared_validation/vectors'):
        manifest = load(HERE / folder / 'manifest.json')
        check_hashes(manifest['files'], HERE / folder)
    for name in ('results.csv', 'batch_cycles.csv'):
        assert (HERE / 'baseline_sim/modelsim_host' / name).read_bytes() == (
               HERE / 'candidate_sim/modelsim_host' / name).read_bytes()
    timing = load(HERE / 'candidate/timing_comparison.json')
    assert not timing['missing_capture_keys'] and not timing['unexplained_worse_global_records']
    assert timing['candidate_named_paths']['raw_sync_asr']['removal']['negative_records'] == 3
    assert timing['candidate_internal']['setup']['negative_records'] == 0
    assert timing['candidate_internal']['hold']['negative_records'] == 0
    layer = HERE / 'layer'
    for folder in ('phases', 'stress_bias_contract_host', 'declared_validation'):
        with (layer / folder / 'layer_cycles.csv').open() as stream:
            records = list(csv.DictReader(stream))
        for record in records:
            assert int(record['core']) == sum(int(value) for key, value in record.items()
                                             if key not in ('case', 'core'))
        assert records[0]['core'] == '20633' and len(records) == 21
    assert (layer / 'declared_validation/layer_cycles.csv').read_bytes() == (
            layer / 'stress_bias_contract_host/layer_cycles.csv').read_bytes()
    stress = load(layer / 'stress_bias_contract_host/receipt.json')
    assert all(case['pw_distinct'] >= 8 and case['pw_nonzero'] > 0 for case in stress['cases'])

    reviewed = {
        'VG153': ('已有驱动证据，严格失败保留', '已命名子模块输出或行为RAM索引写入；逐项定位未找到真实悬空驱动。'),
        'VG155': ('握手语义核实，严格失败保留', 'ST_TX与复位有效蕴含valid，ready时推进；数字回归无丢失/重复。'),
        'VG098': ('人工状态可达性核实，严格失败保留', '初态与转移可追踪，未提供无限活性证明。'),
        'VG097': ('接口证据存在，静态规则未闭合', '工程PH1P接口及真实ERAM映射已核实，参数解析识别限制继续记录。'),
        'VG132': ('时钟连接证据存在，静态规则未闭合', 'PH1P clka/clkb为时钟端口；没有改接时钟以规避规则。'),
        'VG138': ('常量定宽要求待处理', '逐表达式核查；未把未定宽诊断等同于已经发生的数值错误。'),
        'VG145': ('结构规则未处理', '结合真实时序；本批未按源数量盲目增加流水。'),
        'VG146': ('结构规则未处理', '强预算与不确定展开保留；不等同于已证明组合环或负时序。')}
    ledger = []
    for scope, path in [('original_full', HERE / 'gates/original_full/gate.json'),
                        ('reset_candidate', HERE / 'gates/candidate/gate.json'),
                        ('layer_declared', layer / 'declared_validation/gate.json')]:
        gate = load(path)
        for index, finding in enumerate(gate['issues']):
            rule = finding.get('rule_id') or finding.get('code', '')
            status, reason = reviewed.get(rule, ('严格诊断待处理', '原始记录保留，本批未确认或修复该项。'))
            ledger.append({'scope': scope, 'index': index, 'rule': rule,
                'file': finding.get('path'), 'line': finding.get('line'),
                'severity': finding.get('severity'), 'message': finding.get('message'),
                'disposition': status if scope != 'layer_declared' else '层闭包严格诊断未闭合',
                'reason': reason if scope != 'layer_declared' else '声明解析已修正，功能回归通过；该条规则仍须按完整实例身份核实。'})
    write(HERE / '诊断分类与处置清单.json', {'records': ledger,
        'observation_counts_not_independent_defects': True,
        'manual_review_does_not_change_gate': True})
    documents = [HERE / '四步执行与问题处置报告.md', HERE / '滚动状态.md',
                 layer / 'tb_down2_dynamic_tile_contract_spec.md']
    for path in documents:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            assert link == 'delivery_receipt.json' or (path.parent / link).exists(), (path, link)
    check()
    gates = load(HERE / 'diagnostic_classification.json')['scope_counts']
    gates['layer_declared'] = {key: load(layer / 'declared_validation/receipt.json')[key]
                              for key in ('errors', 'strict_warnings', 'checks')}
    write(HERE / 'delivery_receipt.json', {
        'status': 'FOUR_STEPS_EXECUTED_FUNCTION_PASSED_PHYSICAL_AND_STRICT_UNCLOSED',
        'old_files_unchanged': len(load(HERE / 'frozen.json')),
        'core_sources_unchanged': list(CORE), 'physical_scope': timing['scope'],
        'resource_scope': '38-bit reset shell plus serial quantization; no layer scheduler',
        'resources': {'slice':1740, 'lut6':1254, 'registers':1931, 'dsp':4, 'eram':1, 'io':38},
        'internal_timing_ns': {k: v['worst']['slack_ns'] for k,v in timing['candidate_internal'].items()},
        'raw_reset_removal_ns': -.346, 'raw_reset_negative_records':3,
        'external_setup_hold_ns': [.001,-1.024], 'gates':gates,
        'layer_core_cycles':20633, 'layer_dw_pw_cycles':[8462,12171],
        'serialized_pre_silu_post_cycles':18560, 'serialized_fraction':18560/20633,
        'test_package_and_stress_vectors_separate': True,
        'runtime_quantization_loader_real_qat_ddr_full_network': False,
        'no_new_timing_exceptions': True, 'production_deployment_approved': False,
        'tools': {str(p):sha(p) for p in [TD,MSIM/'vlib.exe',MSIM/'vlog.exe',MSIM/'vsim.exe']},
        'artifact_hashes': {str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file()}})
    print('FOUR_STEP_DELIVERY_COMPLETE_FUNCTION_ONLY', flush=True)


if __name__ == '__main__':
    main()
