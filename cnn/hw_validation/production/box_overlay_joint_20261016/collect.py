"""Bind completed display evidence without promoting diagnostic passes to delivery."""
import json
from collections import Counter
import run


def read(relative):
    return json.loads((run.ROOT / relative).read_text(encoding='utf-8'))


def main():
    run.check()
    verification = read('verification/summary.json')
    assert verification['status'] == 'PASS_FUNCTIONAL_MODELSIM'
    assert verification['main_frames'] == 18 and verification['source_unchanged']
    assert verification['tools_unchanged']
    for path, digest in verification['current_verification_source_hashes'].items():
        assert run.sha(path) == digest, path
    review = read('review.json')
    for path, digest in review['source_sha256'].items():
        assert run.sha(run.ROOT / path) == digest, path
    assert not review['confirmed_rtl_defects']
    official = read('timing_probe/attempt_attempt2/receipt.json')
    assert official['status'] == 'PASS'
    for group in ('source_hashes', 'tools'):
        for path, digest in official[group].items():
            assert run.sha(path) == digest, path
    gate_hashes = read('gate_attempt3/source_hashes.json')
    for path, digest in gate_hashes.items():
        assert run.sha(path) == digest, path
    gates = {}
    for name in ('road_box_line_overlay', 'road_box_age_overlay'):
        path = 'gate_attempt3/' + name + '.json'
        report = read(path)
        gates[name] = {
            'report': path, 'report_sha256': run.sha(run.ROOT / path),
            'errors': report['errors'], 'strict_warnings': report['strict_warnings'],
            'delivery_ready': report['delivery_ready'],
            'checks': {key: value['status'] for key, value in report['checks'].items()},
            'rule_counts': dict(Counter(item['code'] for item in report['issues']))}
    old = read('../source_sof_identity_20261015/artifact_hashes.json')
    changed = [path for path, digest in old.items() if run.sha(run.BASE / path) != digest]
    run.save(run.ROOT / 'source_identity_guard.json', {'checked': len(old), 'changed': changed})
    assert not changed
    publisher = run.ROOT.parent / 'result_publish_joint_20261015'
    records = json.loads((publisher / 'frozen_dependencies.json').read_text(encoding='utf-8'))['files']
    changed = [path for item in records for path in (item['source'], item['copy'])
               if run.sha(path) != item['sha256']]
    run.save(run.ROOT / 'publisher_guard.json', {'records': len(records), 'changed': changed})
    assert not changed
    candidate = {str(path.relative_to(run.ROOT)): run.sha(path)
                 for path in sorted((run.ROOT / 'rtl').glob('*.v'))}
    run.save(run.ROOT / 'source_manifest.json', {
        'candidate_rtl': candidate, 'frozen_dependencies': read('frozen.json'),
        'display_synth_rtl': [str(run.ROOT / 'rtl/road_box_line_overlay.v'),
                              str(run.BASE / 'rtl/road_age_overlay.v'),
                              str(run.ROOT / 'rtl/road_box_age_overlay.v')],
        'native_cell': 'PH1P_LOGIC_DRAM; synthesis uses official TD library, not static vendor_interface.v',
        'frozen_dependency_list_is_not_synthesis_file_list': True,
        'interfaces_sha256': run.sha(run.ROOT / 'interfaces.json'),
        'verification_receipt': 'verification/summary.json',
        'verification_receipt_sha256': run.sha(run.ROOT / 'verification/summary.json'),
        'strict_gate_source_hashes': gate_hashes,
        'production_modified': False, 'pixel_clock_MHz': 75, 'video_registers': 2,
        'native_memory': 'PH1P_LOGIC_DRAM 1280x18 asynchronous read; runtime clear',
        'static_interface_is_not_simulation_model': True})
    run.save(run.ROOT / 'component_results.json', {
        'state': 'FUNCTIONAL_PASS_STRICT_AND_PHYSICAL_OPEN',
        'verification': verification, 'official_video_probe': official, 'strict_gates': gates,
        'review': 'review.json', 'review_sha256': run.sha(run.ROOT / 'review.json'),
        'normal_line': {'scan': 320, 'observed_DEfall_to_ready_samples': 323,
                        'official_blank_samples': 370, 'functional_margin_samples': 47},
        'startup': {'clear_plus64_scan_measured': 1601,
                    'SOF_to_DE_transition': 39970, 'SOF_to_first_pixel_consumption': 39971},
        'sequential_bits_manual': {'renderer': 160, 'raw_shadow': 48, 'reused_AGE': 67,
                                   'total': 275, 'new_beyond_AGE': 208, 'mapped': False},
        'resource_intent_not_measurement': {'line_map_bits': 23040,
            'ideal_storage_capacity_Slice_lower_bound': 360, 'Slice_target': 600,
            'new_DSP_target': 0, 'new_ERAM_target': 0,
            'actual_Slice_DSP_ERAM': 'NOT_MEASURED', 'setup_hold': 'NOT_RUN'},
        'limits': {'no_fourth_full_table': True, 'one_active_async_read_port': True,
                   'real7_starts_saved_HEAD112_not_complete_CNN': True,
                   'injected_geometry_not_recognition_demo': True,
                   'PTQ_diagnostic_not_QAT_accuracy_acceptance': True},
        'python_and_script_strict_skill': 'UNAVAILABLE_NOT_CLAIMED_PASS',
        'production_training_TD_bitstream_board_Flash': 'NOT_CHANGED_OR_RUN'})
    run.save(run.ROOT / 'status.json', {
        'phase': 'HANDOFF_READY_DIAGNOSTIC_ONLY', 'functional_pass': True,
        'main_fullframes': 18, 'strict_pass': False, 'physical_pass': False,
        'production_modified': False, 'training_started': False,
        'TD_bitstream_board_Flash': False})
    run.check()
    paths = sorted(path for path in run.ROOT.rglob('*')
                   if path.is_file() and path.name != 'artifact_hashes.json')
    run.save(run.ROOT / 'artifact_hashes.json', {
        str(path.relative_to(run.ROOT)): run.sha(path) for path in paths})
    print('BOX_DISPLAY_HANDOFF', len(paths), 'artifacts; strict and physical remain open')


if __name__ == '__main__':
    main()
