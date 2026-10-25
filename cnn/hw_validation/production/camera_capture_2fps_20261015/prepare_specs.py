"""Render confirmed component contracts, never infer them from generated RTL."""
import json
import sys
from pathlib import Path
import run

ROOT = Path(__file__).resolve().parent
contract = json.loads((ROOT / 'interfaces.json').read_text(encoding='utf-8'))
for key in ('scaler', 'slots'):
    item = contract[key]
    name = item['module']
    module = {
        'name': name, 'feature': 'camera_capture', 'rtl_path': name + '.v',
        'description': '精确2/5面积缩放' if key == 'scaler' else '完整输入帧双槽生命周期控制',
        'interfaces': {'ports': [dict(name=n, direction='input' if n.startswith('i_') else 'output',
                                     width=w, role=n, description=n)
                                 for n, w in item['ports'].items()]},
        'clock': {'domains': 'single i_clk domain; no CDC supplied'},
        'reset': {'assertion': 'i_rstn low asynchronously cancels state and transactions',
                  'release': 'caller supplies locally synchronized release; external DDR drain is not implemented'},
        'behavior': ([
            'AWB96 high lane first; each lane R[23:16], G[15:8], B[7:0].',
            '1280x720 to 512x288; horizontal 11-bit and vertical 13-bit; round once after /25.',
            '128 record queue; each record contains one or two horizontal sums; worker emits at most one pixel per cycle.',
            'Ordinary fixture: 320 active beats plus 480 gap clocks per row; overflow cancels frame.',
            'Output low byte R,G,B; mask01; SOF first pixel, EOL each 512th, EOF final pixel.',
            'No camera backpressure; short/long row, reentrant SOF, overflow or reset flush partial frame.'
        ] if key == 'scaler' else [
            'FREE -> CAPTURING -> WAIT_VISIBLE -> READY -> READING -> FREE.',
            'SOF allocates only pre-edge FREE, slot0 first; no free means whole frame skipped.',
            '442368-byte successful end is not READY until external matching write_visible.',
            'Matching same-edge full capture_end and write_visible may publish.',
            'Claim consumes pre-edge READY only; release consumes matched pre-edge READING only.',
            'Malformed capture quarantines its slot until reset; another slot remains independent.',
            'SOF during active capture quarantines old capture and skips new; independent other-slot events still apply.',
            'External visibility and last-read facts are controlled TB events, not physical DDR proof.'
        ]),
        'constraints': ['Do not modify production, arithmetic, timing exceptions or real peripheral protocol.',
                        'No physical mapping, bitstream, board or real DDR visibility claim.'],
        'corner_cases': ['reset, simultaneous events, partial input, stale events, overload'],
        'verification_cases': ['three complete pixelwise frames and malformed frame tests' if key == 'scaler'
                               else 'double-slot lifecycle, same-edge end/visible, stale identity, quarantine, release'],
        'timing_diagrams': ([{
            'id': 'horizontal_records', 'title': '五拍水平相位与变长记录', 'scenario': 'record_flow',
            'description': 'Each valid AWB96 beat creates one record. Vertical worker drains one pixel per clock; final pipeline latency is measured separately.',
            'wavejson': {'signal': [
                {'name': 'clk', 'wave': 'p......'},
                {'name': 'input_valid', 'wave': '01....0'},
                {'name': 'phase', 'wave': '=======', 'data': ['0','0','4','3','2','1','0']},
                {'name': 'record_pixels', 'wave': '=======', 'data': ['0','1','2','1','2','2','0']}
            ]}
        }] if key == 'scaler' else [{
            'id': 'visible_boundary', 'title': '整帧结束不等于写入可见', 'scenario': 'normal',
            'description': 'Events sampled at rising edges; one illustrated wait is not a real DDR latency guarantee.',
            'wavejson': {'signal': [
                {'name': 'clk', 'wave': 'p.........'},
                {'name': 'SOF', 'wave': '010.......'},
                {'name': 'capture_end', 'wave': '0..10.....'},
                {'name': 'write_visible', 'wave': '0.....10..'},
                {'name': 'claim', 'wave': '0.......10'},
                {'name': 'state_after_edge', 'wave': '==..=..=.=','data': ['FREE','CAPTURING','WAIT_VISIBLE','READY','READING']}
            ]}
        }])
    }
    out = ROOT / 'specifications' / (name + '.json')
    run.save(out, {'modules': [module]})
    entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.workflow.cli',run_name='__main__')"
    argv = [sys.executable, '-B', '-X', 'utf8', '-c', entry, 'write-spec',
            '--spec', str(out), '--out-dir', str(ROOT / 'specifications' / ('source' if '--source' in sys.argv else 'proposal')),
            '--language', 'zh']
    if '--source' in sys.argv:
        argv += ['--source', str(ROOT / 'rtl' / (name + '.v'))]
    work = run.fresh('spec_' + name + ('_source' if '--source' in sys.argv else '_proposal'))
    run.command(argv, ROOT, str(work.relative_to(ROOT) / 'render'))
