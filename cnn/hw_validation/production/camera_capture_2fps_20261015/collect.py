"""Collect current component evidence without rerunning completed simulations."""
import json
from collections import Counter
from pathlib import Path
import run

run.check()
receipts = {}
failures = []
for path in sorted((run.ROOT / 'verification').glob('*/receipt.json')):
    item = json.loads(path.read_text(encoding='utf-8'))
    previous = receipts.get(item['case'])
    if previous is None or path.stat().st_mtime > Path(previous['path']).stat().st_mtime:
        receipts[item['case']] = {'path': str(path), **item}
for item in receipts.values():
    for relative, digest in item['compiled_source_sha256'].items():
        assert run.sha(run.ROOT / relative) == digest, (relative, item['path'])
    for relative, digest in item['input_vector_sha256'].items():
        assert run.sha(run.ROOT / relative) == digest, (relative, item['path'])
    for absolute, digest in item['vendor_source_sha256'].items():
        assert run.sha(absolute) == digest, (absolute, item['path'])
for path in sorted((run.ROOT / 'verification').glob('*/failure.json')):
    failures.append({'path': str(path), **json.loads(path.read_text(encoding='utf-8'))})
assert set(receipts) == {0, 1, 2, 3, 4, 10, 11, 12, 13}, sorted(receipts)
for index in (0, 1, 2):
    assert receipts[index]['output_pixels'] == 147456
    assert receipts[index]['output_bytes'] == 442368
    assert receipts[index]['frame_error_cycles'] == 0
assert receipts[4]['frame_error_cycles'] == 1 and receipts[4]['output_pixels'] == 0
gates = {}
for name in ('road_area_resize', 'road_capture_slots'):
    paths = sorted(run.ROOT.glob('gate*/' + name + '.json'), key=lambda path: path.stat().st_mtime)
    path = paths[-1]
    item = json.loads(path.read_text(encoding='utf-8'))
    gates[name] = {'path': str(path), 'errors': item['errors'], 'strict_warnings': item['strict_warnings'],
                   'delivery_ready': item['delivery_ready'],
                   'checks': {key: value['status'] for key, value in item['checks'].items()},
                   'diagnostics_by_rule': item['delivery_issues_by_rule']}
old_frozen = json.loads((run.BASE / 'frozen.json').read_text(encoding='utf-8'))
old_changed = [path for path, digest in old_frozen.items() if run.sha(path) != digest]
assert not old_changed, old_changed
run.save(run.ROOT / 'component_results.json', {
    'stage': 'COMPONENT_FUNCTIONAL_PASS_NOT_INTEGRATED_OR_PHYSICAL',
    'receipts': receipts, 'retained_failed_attempts': failures,
    'strict_gates': gates,
    'old_baseline_readonly_check': {'checked': len(old_frozen), 'changed': old_changed},
    'numeric_contract': {'horizontal_max': 1275, 'vertical_max': 6375,
                         'final_rounding': 'RNE once after divide25',
                         'constant_divide_exhaustive_pass': all(((value + 12) * 10486 >> 18) == (value + 12) // 25 for value in range(6376))},
    'resource_scope': {'explicit_eram_instances': 2, 'record_fifo_bits': 128 * 67,
                        'mapped_eram': None, 'mapped_slice': None, 'mapped_dsp': None,
                        'fits_shared_D_budget': 'UNMEASURED'},
    'real_ddr_visible': False, 'physical_started': False, 'bitstream': False,
    'clock_fixture_hz': 100000000,
    'budget_cycles': {'two_fps': 50000000, 'one_fps_fallback': 100000000,
                      'expire_age_ms_unchanged': 500},
})
run.save(run.ROOT / 'status.json', {
    'stage': 'COMPONENT_FUNCTIONAL_PASS_NOT_INTEGRATED_OR_PHYSICAL',
    'scaler_full_frames_passed': 3, 'scaler_error_recovery_cases_passed': 2,
    'slot_regression_passed': 4, 'strict_gate_closed': False,
    'real_ddr_visible': False, 'physical_started': False, 'bitstream': False,
    'next': 'prepare complete detection-table CDC contract; physical queue and real PAXI visibility remain separate',
})
hashes = {str(path.relative_to(run.ROOT)): run.sha(path)
          for path in run.ROOT.rglob('*') if path.is_file()
          and not any(part in ('work', '__pycache__') for part in path.relative_to(run.ROOT).parts)
          and path.name not in ('artifact_hashes.json', 'modelsim.ini', 'vsim.wlf')}
run.save(run.ROOT / 'artifact_hashes.json', hashes)
print({'functional_cases': len(receipts), 'retained_failures': len(failures),
       'gates': {name: (item['errors'], item['strict_warnings']) for name, item in gates.items()},
       'old_checked': len(old_frozen), 'artifacts': len(hashes)}, flush=True)
