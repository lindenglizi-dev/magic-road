"""Bounded address and source evidence, not a physical DDR guarantee."""
import run
import json

run.check()
video_bases_native = [0, 7000000, 14000000, 21000000]
video_payload = 1280 * 720 * 3
video_ranges = [[base * 2, base * 2 + video_payload] for base in video_bases_native]
slot_bases = [54525952, 55050240]
slot_ranges = [[base, base + 524288] for base in slot_bases]
assert video_payload == 2764800
assert 512 * 288 * 3 == 442368
assert all(v_end <= start or end <= v_start
           for start, end in slot_ranges for v_start, v_end in video_ranges)
assert slot_ranges[0][1] == slot_ranges[1][0] == 55050240
sources = [
    run.PROJECT / 'cnn/template/design_top_wrapper.v',
    run.PROJECT / 'cnn/template/source_manifest.json',
    run.PROJECT / 'user_source/hdl_source/isp/isp_top.v',
    run.PROJECT / 'cnn/hw_validation/production/reports/ddr_contract_handoff_20261015/C8完整前三层_DDR协议差距交接.txt',
    run.BASE / '唯一视频DDR采集接口方案_2FPS.txt',
    run.PROJECT / 'cnn/hw_validation/production/reports/ddr_visibility_evidence_20261015/PH1P写可见性证据与C8最小服务合同.txt',
]
graph_path = run.PROJECT / 'cnn/hw_validation/production/graph_artifacts/graph.json'
graph = json.loads(graph_path.read_text(encoding='utf-8'))
sources.append(graph_path)
allocations = [{'name': node['name'], **node['storage']} for node in graph['nodes'] if 'storage' in node]
for index, item in enumerate(allocations):
    assert item['end'] == item['base'] + item['allocated_bytes']
    assert graph['memory']['feature_begin'] <= item['base'] < item['end'] <= graph['memory']['feature_end']
    for earlier in allocations[:index]:
        assert item['end'] <= earlier['base'] or earlier['end'] <= item['base']
    for start, end in slot_ranges + video_ranges:
        assert item['end'] <= start or end <= item['base']
assert len(allocations) == 70
pw = next(item for item in allocations if item['name'] == 'down2.pw.conv')
assert pw['base'] == 0x035B4000
old_pw = [0x03600000, 0x03600000 + 221184]
old_overlap = [item['name'] for item in allocations
               if old_pw[0] < item['end'] and item['base'] < old_pw[1]]
run.save(run.ROOT / 'graph_address_ledger.json', {
    'graph_sha256': run.sha(graph_path), 'physical_allocations': allocations,
    'view_or_alias_nodes': [node for node in graph['nodes'] if 'allocation' in node or 'storage_alias' in node],
    'all_distinct_physical_allocations_disjoint': True,
    'liveness_reuse': False,
    'alias_lifecycle': 'split/concat are views, residual storage_alias requires read-before-in-place-write and completed producer; live scheduler not implemented here',
    'old_diagnostic_pw_range': old_pw, 'old_range_overlaps_graph_allocations': old_overlap,
    'old_diagnostic_cannot_be_wired_into_graph_unchanged': True,
    'single_conversion_boundary': 'component bases remain byte addresses; only future sole PAXI service converts byte >> 1 once',
    'actual_scheduler_alias_and_visibility_verified': False,
})
run.save(run.ROOT / 'interface_evidence.json', {
    'status': 'STATIC_NORMAL_PAYLOAD_DISJOINT_NOT_RUNTIME_DMA_APPROVAL',
    'source_sha256': {str(path): run.sha(path) for path in sources},
    'video_normal_payload_byte_ranges_half_open': video_ranges,
    'cnn_slot_byte_ranges_half_open': slot_ranges,
    'slot_payload_bytes': 442368,
    'normal_highest_video_to_cnn_gap_bytes': slot_bases[0] - video_ranges[-1][1],
    'native_address_rule': 'byte >> 1; 16-byte beat advances native address by 8',
    'runtime_address_guard_verified': False,
    'whole_reserved_video_bank_disjoint_claim': False,
    'real_paxi_visibility_verified': False,
    'shared_reset_late_response_drain_verified': False,
    'external_event_scope': 'component TB supplies write_visible and last_read_consumed facts',
    'input_contract': 'AWB96 high lane first; 320 beats per row; ordinary reference gap480 clocks',
    'performance_budget': {'clock_hz': 100000000, 'minimum_cnn_fps': 2,
                           'whole_result_cycles': 50000000, 'expire_age_ms': 500,
                           'one_fps_fallback_cycles_not_approved_threshold_change': 100000000,
                           'previous_frontend_cycles': 15848967,
                           'cycles_left_after_frontend_only': 34151033},
})
print('INTERFACE_STATIC_LEDGER_PASS; real DDR integration remains unverified', flush=True)
