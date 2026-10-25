"""Freeze source inputs and render the confirmed SRIF1 specifications."""
import json
import sys
import run

contract = json.loads((run.ROOT / 'interfaces.json').read_text(encoding='utf-8'))
if not (run.ROOT / 'frozen.json').exists():
    paths = [run.BASE / 'artifact_hashes.json', run.BASE / 'component_results.json',
             run.BASE / 'verification/suite_manifest.json',
             run.PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015/连续视频1FPS目标与第四批任务_20261015.txt',
             run.PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015/后处理共享RAM与接口约定_20261015.txt',
             run.PROJECT / 'cnn/spec/integration_contract.md',
             run.PROJECT / 'cnn/template/design_top_wrapper.v',
             run.PROJECT / 'user_source/ip_source/PLL/PLL.v']
    paths += list((run.BASE / 'rtl').glob('*'))
    run.save(run.ROOT / 'frozen.json', {str(path): run.sha(path) for path in paths if path.is_file()})
    run.save(run.ROOT / 'reused_sources.json', {})
run.check()
baseline = json.loads((run.BASE / 'artifact_hashes.json').read_text(encoding='utf-8'))
changed = [name for name, digest in baseline.items() if run.sha(run.BASE / name) != digest]
run.save(run.ROOT / 'capture_baseline_guard.json', {'checked': len(baseline), 'changed': changed,
                                                  'manifest_sha256': run.sha(run.BASE / 'artifact_hashes.json')})
assert not changed, changed
pll = run.PROJECT / 'user_source/ip_source/PLL/PLL.v'
pll_text = pll.read_text(encoding='utf-8')
assert 'C0        \t| 100.000000' in pll_text and 'C4        \t| 75.000000' in pll_text
run.save(run.ROOT / 'clock_evidence.json', {
    'template_sha256': run.sha(run.PROJECT / 'cnn/template/design_top_wrapper.v'),
    'pll_source': str(pll), 'pll_sha256': run.sha(pll),
    'source': 'PLL.clk0_out -> S_100m_clk', 'source_nominal_hz': 100000000,
    'destination': 'PLL.clk4_out -> S_hdmi_pixel_clk', 'destination_nominal_hz': 75000000,
    'pll_reference_nominal_hz': 50000000, 'feedback_div': 2,
    'source_output_div': 15, 'destination_output_div': 20,
    'actual_board_frequency_measured': False,
    'source_ms_divisor': 100000, 'watchdog_destination_cycles': 150000,
    'snapshot_bound_assumptions': 'both clocks active at configured PLL ratio; digital synchronizer behavior; physical MTBF/bundled timing unverified',
})
for key in ('time', 'table'):
    item = contract[key]
    name = item['module']
    timing = ([
        {'name': 'dst_clk', 'wave': 'p.......'},
        {'name': 'request', 'wave': '01......'},
        {'name': 'req_meta', 'wave': '0.1.....'},
        {'name': 'req_sync', 'wave': '0..1....'},
        {'name': 'capture_pending', 'wave': '0...10..'},
        {'name': 'capture_ack', 'wave': '0....1..'},
        {'name': 'held_payload', 'wave': '=.......', 'data': ['epoch,time held']}
    ] if key == 'time' else [
        {'name': 'dst_clk', 'wave': 'p.........'},
        {'name': 'copy_enable', 'wave': '1..0..1...'},
        {'name': 'copy_index', 'wave': '===...==..', 'data': ['0','1','2','3','last']},
        {'name': 'SOF', 'wave': '0......101'},
        {'name': 'pending_valid', 'wave': '0.......10'},
        {'name': 'active_update', 'wave': '0........1'}
    ])
    module = {
        'name': name, 'feature': 'detection_table_cdc', 'rtl_path': name + '.v',
        'description': '独立同源时间冻结快照' if key == 'time' else '三表完整64框跨域与SOF发布',
        'interfaces': {'ports': [dict(name=n, direction='input' if n.startswith('i_') else 'output',
                                     width=w, role=n, description=n)
                                 for n, w in item['ports'].items()]},
        'parameters': [{'name': n, 'default': v, 'description': '冻结模型标识或默认年龄门限'}
                       for n, v in item.get('parameters', {}).items()],
        'clock': {'domains': 'source100MHz, HDMI75MHz; actual template PLL.v C0/C4'},
        'reset': {'assertion': 'common i_rstn low asynchronously cancels both domains',
                  'release': 'two locally clocked release registers per domain; no single-domain hot reset proof'},
        'behavior': ([
            '100000 source clocks per ms; epoch/time frozen before request toggle until synchronized ack.',
            'Two destination request synchronizers, one stable capture wait; capture then ack.',
            'Time channel independent of table pending/copy backpressure.',
            'No time_valid before first new snapshot; >150000 destination clocks without update invalidates.',
            'Physical CDC/bundled-data checks pending; clocks must be active for digital latency bound.'
        ] if key == 'time' else [
            'Sequential entry valid/ready loads sole source table; seal count equals accepted entry count.',
            'Source metadata265 and source97x64 remain frozen until last copy acknowledgement.',
            'Two destination97x64 banks rotate pending/active at SOF; no fourth table.',
            'copy_enable backpressure holds cursor; count0 becomes a complete empty pending table.',
            'Final copy concurrent SOF never bypasses pending completeness; active entries immutable within display frame.',
            'Draw only valid time, matching epoch/model, status0, legal count and capture<=completion<=now.',
            'Age upper bound now-capture+4ms; default500; independent2000 instance is not deployment approval.',
            'No active table, invalid/lost time, epoch mismatch or illegal timestamp order reports UINT64_MAX unknown age, never zero freshness; overflow saturates.',
            'Local source abort discards only unsealed load; published transaction waits for ack or common reset.'
        ]),
        'constraints': ['No production, arithmetic, TD, timing exceptions, bitstream, board or Flash changes.',
                        'RAM and metadata/time bundled-data physical constraints remain unsigned-off.'],
        'corner_cases': ['zero/full count, pending full, reset, stale identity, future time, time loss'],
        'verification_cases': ['dual clocks; all copy positions reset; backpressure; counts0/1/32/33/64; age500/2000; time watchdog'],
        'timing_diagrams': [{'id': 'held_transfer', 'title': '冻结载荷与完整复制发布', 'scenario': 'normal',
                             'description': 'Rising-edge digital illustration; source payload must remain physically stable until ack.',
                             'wavejson': {'signal': timing}}]
    }
    spec_path = run.ROOT / 'specifications' / (name + '.json')
    run.save(spec_path, {'modules': [module]})
    output = run.ROOT / 'specifications' / ('source' if '--source' in sys.argv else 'proposal')
    entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.workflow.cli',run_name='__main__')"
    args = [sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', str(spec_path),
            '--out-dir', str(output), '--language', 'zh']
    if '--source' in sys.argv:
        args += ['--source', str(run.ROOT / 'rtl' / (name + '.v'))]
    work = run.fresh('spec_' + name + ('_source' if '--source' in sys.argv else '_proposal'))
    run.command(args, run.ROOT, str(work.relative_to(run.ROOT) / 'render'))
run.check()
