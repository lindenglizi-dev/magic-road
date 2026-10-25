"""Check S1 final test closure and compare the same full-frontend endpoint window."""
import json
import run


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    root = run.ROOT
    run.check()
    cases = {}
    for path in sorted((root / 'verification').glob('*/receipt.json')):
        item = load(path)
        if 'compiled_source_sha256' in item:
            cases[item['case']] = (path, item)
    assert set(cases) == set(range(10)), 'All original eight and two load-stall cases required'
    for _, item in cases.values():
        assert item['result'].startswith('PASS_')
        assert all(run.sha(root / p) == h for p, h in item['compiled_source_sha256'].items())
        assert all(run.sha(root / 'vectors' / p) == h for p, h in item['input_vector_sha256'].items())
        if item['case'] in (0, 1, 2, 3, 8, 9):
            assert (item['writes'], item['reads'], item['output_bytes'], item['halo_accepts']) == (78336, 97564, 221184, 1306368)
            assert item['acc_pre_silu_post'] == [958464] * 4
            assert sum(item['cycle_bins']) == item['cycles']
    old = load(run.BASE / 'verification/normal_20261015_161531_547383/receipt.json')
    normal = cases[0][1]
    reference = load(root / 'reference_s1.json')
    saved = old['cycles'] - normal['cycles']
    assert normal['cycles'] == reference['expected_normal_cycles'] == 15848967
    assert saved == reference['saved_mapping_state_cycles'] == 1403112
    differences = [a - b for a, b in zip(old['cycle_bins'], normal['cycle_bins'])]
    assert differences == [0, 0, 0, saved, 0, 0, 0, 0, 0, 0]
    assert cases[8][1]['cycles'] == normal['cycles'] + 257
    assert cases[9][1]['cycles'] == normal['cycles']
    assert not list((root / 'implementation').glob('td*')) and not list(root.rglob('*.bit'))
    original_gate = load(root / 'gate_original/rtl.json')
    candidate_gate = load(root / 'gate_candidate/rtl.json')
    tb_gate = load(root / 'verification/tb_gate.json')
    keys = ('errors', 'strict_warnings', 'delivery_ready')
    summary = {'stage': 'S1_FUNCTIONAL_PASS_PHYSICAL_PREPARED_NOT_RUN', 'baseline': str(run.BASE),
        'candidate': str(root), 'changed_rtl': 'rtl/road_stem_ddr_sequence.v',
        'reference': reference, 'normal_old_cycles': old['cycles'], 'normal_new_cycles': normal['cycles'],
        'saved_state_cycles': saved, 'saved_percent': saved / old['cycles'] * 100,
        'exclusive_bin_reduction': differences, 'normal_cycle_bins': normal['cycle_bins'],
        'ddr_reads_removed': 0, 'ddr_writes_removed': 0, 'read_requests': normal['reads'],
        'write_accept_responses': normal['writes'], 'pw_bytes': normal['output_bytes'],
        'cases': [{'receipt': str(path), 'case': item['case'], 'result': item['result'], 'cycles': item['cycles']}
                  for path, item in cases.values()],
        'rtl_gate_before': {k: original_gate[k] for k in keys},
        'rtl_gate_after': {k: candidate_gate[k] for k in keys},
        'testbench_gate': {k: tb_gate[k] for k in keys},
        'public_gates': {label: {k: v.get('status') for k, v in gate['checks'].items() if isinstance(v, dict)}
                         for label, gate in (('rtl', candidate_gate), ('testbench', tb_gate))},
        'strict_delivery_pass': False,
        'physical_preparation': load(root / 'physical_preparation.json'),
        'physical_run': False, 'new_resource_or_timing_result': None, 'bitstream_generated': False,
        'board_run': False, 'production_modified': False, 'training_started': False,
        'interfaces': '接口与功能自检边界.txt',
        'limits': ['TEST_ONLY parameters; no accuracy claim', 'Controlled memory, not real DDR board proof',
                   'First three layers only, no whole-network 5FPS', 'W accepted is not visible/commit',
                   'Single client and whole reset only', 'Fixed diagnostic frontend is not yet a generic tile DMA']}
    run.save(root / 'comparison.json', summary)
    run.save(root / 'status.json', {'stage': summary['stage'], 'comparison': str(root / 'comparison.json'),
        'handoff': str(root / 'S1执行结果与集成交接.txt'), 'physical_started': False,
        'bitstream_generated': False, 'board_run': False, 'strict_delivery_pass': False})
    manifest = [p for p in root.iterdir() if p.is_file() and p.suffix in ('.py', '.json', '.txt', '.v')
                and p.name != 'artifact_hashes.json']
    for folder in ('rtl', 'reused', 'build', 'tests', 'vectors', 'specifications'):
        manifest.extend(p for p in (root / folder).rglob('*') if p.is_file())
    manifest += [p for p in (root / 'verification').iterdir() if p.is_file()]
    manifest += [root / 'implementation/source_hashes.json']
    run.save(root / 'artifact_hashes.json', {str(p): run.sha(p) for p in manifest})
    run.check()
    print(json.dumps({'normal_old': old['cycles'], 'normal_s1': normal['cycles'], 'saved': saved, 'cases': len(cases)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
