"""Seal the read-back evidence, retaining raw pin differences and failed runs."""
import ast
import json
import re
from pathlib import Path
from recheck import HERE, TD, digest, guard_test, publish, verify
from summarize import rows


def minima(records):
    result = {}
    for row in records:
        key = (row['kind'], 'capture:' + row['capture_net']
               if row.get('capture_net') else 'pin:' + row['end'])
        result[key] = min(result.get(key, float('inf')), row['slack_ns'])
    return result


def main():
    for name in ('capture_dominance.json', 'delivery_receipt.json'):
        if (HERE / name).exists():
            raise FileExistsError(name)
    frozen = json.loads((HERE / 'frozen_inputs.json').read_text(encoding='utf-8'))
    snapshot = json.loads((HERE / 'snapshot_hashes.json').read_text(encoding='utf-8'))
    assert verify(frozen) == 377 and verify(snapshot) == 11
    guard_test()
    scripts = sorted(HERE.glob('*.py'))
    for path in scripts:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    # Do not merge differently named pins without an explicit TD capture net.
    sample = [{'kind': 'hold', 'end': 'cell.ie', 'capture_net': 'q', 'slack_ns': .1},
              {'kind': 'hold', 'end': 'cell.imf', 'capture_net': 'q', 'slack_ns': .02},
              {'kind': 'hold', 'end': 'macro.d', 'slack_ns': .03}]
    assert minima(sample) == {('hold', 'capture:q'): .02, ('hold', 'pin:macro.d'): .03}
    global_rows = [r for r in rows(HERE / 'precise_fixed/all_endpoints.timing')
                   if not r['begin'].startswith('i_') and not r['end'].startswith('o_')]
    dedicated = []
    for folder in ('complete_sources', 'physical_sources'):
        for path in sorted((HERE / folder).glob('*.timing')):
            if path.stem != 'input_all_destinations':
                dedicated.extend(r for r in rows(path)
                                 if not r['begin'].startswith('i_') and not r['end'].startswith('o_'))
    global_min, dedicated_min = minima(global_rows), minima(dedicated)
    missing = sorted(set(global_min) - set(dedicated_min))
    worse = [key for key, slack in global_min.items()
             if dedicated_min.get(key, float('inf')) > slack + .0005]
    assert len(global_min) == 6909 and not missing and not worse
    acceptance = json.loads((HERE / 'timing_scope_acceptance.json').read_text(encoding='utf-8'))
    assert len(acceptance['reports']) == 28 and acceptance['signoff'] is False
    publish(HERE / 'capture_dominance.json', {
        'global_internal_capture_keys': len(global_min), 'missing': missing,
        'dedicated_worse_than_global': worse, 'tolerance_ns': .0005,
        'raw_pin_variants_preserved': len(acceptance['global_selected_pairs_not_in_dedicated_internal_queries']),
        'method': 'Explicit TD capture net plus check kind; otherwise exact physical pin',
        'scope': 'Selected worst-corner records, not an exhaustive path enumeration'})
    report = HERE / '时序对象与签核范围复核报告.md'
    links = re.findall(r'\]\(([^)]+)\)', report.read_text(encoding='utf-8'))
    pending = 'delivery_receipt.json'
    assert all(link == pending or (HERE / link).exists() for link in links)
    assert verify(frozen) == 377 and verify(snapshot) == 11
    publish(HERE / pending, {
        'status': 'A_READBACK_COMPLETE_NOT_PRODUCTION_READY',
        'original_files_unchanged': 377, 'snapshot_files_unchanged': 11,
        'syntax_checked': [p.name for p in scripts], 'guard_and_minima_selfcheck': 'passed',
        'report_links_checked': len(links), 'timing_reports': 28,
        'capture_keys': 6909, 'missing_or_unexplained_worse_capture_keys': 0,
        'strict_gate': acceptance['strict_gate'],
        'rtl_sdc_modified': False, 'new_synthesis_place_route': False,
        'training_bitstream_board_flash': False, 'production_signoff': False,
        'td_sha256': digest(TD),
        'artifacts': {str(p.relative_to(HERE)): digest(p)
                      for p in sorted(HERE.rglob('*')) if p.is_file()}})
    assert all((HERE / link).exists() for link in links)
    print('FINAL_A_EVIDENCE_COMPLETE_NOT_PRODUCTION_READY', len(global_min))


if __name__ == '__main__':
    main()
