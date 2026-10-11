"""核对五套独立诊断和既有功能证据，不改写旧报告或 RTL。"""
import hashlib
import difflib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
PRODUCTION = REPORTS.parent
SKILL = Path('C:/Users/lenovo/.codex/skills/readable-verilog-generator')


def receipt(path):
    path = Path(path)
    return {'path': str(path), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def verify(entries):
    for entry in entries:
        assert receipt(entry['path'])['sha256'] == entry['sha256'], entry['path']


def main():
    regression = REPORTS / 'v4_silu_regression_20261005'
    evidence = json.loads((regression / 'evidence.json').read_text(encoding='utf-8-sig'))
    verify(evidence['inputs'] + evidence['outputs'])
    prior_index = json.loads((REPORTS / 'v4_execution_20261005/execution_index.json').read_text(encoding='utf-8-sig'))
    verify(prior_index['files'])
    cases = []
    for case in evidence['cases']:
        text = (regression / case['log']).read_text(encoding='utf-8-sig')
        assert case['marker'] in text, case['log']
        if case['status'] == 'pass':
            assert not any(marker in text for marker in ('TB_ERROR', 'TB_FAIL', 'TB_MISMATCH'))
        cases.append(dict(case, execution='reused_hash_verified_not_rerun'))
    assert len(cases) == 8
    gate_paths = [
        ('silu_original', REPORTS / 'v4_execution_20261005/original_gate.json', 174, 'v4_same_rule_rerun'),
        ('silu_candidate', REPORTS / 'v4_execution_20261005/candidate_gate.json', 242, 'v4_same_rule_rerun'),
        ('round_testbench', REPORTS / 'v3_round_stall_20261005/strict_gate_final.json', 413, 'v3_round_testbench'),
        ('silu_contract_testbench', regression / 'contract_strict_gate.json', 157, 'v4_contract_testbench'),
        ('silu_full_domain_testbench', regression / 'full_domain_strict_gate.json', 148, 'v4_full_domain_testbench'),
    ]
    classification = json.loads((REPORTS / 'v4_gate_diagnosis_20261005/finding_classification.json').read_text(encoding='utf-8-sig'))
    runs, findings, groups = [], [], Counter()
    for run_id, path, expected, stage in gate_paths:
        gate = json.loads(path.read_text(encoding='utf-8-sig'))
        assert gate['errors'] == expected and not gate['delivery_ready'], run_id
        issues = gate['issues']
        run = {'id': run_id, 'stage': stage, 'report': receipt(path),
               'source_target': gate['root'], 'errors': expected, 'raw_issues': len(issues),
               'run_level_errors': expected - len(issues),
               'counts_by_rule': gate['delivery_issues_by_rule'], 'checks': gate['checks'],
               'delivery_ready': False, 'execution': 'reused_not_rerun',
               'included_in_v4_829': run_id in {item[0] for item in gate_paths[:3]},
               'command_evidence': 'Adjacent console logs and v4 execution plan; missing fields not invented',
               'historical_exit_code': None,
               'historical_command_complete': False,
               'historical_checker_closure_verified': False,
               'missing_evidence': 'Historical gate JSON alone does not establish full invocation or checker source closure'}
        existing_rows = [row for row in classification['issue_records']
                         if row['classification']['dataset'] == run_id]
        if run['included_in_v4_829']:
            assert [row['raw_issue'] for row in existing_rows] == issues, run_id
            run['root_cause_index'] = str(REPORTS / 'v4_gate_diagnosis_20261005/root_cause_groups.json')
        else:
            run['root_cause_index'] = None
            run['root_cause_status'] = 'not_in_v4_classification; separate pending checker rerun'
        runs.append(run)
        for index, issue in enumerate(issues):
            if existing_rows:
                group = existing_rows[index]['classification']['rootcause']
                group_status = 'reused_v4_classification'
            elif (issue.get('evidence') or {}).get('detail') == 'FORMATTER_AST_PARSE':
                group = 'testbench_formatter_parse_derived'
                group_status = 'parse_failure_evidence_not_independent_fault'
            else:
                group = 'rule_' + str(issue.get('code', 'unknown'))
                group_status = 'mechanical_rule_group_manual_rootcause_pending'
            groups[(run_id, group, group_status)] += 1
            findings.append({'run': run_id, 'raw_index': index, 'raw_issue': issue,
                             'blocking': True, 'status': 'historical_unclosed',
                             'group': group, 'group_status': group_status})
    assert sum(run['errors'] for run in runs[:3]) == 829
    assert sum(run['raw_issues'] for run in runs[:3]) == 826
    assert sum(run['run_level_errors'] for run in runs[:3]) == 3
    assert sum(run['errors'] for run in runs[3:]) == 305
    original = PRODUCTION / 'silu/silu_shared_unit.v'
    candidate = REPORTS / 'v3_silu_stall_candidate_20261005/silu_shared_unit.v'
    assert receipt(original)['sha256'] == receipt(regression / 'original/silu_shared_unit.v')['sha256']
    assert receipt(candidate)['sha256'] == receipt(regression / 'candidate/silu_shared_unit.v')['sha256']
    old_lines = original.read_text(encoding='utf-8').splitlines(True)
    new_lines = candidate.read_text(encoding='utf-8').splitlines(True)
    changed_lines = []
    for operation, start_old, end_old, start_new, end_new in difflib.SequenceMatcher(None, old_lines, new_lines).get_opcodes():
        if operation != 'equal':
            changed_lines.extend(old_lines[start_old:end_old] + new_lines[start_new:end_new])
    # 一行连接与同行注释一起变化：旧行+新行合计两行，而不是两处独立改动。
    assert len(changed_lines) == 2
    assert all(line.lstrip().startswith('//') or '.cea(' in line for line in changed_lines)
    assert any(".cea(1'b1)" in line for line in changed_lines)
    assert any('.cea(flag_pipeline_enable)' in line for line in changed_lines)
    diff_path = HERE / 'dut_frozen_diff.patch'
    diff_path.write_text(''.join(difflib.unified_diff(old_lines, new_lines,
                         fromfile=str(original), tofile=str(candidate))), encoding='utf-8')
    runtime = {'python': receipt(sys.executable),
               'installed_checker_python': [receipt(p) for p in sorted((SKILL / 'scripts').rglob('*.py'))],
               'installed_rule_json': [receipt(p) for folder in ('assets', 'config')
                                      for p in sorted((SKILL / folder).rglob('*.json'))]}
    manifest = {'schema': 'RoadYOLO-v5-evidence-v1', 'runs': runs,
                'historical_829_scope': 'first three only; contract157/full148 separate',
                'five_run_errors': 1134,
                'warning': '1134 counts entries across runs, not unique defects or current remaining failures',
                'source': [receipt(original), receipt(candidate)], 'runtime': runtime,
                'verified_dut_diff': receipt(diff_path),
                'groups': [{'run': key[0], 'group': key[1], 'status': key[2], 'raw_count': count}
                           for key, count in sorted(groups.items())],
                'grouping_warning': 'Mechanical rule groups do not prove distinct root causes',
                'prior_index_verified': receipt(REPORTS / 'v4_execution_20261005/execution_index.json'),
                'functional_evidence_verified': receipt(regression / 'evidence.json'),
                'functional_inputs': evidence['inputs'], 'functional_outputs': evidence['outputs'],
                'cases': cases, 'dut_changed': False, 'td_executed': False,
                'instructions': receipt('E:/EDownloads/RoadYOLO_AI建议要求与任务计划_v5_检查器适配与物理验证.md')}
    fresh_runs = []
    for label in ('old_original', 'old_candidate', 'new_original_ownership',
                  'new_candidate_ownership', 'new_original_final', 'new_candidate_final'):
        path = HERE / label / 'receipt.json'
        if path.exists():
            fresh = json.loads(path.read_text(encoding='utf-8'))
            verify(fresh['loaded_runtime'])
            process = HERE / label / 'process.json'
            fresh_runs.append({'label': label, 'receipt': receipt(path),
                               'process': receipt(process), 'gate': receipt(HERE / label / 'gate.json'),
                               'console': receipt(HERE / label / 'console.log'),
                               'executed_command': json.loads(process.read_text(encoding='utf-8')),
                               'gate_argv': fresh['argv'], 'gate_exit': fresh['gate_exit'],
                               'source_sha256': fresh['source_sha256'],
                               'spec_sha256': fresh['spec_sha256'],
                               'interface_sha256': fresh['interface_sha256'],
                               'loaded_checker_runtime': fresh['loaded_runtime']})
    manifest['fresh_checker_runs'] = fresh_runs
    new_functional = REPORTS / 'v5_vendor_regression_final_traces_20261005/results.json'
    if new_functional.exists():
        fresh_functional = json.loads(new_functional.read_text(encoding='utf-8'))
        assert fresh_functional['new_run'] and len(fresh_functional['cases']) == 8
        verify(fresh_functional['input_closure'])
        for case in fresh_functional['cases']:
            assert receipt(case['log'])['sha256'] == case['log_sha256']
            log = Path(case['log']).read_text(encoding='utf-8-sig')
            assert case['marker'] in log
            assert 'Failed to open file' not in log
            if case.get('cycle_trace'):
                assert receipt(case['cycle_trace'])['sha256'] == case['cycle_trace_sha256']
            if case['expected_status'] == 'pass':
                assert not any(marker in log for marker in ('TB_ERROR', 'TB_FAIL', 'TB_MISMATCH'))
        manifest['new_functional_regression'] = {
            'result': receipt(new_functional), 'cases': fresh_functional['cases'],
            'commands': receipt(new_functional.parent / 'commands.json'),
            'failed_first_attempt': str(REPORTS / 'v5_vendor_regression_20261005'),
            'preserved_functional_run_with_missing_traces': str(REPORTS / 'v5_vendor_regression_fixed_paths_20261005'),
            'coverage_warning': 'Fresh rerun of the same eight cases; not eight additional coverage classes',
        }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (HERE / 'historical_findings.json').write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'verified': True, 'runs': len(runs), 'functional_cases_reused': len(cases),
                      'errors': [run['errors'] for run in runs],
                      'raw_issues': [run['raw_issues'] for run in runs]}))


if __name__ == '__main__':
    main()
