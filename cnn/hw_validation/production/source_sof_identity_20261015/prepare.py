"""Freeze dependencies and render confirmed interfaces before new RTL."""
import json
import sys
import run

contract = json.loads((run.ROOT / 'interfaces.json').read_text(encoding='utf-8'))
if not (run.ROOT / 'frozen.json').exists():
    paths = [run.BASE / 'artifact_hashes.json', run.PROJECT / 'cnn/template/source_manifest.json',
             run.PROJECT / 'cnn/template/design_top_wrapper.v',
             run.PROJECT / 'user_source/hdl_source/isp/isp_top.v',
             run.PROJECT / 'user_source/hdl_source/awb.v',
             run.PROJECT / 'user_source/ip_source/PLL/PLL.v',
             run.PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015/第六批任务_共享计算与结果发布接入_20261015.txt',
             run.PROJECT / 'cnn/hw_validation/production/camera_capture_2fps_20261015/artifact_hashes.json']
    paths += list((run.BASE / 'rtl').glob('*.v'))
    paths += list((run.ROOT.parent / 'camera_capture_2fps_20261015/rtl').glob('*.v'))
    run.save(run.ROOT / 'frozen.json', {str(p): run.sha(p) for p in paths})
    run.save(run.ROOT / 'reused_sources.json', {})
run.check()
for directory in (run.BASE, run.ROOT.parent / 'camera_capture_2fps_20261015'):
    baseline = json.loads((directory / 'artifact_hashes.json').read_text(encoding='utf-8'))
    changed = [name for name, digest in baseline.items() if run.sha(directory / name) != digest]
    run.save(run.ROOT / (directory.name + '_guard.json'), {'checked': len(baseline), 'changed': changed})
    assert not changed, changed
for key in ('identity', 'overlay'):
    item = contract[key]
    name = item['module']
    behavior = (contract['admission'] + contract['cdc']) if key == 'identity' else contract['overlay_contract']
    signals = ([{'name': 'camera_clk', 'wave': 'p.........'},
                {'name': 'mirror_valid', 'wave': '0..1......'},
                {'name': 'physical_sof', 'wave': '010.10..10'},
                {'name': 'frame_count', 'wave': '===.===.==', 'data': ['0','1 skipped','2 admitted','2','2','3 skipped']},
                {'name': 'admit', 'wave': '0...10....'},
                {'name': 'held_event', 'wave': 'x...=.....', 'data': ['epoch,frame2,old time']},
                {'name': 'event_busy', 'wave': '0...1.....'}]
               if key == 'identity' else
               [{'name': 'pixel_clk', 'wave': 'p.......'},
                {'name': 'sof_blank', 'wave': '010.....'},
                {'name': 'table_age', 'wave': '=.=.....', 'data': ['old','new']},
                {'name': 'text_latch', 'wave': '0.10....'},
                {'name': 'live_draw', 'wave': '1....0..'},
                {'name': 'draw_permit', 'wave': '1....0..'}])
    spec = {'modules': [{
        'name': name, 'feature': 'source_sof_identity', 'rtl_path': name + '.v',
        'description': '真实AWB源帧身份与单计时器镜像' if key == 'identity' else '复用固定字形的结果年龄文字',
        'interfaces': {'ports': [dict(name=n, direction='input' if n.startswith('i_') else 'output',
                                     width=w, role=n, description=n) for n, w in item['ports'].items()]},
        'parameters': [dict(name=n, default=v, description='已配置摄像头域两毫秒失联计数，不是绝对计时器')
                       for n, v in item.get('parameters', {}).items()],
        'clock': contract['clock_contract'],
        'reset': {'assertion': 'common asynchronous cancellation',
                  'release': 'identity two local release edges; overlay uses supplied pixel-domain released reset'},
        'behavior': behavior, 'constraints': contract['boundaries'],
        'corner_cases': ['SOF during reset, no time, busy, no credit, long stall, common reset, unknown age'],
        'verification_cases': ['Python reference first', 'actual local ModelSim', 'strict eight gates kept separate'],
        'timing_diagrams': [{'id': 'source_frame', 'title': '源帧接纳或帧边界年龄切换', 'scenario': 'normal',
                             'description': 'Digital waveform only; no physical CDC signoff.', 'wavejson': {'signal': signals}}]
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
