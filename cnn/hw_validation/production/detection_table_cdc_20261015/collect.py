"""Final read-only closure checks and bounded component handoff receipts."""
import json
from pathlib import Path
import run

run.check()
manifest_path = run.ROOT / 'verification/suite_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for relative, digest in manifest['frozen_sha256'].items():
    assert run.sha(run.ROOT / relative) == digest, relative
receipts = []
for case in manifest['final_cases']:
    path = run.ROOT / 'verification' / case['receipt']
    receipt = json.loads(path.read_text(encoding='utf-8'))
    assert receipt['case'] == case['case'] and receipt['result'] == case['result']
    assert run.sha(run.ROOT / 'verification/run_verify.py') == receipt['runner_sha256']
    for field in ('compiled_source_sha256', 'reference_sha256', 'specification_sha256'):
        for relative, digest in receipt[field].items():
            assert run.sha(run.ROOT / relative) == digest, (relative, path)
    receipts.append({'path': str(path), **receipt})
assert {item['case'] for item in receipts} == {0, 1, 10, 11, 12, 13, 14, 20}
old_checks = []
for root, filename in ((run.BASE, 'artifact_hashes.json'), (run.BASE, 'frozen.json'),
                       (run.BASE.parent / 'frontend_rgb_reuse_20261015', 'frozen.json')):
    hashes = json.loads((root / filename).read_text(encoding='utf-8'))
    changed = [name for name, digest in hashes.items()
               if run.sha(root / name if filename == 'artifact_hashes.json' else name) != digest]
    assert not changed, changed
    old_checks.append({'root': str(root), 'manifest': filename, 'checked': len(hashes), 'changed': changed})
gates = {}
for name in ('road_time_snapshot', 'road_detection_table_cdc'):
    paths = sorted(run.ROOT.glob('gate*/' + name + '.json'), key=lambda path: path.stat().st_mtime)
    path = paths[-1]
    item = json.loads(path.read_text(encoding='utf-8'))
    source_hashes = json.loads((path.parent / 'source_hashes.json').read_text(encoding='utf-8'))
    assert source_hashes[str(run.ROOT / 'rtl' / (name + '.v'))] == run.sha(run.ROOT / 'rtl' / (name + '.v'))
    gates[name] = {'path': str(path), 'errors': item['errors'], 'strict_warnings': item['strict_warnings'],
                   'delivery_ready': item['delivery_ready'], 'rules': item['delivery_issues_by_rule'],
                   'static_checks': {key: value['status'] for key, value in item['checks'].items()}}
observer = json.loads((run.ROOT / 'endpoint_measurement_receipt.json').read_text(encoding='utf-8'))
assert run.sha(observer['path']) == observer['sha256']
measurement = json.loads(Path(observer['path']).read_text(encoding='utf-8'))
for path, digest in measurement['compiled_source_sha256'].items():
    assert run.sha(path) == digest
tools = {name: {'path': str(run.MSIM / (name + '.exe')), 'sha256': run.sha(run.MSIM / (name + '.exe'))}
         for name in ('vlib', 'vlog', 'vsim')}
run.save(run.ROOT / 'component_results.json', {
    'stage': 'FUNCTIONAL_CDC_PASS_STRICT_GATE_NOT_CLOSED_PHYSICAL_NOT_RUN',
    'frozen_sha256': manifest['frozen_sha256'], 'cases': receipts,
    'strict_rtl_gates': gates, 'functional_gate_evidence': str(manifest_path),
    'observer': observer, 'real_seal_to_ack': measurement['rows'],
    'old_baseline_checks': old_checks, 'tool_binaries': tools,
    'resource': {'table_payload_bits': 3 * 97 * 64, 'table_metadata_bits': 3 * 265,
                 'time_held_payload_bits': 96, 'mapped_slice': None, 'mapped_dsp': None,
                 'mapped_eram': None, 'memory_mapping_intent': 'LUTRAM, not forced or physically verified'},
    'clock_evidence': str(run.ROOT / 'clock_evidence.json'),
    'real_camera_sof_timestamp_bound': False, 'physical_cdc_signed_off': False,
    'timing_signed_off': False, 'real_ddr_visible': False, 'bitstream': False,
    'default_expire_ms': 500, 'comparison_only_expire_ms': 2000,
    'new_bitstreams_generated': 0, 'end_to_end_cnn_fps_measured': None,
})
run.save(run.ROOT / 'source_manifest.json', {
    'scope': 'one time snapshot and one three-table module; not a deployment top',
    'synthesis_sources': [{'path': str(run.ROOT / 'rtl' / name), 'sha256': run.sha(run.ROOT / 'rtl' / name)}
                          for name in ('road_time_snapshot.v', 'road_detection_table_cdc.v')],
    'required_clocks_hz': {'i_src_clk': 100000000, 'i_dst_clk': 75000000},
    'common_reset': 'i_rstn common assertion; each module locally synchronizes release',
    'deployment_parameters': {'AGE_LIMIT_MS': 500, 'EXPECTED_MODEL_ID': '0xB35D4A66'},
    'expected_full_payload_sha256': 'b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145',
    'model_id_filter_is_not_rom_integrity_proof': True,
    'test_only_sources': ['tests/tb_road_time_snapshot.v', 'tests/tb_road_detection_table_cdc.v',
                          'tests/tb_time_table_integrated.v'],
    'exclude_from_synthesis': ['retained_before_age_invalid/', 'reference/', 'verification/', 'tests/'],
    'duplicate_table_or_time_instances_for_2000ms_in_tb_are_not_deployment': True,
})
run.save(run.ROOT / 'status.json', {
    'stage': 'FUNCTIONAL_CDC_PASS_STRICT_GATE_NOT_CLOSED_PHYSICAL_NOT_RUN',
    'formal_cases_passed': 8, 'observer_case_passed': 1,
    'strict_gate_closed': False, 'physical_started': False, 'bitstream': False,
    'camera_sof_binding': 'C7_PENDING', 'real_ddr_visible': False,
    'next': 'single actual integrated top and physical CDC/RAM/timing review scheduled by C7',
})
hashes = {str(path.relative_to(run.ROOT)): run.sha(path)
          for path in run.ROOT.rglob('*') if path.is_file()
          and not any(part in ('work', '__pycache__') for part in path.relative_to(run.ROOT).parts)
          and path.name not in ('artifact_hashes.json', 'modelsim.ini', 'vsim.wlf')}
run.save(run.ROOT / 'artifact_hashes.json', hashes)
print({'formal_cases': len(receipts), 'observer_cases': 1, 'artifacts': len(hashes),
       'old_checked': [item['checked'] for item in old_checks],
       'strict_errors': {name: item['errors'] for name, item in gates.items()}}, flush=True)
