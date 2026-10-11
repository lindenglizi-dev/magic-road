"""汇总实际TD端点及同向量数值/周期，不修改约束或源文件。"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = ('setup', 'hold', 'recovery', 'removal')
PATH_ROW = re.compile(r'^Slack\s*:\s*([-+\d.]+)ns\s*\nBegin Point\s*:\s*([^\n]+)\nEnd Point\s*:\s*([^\n]+)\nCheck Type\s*:\s*(\w+)\s*\nProcess\s*:\s*([^\n]+)', re.M)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def timing_rows(text):
    for match in PATH_ROW.finditer(text):
        slack, begin, end, kind, corner = match.groups()
        assert kind in KINDS, kind
        yield {'slack_ns': float(slack), 'begin': begin.split(' (')[0].strip(),
               'end': end.split(' (')[0].strip(), 'kind': kind, 'corner': corner.strip()}

def numerical_trace(name):
    with (ROOT / 'verification' / name).open(encoding='utf-8') as handle:
        return [(row['event'], row['case'], row['beat'], row['fault'], row['data'])
                for row in csv.DictReader(handle)
                if row['event'] in ('dot', 'candidate', 'result_valid', 'result_accept')]

def main():
    assert numerical_trace('mac_baseline.csv') == numerical_trace('mac_final.csv')
    assert numerical_trace('mac_final.csv') == numerical_trace('mac_long_hold.csv')
    for name in ('mac_baseline.log', 'mac_final.log', 'mac_long_hold.log'):
        text = (ROOT / 'verification' / name).read_text(encoding='utf-8')
        assert 'TB_PASS_MAC_STREAM' in text and 'TB_ERROR' not in text and 'TB_FAIL' not in text
    physical = ROOT / 'physical'
    text = (physical / 'coverage_100000_all_paths.timing').read_text(encoding='utf-8')
    assert 'Confidence          : Routed' in text and 'STA coverage        : 100.00%' in text
    rows = list(timing_rows(text))
    assert len(rows) > 20000, 'Incomplete endpoint report'
    partition = {}
    for label, subset in (
        ('internal', [r for r in rows if not r['begin'].startswith('i_') and not r['end'].startswith('o_')]),
        ('external', [r for r in rows if r['begin'].startswith('i_') or r['end'].startswith('o_')])):
        partition[label] = {}
        for kind in KINDS:
            group = [r for r in subset if r['kind'] == kind]
            partition[label][kind] = {'reported_rows': len(group),
                'negative_rows': sum(r['slack_ns'] < 0 for r in group),
                'worst': min(group, key=lambda r: r['slack_ns']) if group else None}
    area = (physical / 'shell_route.area').read_text(encoding='utf-8')
    resources = {key: int(re.search(r'^#' + key + r'\s+(\d+)', area, re.M)[1])
                 for key in ('slice', 'lut6', 'reg', 'dsp', 'eram', 'IO')}
    tile = (ROOT / 'verification/tile_final.log').read_text(encoding='utf-8')
    assert 'TB_PASS_DOWN2_TILE' in tile and 'TB_ERROR' not in tile and 'TB_FAIL' not in tile
    cycle_rows = [{key: int(value) for key, value in re.findall(r'(\w+)=(\d+)', line)}
                  for line in tile.splitlines() if line.startswith('CYCLE_RESULT')]
    assert [r['core'] for r in cycle_rows] == [3257, 3257, 3259, 1310, 1594]
    critical_bindings = {}
    for directory, suffix in (('rtl', '*.v'), ('physical', '*'), ('verification', '*.log'), ('spec', '*.json')):
        for p in sorted((ROOT / directory).glob(suffix)):
            if p.is_file() and p.name not in ('physical_status.json', 'collect_results_final.log'):
                critical_bindings[str(p.relative_to(ROOT)).replace('\\', '/')] = sha(p)
    for directory in ('reference', 'spec', 'verification'):
        for p in sorted((ROOT / directory).rglob('*')):
            if p.is_file() and p.suffix in ('.py', '.v', '.hex', '.txt', '.csv', '.svg', '.json5', '.json', '.md'):
                critical_bindings[str(p.relative_to(ROOT)).replace('\\', '/')] = sha(p)
    for name in ('verify_candidate.py', 'collect_results.py', 'baseline_freeze.json'):
        critical_bindings[name] = sha(ROOT / name)
    tools = {name: {'path': str(path), 'sha256': sha(path)} for name, path in {
        'python': Path(r'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe'),
        'iverilog': Path(r'E:\project\qiansai\.tools\iverilog\bin\iverilog.exe'),
        'vvp': Path(r'E:\project\qiansai\.tools\iverilog\bin\vvp.exe'),
        'td': Path(r'E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe')}.items()}
    gate = json.loads((ROOT / 'gates/candidate_full.json').read_text(encoding='utf-8'))
    baseline_gate = json.loads((ROOT / 'gates/baseline_full.json').read_text(encoding='utf-8'))
    report = {'conclusion': 'DIAGNOSTIC_ONLY_NOT_PRODUCTION_SIGNOFF', 'device': 'PH1P35MDG324',
        'speed_grade': -3, 'clock_period_ns': 10, 'resources_including_shell_and_scheduler': resources,
        'partition_rule': 'Exclude top i_* origins and top o_* destinations; retain DSP/RAM endpoints.',
        'timing': partition, 'coverage': '100% reported; Slow/Fast max/min; not board signoff',
        'same_vector_numerical_trace_rows': len(numerical_trace('mac_final.csv')),
        'cycle_rows': cycle_rows, 'strict_gate': {k: v['status'] for k, v in gate['checks'].items()},
        'strict_diagnostics': sum(gate['delivery_issues_by_rule'].values()),
        'strict_baseline_same_six_sources': sum(baseline_gate['delivery_issues_by_rule'].values()),
        'binding_sha256': critical_bindings, 'tools': tools, 'bitstream_requested': False, 'new_timing_exceptions': False}
    (physical / 'physical_status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('binding_sha256',)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
