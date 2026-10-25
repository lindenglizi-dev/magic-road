"""Observe the frozen passing count TB once; do not edit DUT or test stimulus."""
import importlib.util
import json
from pathlib import Path
import run

run.check()
manifest = json.loads((run.ROOT / 'verification/suite_manifest.json').read_text(encoding='utf-8'))
for relative, digest in manifest['frozen_sha256'].items():
    assert run.sha(run.ROOT / relative) == digest, relative
work = run.fresh('endpoint_observation')
spec = importlib.util.spec_from_file_location('frozen_verification', run.ROOT / 'verification/run_verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)
metadata, payload, diagnostics, diagnostic_payload = verify.materialize_reference_vectors(work)
run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
sources = [run.ROOT / 'rtl/road_detection_table_cdc.v', run.ROOT / 'tests/tb_road_detection_table_cdc.v']
run.command([run.MSIM / 'vlog.exe', '-work', 'work', *sources], work, 'vlog')
output = run.command([run.MSIM / 'vsim.exe', '-c', '-t', '1ps', '-voptargs=+acc', '-lib', 'work',
                      'tb_road_detection_table_cdc', '+CASE=10', '+TABLE_META=' + metadata.name,
                      '+TABLE_ENTRIES=' + payload.name, '+DIAG_META=' + diagnostics.name,
                      '+DIAG_ENTRIES=' + diagnostic_payload.name, '-do', run.ROOT / 'observe_endpoints.do'],
                     work, 'vsim')
assert 'TB_PASS_TABLE case=10' in output
codes, state, updates = {}, {}, {}
timestamp, entries, rows = 0, [], []
current = None


def number(value):
    return int(value, 2) if value and all(bit in '01' for bit in value) else None


def flush():
    global current, entries
    prior = dict(state)
    state.update(updates)
    def val(name):
        return number(state.get(name))
    def old(name):
        return number(prior.get(name))
    def rise(name):
        return old(name) == 0 and val(name) == 1
    if rise('i_src_clk'):
        if old('i_src_entry_valid') == 1 and old('o_src_entry_ready_500') == 1:
            entries.append(timestamp)
        if old('i_src_meta_valid') == 1 and old('o_src_meta_ready_500') == 1:
            assert current is None
            count = (old('i_src_metadata') >> 128) & 127
            assert count == len(entries), (count, entries)
            current = {'count': count, 'seal_ps': timestamp, 'preload_accepts': count,
                       'first_entry_ps': entries[0] if entries else None,
                       'last_entry_ps': entries[-1] if entries else None}
            entries = []
    if current is not None:
        if rise('o_dst_copy_busy_500'):
            current['copy_start_ps'] = timestamp
        if old('o_dst_copy_busy_500') == 1 and val('o_dst_copy_busy_500') == 0:
            current['copy_end_ps'] = timestamp
        if rise('o_dst_pending_valid_500'):
            current['pending_ps'] = timestamp
        if rise('o_src_copy_ack_500'):
            current['ack_ps'] = timestamp
        if rise('o_dst_update_500'):
            current['active_ps'] = timestamp
            current['seal_to_ack_ps'] = current['ack_ps'] - current['seal_ps']
            current['pending_to_active_ps'] = timestamp - current['pending_ps']
            if current['count']:
                current['copy_busy_ps'] = current['copy_end_ps'] - current['copy_start_ps']
                assert current['copy_busy_ps'] == current['count'] * 13334
            else:
                current['copy_busy_ps'] = 0
            rows.append(current)
            current = None
    updates.clear()


with (work / 'endpoints.vcd').open(encoding='utf-8') as stream:
    for line in stream:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == '$var':
            codes[parts[3]] = parts[4]
        elif line.startswith('#'):
            flush()
            timestamp = int(line[1:])
        elif line[0] in '01xz':
            code = line.strip()[1:]
            if code in codes:
                updates[codes[code]] = line[0]
        elif line[0] in 'bB':
            if parts[1] in codes:
                updates[codes[parts[1]]] = parts[0][1:]
    flush()
assert [row['count'] for row in rows] == [0, 1, 32, 33, 64], rows
result = {'scope': 'observed frozen real DUT/TB outputs; no forced signals or changed stimulus',
          'timescale': '1ps', 'clock_period_ps': {'source': 10000, 'destination': 13334},
          'rows': rows, 'compiled_source_sha256': {str(path): run.sha(path) for path in sources},
          'observer_sha256': run.sha(run.ROOT / 'observe_endpoints.do'),
          'vcd_sha256': run.sha(work / 'endpoints.vcd')}
run.save(work / 'measurement.json', result)
run.save(run.ROOT / 'endpoint_measurement_receipt.json', {'path': str(work / 'measurement.json'),
                                                       'sha256': run.sha(work / 'measurement.json')})
run.check()
print(rows, flush=True)
