"""保留全部原始项，为差异和剩余阻塞附加依据，不改写门禁结论。"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TARGETS = {'original': ROOT / 'silu/silu_shared_unit.v',
           'candidate': ROOT / 'reports/v3_silu_stall_candidate_20261005/silu_shared_unit.v'}


def detail(issue):
    return (issue.get('evidence') or {}).get('detail') or issue.get('detail', '')


def target(issue):
    match = re.search(r'(?:^|; )target=([^;]+)', detail(issue))
    return match.group(1) if match else None


def next_step(issue):
    code, text = issue.get('code'), detail(issue)
    if code in {'VG145', 'VG146', 'VG147'}:
        if 'external output implementation is unknown' in text:
            return '保留 opaque 输出未知；补充受审的原语边界事实与官方行为/物理证据，不把接口声明当内部实现。'
        if 'inconclusive_reason=' in text and 'inconclusive_reason=none;' not in text:
            return '按 target 最小复现剩余 native formatter 缺失事实，修复原生解析并保持负例；未知期间不放行。'
        return '按完整依赖锥审查同拍等价预译码/控制状态方案；另立行为候选并回归 latency=5、停顿和装表，不用别名掩盖。'
    if code == 'VG122':
        return '逐项证明计数器/地址范围和合法截断，或另立显式位宽候选；不得仅引用 Verilog 截断语义宣称无溢出。'
    if code == 'VG013' and 'cnt_pending' in issue.get('message', ''):
        return '计数器被识别为flag的命名分类需最小复现；核对真实3位计数器语义，不能只把counter改名成flag以消警。'
    if code in {'VG084', 'VG137'}:
        return '原生检查仅给运行级unknown，尚无精确故障位置；从相关case/assign逐条最小化定位，再补原生位宽事实，期间保持阻塞。'
    if code in {'VG085', 'VG097', 'VG084'}:
        return '保留真实位宽/类型错误；核对切片、参数求值、signed 和实际端口绑定的最小正负例。'
    if code in {'VG060', 'VG013', 'VG061', 'VG040', 'VG063', 'VG062', 'VG065', 'VG066',
                'VG125', 'VG132', 'VG137', 'VG138', 'VG153', 'COMMENT_COMMENT_PLACEMENT'}:
        return '在独立非行为整理副本修正此处命名/注释/格式；保持冻结 DUT，逐项复跑原生检查及功能回归。'
    if code == 'FORMATTER_TEMPLATE_MISMATCH':
        return '核对原生格式器模板差异；修正源码格式，不豁免或替代 AST/格式检查。'
    return '按原始证据最小复现此规则，先确认适用性再修改；本项仍阻塞。'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True, choices=['ownership', 'final'])
    args = parser.parse_args()
    comparison = json.loads((HERE / f'matrix_comparison_{args.label}.json').read_text(encoding='utf-8'))
    changes = []
    for row in comparison['raw_changes']:
        issue = row['raw_issue']
        code, text = issue.get('code'), detail(issue)
        explanation = None
        evidence = None
        if code in {'VG146', 'VG147'} and ('external interface has no implementation' in text
                                         or 'external output implementation is unknown' in text
                                         or 'inconclusive_reason=none;' in text):
            explanation = ('仅依据已声明 formal 方向改变 producer 图：input 是 sink，不再反向污染上游；'
                           'output 仍是 opaque unknown。该行变化不代表预算/功能/物理通过；'
                           '对照相同 target 的完整旧新报告，超预算项仍保留。')
            evidence = 'checker_snapshot_' + args.label + '/scripts/python/quality/vg_comb_targets.py'
        elif code == 'VG085' and issue.get('line') in {145, 200, 218, 278}:
            explanation = '原表达式实际含 cnt_table_expected[9:0]；原算符事实错误丢失 selector，前端修复为10位；原11位计数器未修改。真实宽度负例仍失败。'
            evidence = 'v5_checker_adapter_20261005 前端差分及切片正负例'
        elif code in {'VG146', 'VG147'} and 'wire_table_write_data:' in text and "expected '}', got '{'" in text:
            explanation = ('移除无依据的 RAM input producer 后，原来被 external unknown 掩盖的'
                           'wire_table_write_data 重复拼接解析失败成为直接原因；保持 failed，未当成新硬件故障或通过。')
            evidence = '相同 target 的 old/new gate.json；vg_comb_targets.py typed interface 补丁'
        changes.append(dict(row, explanation=explanation,
                            explanation_status='evidence_linked' if explanation else 'manual_review_pending',
                            adapter_evidence=evidence))
    (HERE / f'annotated_changes_{args.label}.json').write_text(
        json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
    remaining = []
    budgets = []
    for variant, source in TARGETS.items():
        gate = json.loads((HERE / f'new_{variant}_{args.label}/gate.json').read_text(encoding='utf-8'))
        assert not gate['delivery_ready'], 'This unclosed-candidate catalog must be reconsidered after admission passes'
        lines = source.read_text(encoding='utf-8').splitlines()
        for index, issue in enumerate(gate['issues']):
            name = target(issue)
            if name is None and issue.get('code') == 'VG013':
                named = re.search(r'`([^`]+)`', issue.get('message', ''))
                name = named.group(1) if named else None
            identifier = (name or '').split('$')[0].split('[')[0]
            related = [{'line': n, 'source': line.strip()} for n, line in enumerate(lines, 1)
                       if identifier and re.search(r'\b' + re.escape(identifier) + r'\b', line.split('//')[0])]
            location = issue.get('location') or {}
            reported_line = location.get('line_start') or issue.get('line')
            path_line = re.search(r':(\d+)$', str(issue.get('path', '')))
            if reported_line is None and path_line:
                reported_line = int(path_line.group(1))
            row = {'variant': variant, 'raw_index': index, 'raw_issue': issue,
                   'source_path': str(source), 'line': reported_line,
                   'location_status': 'reported_line' if reported_line else 'native_location_unresolved_not_invented',
                   'target': name, 'source_occurrences_not_exact_driver_locations': related,
                   'next_step': next_step(issue), 'blocking': True,
                   'status': 'unclosed'}
            remaining.append(row)
            if issue.get('code') in {'VG145', 'VG146', 'VG147'}:
                budgets.append(row)
        remaining.append({'variant': variant, 'raw_index': None, 'raw_issue': None,
                          'source_path': str(source), 'line': None, 'target': None,
                          'blocking': True, 'status': 'unclosed',
                          'run_level_errors': gate['errors'] - len(gate['issues']),
                          'ast_checks': gate['checks']['ast'],
                          'next_step': '单列 formatter 运行级模板失败；见 checks.ast（parse_errors=0）；修正格式模板，不计作语法解析失败或独立功能故障。'})
        assert gate['errors'] == len(gate['issues']) + remaining[-1]['run_level_errors']
    result = {'label': args.label, 'normal_physical_admission': False,
              'counts_are_not_unique_root_causes': True,
              'mechanical_rule_group_counts': dict(Counter(row['raw_issue']['code'] for row in remaining if row['raw_issue'])),
              'unexplained_changes': sum(row['explanation'] is None for row in changes),
              'remaining': remaining, 'budget_details': budgets}
    (HERE / f'remaining_blockers_{args.label}.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    with (HERE / f'remaining_blockers_{args.label}.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['variant', 'raw_index', 'code', 'source', 'line', 'target', 'evidence', 'next_step'])
        for row in remaining:
            issue = row['raw_issue'] or {}
            writer.writerow([row['variant'], row['raw_index'], issue.get('code', 'RUN_LEVEL_FORMATTER'),
                             row['source_path'], row['line'], row['target'], detail(issue), row['next_step']])
    print(json.dumps({'changes': len(changes), 'unexplained': result['unexplained_changes'],
                      'remaining_rows': len(remaining), 'normal_physical_admission': False}))


if __name__ == '__main__':
    main()
