"""测试显式零端口测试台规格及真实接口负例，不放行 RTL 门禁。"""
import copy
import argparse
import difflib
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')
sys.path[:0] = [str(ROOT / 'checker_overlay'), str(SKILL)]
from scripts.python.workflow import spec_document as document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['frontend', 'final'])
    args = parser.parse_args()
    suffix = '_' + args.label if args.label else ''
    spec = {'name': 'tb_zero_port_parentheses', 'module_role': 'testbench',
            'rtl_path': 'rtl/tb_zero_port_parentheses.v',
            'description': '验证零端口测试台 schema，不代表 SiLU 功能或物理验证。',
            'interfaces': {'ports': []}, 'clock': {'signal': 'i_clk', 'source': 'internal stimulus'},
            'reset': {'policy': 'not used by this schema fixture'},
            'behavior': ['测试台内部产生刺激，顶层没有外部端口。'],
            'constraints': ['仅供仿真；不属于可综合生产模块。'],
            'corner_cases': ['接口缺失、真实多出端口及非法源码必须失败。'],
            'verification_cases': ['显式测试台零端口通过；默认设计零端口拒绝。'],
            'timing_diagrams': [{'id': 'internal-clock', 'title': '内部刺激说明',
                'scenario': 'schema-contract', 'description': '契约示意图，不是实测波形。',
                'wavejson': {'signal': [{'name': 'i_clk', 'wave': '0...'}]}}]}
    (HERE / 'zero_port_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    results = []

    def check(name, data, expected, sources=None):
        report = document.validate_spec_document(data, source_paths=sources)
        results.append({'case': name, 'expected': expected, 'actual': report['ok'],
                        'passed': report['ok'] == expected, 'diagnostics': report['issues']})

    check('explicit_zero_port_testbench', spec, True)
    check('parenthesized_source', spec, True, [HERE / 'tb_zero_port_parentheses.v'])
    # 保留首次前端缺失记录；已适配运行须把 bare header 当真正的正例。
    bare = document.validate_spec_document(spec, source_paths=[HERE / 'tb_zero_port_bare.v'])
    if args.label:
        check('bare_zero_port_source', spec, True, [HERE / 'tb_zero_port_bare.v'])
    variants = []
    design = copy.deepcopy(spec)
    design.pop('module_role')
    variants.append(('default_design_empty_ports', design, False))
    for name, role in [('explicit_design_empty_ports', 'design'), ('unknown_role', 'opaque'),
                       ('invalid_role_type', [])]:
        data = copy.deepcopy(spec)
        data['module_role'] = role
        variants.append((name, data, False))
    for name, interfaces in [('missing_ports', {}), ('invalid_ports_type', {'ports': {}}),
                              ('missing_interface', None)]:
        data = copy.deepcopy(spec)
        data['interfaces'] = interfaces
        variants.append((name, data, False))
    missing_wave = copy.deepcopy(spec)
    missing_wave['timing_diagrams'] = []
    variants.append(('missing_waveform', missing_wave, False))
    for args in variants:
        check(*args)
    check('extra_actual_port', spec, False, [HERE / 'tb_port_mismatch.v'])
    check('malformed_source', spec, False, [HERE / 'tb_malformed_source.v'])
    check('duplicate_module_sources', spec, False,
          [HERE / 'tb_zero_port_parentheses.v', HERE / 'tb_zero_port_parentheses.v'])
    # 现有生产规范仍兼容，验证没有全面放松端口/schema规则。
    baseline = json.loads((ROOT / 'reports/v3_silu_stall_candidate_20261005/silu_shared_unit_spec_input.json').read_text(encoding='utf-8'))
    check('existing_silu_spec', baseline, True)
    fixed = Path(document.__file__)
    upstream = SKILL / 'scripts/python/workflow/spec_document.py'
    patch = ''.join(difflib.unified_diff(upstream.read_text(encoding='utf-8').splitlines(True),
                    fixed.read_text(encoding='utf-8').splitlines(True),
                    fromfile='installed/spec_document.py', tofile='project/spec_document.py'))
    (HERE / ('zero_port_schema' + suffix + '.patch')).write_text(patch, encoding='utf-8')
    report = {'cases': results, 'all_passed': all(row['passed'] for row in results),
              'bare_header_parser': bare, 'source': str(fixed),
              'source_sha256': hashlib.sha256(fixed.read_bytes()).hexdigest(),
              'upstream_sha256': hashlib.sha256(upstream.read_bytes()).hexdigest(),
              'new_parser_added': False, 'design_synthesis_rule_changed': False,
              'canonical_bundle_executed': False, 'rtl_strict_gate_passed': False}
    (HERE / ('zero_port_schema_results' + suffix + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'cases': len(results), 'all_passed': report['all_passed'],
                      'bare_header_crosscheck': bare['ok']}, ensure_ascii=False))
    assert report['all_passed'], results


if __name__ == '__main__':
    main()
