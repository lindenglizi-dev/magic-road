"""在工程根目录运行：python sim/run_rotation_checks.py [--full]。"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--full',action='store_true',help='包含耗时较长的8帧RGB整链路检查')
args=parser.parse_args()
output=root/'reports/rotation_checks'
output.mkdir(parents=True,exist_ok=True)
iverilog=shutil.which('iverilog') or 'E:/project/qiansai/.tools/iverilog/bin/iverilog.exe'
vvp=shutil.which('vvp') or str(Path(iverilog).with_name('vvp.exe'))
tops=['numeric','capture','image','faults','queue']+(['runtime'] if args.full else [])
sources=[str(p) for p in (root/'rtl').glob('*.v')]
for kind in tops:
    name='tb_ball_rotation_'+kind
    image=output/(kind+'.vvp')
    for phase,command in [('compile',[iverilog,'-g2001','-Wall','-s',name,'-o',str(image),str(root/'sim'/(name+'.v')),*sources]),('simulation',[vvp,str(image)])]:
        result=subprocess.run(command,cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (output/(kind+'_'+phase+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
        if result.returncode:
            print(result.stdout,result.stderr);result.check_returncode()
        print(kind,phase,'PASS',flush=True)
if args.full:
    sys.path.insert(0,str(root/'python_sim'))
    import rotation_rtl_model as model
    model.CLOCK_HZ=25_000_000
    meter=model.FixedMeter()
    phases=json.loads((root/'sim/rotation_expected_phases.json').read_text(encoding='utf-8'))
    rows=(root/'reports/runtime_rotation_trace.txt').read_text().splitlines()
    assert len(rows)==7
    states={'WAIT MARKER':0,'ACQUIRE':1,'WARMUP':2,'CW':3,'CCW':4,'STOP':5,'MARKER LOST':6}
    for index,row in enumerate(rows):
        values=row.split()
        frame,epoch,tick,valid=map(int,values[:4]);phase=int(values[4],16)
        assert frame==index and epoch==int(frame>=5)
        expected=None if frame in (0,5) else phases[frame]
        if int(values[13]):meter.reset()
        assert valid==int(expected is not None)
        if valid:assert phase==expected
        meter.update(expected,tick)
        assert int(values[5])==int(meter.rpm_x10 is not None)
        if meter.rpm_x10 is not None:assert int(values[6],16)==meter.rpm_x10&0xffffff
        assert int(values[7])==states[meter.state]
        assert int(values[8],16)==meter.net_phase&((1<<48)-1)
        assert tuple(map(int,values[9:12]))==(meter.cw,meter.ccw,int(meter.partial))
    print('RGB full-chain Python integer comparison PASS',flush=True)
(output/'summary.json').write_text(json.dumps({'passed':tops,'runtime_python_comparison':args.full,'bitstream_generated':False},indent=2),encoding='utf-8')
