"""Check the three observed writes; never promote observations to memory PASS."""
from collections import Counter
import json
import re

import run

ROOT = run.ROOT


def records(lines, prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line))
            for line in lines if prefix in line]


assert records(['# REAL_EVENT kind=AW_ACCEPT case=0 time_ps=42'], 'REAL_EVENT') == [
    {'kind': 'AW_ACCEPT', 'case': '0', 'time_ps': '42'}]
run.helper.check()
work = max(ROOT.glob('simulation*'), key=lambda path: path.stat().st_mtime)
receipt = json.loads((work / 'receipt.json').read_text(encoding='utf-8'))
assert receipt['completed'] and not receipt['changed_during_run']
events = records(receipt['lines'], 'REAL_EVENT')
summary, = records(receipt['lines'], 'REAL_SUMMARY')
expected = {'aw': 3, 'w': 3, 'ar': 1, 'b': 3, 'dhi_write': 3,
            'dhi_read': 1, 'pin_write': 3, 'pin_read': 1, 'memory_pass': 0}
assert all(int(summary[name]) == value for name, value in expected.items()), summary
assert not any('REAL_ERROR' in line for line in receipt['lines'])


def event(kind, case):
    matches = [item for item in events if item['kind'] == kind
               and item.get('case', item.get('window_case')) == str(case)]
    assert len(matches) == 1, (kind, case, matches)
    return matches[0]


writes = []
for case in range(3):
    aw, w, b, dhi, pin = [event(kind, case) for kind in
                         ('AW_ACCEPT', 'W_ACCEPT', 'INTERNAL_BVALID', 'DHI_WRITE', 'DDR_PIN_WRITE')]
    assert int(aw['addr'], 16) == case * 8
    assert int(w['dhi_cycle']) - int(aw['dhi_cycle']) == case
    assert int(b['dhi_cycle']) - int(w['dhi_cycle']) == 1
    assert int(b['time_ps']) < int(pin['time_ps'])
    code = int(dhi['code'], 16)
    assert code >> 28 == 0xC and (code >> 20) & 3 == case
    assert int(pin['bank'], 16) == case and int(pin['addr'], 16) == 0
    writes.append({'case': case, 'native_address': case * 8, 'observed_gap_cycles': case,
                   'aw_cycle': int(aw['dhi_cycle']), 'w_cycle': int(w['dhi_cycle']),
                   'b_cycle': int(b['dhi_cycle']), 'dhi_write_cycle': int(dhi['dhi_cycle']),
                   'w_to_b_cycles': 1,
                   'b_to_ddr_write_ps': int(pin['time_ps'])-int(b['time_ps']),
                   'w_to_ddr_write_ps': int(pin['time_ps'])-int(w['time_ps']),
                   'pin_bank': case, 'pin_address': 0})
ar, pin_read = event('AR_ACCEPT', 3), event('DDR_PIN_READ', 3)
read = {'ar_cycle': int(ar['dhi_cycle']),
        'ar_to_ddr_read_ps': int(pin_read['time_ps'])-int(ar['time_ps']),
        'r_count': int(summary['r']), 'owner_at_end': int(summary['owner']),
        'timeout_seen': any('REAL_READ_RETURN_NOT_OBSERVED' in line for line in receipt['lines'])}
log = (work / 'handshake.log').read_text(encoding='utf-8')
warning_counts = Counter(re.findall(r'Warning:[^\n]*?\((v[a-z]+-\d+)\)', log))
result = {'scope': 'Real vendor command path only; no DRAM device model',
          'simulation': str(work), 'writes': writes, 'read': read,
          'source_freeze': json.loads((ROOT / 'frozen_check.json').read_text()),
          'warning_counts': dict(warning_counts),
          'phy_ready_time_ps': int(next(e for e in events if e['kind'] == 'PHY_READY')['time_ps']),
          'memory_pass': False, 'commit_proved': False, 'bridge_instantiated': False,
          'limits': ['Window labels are not controller transaction IDs.',
                     'DHI data on request edge is not a data response check.',
                     'An early B cannot prove physical write retirement; ordering is still unspecified.']}
run.helper.save(ROOT / 'analysis.json', result)
print(json.dumps(result, ensure_ascii=False, indent=2))
