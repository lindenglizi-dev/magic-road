"""Collect source-bound diagnostic evidence; never relabel strict failures."""
import difflib
import json
import re
from pathlib import Path
import run

run.check()
identity = json.loads((run.ROOT / 'verification/identity_attempt2/receipt.json').read_text(encoding='utf-8'))
overlay = json.loads((run.ROOT / 'verification/overlay_attempt3/receipt.json').read_text(encoding='utf-8'))
for receipt in (identity, overlay):
    assert receipt['status'] == 'PASS'
    assert all(run.sha(path) == digest for path, digest in receipt['sources'].items())
    assert all(run.sha(path) == digest for path, digest in receipt['tools'].items())
before = run.ROOT / 'retained_before_attributes/road_source_sof_identity.v'
after = run.ROOT / 'rtl/road_source_sof_identity.v'
old_text = before.read_text(encoding='utf-8')
new_text = after.read_text(encoding='utf-8')
normalize = lambda text: ''.join(re.sub(r'\(\* ASYNC_REG = "TRUE" \*\)', '', text).split())
assert normalize(old_text) == normalize(new_text)
assert new_text.count('(* ASYNC_REG = "TRUE" *)') == 6
run.save(run.ROOT / 'attribute_only_receipt.json', {
    'before': run.sha(before), 'after': run.sha(after), 'sync_chain_attributes': 6,
    'equal_after_removing_only_attributes_and_whitespace': True,
    'diff': ''.join(difflib.unified_diff(old_text.splitlines(True), new_text.splitlines(True)))})
gates = {}
for name in ('road_source_sof_identity', 'road_age_overlay'):
    report_path = run.ROOT / 'gate_attempt2' / (name + '.json')
    report = json.loads(report_path.read_text(encoding='utf-8'))
    gates[name] = {'raw_report': str(report_path.relative_to(run.ROOT)),
                   'raw_report_sha256': run.sha(report_path),
                   'errors': report['errors'], 'strict_warnings': report['strict_warnings'],
                   'delivery_ready': report['delivery_ready'],
                   'checks': {n: r['status'] for n, r in report['checks'].items()},
                   'rules': {code: sum(x.get('code') == code for x in report['issues'])
                             for code in sorted({x.get('code') for x in report['issues']})}}
run.save(run.ROOT / 'component_results.json', {
    'state': 'DIAGNOSTIC_FUNCTIONAL_PASS_STRICT_AND_PHYSICAL_NOT_CLOSED',
    'identity': identity, 'overlay': overlay, 'strict_gates': gates,
    'sequential_declaration_bits': {'identity': 536, 'overlay': 67, 'sum': 603,
        'boundary': 'manual source-level sequential state tally, not mapped registers/Slice; excludes existing timer, table/publisher and capture'},
    'resources': {'Slice': 'NOT_MEASURED', 'DSP': 'NOT_MEASURED', 'ERAM': 'NOT_MEASURED',
        'intent': 'no new memory arrays or variable multipliers; constant divider/glyph mapping still requires actual TD'},
    'physical': {'TD': 'NOT_RUN', 'CDC_MTBF_bundled_timing': 'NOT_SIGNED_OFF'},
    'production_or_board_changes': False,
    'source_frame_id_scope': 'every observed AWB reconstructed SOF incl application skips; malformed CSI/exposure mapping NOT_PROVED',
    'same_origin_time': 'frozen existing road_time_snapshot.o_src_now_ms; no second absolute timer',
    'new_demo_age_limit_ms': 2000, 'old_age_limit_readonly_ms': 500,
    'remaining': ['actual credit/slot metadata binding', 'full pixel DMA and verified DDR visibility',
                  'real table/publisher/overlay joint integration', 'physical resource/timing/CDC',
                  'full-network throughput and real-model precision']})
run.save(run.ROOT / 'source_manifest.json', {
    'candidate_rtl': {str(p.relative_to(run.ROOT)): run.sha(p) for p in (run.ROOT / 'rtl').glob('*.v')},
    'reused_time_rtl': {str(run.BASE / 'rtl/road_time_snapshot.v'): run.sha(run.BASE / 'rtl/road_time_snapshot.v')},
    'is_production_top': False, 'C9_publisher_not_reimplemented': True,
    'clock_domains': {'time': '100MHz unique absolute counter', 'AWB': 'configured nominal60MHz recovered MIPI byte clock',
                      'HDMI': '75MHz PLL C4; overlay one-pixel latency'}})
for directory in (run.BASE, run.ROOT.parent / 'camera_capture_2fps_20261015'):
    baseline = json.loads((directory / 'artifact_hashes.json').read_text(encoding='utf-8'))
    changed = [name for name, digest in baseline.items() if run.sha(directory / name) != digest]
    run.save(run.ROOT / (directory.name + '_guard.json'), {'checked': len(baseline), 'changed': changed})
    assert not changed
run.check()
run.save(run.ROOT / 'status.json', {'phase': 'HANDOFF_READY_DIAGNOSTIC_ONLY',
    'functional_cases_passed': 2, 'strict_pass': False, 'physical_pass': False,
    'production_modified': False, 'training_started': False, 'bitstream_or_board_or_flash': False})
paths = sorted(p for p in run.ROOT.rglob('*') if p.is_file() and p.name != 'artifact_hashes.json')
run.save(run.ROOT / 'artifact_hashes.json', {str(p.relative_to(run.ROOT)): run.sha(p) for p in paths})
print('SOURCE_SOF_HANDOFF', len(paths), 'artifacts; strict/physical remain unclosed')
