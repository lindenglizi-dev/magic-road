"""核对同刺激的 CEA 故障周期；不把周期跟踪当成物理 STA。"""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent / 'v5_vendor_regression_final_traces_20261005'


def rows(name):
    with (RUN / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    old, new = rows('case_01.csv'), rows('case_02.csv')
    assert [row['cycle'] for row in old] == [row['cycle'] for row in new]
    assert old[1037]['advance'] == old[1038]['advance'] == '0'
    assert new[1037]['advance'] == new[1038]['advance'] == '0'
    assert old[1037]['ram_data'] == '2' and old[1038]['ram_data'] == '4'
    assert new[1037]['ram_data'] == new[1038]['ram_data'] == '2'
    assert old[1039]['output_data'] == '4' and new[1039]['output_data'] == '2'
    assert int(old[1038]['time_ns']) - int(old[1037]['time_ns']) == 10000
    traces = []
    for case in range(1, 6):
        path = RUN / f'case_{case:02d}.csv'
        values = rows(path.name)
        assert len(values) > 1039 and len(values[0]) == 18
        traces.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'rows': len(values), 'columns': list(values[0])})
    report = {'passed': True, 'traces': traces,
              'original_fault_window': old[1036:1042], 'candidate_window': new[1036:1042],
              'unit_warning': 'The frozen CSV header time_ns is misleading: %t uses 1ps display precision; values/1000 give ns. 10000 trace units per 10ns cycle.',
              'sampling': 'CSV records at negedge after preceding posedge; fault TB message cycle1040 uses a different monitor counter point.',
              'coverage': 'Five contract traces; full-domain and seed42 coverage are separate assertion logs, not trace files.',
              'physical_timing_evidence': False}
    (HERE / 'cycle_trace_analysis.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'passed': True, 'trace_files': len(traces), 'fault_cycle': 1038}))


if __name__ == '__main__':
    main()
