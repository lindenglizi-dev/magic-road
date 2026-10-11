"""Verilog-2001 regression of actual MAC -> DW cache -> PW -> dynamic core."""
import json
import shutil
from pathlib import Path
from execute import HERE,CORE,MODEL,MSIM,check,run,sha,write

check()
d=HERE/'layer'
assert all(sha(Path(p))==h for p,h in json.loads((HERE/'layer_inputs.json').read_text()).items())
for p in (d/'vectors').glob('*_records.json'):
    values=[v for row in json.loads(p.read_text()) for v in (row['pre'],row['silu'],row['post'])]
    with p.with_name(p.name.replace('_records.json','_stages.hex')).open('x',encoding='ascii') as f:
        f.write(''.join(f'{v&0xffffffff:08x}\n' for v in values))
run([MSIM/'vlib.exe','work'],d,'vlib.log')
sources=[d/'rtl/down2_dynamic_tile_runner.v',d/'rtl/road_down2_dynamic_adapter.v',d/'rtl/road_mac_probe.v',
         *[HERE/'hardware'/n for n in CORE],HERE/'model'/MODEL,d/'tb_down2_dynamic_tile.v']
run([MSIM/'vlog.exe','-work','work',*sources],d,'vlog.log')
run([MSIM/'vsim.exe','-c','-lib','work','tb_down2_dynamic_tile','-do',
     'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'],d,'simulation.log')
log=(d/'simulation.log').read_text()
assert 'TB_PASS_DOWN2_DYNAMIC_TILE' in log and '** Error:' not in log and 'Fatal:' not in log
assert all(sha(Path(p))==h for p,h in json.loads((HERE/'layer_inputs.json').read_text()).items())
write(d/'receipt.json',{'status':'TEST_PACKAGE_TILE_FUNCTION_PASS_NOT_PHYSICAL',
      'sources':{str(p):sha(p) for p in sources},'dynamic_arithmetic_core_unchanged':True,
      'parameters':'frozen TEST-package constants in adapter; not real QAT or cost of runtime loader',
      'legacy_stage_counters_valid':False,'actual_tb_state_classification':'layer_cycles.csv'})
check()
print('\n'.join(x for x in log.splitlines() if 'PASS' in x))
