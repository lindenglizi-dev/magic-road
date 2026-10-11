"""Summarize named TD query scopes without pretending a filtered table is full."""
from pathlib import Path
import json
import re
from recheck import HERE, publish, verify

KINDS = ('setup', 'hold', 'recovery', 'removal')
SLACK = re.compile(r'^Slack\s*:\s*([-+\d.]+)ns\s*$')


def rows(path):
    result = []
    current = None
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            match = SLACK.match(line)
            if match:
                if current:
                    result.append(current)
                current = {'slack_ns': float(match[1])}
            elif current:
                for label, key in (('Begin Point', 'begin'), ('End Point', 'end'),
                                   ('Check Type', 'kind'), ('Process', 'corner')):
                    if line.startswith(label) and ':' in line:
                        current[key] = line.split(':', 1)[1].split(' (')[0].strip()
                if 'clk2q' in line and 'pin:' in line and 'launch_q' not in current:
                    current['launch_q'] = line.split('pin:', 1)[1].strip().split()[0]
                capture = re.search(r'(?:^reg\s|\(reg\)).*?net:\s*([^,\r\n]+)', line)
                if capture:
                    current['capture_net'] = capture[1].strip()
    if current:
        result.append(current)
    if not result or any(not {'slack_ns', 'begin', 'end', 'kind', 'corner'} <= row.keys() for row in result):
        raise ValueError(f'Incomplete timing records: {path}')
    return result


def statistics(records):
    report = {}
    for kind in KINDS:
        selected = [row for row in records if row['kind'] == kind]
        report[kind] = {'records': len(selected), 'unique_endpoints': len({r['end'] for r in selected}),
            'negative_records': sum(r['slack_ns'] < 0 for r in selected),
            'worst': min(selected, key=lambda r: r['slack_ns']) if selected else None}
    return report


def main():
    source = HERE / 'precise_fixed'
    files = {}
    parsed = {}
    for path in sorted(source.glob('*.timing')):
        record = rows(path)
        parsed[path.stem] = record
        files[path.name] = statistics(record)
    for path in sorted((HERE / 'complete_sources').glob('*.timing')):
        record = rows(path)
        parsed['source_' + path.stem] = record
        files['complete_sources/' + path.name] = statistics(record)
    for path in sorted((HERE / 'physical_sources').glob('*.timing')):
        record = rows(path)
        parsed['physical_' + path.stem] = record
        files['physical_sources/' + path.name] = statistics(record)
    needed = ('all_endpoints', 'raw_sync_asr', 'meta_done', 'done_function_regs',
              'done_dsp_reset', 'reg_reg', 'reg_dsp', 'reg_eram', 'dsp_reg',
              'eram_reg', 'input_reg', 'input_eram', 'reg_output', 'raw_regs')
    missing = [name for name in needed if name not in parsed]
    if missing:
        raise ValueError(f'Required reports missing: {missing}')
    assert all(r['end'] == 'reg_release_done_reg_syn_3.asr' for r in parsed['raw_sync_asr'])
    assert all(r['end'] == 'reg_release_done_reg_syn_3.ima' and
               r.get('launch_q') == 'reg_release_done_reg_syn_3.oqb' for r in parsed['meta_done'])
    assert all(r.get('launch_q') == 'reg_release_done_reg_syn_3.oqa' for r in parsed['done_function_regs'])
    assert not any(r['end'].startswith('reg_release_done_reg_syn_3.') for r in parsed['done_function_regs'])
    for name in ('reg_dsp', 'done_dsp_reset'):
        assert all(re.search(r'mult0_syn_(681|776|1105|1200)\.', r['end']) for r in parsed[name]), name
    assert all('/PH1P_LOGIC_ERAM_Inst_silu_table_syn_1.' in r['end'] for r in parsed['reg_eram'])
    internal_names = ('reg_reg', 'reg_dsp', 'reg_eram', 'dsp_reg', 'eram_reg',
                      'dsp_dsp', 'eram_dsp', 'reg_distributed_memory')
    internal = [r for name in internal_names for r in parsed.get(name, [])]
    assert not any(r['begin'].startswith('i_') or r['end'].startswith('o_') for r in internal)
    source_internal = [r for name in ('source_reg_all_destinations', 'source_dsp_all_destinations',
                       'source_eram_all_destinations', 'source_distributed_memory_all_destinations')
                       for r in parsed[name] if not r['end'].startswith('o_')]
    assert not any(r['begin'].startswith('i_') for r in source_internal)
    internal.extend(source_internal)
    physical_internal = [r for name, record in parsed.items() if name.startswith('physical_')
                         for r in record if not r['end'].startswith('o_')]
    assert not any(r['begin'].startswith('i_') for r in physical_internal)
    internal.extend(physical_internal)
    external = [r for name in ('input_reg', 'input_eram', 'input_dsp', 'reg_output',
                              'dsp_output', 'eram_output', 'done_output') for r in parsed.get(name, [])]
    external.extend(r for name, group in parsed.items() if name.startswith('source_')
                    for r in group if r['begin'].startswith('i_') or r['end'].startswith('o_'))
    external.extend(r for name, group in parsed.items() if name.startswith('physical_')
                    for r in group if r['end'].startswith('o_'))
    global_internal = {(r['kind'], r['end']) for r in parsed['all_endpoints']
                       if not r['begin'].startswith('i_') and not r['end'].startswith('o_')}
    covered = {(r['kind'], r['end']) for r in internal}
    absent = sorted(global_internal - covered)
    def capture_key(row):
        return (row['kind'], 'capture:' + row['capture_net'] if row.get('capture_net') else 'pin:' + row['end'])
    global_capture = {capture_key(r) for r in parsed['all_endpoints']
                      if not r['begin'].startswith('i_') and not r['end'].startswith('o_')}
    covered_capture = {capture_key(r) for r in internal}
    absent_capture = sorted(global_capture - covered_capture)
    log = (source / 'td.log').read_text(encoding='utf-8', errors='replace')
    warnings = [line for line in log.splitlines() if 'WARNING' in line or 'ERROR:' in line]
    count = verify(json.loads((HERE / 'frozen_inputs.json').read_text(encoding='utf-8')))
    publish(HERE / 'timing_scope_acceptance.json', {
        'scope': 'Frozen dynamic serial chain with diagnostic shell, not MAC/DW/PW/full CNN',
        'source_directories': ['precise_fixed', 'complete_sources', 'physical_sources'], 'reports': files,
        'internal_union': statistics(internal), 'external_union': statistics(external),
        'global_selected_internal_endpoint_kind_pairs': len(global_internal),
        'global_selected_pairs_not_in_dedicated_internal_queries': absent,
        'global_internal_capture_keys': len(global_capture),
        'global_capture_keys_not_in_internal_queries': absent_capture,
        'a_evidence_status': 'CAPTURE_CROSSCHECK_CLOSED' if not absent_capture else 'COVERAGE_GAPS_REMAIN',
        'query_warnings': warnings, 'original_files_unchanged': count,
        'strict_gate': json.loads((HERE / 'static_gate/receipt.json').read_text(encoding='utf-8')),
        'signoff': False, 'new_constraints_or_exceptions': False})
    for label, record in (('internal', internal), ('external', external)):
        print(label, {kind: data['worst']['slack_ns'] if data['worst'] else None
                      for kind, data in statistics(record).items()})
    print('DEDICATED_SCOPE_ASSERTIONS_PASS', 'coverage_missing_pairs', len(absent), 'files', len(files))
    print('CAPTURE_KEYS', len(global_capture), 'MISSING', len(absent_capture))


if __name__ == '__main__':
    main()
