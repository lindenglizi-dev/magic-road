"""Bind the isolated functional and routed evidence without declaring release."""
import ast
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
import evidence

ROOT = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def timing_rows(path):
    row = None
    fields = {'Begin Point': 'begin', 'End Point': 'end', 'Check Type': 'kind', 'Process': 'corner'}
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            slack = re.match(r'^Slack\s*:\s*([-+\d.]+)ns\s*$', line)
            if slack:
                row = {'slack_ns': float(slack[1])}
            elif row is not None:
                prefix = line.split(':', 1)[0].strip()
                if prefix in fields:
                    row[fields[prefix]] = line.split(':', 1)[1].strip().split(' (')[0]
                    if prefix == 'Process':
                        yield row
                        row = None


def physical(folder):
    path = ROOT / 'physical' / folder
    rows = list(timing_rows(path / 'coverage_100000_all_paths.timing'))
    assert len(rows) > 15000
    partition = {}
    for label, selected in (
        ('internal', [r for r in rows if not r['begin'].startswith('i_') and not r['end'].startswith('o_')]),
        ('external', [r for r in rows if r['begin'].startswith('i_') or r['end'].startswith('o_')])):
        partition[label] = {}
        for kind in ('setup', 'hold', 'recovery', 'removal'):
            subset = [r for r in selected if r['kind'] == kind]
            assert subset, (folder, label, kind)
            partition[label][kind] = {
                'records': len(subset), 'negative_records': sum(r['slack_ns'] < 0 for r in subset),
                'worst': min(subset, key=lambda r: r['slack_ns']),
                'corners': dict(Counter(r['corner'] for r in subset)),
            }
            if label == 'internal':
                assert partition[label][kind]['negative_records'] == 0
    area = (path / 'shell_route.area').read_text(encoding='utf-8')
    resources = {key: int(re.search(r'^#' + key + r'\s+(\d+)', area, re.M)[1])
                 for key in ('slice', 'lut6', 'reg', 'dsp', 'eram', 'IO')}
    assert resources['IO'] == 38
    assert resources['slice'] <= 21216 and resources['dsp'] <= 40 and resources['eram'] <= 108
    with (path / 'coverage_100000_all_paths.timing').open(encoding='utf-8') as stream:
        header = ''.join(next(stream) for _ in range(25))
    assert '100.00%' in header and 'Routed' in header and 'Both (Slow and Fast)' in header
    assert (path / 'pr.db').is_file()
    return {'resources_including_shell': resources, 'timing': partition,
            'sta_coverage_reported': '100.00%', 'routed': True,
            'partition_rule': 'external if launch begins i_ or capture begins o_; retain internal DSP/ERAM paths'}


def main():
    assert not (ROOT / 'delivery_receipt.json').exists(), 'Do not overwrite final receipt'
    evidence.check()
    for path in [ROOT / 'update_budget.py', ROOT / 'finalize.py', * (ROOT / 'tests').rglob('*.py')]:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    core = read_json(ROOT / 'tests/receipt.json')
    for name, digest in core['source_sha256'].items():
        assert sha(ROOT / 'rtl' / name) == digest, name
    assert 'runtime_post_faults=1' in core['pass_marker']
    layer = read_json(ROOT / 'tests/layer/receipt.json')
    for name, digest in layer['sources'].items():
        assert sha(Path(name)) == digest, name
    assert len(layer['results']) == 2
    for cases in layer['results'].values():
        assert len(cases) == 7
        for row in cases:
            assert row['endpoint'] == row['dw_endpoint'] + row['pw_endpoint']
            assert sum(row[key] for key in ('writeback_stall', 'capacity_wait', 'commit_cycle',
                       'mac_issue', 'input_wait', 'task_close', 'drain', 'other')) == row['endpoint']
            assert all(row[key] == 640 for key in ('acc', 'pre', 'silu', 'post', 'commit'))
            assert row['export'] == 384
    budget = read_json(ROOT / 'layer_cycle_budget.json')
    assert budget['full_frame_prediction_cycles'] is None and len(budget['layers']) == 67
    scopes = {name: physical(name) for name in ('layer_shell', 'runtime_chain')}
    summary = read_json(ROOT / 'physical/physical_summary.json')
    for scope in scopes:
        for suffix in ('sdc', 'adc'):
            path = ROOT / 'physical' / scope / ('shell.' + suffix)
            assert sha(path) == summary['constraints'][suffix + '_sha256'].lower()
        claimed = summary[scope]['resource']
        actual = scopes[scope]['resources_including_shell']
        assert actual['slice'] == claimed['slice'] and actual['dsp'] == claimed['dsp']
        assert actual['eram'] == claimed['eram']
        for kind in ('setup', 'hold', 'recovery', 'removal'):
            assert scopes[scope]['timing']['internal'][kind]['worst']['slack_ns'] == \
                summary[scope]['timing']['internal'][kind]['worst_slack_ns']
    gate = read_json(ROOT / 'gates/generated_deliverable_gate_final.json')
    gate_checks = {name: value['status'] for name, value in gate['checks'].items()}
    evidence.check()
    bindings = {}
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and 'work' not in path.relative_to(ROOT).parts and path.name != 'status.json':
            bindings[path.relative_to(ROOT).as_posix()] = sha(path)
    receipt = {
        'status': 'FUNCTION_AND_INTERNAL_TIMING_PASS_EXTERNAL_AND_STRICT_UNCLOSED',
        'old_frozen_files_verified': 1251, 'core_regression': core['pass_marker'],
        'layer_cases': 14, 'old_serial_layer_cycles': 20633, 'new_no_stall_layer_cycles': 3331,
        'phase_cycles': {'DW': 2015, 'PW': 1316}, 'physical': scopes,
        'strict_checks': gate_checks, 'production_delivery': False,
        'full_frame_5fps': False, 'real_QAT_attached': False,
        'production_changed': False, 'training_started': False,
        'bitstream_generated': False, 'board_or_flash_used': False,
        'new_timing_exceptions': False, 'artifact_sha256': bindings,
    }
    (ROOT / 'delivery_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'status.json').write_text(json.dumps({key: value for key, value in receipt.items()
         if key not in ('artifact_sha256',)}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('FINAL_EVIDENCE_PASS_OLD1251_FUNCTION_INTERNAL_TIMING_EXTERNAL_STRICT_UNCLOSED')


if __name__ == '__main__':
    main()
