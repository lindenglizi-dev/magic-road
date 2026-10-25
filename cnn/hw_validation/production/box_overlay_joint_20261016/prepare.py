"""Freeze actual reuse closure and render the two confirmed video interfaces."""
import json
import sys
import run

contract = json.loads((run.ROOT / 'interfaces.json').read_text(encoding='utf-8'))
publisher = run.ROOT.parent / 'result_publish_joint_20261015'
vendor = publisher / 'vendor_rom'
dram = __import__('pathlib').Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_dram.v')
if not (run.ROOT / 'frozen.json').exists():
    paths = [run.BASE / 'artifact_hashes.json', run.BASE / 'interfaces.json',
             run.PROJECT / 'cnn/template/design_top_wrapper.v',
             run.PROJECT / 'cnn/template/source_manifest.json',
             run.PROJECT / 'user_source/hdl_source/hdmi_mixer.v',
             publisher / 'frozen_dependencies.json', publisher / 'handoff.txt',
             publisher / 'verification/tb_road_result_publish_joint.v',
             publisher / 'verification/run_vendor_rom.ps1', dram]
    paths += list((run.BASE / 'rtl').glob('*.v'))
    paths += list((publisher / 'rtl').glob('*.v'))
    paths += [p for p in vendor.rglob('*') if p.is_file()]
    core = run.ROOT.parent / 'reports/board_selftest_20261010/core'
    paths += [core / name for name in ('road_mac_probe.v', 'road_dynamic_postprocess.v',
                                      'road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v')]
    run.save(run.ROOT / 'frozen.json', {str(p): run.sha(p) for p in paths})
    run.save(run.ROOT / 'reused_sources.json', {})
run.check()
old = json.loads((run.BASE / 'artifact_hashes.json').read_text(encoding='utf-8'))
changed = [name for name, digest in old.items() if run.sha(run.BASE / name) != digest]
run.save(run.ROOT / 'source_identity_guard.json', {'checked': len(old), 'changed': changed})
assert not changed
receipt = json.loads((publisher / 'frozen_dependencies.json').read_text(encoding='utf-8'))
changes = [p for item in receipt['files'] for p in (item['source'], item['copy']) if run.sha(p) != item['sha256']]
run.save(run.ROOT / 'publisher_guard.json', {'records': len(receipt['files']), 'changed': changes})
assert not changes
for key in ('renderer', 'combined'):
    item = contract[key]
    name = item['module']
    signals = [
        {'name': 'pixel_clk', 'wave': 'p.........'},
        {'name': 'DE', 'wave': '10.......1'},
        {'name': 'phase', 'wave': '==========', 'data': ['flush','wait','fetch','read0','write0','read1','write1','next','ready','paint']},
        {'name': 'RAM_WE', 'wave': '10..1010..'},
        {'name': 'line_ready', 'wave': '0.......1.'},
        {'name': 'live_draw', 'wave': '1........0'}]
    spec = {'modules': [{
        'name': name, 'feature': 'box_overlay_joint', 'rtl_path': name + '.v',
        'description': '五拍串行准备的64框行端点事件图' if key == 'renderer' else '固定两拍视频延迟的64框与既有AGE叠加',
        'interfaces': {'ports': [dict(name=n, direction='input' if n.startswith('i_') else 'output',
                                     width=w, role=n, description=n) for n, w in item['ports'].items()]},
        'clock': {'domain': '75MHz HDMI pixel', 'timing': contract['timing']},
        'reset': {'assertion': 'common low reset cancels local line-valid immediately',
                  'release': 'supplied pixel-domain synchronous-release reset; explicit1280-address clear before paint'},
        'behavior': contract['geometry'] + (contract['line_events'] if key == 'renderer' else contract['age_and_live_gating']),
        'constraints': contract['boundaries'] + [str(contract['resource_intent'])],
        'corner_cases': ['0/1/32/33/64,overlap,tiny/right/bottom edges,late preparation,reset,map clear,age2000/invalid'],
        'verification_cases': ['Python complete-frame pixels', 'actual vendor distributedRAM', 'real C9 ROM/postprocess/publisher/table chain'],
        'timing_diagrams': [{'id': 'line_prepare', 'title': '行消隐准备与连续像素输出', 'scenario': 'normal',
                             'description': 'Five cycles per entry, no same-address consumed read/write; physical timing unverified.',
                             'wavejson': {'signal': signals}}]
    }]}
    path = run.ROOT / 'specifications' / (name + '.json')
    run.save(path, spec)
    output = run.ROOT / 'specifications' / ('source' if '--source' in sys.argv else 'proposal')
    entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.workflow.cli',run_name='__main__')"
    args = [sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec', '--spec', str(path),
            '--out-dir', str(output), '--language', 'zh']
    if '--source' in sys.argv:
        args += ['--source', str(run.ROOT / 'rtl' / (name + '.v'))]
    work = run.fresh('spec_' + key + ('_source' if '--source' in sys.argv else '_proposal'))
    run.command(args, run.ROOT, str(work.relative_to(run.ROOT) / 'render'))
run.check()
