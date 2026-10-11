"""Add measurement only; preserve the first passing TB and its logs."""
import json
import shutil
from execute import HERE,MSIM,CORE,MODEL,run,check,sha,write

check()
p=HERE/'layer';d=p/'phases';d.mkdir()
shutil.copytree(p/'vectors',d/'vectors')
run([MSIM/'vlib.exe','work'],d,'vlib.log')
sources=[p/'rtl/down2_dynamic_tile_runner.v',p/'rtl/road_down2_dynamic_adapter.v',p/'rtl/road_mac_probe.v',
         *[HERE/'hardware'/n for n in CORE],HERE/'model'/MODEL,p/'tb_down2_dynamic_tile_phases.v']
run([MSIM/'vlog.exe','-work','work',*sources],d,'vlog.log')
run([MSIM/'vsim.exe','-c','-lib','work','tb_down2_dynamic_tile_phases','-do',
     'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],d,'simulation.log')
log=(d/'simulation.log').read_text()
assert 'TB_PASS_DOWN2_DYNAMIC_TILE' in log and 'Fatal:' not in log and '** Error:' not in log
write(d/'receipt.json',{'status':'SAME_RTL_MEASUREMENT_ONLY_PASS',
      'sources':{str(x):sha(x) for x in sources},
      'classification':'Mutually exclusive priority occupancy; does not mean isolated operator latency'})
check()
print('\n'.join(x for x in log.splitlines() if 'PASS' in x or 'LAYER_SPLIT' in x))
